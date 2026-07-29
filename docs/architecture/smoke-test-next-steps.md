# Smoke Test — Next Steps for Runs 2 and 3

**gro\\/\\/ stack** — What it takes to execute the two runs that have never happened

-----

## What This Document Is

`pipeline-smoke-test.md` is the scoring authority — it says what a run must
demonstrate. This document is operational: what stands between us and executing
runs 2 and 3, what has to be decided first, and the exact preparation each needs.

The two do not duplicate each other. When they disagree, the rubric wins on
*what to score* and this file wins on *how to get there*.

-----

## Where Run 1 Left Off

Run 1 executed Steps 0–9 in new-project mode on 2026-07-27 against a throwaway
target: a digital salesroom for CARET Legal, with a real product brief and a real
discovery deck supplied by the user. 229 files generated.

| Outcome | Value |
|---------|-------|
| Findings | 10 — 0 blockers, 8 defects, 2 notes, 1 withdrawn on verification |
| Rubric rows scored | P, U, G, S, T, M, W (partial) |
| Rubric rows **never exercised** | **R1–R15** (re-entry), **D1–D11** (adopt) |
| Target survival | **None.** The container was ephemeral; the target is gone |

Every defect is fixed. The rubric gained P6, P7, U12–U14, S17–S20.

A propagation audit run afterwards found the F1 defect a **fourth** time, in the
bullet immediately above the one that had just been fixed — and behind it a real
structural gap: the target's context file was written by three separate
instructions and created by none of them. Run 1's target ended up with one only
because the run invented it. Step 1 now owns its creation.

**The most instructive finding was not a pipeline defect at all.** Twice in one
session the run asserted a fact from an absence: a question recorded as *refused*
that had never been delivered, and a skill recorded as *missing* that was still
being written by a queued agent. Both went into durable artifacts before being
checked; the second was pushed as a blocker and withdrawn an hour later. Runs 2
and 3 should be executed with that failure mode in mind — an absence is not
evidence until you know the work finished.

-----

## The Blocker Both Runs Share

**Run 2 requires run 1's output to still exist.** The whole point of a re-entry
run is that it meets artifacts a previous run wrote. Run 3 needs a foreign
codebase this repository does not have.

Neither survives a session boundary in the current setup, and that — not effort —
is the reason neither has ever run. This needs a decision before either can be
scheduled. See Open Questions below.

-----

## Run 2 — Re-entry

### What it proves

That Steps 6 and 7 **reconcile rather than regenerate**. This is Layer 2's entire
claim and nothing has ever tested it. No check script holds state or compares
across time, and only `tracker-setup.md` ever defined a second run of itself.

The clause most likely to be lost in implementation is the one that makes it work:
*a re-entry that changes nothing and returns a list of questions has succeeded.*
Every other step in the pipeline terminates in an artifact, so an implementation
with no shape for "no action" will write something to prove it ran. **R15 scores
the disk for exactly this.**

### Preparation — three edits, no more

Per the rubric. Commit run 1's output first, then make exactly these edits and
record the line numbers:

| # | Edit | Verdict it should force |
|---|------|------------------------|
| 1 | Swap the database in `docs/tech-spec.md` — PostgreSQL for SQLite | Every skill and agent asserting the old one is **drifted** |
| 2 | Drop an integration named in run 1 | The specialist Step 7 added for it is **orphaned** |
| 3 | Hand-edit one generated `SKILL.md`, adding a distinctive line | The artifact **R9** scores — did the hand edit survive |

Two spec edits, one of each verdict, so the run must produce both answers rather
than only the easy one. Then invoke the pipeline again against the same directory.

### Run-1-specific note for this target

Run 1's target has **no Stripe specialist to orphan** — Stripe and Lago were
deliberately excluded from the salesroom because it has no billing surface. The
three project-specific agents are `access-control`, `engagement-analytics` and
`room-composition`. Orphan `engagement-analytics` by removing Consensus from the
tech spec, which is a genuine integration drop rather than a contrived one.

If run 1 is re-executed from scratch rather than restored, this note may not
apply — check what Step 7 actually generated before choosing what to drop.

### What to watch

- **R14 is a blocker and the subtlest row in the rubric.** Run 1 left the frontend
  framework *unanswered*. So run 2 must neither infer it from its own generated
  artifacts nor re-litigate it — it carries forward as still-open. A run reasoning
  "the skills already show Astro patterns, so" has pre-empted the user with its own
  output, which is the exact failure both ask-first rules exist to prevent.
