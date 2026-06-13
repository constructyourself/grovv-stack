---
name: grovv-scaffold
description: "Scaffolds a project with the grovv stack production-first process — generates the product spec, development plan, technical spec, a development best-practices skills repository, a project-specific agent team (harness), and the README. Use whenever the user wants to: 'build out this project', 'scaffold with grovv', 'set up grovv stack', 'grovv stack this repo', 'adopt grovv stack' in an existing codebase, or start a new production-ready project from scratch. Also triggers on requests to lay down docs/specs/skills foundations or an agent team for a new or existing project. Prefer the /grovv command when the user wants an explicit kickoff; this skill catches the same intent expressed in natural language."
---

# grovv-scaffold — start the gro\\/\\/ stack process

Runs the gro\\/\\/ stack production-first scaffolding process against the project in the current working directory. The output is documents, configuration, and an agent team in the target project — never code in the grovv-stack repo itself.

## Read the directive first

Before writing any file, read the master directive bundled with this plugin:

```
${CLAUDE_PLUGIN_ROOT}/grovv-stack-scaffold.md
```

When running from a clone of the grovv-stack repo rather than an installed plugin, read `grovv-stack-scaffold.md` at the repo root. It defines the full workflow (Steps 0–9) and is authoritative. Also follow the conventions in `CLAUDE.md` and `.claude/CLAUDE.md`.

## Detect new vs existing

Inspect the working directory:

- **Existing project** — source code, configs (`package.json`, `go.mod`, `tsconfig.json`, etc.), or a populated `docs/` are present. Start at Step 0: assess the codebase, then propose an adoption plan and wait for approval before changing anything. Never overwrite or break working code.
- **New project** — the directory is essentially empty. Start at Step 1.

State which mode you detected and why before proceeding.

## Run the workflow, ask first

Follow the directive's steps in order, pausing for confirmation at each major artifact. This is conversation-driven — understand before generating:

- Ask about the product, users, core features, constraints, stack, and deployment target before generating specs.
- Standing ask-first rules: ask which frontend framework (Astro + React or Next.js) before any frontend work, and ask what Playwright should test before writing any E2E test. Do not pre-empt these.
- Mark unknowns with `@TODO` and revisit them.
- Apply gro\\/\\/ stack branding and document conventions to everything generated.

## Pipeline

The directive runs: structure + config → product spec → development plan → tech spec → prompt docs → **skills-builder** → **team-design (harness)** → **linear-tracking** → readme-generator. The team-design step (`docs/prompts/team-design.md`) designs a project-specific agent team additive to the six grovv default agents, using the bundled harness meta-skill. The linear-tracking step (`docs/prompts/linear-tracking.md`) seeds a Linear project and issues from the development plan via the Linear MCP.

Begin by reading the directive, then engage the user.
