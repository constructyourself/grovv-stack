# Unknowns — Proposed Skill Bodies

Specification appendix. This document contains the **proposed content** for four new baseline skills and four insertions into existing baseline skills, arising from the unknowns workstream. Nothing here has been applied.

Scope of this document: content only. It writes no pipeline edits and changes no step numbers; a later session executes it mechanically against the files named below. The single edit made outside this file is the folder-name reconciliation in `docs/architecture/unknowns-engineering.md`, recorded in Part 1.

-----

## How a Later Session Executes This

The four new skills and the four insertions are **generated output** — they are written into target projects by the skills-builder step, not into this repo. The executable change is therefore to the two files that enumerate the baseline set independently: `docs/prompts/skills-builder.md`, which the step reads, and `grovv-stack-scaffold.md`, which the `grovv` skill reads first and which carries its own copy of the same list.

| Change | File and location |
|--------|-------------------|
| Add four rows to the baseline skill set | `docs/prompts/skills-builder.md` — the table under "The Baseline Skill Set" (`Skill folder` / `Triggers on` / `Covers`) |
| Add four folders to the directory tree | `docs/prompts/skills-builder.md` — the tree under "Where Skills Are Written" |
| Carry the four insertion sections as required content | `docs/prompts/skills-builder.md` — the "Covers" cells named in Part 2, plus the section text quoted verbatim |
| Add `architecture-planning` to both ask-first rule sites | `docs/prompts/skills-builder.md:119-124` ("Ask-First Rules (embed these in the skills)") and the matching checklist item at `:196` — literal replacement bullets at the end of Part 2 |
| Amend the footer rule to cover these four bodies | `docs/prompts/skills-builder.md:183` — see "Conventions Used in This Appendix" |
| Add the checklist lines | `docs/prompts/skills-builder.md` — "Deliverable Checklist" (see Part 3) |
| Add four rows to the mirrored baseline table, and apply the Part 2 "Covers" gains to its `architecture-planning` and `dev-standards` rows | `grovv-stack-scaffold.md:329-340` — two columns (`Skill` / `Covers`), **not** the three-column skills-builder shape. Its wording differs too: it says "the pre-dev checklist, ADRs" where skills-builder says "the pre-development checklist", and its `dev-standards` row never names the definition of done. Edit the cells that are there; do not import the other file's wording |
| Add four folders to the mirrored project tree | `grovv-stack-scaffold.md:111-120` — bare fence, inserted before the `{orchestrator}/` line at `:121` |
| Change the expected-output count | `grovv-stack-scaffold.md:376` — "~10 invocable skills (the baseline set)" becomes "~14" |

The baseline set goes from ten skills to fourteen, and **both** enumerations have to say so. `grovv-stack-scaffold.md` is read end-to-end on every invocation before any file is written, so a session that updates only `docs/prompts/skills-builder.md` ships a directive advertising ten baseline skills against a prompt that generates fourteen — the drift the repository's own "propagate to every doc that references them; grep before committing" rule exists to prevent.

The four techniques in Part 2 deliberately do **not** become skills — they are sections inside skills that already own their subject, so the trigger surface stays small.

-----

## Conventions Used in This Appendix

Each skill body below is a complete `SKILL.md`, frontmatter included, shown inside a fenced block and ready to be written to disk verbatim.

The bodies carry **no colophon and no footer line**. That matches the two skills this repo actually ships — `.claude/skills/grovv/SKILL.md` and the vendored `.claude/skills/harness/SKILL.md`, both exposed by `"skills": "./.claude/skills/"` in `.claude-plugin/plugin.json` and both mirrored under `.grovv/`, `.vibe/`, and `.codex/`. Neither carries a colophon or a footer.

It is also a deliberate departure from a standing instruction, and the departure has to be executed rather than assumed. `docs/prompts/skills-builder.md:183` instructs that the gro\\/\\/ stack footer be applied to grovv-authored skill bodies where it reads naturally, with terse reference files as the only stated exemption — and these four are grovv-authored skill bodies. The executable change above therefore extends that line's parenthetical exemption to name the four unknowns skills. Amend the parenthetical in place; do not retype the wordmark on that line.

