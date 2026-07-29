# CI Checks

**gro\\/\\/ stack** — Check-Only Continuous Integration

-----

## What This Is

This repo produces documents and configuration, not software. It has no dependencies, no lockfile and no build step, and it must not gain any. CI therefore validates what is written here; it never builds it.

Every check is Python 3 standard library only — no `pip install`, no npm, no actions beyond `actions/checkout` and `actions/setup-python`. The workflow is `.github/workflows/checks.yml`, which runs each script as its own named step so a failure names itself in the GitHub UI.

```
.github/
├── workflows/
│   └── checks.yml              # push + pull_request; check-only
└── scripts/
    ├── check_wordmark.py       # wordmark escaping in Markdown
    ├── check_versions.py       # manifest and MEMORY.md version parity
    ├── check_tool_sync.py      # .grovv canonical vs derived tool dirs
    ├── check_references.py     # every repo path a document names exists
    ├── check_step_numbers.py   # pipeline step numbering is consistent
    ├── check_stack_tables.py   # the stack tables agree with canonical
    ├── check_ask_first.py      # the two ask-first rules are intact
    └── README.md               # this file
```

Each script also runs standalone from any working directory, so an agent can verify its work before committing:

```bash
python3 .github/scripts/check_wordmark.py
python3 .github/scripts/check_versions.py
python3 .github/scripts/check_tool_sync.py
python3 .github/scripts/check_references.py
python3 .github/scripts/check_step_numbers.py
python3 .github/scripts/check_stack_tables.py
python3 .github/scripts/check_ask_first.py
```

Each exits `0` when clean, or non-zero after printing every problem it found as `path:line` plus the offending text.

-----

## The Checks

| Script | Enforces | Why |
|--------|----------|-----|
| `check_wordmark.py` | Wordmark backslash escaping in every `*.md` | The single most common review catch in this repo |
| `check_versions.py` | One version across two manifests and `MEMORY.md` | Two manifests silently drifted apart |
| `check_tool_sync.py` | `.grovv/` canonical, tool dirs derived | Four copies of every agent invite silent divergence |
| `check_references.py` | Every repo-rooted path a document names exists | A prompt was renamed and stale references survived across many files |
| `check_step_numbers.py` | Step headings, ranges and pipeline lists agree | A heading read "Steps 0–9" over a list numbered 1 to 10, in four files |
| `check_stack_tables.py` | Stack tables carry canonical's categories | Seven tables had drifted; one was missing three rows |
| `check_ask_first.py` | Both ask-first rules present where they govern | They are the repo's hardest guarantees and were prose only |

Every one of these was written after the drift it detects had already happened. None is hypothetical.

-----

## check_wordmark.py

The wordmark needs doubled backslashes in Markdown prose to survive escaping, and single backslashes in fenced code, where backslashes are already literal.

| Context | Correct form | Checked |
|---------|--------------|---------|
| Markdown prose | `gro\\/\\/ stack` | Yes |
| Fenced code block | `gro\/\/ stack` | Yes |
| Inline code span | `gro\/\/ stack` | No — exempt in both directions |

The script walks every `*.md` file, skipping `.git` and any `skills/harness/` tree, tracking fenced-code state line by line. It flags the single-backslash form in prose and the doubled form inside a fence. That is the whole of what it enforces.

Inline code spans are exempt, and the exemption runs both ways: the prose branch strips spans out of a line before judging it, and the fenced branch never meets one. Neither form is ever reported inside backticks. That is deliberate rather than an oversight — a span is how a document quotes the prose form while explaining what prose should contain, and equally how it quotes the fenced form while explaining what a fence should contain. Both uses are correct, they routinely share a sentence, and nothing at line level separates them. The check declines to guess, which also means it cannot see two documents disagreeing inside spans.

Thirteen lines currently rely on the exemption. Each writes the single-backslash form inside a span on a prose line, so the prose branch would report it if spans were judged as prose:

| File | Line(s) |
|------|---------|
| `.claude/CLAUDE.md` | 202 |
| `.claude/agents/scaffold.md` | 53 |
| `.codex/agents/scaffold.md` | 53 |
| `.github/scripts/README.md` | 53, 54 |
| `.grovv/CLAUDE.md` | 182 |
| `.grovv/agents/scaffold.md` | 53 |
| `.vibe/agents/scaffold.md` | 53 |
| `CLAUDE.md` | 205 |
| `CODEX.md` | 166 |
| `MEMORY.md` | 60 |
| `VIBE.md` | 176 |
| `grovv-stack-scaffold.md` | 538 |

Two of those are rows 53 and 54 of the table above, in this file. The exemption covers this document on exactly the terms it covers the others; it is not a carve-out for files nobody is fixing.

### What the exemption cannot excuse

A span may quote either form, but **neither valid form is truncated and neither has mismatched backslash runs**. Those shapes are wrong in prose, spans and fenced code alike, so the check judges them on the raw line regardless of context: a wordmark with one escaped slash instead of two, with runs of differing length, or with a run longer than two, is reported wherever it appears.

This closes the hole that produced the original defect. All five statements of the convention in this repo were once wrong in exactly this way — each showed the single form while calling it doubled, and gave a code-block example truncated to a single escaped slash — and the span exemption made every one of them invisible. A rule documented wrongly in every copy is a sufficient explanation for why it was the most-violated rule here.

This paragraph cannot quote the shapes it describes, because the check rejects them wherever they appear, including here. That is the rule working: a malformed wordmark has no legitimate use, not even as an example.

-----

## check_versions.py

Three places state the version and must agree:

| Source | Role |
|--------|------|
| `.claude-plugin/plugin.json` | The manifest Claude Code actually reads |
| `plugin.json` | Root documentation manifest; its schema is read by nothing |
| `MEMORY.md` | The version quoted in `## Current State` prose |

Because nothing loads the root manifest, drift there is invisible until someone reads it and believes it. The check reports all three values whenever they disagree, so the fix is obvious rather than a guess.

-----

## check_tool_sync.py

`.grovv/` is canonical. `.claude/`, `.vibe/` and `.codex/` are derived copies. Three tiers, strictest first:

| Tier | Scope | Rule |
|------|-------|------|
| a | `skills/harness/**` | Byte-identical across all four trees |
| b | `agents/*.md` | Identical to `.grovv/` after normalizing tool path prefixes and `${*_PLUGIN_ROOT}` names, and excising one optional tool-specific section |
| c | Tier b plus `skills/grovv/SKILL.md` | Every target exists in all four trees |

Tier a is strict because harness is vendored verbatim under Apache-2.0 and its `ATTRIBUTION.md` forbids hand-editing; any byte difference is a bug, not a customization.

Tier b rewrites the `.claude/`, `.vibe/`, `.codex/` and `.grovv/` path prefixes to a common placeholder on both sides before diffing, so a legitimate path adaptation passes and anything else fails. It normalizes `${CLAUDE_PLUGIN_ROOT}` and its siblings the same way — each tree names its own, which is sanctioned variation, and normalizing only the path prefix would report every correct file as broken.

A tier b file may also carry **one** tool-specific section, headed `## <Tool>-Specific ...` and fenced by five-dash rules like any other section. `.vibe/agents/scaffold.md` uses it to say that Vibe spawns subagents with its `task` tool where Claude Code uses `Agent`. That section is excised between its fencing rules before comparison rather than truncated to end of file, so the footer that follows it is still compared and the exemption cannot become a hiding place. A second such section is itself reported. Four tamper cases confirm this: drift in a plain derived file, drift after the section, drift in the shared body before it, and a second section — all caught.

`skills/grovv/SKILL.md` is deliberately **tier c only**. The kickoff skill carries genuine per-tool instruction, so its copies are adapted rather than derived; comparing them would report correct files as broken, and "fixing" that would delete the guidance. It must still exist in all four trees.

Tier c names the absent path. It catches the failure mode where a file is added to one tool directory and forgotten in the other three, and the mirror of it: a deleted derived file removes a tier b comparison, so without tier c, deleting a tool's plugin entry point would report fewer problems than leaving it in place.

-----

## check_references.py

Every repo-rooted path a document names must exist. This is the check whose absence let a prompt rename leave dangling references across many files at once.

