# Loop Engineering

A diagnosis of what happens after the gro\\/\\/ stack pipeline finishes, and a scoped plan for the three loops it is missing.

**Status, 2026-07-27.** Layer 1 is **complete** — Step 1 discovers the target's verify commands, Step 8 records them in `MEMORY.md`, Step 6 asks a four-option CI question and generates a workflow from exactly those commands, and Step 9's README reads the table instead of inventing `npm` scripts. `docs/architecture/verify-loop.md` is the specification and carries the detail. Layer 2 is **complete** — the third detect branch, the named baseline-skill subject, the settled ask-first clash, and both `## Re-entry` sections with the directive and `scaffold.md` pointers that reach them. `docs/architecture/re-entry.md` is the specification. Layer 3 is the one still partial: seven check-only scripts run in CI, and the smoke-test rubric at `docs/architecture/pipeline-smoke-test.md` has still never been run — which is now the largest open item in this note, because Layers 1 and 2 both added generation the rubric has never scored.

One figure here is stale and should not be reused. This note's recommendation at the top of Part Two prices a renumber at "61 step references across 16 files," and the rejections table repeats it. Re-derived against `HEAD` on 2026-07-27, excluding the vendored harness trees and `docs/architecture/`, the figure is **100 lines across 18 files** — plus 20 more inside the harness trees, where they are that skill's own Korean-language phase numbers in Apache-2.0 code and must never be touched. The conclusion the number supported — do not renumber — held, and was reached again independently for the unknowns pass; see `docs/architecture/unknowns-engineering.md`.

> **Historical note, 2026-07-27.** This document describes the pipeline as it stood when it was written. Step numbers, line citations, and counts below are a snapshot, not a live index — `grovv-stack-scaffold.md` and `docs/prompts/` are the source of truth for what the pipeline does now. Re-derive any locator here before acting on it.

This file is the architecture note of record for the decision. `docs/architecture/` already exists and this document sits in it, so there is no separate ADR to write; the "What We Are Deliberately Not Doing" section is the rejections record a future session should read before re-opening the new-step option. Part One is the diagnosis. Part Two is the plan. Every count and every line citation in this document was re-derived by grep against the **working tree** on the date in the colophon, and each is cited with the paths that produced it. Where a citation is deliberately against some other tree it names that tree inline — `main:` for the pre-fix state of two agent files, `cb733e6` for the commit that fixed them, `pr-10:` for the sibling note. Counts exclude the vendored `skills/harness/` trees and this file.

It has a sibling: `docs/architecture/knowledge-graph-engineering.md` (currently on branch `pr-10`). That note's Phase 1 turns out not to belong to it, and the argument for moving it here is made below.

-----

## Summary

### The diagnosis in about 200 words

`grovv-stack-scaffold.md` defines ten numbered steps — Step 0 through Step 9, at `:152`, `:172`, `:198`, `:245`, `:270`, `:319`, `:370`, `:381`, `:396` and `:408`. They run once. Nothing in the directive and nothing in the kickoff skill defines what run 2 does; exactly one prompt document, Step 8's, defines a second run of itself. The pipeline is a one-shot generator whose termination condition is a list of files existing: the Success Criteria at `:561-575` are fifteen checkboxes, and not one of them names a test that passes, a build that succeeds, a lint that is clean, or a CI job that is green.

The same missing idea appears at three altitudes. The generated project gets no verify loop: no step discovers or records its build, test and lint commands, and no step writes a CI workflow, though four copies of the testing agent assert at `:60` that "all tests must run in CI/CD (GitHub Actions)". grovv gets no re-entry loop: Steps 6 and 7 derive skills and an agent team from `docs/tech-spec.md`, and when that spec changes nothing regenerates, diffs, or reports. And grovv gets no evals: a prompt edit that breaks generation is invisible until a human notices, and the smoke test that would notice has been open since 2026-07-04.

### The recommendation in about 150 words

Fold Layer 1 into Steps 1 and 6, do not give it a number. Step 1 records the target's verify commands; Step 6 generates the workflow that runs exactly those commands. A number would cost 61 step references across 16 files, and — since only an append avoids a full renumber — would place CI generation after the README, which is both too late and the position most likely to be dropped by a long session.

Give Layer 2 a written re-entry contract in the two prompts that need one, plus a third detect branch in the kickoff skill so a grovv-scaffolded project is recognized as such instead of being assessed as a foreign codebase.

For Layer 3, ship what documents can actually enforce: one more check-only CI script that validates the directive's internal contract, and a hand-run smoke-test rubric. An automated golden-output diff is not achievable here and should not be attempted — the reason is the same rule this repo just finished fixing.

-----

## Part One: The Pipeline Is a One-Shot Generator

### What Steps 0-9 terminate on