The reason to depart rather than comply is mechanical. Every body here lives inside a fenced block until the moment it is written to disk, and the wordmark takes single backslashes inside a fence and doubled backslashes in prose. A footer would put the wordmark exactly on that boundary — read one way in this document, written the other. The bodies avoid the wordmark entirely, which is what makes them copyable verbatim. If a project adds a footer of its own after the fact, it lands in prose position and takes the doubled-backslash form.

Every body ends with a one-line attribution (see Attribution, below). Keep it — it is the credit for the technique.

-----

## The Four Quadrants

Stated once, here, so that every mapping below is checkable against it rather than re-glossed skill by skill. The definitions are the field guide's.

| Quadrant | Definition | Worked by |
|----------|-----------|-----------|
| Known knowns | What you have told the agent you want — effectively, your prompt | Nothing here; it is already in the map |
| Known unknowns | Gaps you have identified and can name, but have not resolved | `interviews`; the implementation-plan section |
| Unknown knowns | Context so obvious you would never write it down, but that you recognise on sight | The brainstorms-and-prototypes section; the references section; `change-quiz`, for your own diff |
| Unknown unknowns | What you have not considered at all — knowledge you do not know exists, including not knowing how good the result could be | `blind-spot-pass`; `implementation-notes`; the pitches-and-explainers section, for other people's |

The middle pair is the one that gets collapsed. **Recognition on sight** is the discriminator for unknown knowns. **Not having considered it at all** is the discriminator for unknown unknowns. The operational consequence is that a question can surface a known unknown, but only an artifact to react to surfaces an unknown known.

-----

## Part 1: Four New Baseline Skills

| Skill folder | Triggers on | Owns |
|--------------|-------------|------|
| `blind-spot-pass` | "blind spot pass", "unknown unknowns", "what am I missing", unfamiliar module or domain | Pre-work reconnaissance; user calibration before investigation |
| `interviews` | "interview me", "ask me questions", underspecified requests, open `@TODO`s | One-question-at-a-time elicitation, ordered by architectural leverage, with a stopping rule |
| `implementation-notes` | Starting a build from a plan; "keep implementation notes", "log deviations" | The working notes file, the Deviations log, the conservative-default rule |
| `change-quiz` | "quiz me", "explain this change", pre-merge review of a long session | Change report plus quiz; advisory by default |

**The folder names above are fixed.** `docs/prompts/skills-builder.md:54` and `:198` make baseline skill names a precondition for the team-design duplicate review (harness Phase 4-0), so a rename after generation is not cheap. The sibling note `docs/architecture/unknowns-engineering.md` originally specified `interview-me` for the second skill; it has been reconciled to `interviews`, the name the decision was stated in. Both documents now say `interviews`.

-----

### 1. `blind-spot-pass`

Path: `.claude/skills/blind-spot-pass/SKILL.md`

````markdown
---
name: blind-spot-pass
description: "Runs a blind spot pass to surface your unknown unknowns before you commit to an approach. Use whenever the user says 'blind spot pass', 'unknown unknowns', 'what am I missing', 'I don't know this part of the codebase', or 'help me prompt you better' — and whenever work is starting in an unfamiliar module, an unfamiliar domain, or a discipline the user has never practised. Establishes what the user already knows first, then investigates the code and the prior art, then reports the gaps as a map they can act on. Reconnaissance only: it explains, it does not implement."
---

# Blind Spot Pass

A blind spot pass finds the unknown unknowns — what you have not considered at all: knowledge you do not know exists, constraints nobody thought to tell you, and the possibility that you have no basis for judging how good the result could be. It is not the pass for something you would recognise on sight; that is a different kind of unknown, and an artifact to react to surfaces it, not a report. Run a blind spot pass before committing to an approach, while changing direction is still cheap.

This is reconnaissance. The output is understanding. Do not write implementation code during a blind spot pass.

-----

## Establish what the user already knows — first

Before opening a single file, find out where the user is starting from. A blind spot pass calibrated to the wrong person is worthless: the same report either patronises an expert or buries a beginner in vocabulary they cannot use.

Ask these briefly, in one message, and wait:

| Question | What it calibrates |
|----------|--------------------|
| How much have you worked in this part of the codebase? | How much orientation the report needs |
| Have you built this kind of thing before, anywhere? | Whether domain fundamentals are a gap or an insult |
| What have you already tried or ruled out? | Stops the report re-covering known ground |
| Where are you — exploring, deciding, or already committed? | How hard to push alternatives |
| Do you want me to teach, to challenge, or to execute? | The register for the whole collaboration |

