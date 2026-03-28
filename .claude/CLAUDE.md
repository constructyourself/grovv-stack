# grovv-stack

**gro\/\/ stack** — Production-First Project Scaffolding

-----

## What This Is

grovv-stack is a prompt-driven project scaffolding system that generates production-ready codebases with built-in best practices, security, and test-driven development patterns. It works for both new and existing projects through a conversational process.

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
| **Languages** | TypeScript, Python | Primary development |
| **Runtime** | Bun (preferred), Node.js | JavaScript execution |
| **Database** | PostgreSQL (Neon/Supabase), SQLite | Data persistence |
| **Auth** | Clerk | Identity management |
| **Frontend** | Astro, React/Preact | UI framework |
| **Background Jobs** | PostgreSQL-native | Background job processing |
| **Observability** | PostHog | Analytics and monitoring |
| **Deployment** | Vercel, Docker | Production hosting |
| **Dev Environment** | VS Code, sprites.dev | Local and cloud IDE |
| **AI CLI** | Claude Code | Agentic coding and automation |

-----

## Repository Structure

```
grovv-stack/
├── .claude/                # Claude Code configuration
│   ├── CLAUDE.md           # This file — project context for Claude
│   └── settings.json       # Claude Code settings
├── docs/
│   ├── prompts/            # Executable prompts for scaffolding
│   │   ├── skills-builder.md
│   │   ├── tech-spec.md
│   │   ├── tech-spec-template.md
│   │   └── readme-generator.md
│   ├── skills/             # Generated development best practices
│   └── architecture/       # Architecture decision records
├── grovv-stack-scaffold.md # Main scaffolding directive
├── settings.json           # Claude Code agent team config
└── README.md               # Project readme
```

-----

## How the Scaffolding Works

### Prompt Execution Order

1. **skills-builder** → Generates `/docs/skills/` with development best practices
2. **tech-spec** → Creates technical specification document
3. **readme-generator** → Generates project README

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

## UI Standards (New Projects)

- **Font:** Alexandria (fonts.bunny.net)
- **Framework:** Bootstrap 5.3+
- **Colors:** Monochrome (black/white/grey)
- **Background:** White default
- **Animations:** None (Bootstrap built-ins only)

For existing projects, analyze and match established patterns.

-----

## Document Conventions

- Horizontal rules: `-----` (five dashes)
- Fenced code blocks with language hints
- Tables for structured reference data
- `@TODO` markers for incomplete sections
- Colophon with version, status, author, model metadata
- Footer: `gro\/\/ stack — [Purpose or Project Name]`
- No excessive bold or emoji in headings

-----

## Key Directives

- **Ask before generating** — understand the product, users, constraints, and stack first
- **Never overwrite working code** in existing projects without approval
- **Mark unknowns with `@TODO`** and revisit as conversation progresses
- **Apply gro\/\/ stack branding** to all generated documents
- **Iterate** — documents are living artifacts, revise as understanding deepens

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
```

-----
gro\/\/ stack
