# grovv-stack

```
 ██████╗ ██████╗  ██████╗ ██╗   ██╗██╗   ██╗
██╔════╝ ██╔══██╗██╔═══██╗██║   ██║██║   ██║
██║  ███╗██████╔╝██║   ██║██║   ██║██║   ██║
██║   ██║██╔══██╗██║   ██║╚██╗ ██╔╝╚██╗ ██╔╝
╚██████╔╝██║  ██║╚██████╔╝ ╚████╔╝  ╚████╔╝
 ╚═════╝ ╚═╝  ╚═╝ ╚═════╝   ╚═══╝    ╚═══╝
```

**gro\\/\\/ stack** — Production-First Project Scaffolding

-----

## What is This?

This is the starting document for any project — new or existing. It defines the full scaffolding workflow that the agent follows.

The easiest way to kick it off is the **gro\\/\\/ stack plugin**. Install once, then run `/grovv` in any repo (or just say "build out this project with grovv stack"):

```
/plugin marketplace add constructyourself/grovv-stack
/plugin install grovv-stack@grovv
```

- `/grovv` — explicit kickoff. Optional argument `new` or `adopt` forces the mode; otherwise it auto-detects new vs existing.
- Natural language — the same `grovv` skill triggers on intent ("build out this project") and runs this same workflow.

Both routes are the one `grovv` skill — there is no separate command.

Without the plugin, you can still drop this file into a project folder, open a conversation with an AI agent, and say:

> *"Read grovv-stack-scaffold.md and help me build out this project."*

Either way, the agent will ask questions to fully understand your product, your goals, your constraints, and your technical preferences — then systematically build out the documentation foundation that drives development.

This is not a boilerplate generator. It is a **conversational scaffolding process** — the agent works with you to understand the project deeply before generating anything.

-----

## How It Works

### New Projects

1. Create your project folder (lowercase, dashes): `my-project/`
2. Place this file in the root
3. Start a conversation — the agent asks questions, then builds everything from scratch

### Existing Projects

1. Place this file in the project root
2. Start a conversation — tell the agent this is an existing project
3. The agent will **analyze what already exists** before doing anything:
   - Read existing code, configs, and documentation
   - Identify the current tech stack, patterns, and conventions
   - Map what exists to the grovv stack structure
   - Identify gaps and misalignments
4. The agent then proposes an **adoption plan** — what to create, what to refactor, and what to leave alone
5. You approve the plan, and the agent builds incrementally

For existing projects, the agent should **never overwrite or break working code**. The approach is additive and iterative — bring the project into alignment with grovv stack patterns at a pace that makes sense.

-----

## Conversation First

Whether new or existing, the agent should **ask questions before generating**. The goal is to build a complete understanding of:

- What is the product and what problem does it solve?
- Who are the target users?
- What are the core features and priorities?
- What is the technology stack? (existing projects: what is it currently, and should anything change?)
- What are the constraints — timeline, budget, team size, existing systems?
- What is the deployment target?
- Are there integrations, background jobs, or real-time requirements?

**For existing projects, also ask:**

- What is the current state of the codebase? What works well, what doesn't?
- Is there existing documentation? Where does it live?
- Are there patterns or conventions already established that should be preserved?
- What is the motivation for adopting grovv stack? (better docs, refactoring, scaling, onboarding?)
- Are there areas of the codebase that should not be touched?
- What is the priority — documentation first, or refactoring alongside?

The agent should not assume. If information is missing or ambiguous, ask. Mark incomplete sections with `@TODO` and return to them as the conversation progresses.

Some questions cannot be answered in the abstract. The user recognizes the answer on sight but cannot specify it — visual design is the canonical case. When a question is of that shape, asking harder does not help; build something disposable for the user to react to, under the rules below.

These questions are all about the artifact. Step 2 opens with four about the *person* — what they have built before, how well they know this domain, where they are in their own thinking, and what they are least sure about — because the right depth for everything above depends on answers this list never asks for.

-----

## The Throwaway Tier

Production-first governs what ships. It does not govern what you build to find out what should ship.

An **exploratory artifact** — a prototype, mockup, brainstorm, or spike — exists to be reacted to and then deleted. It is exempt from the production bar: it may be untyped, unwired, hard-coded, styled by hand, and built from fake data. What it may never be is merged.

| Rule | Detail |
|------|--------|
| Name it | Prototype, mockup, brainstorm, or spike. Never a "first pass" or "draft implementation" — those read as production code that is not finished yet, which is the thing this tier exists to avoid |
| Where it lives | Multi-file exploration goes on a `proto/*` or `spike/*` branch that is never merged. A single-file mockup goes in a gitignored `prototypes/` directory |
| How long it lives | Until the decision it exists to inform is recorded. Then it is deleted |
| What survives it | The decision, not the artifact. Write it down before deleting |
| What it cannot decide | An exploratory artifact never satisfies an ask-first rule. Four mockups built in React is not a decision to use Next.js — that question is still asked, and still answered by the user |
| How it is reviewed | Code review does not apply the production checklist to an exploratory artifact. It checks three things: that the artifact is unmerged, that it is gitignored or on a throwaway branch, and that the decision it informed was recorded |

Build several at once when the question is one of taste rather than fact. One mockup invites approval; three or four wildly different directions invite a reaction, and the reaction is the information.

-----

## Directory Structure

The scaffolding process creates or integrates the following structure:

