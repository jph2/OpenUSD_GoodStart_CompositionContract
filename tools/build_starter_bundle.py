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
    files['START_HERE.md'] = (
        '# Composition Contracts starter 0.1.1\n\n'
        'Open `SceneROOT_STARTER.usda` using `Open_In_Kit.ps1` (defaults to STARTER in this bundle). '
        'The launcher needs an existing compatible Kit installation; provide -KitExe and -AppConfig '
        'if it cannot detect a running Kit application. It installs no applications.\n\n'
        'Opinion is the default editable target; other persistent layers are protected. '
        'Save retains Opinion edits. Demo roots share their own Opinion; Starter is independent. '
        'Starter includes demo assets and optional layer slots: remove or mute what you do not need. '
        'See README.md for details. Source-repository links in copied documentation may require '
        'https://github.com/jph2/OpenUSD_Composition_Contracts .\n\n'
        'Keep asset/resource paths relative and copy the whole package for an independent project. '
        'Contracts are in `_contracts/reference`. This project was developed with AI assistance, '
        'including OpenAI Codex; human review and verification remain required.\n'
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
    (OUTPUT / 'README_SETUP.md').write_text(
        '# Portable setup\n\nCopy this entire folder into the intended project location. '
        'Keep the BAT, PS1 and ZIP together. Double-click Create_Composition_Project.bat. '
        'It expands the preset beside itself. To choose another destination, run '
        '`Create_Composition_Project.ps1 -Destination "E:\\Projects\\MyWorkcell"`.\n\n'
        'Windows PowerShell is required; Python, network access and administrator rights are not. '
        'Existing destination files stop setup before extraction; never rerun over edited work. '
        'After extraction, read START_HERE.md and launch Open_In_Kit.ps1. '
        'The setup does not install Omniverse, physics solvers or runtime connectors.\n', encoding='utf-8')
    print(f'Packaged {len(files)} files: {archive}')


if __name__ == '__main__':
    main()
