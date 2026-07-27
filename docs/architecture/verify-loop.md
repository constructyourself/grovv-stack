# The Verify Loop

Specification for giving a scaffolded project an inner development loop. Layer 1 of `loop-engineering.md`.

**Status: Phase 1 implemented; Phases 2 and 3 proposed.** Step 1's discovery and the `MEMORY.md` Verify table are in the pipeline. The Step 6 CI question and workflow generation are not — they remain proposals to be approved or rejected before anything runs for a real project.

-----

## Summary

A project scaffolded by gro\\/\\/ stack has no green/red signal. Nothing in Steps 0–9 discovers the commands that make "done" checkable, records them where a later step or a later session can find them, or generates continuous integration into the project. The scaffolder now enforces its own conventions with seven checks while producing projects that inherit none.

The fix is small and it is not a new step. Step 1 records the verify commands, because that is where the project's shape is decided. Step 6 generates the workflow, because that is where generated configuration already lands. `loop-engineering.md` argued that a number in the master directive means every project runs it, and that reasoning holds here: some projects genuinely should decline CI, so the capability is a question rather than an assumption.

The question is the point of this document. The scaffolder does not decide how much CI a project gets. The user does, from four options, at a moment when they know enough to answer.

-----

## The Question, and Where It Is Asked

### Why not Step 1

Step 1 is where the project's directories and configuration are created, which makes it the obvious home. It is the wrong one. At Step 1 the technical specification does not exist yet — Step 4 writes it — so neither the agent nor the user knows the stack. "Which checks do you want?" is unanswerable before "what is this written in?", and an agent that asks anyway will offer a generic list and get a generic answer.

### Why Step 6

By Step 6 the specs exist. `docs/tech-spec.md` names the stack, `docs/development-plan.md` names the phases, and the skills-builder step is already generating configuration into the project's tool directories. The question can be concrete — naming the actual test runner, the actual linter — and the answer can be acted on immediately.

Step 1 still does the recording. Discovering a project's verify commands is cheap in adopt mode and free in new-project mode, the result is useful to every later step whether or not CI is ever generated, and it costs the user nothing because it is not a question.

### The split

| Step | Does | Costs the user |
|------|------|----------------|
| 1 | Discovers the project's verify commands and states them; Step 8 records them in `MEMORY.md` | Nothing — no question is asked |
| 6 | Asks how much CI the project should have, and generates it | One question |

-----

## Step 1: Record the Verify Commands

No question. The agent determines the commands that prove the project is working and records them.

**Adopt mode — read them from the project.** In precedence order, stopping at the first that yields commands:

| Source | What to take |
|--------|--------------|
| `package.json` `scripts` | `test`, `lint`, `typecheck`, `build` — whichever exist, under their real names |
| `Makefile` | Targets named `test`, `lint`, `check`, `build` |
| `Taskfile.yml` / `justfile` | The same task names |
| `go.mod` present | `go test ./...`, `go vet ./...`, and `golangci-lint run` if its config is present |
| An existing CI workflow | The commands its steps actually run — the most reliable source, because it is what the project already trusts |

If two sources disagree, prefer the CI workflow, then the task runner, then the manifest. Record which source was used; a command read from a stale Makefile is worth less than one read from a workflow that runs on every push.

**New-project mode — derive them from the stack.** The tech spec does not exist yet at Step 1, so record the commands implied by the stack once Step 4 has chosen it, and treat Step 1's entry as provisional until then. For the gro\\/\\/ stack defaults that means `vitest run`, `tsc --noEmit`, and the project's linter for TypeScript; `go test ./...` and `go vet ./...` for Go.

**Correction applied during implementation.** This section originally had Step 1 write the table itself. It cannot: `MEMORY.md` does not exist until Step 8 creates it, so Step 1 has no file to write to. As built, Step 1 *discovers and states* the commands and Step 8 *records* them — which also keeps Phase 1 true to its own claim of generating nothing. The table's home is unchanged.

**Where they are recorded.** A `Verify` table in the project's `MEMORY.md`, next to the Tracker Coordination table:

```markdown
## Verify

| Check | Command | Source |
|-------|---------|--------|
| test | `npm test` | package.json scripts |
| typecheck | `npm run typecheck` | package.json scripts |
| lint | `npm run lint` | package.json scripts |
```

