# MEMORY.md

Cross-session memory for grovv-stack development. An agent starting a session in this repo reads this file first; an agent finishing meaningful work updates it before ending. It works in coordination with the Linear project — Linear owns the backlog, this file owns the context.

-----

## How This File Works

- **Read at session start.** A `SessionStart` hook in `.claude/settings.json` surfaces this file automatically; if hooks are unavailable, read it manually before any other work.
- **Update before ending a session** that changed anything meaningful: refresh Current State, append a dated entry to the Decision Log, update Next Steps, and prune anything stale.
- **Linear owns the backlog.** Tasks, priorities, status, and assignments live in the Linear project. Never duplicate issue lists here — reference issues by identifier instead.
- **This file owns context.** Decisions and rationale, gotchas, in-flight state, and anything a fresh session needs that does not fit a Linear issue.
- **Stay small.** Keep this file under ~120 lines. It is loaded into context every session; verbosity here is a tax on every future session. Prune aggressively — history lives in git.

-----

## Linear Coordination

| Field | Value |
|-------|-------|
| Project | @TODO — Linear project URL (fill in once confirmed via Linear MCP) |
| Team | @TODO |
| Issue prefix | @TODO |

Sync rules:

- When work in this repo completes a Linear issue, note the issue identifier in the Decision Log entry and mark it done in Linear (or flag it here with `@TODO` if Linear is unreachable from the session).
- When a decision here changes the scope of a Linear issue, update the issue — do not let the two drift.
- New work discovered mid-session becomes a Linear issue, not a bullet that lives here forever. Next Steps below is a short-term pointer, not a backlog.

-----

## Current State

- Repo is an installable Claude Code plugin (`grovv-stack` v0.3.0) — a prompt-driven scaffolding system, not an application. Output is docs/config in *other* projects.
- Single entry point: the `grovv` skill (`/grovv`, auto-detects new vs adopt). Pipeline: Steps 0–9 in `grovv-stack-scaffold.md`.
- Step 8 (linear-tracking) now also creates and maintains a `MEMORY.md` in target projects, coordinated with their Linear project.
- Six baseline agents in `.claude/agents/`; harness meta-skill vendored under `.claude/skills/harness/` (Apache-2.0) powers the team-design step.
- No build steps, no dependencies — documents and configuration only.

-----

## Decision Log

Append-only, newest first, dated. One line of decision, one line of why. Prune entries older than a few months if no longer load-bearing.

- **2026-07-04** — Adopted the MEMORY.md convention, both for this repo and as scaffold output. Maintained via CLAUDE.md rules plus a `SessionStart` hook in `.claude/settings.json`; generated in target projects by the linear-tracking step (Step 8), since the two artifacts coordinate: Linear = backlog, MEMORY.md = session context.
- **2026-07-04** — Division of responsibility fixed: never mirror Linear issue lists into memory files; reference identifiers only.

-----

## Gotchas

- The gro\\/\\/ wordmark: doubled backslashes (`gro\\/\\/`) in prose, single (`gro\/\/`) inside code blocks. Getting this wrong is the most common review catch in this repo.
- Stack or pipeline changes must propagate to every doc that references them: `grovv-stack-scaffold.md`, `CLAUDE.md`, `.claude/CLAUDE.md`, `.claude/agents/*.md`, `docs/prompts/*`, `README.md`, and the `grovv` skill. Grep before committing.
- Bump `version` in `.claude-plugin/plugin.json` for any behavior change installed users should receive.
- Agents and skills live only under `.claude/` — never duplicate into root-level `agents/` or `skills/`.
- Ask-first rules (frontend framework, Playwright scope) must never be pre-empted by any generated artifact, including Linear issues and memory entries.

-----

## Next Steps

- @TODO — Fill in the Linear Coordination table once the Linear project is confirmed via the Linear MCP.
- @TODO — Reconcile the existing grovv-stack Linear project issues with the MEMORY.md work (add issues for the convention rollout; update any issue that references the old Step 8 scope).

-----
gro\\/\\/ stack — Cross-Session Memory
