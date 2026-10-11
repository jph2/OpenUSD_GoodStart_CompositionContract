"""Opt-in Kit bootstrap: visible controls + JSON-driven point-instancer preview.

Run through Open_In_Kit.ps1 -Scene MotionGraphics, or runpy.run_path() in Kit.
No extension installation, autoplay, disk USD writes or user edit-target changes
by the motion controller. builtins.cc_motion_graphics.stop() removes the preview.
"""
import asyncio
import builtins
import hashlib
from pathlib import Path
import runpy
import time
from types import ModuleType

import carb
import carb.settings
import omni.kit.app
import omni.timeline
import omni.usd
from pxr import Sdf, Usd, UsdGeom


_settings = carb.settings.get_settings()
_script_path = _settings.get('/cc/motion/script') or globals().get('__file__')
if not _script_path:
    raise RuntimeError('Use the MotionGraphics launcher or runpy.run_path with this script\'s full path.')
_settings.destroy_item('/cc/motion/script')
_folder = Path(_script_path).resolve().parent


def load_local_source(name, path):
    """Reload these trusted package scripts without Kit's importer/stat/pyc cache.

    Only the fixed package paths below use this loader. JSON remains data. No global
    import hooks, sys.modules entries or host caches are changed.
    """
    path = path.resolve()
    source = path.read_bytes()
    module = ModuleType(name)
    module.__file__ = str(path)
    module.__package__ = ''
    exec(compile(source, str(path), 'exec'), module.__dict__)
    carb.log_info(f'CC motion: loaded current source {path} (sha256 {hashlib.sha256(source).hexdigest()[:12]}).')
    return module


model = load_local_source('cc_motion_model', _folder.parent / 'motion_graphics_core.py')
_required = ('control_hints', 'default_document', 'validate', 'read_snapshot',
             'parse_document', 'save_controls', 'evaluate', 'usd_values')
_missing = [name for name in _required if not callable(getattr(model, name, None))]
_missing += [name for name in ('CHOICES', 'NUMBERS', 'PROFILE', 'CONTROL_PRIM', 'CLONER')
             if not hasattr(model, name)]
if _missing:
    raise RuntimeError(f'Motion control files are incompatible: {model.__file__} is missing {_missing}. '
                       'Update the whole _workflows folder together, then rerun this bootstrap.')
panel_module = load_local_source('cc_motion_panel', _folder / 'motion_graphics_panel.py')
diagnostics = load_local_source('cc_motion_diagnostics', _folder / 'diagnose_motion_graphics.py')


def notify(text, warning=False):
    """Optional host toast; logging remains available in minimal Kit apps."""
    try:
        import omni.kit.notification_manager as notifications
        notifications.post_notification(text, duration=8,
            status=notifications.NotificationStatus.WARNING if warning else notifications.NotificationStatus.INFO)
    except (ImportError, RuntimeError) as error:
        carb.log_info(f'CC motion notification unavailable: {error}')


