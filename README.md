# grovv stack

```
 ██████╗ ██████╗  ██████╗ ██╗   ██╗██╗   ██╗
██╔════╝ ██╔══██╗██╔═══██╗██║   ██║██║   ██║
██║  ███╗██████╔╝██║   ██║██║   ██║██║   ██║
██║   ██║██╔══██╗██║   ██║╚██╗ ██╔╝╚██╗ ██╔╝
╚██████╔╝██║  ██║╚██████╔╝ ╚████╔╝  ╚████╔╝
 ╚═════╝ ╚═╝  ╚═╝ ╚═════╝   ╚═══╝    ╚═══╝
```

**gro\/\/ stack** — Production-First Project Scaffolding

A prompt-driven scaffolding system that an AI agent uses to generate production-ready codebases (new projects) or layer documentation, skills, conventions, and an agent team onto existing ones. It is conversation-driven and ask-first: it understands the product, users, constraints, and stack before generating anything.

This repository is **not an application**. Its output is documents, configuration, and an agent team in *your* project — never code in this repo.

-----

## Supported AI Coding Assistants

| Tool | Status | Installation | Invocation |
|------|--------|-------------|------------|
| **Claude Code** | Fully Supported | `/plugin marketplace add constructyourself/grovv-stack` then `/plugin install grovv-stack@grovv` | `/grovv` |
| **Vibe** | Supported | Clone this repo | `/grovv` or natural language |
| **Codex** | Supported | Clone this repo | Natural language trigger |

-----

## Key Features

| Feature | Description |
|---------|-------------|
| **Multi-Tool Support** | Works with Claude Code, Vibe, and Codex |
| **Production-First** | Generates production-ready code with built-in best practices |
| **Conversation-Driven** | Asks questions to understand your project before generating |
| **Agent Team** | Creates a team of specialized agents for your project |
| **Invocable Skills** | Generates best-practice skills for common tasks |
| **Linear Integration** | Seeds Linear project and issues from development plan |
| **Cross-Session Memory** | MEMORY.md coordinates with Linear for continuity |
| **Harness Meta-Skill** | Uses vendored harness (Apache-2.0) for team design |
| **Backward Compatible** | Existing Claude Code installations work unchanged |
| **Tool-Agnostic Core** | Canonical definitions in `.grovv/` work across all tools |

---

## Install

### Claude Code (Plugin Marketplace)

```
/plugin marketplace add constructyourself/grovv-stack
/plugin install grovv-stack@grovv
```

### Vibe & Codex (From Clone)

Clone this repo and work from any project directory:
```bash
cd /path/to/your-project
git clone https://github.com/constructyourself/grovv-stack.git ../grovv-stack
# Copy the master directive to your project root
cp ../grovv-stack/grovv-stack-scaffold.md .
```

-----

## Kick it off

In any repository — new or existing:

| Entry point | How | Tools |
|-------------|-----|-------|
| `/grovv` | Invoke the `grovv` skill explicitly — auto-detects new vs existing. Force the mode with `/grovv new` or `/grovv adopt`. | Claude, Vibe |
| Natural language | "build out this project with grovv stack", "adopt grovv stack in this repo" — the same `grovv` skill triggers on intent. | Claude, Vibe, Codex |

Both routes are the one `grovv` skill (there is no separate command) and run the same workflow defined in `grovv-stack-scaffold.md`. For an existing project, the agent assesses the codebase and proposes an adoption plan before changing anything — it never overwrites working code without approval.

Working from a clone of this repo (without installing) also works: the agents and skills under the tool-specific directories (`.claude/`, `.vibe/`, `.codex/`) load as project-scope components.

-----

## What it generates

Into the target project:

```
docs/product-spec.md       # What, who, why
docs/development-plan.md    # Engineering plan
docs/tech-spec.md          # Complete technical specification
docs/prompts/              # Prompt specs (skills-builder, team-design, linear-tracking, tech-spec, readme)
docs/architecture/         # Architecture decision records
[.claude|.vibe|.codex]/agents/    # Project-specific agent team (additive to the six defaults)
[.claude|.vibe|.codex]/skills/    # Invocable skills — best-practice set + the agents' skills + an orchestrator
MEMORY.md                  # Cross-session memory, coordinated with the Linear project
README.md                  # Project README
```

