"""Kit startup helper for CC stages explicitly opting into session authoring.

Run with Kit --exec, or execute this file in Kit's Script Editor. No layer is
saved. Locks are applied once on open; the user can deliberately unlock later.
"""

import asyncio
import builtins

import carb
import carb.settings
import omni.kit.app
import omni.kit.usd.layers as kit_layers
import omni.usd


class SessionDefaults:
    def __init__(self):
        self.context = omni.usd.get_context()
        self.task = None
        self.permissions = []
        self.ui_settings = {}
        self.subscription = self.context.get_stage_event_stream().create_subscription_to_pop(
            self.on_stage_event, name="CC session authoring defaults")
        self.schedule()

    def restore(self):
        for layer, editable in self.permissions:
            layer.SetPermissionToEdit(editable)
        self.permissions.clear()
        settings = carb.settings.get_settings()
        for key, value in self.ui_settings.items():
            if value is None:
                settings.destroy_item(key)
            else:
                settings.set(key, value)
        self.ui_settings.clear()

    def stop(self):
        if self.task and not self.task.done():
            self.task.cancel()
        self.subscription = None
        self.restore()

    def on_stage_event(self, event):
        if event.type == int(omni.usd.StageEventType.CLOSING):
            if self.task and not self.task.done():
                self.task.cancel()
            self.restore()
        elif event.type == int(omni.usd.StageEventType.OPENED):
            self.schedule()

    def schedule(self):
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
        if not stage or stage.GetRootLayer().customLayerData.get("cc:defaultAuthoring") != "session":
            return
        # Let the Layers panel finish restoring its saved UI state first.
        for _ in range(3):
            await omni.kit.app.get_app().next_update_async()
        if self.context.get_stage() != stage:
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
        if stage.GetRootLayer().customLayerData.get("cc:lockPersistentLayers", False):
            for layer in stage.GetUsedLayers():
                if layer.anonymous:
                    continue
                self.permissions.append((layer, layer.permissionToEdit))
                # Includes the root, which Kit's normal layer-lock helper excludes.
                layer.SetPermissionToEdit(False)
        stage.SetEditTarget(session)
        carb.log_info(f"CC: Session Layer selected; {len(self.permissions)} persistent layers protected.")

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
    previous.stop()
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