The directive is explicit that it is conversation-driven and iterative — `:551` says "Documents are living artifacts. Revise as understanding deepens." That instruction has no mechanism behind it. The Success Criteria are the only definition of done the system has, and they are an inventory:

| Criterion shape | Count at `grovv-stack-scaffold.md:561-575` |
|-----------------|--------------------------------------------|
| "X exists" / "X is populated" / "X reflects Y" | 15 |
| Names a command that must run | 0 |
| Names a passing test, a clean lint, or a green CI job | 0 |

Grepping that block for `test|build|lint|ci` returns five lines, and every one of them is an incidental substring: "specification" (`:561`), "skills-builder" (`:566`), "project-specific" (`:568`), "explicitly" (`:569`) and "principles" (`:574`). Case-insensitively it is the same five. Not one names a command. A project can satisfy every criterion and not compile.

That is the whole diagnosis in one sentence, and the three layers below are the same absence measured at three distances from the user:

| Layer | Whose loop | What is missing | What exists instead |
|-------|-----------|-----------------|---------------------|
| 1 | The generated project's inner dev loop | A recorded, runnable definition of "done" and a CI job that enforces it | Fourteen lines asserting that CI exists, and a README template that invents four commands |
| 2 | grovv's own re-entry, run 2..N | A contract for what a second run of Steps 6 and 7 does to the first run's output | One re-entry contract, in Step 8, the only step that writes outside the repository |
| 3 | Evals for the scaffolder itself | Any signal that a prompt edit changed generation for the worse | Four convention checks over this repo's own Markdown, and a smoke test open since July 4 |

Each layer is a case of the same thing: an artifact is produced, and nothing afterward asks whether it is still right. Fixing one does not fix the others, but the fixes are shaped alike — audit what exists, compare it to the source of truth, report the difference before acting.

### Layer 1 — the target project has no green/red signal

Step 1 (`:172-196`) creates three directories and a `settings.json` holding one environment variable. It does not ask what `npm test` is, whether there is a `go.mod`, or what command the project considers "done". In adopt mode, Step 0 (`:154-161`) reads `package.json` and `tsconfig.json` — and records the *stack*, never the *commands*.

Nothing downstream fills the gap. CI is asserted fourteen times across the repository and generated zero times:

| Where CI is asserted | Lines |
|----------------------|-------|
| `agents/testing.md:18` and `:60`, in all four tool trees (`.grovv`, `.claude`, `.vibe`, `.codex`) | 8 |
| `CLAUDE.md:154`, `.claude/CLAUDE.md:153`, `.grovv/CLAUDE.md:132` | 3 |
| `docs/prompts/skills-builder.md:72` (the `deployment-ops` Covers cell), `grovv-stack-scaffold.md:339`, `docs/prompts/readme-generator.md:42` | 3 |

`grep -rn "\.github/workflows"` over tracked Markdown returns nothing outside `.github/` itself. `deployment-ops` is a skill body that *describes* GitHub Actions patterns to a future reader; no step instructs anyone to write a workflow file into the target.

The README step then asserts a dev loop nobody checked. `docs/prompts/readme-generator.md:100-114` emits a hard-coded quick start — `npm install`, `cp .env.example .env`, `npm run db:migrate`, `npm run dev` — as template text. The file contains no instruction to confirm those scripts exist. For a Go project, or a project using pnpm, or one whose migration script is named anything else, the pipeline's final artifact ships four commands that will fail on first use, in the document a new contributor reads first.

Consider what the first agent session in a freshly scaffolded project actually has. It has ten skills describing how to write tests, an agent definition insisting tests run in CI, a development plan, a tech spec, a seeded backlog, and no way to find out whether the code in front of it works. Asked to implement the first issue, it must guess the test command, guess whether the guess was right, and report success on the strength of having written files — which is precisely the failure mode the ten skills exist to prevent, reproduced one level up. The skills teach red-green-refactor to a project with no red and no green.

This is the sharpest form of the diagnosis: grovv is a production-first system that can produce a project in which nothing is runnable and nothing says so.

### Layer 2 — grovv cannot re-enter its own output

Step 6 generates ten baseline skills (`docs/prompts/skills-builder.md:64-73`, mirrored at `grovv-stack-scaffold.md:331-340`), each required to "reference the project's `docs/tech-spec.md` for project-specific customization" (`skills-builder.md:117`). Step 7 designs an agent team, reading the same spec at `team-design.md:66`. Both outputs are therefore derivatives of a document that is explicitly expected to change.

Nothing reconciles them afterward. The evidence is a contrast inside the repository:

| Step | Re-entry contract |
|------|-------------------|
| Step 8 (tracking) | Defined. `docs/prompts/tracker-setup.md:321` — "Stay re-runnable. On a later run, reconcile `docs/development-plan.md` against the tracker" — add issues for new features, update changed priorities, flag issues that no longer map, never delete silently, keep milestones aligned with the plan's phases. Reinforced at `:314`: "Never duplicate... This holds on every re-run." Inherited intact from `linear-tracking.md`, which the rename replaced |
| Steps 6 and 7 | None. `skills-builder.md` has no re-entry section; its nearest analogue, `:175`, is scoped to adopt mode: "If the project already has skills in `.claude/skills/`, extend or update them rather than overwriting" |
| Steps 1-5, 9 | None |

The one step with a defined second run is the one that talks to an external system, where a duplicate would be visible to a human immediately. Everywhere the duplicate would be a file, there is no rule.

Three specific holes:

- **No drift detection against the spec.** `team-design.md:65` runs a harness Phase 0 audit, but it audits the target's existing `.claude/agents/`, `.claude/skills/` and `CLAUDE.md`. Nothing compares either output back to `docs/tech-spec.md`. A spec that switches Postgres for SQLite, or drops Stripe, leaves ten skills asserting the old stack and no signal that they are wrong.
- **Additive with no cap and no named audit.** `team-design.md:37` asks for "the smallest team that covers the domain" — a goal, not a bound. The checklist item at `:143` — "Duplicate review was run before adding each agent and each skill (Phases 3-0, 4-0)" — extends the claim to the skills side, yet nothing anywhere names the ten baseline skills that half of the review is supposed to run against. The dependency is asserted only from the other side, at `skills-builder.md:198`: "Baseline skill names are stable so the team-design audit can dedupe against them." One side promises stability; the other side is never told what to compare.
- **Run 2 is misclassified at the entry point.** `.claude/skills/grovv/SKILL.md:26-34` has exactly two detect branches. "Existing project" is signalled by "source code, configs (`package.json`, `go.mod`, `tsconfig.json`, etc.), or a populated `docs/`". A grovv-scaffolded project has a populated `docs/` by construction. So the second `/grovv` in a project grovv itself built starts at Step 0 and proposes an adoption plan for a codebase it wrote — the mode designed for foreign code, applied to its own output.

### Layer 3 — no evals for the scaffolder

This repository's output is other repositories, which makes its regression surface entirely invisible from inside itself. There is no golden fixture, no sample generated project, and no recorded example of what a correct run produces. A prompt edit that quietly breaks generation is caught only when a human runs the pipeline and dislikes the result.

The one thing that would catch it is a manual smoke test, listed under Next Steps at `MEMORY.md:72`: "Run the GRO-197 smoke test (SessionStart hook fires; Step 8 generates memory in a real target project)." The Decision Log entry that work belongs to is dated `MEMORY.md:53` — 2026-07-04. It has been open at least twenty-two days as of the date in the colophon. (The brief for this note named GRO-127; `GRO-127` appears nowhere in this repository on any branch. `GRO-197` is the identifier of record — see Open Questions.)

The constraint is real and non-negotiable: this repo has no dependencies, no lockfile and no build step, and must not gain any. The check-only CI landing alongside this note honours that exactly — `.github/workflows/checks.yml` runs four steps using Python standard library and `find`, and its own README says "CI therefore validates what is written here; it never builds it." But every one of those checks is a *convention* check: wordmark escaping, manifest version parity, `.grovv/` against its derived tool trees. None of them can tell whether Step 6 still produces ten well-formed skills, because Step 6's output does not exist in this repository.

That CI's own "Known Open Drift" section is itself Layer-3 evidence: it records three real, unfixed divergences — the two manifest versions disagreeing, `.vibe/agents/scaffold.md` diverging beyond path substitution, and `skills/grovv/SKILL.md` diverging in all three tool directories — that existed silently until something finally looked. Running `check_wordmark.py` today reports 34 occurrences across ten tracked files, including `CLAUDE.md:3`, `README.md:12` and — with some irony — `MEMORY.md:60`, the line that states the rule. Every one of them was invisible until the first check was written, in a repository that calls this "the most common review catch."

Sorted by what can catch what, the regression surface looks like this:

| Breakage | Caught today by | Catchable without a runtime |
|----------|-----------------|------------------------------|
| A convention violation in this repo's Markdown | The four check-only scripts | Yes — already done |
| A prompt edit that contradicts the master directive (a renamed prompt, a step number that no longer matches, an enumeration that says "five") | Nothing | Yes — structural, greppable |
| A prompt edit that degrades what Step 6 generates | Nothing | No — the output does not exist here |
| Run 2 duplicating or clobbering run 1's output | Nothing | No — requires an actual second run |

The middle row is the one worth buying, and it is the largest class by frequency: every change to this repository is a prompt edit.

### The mis-filed half of Layer 3

`pr-10:docs/architecture/knowledge-graph-engineering.md` proposes a phased rollout whose Phase 1 (`:563`, `:567-595`) is described as "grounding discipline" and justified as the cheapest slice of a knowledge-graph adoption. It is not a knowledge-graph decision. It is the evaluation half of Layer 3, and the note itself says so in passing at `:567`: "Every line of it applies to every project grovv scaffolds, including every project that will correctly decline a graph forever."

