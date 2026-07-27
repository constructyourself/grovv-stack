# grovv-stack

**gro\\/\\/ stack** — Production-First Project Scaffolding

-----

## What This Is

grovv-stack is a prompt-driven project scaffolding system that generates production-ready codebases with built-in best practices, security, and test-driven development patterns. It works for both new and existing projects through a conversational process.

It ships as a Claude Code plugin. Install it once, then kick it off in any repo:

```
/plugin marketplace add constructyourself/grovv-stack
/plugin install grovv-stack@grovv
```

- `/grovv` — explicit kickoff: invokes the `grovv` skill; optional `new` or `adopt` argument, otherwise auto-detects.
- Natural language — the same `grovv` skill triggers on intent ("build out this project", "adopt grovv stack here").

Both routes are the one `grovv` skill (no separate command); both read `grovv-stack-scaffold.md` and run the same Steps 0–9 workflow.

-----

## Core Principles

| Principle | Description |
|-----------|-------------|
| **Production-First** | Everything that ships is production-ready from the start. Exploratory artifacts are exempt, and never ship |
| **Zero Data Loss** | Transactional integrity is non-negotiable |
| **Security by Default** | Security considerations never deferred |
| **Test-Driven** | Tests define contracts and prevent regressions |
| **Documentation as Code** | Docs maintained alongside code |
| **Conversation-Driven** | Ask questions, understand deeply, then build |

-----

## The Throwaway Tier

Production-first governs what ships, not what you build to find out what should ship. An exploratory artifact — prototype, mockup, brainstorm, or spike — is exempt from the production bar and is never merged.

- Multi-file exploration goes on an unmerged `proto/*` or `spike/*` branch; a single-file mockup goes in the gitignored `prototypes/` directory. Delete it once the decision it informed is recorded.
- An exploratory artifact never satisfies an ask-first rule. Four mockups built in React is not a decision to use Next.js — that question is still asked, and still answered by the user.

Full rules: the Throwaway Tier section in `grovv-stack-scaffold.md`.

-----

## Technology Stack

Stack-agnostic scaffolding, optimized for this default stack. Adapt per project.

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Languages** | TypeScript, Go | Primary development |
| **Runtime** | Node.js (LTS) | JavaScript execution |
| **Database** | PostgreSQL (Neon/Supabase), SQLite | Data persistence |
| **Auth** | Clerk | Identity management |
| **Frontend** | Astro + React **or** Next.js (ask first), shadcn/ui, Tailwind CSS | UI framework |
| **Background Jobs** | PostgreSQL-native | Background job processing |
| **Email** | Resend or Plunk (Amazon SES if really needed) | Transactional and marketing email |
| **Payments** | Stripe | Subscriptions, one-time payments, invoicing |
| **Usage Tracking** | Lago | Metering and usage-based billing |
| **Observability** | PostHog | Analytics and monitoring |
| **Project Tracking** | GitHub Issues (recommended) or Linear | Issue and project tracking — chosen per project |
| **Deployment** | Vercel, Docker | Production hosting |
| **Dev Environment** | VS Code, sprites.dev | Local and cloud IDE |
| **AI CLI** | Claude Code | Agentic coding and automation |

-----

## Repository Structure

