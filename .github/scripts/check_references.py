#!/usr/bin/env python3
r"""Check that paths naming this repo's own files actually exist.

A prompt file was renamed and references to the old path survived in many
documents, each one silently pointing at nothing. Nothing caught it.

The hard part is knowing which paths this repo is answerable for: these
documents also name files the scaffolder CREATES IN A TARGET PROJECT, which
must NOT exist here. That output mirrors this repo's shape, so nothing
structural separates the two and no inference should try - OWNED_TREES and
OWNED_DIRS name what is ours, literally, and the rest goes unjudged. Every
message says how much that was.

Standard library only. Runs from anywhere:

    python3 .github/scripts/check_references.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# Excluding fenced content is what keeps this check usable: a fence here is
# illustrative - a tree of a project that does not exist yet, a shell command.
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
INLINE_CODE = re.compile(r"`+([^`]+)`+")
LINK_TARGET = re.compile(r"\]\(([^)\s]+)\)")
# A trailing ":41" or ":60-73" comes off first. The line number is deliberately
# NOT verified - documents grow, and a reference to a moved line is still valid.
LINE_SUFFIX = re.compile(r":\d+(?:-\d+)?$")
# What a repo-rooted path may contain, in full: no whitespace (a span holding a
# shell command is never read as a path), no "*" glob, no {name}/<tool>
# placeholder, no "#", no surviving ":" (URL schemes, "main:.claude/agents/x.md").
# The required "/" drops bare filenames - `CLAUDE.md` names this repo's file, a
# tool tree's, or a generated project's, depending on the sentence.
PATH_SHAPE = re.compile(r"[\w.@+-]+(?:/[\w.@+-]+)+")
# Requiring an extension drops directory references: a directory this repo names
# may legitimately be absent, gitignored (prototypes/) or owned by a target.
EXTENSION = re.compile(r"\.[A-Za-z0-9]+$")
HEADING = re.compile(r"^##\s+(.*?)\s*$")

# Whole subtrees only this repo has, matched by prefix.
OWNED_TREES = (
    ".claude-plugin/",  # plugin packaging; a scaffolded project never gets one
    ".github/",         # this repo's CI; no step writes into a target's .github/
    ".grovv/",          # the canonical tool tree; only this repo has one
)
# Owned at their own level only, because paths BELOW them are ambiguous:
# docs/prompts/tech-spec.md:431 tells a TARGET to keep prompts in
# docs/prompts/skills/, and the agents/ and skills/ subtrees under the tool
# roots are the shape team-design and skills-builder write into a target.
# check_tool_sync.py already holds those subtrees to presence in all four trees.
OWNED_DIRS = ("docs/prompts", ".claude", ".vibe", ".codex")

# Regions discussing the file set at another point in time, where a name
# resolving to nothing is the subject, not the defect. Measured, not assumed:
# docs/architecture/ names 13 absent files and every one is correct - a note on
# another branch, a file a plan proposes, a prompt renamed away. A Decision Log
# entry records that A became B; "correcting" A leaves "B became B".
NARRATIVE_DIRS = ("docs/architecture",)
NARRATIVE_SECTION = "Decision Log"
SKIP_DIR = ".git"

SCOPE = (
    "Judged: inline code spans and link targets, outside fenced code, under "
    + ", ".join(OWNED_TREES + tuple(d + "/" for d in OWNED_DIRS))
    + " (that second group at its own level only). Not judged: everything else, "
    "including docs/architecture/ and Decision Log sections."
)


def is_vendored_harness(parts: tuple[str, ...]) -> bool:
    """True for anything under a skills/harness/ tree (Apache-2.0, verbatim)."""
    return any(parts[i : i + 2] == ("skills", "harness") for i in range(len(parts)))


def markdown_files(root: Path):
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        if SKIP_DIR in rel.parts or is_vendored_harness(rel.parts):
            continue
        if not rel.as_posix().startswith(NARRATIVE_DIRS):
            yield path


def is_ours(bare: str) -> bool:
    """True when a reference names a file this repo is answerable for.

    Literal text, never inferred from disk: "judge it if that directory exists
    and holds files like it" is switched OFF by the very change it should catch,
    and one stray file in docs/ would arm it over dozens of correct targets."""
    return bare.startswith(OWNED_TREES) or bare.rpartition("/")[0] in OWNED_DIRS


def candidates(raw: str):
    for token in INLINE_CODE.findall(raw) + LINK_TARGET.findall(raw):
        written = token.strip()
        bare = LINE_SUFFIX.sub("", written)
        shaped = PATH_SHAPE.fullmatch(bare) and EXTENSION.search(bare)
        if shaped and ".." not in bare.split("/"):  # Never leave the repo.
            yield written, bare


def where(target: Path) -> str:
    """What is at the reference's parent, so the fix needs no digging."""
    parent, shown = target.parent, target.parent.relative_to(REPO_ROOT).as_posix()
    if not parent.is_dir():
        return f"{shown}/ does not exist either - that directory moved or went away"
    held = sorted(p.name for p in parent.iterdir() if p.suffix == target.suffix)
    return f"{shown}/ holds: {', '.join(held)[:200] or 'no file of that kind'}"


def references(path: Path):
    """Yield (lineno, written, bare, raw) for every path this check looks at."""
    fence_marker: str | None = None
    narrative = False
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        opener = FENCE.match(raw)
        if opener:
            marker = opener.group(1)[0]
            if fence_marker is None:
                fence_marker = marker
            elif fence_marker == marker:
                fence_marker = None
            continue
        if fence_marker is not None:
            continue
        # Tested after the fence guard, so a heading quoted inside a fenced
        # template cannot switch off the rest of a real document.
        head = HEADING.match(raw)
        if head:
            narrative = head.group(1) == NARRATIVE_SECTION
        if narrative:
            continue
        for written, bare in candidates(raw):
            yield lineno, written, bare, raw


def main() -> int:
    problems: list[str] = []
    scanned = judged = seen = 0
    for path in markdown_files(REPO_ROOT):
        scanned += 1
        rel = path.relative_to(REPO_ROOT).as_posix()
        for lineno, written, bare, raw in references(path):
            seen += 1
            if not is_ours(bare):
                continue
            judged += 1
            target = REPO_ROOT / bare
            if target.exists():
                continue
            problems.append(
                f"{rel}:{lineno}: names {written!r}, which does not exist\n"
                f"    {raw.strip()[:160]}\n"
                f"    {where(target)}"
            )

    if problems:
        print(f"Reference check FAILED - {len(problems)} dangling reference(s):\n")
        print("\n".join(problems))
        print("\nFix: point each reference at the file's current path, or drop it "
              "if the file is gone - then grep the repo for the old path, because "
              f"unjudged regions may name it too and go unreported.\n{SCOPE}")
        return 1

    print(f"Reference check passed - {judged} of {seen} repo-rooted path(s) across "
          f"{scanned} Markdown file(s) resolve; {seen - judged} not judged.\n{SCOPE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
