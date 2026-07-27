# Unknowns Engineering for the gro\\/\\/ stack Pipeline

An assessment of the finding-your-unknowns field guide and a scoped plan for absorbing it into the scaffolding pipeline.

**Status, 2026-07-27: the substance landed; the renumber was declined.** The Unknowns Pass is implemented as the opening phase of Step 2, before the product spec is written, rather than as a new numbered Step 2 that pushes Steps 2 through 9 to 3 through 10. The starting-point questions, the blind spot pass, the one-question-at-a-time interview, the prototype limb, the stopping rules, the escape hatch, and `docs/unknowns.md` with its four named consumers are all in `grovv-stack-scaffold.md`. Step 1 creates the file; Step 2 fills it; Steps 4 and 8 read it. `grovv-stack-scaffold.md:346`'s "(if not already clear)" hedge — contradiction 3, the note's sharpest single finding — is gone, replaced by an instruction to state each default and ask.

Three things drove declining the number, and none of them is the mechanical cost on its own:

- **Two of the three findings the step existed for were already closed by the Throwaway Tier**, which landed between this note being written and being executed. Contradiction 1 (production-first forbids the disposable artifact) and the standing-ask-first clause the prototype limb needed are both stated there in full. What remained was the discovery work, which is a phase of understanding the product — not a separate artifact-producing step.
- **The position argument survives the fold intact.** This note rejected appending as Step 10 because "a pass after the specs audits documents instead of informing them." Being the first half of Step 2 is upstream of the product spec, which is all the argument ever required. The number was never what bought the position.
- **The map does not survive contact.** Re-run on 2026-07-27 against `HEAD`, this note's own verification grep — same filter, excluding `.git`, the harness trees and `docs/architecture/` — returns **100 lines across 18 files**, against the 62 across 15 recorded here. A 61% growth in the surface, on a map whose own opening paragraph warns that its line numbers have a short shelf life. Outside that filter sit 20 more step tokens in the vendored harness trees, which are that skill's own Korean-language phase numbers (`**Step 1: 현황 감사**`) in Apache-2.0 code a mechanical pass would corrupt. Both traps this note flagged are real and confirmed: there are 13 `Steps 0–9` en-dash ranges and exactly one ASCII-hyphen range, and that one range — `grovv-stack-scaffold.md:622`, "Work through Steps 2-9 sequentially" — is precisely the site where a mechanical +1 on both ends is wrong, because the item before it covers Step 1, so its lower bound means "everything after Step 1."

What is **not** implemented and remains proposed: the agent-definition changes (implementation notes into `testing.md`, the change-comprehension quiz into `code-review.md`, both across four tool trees — Phase 1 of the rollout below), and the four new baseline skills specified in `unknowns-skill-bodies.md` (Phase 3). Both are standalone and neither needs a renumber.

> **Historical note, 2026-07-27.** Everything below this block is preserved as the reasoning record, unedited except where a section says otherwise. Its step numbers, line citations, and counts are a snapshot of a working tree that has since moved — `grovv-stack-scaffold.md` and `docs/prompts/` are the source of truth for what the pipeline does now. Re-derive any locator here before acting on it, and read the renumbering section as a rejected option rather than a plan.

This file is the architecture note of record for the decision. Part One is a fidelity pass over the source. Part Two is the plan. This round produces a decision document, not applied edits: every change below is specified precisely enough for a later session to apply, and no pipeline file is touched by this workstream. Every repository count in Part Two was re-derived by grep against this repository on the date in the colophon and is cited with the command or paths that produced it. Where re-derivation contradicted a number this note was handed, the note states the contradiction and keeps the derived figure.

**Baseline for every line number below.** The map is derived against the working tree as of the colophon date — that is, with the `docs/prompts/linear-tracking.md` → `docs/prompts/tracker-setup.md` rename applied. That rename is staged but not yet committed, so the same grep run against `HEAD` returns different figures: 16 files rather than 15, `grovv-stack-scaffold.md` at 576 lines rather than 578, and four `MEMORY.md` step-token lines rather than five. Line numbers are therefore load-bearing on a baseline that has not landed. A later session must re-run the verification grep in the renumbering section, confirm it matches this map, and reconcile any difference **before** applying anything — not apply the map blind and reconcile after.

This is not a hypothetical caution. The four mirrored `agents/scaffold.md` ordinal lists were re-indexed by concurrent work in this repository while this note's map was being derived, which moved content under a locator the map had already recorded. Any line number in an unmerged working tree is a claim with a short shelf life; treat every one below as needing confirmation rather than trust.

Source document: "A field guide to Claude Fable 5: Finding your unknowns," by Thariq Shihipar, member of technical staff, Anthropic, published 6 July 2026. It is a first-person practice essay about working with Claude Code, not a study. Its instruction text is paraphrased throughout this note and never copied verbatim into any artifact this plan generates; the techniques are credited to the article by name.

-----

## Summary

### The field guide in about 200 words

The essay opens on the map and the territory. The map is what you give the agent — prompts, skills, context. The territory is where the work actually happens: the codebase, the real world, its constraints. The gap between them is what the author calls an unknown, and an unknown is defined operationally: the moment the agent has to decide something on its best guess of what you wanted. More work per turn means more of those moments.

The claim about the model is narrow and specific. On Fable, the author finds the ceiling on output quality is no longer the model's capability but his own ability to clarify what it does not know.

The conceptual core is a 2x2 over what you know and what you know you know: known knowns, known unknowns, unknown knowns, unknown unknowns. Eight techniques are offered across three phases — five before implementation, one during, two after. The through-line is that each technique is a cheap way to find out something you did not know, before finding it out becomes expensive.

Two warnings frame the technique list. Instructions that are too specific make the agent follow you off a cliff; instructions that are too vague make it substitute industry best practice for your actual problem. Accounting for unknowns is what fixes both, because both are failures of the same missing information.

### The integration recommendation in about 150 words

Adopt in three landing zones, staged, with the pipeline change first.

A new Step 2, the Unknowns Pass, is inserted before the product spec and the existing Steps 2 through 9 renumber to 3 through 10. It has two limbs: a blind spot pass plus a one-question-at-a-time interview, which work the two known-unknown and unknown-unknown quadrants; and a prototype limb, several deliberately disposable HTML directions the user reacts to, which is the only instrument that surfaces unknown knowns. It writes `docs/unknowns.md`, a living document that later steps read and prune rather than consume.

The implementation-notes and merge-quiz conventions fold into the existing testing and code-review agent definitions, unconditionally, with the quiz advisory by default.

Four techniques become baseline skills and four become sections inside two existing skills, taking the baseline set from 10 to 14 rather than to 18.

-----

## Part One: What the Field Guide Says

### Map, territory, and the definition of an unknown

The framing is borrowed from general-semantics usage and applied to agentic coding without ceremony. The map is the representation of the work: the prompt, the skills, the accumulated context. The territory is the place the work lands: the actual codebase, the actual product, the actual constraint that nobody wrote down.

The definition that does the work in the rest of the essay is not "something you do not know." It is **the moment the agent must decide based on its best guess of what you want**. That relocation matters. It makes unknowns countable in principle — they are decision points, not topics — and it makes the count scale with the size of the task, which is the essay's explanation for why the problem got worse as models got better. A model that does more per turn encounters more of those moments per turn.

The essay's strongest structural claim follows from this and is stated early: planning ahead is not sufficient. Unknowns are found deep in implementation, and some of them do not resolve into an answer at all — they resolve into the discovery that the problem should have been approached a different way. Discovery is therefore an iterative process running before, during, and after implementation, which is why the technique list has three phases rather than one.

### The 2x2

This is the essay's central conceptual contribution and the part with the most leverage for a spec-generating pipeline.

| Quadrant | Definition | Where it lives |
|----------|-----------|----------------|
| Known knowns | What you tell the agent you want. Effectively, your prompt | Already in the map |
| Known unknowns | What you have not figured out yet, but are aware you have not | Nameable; you can ask about it |
| Unknown knowns | So obvious you would never write it down — but you would recognize it instantly if you saw it | Not nameable; only recognizable |
| Unknown unknowns | What you have not considered at all. Knowledge you do not know exists. Not knowing how good a thing can be | Neither nameable nor recognizable without help |

