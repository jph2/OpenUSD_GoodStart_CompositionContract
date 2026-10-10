"""Package the authored starter for offline Windows setup; does not run tests."""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile

REPO = Path(__file__).resolve().parents[1]
SOURCE = REPO / 'examples/01_LayeredScene'
OUTPUT = REPO / 'starter/Composition_Starter_0.1.1'


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    files = {}
    for path in sorted(SOURCE.rglob('*')):
        if not path.is_file():
            continue
        relative = path.relative_to(SOURCE).as_posix()
        if relative.startswith('_pipeline_reports/') or '__pycache__' in path.parts:
            continue
        files[relative] = path.read_bytes()
    # The portable bundle opens the generous master by default.
    files['Open_In_Kit.ps1'] = files['Open_In_Kit.ps1'].replace(
        b"[string]$Scene = 'Standard'", b"[string]$Scene = 'STARTER'")
    for name in ('CompositionContracts.md', 'PROJECT_STRUCTURE.md'):
        files['_contracts/reference/' + name] = (REPO / name).read_bytes()
    files['_pipeline_reports/README.md'] = (
        '# Preset provenance\n\nThis bundle copies authored files; packaging is not USD or Kit acceptance. '
        'The source example\'s historical build report is deliberately excluded. '
        'Inventory hashes describe the packaged bytes only. Optional roles are empty authoring slots.\n'
    ).encode()
    files['_pipeline_reports/preset_inventory.json'] = json.dumps({
        'version': '0.1.1', 'scope': 'packaging inventory, not acceptance evidence',
        'files': {name: {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
                  for name, data in sorted(files.items())},
    }, indent=2).encode()
    archive = OUTPUT / 'Composition_Starter.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as package:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 10, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            package.writestr(info, data)
    for name in ('Create_Composition_Project.bat', 'Create_Composition_Project.ps1'):
        shutil.copyfile(REPO / 'tools/setup' / name, OUTPUT / name)
    shutil.copyfile(REPO / 'tools/setup/README_SETUP.md', OUTPUT / 'README_SETUP.md')
    print(f'Packaged {len(files)} files: {archive}')


if __name__ == '__main__':
    main()
