"""Bounded USD-aware migration of Cube, Cone and DisplayPair to recursive packages."""
import json
import os
from pathlib import Path
from pxr import Sdf, UsdUtils
from build_example import Author, opinion_layer

PACKAGE = Path(__file__).resolve().parents[1] / 'examples/01_LayeredScene'


def main():
    packages = [('USD_Wrappers/Cube', 'Cube', 'asset:Cube@1'),
                ('USD_Wrappers/Cone', 'Cone', 'asset:Cone@1'),
                ('Assemblies/DisplayPair', 'DisplayPair', 'assembly:DisplayPair@1')]
    moves = {}
    for folder, name, owner in packages:
        base = PACKAGE / '010_ASS_USD' / folder
        moves[base / f'{name}.usda'] = base / f'AssetROOT_{name}.usda'
        for path in (base / 'layers').glob('*.usda'):
            moves[path] = base / '020_BASE_LYR' / path.name
    if any(not old.exists() or new.exists() for old, new in moves.items()):
        raise RuntimeError('Expected original package files and unused destinations; refusing migration.')
    # Prepare every layer before writing. Preserve authored specs and variant contexts.
    candidates = []
    for old in sorted(PACKAGE.rglob('*.usda')):
        new = moves.get(old, old)
        layer = Sdf.Layer.CreateAnonymous('.usda')
        layer.TransferContent(Sdf.Layer.FindOrOpen(str(old)))
        def remap(path):
            if not path or '://' in path or os.path.isabs(path) or not path.startswith('.'):
                return path
            resolved = (old.parent / path).resolve()
            target = moves.get(resolved, resolved)
            result = Path(os.path.relpath(target, new.parent)).as_posix()
            return result if result.startswith('.') else './' + result
        UsdUtils.ModifyAssetPaths(layer, remap)
        data = dict(layer.customLayerData)
        omni = dict(data.get('omni_layer', {}))
        for key in ('locked', 'muteness'):
            if key in omni:
                omni[key] = {remap(path): value for path, value in omni[key].items()}
        if 'authoring_layer' in omni:
            omni['authoring_layer'] = remap(omni['authoring_layer'])
        if omni:
            data['omni_layer'] = omni
        layer.customLayerData = data
        candidates.append((new, layer))
    a = Author(PACKAGE)
    for folder, name, owner in packages:
        base = PACKAGE / '010_ASS_USD' / folder
        relative = (base / '050_OPINION_LYR/OpinLYR_default.usda').relative_to(PACKAGE).as_posix()
        opinion_layer(a, relative, owner)
        new_root = base / f'AssetROOT_{name}.usda'
        layer = next(layer for dest, layer in candidates if dest == new_root)
        opinion = './050_OPINION_LYR/OpinLYR_default.usda'
        layer.subLayerPaths = [opinion, *layer.subLayerPaths]
        data = dict(layer.customLayerData)
        data.update({'cc:defaultAuthoring': 'opinion', 'cc:opinionLayer': opinion,
                     'cc:lockPersistentLayers': True})
        omni = dict(data.get('omni_layer', {}))
        locks = dict(omni.get('locked', {})); locks[opinion] = False
        omni.update({'locked': locks, 'authoring_layer': opinion})
        data['omni_layer'] = omni; layer.customLayerData = data
        for lane in ('000_SOURCE', '010_ASS_USD', '030_SIM_LYR', '035_RUNTIME_LYR', '040_DATA_LYR', '_contracts'):
            a.text((base/lane/'README.md').relative_to(PACKAGE),
                   f'# {lane}\n\nReserved at the {name} package scope. Add owned content only when required. '
                   'This directory does not create a composed layer. External dependencies remain declared relative links.')
        a.text((base/'README.md').relative_to(PACKAGE),
               f'# {name} reusable package\n\nOpen AssetROOT_{name}.usda. Opinion is the default authoring layer '
               'when opened directly in compatible Kit; other layers are protected. '
               '020_BASE_LYR contains this package\'s geometry, transforms and controls. '
               '050_OPINION_LYR contains package-owned experiments; saving them affects every consumer. '
               'When used inside a scene, author scene experiments in the scene Opinion instead. '
               'Other class directories are reserved, not empty USD layers. '
               'A building or workcell follows the same AssetROOT convention when reused in a larger scene.')
    for new, layer in candidates:
        new.parent.mkdir(parents=True, exist_ok=True)
        layer.Export(str(new))
    for old in moves:
        if not old.resolve().is_relative_to(PACKAGE.resolve()):
            raise RuntimeError('Unexpected source outside package')
        old.unlink()
    replacements = {old.relative_to(PACKAGE).as_posix(): new.relative_to(PACKAGE).as_posix()
                    for old, new in moves.items()}
    def update(value):
        if isinstance(value, str):
            for old, new in replacements.items():
                value = value.replace(old, new)
            return value.replace('layers/GeoLyr', '020_BASE_LYR/GeoLyr')
        if isinstance(value, list): return [update(item) for item in value]
        if isinstance(value, dict): return {key: update(item) for key, item in value.items()}
        return value
    for path in (PACKAGE/'_contracts').glob('*.json'):
        data = update(json.loads(path.read_text()))
        if path.name == 'profile.json': data['roles'].extend(a.roles)
        a.json(path.relative_to(PACKAGE), data)
    print('Migrated recursive asset packages and dependency paths. No tests run.')


if __name__ == '__main__':
    main()