The essay is precise about unknown knowns and it is the quadrant most often collapsed into the others. It is not ignorance. The information is fully present in the user's head — it is simply below the threshold at which anyone writes anything down. The article's two examples are a button added to a frame — you want to see how it looks without wiring up a backend route or carrying extra frontend state — and visual design. Only the second carries the author's "difficult to articulate, but I know what I want when I see it," and he says it once, of visual design alone.

The operational consequence is the part a pipeline has to internalize. **A question cannot surface an unknown known.** Asking someone what they want, when they only know it on sight, produces either a shrug or a plausible-sounding answer they do not actually hold. The instrument that surfaces this quadrant is an artifact to react to — a prototype, a mock, several directions side by side. That is why the essay reaches for prototypes rather than more questions, and it says so explicitly: identifying and verbalizing unknown knowns early during prototyping is valuable precisely because finding them during implementation is expensive, since small spec changes cause drastically different implementations and agents revert previous work poorly.

### Which technique addresses which quadrant

The essay does not draw this table; the mapping is assembled here from its own descriptions, and where it is an inference rather than the essay's phrasing it is marked.

| Technique | Phase | Primary quadrant | Note |
|-----------|-------|-----------------|------|
| Blind spot pass | Pre | Unknown unknowns | Stated directly — the essay uses the literal phrase "unknown unknowns" |
| Brainstorms and prototypes | Pre | Unknown knowns | Stated directly — introduced as the technique for "an area with a lot of unknown knowns" |
| Interviews | Pre | Known unknowns | Inference. The essay places it after brainstorming, on "any unknowns or ambiguities," and prioritizes questions whose answers change the architecture |
| References | Pre | Unknown knowns | Inference. Used when you cannot describe what you want; source code carries the structure a screenshot loses |
| Implementation plan | Pre | Known unknowns | Inference. It front-loads the decisions most likely to change, which is a request to surface what is still open |
| Implementation notes | During | Unknown unknowns | Stated. The essay's premise is that no amount of planning eliminates them |
| Pitches and explainers | Post | Unknown unknowns, other people's | Inference. The essay names no quadrant here. It says reviewers start with the same unknowns you did and that experts want to see the failure points accounted for; the quadrant is this note's reading |
| Quizzes | Post | Unknown knowns, yours about the diff | Inference. Reading a diff does not tell you what happened; a quiz makes you recognize whether you actually understood it |

Three of the eight target unknown knowns or come close, and all three work by putting something in front of the user to react to rather than by asking a question. Two of the three — brainstorms and prototypes, and quizzes — produce that artifact. The third, references, consumes one the user already has, which is exactly why the essay recommends it: when you cannot describe what you want, you point at something instead. Either way the instrument is an artifact, not a question, and that distribution is the single most important thing in the essay for a system that currently produces only prose specs.

### The too-specific and too-vague pair

The essay's framing of instruction quality is a pair of symmetric failures, not a spectrum with a correct midpoint.

- **Too specific** and the agent follows your instructions even where a pivot would have been better. You have encoded a path and forbidden deviation from it.
- **Too vague** and the agent fills the gap with industry best practice, which may be a poor fit for your actual task.

The connecting claim is the sharp one: when you do not account for your unknowns, you fail *both* ways at once. You do not know which parts of the path are full of obstacles, so you cannot afford to be loose there; and you do not know which parts are clear, so you cannot afford to be rigid there either. Precision and latitude both have to be allocated, and you cannot allocate either without knowing where the unknowns are. Accounting for unknowns is not a third option between specific and vague — it is the input that lets you choose correctly per decision.

### The eight techniques

**Pre-implementation.**

*Blind spot pass.* For entering unfamiliar territory: a new part of the codebase, or a domain you have no vocabulary for. You do not know what questions to ask, what good looks like, what has already been tried, or what to avoid. The essay recommends the literal phrases "blind spot pass" and "unknown unknowns," and stresses that context about who you are and what you already know is what lets Claude choose how to collaborate. Both example prompts end with the same request — help me prompt you better.

*Brainstorms and prototypes.* For unknown knowns. Ask for several wildly different directions and react to them. The canonical example is a single HTML file mocking a UI with fake data, before anything is wired up. The author starts almost every coding session with an exploration phase, and gives a reason that cuts both ways: brainstorming stops him setting scope too narrow *or* too wide, and Claude both finds high-value approaches he would have missed and sometimes misses the forest for the trees.

*Interviews.* After brainstorming, when unknowns remain. One question at a time, with context supplied to guide the questions, and prioritized by whether the answer would change the architecture.

*References.* For when you cannot describe what you want, either because you lack the vocabulary or because describing it would take too long. Diagrams, docs, and pictures all work, but the essay is unambiguous that the best reference is source code — even in a different language — because it carries markup and structure that a screenshot does not.

*Implementation plans.* Ask for a plan, and ask for it ordered by what you are most likely to change: data models, type interfaces, UX flows first; mechanical refactoring last. The point is not the plan, it is surfacing the decisions still worth altering.

**During implementation.**

*Implementation notes.* Start a fresh session, pass in the planning artifacts, and ask the agent to keep a temporary `implementation-notes.md` recording decisions. The recommended discipline for a forced deviation is three-part; the essay's example prompt puts it as "pick the conservative option, log it under 'Deviations', and keep going." The notes exist so the *next* attempt learns from this one.

**Post-implementation.**

*Pitches and explainers.* Package the artifacts into one document that gets buy-in. Two stated benefits: reviewers who start with the unknowns you started with come up to speed faster, and experts approve faster when they can see you accounted for the failure points they would have raised.

*Quizzes.* After a long session, reading the diff gives only a light understanding, because behavior depends on existing code paths the diff does not show. Ask for a report on the change plus a quiz, and — the author's own gate — merge only after passing it perfectly.

### The artifact bias

Worth naming separately, because it is a property of the outputs rather than of the argument, and it is the property most relevant to what this pipeline should generate.

The eight techniques carry eleven example prompts between them, not one each. The requested artifact is an HTML page in four of the eleven: the four design directions, the toolbar mock, the implementation plan, and the change report with the quiz. Two of those four — the design directions and the toolbar mock — sit inside brainstorms and prototypes, so the HTML bias concentrates in three techniques rather than spreading across four. Implementation notes are offered as Markdown *or* HTML. The reference technique points at source code the user already has. Three techniques produce no artifact at all: the interview, the blind spot pass (whose two prompts ask Claude to explain and to teach), and references.

The bias is toward things you look at and react to, not things you read and approve. A spec is read; a mock is reacted to. Since the quadrant that matters most is the one that only responds to recognition, the medium is not incidental — the essay's method depends on producing artifacts that trigger recognition, and prose does not reliably do that.

### The worked example, and what it demonstrates

The launch video for Fable, edited end-to-end with Claude Code, in a domain the author states plainly he is not expert in. Three moves, in order:

1. Started from a known known — Claude can edit and transcribe video with code — and immediately tested the adjacent known unknown by asking how transcription works and whether ums and pauses could be cut accurately with ffmpeg.
2. Prototyped a Remotion-plus-transcription video to find out whether word-timed UI was possible at all, rather than assuming.
3. Hit a wall on color grading. The first instinct was the prototype technique — generate variations and pick — and it failed, because he could not tell which variation was good. Recognizing that, he switched to the blind spot pass and asked to be taught the domain instead.

The third move is the most instructive part of the essay, and it is under-drawn in the text. It demonstrates that the techniques are not interchangeable and that picking the wrong one is itself detectable: prototypes only work when you can recognize the answer, and when recognition fails you need the teaching technique instead. That is a diagnostic, and the essay does not generalize it.

### What the field guide does not establish

Recorded plainly, because these limits shape how much weight Part Two can put on it.

