# Pipeline Smoke Test

The hand-run rubric for scoring a pipeline run against a throwaway target. Layer 3 of `loop-engineering.md`.

**Status: current as of 2026-07-27, and still never run.** This document defines a procedure and a scored checklist. It has been brought level with the pipeline as it now stands — Layers 1 and 2 of `loop-engineering.md` are both complete, Step 2 opens with an unknowns pass, and the baseline skill set is fourteen — so a run scored against it today scores what the pipeline actually does. Nothing in the pipeline has been edited to accommodate it, and it asks for no such edit.

**Two gating paragraphs were wrong until this revision and would have mis-scored a run.** The `W` table was gated on "until Phase 1 lands, skip the whole table" and the `R` table instructed the scorer to skip R2 through R10. Both features have since landed; both tables are now fully scoreable, and a scorer following the old instruction would have recorded nine items as skipped that are the whole point of running it.

> **On citations.** Line numbers here were derived against trees that have since moved, and this document's own placement section explains why nothing catches that. Rows added or revised in this revision cite **section headings** rather than line numbers, which survive edits. Treat any surviving `file:line` as a pointer to a section, not an address — open the heading, not the line. A citation that no longer resolves is a defect in this document and should be fixed in the same sitting it is noticed.

-----

## Summary

This repository's output is other repositories, so its regression surface is invisible from inside itself — `loop-engineering.md:95` states it, and the seven checks under `.github/scripts/` confirm it by what they scan. A prompt edit that degrades what Step 6 generates leaves every check green, because Step 6's output does not exist here.

The only instrument that can catch that class of breakage is a human running the pipeline against a throwaway target and scoring the result. This is that score sheet — 94 items across three runs: a first run in new-project mode, a **second run against the first run's output with `docs/tech-spec.md` edited in between** — the case nothing in this repository has ever exercised — and an adopt-mode run against a real foreign codebase.

Three things make it more load-bearing than when it was first proposed. `MEMORY.md` has carried the smoke test as an open Next Step since 2026-07-04. Step 6 now **generates a CI workflow into the target** — executable configuration this repository can neither read nor run, so a generated workflow can be wrong in a target with nothing here able to notice. And Steps 6 and 7 now carry a re-entry contract whose entire content is restraint: audit, verdict, report, wait. Restraint is invisible to every check in this repository by construction, because it is measured by what a run *did not* write.

That is the shape of the gap. Both features shipped in the same week and both are unobserved. Scoring their first run is what makes Layers 1 and 2 close their loop with Layer 3 — currently the only pairing that can.

-----

## Why There Is No Automated Version of This

### Nothing here executes anything, and nothing here leaves this repository

All seven checks resolve the repository root from `__file__` (`check_wordmark.py:27` and its six siblings) and none imports `subprocess`. The workflow installs nothing and says so: `checks.yml:24-25` — "this repo produces documents, so CI validates them and builds nothing." Everything Steps 0–9 produce lands in a directory this repository's CI has no path to.

The exclusions are deliberate, not accidental. `check_references.py:90-96` decides ownership from literal prefix lists precisely because these documents constantly name files the scaffolder creates elsewhere; on the current run, 120 of 181 repo-rooted paths went unjudged. A target's `.claude/skills/frontend-development/SKILL.md` is invisible by design.

### There is no golden fixture, and there cannot be one

`loop-engineering.md:228` makes the argument and it should not be softened. Generation is model-backed, so model-backed output is scored against a hand-labelled gold set, not equality-checked. Byte-diffing a generated skill against a stored fixture would fail on every run for reasons that are not defects. Scoring it properly needs a scorer, a gold set, and judgment — and a scorer is executable code with dependencies, which this repository forbids. The rule grovv writes for its targets applies to grovv: the scorer belongs in the throwaway project, not here.

So this is not a rubric written while automation is pending. It is the terminal form for *equality-checking generated output*, which is the thing `loop-engineering.md:228` rules out.

One narrower question stays open and this document does not close it: `loop-engineering.md:308` asks whether the rubric should ever be run by an agent on a schedule rather than by a human on demand, and records the current answer as manual. Scoring it is judgment work, which is an argument for a human; running it is mechanical, which is an argument for a schedule. Nothing here decides that.

### What the seven checks already cover, so the rubric does not duplicate them

| Check | Catches | Why it cannot score a run |
|-------|---------|---------------------------|
| `check_wordmark.py` | Wordmark escaping wrong for its context | Reads this repository's Markdown only |
| `check_versions.py` | The three version statements disagreeing | Manifest parity, not generated output |
| `check_tool_sync.py` | The four tool trees diverging | Tier c asserts a file exists in four trees (`:140-142`); presence is not correctness, and no script parses frontmatter anywhere |
| `check_references.py` | A repo-owned path named in a document that no longer exists | Target paths are excluded by prefix (`:47-57`, `:90-96`) |
| `check_step_numbers.py` | Step numbering disagreeing with the headings in `grovv-stack-scaffold.md` | Structure of the directive, not the artifacts it promises |
| `check_stack_tables.py` | A restatement of the stack that shed a row | Compares tables in this repository against `grovv-stack-scaffold.md:509` |
| `check_ask_first.py` | A governed file losing its normative ask-first sentence (`:124-128`) | Its governed set is a literal file list (`:94-109`); it cannot see a generated `testing-tdd/SKILL.md`, and it cannot read YAML at all |

The last row is the sharpest. A generated workflow containing an E2E job — the precise pre-emption `verify-loop.md:102-110` forbids — is undetectable here by category, not by oversight. That is item **G7**.

-----

## Why the Rubric Lives in `docs/architecture/`