`MEMORY.md` is the right home because it is already read at session start by a hook, it already carries the tracker coordination a later session needs, and an agent that knows how to check its own work is exactly what that file exists to provide. A command that is wrong is corrected there rather than rediscovered.

**If nothing is found**, write the table with a single `@TODO` row rather than omitting it. An empty table is a visible gap; a missing table is invisible.

-----

## Step 6: Ask How Much CI

Ask exactly this, substituting the real commands recorded in Step 1:

> This project has no continuous integration. I can add a workflow that runs your checks on every push and pull request, so a break is caught before review rather than after merge.
>
> 1. **Everything** — test, typecheck, lint, and build, on every push and pull request. The strongest signal; also the slowest, and the most likely to need tuning in the first week.
> 2. **Minimal** — tests only. Catches the failures that matter most, stays fast, and is the easiest to keep green. A good starting point if the project's linting is not yet settled.
> 3. **Pick them** — I will list the checks I found and you choose. Right when some of these are not ready to gate a merge yet.
> 4. **None** — no workflow. Correct for a spike, a project whose CI lives somewhere this scaffolder cannot see, or a team that will wire this up themselves.
>
> I found these commands in this project: [list the recorded commands]. If any is wrong, say so — I recorded them from [source] and a wrong command is worse than no workflow.

Four rules govern the answer:

- **Wait for an explicit answer.** "Whatever you think" is not an answer. Name the recommendation for *this* project, say what would change it, and ask them to confirm.
- **Never invent a check the project cannot run.** Only commands recorded in Step 1 may appear in a generated workflow. A workflow that runs `npm run lint` in a project with no lint script fails on its first run and teaches the team to ignore it.
- **Declining is a successful outcome, not a skipped step.** On "None", write one line in `MEMORY.md`'s Verify table recording that CI was offered and declined, and why. That line is what makes a wrong decline visible to a human later. This mirrors how the tracker step records an unavailable tracker rather than failing silently.
- **In adopt mode, if the project already has CI, this becomes a proposal.** State what exists, state what would change, and generate nothing until the user approves. The standing rule against overwriting working code applies to a workflow file exactly as it applies to source.

-----

## The Playwright Interaction

This is the sharpest constraint in the specification, and getting it wrong would break a standing guarantee.

**Playwright scope is ask-first.** The rule is that the agent always asks what Playwright should test before writing any end-to-end test. A generated CI workflow containing an E2E job is that rule being pre-empted by configuration: the workflow asserts that E2E tests exist and should gate merges, which is a decision about scope that only the user makes.

The rule therefore holds without exception:

- **A generated workflow never contains a Playwright or E2E job on the strength of the CI question alone.** Option 1 is "everything" among the checks *recorded in Step 1*, and E2E is not one of them unless the user has separately approved E2E tests and those tests exist.
- **If the project already has Playwright tests and an existing CI workflow that runs them**, that is the user's prior decision and adopt mode preserves it. Preserving an existing job is not the same as generating a new one.
- **If the project has Playwright tests but no CI**, the E2E job is offered as its own question, naming the specs that exist, and never bundled into "everything".

The failure this prevents is quiet and expensive: a scaffolder that generates an E2E job produces a red build on the first push, for tests the user never agreed to write, in a project that has no E2E tests at all. The second-order damage is worse — a team that starts by ignoring a red build.

-----

## What Gets Generated

Per stack, and only from recorded commands:

| Stack | Checks available | Notes |
|-------|-----------------|-------|
| TypeScript | `vitest run`, `tsc --noEmit`, the project's linter, `build` | The runner is whatever the project uses; do not substitute Vitest into a project on another runner |
| Go | `go test ./...`, `go vet ./...`, `golangci-lint run` | Include `golangci-lint` only when its config file is present |
| Both | The union, as separate jobs | A Go failure and a TypeScript failure should be separately legible |

Workflow shape, matching the posture this repository uses on itself where it transfers:

- Each check is its own named step, so a failure names itself in the interface rather than requiring a log read.
- Later steps run even after an earlier one fails, so one run reports every problem instead of only the first.
- Triggers are push and pull request.

What does **not** transfer: this repository is deliberately dependency-free because it produces documents. A scaffolded TypeScript or Go project has a real toolchain, and its workflow will install dependencies and cache them. Copying the no-install posture into a target would produce a workflow that cannot run. The transferable idea is *check-only, named steps, report everything*; the dependency-free part is a property of this repo, not a principle.