| Gap | Detail |
|-----|--------|
| Evidence class | A first-person practice narrative by one engineer. No study, no control, no comparison against a baseline workflow |
| Measurement | Zero numbers of any kind. No time saved, no defect rate, no rework avoided, no cost per technique. Every claim of value is qualitative |
| Sample | n=1 on the only end-to-end worked example (the launch video), self-reported by the person who performed it and who works on the product |
| Practitioner claims | "The best agentic coders have relatively few unknowns" rests on watching two named colleagues. It is an observation about two people, offered as a characterization of expertise |
| Quadrant-to-technique mapping | Asserted for three techniques and inferred for five (marked above). The three asserted are the ones where the essay uses the quadrant term literally — blind spot pass, brainstorms and prototypes, implementation notes. No test that a given technique surfaces its claimed quadrant more than another would |
| The 2x2 itself | A well-worn framing with a long lineage — Johari-window and Rumsfeld usage — presented without attribution. Fine for an essay; it means the categories are illustrative rather than operationally defined, and two people may sort the same item differently |
| No stopping rule | The essay never says when you have found enough unknowns, or how to tell a productive pass from an indefinite one. This is the gap that a pipeline step must fill itself, and Part Two fills it explicitly |
| No cost accounting | "Cheap" is asserted throughout and never quantified. A blind spot pass plus an interview plus four prototype directions is a real number of turns and tokens, unstated |
| Failure modes | No discussion of what goes wrong. Prototype fixation, interview fatigue, and notes nobody reads are all obvious risks and none are named |

None of this makes the essay wrong. The techniques are individually cheap, individually reversible, and internally coherent, which is a much lower evidentiary bar than an architectural claim needs to clear. It does mean this note treats the field guide as a well-argued practice, adopts its structure, and supplies the stopping rule, the cost bound, and the failure modes it omits.

-----

## Part Two: What This Means for gro\\/\\/ stack

### The strongest finding: grovv's defaults are the too-vague failure, industrialized

The sharpest available argument is this. The essay's too-vague failure is defined as the agent substituting industry best practice for a fit to your actual task. grovv does not merely risk that failure — it is architected to produce it, and then to propagate it through four derived layers before anyone can see it.

The evidence is a hedge read against its own answer. `grovv-stack-scaffold.md:274` asks about the technology stack "(if not already clear)". It is always already clear: the answer is fixed in six places — `grovv-stack-scaffold.md:447-466` (a 13-row vendor table), `CLAUDE.md:44-60`, `.grovv/CLAUDE.md:35-48`, `.claude/agents/scaffold.md:52-63`, `docs/prompts/skills-builder.md:114`, and `docs/prompts/tech-spec.md:102-155`. So vagueness never surfaces as a question. It resolves silently to Clerk, Neon or Supabase, Stripe, Lago, PostHog, Vercel. Then it hardens: the skills-builder step writes ten skills against that stack (`docs/prompts/skills-builder.md:62-73`, ten rows verified), team-design designs agents against those skills, and the tracking step seeds a live external backlog from it. By the time a misfit is discovered, it is embedded four layers deep.

The same shape appears at its most acute on visual design. `docs/prompts/skills-builder.md:67` bakes the answer into a generated skill — Alexandria, monochrome, white background, no animations — and the same fixed list appears at `CLAUDE.md:174-179` and `.claude/agents/frontend.md:68-73`. Visual design is the essay's canonical unknown known: the thing you can only recognize on sight. grovv settles it by decree, in multiple files, before the user has spoken. Meanwhile the *answerable* question, Astro or Next.js, is one of only two hard stops in the entire system (`.claude/agents/frontend.md:11-18`, "Do not proceed until the user has chosen"). The guardrails are on the cheap decision and absent from the expensive one.

And grovv has no vocabulary for the instrument that would fix it. A grep for the entire prototype vocabulary — prototype, mockup, brainstorm, throwaway, disposable, proof-of-concept — across all Markdown outside `.git`, the vendored harness trees, and `docs/architecture/` returns exactly four lines, all in one file: `docs/prompts/tech-spec-template.md:130`, `:131`, `:199-200`, and `:415`. Every one is a *consumption* slot. The template asks the user to supply wireframes, mockups, and spike results that no step of the pipeline ever produces. grovv's own instruction surface contains none of these words.

**Where the argument does not apply, stated honestly.** Three limits, and the third is the largest.

First, grovv's defaults are not arbitrary industry best practice — they are a deliberately chosen, internally consistent house stack, and the repository says so at `CLAUDE.md:42` ("Stack-agnostic scaffolding, optimized for this default stack. Adapt per project."). A curated default that the document admits is a default is a materially weaker version of the failure the essay describes. The problem is not that the default exists; it is that the mechanism to override it was never built.

Second, grovv already has real verification discipline. `.claude/agents/code-review.md:70-76` requires every factual claim in a review to cite a checkable locator, requires that the locator was opened before the claim was made, and requires unverified claims to be escalated rather than asserted. That is stronger than most repositories manage. The defect is placement, not absence: the standard governs the last mile of a plan whose foundational claims — Target Users, Success Metrics, Constraints in the product-spec template at `grovv-stack-scaffold.md:215-243` — require no grounding at all.

Third, and this is the honest limit on the whole argument: the essay supplies no measurement, so the claim that grovv's defaults cost projects real quality is a reasoned inference and not a demonstrated one. It is entirely possible that for the median grovv project the house stack is correct and the pass costs more turns than it saves. This note therefore demotes the argument from "grovv produces bad output" to the narrower and defensible "grovv cannot detect when it has, and has no cheap instrument that would." The plan below is sized to that narrower claim: one step, one document, four skills, and no change to any default.

### The contradiction ledger

Twelve conflicts were identified against the repository. Ranked by whether the plan below closes them.

| # | Conflict | Anchor | Severity | Closed by |
|---|----------|--------|----------|-----------|
| 1 | Production-first forbids the disposable artifact the essay depends on | `grovv-stack-scaffold.md:532`, `docs/prompts/skills-builder.md:99` | Direct | Step 2 prototype limb, with an explicit exemption clause |
| 2 | Visual design pre-decided in five files; the unknown known settled by decree | `docs/prompts/skills-builder.md:67`, `CLAUDE.md:174-179` | Direct | Step 2 prototype limb (visual direction case) |
| 3 | Vagueness resolves to a fixed vendor list instead of to a question | `grovv-stack-scaffold.md:274` vs six copies of the answer | Direct | Step 2 interview limb, stack question promoted |
| 4 | `MEMORY.md` must yield to `docs/`; deviations are a defect, not a signal | `docs/prompts/tracker-setup.md:276` | Direct | Implementation-notes convention plus the `docs/unknowns.md` back-flow rule |
| 5 | Thirteen intake questions, none about the user | `grovv-stack-scaffold.md:70-76` (7) and `:80-85` (6) | Gap | Step 2 starting-point questions |
| 6 | Nothing in the pipeline renders anything to react to | `grovv-stack-scaffold.md:213` onward | Gap | Step 2 prototype limb |
| 7 | The one forced default-question in the repo guards a tool choice at Step 8; no product-level default gets the same treatment | `docs/prompts/tracker-setup.md:28-38` | Gap | Reused as the pattern for the Step 2 gate |
| 8 | `@TODO` is a marker, not a loop; no step re-reads Open Questions | `docs/prompts/tech-spec.md:96` | Tension | `docs/unknowns.md` lifecycle, with named consumers |
| 9 | Two hard stops, both tool selection; every product question is soft | `.claude/agents/frontend.md:11`, `.claude/agents/testing.md:43-54` | Tension | Step 2's stop condition, which is a real gate |
| 10 | Fifteen success criteria, all certifying existence or style | `grovv-stack-scaffold.md:561-575` (15 verified) | Tension | Two new criteria items; partial — see Open Questions |
| 11 | Evidentiary standard inverted: locators for review claims, nothing for product claims | `.claude/agents/code-review.md:70-76` vs `grovv-stack-scaffold.md:215-243` | Tension | Partial. Step 2 records provenance for unknowns; the spec template is untouched |
| 12 | Adopt mode reads the codebase but never helps the user find their own blind spots in it | `grovv-stack-scaffold.md:211` | Tension | Step 2 adopt-mode limb |

### The new Step 2: Unknowns Pass

