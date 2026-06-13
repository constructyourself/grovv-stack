# grovv-stack

**gro\/\/ stack** — Production-First Project Scaffolding

This repository is **not an application**. It is a prompt-driven scaffolding system that an AI agent uses to generate production-ready codebases (new projects) or layer documentation, skills, and conventions onto existing ones. The output of this repo is documents and configuration files in another project — never code in this repo.

-----

## Operating Mode

grovv stack is installable as a Claude Code plugin. Once installed (`/plugin marketplace add constructyourself/grovv-stack` then `/plugin install grovv-stack@grovv`), it is kicked off two ways:

- `/grovv` — the explicit command front door (`commands/grovv.md`). Optional argument `new` or `adopt` forces the mode; otherwise it auto-detects.
- Natural language — the `grovv-scaffold` skill triggers on intent like "build out this project" or "adopt grovv stack in this repo".

Both entry points read `grovv-stack-scaffold.md` and run the same workflow. This repo is conversation-driven. When invoked against a target project:

1. **Read** `grovv-stack-scaffold.md` — the master directive that defines the full workflow.
2. **Ask** before generating. Understand product, users, constraints, and stack first.
3. **Assess** for existing projects (Step 0 of the scaffold) — never overwrite working code without an approved adoption plan.
4. **Execute** Steps 1–8 sequentially, pausing for confirmation at each major artifact. Step 7 designs the project-specific agent team (harness) after the skills repository exists.
5. **Mark** unknowns with `@TODO`; revisit as the conversation progresses.

If the user asks "build out this project," start by reading `grovv-stack-scaffold.md` end-to-end before any tool call that writes a file.

-----

## Repository Map

| Path | Role |
|------|------|
| `grovv-stack-scaffold.md` | Master scaffolding directive — read this first |
| `.claude-plugin/plugin.json` | Plugin manifest — makes this repo installable as a Claude Code plugin (`grovv-stack`) |
| `.claude-plugin/marketplace.json` | Marketplace catalog for `/plugin marketplace add` |
| `commands/grovv.md` | The `/grovv` slash command — the kickoff front door (auto-detects new vs existing) |
| `.claude/skills/grovv-scaffold/` | Natural-language skill that triggers the same scaffolding flow without the explicit command |
| `docs/prompts/skills-builder.md` | Generates the target project's `docs/skills/` (15+ best-practice guides) |
| `docs/prompts/team-design.md` | Designs the target project's agent team + skills (harness step, runs after skills-builder) |
| `docs/prompts/tech-spec.md` | Generates the target project's technical specification |
| `docs/prompts/tech-spec-template.md` | Section structure used by `tech-spec.md` |
| `docs/prompts/readme-generator.md` | Generates the target project's README |
| `.claude/agents/` | Sub-agent definitions (scaffold, frontend, backend, database, testing, code-review) |
| `.claude/skills/harness/` | Vendored harness meta-skill (Apache-2.0) — powers the team-design step; see its `ATTRIBUTION.md` |
| `.claude/CLAUDE.md` | Extended project context (stack details, conventions, env vars) |
| `settings.json` | Claude Code agent-team configuration |

When in doubt about a convention, the master directive (`grovv-stack-scaffold.md`) is authoritative.

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
| Deployment | Vercel, Docker |

-----

## Non-Negotiable Rules

- **Ask which frontend framework** (Astro + React or Next.js) before writing any frontend code.
- **Ask what Playwright should test** before writing any E2E test. Never auto-generate Playwright flows.
- **Production-first** — every example must be complete, typed, with error handling. No pseudo-code.
- **Security by default** — input validation, auth, dependency audits in every layer. Never deferred.
- **Zero data loss** — transactions for all multi-step data operations.
- **Never overwrite working code** in existing projects without an approved adoption plan.
- **Apply gro\/\/ stack branding** to every generated document (footer, conventions below).

-----

## Document Conventions

Apply to every file this repo generates:

- Horizontal rules: `-----` (five dashes).
- Fenced code blocks with language hints.
- Tables for structured reference data.
- `@TODO` markers for incomplete sections.
- Colophon (version, status, author, model) on specs.
- Footer: `gro\/\/ stack — [Purpose or Project Name]`.
- No emoji in headings; minimal bold.
- Project folder names: lowercase with dashes.

-----

## When You Touch This Repo Itself

These files are the source of truth that downstream projects depend on. Treat changes accordingly:

- Stack changes (e.g., adding a runtime, swapping a default) must propagate to **every** doc that references the stack: `grovv-stack-scaffold.md`, `.claude/CLAUDE.md`, `.claude/agents/*.md`, and every prompt under `docs/prompts/`. Grep before committing.
- The sub-agent definitions in `.claude/agents/` and the prompts in `docs/prompts/` are read by future agent runs. A small wording change here changes behavior at scale — review with care.
- Don't introduce dependencies or build steps in this repo. It still produces documents, not compiled artifacts. The plugin manifests (`.claude-plugin/*.json`), the `/grovv` command, and the skills are configuration, not a build pipeline — keep it that way.
- This repo is also an **installable plugin**. The single source of truth for agents and skills stays under `.claude/`; `plugin.json` points `skills` at `.claude/skills/` and lists the six agents from `.claude/agents/` — do not duplicate those files into root-level `agents/` or `skills/`, or they will drift. When you add or rename an agent, update the `agents` array in `.claude-plugin/plugin.json` too.
- Bump `version` in `.claude-plugin/plugin.json` when you change behavior that installed users should receive.

-----

## Installation

```
/plugin marketplace add constructyourself/grovv-stack
/plugin install grovv-stack@grovv
```

Then run `/grovv` in any project, or just say "build out this project with grovv stack". Working from a clone of this repo (without installing) also works — the `.claude/` agents and skills load as project-scope components and the `grovv-scaffold` skill triggers on intent.

-----
gro\/\/ stack — Repository Guide
