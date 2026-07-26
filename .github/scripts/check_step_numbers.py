#!/usr/bin/env python3
r"""Check that the scaffolding pipeline's step numbering stays consistent.

The "### Step N: Name" headings in grovv-stack-scaffold.md are the source of
truth and must form one complete run. Three things then have to agree:

    a  a range ("Steps 0-9", hyphen or en dash) names real steps
    b  a step number standing beside the prompt that step executes -
       "`tracker-setup.md` (Step 8)" - names that prompt's step
    c  an ordered list a range introduces enumerates the pipeline, so its
       numbering and the wording of each item track the headings

A range that starts at the first step but stops short of the last only WARNS.
"Steps 0-4 produce the documents; Steps 5-9 execute them" is a true sentence
about a partial span, and failing it would be answered by widening the range
until the sentence is false - but the same shape is what a renumber leaves
behind, so it is worth a human's eye and not worth a red build.

Rule b is the one that survives a renumber: inserting a step leaves every stale
reference numerically in range, so existence proves nothing, while the binding
between a prompt filename and its step number is unambiguous and breaks loudly.

Only lines tying themselves to THIS pipeline are judged - naming
grovv-stack-scaffold.md, the pipeline, the scaffolding, or one of its prompts.
This repo's whole subject is documents written into OTHER projects, and a
generated plan describing "Steps 1-12 of delivery" is not its business.

Standard library only. Runs from anywhere: python3 .github/scripts/check_step_numbers.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE = "grovv-stack-scaffold.md"
PROMPTS = "docs/prompts/"

STEP_HEADING = re.compile(r"^#{2,6}\s+Step\s+(\d+)\s*:\s*(.+?)\s*$")
# Both dash forms - prose here uses en dashes, plain text hyphens.
STEP_RANGE = re.compile(r"\bSteps\s+(\d+)\s*[-–—]\s*(\d+)")
# A lone "Step 7". Title case only; lowercase would drag in unrelated prose.
STEP_REF = re.compile(r"\bSteps?\s+(\d+)")
# The line that binds a prompt to its step: "Read and execute `docs/prompts/X.md`".
EXECUTES = re.compile(r"execute\s+`?docs/prompts/([a-z0-9-]+)\.md")
# A prompt stating its own position: "It is **Step 7** of the pipeline", "This
# is the tracker-setup step (Step 8)". Only read inside a prompt the pipeline
# executes. The number must be bracketed or bolded (or follow the copula
# directly), which is how a document names itself; a number reached through a
# preposition - "This is the last chance to fix the plan from Step 3" - is
# about a neighbour, as is one preceded by another prompt's name.
SELF = re.compile(r"\b(?:this|it) is\s+(?:([^.!?]{0,80}?)[(*]\s*)?Step\s+(\d+)", re.IGNORECASE)
ORDERED_ITEM = re.compile(r"^\s*(\d+)\.\s+(\S.*)$")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
HEADING = re.compile(r"^\s*#{1,6}\s")
WORD = re.compile(r"[a-z0-9]+")
# Words that put a line in scope by naming this pipeline. A prompt stem names it
# just as specifically, and rule b already requires one.
MARKER = re.compile(r"scaffold|pipeline", re.IGNORECASE)
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


def load_pipeline(problems: list[str]) -> tuple[dict[int, tuple[str, int]], dict[str, int]]:
    """The source of truth: number -> (name, lineno), plus the prompt each step
    executes as stem -> number. The headings must read as one complete run - no
    number skipped, none used twice."""
    path = REPO_ROOT / SOURCE
    lines = path.read_text(encoding="utf-8").splitlines() if path.is_file() else []
    found, bound, current = headings(lines), {}, None
    numbers = [number for number, _, _ in found]
    run = list(range(numbers[0], numbers[0] + len(numbers))) if numbers else []
    if numbers != run or not numbers:
        first = next((i for i, n in enumerate(numbers) if n != run[i]), 0)
        note(problems, SOURCE, found[first][2] if found else 1,
             f"the step headings read {', '.join(map(str, numbers)) or 'as none at all'}"
             " - they must form one complete run, no number skipped, none used twice")
    for _, raw in prose(lines):
        if match := STEP_HEADING.match(raw):
            current = int(match.group(1))
        elif current is not None and (match := EXECUTES.search(raw)):
            bound.setdefault(match.group(1), current)  # First wins, as for headings.
    # Reversed so the first heading wins a duplicate, matching how a reader
    # resolves one: the second occurrence is the mistake.
    return {n: (name, lineno) for n, name, lineno in reversed(found)}, bound


def binding_patterns(bound: dict[str, int]) -> tuple[re.Pattern, re.Pattern] | None:
    """A prompt stem and a step number close enough to be naming each other, in
    either order. The gap admits no sentence end and no backtick, so a second
    filename cannot sit inside it: "`team-design.md` (Step 7) and
    `tracker-setup.md` (Step 8)" resolves as the two pairs a reader sees, and a
    number a whole clause away from a filename is left alone."""
    names = "|".join(sorted(map(re.escape, bound), key=len, reverse=True))
    return (re.compile(rf"\b({names})(?:\.md)?`?[^.!?`]{{0,20}}?\bStep\s+(\d+)"),
            re.compile(rf"\bStep\s+(\d+)[^.!?`]{{0,6}}?\b({names})\b")) if bound else None


def bindings(raw: str, patterns) -> list[tuple[str, int]]:
    """Every (prompt stem, step number) pair named on one line."""
    forward, reverse = patterns
    return ([(m.group(1), int(m.group(2))) for m in forward.finditer(raw)]
            + [(m.group(2), int(m.group(1))) for m in reverse.finditer(raw)])


def pipeline_list(lines: list[str], index: int) -> list[tuple[int, int, str]]:
    """The ordered list a range on line `index` introduces, as (lineno, number,
    text). Blank lines and one line of prose may sit between: the range is as
    often in a heading, or a sentence ending in a full stop, as in a colon
    introducer, and keying on the colon let three ordinary rewordings disable
    the check. A heading or fence ends the search - what follows one of those
    belongs to something else."""
    cursor, slack, items = index + 1, 1, []
    while cursor < len(lines) and not ORDERED_ITEM.match(lines[cursor]):
        line = lines[cursor]
        if line.strip():
            if not slack or HEADING.match(line) or FENCE.match(line):
                return []
            slack -= 1
        cursor += 1
    while cursor < len(lines) and (match := ORDERED_ITEM.match(lines[cursor])):
        items.append((cursor + 1, int(match.group(1)), match.group(2)))
        cursor += 1
    return items


def check_list(rel, lines, index, first, last, steps, problems) -> None:
    """A following list is the pipeline's only if its shape says so: one
    consecutively numbered item per step in the range. Anything else is an
    unrelated list that happens to follow - agents/scaffold.md has one right
    above the pipeline list, and "two of Steps 0-9 ask a question:" over a
    two-item list is a true sentence - so it is left alone, not reported."""
    items = pipeline_list(lines, index)
    numbers = [number for _, number, _ in items]
    run = list(range(numbers[0], numbers[0] + len(items))) if items else []
    if len(items) != last - first + 1 or numbers != run:
        return
    if numbers[0] != first:
        note(problems, rel, items[0][0], f"the list introduced by 'Steps {first}-{last}' is"
             f" numbered {numbers[0]} to {numbers[-1]}; it must run {first} to {last}, one"
             " item per step")
        return  # Item names are judged by number, which is not trustworthy yet.

    # Scored relatively, not by exact match: an item paraphrases its heading
    # ("Create directory structure and `settings.json`" for "Create Structure and
    # Configuration"). Only a decisive mismatch is reported - nothing shared with
    # its own heading and two or more words with another's, which is what a
    # rotated list looks like. One shared word is usually a generic verb
    # ("Generate", "Create", "Set") an honest rewording reaches for, and
    # reporting that teaches the editor to revert correct prose.
    for lineno, number, text in items:
        scores = {n: len(words(text) & words(name)) for n, (name, _) in steps.items()}
        best = max(scores.values())
        if scores[number] == 0 and best >= 2:
            other = min(n for n, score in scores.items() if score == best)
            note(problems, rel, lineno, f"list item {number} reads {text.strip()[:60]!r},"
                 f" naming Step {other} ({steps[other][0]!r}), not Step {number} "
                 f"({steps[number][0]!r})")


def check_file(path: Path, steps: dict[int, tuple], bound, patterns, problems, warnings) -> None:
    rel = path.relative_to(REPO_ROOT).as_posix()
    lines = path.read_text(encoding="utf-8").splitlines()
    low, high = min(steps), max(steps)
    # A document may number its own internal workflow - docs/prompts/tracker-setup.md
    # opens with '## Step 0: Tracker Selection' and refers back to it four times.
    # Numbers a file defines itself are its own; numbers it does not are the
    # pipeline's, and stay checked. SOURCE is excluded because its headings ARE
    # the pipeline, so exempting them would exempt every reference in it.
    internal = set() if rel == SOURCE else {n for n, _, _ in headings(lines)}
    own = bound.get(path.stem) if rel.startswith(PROMPTS) else None

    for lineno, raw in prose(lines):
        for stem, number in bindings(raw, patterns) if patterns else []:
            if number != bound[stem] and number not in internal:
                note(problems, rel, lineno, f"'Step {number}' stands beside {stem!r}, "
                     f"which {SOURCE} executes at Step {bound[stem]}", raw)
        # A prompt is one of the steps, so its own position is a binding too -
        # the reference no filename sits next to.
        if own is not None and MARKER.search(raw) and (match := SELF.search(raw)):
            number, gap = int(match.group(2)), match.group(1) or ""
            if number != own and number not in internal and not any(
                    stem in gap for stem in bound if stem != path.stem):
                note(problems, rel, lineno, f"this line calls {path.name} 'Step {number}';"
                     f" {SOURCE} executes it at Step {own}", raw)
        # SOURCE is in scope throughout: it IS the pipeline definition, so every
        # step token in it is a claim about the pipeline by construction.
        if rel != SOURCE and not MARKER.search(raw):
            continue
        for match in STEP_RANGE.finditer(raw):
            first, last = int(match.group(1)), int(match.group(2))
            if {first, last} <= internal:
                continue
            if not {first, last} <= steps.keys() or first >= last:
                note(problems, rel, lineno, f"{match.group(0)!r} does not name a real span", raw)
                continue
            # Endpoints only, and a short head-anchored range warns rather than
            # fails - see the module docstring.
            if first == low and last != high:
                note(warnings, rel, lineno, f"WARNING - {match.group(0)!r} starts at the "
                     f"first step but stops short of Step {high}. A deliberate partial "
                     "span is fine; a whole-pipeline range left stale by a renumber is "
                     "not", raw)
            check_list(rel, lines, lineno - 1, first, last, steps, problems)

        for match in STEP_REF.finditer(STEP_RANGE.sub("", raw)):
            if int(match.group(1)) not in steps.keys() | internal:
                note(problems, rel, lineno, f"{match.group(0)!r} does not exist", raw)


def main() -> int:
    problems: list[str] = []
    warnings: list[str] = []
    (steps, bound), scanned = load_pipeline(problems), 0
    patterns = binding_patterns(bound)
    # Only if the run itself is sound: references judged against a broken
    # pipeline produce noise on top of the one problem worth fixing first.
    for path in markdown_files(REPO_ROOT) if not problems else []:
        scanned += 1
        check_file(path, steps, bound, patterns, problems, warnings)

    run = f"Step {min(steps)} through Step {max(steps)}" if steps else "no steps at all"
    if warnings:
        print(f"Step numbering WARNINGS - {len(warnings)} range(s), not build-failing. "
              f"{SOURCE} defines the pipeline as {run}:\n")
        print("\n".join(warnings))
        print("\nEach is a partial span anchored at the first step. If it is deliberate, "
              "leave it; if it once meant the whole pipeline, widen it.\n")

    if problems:
        print(f"Step numbering check FAILED - {len(problems)} problem(s). {SOURCE} "
              f"defines the pipeline as {run}:\n")
        print("\n".join(problems))
        print(f"\nFix: the 'Step N: Name' headings in {SOURCE} are the source of truth. "
              "Renumber or rename there first, then update every reference to agree - "
              "range expressions, the step number quoted beside each prompt filename, and "
              "the numbering and wording of any ordered list a range introduces.")
        return 1

    print(f"Step numbering check passed - {run} from {SOURCE}, {len(bound)} prompt "
          f"binding(s), {scanned} Markdown file(s) scanned"
          + (f", {len(warnings)} warning(s) above." if warnings else "."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
