# grovv-stack

**gro\\/\\/ stack** — Production-First Project Scaffolding for Vibe

-----

## What This Is

grovv-stack is a prompt-driven project scaffolding system that generates production-ready codebases with built-in best practices, security, and test-driven development patterns. It works for both new and existing projects through a conversational process.

This file provides Vibe-specific context. For the complete project documentation, see `CLAUDE.md` in the `.grovv/` directory or the root `README.md`.

-----

## Installation for Vibe

### As a Vibe Plugin (Recommended)

```
vibe plugin add constructyourself/grovv-stack
```

Then kick it off in any repo:
- `/grovv` — explicit kickoff
- `build out this project with grovv stack` — natural language trigger

### From a Clone

Clone this repo and work from any project directory:
```bash
cd /path/to/your-project
git clone https://github.com/constructyourself/grovv-stack.git ../grovv-stack
# Copy grovv-stack-scaffold.md to your project root
cp ../grovv-stack/grovv-stack-scaffold.md .
```

Then invoke: `/grovv` or "build out this project with grovv stack"

-----

## Vibe-Specific Configuration

### Directory Structure

```
.grovv/                    # Shared, tool-agnostic configuration
├── agents/                # Canonical agent definitions
│   ├── scaffold.md
│   ├── frontend.md
│   ├── backend.md
│   ├── testing.md
│   ├── database.md
│   └── code-review.md
└── skills/                # Canonical skill definitions
    ├── grovv/
    └── harness/

.vibe/                     # Vibe-specific configuration
├── agents/                # Vibe-adapted agent definitions
├── skills/                # Vibe-adapted skill definitions
│   ├── grovv/
│   │   └── SKILL.md       # Entry point
│   └── harness/
└── settings.json          # Vibe settings and hooks
```

### Settings

The `.vibe/settings.json` file configures Vibe-specific behavior:

```json
{
  "hooks": {
    "SessionStart": ["MEMORY.md"]
  }
}
```

This ensures `MEMORY.md` is loaded at the start of every session for cross-session continuity.

-----

## Sub-Agents for Vibe

The six baseline agents are defined in `.vibe/agents/`:

| Agent | File | Purpose |
|-------|------|---------|
| **Scaffold** | `agents/scaffold.md` | Guides scaffolding process for new and existing projects |
| **Frontend** | `agents/frontend.md` | Frontend development — asks user to choose Astro + React or Next.js |
| **Backend** | `agents/backend.md` | TypeScript and Go API/service development |
| **Testing** | `agents/testing.md` | TDD enforcement, automated tests, Playwright E2E |
| **Database** | `agents/database.md` | Schema design, migrations, query optimization |
| **Code Review** | `agents/code-review.md` | Security, quality, and standards review |

**Vibe Adaptation:** These agents use Vibe's `task` tool for spawning subagents instead of Claude's `TeamCreate`/`Agent` tools. The coordination model is adapted for Vibe's architecture.

-----

## How the Scaffolding Works

### Pipeline Execution Order

1. **tech-spec** → Creates the technical specification (`docs/tech-spec.md`)
2. **skills-builder** → Generates the project's invocable skills under `.vibe/skills/`
3. **team-design** → Designs the project-specific agent team using harness meta-skill
4. **tracker-setup** → Asks which tracker to use (GitHub Issues or Linear), then seeds the backlog
5. **readme-generator** → Generates project README

### Tool-Specific Notes

- **Subagent Spawning**: Uses Vibe's `task` tool with `agent: "explore"` or custom agent types
- **Parallel Execution**: Vibe's native parallel tool execution is leveraged where possible
- **Memory**: `MEMORY.md` at repo root coordinates with Linear project
- **Hooks**: SessionStart hook in `.vibe/settings.json` loads memory automatically

-----

## Default Technology Stack

Adapt per project; never assume.

| Category | Default |
|----------|---------|
| Languages | TypeScript, Go |
| Runtime | Node.js (LTS) |
| Database | PostgreSQL (Neon/Supabase), SQLite |
| Auth | Clerk |
| Frontend | Astro + React **or** Next.js (ask first) |
| UI | Tailwind CSS + shadcn/ui, Alexandria font, monochrome palette |
| Testing | Vitest (TypeScript), `go test` (Go), Playwright (E2E — ask first) |
| Background Jobs | PostgreSQL-native |
| Email | Resend or Plunk (Amazon SES only if really needed) |
| Payments | Stripe |
| Usage Tracking | Lago |
| Observability | PostHog |
| Project Tracking | GitHub Issues (recommended) or Linear — chosen per project |
| Deployment | Vercel, Docker |

-----

## Non-Negotiable Rules

- **Ask which frontend framework** (Astro + React or Next.js) before writing any frontend code.
- **Ask what Playwright should test** before writing any E2E test. Never auto-generate Playwright flows.
- **Production-first** — every example must be complete, typed, with error handling. No pseudo-code.
- **Security by default** — input validation, auth, dependency audits in every layer. Never deferred.
- **Zero data loss** — transactions for all multi-step data operations.
- **Never overwrite working code** in existing projects without an approved adoption plan.
- **Apply gro\\/\\/ stack branding** to every generated document (footer, conventions below).

-----

## Document Conventions

Apply to every file this repo generates:

- Horizontal rules: `-----` (five dashes).
- Fenced code blocks with language hints.
- Tables for structured reference data.
- `@TODO` markers for incomplete sections.
- Colophon (version, status, author, model) on specs.
- Footer (in prose): `gro\\/\\/ stack — [Purpose or Project Name]` — doubled backslashes so it renders as the gro\\/\\/ wordmark, not gro//. Inside code blocks, use single backslashes (`gro\/\/`).
- No emoji in headings; minimal bold.
- Project folder names: lowercase with dashes.

-----

## Cross-Session Memory

`MEMORY.md` at the repo root is durable memory across Vibe sessions, coordinated with the Linear project:

- **Read it at session start** — the `SessionStart` hook in `.vibe/settings.json` surfaces it automatically
- **Update it before ending** any session that changed something meaningful: Current State, a dated Decision Log entry, Next Steps; prune stale content
- **Linear owns the backlog** — tasks, priorities, status, and assignments live in Linear. Reference issues by identifier, never mirror issue lists into MEMORY.md
- **This file owns context** — decisions, rationale, gotchas, in-flight state
- **Stay small** — keep under ~120 lines. History lives in git, the backlog lives in Linear

-----

## When You Touch This Repo Itself

- Stack changes must propagate to **every** doc that references the stack
- Agent definitions in `.vibe/agents/` and `.grovv/agents/` are read by future agent runs
- Changes to prompts in `docs/prompts/` affect all downstream projects
- Bump `version` in `.vibe-plugin/plugin.json` (when created) for behavior changes
- This repo produces documents and configuration, not compiled artifacts

-----

gro\\/\\/ stack — Vibe Configuration Guide