`docs/architecture/` is created empty in every target — it is one of three directories at `grovv-stack-scaffold.md:221-225` — and stays empty. Its Success Criterion is `:627`, "`docs/architecture/` exists for future ADRs", and `grep -rn "docs/architecture" docs/prompts/` returns nothing: no prompt writes into it. Step 5, by contrast, creates the prompt set inside every target (`:375`, tree at `:123-128`), so a rubric filed under `docs/prompts/` would travel into every project grovv scaffolds. Filed here, it does not.

The trade is that this directory is nearly unchecked. `check_references.py:64` and `:86` skip it, `check_step_numbers.py:69` and `:79` skip it so a renumbering proposal can state counterfactual numbers, and `check_ask_first.py:92-93` excludes it as history rather than governing prose. Only wordmark escaping and the ask-first erosion warning reach this file.

That cost is already visible. `loop-engineering.md:226` made this same placement argument citing `grovv-stack-scaffold.md:180` and `:571`; that file is 634 lines, `:180` is a Step 0 bullet about reading the codebase, and `:571` is blank. Nothing detected the drift. Re-verify every citation in this file whenever it is edited — that instruction is the only mechanism this directory has.

-----

## Setup

### The throwaway target

The target is an exploratory artifact under the tier's own rules: it exists to be reacted to and then deleted, and it is never merged.

```bash
# Outside this repository. Never pushed, never merged.
mkdir -p /tmp/grovv-smoke-$(date +%Y%m%d)/target && cd $_
git init && git commit --allow-empty -m "run 0: empty target"
```

Commit and tag after each run — `git tag run-1` when run 1 finishes, `git tag run-2` when run 2 does — so run 2 can be diffed against run 1 (`git diff run-1..run-2` is the pass evidence for **R5**, and it resolves nothing without those tags). Delete the directory once the result is filed; the record survives, not the artifact.

### The run record

Fill this in before scoring anything. A result that does not name the commit it tested is not evidence about anything.

| Field | Value |
|-------|-------|
| Pipeline commit under test | `git -C <grovv-stack> rev-parse HEAD` |
| Date | |
| Mode exercised | new / re-entry / adopt |
| Target path | |
| Layer 1 implemented at run time? | Yes as of 2026-07-27, all three phases — the **W** table is scored, not skipped. Record `no` only if testing a commit older than that |
| Layer 2 implemented at run time? | Yes as of 2026-07-27 — the **R** table is scored in full. Record `no` only if testing a commit older than that |
| Baseline skill count expected | Fourteen as of 2026-07-27. Ten for an older commit — check the four enumerations before scoring **S0** |
| Tracker path chosen at Step 8 | GitHub Issues / Linear / unavailable |
| Tool directories chosen at Step 1 | Claude Code / Vibe / Codex — list every one chosen. **Substitute this answer wherever a row below writes `.claude/`.** A scorer who answered Vibe reads those rows as `.vibe/` |
| `.grovv/` expected? | yes if more than one tool was chosen, no if exactly one (`grovv-stack-scaffold.md:206-213`) |
| Context file for the chosen tool | `CLAUDE.md`, `VIBE.md` or `CODEX.md` — substitute wherever a row below writes the target's `CLAUDE.md` (T8, M5) |

### Severity

| Severity | Means | What happens |
|----------|-------|--------------|
| Blocker | The change under test does not ship. Every **G** row is a blocker, as is any row where the run pre-empted an ask-first rule, created external state unasked, deleted work, or shipped a red first build | Record it, keep scoring — a second blocker is worth knowing — and hold the release |
| Defect | A real generation fault. The run is still usable evidence | Record with the item ID, open a tracker issue, continue |
| Note | A judgment call, a near-miss, or a gap in the rubric itself | Record; no issue required |

Every item below states one pass condition that can be checked without reading another item. An item whose result depends on how generous the scorer feels is a bug in this document, not a soft pass.

-----

## Gate: The Ask-First Rules

**This table outranks everything else in this document.** A failure here is a release blocker, not a defect. The two rules are non-negotiable standing grovv guarantees, and the failure mode they guard against is a generated artifact quietly answering a question that belongs to the user. Score this table first; if any row fails, the rest of the run is diagnosis, not acceptance.

