#!/usr/bin/env python3
r"""Check that the repo states one version, not three.

Three places carry the version and must agree:

    .claude-plugin/plugin.json   the manifest Claude Code actually reads
    plugin.json                  the root documentation manifest
    MEMORY.md                    the version quoted in Current State prose

Standard library only. Run from anywhere:

    python3 .github/scripts/check_versions.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

PLUGIN_MANIFEST = Path(".claude-plugin/plugin.json")
ROOT_MANIFEST = Path("plugin.json")
MEMORY = Path("MEMORY.md")

CURRENT_STATE = re.compile(r"^##\s+Current State\s*$")
NEXT_HEADING = re.compile(r"^##\s+")
SEMVER_IN_PROSE = re.compile(r"\bv(\d+\.\d+\.\d+)\b")


def manifest_version(rel: Path) -> tuple[str | None, str]:
    """Return (version, source) for a JSON manifest, or (None, reason)."""
    path = REPO_ROOT / rel
    if not path.is_file():
        return None, f"{rel.as_posix()}: file not found"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, f"{rel.as_posix()}:{exc.lineno}: invalid JSON - {exc.msg}"
    version = data.get("version")
    if not isinstance(version, str) or not version:
        return None, f'{rel.as_posix()}: no string "version" key'
    return version, f"{rel.as_posix()} (version)"


def memory_version() -> tuple[str | None, str]:
    """Return (version, source) for the Current State prose, or (None, reason)."""
    path = REPO_ROOT / MEMORY
    if not path.is_file():
        return None, f"{MEMORY.as_posix()}: file not found"

    lines = path.read_text(encoding="utf-8").splitlines()
    start = next((i for i, line in enumerate(lines) if CURRENT_STATE.match(line)), None)
    if start is None:
        return None, f"{MEMORY.as_posix()}: no '## Current State' heading"

    for offset, line in enumerate(lines[start + 1 :], start=start + 2):
        if NEXT_HEADING.match(line):
            break
        match = SEMVER_IN_PROSE.search(line)
        if match:
            return match.group(1), f"{MEMORY.as_posix()}:{offset} (Current State prose)"

    return None, (
        f"{MEMORY.as_posix()}:{start + 1}: no vX.Y.Z version stated under "
        "'## Current State'"
    )


def main() -> int:
    readings = [
        manifest_version(PLUGIN_MANIFEST),
        manifest_version(ROOT_MANIFEST),
        memory_version(),
    ]

    missing = [source for version, source in readings if version is None]
    if missing:
        print("Version check FAILED - could not read a version:\n")
        for reason in missing:
            print(f"  {reason}")
        return 1

    versions = {version for version, _ in readings}
    if len(versions) > 1:
        print("Version check FAILED - the three version statements disagree:\n")
        for version, source in readings:
            print(f"  {version:<12} {source}")
        print(
            "\nFix: pick the intended version and set it in all three places. "
            "The manifests must match each other exactly, and MEMORY.md's "
            "Current State prose must quote the same value."
        )
        return 1

    print(f"Version check passed - all three sources state {versions.pop()}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
