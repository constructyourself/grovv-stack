# Prompt: Set Up Project Tracking and Cross-Session Memory

Use this prompt to stand up the scaffolded project's **issue tracker** and its **`MEMORY.md`** cross-session memory file. This is the **tracker-setup step (Step 8)** of the gro\\/\\/ stack pipeline: it runs **after `team-design.md` (Step 7) and before `readme-generator.md` (Step 9)**. By this point the product spec, development plan, technical spec, and agent team all exist, so the work can be seeded into a live backlog.

This is a **generic tracker step**. Two trackers are implemented today — **GitHub Issues** and **Linear** — and the step is structured so a third can be added without rewriting it (see "Adding Another Tracker"). Everything that is not tracker-specific lives in "The Common Path"; each tracker supplies four things and nothing more.

The step **always asks the user which tracker to use** before doing anything else (see Step 0). Whichever is chosen, the same two artifacts result, and they coordinate: **the project's tracker owns the backlog** (tasks, priorities, status); **`MEMORY.md` owns session context** (decisions, rationale, gotchas, in-flight state). Together they let any future agent session pick up exactly where the last one left off without re-deriving the project's state.

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

Both implemented trackers are fully supported. GitHub Issues is the gro\\/\\/ stack recommendation, and a recommendation is a starting position with reasons attached — not a conclusion the question is a formality around. Give the user what they need to disagree with it: both options, the reasoning behind each, and the condition that flips the answer.

Ask exactly this:

> Which issue tracker should this project use? Both are fully supported — pick the one that matches how this project will actually be run.
>
> 1. **GitHub Issues** — the gro\\/\\/ stack recommendation. It lives in the same repo as the code, so issues, branches, and PRs cross-link with no extra service to run and no second account for a contributor to hold.
> 2. **Linear** — the better choice when the project needs heavy cross-referencing: multiple repos, initiatives spanning teams, cycles and estimates, or a backlog shared with people who do not live in GitHub.
>
> If the second description fits this project better than the first, choose Linear. The recommendation assumes one repo and a small team — worth checking against this project rather than inheriting.

- Wait for an explicit answer. A recommendation is not an answer. If the user says "whatever you think", say why GitHub Issues is the recommendation **for this project**, name the condition that would flip it to Linear, and ask them to confirm — a stated default is still an answer they gave.
- If the user names a tracker neither path covers (Jira, Shortcut, a plain `docs/backlog.md`), do not quietly substitute one of these two. See "Adding Another Tracker".
- Record the choice in `MEMORY.md` (Tracker Coordination table) so later sessions do not re-ask.
- Follow **Path A** for GitHub Issues, **Path B** for Linear. Do not run both.

-----

## The Common Path

Every stage below is tracker-independent: it holds whichever path runs, and it is what a third tracker would have to honour unchanged. The tracker-specific mechanics live in Path A and Path B — nothing in this section belongs to either.

| Stage | What happens, on every tracker |
|-------|--------------------------------|
| 1. Preflight | Confirm the tracker is reachable and writable **before** creating anything |
| 2. Reuse or create | Find the existing backlog for this codebase and reuse it; create one only when none exists. Never replace an existing setup |
| 3. Milestones | One milestone per phase in `docs/development-plan.md`, carrying over names and any dated targets |
| 4. Confirm the plan | Present the proposed milestones and every issue title, with labels/priority and milestone, and get approval before the first create command runs |
| 5. Never duplicate | Search existing issues by title first — on the first run and on every re-run. A match is updated, never duplicated |
| 6. Seed from the plan | Every issue traces to a `docs/development-plan.md` feature or a `docs/tech-spec.md` component, and its body opens with a `Source:` line naming that document and section |
| 7. Record the reference format | Write the tracker, the backlog location, the reference format, and the status source into the `MEMORY.md` Tracker Coordination table, and link the backlog from `docs/development-plan.md` |
| 8. Ask-first rules survive | No issue and no memory entry pre-decides the frontend framework or the Playwright E2E scope |

