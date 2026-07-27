# The Re-entry Contract

Specification for what a second run of the gro\\/\\/ stack pipeline does to the first run's output. Layer 2 of `loop-engineering.md`.

**Status: Phase 1 implemented; Phases 2 through 4 proposed.** The ten baseline skill names are now stated in `team-design.md`, so its Phase 4-0 duplicate review has the subject it has always claimed. The `## Re-entry` sections themselves are not written. This document specifies a `## Re-entry` section for two prompt documents and nothing else. No prompt file has been edited. `grep -rn "Re-entry\|re-entry\|re-run" docs/prompts/` returns five lines at the time of writing, all of them in `tracker-setup.md` — `:60`, `:111`, `:171`, `:379` and `:384`. That is the entire re-entry vocabulary the pipeline has.

One dependency **has already landed** and is deliberately not re-specified here: the third detect branch in the kickoff skill (`b369164`), so that a second `/grovv` in a project grovv itself built is recognized as a resume rather than assessed as foreign code. This document specifies what happens *after* a run has been correctly identified as a resume.

That commit also sets two expectations this document must live up to rather than introduce. It instructs a resuming run to "re-read `docs/tech-spec.md`, report which existing artifacts it still implies and which have drifted under it, and wait", and it states that "a run that changes nothing and returns a list of questions is a successful run." Both are one-sentence promises made at the entry point to a pipeline that has no machinery behind them. Everything below is that machinery.

-----

## Summary

Steps 6 and 7 derive their output from `docs/tech-spec.md`, a document the directive explicitly expects to change — `grovv-stack-scaffold.md:607` says "Documents are living artifacts. Revise as understanding deepens." Nothing reconciles the derived artifacts afterward. Step 8 is the only step in the pipeline with a defined second run, and the reason is visibility: it writes into GitHub Issues or Linear, where a duplicate lands in a human's inbox within hours. Everywhere a duplicate would just be a file on disk, there is no rule.

The fix is two `## Re-entry` sections, modelled clause by clause on the one that already works. It is the cheapest of `loop-engineering.md`'s three layers to specify and the easiest to get wrong, because every clause of it is a restraint. Nothing here adds a step, a marker file, a manifest, or a generated artifact. It adds roughly a hundred and twenty lines of instruction that mostly tell a second run what *not* to do.

Of the three ideas this specification turns on, one is absent from the repository entirely and two are asserted at the entry point with nothing behind them. Absent: a named subject for the duplicate review that `team-design.md:143` claims to run. Asserted but unimplemented: drift detection against `docs/tech-spec.md`, and the pipeline's ability to conclude that the right action is no action — both promised by the detect branch in `b369164` and honoured by no prompt document.

-----

## The Problem

### Two steps derive from a document that is expected to change

Step 6 generates ten baseline skills, listed twice in the prompt that generates them — as a folder tree at `docs/prompts/skills-builder.md:17-45` and as a table at `:64-73`, mirrored a third time in the directive at `grovv-stack-scaffold.md:385-394`. Every one of them is required to "reference the project's `docs/tech-spec.md` for project-specific customization" (`skills-builder.md:117`).

Step 7 reads the same document. `team-design.md:66` is the Phase 1 row: "Identify the domain, dominant task types, and the project stack from `docs/tech-spec.md` / codebase." The team is designed against the spec; the skills assert the spec's stack.

Both outputs are derivatives. Neither has a reconciliation rule. A spec that switches Postgres for SQLite, or drops Stripe, leaves ten skills asserting the old stack and no signal anywhere that they are wrong — and a stale skill is worse than a stale document, because it actively misinstructs every future agent session in that project.

The nearest thing either prompt has to a re-entry rule is `skills-builder.md:186`: "If the project already has skills in `.claude/skills/`, extend or update them rather than overwriting; surface conflicts instead of silently replacing." That sentence sits under `## Existing Projects` (`:179`), which `:181` frames as pre-generation customization — "Customize, don't templatize. Before generating". It governs *foreign* skills encountered on a first run. It says nothing about grovv's own output on a second one, and it will be misread as covering that case until something says otherwise.

### One step has a second run, and it is the one an outsider can see