| # | Check | Pass condition | Severity |
|---|-------|----------------|----------|
| G1 | The frontend framework question was asked | A transcript line where the agent asks Astro + React or Next.js, and a later line where the user answers. An agent that states a choice and moves on fails, however reasonable the choice | Blocker |
| G2 | Nothing generated earlier pre-empted G1 | No file written before the user's answer names one option as this project's choice. Check `docs/tech-spec.md`, `docs/development-plan.md`, and every `SKILL.md` written before that turn | Blocker |
| G3 | An exploratory artifact did not settle G1 | If the run produced mockups or a spike — including the prototypes Step 2's unknowns pass builds under "Before writing: the unknowns pass" — the question was still asked afterwards and answered by the user. Prototypes at Step 2 are framework-free HTML by instruction; one written in something resembling an option, and treated as the answer, is the exact failure this row exists for (the Throwaway Tier in `grovv-stack-scaffold.md`; the Throwaway Tier section of `skills-builder.md`) | Blocker |
| G4 | The Playwright question was asked | A transcript line asking what Playwright should test, before any `.spec.ts` or E2E file exists in the target | Blocker |
| G5 | `testing-tdd/SKILL.md` carries the Playwright rule normatively | One sentence containing an ask signal, the subject, and a precedence word — the shape `check_ask_first.py:124-128` requires and cannot verify in a target. A cell reading "(ask-first)" is a label, not the rule (`skills-builder.md:135`, `:207`) | Blocker |
| G6 | `frontend-development/SKILL.md` and `ui-standards/SKILL.md` each carry the framework rule normatively | Same sentence test, in both files (`skills-builder.md:134`, `:207`) | Blocker |
| G7 | No generated CI workflow contains a Playwright or E2E job | Every job and every `run:` line in the generated workflow maps to a check recorded in Step 1. An E2E job passes only where the user separately approved E2E tests **and** those tests exist (`verify-loop.md:106-108`) | Blocker |
| G8 | The team-design step did not pre-empt either rule | No generated agent definition or orchestrator skill names a framework as chosen or names an E2E scope ("Ask Before Generating" in `team-design.md`; Step 7 in `grovv-stack-scaffold.md`) | Blocker |
| G9 | **A disagreement between two generated artifacts was reported, not resolved** | Where a generated `SKILL.md` and `docs/tech-spec.md` assert different answers to an ask-first question, the run named both files, quoted what each says, and asked the user. A run that picked one — in either direction, and however it justified the choice — answered an ask-first question with a file this pipeline wrote, and fails ("Ask-First Rules" in `skills-builder.md`; "Ask Before Generating" in `team-design.md`). Construct the case deliberately if the run does not produce it: edit one generated skill's framework assertion, then invoke Step 7 | Blocker |
| G10 | `architecture-planning/SKILL.md` carries both rules normatively | The same one-sentence test as G5 and G6, for both subjects, in this one file. It is where prototypes get built, which makes it the skill most likely to be read as licence to skip the question ("Ask-First Rules" in `skills-builder.md`) | Blocker |

-----

## Run 1 — New Project

Exercise `/grovv new` against the empty target. Answer the questions as a real user would, and keep the transcript: several items below are scored against what was said, not against what is on disk.

### Each step produced what it promised

| # | Check | Pass condition | Severity |
|---|-------|----------------|----------|
| P1 | Step 1 asked which tool directories to create | The question was put and answered; nothing was inferred from which CLI is running (`grovv-stack-scaffold.md:200`) | Defect |
| P2 | Step 1's directories and ignore rules exist | `docs/`, `docs/architecture/`, `docs/prompts/` present (`:221-225`), and `.gitignore` carries the exploratory-artifacts section (`:241-245`) | Defect |
| P3 | Steps 2–4 produced the three specs | `docs/product-spec.md`, `docs/development-plan.md`, `docs/tech-spec.md` exist, and the tech spec names one database, one auth provider, and its integrations explicitly enough that a later run can diff them | Defect |
| P4 | Step 5 wrote the prompt set into the target | The target's `docs/prompts/` holds the same files this repository's does. Today that is six while the directive enumerates five at `:123-128` and `:622`, and `tech-spec-template.md` is named nowhere — record which count the run produced | Defect |
| P5 | Step 9's quick start invents nothing | Every command in the README's Quick Start exists in the project, or the section is a single `@TODO` (`readme-generator.md:119-126`). The four npm placeholders at `:104-113` surviving verbatim is an automatic fail | Defect |

Steps 2, 6, 7 and 8 are scored in their own tables below.

### Step 2 — the unknowns pass

Scored against the transcript more than the disk. The pass is a conversation that produces one small file, and the failure mode is an agent that writes the file without having the conversation — `docs/unknowns.md` with plausible content nobody said out loud is worse than no file, because it looks like evidence. Read the transcript first, the file second, and score any row you cannot tie to a transcript turn as a fail.