What Phase 1 actually fixes is a contradiction between two baseline agents. On `main`:

```markdown
- Tests must be deterministic — no flaky tests
```

That is `main:.claude/agents/testing.md:60` (file length 95). And:

```markdown
- [ ] Tests are deterministic and not flaky
```

That is `main:.claude/agents/code-review.md:41` (file length 79), where the same rule is a blocking review checkbox. Neither carries a carve-out.

For any project shipping a model-backed feature, these two lines make correct work unshippable. The testing agent forbids writing the only test that can evaluate a prompt — a score against a hand-labelled gold set, which varies run to run and cannot carry an equality assertion. If a developer writes one anyway, the code-review agent is instructed to block it, because a scored evaluation is by construction non-deterministic. The two agents are not merely redundant; they close the loop against each other. The producer is told not to write the test, and the reviewer is told to reject it if written. The result is that model-backed features ship with no quality signal at all, which is the exact failure this repository's production-first principle exists to prevent.

That is a Layer 3 defect in grovv's guidance about evaluation, wearing knowledge-graph clothing because that is where it happened to be noticed. It ships separately, and it is landing now — which produces the second piece of evidence for this note's thesis.

PR #10's artifact table (`pr-10:...:516-518`) scoped Phase 1 to three files and about 55 lines. In the commit that landed it (`cb733e6`) it is 9 files and 184 insertions — `git show cb733e6 --stat -- '*agents/testing.md' '*agents/code-review.md' docs/prompts/team-design.md` — because `testing.md` and `code-review.md` now exist in four trees rather than one. The multi-tool split (`MEMORY.md:52`, dated 2026-07-25) landed the same day PR #10 measured its cascade, and the estimate was stale before it was read. Nothing detected that. Nothing could have.

The same erosion is measurable on the numbers PR #10 based its central argument on:

| Grep | PR #10, 2026-07-25 (`:419-421`) | Re-derived today | Change |
|------|-------------------------------|------------------|--------|
| Numbered step references (`[Ss]teps? [0-9]`, Markdown + JSON) | 37 lines / 9 files | 61 lines / 16 files | +65% lines |
| "Steps 0-9" range expressions | 6 lines / 6 files | 11 lines / 11 files | +83% |
| Step references in JSON manifests | 0 | 0 | unchanged |

### What the repository already gets right

Three counterweights, so the diagnosis is not read as worse than it is. Step 8's prompt has a genuine, well-written re-entry contract that the other steps can be modelled on — the pattern does not need inventing, only copying. The harness Phase 0 audit at `team-design.md:65` establishes that auditing before acting is already the house idiom. And the check-only CI proves that meaningful automated enforcement is possible here inside the no-dependency rule; the question for Layer 3 is only what else can be expressed in that form.

-----

## Part Two: The Plan

### Layer 1 — fold into Steps 1 and 6

Two edits to existing steps, no new step, no new artifact in the target beyond a workflow file.

**Step 1 records the verify commands.** After the `settings.json` block at `:196`, Step 1 gains a short subsection: determine the project's build, test and lint commands and write them into the target's `CLAUDE.md` as a three-row table. In adopt mode the commands are read from `package.json`, `go.mod`, `Makefile` or the CI config that Step 0 already opened, and each one is run once to record whether the project is currently green or red — a baseline, not a gate. In new mode the stack is not yet chosen, so the table is created with `@TODO` in each cell and reconciled at Step 6. `CLAUDE.md` is the right home because it is the one file loaded into every future session in that project; the tech spec links to it rather than duplicating it.

**Correction applied during implementation.** As built, Step 1 *discovers and states* the commands and Step 8 *records* them in the `MEMORY.md` Verify table — not the target's `CLAUDE.md`, and not at Step 1. The paragraph above describes the design as planned, and is left in place as the record of what was intended; it is not what shipped. See `verify-loop.md:62`. A later change made from the paragraph above rather than this note re-introduces the original defect, which is a write to a file that does not exist yet at that point in the sequence. The two Open Questions below about where the table lives are answered by this correction and are no longer open.

The table is three rows and one rule, and it is the smallest artifact in this plan:

```markdown
## Verify

| Check | Command | Baseline |
|-------|---------|----------|
| Build | npm run build | green 2026-07-26 |
| Test  | npm test      | green 2026-07-26 |
| Lint  | npm run lint  | @TODO not configured |

Run all three before reporting any task done. If a command is missing, say so
rather than substituting a different one.
```

The second sentence of that rule is the part that matters. Today an agent that cannot find a test command invents one; the instruction converts a silent guess into a stated gap.

