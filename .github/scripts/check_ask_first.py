#!/usr/bin/env python3
r"""Check that the repo's two ask-first rules survive every edit.

    frontend    ask which framework - Astro + React or Next.js - before
                writing any frontend code
    playwright  ask what Playwright should test before writing any E2E test

Part one is presence: every file in RULES must still state its rule, in its own
words - a line counts when it carries an ASK signal, the rule's SUBJECT and a
PRECEDENCE word putting the ask ahead of the work, all on one line (this repo
writes a paragraph per line). Matching one exact string would instead fire on
any legitimate rewording.

Part two is erosion: the throwaway tier sanctions prototypes, so prose could
come to treat "I built four mockups in React" as the framework question having
been answered. It has not been. A line naming an exploratory artifact and a
framework must also state that boundary. Heuristic, so it only WARNS.

Standard library only. Runs from anywhere: python3 .github/scripts/check_ask_first.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKIP_DIR, TREES = ".git", (".grovv", ".claude", ".vibe", ".codex")

# "discuss" counts because the code-review checklists word the rule as "discussed
# with user"; the user-decides clause counts because a file may state the rule as
# whose choice it is rather than as an instruction to ask. Neither says "ask".
ASK = re.compile(
    r"\bask(?:s|ed|ing)?\b|\bdiscuss(?:es|ed|ion)?\b|\bconfirm(?:s|ed)?\b"
    r"|\buser\b[^.;]{0,60}\b(?:choos|chose|decid|pick|select)"
    r"|\b(?:choos|chose|decid|pick|select)\w*[^.;]{0,60}\buser\b", re.I)
# Bare "first" is deliberately absent: the stack tables carry a bare "(ask
# first)" cell, and letting that satisfy the check would mean the rule could be
# deleted from the directives while a table cell kept CI green.
PRECEDENCE = re.compile(
    r"\bbefore\b|\bnever\b|\bnot\b|\buntil\b|\bwithout\b|\bask-first\b"
    r"|\bpre-(?:empt|decid)\w*", re.I)
FRONTEND = re.compile(r"\bframeworks?\b|\bastro\b|\bnext\.js\b", re.I)
PLAYWRIGHT = re.compile(r"\bplaywright\b|\be2e\b|\bend-to-end\b", re.I)

# Part two signals. Bare "React" is not a framework signal: it names half of
# both options, so on its own it marks no choice.
ARTIFACT = re.compile(r"\b(?:prototyp\w*|mock(?:-?ups?|s|ing)?|spikes?|throwaway|exploratory)\b", re.I)
# The correct pattern, which must NOT warn: a negation reaching a word about
# deciding - "is not a decision to use Next.js", "Mockups never answer the
# framework question", "must not be read as having pre-empted that question".
BOUNDARY = re.compile(
    r"(?:\b(?:not|never|cannot|nor)\b|n't)[^.;]{0,90}\b(?:answer|decid|decision|"
    r"satisf|choos|choice|commit|select|pick|settle|pre-empt|substitut)"
    r"|\bstill\b[^.;]{0,60}\bask", re.I)

def per_tree(rel: str) -> tuple[str, ...]:
    return tuple(f"{tree}/{rel}" for tree in TREES)

# The governed files, derived by grepping every non-harness Markdown file for a
# statement of each rule and keeping those carrying one today: context files, the
# master directive, the agent definitions owning each subject across all four tool
# trees, the kickoff skill in all four, and the prompts generating frontend or
# testing guidance. To extend: when a file starts governing a rule add it here;
# when one stops, drop it here in the commit that removes the prose. Two
# deliberate omissions - MEMORY.md states both rules today, but its own convention
# is to prune aggressively and stay under ~120 lines, so a permanent requirement
# there would fight that rule; docs/architecture/*.md record engineering already
# done, so they are history, not governing documents.
CONTEXT = ("CLAUDE.md", ".claude/CLAUDE.md", ".grovv/CLAUDE.md", "VIBE.md",
           "CODEX.md", "README.md", "grovv-stack-scaffold.md")
PROMPTS = ("docs/prompts/skills-builder.md", "docs/prompts/team-design.md",
           "docs/prompts/tracker-setup.md")
KICKOFF = per_tree("skills/grovv/SKILL.md")

RULES = (
    ("frontend-framework", FRONTEND, "framework / Astro / Next.js",
     CONTEXT + per_tree("agents/frontend.md") + KICKOFF + PROMPTS,
     "Always ask which frontend framework - Astro + React or Next.js - before "
     "writing frontend code"),
    ("playwright", PLAYWRIGHT, "Playwright / E2E / end-to-end",
     CONTEXT + per_tree("agents/testing.md") + per_tree("agents/code-review.md")
     + KICKOFF + PROMPTS + ("docs/prompts/tech-spec.md",),
     "Always ask the user what Playwright should test before writing any "
     "Playwright tests"),
)
STATEMENTS = sum(len(rule[3]) for rule in RULES)
GOVERNED = {target for rule in RULES for target in rule[3]}

def is_vendored_harness(parts: tuple[str, ...]) -> bool:
    """True for anything under a skills/harness/ tree (Apache-2.0, verbatim)."""
    return any(parts[i : i + 2] == ("skills", "harness") for i in range(len(parts)))

def markdown_files(root: Path):
    for path in sorted(root.rglob("*.md")):
        parts = path.relative_to(root).parts
        if SKIP_DIR not in parts and not is_vendored_harness(parts):
            yield path

def states_rule(path: Path, subject: re.Pattern[str]) -> bool:
    return any(ASK.search(raw) and subject.search(raw) and PRECEDENCE.search(raw)
               for raw in path.read_text(encoding="utf-8").splitlines())


def check_presence(problems: list[str]) -> None:
    """Part one - every governed file still states the rule it carries."""
    for name, subject, words, targets, example in RULES:
        for target in targets:
            path = REPO_ROOT / target
            if not path.is_file():
                problems.append(f"{target}:1: file not found - it must state the "
                                f"{name} ask-first rule")
            elif not states_rule(path, subject):
                problems.append(
                    f"{target}:1: no statement of the {name} ask-first rule - one "
                    "line must carry an ask signal (ask/discuss/confirm, or the "
                    f"user choosing), the subject ({words}), and a precedence word "
                    f'(before/never/not/until/without)\n    e.g. "{example}"')


def check_erosion(warnings: list[str]) -> int:
    """Part two - heuristic, warns only. Returns Markdown files scanned."""
    scanned = 0
    for path in markdown_files(REPO_ROOT):
        scanned += 1
        rel = path.relative_to(REPO_ROOT).as_posix()
        for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if ARTIFACT.search(raw) and FRONTEND.search(raw) and not BOUNDARY.search(raw):
                warnings.append(
                    f"{rel}:{lineno}: WARNING - names an exploratory artifact and a "
                    "framework choice in one line without saying the ask-first rule "
                    f"still applies; a human should read it\n    {raw.strip()[:160]}")
    return scanned


def main() -> int:
    problems: list[str] = []
    warnings: list[str] = []
    check_presence(problems)
    scanned = check_erosion(warnings)

    if warnings:
        print(f"Ask-first WARNINGS - {len(warnings)} line(s), not build-failing:\n")
        print("\n".join(warnings))
        print("\nEach is a heuristic hit. If the line already makes plain that a "
              "prototype is not a framework decision it is a false positive - leave "
              "it; otherwise add that sentence.\n")

    if problems:
        print(f"Ask-first check FAILED - {len(problems)} missing statement(s):\n")
        print("\n".join(problems))
        print("\nFix: restore the rule in the named file, in that file's own idiom. "
              "Both are non-negotiable - ask which frontend framework (Astro + React "
              "or Next.js) before any frontend code, and ask what Playwright should "
              "test before any E2E test.")
        return 1

    print(f"Ask-first check passed - {STATEMENTS} rule statement(s) present across "
          f"{len(GOVERNED)} governed file(s); {len(warnings)} erosion warning(s) from "
          f"{scanned} Markdown file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