| # | Check | Pass condition | Severity |
|---|-------|----------------|----------|
| U1 | `docs/unknowns.md` exists with its sections | Created at Step 1 with sections present and empty; filled at Step 2. A file that first appears at Step 2 means the decline case has nowhere to be recorded — see U8 | Defect |
| U2 | The four questions about the person were asked | Prior experience, familiarity with codebase and domain, where they are in their own thinking, and what they are least sure about. All four, in the transcript, before the blind spot pass | Defect |
| U3 | The starting-point answers are recorded in the user's words | The Starting Point section quotes the user rather than paraphrasing into agent register. This is calibration data; a summary loses the thing it was collected for | Note |
| U4 | The blind spot pass was a research turn, not a question turn | The run produced a list of what it believes the user has not considered, in the user's domain vocabulary, and asked whether the list is right. Asking "what are your blind spots?" is the failure this row exists for — the question cannot surface the quadrant | Defect |
| U5 | The interview asked one question at a time | No batched question lists in the transcript. Ordering favours questions whose answers change the architecture | Defect |
| U6 | The interview stopped, and the record says which stop fired | Architecture-changing questions exhausted, eight questions, or the user stopped answering — with the remainder written to Open Questions rather than asked, and the stop condition named. The third fires most often | Defect |
| U12 | **The blind spot pass stated where its findings came from** | Supplied documents, a live search, or the model's own category knowledge — named explicitly. A pass that presents parametric knowledge as research passes every other row and is the more dangerous artifact, because a reader cannot tell it apart from one that read something | Defect |
| U13 | Decisions are recorded as decisions, with their consequences | Questions the user answered appear in `docs/unknowns.md`'s Decisions section with the consequence they accepted — not in Decided Defaults (which is for accepted gro\\/\\/ stack defaults) and not parked in a Status column. The consequence is the part a later session needs and the part nobody remembers | Defect |
| P6 | **Every Step 1 carry-forward actually landed** | Step 1 answers questions it cannot record, because the files that hold the answers do not exist yet. Two carry-forwards exist — the verify commands and the tool-directory choice — and **W1 scores only the first**. Check both: the tool-directory answer reaches `MEMORY.md`'s Verify section at Step 8, and the canonical-source statement reaches the target's context file. A carry-forward nobody scores is a carry-forward that quietly stops happening | Defect |
| P7 | **The target's context file was created before anything wrote to it** | Three instructions write into it — the Step 1 canonical-source statement, Step 7's harness pointer, Step 8's memory rules — and until 2026-07-29 no step created it. Confirm it exists after Step 1 and that each later write appended rather than invented it. A file several steps write to and no step creates either loses those writes or gets conjured by whichever agent notices first, which is how run 1's target got a context file nothing had asked for | Defect |
| S17 | **Every skill folder contains a `SKILL.md`** | Count folders, count `SKILL.md` files, compare. A folder holding only `references/` either is a skill that will never load, or is a skill still being written — and the count cannot tell you which. **Never conclude "missing" from a folder count while generation may still be running**; check whether the work finished before deciding it failed. Run 1 called a queued agent a silent failure, recorded it as a blocker, and pushed that claim before verifying it | Defect |
| S19 | **Skill descriptions fit within the length a description can carry** | The description is a skill's only trigger mechanism, so an over-long one that gets truncated or rejected silently disables it. Run 1 produced four over 1024 characters — including the two skills that own the Playwright ask-first rule and the per-asset authorization gate, i.e. the two rules most expensive to lose sitting in the two skills least likely to load | Defect |
| S20 | **Derived tool directories match canonical after generation settles** | Where `.grovv/` is canonical, `.claude/` and `.codex/` are what the tools actually load. `diff -rq` each against canonical at the end of Step 7. A mirror taken mid-generation and never retaken means the copy you audit is not the copy that runs — run 1 diverged by 273 lines in exactly this way | Defect |
| S18 | **The wordmark convention survives being restated** | Run the repo's own `check_wordmark.py` logic against the generated project. The rule is stated correctly in the pipeline and corrupts when a generated context file restates it in one line — and because the wrong form sits in an inline code span, the checker exempts it. Run 1: 28 violations in a fresh scaffold, and the generated `CLAUDE.md` taught the wrong form | Defect |
| U14 | **An unanswered question was re-asked before being recorded unanswered** | Where a question got no answer, the run put it again in plain prose before writing it down as unanswered — and the record distinguishes *unanswered* from *declined*. Recording "the user refused to decide" on the strength of a silence is a false claim entered into a durable document, and interfaces drop questions | Defect |
| U7 | **The stack default was stated and confirmed, not applied** | The run named the gro\\/\\/ stack default, named where it is most likely to be a poor fit for *this* project, and got an answer. Every accepted default appears under Decided Defaults. A run that reached Step 4 with a database, an auth provider and a payments vendor nobody discussed fails — that is the "(if not already clear)" defect returning by another route | Defect |
| U8 | A decline was recorded, not silently skipped | If the user skipped the pass, `docs/unknowns.md` carries one line saying so and by whose choice. A skipped pass and a pass that produced nothing must not look identical | Defect |
| U9 | Prototypes were contained and disposable | Any artifact built to be reacted to is in the gitignored `prototypes/` directory or on an unmerged branch, is framework-free, and the decision it informed was written down. Its framework implications are **G3**, scored at blocker severity, not here | Defect |
| U10 | The pass informed the spec rather than becoming it | Recognized Constraints appear as product-spec text in the user's terms. `docs/unknowns.md` is not pasted into `docs/product-spec.md`, and the spec is not written before the handoff was confirmed | Defect |
| U11 | Steps 4 and 8 actually read it | Step 4 restates Decided Defaults as explicit choices with reasons; Step 8 turns a still-blocking open question into a tracker issue. Two named consumers, both observable. This is the row that separates `docs/unknowns.md` from an `@TODO` nobody re-reads | Defect |

### Step 6 — the fourteen skills are well-formed

The set is specified in four places — the table and tree under "The Baseline Skill Set" and "Where Skills Are Written" in `skills-builder.md`, the mirrored table and project tree in `grovv-stack-scaffold.md`, and both dedupe sites in `team-design.md` — and nothing in this repository compares any of them to each other, let alone to a generated tree. The directive expects "~14 invocable skills" and has no mechanical reader. **S0 exists because that fan-out is the drift this change bought.**

