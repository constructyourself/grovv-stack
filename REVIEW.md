# REVIEW.md

Review checklist for grovv-stack PRs. Read by the agent reviewer (`.github/workflows/agent-review.yml`) and by humans. Downstream grovv projects keep their own `REVIEW.md` in the same shape.

-----

## Blocking

| Check | What to look for |
|-------|------------------|
| **Propagation** | A stack, pipeline, or step change must land in every file that references it: `grovv-stack-scaffold.md`, `.grovv/CLAUDE.md`, `CLAUDE.md`, `.claude/CLAUDE.md`, `VIBE.md`, `CODEX.md`, `.grovv/agents/*.md` and the `.claude/` / `.vibe/` / `.codex/` copies, `docs/prompts/*`, `README.md`, and every tool's `grovv` skill. Grep the old wording; any surviving copy is a finding. |
| **Canonical first** | Agent and skill edits start in `.grovv/` and are mirrored into each tool directory with only tool-specific adaptation. A change made in one tool directory alone is a finding. |
| **Manifests** | A new or renamed agent updates the `agents` array in `.claude-plugin/plugin.json`. Both `plugin.json` files carry the same `version`. (`scripts/check-consistency.sh` enforces the mechanical part.) |
| **Version bump** | Behavior installed users should receive (agents, skills, prompts, scaffold steps) bumps `version` in both manifests. |
| **Ask-first rules** | Nothing pre-empts the frontend-framework question (Astro + React or Next.js) or the Playwright-scope question — not a prompt, agent, generated issue, or memory entry. |
| **No build steps** | No dependencies, package managers, or compiled artifacts. CI scripts use bash, git, and jq only. |
| **Vendored harness** | `.claude/skills/harness/` and its mirrors stay verbatim (Apache-2.0); changes go in `docs/prompts/team-design.md`, not the vendored files. |

## Should fix

- Wordmark: in Markdown prose the footer uses doubled backslashes so it renders as the gro\\/\\/ wordmark; inside code blocks it uses single backslashes. A bare `gro//` in a footer is a finding (explanatory text that names the wrong form is fine).
- Document conventions: `-----` rules, fenced blocks with language hints, `@TODO` for unknowns, colophon and footer on generated documents.
- `MEMORY.md` updated (Current State, dated Decision Log entry, Next Steps) when the PR changes something a future session needs; kept under ~120 lines; no mirrored issue lists.

## Nit

- Wording, typos, table alignment. Report at most a handful.

-----
gro\\/\\/ stack — Review Checklist
