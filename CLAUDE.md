# grovv-stack

**gro\/\/ stack** — Production-First Project Scaffolding (Claude Code)

-----

## What This Is

grovv-stack is a prompt-driven project scaffolding system that generates production-ready codebases with built-in best practices, security, and test-driven development patterns. It works for both new and existing projects through a conversational process.

**This file is Claude Code specific.** For other tools:
- Vibe users: See [`VIBE.md`](VIBE.md)
- Codex users: See [`CODEX.md`](CODEX.md)
- Tool-agnostic core: See [`.grovv/CLAUDE.md`](.grovv/CLAUDE.md)

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
| **Dev Environment** | VS Code, sprites.dev | Local and cloud IDE |
| **AI CLI** | Claude Code | Agentic coding and automation |

-----

## Repository Structure

```
grovv-stack/
├── .grovv/                    # Shared, tool-agnostic configuration
│   ├── agents/                # Canonical agent definitions (6 baseline agents)
│   └── skills/                # Canonical skill definitions (grovv, harness)
├── .claude/                   # Claude Code specific (THIS DIRECTORY)
│   ├── CLAUDE.md              # This file — project context for Claude
│   ├── settings.json          # Claude Code settings
│   ├── agents/                # Claude-adapted agent definitions
│   │   ├── scaffold.md
│   │   ├── frontend.md
│   │   ├── backend.md
│   │   ├── testing.md
│   │   ├── database.md
│   │   └── code-review.md
│   └── skills/                # Skills shipped via plugin.json
│       ├── grovv/             # Kickoff skill — /grovv, also triggers on intent
│       └── harness/           # harness meta-skill (Apache-2.0, vendored)
├── .vibe/                    # Vibe specific configuration
├── .codex/                   # Codex specific configuration
├── plugin.json                # Unified plugin manifest
├── VIBE.md                   # Vibe-specific documentation
├── CODEX.md                  # Codex-specific documentation
├── grovv-stack-scaffold.md    # Main scaffolding directive
├── MEMORY.md                 # Cross-session memory for this repo
├── settings.json             # Claude Code agent-team configuration
└── README.md                 # Project readme
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
4. **linear-tracking** → Creates/reuses a Linear project and seeds issues from the development plan (via Linear MCP); also creates the target project's `MEMORY.md`, its `CLAUDE.md` maintenance rules, and a `SessionStart` hook
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

Apply to every file this repo generates:

- Horizontal rules: `-----` (five dashes)
- Fenced code blocks with language hints
- Tables for structured reference data
- `@TODO` markers for incomplete sections
- Colophon with version, status, author, model metadata
- Footer (in prose): `gro\/\/ stack — [Purpose or Project Name]` — doubled backslashes so it renders as the gro\/\/ wordmark, not gro//. Inside code blocks, use single backslashes (`gro\/`).
- No excessive bold or emoji in headings

-----

## Cross-Session Memory

`MEMORY.md` at the repo root is this repo's durable memory across agent sessions, coordinated with the grovv-stack Linear project:

- **Read it at session start** — a `SessionStart` hook in `.claude/settings.json` surfaces it automatically; read it manually if hooks didn't fire.
- **Update it before ending** any session that changed something meaningful: Current State, a dated Decision Log entry, Next Steps, and prune anything stale.
- **Linear owns the backlog** — Tasks, priorities, status, and assignments live in Linear. Never duplicate issue lists into the file — reference Linear issues by identifier.
- **This file owns context** — Decisions and rationale, gotchas, in-flight state, and anything a fresh session needs that does not fit a Linear issue.
- **Stay small** — Keep this file under ~120 lines. It is loaded into context every session; verbosity here is a tax on every future session. Prune aggressively — history lives in git.

Target projects get the same convention: the linear-tracking step (Step 8) generates their `MEMORY.md`, `CLAUDE.md` rules, and `SessionStart` hook.

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

## When You Touch This Repo Itself

These files are the source of truth that downstream projects depend on. Treat changes accordingly:

- Stack changes (e.g., adding a runtime, swapping a default) must propagate to **every** doc that references them: `grovv-stack-scaffold.md`, `.grovv/CLAUDE.md`, `.claude/CLAUDE.md`, `.claude/agents/*.md`, and every prompt under `docs/prompts/`. Grep before committing.
- The sub-agent definitions in `.claude/agents/` and the prompts in `docs/prompts/` are read by future agent runs. A small wording change here changes behavior at scale — review with care.
- Don't introduce dependencies or build steps in this repo. It still produces documents, not compiled artifacts. The plugin manifests (`.claude-plugin/*.json`) and the skills (including the `grovv` kickoff skill) are configuration, not a build pipeline — keep it that way.
- This repo is also an **installable plugin**. The single source of truth for agents and skills stays under `.claude/` for Claude; the canonical versions are in `.grovv/`. When you add or rename an agent, update the `agents` array in `.claude-plugin/plugin.json` too.
- Bump `version` in `.claude-plugin/plugin.json` when you change behavior that installed users should receive.

-----

## Installation

```
/plugin marketplace add constructyourself/grovv-stack
/plugin install grovv-stack@grovv
```

Then run `/grovv` in any project, or just say "build out this project with grovv stack". Working from a clone of this repo (without installing) also works — the `.claude/` agents and skills load as project-scope components and the `grovv` skill triggers on intent.

-----

## Multi-Tool Support

This repository now supports multiple AI coding assistants:

| Tool | Directory | Status |
|------|----------|--------|
| **Claude Code** | `.claude/` | Original, fully supported |
| **Vibe** | `.vibe/` | Supported |
| **Codex** | `.codex/` | Supported |
| **Shared** | `.grovv/` | Canonical definitions |

All tool-specific directories mirror the canonical `.grovv/` structure with tool-specific adaptations. The existing Claude Code setup is **unchanged and fully backward compatible**.

-----
gro\/\/ stack — Repository Guide (Claude Code)