| # | Check | Pass condition | Severity |
|---|-------|----------------|----------|
| S0 | The four enumerations agree with each other | Before scoring anything generated, diff the four lists named above. They must contain the same fourteen names. This costs two minutes and is the only check that catches the drift risk the fourteen-skill change introduced — no script can see it | Defect |
| S1 | The baseline set is present | All fourteen baseline folder names are present under the target's chosen skills directory — not *only* fourteen, since Step 7 adds agent skills and an orchestrator to the same directory (Step 7 in `grovv-stack-scaffold.md`), or fewer with each drop named and justified against this project in the transcript ("The Baseline Skill Set" in `skills-builder.md`). A silent drop fails | Defect |
| S2 | Each folder holds a `SKILL.md` | One file per folder; no empty directories | Defect |
| S3 | Frontmatter parses and `name` matches the folder | For each: YAML parses, `name` is lowercase-with-dashes, and equals the folder name (`skills-builder.md:90`, `:203`). No script anywhere parses frontmatter, in this repository or a target | Defect |
| S4 | Descriptions are trigger-rich and mutually distinguishable | Each `description` names concrete situations that should invoke the skill, not a topic label; no two are so close that a near-miss request could route either way (`skills-builder.md:91-93`) | Note |
| S5 | Bodies are lean | `wc -l` under 500 for every `SKILL.md`, with depth in `references/` wherever it would have exceeded (`skills-builder.md:100`, `:204`) | Defect |
| S6 | Skills assert this project's stack, not the defaults | Take three facts from `docs/tech-spec.md` — the database, the auth provider, the runtime — and grep every `SKILL.md` for a contradicting assertion. Zero hits passes; each hit is a fail with the file named (`skills-builder.md:117`, `:206`) | Defect |
| S7 | The throwaway tier is carried | Stated in `dev-standards`, and in `ui-standards`, `frontend-development`, `architecture-planning` and `testing-tdd` where they touch exploration (`skills-builder.md:121`, `:208`) | Defect |
| S8 | Nothing landed where it must not | No `docs/skills/` directory and no `.claude/commands/` in the target (`skills-builder.md:209`) | Defect |
| S9 | Examples are complete and typed | Spot-check three skills: no pseudo-code, error handling present, anti-pattern shown beside the correct pattern where it teaches something (`skills-builder.md:99`, `:205`) | Note |
| S10 | `blind-spot-pass` triggers on the literal phrases | Its `description` carries "blind spot pass" and "unknown unknowns" verbatim, and the body instructs the agent to establish the user's starting point before investigating. The literal phrases matter: they are how a user invokes it mid-work, and a paraphrase does not trigger | Defect |
| S11 | `interviews` carries the stopping rule | A stated bound — architecture-changing questions exhausted, or a question count — and what happens to the remainder. An interview skill with no stopping rule is the failure mode the technique is most prone to | Defect |
| S12 | `change-quiz` is advisory and says how to make it blocking | Advisory by default, plus the one line a project puts in its own `CLAUDE.md` to make it a merge gate. A skill that is silently blocking, or that offers no way to become blocking, both fail | Defect |
| S13 | `implementation-notes` names the Deviations log and the conservative default | The working notes file, a `Deviations` heading, and the rule for a forced departure: take the lower-risk path, log it against the section it invalidates, continue | Defect |
| S14 | The four fold-in sections are present, in the right skills | `architecture-planning` carries brainstorms-and-prototypes and implementation-plans; `dev-standards` carries references and pitches-and-explainers ("Required Sections in Two Existing Skills" in `skills-builder.md`). A section in the wrong skill fails — placement is what keeps the trigger surface small | Defect |
| S15 | The implementation-plan section states the ordering | Data model first, then types and interfaces, then anything user-facing, with mechanical refactoring last. An unordered "write a plan" instruction fails: the ordering is the technique | Note |
| S16 | The four new skills carry their attribution line | One line crediting the technique. They carry no gro\\/\\/ stack footer by design, so the attribution is the only provenance they have | Note |

The ask-first content of these skills is **G5**, **G6** and **G10**, not an S row. It is scored at blocker severity. **G10** in particular covers `architecture-planning`, which is where S14's prototype section lands.

### Step 7 — every agent carries a stated rationale

| # | Check | Pass condition | Severity |
|---|-------|----------------|----------|
| T1 | The six defaults are intact | `scaffold`, `frontend`, `backend`, `testing`, `database`, `code-review` all present and unmodified except where the user approved a change (`team-design.md:33`, `:142`) | Blocker |
| T2 | Every added specialist has a definition file | `.claude/agents/{name}.md` exists for each (`team-design.md:144`) | Defect |
| T3 | **Every added specialist carries a stated rationale** | For each specialist, one sentence — in its definition or in the step's report — naming the component or capability in `docs/tech-spec.md` it covers, and why no default covers it. A specialist with no such sentence fails, however plausible it looks (`team-design.md:34`, `:37`) | Defect |
| T4 | The dedupe review ran against a named subject | The report lists the fourteen baseline skill folder names it deduped against. "Duplicate review was run" without them is the assertion, not the evidence ("Workflow" and the Deliverable Checklist in `team-design.md`) | Defect |
| T5 | Exactly one orchestrator skill | One, and it names the data flow, the error handling, and a test scenario (`team-design.md:146`) | Defect |
| T6 | The data-passing strategy is named and argued | One of the five at `team-design.md:97-103` is named explicitly; a shared store appears only where all three promotion conditions at `:105-113` are argued to hold | Defect |
| T7 | Cross-agent artifacts carry provenance | Writing agent, source artifact, and time, on every artifact one agent writes for another (`team-design.md:117`, `:149`) | Defect |
| T8 | The harness pointer is registered | The target's `CLAUDE.md` carries a trigger rule and a change-log table (`team-design.md:152`) | Defect |
| T9 | Nothing landed in `.claude/commands/` | Directory absent (`team-design.md:151`) | Defect |

### Step 8 — the backlog, `MEMORY.md`, and the hook

| # | Check | Pass condition | Severity |
|---|-------|----------------|----------|
| M1 | The tracker question was asked first | GitHub Issues or Linear put to the user, and nothing created until answered. Inferring it from a `.git` remote or an available MCP connection fails (`grovv-stack-scaffold.md:456`) | Blocker |
| M2 | Milestones and issues were presented before creation | The proposed list appears in the transcript before the first write to an external system (`grovv-stack-scaffold.md:462`; `tracker-setup.md:59`, `:398`) | Blocker |
| M3 | The backlog is actually seeded | Every phase in `docs/development-plan.md` has a milestone and every feature has an issue, or each difference is accounted for. Count both sides; do not eyeball | Defect |
| M4 | `MEMORY.md` was created | Present in the target root with the Tracker Coordination table filled in, or marked `@TODO` if the tracker path was unavailable (`tracker-setup.md:274`, `:401`) | Defect |
| M5 | Memory rules reached the target's `CLAUDE.md` | Read at session start; update before ending a session that changed anything meaningful (`tracker-setup.md:353`) | Defect |
| M6 | The hook is merged, not overwritten | `SessionStart` present in `.claude/settings.json` in the guarded form, with any pre-existing hooks preserved (`tracker-setup.md:354-373`, `:403`) | Defect |
| M7 | **The hook actually fires** | Start a fresh agent session with the working directory set to a *subdirectory* of the target, and confirm `MEMORY.md`'s content is in the opening context. The root is not a sufficient test: the `$CLAUDE_PROJECT_DIR` prefix exists because a bare `cat` prints nothing from a subdirectory, and the `2>/dev/null \|\| true` tail makes a hook that fires and a hook that silently does nothing look identical (`tracker-setup.md:373`) | Defect |

