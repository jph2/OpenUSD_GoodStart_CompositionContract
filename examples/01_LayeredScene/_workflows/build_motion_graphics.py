"""Author the bounded MoGraph example, or explicitly rebake its animation.

Requires pxr. Default: print plan. --apply creates a NEW scene; --rebake replaces
only the animation, preserving previous bytes and the exact control input.
Close/reload the scene around rebaking. No Kit launch or acceptance tests.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import uuid

from pxr import Gf, Sdf, Usd, UsdGeom, Vt
from motion_graphics_core import (CLONER, CONTROL_PRIM, PROFILE, control_schema,
                                 default_document, evaluate, read_controls, usd_values, validate)

PACKAGE = Path(__file__).resolve().parents[1]
CONTROL = '040_DATA_LYRs/Controls/motion_graphics.json'
ANIMATION = '020_BASE_LYR/AnimLyr_MotionGraphics.usdc'
ROOT = 'SceneROOT_MotionGraphics.usda'
OPINION = '050_REVIEW/MotionGraphics/OpinLYR_default.usda'
ROLES = [OPINION, '040_DATA_LYRs/DataLyr_MotionGraphics.usda', ANIMATION,
         '020_BASE_LYR/CamLyr_MotionGraphics.usda',
         '020_BASE_LYR/TransLyr_MotionGraphics.usda',
         '020_BASE_LYR/VariLyr_MotionGraphics.usda',
         '020_BASE_LYR/GeoLyr_MotionGraphics.usda']


def new_layer(role):
    layer = Sdf.Layer.CreateAnonymous('.usda')
    layer.customLayerData = {'cc:owner': 'scene:MotionGraphics@1', 'cc:role': role,
                            'cc:profile': PROFILE}
    return layer


def make_animation(controls, digest):
    layer = new_layer('AnimLyr')
    layer.customLayerData = {**layer.customLayerData, 'cc:inputSha256': digest,
                            'cc:input': CONTROL, 'cc:sampleStep': 2}
    prim = Sdf.CreatePrimInLayer(layer, CLONER)
    types = {'positions': Sdf.ValueTypeNames.Point3fArray,
             'orientations': Sdf.ValueTypeNames.QuathArray,
             'scales': Sdf.ValueTypeNames.Float3Array,
             'protoIndices': Sdf.ValueTypeNames.IntArray,
             'extent': Sdf.ValueTypeNames.Float3Array}
    specs = {name: Sdf.AttributeSpec(prim, name, kind) for name, kind in types.items()}
    for frame in range(0, 481, 2):
        values = usd_values(evaluate(controls, frame / 60))
        for name, value in values.items():
            if frame == 0:
                specs[name].default = value
            layer.SetTimeSample(specs[name].path, frame, value)
    return layer


def schema():
    return control_schema()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--apply', action='store_true')
    group.add_argument('--rebake', action='store_true')
    args = parser.parse_args()
    if not args.apply and not args.rebake:
        print(f'Create {ROOT}, {len(ROLES)} direct roles, controls/schema and profile with --apply.')
        print(f'Or --rebake: replace ONLY {ANIMATION} from {CONTROL}; keep backup/input record.')
        return
    control_path = PACKAGE / CONTROL
    if args.rebake:
        controls, digest = read_controls(control_path)
        input_bytes = control_path.read_bytes()
        if hashlib.sha256(input_bytes).hexdigest() != digest:
            raise RuntimeError('Control input changed during capture; nothing replaced.')
        destination = PACKAGE / ANIMATION
        if not destination.is_file():
            raise RuntimeError('Animation missing; create the scene first.')
        previous = destination.read_bytes()
        layer = make_animation(controls, digest)
        # Stop if inputs or output changed while baking.
        if read_controls(control_path)[1] != digest or destination.read_bytes() != previous:
            raise RuntimeError('Input or animation changed while baking; nothing replaced.')
        backup = PACKAGE / '_pipeline_reports/motion_graphics' / uuid.uuid4().hex
        backup.mkdir(parents=True)
        (backup / destination.name).write_bytes(previous)
        (backup / 'motion_graphics.json').write_bytes(input_bytes)
        (backup / 'record.json').write_text(json.dumps({'profile': PROFILE, 'input_sha256': digest,
            'previous_sha256': hashlib.sha256(previous).hexdigest(), 'destination': ANIMATION}, indent=2), encoding='utf-8')
        temp = destination.with_name('.' + uuid.uuid4().hex + '.usdc')
        try:
            if not layer.Export(str(temp)):
                raise RuntimeError('Animation export failed.')
            if read_controls(control_path)[1] != digest or destination.read_bytes() != previous:
                raise RuntimeError('Input or animation changed before replacement; nothing replaced.')
            os.replace(temp, destination)
        finally:
            temp.unlink(missing_ok=True)
        print(f'Rebaked {ANIMATION}; previous clip and input retained in {backup}.')
        return

    paths = [ROOT, *ROLES, CONTROL, '040_DATA_LYRs/Controls/motion_graphics.schema.json',
             '_contracts/motion_graphics.json']
    for relative in paths:
        if (PACKAGE / relative).exists():
            raise RuntimeError(f'Refusing to overwrite {relative}; use --rebake only for animation.')
    doc = default_document()
    doc['$schema'] = './motion_graphics.schema.json'
    raw = (json.dumps(doc, indent=2) + '\n').encode('utf-8')
    digest = hashlib.sha256(raw).hexdigest()
    pending = {OPINION: new_layer('Opinion'), ANIMATION: make_animation(validate(doc), digest)}

    geo = new_layer('GeoLyr')
    # Author specs without composing relative references from an anonymous layer.
    for path, kind in [('/World', 'Xform'), ('/World/MotionGraphics', 'Xform'),
                       (CLONER, 'PointInstancer'), (CLONER + '/Prototypes', 'Scope')]:
        spec = Sdf.CreatePrimInLayer(geo, path)
        spec.specifier, spec.typeName = Sdf.SpecifierDef, kind
    instancer = geo.GetPrimAtPath(CLONER)
    Sdf.AttributeSpec(instancer, 'ids', Sdf.ValueTypeNames.Int64Array).default = Vt.Int64Array(range(1024))
    prototype_paths = []
    for shape in ('Cube', 'Cone'):
        for finish in ('Red', 'Blue', 'Yellow'):
            path = f'{CLONER}/Prototypes/{shape}{finish}'
            site = Sdf.CreatePrimInLayer(geo, path)
            site.specifier, site.typeName = Sdf.SpecifierDef, 'Xform'
            site.referenceList.prependedItems = [Sdf.Reference(f'../010_ASS_USD/USD_Wrappers/{shape}Lofted/AssetROOT_{shape}Lofted.usda')]
            prototype_paths.append(Sdf.Path(path))
    Sdf.RelationshipSpec(instancer, 'prototypes', False).targetPathList.explicitItems = prototype_paths
    pending['020_BASE_LYR/GeoLyr_MotionGraphics.usda'] = geo
    vari = new_layer('VariLyr')
    for path in prototype_paths:
        spec = Sdf.CreatePrimInLayer(vari, path)
        spec.variantSelections['Size'] = 'Normal'
        spec.variantSelections['Finish'] = next(c for c in ('Red', 'Blue', 'Yellow') if str(path).endswith(c))
    pending['020_BASE_LYR/VariLyr_MotionGraphics.usda'] = vari

    trans = new_layer('TransLyr')
    tstage = Usd.Stage.Open(trans)
    xform = UsdGeom.Xformable(tstage.OverridePrim('/World/MotionGraphics'))
    xform.AddTranslateOp().Set(Gf.Vec3d(0))
    pending['020_BASE_LYR/TransLyr_MotionGraphics.usda'] = trans

    camera = new_layer('CamLyr')
    cstage = Usd.Stage.Open(camera)
    cam = UsdGeom.Camera.Define(cstage, '/World/MotionOverview')
    cam.CreateClippingRangeAttr(Gf.Vec2f(10, 100000))
    cam.CreateFocalLengthAttr(35)
    matrix = Gf.Matrix4d().SetLookAt(Gf.Vec3d(7000, -8500, 8500), Gf.Vec3d(0, 0, 700), Gf.Vec3d(0, 0, 1)).GetInverse()
    cam.AddTransformOp().Set(matrix)
    pending['020_BASE_LYR/CamLyr_MotionGraphics.usda'] = camera

    data = new_layer('DataLyr')
    # This scene owns its input declaration, without unrelated teaching-object IDs.
    spec = Sdf.CreatePrimInLayer(data, CONTROL_PRIM)
    spec.specifier, spec.typeName = Sdf.SpecifierDef, 'Scope'
    for name, kind, value in [
        ('cc:controls', Sdf.ValueTypeNames.Asset, Sdf.AssetPath('./Controls/motion_graphics.json')),
        ('cc:profile', Sdf.ValueTypeNames.String, PROFILE),
        ('cc:target', Sdf.ValueTypeNames.String, CLONER),
        ('cc:identityScope', Sdf.ValueTypeNames.String, 'MotionGraphics cloner IDs 0..1023; fixed row-major topology'),
        ('cc:writer', Sdf.ValueTypeNames.String, 'baked AnimLyr OR temporary runtime overlay'),
    ]:
        Sdf.AttributeSpec(spec, name, kind, declaresCustom=True).default = value
    pending['040_DATA_LYRs/DataLyr_MotionGraphics.usda'] = data

    root = new_layer('Root')
    original = Sdf.Layer.FindOrOpen(str(PACKAGE / 'SceneROOT_Example.usda'))
    root.TransferContent(original)
    root.subLayerPaths = ['./' + item for item in ROLES]
    root.startTimeCode, root.endTimeCode, root.timeCodesPerSecond, root.framesPerSecond = 0, 480, 60, 60
    metadata = dict(root.customLayerData)
    locks = {name: True for name in root.subLayerPaths}
    locks['./' + OPINION] = False
    metadata.update({'cc:owner': 'scene:MotionGraphics@1', 'cc:profile': PROFILE,
                     'cc:opinionLayer': './' + OPINION,
                     'omni_layer': {'authoring_layer': './' + OPINION, 'locked': locks}})
    camera_settings = dict(metadata['cameraSettings'])
    camera_settings['Perspective'] = {'position': Gf.Vec3d(7000, -8500, 8500), 'target': Gf.Vec3d(0, 0, 700)}
    camera_settings['boundCamera'] = '/World/MotionOverview'
    metadata['cameraSettings'] = camera_settings
    root.customLayerData = metadata
    pending[ROOT] = root

    for relative, layer in pending.items():
        destination = PACKAGE / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not layer.Export(str(destination)):
            raise RuntimeError(f'Export failed: {destination}')
    control_path.parent.mkdir(parents=True, exist_ok=True)
    control_path.write_bytes(raw)
    (control_path.parent / 'motion_graphics.schema.json').write_text(json.dumps(schema(), indent=2) + '\n', encoding='utf-8')
    profile = {'profile': PROFILE, 'status': 'authored; Kit acceptance pending',
        'root': ROOT, 'direct_sublayers_strongest_first': ROLES,
        'controls': CONTROL, 'input_prim': CONTROL_PRIM, 'target': CLONER,
        'count': 1024, 'ids': '0..1023, fixed row-major 32 x 32',
        'prototypes': [str(p) for p in prototype_paths],
        'writer_properties': ['positions', 'orientations', 'scales', 'protoIndices', 'extent'],
        'units': {'distance': 'cm', 'time': 'seconds', 'angle': 'degrees'},
        'baked': {'file': ANIMATION, 'time_codes_per_second': 60, 'range': [0, 480], 'sample_step': 2, 'input_sha256': digest},
        'runtime': {'storage': 'owned anonymous sublayer of session', 'save': 'never',
            'precedence': 'runtime arrays override baked arrays; direct Session opinions can still mask them',
            'clock': 'Kit timeline seconds; no wall-clock accumulation', 'poll_seconds': 0.25,
            'stale_input': 'hold last valid controls and continue timeline; report error',
            'stop': 'disable live_preview or stop helper removes owned overlay, exposing bake',
            'reload': 'stage replacement/rerun tears down old tasks/overlay'},
        'rules': ['CC-05c', 'CC-05d', 'CC-21', 'CC-23', 'CC-27', 'CC-28'],
        'limitations': ['not a generic binding engine', 'no physics', 'no per-point prim namespace',
                        'runtime undo uses overlay removal; no per-frame undo commands',
                        'prototype/source edits invalidate the conservative extent assumption',
                        'Kit playback, point-instancer rendering and throughput not verified']}
    (PACKAGE / '_contracts/motion_graphics.json').write_text(json.dumps(profile, indent=2) + '\n', encoding='utf-8')
    print(f'Authored {len(pending)} USD files, 1024 points, six prototypes, 241 samples. No acceptance tests run.')


if __name__ == '__main__':
    main()
