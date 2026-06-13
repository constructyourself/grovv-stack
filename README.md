# grovv stack

```
 ██████╗ ██████╗  ██████╗ ██╗   ██╗██╗   ██╗
██╔════╝ ██╔══██╗██╔═══██╗██║   ██║██║   ██║
██║  ███╗██████╔╝██║   ██║██║   ██║██║   ██║
██║   ██║██╔══██╗██║   ██║╚██╗ ██╔╝╚██╗ ██╔╝
╚██████╔╝██║  ██║╚██████╔╝ ╚████╔╝  ╚████╔╝
 ╚═════╝ ╚═╝  ╚═╝ ╚═════╝   ╚═══╝    ╚═══╝
```

**gro\\/\\/ stack** — Production-First Project Scaffolding

A prompt-driven scaffolding system that an AI agent uses to generate production-ready codebases (new projects) or layer documentation, skills, conventions, and an agent team onto existing ones. It is conversation-driven and ask-first: it understands the product, users, constraints, and stack before generating anything.

This repository is **not an application**. Its output is documents, configuration, and an agent team in *your* project — never code in this repo.

-----

## Install

```
/plugin marketplace add constructyourself/grovv-stack
/plugin install grovv-stack@grovv
```

-----

## Kick it off

In any repository — new or existing:

| Entry point | How |
|-------------|-----|
| Command | `/grovv` — auto-detects new vs existing. Force the mode with `/grovv new` or `/grovv adopt`. |
| Natural language | "build out this project with grovv stack", "adopt grovv stack in this repo" — triggers the `grovv-scaffold` skill. |

Both run the same workflow defined in `grovv-stack-scaffold.md`. For an existing project, the agent assesses the codebase and proposes an adoption plan before changing anything — it never overwrites working code without approval.

Working from a clone of this repo (without installing) also works: the agents and skills under `.claude/` load as project-scope components.

-----

## What it generates

Into the target project:

```
product-spec.md            # What, who, why
development-plan.md         # Engineering plan
tech-spec.md               # Complete technical specification
docs/skills/               # 12-15 development best-practice guides
docs/prompts/              # Prompt specs (skills-builder, team-design, tech-spec, readme)
docs/architecture/         # Architecture decision records
.claude/agents/            # Project-specific agent team (additive to the six defaults)
.claude/skills/            # Skills the agents use + an orchestrator
README.md                  # Project README
```

The pipeline runs: structure + config → product spec → development plan → tech spec → prompt docs → skills-builder → **team-design (harness)** → **linear-tracking** → readme. The team-design step uses the bundled [harness](.claude/skills/harness/ATTRIBUTION.md) meta-skill to design a project-specific agent team, additive to the six grovv defaults. The linear-tracking step uses the Linear MCP to create a project and seed issues from the development plan.

-----

## What ships in the plugin

| Component | Path |
|-----------|------|
| Command | `commands/grovv.md` |
| Kickoff skill | `.claude/skills/grovv-scaffold/` |
| harness meta-skill (Apache-2.0, vendored) | `.claude/skills/harness/` |
| Default agents | `.claude/agents/` (scaffold, frontend, backend, testing, database, code-review) |
| Master directive | `grovv-stack-scaffold.md` |

-----

## Non-negotiables

- Ask which frontend framework (Astro + React or Next.js) before any frontend code.
- Ask what Playwright should test before writing any E2E test.
- Production-first, security by default, zero data loss (transactions for multi-step data ops).
- Never overwrite working code in existing projects without an approved adoption plan.

-----

## License

grovv stack is licensed under the [MIT License](LICENSE). Vendored third-party components keep their own licenses — the bundled harness meta-skill is Apache-2.0; see [`.claude/skills/harness/ATTRIBUTION.md`](.claude/skills/harness/ATTRIBUTION.md).

-----
gro\\/\\/ stack — Production-First Project Scaffolding
