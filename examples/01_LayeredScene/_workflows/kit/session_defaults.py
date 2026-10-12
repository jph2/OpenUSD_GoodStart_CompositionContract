"""Kit startup helper for CC stages opting into declared Opinion/session authoring.

Run with Kit --exec, or execute this file in Kit's Script Editor. No layer is
saved. Locks are applied once on open; the user can deliberately unlock later.
The active root stays writable for Kit's camera and authoring-target settings.
"""

import asyncio
import builtins

import carb
import carb.settings
import omni.kit.app
import omni.kit.usd.layers as kit_layers
import omni.usd
from pxr import Sdf


def restore_state(owner):
    """Restore surviving layer instances; never reopen an expired layer.

    Used directly when replacing an older in-memory helper, whose own restore()
    may still call SetPermissionToEdit on invalid Sdf handles.
    """
    permissions, owner.permissions = getattr(owner, "permissions", []), []
    ui_settings, owner.ui_settings = getattr(owner, "ui_settings", {}), {}
    expired = 0
    for record in permissions:
        identifier = "<legacy layer handle>"
        try:
            if len(record) == 2:
                # Compatibility with helpers started before this lifecycle fix.
                original, editable = record
                if not original:
                    expired += 1
                    continue
                identifier = original.identifier
            else:
                identifier, original, editable = record
            if not original:
                expired += 1
                continue
            # Find only consults the loaded-layer registry. FindOrOpen would
            # load old scenes and could apply stale state to a new instance.
            layer = Sdf.Find(identifier)
            if not layer or layer != original:
                expired += 1
                continue
            layer.SetPermissionToEdit(bool(editable))
        except Exception as error:
            # Boost.Python/Tf errors differ by build. Isolate each record so a
            # failed/expired handle cannot prevent other layers/UI restoration.
            carb.log_warn(f"CC cleanup: could not restore layer permission for {identifier}: {error}")
    if expired:
        carb.log_info(f"CC cleanup: skipped {expired} expired or replaced layer handle(s).")
    settings = carb.settings.get_settings()
    for key, value in ui_settings.items():
        try:
            if value is None:
                settings.destroy_item(key)
            else:
                settings.set(key, value)
        except Exception as error:
            carb.log_warn(f"CC cleanup: could not restore setting {key}: {error}")


def stop_helper(owner):
    """Use current cleanup code even when owner was made by an older script."""
    owner.stopped = True
    task = getattr(owner, "task", None)
    if task and not task.done():
        task.cancel()
    owner.task = None
    owner.subscription = None
    restore_state(owner)


