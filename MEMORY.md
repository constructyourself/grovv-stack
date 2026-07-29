# MEMORY.md

Cross-session memory for grovv-stack development. An agent starting a session in this repo reads this file first; an agent finishing meaningful work updates it before ending. It works in coordination with the Linear project — Linear owns the backlog, this file owns the context.

-----

## How This File Works

- **Read at session start.** A `SessionStart` hook in tool-specific `settings.json` surfaces this file automatically; if hooks are unavailable, read it manually before any other work.
- **Update before ending a session** that changed anything meaningful: refresh Current State, append a dated entry to the Decision Log, update Next Steps, and prune anything stale.
- **Linear owns the backlog.** Tasks, priorities, status, and assignments live in the Linear project. Never duplicate issue lists here — reference issues by identifier instead.
- **This file owns context.** Decisions and rationale, gotchas, in-flight state, and anything a fresh session needs that does not fit a Linear issue.
- **Stay small.** Keep this file under ~120 lines. It is loaded into context every session; verbosity here is a tax on every future session. Prune aggressively — history lives in git.

-----

## Linear Coordination

| Field | Value |
|-------|-------|
| Project | https://linear.app/grovv/project/grovv-stack-838efdf244c3 |
| Team | Grovv |
| Issue prefix | GRO |

Sync rules:

- When work in this repo completes a Linear issue, note the issue identifier in the Decision Log entry and mark it done in Linear (or flag it here with `@TODO` if Linear is unreachable from the session).
- When a decision here changes the scope of a Linear issue, update the issue — do not let the two drift.
- New work discovered mid-session becomes a Linear issue, not a bullet that lives here forever. Next Steps below is a short-term pointer, not a backlog.

-----

## Current State

- Repo is a multi-tool prompt-driven scaffolding system (`grovv-stack` v0.9.1) — not an application. Output is docs/config in *other* projects.
- **Multi-tool support added**: Claude Code (original), Vibe, and Codex now supported via tool-specific directories (`.claude/`, `.vibe/`, `.codex/`).
- **Canonical shared definitions** in `.grovv/` directory for tool-agnostic agents and skills.
- **Step 1 asks which tool directories a target gets.** Choose one assistant and only that directory is created (no `.grovv/`); choose more and `.grovv/` is canonical with the rest derived. Previously a target received only the directory of whichever CLI ran the scaffold.
- **The kickoff skill has a third detect branch.** `docs/prompts/skills-builder.md` plus a populated skills directory means a grovv project is resuming, tested before the existing-project branch. Without it a second `/grovv` proposed an adoption plan for output grovv itself wrote.
- Single entry point: the `grovv` skill (`/grovv`, auto-detects new vs adopt). Pipeline: Steps 0–9 in `grovv-stack-scaffold.md`.
- Step 8 (tracker-setup) asks which tracker a target project should use — GitHub Issues (recommended) or Linear — seeds that backlog, and creates/maintains the project's `MEMORY.md`, coordinated with the chosen tracker.
- Six baseline agents: canonical in `.grovv/agents/`, tool-adapted in `.claude/agents/`, `.vibe/agents/`, `.codex/agents/`.
- harness meta-skill vendored under `.grovv/skills/harness/` (Apache-2.0) powers the team-design step, mirrored to tool directories.
- The Throwaway Tier scopes production-first: exploratory artifacts (prototype, mockup, brainstorm, spike) are exempt from the production bar and never merged. `proto/*` or `spike/*` branches, or the gitignored `prototypes/`. Full rules in `grovv-stack-scaffold.md`.
- **Step 2 opens with an unknowns pass**, before the product spec: four questions about the person, a blind spot pass, a one-question-at-a-time interview, and prototypes to react to. Writes `docs/unknowns.md` (created empty at Step 1, read at Steps 4 and 8). Declinable, with the decline recorded. It has no step number of its own — see the Decision Log.
- **Step 6 asks how much CI a target gets** — everything, minimal, pick-them, or none — and generates a workflow from only the commands Step 1 discovered. Never an E2E job, never a deploy job. Layer 1 of `loop-engineering.md` is complete end to end.
- **No generated artifact ever settles an ask-first question.** When a generated skill and `docs/tech-spec.md` disagree about the framework or Playwright scope, both are named to the user and the user decides. Written into `skills-builder.md` and `team-design.md`.
- **Fourteen baseline skills**, not ten — the original ten plus `blind-spot-pass`, `interviews`, `implementation-notes`, `change-quiz`. Named in four places: `skills-builder.md`'s table and tree, `grovv-stack-scaffold.md`'s mirrored table and tree, and both of `team-design.md`'s dedupe sites. Change one, change all four.
- **Steps 6 and 7 reconcile on a second run**, they do not regenerate: audit, verdict each artifact against the current tech spec, report, wait. A run that changes nothing and returns questions has succeeded. `## Re-entry` in both prompts; Layer 2 of `loop-engineering.md` is complete.
- CI exists: `.github/workflows/checks.yml` runs seven check-only scripts (wordmark, versions, tool sync, references, step numbers, stack tables, ask-first). Standard library only — no build step, and a check enforces that.
- No build steps, no dependencies — documents and configuration only.
- Backward compatible: existing Claude Code users unaffected.