| Step | Prompt | Re-entry contract |
|------|--------|-------------------|
| 6 | `docs/prompts/skills-builder.md` | None. Nearest analogue is `:186`, scoped to foreign skills on a first run |
| 7 | `docs/prompts/team-design.md` | None. `:65` audits the target's existing files; nothing compares them back to the spec |
| 8 | `docs/prompts/tracker-setup.md` | Defined, in five places: `:60`, `:111`, `:171`, `:379`, `:384` |

The asymmetry is one of visibility, not of risk. Step 8's failure mode is loud — a duplicated issue appears twice in a board column and draws a "didn't we already file this?" comment from someone who did not run the pipeline. Steps 6 and 7's failure mode is silent. A stale generated skill sits in a directory and misinstructs, and nothing renders it.

Two further reasons Step 8 got there first, both worth stating because they explain why copying the pattern is not free. Step 8 cannot start from zero — its target may already hold a backlog it did not create, so reuse-vs-create was a *first-run* problem for that step (`tracker-setup.md:15`, `:57`, `:212`) and the machinery that makes run 2 safe was already required for run 1. And duplicate detection at Step 8 is a query: `gh issue list --repo "$REPO" --state all --limit 200 --json number,state,title` at `:174`, matched on title at `:178`. Steps 6 and 7 have no query. Comparing a generated skill body against a spec that was rewritten in prose is judgment, and `loop-engineering.md:288` rejects making it mechanical: "The drift report stays prose and judgment."

So the contract below has to supply the visibility that no external system will.

### The entry point misclassifies run 2

`loop-engineering.md:91` records the defect: the kickoff skill had exactly two detect branches, and "existing project" was signalled by source code, configs, or a populated `docs/`. A grovv-scaffolded project has a populated `docs/` by construction — Step 2 writes `docs/product-spec.md` and Step 5 writes `docs/prompts/`. The second `/grovv` in a project grovv itself built therefore started at Step 0 and proposed an adoption plan for files it had written: the mode designed for foreign code, applied to its own output.

That precondition is now satisfied — `b369164` added the branch to all four tool trees, tested before the existing-project branch. It matters here for two reasons. Without it none of the contract below ever fires, because the run never reaches a step that would consult it. And with it, the entry point now makes a promise the prompt documents cannot keep: it tells a resuming run to report drift, and no step downstream knows how.

-----

## The Question Run 2 Asks

Stated once, in these words, so both prompts carry the identical sentence rather than two paraphrases that drift apart:

> Given a specification that has moved since these artifacts were generated, which of them are still implied by it?

That is the whole of the re-entry judgment. It is deliberately not "what changed in the spec?" — a diff of the spec is a diff of the wrong document. The subject is the artifact, and the spec is the evidence.

-----

## The Three Verdicts

Three answers, three actions. Identical wording in both prompts.

| Verdict | Meaning | Action |
|---------|---------|--------|
| Unchanged | The artifact's assumptions still match the spec | Leave it alone and say so |
| Drifted | The spec changed under it — a different database, a dropped integration, a renamed component | Propose the specific revision, name the spec line that moved |
| Orphaned | Nothing in the current spec justifies it | Surface it for removal; never delete without approval |

Three properties of this table matter more than the table:

- **Unchanged is not silence.** "Leave it alone *and say so*." A re-entry that reports only what it wants to change has produced an unreadable report — the reader cannot tell an artifact that was judged sound from one that was never opened.
- **Drifted carries a citation.** "Name the spec line that moved" makes the verdict checkable rather than trusted. This mirrors what `tracker-setup.md:384` already requires of a flagged issue: it is surfaced with its reason, not labelled.
- **Orphaned never self-executes.** Removal is a proposal. `tracker-setup.md:384` states the same rule in the same breath — "flag issues that no longer map to the plan — surface them, never delete silently" — and `:382` generalizes it: "Surface conflicts to the user instead of resolving them silently."

Absence gets no verdict, because absence is not an artifact. It is handled by a separate clause, below.

-----

## Drift Detection Against `docs/tech-spec.md`

The entry point now *instructs* it — `b369164` tells a resuming run to re-read the spec and report what has drifted — but no prompt document implements it, so the instruction has no procedure to follow. Closing that gap is the core of the contract.

`team-design.md:65` looks like drift detection and is not: "Read the target's existing `.claude/agents/`, `.claude/skills/`, and `CLAUDE.md`. Decide: new build, extension, or maintenance. Detect drift. Report before acting." That phase audits the target's files *against each other*. The tech spec is not among its inputs — it enters at Phase 1 (`:66`), after the audit has already concluded. Nothing in either prompt ever compares a generated artifact back to the document it was generated from.

