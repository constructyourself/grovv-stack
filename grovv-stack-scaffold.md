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

This is the starting document for any project — new or existing. Drop this file into a project folder, open a conversation with an AI agent, and say:

> *"Read grovv-stack-scaffold.md and help me build out this project."*

The agent will ask questions to fully understand your product, your goals, your constraints, and your technical preferences — then systematically build out the documentation foundation that drives development.

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

-----

## Directory Structure

The scaffolding process creates or integrates the following structure:

```
project-folder/
├── docs/
│   ├── architecture/          # Architecture decision records (ADRs)
│   ├── prompts/               # Prompt specs for building docs and skills
│   │   ├── skills-builder.md
│   │   ├── tech-spec.md
│   │   └── readme-generator.md
│   └── skills/                # Development best practices and guides
│       ├── Claude.md
│       ├── README.md
│       ├── INDEX.md
│       ├── QUICK-REFERENCE.md
│       ├── planning/
│       │   └── ARCHITECTURE.md
│       ├── frontend/
│       │   ├── FRONTEND.md
│       │   └── UI-STANDARDS.md
│       ├── backend/
│       │   └── BACKEND.md
│       ├── database/
│       │   └── DATABASE.md
│       ├── security/
│       │   └── SECURITY.md
│       ├── testing/
│       │   └── TESTING.md
│       └── operations/
│           ├── DEPLOYMENT.md
│           └── DEBUGGING.md
├── product-spec.md            # Product-level definition
├── development-plan.md        # Engineering plan based on product-spec
├── tech-spec.md               # Complete technical specification
├── settings.json              # Claude Code agent configuration
└── README.md                  # Project README (generated last)
```

**For existing projects:** This structure is additive. The `docs/` folder and root spec documents are created alongside whatever already exists. Existing files like `README.md` are updated rather than replaced — the agent should merge grovv stack conventions into what is already there.

### File and Folder Reference

| Path | Purpose |
|------|---------|
| `project-folder/` | Root directory — lowercase with dashes (e.g., `my-saas-app`) |
| `docs/` | Primary docs folder, built out over time through scaffolding |
| `docs/architecture/` | Architecture Decision Records documenting key technical choices |
| `docs/prompts/` | Prompt specifications for generating project-specific documents and skills |
| `docs/skills/` | Development best practices — planning, frontend, backend, database, security, testing, operations |
| `product-spec.md` | Product-level definition: what, who, why |
| `development-plan.md` | Engineering development plan derived from product-spec |
| `tech-spec.md` | Complete technical specification built from product-spec + development-plan |
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

Create directories and the `settings.json` configuration file.

**Directories to create:**

```
docs/
docs/architecture/
docs/prompts/
docs/skills/
```

For existing projects, only create directories that don't already exist. If the project has an existing `docs/` folder, integrate into it rather than replacing it.

**Create `settings.json`** in the project root:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

For existing projects that already have a `settings.json`, merge the `env` block into the existing file.

### Step 2: Product Spec

Create `product-spec.md` in the project root. This is the foundation — everything downstream traces back to it.

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

Create `development-plan.md` in the project root. Translates the product spec into an actionable engineering plan.

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

Create `tech-spec.md` in the project root. This is the comprehensive technical document built from both product-spec and development-plan.

**The agent should ask (if not already clear):**

- What is the preferred technology stack? Or should the agent recommend one?
- What database provider? (Neon, Supabase, self-hosted)
- Does this need authentication? (Clerk, etc.)
- Are there background jobs or event-driven requirements?
- What is the deployment target? (Vercel, Docker, sprites.dev)
- What are the observability requirements?

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

Generates the `/docs/skills/` folder — a comprehensive development best practices repository.

**Skills to generate:**

