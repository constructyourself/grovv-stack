#!/usr/bin/env python3
r"""Check that the scaffolding pipeline's step numbering stays consistent.

The "### Step N: Name" headings in grovv-stack-scaffold.md are the source of
truth and must form one complete run. Every other document then has to agree:
a range ("Steps 0-9", hyphen or en dash) names real steps and, if it starts at
the first, reaches the last; an inline "Step N" names a step that exists; and
an ordered list a range introduces is the pipeline list, so its numbering and
the wording of each item track the headings. A renumber touches 60-odd
references at once, and this is the net for doing that by hand.

Standard library only. Runs from anywhere: python3 .github/scripts/check_step_numbers.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE = "grovv-stack-scaffold.md"

STEP_HEADING = re.compile(r"^#{2,6}\s+Step\s+(\d+)\s*:\s*(.+?)\s*$")
# Both dash forms - prose here uses en dashes, plain text hyphens.
STEP_RANGE = re.compile(r"\bSteps\s+(\d+)\s*[-–—]\s*(\d+)")
# A lone "Step 7". Title case only; lowercase would drag in unrelated prose.
STEP_REF = re.compile(r"\bSteps?\s+(\d+)")
ORDERED_ITEM = re.compile(r"^\s*(\d+)\.\s+(\S.*)$")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
WORD = re.compile(r"[a-z0-9]+")
# Dropped before scoring an item against a heading - they carry no signal.
STOPWORDS = {"the", "and", "for", "with", "from", "into", "its"}
SKIP_DIR = ".git"
# Architecture notes are proposals - they argue about numbering the repo does
# not have yet ("a new Step 2 ... Steps 2 through 9 renumber to 3 through 10").
# Every step token in them is deliberately counterfactual, so holding them to
# today's headings would make a renumber impossible to write down.
ARCHITECTURE = ("docs", "architecture")


def is_vendored_harness(parts: tuple[str, ...]) -> bool:
    """True for anything under a skills/harness/ tree (Apache-2.0, verbatim)."""
    return any(parts[i : i + 2] == ("skills", "harness") for i in range(len(parts)))

def markdown_files(root: Path):
    for path in sorted(root.rglob("*.md")):
        parts = path.relative_to(root).parts
        if SKIP_DIR in parts or is_vendored_harness(parts) or parts[:2] == ARCHITECTURE:
            continue
        yield path

def words(text: str) -> set[str]:
    return {w for w in WORD.findall(text.lower()) if w not in STOPWORDS and len(w) > 2}

def note(problems: list[str], rel: str, lineno: int, why: str, quote: str = "") -> None:
    problems.append(f"{rel}:{lineno}: {why}" + (f"\n    {quote.strip()[:150]}" if quote else ""))

def prose(lines: list[str]):
    # (lineno, line) outside fenced code. A fence quotes sample output or a
    # target project's own text, not a claim about this pipeline.
    marker: str | None = None
    for lineno, raw in enumerate(lines, 1):
        if opener := FENCE.match(raw):
            seen = opener.group(1)[0]
            marker = seen if marker is None else (None if marker == seen else marker)
        elif marker is None:
            yield lineno, raw

def headings(lines: list[str]) -> list[tuple[int, str, int]]:
    """Every "Step N: Name" heading in a file, as (number, name, lineno)."""
    return [(int(m.group(1)), m.group(2), lineno) for lineno, raw in prose(lines)
            if (m := STEP_HEADING.match(raw))]


def load_pipeline(problems: list[str]) -> dict[int, tuple[str, int]]:
    """The source of truth as number -> (name, lineno). Its headings must read
    as one complete run - no number skipped, none used twice."""
    path = REPO_ROOT / SOURCE
    found = headings(path.read_text(encoding="utf-8").splitlines()) if path.is_file() else []
    numbers = [number for number, _, _ in found]
    run = list(range(numbers[0], numbers[0] + len(numbers))) if numbers else []
    if numbers != run or not numbers:
        first = next((i for i, n in enumerate(numbers) if n != run[i]), 0)
        note(problems, SOURCE, found[first][2] if found else 1,
             f"the step headings read {', '.join(map(str, numbers)) or 'as none at all'}"
             " - they must form one complete run, no number skipped, none used twice")
    # Reversed so the first heading wins a duplicate, matching how a reader
    # resolves one: the second occurrence is the mistake.
    return {number: (name, lineno) for number, name, lineno in reversed(found)}


def check_list(rel, lines, index, low, high, steps, problems) -> None:
    """The ordered list introduced by a range expression ending in ':'. Demanding
    that introducer is what keeps unrelated ordered lists out - agents/scaffold.md
    has one right above the pipeline list, under a plain '## Behavior' heading,
    and treating that one as the pipeline would be wrong."""
    cursor = index + 1
    while cursor < len(lines) and not lines[cursor].strip():
        cursor += 1
    items = []
    while cursor < len(lines) and (m := ORDERED_ITEM.match(lines[cursor])):
        items.append((cursor + 1, int(m.group(1)), m.group(2)))
        cursor += 1
    if not items:
        return
    numbers = [number for _, number, _ in items]
    if numbers != list(range(low, high + 1)):
        note(problems, rel, items[0][0], f"the list introduced by 'Steps {low}-{high}' is"
             f" numbered {', '.join(map(str, numbers))}; it must run {low} to {high}, one"
             " item per step")
        return  # Item names are judged by number, which is not trustworthy yet.

    # Scored relatively, not by exact match: an item paraphrases its heading
    # ("Create directory structure and `settings.json`" for "Create Structure and
    # Configuration"), but a botched renumber leaves it matching a NEIGHBOUR
    # better than its own step - that shift is what gets reported.
    for lineno, number, text in items:
        scores = {n: len(words(text) & words(name)) for n, (name, _) in steps.items()}
        best = max(scores.values())
        if best and scores[number] < best:
            other = min(n for n, score in scores.items() if score == best)
            note(problems, rel, lineno, f"list item {number} reads {text.strip()[:60]!r},"
                 f" naming Step {other} ({steps[other][0]!r}), not Step {number} "
                 f"({steps[number][0]!r})")


def check_file(path: Path, steps: dict[int, tuple], problems: list[str]) -> None:
    rel = path.relative_to(REPO_ROOT).as_posix()
    lines = path.read_text(encoding="utf-8").splitlines()
    low, high = min(steps), max(steps)
    # A document may number its own internal workflow - docs/prompts/tracker-setup.md
    # opens with '## Step 0: Tracker Selection' and refers back to it four times.
    # Numbers a file defines itself are its own; numbers it does not are the
    # pipeline's, and stay checked. SOURCE is excluded because its headings ARE
    # the pipeline, so exempting them would exempt every reference in it.
    internal = set() if rel == SOURCE else {n for n, _, _ in headings(lines)}

    for lineno, raw in prose(lines):
        for match in STEP_RANGE.finditer(raw):
            first, last, why = int(match.group(1)), int(match.group(2)), ""
            if {first, last} <= internal:
                continue
            if not {first, last} <= steps.keys() or first >= last:
                why = "does not name a real span"
            # Starting at the first step claims the whole workflow, so it has
            # to reach the last. A range starting later ("Steps 2-9" - everything
            # after Step 1) is a deliberate partial span, endpoints only.
            elif first == low and last != high:
                why = f"starts at the first step but stops at Step {last}"
            if why:
                note(problems, rel, lineno, f"{match.group(0)!r} {why}", raw)
            elif raw.rstrip().endswith(":"):
                check_list(rel, lines, lineno - 1, first, last, steps, problems)

        for match in STEP_REF.finditer(STEP_RANGE.sub("", raw)):
            if int(match.group(1)) not in steps.keys() | internal:
                note(problems, rel, lineno, f"{match.group(0)!r} does not exist", raw)


def main() -> int:
    problems: list[str] = []
    steps, scanned = load_pipeline(problems), 0
    # Only if the run itself is sound: references judged against a broken
    # pipeline produce noise on top of the one problem worth fixing first.
    for path in markdown_files(REPO_ROOT) if not problems else []:
        scanned += 1
        check_file(path, steps, problems)

    run = f"Step {min(steps)} through Step {max(steps)}" if steps else "no steps at all"
    if problems:
        print(f"Step numbering check FAILED - {len(problems)} problem(s). {SOURCE} "
              f"defines the pipeline as {run}:\n")
        print("\n".join(problems))
        print(f"\nFix: the 'Step N: Name' headings in {SOURCE} are the source of truth. "
              "Renumber or rename there first, then update every reference to agree - "
              "inline numbers, range expressions, and the numbering and wording of any "
              "ordered list a range expression introduces.")
        return 1

    print(f"Step numbering check passed - {run} from {SOURCE}, "
          f"{scanned} Markdown file(s) scanned.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