**What the check reads.** `docs/tech-spec.md` as it stands now, and each generated artifact's stated assumptions. For a skill, the assumptions are what its body asserts about the stack: the framework, the database, the auth provider, the integrations, the test runner. `skills-builder.md:184` already names exactly these as the customization surface — "if it is Next.js, `frontend-development` covers Next.js, not Astro; if auth is not Clerk, `security-practices` covers the real provider." Those are the assertions that go stale, so those are the assertions that get checked. For a project-specific agent, the assumption is the rationale its own definition states: the spec component it exists to serve.

**What the check produces.** Prose, per artifact, in the shape *artifact — verdict — evidence*. A drifted verdict names the line of `docs/tech-spec.md` that moved. Nothing is machine-readable and nothing is stored; `loop-engineering.md:288` rejects a spec-to-artifact manifest, and this specification does not reopen it.

**What the check does not do.** It does not diff the spec against a previous version of the spec. There is no previous version to diff against — the pipeline stores none, and storing one is the marker-file idea rejected at `loop-engineering.md:285`. Drift is established by reading the artifact and the current spec side by side, which is how a human would establish it.

**Cost, stated plainly.** For ten skills and a handful of agents this is a full read of the tech spec and a full read of each body. That is the most expensive clause in this document, and it is the one that produces the entire value.

-----

## The Dedupe Subject: Naming the Ten Baseline Skills

`team-design.md:143` is a checklist item asserting a review that has no subject:

> - [ ] Duplicate review was run before adding each agent and each skill (Phases 3-0, 4-0)

The agent half has a subject — `team-design.md:31` names the six defaults (`scaffold`, `frontend`, `backend`, `testing`, `database`, `code-review`) and `:35` names Phase 3-0. The skill half does not. Phase 4-0 is named at `skills-builder.md:54` and at `team-design.md:143`, and nothing anywhere in `team-design.md` says what the ten baseline skills are called.

The dependency is asserted only from the far side. `skills-builder.md:210` is the final checklist item — "Baseline skill names are stable so the team-design audit can dedupe against them" — and `:54` repeats the promise in prose: "Keep the baseline names below stable so that audit is reliable." One document promises stability; the other is never told what to compare.

The fix costs one sentence. The `## Re-entry` section in `team-design.md` names all ten by folder name, as written at `skills-builder.md:17-45` and `:64-73`:

| # | Folder | Tree | Table |
|---|--------|------|-------|
| 1 | `dev-standards` | `skills-builder.md:17` | `:64` |
| 2 | `architecture-planning` | `:19` | `:65` |
| 3 | `frontend-development` | `:22` | `:66` |
| 4 | `ui-standards` | `:25` | `:67` |
| 5 | `backend-development` | `:28` | `:68` |
| 6 | `database-design` | `:31` | `:69` |
| 7 | `security-practices` | `:34` | `:70` |
| 8 | `testing-tdd` | `:37` | `:71` |
| 9 | `deployment-ops` | `:40` | `:72` |
| 10 | `debugging` | `:43` | `:73` |

This is a fourth copy of the list, and that is a real cost. It is worth paying because the other three copies all live in documents `team-design.md` does not read, and a review with no subject is a checkbox that always passes.

The same sentence also gives the re-entry a third category it needs. A skill in `.claude/skills/` is baseline, or it was added by this step, or it belongs to the project and grovv never wrote it. Only the first two are grovv's to reconcile. The third is governed by `skills-builder.md:186` and is audited, never rewritten.

-----

## Preserving Hand Edits

A generated file that has been edited by hand is reported and asked about. It is never overwritten and it is never skipped.

This is `tracker-setup.md:382` — "Never overwrite an existing tracker setup" — applied to grovv's own output, and it is the clause most likely to be quietly dropped in implementation, because a step writing into a directory it believes it owns feels safe overwriting. It is not. `tracker-setup.md` is written throughout to interoperate with state it does not own: `:274` extends an existing memory file rather than replacing it, and `:354` merges the `SessionStart` hook — "read the current `hooks` object, append to the `SessionStart` array, and write the merged result. Never overwrite the object wholesale." A generated skill is state grovv wrote and a human then changed, which makes it exactly as unownable.