**Step 6 generates the CI.** `skills-builder.md` already owns `deployment-ops`, already claims GitHub Actions, and already runs after the stack is settled. It gains a section instructing the step to write a workflow into the target that runs exactly the commands recorded in Step 1 — not a generic template — and to replace any remaining `@TODO` in the verify table with the command it just wired up. If the project already has CI, the step reports what it found and proposes an addition rather than writing over it, per the standing never-overwrite rule.

**Step 9 stops inventing commands.** `readme-generator.md`'s quick start reads the verify table instead of hard-coding npm.

### Why this must not become a numbered step

PR #10 rejected a new step on the grounds that "a numbered step is a promise that the step runs, and a permanent lengthening of a document whose cost is paid by every project" (`:624`). For a default-off capability that argument is decisive. Here the premise inverts — every project *should* have a verify loop — so the argument has to be made differently, and it still lands.

**A step is a phase; this is a property of two phases.** Steps 0-9 each terminate in an artifact. The verify loop is not one artifact produced once: it is a fact recorded when the project is first understood and a file generated when the stack is known. Splitting it out would separate the recording from the moment the commands become knowable, and separate both from the CI that runs them.

**Position, and the cascade that constrains it.** Inserting a step mid-pipeline requires renumbering: 61 numbered references across 16 files, 11 of them "Steps 0-9" range expressions, in four mirrored tool trees that `check_tool_sync.py` tier b now holds to parity after path normalization. Appending is far cheaper — the 11 ranges and the four `agents/scaffold.md` lists change, the rest stay correct — but appending means Step 10, after the README. CI would then be generated after the project has already been documented as working, and it would sit in the position a long session is most likely to drop. The defect being fixed is "nothing happens at the end of the run." Putting the fix at the end inherits it.

**The general form of PR #10's principle still applies.** A number tells every future agent that this is a separable phase, deferrable and skippable. Folded into Steps 1 and 6, it is inseparable from work that already always happens.

### Layer 2 — a written re-entry contract

Model it on `tracker-setup.md:321`, which already works. Each of the two prompts gains a `## Re-entry` section stating what a second run does:

1. **Audit before writing.** Enumerate what exists. For Step 6 that is the skill folders present and the stack each asserts; for Step 7 the project-specific agents and their stated rationale.
2. **Diff against the current spec.** Re-read `docs/tech-spec.md` and name every artifact whose assumptions no longer match it. This is the check that does not exist today at all.
3. **Report before acting.** Present three lists — unchanged, drifted, orphaned — and wait. Never delete silently, exactly as Step 8 already requires.
4. **Update, never append blindly.** A skill whose name already exists is revised, never duplicated with a suffix. A specialist agent whose rationale no longer maps to any spec component is surfaced for removal, not left standing.
5. **Re-justify rather than inherit.** Step 7's additive rule stays, but on a second run each existing specialist must be re-argued against the current spec, and the audit explicitly names the ten baseline skills by folder name so the dedupe check has a subject.
6. **Preserve hand edits.** A generated file modified by hand is reported and asked about, never overwritten. This is the never-overwrite rule applied to grovv's own output.

The question run 2 is asking, stated once so both prompts can inherit it: *given a spec that has moved since these artifacts were generated, which of them are still implied by it?* Three answers, three actions.

| Verdict | Meaning | Action |
|---------|---------|--------|
| Unchanged | The artifact's assumptions still match the spec | Leave it alone and say so |
| Drifted | The spec changed under it — a different database, a dropped integration, a renamed component | Propose the specific revision, name the spec line that moved |
| Orphaned | Nothing in the current spec justifies it | Surface it for removal; never delete without approval |

The entry point gains a third detect branch: if `docs/prompts/skills-builder.md` and a populated `.claude/skills/` are both present, this is a grovv-scaffolded project, and the run resumes — go to the re-entry contract, not to Step 0. The artifacts are the marker; no version file is introduced (see the rejections).

This is the cheapest of the three layers to specify and the easiest to get wrong in implementation, because every clause of it is a restraint. A re-entry run that changes nothing and returns a list of questions is a successful run, in the same way that declining the knowledge-graph capability is a successful outcome of Step 6 in the sibling note. Both are cases of the pipeline being allowed to conclude that the right action is no action — something a one-shot generator has never had to express.

### Layer 3 — what documents alone can do

Split the problem by what is mechanically checkable.

**Checkable now, in the existing check-only CI.** The class of breakage where a prompt edit silently contradicts the directive is structural, and structure is greppable. A fifth script, `check_directive_contract.py`, standard library only, in the shape `.github/scripts/README.md` already prescribes:

- Step headings in `grovv-stack-scaffold.md` are contiguous and start at 0.
- Every `docs/prompts/*.md` on disk is referenced by the directive, and every prompt the directive names exists on disk. (This check fails today: `docs/prompts/` holds six files, but `grep -n tech-spec-template grovv-stack-scaffold.md` returns nothing — `tech-spec-template.md` exists on disk and the directive never names it, referenced only from inside `docs/prompts/tech-spec.md`.)
- Every prompt that declares its own step number declares one the directive agrees with — `skills-builder.md:3` says Step 6, `team-design.md:3` says Step 7.
- Every enumeration of the prompt set agrees with the set on disk. Three currently say five where the directory holds six: `grovv-stack-scaffold.md:566` in words, and `grovv-stack-scaffold.md:103-107` and `README.md:91` by listing exactly five entries.
- The Success Criteria name every artifact the steps promise to create.

**Checkable by hand, against a written rubric.** Whether Step 6 still produces ten well-formed skills can only be established by running the pipeline. `docs/architecture/pipeline-smoke-test.md` becomes the rubric: a throwaway target directory, the run, and a scored checklist covering both a first run and — the case nothing has ever exercised — a second run against the first run's output with the spec edited in between. It lives in `docs/architecture/` deliberately: Step 5 creates the prompt set inside every target project, while `docs/architecture/` is created empty at `:180` and stays empty by `:571` ("exists for future ADRs"), so a rubric placed here does not travel into anyone's project.

**Not achievable, and it should be said plainly.** An automated golden-output diff is out of reach, for the reason the newly-fixed testing agent now states in its own words: model-backed output is scored against a hand-labelled gold set, not equality-checked. Byte-diffing a generated skill against a stored fixture would fail on every run for reasons that are not defects. Scoring it properly requires a scorer, a gold set, and judgment — and a scorer is executable code with dependencies, which this repository forbids. The rule grovv writes for its targets applies to grovv: the scorer belongs in the throwaway project, not here. What this repository can hold is the rubric and the structural checks.

### Artifacts

| Path | New or edit | Layer | Purpose | Size |
|------|-------------|-------|---------|------|
| `grovv-stack-scaffold.md` | Edit | 1, 2 | Step 1 verify-commands subsection after `:196`; a CI paragraph in Step 6; one sentence each in Steps 6 and 7 pointing at the re-entry contract; two Success Criteria items; one File-and-Folder row | +29 on 578 |
| `docs/prompts/skills-builder.md` | Edit | 1, 2 | A "Generated CI" section wiring the recorded commands into a target workflow; a `## Re-entry` section; the `deployment-ops` Covers cell; three checklist items | +54 on 201 |
| `docs/prompts/team-design.md` | Edit | 2 | A `## Re-entry` section; the baseline-skill audit named explicitly at `:143`; one checklist item | +26 on 163 |
| `docs/prompts/readme-generator.md` | Edit | 1 | Quick start reads the verify table instead of hard-coding npm at `:100-114` | +6 on 342 |
| `.grovv/skills/grovv/SKILL.md` and three derived copies | Edit | 2 | Third detect branch: already-scaffolded resumes, it does not adopt | +8 each, 32 total |
| `.grovv/agents/testing.md` and three derived copies | Edit | 1 | `:60`'s CI claim points at the generated workflow rather than asserting one exists | +2 each, 8 total |
| `.grovv/agents/scaffold.md` and three derived copies | Edit | 2 | One line on re-entry in Scaffolding Order | +2 each, 8 total |
| `.github/scripts/check_directive_contract.py` | New | 3 | The five structural checks above; standard library, under 150 lines, resolves repo root from `__file__` | ~130 |
| `.github/workflows/checks.yml` | Edit | 3 | One named step, `if: ${{ !cancelled() }}` like its siblings | +3 |
| `.github/scripts/README.md` | Edit | 3 | One table row and one section, matching the existing per-script format | +16 |
| `docs/architecture/pipeline-smoke-test.md` | New | 3 | The hand-run rubric: first run, second run with an edited spec, scored checklist | ~90 |
| `MEMORY.md` | Edit | — | Version, a dated Decision Log entry referencing the tracker issue by identifier, one Gotchas line on the four-tree fan-out | +5 on 76 |

Roughly 190 lines of edits across 17 files plus about 220 new lines. The four-tree fan-out accounts for 48 of the edit lines on its own — a cost worth stating explicitly, because every estimate in this repository written before 2026-07-25 understates it.

### Phased rollout

| Phase | Delivers | Size |
|-------|----------|------|
| 1 — Layer 3 structural checks | `check_directive_contract.py`, its workflow step and README section. Zero cascade, and it catches two live defects on the first run: `tech-spec-template.md` unreferenced by the directive, and the three prompt-set enumerations that say five where the directory holds six | ~150 lines, half a day |
| 2 — Layer 1 | Step 1 and Step 6 edits, the README quick start, the four testing-agent copies | ~45 lines across 7 files, one day |
| 3 — Layer 2 | Both `## Re-entry` sections, the third detect branch in four trees, the scaffold-agent lines | ~70 lines across 11 files, one to two days |
| 4 — The rubric, and running it | `pipeline-smoke-test.md`, then an actual run against a throwaway project — which is also the long-open smoke test | ~90 lines plus a session |