If the user answers only some, proceed with what you have and say plainly which calibration is missing.

Never infer these answers from the codebase. A repository records what was built. It says nothing about who is asking or what they know.

-----

## Then investigate

With calibration in hand, go wide before going deep:

- Read the code that already touches this area, including the parts the user did not mention.
- Read the history — commit messages, prior attempts, reverted changes, `@TODO`s left behind. A reverted commit is often the cheapest available lesson.
- Read the project's own documents: `docs/tech-spec.md`, ADRs, the development plan. Note where they and the code disagree.
- Look outside the repo for standard practice in this domain, especially the failure modes practitioners treat as obvious.
- Note what does not exist. Missing tests, missing migrations, missing error paths are blind spots too.

-----

## Report the blind spots

Structure the report by *kind* of unknown, not by file. Kinds are what make a blind spot recognisable.

| Category | What goes here |
|----------|----------------|
| Already exists | Code, config, or infrastructure that solves part of this and the user did not know about |
| Already decided | Constraints locked in by earlier choices, with the locator that proves it |
| Standard practice | What practitioners in this domain treat as table stakes |
| Known failure modes | The specific ways this goes wrong, and the early signal for each |
| Vocabulary | Terms the user will need to ask precise questions |
| What "good" looks like | The quality bar, when the user has no basis to judge it yet |

Cite a checkable locator — file and line, commit, test name — for every claim about this codebase. A claim with no locator is flagged as unverified, not asserted.

Rank the report. Lead with the blind spot that would be most expensive to discover late.

-----

## Close with better prompts

End with the two things that make the pass reusable:

1. **The questions the user can now answer** that they could not answer an hour ago. Ask them.
2. **A sharper prompt** for the actual work, written in their voice, incorporating what the pass found.

-----

## Boundaries

- A blind spot pass never resolves a standing ask-first question on the user's behalf. Naming a decision as a blind spot is the job; making it is not.
- Record anything still open as `@TODO` in the relevant document. An unknown that is now *known* to be unknown is a result, not a failure.
- If the pass reveals the work should be scoped differently, say so before proposing an implementation.

-----

## Anti-patterns

- Reading the codebase first and asking about the user second — the report is then written for nobody.
- A flat list of everything found. Unranked findings are indistinguishable from noise.
- Confusing a blind spot pass with a plan. This pass ends in questions, not tasks.
- Reassurance. "This looks straightforward" is the one sentence a blind spot pass must never produce.

-----

Technique adapted from "Finding your unknowns," a field guide by Thariq Shihipar of Anthropic (July 2026) — one practitioner's documented practice, not a validated method. The specific rules above are this project's.
````

-----

### 2. `interviews`

Path: `.claude/skills/interviews/SKILL.md`

````markdown
---
name: interviews
description: "Interviews the user one question at a time to resolve ambiguity before building, prioritising the questions whose answer would change the architecture. Use when the user says 'interview me', 'ask me questions', or 'what do you need to know'; when a spec, plan, or ticket still carries open @TODOs; or when a request is underspecified enough that you would otherwise have to guess. Carries an explicit stopping rule — an interview that never ends is worse than no interview."
---

# Interviews

An interview converts your known unknowns into answers before they harden into code. It is a conversation, not a form: one question, one answer, then the next question chosen in light of it.

-----

## The format

- **One question per message.** Never batch. A batched list gets one skimmed reply and loses the follow-ups, which is where the real answers live.
- **Say why you are asking.** State what changes depending on the answer. A question with visible stakes gets a considered answer.
- **Offer real options with consequences**, not open air — but leave room for an answer you did not list.
- **Let the previous answer choose the next question.** If an answer eliminates a branch, drop every question on that branch.
- **A stated default is still an answer they gave.** If the user says "whatever you think", state your recommendation and ask them to confirm it. Do not treat silence as confirmation.
- **Record "I don't know" as `@TODO`** against the document it affects, and move on. Not knowing is a valid answer and a useful one.

-----

## Ordering: architectural leverage first

Before asking anything, list the candidate questions and rank them by how much the answer changes the *shape* of what gets built. Ask in that order, highest first.

| Leverage | Examples | Ask? |
|----------|----------|------|
| Changes the architecture | What is deliberately out of scope; who the user actually is; what must never be lost; single- or multi-tenant; sync or async | Always, first |
| Changes a contract | Data model shape, API surface, auth boundary, what a failure returns | Yes, next |
| Changes a dependency | Which vendor, which library | Only if not already settled by the project |
| Changes a detail | Naming, file layout, formatting | No — decide it yourself and mention it |