M7 is the item `MEMORY.md:81` has carried open since 2026-07-04.

-----

## Run 1 — The Generated Workflow

**All three `verify-loop.md` phases have landed, so this table is fully scoreable.** That was not true when this section was written: it instructed the scorer to skip the whole table until Phase 1 shipped. Phase 1 (Step 1 discovers the commands, Step 8 records them in the Verify table), Phase 2 (the Step 6 question and workflow generation) and Phase 3 (the adopt-mode proposal path, scored as **D8**) are all in the pipeline. Score every row.

One correction to W1 that follows from how Phase 1 was actually built: **Step 1 states the commands, Step 8 writes them.** `MEMORY.md` does not exist until Step 8 creates it, so a scorer looking for a Verify table immediately after Step 1 will find nothing and record a false fail. Check the transcript at Step 1 for the commands and their sources, and the file after Step 8.

This is the table that makes Layer 1 and Layer 3 close each other's loop. Layer 1 generates executable configuration into a target; nothing in this repository can read YAML, run a job, or observe a build. **W5** is the only item in the system that can tell a generated workflow from a plausible-looking one.

| # | Check | Pass condition | Severity |
|---|-------|----------------|----------|
| W1 | The verify commands were discovered at Step 1 and recorded at Step 8 | Step 1's transcript states the commands and the source each came from; the target's `MEMORY.md` then carries a `## Verify` table with a `Source` column, or a single `@TODO` row rather than an omitted table. For a new project the commands are unknown at Step 1 by construction and are derived at Step 4 from the chosen stack — check there instead, and score a Step 1 that invented them anyway as a fail | Defect |
| W2 | The recorded commands run | Execute each in the target and record the exit code. This is the one thing `verify-loop.md:178` admits nothing detects | Defect |
| W3 | The CI question was asked and an explicit answer waited for | The four options were offered and one was chosen. "Whatever you think" accepted as an answer fails (`verify-loop.md:80-87`, `:91`). If unasked generation also produced an E2E job, that is **G7** and the severity escalates to blocker | Defect |
| W4 | The workflow runs only recorded commands | Every `run:` line maps to a row in the Verify table. A `npm run lint` in a project with no lint script fails this item (`verify-loop.md:92`) | Defect |
| W5 | **The workflow's first run is green** | Push the branch to a throwaway remote and observe the first run of the generated workflow complete with every job succeeding. A red first run — missing script, missing lockfile, uninstalled toolchain, wrong runtime version — fails. `verify-loop.md:110` names the second-order damage: a team that starts by ignoring a red build | Blocker |
| W6 | The no-install posture did not transfer | The workflow installs and caches dependencies. This repository's `checks.yml:24-25` shape appearing in a target is a fail — that posture is a property of a repository that produces documents (`verify-loop.md:130`) | Defect |
| W7 | The workflow shape transferred | Each check is its own named step, later steps run after an earlier failure, triggers are push and pull request (`verify-loop.md:126-128`) | Note |
| W8 | A decline was recorded, not silently skipped | On "None", one line in `MEMORY.md` recording that CI was offered, declined, and why (`verify-loop.md:93`) | Defect |
| W9 | The README reads the table | The Quick Start's commands come from the Verify table, not from the npm placeholders (`readme-generator.md:121`) | Defect |

-----

## Run 2 — Re-entry Against Run 1's Output

**This is the case nothing has ever exercised.** No check script holds state, a baseline, or a comparison across time, and only one prompt document defines a second run of itself — `tracker-setup.md:384`, "Stay re-runnable", which is why `loop-engineering.md:193` models the re-entry contract on that file. Run 2 behaviour elsewhere is both unspecified and unobserved.

### Preparing run 2

Commit run 1's output, then make exactly three edits and record the line numbers of each:

1. **Swap the database** in `docs/tech-spec.md` — PostgreSQL for SQLite, say. Every skill and agent asserting the old one is now *drifted*.
2. **Drop an integration** named in run 1 — Stripe, say. The specialist Step 7 added for it is now *orphaned*.
3. **Hand-edit one generated `SKILL.md`**, adding a distinctive line. This is the artifact **R9** scores.

Two spec edits, one of each verdict at `loop-engineering.md:204-208`, so the run must produce both answers rather than the easy one. Then invoke the pipeline again against the same directory.

**Every row in this table is now scoreable.** That reverses the instruction this section carried until 2026-07-27, which told the scorer to skip R2 through R10 because the contract did not exist. It does now: `grep -rn "^## Re-entry" docs/prompts/` returns both prompts, each specifying the audit, the three verdicts, the drift naming, and the hand-edit rule. A scorer still following the old instruction would skip nine rows that are the entire reason run 2 exists.

Two rows gained a subject in the same change. **R3**'s three verdicts and **R8**'s re-justification are now written instructions rather than inferred expectations, which means a failure here is a real regression rather than an unbuilt feature. And a new row, **R15**, covers the clause most likely to be dropped in implementation.

