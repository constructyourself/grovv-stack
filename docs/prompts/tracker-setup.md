# Prompt: Set Up Project Tracking and Cross-Session Memory

Use this prompt to stand up the scaffolded project's **issue tracker** and its **`MEMORY.md`** cross-session memory file. This is the **tracker-setup step (Step 8)** of the gro\\/\\/ stack pipeline: it runs **after `team-design.md` (Step 7) and before `readme-generator.md` (Step 9)**. By this point the product spec, development plan, technical spec, and agent team all exist, so the work can be seeded into a live backlog.

Two trackers are supported — **GitHub Issues** and **Linear**. The step **always asks the user which one** before doing anything else (see Step 0). Either way the same two artifacts result, and they coordinate: **the project's tracker owns the backlog** (tasks, priorities, status); **`MEMORY.md` owns session context** (decisions, rationale, gotchas, in-flight state). Together they let any future agent session pick up exactly where the last one left off without re-deriving the project's state.

-----

## What This Step Produces

It does not invent work — every issue traces back to a feature in `docs/development-plan.md` or a component in `docs/tech-spec.md`. In the chosen tracker:

- One **project or repository backlog** for the scaffolded codebase (reused if one already exists, created otherwise)
- **Milestones** mirroring the phases in `docs/development-plan.md`
- **Issues** for the features and technical tasks, with labels/priorities and milestone assignment
- A link from `docs/development-plan.md` (and later the README) back to the tracker

In the target project's root:

- A **`MEMORY.md`** cross-session memory file, linked to the tracker
- **Memory maintenance rules** appended to the target project's `CLAUDE.md` (read at session start, update before ending)
- A **`SessionStart` hook** merged into the target project's `.claude/settings.json` that surfaces `MEMORY.md` automatically

-----

## Step 0: Tracker Selection

**This runs before anything else, and it is always a question.** The agent must not choose silently, must not infer the tracker from the presence of a `.git` remote or a Linear MCP connection, and must not start creating labels, milestones, or issues until the user has answered.

Ask exactly this:

> Which issue tracker should this project use?
>
> 1. **GitHub Issues (recommended)** — it is the gro\\/\\/ stack ecosystem default as of 2026-07-25, and it lives in the same repo as the code, so issues, branches, and PRs cross-link with no extra service.
> 2. **Linear** — worth choosing when the project needs heavy cross-referencing: multiple repos, initiatives spanning teams, or a backlog shared with people who do not live in GitHub.

- Wait for an explicit answer. If the user says "whatever you think", state the recommendation (GitHub Issues) and ask them to confirm it — a stated default is still an answer they gave.
- Record the choice in `MEMORY.md` (Tracker Coordination table) so later sessions do not re-ask.
- Follow **Path A** for GitHub Issues, **Path B** for Linear. Do not run both.

-----

## Path A: GitHub Issues

### A0. Preflight

Confirm tooling **before** creating anything. Run, in the target project's root:

```bash
gh --version
gh auth status
REPO="$(gh repo view --json nameWithOwner --jq .nameWithOwner)"
gh api "repos/$REPO" --jq '.permissions.push'
```

Expected: `gh auth status` reports a logged-in account whose token scopes include `repo`, `$REPO` resolves to the intended `org/repo`, and the last command prints `true` (write access — required to create labels, milestones, and issues). Then, in order:

| Situation | Action |
|-----------|--------|
| `gh` present, authenticated, `push` is `true` | Proceed with the `gh` commands below. |
| `gh` missing, unauthenticated, or lacking `repo` scope | Fall back to the **GitHub MCP server** — same workflow, MCP tools instead of `gh` (`search_issues` / `list_issues` to check for duplicates, `issue_write` to create, `get_label` to verify the taxonomy). The MCP server has no milestone-creation tool: create the issues, then write an `@TODO` in `docs/development-plan.md` asking the repo owner to add the milestones and back-fill them. |
| Neither `gh` nor the GitHub MCP server is available | **Skip and stop.** Write an `@TODO` into the target project's `MEMORY.md` (Tracker Coordination table + Next Steps) recording that tracker setup is pending and what unblocks it (`gh auth login --scopes repo`, or connecting the GitHub MCP server), then continue the pipeline. Do **not** half-create the taxonomy or a partial issue list. |

### A1. Label taxonomy