```
project-folder/
├── docs/
│   ├── unknowns.md            # What is still open — written by Step 2's unknowns pass
│   ├── product-spec.md        # Product-level definition
│   ├── development-plan.md    # Engineering plan based on product-spec
│   ├── tech-spec.md           # Complete technical specification
│   ├── architecture/          # Architecture decision records (ADRs)
│   └── prompts/               # Prompt specs for building docs and skills
│       ├── skills-builder.md
│       ├── team-design.md
│       ├── tracker-setup.md
│       ├── tech-spec.md
│       └── readme-generator.md
├── .claude/                   # One directory per tool the team chose in Step 1 (.claude/, .vibe/, .codex/)
│   ├── agents/                # Project-specific agent team (from team-design step)
│   └── skills/                # Invocable skills — best-practice set + agent skills + orchestrator
│       ├── dev-standards/         # Core philosophy + workflow (from skills-builder)
│       ├── architecture-planning/
│       ├── frontend-development/
│       ├── ui-standards/
│       ├── backend-development/
│       ├── database-design/
│       ├── security-practices/
│       ├── testing-tdd/
│       ├── deployment-ops/
│       ├── debugging/
│       ├── blind-spot-pass/
│       ├── interviews/
│       ├── implementation-notes/
│       ├── change-quiz/
│       └── {orchestrator}/        # + agent skills (from team-design step)
├── .grovv/                    # Canonical definitions — only when more than one tool was chosen
├── .gitignore                 # Ignore rules — includes the gitignored prototypes/ the throwaway tier requires
├── MEMORY.md                  # Cross-session memory, coordinated with the tracker (from tracker-setup step)
├── settings.json              # Claude Code agent configuration
└── README.md                  # Project README (generated last)
```

**For existing projects:** This structure is additive. The `docs/` folder (including the spec documents) and the `.claude/` skills are created alongside whatever already exists. Existing files like `README.md` are updated rather than replaced — the agent should merge grovv stack conventions into what is already there.

### File and Folder Reference

| Path | Purpose |
|------|---------|
| `project-folder/` | Root directory — lowercase with dashes (e.g., `my-saas-app`) |
| `docs/` | Primary docs folder, built out over time through scaffolding |
| `docs/architecture/` | Architecture Decision Records documenting key technical choices |
| `docs/prompts/` | Prompt specifications for generating project-specific documents and skills |
| `docs/unknowns.md` | Living record of what is still open: starting point, blind spots, open questions, recognized constraints, decided defaults, deviations. Written by Step 2's unknowns pass, read at Steps 4 and 8 |
| `docs/product-spec.md` | Product-level definition: what, who, why |
| `docs/development-plan.md` | Engineering development plan derived from product-spec |
| `docs/tech-spec.md` | Complete technical specification built from product-spec + development-plan |
| `docs/prompts/team-design.md` | Prompt that designs the project-specific agent team and its skills (harness) |
| `docs/prompts/tracker-setup.md` | Prompt that sets up the project's issue tracker — asks for GitHub Issues or Linear, then seeds the backlog from the development plan |
| `.claude/agents/` | Project-specific agent team generated by the team-design step (additive to grovv defaults) |
| `.claude/skills/` | Invocable skills: the best-practice set from skills-builder, plus the agent team's skills and the orchestrator from team-design |
| `.gitignore` | Ignore rules, including the gitignored `prototypes/` directory the throwaway tier's containment rule depends on |
| `MEMORY.md` | Cross-session memory — decisions, gotchas, in-flight state; coordinates with the project's tracker (the tracker owns the backlog) |
| `settings.json` | Claude Code configuration |
| `README.md` | Project README, generated or updated as the final step |

-----

## Scaffolding Steps

### Step 0: Assess (Existing Projects Only)

Before creating anything, the agent should analyze the existing project:

1. **Read the codebase** — scan directory structure, configs (`package.json`, `tsconfig.json`, `docker-compose.yml`, etc.), and existing documentation
2. **Identify the current stack** — languages, frameworks, database, deployment, auth
3. **Catalog existing patterns** — coding conventions, project structure, naming, testing approach
4. **Check for existing docs** — README, specs, ADRs, inline docs, wikis
5. **Map gaps** — what grovv stack provides that the project is missing
6. **Propose an adoption plan** — present to the user for approval before proceeding

The adoption plan should clearly state:

