#!/usr/bin/env python3
r"""Check that the derived tool directories stay in sync with canonical .grovv.

.grovv/ is the single source of truth; .claude/, .vibe/ and .codex/ are derived.

    a  skills/harness/**        byte-identical everywhere (vendored Apache-2.0)
    b  agents/*.md              identical to .grovv once the tool path prefixes
                                and ${*_PLUGIN_ROOT} variables are normalized,
                                and one optional tool-specific section is excised
    c  tier b + the kickoff     present in all four trees
       skills/grovv/SKILL.md

The kickoff skill is tier c only, never tier b: it carries genuine per-tool
instruction, so its copies are adapted rather than derived. See derived_targets.

A tier b file may carry at most one "## <Tool>-Specific ..." section, fenced by
five-dash rules like every other section here. Everything outside it is still
compared, so the exemption cannot hide drift.

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
# The matching plugin-root variables. Each tree names its own, so this is
# sanctioned variation rather than drift, and normalizing only the path prefix
# would report every correct file as broken.
TOOL_ROOT_VAR = re.compile(r"\$\{(?:CLAUDE|VIBE|CODEX|GROVV)_PLUGIN_ROOT\}")
# The one sanctioned escape hatch: a trailing per-tool section, e.g.
# "## Vibe-Specific Notes". Everything from it to end of file is exempt.
TOOL_SECTION = re.compile(r"^#{2,}\s+\S+-Specific\b", re.IGNORECASE)
# A five-dash horizontal rule, this repo's section separator.
RULE = re.compile(r"^-{5,}\s*$")
PLACEHOLDER, ROOT_VAR_PLACEHOLDER = "<TOOL>/", "${<TOOL>_PLUGIN_ROOT}"
EOF = "<end of file>"

HARNESS_WHY = (
    "differs from the vendored canonical copy - harness is Apache-2.0 and must "
    "stay byte-identical (never hand-edited)"
)


def lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8", errors="replace").splitlines()

def normalize(text: list[str]) -> list[str]:
    return [
        TOOL_ROOT_VAR.sub(ROOT_VAR_PLACEHOLDER, TOOL_PREFIX.sub(PLACEHOLDER, line))
        for line in text
    ]

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


def derived_targets() -> list[str]:
    """Tier b targets, named relative to a tree root. Agent names are the union
    across all four trees so a file only one tree has is still a target.

    An agent's shared body is the same document in all four trees, differing
    only by paths. A tree may carry ONE tool-specific section (see TOOL_SECTION)
    for genuine per-tool instruction, such as .vibe telling the agent to spawn
    subagents with Vibe's task tool. That section is excised before comparison;
    everything outside it, including the footer that follows it, is compared.

    skills/grovv/SKILL.md is deliberately NOT here. The kickoff skill carries
    real per-tool instruction - Vibe spawns subagents with its task tool where
    Claude Code uses Agent, and each tree names its own context file - so the
    copies are adapted, not derived. Comparing them would report correct files
    as broken, and "fixing" that would delete the guidance. It is still held to
    tier c: it must exist in all four trees."""
    names = {
        p.name
        for tree in (CANONICAL, *TOOLS)
        for p in (REPO_ROOT / tree / AGENTS).glob("*.md")
    }
    return [f"{AGENTS}/{name}" for name in sorted(names)]


def presence_targets() -> list[str]:
    """Tier c targets - every tier b file, plus the per-tool kickoff skill."""
    return derived_targets() + [SKILL]


def shared_body(text: list[str], path: Path, problems: list[str]) -> list[str]:
    """The part of a derived file that must match canonical.

    One tool-specific section is allowed. It is excised - from its heading to
    the rule that closes it - rather than truncated to end of file, so the
    document still ends in the five-dash rule and footer every document here
    ends in, and so nothing after the section escapes comparison. Allowing more
    than one would turn the heading into a hiding place for real drift."""
    hits = [i for i, line in enumerate(text) if TOOL_SECTION.match(line)]
    if not hits:
        return text
    if len(hits) > 1:
        problems.append(
            f"{rel(path)}:{hits[1] + 1}: a second tool-specific section - a "
            "derived file may append at most one"
        )

    # A section sits between two five-dash rules. Excise from the opening rule
    # up to (not including) the closing one, so exactly one rule survives and
    # the file still ends "-----" then footer, as canonical does.
    start = hits[0]
    end = next(
        (i for i in range(start + 1, len(text)) if RULE.match(text[i])), len(text)
    )
    while start and not text[start - 1].strip():
        start -= 1
    if start and RULE.match(text[start - 1]):
        start -= 1  # The blank line before this rule belongs to the shared body.
    return text[:start] + text[end:]


def check_derived(problems: list[str]) -> None:
    """Tier b - agent definitions match .grovv after path substitution."""
    for tool in TOOLS:
        for target in derived_targets():
            canon_path, tool_path = REPO_ROOT / CANONICAL / target, REPO_ROOT / tool / target
            if not canon_path.is_file() or not tool_path.is_file():
                continue  # check_presence names every absent target by path.
            raw = (
                shared_body(lines(canon_path), canon_path, problems),
                shared_body(lines(tool_path), tool_path, problems),
            )
            cmp_pair = (normalize(raw[0]), normalize(raw[1]))
            if cmp_pair[0] != cmp_pair[1]:
                why = (
                    f"differs from canonical {rel(canon_path)} beyond tool path "
                    "substitution"
                )
                problems.append(report(tool_path, why, cmp_pair, raw))


def check_presence(problems: list[str]) -> None:
    """Tier c - every tier b target exists in .grovv and in all three tool dirs.

    Without this, deleting a derived file would remove a tier b comparison and
    make the run report fewer problems - a missing plugin entry point reading
    as a greener build."""
    trees = (CANONICAL, *TOOLS)
    for target in presence_targets():
        present = [t for t in trees if (REPO_ROOT / t / target).is_file()]
        if not present:
            problems.append(
                f"{target}: missing from every tree ({', '.join(trees)}) - "
                "every derived file must exist in all four"
            )
            continue
        for tree in trees:
            if tree not in present:
                problems.append(
                    f"{tree}/{target}: missing - present in "
                    f"{', '.join(present)}; every derived file must exist in "
                    "all four trees"
                )


def main() -> int:
    problems: list[str] = []
    check_harness(problems)
    check_derived(problems)
    check_presence(problems)

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