Create the labels **before any issue**, so no issue is ever created unlabeled. `--force` makes this re-runnable — it updates an existing label instead of failing.

```bash
gh label create "type:feature"       --repo "$REPO" --color 1D76DB --description "New capability from the development plan" --force
gh label create "type:bug"           --repo "$REPO" --color D73A4A --description "Defect in existing behavior" --force
gh label create "type:improvement"   --repo "$REPO" --color 0E8A16 --description "Refactor, performance, or DX work" --force
gh label create "status:backlog"     --repo "$REPO" --color EEEEEE --description "Accepted, not yet scheduled" --force
gh label create "status:todo"        --repo "$REPO" --color BFBFBF --description "Scheduled, not started" --force
gh label create "status:in-progress" --repo "$REPO" --color 8B8B8B --description "Actively being worked" --force
gh label create "resolution:canceled" --repo "$REPO" --color 4A4A4A --description "Closed without being done" --force
```

Verify the result with `gh label list --repo "$REPO"`.

State semantics — status labels apply to **open issues only**, and closed state carries the outcome:

| State | Representation |
|-------|----------------|
| Backlog | open + `status:backlog` |
| Todo | open + `status:todo` |
| In Progress | open + `status:in-progress` |
| Done | closed, **no resolution label** |
| Canceled | closed + `resolution:canceled` |

Exactly one `status:*` label per open issue, and none on a closed one. Closing an issue is therefore two commands — strip the status label, then close with the reason that matches the outcome:

```bash
gh issue edit 42 --repo "$REPO" --remove-label "status:in-progress"
gh issue close 42 --repo "$REPO" --reason completed

gh issue edit 43 --repo "$REPO" --remove-label "status:todo" --add-label "resolution:canceled"
gh issue close 43 --repo "$REPO" --reason "not planned"
```

### A2. Milestones

Use **native GitHub Milestones**, not a Project board. Rationale, in order of weight:

- **Native to Issues** — a milestone is a first-class field on every issue; no extra object model to keep in sync.
- **No extra auth scope** — milestones work with the `repo` scope the preflight already confirmed; Projects need `project`, which requires an interactive re-auth.
- **Maps 1:1 to Linear milestones** — the same phase list produces the same structure on either path, so `MEMORY.md` and the development plan read identically.

Seed one milestone per phase in `docs/development-plan.md`. Check first, then create — keep `due_on` (ISO-8601) only when the plan gives a dated target, and drop that flag otherwise:

```bash
gh api "repos/$REPO/milestones?state=all" --jq '.[] | "\(.number)\t\(.state)\t\(.title)"'

gh api --method POST "repos/$REPO/milestones" \
  -f title="Phase 2 — Billing" \
  -f state="open" \
  -f description="Seeded from docs/development-plan.md" \
  -f due_on="2026-09-30T00:00:00Z"
```

`@TODO` — an aggregating **monitoring GitHub Project** (a cross-milestone board view) is out of scope for this step. It requires the `project` scope, which only an interactive `gh auth refresh -s project` run by the repo owner can grant. Note it in `docs/development-plan.md` and move on; the milestones above are sufficient for the backlog.

### A3. Seed issues

Derive issues from `docs/development-plan.md` (features, ordering) and `docs/tech-spec.md` (technical breakdown). One issue per feature or discrete task, title in imperative voice.

**Check for duplicates first — always, including on re-runs:**

```bash
gh issue list --repo "$REPO" --state all --limit 200 --json number,state,title \
  --jq '.[] | "\(.number)\t\(.state)\t\(.title)"'
```

Match on title. If an issue already covers the work, **update it** (`gh issue edit`) rather than creating a second one.

**Confirm the full list with the user before bulk-creating.** Present the proposed milestones and every issue title with its labels and milestone, and get approval. Creating dozens of issues is hard to undo.

Only then create them, one command per issue:

```bash
gh issue create --repo "$REPO" \
  --title "Verify Stripe webhook signatures before processing events" \
  --body "Source: docs/development-plan.md — Phase 2, Billing. Acceptance: every inbound webhook is verified against STRIPE_WEBHOOK_SECRET; unverified payloads are rejected with 400 and logged." \
  --label "type:feature" \
  --label "status:backlog" \
  --milestone "Phase 2 — Billing"
```

Every issue body opens with a `Source:` line naming the document and section it came from — that is the traceability contract.