The cost is recorded honestly at `loop-engineering.md:307`: overwriting destroys work, skipping preserves drift forever, and reporting costs a re-entry run that ends with nothing changed and a list of questions. That is accepted here, not settled — see Open Questions.

Detection is judgment, not a hash. There is no stored checksum and this specification does not add one; a hash file is the marker-file rejection at `loop-engineering.md:285` in another costume. The signals available are the ones a reader has: prose that does not match the generated voice, a section the generator does not produce, project-specific detail no template would contain. When the signal is ambiguous, the artifact is reported as possibly hand-edited and asked about. A false positive costs one turn of conversation; a false negative destroys someone's work.

-----

## The Contract, as Insertable Markdown

Both sections go in the same position in their respective documents — after the last substantive section and before `## grovv Conventions for Generated Output`, so the conventions and the checklist stay last and the footer is untouched.

### For `docs/prompts/skills-builder.md`

**Where it goes.** Insert at line 189 — the blank line after the `-----` at `:188` and before the `## grovv Conventions for Generated Output` heading at `:190`. This places `## Re-entry` immediately after `## Existing Projects` (`:179-186`), the only other section about partial state, so the two adopt-and-resume concerns sit together.

````markdown
## Re-entry

A later run of this prompt does not regenerate the skill set. It reconciles the
skills already in `.claude/skills/` against the current `docs/tech-spec.md`.
These are the standing rules about how, and they hold on every run after the
first — on run 2 and on run 12.

The question a re-entry asks is one question:

> Given a specification that has moved since these artifacts were generated,
> which of them are still implied by it?

Three answers, three actions:

| Verdict | Meaning | Action |
|---------|---------|--------|
| Unchanged | The skill's assumptions still match the spec | Leave it alone and say so |
| Drifted | The spec changed under it — a different database, a dropped integration, a renamed component | Propose the specific revision, name the spec line that moved |
| Orphaned | Nothing in the current spec justifies it | Surface it for removal; never delete without approval |

- **Audit before writing.** List every folder in `.claude/skills/`, and for each
  one the stack its body asserts — framework, database, auth provider,
  integrations, test runner. Separate the skills this pipeline generated from
  skills the project already had; the latter are governed by "Existing Projects"
  above and are audited, never rewritten. Nothing is written until that list
  exists.
- **Diff against the current spec.** Re-read `docs/tech-spec.md` and give every
  generated skill exactly one verdict from the table above. A drifted verdict
  names the line of the spec that moved, so the report can be checked rather
  than trusted. This is the only check that catches a skill teaching the wrong
  stack.
- **Report before acting.** Present the three lists and **wait**. Never delete
  silently. Report the unchanged skills too — a report that names only what will
  change cannot be told from a report that skipped half the directory.
- **Update, never append blindly.** A skill whose folder name already exists is
  revised in place. Never create a suffixed sibling — no `testing-tdd-v2`, no
  `testing-tdd-new`. The baseline names are fixed so the team-design audit can
  dedupe against them, and a duplicate folder breaks exactly that.
- **Absence is a question, not a fact.** A baseline folder that is missing is
  either explained by the current spec — a project with no database needs no
  `database-design` — or it is unexplained. Explained, say so and move on.
  Unexplained, ask before regenerating. A re-entry never silently resurrects a
  skill a previous run consciously dropped, and never silently removes one.
- **Preserve hand edits.** A generated skill that has been edited by hand is
  reported as hand-edited and asked about. It is never overwritten and never
  skipped. Name what drifted and what the edit appears to protect, and let the
  user decide. When the signal is ambiguous, report it as possibly hand-edited;
  a false alarm costs a turn, a missed one costs someone's work.
- **A previous run is not an answer to an ask-first rule.** The frontend
  framework (Astro + React or Next.js) and the Playwright E2E scope are
  inherited from the user, never from an earlier run's output. A re-entry
  decides neither and re-litigates neither: it does not treat a generated
  artifact as evidence that a choice was made, and it does not re-ask a
  question the user has already answered. Where the record is genuinely
  absent, it asks.
- **A re-entry does not advance the pipeline on its own.** Reconciling this step
  is a complete outcome. Continue to `team-design.md` (Step 7) only if the user
  asks for it.

A re-entry that changes nothing and returns a list of questions has succeeded.
No action is a valid result of this step.
````

**Checklist items**, appended after `:210`:

````markdown
- [ ] On a re-entry, every generated skill carried a verdict — unchanged, drifted, or orphaned — and the report was presented before anything was written
- [ ] No hand-edited skill was overwritten, and no baseline skill was silently resurrected or silently removed
- [ ] No skill folder was duplicated with a suffix
````

### For `docs/prompts/team-design.md`

**Where it goes.** Insert at line 120 — the blank line after the `-----` at `:119` and before the `## grovv Conventions for Generated Output` heading at `:121`. Same position as in `skills-builder.md`, which keeps the two documents legible side by side, and leaves `## Deliverable Checklist` (`:137`) and `## After This Step` (`:158`) as the closing sections.

The section is written as the grovv-facing extension of harness Phase 0, not as a competing procedure. `team-design.md:74` forbids duplicating vendored detail here and `:133` states that behaviour is extended in this prompt, never in the vendored files. Phase 0 (`:65`) supplies the audit; this section supplies the grovv rules its result is judged by.

````markdown
## Re-entry

Phase 0 above already audits the target's `.claude/agents/` and
`.claude/skills/`. This section states what a later run does with what that
audit finds. It adds no procedure to the vendored skill — it is the grovv side
of Phase 0, and it holds on every run after the first, on run 2 and on run 12.

The question a re-entry asks is one question:

> Given a specification that has moved since these artifacts were generated,
> which of them are still implied by it?

Three answers, three actions:

| Verdict | Meaning | Action |
|---------|---------|--------|
| Unchanged | The agent's rationale still maps to the spec | Leave it alone and say so |
| Drifted | The spec changed under it — a different database, a dropped integration, a renamed component | Propose the specific revision, name the spec line that moved |
| Orphaned | Nothing in the current spec justifies it | Surface it for removal; never delete without approval |

- **Audit before writing.** List every project-specific agent in
  `.claude/agents/` with the rationale its definition states, and every skill
  this step added to `.claude/skills/`. Nothing is written until that list
  exists.
- **Name the baseline before deduping.** The duplicate review (Phases 3-0 and
  4-0) has two subjects. On the agent side it is the six grovv defaults named
  above. On the skill side it is the ten baseline skills that `skills-builder.md`
  (Step 6) writes: `dev-standards`, `architecture-planning`,
  `frontend-development`, `ui-standards`, `backend-development`,
  `database-design`, `security-practices`, `testing-tdd`, `deployment-ops`, and
  `debugging`. Anything in `.claude/skills/` outside those ten and outside this
  step's own additions belongs to the project — audit it, never rewrite it.
- **Diff against the current spec.** Re-read `docs/tech-spec.md` and give every
  project-specific agent and every skill this step added exactly one verdict from
  the table above. A drifted verdict names the line of the spec that moved.
- **Re-justify rather than inherit.** The additive rule protects the six
  defaults, not the specialists. On a later run each project-specific agent is
  re-argued against the current spec; an agent that exists only because an
  earlier run added it is orphaned. "The smallest team that covers the domain" is
  a ceiling, and a re-entry must be able to lower it as readily as raise it.
- **The six defaults are exempt.** `scaffold`, `frontend`, `backend`, `testing`,
  `database`, and `code-review` are never orphaned and never removed by a
  re-entry. They are the baseline team, not a derivative of the spec.
- **Report before acting.** Present the three lists and **wait**. Never delete
  silently, and report the unchanged specialists too.
- **Update, never append blindly.** An agent or skill whose name already exists
  is revised in place, never duplicated with a suffix.
- **One pointer, one change log.** The target `CLAUDE.md` carries a single
  harness pointer. A re-entry adds a dated row to the existing change log and
  leaves the trigger rule alone; it never writes a second pointer.
- **Preserve hand edits.** A generated agent or skill that has been edited by
  hand is reported as hand-edited and asked about. It is never overwritten and
  never skipped.
- **A previous run is not an answer to an ask-first rule.** The frontend
  framework (Astro + React or Next.js) and the Playwright E2E scope are
  inherited from the user, never from an earlier run's output. A re-entry
  decides neither and re-litigates neither: it does not treat a generated
  artifact as evidence that a choice was made, and it does not re-ask a
  question the user has already answered. Where the record is genuinely
  absent, it asks.
- **A re-entry does not advance the pipeline on its own.** Reconciling this step
  is a complete outcome. Continue to `tracker-setup.md` (Step 8) only if the user
  asks for it.