Phase 1 stands alone and is startable as written. Phase 4 is the only one that produces evidence rather than instructions, and it is the one that has been deferred since July 4.

### Relationship to the knowledge-graph note

The two notes overlap at exactly one place and should not be merged.

| | `knowledge-graph-engineering.md` | This note |
|---|---|---|
| Scope | A conditional capability grovv can scaffold into some targets | A property every target and every run needs |
| Default | Off, behind a two-condition gate | On, unconditionally |
| Overlap | Phase 1: the determinism contradiction and gold-set scoring | Layer 3, the evaluation half |

Phase 1 moves here in substance and ships on its own branch. What stays in the knowledge-graph note is everything downstream of the gate. The reason to separate them is not tidiness: a reviewer evaluating a default-off capability applies a much higher bar than one evaluating a fix to two contradicting lines, and Phase 1 has been carrying the wrong bar. Its own note says as much at `pr-10:...:567` — "If exactly one phase is approved, approve this one."

-----

## What We Are Deliberately Not Doing

| Rejected | Reason |
|----------|--------|
| A numbered Step 10 for CI or verification | A step is a phase producing an artifact; this is a property of two existing phases. Insertion costs a renumber across 61 references in 16 files; appending is cheap but puts CI after the README, which is both too late and the position a long session drops first. See below |
| A numbered step for the re-entry contract | Same objection, plus a worse one: a re-entry step would run at the end of run 1, where there is nothing to re-enter |
| An eleventh baseline skill (`ci-loop` or similar) | `skills-builder.md:60` sanctions dropping baseline skills that seem irrelevant, so a baseline row makes the verify loop opt-out. CI is already `deployment-ops`'s stated scope at `:72`; the gap is that nothing generates a file, not that nothing describes one |
| A seventh baseline agent for devops or evals | Seven roster enumerations and thirteen prose counts of "six" (`pr-10:...:548`), now across four tool trees. Doctrinally wrong besides: harness holds that skills are how and agents are who, and "run the verify commands" is overwhelmingly how |
| A committed golden-output tree in this repository | Thousands of generated lines that go stale on the first prompt edit, in a repo whose whole point is that its output lives elsewhere. And equality-diffing model-backed output is precisely what `agents/testing.md:61-67` was just rewritten to forbid |
| A runnable scorer under `.github/scripts/` | Already rejected once (`pr-10:...:617`) for the same reason: executable code with dependencies in a repository whose output is documents. A scorer needs a gold set of generated documents and human judgment, neither of which is standard library. It belongs in the throwaway target project |
| grovv-stack's own CI executing a scaffolded project's verify commands | That requires a Node or Go runtime here, which is the one thing the repo may never gain. The scaffolding agent runs inside the target's working directory and can run them there; this repository cannot |
| A `.grovv-version` or similar marker file in target projects | Hidden state that must be maintained and will drift — the two `plugin.json` versions already have, per `.github/scripts/README.md`'s Known Open Drift. The artifacts are the marker: `docs/prompts/skills-builder.md` plus a populated `.claude/skills/` is unambiguous |
| A seventh prompt document (`ci-setup.md`) | Step 5 copies `docs/prompts/` into every target, so a seventh file travels into every project. It also reopens the prompt-set enumeration cascade — eight locations, three of which currently say "five" |
| A new root file in target projects for the verify table | A third root-level artifact alongside `README.md` and `MEMORY.md`, for three rows. `CLAUDE.md` is already loaded every session and already carries project rules |
| A machine-readable spec-to-artifact manifest to make drift diffable | That is a knowledge graph over the scaffolding's own artifacts, rejected in the sibling note (`pr-10:...:628`) for a corpus that fits in one context window and needs the dependency this repo forbids. The drift report stays prose and judgment |
| Fixing the prompt-set enumerations while here | Real and worth fixing — `docs/prompts/` holds six files while `grovv-stack-scaffold.md:103-107`, `:566` and `README.md:91` all say five, and `tech-spec-template.md` is named nowhere in the directive — but it belongs to the prompt set, not to a loop-engineering change. The new CI check will keep failing until it is done, which is the correct pressure |
| Making the generated workflow provider-agnostic | Four agent copies already assert GitHub Actions at `:60`. Generating for one provider and asking when the project already has CI elsewhere is cheaper and more honest than a matrix of templates nobody has run |
| Having Step 1 fail the run when a verify command is missing | A new project at Step 1 has no commands by construction, and an adopted project with a red test suite is a fact to record, not a reason to refuse to scaffold. `@TODO` and a recorded baseline are the grovv-idiomatic answers; a gate here would block the projects that need the pipeline most |
| A `## Re-entry` section in all six prompt documents for symmetry | Steps 2-5 and 9 rewrite whole documents and already behave correctly on a second pass; only Steps 6 and 7 append into a directory. Sections that say "nothing special happens here" are how prompts get long enough to stop being read |
| Extending `check_tool_sync.py` to compare generated skills across projects | There are no generated skills in this repository to compare, and reaching into a target project's tree from this repository's CI inverts the dependency the whole design rests on |