The pipeline runs: structure + config → product spec → development plan → tech spec → prompt docs → **skills-builder** → **team-design (harness)** → **linear-tracking** → readme. The team-design step uses the bundled [harness](.grovv/skills/harness/ATTRIBUTION.md) meta-skill to design a project-specific agent team, additive to the six grovv defaults. The linear-tracking step uses the Linear MCP to create a project and seed issues from the development plan, and creates `MEMORY.md` — durable cross-session memory that coordinates with the Linear backlog (Linear owns the tasks; MEMORY.md owns decisions, gotchas, and in-flight context), kept alive by tool-specific context file rules (`CLAUDE.md`, `VIBE.md`, or `CODEX.md`) and a SessionStart hook.

-----

## Repository Structure

```
grovv-stack/
├── .grovv/                    # Shared, tool-agnostic canonical definitions
│   ├── agents/                # Canonical agent definitions (6 baseline agents)
│   └── skills/                # Canonical skill definitions (grovv, harness)
├── .claude/                   # Claude Code specific configuration
│   ├── agents/                # Claude-adapted agents
│   ├── skills/                # Claude-adapted skills
│   └── CLAUDE.md              # Claude-specific context
├── .vibe/                    # Vibe specific configuration
│   ├── agents/                # Vibe-adapted agents
│   ├── skills/                # Vibe-adapted skills
│   └── settings.json          # Vibe hooks and settings
├── .codex/                   # Codex specific configuration
│   ├── agents/                # Codex-adapted agents
│   ├── skills/                # Codex-adapted skills
│   └── settings.json          # Codex hooks and settings
├── plugin.json                # Unified plugin manifest for all tools
├── grovv-stack-scaffold.md    # Master directive (tool-agnostic)
├── CLAUDE.md                  # Claude Code specific documentation
├── VIBE.md                    # Vibe specific documentation
├── CODEX.md                   # Codex specific documentation
├── MEMORY.md                  # Cross-session memory for this repo
├── README.md                  # This file
└── docs/                     # Prompts and architecture docs
```

-----

## Tool-Specific Documentation

- **Claude Code**: See [`CLAUDE.md`](CLAUDE.md) for Claude-specific setup and conventions
- **Vibe**: See [`VIBE.md`](VIBE.md) for Vibe-specific setup and conventions
- **Codex**: See [`CODEX.md`](CODEX.md) for Codex-specific setup and conventions
- **Shared/Canonical**: See [`.grovv/CLAUDE.md`](.grovv/CLAUDE.md) for tool-agnostic core documentation

-----

## What ships in the plugin

| Component | Path | Tools |
|-----------|------|-------|
| Kickoff skill — `/grovv`, also triggers on intent | `.claude/skills/grovv/`, `.vibe/skills/grovv/`, `.codex/skills/grovv/` | All |
| harness meta-skill (Apache-2.0, vendored) | `.grovv/skills/harness/` (canonical), mirrored to tool dirs | All |
| Default agents | `.grovv/agents/` (canonical), mirrored to tool dirs | All |
| Master directive | `grovv-stack-scaffold.md` | All |

-----

## Non-negotiables

- Ask which frontend framework (Astro + React or Next.js) before any frontend code.
- Ask what Playwright should test before writing any E2E test.
- Production-first, security by default, zero data loss (transactions for multi-step data ops).
- Never overwrite working code in existing projects without an approved adoption plan.

-----

## Backward Compatibility

Existing Claude Code users are not affected. All original `.claude/` files and structure remain intact. The new `.vibe/`, `.codex/`, and `.grovv/` directories are additive and do not interfere with existing Claude Code installations.

-----

## License

grovv stack is licensed under the [MIT License](LICENSE). Vendored third-party components keep their own licenses — the bundled harness meta-skill is Apache-2.0; see [`.grovv/skills/harness/ATTRIBUTION.md`](.grovv/skills/harness/ATTRIBUTION.md).

-----
gro\/\/ stack — Production-First Project Scaffolding