-----

## Decision Log

Append-only, newest first, dated. One line of decision, one line of why. Prune entries older than a few months if no longer load-bearing.

- **2026-07-27** — **First smoke-test run, ever — Steps 0–9 complete.** New-project mode, real product brief, real discovery deck, 229 files generated. Ten findings. One was recorded as a blocker, pushed, and then **withdrawn on verification** — `change-quiz` had not failed to generate, it was queued behind a concurrency cap, and the run counted folders and called them skills. Real defects found instead: four skill descriptions over 1024 characters, including the two owning the Playwright and per-asset-gating rules, and a `.claude/` mirror 273 lines out of sync with canonical so the audited copy was not the loadable one. The wordmark convention corrupted when a generated `CLAUDE.md` restated it in one line, and the inline-span exemption meant `check_wordmark` could not catch it — the third time that exact bug has landed here. Ask-first held throughout: framework never chosen, no Playwright flows invented, CI declined and the decline recorded. The two worth remembering: Step 1 told the agent to write the tool-directory answer to `MEMORY.md`, which does not exist until Step 8 — the *identical* defect fixed hours earlier for the verify commands, in the same step, missed because the first fix did not check for the same sentence pattern nearby. And the pass recorded a question as "asked, not answered" when the question was never delivered to the user, entering a false claim about a human into a durable artifact. Rubric rows U12–U14 added.
- **2026-07-27** — Layer 2 finished: both `## Re-entry` sections written, with the directive and `agents/scaffold.md` pointers that reach them and a Success Criteria item for a resume run. The clause most likely to be lost in implementation is the one that makes it work — *a re-entry that changes nothing and returns a list of questions has succeeded* — because every other step in the pipeline terminates in an artifact, so an implementation with no shape for "no action" will write something to prove it ran.
- **2026-07-27** — Baseline skill set went from 10 to 14: `blind-spot-pass`, `interviews`, `implementation-notes`, `change-quiz`. Four more techniques fold into `architecture-planning` and `dev-standards` as required sections rather than skills, keeping the trigger surface small. `architecture-planning` now carries both ask-first rules, since it is where prototypes get built. The count is mirrored in `grovv-stack-scaffold.md` and in both of `team-design.md`'s dedupe sites — a set named in four places is the drift risk this change buys.
- **2026-07-27** — Implementation notes into `agents/testing.md`, change-comprehension quiz into `agents/code-review.md`, four trees each. The quiz is advisory by default with a documented one-line opt-in to make it blocking; a blocking merge gate is a strong claim about a review culture grovv has never met.
- **2026-07-27** — The Unknowns Pass landed **inside Step 2** rather than as a new numbered step; the 2–9 → 3–10 renumber was declined. Three reasons: the Throwaway Tier had already closed two of the three findings the step existed for; the position argument only ever required being upstream of the product spec, which the opening of Step 2 satisfies; and the renumber surface had grown 61% since the map was drawn. Also killed `grovv-stack-scaffold.md`'s "(if not already clear)" stack hedge — always satisfied by the stack table, so the question never fired and projects inherited six vendors nobody weighed.
- **2026-07-27** — Layer 1 finished: Step 6 now asks how much CI, in four options, and generates a workflow from exactly the commands Step 1 found. Declining is a recorded outcome, not a skipped step. A generated workflow never carries an E2E job — a workflow asserting that E2E tests gate merges answers the Playwright question by configuration, which is the pre-emption the rule exists to stop.
- **2026-07-27** — Settled `re-entry.md`'s sharpest open question: when a generated skill and the generated tech spec disagree about an ask-first answer, report both and let the user decide. Deferring to the spec "because it is authoritative" answers the question with an artifact this pipeline wrote, and deferring to the skill is the same error reversed. Implemented ahead of the `## Re-entry` sections because adopt mode meets the clash on a *first* run, not only a second.
- **2026-07-27** — `docs/architecture/` notes get a dated historical note rather than being renumbered or rewritten as the pipeline moves. They are reasoning records; their locators are snapshots and say so.
- **2026-07-27** — Target projects now get the tool directories their team actually uses, asked in Step 1 rather than inferred from the running CLI. The multi-tool promise held for this repo and stopped at its output, which is backwards — the output is where teams work. `.grovv/` is created only when more than one tool is chosen, since a single-tool project should not carry a canonical tree nobody opens.
- **2026-07-27** — Fixed the re-entry misclassification (loop-engineering Layer 2): a populated `docs/` was the existing-project signal, and grovv creates one by construction, so every second `/grovv` in a grovv-built project ran the mode designed for foreign code against its own output. A third detect branch, tested first, resumes instead.
- **2026-07-27** — `readme-generator.md` no longer emits its Quick Start template unchecked. It shipped `npm install` / `cp .env.example .env` / `npm run db:migrate` / `npm run dev` with no instruction to confirm those scripts exist — four commands that fail on first use, in the document a new contributor reads first. It must now substitute real commands or write a `@TODO`.
- **2026-07-27** — Layer 1 specified in `docs/architecture/verify-loop.md` (proposed, not implemented). The CI question is Step 6, not Step 1, because at Step 1 the tech spec does not exist and the question cannot name the project's real test runner. A generated workflow never contains an E2E job on the strength of that question — Playwright scope is ask-first, and a workflow asserting E2E tests gate merges pre-empts it.
- **2026-07-26** — Added the Throwaway Tier, scoping production-first rather than weakening it. An audit against the "Finding your unknowns" field guide found the principle structurally forbade prototypes: production-readiness plus never-pseudo-code made a disposable mock non-compliant by definition, so unknown knowns surfaced during implementation instead of while reacting to something cheap. Everything that ships is still production-ready; exploratory artifacts are exempt and never merged. Two boundaries carry the weight — a prototype never satisfies an ask-first rule, and code review checks unmerged/throwaway-located/decision-recorded instead of the production checklist.
- **2026-07-26** — Added CI: seven check-only scripts under `.github/`. Each was written after the drift it detects had already happened, not speculatively. Notable: the wordmark rule was stated *incorrectly* in all five places that stated it, and `.grovv/` — the canonical tree — was the wrong copy in two files, so "sync from canonical" would have propagated the error.
- **2026-07-26** — Step 8 is now tracker-agnostic: `docs/prompts/linear-tracking.md` was renamed to `docs/prompts/tracker-setup.md`, and the step opens by asking the user for GitHub Issues (recommended) or Linear. Project Tracking in every stack table now reads "GitHub Issues (recommended) or Linear — chosen per project". Rationale: most scaffolded projects already live in a GitHub repo, so issues, branches, and PRs cross-link with no extra service; Linear stays first-class for multi-repo or cross-team backlogs. This repo's own backlog is unaffected — it stays in Linear (GRO).
- **2026-07-25** — Added multi-tool support for Vibe and Codex. Created `.vibe/`, `.codex/`, and `.grovv/` directories with tool-specific and canonical configurations. Updated all documentation (README.md, CLAUDE.md, created VIBE.md, CODEX.md). Created unified plugin.json. All tool-specific skills and agents adapted for their respective platforms. Backward compatible with existing Claude Code installations.
- **2026-07-04** — Adopted the MEMORY.md convention, both for this repo and as scaffold output (GRO-196, PR #9; promoted from GRO-169). Maintained via tool-specific context file rules plus a `SessionStart` hook; generated in target projects by the linear-tracking step (Step 8), since the two artifacts coordinate: Linear = backlog, MEMORY.md = session context.
- **2026-07-04** — Division of responsibility fixed: never mirror Linear issue lists into memory files; reference identifiers only.

-----

## Gotchas

- The gro\\/\\/ wordmark: doubled backslashes (`gro\\/\\/`) in prose, single (`gro\/\/`) inside code blocks. `.github/scripts/check_wordmark.py` enforces it. Getting this wrong is the most common review catch in this repo.
- Stack or pipeline changes must propagate to **every** doc that references them: `grovv-stack-scaffold.md`, `.grovv/CLAUDE.md` (canonical), `CLAUDE.md`, `VIBE.md`, `CODEX.md`, `.claude/agents/*.md`, `.vibe/agents/*.md`, `.codex/agents/*.md`, `docs/prompts/*`, `README.md`, and all tool-specific grovv skill files. Grep before committing.
- Bump `version` in `.claude-plugin/plugin.json` and `plugin.json` for any behavior change installed users should receive.
- Canonical agents and skills live in `.grovv/`; tool-specific adaptations in `.claude/`, `.vibe/`, `.codex/` — never duplicate into root-level `agents/` or `skills/`.
- Tool-specific context files: `CLAUDE.md` (Claude), `VIBE.md` (Vibe), `CODEX.md` (Codex) at root; `.grovv/CLAUDE.md` is canonical core.
- Ask-first rules (frontend framework, Playwright scope) must never be pre-empted by any generated artifact, including Linear issues and memory entries.
- **Renumbering the pipeline: count in lines, and say which unit you counted.** Two figures in this file once contradicted each other and *both were right* — one counted occurrences, one counted lines. Measured against `HEAD` on 2026-07-27, excluding `.git`, the vendored harness and `docs/architecture/`: **123 occurrences across 100 lines in 18 files**. `docs/architecture/` holds **261 occurrences across 158 lines in 5 files** and is deliberately excluded — those notes are dated history, not live references. The harness trees hold **20 more** that are that skill's own Korean-language phase numbers in Apache-2.0 vendored code; a naive `sed` corrupts them, and the exclusion must be applied to the **path field**, not the whole line, or it drops a real reference whose prose happens to mention the harness path.
- **Two renumber traps, both confirmed live.** Exactly one ASCII-hyphen range exists — `grovv-stack-scaffold.md`, "Work through Steps 2-9 sequentially" — and its lower bound must stay 2 while the upper bound moves, because the list item before it covers Step 1, so the bound means "everything after Step 1" rather than "old Step 2". A mechanical +1 on both ends is wrong there and only there. The other 13 ranges are `Steps 0–9` with en dashes, so a `sed` for one dash form silently misses the other. Matching en dashes inside a POSIX bracket expression is locale-dependent and returned zero when it should have returned 13 — count with `grep -o` and read the separators, do not trust a bracket class.
- Renumbering has been proposed twice and declined twice (loop-engineering, unknowns-engineering), both times folding into an existing step instead. Read both rejection records before proposing it a third time.

-----

## Next Steps

- Run the GRO-197 smoke test (SessionStart hook fires; Step 8 generates memory in a real target project). Open since 2026-07-04 and now more load-bearing: it is the only thing that can catch a generation regression, and `verify-loop.md` proposes generating a CI workflow into targets.
- @TODO — GRO-169's description still lists "memory system" as open; editing it was approval-gated from the agent session (a comment noting the promotion was added instead). Strike it through manually or from an approved session.
- Run the smoke-test rubric (`docs/architecture/pipeline-smoke-test.md`) against a throwaway target. It is now the only thing that can catch a generation regression, and the pipeline generates materially more than when the rubric was written — Step 2's pass and Step 6's workflow are both unscored by it.
- **Read `docs/architecture/smoke-test-next-steps.md` before scheduling either remaining run.** It carries the preparation each needs and six open questions; N1 (how run 1's target survives to run 2) blocks everything about run 2.
- **The target's context file is created at Step 1**, one per chosen tool. It used to be created by nothing while three instructions wrote into it — Step 1's canonical-source statement, Step 7's harness pointer, Step 8's memory rules. Step 1 owns it because Step 1 is where the tool choice that decides which context files exist is made.
- **F1's shape has now appeared four times**: verify commands (fixed), tool-directory answer (fixed, adjacent bullet), the canonical-source statement (found by an audit, in the bullet immediately *above* the second fix), and the stale Layer 1 design in `loop-engineering.md` that still specified the corrected-away version. Each fix was correct and none of them looked one line further. When this shape appears again, grep the whole step and every architecture note before calling it closed.
- **A fix in `grovv-stack-scaffold.md` is not a fix until it reaches `docs/prompts/*.md`.** Three times now a rule landed in the directive and not in the prompt that executes it. The scaffold is read once at the start; the prompt is what runs at generation time. Same lesson as F1, different axis — grep the prompts before calling a defect closed.
- **Run 2 and run 3 are still unexercised.** Run 1 covered Steps 0–9 in new mode. The re-entry contract (R1–R15) needs a second session against the same target, and adopt mode (D1–D11) has never run at all. Both are where reconciliation-rather-than-regeneration is proved, and neither has been tested once.
- **Never assume a question was delivered.** The run recorded one as refused when it never arrived; the user said so. Re-ask in plain prose before writing anyone's silence into a document.
- **When fixing a defect, grep for the same shape nearby.** F1 was the same bug as the verify-commands defect, in the same step, found hours later by a human running the pipeline rather than by the fix that should have caught it.
- **An absence is not evidence until you know the work finished.** Twice in one session a fact was asserted from a silence: a question recorded as refused that was never delivered, and a skill recorded as missing that was still being written. Both went into durable artifacts before being checked. Where work runs concurrently, confirm it has finished before concluding anything about what it did not produce.
- ~~Run the smoke test.~~ Done once, partially. Standing detail below still applies: Layers 1 and 2 are complete, and every remaining risk is a generation regression only a real run can catch. The rubric (`docs/architecture/pipeline-smoke-test.md`, v0.2.0) is now level with the pipeline — 94 items, with the unknowns pass, the CI question, the re-entry contract and the fourteen-skill set all scored. **A human has to answer the ask-first questions**: G1, G4, R14 and D7 each require a user turn in the transcript, so an agent scoring its own run invalidates exactly the rows that matter most. A solo run is worth doing for the structural rows and is not an acceptance test.
- Run 2 — re-entry against run 1's output with the spec edited in between — is still the case nothing has ever exercised, and it is now the highest-value half, because the whole re-entry contract is restraint and restraint is invisible to every check here by construction.
- `docs/prompts/tech-spec.md` and `tech-spec-template.md` (897 lines, legacy idiom) have been skipped by every change so far. `tech-spec-template.md` is also still unreferenced by the master directive.


-----
gro\\/\\/ stack — Cross-Session Memory