**Skip gracefully.** If the preflight fails and the path has no fallback mechanism left, stop that path cleanly: write an `@TODO` into `MEMORY.md` (Tracker Coordination table + Next Steps) and `docs/development-plan.md` recording that tracker setup is pending and exactly what unblocks it, then continue the pipeline. Still create `MEMORY.md` — it does not depend on the tracker existing. Never leave a half-created taxonomy or a partial backlog behind.

-----

## What a Tracker Supplies

A tracker plugs into the common path by supplying exactly four things. Path A and Path B are these four filled in:

| Contract | GitHub Issues (Path A) | Linear (Path B) |
|----------|------------------------|-----------------|
| **Reference format** | `org/repo#NN`; branches `<NN>-<short-slug>` | `ABC-123`; branches from Linear's `gitBranchName` |
| **Status model** | Open + exactly one `status:*` label; closed state carries the outcome | Native Linear issue states |
| **Creation mechanism** | `gh` CLI, falling back to the GitHub MCP server | Linear MCP server |
| **Availability preflight** | `gh --version`, `gh auth status`, push permission on the repo | Linear MCP server reachable, target team identified |

-----

## Path A: GitHub Issues

The common path implemented with `gh`. A0 is the preflight (stage 1), A1–A2 the taxonomy and milestones (stages 2–3), A3 the confirm-dedupe-seed sequence (stages 4–6, 8), A4 the reference format recorded in memory (stage 7).

### A0. Preflight

Confirm tooling **before** creating anything. Run, in the target project's root:

```bash
gh --version
gh auth status
export REPO="$(gh repo view --json nameWithOwner --jq .nameWithOwner)"
gh api "repos/$REPO" --jq '.permissions.push'
```

Expected: `gh auth status` reports a logged-in account whose token scopes include `repo`, `$REPO` resolves to the intended `org/repo`, and the last command prints `true` (write access — required to create labels, milestones, and issues).

**`$REPO` does not survive between fenced blocks.** Most agents run each block as its own shell invocation, so a later `--repo "$REPO"` expands to an empty string and `gh` fails with `expected the "[HOST/]OWNER/REPO" format`. Either run all of Path A in a single shell session, or substitute the literal `org/repo` into every command below before running it.

Then, in order:

| Situation | Action |
|-----------|--------|
| `gh` present, authenticated, `push` is `true` | Proceed with the `gh` commands below. |
| `gh` missing, unauthenticated, lacking `repo` scope, or `.permissions.push` is `false` | Fall back to the **GitHub MCP server** — same workflow, MCP tools instead of `gh` (`search_issues` / `list_issues` to check for duplicates, `issue_write` to create, `get_label` to verify the taxonomy). The MCP server has no milestone-creation tool: create the issues, then write an `@TODO` in `docs/development-plan.md` asking the repo owner to add the milestones and back-fill them. |
| Neither `gh` nor the GitHub MCP server is available | **Skip gracefully** (common path): `@TODO` recording that tracker setup is pending and what unblocks it — `gh auth login --scopes repo`, or connecting the GitHub MCP server — then continue the pipeline. Do **not** half-create the taxonomy or a partial issue list. |

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

The same common path implemented through the **Linear MCP server**. B0 is the preflight and reuse check (stages 1–2), B1 the confirmation (stage 4), B2 the project and milestones (stages 2–3), B3 the seeding (stages 5–6, 8), B4 the reference format recorded in memory (stage 7).

If the Linear MCP server is unavailable, skip gracefully: note it with `@TODO` in `docs/development-plan.md`, tell the user how to connect Linear, and **still create `MEMORY.md`** with the Tracker Coordination table marked `@TODO`.

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

## Adding Another Tracker

Two paths exist because two trackers are implemented, not because two is the limit. Jira, Shortcut, a plain `docs/backlog.md` — any of them is a legitimate future Path C. Adding one touches exactly four places:

| Edit site | What changes |
|-----------|--------------|
| Step 0's ask block | One more numbered option, with the condition that makes it the right choice |
| "What a Tracker Supplies" | One more column, filling in the four contract items |
| A new path section | The mechanics — preflight, taxonomy, milestones, seeding, reference format |
| Deliverable Checklist | The path's own preflight and taxonomy items, alongside the existing `(GitHub)` and `(Linear)` ones |

