#!/usr/bin/env python3
r"""Check the gro\/\/ wordmark escaping convention in every Markdown file.

Prose renders Markdown, so the wordmark needs doubled backslashes to survive
escaping. Fenced code takes backslashes literally, so it needs the
single-backslash form.

    prose   gro\\/\\/ stack
    fence   gro\/\/ stack

Inline code spans are exempt, in both directions. A span is how these
documents quote either form while explaining where it belongs, so both occur
and no line-level rule can tell them apart. Spans are stripped from prose
lines before judging them, and a fence never contains one.

Standard library only. Run from anywhere:

    python3 .github/scripts/check_wordmark.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# "gro", a run of backslashes, a slash, another run of backslashes, a slash.
WORDMARK = re.compile(r"gro(\\+)/(\\+)/")
# A fence opener/closer: three or more backticks or tildes.
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
# Inline code spans. Not judged in either direction - see module docstring.
INLINE_CODE = re.compile(r"`+[^`]*`+")

SKIP_DIR = ".git"


def is_vendored_harness(parts: tuple[str, ...]) -> bool:
    """True for anything under a skills/harness/ tree (Apache-2.0, verbatim)."""
    return any(parts[i : i + 2] == ("skills", "harness") for i in range(len(parts)))


def markdown_files(root: Path):
    for path in sorted(root.rglob("*.md")):
        parts = path.relative_to(root).parts
        if SKIP_DIR in parts or is_vendored_harness(parts):
            continue
        yield path


def scan(path: Path, rel: str) -> list[str]:
    """Return one formatted problem string per offending wordmark occurrence."""
    problems: list[str] = []
    fence_marker: str | None = None

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
            # Inside a fence: single backslashes are correct, doubled are not.
            haystack, bad_run = raw, 2
            message = (
                r"fenced code must use the single-backslash wordmark (gro\/\/), "
                r"found doubled (gro\\/\\/)"
            )
        else:
            # Prose: doubled backslashes are correct. Inline code spans are
            # exempt either way, so remove them before judging the line.
            haystack, bad_run = INLINE_CODE.sub("", raw), 1
            message = (
                r"prose must use the doubled-backslash wordmark (gro\\/\\/), "
                r"found single (gro\/\/)"
            )

        for match in WORDMARK.finditer(haystack):
            runs = (len(match.group(1)), len(match.group(2)))
            if bad_run in runs:
                problems.append(
                    f"{rel}:{lineno}: {message}\n"
                    f"    {raw.strip()[:160]}"
                )

    return problems


def main() -> int:
    problems: list[str] = []
    scanned = 0

    for path in markdown_files(REPO_ROOT):
        scanned += 1
        problems.extend(scan(path, path.relative_to(REPO_ROOT).as_posix()))

    if problems:
        print(f"Wordmark check FAILED - {len(problems)} occurrence(s):\n")
        for problem in problems:
            print(problem)
        print(
            "\nFix: in Markdown prose write the wordmark with doubled "
            r"backslashes (gro\\/\\/ stack); inside a fenced code block write "
            r"it with single backslashes (gro\/\/ stack). Inline code spans "
            "are not checked in either direction."
        )
        return 1

    print(f"Wordmark check passed - {scanned} Markdown file(s) scanned.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