The judgement that decides whether it is usable is separating references to **this** repo from references to a **target** project. These documents constantly name `docs/product-spec.md`, `MEMORY.md` and `.claude/skills/{name}/SKILL.md` as things the scaffolder creates somewhere else. Those do not exist here and must never be reported. Paths inside fenced code blocks are excluded for the same reason — trees, example commands and templates describe files elsewhere. A trailing `:41` or `:60-73` is stripped before the existence test; the line number itself is not verified, since documents grow and the reference stays valid.

## check_step_numbers.py

The step headings in `grovv-stack-scaffold.md` are the source of truth. The check verifies they form a complete run with no gaps or duplicates, that every range expression elsewhere matches the real first and last step (both hyphen and en dash — this repo uses en dashes in prose), that every inline step reference names a step that exists, and that where a document pairs a step range with an ordered list of the pipeline, the list agrees.

That last rule is the `scaffold.md` defect: a heading reading "Steps 0–9" above a list numbered 1 to 10, so every item named a step one higher than its own number, in all four trees. Detecting it means not mistaking the unrelated ordered list immediately above the pipeline list for the pipeline itself.

This check matters most for a change nobody has made yet. Inserting a step and renumbering the rest touches sixty-odd references; it should not be attempted without this running.

## check_stack_tables.py

The stack is restated in many tables. The check treats the Core Technology Stack Reference in `grovv-stack-scaffold.md` as canonical and compares **category sets**, not cell text — categories are what must not go missing, while wording legitimately varies between a master directive and a compressed agent definition. Tables inside `docs/prompts/` are templates for a generated project and are held to their own standard rather than to grovv's defaults.

It found seven drifted tables on its first run. Four copies of `agents/scaffold.md` were missing Background Jobs, Project Tracking and Dev Environment; `.grovv/CLAUDE.md`, `CODEX.md` and `VIBE.md` were each missing Dev Environment. All are fixed.

It also reports, without failing, any **prose** restatement of the stack it finds. Two exist. A sentence cannot be compared structurally against a table, so those copies drift unobserved — converting them, pointing them at the canonical table, or accepting them is a human decision, and the check surfaces it rather than pretending it does not exist.

## check_ask_first.py

Two rules are non-negotiable: ask which frontend framework before writing frontend code, and ask what Playwright should test before writing E2E tests. They are stated as prose in many files and nothing verified they survived an edit.

Presence is matched on meaning rather than one exact string, since each file states its rule in its own idiom and a brittle match would fire on a legitimate rewording. A missing rule fails the build.

The second half is an **erosion heuristic**: text that puts a prototype or mockup in the same breath as a framework choice without stating that the rule still applies. That risk became concrete when the throwaway tier landed — an agent could read "I built four mockups in React" as the framework question having been answered. It has not been. Because the heuristic guesses at intent, it emits warnings and never fails the build. A guess should not be able to redden CI.

-----

## Known Open Drift

Everything previously listed here is fixed: manifest versions agree, `.vibe/agents/scaffold.md` reconciles with canonical, `skills/grovv/SKILL.md` was settled as a legitimate per-tool adaptation (tier c), and the two context files no longer disagree about the footer example.

What remains is not drift the checks can see:

- **Two prose restatements of the stack**, reported by `check_stack_tables.py` and unverifiable by construction. See above.
- **Scaffolded projects get no CI.** These checks guard this repo. Projects grovv generates inherit none of them, and no step records the commands that make "done" checkable in a generated project. That is the widest-blast-radius gap in the system, and it is not fixable from inside `.github/`.

-----

## Adding a Check

Keep new checks in the same shape: standard library only, well under 150 lines, resolve the repo root from `__file__` so cwd never matters, print every problem rather than only the first, and exit non-zero with a message naming file and line. Add it to `checks.yml` as its own named step.

-----

## Colophon

| Field | Value |
|-------|-------|
| **Version** | 2.0.0 |
| **Last Updated** | 2026-07-26 |
| **Status** | Active |
| **Author(s)** | Dan |
| **Model** | Claude (Claude Code) |

-----
gro\\/\\/ stack — CI Checks
