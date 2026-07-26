#!/usr/bin/env python3
r"""Check that no restatement of the technology stack drops a category.

The stack is restated in a dozen tables here, and copies drift.
grovv-stack-scaffold.md's "Core Technology Stack Reference" is canonical; every
other stack table must carry at least its categories.

Only the CATEGORY names are compared, never the cell text - an agent definition
may compress a description the master directive spells out, which is editing,
not drift. So this does not verify that the tables agree: a copy naming Auth0
where canonical names Clerk passes. It verifies only that no category goes
missing, because a missing row silently deletes a default.

Extra categories pass: CLAUDE.md adds "AI CLI", VIBE.md and CODEX.md add "UI"
and "Testing". A rename still fails, since the old name goes missing - and the
extras print alongside so the rename reads clearly.

Two exemptions, both for content that describes a TARGET project rather than
grovv itself:

    fenced tables    an illustration of a generated project's document. A fence
                     is a quotation, never a statement of grovv's own defaults
    docs/prompts/    templates for a target's documents. A target's tech spec
                     says "Identity Management | Clerk", picking one option
                     where grovv lists the menu, so grovv's category vocabulary
                     does not apply

The second is path-shaped rather than content-shaped, so the run prints how many
tables it swallowed - a grovv-own table moved under docs/prompts goes unchecked,
but not unremarked.

Two limits worth stating. Tables are recognised by this repo's format, a leading
pipe on every row; a pipe-less GFM table is not seen. And a stack restated in
prose is not seen either - grovv-stack-scaffold.md and docs/prompts/
skills-builder.md both do that, and no table-shaped check can compare a sentence.

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

# The heading a stack table sits under: "Technology Stack", "Technology Stack
# Defaults", "Default Technology Stack", "Core Technology Stack Reference". This
# is the signal that survives row deletion - gut a table to four rows and the
# heading still says what it is - so the worse the drift, the surer the catch.
STACK_HEADING = re.compile(r"technology stack", re.IGNORECASE)
# Every stack table here is headed "| Category | ...". Requiring it keeps out the
# Sub-Agents tables (which name Frontend and Database as agent names) and the
# tech-spec Component tables, without needing a path rule for either.
STACK_COLUMN = "category"
# Fallback signal, for a stack table under some other heading: this many of the
# canonical categories named in one table. Five catches the abridged copies (the
# smallest real one names ten) while missing unrelated Category-headed tables
# (the nearest names one).
MIN_CANONICAL_ROWS = 5
# The canonical table carries thirteen rows. A table under the canonical heading
# with fewer than this is a note or a legend, not the canon - see canonical().
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

    Fenced blocks are skipped whole: a table inside one is quoted, and every
    quoted stack table in this repo illustrates a generated project's document.
    Headings inside a fence are ignored too, since a shell comment looks exactly
    like one."""
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
    """True when a table restates grovv's defaults and so must carry them all.

    Either signal suffices, and both require the Category column. Detecting on
    canonical row count alone would invert the incentive: a table that shed nine
    of thirteen rows would drop below the bar and stop being reported, so the
    worse the drift the greener the run."""
    return header.lower() == STACK_COLUMN and (
        bool(STACK_HEADING.search(heading))
        or len(canon & set(rows)) >= MIN_CANONICAL_ROWS
    )

def canonical() -> tuple[int, list[str]]:
    """Locate the canonical table by its heading, never by a hardcoded line.

    The first table under that heading is not trusted to be it. A legend or note
    table slipped in above would become the canon, every real stack table would
    then fall below the detection bar, and the run would report a pass with all
    the drift intact. Only a Category-headed table of real length qualifies."""
    lines = (REPO_ROOT / CANONICAL_DOC).read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        if CANONICAL_HEADING.match(line):
            for lineno, header, rows, _heading in tables(lines[i:]):
                if header.lower() == STACK_COLUMN and len(rows) >= MIN_CANONICAL_TABLE:
                    return i + lineno, rows
    raise SystemExit(
        f"{CANONICAL_DOC.as_posix()}: no table of at least {MIN_CANONICAL_TABLE} "
        "rows headed '| Category |' under a 'Core Technology Stack Reference' "
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
    # seeing the copies - a renamed heading, a change to the table format, a
    # canon that matched the wrong table - ends with nothing left to compare.
    if not checked:
        problems.append(
            f"{canon_at}: no stack table found anywhere but the canonical one - "
            "the check has lost its anchor and is verifying nothing"
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
          "target-project template(s) under docs/prompts/ exempt.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