The test for the top row: if the answer flipped, would work already done have to be thrown away? If yes, it belongs at the top.

-----

## The stopping rule

Stop at the first of these. This is not optional — an interview with no terminus burns the user's patience and produces worse answers as it goes.

1. **Leverage exhausted.** The highest-ranked remaining question would only change an implementation detail. Stop; decide the rest yourself.
2. **Three deferrals in a row.** Three consecutive "I don't know" or "you decide" answers means the user is out of context, not out of opinions. Stop, record the remainder as `@TODO`, and offer to resume after something concrete exists to react to.
3. **Ten questions.** Hard cap per session. If more remain, say how many and ask whether to continue — never continue unasked.
4. **The user stops it.** Immediately, without a closing argument.

-----

## Close with a written summary

Every interview ends with an artifact, not a vibe:

- **Decisions** — one line each, in the user's words where possible.
- **Deferred** — the questions left open, each as a `@TODO` in the document it belongs to.
- **Consequences** — what you will now do differently from what you would have guessed.

Write the decisions into the relevant document (`docs/product-spec.md`, `docs/tech-spec.md`, or the ticket) so the answers outlive the session.

-----

## Boundaries

- An interview never substitutes for a standing ask-first rule, and never re-litigates one. Those questions get asked on their own terms whether or not an interview happened.
- Do not interview about something you can determine yourself. Read the code first; ask about intent, not about facts.
- If the answers reveal the plan is wrong, say so at the end of the interview rather than quietly building the old plan.

-----

## Anti-patterns

- A twenty-question intake form delivered in one message.
- Asking about preferences before asking about constraints.
- Continuing past the point where the user has begun answering in one word.
- Treating the interview as consent: agreement to a question is not approval of a plan.

-----

Technique adapted from "Finding your unknowns," a field guide by Thariq Shihipar of Anthropic (July 2026) — one practitioner's documented practice, not a validated method. The specific rules above are this project's.
````

-----

### 3. `implementation-notes`

Path: `.claude/skills/implementation-notes/SKILL.md`

````markdown
---
name: implementation-notes
description: "Keeps an implementation-notes.md working file during a build, recording decisions and — under a Deviations heading — every place where reality forced a departure from the plan. Use when starting implementation from a spec, plan, or ticket; on any session long enough that decisions will be forgotten; or when the user asks for implementation notes or a deviation log. Defines the conservative-default rule: when the plan and the codebase disagree, take the most reversible option, log it, and keep going rather than stopping to ask."
---

# Implementation Notes

No plan survives contact with the codebase. The notes file is where the departures get recorded while they are still fresh, so the next attempt starts from what was learned instead of from the plan that was wrong.

Create `implementation-notes.md` at the start of the work and keep it current as you go — not reconstructed at the end.

-----

## The file

Working artifact, not a deliverable. Put it at the repo root or beside the plan it tracks, and treat it as temporary.

```markdown
# Implementation Notes — [feature]

Plan: [path to the spec, plan, or ticket this implements]
Started: [date]

## Decisions
- [what was chosen, and the reason, one line each]

## Deviations
- [see the entry format below]

## Open Questions
- [things to raise with the user, not blocking]

## Discarded
- [approaches tried and abandoned, and why — this is the most valuable section on the second attempt]
```

-----

## The conservative-default rule

When the plan and the codebase disagree, do not stop and wait. Choose, log, and continue.

Conservative means, in order:

1. **Most reversible** — the option that is cheapest to undo next week.
2. **Narrowest blast radius** — touches the fewest callers, tables, and contracts.
3. **Preserves existing behaviour** — when in doubt, keep what is already true for existing users.
4. **Most visible** — the option whose wrongness would show up in a test or a log rather than silently.

Then log it. A deviation entry is not a diary line; it is a decision record:

```markdown
### [Short name of the deviation]
- **Plan said:** [what the plan assumed]
- **Found:** [what is actually true, with file:line or test name]
- **Chose:** [the conservative option taken]
- **Cost if wrong:** [what breaks, and how it would surface]
- **Would change my mind:** [the fact that would flip this decision]
```

The last line is the important one. It turns a deviation into a question the user can answer in ten seconds.

