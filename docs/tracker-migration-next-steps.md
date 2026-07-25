# Next steps — make tracker setup ecosystem-aware (Linear → GitHub Issues)

> Status: **planning doc, not yet implemented.** Written 2026-07-25 so this can be picked up in a
> follow-up session. Nothing in this repo has been changed yet — this only maps out what needs to.

## Why

`constructyourself/grovv-planning` executed a tracker migration on 2026-07-25
(`plans/tracker-migration.md` there has the full record): most grovv projects now track issues in
**GitHub Issues**, not Linear. Only four projects stay in Linear — **shipments.fyi**,
**support@shipments.fyi**, **futures.exchange**, **portshift** — because they're the heaviest /
most cross-referenced. Everything else (16 projects at migration time, and by default any new one)
tracks work as GitHub Issues in its own repo, with a label taxonomy standing in for Linear's
status/type fields.

grovv-stack currently hardcodes **Linear as the only supported tracker** — it's baked into Step 8
of the scaffold pipeline, a dedicated prompt document, and both `CLAUDE.md` files. A newly
scaffolded project today would always get a Linear project, which no longer matches the
ecosystem's actual default. This doc maps out what needs to change so grovv-stack offers both,
defaulting new projects to the same choice grovv-planning made.

## What needs to change

### 1. `docs/prompts/linear-tracking.md` → generalize (the biggest piece)

Currently 224 lines, entirely Linear-specific: creates/reuses a Linear project via the Linear MCP,
seeds milestones + issues from `docs/development-plan.md` / `docs/tech-spec.md`, and writes the
target project's `MEMORY.md` with a "Linear Coordination" table.

Target shape:

- Rename to something tracker-neutral — e.g. `docs/prompts/tracker-setup.md`. (This is pre-1.0
  internal tooling; a clean rename is fine, no need for a redirect stub.)
- Add a **tracker-selection step** at the top, before anything else:
  - If the target codebase already has a `grovv-planning` registry entry reachable (e.g. the agent
    can read `registry.yaml` from a sibling checkout or the user pastes it in), use its `tracker:`
    field.
  - Otherwise **ask the user** — "Linear or GitHub Issues?" — and default the *recommendation* to
    **GitHub Issues**, matching the ecosystem-wide default since 2026-07-25. Still ask; don't
    silently choose.
- **If GitHub Issues is chosen:**
  - Create the label taxonomy in the target repo (see table below) via `gh label create`.
  - Seed issues from the development plan via `gh issue create --label "type:X,status:Y"` instead
    of the Linear MCP.
  - `MEMORY.md`'s coordination table references issues as `org/repo#NN`, not `GRO-###`.
  - No Linear MCP dependency — this path only needs `gh` authenticated against the target repo.
- **If Linear is chosen** — keep today's flow as-is (Linear MCP, milestones, `GRO-###` in
  `MEMORY.md`). Still useful for a project expected to need Linear's heavier cross-referencing.
- Guardrails carry over either way: ask-first, confirm the plan before bulk-creating, never
  duplicate existing issues, skip gracefully with `@TODO` if the chosen tracker's tooling is
  unavailable (Linear MCP unreachable, or `gh` not authenticated).

### 2. `grovv-stack-scaffold.md` — Step 8 and its supporting references

- **Step 8** ("Set Up Project Tracking (Linear) and Cross-Session Memory", ~line 396) — retitle to
  drop the Linear-only framing; describe the tracker-selection logic above instead of assuming
  Linear + the Linear MCP.
- The **prompt-reference table** entry for `docs/prompts/linear-tracking.md` (~line 141) — update
  the filename and description once renamed.
- **Tree diagrams** referencing `linear-tracking.md` (~lines 105, 122) — same rename.
- **Step 9's completion checklist** (~lines 564, 567–568) — "Linear project tracking is set up…"
  and "the Linear Coordination table" — generalize wording to cover both trackers.
- The **repository-map "Project Tracking" row** (~line 463) — currently `Linear (via Linear MCP)`.

### 3. `.claude/CLAUDE.md` and root `CLAUDE.md`

- **"Project Tracking" table rows** in both files — generalize from `Linear (via Linear MCP)` to
  something like `Linear or GitHub Issues (per-project choice)`.
- **MEMORY.md conventions** section (`.claude/CLAUDE.md` ~198–215, root `CLAUDE.md` ~54–61) —
  "Linear owns the backlog; MEMORY.md owns context" → generalize to "the project's tracker owns the
  backlog."
- **Env var section** in `.claude/CLAUDE.md` (~249–255) listing `LINEAR_API_KEY` — note it's
  conditional now, only needed if the scaffolded project (or this repo's own tracking) uses Linear.

### 4. Reference conventions to adopt (mirror grovv-planning exactly)

| Tracker | Reference format | Status source |
|---|---|---|
| Linear | `GRO-123` | Backlog / Todo / In Progress / Done / Canceled |
| GitHub Issues | `org/repo#NN` | open + label, per the taxonomy below |

**GitHub label taxonomy** (create these in any repo that chooses GitHub Issues):

| Label | Meaning |
|---|---|
| `type:feature` / `type:bug` / `type:improvement` | mirrors Linear's issue-type labels |
| `status:backlog` / `status:todo` / `status:in-progress` | on **open** issues only |
| *(closed, no resolution label)* | = Done |
| `resolution:canceled` *(on a closed issue)* | = Canceled |

## Open questions to resolve when picking this up

- **Rename outright, or generalize in place?** Renaming `linear-tracking.md` → `tracker-setup.md`
  is cleaner but touches every file that links to it (all listed above). Worth doing in one PR
  rather than splitting the rename from the behavior change.
- **Registry lookup vs. always-ask.** Checking grovv-planning's `registry.yaml` for an existing
  `tracker:` value only works if the scaffolding session has that repo accessible — which won't
  always be true for a fresh clone elsewhere. Might be simplest to always ask, and mention the
  registry as a hint the user can check themselves.
- **Monitoring Project.** grovv-planning's migration plan calls for one aggregating GitHub Project
  ("Grovv", linked to `grovv-planning`) that auto-adds issues from every GitHub-tracked repo — not
  yet stood up (needs an interactive `gh auth refresh -s project` the founder has to run). If it
  exists by the time this is picked up, decide whether Step 8's GitHub path should also add the new
  repo to that Project (`gh project item-add` or the "auto-add" workflow should already cover new
  repos automatically once configured — probably no action needed here).
- **Existing projects using the old flow.** No grovv-stack-scaffolded project needs retroactive
  changes — this only affects newly scaffolded or newly adopted projects going forward.

## Reference

Full migration record and rationale: `constructyourself/grovv-planning`, `plans/tracker-migration.md`
(executed 2026-07-25) — has the complete label taxonomy, per-project mapping, and execution log.
