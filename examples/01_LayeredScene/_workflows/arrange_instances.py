"""Map 1,024 normalized JSON samples to shared-asset selections and placement.

Requires Python with pxr (usd-core 26.8). Default prints a plan; --apply writes
the named derived scene, its two role layers and Opinion, retaining backups.
Run outside Kit, then reopen/reload the scene; do not overwrite unsaved Kit edits.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import os
import tempfile
import uuid
from collections import Counter

from pxr import Gf, Sdf

PACKAGE = Path(__file__).resolve().parents[1]
SIZES = ('Normal', 'Large', 'Tall')
FINISHES = ('Red', 'Blue', 'Yellow')


def layout(index, value, shape):
    row, column = divmod(index, 32)
    if shape in ('grid', 'wave'):
        x, y = (column - 15.5) * 240, 500 + row * 240
        z = value * 600 if shape == 'wave' else 0
        yaw = value * 360
    elif shape == 'spiral':
        angle = index * 0.24
        radius = 130 * math.sqrt(index + 1)
        x, y, z = radius * math.cos(angle), 4700 + radius * math.sin(angle), value * 600
        yaw = math.degrees(angle)
    else:
        angle = column * 2 * math.pi / 32
        radius = 1500 + row * 250
        x, y, z = radius * math.cos(angle), 10300 + radius * math.sin(angle), value * 600
        yaw = math.degrees(angle)
    return (x, y, z), (0, 0, yaw)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=PACKAGE / '_workflows/inputs/instance_signal.json')
    parser.add_argument('--shape', choices=('wave', 'spiral', 'rings'), default='wave')
    parser.add_argument('--apply', action='store_true', help='Write the listed derived scene files after backing up their current bytes')
    args = parser.parse_args()
    raw = args.input.read_bytes()
    signal = json.loads(raw)
    values = signal.get('values')
    if not isinstance(values, list) or len(values) != 1024 or any(
        isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or not 0 <= v <= 1 for v in values
    ):
        raise ValueError('Input must contain values: exactly 1024 finite numbers in [0, 1], in row-major order.')
    purpose = 'Instanced_' + args.shape.title()
    owner = f'scene:{purpose}@1'
    targets = [PACKAGE / f'020_BASE_LYR/{role}_{purpose}.usda' for role in ('TransLyr', 'VariLyr')]
    targets += [PACKAGE / f'SceneROOT_{purpose}.usda', PACKAGE / f'050_REVIEW/{purpose}/OpinLYR_default.usda']
    originals = [path.read_bytes() if path.exists() else None for path in targets]
    layers = []
    for path in targets[:2]:
        template = path if path.exists() else PACKAGE / f'020_BASE_LYR/{path.name.split("_")[0]}_Instanced.usda'
        src = Sdf.Layer.FindOrOpen(str(template))
        if src.customLayerData.get('cc:owner') != (owner if path.exists() else 'scene:Instanced@1'):
            raise ValueError(f'Unexpected layer owner: {path}')
        candidate = Sdf.Layer.CreateAnonymous('.usda')
        candidate.TransferContent(src)
        candidate.customLayerData = {**candidate.customLayerData,
            'cc:owner': owner,
            'cc:driver': 'arrange_instances.py/0.1.1', 'cc:shape': args.shape,
            'cc:inputSha256': hashlib.sha256(raw).hexdigest(),
            'cc:context': 'generated ordinary placement' if path.name.startswith('Trans') else 'generated public variant selections'}
        layers.append(candidate)
    counts = Counter()
    for index, value in enumerate(values):
        row, column = divmod(index, 32)
        occurrence = f'/World/InstanceGrid/Shape_r{row:02d}_c{column:02d}'
        band = min(8, int(value * 9))
        size, finish = SIZES[band // 3], FINISHES[band % 3]
        shape = 'Cube' if (row + column) % 2 == 0 else 'Cone'
        counts[f'{shape}/{size}/{finish}'] += 1
        position, rotation = layout(index, value, args.shape)
        prim = Sdf.CreatePrimInLayer(layers[0], occurrence)
        for name, type_name, val in [
            ('xformOp:translate', Sdf.ValueTypeNames.Double3, Gf.Vec3d(*position)),
            ('xformOp:rotateXYZ', Sdf.ValueTypeNames.Double3, Gf.Vec3d(*rotation)),
            ('xformOpOrder', Sdf.ValueTypeNames.TokenArray, ['xformOp:translate', 'xformOp:rotateXYZ']),
        ]:
            attr = prim.attributes.get(name) or Sdf.AttributeSpec(prim, name, type_name,
                Sdf.VariabilityUniform if name == 'xformOpOrder' else Sdf.VariabilityVarying)
            attr.default = val
        variant = Sdf.CreatePrimInLayer(layers[1], occurrence + '/Adjustment/Asset')
        variant.variantSelections['Size'] = size
        variant.variantSelections['Finish'] = finish
    root = Sdf.Layer.CreateAnonymous('.usda')
    root.TransferContent(Sdf.Layer.FindOrOpen(str(targets[2] if targets[2].exists() else PACKAGE / 'SceneROOT_Instanced.usda')))
    opinion_path = './' + targets[3].relative_to(PACKAGE).as_posix()
    root.subLayerPaths = [opinion_path, './040_DATA_LYRs/DataLyr.usda',
                         './' + targets[0].relative_to(PACKAGE).as_posix(),
                         './' + targets[1].relative_to(PACKAGE).as_posix(),
                         './020_BASE_LYR/GeoLyr_Instanced.usda']
    locks = {path: True for path in root.subLayerPaths}
    locks[opinion_path] = False
    root.customLayerData = {**root.customLayerData, 'cc:owner': owner, 'cc:opinionLayer': opinion_path,
                           'omni_layer': {'authoring_layer': opinion_path, 'locked': locks}}
    opinion = Sdf.Layer.CreateAnonymous('.usda')
    if targets[3].exists():
        opinion.TransferContent(Sdf.Layer.FindOrOpen(str(targets[3])))
    else:
        opinion.customLayerData = {'cc:owner': owner, 'cc:role': 'Opinion', 'cc:profile': 'CC-SCALE-01/0.1.1'}
    layers.extend([root, opinion])
    plan = {'scene': purpose, 'shape': args.shape, 'grid_occurrences': 1024, 'configurations': dict(sorted(counts.items())),
            'writes': [str(path.relative_to(PACKAGE)) for path in targets],
            'input_sha256': hashlib.sha256(raw).hexdigest(), 'apply': args.apply}
    print(json.dumps(plan, indent=2))
    if not args.apply:
        print('Plan only. Add --apply to write this derived scene. Sources and the base Instanced scene are unchanged.')
        return
    backup = PACKAGE / '_pipeline_reports/instance_driver' / uuid.uuid4().hex
    backup.mkdir(parents=True)
    for path, data in zip(targets, originals):
        if data is not None:
            (backup / path.name).write_bytes(data)
    (backup / 'plan.json').write_text(json.dumps(plan, indent=2), encoding='utf-8')
    (backup / 'input.json').write_bytes(raw)
    temporary = []
    written = []
    try:
        for path, candidate in zip(targets, layers):
            path.parent.mkdir(parents=True, exist_ok=True)
            fd, temp = tempfile.mkstemp(suffix='.usda', dir=path.parent)
            os.close(fd)
            temporary.append(Path(temp))
            if not candidate.Export(temp):
                raise RuntimeError(f'Could not export {temp}')
        if any((path.read_bytes() if path.exists() else None) != data for path, data in zip(targets, originals)):
            raise RuntimeError('A destination changed while planning; rerun against its new contents.')
        for path, temp in zip(targets, temporary):
            os.replace(temp, path)
            written.append(path)
    except Exception:
        for path in written:
            data = originals[targets.index(path)]
            if data is None:
                path.unlink()
            else:
                path.write_bytes(data)
        raise
    finally:
        for temp in temporary:
            if temp.exists():
                temp.unlink()
    print(f'Wrote derived scene. Backups/input/plan: {backup}. Open SceneROOT_{purpose}.usda in Kit.')


if __name__ == '__main__':
    main()
