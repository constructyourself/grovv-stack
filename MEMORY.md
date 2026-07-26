# MEMORY.md

Cross-session memory for grovv-stack development. An agent starting a session in this repo reads this file first; an agent finishing meaningful work updates it before ending. It works in coordination with the Linear project — Linear owns the backlog, this file owns the context.

-----

## How This File Works

- **Read at session start.** A `SessionStart` hook in tool-specific `settings.json` surfaces this file automatically; if hooks are unavailable, read it manually before any other work.
- **Update before ending a session** that changed anything meaningful: refresh Current State, append a dated entry to the Decision Log, update Next Steps, and prune anything stale.
- **Linear owns the backlog.** Tasks, priorities, status, and assignments live in the Linear project. Never duplicate issue lists here — reference issues by identifier instead.
- **This file owns context.** Decisions and rationale, gotchas, in-flight state, and anything a fresh session needs that does not fit a Linear issue.
- **Stay small.** Keep this file under ~120 lines. It is loaded into context every session; verbosity here is a tax on every future session. Prune aggressively — history lives in git.

-----

## Linear Coordination

| Field | Value |
|-------|-------|
| Project | https://linear.app/grovv/project/grovv-stack-838efdf244c3 |
| Team | Grovv |
| Issue prefix | GRO |

Sync rules:

- When work in this repo completes a Linear issue, note the issue identifier in the Decision Log entry and mark it done in Linear (or flag it here with `@TODO` if Linear is unreachable from the session).
- When a decision here changes the scope of a Linear issue, update the issue — do not let the two drift.
- New work discovered mid-session becomes a Linear issue, not a bullet that lives here forever. Next Steps below is a short-term pointer, not a backlog.

-----

## Current State

- Repo is a multi-tool prompt-driven scaffolding system (`grovv-stack` v0.6.0) — not an application. Output is docs/config in *other* projects.
- **Multi-tool support added**: Claude Code (original), Vibe, and Codex now supported via tool-specific directories (`.claude/`, `.vibe/`, `.codex/`).
- **Canonical shared definitions** in `.grovv/` directory for tool-agnostic agents and skills.
- Single entry point: the `grovv` skill (`/grovv`, auto-detects new vs adopt). Pipeline: Steps 0–9 in `grovv-stack-scaffold.md`.
- Step 8 (tracker-setup) asks which tracker a target project should use — GitHub Issues (recommended) or Linear — seeds that backlog, and creates/maintains the project's `MEMORY.md`, coordinated with the chosen tracker.
- Six baseline agents: canonical in `.grovv/agents/`, tool-adapted in `.claude/agents/`, `.vibe/agents/`, `.codex/agents/`.
- harness meta-skill vendored under `.grovv/skills/harness/` (Apache-2.0) powers the team-design step, mirrored to tool directories.
- The Throwaway Tier scopes production-first: exploratory artifacts (prototype, mockup, brainstorm, spike) are exempt from the production bar and never merged. `proto/*` or `spike/*` branches, or the gitignored `prototypes/`. Full rules in `grovv-stack-scaffold.md`.
- CI exists: `.github/workflows/checks.yml` runs seven check-only scripts (wordmark, versions, tool sync, references, step numbers, stack tables, ask-first). Standard library only — no build step, and a check enforces that.
- No build steps, no dependencies — documents and configuration only.
- Backward compatible: existing Claude Code users unaffected.

-----

## Decision Log

Append-only, newest first, dated. One line of decision, one line of why. Prune entries older than a few months if no longer load-bearing.