```
grovv-stack/
├── .claude-plugin/             # Plugin packaging (makes this repo installable)
│   ├── plugin.json             # Plugin manifest — name, version, component paths
│   └── marketplace.json        # Marketplace catalog for /plugin marketplace add
├── .claude/                    # Claude Code configuration
│   ├── CLAUDE.md               # This file — project context for Claude
│   ├── settings.json           # Claude Code settings
│   ├── agents/                 # Sub-agent definitions (shipped via plugin.json)
│   │   ├── scaffold.md         # Scaffolding agent
│   │   ├── frontend.md         # Frontend development agent
│   │   ├── backend.md          # Backend development agent
│   │   ├── testing.md          # Testing and TDD agent
│   │   ├── database.md         # Database design agent
│   │   └── code-review.md      # Code review agent
│   └── skills/                 # Skills shipped via plugin.json
│       ├── grovv/              # Kickoff skill — /grovv, also triggers on intent (single entry point)
│       └── harness/            # harness meta-skill (Apache-2.0) — team-design step
├── docs/
│   ├── prompts/                # Executable prompts for scaffolding
│   │   ├── skills-builder.md
│   │   ├── team-design.md
│   │   ├── tracker-setup.md
│   │   ├── tech-spec.md
│   │   ├── tech-spec-template.md
│   │   └── readme-generator.md
│   └── architecture/           # Architecture decision records
├── grovv-stack-scaffold.md     # Main scaffolding directive
├── MEMORY.md                   # Cross-session memory for this repo (coordinates with Linear)
├── settings.json               # Claude Code agent team config
└── README.md                   # Project readme
```

-----

## Sub-Agents

The `.claude/agents/` folder contains specialized sub-agent definitions:

| Agent | File | Purpose |
|-------|------|---------|
| **Scaffold** | `agents/scaffold.md` | Guides scaffolding process for new and existing projects |
| **Frontend** | `agents/frontend.md` | Frontend development — asks user to choose Astro + React or Next.js |
| **Backend** | `agents/backend.md` | TypeScript and Go API/service development |
| **Testing** | `agents/testing.md` | TDD enforcement, automated tests, Playwright E2E |
| **Database** | `agents/database.md` | Schema design, migrations, query optimization |
| **Code Review** | `agents/code-review.md` | Security, quality, and standards review |

These six are the **baseline team**. During the team-design step (prompt: `docs/prompts/team-design.md`), the scaffolder uses the vendored **harness** meta-skill (`.claude/skills/harness/`) to design *additional*, project-specific agents and the skills they use, plus an orchestrator — written into the **target project's** `.claude/`. The step is additive: the six defaults stay intact, and only the specialists a given domain needs are added. harness is vendored verbatim under Apache-2.0; see `.claude/skills/harness/ATTRIBUTION.md` for provenance. The grovv-facing interface is the team-design prompt, not the vendored files.

-----

## How the Scaffolding Works

### Prompt Execution Order

1. **tech-spec** → Creates the technical specification (`docs/tech-spec.md`)
2. **skills-builder** → Generates the project's invocable skills under `.claude/skills/` (the baseline best-practice set)
3. **team-design** → Designs the project-specific agent team + skills (harness); additive to grovv defaults
4. **tracker-setup** → Asks which tracker to use (GitHub Issues or Linear), then creates/reuses the backlog and seeds issues from the development plan; also creates the target project's `MEMORY.md`, its `CLAUDE.md` memory rules, and a `SessionStart` hook
5. **readme-generator** → Generates project README

### For New Projects

1. Create project folder (lowercase with dashes)
2. Place `grovv-stack-scaffold.md` in root
3. Start conversation — agent asks questions, then builds everything

### For Existing Projects

1. Place `grovv-stack-scaffold.md` in project root
2. Agent analyzes codebase, identifies stack/patterns/gaps
3. Agent proposes adoption plan — user approves before changes
4. Build incrementally without breaking existing code

-----

## Code Quality Standards

- All code must be production-ready, fully typed, with comprehensive error handling
- Security considerations in every layer (input validation, auth, XSS/CSRF/SQLi prevention)
- Test-driven development — critical tests first, then integration, then E2E
- Complete code examples only — no pseudo-code. This governs generated code and documentation; exploratory artifacts in the throwaway tier are exempt by definition.
- Anti-patterns documented alongside correct patterns

-----

## Testing Standards

- **TDD** — write tests before implementation (red-green-refactor)
- **Automated tests** — all tests run in CI/CD pipelines
- **Vitest** — unit and integration tests for TypeScript
- **Go testing** — unit and integration tests for Go
- **Playwright** — E2E browser testing

### CRITICAL: Playwright Policy