class SessionDefaults:
    def __init__(self):
        self.context = omni.usd.get_context()
        self.task = None
        self.permissions = []
        self.ui_settings = {}
        self.stopped = False
        self.subscription = self.context.get_stage_event_stream().create_subscription_to_pop(
            self.on_stage_event, name="CC session authoring defaults")
        self.schedule()

    def restore(self):
        restore_state(self)

    def remember_permission(self, layer):
        # Capture the identifier while valid, plus instance identity. A later
        # layer with the same filename must not inherit this restoration record.
        self.permissions.append((layer.identifier, layer, bool(layer.permissionToEdit)))

    def stop(self):
        stop_helper(self)

    def on_stage_event(self, event):
        if self.stopped:
            return
        if event.type == int(omni.usd.StageEventType.CLOSING):
            if self.task and not self.task.done():
                self.task.cancel()
            self.restore()
        elif event.type == int(omni.usd.StageEventType.OPENED):
            self.schedule()

    def schedule(self):
        if self.stopped:
            return
        if self.task and not self.task.done():
            self.task.cancel()
        self.task = asyncio.ensure_future(self.apply())
        self.task.add_done_callback(self.report_error)

    @staticmethod
    def report_error(task):
        if not task.cancelled() and task.exception():
            carb.log_error(f"CC session defaults failed: {task.exception()}")

    async def apply(self):
        stage = self.context.get_stage()
        if not stage:
            return
        policy = stage.GetRootLayer().customLayerData.get("cc:defaultAuthoring")
        if policy not in ("session", "opinion"):
            return
        # Let the Layers panel finish restoring its saved UI state first.
        for _ in range(3):
            await omni.kit.app.get_app().next_update_async()
        if self.stopped or self.context.get_stage() != stage:
            return
        self.restore()
        settings = carb.settings.get_settings()
        for key, value in {
            "/persistent/app/layerwindow/showSessionLayer": True,
            "/persistent/app/layerwindow/enableAutoAuthoringMode": False,
            "/persistent/app/layerwindow/enableSpecLinkingMode": False,
        }.items():
            self.ui_settings[key] = settings.get(key)
            settings.set(key, value)
        kit_layers.get_layers(self.context).set_edit_mode(kit_layers.LayerEditMode.NORMAL)
        session = stage.GetSessionLayer()
        stage.SetEditTarget(session)
        target = session
        if policy == "opinion":
            path = stage.GetRootLayer().customLayerData.get("cc:opinionLayer", "")
            target = Sdf.Layer.FindRelativeToLayer(stage.GetRootLayer(), path) if path else None
            if target is None or target not in stage.GetLayerStack():
                raise RuntimeError("Declared Opinion layer is unavailable in the local stack; Session retained.")
        if stage.GetRootLayer().customLayerData.get("cc:lockPersistentLayers", False):
            root = stage.GetRootLayer()
            self.remember_permission(root)
            # Kit writes cameraSettings and omni_layer authoring metadata here
            # during SETTINGS_SAVING. Sdf's edit permission covers the entire
            # layer, so hard-locking the root also breaks those host operations.
            root.SetPermissionToEdit(True)
            for layer in stage.GetUsedLayers():
                if layer.anonymous or layer == target or layer == root:
                    continue
                self.remember_permission(layer)
                layer.SetPermissionToEdit(False)
        if target != session:
            self.remember_permission(target)
            self.unlock(target.identifier)
        # Use Kit's own edit-target path, as used by its Layers panel utilities.
        omni.usd.set_edit_target_by_identifier(stage, target.identifier)
        if stage.GetEditTarget().GetLayer() != target:
            raise RuntimeError(f"Kit could not select authoring layer: {target.identifier}")
        carb.log_info(f"CC: {target.identifier} selected; persistent work/source layers protected; root writable for Kit settings.")

    def unlock(self, layer_identifier):
        """Explicit persistent-authoring escape hatch; never selects or saves a layer."""
        stage = self.context.get_stage()
        if not stage:
            raise RuntimeError("No stage is open.")
        layer = next((item for item in stage.GetUsedLayers() if item.identifier == layer_identifier), None)
        if layer is None:
            raise ValueError("Layer is not used by the current stage.")
        root = stage.GetRootLayer()
        if layer != root:
            editable = root.permissionToEdit
            root.SetPermissionToEdit(True)
            try:
                kit_layers.get_layers(self.context).get_layers_state().set_layer_lock_state(layer.identifier, False)
            finally:
                root.SetPermissionToEdit(editable)
        layer.SetPermissionToEdit(True)


previous = getattr(builtins, "cc_session_defaults", None)
if previous:
    stop_helper(previous)
builtins.cc_session_defaults = SessionDefaults()


async def open_requested_stage():
    settings = carb.settings.get_settings()
    path = settings.get("/cc/sessionDefaults/stage")
    if path:
        settings.destroy_item("/cc/sessionDefaults/stage")
        success, error = await omni.usd.get_context().open_stage_async(path)
        if not success:
            raise RuntimeError(f"Could not open CC stage: {error}")


_open_task = asyncio.ensure_future(open_requested_stage())
_open_task.add_done_callback(SessionDefaults.report_error)