- **2026-07-26** — Added the Throwaway Tier, scoping production-first rather than weakening it. An audit against the "Finding your unknowns" field guide found the principle structurally forbade prototypes: production-readiness plus never-pseudo-code made a disposable mock non-compliant by definition, so unknown knowns surfaced during implementation instead of while reacting to something cheap. Everything that ships is still production-ready; exploratory artifacts are exempt and never merged. Two boundaries carry the weight — a prototype never satisfies an ask-first rule, and code review checks unmerged/throwaway-located/decision-recorded instead of the production checklist.
- **2026-07-26** — Added CI: seven check-only scripts under `.github/`. Each was written after the drift it detects had already happened, not speculatively. Notable: the wordmark rule was stated *incorrectly* in all five places that stated it, and `.grovv/` — the canonical tree — was the wrong copy in two files, so "sync from canonical" would have propagated the error.
- **2026-07-26** — Step 8 is now tracker-agnostic: `docs/prompts/linear-tracking.md` was renamed to `docs/prompts/tracker-setup.md`, and the step opens by asking the user for GitHub Issues (recommended) or Linear. Project Tracking in every stack table now reads "GitHub Issues (recommended) or Linear — chosen per project". Rationale: most scaffolded projects already live in a GitHub repo, so issues, branches, and PRs cross-link with no extra service; Linear stays first-class for multi-repo or cross-team backlogs. This repo's own backlog is unaffected — it stays in Linear (GRO).
- **2026-07-25** — Added multi-tool support for Vibe and Codex. Created `.vibe/`, `.codex/`, and `.grovv/` directories with tool-specific and canonical configurations. Updated all documentation (README.md, CLAUDE.md, created VIBE.md, CODEX.md). Created unified plugin.json. All tool-specific skills and agents adapted for their respective platforms. Backward compatible with existing Claude Code installations.
- **2026-07-04** — Adopted the MEMORY.md convention, both for this repo and as scaffold output (GRO-196, PR #9; promoted from GRO-169). Maintained via tool-specific context file rules plus a `SessionStart` hook; generated in target projects by the linear-tracking step (Step 8), since the two artifacts coordinate: Linear = backlog, MEMORY.md = session context.
- **2026-07-04** — Division of responsibility fixed: never mirror Linear issue lists into memory files; reference identifiers only.

-----

## Gotchas

- The gro\\/\\/ wordmark: doubled backslashes (`gro\\/\\/`) in prose, single (`gro\/\/`) inside code blocks. `.github/scripts/check_wordmark.py` enforces it. Getting this wrong is the most common review catch in this repo.
- Stack or pipeline changes must propagate to **every** doc that references them: `grovv-stack-scaffold.md`, `.grovv/CLAUDE.md` (canonical), `CLAUDE.md`, `VIBE.md`, `CODEX.md`, `.claude/agents/*.md`, `.vibe/agents/*.md`, `.codex/agents/*.md`, `docs/prompts/*`, `README.md`, and all tool-specific grovv skill files. Grep before committing.
- Bump `version` in `.claude-plugin/plugin.json` and `plugin.json` for any behavior change installed users should receive.
- Canonical agents and skills live in `.grovv/`; tool-specific adaptations in `.claude/`, `.vibe/`, `.codex/` — never duplicate into root-level `agents/` or `skills/`.
- Tool-specific context files: `CLAUDE.md` (Claude), `VIBE.md` (Vibe), `CODEX.md` (Codex) at root; `.grovv/CLAUDE.md` is canonical core.
- Ask-first rules (frontend framework, Playwright scope) must never be pre-empted by any generated artifact, including Linear issues and memory entries.

-----

## Next Steps

- Run the GRO-197 smoke test (SessionStart hook fires; Step 8 generates memory in a real target project).
- @TODO — GRO-169's description still lists "memory system" as open; editing it was approval-gated from the agent session (a comment noting the promotion was added instead). Strike it through manually or from an approved session.
- Decide: should a scaffolded project receive tool directories for every CLI its team uses? Today it gets only the one that ran the scaffold, so a project scaffolded from Claude Code is not usable from Codex or Vibe. Agreed direction is to ask the user which tools they use and generate only those, with `.grovv/` canonical when more than one is chosen. Not yet implemented.
- Two prose restatements of the stack cannot be checked structurally — `check_stack_tables.py` reports them without failing. Convert, point at canonical, or accept.
- Loop engineering: Layer 3 (gold-set scoring, grounding) is implemented and Layer 2 is partly covered by harness Phase 0. **Layer 1 is not built** — nothing records a target project's verify commands and nothing generates CI into it. Plan is in `docs/architecture/loop-engineering.md`: fold into Step 1 and Step 6, no new numbered step.
- `check_step_numbers.py` now exists, which was the stated precondition for executing the Step 2 unknowns insertion (renumber 2–9 → 3–10). The map in `docs/architecture/unknowns-engineering.md` still must be re-derived against the tree first — it predates the tracker rename.

-----
gro\\/\\/ stack — Cross-Session Memory