Inserted between Step 1 (Create Structure and Configuration) and the current Step 2 (Product Spec). Driven by a new prompt document, `docs/prompts/unknowns-pass.md`.

**Position.** Before the product spec, because everything downstream traces back to it — the directive says so at `grovv-stack-scaffold.md:200`. A pass that runs after the spec is auditing a document instead of informing one. Appending it at the end, which would avoid the renumber, is not available: the entire value is upstream of the first artifact.

**What it reads.** New-project mode: the Conversation First intake answers only. There is nothing else. Adopt mode: the Step 0 assessment output — the codebase scan, the identified stack, the catalogued patterns, the existing docs, the mapped gaps — plus the approved adoption plan.

**What it asks first, and this is the part grovv has never asked.** Four questions about the person, not the artifact. They are cheap, they are asked once, and they calibrate everything after.

1. Have you built this kind of thing before? If so, what did you learn that you would not want to repeat?
2. How well do you know this codebase or this domain — intimately, partially, or not at all?
3. Where are you in your own thinking: exploring what to build, deciding between approaches, or executing a decision you have already made?
4. What is the part of this you are least sure about?

The last question is the interview seed. The first three set whether the pass should teach, challenge, or execute, which is exactly the calibration the essay says context about your starting point buys you.

**Limb A — blind spot pass and interview.** Targets unknown unknowns and known unknowns.

The blind spot pass is a research turn, not a question turn. In new-project mode it searches for what is known about the problem domain, what the common failure modes are, what "good" looks like in this category, and what the user has not mentioned that projects of this shape usually need. In adopt mode it has a real codebase to work against, which makes it materially stronger: it reports what the code does that the user has not described, where the conventions are inconsistent, which subsystems are load-bearing and undocumented, and what a newcomer to this repository would get wrong. It ends by naming what it believes the user's blind spots are, in the user's own domain vocabulary, and asking whether that list is right.

The interview follows: one question at a time, never batched, prioritized by whether the answer would change the architecture. The stack question moves here and stops being conditional. Instead of `grovv-stack-scaffold.md:274`'s "(if not already clear)", the pass states the gro\\/\\/ stack default explicitly, names the two or three places it is most likely to be wrong for this project, and asks. Stating a default and asking for confirmation is not the same as inferring one, and the repository already knows the difference: `docs/prompts/tracker-setup.md:28-38` says it exactly right — a stated default is still an answer they gave. That rule is reused here. What is new is where it applies: today it guards a tool choice at Step 8, and no product-level default is guarded at all.

**Limb B — prototypes.** Targets unknown knowns. This is the limb without which the step is just a longer intake form.

Before the product spec is written, the pass produces artifacts the user reacts to. Not one artifact — several deliberately different directions, side by side, in a single self-contained HTML file with fake data and nothing wired up. What varies depends on what the project is: for a product with a UI, three or four visual and layout directions, including at least one that departs from the monochrome default so the default becomes a choice rather than an inheritance; for a data or API product, three shapes of the core object or the core response; for a tool, three interaction models. The user reacts. The reactions go into `docs/unknowns.md` as recognized constraints, in the user's words.

Two rules make this compatible with production-first rather than in violation of it. First, the artifacts are written to `docs/unknowns/prototypes/` and are explicitly, in their own visible text, not production code — untyped, unwired, unsecured, and disposable by design. Second, nothing generated in this limb may be promoted into the implementation. If a direction is chosen, the chosen properties are written down as spec text and the implementation is built to the production bar from scratch. The exemption is scoped to one directory and one step, and the directive must say so in the same paragraph that introduces the limb, or the next reader will correctly read it as a contradiction of `grovv-stack-scaffold.md:532`.

A third rule belongs in that same paragraph, and its absence is the more dangerous gap. Step 2 runs long before any framework question would naturally arise, and this limb renders UI. `.claude/agents/frontend.md:11-18` requires the framework choice to be put to the user before any frontend code is written and forbids proceeding until they answer. A prototype is not that code and must not be read as having pre-empted that question. The prompt document must therefore state, verbatim in the same paragraph as the disposability exemption: **standing ask-first rules (frontend framework, Playwright) are not pre-empted by any prototype, reaction, or unknowns entry; prototype files are framework-free HTML and are not the framework choice.** The repository already carries exactly this protective sentence for the tracking step at `grovv-stack-scaffold.md:406`, so the pattern is established rather than invented. Without it, a future agent has a plausible reading in which the UI has already been started under an authorization Step 2 never had.

Adopt mode changes the prototype limb rather than skipping it. A working product already exists, so the directions are not greenfield: the pass prototypes the *change* — the new surface, the reworked flow, the shape of the thing being added — against screenshots or component code read from the existing repository, and it matches established patterns per `CLAUDE.md`'s existing-project rule rather than proposing a restyle nobody asked for.

**What it writes.** `docs/unknowns.md`, specified below, plus the prototype files. Nothing else. It does not write the product spec, and it does not pre-empt it.

**When it stops.** The essay supplies no stopping rule, so this is grovv's, and it needs to be conservative because an unknowns pass is exactly the kind of step that can run forever.

- The interview stops after the questions whose answers would change the architecture are exhausted, or after eight questions, whichever comes first. Remaining questions are written to `docs/unknowns.md` as open, not asked.
- The prototype limb runs one round. One set of directions, one round of reactions. A second round happens only if the user asks for it.
- The blind spot pass is one research turn producing one list.
- The whole step ends with an explicit handoff: the pass summarizes what changed in its understanding, names what is still open, and asks for confirmation to proceed to the product spec. This is a real gate — the pipeline's third, and the first one attached to a product-level decision rather than a tool choice.
- Escape hatch, stated in the prompt: a user who says "skip this" gets it skipped, with one line in `docs/unknowns.md` recording that it was skipped and by whose choice. A step that cannot be declined will be worked around rather than declined.

### `docs/unknowns.md`

The artifact that makes the step more than a conversation. It persists as a living document rather than being consumed by the next step.

```markdown
# Unknowns: [Project Name]

> Living document. Updated at Step 2, during implementation, and at review.
> Owned by the scaffolding agent; pruned by whoever closes an entry.

## Starting Point

[The user's own answers: prior experience, familiarity with codebase and domain,
where they are in their thinking. Verbatim where possible — this is calibration
data, not a summary.]

## Blind Spots Identified

| # | Blind spot | How it surfaced | Status |
|---|-----------|-----------------|--------|
| B1 | [What the user did not know they did not know] | [Blind spot pass / interview / reaction] | Open / Closed / Accepted |

## Open Questions

| # | Question | Why it matters | Blocks | Status |
|---|----------|----------------|--------|--------|
| Q1 | [Question, in the user's vocabulary] | [What changes depending on the answer] | [Spec section, or "nothing yet"] | Open / Answered |

## Recognized Constraints

[Unknown knowns surfaced by reaction to a prototype. Record the user's own
words and what they were reacting to. These are the entries a later session
cannot re-derive from any other document.]

| # | Constraint | Surfaced by | Confidence |
|---|-----------|-------------|------------|

## Prototype Directions

| Direction | File | Reaction | Carried into spec |
|-----------|------|----------|-------------------|

## Deviations

[Appended during implementation. What forced a departure from the plan,
which conservative option was taken, and which section above it invalidates.]

| Date | Deviation | Conservative choice made | Invalidates |
|------|-----------|--------------------------|-------------|

## Decided Defaults

[Every place the gro\/\/ stack default was stated and accepted rather than
chosen. One line each. This is the record that makes a wrong default visible
later.]

-----
gro\/\/ stack — Unknowns
```

**Lifecycle and consumers.** The document is written at Step 2 and read at four named points, which is what distinguishes it from the `@TODO` markers at `docs/prompts/tech-spec.md:96` that nothing re-reads.

