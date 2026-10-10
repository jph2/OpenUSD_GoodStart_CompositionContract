"""Flatten only scene BASE storage and repair the accidental MDL path anchoring."""
import json
import os
from pathlib import Path
from pxr import Sdf, UsdUtils


def main():
    repo = Path(__file__).resolve().parents[1]
    package = repo / 'examples/01_LayeredScene'
    base = package / '020_BASE_LYR'
    moves = {path: base / (path.stem + '_Starter.usda') for path in (base/'Starter').glob('*.usda')}
    moves[base/'Scenarios/VariLyr.usda'] = base/'VariLyr_Scenarios.usda'
    if any(not old.exists() or new.exists() for old, new in moves.items()):
        raise RuntimeError('Unexpected layout; refusing overwrite.')
    for old in sorted(package.rglob('*.usda')):
        new = moves.get(old, old)
        source = Sdf.Layer.FindOrOpen(str(old))
        layer = Sdf.Layer.CreateAnonymous('.usda'); layer.TransferContent(source)
        def remap(path):
            if path == './OmniPBR.mdl': return 'OmniPBR.mdl'
            if not path or '://' in path or os.path.isabs(path) or not path.startswith('.'):
                return path
            resolved = (old.parent/path).resolve()
            target = moves.get(resolved, resolved)
            if new == old and target == resolved: return path
            result = Path(os.path.relpath(target, new.parent)).as_posix()
            return result if result.startswith('.') else './'+result
        UsdUtils.ModifyAssetPaths(layer, remap)
        data = dict(layer.customLayerData); omni = dict(data.get('omni_layer', {}))
        for key in ('locked', 'muteness'):
            if key in omni: omni[key] = {remap(path): value for path,value in omni[key].items()}
        if omni: data['omni_layer'] = omni
        layer.customLayerData = data
        layer.Export(str(new))
    for old in moves:
        if not old.resolve().is_relative_to(base.resolve()): raise RuntimeError('Unexpected source')
        old.unlink()
    replacements = {old.relative_to(package).as_posix():new.relative_to(package).as_posix() for old,new in moves.items()}
    for path in (package/'_contracts').glob('*.json'):
        text = path.read_text()
        for old,new in replacements.items(): text=text.replace(old,new)
        path.write_text(text,encoding='utf-8')
    # Empty directories only; no recursive removal.
    for folder in (base/'Starter',base/'Scenarios'):
        if folder.exists() and not any(folder.iterdir()): folder.rmdir()
    print('Flattened scene BASE folders and restored OmniPBR search identifier; no tests run.')


if __name__ == '__main__': main()