class MotionGraphics:
    def __init__(self):
        self.context = omni.usd.get_context()
        self.timeline = self.context.get_timeline()
        self.timeline_name = self.context.get_timeline_name()
        self.timeline_restore = []
        self.partition_restore = None
        self.stage = None
        self.overlay = None
        self.sample_times = set()
        self.diagnostic_task = None
        self.watcher = None
        self.controls = None
        self.digest = None
        self.last_frame = None
        self.closing_stage = None
        self.reported = None
        self.path = None
        self.stopped = False
        self.operations = set()
        self.frame_count = 0
        self.last_health = 0.0
        self.last_clock = None
        self.clock_changed_at = time.monotonic()
        self.health_key = None
        self.play_requested_at = None
        self.play_error = None
        self.panel = panel_module.MotionControlsPanel(self, model)
        carb.log_info('CC motion: Motion Graphics Controls panel opened. Change values, Apply & Save JSON, then Play.')
        self.subscription = self.context.get_stage_event_stream().create_subscription_to_pop(
            self.on_stage_event, name='CC motion graphics lifecycle')
        self.task = asyncio.ensure_future(self.run())
        self.task.add_done_callback(self.finished)

    def finished(self, task):
        if task is not self.task:
            return
        error = None if task.cancelled() else task.exception()
        if error:
            carb.log_error(f'CC motion stopped: {error}')
            notify(f'Live motion stopped: {error}', warning=True)
        self.detach()
        if error and not self.stopped:
            self.panel.set_status(f'CONTROLLER STOPPED: {error}\nCorrect the problem and rerun the bootstrap.', error=True)
            self.panel.set_runtime('CONTROLLER STOPPED — see error below. Correct it, then Reconnect.', error=True)

    def watcher_finished(self, task):
        if task is not self.watcher:
            return
        if not task.cancelled() and task.exception():
            carb.log_error(f'CC motion JSON watcher stopped: {task.exception()}')
            notify(f'JSON watcher stopped: {task.exception()}', warning=True)
            if not self.stopped:
                self.panel.set_status(f'JSON WATCHER STOPPED: {task.exception()}', error=True)

    def on_stage_event(self, event):
        if event.type == int(omni.usd.StageEventType.CLOSING):
            self.closing_stage = self.context.get_stage()
            self.detach()
        elif event.type == int(omni.usd.StageEventType.OPENED):
            self.closing_stage = None

    def stop(self):
        if self.stopped:
            return
        self.stopped = True
        self.task.cancel()
        self.subscription = None
        self.detach()
        self.panel.destroy()

    def show_panel(self):
        self.panel.window.visible = True
        self.panel.window.focus()

    def play(self):
        """Explicit callback, bound to the USD context's actual timeline."""
        carb.log_info('CC motion: Play clicked.')
        self.play_error = None
        try:
            if self.stopped or self.task.done():
                raise RuntimeError('Controller is stopped. Click Reconnect first.')
            if self.context.get_stage() != self.stage or not self.path:
                raise RuntimeError('No connected MotionGraphics scene. Open it, then click Reconnect.')
            if self.controls is None:
                raise RuntimeError('No valid controls loaded. Resolve the JSON error or use the preset and Apply & Save.')
            self.timeline = self.context.get_timeline()
            self.timeline_name = self.context.get_timeline_name()
            if self.timeline.get_director() is not None:
                raise RuntimeError('Another timeline is directing this context; its director must control playback.')
            start, end = self.stage.GetStartTimeCode(), self.stage.GetEndTimeCode()
            if end <= start:
                raise RuntimeError(f'Current stage playback range is empty: {start} to {end}.')
            if not self.timeline.is_auto_updating():
                self.timeline_restore.append((self.timeline, False))
                self.timeline.set_auto_update(True)
                carb.log_info('CC motion: enabled automatic timeline advancement for Play; restored on disconnect.')
            self.timeline.play(start_timecode=start, end_timecode=end, looping=True)
            self.start_diagnostic()
            self.play_requested_at = time.monotonic()
            self.clock_changed_at = self.play_requested_at
            self.last_health = 0.0
            self.panel.set_runtime('PLAY REQUESTED — waiting for timeline advancement...')
            carb.log_info(f'CC motion: Play requested on context timeline {self.timeline_name!r}; frames {start}..{end}.')
        except Exception as error:
            self.play_error = str(error)
            self.panel.set_runtime(f'PLAY BLOCKED — {error}', error=True)
            carb.log_error(f'CC motion: Play blocked: {error}')

    def pause(self):
        try:
            self.context.get_timeline().pause()
            self.play_requested_at = None
            self.play_error = None
            self.last_health = 0.0
            carb.log_info('CC motion: Pause clicked.')
        except Exception as error:
            self.panel.set_runtime(f'PAUSE FAILED — {error}', error=True)
            carb.log_error(f'CC motion: Pause failed: {error}')

    def start_diagnostic(self):
        if self.diagnostic_task and not self.diagnostic_task.done():
            self.diagnostic_task.cancel()
        self.diagnostic_task = asyncio.ensure_future(diagnostics.report_motion(self))

    def reconnect(self):
        if self.stopped:
            return
        carb.log_info('CC motion: reconnecting the current stage and recreating the owned preview layer.')
        self.task.cancel()
        self.detach()
        self.closing_stage = None
        self.task = asyncio.ensure_future(self.run())
        self.task.add_done_callback(self.finished)
        self.panel.set_runtime('RECONNECTING — reading the current stage and DATA declaration...')

    def remove_overlay(self):
        if self.overlay is not None and self.stage is not None:
            session = self.stage.GetSessionLayer()
            paths = list(session.subLayerPaths)
            if self.overlay.identifier in paths:
                paths.remove(self.overlay.identifier)
                session.subLayerPaths = paths
        self.overlay = None
        self.sample_times.clear()
        self.last_frame = None

    def detach(self):
        if self.diagnostic_task:
            self.diagnostic_task.cancel()
            self.diagnostic_task = None
        if self.watcher:
            self.watcher.cancel()
            self.watcher = None
        self.remove_overlay()
        if self.partition_restore:
            settings, path, value = self.partition_restore
            try:
                settings.set_bool(path, value)
                carb.log_info(f'CC motion: restored {path}={value}.')
            except Exception as error:
                carb.log_warn(f'CC motion: could not restore {path}: {error}')
            self.partition_restore = None
        self.stage = None
        self.controls = self.digest = None
        self.reported = None
        self.path = None
        self.frame_count = 0
        self.last_clock = None
        self.last_health = 0.0
        self.health_key = None
        self.play_requested_at = None
        self.play_error = None
        for timeline, auto_update in self.timeline_restore:
            try:
                timeline.set_auto_update(auto_update)
            except Exception as error:
                carb.log_warn(f'CC motion: could not restore timeline advancement: {error}')
        self.timeline_restore.clear()
        if not self.stopped:
            self.panel.bind(None)
            self.panel.set_status('Waiting for SceneROOT_MotionGraphics.usda.')
            self.panel.set_runtime('DISCONNECTED — open SceneROOT_MotionGraphics.usda, then Reconnect.')
            self.panel.set_probe('Playback read-back: waiting for a connected scene.')

    def attach(self, stage):
        self.stage = stage
        self.timeline = self.context.get_timeline()
        self.timeline_name = self.context.get_timeline_name()
        if stage.GetRootLayer().customLayerData.get('cc:profile') != model.PROFILE:
            notify('Live motion is waiting for SceneROOT_MotionGraphics.usda.')
            return
        # This sample does not author scene partitions. NVIDIA documents an FSD
        # bug in Kit 110.3 where instanced-scene transforms can remain visually
        # stale although Fabric world transforms are current. Disable partitioning
        # only for this preview if the host enabled it, and restore its exact prior
        # state when this controller detaches. Never change the user's Kit config.
        renderer_settings = carb.settings.get_settings()
        partition_path = '/renderer/scenePartitioning/enabled'
        try:
            partition_enabled = renderer_settings.get(partition_path)
        except Exception:
            partition_enabled = None
        if partition_enabled is True:
            self.partition_restore = (renderer_settings, partition_path, True)
            renderer_settings.set_bool(partition_path, False)
            carb.log_warn('CC motion: temporarily disabled RTX scene partitioning for this unpartitioned '
                          'PointInstancer preview; Kit 110.3 documents stale instanced transforms with FSD. '
                          'The previous setting will be restored on disconnect.')
            notify('Motion preview: temporarily disabled scene partitioning to avoid stale FSD instance transforms.')
        declaration = stage.GetPrimAtPath(model.CONTROL_PRIM)
        if not declaration or declaration.GetAttribute('cc:profile').Get() != model.PROFILE:
            raise RuntimeError('Motion DATA declaration missing or profile mismatch.')
        if declaration.GetAttribute('cc:target').Get() != model.CLONER:
            raise RuntimeError('Unsupported DATA target; this writer only owns the declared cloner.')
        cloner = UsdGeom.PointInstancer(stage.GetPrimAtPath(model.CLONER))
        if not cloner or list(cloner.GetIdsAttr().Get() or []) != list(range(1024)):
            raise RuntimeError('Expected PointInstancer with stable IDs 0..1023.')
        if len(cloner.GetPrototypesRel().GetTargets()) != 6:
            raise RuntimeError('Expected six prototype configurations.')
        attribute = declaration.GetAttribute('cc:controls')
        asset = attribute.Get()
        if not isinstance(asset, Sdf.AssetPath) or not asset.path:
            raise RuntimeError('DATA must declare a local controls asset path.')
        specs = attribute.GetPropertyStack()
        resolved = asset.resolvedPath or Sdf.ComputeAssetPathRelativeToLayer(specs[0].layer, asset.path)
        path = Path(resolved).resolve()
        # This bounded example accepts only its package-owned data file.
        package = Path(stage.GetRootLayer().realPath).resolve().parent
        if path != (package / '040_DATA_LYR/Controls/motion_graphics.json').resolve():
            raise RuntimeError('Controls must resolve to this package\'s motion_graphics.json.')
        self.path = path
        self.clock_changed_at = time.monotonic()
        self.panel.bind(path)
        self.watcher = asyncio.ensure_future(self.watch(path, stage))
        self.watcher.add_done_callback(self.watcher_finished)
        self.start_diagnostic()
        carb.log_info(f'CC motion ready: save {path}; Play uses the Kit timeline. Opinion remains your edit target.')

    async def watch(self, path, stage):
        observed = None
        while self.stage == stage:
            digest = None
            try:
                raw, digest = await asyncio.to_thread(model.read_snapshot, path)
                if self.stage != stage:
                    return
                if digest != observed:
                    observed = digest
                    _, controls = model.parse_document(raw)
                    self.accept(controls, digest)
            except (OSError, ValueError, TypeError) as error:
                if self.stage != stage:
                    return
                message = str(error)
                if isinstance(error, OSError):
                    observed = None
                if message != self.reported:
                    carb.log_warn(f'CC motion: keeping last valid controls (or baked clip): {message}')
                    notify(f'JSON changes NOT applied. {message}\nKeeping last valid controls or saved animation.', warning=True)
                    self.reported = message
                self.panel.rejected(message, digest)
            await asyncio.sleep(0.25)

    def accept(self, controls, digest, force=False):
        changed = digest != self.digest
        self.controls, self.digest = controls, digest
        self.last_frame = None
        if changed:
            carb.log_info('CC motion: accepted saved JSON controls.')
        self.reported = None
        self.panel.accepted(controls, digest, force)
        self.panel.set_status('JSON ACCEPTED — live controls active. Play for motion; paused edits update the current pose.'
                              if controls['live_preview'] else
                              'JSON ACCEPTED — live preview OFF. Showing the saved animation; other JSON controls are inactive.')

    def operation(self, coroutine):
        task = asyncio.ensure_future(coroutine)
        self.operations.add(task)
        task.add_done_callback(self.operation_finished)

    def operation_finished(self, task):
        self.operations.discard(task)
        if not task.cancelled() and task.exception():
            carb.log_error(f'CC motion file operation: {task.exception()}')
            if not self.stopped:
                self.panel.set_busy(False)
                self.panel.set_status(f'FILE OPERATION FAILED: {task.exception()}', error=True)

    def reload_from_panel(self):
        if self.path and not self.panel.busy:
            self.panel.set_busy(True)
            self.operation(self.reload_file(self.path, self.stage))

    async def reload_file(self, path, stage):
        digest = None
        try:
            raw, digest = await asyncio.to_thread(model.read_snapshot, path)
            if self.stopped or self.stage != stage:
                return
            _, controls = model.parse_document(raw)
            self.accept(controls, digest, force=True)
        except (OSError, ValueError, TypeError) as error:
            if not self.stopped and self.stage == stage:
                self.panel.rejected(str(error), digest, force=True)
        finally:
            if not self.stopped and self.stage == stage:
                self.panel.set_busy(False)

    def save_from_panel(self, controls, expected_digest):
        if self.path and not self.panel.busy:
            self.panel.set_busy(True)
            self.panel.set_status('Saving DATA JSON; keeping a backup of the previous file...')
            self.operation(self.save_file(self.path, self.stage, controls, expected_digest))

    async def save_file(self, path, stage, controls, expected_digest):
        # A dispatched disk save finishes even if the stage closes. No USD/UI
        # access in its worker; completion is ignored by a replaced controller.
        try:
            document, digest, backup = await asyncio.to_thread(model.save_controls, path, controls, expected_digest)
            carb.log_info(f'CC motion: saved {path}; previous JSON: {backup}')
            if not self.stopped and self.stage == stage:
                self.accept(model.validate(document), digest, force=True)
        except (OSError, ValueError, TypeError) as error:
            if not self.stopped and self.stage == stage:
                self.panel.set_status(f'NOT SAVED: {error}', error=True)
        finally:
            if not self.stopped and self.stage == stage:
                self.panel.set_busy(False)

    def apply_frame(self, seconds):
        # Keep a two-sample window, so imaging sees time-varying arrays rather
        # than a static default that is repeatedly replaced. The next sample is
        # evaluated from the same accepted controls; no accumulated simulation.
        rate = self.stage.GetTimeCodesPerSecond()
        code = seconds * rate
        samples = [(code, model.usd_values(model.evaluate(self.controls, seconds))),
                   (code + 1.0, model.usd_values(model.evaluate(self.controls, seconds + 1.0 / rate)))]
        times = {sample[0] for sample in samples}
        if self.overlay is None:
            self.overlay = Sdf.Layer.CreateAnonymous('CC_MotionGraphics_Runtime.usda')
            self.overlay.timeCodesPerSecond = rate
            self.overlay.customLayerData = {'cc:role': 'RuntimeLyr', 'cc:profile': model.PROFILE,
                'cc:owner': 'scene:MotionGraphics@1', 'cc:writer': 'JSON motion preview; never saved'}
            prim = Sdf.CreatePrimInLayer(self.overlay, model.CLONER)
            types = {'positions': Sdf.ValueTypeNames.Point3fArray,
                     'orientations': Sdf.ValueTypeNames.QuathArray,
                     'scales': Sdf.ValueTypeNames.Float3Array,
                     'protoIndices': Sdf.ValueTypeNames.IntArray,
                     'extent': Sdf.ValueTypeNames.Float3Array}
            for name, kind in types.items():
                Sdf.AttributeSpec(prim, name, kind)
            session = self.stage.GetSessionLayer()
            # Insert our layer only; preserve all other Session contributions.
            session.subLayerPaths = [self.overlay.identifier, *session.subLayerPaths]
        with Sdf.ChangeBlock():
            for sample_code, values in samples:
                for name, value in values.items():
                    self.overlay.SetTimeSample(model.CLONER + '.' + name, sample_code, value)
            for stale_code in self.sample_times - times:
                for name in samples[0][1]:
                    self.overlay.EraseTimeSample(model.CLONER + '.' + name, stale_code)
            if self.overlay.customLayerData.get('cc:inputSha256') != self.digest:
                self.overlay.customLayerData = {**self.overlay.customLayerData, 'cc:inputSha256': self.digest}
        self.sample_times = times
        self.frame_count += 1

    def update_health(self, seconds):
        try:
            self.update_health_details(seconds)
        except Exception as error:
            message = f'Connection diagnostic failed: {error}'
            if self.health_key != message:
                carb.log_warn('CC motion: ' + message)
                self.health_key = message
            self.panel.set_runtime(message, error=True)

    def update_health_details(self, seconds):
        """Visible clock/output heartbeat and bounded composition diagnostics."""
        now = time.monotonic()
        if seconds != self.last_clock:
            self.last_clock = seconds
            self.clock_changed_at = now
        if now - self.last_health < 0.5:
            return
        self.last_health = now
        playing = self.timeline.is_playing()
        mode = 'LIVE' if self.controls['live_preview'] else 'BAKED'
        if playing:
            self.play_requested_at = None
        elif self.play_requested_at and now - self.play_requested_at > 1:
            self.play_error = 'Play was requested but this timeline is not playing.'
            self.play_requested_at = None
        issues = [self.play_error] if self.play_error else []
        if playing and now - self.clock_changed_at > 1:
            issues.append('Timeline reports Play but time is not advancing.')
        if not self.timeline.is_auto_updating():
            issues.append('Automatic timeline advancement is off; click Play to enable it.')
        prim = self.stage.GetPrimAtPath(model.CLONER)
        if not prim or not prim.IsA(UsdGeom.PointInstancer):
            issues.append('PointInstancer is missing; check whether GeoLyr is muted.')
        elif self.controls['live_preview']:
            if self.overlay is None or self.overlay not in self.stage.GetLayerStack():
                issues.append('Runtime layer is muted or detached. Reconnect recreates the owned preview.')
            else:
                code = Usd.TimeCode(seconds * self.stage.GetTimeCodesPerSecond())
                for name in ('positions', 'orientations', 'scales', 'protoIndices', 'extent'):
                    attribute = prim.GetAttribute(name)
                    for spec in attribute.GetPropertyStack(code):
                        if spec.HasInfo('default') or spec.layer.GetNumTimeSamplesForPath(spec.path):
                            if spec.layer != self.overlay:
                                issues.append(f'{name} is masked by {spec.layer.GetDisplayName()}.')
                            break
                if UsdGeom.Imageable(prim).ComputeVisibility(code) == UsdGeom.Tokens.invisible:
                    issues.append('Cloner is invisible in the composed stage.')
            if self.controls['strength'] == 0 and self.controls['color_cycle_hz'] == 0:
                issues.append('Strength and colour cycling are zero; controls request a static layout.')
        state = 'PLAYING' if playing else 'PAUSED'
        detail = ' '.join(issues) if issues else 'Timeline samples active. See playback read-back below.'
        if self.partition_restore:
            detail += ' RTX scene partitioning is temporarily OFF for this preview (restored on disconnect).'
        else:
            partition_enabled = carb.settings.get_settings().get('/renderer/scenePartitioning/enabled')
            detail += (' RTX scene partitioning is ON.' if partition_enabled is True else
                       ' RTX scene partitioning is OFF or not configured.')
        self.panel.set_runtime(f'{mode} {state} | time {seconds:.2f} s | runtime updates {self.frame_count}\n{detail}', error=bool(issues))
        key = (mode, state, tuple(issues))
        if key != self.health_key:
            message = f'CC motion: {mode} {state}; time={seconds:.3f}s; updates={self.frame_count}; {detail}'
            (carb.log_warn if issues else carb.log_info)(message)
            self.health_key = key

    async def run(self):
        while True:
            await omni.kit.app.get_app().next_update_async()
            current = self.context.get_stage()
            if current == self.closing_stage:
                continue
            if current != self.stage:
                self.detach()
                if current:
                    self.attach(current)
            if not self.stage or self.controls is None:
                continue
            # Applications can assign a named timeline to their USD context.
            # Reading the global default would then leave this controller static.
            if self.context.get_timeline_name() != self.timeline_name:
                self.timeline = self.context.get_timeline()
                self.timeline_name = self.context.get_timeline_name()
            seconds = self.timeline.get_current_time()
            if not self.controls['live_preview']:
                if self.overlay is not None:
                    self.remove_overlay()
                    carb.log_info('CC motion: live preview disabled; saved animation exposed.')
                self.update_health(seconds)
                continue
            stamp = (seconds, self.digest)
            if stamp == self.last_frame:
                self.update_health(seconds)
                continue
            # USD mutations stay on Kit's update thread. No per-frame undo entries;
            # removing the owned layer restores the underlying authored clip.
            self.apply_frame(seconds)
            self.last_frame = stamp
            self.update_health(seconds)


previous = getattr(builtins, 'cc_motion_graphics', None)
# Recover/reapply the authoring helper first. A startup error here must not
# tear down an otherwise running motion panel/controller.
runpy.run_path(str(_folder / 'session_defaults.py'))
if previous:
    previous.stop()
builtins.cc_motion_graphics = MotionGraphics()