-----

## When to stop instead

The conservative default applies to implementation choices. Stop and ask when the deviation is not one of those:

- Anything destructive or irreversible — data loss, a down-migration that cannot be undone, deleting a user's content.
- Any change to an authorisation boundary, a secret, or what a given user can see.
- Anything that would require answering a standing ask-first question on the user's behalf.
- A discovery that invalidates the premise of the spec rather than a detail of it.
- A cost commitment — a new paid dependency, a new vendor, a new service.

Stopping is cheap in these five cases and expensive in all the others. Keep the list short and honour it.

-----

## Close the loop

The notes file exists to feed something back. At the end of the work, walk the Deviations section with the user, and give every entry a destination:

| Outcome | Where it goes |
|---------|---------------|
| Changes what the product should be | Back into `docs/product-spec.md` |
| Changes the technical approach | Back into `docs/tech-spec.md`, or a new ADR |
| Is work that still needs doing | A tracker issue |
| Was a one-off, now settled | Nothing — it dies with the file |

A deviation is a signal, not a defect. If a document and a discovery disagree, the discovery is the newer evidence — update the document rather than filing the discovery away.

Once every entry has a destination, delete or archive the notes file. It is scaffolding.

-----

## Anti-patterns

- Writing the notes at the end from memory. The entries that matter are the ones you would no longer remember.
- Logging everything. Notes that record routine work are not read; keep them to decisions, deviations, and dead ends.
- Deviating silently because the change seemed small. Small changes to a contract are the expensive ones.
- Stopping on every ambiguity. Constant escalation is as unhelpful as silent drift.
- Letting the notes file contradict the docs and leaving it that way. Resolve it in one direction or the other before the work is called done.

-----

Technique adapted from "Finding your unknowns," a field guide by Thariq Shihipar of Anthropic (July 2026) — one practitioner's documented practice, not a validated method. The specific rules above are this project's.
````

-----

### 4. `change-quiz`

Path: `.claude/skills/change-quiz/SKILL.md`

````markdown
---
name: change-quiz
description: "Produces a report explaining a completed change — context, intuition, what actually happened, what could break — ending in a quiz the reviewer answers. Use after a long working session, before merging a change you did not write line by line, when handing work to someone else, or when the user says 'quiz me', 'explain this change', or 'I want to understand what you did'. Advisory by default; a project can make a passing quiz a merge gate with a single line."
---

# Change Quiz

A diff shows what changed. It does not show what is now true. After a long session, reading the diff gives a reviewer the illusion of understanding while the actual behaviour lives in code paths the diff never touched.

This skill produces a report that explains the change, and a quiz that proves the explanation landed.

-----

## The report

Write it for someone who was not in the session. Order it so understanding accumulates.

| Section | Contents |
|---------|----------|
| What this change is for | The problem, in one paragraph, before any code |
| How it works now | The mental model — how a request or a record flows through the system after this change |
| What changed | The diff, grouped by intent rather than by file |
| What the diff does not show | Existing code paths this now depends on, defaults it inherits, behaviour it changes at a distance. The most important section |
| What could break | Concrete failure modes, and the signal that would surface each |
| What was deliberately not done | Scope consciously left out, with the reason |
| Open items | Anything still `@TODO`, and any Deviations not yet folded back into the docs |

Cite locators. Every claim about behaviour points at a file and line, a test name, or a log line.

Markdown by default. A single self-contained HTML file is fine when the reader wants to read it in a browser. Either way the report is a review artifact — it is not shipped code and does not live in `src/`.

-----

## The quiz

Five to eight questions, at the bottom, with the answers in a separate section below them so the reader answers first.

Every quiz must include at least one of each:

- **A behaviour not visible in the diff.** "After this change, what happens to an existing record that has no value in the new column?"
- **A failure mode.** "If the third-party call times out mid-transaction, what does the user see, and what is left in the database?"
- **An applied question.** "You now need to add a second provider. Which file do you touch first, and what would you have to change that this design made harder?"

Prefer questions with a specific right answer. Avoid anything answerable by re-reading the diff, and anything answerable "it depends".

-----

## Advisory by default

The quiz informs the merge decision; it does not make it. Report which questions were missed and what to re-read, then leave the decision to the human. Do not block, do not gate, and do not grade yourself on the reviewer's behalf.