Nothing else moves. The common path, the `MEMORY.md` template (its Tracker Coordination placeholders name no tracker), the `SessionStart` hook, and the guardrails all hold unchanged.

A tracker is ready to add when it can supply all four contract items:

| Requirement | What it must state |
|-------------|--------------------|
| **Reference format** | The unambiguous way an issue is written in `MEMORY.md`, commit messages, and PR bodies, plus the branch-naming convention that follows from it |
| **Status model** | How Backlog, Todo, In Progress, Done, and Canceled are each represented, so `MEMORY.md` can name one status source |
| **Creation mechanism** | The concrete tool that creates milestones and issues — a CLI, an MCP server, an API — and the fallback when the first choice is unavailable |
| **Availability preflight** | The checks that prove the tracker is reachable and writable before anything is created, and what a failure means: fall back, or skip with an `@TODO` |

Until a tracker supplies all four, do not offer it in Step 0. If a user asks for one that is not implemented, say so plainly, offer the paths that are, and record the request as an `@TODO` — never improvise a half-path.

-----

## Cross-Session Memory

This section applies to **both paths** — the template is identical on either, and only the values filled into the Tracker Coordination table differ. Create `MEMORY.md` in the target project's root — the durable memory that coordinates with the tracker across agent sessions. For existing projects that already have a memory file, extend it rather than replacing it.

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
| Tracker | [the chosen tracker] |
| Project / Repo | [the backlog's location — repo or project URL] |
| Reference format | [the tracker's reference format] |
| Status source | [the tracker's status source] |

- Completed an issue? Note the reference in the Decision Log and close it in
  the tracker (or mark @TODO here if the tracker is unreachable).
- Decision changes an issue's scope? Update the issue — never let them drift.
- New work discovered mid-session becomes a tracker issue, not a permanent
  bullet here.

-----

## Verify

| Check | Command | Source |
|-------|---------|--------|
| [test / typecheck / lint / build] | `[the real command]` | [where it was read from] |

- These are the commands that prove this project works. Step 1 discovered them
  by reading the project; fill this table from what it found.
- Found none? Write one row of `@TODO` rather than omitting the table. An empty
  table is a visible gap; a missing one is invisible.
- A command that stops working is corrected here, not rediscovered.
- CI: [which of these the generated workflow runs — or that CI was offered at
  Step 6 and declined, and why]. Recording a decline is what makes a wrong one
  visible later.

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

The common path states **what** every tracker does. These are the standing rules about **how**, and they hold on every path, implemented or future, and on every re-run:

- **Ask first.** The tracker choice (Step 0) is always a question, and the recommendation never answers it. So is every ambiguous case inside a path — the target team on the Linear path, the target repo on the GitHub path when more than one remote exists.
- **Never overwrite an existing tracker setup.** An existing Linear project, an existing label taxonomy, or an existing milestone set is reused and synced, not replaced. Surface conflicts to the user instead of resolving them silently.
- **Link back.** Write the tracker location (repo URL or Linear project URL) into a "Tracking" section of `docs/development-plan.md` and into the `MEMORY.md` Tracker Coordination table, so the plan, the memory, and the backlog stay connected. The README step surfaces it too.
- **Stay re-runnable.** On a later run, reconcile `docs/development-plan.md` against the tracker (add issues for new features, update changed priorities, flag issues that no longer map to the plan — surface them, never delete silently), keep milestones aligned with the plan's phases, and prune `MEMORY.md` while verifying its Tracker Coordination table still points at the right place.
- **Document style** for any grovv-authored notes about tracking: `-----` rules, `@TODO` for unknowns, tables for reference data, no emoji in headings. Project names lowercase with dashes.

-----

## Deliverable Checklist

- [ ] Tracker choice put to the user explicitly, with both options and their reasoning presented — GitHub Issues stated as a recommendation the user was asked to weigh, not a default applied on their behalf
- [ ] Chosen tracker recorded in the `MEMORY.md` Tracker Coordination table, along with its reference format and status source
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
| **Version** | 1.1.0 |
| **Last Updated** | 2026-07-26 |
| **Status** | Active |
| **Author(s)** | Dan |
| **Model** | Claude (Claude Code) |

-----
gro\\/\\/ stack — Project Tracking and Cross-Session Memory
