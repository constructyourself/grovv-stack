#!/usr/bin/env python3
r"""Check that the derived tool directories stay in sync with canonical .grovv.

.grovv/ is the single source of truth; .claude/, .vibe/ and .codex/ are derived.

    a  skills/harness/**        byte-identical everywhere (vendored Apache-2.0)
    b  agents/*.md,             identical to .grovv once the tool path prefixes
       skills/grovv/SKILL.md    (.claude/ .vibe/ .codex/ .grovv/) are normalized
    c  agents/ file set         same agent files present in all four trees

Standard library only. Runs from anywhere: python3 .github/scripts/check_tool_sync.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

CANONICAL, TOOLS = ".grovv", (".claude", ".vibe", ".codex")
HARNESS, SKILL, AGENTS = "skills/harness", "skills/grovv/SKILL.md", "agents"

# Any of the four tool path prefixes, wherever it appears in a line.
TOOL_PREFIX = re.compile(r"\.(?:claude|vibe|codex|grovv)/")
PLACEHOLDER, EOF = "<TOOL>/", "<end of file>"

HARNESS_WHY = (
    "differs from the vendored canonical copy - harness is Apache-2.0 and must "
    "stay byte-identical (never hand-edited)"
)


def lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8", errors="replace").splitlines()

def normalize(text: list[str]) -> list[str]:
    return [TOOL_PREFIX.sub(PLACEHOLDER, line) for line in text]

def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()

def at(text: list[str], lineno: int) -> str:
    return text[lineno - 1].strip()[:120] if lineno <= len(text) else EOF

def files_under(root: Path) -> dict[Path, Path]:
    return {p.relative_to(root): p for p in root.rglob("*") if p.is_file()}


def report(tool_path: Path, why: str, cmp_pair, raw_pair) -> str:
    """Locate the first difference in cmp_pair (possibly normalized), then quote
    raw_pair at that line so the reader sees the text as it is on disk."""
    canon, other = cmp_pair
    for lineno, (a, b) in enumerate(zip(canon, other), 1):
        if a != b:
            break
    else:  # Equal as far as both go - the difference is trailing lines.
        lineno = min(len(canon), len(other)) + 1
    return (
        f"{rel(tool_path)}:{lineno}: {why}\n"
        f"    {CANONICAL}: {at(raw_pair[0], lineno)}\n"
        f"    {tool_path.relative_to(REPO_ROOT).parts[0]}: {at(raw_pair[1], lineno)}"
    )


def check_harness(problems: list[str]) -> None:
    """Tier a - the vendored harness tree must be byte-identical everywhere."""
    canon_root = REPO_ROOT / CANONICAL / HARNESS
    if not canon_root.is_dir():
        problems.append(f"{CANONICAL}/{HARNESS}: canonical harness tree is missing")
        return

    canon_files = files_under(canon_root)
    for tool in TOOLS:
        tool_files = files_under(REPO_ROOT / tool / HARNESS)
        for name in sorted(set(canon_files) | set(tool_files), key=str):
            canon_path, tool_path = canon_files.get(name), tool_files.get(name)
            if tool_path is None:
                problems.append(
                    f"{tool}/{HARNESS}/{name.as_posix()}: missing - vendored file "
                    f"present in {rel(canon_path)}"
                )
            elif canon_path is None:
                problems.append(
                    f"{rel(tool_path)}: not present in {CANONICAL}/{HARNESS} - "
                    "the vendored tree must not gain files"
                )
            elif canon_path.read_bytes() != tool_path.read_bytes():
                pair = (lines(canon_path), lines(tool_path))
                problems.append(report(tool_path, HARNESS_WHY, pair, pair))


def check_derived(problems: list[str]) -> None:
    """Tier b - agents and the grovv skill match .grovv after path substitution."""
    canon_agents = sorted((REPO_ROOT / CANONICAL / AGENTS).glob("*.md"))
    targets = [f"{AGENTS}/{p.name}" for p in canon_agents] + [SKILL]

    for tool in TOOLS:
        for target in targets:
            canon_path, tool_path = REPO_ROOT / CANONICAL / target, REPO_ROOT / tool / target
            if not canon_path.is_file() or not tool_path.is_file():
                continue  # Tier c reports presence problems.
            raw = (lines(canon_path), lines(tool_path))
            cmp_pair = (normalize(raw[0]), normalize(raw[1]))
            if cmp_pair[0] != cmp_pair[1]:
                why = (
                    f"differs from canonical {rel(canon_path)} beyond tool path "
                    "substitution"
                )
                problems.append(report(tool_path, why, cmp_pair, raw))


def check_agent_parity(problems: list[str]) -> None:
    """Tier c - the same agent files exist in all four trees."""
    trees = {
        tree: {p.name for p in (REPO_ROOT / tree / AGENTS).glob("*.md")}
        for tree in (CANONICAL, *TOOLS)
    }
    for name in sorted(set().union(*trees.values())):
        absent = sorted(t for t, names in trees.items() if name not in names)
        if absent:
            present = sorted(t for t, names in trees.items() if name in names)
            problems.append(
                f"{AGENTS}/{name}: present in {', '.join(present)} but missing from "
                f"{', '.join(absent)} - every agent must exist in all four trees"
            )


def main() -> int:
    problems: list[str] = []
    check_harness(problems)
    check_derived(problems)
    check_agent_parity(problems)

    if problems:
        print(f"Tool sync check FAILED - {len(problems)} problem(s):\n")
        print("\n".join(problems))
        print(f"\nFix: {CANONICAL}/ is canonical. Re-derive the offending file "
              "from it, changing only the tool path prefix.")
        return 1

    print(f"Tool sync check passed - {', '.join(TOOLS)} match {CANONICAL}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