- What will be **created** (new docs, new folders)
- What will be **updated** (existing README, existing configs)
- What will be **left alone** (working code, established patterns that don't need changing)
- What could be **refactored over time** (suggestions for incremental improvement, not immediate changes)

**Do not proceed until the user approves the plan.**

### Step 1: Create Structure and Configuration

Create directories, the `settings.json` configuration file, and the project's `.gitignore` entries.

**Which tool directories to create is a question, not an assumption.** The scaffolder runs from one CLI, but the project outlives the session that created it, and a teammate may open it from a different one. Generating only the running CLI's directory is how a project ends up usable from exactly one tool by accident rather than by choice. Ask before creating any of them; never infer the answer from which CLI happens to be running.

Ask exactly this:

> Which AI coding assistants will be used in this project? Pick every one your team works in — I will generate configuration for those and no others.
>
> 1. **Claude Code** — `.claude/`
> 2. **Vibe** — `.vibe/`
> 3. **Codex** — `.codex/`
>
> I am running from one of these already, so that one is a safe answer on its own. Adding another costs one directory and means a teammate on that tool can pick this project up with no migration. Leaving it out keeps the project smaller. Adding one later is possible but more work than adding it now, while the skills and agents are being generated.

- Wait for an explicit answer. If the user says "whatever you think", name the CLI this session is running from, say that it is the only one you can confirm they have, and ask them to confirm — a stated default is still an answer they gave.
- **One tool chosen** — create only that tool's directory. Do **not** create `.grovv/`. A single-tool project should not carry a canonical tree nobody will open.
- **More than one chosen** — create `.grovv/` as the canonical definitions plus each chosen tool's directory derived from it, identical apart from the tool path prefix. State in the project's context file that `.grovv/` is the source of truth and the tool directories are derived from it, so a future editor changes the canonical copy rather than one derived copy.
- Record the answer in the project's `MEMORY.md` so Steps 6 and 7 write into the chosen directories and a later session does not re-ask.

Derived copies drift silently — this repository keeps four in sync only because a CI check compares them. A target project that chose more than one tool has the same exposure and may want the same check. Do not generate one here; that is the verify-loop decision, and it belongs to the user.

**Discover the commands that prove this project works.** This is not a question — it is a read, and it costs the user nothing. Every later step is better for knowing them, and the README step (Step 9) is wrong without them.

For an existing project, read them from the project itself, stopping at the first source that yields commands:

| Source | What to take |
|--------|--------------|
| An existing CI workflow | The commands its steps actually run — the most reliable source, because it is what the project already trusts |
| `package.json` `scripts` | `test`, `lint`, `typecheck`, `build` — whichever exist, under their real names |
| `Makefile` | Targets named `test`, `lint`, `check`, `build` |
| `Taskfile.yml` / `justfile` | The same task names |
| `go.mod` present | `go test ./...`, `go vet ./...`, and `golangci-lint run` if its config file is present |

Where two sources disagree, prefer the CI workflow, then the task runner, then the manifest. Record which source each command came from — a command read from a stale `Makefile` is worth less than one read from a workflow that runs on every push.

For a new project the stack is not chosen until Step 4, so nothing can be read here. Note that the commands are pending, and derive them at Step 4 from the stack that step selects.

State the commands you found, and say plainly if you found none. **Do not write them to a file at this step** — the project's `MEMORY.md` does not exist until Step 8, which creates it. Carry them forward: Step 8 records them in that file's `Verify` table, and Step 9 uses them instead of guessing at a quick start. If nothing was found, they are carried forward as `@TODO`, because an empty table is a visible gap and a missing one is invisible.

**Directories to create:**

```
docs/
docs/architecture/
docs/prompts/
```

The `skills/` directory inside each chosen tool directory is created later by the skills-builder step (Step 6) and the team-design step (Step 7). For existing projects, only create directories that don't already exist. If the project has an existing `docs/` folder, integrate into it rather than replacing it.

**Create `docs/unknowns.md`** from the template in Step 2, with its sections present and empty. Step 2's unknowns pass fills it before the product spec is written, and Steps 4 and 8 read it. Creating the file here rather than there is deliberate: an empty section is a visible prompt to fill it, and a file that only exists when the pass ran cannot record that the pass was declined.

**Create `settings.json`** in the project root:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

For existing projects that already have a `settings.json`, merge the `env` block into the existing file.

**Create or append to `.gitignore`** in the project root. Without this the throwaway tier's containment rule has nothing enforcing it — mockups built in `prototypes/` are tracked, committable, and code review's containment check can never pass. Add an exploratory-artifacts section:

```gitignore
# Exploratory artifacts — prototypes, mockups, brainstorms and spikes are
# throwaway by definition and are never committed. Multi-file exploration
# belongs on an unmerged proto/* or spike/* branch instead.
prototypes/
```

For existing projects, append this section rather than replacing the file, and skip it if `prototypes/` is already ignored.

### Step 2: Product Spec

Create `docs/product-spec.md`. This is the foundation — everything downstream traces back to it.

#### Before writing: the unknowns pass

The product spec is where guesses become permanent. Everything after it — the development plan, the tech spec, ten generated skills, an agent team, a seeded backlog — is a derivative, so a wrong assumption here is discovered four layers deep and costs a rewrite of all four. This pass is the cheapest available way to find out what nobody has said yet, and it runs before the first spec line rather than as an audit afterwards.

It has no step number of its own deliberately. It is not a separable phase producing its own artifact — it is how this step starts.

**Ask about the person first.** Four questions, asked once, that the thirteen intake questions above never cover. They calibrate everything after: whether this pass should teach, challenge, or get out of the way.

1. Have you built this kind of thing before? If so, what did you learn that you would not want to repeat?
2. How well do you know this codebase or this domain — intimately, partially, or not at all?
3. Where are you in your own thinking: exploring what to build, deciding between approaches, or executing a decision you have already made?
4. What is the part of this you are least sure about?

The fourth is the interview seed. Record the answers in `docs/unknowns.md` in the user's own words — this is calibration data, not a summary to be tidied.

**Then a blind spot pass.** A research turn, not a question turn — asking someone to name what they have not considered does not work. For a new project, find out what is known about this problem domain, what its common failure modes are, what "good" looks like in this category, and what projects of this shape usually need that the user has not mentioned. For an existing project this is materially stronger, because there is real code to read: report what the code does that the user did not describe, where conventions are inconsistent, which subsystems are load-bearing and undocumented, and what a newcomer would get wrong. End by naming what you believe their blind spots are, in their own domain vocabulary, and asking whether the list is right.

**Then interview, one question at a time.** Never batched. Prioritize by whether the answer would change the architecture — a question whose answer changes nothing can wait, and a question whose answer changes the data model cannot.

The technology stack is one of these questions, and it is asked rather than assumed. The gro\\/\\/ stack defaults exist and are good, but a default nobody was told about is indistinguishable from a decision nobody made. State the default, name the two or three places it is most likely to be wrong for *this* project, and ask. A stated default the user accepts is still an answer they gave; a silent one is not.

**Where a question cannot be answered in the abstract, build something to react to.** Visual direction is the canonical case, and the instrument is the throwaway tier: several deliberately different directions, fake data, nothing wired up, deleted once the reaction is recorded. Include at least one direction that departs from the monochrome default, so the default becomes a choice rather than an inheritance. The reactions go into `docs/unknowns.md` in the user's words — those entries are the ones no later session can re-derive from any other document.

The throwaway tier's rules govern these artifacts in full, and one of them decides the question most likely to be misread here: **an exploratory artifact never answers an ask-first rule.** Prototypes at this step are framework-free HTML. Building four of them does not choose a frontend framework and must never be read as having chosen one — that question is still asked, at the point frontend code is first written, and still answered by the user.

**When it stops.** An unknowns pass is exactly the kind of work that runs forever, so the bounds are explicit:

- The interview stops when the architecture-changing questions are exhausted, or after eight questions, whichever comes first. What remains is written down as open, not asked.
- The prototype limb runs one round. A second round happens only if the user asks for it.
- The blind spot pass is one research turn producing one list.
- The pass ends with a handoff: summarize what changed in your understanding, name what is still open, and ask for confirmation before writing the product spec.
- **It can be declined.** A user who says "skip this" gets it skipped, with one line in `docs/unknowns.md` recording that it was skipped and by whose choice. Propose skipping it yourself when the intake describes something small and well-understood. A step that cannot be declined gets worked around instead of declined.

**What it writes.** `docs/unknowns.md`, and the throwaway prototypes. Not the product spec — that is the rest of this step, and this pass informs it rather than pre-empting it.

`docs/unknowns.md` is read again at Step 4, where the recorded defaults are restated in the tech spec as explicit choices with reasons, and at Step 8, where an open question that still blocks something becomes a tracker issue. Whoever closes an entry deletes it in the same edit, moving anything durable into the document that now owns it. Keep it under ~150 lines; history lives in git.

```markdown
# Unknowns: [Project Name]

> Living document. Written at Step 2, read at Steps 4 and 8, appended to during
> implementation. Pruned by whoever closes an entry.

## Starting Point

[The user's own answers about prior experience, familiarity, and where they are
in their thinking. Verbatim where possible — this is calibration data.]

## Blind Spots Identified

| # | Blind spot | How it surfaced | Status |
|---|-----------|-----------------|--------|
| B1 | [What the user did not know they did not know] | Blind spot pass / interview / reaction | Open / Closed / Accepted |

## Open Questions

| # | Question | Why it matters | Blocks | Status |
|---|----------|----------------|--------|--------|
| Q1 | [In the user's vocabulary] | [What changes depending on the answer] | [Spec section, or nothing yet] | Open / Answered |

## Recognized Constraints

[Surfaced by reaction to a prototype. Record the user's own words and what they
were reacting to. These cannot be re-derived from any other document.]

| # | Constraint | Surfaced by | Confidence |
|---|-----------|-------------|------------|

## Prototype Directions

| Direction | File | Reaction | Carried into spec |
|-----------|------|----------|-------------------|

## Decided Defaults

[Every place a gro\/\/ stack default was stated and accepted rather than chosen.
One line each. This is what makes a wrong default visible later.]

## Deviations

[Appended during implementation: what forced a departure from the plan, which
conservative option was taken, and which section above it invalidates. Where a
deviation contradicts docs/, the spec is what gets revisited — the opposite of
the MEMORY.md rule, deliberately. That file records session state and yields to
docs/; this one records that docs/ was incomplete.]

| Date | Deviation | Conservative choice made | Invalidates |
|------|-----------|--------------------------|-------------|

-----
gro\/\/ stack — Unknowns
```

The techniques in this pass — the blind spot pass, one-question-at-a-time interviews, reacting to prototypes rather than specifying, and implementation notes — are adapted from Thariq Shihipar's field guide to finding your unknowns (Anthropic, 2026).

#### Writing the spec

**Before writing, the agent should ask the user:**

- What does this product do in one sentence?
- Who is the primary user? Are there secondary users?
- What are the 3-5 core features?
- What does success look like?
- What is explicitly out of scope?
- Are there existing systems this needs to integrate with?

**For existing projects:** The agent should draft the product spec based on what it learned during Step 0, then ask the user to confirm and refine. Don't ask questions the codebase already answers.

**Template:**

```markdown
# Product Specification: [Project Name]

> [One-line description]

## Overview
[What is this product and what problem does it solve?]

## Target Users
[Who is this for? Include personas if helpful.]

## Core Features
[Primary capabilities, ordered by priority.]

## Success Metrics
[How do we measure success?]

## Constraints
[Technical, business, or timeline constraints.]

## Out of Scope
[What this product does NOT do in this version.]

## Open Questions
[Anything unresolved — the agent should flag these for discussion.]

-----
gro\/\/ stack — [Project Name]
```

### Step 3: Development Plan

Create `docs/development-plan.md`. Translates the product spec into an actionable engineering plan.

**The agent should ask:**

- What is the timeline or delivery cadence?
- Is there a team, or is this solo development?
- Are there hard dependencies or external APIs?
- What should be built first (MVP scope)?

**For existing projects:** The development plan should account for what is already built. Focus on what remains, what needs refactoring, and what new capabilities are planned. Include a section on technical debt if relevant.

**The development plan should include:**

- Development phases and milestones
- Feature breakdown by priority
- Technical approach per feature
- Dependencies and integration points
- Testing strategy overview
- Estimated timeline
- (Existing projects) Refactoring priorities and technical debt items

Every feature should trace back to the product spec.

### Step 4: Technical Specification

Create `docs/tech-spec.md`. This is the comprehensive technical document built from both product-spec and development-plan.

**Read `docs/unknowns.md` first.** Its Decided Defaults section lists every place a gro\\/\\/ stack default was stated and accepted rather than actively chosen; restate each one here as an explicit choice with the reason, so the tech spec records a decision instead of an inheritance. Open questions that still block a section of this document get asked before that section is written, not flagged after.

**The agent should ask about each of these:**

- What is the preferred technology stack? Or should the agent recommend one?
- What database provider? (Neon, Supabase, self-hosted)
- Does this need authentication? (Clerk, etc.)
- Are there background jobs or event-driven requirements?
- What is the deployment target? (Vercel, Docker, sprites.dev)
- What are the observability requirements?

State the gro\\/\\/ stack default alongside each question rather than applying it silently. "If not already clear" is not the test — the Core Technology Stack Reference below always makes it clear, so a conditional ask is an ask that never happens, and the project inherits Clerk, Neon, Stripe, Lago, PostHog and Vercel without anyone having weighed them. Name the default, say where it is most likely to be a poor fit for this project, and let the user confirm or override. Record what they accepted in `docs/unknowns.md` under Decided Defaults.

**For a new project, this is also where the verify commands become knowable.** Step 1 could not read them because the stack did not exist yet. Derive them from the stack chosen here — the project's test runner, typechecker, linter and build — and carry them forward to Step 8's `MEMORY.md` Verify table.

**For existing projects:** The tech spec documents the current architecture and the target architecture. If the project needs to evolve from its current state, include a migration path.

**Tech spec contents:**

- System architecture overview
- Technology stack with rationale
- Database schema design
- API design and endpoints
- Authentication and authorization
- Background job processing (if applicable)
- Error handling strategy
- Monitoring and observability
- Deployment architecture
- Security considerations
- (Existing projects) Current vs. target architecture, migration plan

**Key principles:**

| Principle | Description |
|-----------|-------------|
| Clarity | Clear language for both technical and non-technical readers |
| Completeness | All sections addressed or marked `@TODO` |
| Traceability | Decisions include rationale and alternatives considered |
| Practicality | Actionable, implementable specifications |
| Stack Alignment | Solutions leverage the chosen technology stack |

**Colophon required:**

| Field | Value |
|-------|-------|
| Version | Semver (e.g., 0.1.0) |
| Last Updated | Date |
| Status | Draft / In Review / Approved / Archived |
| Author(s) | Names |
| Model | AI model used |

### Step 5: Prompt Documents

Create the prompt files in `docs/prompts/` that will be used to generate project-specific documentation and skills.

#### `docs/prompts/skills-builder.md`

Generates the target project's **invocable skills** — a set of development best-practice skills under `.claude/skills/`, each a real `SKILL.md` with `name` + `description` frontmatter and `references/` for depth, so Claude triggers and uses them. These are not documentation files and are not written to `docs/skills/`.

**Baseline skills to generate** (one folder each under `.claude/skills/`):

| Skill | Covers |
|-------|--------|
| `dev-standards` | Core philosophy, the dev workflow (red-green-refactor), the code-quality bar, using source code as a reference, packaging a change for review and buy-in, when to reach for the other skills |
| `architecture-planning` | System design, data modeling, API contracts, background-job patterns, the pre-dev checklist, brainstorming and throwaway prototypes, implementation plans ordered by what is most likely to change, ADRs |
| `frontend-development` | Framework patterns (Astro + React or Next.js), hydration, type-safe components, forms, accessibility |
| `ui-standards` | Tailwind CSS + shadcn/ui, Alexandria font, monochrome palette, component examples |
| `backend-development` | API standards, service/repository patterns, background jobs, webhooks, email/Stripe/Lago integrations |
| `database-design` | Schema design, indexing, migrations, query optimization, transactions, ORM patterns |
| `security-practices` | Auth flows (Clerk), input validation, SQLi/XSS/CSRF prevention, secrets, rate limiting, dependency audits |
| `testing-tdd` | TDD workflow, Vitest, `go test`, integration tests, Playwright E2E (ask-first), CI |
| `deployment-ops` | Docker, CI/CD, environment management, health checks, PostHog observability, backups |
| `debugging` | Debugging methodology, profiling, error tracking, production debugging, emergency procedures |
| `blind-spot-pass` | Pre-work reconnaissance in an unfamiliar module or domain; establishing the user's starting point, then naming what they have not considered |
| `interviews` | One-question-at-a-time elicitation, ordered by architectural leverage, with a stopping rule |
| `implementation-notes` | The working notes file, the Deviations log, and the conservative-default rule for a forced departure from the plan |
| `change-quiz` | A change report plus a quiz on the parts a reader could get wrong; advisory by default |

**For existing projects:** Customize each skill to the project's actual stack and patterns — Next.js instead of Astro, the real auth provider, established conventions. The skills are a reference for *this* project, not a generic template. Extend existing skills rather than overwriting them.

**Content requirements:**

- Each skill is invocable: valid frontmatter (`name` matching the folder, a pushy trigger-rich `description`), a body under 500 lines, with depth pushed to `references/`
- Technology agnostic, defaulting to the Core Technology Stack Reference below — read it there rather than restating it here, so there is one copy to keep current
- All code examples complete, typed, and production-ready (not pseudo-code), with error handling and security built in; anti-patterns shown alongside correct patterns. This governs generated code and documentation; exploratory artifacts in the throwaway tier are exempt by definition
- The throwaway tier is stated wherever a generated skill would otherwise imply that everything built must clear the production bar — in `dev-standards` above all, and in `ui-standards`, `frontend-development`, `architecture-planning`, and `testing-tdd` where they touch exploration. Keep the wording consistent with the tier as stated above rather than inventing a second rule set
- The frontend-framework ask-first rule lives in `frontend-development` / `ui-standards`; the Playwright ask-first rule lives in `testing-tdd`
- Reference the project's `docs/tech-spec.md` for project-specific customization

See `docs/prompts/skills-builder.md` for the full authoring rules and deliverable checklist.

#### `docs/prompts/team-design.md`

Instructions for designing the project-specific **agent team and the skills they use** (the harness step). Adapts the vendored harness meta-skill (`.claude/skills/harness/`) to grovv conventions. It is executed in Step 7, after the skills repository exists, and is additive to grovv's six default agents — it generates only the specialists the domain actually needs. See the prompt for the full phase workflow, the six architecture patterns, and the deliverable checklist.

#### `docs/prompts/tracker-setup.md`

Instructions for setting up the project's **issue tracker** and its **`MEMORY.md`** cross-session memory. Executed in Step 8. It opens by asking which tracker the project should use — **GitHub Issues** (the recommended default, since it lives in the same repo as the code) or **Linear** (via the Linear MCP, for multi-repo or cross-team backlogs) — then creates or reuses that backlog, seeds milestones and issues from `docs/development-plan.md` and `docs/tech-spec.md`, and creates the root `MEMORY.md` (plus its `CLAUDE.md` rules and `SessionStart` hook) that coordinates with the chosen tracker. It is ask-first — confirm the tracker and the proposed issue list before bulk-creating, and never duplicate existing issues. See the prompt for both paths, the workflow, and the deliverable checklist.

#### `docs/prompts/tech-spec.md`

Instructions for creating or refining the technical specification. References the template from Step 4 and includes guidance for iterative refinement, `@TODO` marking, and version history.

#### `docs/prompts/readme-generator.md`

Instructions for generating the project README from the tech spec and codebase. Output includes: project overview, quick start, tech stack, project structure, development setup, deployment, API overview, contributing guidelines, and support information.

### Step 6: Execute Skills Builder

Read and execute `docs/prompts/skills-builder.md` to populate `.claude/skills/` with invocable best-practice skills. This is the most substantial generation step.

**Expected output:**

- ~14 invocable skills (the baseline set), each a `.claude/skills/{name}/SKILL.md` with valid frontmatter
- Production-ready, typed code examples with security built in; anti-patterns alongside correct patterns
- Lean bodies (under 500 lines) with depth in `references/`
- Ask-first rules embedded where relevant (frontend framework, Playwright)
- The throwaway tier stated in `dev-standards` and in every other skill that would otherwise imply everything built must clear the production bar

**Then ask how much continuous integration this project should have.** Step 1 discovered the commands that prove the project works; this is where they become a signal somebody sees. By now the tech spec names the stack and the skills-builder step is already writing configuration, so the question can name the project's real commands rather than a generic list.

Ask exactly this, substituting the commands Step 1 found:

> This project has no continuous integration. I can add a workflow that runs your checks on every push and pull request, so a break is caught before review rather than after merge.
>
> 1. **Everything** — test, typecheck, lint, and build. The strongest signal; also the slowest, and the most likely to need tuning in the first week.
> 2. **Minimal** — tests only. Catches the failures that matter most, stays fast, and is the easiest to keep green. A good starting point if linting is not yet settled.
> 3. **Pick them** — I list the checks I found and you choose. Right when some of these are not ready to gate a merge yet.
> 4. **None** — no workflow. Correct for a spike, a project whose CI lives somewhere I cannot see, or a team that will wire this up themselves.
>
> I found these commands in this project: [list them with their sources]. If any is wrong, say so — a wrong command is worse than no workflow.

- **Wait for an explicit answer.** "Whatever you think" is not an answer. Name the recommendation for *this* project, say what would change it, and ask them to confirm — a stated default is still an answer they gave.
- **Never generate a check the project cannot run.** Only commands recorded at Step 1 may appear in the workflow. A workflow that runs `npm run lint` in a project with no lint script fails on its first run and teaches the team to ignore red builds.
- **Declining is a successful outcome, not a skipped step.** On "None", carry one line forward to `MEMORY.md`'s Verify table at Step 8 recording that CI was offered, declined, and why. That line is what makes a wrong decline visible to a human later.
- **If the project already has CI, this is a proposal, not a question.** State what exists, state what would change, and generate nothing until the user approves. The standing rule against overwriting working code covers a workflow file exactly as it covers source.
- **A generated workflow never contains a Playwright or E2E job.** "Everything" means everything among the commands Step 1 recorded, and E2E is not one of them. Generating an E2E job asserts that end-to-end tests exist and should gate merges — a scope decision only the user makes, and the Playwright ask-first rule is not answered by a workflow file. Where E2E tests already exist with CI that runs them, adopt mode preserves that; where they exist without CI, the job is offered as its own separate question.

`docs/prompts/skills-builder.md` carries the generation rules — which checks are available per stack, the workflow's shape, and the adopt-mode proposal path.

**On a second run, this step reconciles rather than regenerates.** `skills-builder.md`'s `## Re-entry` section is the contract: audit what exists, give each generated skill a verdict against the current `docs/tech-spec.md`, report before writing, and never overwrite a hand edit. A run that changes nothing and returns a list of questions has succeeded.

### Step 7: Design the Agent Team (Harness)

Read and execute `docs/prompts/team-design.md` to design the project-specific agent team and the skills they use. This runs after the baseline skills exist in `.claude/skills/` (Step 6), because the team is designed to execute against those best practices — and it audits and dedupes against them (harness Phase 4-0) before adding any new skill.

**This step is additive.** grovv's six default agents (`scaffold`, `frontend`, `backend`, `testing`, `database`, `code-review`) stay intact. The team-design step adds only the specialists the domain needs, following the harness phase workflow (audit → domain analysis → team architecture → agent definitions → skills → orchestration → validation).

**Expected output (written into the target project's `.claude/`):**

- Project-specific agent definitions in `.claude/agents/`
- The skills those agents use in `.claude/skills/`
- One orchestrator skill that coordinates the team
- A harness pointer (trigger rule + change log) registered in the target `CLAUDE.md`

**Ask-first rules are preserved:** never pick the frontend framework here (inherit the earlier choice), and never auto-generate Playwright flows. Nothing is written to `.claude/commands/`.

**On a second run, this step reconciles rather than regenerates.** `team-design.md`'s `## Re-entry` section is the contract, and it is the grovv side of harness Phase 0 rather than a competing procedure: each project-specific agent is re-argued against the current spec, the six defaults are exempt from removal, and the target `CLAUDE.md` gets a dated change-log row rather than a second harness pointer.

### Step 8: Set Up Project Tracking and Cross-Session Memory

Read and execute `docs/prompts/tracker-setup.md` to stand up the project's issue tracker and its cross-session memory. By now the development plan, tech spec, and agent team all exist, so the work can be seeded into a live backlog.

**Ask which tracker first.** The step opens with an explicit question — **GitHub Issues** (recommended: it lives in the same repo as the code, so issues, branches, and PRs cross-link with no extra service) or **Linear** (worth choosing for multi-repo work, cross-team initiatives, or a backlog shared with people who do not live in GitHub). Never infer the answer from a `.git` remote or an available MCP connection, and create nothing until the user has answered. GitHub Issues runs through `gh` (or the GitHub MCP server as a fallback); Linear runs through the Linear MCP server.

Either way the step mirrors the development plan's phases as milestones and seeds issues from the plan's features and the tech spec's components. It also reads `docs/unknowns.md`: any question still open and still blocking becomes a tracker issue, so it is owned by someone rather than sitting in a file. `MEMORY.md` gets a one-line pointer to that file, never a copy of it.

It also creates **`MEMORY.md`** in the project root — the durable cross-session memory that coordinates with the chosen tracker. The division of responsibility: **the tracker owns the backlog** (tasks, priorities, status); **`MEMORY.md` owns session context** (decisions, gotchas, in-flight state, referencing issues by the tracker's reference format). The step wires up maintenance so the file is actually used: memory rules in the project's `CLAUDE.md` (read at session start, update before ending) and a `SessionStart` hook merged into `.claude/settings.json` that surfaces the file automatically.

**It is ask-first and external:** present the proposed milestones and issue list before creating anything; never duplicate existing issues; reuse an existing project or label taxonomy when one already maps to the codebase. If the required tooling is unavailable, skip that path with an `@TODO` in `docs/development-plan.md` and tell the user what unblocks it — but still create `MEMORY.md` with its Tracker Coordination table marked `@TODO`. Standing ask-first rules (frontend framework, Playwright) are not pre-empted by any issue or memory entry.

### Step 9: Generate README

Read and execute `docs/prompts/readme-generator.md` to create or update the root `README.md`. The README should reflect the actual project as defined in the tech spec.

**For existing projects:** If a README already exists, update it to incorporate grovv stack conventions — don't discard existing content that is still accurate. Merge, don't replace.

-----

## Existing Project Adoption Guide

When applying grovv stack to an existing project, the overall approach is:

### Phase 1: Document What Exists

- Create the product spec, development plan, and tech spec based on the current project
- These documents capture the *current* state and the *intended* direction
- This alone adds significant value — many projects lack this documentation

### Phase 2: Add the Scaffolding

- Create the `docs/` structure alongside existing code
- Generate skills customized to the project's actual stack
- Update the README with grovv stack conventions

### Phase 3: Refactor Incrementally

- Use the tech spec and skills as reference for new development
- Refactor existing code toward grovv stack patterns as you touch it
- Don't rewrite working systems for the sake of alignment — refactor when there is a practical reason

### What Not to Do

- Don't restructure the entire codebase at once
- Don't replace working patterns with grovv stack defaults if the existing patterns are solid
- Don't create documentation that contradicts the actual codebase
- Don't force a stack change unless there is a clear benefit

The goal is to **bring the benefits** — documentation, best practices, testing patterns, security standards — **without disrupting** what already works.

-----

## Core Technology Stack Reference

Stack-agnostic scaffolding, optimized for this default stack. Adapt per project.

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Languages** | TypeScript, Go | Primary development |
| **Runtime** | Node.js (LTS) | JavaScript execution |
| **Database** | PostgreSQL (Neon/Supabase), SQLite | Data persistence |
| **Auth** | Clerk | Identity management |
| **Frontend** | Astro, React/Next.js, shadcn/ui | UI framework |
| **Background Jobs** | PostgreSQL-native | Background job processing |
| **Email** | Resend or Plunk (Amazon SES if really needed) | Transactional and marketing email |
| **Payments** | Stripe | Subscriptions, one-time payments, invoicing |
| **Usage Tracking** | Lago | Metering and usage-based billing |
| **Observability** | PostHog | Analytics and monitoring |
| **Project Tracking** | GitHub Issues (recommended) or Linear | Issue and project tracking — chosen per project |
| **Deployment** | Vercel, Docker | Production hosting |
| **Dev Environment** | VS Code, sprites.dev | Local and cloud IDE |

-----

## Branding and Document Style

All generated documents should follow the **gro\\/\\/ stack** style.

### Brand Identity

- **Parent brand:** grovv — stylized as **gro\\/\\/**
- **This system:** grovv stack
- **Project names:** lowercase with dashes (e.g., `my-project`)

### Document Footer

Every generated document ends with a horizontal rule and a branded footer:

```markdown
-----
gro\/\/ stack — [Document Purpose or Project Name]
```

Examples:

```
-----
gro\/\/ stack — Product Specification
```

```
-----
gro\/\/ stack — my-saas-app
```

**Escaping the wordmark.** The footer normally sits in Markdown prose, not a code block. In prose, double the backslashes — `gro\\/\\/ stack — …` — so it renders as the gro\\/\\/ wordmark rather than gro//. The fenced examples above use the single-backslash `gro\/\/` form because backslashes are already literal inside code blocks.

### Document Conventions

- `-----` (five dashes) for horizontal rules
- Fenced code blocks with language hints for all code
- Tables for structured reference data
- `@TODO` markers for incomplete sections
- Colophon sections with version, status, author, and model metadata
- Clean, minimal formatting — no excessive bold, no emoji in headings
- Horizontal rules between major sections

### README Style

Project READMEs generated through grovv stack should include:

- Project name as H1
- One-line description immediately below
- Status badges where applicable
- Clear quick start with copy-paste commands
- Technology stack table
- Project structure tree
- gro\\/\\/ stack footer

-----

## Principles

Every document generated through this scaffolding follows:

- **Production-first** — Production readiness is the default for everything that ships, not aspirational. Exploratory artifacts (prototypes, mockups, spikes) are explicitly exempt and are never merged. See the Throwaway Tier.
- **Zero data loss** — Transactional integrity in every data operation
- **Security by default** — Auth, validation, and secure patterns in every layer
- **Test-driven development** — Critical tests first, comprehensive coverage
- **Documentation as code** — Docs maintained alongside code
- **Conversation-driven** — Ask questions, understand deeply, then build

-----

## Agent Instructions Summary

When an AI agent reads this document, it should:

1. **Determine if this is a new or existing project.** If existing, start with Step 0 (assess the codebase) and propose an adoption plan before generating anything.
2. **Ask questions first.** Understand the product, the user, the constraints, and the stack before generating files.
3. **Create the directory structure and `settings.json`.** For existing projects, integrate rather than overwrite.
4. **Work through Steps 2-9 sequentially**, pausing to confirm direction as needed. Step 7 designs the project-specific agent team (harness) after the skills repository exists; Step 8 asks which tracker to use — GitHub Issues or Linear — then seeds that backlog from the development plan and creates the cross-session `MEMORY.md` that coordinates with it.
5. **Mark unknowns with `@TODO`** and revisit them as the conversation progresses.
6. **Apply gro\\/\\/ stack branding** — footers, naming conventions, and document style to all generated files.
7. **Iterate.** Documents are living artifacts. Revise as understanding deepens.

If the user provides existing documents (product spec, tech spec, etc.), the agent should read them first and pick up from the appropriate step rather than starting from scratch.

-----

## Success Criteria

Scaffolding is complete when:

- [ ] Directory structure matches the specification (integrated with existing project if applicable)
- [ ] `settings.json` exists with correct configuration
- [ ] `docs/unknowns.md` exists, and either records the unknowns pass — starting point, blind spots, open questions, decided defaults — or records that the pass was declined and by whose choice
- [ ] Every stack default the project accepted was stated and confirmed rather than applied silently, and is listed under Decided Defaults
- [ ] `docs/product-spec.md` clearly defines the product
- [ ] `docs/development-plan.md` provides an actionable engineering plan
- [ ] `docs/tech-spec.md` is comprehensive and traceable to product spec
- [ ] `docs/prompts/` contains all five prompt documents (skills-builder, team-design, tracker-setup, tech-spec, readme-generator)
- [ ] `.claude/skills/` is populated with the invocable baseline best-practice skills (each a `SKILL.md` with valid frontmatter)
- [ ] `.claude/agents/` and `.claude/skills/` also hold the project-specific agent team, its skills, and the orchestrator (grovv defaults intact)
- [ ] Tracker choice put to the user explicitly, and project tracking is set up in the chosen tracker (backlog + milestones + issues seeded from the development plan), or skipped with an `@TODO` if the required tooling is unavailable
- [ ] `MEMORY.md` exists in the project root with the Tracker Coordination table, memory rules are in the project's `CLAUDE.md`, and the `SessionStart` hook is merged into `.claude/settings.json`
- [ ] `MEMORY.md`'s Verify table holds the commands that prove the project works, and the CI question was put to the user explicitly — a workflow generated from exactly those commands, or CI declined with the reason recorded
- [ ] `docs/architecture/` exists for future ADRs
- [ ] Root `README.md` reflects the actual project
- [ ] All documents carry gro\\/\\/ stack branding and style
- [ ] All documents follow the established principles
- [ ] (Existing projects) Adoption plan was reviewed and approved before changes were made
- [ ] (Resume runs) Steps 6 and 7 reconciled their existing output against the current tech spec and reported before writing — a run that changed nothing and returned questions is complete, not failed

-----
gro\\/\\/ stack scaffold
