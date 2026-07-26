#!/usr/bin/env python3
r"""Check that no restatement of the technology stack drops a category.

The stack is restated in a dozen tables here, and copies drift.
grovv-stack-scaffold.md's "Core Technology Stack Reference" is canonical; every
other stack table must carry at least its categories.

Only CATEGORY names are compared, never cell text - a copy may compress a
description the master directive spells out, which is editing, not drift. So
this does not verify that the tables agree: a copy naming Auth0 where canonical
names Clerk passes. It verifies only that no category goes missing. Extras pass
(CLAUDE.md adds "AI CLI"), but a rename still fails, since the old name goes
missing, and the extras print alongside so the rename reads clearly.

Two exemptions, both for content describing a TARGET project, not grovv itself.
A fenced table is quoted, and every quoted stack table here illustrates a
generated project's document. docs/prompts/ holds templates for a target's
documents, whose "Identity Management | Clerk" picks one option where grovv
lists the menu; that one is path-shaped, so the run prints how many tables it
swallowed. Unseen: a pipe-less GFM table, since every row here leads with a
pipe, and a stack restated in prose, as grovv-stack-scaffold.md does.

Standard library only. Runs from anywhere: python3 .github/scripts/check_stack_tables.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

CANONICAL_DOC = Path("grovv-stack-scaffold.md")
CANONICAL_HEADING = re.compile(r"^#{2,}\s+Core Technology Stack Reference\s*$")
TEMPLATE_DIR = ("docs", "prompts")

DELIMITER = re.compile(r"^\s*\|[\s:|-]+\|\s*$")  # a table's |---|---| row
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
HEADING = re.compile(r"^#{1,6}\s+(.*?)\s*$")

# The heading a stack table sits under ("Technology Stack Defaults", "Core
# Technology Stack Reference"). This signal survives row deletion, so gutting a
# table cannot hide it - and gutting is the drift this check exists to catch.
STACK_HEADING = re.compile(r"technology stack", re.IGNORECASE)
# Every stack table here is headed "| Category | ...". Requiring it keeps out the
# Sub-Agents and tech-spec Component tables, which name Frontend and Database in
# passing, with no path rule for either.
STACK_COLUMN = "category"
# Fallback signal, for a stack table under some other heading. Five catches the
# abridged copies (the smallest real one names ten) and misses unrelated
# Category-headed tables (the nearest names one).
MIN_CANONICAL_ROWS = 5
# The canonical table carries thirteen rows; a shorter one under that heading is
# a note or a legend, not the canon - see canonical().
MIN_CANONICAL_TABLE = 8


def is_vendored_harness(parts: tuple[str, ...]) -> bool:
    """True for anything under a skills/harness/ tree (Apache-2.0, verbatim)."""
    return any(parts[i : i + 2] == ("skills", "harness") for i in range(len(parts)))

def markdown_files(root: Path):
    for path in sorted(root.rglob("*.md")):
        parts = path.relative_to(root).parts
        if ".git" not in parts and not is_vendored_harness(parts):
            yield path, parts

def label(row: str) -> str:
    """The first cell of a table row, stripped of bold markers."""
    return row.strip().strip("|").split("|")[0].strip().strip("*").strip()

def tables(lines: list[str]):
    """Yield (lineno, header, row_labels, heading) per table outside a fence.

    Headings inside a fence are skipped too - a shell comment looks like one."""
    i, in_fence, heading = 0, False, ""
    while i < len(lines):
        step = 1
        if FENCE.match(lines[i]):
            in_fence = not in_fence
        elif not in_fence:
            found = HEADING.match(lines[i])
            if found:
                heading = found.group(1)
            end = i
            while end < len(lines) and lines[end].lstrip().startswith("|"):
                end += 1
            if end - i >= 3 and DELIMITER.match(lines[i + 1]):
                rows = [label(row) for row in lines[i + 2 : end]]
                yield i + 1, label(lines[i]), rows, heading
            step = max(end - i, 1)
        i += step

def is_stack_table(header: str, rows: list[str], heading: str, canon: set) -> bool:
    """True when a table restates grovv's defaults, so must carry them all.

    Either signal suffices; both need the Category column. Detecting on canonical
    row count alone would invert the incentive - a table that shed nine of
    thirteen rows would fall below the bar and stop being reported."""
    return header.lower() == STACK_COLUMN and (
        bool(STACK_HEADING.search(heading))
        or len(canon & set(rows)) >= MIN_CANONICAL_ROWS
    )

def canonical() -> tuple[int, list[str]]:
    """Locate the canonical table by its heading, never by a hardcoded line.

    The first table under that heading is not trusted to be it. A legend slipped
    in above would become the canon, every real stack table would then fall below
    the detection bar, and the run would report a pass with the drift intact."""
    lines = (REPO_ROOT / CANONICAL_DOC).read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        if CANONICAL_HEADING.match(line):
            for lineno, header, rows, _heading in tables(lines[i:]):
                if header.lower() == STACK_COLUMN and len(rows) >= MIN_CANONICAL_TABLE:
                    return i + lineno, rows
    raise SystemExit(
        f"{CANONICAL_DOC.as_posix()}: no '| Category |' table of at least "
        f"{MIN_CANONICAL_TABLE} rows under a 'Core Technology Stack Reference' "
        "heading - the canonical stack table cannot be located"
    )


def main() -> int:
    canon_line, canon_rows = canonical()
    canon, canon_at = set(canon_rows), f"{CANONICAL_DOC.as_posix()}:{canon_line}"
    problems: list[str] = []
    checked = exempt = 0

    for path, parts in markdown_files(REPO_ROOT):
        rel = path.relative_to(REPO_ROOT).as_posix()
        lines = path.read_text(encoding="utf-8").splitlines()
        for lineno, header, rows, heading in tables(lines):
            if not is_stack_table(header, rows, heading, canon):
                continue
            if parts[:2] == TEMPLATE_DIR:
                exempt += 1  # A target-project template - see module docstring.
                continue
            if (rel, lineno) == (CANONICAL_DOC.as_posix(), canon_line):
                continue
            checked += 1
            missing = [row for row in canon_rows if row not in rows]
            extra = [row for row in rows if row not in canon]
            if missing:
                problems.append(
                    f"{rel}:{lineno}: stack table (under '{heading}') is missing "
                    f"{len(missing)} category row(s) that {canon_at} carries\n"
                    f"    missing: {', '.join(missing)}"
                    + (f"\n    extra here (allowed; shown in case a category was "
                       f"renamed, not dropped): {', '.join(extra)}" if extra else "")
                )

    # Coverage collapse must never read as a pass. Every way this check can stop
    # seeing the copies - a renamed heading, a changed table format, a canon
    # matched against the wrong table - ends with nothing left to compare.
    if not checked:
        problems.append(
            f"{canon_at}: no stack table found anywhere but the canonical one - "
            "the check has lost its anchor and is verifying nothing\n"
            "    a stack table is a '| Category |' table under a heading naming "
            "the technology stack; if that convention changed, change this script"
        )

    if problems:
        print(f"Stack table check FAILED - {len(problems)} problem(s):\n")
        print("\n".join(problems))
        print(f"\nFix: {canon_at} is canonical. Add the missing category rows to "
              "the offending table, wording each cell to suit that document - only "
              "the category names must match, not the descriptions.")
        return 1

    print(f"Stack table check passed - {checked} stack table(s) carry every "
          f"category in {canon_at} ({len(canon_rows)} categories); {exempt} "
          "docs/prompts/ target-project template(s) exempt.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