**To make it blocking**, a project adds this line to its `CLAUDE.md` under the merge or definition-of-done rules — and, so it is enforced at the point of use, to the "Definition of Done" section of `dev-standards`:

```text
Merging requires a passing change quiz: run the change-quiz skill and answer every question correctly before the change is merged.
```

That single line is the whole switch. Nothing in this skill changes; the project's own rules decide whether the quiz is a gate.

-----

## Anti-patterns

- A quiz whose answers are all visible in the diff. It tests reading, not understanding.
- Grading the reviewer's answers charitably. A near-miss on a failure-mode question is a miss.
- Writing the report as a changelog. A list of files changed is not an explanation.
- Producing the report for a two-line change. Use this when the session was long enough that the reviewer genuinely cannot hold it all.

-----

Technique adapted from "Finding your unknowns," a field guide by Thariq Shihipar of Anthropic (July 2026) — one practitioner's documented practice, not a validated method. The specific rules above are this project's.
````

-----

## Part 2: Four Techniques Folded Into Existing Skills

These four do not become skills. Each is a section inserted into a baseline skill that already owns the subject.

| Technique | Target skill | Insertion point | "Covers" cell gains |
|-----------|--------------|-----------------|---------------------|
| Brainstorms and prototypes | `architecture-planning` | After the pre-development checklist, before ADRs | "brainstorming and throwaway prototypes" |
| References | `dev-standards` | After the dev workflow, before the definition of done | "using source code as a reference" |
| Implementation plans | `architecture-planning` | Immediately after the brainstorms and prototypes section | "implementation plans ordered by what is most likely to change" |
| Pitches and explainers | `dev-standards` | After the definition of done | "packaging a change for review and buy-in" |

-----

### A. Brainstorms and Prototypes — into `architecture-planning`

````markdown
-----

## Brainstorms and Prototypes

Some criteria cannot be written down in advance and can only be recognised on sight. Visual design is the usual example, but so are information density, tone, and how a flow *feels* in sequence. For those, more questions do not help. Something to react to does.

### Brainstorm before you scope

Start work with a spread, not a proposal. Ask for the range — the cheapest intervention through the most ambitious — and let the user cut it down. A spread prevents both errors at once: a scope drawn too narrow to solve the problem, and one drawn too wide to finish.

### Prototype to provoke a reaction

When the open question is one the user will answer by looking:

- Produce **several genuinely different directions**, not one idea with the spacing changed. Three to five, each committing to a different premise.
- Keep them **disposable**: one self-contained file, fake data, no backend, no state, no auth, no tests.
- Put them somewhere clearly non-production — `prototypes/`, or a scratch directory outside `src/`. Nothing in the application imports them.
- Present them together and ask which parts land. Expect the answer to be a mixture; that is the point.
- **Record the decision, discard the artifact.** The prototype's only job is to produce a decision. Write the decision into the spec; delete the file.

### Production-first still holds — for production

A prototype is a question, not an implementation. The production bar — typed, tested, error-handled, secure — applies to code that ships. It does not apply to a mock built to be looked at once and thrown away. Do not launder a prototype into the codebase: if a direction is chosen, the real implementation is written properly, from the decision, not by hardening the mock.

### A prototype is not a framework commitment

This is a hard boundary and it has been read wrong before.

Building a throwaway mock does **not** answer the standing question of which frontend framework the project uses, and must never be treated as having answered it. Ask which framework — Astro + React or Next.js — before writing any real frontend code, even when a prototype already exists, even when the user liked it, and even when the prototype happens to be written in something that resembles one of the options. A single HTML file expresses a layout, not an architecture.

The same holds for the other standing ask-first rules. In particular, do not write end-to-end tests for a prototype at all: it is being deleted, and the Playwright ask-first rule is not satisfied by a flow that was never real.
````

-----

### B. References — into `dev-standards`

````markdown
-----

## References: Point at Source Code

Some things are faster to show than to describe. When a behaviour is intricate — a retry policy, a state machine, a layout, a permissions model — writing the specification costs more than pointing at something that already does it.

The strongest reference is **source code**. A screenshot shows an outcome; source shows the structure that produced it, the edge cases the author hit, and the names they chose. Prefer, in order:

| Reference | Carries |
|-----------|---------|
| Source code | Structure, edge cases, naming, the decisions behind them |
| A test suite | The contract, and the failure modes someone already found |
| Documentation | Intent, without the details that matter at implementation time |
| A screenshot or recording | The outcome only |