A re-entry that changes nothing and returns a list of questions has succeeded.
No action is a valid result of this step.
````

**Checklist items**, appended after `:154`:

````markdown
- [ ] On a re-entry, every project-specific agent and every skill this step added carried a verdict, and the report was presented before anything was written
- [ ] The duplicate review named the ten baseline skills explicitly; the six default agents were exempt from removal
- [ ] No hand-edited generated file was overwritten, and the `CLAUDE.md` harness pointer was updated rather than duplicated
````

-----

## No Action Is a Result

The pipeline has expressed this exactly once, at the entry point, in `b369164`: "a run that changes nothing and returns a list of questions is a successful run." No step document repeats it, and it is the clause most likely to be lost in implementation.

Every step from Step 1 to Step 9 terminates in an artifact, and Step 0 terminates in an adoption plan put to the user for approval (`grovv-stack-scaffold.md:176`). The Success Criteria at `grovv-stack-scaffold.md:617-631` are fifteen checkboxes and every one of them is an existence claim — a file exists, a directory is populated, a document reflects something. There is no shape in the directive for a step that ran correctly and produced nothing.

A re-entry needs that shape. The most common correct outcome of a second run against an unchanged spec is: ten skills unchanged, three specialists unchanged, two files possibly hand-edited, one question. Nothing written. If that reads as a failure, implementations will start writing something to prove the step ran, which is precisely the failure this contract exists to prevent.

Both `## Re-entry` sections therefore end with the same two sentences, and they are not decoration:

> A re-entry that changes nothing and returns a list of questions has succeeded. No action is a valid result of this step.

`tracker-setup.md` reaches the same conclusion from a different direction at `:65`, where a failed preflight writes an `@TODO` and continues rather than failing the run — "Never leave a half-created taxonomy or a partial backlog behind." A recorded gap is a result. So is a recorded absence of drift.

The existing checklists will not detect the difference on their own. `skills-builder.md:202-210` are existence checks with one exception: `:206` — "Skills reflect the project's actual stack (existing projects) and reference `docs/tech-spec.md`" — is a content-accuracy check, and a second run against a changed spec does not pass it trivially. It is the closest thing the repository has to a drift check today. What it lacks is a procedure: it states the property without saying how a second run establishes it, which is what turns a true checklist item into one nobody can fail. That is not a contradiction with this contract, but it is a trap: the checklist reads as satisfied while the reconciliation was never done. The three added checklist items exist to close it.

-----

## Artifacts

| Path | New or edit | Purpose | Line delta |
|------|-------------|---------|------------|
| `docs/prompts/skills-builder.md` | Edit | `## Re-entry` inserted at line 189; three checklist items after `:210` | +64 on 213 |
| `docs/prompts/team-design.md` | Edit | `## Re-entry` inserted at line 120, framed as the grovv side of Phase 0; the ten baseline skills named; three checklist items after `:154` | +68 on 163 |
| `grovv-stack-scaffold.md` | Edit | One sentence in Step 6 (`:425-435`) and one in Step 7 (`:437-450`) pointing at each prompt's re-entry contract; one Success Criteria item covering a resume run | +5 on 634 |
| `.grovv/agents/scaffold.md` and three derived copies | Edit | One line under `## Scaffolding Order` (`:23`): a resume goes to the re-entry contract, not Step 0 | +2 each, +8 total |
| The kickoff skill in four tool trees | **Landed** (`b369164`) | The third detect branch. Precondition for all of the above; already applied, not specified in this document | 0 — done |
| `MEMORY.md` | Edit | A dated Decision Log entry referencing the tracker issue by identifier | +4 on 90 |
| `docs/architecture/re-entry.md` | New | This document | ~400 |

About 149 lines of edits across five paths — eight actual files, once `.grovv/agents/scaffold.md`'s three synced copies are counted. No new prompt document, no new numbered step, no new file in any target project, and nothing generated into a target. The whole change is text that constrains a run that already happens.

Two notes on the arithmetic. `loop-engineering.md:255` scoped Layer 2 at "~70 lines across 11 files"; the two `## Re-entry` sections alone are 122, and 128 with the checklist items each section needs to be enforced, because that estimate counted the clauses and not the table, the question, or the ten named skills. And the fan-out deserves its own line: `.grovv/agents/scaffold.md` exists in four trees held to parity by `check_tool_sync.py`, so a two-line edit there is an eight-line change. Every estimate in this repository written before 2026-07-25 understates that.