Respect the standing gro\\/\\/ stack ask-first rules: do not create issues that pre-decide the frontend framework or the Playwright E2E scope. Those remain conversations to have when the work is picked up.

### A4. Reference format

In `MEMORY.md`, commit messages, PR bodies, and every downstream document, reference issues as **`org/repo#NN`** (for example, `constructyourself/grovv-stack#42`). The fully qualified form stays unambiguous when the reference is read outside the repo. Branch naming: `<NN>-<short-slug>`.

-----

## Path B: Linear

Linear is set up through the **Linear MCP server**. If it is unavailable, skip this path, note it with `@TODO` in `docs/development-plan.md`, tell the user how to connect Linear, and **still create `MEMORY.md`** with the Tracker Coordination table marked `@TODO`.

### B0. Discover

- List Linear teams and projects. Determine the target team — **ask if ambiguous, never guess**.
- Check whether a project already exists for this codebase (match on the project folder name or product name). If found, plan to **reuse and sync** it rather than create a new one.

### B1. Confirm scope

Present and get approval before writing anything:

- Target team
- Project name (default: the project folder name, lowercase with dashes) and summary (one line from `docs/product-spec.md`)
- The milestones derived from `docs/development-plan.md`
- The issue list (titles, priorities, and which milestone each belongs to)

### B2. Create or reuse the project, then seed milestones

- Name: the project folder name. Summary: the one-line product description. Lead: the user (`me`) unless told otherwise.
- Set a start date if the development plan has one; leave the target date as `@TODO` if unknown.
- One milestone per phase in `docs/development-plan.md`, carrying over names and any dated targets.

### B3. Seed issues

- One issue per feature or discrete task. Title in imperative voice.
- **Priority** from the development plan's ordering (Urgent/High/Medium/Low).
- **Labels** by area where the team uses them (frontend, backend, database, security, testing, infra).
- **Milestone** assignment matching the phase.
- **Estimate** only when the plan gives a clear sizing; otherwise leave unset.
- Link the GitHub repository (and PR, if one exists) on the relevant issues.
- Search existing issues by title before creating — update rather than duplicate.
- As on the GitHub path, do not create issues that pre-decide the frontend framework or Playwright scope.

### B4. Reference format

Reference issues by the team's issue prefix and number — for example, `GRO-123`. Use Linear's `gitBranchName` convention for branches when implementing issues.

-----

## Cross-Session Memory

This section applies to **both paths**, with only the Tracker Coordination table differing. Create `MEMORY.md` in the target project's root — the durable memory that coordinates with the tracker across agent sessions. For existing projects that already have a memory file, extend it rather than replacing it.

Division of responsibility (state it in the file itself):

- **The project's tracker owns the backlog** — tasks, priorities, status, assignments. Never mirror issue lists into `MEMORY.md`; reference issues by the path's reference format.
- **`MEMORY.md` owns session context** — decisions and rationale, gotchas, in-flight state, and anything a fresh session needs that does not fit an issue.

Template:

```markdown
# MEMORY.md

Cross-session memory for [project-name]. Read at session start; update before
ending any session that changed something meaningful. The project's tracker
owns the backlog; this file owns the context.

-----

## How This File Works

- Read at session start (a SessionStart hook surfaces it automatically).
- Update before ending: refresh Current State, append a dated Decision Log
  entry, update Next Steps, prune anything stale.
- Keep under ~120 lines — this file is loaded every session. History lives
  in git; the backlog lives in the tracker.

-----

## Tracker Coordination

| Field | Value |
|-------|-------|
| Tracker | [GitHub Issues or Linear] |
| Project / Repo | [org/repo, or the Linear project URL] |
| Reference format | [org/repo#NN, or ABC-123] |
| Status source | [open + status:* labels / closed state, or Linear issue state] |

- Completed an issue? Note the reference in the Decision Log and close it in
  the tracker (or mark @TODO here if the tracker is unreachable).
- Decision changes an issue's scope? Update the issue — never let them drift.
- New work discovered mid-session becomes a tracker issue, not a permanent
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

[Short-term pointers only — the backlog lives in the tracker]

-----
gro\/\/ stack — Cross-Session Memory
```

Keep the memory file honest: it must never contradict `docs/` or the codebase. When it grows past ~120 lines, prune — move anything durable into the tech spec or an ADR, anything actionable into the tracker.

