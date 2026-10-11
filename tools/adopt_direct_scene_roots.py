"""Bounded migration of the three original example wrappers to direct scene roots."""
import json
import hashlib
from pathlib import Path
from pxr import Sdf

repo = Path(__file__).resolve().parents[1]
package = repo / 'examples/01_LayeredScene'
archive = repo / 'harness/evidence/before_direct_scene_roots'
mapping = {
    'World_Manual.usda': ('ROOT_example.usda', []),
    'World_MaskedSize.usda': ('ROOT_example.usda', ['./050_REVIEW_LYR/MaskedSize/ReviewLyr.usda']),
    'World_MaskedSelection.usda': ('World_Scenarios.usda', ['./050_REVIEW_LYR/MaskedSelection/ReviewLyr.usda']),
}
if archive.exists():
    raise RuntimeError('Migration evidence already exists; inspect before repeating.')
layers = {}
for name, (base, review) in mapping.items():
    layer = Sdf.Layer.FindOrOpen(str(package / name))
    baseline = Sdf.Layer.FindOrOpen(str(package / base))
    if list(layer.subLayerPaths) != review + ['./' + base] or list(layer.rootPrims):
        raise RuntimeError(f'{name}: expected untouched wrapper; refusing overwrite.')
    candidate = Sdf.Layer.CreateAnonymous('.usda')
    candidate.TransferContent(baseline)
    candidate.subLayerPaths = review + list(baseline.subLayerPaths)
    data = dict(candidate.customLayerData)
    omni = dict(data.get('omni_layer', {}))
    locks = dict(omni.get('locked', {}))
    locks.update({path: True for path in review})
    omni['locked'] = locks
    data['omni_layer'] = omni
    candidate.customLayerData = data
    layers[name] = (layer, candidate)
archive.mkdir(parents=True)
records = {}
for name in [*mapping, '_contracts/profile.json', '_contracts/expected.json', '_pipeline_reports/build_manifest.json']:
    source = package / name
    destination = archive / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(source.read_bytes())
for name, (layer, candidate) in layers.items():
    layer.TransferContent(candidate)
    layer.Save()
    records[name] = {'sublayers': list(layer.subLayerPaths), 'sha256': hashlib.sha256((package / name).read_bytes()).hexdigest()}
profile_path = package / '_contracts/profile.json'
profile = json.loads(profile_path.read_text())
profile.pop('compatibility_alias', None)
profile['manual_entrypoint'] = 'World_Manual.usda; independent root with direct scene sublayers'
for name, record in records.items():
    profile['entrypoints_strongest_first'][name] = record['sublayers']
profile_path.write_text(json.dumps(profile, indent=2, sort_keys=True) + '\n')
expected_path = package / '_contracts/expected.json'
expected = expected_path.read_text().replace('compatibility alias of ROOT_example.usda', 'independent manual root; same baseline and direct stack as ROOT_example.usda')
expected_path.write_text(expected)
manifest_path = package / '_pipeline_reports/build_manifest.json'
manifest = json.loads(manifest_path.read_text())
manifest['subsequent_direct_root_migration'] = {
    'changes': records, 'prior_report': 'harness/evidence/before_direct_scene_roots/_pipeline_reports/build_manifest.json',
    'scope': 'Sdf-authored wrapper replacement; prior observations and file inventory are historical, not revalidated',
    'tests': 'not run', 'kit_acceptance': 'pending',
}
manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
print(json.dumps(records, indent=2))