**Applying both insertion points.** Every line number in this document is measured against the files as they stand today, before any edit. Apply one `## Re-entry` section and the other document's numbers are unaffected, but the *same* document's later references — the checklist items appended after `skills-builder.md:210` and `team-design.md:154` — shift by roughly sixty lines. Locate those by heading rather than by number, or append the checklist items first and insert the section second.

Both insertable blocks end where a `-----` rule is required by the document convention, since each is specified as going immediately before a `## grovv Conventions for Generated Output` heading. Add that rule when inserting; it is omitted from the blocks below so they can be lifted verbatim without a trailing separator that would be wrong in another position.

-----

## Phased Rollout

| Phase | Delivers | Standalone? |
|-------|----------|-------------|
| 1 | The ten baseline skill names, inserted into `team-design.md`'s Phase 4-0 audit as a standalone sentence — **not** as part of any `## Re-entry` section | Yes, genuinely. See the wording and insertion point below; it depends on nothing else in this document |
| 2 | The `## Re-entry` section in `docs/prompts/skills-builder.md`, plus its checklist items | Yes. The third detect branch has landed (`b369164`), so a resuming run now reaches Step 6 as a resume |
| 3 | The `## Re-entry` section in `docs/prompts/team-design.md`, plus its checklist items | Yes. Phase 1 already supplies the dedupe subject; Phase 3 restates it in context rather than depending on it |
| 4 | The directive and `scaffold.md` pointers | Needs Phases 2 and 3 to point at |

Phase 1 is the smallest correct change in this document and the only one that fixes a defect rather than filling a gap: `team-design.md:143` currently claims a review that half-runs against nothing.

**Phase 1, in full, so it can be applied without reading the rest of this document.** Append to `team-design.md`'s Phase 4-0 paragraph:

> The skill-side subject of this duplicate review is the ten baseline skills `skills-builder.md` (Step 6) writes: `dev-standards`, `architecture-planning`, `frontend-development`, `ui-standards`, `backend-development`, `database-design`, `security-practices`, `testing-tdd`, `deployment-ops`, and `debugging`. A skill matching one of those names is never re-created under a variant name. Anything outside those ten and outside this step's own additions belongs to the project — audit it, never rewrite it.

Three sentences, no behaviour change beyond giving an already-claimed review its missing subject, and no dependency on any other phase. `skills-builder.md:198` already promises that these names are stable "so the team-design audit can dedupe against them" — one side has been keeping a promise the other side was never told about.

Nothing here is verifiable by CI. The seven check scripts validate this repository's conventions; a re-entry contract can only be exercised by running the pipeline twice against a throwaway project with the spec edited in between, which is the smoke-test rubric `loop-engineering.md:226` proposes and the case nothing has ever exercised.

-----

## What We Are Deliberately Not Doing

| Rejected | Reason |
|----------|--------|
| A numbered step for re-entry | A re-entry step would run at the end of run 1, where there is nothing to re-enter (`loop-engineering.md:279`). Insertion also costs a renumber across every numbered reference in the repository |
| A `.grovv-version` or similar marker file in target projects | Hidden state that must be maintained and will drift. The artifacts are the marker (`loop-engineering.md:285`), and the detect branch already uses them |
| A stored checksum or manifest to detect hand edits mechanically | Same objection in another costume, plus it makes every legitimate edit look like tampering. Detection stays judgment, with the ambiguous case reported rather than guessed |
| A machine-readable spec-to-artifact map to make drift diffable | Rejected at `loop-engineering.md:288` for a corpus that fits in one context window and needs a dependency this repo forbids. The drift report stays prose and judgment |
| A `## Re-entry` section in all six prompt documents | Steps 2-5 and 9 rewrite whole documents and already behave correctly on a second pass; only Steps 6 and 7 append into a directory (`loop-engineering.md:292`). Sections that say "nothing special happens here" are how prompts get long enough to stop being read |
| Specifying the third detect branch here | It lands separately, in four tool trees. This document specifies what happens after a run is identified as a resume, and would go stale the moment that change edits a line it cited |
| Letting a re-entry delete an orphaned artifact after reporting it | "Report, then delete unless told otherwise" is deleting silently with extra steps. `tracker-setup.md:384` surfaces and stops; so does this |
| Letting a re-entry remove any of the six default agents | `team-design.md:33` — "Do not delete or replace them" — and checklist item `:142`. The defaults are not derived from the spec, so no spec change can orphan them |
| Skipping the questions a first run asked, on the grounds that a prior run answered them | A prior run is an artifact, not a decision, exactly as a prototype is not a decision. `team-design.md:52` carries the two ask-first rules forward from the *user*; a generated file is never the source |
| Re-litigating the two ask-first rules on every re-entry | The opposite error. `team-design.md:52` says carry forward, do not re-litigate. The framework and Playwright decisions are inherited from the user and are neither decided nor re-decided by this step |
| Regenerating the baseline skill set from scratch on a second run | Fastest to implement and it destroys every project-specific customization `skills-builder.md:181-185` asked for. It also contradicts `:186` for any project that had skills before grovv arrived |
| A re-entry that auto-advances through the remaining steps | Reconciling one step is a complete outcome. Auto-advancing turns a reconciliation into a full re-run and makes the cheap case expensive |
| A new file in the target recording which baseline skills were dropped | `skills-builder.md:60` sanctions dropping a skill and `:202` calls it "consciously dropped", but the record it needs already exists: the spec. An absence the spec explains needs no note, and one it does not explain is a question. A fourth root-level artifact for one fact is not worth it |
| Extending the check scripts to validate re-entry behaviour | There are no generated skills in this repository to check, and reaching into a target project's tree from this repository's CI inverts the dependency the whole design rests on |

