# Prompt: Design the Agent Team (Harness)

Use this prompt to generate a project-specific **agent team and the skills they use** for the target project. It is **Step 7** of the grovv stack scaffolding pipeline — it runs **after `skills-builder.md` (Step 6) and before `tracker-setup.md` (Step 8)**. The specs (`docs/product-spec.md`, `docs/development-plan.md`, `docs/tech-spec.md`) already exist by now, and once the baseline best-practice skills exist, the team is designed to execute against them.

This step adapts the vendored **harness** meta-skill (`.claude/skills/harness/`) to grovv stack conventions. harness is the team-architecture factory: it turns a domain description into coordinated agents plus the skills those agents use, using six proven orchestration patterns. See `.claude/skills/harness/ATTRIBUTION.md` for provenance and license.

-----

## What This Step Produces

Run against the **target project**, this step writes into the target's `.claude/`:

```
target-project/
└── .claude/
    ├── agents/                 # Project-specific agent definitions (additive)
    │   └── {role}.md
    └── skills/                 # Skills the agents use
        ├── {orchestrator}/SKILL.md
        └── {skill}/SKILL.md
```

It also registers a minimal **harness pointer** in the target's `CLAUDE.md` (trigger rule + change log), so a fresh session knows the orchestrator skill exists.

It does **not** generate anything under `.claude/commands/`.

-----

## Relationship to the grovv Default Agents

grovv stack ships six baseline sub-agents (`scaffold`, `frontend`, `backend`, `testing`, `database`, `code-review`). This step is **additive**:

- Treat the six defaults as the baseline team. Do not delete or replace them.
- Design **additional, project-specific agents** only where the domain needs capability the defaults do not cover (e.g., a `billing-reconciler` for a Stripe + Lago product, an `ingest-pipeline` agent for a data product, a `qa` agent for cross-boundary integration checks).
- Before adding an agent, run the harness duplicate review (Phase 3-0 in `.claude/skills/harness/SKILL.md`): if a default already covers the role, extend it rather than spawn a near-duplicate.

The deliverable is the **smallest team that covers the domain** — the baseline plus the few specialists the product actually requires.

-----

## Ask Before Generating

Consistent with the grovv stack non-negotiables, ask first — never assume:

- What is the core workflow this team automates end to end?
- Which task types dominate — generation, review, analysis, transformation, orchestration?
- Where does the work fan out (parallelizable) versus where is it strictly sequential?
- Does the product need a quality gate (a reviewer/QA agent separate from the producer)?
- Are there capabilities the six defaults do not cover?
- Does any state one agent produces need to be read by other agents, or outlive the producing agent's context window — or is passing results through the orchestrator sufficient? Sufficient is the usual answer; see Data Passing Between Agents below.

Carry forward, do not re-litigate, the two standing grovv ask-first rules. This step must not pre-empt them:

- **Frontend framework** (Astro + React or Next.js) — if the team includes a frontend agent, it inherits whatever was already chosen; do not pick here.
- **Playwright** — never auto-generate E2E flows. A testing/QA agent must still ask what Playwright should test before writing any E2E test.

Phase 0's audit reads artifacts that Step 6 generated, and those can disagree with the spec. **When a generated skill and `docs/tech-spec.md` disagree about an ask-first answer, report it and let the user decide.** A skill asserting Astro while the spec names Next.js is a conflict between two generated files, so neither is the source — the user is. Deferring to the spec because it sounds authoritative answers the framework question with an artifact this pipeline wrote, and deferring to the skill is the same mistake in the other direction. Name both files, quote what each asserts, and design no agent that depends on the answer until the user has given one.

-----

## Workflow

Follow the phased workflow defined in the vendored skill `.claude/skills/harness/SKILL.md`. Summary, in grovv terms:

| Phase | Purpose |
|-------|---------|
| 0 — Audit | Read the target's existing `.claude/agents/`, `.claude/skills/`, and `CLAUDE.md`. Decide: new build, extension, or maintenance. Detect drift. Report before acting. |
| 1 — Domain analysis | Identify the domain, dominant task types, and the project stack from `docs/tech-spec.md` / codebase. |
| 2 — Team architecture | Choose execution mode (agent team is the default) and one of the six patterns. |
| 3 — Agent definitions | Write each agent to `.claude/agents/{name}.md` (duplicate review first; reuse defaults where possible). |
| 4 — Skill generation | Write the skills each agent uses to `.claude/skills/{name}/SKILL.md` with progressive disclosure. |
| 5 — Orchestration | Write the orchestrator skill (who collaborates, in what order, with what data-passing and error handling). Register the harness pointer in the target `CLAUDE.md`. |
| 6 — Validation | Structure check, trigger check (should / should-not), dry-run the data flow. |
| 7 — Evolution | After each run, offer to refine; record changes in the `CLAUDE.md` change log. |

