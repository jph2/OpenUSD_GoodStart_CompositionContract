#!/usr/bin/env python3
"""Refresh the contract skill; optionally install it or check freshness read-only.

Only this package's named files are written. No scene or contract is modified.
The semantic SKILL.md guidance must be reviewed by its maintainer before syncing.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import quote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
NAME = "openusd-composition-contract"
PACKAGE = ROOT / "skills" / NAME
REPOSITORY = "https://github.com/jph2/OpenUSD_GoodStart_CompositionContract"
MANIFEST = "references/source.json"


def text(path):
    # Stable across Windows/Git checkout newline conversions.
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")


def digest(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def contract_reference(contract, version):
    def rebase(match):
        target = match.group(2)
        parts = urlsplit(target)
        if parts.scheme or parts.netloc or target.startswith("#"):
            return match.group(0)
        destination = (ROOT / parts.path).resolve()
        if not destination.is_relative_to(ROOT):
            raise ValueError(f"Companion link escapes the repository: {target}")
        route = quote(destination.relative_to(ROOT).as_posix(), safe="/")
        suffix = ("?" + parts.query if parts.query else "")
        suffix += "#" + parts.fragment if parts.fragment else ""
        return f"{match.group(1)}{REPOSITORY}/blob/main/{route}{suffix})"

    # Rebase Markdown prose links only; preserve fenced examples verbatim.
    lines = []
    fence = None
    for line in contract.splitlines(keepends=True):
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            lines.append(line)
        elif fence:
            lines.append(line)
        else:
            lines.append(re.sub(r"(\[[^\]\n]+\]\()([^\s)]+)\)", rebase, line))
    banner = (
        f"> Generated reference for contract **{version}**. Edit the source repository's\n"
        "> `CompositionContract.md`, then run `tools/sync_composition_skill.py`.\n"
        "> Companion-file links point to the repository's mutable main branch for navigation;\n"
        "> they may differ from this snapshot or await publication. The bundled text and\n"
        "> `source.json` identify this skill's baseline. No scene fixtures are bundled.\n\n"
    )
    return banner + "".join(lines)


def expected_files():
    contract = text(ROOT / "CompositionContract.md")
    match = re.search(r"^\*\*Status:\*\* version (\d+\.\d+\.\d+),", contract, re.M)
    if not match:
        raise ValueError("Cannot find the contract's three-part Status version")
    version = match.group(1)
    skill = text(PACKAGE / "SKILL.md")
    skill, count = re.subn(r'^  version: "[^"\n]+"$', f'  version: "{version}"', skill, flags=re.M)
    if count != 1:
        raise ValueError("SKILL.md must contain exactly one metadata.version field")
    files = {
        "SKILL.md": skill,
        "agents/openai.yaml": text(PACKAGE / "agents/openai.yaml"),
        "references/CompositionContract.md": contract_reference(contract, version),
    }
    provenance = {
        "skill": NAME,
        "version": version,
        "contract_version": version,
        "source_repository": REPOSITORY,
        "source_file": "CompositionContract.md",
        "source_sha256": digest(contract),
        "hash_normalization": "UTF-8 without BOM, LF line endings",
        "reference_transform": "Generated notice; relative prose links rebased to repository main; contract prose and fenced examples retained",
        "rule_ids": re.findall(r"^\*\*(CC-\d{2}[a-z]?) —", contract, re.M),
        "files_sha256": {name: digest(content) for name, content in files.items()},
    }
    files[MANIFEST] = json.dumps(provenance, ensure_ascii=False, indent=2) + "\n"
    return version, files


def bounded_path(directory, relative):
    candidate = directory / relative
    if not candidate.resolve().is_relative_to(directory.resolve()):
        raise ValueError(f"Managed file resolves outside package: {candidate}")
    return candidate


def check_install_owner(directory):
    if not directory.exists() or not any(directory.iterdir()):
        return
    manifest = bounded_path(directory, MANIFEST)
    if not manifest.is_file():
        raise ValueError(f"Existing installation has no source manifest; reconcile it first: {directory}")
    previous = json.loads(text(manifest))
    if previous.get("skill") != NAME or previous.get("source_repository") != REPOSITORY:
        raise ValueError(f"Existing installation has a different owner: {directory}")
    # Installed edits belong back in the maintained package before overwriting.
    for relative in ("SKILL.md", "agents/openai.yaml", "references/CompositionContract.md"):
        path = bounded_path(directory, relative)
        recorded = previous.get("files_sha256", {}).get(relative)
        if path.exists() and digest(text(path)) != recorded:
            raise ValueError(f"Locally changed installed file; reconcile before syncing: {path}")


def synchronize(directory, files, check):
    stale = []
    for relative, content in files.items():
        path = bounded_path(directory, relative)
        if path.is_file() and text(path) == content:
            continue
        stale.append(relative)
        if not check:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
    label = "stale" if check else "updated"
    print(f"{directory}: {label} {len(stale)} file(s)")
    for relative in stale:
        print(f"  {relative}")
    return stale


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Read-only freshness comparison; exit 1 on drift")
    parser.add_argument("--install", action="store_true", help="Also synchronize the personal skill (compare only with --check)")
    parser.add_argument("--skills-root", type=Path, help="Personal skills directory; requires --install")
    args = parser.parse_args()
    if args.skills_root and not args.install:
        parser.error("--skills-root requires --install")
    try:
        version, files = expected_files()
        targets = [PACKAGE]
        if args.install:
            codex_directory = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")
            skills_directory = args.skills_root or codex_directory / "skills"
            installed = (skills_directory.expanduser() / NAME).resolve()
            if installed == PACKAGE.resolve():
                raise ValueError("Installation must be separate from the maintained skill")
            if not args.check:
                check_install_owner(installed)
            targets.append(installed)
        # Resolve all named outputs before any write. No cleanup/deletion occurs.
        for target in targets:
            for relative in files:
                bounded_path(target, relative)
        stale = []
        for target in targets:
            stale.extend(synchronize(target, files, args.check))
        print(f"Contract and skill version: {version}")
        return 1 if args.check and stale else 0
    except (OSError, ValueError) as error:
        print(f"Skill synchronization failed: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