| # | Check | Pass condition | Severity |
|---|-------|----------------|----------|
| R1 | The run was identified as a resume, not an adoption | The run states which it detected and why, before acting, and resumes. Proposing an adoption plan for a codebase grovv itself wrote is the failure `loop-engineering.md:91` and `:210` describe. Escalates to blocker if anything was written before approval | Defect |
| R2 | Step 6 audited before writing | The skill folders present and the stack each asserts are enumerated in the report *before* the first write (`loop-engineering.md:195`) | Defect |
| R3 | Three verdicts were reported before any action | Unchanged, drifted and orphaned lists all presented, and the run waited (`loop-engineering.md:197`, `:204-208`). A report carrying only one verdict fails even if that verdict is right | Defect |
| R4 | **Drifted artifacts are named, not left asserting the old stack** | Grep every generated `SKILL.md` and every agent definition for the old database name. Every hit appears in the drift list. One hit not in the list fails the item and names the file | Defect |
| R5 | Nothing was deleted or overwritten without approval | `git diff run-1..run-2` in the target shows no file removed and no content lost, except where the transcript shows the user approving it (`loop-engineering.md:197`, `:200`, `:208`) | Blocker |
| R6 | No duplicate-with-suffix folders | No `-2`, `-v2`, `-new` or `-updated` sibling of any run-1 skill folder. A skill whose name already exists is revised, never re-created (`loop-engineering.md:198`) | Defect |
| R7 | The orphaned specialist was surfaced, not deleted | The agent added for the dropped integration appears in the orphaned list and still exists on disk pending approval (`loop-engineering.md:198`, `:208`) | Defect |
| R8 | Surviving specialists were re-argued, not inherited | Each specialist's rationale in run 2's report cites a component in the *edited* spec. A rationale copied forward unchanged from run 1 fails (`loop-engineering.md:199`) | Defect |
| R9 | The hand edit survived or was asked about | The distinctive line is still present, or the run reported it and asked. Silently overwritten fails (`loop-engineering.md:200`) | Defect |
| R10 | A no-change run was reported as a success | If the run correctly concluded that the right action is no action, its closing report says so rather than reading as a skipped step (`loop-engineering.md:212`) | Note |
| R11 | Step 8 reconciled rather than duplicated | No duplicate issue titles; issues that no longer map to the edited plan are flagged, never deleted silently; milestones still track the plan's phases (`tracker-setup.md:60`, `:384`) | Defect |
| R12 | A declined workflow was not quietly regenerated | If run 1 declined CI, run 2 generated none, did not silently re-ask, and the decline line in `MEMORY.md` survived (`verify-loop.md:93`). Conditional on **W** | Defect |
| R13 | The Verify table was reconciled, not appended to | One table, no duplicate rows, and every command in it still runs. Conditional on **W** | Defect |
| R14 | **Neither ask-first rule was treated as settled by run 1's artifacts** | The framework choice and the Playwright scope carry forward as *recorded user decisions*, cited to where the user made them. A run reasoning "the skills already use Next.js, so" has inferred a decision from its own output, which is the pre-emption both rules exist to prevent. Nor were they re-litigated: the contract says carry forward, and re-asking a settled question is the opposite error | Blocker |
| R15 | **A no-action run was reported as complete, not as a skipped step** | Both `## Re-entry` sections end with "a re-entry that changes nothing and returns a list of questions has succeeded", and this is the clause an implementation is most likely to drop, because every other step in the pipeline terminates in an artifact. Score it directly: after the edits above, a correct run 2 writes nothing until the user approves. If the run wrote something to demonstrate it ran — a regenerated skill nobody asked for, a cosmetic revision, a duplicate table row — it failed, and the file it wrote is the evidence. R10 scores the closing report's wording; this row scores the disk | Blocker |

-----

## Run 3 — Adopt Mode Against a Real Foreign Codebase

Clone a third-party repository grovv did not write, into a throwaway directory that is never pushed. Choose one that is **not** the default stack — a Go service, a Python API — because a target that already matches the defaults cannot distinguish reading the project from restating them.

| # | Check | Pass condition | Severity |
|---|-------|----------------|----------|
| D1 | The adoption plan was approved before anything was written | The plan appears in the transcript, the user approves, and the first write follows (`grovv-stack-scaffold.md:185`, `:194`, `:631`) | Blocker |
| D2 | The plan's four sections are populated | Created, updated, left alone, and refactored-over-time all present with real entries (`grovv-stack-scaffold.md:189-192`) | Defect |
| D3 | Working code was not modified | `git status` in the target shows no change to any pre-existing source file | Blocker |
| D4 | An existing README was merged, not replaced | Content that was accurate before the run is still present (`grovv-stack-scaffold.md:468`) | Defect |
| D5 | Skills describe the real stack | For a Go target, `backend-development` covers Go; `database-design` covers the real database; `security-practices` names the real auth provider. Every skill asserting a grovv default the project does not use is a named fail (`skills-builder.md:181-185`; `grovv-stack-scaffold.md:396`) | Defect |
| D6 | Existing skills were extended, conflicts surfaced | Pre-existing entries under the target's `.claude/skills/` were updated rather than replaced, and every conflict was reported (`skills-builder.md:186`) | Defect |
| D7 | The framework question survived an existing frontend | The run either asked, or named the project's existing commitment out loud and had the user confirm it. Reading it silently out of `package.json` and proceeding fails — see **G1** | Blocker |
| D8 | Existing CI was not written over | With a workflow already present, the run stated what exists, stated what would change, and generated nothing before approval. This is verify-loop Phase 3 and is no longer conditional — it shipped with Phases 1 and 2 (Step 6 in `grovv-stack-scaffold.md`; "Generated CI" in `skills-builder.md`) | Blocker |
| D10 | The unknowns pass read the codebase rather than the intake | In adopt mode the blind spot pass has real code to work against, and that is where it is strongest: it should report what the code does that the user did not describe, where conventions are inconsistent, and what a newcomer would get wrong. A generic new-project blind spot list, produced against a repository sitting right there, fails | Defect |
| D11 | Existing verify commands were read, not invented | Step 1's recorded commands come from the project's own CI workflow, task runner or manifest, with the source named, and precedence given to the CI workflow where they disagree. A command that appears in the Verify table but in no project file fails, and names the file it should have come from | Defect |
| D9 | The tracker step reused what maps | An existing project or label taxonomy was reused where one maps to the codebase, and no existing issue was duplicated (`grovv-stack-scaffold.md:462`; `tracker-setup.md:171`) | Defect |