**The duplicate review in Phases 3-0 and 4-0 has two subjects, and both must be named before it runs.** On the agent side it is the six grovv defaults. On the skill side it is the fourteen baseline skills that `skills-builder.md` (Step 6) writes: `dev-standards`, `architecture-planning`, `frontend-development`, `ui-standards`, `backend-development`, `database-design`, `security-practices`, `testing-tdd`, `deployment-ops`, `debugging`, `blind-spot-pass`, `interviews`, `implementation-notes`, and `change-quiz`. A skill matching one of those names is never re-created under a variant name. Anything outside those fourteen and outside this step's own additions belongs to the project — audit it, never rewrite it.

For pattern decision trees, agent-definition structure, orchestrator templates, the QA agent guide, and skill-writing/testing methodology, read the corresponding files under `.claude/skills/harness/references/`. Do not duplicate that detail here — load it when the phase needs it.

-----

## The Six Architecture Patterns

Pick the one that matches the work, then confirm with the user before generating:

| Pattern | Use when |
|---------|----------|
| Pipeline | Sequential, dependent stages — each output feeds the next |
| Fan-out / Fan-in | Independent work in parallel, then consolidate the results |
| Expert Pool | Context-triggered selection — only the relevant specialist runs |
| Producer-Reviewer | Generation followed by an independent quality gate |
| Supervisor | A central coordinator manages state and routes work dynamically |
| Hierarchical Delegation | A lead decomposes and recursively delegates to sub-agents |

-----

## Data Passing Between Agents

The vendored harness skill defines four data-passing strategies in its orchestration phase. grovv adds a fifth. Extend the set here — never by editing the vendored files.

| Strategy | Mechanism | Mode | Use when |
|----------|-----------|------|----------|
| Message-based | `SendMessage` directly between team members | Team | Real-time coordination, feedback exchange, lightweight state |
| Task-based | `TaskCreate` / `TaskUpdate` carrying shared task state | Team | Progress tracking, dependency management |
| File-based | Write and read at agreed paths | Team + sub | Large or structured artifacts, audit trail |
| Return-value-based | The `Agent` tool's return message | Sub | The orchestrator collects sub-agent results directly |
| Shared store (grovv addition) | Structured state living outside any context window, queried by slice rather than read whole | Team + sub | All three promotion conditions below hold |

The fifth strategy is not a default. Promote to it only when **all three** of the following hold at once:

1. Three or more agents must read state that another agent produced, not merely report it upward to the orchestrator.
2. The state outlives a single agent's context window — a later phase, a later run, or a later session reads it.
3. Consumers need provenance — which agent wrote a fact, from which artifact, and when — in order to act on it.

Fewer than all three, and file-based passing — plus task-based coordination in team mode, or return values in sub-agent mode — is sufficient and cheaper. Say so explicitly in the orchestrator skill rather than leaving the choice unexamined.