Language does not matter. An implementation in Rust, Go, or Ruby is a perfectly good reference for TypeScript work — read it for the semantics and reimplement them idiomatically here. Do not transliterate.

When using a reference:

- Say **what to take from it**. "The backoff and jitter behaviour, not the error types" is a usable instruction; "make it like this" is not.
- Read the reference before citing it. A reference asserted from memory is a guess wearing a citation.
- Name what deliberately differs here, and why. The gap between the reference and this codebase is where the bugs live.
- Check the licence before copying anything verbatim. Reimplementing semantics is not the same as copying source.

Good places to look first: a vendored dependency already in this repo, an earlier feature in this codebase that solved the same shape of problem, or the upstream library whose behaviour is being matched.
````

-----

### C. Implementation Plans — into `architecture-planning`

````markdown
-----

## Implementation Plans: Decisions First

A plan gets a short skim, not a close read. Order it so the skim lands on the parts a reviewer can actually change.

Lead with the decisions most likely to be wrong or contested:

1. **Data model changes** — new tables, new columns, anything that alters what is stored or what becomes hard to undo.
2. **Type and interface changes** — the contracts other code will be written against.
3. **Anything user-facing** — flows, states, copy, what happens on error.
4. **Anything irreversible** — migrations, deletions, external side effects, vendor commitments.

Then, and only then, the mechanical work: refactors, file moves, renames, test scaffolding. It goes at the bottom, summarised. Nobody needs to review a rename in detail, and burying the data model beneath one is how plans get approved unread.

For each decision in the top half, give:

- The choice, stated plainly.
- The alternative that was rejected, and why.
- What it would cost to reverse this later. This is the number that tells a reviewer how hard to think.

Mark unresolved items `@TODO` in the plan itself, and say which ones block the start of work versus which can be settled during it.

Write the plan as a document the user can react to and mark up. When the user's feedback changes a decision, change the plan before starting — a plan revised in five minutes is cheaper than an implementation revised in five hours.
````

-----

### D. Pitches and Explainers — into `dev-standards`

````markdown
-----

## Pitches and Explainers

Shipping usually ends with a person who was not there deciding whether this is good. That person starts with the unknowns you started with, minus the weeks you spent resolving them. Packaging the work is part of the work.

When a change needs buy-in, an approval, or a handover, assemble one document from what already exists:

| Source | What it contributes |
|--------|---------------------|
| The prototype or a recording | The demo — what it looks like and does |
| The spec | What was decided, and what was ruled out |
| The implementation notes | Deviations, and what was learned building it |
| The tests | Evidence the claims hold |

Lead with the demonstration. A reviewer who can see the thing working reads everything that follows more generously and more accurately.

Then, in order: the problem in one paragraph; what was built; the decisions a reviewer might have made differently, with the reasoning; the failure modes anticipated and how each is handled; what is deliberately not covered; and what is being asked for — approval, feedback, or a decision on a named open question.

Two rules that decide whether it works:

- **Address the expert's objections before they raise them.** Someone senior in this domain arrives with a standing set of objections. Answer them in the document. Nothing accelerates approval like visible evidence that the known failure modes were already considered.
- **Never overstate.** Every claim carries its locator, and every open item is listed as open. A pitch that hides an unknown gets one approval and costs all the trust afterwards.

Keep it one document, self-contained, readable in five minutes.
````

-----

### Register Update: `architecture-planning` Joins Both Ask-First Sites

Not a fifth technique — a bookkeeping consequence of section A, and it has to be executed or the register silently stops matching what the pipeline generates.

`docs/prompts/skills-builder.md:119-124` is the canonical statement of which skill carries which standing ask-first rule. It names `frontend-development` and `ui-standards` for the frontend-framework rule, and `testing-tdd` for Playwright. Section A restates **both** rules inside `architecture-planning`. Replace the two bullets at `:123-124` with:

- `frontend-development`, `ui-standards`, and `architecture-planning` must instruct the agent to **ask which frontend framework** (Astro + React or Next.js) before writing frontend code, unless the project has already committed to one. In `architecture-planning` the rule is stated for the prototype case: building a throwaway mock never answers the framework question, however much the user liked the mock.
- `testing-tdd` and `architecture-planning` must instruct the agent to **ask what Playwright should test** before writing any E2E test — never auto-generate E2E flows. In `architecture-planning` the rule is stated as a prohibition: a prototype gets no E2E tests at all.

