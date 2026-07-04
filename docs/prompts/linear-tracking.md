# Prompt: Set Up Project Tracking (Linear) and Cross-Session Memory

Use this prompt to stand up **Linear** project tracking and the **MEMORY.md** cross-session memory file for the scaffolded project. It runs as a step in the grovv stack pipeline, **after the agent team is designed and before the README** — once the development plan, technical spec, and agent team exist, the work is seeded into Linear so the build phase has a live backlog.

Linear is the gro\\/\\/ stack default for project and issue tracking. This step uses the **Linear MCP server** to create (or reuse) a project and seed issues from `docs/development-plan.md` and `docs/tech-spec.md`.

The two artifacts coordinate: **Linear owns the backlog** (tasks, priorities, status); **MEMORY.md owns session context** (decisions, rationale, gotchas, in-flight state). Together they let any future agent session pick up exactly where the last one left off without re-deriving the project's state.

-----

## What This Step Produces

In the team's Linear workspace:

- One **Linear project** for the scaffolded codebase (reused if one already exists, created otherwise)
- **Milestones** mirroring the phases/milestones in `docs/development-plan.md`
- **Issues** for the features and technical tasks, with priorities, labels, and milestone assignment
- A link from `docs/development-plan.md` (and later the README) back to the Linear project URL

In the target project's root:

- A **`MEMORY.md`** cross-session memory file, linked to the Linear project
- **Memory maintenance rules** appended to the target project's `CLAUDE.md` (read at session start, update before ending)
- A **`SessionStart` hook** merged into the target project's `.claude/settings.json` that surfaces `MEMORY.md` automatically

It does not invent work. Every issue traces back to a feature in `docs/development-plan.md` or a component in `docs/tech-spec.md`.

-----

## Prerequisites and Guardrails