The two longest arguments, in prose rather than in cells.

**A numbered step.** The cost is real: 61 numbered references across 16 files, 11 of them range expressions that change even under an append, in four mirrored trees now held to parity by `check_tool_sync.py`. But the cascade is a supporting argument. The decisive one is that appending is the only affordable placement, and appending puts the verify loop after the README — after the project has already been documented as working. A verify loop generated last is a verify loop that arrives after every decision it was supposed to constrain, in the slot most likely to be skipped when a session runs long or a user says "that's enough for today." The failure mode being repaired is that the pipeline's end is where things stop happening. The repair cannot live there.

**A golden-output eval.** This is the rejection most likely to be re-litigated, because "just commit a sample and diff it" sounds obviously correct. It fails twice over. Mechanically: generation is model-backed, so the diff is noise, and the repo's own testing guidance — as of the change landing beside this note — says model-backed output is scored against a hand-labelled gold set with a no-regression gate, never equality-checked. Structurally: a scorer is code with dependencies, and this repository has none and gets none. What remains is worth having and should not be undersold. The structural contract check catches the largest real class of regression, which is a prompt edit that contradicts the directive, and it costs about 130 lines of standard library. The rest is a rubric and a human, which is exactly what `pr-10:...:637` concluded when it hit the same wall from the other side: "narrow Phase 3 to schemas, prompts, storage DDL, and decision rules, and mark any full-stage implementation explicitly as unvalidated reference until it has been run in a throwaway project."

-----

## Open Questions

- ~~Where does the verify table live in the target?~~ **Answered by the implementation: `MEMORY.md`, written at Step 8.** Step 1 states the commands and carries them forward. Separately, the question exposed a real structural gap — the target's context file was written by Steps 7 and 8 and created by nothing, so Step 1 now creates it as a stub, which is where the tool choice that decides *which* context files exist is made.
- New projects have no commands at Step 1. Step 6 is nominated to reconcile the `@TODO`, but Step 4 is where the stack is actually decided. Currently: recorded empty at Step 1, filled at Step 6, because Step 6 is where the workflow that runs them is written.
- What happens on re-entry when a generated skill was edited by hand? Overwriting destroys work; skipping preserves drift forever. Currently: report and ask, matching the never-overwrite rule — at the cost of a re-entry run that can end with nothing changed and a list of questions.
- Should the smoke-test rubric ever be run by an agent on a schedule rather than by a human? That needs a live API budget and a runtime, and it turns a rubric into a harness. Currently: manual, tracked as a tracker issue.
- Is a drift report worth anything if "what the spec implies" is never written down in a comparable form? A human reading two documents is the whole mechanism. The alternative is the artifact manifest rejected above. Currently: prose report, accepting that its quality is the reading agent's quality.
- Does the third detect branch risk a false positive — a project with a `docs/prompts/skills-builder.md` copied in by hand but never run? Currently accepted: the branch reports what it detected and why before acting, so a wrong detection costs one correction turn.
- Who owns the three drifts recorded under Known Open Drift in `.github/scripts/README.md`, and the 34 wordmark occurrences the checker reports? All are flagged with `@TODO` and no issue identifier. Leaving them unowned is how they became drift in the first place, and a check whose failures nobody owns trains people to ignore the check.
- Does the generated workflow run on push, on pull request, or both? Copying this repository's own `checks.yml` (`on: push` and `on: pull_request`) is the obvious default, but a target project with a paid CI budget may want otherwise. Currently: both, stated in the prompt as a default the user can change during Step 6.
- ~~Should Layer 1's verify table travel into `MEMORY.md` as well?~~ **Answered: `MEMORY.md` is its only home**, written at Step 8, referenced from the tech spec. The premise of the question — that `CLAUDE.md` held it — was corrected during implementation.
- @TODO — Confirm the tracker identifier before this is cited in a commit message. The brief for this note named GRO-127; `GRO-127` appears nowhere in this repository on `main`, `pr-10`, `pr-11`, `pr-17` or `HEAD`. The only smoke-test identifier present is GRO-197, at `MEMORY.md:72`. The Linear MCP was not reachable from this session to check whether GRO-127 exists under a different description.

-----

## Colophon

| Field | Value |
|-------|-------|
| Version | 0.1.0 |
| Last Updated | 2026-07-26 |
| Status | Draft |
| Author(s) | grovv stack scaffolding agent |
| Model | Claude (Claude Code) |

-----
gro\\/\\/ stack — Loop Engineering