-----

## How to Record a Result

**One record per run, filed against the tracker issue that owns the smoke test** — GRO-197 as of `MEMORY.md:81` — not as a file in this repository. A result is evidence about one commit and goes stale; the rubric is versioned here, the results are not. A growing results log under `docs/architecture/` would also sit in a directory `check_references.py:64` deliberately does not read.

The record carries:

```text
commit:   <git rev-parse HEAD in grovv-stack>
date:     <YYYY-MM-DD>
mode:     new | re-entry | adopt
target:   <path, and the upstream repo for adopt mode>
layer-1:  implemented | not implemented (W table skipped)
layer-2:  implemented | not implemented (R2-R10, R15 skipped)
skills:   14 | 10

G1 pass   G2 pass   G3 n/a    G4 pass   ...
S5 FAIL   defect    testing-tdd/SKILL.md is 612 lines, no references/
U7 FAIL   defect    tech-spec names Clerk and Neon; no turn in the transcript
                    where either was put to the user. Decided Defaults empty
...

blockers: 0    defects: 3    notes: 1    skipped: 0
```

Four rules for the record:

- **One line per item ID, always**, including `n/a` and `skipped`. An item silently absent from a record is indistinguishable from one nobody checked, and that is how the July 4 smoke test stayed open.
- **A fail carries one sentence of observation**, naming the file or the transcript turn. "S6 fail — skills wrong" is not a finding; "S6 fail — `database-design` and `backend-development` both assert PostgreSQL, spec says SQLite at tech-spec.md:88" is.
- **Blockers do not stop the scoring, they stop the release.** Keep going: a second blocker found in the same session is free, and found in the next release is not.
- **Then update `MEMORY.md`** — a dated Decision Log entry with the commit, the mode, and the three counts. Reference the tracker issue by identifier; do not mirror the item list into the file, which has a ~120-line budget.

-----

## Open Questions

- How often is this run? It is now **94 scored items** across three runs — G 10, U 11, P 5, S 17, T 9, M 7, W 9, R 15, D 11 — up from about sixty, and growing every time the pipeline gains a feature. That is the tension this rubric cannot resolve on its own. Running it on every prompt edit would mean nobody runs it. Currently: before any release that changes `grovv-stack-scaffold.md` or anything under `docs/prompts/`, which is most releases and is the point. If it grows past a session, the honest move is to split the gate table plus run 1 into a short pass that runs every release, and runs 2 and 3 into a long pass that runs less often — not to quietly stop running any of it.
- **Who answers the ask-first questions?** G1, G4, R14 and D7 all require a *user* turn in the transcript, so an agent running this rubric alone cannot score them without answering its own questions, which invalidates exactly the rows that matter most. Currently: a human answers, and a solo run records those rows as `n/a — no user present` rather than passing them. A solo run is still worth doing for the structural rows; it is not an acceptance test.
- Runs 1 and 2 must share a target, so either they happen in one sitting or the throwaway directory outlives the session. A directory kept for a week is a directory somebody commits. Currently: one sitting, deleted after the record is filed.
- Does **W5** need a real CI provider? A local runner does not reproduce a missing toolchain or a wrong runtime version, which is the failure the item exists to catch. Currently: a real push to a throwaway remote, accepting that it costs a repository and some minutes.
- Are two spec edits enough for run 2? A third and fourth would exercise more of the drift report and would make a wrong report much harder to score, because the pass condition stops being enumerable. Currently: two spec edits plus one hand edit.
- Which foreign codebase for run 3? A fixed choice makes results comparable across releases but trains the pipeline against one repository; a rotating choice makes every run a fresh test and every regression an argument about whether the target changed. Currently: rotating, with the upstream repository and its commit recorded.
- Should this rubric's own citations be checked? They rot exactly as `loop-engineering.md:226`'s did, and arming a checker over `docs/architecture/` would break the three notes that correctly name files which do not exist. Currently: re-verify by hand on every edit, which is a rule with no enforcement and should be read as such.
- Nothing here scores the *quality* of a generated skill — whether its guidance is good, only whether it is well-formed and consistent with the spec. That is the judgment `loop-engineering.md:228` says needs a scorer and a gold set. Currently: out of scope, and stated rather than implied.
- @TODO — confirm GRO-197 is still the issue of record before a result is filed against it. `loop-engineering.md:314` records that the brief for that note named GRO-127, which appears nowhere in this repository.

-----

## Colophon

| Field | Value |
|-------|-------|
| **Version** | 0.2.0 |
| **Last Updated** | 2026-07-27 |
| **Status** | Current — level with the pipeline, never run |
| **Author(s)** | grovv stack scaffolding agent |
| **Model** | Claude (Claude Code) |

-----
gro\\/\\/ stack — Pipeline Smoke Test