| When | Who reads it | What they do |
|------|-------------|--------------|
| Step 3, Product Spec | The scaffolding agent | Recognized Constraints become spec text. Open Questions that block a spec section are asked before that section is written, not after |
| Step 5, Technical Specification | The scaffolding agent | Decided Defaults are restated in the tech spec as explicit choices with the reason. Remaining Open Questions seed the tech spec's own Open Questions table |
| During implementation | The testing agent's implementation-notes convention | Deviations are appended here as they are found, with the invalidated section named |
| Step 9, tracking setup | The tracking prompt | Any Open Question still open and still blocking becomes a tracker issue. `MEMORY.md` gets a one-line pointer to this file, not a copy of it |

**Pruning.** Whoever closes an entry deletes it in the same edit, moving anything durable into the spec that now owns it. The Deviations table is the exception: it is append-only within a milestone and cleared when the milestone closes, because its value is the pattern across entries, not any single row. A soft ceiling of 150 lines applies, and the same rule as `MEMORY.md` — history lives in git.

**The back-flow rule, which is the point.** When a Deviation contradicts something in `docs/product-spec.md`, `docs/development-plan.md`, or `docs/tech-spec.md`, the *spec* is what gets revisited. This is a deliberate inversion of `docs/prompts/tracker-setup.md:276` ("it must never contradict `docs/` or the codebase"), which today requires the memory file to yield to `docs/` unconditionally. That rule is correct for `MEMORY.md`, which records session state; it is wrong for a file whose entire purpose is recording that the map was incomplete. The two rules must be stated as distinct, in both files, or the next reader will read one as a bug.

### The renumbering — declined, 2026-07-27

**This section is a rejected option, kept for its map and its traps.** The pass landed inside Step 2 and nothing was renumbered; see the Status block at the top of this file. Two findings here proved out on re-derivation and are worth keeping for whoever next proposes a pipeline insertion: the ASCII-hyphen range — at `:548` when this was written, `:622` at `HEAD` on 2026-07-27 — is real, is the repository's only one against 13 en-dash ranges, and is exactly the site where a mechanical +1 on both ends is wrong; and applying the harness exclusion to the path field rather than the whole line is the only filter that neither drops a real reference nor admits 20 vendored ones. The counts below are stale: the same grep now returns 100 lines across 18 files.

**Verified counts, re-derived.** A literal step-token grep over Markdown, JSON, and YAML, excluding `.git`, every vendored `skills/harness/` tree, and `docs/architecture/`:

```bash
grep -rnE "[Ss]teps? ?[0-9]" --include="*.md" --include="*.json" --include="*.yml" . \
  | awk -F: '$1 !~ /^\.\/\.git\// && $1 !~ /skills\/harness\// && $1 !~ /^\.\/docs\/architecture\//'
```

