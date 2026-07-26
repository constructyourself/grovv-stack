#!/usr/bin/env python3
r"""Check that every restatement of the technology stack lists the same categories.

The stack is restated in a dozen tables here, and copies drift.
grovv-stack-scaffold.md's "Core Technology Stack Reference" is canonical; every
other stack table must carry at least its categories. Only the CATEGORY set is
compared, never the cell text - an agent definition may compress a description
the master directive spells out, which is editing, not drift. A missing category
is drift: it silently deletes a default.

Extra categories pass: CLAUDE.md adds "AI CLI", VIBE.md and CODEX.md add "UI" and
"Testing". A rename still fails, since the old name goes missing - and the extras
print alongside so the rename reads clearly.

Tables under docs/prompts/ are exempt: they are TEMPLATES for a generated target
project's documents, not grovv's own defaults. A target's tech spec says
"Identity Management | Clerk", picking one option where grovv lists the menu, so
grovv's category vocabulary does not apply to them.

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

# A table is a stack table when its rows name this many canonical categories -
# structural, so a new copy is covered without being listed here. Five catches
# the abridged copies (the smallest real one names ten) while missing unrelated
# Category-headed tables (the nearest names one). A table that shed nine of
# thirteen rows falls below the bar, but that is a rewrite, not row-at-a-time
# drift.
MIN_CANONICAL_ROWS = 5

# Vendor names from the canonical table, used only to spot prose restatements.
TECHNOLOGIES = (
    "TypeScript Go Node.js PostgreSQL SQLite Neon Supabase Clerk Astro Next.js "
    "React shadcn/ui Tailwind Resend Plunk Stripe Lago PostHog Vercel Docker"
).split()
TECH = [re.compile(rf"(?<![\w./]){re.escape(n)}(?![\w.])") for n in TECHNOLOGIES]
# The two real prose restatements name seventeen technologies on one line; the
# nearest incidental mention names six. Ten sits in that gap, so merely
# discussing the stack in a sentence does not trip this.
MIN_PROSE = 10


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
    """Yield (lineno, header, row_labels) for every Markdown table in the text."""
    i = 0
    while i < len(lines):
        end = i
        while end < len(lines) and lines[end].lstrip().startswith("|"):
            end += 1
        if end - i >= 3 and DELIMITER.match(lines[i + 1]):
            yield i + 1, label(lines[i]), [label(r) for r in lines[i + 2 : end]]
        i = max(end, i + 1)

def canonical() -> tuple[int, list[str]]:
    """Locate the canonical table by its heading, never by a hardcoded line."""
    lines = (REPO_ROOT / CANONICAL_DOC).read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        if CANONICAL_HEADING.match(line):
            for lineno, _header, rows in tables(lines[i:]):
                return i + lineno, rows
    raise SystemExit(
        f"{CANONICAL_DOC.as_posix()}: no table under a 'Core Technology Stack "
        "Reference' heading - the canonical stack table cannot be located"
    )

def prose_copies(lines: list[str], rel: str) -> list[str]:
    """Sentences that restate the stack. Reported, never failed - see main()."""
    found, in_fence = [], False
    for lineno, raw in enumerate(lines, 1):
        if FENCE.match(raw):
            in_fence = not in_fence
        elif not in_fence and not raw.lstrip().startswith("|"):
            hits = sum(1 for pattern in TECH if pattern.search(raw))
            if hits >= MIN_PROSE:
                found.append(
                    f"  {rel}:{lineno}: names {hits} stack technologies in prose, "
                    f"so no table-shaped check can verify it\n"
                    f"      {raw.strip()[:140]}"
                )
    return found


def main() -> int:
    canon_line, canon_rows = canonical()
    canon, canon_at = set(canon_rows), f"{CANONICAL_DOC.as_posix()}:{canon_line}"
    problems: list[str] = []
    notes: list[str] = []  # Prose copies - printed, never fatal. See the summary.
    checked = exempt = 0

    for path, parts in markdown_files(REPO_ROOT):
        rel = path.relative_to(REPO_ROOT).as_posix()
        lines = path.read_text(encoding="utf-8").splitlines()
        notes.extend(prose_copies(lines, rel))

        for lineno, header, rows in tables(lines):
            if len(canon & set(rows)) < MIN_CANONICAL_ROWS:
                continue  # Not a stack table.
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
                    f"{rel}:{lineno}: stack table (| {header} | ...) is missing "
                    f"{len(missing)} category row(s) that {canon_at} carries\n"
                    f"    missing: {', '.join(missing)}"
                    + (f"\n    extra here (allowed; shown in case a category was "
                       f"renamed, not dropped): {', '.join(extra)}" if extra else "")
                )

    if problems:
        print(f"Stack table check FAILED - {len(problems)} table(s):\n")
        print("\n".join(problems))
        print(f"\nFix: {canon_at} is canonical. Add the missing category rows to "
              "the offending table, wording each cell to suit that document - only "
              "the category names must match, not the descriptions.")
    else:
        print(f"Stack table check passed - {checked} stack table(s) carry every "
              f"category in {canon_at} ({len(canon_rows)} categories); {exempt} "
              "target-project template(s) exempt.")

    if notes:
        print(f"\nNote - {len(notes)} prose restatement(s) of the stack, unchecked:\n")
        print("\n".join(notes))
        print("\nA sentence cannot be compared structurally against a table, so "
              "these copies drift unobserved. Converting them, pointing them at "
              "the canonical table, or accepting them is a human decision.")

    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