-----

## SessionStart Hook

Wire up maintenance so the file actually gets used:

- **Append memory rules to the target project's `CLAUDE.md`:** read `MEMORY.md` at session start; before ending a session that changed anything meaningful, update it (Current State, dated Decision Log entry, Next Steps) and sync completed or changed work to the tracker.
- **Merge a `SessionStart` hook** into the target project's `.claude/settings.json` — create the file if absent, merge if it exists. **Preserve existing hooks:** read the current `hooks` object, append to the `SessionStart` array, and write the merged result. Never overwrite the object wholesale.

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cat \"$CLAUDE_PROJECT_DIR/MEMORY.md\" 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

The `$CLAUDE_PROJECT_DIR` prefix is required — a bare `cat MEMORY.md` resolves against the session's working directory and silently prints nothing when a session starts in a subdirectory. The `2>/dev/null || true` tail keeps a missing file from failing the hook.

-----

## Guardrails

These apply to **both paths**:

- **Ask first.** The tracker choice (Step 0) is always a question. So is the target team on the Linear path, and the target repo on the GitHub path when more than one remote exists.
- **Confirm the plan before bulk-creating.** Present the milestones and the full issue list, with labels and priorities, and get approval before the first create command runs.
- **Never duplicate.** Search existing issues and milestones by title first; update the match rather than creating a second one. This holds on every re-run.
- **Skip gracefully.** If the required tooling is unavailable, write an `@TODO` recording what is pending and what unblocks it, then stop that path cleanly — never leave a half-created taxonomy or a partial backlog.
- **Never overwrite an existing tracker setup.** An existing Linear project, an existing label taxonomy, or an existing milestone set is reused and synced, not replaced. Surface conflicts to the user instead of resolving them silently.
- **Traceability.** Every issue maps to a `docs/development-plan.md` feature or a `docs/tech-spec.md` component.
- **Ask-first rules survive.** No issue and no memory entry may pre-empt the frontend-framework choice or the Playwright E2E scope.
- **Document style** for any grovv-authored notes about tracking: `-----` rules, `@TODO` for unknowns, tables for reference data, no emoji in headings. Project names lowercase with dashes.
- **Link back.** Write the tracker location (repo URL or Linear project URL) into a "Tracking" section of `docs/development-plan.md` and into the `MEMORY.md` Tracker Coordination table, so the plan, the memory, and the backlog stay connected. The README step surfaces it too.
- **Stay re-runnable.** On a later run, reconcile `docs/development-plan.md` against the tracker (add issues for new features, update changed priorities, flag issues that no longer map to the plan — surface them, never delete silently), keep milestones aligned with the plan's phases, and prune `MEMORY.md` while verifying its Tracker Coordination table still points at the right place.

-----

## Deliverable Checklist

- [ ] Tracker choice put to the user explicitly, with GitHub Issues stated as the recommendation
- [ ] Chosen tracker recorded in the `MEMORY.md` Tracker Coordination table
- [ ] (GitHub) `gh` preflight run — installed, authenticated with `repo` scope, push access confirmed; MCP fallback used if not, or the path skipped with an `@TODO` if neither was available
- [ ] (GitHub) Full label taxonomy created before the first issue, native milestones seeded from the plan's phases
- [ ] (GitHub) `@TODO` recorded for the out-of-scope aggregating monitoring Project
- [ ] (Linear) Linear MCP availability and target team confirmed; project created or reused with milestones mirroring the plan's phases
- [ ] Existing issues checked — reused and synced rather than duplicated
- [ ] Issue list approved by the user before bulk creation
- [ ] Issues seeded from `docs/development-plan.md` + `docs/tech-spec.md`, each traceable to its source
- [ ] Tracker location written back into `docs/development-plan.md`
- [ ] `MEMORY.md` created (or extended) in the target project root, Tracker Coordination table filled in
- [ ] Memory maintenance rules appended to the target project's `CLAUDE.md`
- [ ] `SessionStart` hook merged into `.claude/settings.json`, guarded form, existing hooks preserved
- [ ] Ask-first rules (frontend framework, Playwright) not pre-empted by any issue or memory entry

-----

## After This Step

Continue the pipeline: proceed to `readme-generator.md` (Step 9). The README can link to the tracker so contributors find the backlog.

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
gro\\/\\/ stack — Project Tracking and Cross-Session Memory