| File | Content |
|------|---------|
| `Claude.md` | Core philosophy, workflow standards, code quality expectations |
| `README.md` | Skills overview and navigation |
| `INDEX.md` | Complete navigation index |
| `QUICK-REFERENCE.md` | Cheat sheet for common patterns |
| `planning/ARCHITECTURE.md` | System design, data modeling, API contracts, pre-dev checklists |
| `frontend/FRONTEND.md` | Framework patterns, progressive hydration, accessibility, performance |
| `frontend/UI-STANDARDS.md` | UI design philosophy, Bootstrap minimal stack, component examples |
| `backend/BACKEND.md` | API standards, service/repository patterns, background jobs, webhooks |
| `database/DATABASE.md` | Schema design, indexing, migrations, query optimization, ORM patterns |
| `security/SECURITY.md` | Auth flows, input validation, secure coding, Clerk integration |
| `testing/TESTING.md` | TDD workflow, critical tests first, unit/integration/E2E |
| `operations/DEPLOYMENT.md` | Production deployment, Docker, CI/CD, environment management |
| `operations/DEBUGGING.md` | Debugging methodology, profiling, emergency procedures |

**For existing projects:** Skills should be customized to reflect the project's actual stack and patterns. If the project uses Next.js instead of Astro, the frontend skills should cover Next.js. If the project uses a different auth provider, security skills should reflect that. The skills are a reference for *this* project, not a generic template.

**Content requirements:**

- Technology agnostic but primarily JavaScript/TypeScript and Python
- PostgreSQL/SQLite via Neon or Supabase for database
- Bun and Node.js runtimes
- Clerk for identity management
- Astro for content-based websites
- All code examples: complete, working, production-ready (not pseudo-code)
- Error handling, type annotations, and security in every example
- Anti-patterns shown alongside correct patterns
- Reference the project's `tech-spec.md` for project-specific customization

#### `docs/prompts/tech-spec.md`

Instructions for creating or refining the technical specification. References the template from Step 4 and includes guidance for iterative refinement, `@TODO` marking, and version history.

#### `docs/prompts/readme-generator.md`

Instructions for generating the project README from the tech spec and codebase. Output includes: project overview, quick start, tech stack, project structure, development setup, deployment, API overview, contributing guidelines, and support information.

### Step 6: Execute Skills Builder

Read and execute `docs/prompts/skills-builder.md` to populate `docs/skills/`. This is the most substantial generation step.

**Expected output:**

- 12-15 comprehensive guides
- 200+ production-ready code examples
- Security patterns in every guide
- Test examples for each pattern

### Step 7: Generate README

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
| **Languages** | TypeScript, Python | Primary development |
| **Runtime** | Bun, Node.js | JavaScript execution |
| **Database** | PostgreSQL (Neon/Supabase), SQLite | Data persistence |
| **Auth** | Clerk | Identity management |
| **Frontend** | Astro, React/Preact | UI framework |
| **Background Jobs** | PostgreSQL-native | Background job processing |
| **Observability** | PostHog | Analytics and monitoring |
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

- **Production-first** — Production readiness is the default, not aspirational
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
4. **Work through Steps 2-7 sequentially**, pausing to confirm direction as needed.
5. **Mark unknowns with `@TODO`** and revisit them as the conversation progresses.
6. **Apply gro\\/\\/ stack branding** — footers, naming conventions, and document style to all generated files.
7. **Iterate.** Documents are living artifacts. Revise as understanding deepens.

If the user provides existing documents (product spec, tech spec, etc.), the agent should read them first and pick up from the appropriate step rather than starting from scratch.

-----

## Success Criteria

Scaffolding is complete when:

- [ ] Directory structure matches the specification (integrated with existing project if applicable)
- [ ] `settings.json` exists with correct configuration
- [ ] `product-spec.md` clearly defines the product
- [ ] `development-plan.md` provides an actionable engineering plan
- [ ] `tech-spec.md` is comprehensive and traceable to product spec
- [ ] `docs/prompts/` contains all three prompt documents
- [ ] `docs/skills/` is populated with 12-15 development guides
- [ ] `docs/architecture/` exists for future ADRs
- [ ] Root `README.md` reflects the actual project
- [ ] All documents carry gro\\/\\/ stack branding and style
- [ ] All documents follow the established principles
- [ ] (Existing projects) Adoption plan was reviewed and approved before changes were made

-----
gro\\/\\/ stack scaffold