-----

## Open Questions

- What happens on re-entry when a generated skill was edited by hand? Overwriting destroys work; skipping preserves drift forever. Currently: report and ask, per `loop-engineering.md:307` — at the cost of a run that can end with nothing changed and a list of questions. Recorded there as an accepted cost, not a settled certainty.
- Is a drift report worth anything when "what the spec implies" is nowhere written in comparable form? A human reading two documents is the entire mechanism, and the alternative is the manifest rejected above. Currently: prose report, accepting that its quality is the reading agent's quality.
- Does a re-entry re-read the whole tech spec, or only the sections a skill claims to depend on? Whole spec, currently — skills do not record which sections they derived from, and adding that record is the manifest again in miniature. This is the largest cost in the contract and the first place to look if re-entry proves too expensive to run.
- Should the ten baseline names live in `team-design.md` as a literal list, making a fourth copy, or should `team-design.md` point at `skills-builder.md:64-73`? Currently: literal list, because a pointer is a read the audit will skip and a stale pointer fails silently. If a fifth copy is ever proposed, that is the signal to make the list canonical in one place and check it in CI.
- Does the absence rule interact badly with a project that legitimately dropped a skill and later grew into needing it? Currently: the spec decides, and a spec that now implies a database gets `database-design` proposed, not silently written. Untested.
- What does a re-entry do when `docs/tech-spec.md` is itself stale — unchanged since run 1 while the code moved? Nothing, currently. The contract measures artifacts against the spec, not against the code, and a spec nobody updated reports everything unchanged. This is the contract's blind spot and it should be stated in the prompts rather than discovered.
- **Which wins when a skill and the tech spec disagree about an ask-first answer?** `docs/tech-spec.md` is itself generated, at Step 4. The drift clause tells run 2 to reconcile a skill's asserted framework against the spec, while the rejections table says a generated file is never the source of an ask-first answer. Both cannot hold: taken literally, the spec is disqualified from settling the very assertion the drift check exists to settle. The gating keeps this from becoming a violation — nothing is written before the user sees the report — but an implementer meeting "skill says Astro, tech-spec says Next.js" has no rule to apply. Currently: **report the disagreement as Drifted, name both files, and let the user say which is right.** The re-entry never picks a winner, because picking one is answering the ask-first question with a generated artifact whichever way it picks. This is the sharpest unresolved question in the document and the first thing to settle before implementation.
- @TODO — confirm the tracker identifier for this work before it is cited in a commit message. `loop-engineering.md:314` records that its own brief named an identifier that exists nowhere in the repository.

-----

## Colophon

| Field | Value |
|-------|-------|
| **Version** | 0.1.0 |
| **Last Updated** | 2026-07-27 |
| **Status** | Proposed — not implemented |
| **Author(s)** | grovv stack scaffolding agent |
| **Model** | Claude (Claude Code) |

-----
gro\\/\\/ stack — The Re-entry Contract
