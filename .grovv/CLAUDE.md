# grovv-stack

**gro\/\/ stack** — Production-First Project Scaffolding (Canonical)

-----

## What This Is

This is the **canonical, tool-agnostic** context file for grovv-stack. It contains the core documentation that applies across all supported AI coding assistants (Claude Code, Vibe, Codex).

For tool-specific information, see:
- `CLAUDE.md` (root) — Claude Code specific
- `VIBE.md` (root) — Vibe specific  
- `CODEX.md` (root) — Codex specific

-----

## Core Principles

| Principle | Description |
|-----------|-------------|
| **Production-First** | Every implementation is production-ready from start |
| **Zero Data Loss** | Transactional integrity is non-negotiable |
| **Security by Default** | Security considerations never deferred |
| **Test-Driven** | Tests define contracts and prevent regressions |
| **Documentation as Code** | Docs maintained alongside code |
| **Conversation-Driven** | Ask questions, understand deeply, then build |

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
| **Project Tracking** | Linear | Issue and project tracking (via Linear MCP) |
| **Deployment** | Vercel, Docker | Production hosting |

-----

## Repository Structure (Canonical)

```
.grovv/                    # Shared, tool-agnostic configuration
├── agents/                # Canonical agent definitions
│   ├── scaffold.md         # Scaffolding agent
│   ├── frontend.md         # Frontend development agent
│   ├── backend.md          # Backend development agent
│   ├── testing.md          # Testing and TDD agent
│   ├── database.md         # Database design agent
│   └── code-review.md      # Code review agent
└── skills/                # Canonical skill definitions
    ├── grovv/              # Kickoff skill — /grovv, also triggers on intent
    └── harness/            # harness meta-skill (Apache-2.0, vendored)

Tool-specific directories:
├── .claude/               # Claude Code configuration
├── .vibe/                # Vibe configuration
└── .codex/               # Codex configuration
```

Each tool directory mirrors the `.grovv/` structure with tool-specific adaptations.

-----

## Sub-Agents

The `.grovv/agents/` folder contains specialized sub-agent definitions that are the canonical source for all tools:

| Agent | File | Purpose |
|-------|------|---------|
| **Scaffold** | `agents/scaffold.md` | Guides scaffolding process for new and existing projects |
| **Frontend** | `agents/frontend.md` | Frontend development — asks user to choose Astro + React or Next.js |
| **Backend** | `agents/backend.md` | TypeScript and Go API/service development |
| **Testing** | `agents/testing.md` | TDD enforcement, automated tests, Playwright E2E |
| **Database** | `agents/database.md` | Schema design, migrations, query optimization |
| **Code Review** | `agents/code-review.md` | Security, quality, and standards review |

These six are the **baseline team**. During the team-design step, the scaffolder uses the vendored **harness** meta-skill to design *additional*, project-specific agents and the skills they use, plus an orchestrator — written into the **target project's** tool-specific directory. The harness is vendored verbatim from [revfactory/harness](https://github.com/revfactory/harness) under Apache-2.0; see `.grovv/skills/harness/ATTRIBUTION.md` for provenance.

-----

## How the Scaffolding Works

### Prompt Execution Order

1. **tech-spec** → Creates the technical specification (`docs/tech-spec.md`)
2. **skills-builder** → Generates the project's invocable skills under the tool-specific skills directory
3. **team-design** → Designs the project-specific agent team + skills (harness); additive to grovv defaults
4. **linear-tracking** → Creates/reuses a Linear project and seeds issues from the development plan (via Linear MCP); also creates the target project's `MEMORY.md`, its tool-specific context file (`CLAUDE.md`, `VIBE.md`, or `CODEX.md`) memory rules, and a `SessionStart` hook
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
- Complete code examples only — no pseudo-code
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
- Footer (in prose): `gro\/\/ stack — [Purpose or Project Name]` — doubled backslashes so it renders as the gro\/\/ wordmark, not gro//. Inside code blocks, use single backslashes (`gro\/`).
- No excessive bold or emoji in headings

-----

## Cross-Session Memory

`MEMORY.md` at the repo root is durable memory across agent sessions, coordinated with the Linear project:

- **Read it at session start** — a `SessionStart` hook in the tool-specific `settings.json` surfaces it automatically; read it manually if hooks didn't fire
- **Update it before ending** any session that changed something meaningful: Current State, a dated Decision Log entry, Next Steps; prune stale content
- **Linear owns the backlog** — tasks, priorities, status, and assignments live in Linear. Reference issues by identifier, never mirror issue lists into the file
- **This file owns context** — decisions, rationale, gotchas, in-flight state
- **Stay small** — keep under ~120 lines. History lives in git, the backlog lives in Linear

Target projects get the same convention from the linear-tracking step.

-----

## Key Directives

- **Ask before generating** — understand the product, users, constraints, and stack first
- **Never overwrite working code** in existing projects without approval
- **Mark unknowns with `@TODO`** and revisit as the conversation progresses
- **Apply gro\/\/ stack branding** to all generated documents
- **Iterate** — documents are living artifacts, revise as understanding deepens
- **Maintain memory** — read `MEMORY.md` at session start, update it before ending meaningful work, sync with Linear
- **Always ask what Playwright should test** — never auto-generate E2E tests
- **Always ask which frontend framework** — Astro + React or Next.js — before writing frontend code

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

gro\/\/ stack — Canonical Configuration
