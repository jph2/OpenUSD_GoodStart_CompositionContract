"""Read-only live-motion report, also called automatically by the controller.

Waits for Play, then reads three snapshots; changes no playback/scene/settings.
The report is printed to the Script Editor and Kit log. No report file is saved.
"""
import asyncio
import builtins
import json
import time

import carb
import carb.settings
import omni.usd
from pxr import Usd


def points(value):
    if value is None or len(value) == 0:
        return None
    return [[round(float(v), 3) for v in value[i]] for i in (0, len(value) // 2, len(value) - 1)]


def snapshot(controller=None):
    controller = controller or getattr(builtins, 'cc_motion_graphics', None)
    context = controller.context if controller else omni.usd.get_context()
    stage = context.get_stage()
    if not stage or not controller:
        return {'error': 'Open the motion scene and run its bootstrap first.'}
    seconds = context.get_timeline().get_current_time()
    code = Usd.TimeCode(seconds * stage.GetTimeCodesPerSecond())
    path = '/World/MotionGraphics/Cloner'
    attr = stage.GetAttributeAtPath(path + '.positions')
    report = {'root': stage.GetRootLayer().identifier, 'seconds': seconds,
              'playing': context.get_timeline().is_playing(),
              'updates': controller.frame_count, 'usd_positions': points(attr.Get(code))}
    if controller.overlay:
        spec = controller.overlay.GetAttributeAtPath(path + '.positions')
        report['runtime_default'] = points(spec.default) if spec else None
        report['runtime_sample_times'] = list(controller.overlay.ListTimeSamplesForPath(path + '.positions'))
    report['positions_time_varying'] = attr.ValueMightBeTimeVarying()
    report['sources'] = [spec.layer.identifier for spec in attr.GetPropertyStack(code)]
    settings = carb.settings.get_settings()
    report['fabric_delegate'] = settings.get('/app/useFabricSceneDelegate')
    report['scene_partitioning'] = settings.get('/renderer/scenePartitioning/enabled')
    report['scene_partitioning_temporarily_disabled'] = bool(controller.partition_restore)
    report['fast_diffing'] = settings.get('/app/usdrt/population/utils/enableFastDiffing')
    try:
        from omni.kit.viewport.utility import get_active_viewport
        viewport = get_active_viewport()
        report['viewport'] = None if viewport is None else {
            'context': viewport.usd_context_name, 'same_stage': viewport.stage == stage,
            'time': str(viewport.time), 'updates': viewport.updates_enabled,
            'freeze_frame': viewport.freeze_frame, 'camera': str(viewport.camera_path)}
    except Exception as error:
        report['viewport_read_error'] = str(error)
    try:
        import usdrt
        fabric = usdrt.Usd.Stage.Attach(context.get_stage_id())
        # Only inspect a prim already present in Fabric; do not force population/sync.
        if fabric.HasPrimAtPath(usdrt.Sdf.Path(path)):
            prim = fabric.GetPrimAtPath(path)
            report['fabric_positions'] = points(prim.GetAttribute('positions').Get())
        else:
            report['fabric_positions'] = 'Cloner is not present in Fabric.'
    except Exception as error:
        report['fabric_read_error'] = str(error)
    return report


async def report_motion(controller=None):
    controller = controller or getattr(builtins, 'cc_motion_graphics', None)
    if not controller:
        carb.log_warn('CC motion diagnostic: run the motion bootstrap first.')
        return
    stage = controller.context.get_stage()
    deadline = time.monotonic() + 60
    captures = []
    show = getattr(controller.panel, 'set_probe', lambda *args, **kwargs: None)
    show('Playback read-back: waiting for Play, then collecting three snapshots.')
    carb.log_info('CC motion diagnostic: waiting for Play; will capture three moving-time snapshots.')
    while time.monotonic() < deadline and len(captures) < 3:
        await asyncio.sleep(0.37)
        if controller.stopped or controller.context.get_stage() != stage:
            return
        if not controller.context.get_timeline().is_playing() or controller.controls is None:
            continue
        try:
            data = snapshot(controller)
        except Exception as error:
            data = {'read_error': str(error)}
        if 'error' in data or 'read_error' in data:
            message = 'Playback read-back unavailable: ' + str(data)
            carb.log_warn('CC motion diagnostic: ' + message)
            show(message, error=True)
            return
        if captures and data.get('seconds') == captures[-1].get('seconds'):
            continue
        captures.append(data)
        message = 'CC motion diagnostic ' + json.dumps(data)
        print(message)
        carb.log_info(message)
    if len(captures) < 3:
        message = 'No three advancing playback snapshots in 60 seconds. Press Play and leave it running.'
        issue = True
    else:
        usd_changed = captures[0].get('usd_positions') != captures[-1].get('usd_positions')
        fabric_readable = all(isinstance(data.get('fabric_positions'), list) for data in captures)
        fabric_changed = (captures[0]['fabric_positions'] != captures[-1]['fabric_positions']) if fabric_readable else 'unavailable'
        message = f'Playback read-back: USD positions changed={usd_changed}; Fabric changed={fabric_changed}. Viewport image unverified.'
        issue = not usd_changed or fabric_changed is False
    carb.log_info('CC motion diagnostic: ' + message)
    show(message, error=issue)


if __name__ in ('__main__', '<run_path>'):
    _previous = getattr(builtins, 'cc_motion_diagnostic', None)
    if _previous and not _previous.done():
        _previous.cancel()
    builtins.cc_motion_diagnostic = asyncio.ensure_future(report_motion())
