# Prompt: Set Up Project Tracking (Linear)

Use this prompt to stand up **Linear** project tracking for the scaffolded project. It runs as a step in the grovv stack pipeline, **after the agent team is designed and before the README** — once the development plan, technical spec, and agent team exist, the work is seeded into Linear so the build phase has a live backlog.

Linear is the gro\/\/ stack default for project and issue tracking. This step uses the **Linear MCP server** to create (or reuse) a project and seed issues from `development-plan.md` and `tech-spec.md`.

-----

## What This Step Produces

In the team's Linear workspace:

- One **Linear project** for the scaffolded codebase (reused if one already exists, created otherwise)
- **Milestones** mirroring the phases/milestones in `development-plan.md`
- **Issues** for the features and technical tasks, with priorities, labels, and milestone assignment
- A link from `development-plan.md` (and later the README) back to the Linear project URL

It does not invent work. Every issue traces back to a feature in `development-plan.md` or a component in `tech-spec.md`.

-----

## Prerequisites and Guardrails

This step writes to an external system (the user's Linear workspace). Treat it like any outward-facing action — confirm before creating:

- The **Linear MCP server must be available**. If it is not, skip this step, note it with `@TODO` in `development-plan.md`, and tell the user how to connect Linear.
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
- Project name (default: the project folder name, lowercase with dashes) and summary (one line from `product-spec.md`)
- The milestones derived from `development-plan.md`
- The issue list (titles, priorities, and which milestone each belongs to)

### 2. Create or reuse the project

- Name: the project folder name. Summary: the one-line product description. Lead: the user (`me`) unless told otherwise.
- Set a start date if the development plan has one; leave the target date as `@TODO` if unknown.

### 3. Seed milestones

- One milestone per phase/milestone in `development-plan.md`. Carry over names and any dated targets.

### 4. Seed issues

Derive issues from `development-plan.md` (features, priorities) and `tech-spec.md` (technical breakdown):

- One issue per feature or discrete task. Title in imperative voice.
- **Priority** from the development plan's ordering (Urgent/High/Medium/Low).
- **Labels** by area where the team uses them (frontend, backend, database, security, testing, infra).
- **Milestone** assignment matching the phase.
- **Estimate** only when the plan gives a clear sizing; otherwise leave unset.
- Link the GitHub repository (and PR, if one exists) on the relevant issues.

Respect the standing gro\/\/ stack ask-first rules — do not create issues that pre-decide the frontend framework or Playwright E2E scope; those remain conversations to have when the work is picked up.

### 5. Link back

- Write the Linear project URL into `development-plan.md` (a "Tracking" section) so the plan and the backlog stay connected. The README step can surface it too.
- Use Linear's `gitBranchName` convention for branches when implementing issues.

### 6. Maintain and sync

This step is re-runnable. On a later run:

- Reconcile `development-plan.md` against the Linear project: add issues for new features, update changed priorities, and flag issues that no longer map to the plan (do not delete silently — surface them).
- Keep milestones aligned with the plan's phases.

-----

## grovv Conventions

- Conversation-driven: confirm the project, milestones, and issue list before writing to Linear.
- Traceability: every issue maps to a `development-plan.md` feature or a `tech-spec.md` component.
- Document style for any grovv-authored notes about tracking: `-----` rules, `@TODO` for unknowns, no emoji in headings.
- Naming: project name lowercase with dashes.

-----

## Deliverable Checklist

- [ ] Linear MCP availability confirmed (or step skipped with an `@TODO` and instructions)
- [ ] Target team confirmed with the user
- [ ] Existing project/issues checked — reused and synced rather than duplicated
- [ ] Project created or reused, with summary and lead set
- [ ] Milestones mirror `development-plan.md` phases
- [ ] Issues seeded from `development-plan.md` + `tech-spec.md`, each traceable, with priorities and milestones
- [ ] Issue list approved by the user before bulk creation
- [ ] GitHub repo (and PR, if any) linked on relevant issues
- [ ] Linear project URL written back into `development-plan.md`
- [ ] Ask-first rules (frontend framework, Playwright) not pre-empted by any issue

-----

## After This Step

Continue the pipeline: proceed to `readme-generator.md`. The README can include a link to the Linear project so contributors find the backlog.

-----
gro\/\/ stack — Project Tracking (Linear)