All three, and the orchestrator skill must name the store, its schema, and its provenance fields. A shared store earns its cost on three counts: it connects (it links the same entity across agents that never communicated), it compresses (a synthesizer reads structured facts instead of every producer's raw output), and it grounds (every fact it holds traces back to a source). A store that does not do all three is a file with extra steps.

### Provenance on Cross-Agent Artifacts

Whichever strategy is chosen, every artifact one agent writes for another to read carries provenance: which agent wrote it, from which source artifact, and when. This is unconditional — it applies to a file dropped at an agreed path exactly as much as to a shared store. Without it a downstream agent cannot tell a fact it should act on from a guess it should verify, and a reviewer cannot trace a conclusion back to its evidence.

-----

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
  above. On the skill side it is the fourteen baseline skills that
  `skills-builder.md` (Step 6) writes: `dev-standards`, `architecture-planning`,
  `frontend-development`, `ui-standards`, `backend-development`,
  `database-design`, `security-practices`, `testing-tdd`, `deployment-ops`,
  `debugging`, `blind-spot-pass`, `interviews`, `implementation-notes`, and
  `change-quiz`. Anything in `.claude/skills/` outside those fourteen and outside
  this step's own additions belongs to the project — audit it, never rewrite it.
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
  absent, it asks. Where two generated artifacts disagree, the rule above
  applies — report both, resolve neither.
- **A re-entry does not advance the pipeline on its own.** Reconciling this step
  is a complete outcome. Continue to `tracker-setup.md` (Step 8) only if the user
  asks for it.

A re-entry that changes nothing and returns a list of questions has succeeded.
No action is a valid result of this step.

-----

## grovv Conventions for Generated Output

The vendored harness skill is the methodology. When this step writes files into the target project, apply grovv stack conventions on top:

- **Agent teams are the default execution mode** — already aligned with grovv's `settings.json` (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`).
- **Production-first** — agent and skill definitions describe complete, typed, error-handled behavior. No pseudo-instructions.
- **Security by default** — any agent that touches input, auth, or data carries validation and least-privilege expectations.
- **Ask-first preserved** — frontend framework and Playwright rules above are never bypassed by a generated agent.
- **Document style** — `-----` horizontal rules, tables for reference data, `@TODO` for unknowns, no emoji in headings, language-hinted code fences.
- **Naming** — skill and agent folder/file names are lowercase with dashes.
- **Branding** — grovv-authored wrapper documents (not the vendored skill) carry the gro\\/\\/ stack footer.

Note: the vendored `.claude/skills/harness/SKILL.md` is authored in its original language and is left **verbatim** for fidelity and attribution. This prompt is the grovv-facing, English interface to it — extend or adjust behavior here, not in the vendored files.

-----

## Deliverable Checklist

This step is complete when, for the target project:

- [ ] Existing `.claude/agents/` and `.claude/skills/` were audited before any change (harness Phase 0)
- [ ] The six grovv default agents are intact; only genuinely new specialists were added
- [ ] Duplicate review was run before adding each agent and each skill (Phases 3-0, 4-0)
- [ ] Every agent has a `.claude/agents/{name}.md` definition (built-in types included)
- [ ] Each agent's skills exist under `.claude/skills/{name}/SKILL.md` with pushy, trigger-rich descriptions
- [ ] Exactly one orchestrator skill ties the team together (data flow + error handling + test scenario)
- [ ] The data-passing strategy is named explicitly, and a shared store was adopted only where all three promotion conditions hold
- [ ] Where a shared store was adopted, the orchestrator skill names the store, its schema, and its provenance fields
- [ ] Every cross-agent artifact carries provenance — writing agent, source artifact, and time
- [ ] The chosen execution mode and pattern are stated explicitly
- [ ] Nothing was written to `.claude/commands/`
- [ ] The target `CLAUDE.md` carries a harness pointer (trigger rule + change-log table)
- [ ] Frontend-framework and Playwright ask-first rules were not pre-empted
- [ ] Any disagreement between a generated skill and `docs/tech-spec.md` about an ask-first answer was surfaced to the user and decided by them, not resolved by this step
- [ ] On a re-entry, every project-specific agent and every skill this step added carried a verdict, and the report was presented before anything was written
- [ ] The duplicate review named the fourteen baseline skills explicitly; the six default agents were exempt from removal
- [ ] No hand-edited generated file was overwritten, and the `CLAUDE.md` harness pointer was updated rather than duplicated
- [ ] Trigger validation (should-trigger + should-not-trigger) passed with no conflicts against existing skills
- [ ] Every agent definition and every skill this step added has valid frontmatter, a `name` matching its folder or filename exactly, and a `description` short enough to carry literal triggers rather than prose
- [ ] **Where tool directories are derived from `.grovv/`, the mirrors were refreshed after this step and the refresh was verified** — this step writes agents and an orchestrator after Step 6 already mirrored, so a mirror taken then is now stale, and `.claude/`, `.vibe/` and `.codex/` are what the tools actually load. Where the project adapts per tool rather than copying byte for byte, confirm only the deliberate adaptations differ; a plain byte-comparison reports intended per-tool content as drift

-----

## After This Step

Continue the pipeline: proceed to `tracker-setup.md` (Step 8), then `readme-generator.md` (Step 9). Surface the agent team where relevant — in the project's tracker backlog and the README — and revisit `docs/tech-spec.md` if it should document the team as part of the project's development workflow.

-----
gro\\/\\/ stack — Agent Team Design