**Always ask the user what Playwright should test before writing any Playwright tests.** Do not assume which user flows need E2E testing. Ask first, confirm the plan, then implement.

### Testing Priority

1. Critical path tests — core business logic
2. Error handling tests — edge cases and failures
3. Integration tests — cross-service communication
4. E2E tests (Playwright) — full user workflows (ask first)

-----

## UI Standards

- **Font:** Alexandria (fonts.bunny.net)
- **Styling:** Tailwind CSS — the only styling approach
- **Components:** shadcn/ui — accessible, composable component library
- **Colors:** Monochrome (black/white/grey)
- **Background:** White default
- **Animations:** None

For existing projects, analyze and match established patterns.

-----

## Document Conventions

- Horizontal rules: `-----` (five dashes)
- Fenced code blocks with language hints
- Tables for structured reference data
- `@TODO` markers for incomplete sections
- Colophon with version, status, author, model metadata
- Footer (in prose): `gro\\/\\/ stack — [Purpose or Project Name]` — doubled backslashes so it renders as the gro\\/\\/ wordmark, not gro//. Inside code blocks, use single backslashes (`gro\/\/`).
- No excessive bold or emoji in headings

-----

## Cross-Session Memory

`MEMORY.md` at the repo root is this repo's durable memory across agent sessions, coordinated with the grovv-stack Linear project:

- **Read it at session start** — a `SessionStart` hook in `.claude/settings.json` surfaces it automatically; read it manually if hooks didn't fire.
- **Update it before ending** any session that changed something meaningful: Current State, a dated Decision Log entry, Next Steps; prune stale content.
- **Linear owns the backlog; `MEMORY.md` owns context** — reference Linear issues by identifier, never mirror issue lists into the file. Keep it under ~120 lines.

Target projects get the same convention from the tracker-setup step (see `docs/prompts/tracker-setup.md` for the template and hook).

-----

## Key Directives

- **Ask before generating** — understand the product, users, constraints, and stack first
- **Never overwrite working code** in existing projects without approval
- **Mark unknowns with `@TODO`** and revisit as conversation progresses
- **Apply gro\\/\\/ stack branding** to all generated documents
- **Iterate** — documents are living artifacts, revise as understanding deepens
- **Maintain memory** — read `MEMORY.md` at session start, update it before ending meaningful work, sync with Linear
- **Always ask what Playwright should test** — never auto-generate E2E tests
- **Always ask which frontend framework** — Astro + React or Next.js — before writing frontend code
- **Record the verify commands, ask before generating CI** — Step 1 discovers what proves the project works and Step 8 records it in `MEMORY.md`; how much CI to generate from those commands is a Step 6 question with four answers, and "none" is one of them

-----

## Environment Variables Reference

```bash
# Database (Neon/Supabase)
DATABASE_URL="postgresql://..."
DIRECT_URL="postgresql://..."

# Authentication (Clerk)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY="pk_..."
CLERK_SECRET_KEY="sk_..."

# Observability (PostHog)
NEXT_PUBLIC_POSTHOG_KEY="phc_..."
NEXT_PUBLIC_POSTHOG_HOST="https://app.posthog.com"

# Email (Resend preferred; Plunk alternative; SES only if required)
RESEND_API_KEY="re_..."
# PLUNK_API_KEY="sk_..."
# AWS_SES_REGION="us-east-1"
# AWS_ACCESS_KEY_ID="..."
# AWS_SECRET_ACCESS_KEY="..."
EMAIL_FROM="no-reply@example.com"

# Payments (Stripe)
STRIPE_SECRET_KEY="sk_..."
STRIPE_WEBHOOK_SECRET="whsec_..."
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY="pk_..."

# Usage tracking (Lago)
LAGO_API_KEY="..."
LAGO_API_URL="https://api.getlago.com"

# Project tracking (Linear) — primarily via the Linear MCP server;
# API key only needed for non-MCP/CI automation
LINEAR_API_KEY="lin_api_..."
```

-----
gro\\/\\/ stack