That returns **62 lines across 15 files**. Of those, **35 change** under an insert-at-2 and **27 do not** — the 27 being references to Step 0 and Step 1, which are unmoved (`grovv-stack-scaffold.md:152`, `:172`, `:211`, `:545`; four lines in each of the four `skills/grovv/SKILL.md` mirrors at `:26`, `:27`, `:32`, `:33`; line `:17` in each of the four `agents/scaffold.md` mirrors), plus file-internal numbering that is not pipeline numbering (`docs/prompts/tracker-setup.md:5`, `:26`, `:312`, which are that prompt's own Step 0).

Add **32 lines that carry no step token at all** — the ordered-list ordinals at lines 29 through 36 in each of the four mirrored `agents/scaffold.md` files. Those lists run 0 through 9 at lines 27 through 36, aligned with the step numbers, so items 2 through 9 shift to 3 through 10 and the eight affected lines per mirror are 29 through 36. Total: **67 edit sites across 15 files**.

**This is two sites more than the map this note was handed, and one file fewer.** The handed map counted 16 files, 34 changing and 28 unchanged, for 66 sites. Both discrepancies trace to the same in-flight rename. The sixteenth file was `docs/prompts/linear-tracking.md`, which no longer exists on disk, taking its `:34` non-changing site with it. And `MEMORY.md` carries **five** step-token lines, not four: `:38`, `:39`, `:51`, `:53`, `:72`. The handed map listed `:52` and `:71`, which are the pre-rename positions; the two dated Decision Log entries that carry "(Step 8)" are `:51` and `:53`, and the third inline reference is `:72`. Losing one non-changing site and gaining one changing site is what moves 34/28 to 35/27 and 66 to 67. The map now reconciles against the working tree; it does not reconcile against `HEAD`.

**One correction to the grep, and it matters.** The obvious exclusion filter, `grep -v "skills/harness/"`, applies to the whole matched line rather than to the path, and it silently drops `grovv-stack-scaffold.md:356` — a real Step 7 reference whose prose happens to mention `` `.claude/skills/harness/` ``. That filter returns 61, not 62. Any prior count of 61 inherits this false negative. The exclusion must be applied to the path field, as above. Conversely, anchoring the exclusion to `.claude/skills/harness/` alone leaves 15 harness lines in from the `.vibe/`, `.grovv/`, and `.codex/` mirrors and returns 77.

**Insertions no step-grep will ever surface.** Five prose pipeline chains (`.claude/skills/grovv/SKILL.md:48`, `.grovv/skills/grovv/SKILL.md:48`, `.vibe/skills/grovv/SKILL.md:50`, `.codex/skills/grovv/SKILL.md:50`, `README.md:99`) each need the new step inserted or they silently disagree with the directive. Four new ordered-list items, one per `agents/scaffold.md`, inserted at position 3 so the lists run 1 to 11. And because the step introduces a prompt document, the prompt set goes from five to six: five Execution Order lists (`CLAUDE.md:118`, `.claude/CLAUDE.md:117`, `.grovv/CLAUDE.md:96`, `VIBE.md:102`, `CODEX.md:92`), three directory trees (`grovv-stack-scaffold.md:103-107`, `.claude/CLAUDE.md:83-88`, `README.md:91`), the File and Folder Reference table at `grovv-stack-scaffold.md:129-146`, and the checklist item at `grovv-stack-scaffold.md:566` that says "all five prompt documents" in words.

**The one place a mechanical +1 is wrong.** `grovv-stack-scaffold.md:548` reads "Work through Steps 2-9 sequentially." The preceding list item covers Step 1, so the lower bound encodes "everything after Step 1," not "old Step 2." It becomes **Steps 2-10**, not 3-10. It is also the only step range in the repository written with an ASCII hyphen; the other eleven ranges all use an en dash, so a `sed` for one form misses the other entirely.

**Why this earns a number when the knowledge-graph note argued a capability must not.** *(The argument below is sound and was still not decisive — see the Status block. PR #10's test asks whether every project should run the step, and the pass passes it. What the argument does not establish is that passing that test requires a **number**: a phase every project runs is equally well expressed as the opening of a step every project runs, and Step 2 already was one. The number would have bought visibility in the directive's step list, and cost 100 step-token sites across 18 files — plus the 32 untokened ordinals this note found, and the risk of a half-applied renumber. The `#### Before writing: the unknowns pass` heading inside Step 2 buys most of the visibility for none of the cost.)*

The prior architecture note in this repository (PR #10, `docs/architecture/knowledge-graph-engineering.md`) rejected a numbered pipeline step for the knowledge-graph capability, and its reasoning was not about cost. It was semantic: `grovv-stack-scaffold.md` is read end-to-end before any file is written, on every invocation, for every project, so a number is a promise that the step runs. Giving a default-off capability a number would tell every future agent that a knowledge graph is part of the expected shape of a grovv project — which is exactly what the gate existed to prevent. It also observed, correctly, that the mechanical cost was a supporting argument only.

That reasoning is right and this note does not overturn it. It satisfies it. **The test PR #10 established is whether every project should run the step**, and the two capabilities land on opposite sides of it:

| | Knowledge graph | Unknowns pass |
|---|---|---|
| Should every project run it? | No. PR #10's own gate resolves to "no corpus, stop" for the majority | Yes. Every project has a user, and every user has unknowns. There is no project for which the answer is structurally "none" |
| What does a number promise? | That a graph is part of a grovv project's expected shape — false | That the pipeline pauses to find out what it does not know before generating — true, and the promise is the point |
| Correct default | Off, gated, invisible when it does not apply | On, with an explicit escape hatch |
| Correct home | A conditional branch inside an existing step | A step |

The reading generalizes: a number is the right container for a phase every project runs and the wrong container for a capability most decline. PR #10 declined the number because its capability failed that test. This one passes it, which is why the renumber gets paid rather than avoided.

Two honest costs of paying it. First, insertion is genuinely more expensive than appending — 67 edit sites versus roughly a dozen — and the user has accepted that in exchange for correct position. Second, a concurrent and currently untracked note in this same directory, `docs/architecture/loop-engineering.md`, reads PR #10's test the same way, agrees that its own capability passes it, and *still* declines a number, on the grounds that only an append is affordable and an append would place its fix after the README, which is both too late and the position a long session drops first. That reasoning does not transfer here: appending is unaffordable for a different reason — an unknowns pass placed after the specs would be auditing artifacts instead of informing them, which is not a worse version of the step, it is a different and useless one. If both notes land, the two step decisions must be reconciled in one sitting, because they cannot both renumber independently.

### Agent-definition changes

Both unconditional, both small, both in the existing agents' own territory.

**Implementation notes into `.claude/agents/testing.md`.** The testing agent already owns what happens during implementation and already carries the repository's only red-green-refactor discipline. Proposed addition, as a new section:

```markdown
## Implementation Notes

Long implementation runs discover things the plan did not anticipate. Record
them rather than absorbing them silently.

- Keep `docs/unknowns.md` open during implementation. When an edge case forces a
  departure from the plan, choose the lower-risk path, record it under
  **Deviations** alongside the section it invalidates, and continue. Do not stop
  to re-plan unless the deviation invalidates the approach itself.
- A deviation is a signal, not a defect. It means the spec was incomplete, which
  is expected — the point of recording it is that the next attempt starts from a
  better map.
- Where a deviation contradicts `docs/product-spec.md`,
  `docs/development-plan.md`, or `docs/tech-spec.md`, the spec is what gets
  revisited. This is the opposite of the `MEMORY.md` rule, deliberately: that
  file records session state and must yield to `docs/`; this one records that
  `docs/` was incomplete.
```

Credit line for the prompt document, not the agent file: the convention is adapted from the implementation-notes pattern in Thariq Shihipar's field guide to finding your unknowns.

**The merge quiz into `.claude/agents/code-review.md`.** The reviewer already owns the pre-merge gate and already holds the strictest evidentiary standard in the repository at `:70-76`. Proposed addition, as a new section:

```markdown
## Change Comprehension

Reading a diff gives a light understanding of a large change, because behaviour
depends on code paths the diff does not show. For any change large enough that
the author cannot narrate its behaviour from memory:

- Produce a report on the change — what was done, why, what it depends on, and
  what it now makes possible or impossible — followed by a short quiz on the
  parts a reader could plausibly get wrong.
- **Advisory by default.** The quiz informs the review; it does not block the
  merge. A project that wants it to block says so in one line in its own
  `CLAUDE.md`: "The change-comprehension quiz is blocking — no merge until the
  author passes it." Nothing else changes.
```

The advisory default is deliberate. A blocking quiz is a strong claim about a team's review culture, and grovv scaffolds for teams it has never met. The one-line opt-in keeps the strong version available without imposing it, and it is the same shape as the repository's existing escape hatches.

### The baseline-skills change

The baseline set is **10 skills**, enumerated twice: `docs/prompts/skills-builder.md:62-73` (ten rows) and `grovv-stack-scaffold.md:329-340` (ten rows). It goes to **14**.

| New skill | Trigger surface | Quadrant | Why a skill and not a section |
|-----------|----------------|----------|------------------------------|
| `blind-spot-pass` | "I don't know this area", entering unfamiliar code or an unfamiliar domain | Unknown unknowns | Invoked ad hoc, mid-work, far from any planning document. A section inside a planning skill would never trigger |
| `interviews` | "Ask me what you need to know", ambiguity in a request | Known unknowns | Same. It is a mode the user asks for, not a phase of a workflow |
| `implementation-notes` | Starting a long implementation run; hitting a forced deviation | Unknown unknowns | Needs to trigger during implementation, when no planning skill is in context |
| `change-quiz` | Before merging a large change; "explain what just happened" | Unknown knowns, about the diff | Triggers at review time, in a different session from the work |

The four that fold in, and where:

| Technique | Folds into | Why not its own skill |
|-----------|-----------|----------------------|
| Brainstorms and prototypes | `architecture-planning` | It is already the pre-build planning skill. Prototyping is a planning move, and the skill's existing "pre-development checklist" is where it belongs. A cross-reference goes in `ui-standards`, where the visual-direction case lives |
| Implementation plans | `architecture-planning` | The skill already covers system design and API contracts. Ordering a plan by what is most likely to change is a property of how it writes plans, not a separate capability |
| References | `dev-standards` | "When you cannot describe it, point at source code" is a prompting convention that applies to all work. It belongs with the core philosophy, not in a specialist skill |
| Pitches and explainers | `dev-standards` | It attaches to the definition of done, which `dev-standards` already owns |

The reason to stop at 14 rather than 18: every baseline skill is a surface that has to stay in sync with two enumerations, three directory trees, and four mirrored tool trees. Going to 18 buys four more triggerable entry points and creates eight more drift sites for techniques that are one paragraph each. The four that stay are the four that must trigger when no planning document is in context; the four that fold are the four that only ever apply inside work a skill already covers.

### Artifacts

| Path | New or edit | Purpose | Est. lines |
|------|-------------|---------|-----------|
| `docs/prompts/unknowns-pass.md` | New | The whole step: starting-point questions, blind spot pass, interview protocol and priority rule, prototype limb with the disposability exemption **and the standing-ask-first clause beside it**, adopt-mode variants, stopping rules, the `docs/unknowns.md` template, deliverable checklist, attribution to the field guide. The deliverable checklist must include: the prototype limb states that standing ask-first rules (frontend framework, Playwright) are not pre-empted by any prototype, reaction, or unknowns entry, and that prototype files are framework-free HTML rather than the framework choice | ~190 |
| `grovv-stack-scaffold.md` | Edit | New `### Step 2: Unknowns Pass` section; the 14 in-file renumbers including `:548`'s range; a `#### docs/prompts/unknowns-pass.md` subsection under the renumbered Step 6; tree row at `:103-107`; File and Folder Reference row; `:566` five-to-six; two new Success Criteria items | +45 on 578 |
| `.grovv/agents/testing.md` | Edit | **Canonical.** The Implementation Notes section above. The edit originates here | +14 on 121 |
| `.claude/agents/testing.md` | Edit | Re-derived from the canonical copy by tool-path substitution only | +14 on 121 |
| `.vibe/agents/testing.md` | Edit | Same, re-derived | +14 on 121 |
| `.codex/agents/testing.md` | Edit | Same, re-derived | +14 on 121 |
| `.grovv/agents/code-review.md` | Edit | **Canonical.** The Change Comprehension section above. The edit originates here | +12 on 89 |
| `.claude/agents/code-review.md` | Edit | Re-derived from the canonical copy by tool-path substitution only | +12 on 89 |
| `.vibe/agents/code-review.md` | Edit | Same, re-derived | +12 on 89 |
| `.codex/agents/code-review.md` | Edit | Same, re-derived | +12 on 89 |
| `.claude/agents/scaffold.md` | Edit | `:25` range; ordinals `:29-36`; one new list item at position 3 | 10 lines |
| `.grovv/agents/scaffold.md` | Edit | Same | 10 lines |
| `.vibe/agents/scaffold.md` | Edit | Same | 10 lines |
| `.codex/agents/scaffold.md` | Edit | Same. Do **not** silently fix the pre-existing `.claude/` paths at `:33-34` here | 10 lines |
| `.claude/skills/grovv/SKILL.md` | Edit | `:20` range; new step in the `:48` arrow chain | 2 lines |
| `.grovv/skills/grovv/SKILL.md` | Edit | `:20` range; `:48` chain | 2 lines |
| `.vibe/skills/grovv/SKILL.md` | Edit | `:20` range; `:50` chain | 2 lines |
| `.codex/skills/grovv/SKILL.md` | Edit | `:20` range; `:50` chain | 2 lines |
| `CLAUDE.md` | Edit | `:26` range; `:209` step number; Execution Order at `:118` gains an item; repository-structure prompt list | +4 on 263 |
| `.claude/CLAUDE.md` | Edit | `:21` range; tree at `:83-88`; Execution Order at `:117` | +4 on 259 |
| `.grovv/CLAUDE.md` | Edit | Execution Order at `:96`. No step ranges exist in this file — verified zero step tokens | +2 on file |
| `VIBE.md` | Edit | Execution Order at `:102`. Zero step tokens today; the asymmetry is worth closing in the same PR | +2 |
| `CODEX.md` | Edit | Execution Order at `:92`. Same | +2 |
| `README.md` | Edit | Prompt list at `:91`; the `:99` arrow chain. Zero step tokens | +2 on 174 |
| `docs/prompts/skills-builder.md` | Edit | `:3` step number; four new baseline rows at `:62-73`; four fold-in Covers cells; a note that the set is now 14 | +10 on 201 |
| `docs/prompts/team-design.md` | Edit | `:3` and `:160` step numbers | 2 lines |
| `docs/prompts/tracker-setup.md` | Edit | `:3` and `:346` step numbers. Plus one sentence distinguishing the `MEMORY.md` yield rule at `:276` from the `docs/unknowns.md` back-flow rule | +2 on 361 |
| `MEMORY.md` | Edit | `:38`, `:39`, `:72` step numbers; `:51` and `:53` are dated Decision Log entries and a judgment call — see Open Questions; the Current State version string at `:35`, which `check_versions.py` enforces against both manifests; a dated Decision Log entry | +3 on 76 |
| `.claude-plugin/plugin.json` | Edit | Version bump. A pipeline renumber is behaviour installed users receive. One of three sites `check_versions.py` compares | 1 line |
| `plugin.json` | Edit | Version bump. Already out of sync with the manifest above — 0.4.0 versus 0.3.0. Second of the three | 1 line |

### Phased rollout

| Phase | Delivers | Size |
|-------|----------|------|
| 1 — Conventions into the existing agents | `testing.md` and `code-review.md` in all four trees, canonical copy first. The two sections are reproduced literally above. No renumbering, no new files, no enumeration edits, no manifest change | ~104 lines across 8 files, half a day. **Still proposed** |
| 2 — The step and the renumber | ~~`docs/prompts/unknowns-pass.md`; the `### Step 2` section; all 67 renumber sites; the five arrow-chain insertions; the five Execution Order lists; the three trees; `:566`; the two Success Criteria items; the three-way version bump~~ | **Superseded 2026-07-27.** The pass landed inside Step 2 with no new prompt document, no renumber, and no enumeration edits — so none of the cascade was paid. The two Success Criteria items were added |
| 3 — The skills | Four new baseline skills and four fold-in sections in `docs/prompts/skills-builder.md`, plus the `ui-standards` cross-reference. Bodies are specified in `unknowns-skill-bodies.md` | ~10 lines of edits here, several hundred generated into targets, two days. **Still proposed** |

**Phase 1 stands alone and is startable as written.** Its two deliverables are given in full above; nothing else needs to be decided first, and it applies to every project grovv scaffolds, including every project that would skip the Step 2 pass entirely. If exactly one phase is approved, approve this one.

Its cascade is not zero, and an earlier draft of this note said it was. `.github/scripts/check_tool_sync.py` (tier b, run by `.github/workflows/checks.yml`) requires every `agents/*.md` to be identical to the canonical `.grovv/` copy once the tool path prefixes are normalized, and its `derived_targets()` takes the union of agent filenames across all four trees — so `testing.md` and `code-review.md` are in scope in `.grovv/`, `.claude/`, `.vibe/`, and `.codex/` alike, and all eight files exist today. Editing only the two `.claude/` copies leaves six mirrors stale, fails the Tool directory sync gate, and edits a derived copy rather than the source. The correct shape is: make the edit in `.grovv/`, then re-derive the other three by tool-path substitution only. The real size is about 104 lines across 8 files. What Phase 1 genuinely avoids is the renumber, the new files, the enumeration edits, and the manifest change — which is still the whole reason to take it first. **Completion condition: `python3 .github/scripts/check_tool_sync.py` passes.**

Phase 2 carries all of the risk in this plan and should not be split — a half-applied renumber is worse than none, because the directive would then disagree with itself about which step is which. Run the verification grep after applying and confirm it returns 62 lines whose numbers are all one higher than the map's `currentText` where the map says so, and unchanged everywhere else.

-----

## What We Are Deliberately Not Doing

| Rejected | Reason |
|----------|--------|
| A fractional "Step 1.5" | Encodes the step as an afterthought in the one document every agent reads end-to-end. The position is correct; the numbering should say so. The user chose correct position over cheap insertion |
| Appending the pass as Step 10 | The entire value is upstream of the product spec. A pass after the specs audits documents instead of informing them, which is not a cheaper version of the step but a useless one |
| Eight new baseline skills, one per technique | Takes the baseline from 10 to 18 and creates eight new sync surfaces across two enumerations, three trees, and four mirrored tool trees, for techniques that are one paragraph each. Four earn a skill because they must trigger when no planning document is in context; four do not |
| Changing any stack or UI default | The plan builds the mechanism to question a default and changes no default. `docs/prompts/skills-builder.md:67`, `CLAUDE.md:174-179`, and `.claude/agents/frontend.md:68-73` keep their current values. What changes is that the user now sees alternatives before those values are applied |
| Making the change-comprehension quiz blocking by default | A blocking merge gate is a strong claim about a review culture grovv has never met. Advisory with a documented one-line opt-in keeps the strong version available without imposing it |
| Making the Unknowns Pass a third universal ask-first non-negotiable | The two existing ones (`.claude/agents/frontend.md:11`, `.claude/agents/testing.md:43`) are hard stops before a specific irreversible act. This is a phase with its own stop condition, not a question. Adding it to the non-negotiable lists in eight files would inflate a list whose value is its shortness |
| Verbatim article prose in any generated artifact | Attribution is by name and technique, in original instruction text. The field guide is credited in `docs/prompts/unknowns-pass.md` and in each of the four new skills |
| Editing anything under any `skills/harness/` directory | Vendored verbatim under Apache-2.0. The harness trees are mirrored into `.claude/`, `.grovv/`, `.vibe/`, and `.codex/`, and all four contain step-numbered text of their own that must never be touched. Run `git status` before committing |
| Fixing `.codex/agents/scaffold.md:33-34` | It references `.claude/skills/` and `.claude/agents/` where `.vibe`'s copy was correctly adapted. The renumber touches exactly those two lines, which makes it tempting. Folding it in silently would make the diff larger than "renumbering." Call it out, fix it separately |
| Adding grounding requirements to the product-spec template | Contradiction 11 is real — `.claude/agents/code-review.md:70-76` demands a locator for a claim about a line of code and `grovv-stack-scaffold.md:215-243` demands nothing for the claim that invalidates everything downstream. But requiring evidence for Target Users is a different and larger change than adding a discovery step, and conflating them would make both harder to approve |
| Adding a Success Criteria item that any Open Question be closed | The criteria at `:561-575` are all existence checks, which is the deeper problem, but a "no open questions" gate would be routinely satisfied by deleting the questions. Two items are added instead: that `docs/unknowns.md` exists and that its Decided Defaults section is non-empty or explicitly marked as skipped |

-----

## Open Questions

- Does the prototype limb actually survive contact with production-first, or will future agents treat the exemption as a bug and remove it? The exemption is scoped to one directory and one step and is stated in the same paragraph as the limb, which is the strongest defence available in a document-only system. Currently: shipped with the scoping explicit, and flagged here so a future reader finds the reasoning before deleting the clause.
- What is the real turn cost of the pass? The field guide asserts these techniques are cheap and never measures anything. A blind spot pass, up to eight interview questions, one prototype round, and a confirmation gate is plausibly ten to fifteen turns before the first spec line is written. Currently: the stopping rules above are the cost bound, and the escape hatch is the pressure valve. Revisit after the first real run.
- Should the pass run at all for a trivial project? A one-page internal tool does not need a discovery phase, and a step every project runs is exactly what a number promises. Currently: the escape hatch covers it, and the pass is instructed to propose skipping itself when the intake describes something small and well-understood — a stated recommendation the user confirms, following the `tracker-setup.md:28-38` pattern.
- Do the prompt-set enumerations go five-to-six or five-to-seven? PR #10's knowledge-graph plan also adds one prompt document and also describes the change as five-to-six. If both land, `grovv-stack-scaffold.md:566` and the five Execution Order lists must be written once for both, not twice. Currently: whichever lands second reads the other's note first.
- Are the dated `MEMORY.md` Decision Log entries edited? There are two, not one: `:51` and `:53` both carry "(Step 8)", in a section whose own convention is append-only, so changing either to "(Step 9)" edits a historical record. Currently: both mapped as edits, because readers treat the parenthetical as the step's current identity. Leaving them and relying on `:38`, `:39`, and `:72` being current is defensible. Decide deliberately; do not let a global replace decide. Independent of any renumbering, `:53` also names `docs/prompts/linear-tracking.md`, which no longer exists — that reference is stale on its own terms and should be corrected whether or not the entry is renumbered.
- How does `docs/unknowns.md` avoid becoming the thing `@TODO` already is — a record nobody reads? Four named consumers and a pruning owner are the answer on paper. On paper is also what `grovv-stack-scaffold.md:551` ("Documents are living artifacts. Revise as understanding deepens") already says, with no trigger, mechanism, or owner, and it has never fired. Currently: the four consumers are written into the four consuming steps rather than into the unknowns document, on the theory that a rule fires where it is read.
- Should the four new skills ship to projects that skipped the pass? They are general-purpose techniques with no dependency on `docs/unknowns.md` existing. Currently: yes, unconditionally — they are baseline skills, and a user who skipped the pass is precisely the user most likely to want a blind spot pass later.
- @TODO The version drift must be resolved **inside** Phase 2, not deferred. `.github/scripts/check_versions.py` enforces three-way parity — `.claude-plugin/plugin.json`, root `plugin.json`, and the version quoted in `MEMORY.md`'s Current State prose at `:35` — and it fails on `main` today: 0.3.0, 0.4.0, 0.4.0. Since the check is already red, the renumber PR cannot land without picking the intended version and setting it in all three places. An earlier draft of this note read the drift correctly and then called it separable housekeeping; it is not separable, and there is no version of Phase 2 that is green without it.

-----

## Appendix: The Renumbering Map

All 67 edit sites, 15 files. The four mirrored tool trees carry identical line numbers, so each is given once with its mirror set named; expand to four files when applying. Nothing here is a heading-only change — each site's replacement text is a single number substitution except where the Change column says otherwise.

**Re-derive before applying.** Every line number here is against the working tree with the `tracker-setup.md` rename applied, per the baseline note at the top of this file. Re-run the verification grep, confirm it returns 62 lines across 15 files matching this map, and reconcile any difference first. Do not apply the map mechanically — if the rename has landed differently, or anything else has moved, these numbers point at the wrong lines and the failure is silent.

| File | Line | Kind | Change |
|------|------|------|--------|
| `grovv-stack-scaffold.md` | 184 | inline | Step 6 and Step 7 → Step 7 and Step 8 |
| `grovv-stack-scaffold.md` | 198 | heading | Step 2 → Step 3 |
| `grovv-stack-scaffold.md` | 245 | heading | Step 3 → Step 4 |
| `grovv-stack-scaffold.md` | 270 | heading | Step 4 → Step 5 |
| `grovv-stack-scaffold.md` | 319 | heading | Step 5 → Step 6 |
| `grovv-stack-scaffold.md` | 356 | inline | Step 7 → Step 8. Carries `.claude/skills/harness/` in its prose — the line a naive harness filter drops, and it also contains "Phase 4-0" nearby at `:383`, so no regex over `[0-9]-0` |
| `grovv-stack-scaffold.md` | 360 | inline | Step 8 → Step 9 |
| `grovv-stack-scaffold.md` | 364 | inline | Step 4 → Step 5 (template reference) |
| `grovv-stack-scaffold.md` | 370 | heading | Step 6 → Step 7 |
| `grovv-stack-scaffold.md` | 381 | heading | Step 7 → Step 8 |
| `grovv-stack-scaffold.md` | 383 | inline | Step 6 → Step 7. Same line carries "(harness Phase 4-0)" — leave it |
| `grovv-stack-scaffold.md` | 396 | heading | Step 8 → Step 9 |
| `grovv-stack-scaffold.md` | 408 | heading | Step 9 → Step 10 |
| `grovv-stack-scaffold.md` | 548 | range | "Steps 2-9" → "Steps 2-10", **not** 3-10; plus Step 7 → 8 and Step 8 → 9 in the same sentence. The only ASCII-hyphen range in the repo |
| `CLAUDE.md` | 26 | range | Steps 0–9 → Steps 0–10 (en dash) |
| `CLAUDE.md` | 209 | inline | Step 8 → Step 9 |
| `.claude/CLAUDE.md` | 21 | range | Steps 0–9 → Steps 0–10 |
| `MEMORY.md` | 38 | range | Steps 0–9 → Steps 0–10 |
| `MEMORY.md` | 39 | inline | Step 8 → Step 9 |
| `MEMORY.md` | 51 | inline | Step 8 → Step 9. Dated Decision Log entry in an append-only section — see Open Questions before applying |
| `MEMORY.md` | 53 | inline | Step 8 → Step 9. Second dated Decision Log entry, same condition. It also names `docs/prompts/linear-tracking.md`, which no longer exists — a stale reference independent of the renumber |
| `MEMORY.md` | 72 | inline | Step 8 → Step 9 |
| `docs/prompts/skills-builder.md` | 3 | inline | Step 6 → Step 7 |
| `docs/prompts/team-design.md` | 3 | inline | Step 7 → 8, Step 6 → 7, Step 8 → 9 (three numbers, one line) |
| `docs/prompts/team-design.md` | 160 | inline | Step 8 → 9, Step 9 → 10 |
| `docs/prompts/tracker-setup.md` | 3 | inline | Step 8 → 9, Step 7 → 8, Step 9 → 10 |
| `docs/prompts/tracker-setup.md` | 346 | inline | Step 9 → Step 10 |
| `skills/grovv/SKILL.md` ×4 | 20 | range | Steps 0–9 → Steps 0–10. Mirrors: `.claude/`, `.grovv/`, `.vibe/`, `.codex/` |
| `agents/scaffold.md` ×4 | 25 | range | Steps 0–9 → Steps 0–10. Same four mirrors |
| `agents/scaffold.md` ×4 | 29-36 | ordinal | Items 3-10 become 4-11. **No step token on any of these eight lines** — invisible to every step grep. A new item is inserted at position 3 naming the Unknowns Pass; final lists run 1 to 11 |

The 27 sites carrying a step token that must **not** change: `grovv-stack-scaffold.md:152`, `:172`, `:211`, `:545`; `agents/scaffold.md:17` in all four mirrors; `docs/prompts/tracker-setup.md:5`, `:26`, `:312` — that prompt's own internal Step 0, which sits inside the file that *is* a pipeline step, so renumbering it would make the prompt incoherent; and four lines in each `skills/grovv/SKILL.md`, which are **not** at the same numbers across the mirrors: `:26`, `:27`, `:32`, `:33` in `.claude/` and `.grovv/`, but `:28`, `:29`, `:34`, `:35` in `.vibe/` and `.codex/`. That is the same +2 offset the arrow chain already shows (`:48` versus `:50`), and it is the one place in this map where "expand to four files when applying" does not mean "reuse the number."

-----

## Colophon

| Field | Value |
|-------|-------|
| Version | 1.0.0 |
| Last Updated | 2026-07-27 |
| Status | Decided — pass implemented inside Step 2; renumber declined; Phases 1 and 3 still proposed |
| Author(s) | grovv stack scaffolding agent |
| Model | Claude (Claude Code) |

-----
gro\\/\\/ stack — Unknowns Engineering
