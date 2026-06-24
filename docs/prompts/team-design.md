# Prompt: Design the Agent Team (Harness)

Use this prompt to generate a project-specific **agent team and the skills they use** for the target project. It is **Step 7** of the grovv stack scaffolding pipeline — it runs **after `skills-builder.md` (Step 6) and before `linear-tracking.md` (Step 8)**. The specs (`docs/product-spec.md`, `docs/development-plan.md`, `docs/tech-spec.md`) already exist by now, and once the baseline best-practice skills exist, the team is designed to execute against them.

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

Carry forward, do not re-litigate, the two standing grovv ask-first rules. This step must not pre-empt them:

- **Frontend framework** (Astro + React or Next.js) — if the team includes a frontend agent, it inherits whatever was already chosen; do not pick here.
- **Playwright** — never auto-generate E2E flows. A testing/QA agent must still ask what Playwright should test before writing any E2E test.

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
- [ ] The chosen execution mode and pattern are stated explicitly
- [ ] Nothing was written to `.claude/commands/`
- [ ] The target `CLAUDE.md` carries a harness pointer (trigger rule + change-log table)
- [ ] Frontend-framework and Playwright ask-first rules were not pre-empted
- [ ] Trigger validation (should-trigger + should-not-trigger) passed with no conflicts against existing skills

-----

## After This Step

Continue the pipeline: proceed to `linear-tracking.md` (Step 8), then `readme-generator.md` (Step 9). Surface the agent team where relevant — in the Linear backlog and the README — and revisit `docs/tech-spec.md` if it should document the team as part of the project's development workflow.

-----
gro\\/\\/ stack — Agent Team Design