This step writes to an external system (the user's Linear workspace). Treat it like any outward-facing action — confirm before creating:

- The **Linear MCP server must be available** for the Linear portion. If it is not, skip the Linear workflow (steps 0–4 and 6 below), note it with `@TODO` in `docs/development-plan.md`, and tell the user how to connect Linear — but **still create `MEMORY.md`** (step 5) with the Linear Coordination table marked `@TODO`.
- **Ask which team/workspace** if more than one exists, or if it is ambiguous. Never guess the team.
- **Confirm the plan before bulk-creating issues.** Present the proposed project name, milestones, and the list of issues (titles + priorities) and get approval first. Creating dozens of issues is hard to undo.
- **Never duplicate.** Check for an existing project and existing issues first; match by title and update rather than re-create.
- For existing projects being adopted, prefer **reusing** the team's existing Linear project if one already maps to the codebase.

-----

## Workflow

### 0. Discover

- List Linear teams and projects. Determine the target team (ask if ambiguous).
- Check whether a project already exists for this codebase (match on the project folder name or product name). If found, plan to **reuse and sync** it rather than create a new one.

### 1. Confirm scope

Present to the user and get approval:

- Target team
- Project name (default: the project folder name, lowercase with dashes) and summary (one line from `docs/product-spec.md`)
- The milestones derived from `docs/development-plan.md`
- The issue list (titles, priorities, and which milestone each belongs to)

### 2. Create or reuse the project

- Name: the project folder name. Summary: the one-line product description. Lead: the user (`me`) unless told otherwise.
- Set a start date if the development plan has one; leave the target date as `@TODO` if unknown.

### 3. Seed milestones

- One milestone per phase/milestone in `docs/development-plan.md`. Carry over names and any dated targets.

### 4. Seed issues

Derive issues from `docs/development-plan.md` (features, priorities) and `docs/tech-spec.md` (technical breakdown):

- One issue per feature or discrete task. Title in imperative voice.
- **Priority** from the development plan's ordering (Urgent/High/Medium/Low).
- **Labels** by area where the team uses them (frontend, backend, database, security, testing, infra).
- **Milestone** assignment matching the phase.
- **Estimate** only when the plan gives a clear sizing; otherwise leave unset.
- Link the GitHub repository (and PR, if one exists) on the relevant issues.

Respect the standing gro\\/\\/ stack ask-first rules — do not create issues that pre-decide the frontend framework or Playwright E2E scope; those remain conversations to have when the work is picked up.

### 5. Create the cross-session memory file

Create `MEMORY.md` in the target project's root — the durable memory that coordinates with the Linear project across agent sessions. For existing projects that already have a memory file, extend it rather than replacing it.

Division of responsibility (state it in the file itself):

- **Linear owns the backlog** — tasks, priorities, status, assignments. Never mirror issue lists into `MEMORY.md`; reference issues by identifier (e.g., `ABC-12`).
- **`MEMORY.md` owns session context** — decisions and rationale, gotchas, in-flight state, and anything a fresh session needs that does not fit a Linear issue.

Template:

```markdown
# MEMORY.md

Cross-session memory for [project-name]. Read at session start; update before
ending any session that changed something meaningful. Linear owns the backlog;
this file owns the context.

-----

## How This File Works

- Read at session start (a SessionStart hook surfaces it automatically).
- Update before ending: refresh Current State, append a dated Decision Log
  entry, update Next Steps, prune anything stale.
- Keep under ~120 lines — this file is loaded every session. History lives
  in git; the backlog lives in Linear.

-----

## Linear Coordination

| Field | Value |
|-------|-------|
| Project | [Linear project URL] |
| Team | [team name] |
| Issue prefix | [e.g., ABC] |

- Completed an issue? Note the identifier in the Decision Log and close it
  in Linear (or mark @TODO here if Linear is unreachable).
- Decision changes an issue's scope? Update the issue — never let them drift.
- New work discovered mid-session becomes a Linear issue, not a permanent
  bullet here.

-----

## Current State

[3-6 bullets: what is built, what is in flight, key facts a fresh session needs]

-----

## Decision Log

[Append-only, newest first, dated. One line of decision, one line of why.]

-----

## Gotchas

[Hard-won project-specific knowledge: quirks, footguns, conventions]

-----

## Next Steps

[Short-term pointers only — the backlog lives in Linear]

-----
gro\/\/ stack — Cross-Session Memory
```

Wire up maintenance so the file actually gets used:

- **Append memory rules to the target project's `CLAUDE.md`:** read `MEMORY.md` at session start; before ending a session that changed anything meaningful, update it (Current State, dated Decision Log entry, Next Steps) and sync completed/changed work to Linear.
- **Merge a `SessionStart` hook** into the target project's `.claude/settings.json` (create it if absent, merge if it exists — never clobber existing hooks):

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cat MEMORY.md 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

Keep the memory file honest: it must never contradict `docs/` or the codebase. When it grows past ~120 lines, prune — move anything durable into the tech spec or an ADR, anything actionable into Linear.

### 6. Link back

- Write the Linear project URL into `docs/development-plan.md` (a "Tracking" section) and into the `MEMORY.md` Linear Coordination table so the plan, the memory, and the backlog stay connected. The README step can surface it too.
- Use Linear's `gitBranchName` convention for branches when implementing issues.

### 7. Maintain and sync

This step is re-runnable. On a later run:

- Reconcile `docs/development-plan.md` against the Linear project: add issues for new features, update changed priorities, and flag issues that no longer map to the plan (do not delete silently — surface them).
- Keep milestones aligned with the plan's phases.
- Reconcile `MEMORY.md`: prune stale entries, verify the Linear Coordination table still points at the right project, and confirm the Decision Log's recent entries are reflected in Linear issue states (and vice versa).

-----

## grovv Conventions

- Conversation-driven: confirm the project, milestones, and issue list before writing to Linear.
- Traceability: every issue maps to a `docs/development-plan.md` feature or a `docs/tech-spec.md` component.
- Document style for any grovv-authored notes about tracking: `-----` rules, `@TODO` for unknowns, no emoji in headings.
- Naming: project name lowercase with dashes.
- Memory discipline: `MEMORY.md` stays under ~120 lines, never mirrors the Linear backlog, and never contradicts `docs/` or the codebase.

-----

## Deliverable Checklist

- [ ] Linear MCP availability confirmed (or step skipped with an `@TODO` and instructions)
- [ ] Target team confirmed with the user
- [ ] Existing project/issues checked — reused and synced rather than duplicated
- [ ] Project created or reused, with summary and lead set
- [ ] Milestones mirror `docs/development-plan.md` phases
- [ ] Issues seeded from `docs/development-plan.md` + `docs/tech-spec.md`, each traceable, with priorities and milestones
- [ ] Issue list approved by the user before bulk creation
- [ ] GitHub repo (and PR, if any) linked on relevant issues
- [ ] Linear project URL written back into `docs/development-plan.md`
- [ ] `MEMORY.md` created (or extended) in the target project root, with the Linear Coordination table filled in
- [ ] Memory maintenance rules appended to the target project's `CLAUDE.md`
- [ ] `SessionStart` hook merged into the target project's `.claude/settings.json` (existing hooks preserved)
- [ ] Ask-first rules (frontend framework, Playwright) not pre-empted by any issue or memory entry

-----

## After This Step

Continue the pipeline: proceed to `readme-generator.md`. The README can include a link to the Linear project so contributors find the backlog.

-----
gro\\/\\/ stack — Project Tracking (Linear) and Cross-Session Memory