- **R12/R13 are conditional on W.** Run 1 declined CI (unanswered, recorded as a
  decline in `MEMORY.md`). Run 2 must generate none, not silently re-ask, and the
  decline line must survive.
- **R1** — the run must identify itself as a *resume*, not an adoption. The kickoff
  skill's third detect branch exists for this; run 2 is the first thing that has
  ever exercised it.

-----

## Run 3 — Adopt Mode

### What it proves

That the pipeline can read a codebase it did not write without trampling it.
Eleven rows, **five of them blockers** — the highest blocker density in the rubric,
because adopt mode is where the pipeline touches work somebody else owns.

### Choosing the target

**Deliberately not the default stack.** A Go service or a Python API. A target
that already matches grovv's defaults cannot distinguish *reading the project*
from *restating the defaults* — which is precisely what D5 exists to catch.

It must also have, ideally:

| Property | Row it makes scoreable |
|----------|-----------------------|
| An existing README with accurate content | D4 — merged, not replaced |
| Existing CI | D8 — stated, not overwritten (blocker) |
| An existing frontend commitment | D7 — asked, not read silently from `package.json` (blocker) |
| Verify commands in a CI workflow or task runner | D11 — read, not invented |
| Some pre-existing `.claude/skills/` | D6 — extended, conflicts surfaced |

No single small repository will have all five. Pick for D7, D8 and D11 first —
they are the blockers and the ones most likely to fail.

### What to watch

- **D3 is the hard blocker**: `git status` in the target shows no change to any
  pre-existing source file. Everything else is recoverable; this is not.
- **D10** is where adopt mode should be *better* than new mode, not merely
  equivalent. The blind spot pass has real code to work against — it should report
  what the code does that the user did not describe, and where conventions are
  inconsistent. A generic new-project blind spot list, produced against a
  repository sitting right there, fails. Run 1's blind spot pass ran from model
  knowledge of a product category; run 3's has no excuse to.

-----

## Open Questions

These need answers before either run can be scheduled. None has an obvious default.

| # | Question | Why it blocks |
|---|----------|---------------|
| N1 | **How does run 1's target survive to run 2?** Same-session execution, a scratch branch in this repo, or a separate throwaway remote? | Run 2 is meaningless without run 1's artifacts. Same-session is what the rubric assumed and makes for a very long sitting; a scratch branch pollutes a repository that deliberately contains no generated output; a separate remote needs one to exist |
| N2 | **Which foreign repository does run 3 adopt?** | Session GitHub scope is `constructyourself/grovv-stack` only. A public clone may work through the proxy, but the repo must be chosen for the properties in the table above rather than convenience |
| N3 | **Does W5 ever become scoreable?** It needs a throwaway remote to observe a generated workflow's first run go green | Currently marked unscoreable. It is the only row that tests whether generated CI actually *works* rather than merely existing |
| N4 | **Is the 1024-character skill description cap real?** | S19 was written on an audit's assertion. The lengths are measured fact; the cap is not independently confirmed. If it is wrong the row is still useful but its severity is not |
| N5 | **Should the smoke test become a fixture rather than a live exercise?** | Every run so far has been hand-driven, which is why it had never happened before 2026-07-27. A committed fixture target would make run 2 cheap and repeatable — at the cost of testing a frozen artifact rather than what the pipeline produces today |
| N6 | **Should a check script enforce that a fix reaching `grovv-stack-scaffold.md` also reaches the prompt that executes it?** | Three times now a fix has landed in the directive and not in `docs/prompts/*.md`. The prompt is what runs at generation time, so a rule only in the scaffold governs nothing. `check_references.py` already walks cross-file references and could plausibly carry this |

N1 is the one to answer first. Everything about run 2 is downstream of it.

-----

## Recommended Order

1. **Answer N1.** Nothing about run 2 can be scheduled until the target has a home.
2. **Run 2**, since it tests a contract that shipped without ever executing, and
   its fifteen rows include three blockers.
3. **Answer N2**, then **run 3**. Highest blocker density, but adopt mode has at
   least been reasoned about in the directive; re-entry has not been observed at all.
4. Revisit **N3** and **N5** once both runs have happened and the cost of each is
   known rather than estimated.

-----

## Colophon

| Field | Value |
|-------|-------|
| Version | 0.1.0 |
| Last Updated | 2026-07-29 |
| Status | Draft — awaiting N1 |
| Author(s) | grovv-stack maintainers |

-----
gro\\/\\/ stack — Smoke Test Next Steps
