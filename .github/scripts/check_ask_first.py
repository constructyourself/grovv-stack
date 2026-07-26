#!/usr/bin/env python3
r"""Check that the repo's two ask-first rules survive every edit.

    frontend    ask which framework - Astro + React or Next.js - before
                writing any frontend code
    playwright  ask what Playwright should test before writing any E2E test

Part one is presence: every file in RULES must still state its rule, in its own
words - one SENTENCE carrying an ASK signal, the rule's SUBJECT and a PRECEDENCE
word putting the ask ahead of the work, and not revoking it in the same breath.
Sentence scope rather than line scope because this repo writes a paragraph per
line, and across a paragraph those signals co-occur as readily in prose that
cancels the rule as in prose that states it. What passes is a normative
sentence, not a verified meaning - no regex reads - but the realistic failure is
an edit dropping the rule from a document that governs it, and that it catches.
Matching one exact string instead would fire on every legitimate rewording.

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

# A sentence boundary: terminator then whitespace. "Next.js" survives intact
# because no space follows its dot - splitting there would cut the canonical
# statement ("...or Next.js - before writing frontend code") in half and report
# the repo's own wording as missing.
SENTENCE = re.compile(r"(?<=[.;])\s+")
# "discuss" counts because the code-review checklists word the rule as "discussed
# with user"; "agree" because agreeing a scope with the user is the same act; the
# user-decides clause counts because a file may state the rule as whose choice it
# is rather than as an instruction to ask. None of them says "ask".
ASK = re.compile(
    r"\bask(?:s|ed|ing)?\b|\bdiscuss(?:es|ed|ion)?\b|\bconfirm(?:s|ed)?\b"
    r"|\bagree(?:s|d)?\b|\buser\b[^.;]{0,60}\b(?:choos|chose|decid|pick|select)"
    r"|\b(?:choos|chose|decid|pick|select)\w*[^.;]{0,60}\buser\b", re.I)
# The rule's own name, removed before the precedence test but never before the
# ask test: a rule must not satisfy a check by naming itself. Otherwise the bare
# "(ask-first)" cell in a capability table reads as an ordering, and every
# directive could lose the rule while that cell kept CI green.
SELF_LABEL = re.compile(r"\bask[- ]first\b", re.I)
# "without" is deliberately absent: alone it states no order ("generate the flows
# without asking"), and where this repo uses it the order comes from the
# prohibition governing it ("never auto-generate ... without asking first").
# "first" must be unhyphenated, which excludes "production-first".
PRECEDENCE = re.compile(
    r"\bbefore\b|\bnever\b|\bnot\b|\buntil\b|(?<![-\w])first\b|\bup[- ]front\b"
    r"|\bin advance\b|\bahead of\b|\bpre-(?:empt|decid)\w*", re.I)
# Phrases that cancel the rule instead of stating it, so a sentence carrying one
# is not evidence of the rule. Only the unambiguous ones: "unless" and
# "otherwise" are NOT here because the repo uses them in correct rule prose
# (skills-builder states the rule "...before writing frontend code, unless the
# project has already committed to one").
REVOKED = re.compile(
    r"\bno longer\b|\b(?:do|does|did)\s+not\s+ask\b|\bdon'?t\s+ask\b"
    r"|\bno need to ask\b|\bnever\s+ask\b|\bskip\s+(?:the\s+)?ask", re.I)
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
# master directive, the agent definitions owning each subject in all four tool
# trees, the kickoff skill in all four, and the prompts generating frontend or
# testing guidance. To extend: add a file when it starts governing a rule; drop
# it in the commit that removes the prose. Two deliberate omissions - MEMORY.md
# states both rules, but its own convention is to prune to ~120 lines, so a
# permanent requirement here would fight that; docs/architecture/*.md record
# engineering already done, so they are history, not governing documents.
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

def states_line(raw: str, subject: re.Pattern[str]) -> bool:
    """True when one sentence of this line states the rule for `subject`."""
    return any(ASK.search(part) and subject.search(part) and not REVOKED.search(part)
               and PRECEDENCE.search(SELF_LABEL.sub(" ", part))
               for part in SENTENCE.split(raw))

def states_rule(path: Path, subject: re.Pattern[str]) -> bool:
    return any(states_line(raw, subject)
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
                    f"{target}:1: no sentence states the {name} ask-first rule - "
                    "nothing here carries an ask signal, the subject "
                    f'({words}) and a precedence word together\n    e.g. "{example}"')


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
        print("\nFix: restore the rule in the named file, in that file's own idiom, "
              "as ONE sentence carrying an ask signal (ask/discuss/confirm/agree, or "
              "the user choosing), the subject, and a word putting the ask ahead of "
              "the work (before/never/not/until/first/up front/in advance). Calling "
              'the rule "ask-first" does not state it. Both rules are '
              "non-negotiable.")
        return 1

    print(f"Ask-first check passed - {STATEMENTS} file/rule pair(s) across "
          f"{len(GOVERNED)} governed file(s) still carry a normative ask-first "
          f"sentence; {len(warnings)} erosion warning(s) from {scanned} Markdown "
          "file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
