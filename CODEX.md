# grovv-stack

**gro\\/\\/ stack** — Production-First Project Scaffolding for Codex

-----

## What This Is

grovv-stack is a prompt-driven project scaffolding system that generates production-ready codebases with built-in best practices, security, and test-driven development patterns. It works for both new and existing projects through a conversational process.

This file provides Codex-specific context. For the complete project documentation, see `CLAUDE.md` in the `.grovv/` directory or the root `README.md`.

-----

## Installation for Codex

### From a Clone

Clone this repo and work from any project directory:
```bash
cd /path/to/your-project
git clone https://github.com/constructyourself/grovv-stack.git ../grovv-stack
# Copy grovv-stack-scaffold.md to your project root
cp ../grovv-stack/grovv-stack-scaffold.md .
```

Then invoke through Codex's skill system or natural language: "build out this project with grovv stack"

-----

## Codex-Specific Configuration

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

.codex/                    # Codex-specific configuration
├── agents/                # Codex-adapted agent definitions
├── skills/                # Codex-adapted skill definitions
│   ├── grovv/
│   │   └── SKILL.md       # Entry point
│   └── harness/
└── settings.json          # Codex settings and hooks
```

### Settings

The `.codex/settings.json` file configures Codex-specific behavior:

```json
{
  "hooks": {
    "SessionStart": ["MEMORY.md"]
  }
}
```

This ensures `MEMORY.md` is loaded at the start of every session for cross-session continuity.

-----

## Sub-Agents for Codex

The six baseline agents are defined in `.codex/agents/`:

| Agent | File | Purpose |
|-------|------|---------|
| **Scaffold** | `agents/scaffold.md` | Guides scaffolding process for new and existing projects |
| **Frontend** | `agents/frontend.md` | Frontend development — asks user to choose Astro + React or Next.js |
| **Backend** | `agents/backend.md` | TypeScript and Go API/service development |
| **Testing** | `agents/testing.md` | TDD enforcement, automated tests, Playwright E2E |
| **Database** | `agents/database.md` | Schema design, migrations, query optimization |
| **Code Review** | `agents/code-review.md` | Security, quality, and standards review |

**Codex Adaptation:** These agents use Codex's native agent spawning system. The coordination model is adapted for Codex's architecture.

-----

## How the Scaffolding Works

### Pipeline Execution Order

1. **tech-spec** → Creates the technical specification (`docs/tech-spec.md`)
2. **skills-builder** → Generates the project's invocable skills under `.codex/skills/`
3. **team-design** → Designs the project-specific agent team using harness meta-skill
4. **tracker-setup** → Asks which tracker to use (GitHub Issues or Linear), then seeds the backlog
5. **readme-generator** → Generates project README

### Tool-Specific Notes

- **Subagent Spawning**: Uses Codex's native agent spawning
- **Parallel Execution**: Codex's native parallel capabilities are leveraged where possible
- **Memory**: `MEMORY.md` at repo root coordinates with Linear project
- **Hooks**: SessionStart hook in `.codex/settings.json` loads memory automatically

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
| Dev Environment | VS Code, sprites.dev |

-----

## Non-Negotiable Rules

- **Ask which frontend framework** (Astro + React or Next.js) before writing any frontend code.
- **Ask what Playwright should test** before writing any E2E test. Never auto-generate Playwright flows.
- **Production-first** — production readiness is the default for everything that ships, not aspirational. Exploratory artifacts (prototypes, mockups, spikes) are explicitly exempt and are never merged. See the Throwaway Tier.
- **Complete code examples only** — typed, with error handling, no pseudo-code. This governs generated code and documentation; exploratory artifacts in the throwaway tier are exempt by definition.
- **Security by default** — input validation, auth, dependency audits in every layer. Never deferred.
- **Zero data loss** — transactions for all multi-step data operations.
- **Never overwrite working code** in existing projects without an approved adoption plan.
- **Ask how much CI to generate** before writing a workflow into a project, and generate only the verify commands Step 1 actually found. "None" is a valid answer; an invented command is not.
- **Apply gro\\/\\/ stack branding** to every generated document (footer, conventions below).

-----

## The Throwaway Tier

Production-first governs what ships, not what you build to find out what should ship. An exploratory artifact — prototype, mockup, brainstorm, or spike — is exempt from the production bar and is never merged.

- Multi-file exploration goes on an unmerged `proto/*` or `spike/*` branch; a single-file mockup goes in the gitignored `prototypes/` directory. Delete it once the decision it informed is recorded.
- It never satisfies an ask-first rule above. Four mockups built in React is not a decision to use Next.js — Codex still asks, and the user still answers.

Full rules: the Throwaway Tier section in `grovv-stack-scaffold.md`.

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

`MEMORY.md` at the repo root is durable memory across Codex sessions, coordinated with the Linear project:

- **Read it at session start** — the `SessionStart` hook in `.codex/settings.json` surfaces it automatically
- **Update it before ending** any session that changed something meaningful: Current State, a dated Decision Log entry, Next Steps; prune stale content
- **Linear owns the backlog** — tasks, priorities, status, and assignments live in Linear. Reference issues by identifier, never mirror issue lists into MEMORY.md
- **This file owns context** — decisions, rationale, gotchas, in-flight state
- **Stay small** — keep under ~120 lines. History lives in git, the backlog lives in Linear

-----

## When You Touch This Repo Itself

- Stack changes must propagate to **every** doc that references the stack
- Agent definitions in `.codex/agents/` and `.grovv/agents/` are read by future agent runs
- Changes to prompts in `docs/prompts/` affect all downstream projects
- This repo produces documents and configuration, not compiled artifacts

-----

gro\\/\\/ stack — Codex Configuration Guide