The matching checklist item at `:196` names the same three skills.

The generic ask-first guards elsewhere in this appendix — the Boundaries sections of `blind-spot-pass` and `interviews`, and the "When to stop instead" list in `implementation-notes` — need no register entry. They defer to the standing rules without restating either one, so there is nothing for the register to track.

-----

## Part 3: Deliverable Checklist Additions

Add to the "Deliverable Checklist" in `docs/prompts/skills-builder.md`:

- [ ] The four unknowns skills exist: `blind-spot-pass`, `interviews`, `implementation-notes`, `change-quiz`
- [ ] `blind-spot-pass` triggers on the literal phrases "blind spot pass" and "unknown unknowns", and instructs the agent to establish the user's starting point before investigating
- [ ] `interviews` carries the stopping rule
- [ ] `change-quiz` is advisory, and states the one line that makes it blocking
- [ ] `architecture-planning` carries the brainstorms/prototypes and implementation-plan sections, including the statement that a prototype is not a frontend-framework commitment
- [ ] `dev-standards` carries the references and pitches/explainers sections
- [ ] Both baseline enumerations say fourteen: the table in `docs/prompts/skills-builder.md`, and the mirrored table at `grovv-stack-scaffold.md:329-340`, its tree at `:111-120`, and its expected-output count at `:376`
- [ ] The ask-first register at `docs/prompts/skills-builder.md:119-124`, and its checklist item at `:196`, name `architecture-planning` alongside the skills already listed

-----

## Attribution

The eight techniques specified here are drawn from "A field guide to Claude Fable 5: Finding your unknowns" by Thariq Shihipar, member of technical staff at Anthropic, published on the Claude blog on 6 July 2026. The framing — known knowns, known unknowns, unknown knowns, unknown unknowns, and the practice of surfacing them before, during, and after implementation — is his.

**What kind of source this is.** A single practitioner's first-person practice narrative, written in the register of "I've found that" and "I like to use." It carries no measurements, no comparison against a baseline workflow, and one self-reported worked example. The rules derived from it here are this repository's design choices, not validated method, and the Deliverable Checklist in Part 3 is a conformance check against those choices rather than against any Anthropic standard. The split is itemised below.

**What is adapted, and what is not.** Adapted directly from the article's example prompts and phrasing:

| Here | From the article |
|------|------------------|
| The `interviews` frontmatter description — one question at a time, prioritised by whether the answer would change the architecture | Its interview example prompt, near-verbatim |
| The `implementation-notes` frontmatter description, and the Deviations heading it names | Its three-part deviation discipline: take the conservative option, log it under "Deviations," keep going |
| The implementation-plan ordering in Part 2C — data model, then types and interfaces, then anything user-facing, with mechanical refactoring at the bottom | Its implementation-plan prompt, the same items in the same order |
| The reference example in Part 2B — an implementation in another language read for its semantics and reimplemented rather than transliterated | Its own reference example |
| The pitch assembly list in Part 2D — prototype, spec, implementation notes, and tests into one document, leading with the demo | Its pitch prompt |
| "context, intuition" in the `change-quiz` frontmatter description | Its quiz prompt |

Original to this appendix: the stopping rule, the conservative-default ordering, the leverage ranking, the report and quiz structures, the boundaries, every anti-pattern section, and the assembly of the four-quadrant table above — whose definitions are the article's but whose technique mapping is this repository's.

This is credit, not a licence obligation; the attribution line in each skill body is the whole requirement, and it should survive edits.

-----

## Open Items

- @TODO Confirm the four new skills are generated for every project, or gated. `change-quiz` and `implementation-notes` earn their place on any project; `blind-spot-pass` and `interviews` are most valuable on unfamiliar or ambiguous work. Current proposal: generate all four by default, consistent with the rest of the baseline set.
- @TODO Decide whether the four new skills also need `references/` directories. As written, every body is well under 500 lines and needs none.

-----

## Colophon

| Field | Value |
|-------|-------|
| Version | 1.1.0 |
| Last Updated | 2026-07-26 |
| Status | Proposed — not applied |
| Author(s) | grovv-stack unknowns workstream |
| Model | Claude Opus 5 |

-----
gro\\/\\/ stack — Unknowns Skill Bodies (Specification Appendix)