-----

## Artifacts

| Path | New or edit | Purpose | Size |
|------|-------------|---------|------|
| `grovv-stack-scaffold.md` | Edit | Step 1: verify-command discovery and the `MEMORY.md` Verify table. Step 6: the CI question, the four options, and the Playwright boundary | +45 |
| `docs/prompts/skills-builder.md` | Edit | The generation rules — per-stack checks, workflow shape, the never-invent-a-check rule, the adopt-mode proposal path | +35 |
| `docs/prompts/tracker-setup.md` | Edit | The `MEMORY.md` template gains the Verify table alongside Tracker Coordination | +12 |
| `.grovv/agents/testing.md` + 3 copies | Edit | Two rules: the verify commands are recorded in `MEMORY.md` and are the definition of done; a generated workflow never contains an E2E job the user did not approve | +6 each |
| `CLAUDE.md`, `.grovv/CLAUDE.md`, `.claude/CLAUDE.md` | Edit | One line each in Key Directives | +1 each |

No new prompt document. No new numbered step. No stack-table row — CI is not a stack choice.

-----

## Phased Rollout

| Phase | Delivers | Standalone? |
|-------|----------|-------------|
| 1 | Step 1 discovery and the `MEMORY.md` Verify table | **Done.** Cost the user no questions and added no generated files | 
| 2 | The Step 6 question and workflow generation | Needs Phase 1's recorded commands |
| 3 | The adopt-mode proposal path for projects that already have CI | Needs Phase 2 |

Phase 1 is the one to approve if only one is approved. It is the smallest change with the widest benefit and it cannot generate anything wrong, because it generates nothing.

-----

## What We Are Deliberately Not Doing

| Rejected | Reason |
|----------|--------|
| A new numbered pipeline step | A number in the master directive means every project runs it. Some projects should decline CI, and the directive is read end to end on every invocation by every project |
| Generating CI without asking | The user's own framing: they choose whole thing, minimal, à la carte, or none. A scaffolder that decides this is deciding how a team works |
| Bundling E2E into "everything" | Playwright scope is ask-first. A workflow with an E2E job is that rule pre-empted by configuration. See above |
| Inventing commands the project cannot run | A workflow that fails on its first run for a missing script teaches the team to ignore red builds — worse than no workflow |
| Copying this repo's dependency-free CI posture into targets | That posture exists because this repo produces documents. A real project needs installs and caching |
| Overwriting an existing workflow in adopt mode | The standing rule against overwriting working code covers configuration as much as source |
| A `verify` skill in the baseline skill set | The baseline set is already ten skills, and running the project's tests is not a body of practice — it is two commands recorded in a file the agent already reads |
| Deploy, release, or publish jobs | Out of scope. This is a verification loop, not a delivery pipeline, and a generated deploy job touches credentials and live systems |

-----

## Open Questions

- Should Phase 1 run in new-project mode at all? The commands are unknown until Step 4 chooses the stack, so a Step 1 entry is provisional and must be revisited. The alternative is to record them at Step 4 and leave Step 1 to adopt mode only, at the cost of splitting one behaviour across two steps. Currently: record at Step 1, mark provisional, reconcile at Step 4.
- What happens when a recorded command later stops working? Nothing detects it. The honest answer is that `MEMORY.md` is maintained by whoever notices, the same as every other line in it. A check that runs the commands would be a real verification loop for the loop — and would mean this repo executing a target project's code, which it must not do.
- Should the generated workflow pin action versions by SHA? More secure, materially worse to read and update, and this is a scaffolder for projects that may never look at it again. Currently: pin to major version tags.
- Is `MEMORY.md` the right home for the Verify table, given its ~120-line budget? Three rows is cheap and the file is already read at session start. If it grows past a handful of commands the answer changes, and the table should move to the tech spec. Currently: `MEMORY.md`, revisit at five rows.
- @TODO — confirm the four option labels read naturally when spoken by an agent mid-conversation. They were written to be read, and the step is conversational.

-----

## Colophon

| Field | Value |
|-------|-------|
| **Version** | 0.1.0 |
| **Last Updated** | 2026-07-26 |
| **Status** | Proposed — not implemented |
| **Author(s)** | grovv stack scaffolding agent |
| **Model** | Claude (Claude Code) |

-----
gro\\/\\/ stack — The Verify Loop
