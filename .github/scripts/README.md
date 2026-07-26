# CI Checks

**gro\\/\\/ stack** — Check-Only Continuous Integration

-----

## What This Is

This repo produces documents and configuration, not software. It has no dependencies, no lockfile and no build step, and it must not gain any. CI therefore validates what is written here; it never builds it.

Every check is Python 3 standard library only — no `pip install`, no npm, no actions beyond `actions/checkout` and `actions/setup-python`. The workflow is `.github/workflows/checks.yml`, which runs each script as its own named step so a failure names itself in the GitHub UI.

```
.github/
├── workflows/
│   └── checks.yml          # push + pull_request; check-only
└── scripts/
    ├── check_wordmark.py   # wordmark escaping in Markdown
    ├── check_versions.py   # manifest and MEMORY.md version parity
    ├── check_tool_sync.py  # .grovv canonical vs derived tool dirs
    └── README.md           # this file
```

Each script also runs standalone from any working directory, so an agent can verify its work before committing:

```bash
python3 .github/scripts/check_wordmark.py
python3 .github/scripts/check_versions.py
python3 .github/scripts/check_tool_sync.py
```

Each exits `0` when clean, or non-zero after printing every problem it found as `path:line` plus the offending text.

-----

## The Checks

| Script | Enforces | Why |
|--------|----------|-----|
| `check_wordmark.py` | Wordmark backslash escaping in every `*.md` | The single most common review catch in this repo |
| `check_versions.py` | One version across two manifests and `MEMORY.md` | Two manifests silently drifted apart |
| `check_tool_sync.py` | `.grovv/` canonical, tool dirs derived | Four copies of every agent invite silent divergence |

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

Seven lines currently rely on the exemption. Each writes the single-backslash form inside a span on a prose line, so the prose branch would report it if spans were judged as prose:

| File | Line(s) |
|------|---------|
| `.claude/CLAUDE.md` | 191 |
| `.claude/agents/scaffold.md` | 45 |
| `.codex/agents/scaffold.md` | 45 |
| `.github/scripts/README.md` | 53, 54 |
| `.grovv/agents/scaffold.md` | 45 |
| `grovv-stack-scaffold.md` | 502 |

Two of those are rows 53 and 54 of the table above, in this file. The exemption covers this document on exactly the terms it covers the others; it is not a carve-out for files nobody is fixing.

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
| b | `agents/*.md`, `skills/grovv/SKILL.md` | Identical to `.grovv/` after normalizing tool path prefixes |
| c | The tier b file set | Every tier b target exists in all four trees |

Tier a is strict because harness is vendored verbatim under Apache-2.0 and its `ATTRIBUTION.md` forbids hand-editing; any byte difference is a bug, not a customization.

Tier b rewrites the `.claude/`, `.vibe/`, `.codex/` and `.grovv/` path prefixes to a common placeholder on both sides before diffing, so a legitimate path adaptation passes and anything else fails. The report names the file and the first differing line, canonical side first.

Tier c runs over the same target list as tier b — the agents and `skills/grovv/SKILL.md` — and names the absent path. It catches the failure mode where a file is added to one tool directory and forgotten in the other three, and the mirror of it: a deleted derived file removes a tier b comparison, so without tier c, deleting a tool's plugin entry point would report fewer problems than leaving it in place.

-----

## Known Open Drift

@TODO — the following are real and unfixed. The first three are reported by the checks; the last one is invisible to them by construction. The fixes belong to whoever owns each file.

- Manifest versions disagree: `.claude-plugin/plugin.json` and root `plugin.json`.
- `.vibe/agents/scaffold.md` differs from canonical beyond path substitution.
- `skills/grovv/SKILL.md` differs from canonical in all three tool directories — plugin-root variable names and tool-specific paragraphs. Decide whether these are legitimate per-tool adaptations that tier b should normalize, or drift to reconcile.
- The two top-level context files write the same footer example inside an inline span with different escaping: `CLAUDE.md:194` uses the single form, `.claude/CLAUDE.md:191` the doubled one. The check cannot see that disagreement — span contents are exempt in both directions — so the pair has to be reconciled by hand. Pick one form and make both files use it.

-----

## Adding a Check

Keep new checks in the same shape: standard library only, well under 150 lines, resolve the repo root from `__file__` so cwd never matters, print every problem rather than only the first, and exit non-zero with a message naming file and line. Add it to `checks.yml` as its own named step.

-----

## Colophon

| Field | Value |
|-------|-------|
| **Version** | 1.0.0 |
| **Last Updated** | 2026-07-26 |
| **Status** | Active |
| **Author(s)** | Dan |
| **Model** | Claude Opus 5 |

-----
gro\\/\\/ stack — CI Checks
