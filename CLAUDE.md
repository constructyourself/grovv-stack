# grovv-stack

**gro\/\/ stack** — Production-First Project Scaffolding

This repository is **not an application**. It is a prompt-driven scaffolding system that an AI agent uses to generate production-ready codebases (new projects) or layer documentation, skills, and conventions onto existing ones. The output of this repo is documents and configuration files in another project — never code in this repo.

-----

## Operating Mode

This repo is conversation-driven. When invoked against a target project:

1. **Read** `grovv-stack-scaffold.md` — the master directive that defines the full workflow.
2. **Ask** before generating. Understand product, users, constraints, and stack first.
3. **Assess** for existing projects (Step 0 of the scaffold) — never overwrite working code without an approved adoption plan.
4. **Execute** Steps 1–7 sequentially, pausing for confirmation at each major artifact.
5. **Mark** unknowns with `@TODO`; revisit as the conversation progresses.

If the user asks "build out this project," start by reading `grovv-stack-scaffold.md` end-to-end before any tool call that writes a file.

-----

## Repository Map

| Path | Role |
|------|------|
| `grovv-stack-scaffold.md` | Master scaffolding directive — read this first |
| `docs/prompts/skills-builder.md` | Generates the target project's `docs/skills/` (15+ best-practice guides) |
| `docs/prompts/tech-spec.md` | Generates the target project's technical specification |
| `docs/prompts/tech-spec-template.md` | Section structure used by `tech-spec.md` |
| `docs/prompts/readme-generator.md` | Generates the target project's README |
| `.claude/agents/` | Sub-agent definitions (scaffold, frontend, backend, database, testing, code-review) |
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
- Don't introduce dependencies or build steps in this repo. It produces documents, not artifacts.

-----
gro\/\/ stack — Repository Guide
