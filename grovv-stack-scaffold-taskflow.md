# grovv-stack

```
 ██████╗ ██████╗  ██████╗ ██╗   ██╗██╗   ██╗
██╔════╝ ██╔══██╗██╔═══██╗██║   ██║██║   ██║
██║  ███╗██████╔╝██║   ██║██║   ██║██║   ██║
██║   ██║██╔══██╗██║   ██║╚██╗ ██╔╝╚██╗ ██╔╝
╚██████╔╝██║  ██║╚██████╔╝ ╚████╔╝  ╚████╔╝
 ╚═════╝ ╚═╝  ╚═╝ ╚═════╝   ╚═══╝    ╚═══╝
```

**Production-First Project Starter & Framework Alignment Tool**

A prompt-driven project scaffolding system that generates production-ready codebases with built-in best practices, security, and test-driven development patterns.

-----

## What is grovv-stack?

grovv-stack is an immediate project starter that:

- **Scaffolds new projects** with production-first architecture
- **Integrates into existing projects** with refactoring guidance to align with the framework
- **Generates comprehensive documentation** through executable prompts
- **Includes TaskFlow** for PostgreSQL-native background job processing

-----

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/grovv-stack.git my-project
cd my-project
```

### 2. Execute Prompts (in order)

Navigate to `/docs/prompts/` and execute each prompt to build out your project scaffolding:

```bash
# Using Claude Code CLI (recommended for VS Code workflow)
claude

# Then provide the prompts from /docs/prompts/ in sequence
```

**Prompt execution order:**

1. **skills-builder** → Generates `.skills/` and `/docs/skills/` folders
1. **tech-spec** → Creates technical specification document
1. **taskflow-setup** → Pulls TaskFlow into project or configures external connection
1. **readme-generator** → Generates project README

### 3. Build Your Project

Once scaffolding is complete, continue development with your preferred workflow.

-----

## Repository Structure

```
grovv-stack/
├── docs/
│   ├── prompts/           # Executable prompts for scaffolding
│   │   ├── skills-builder.md
│   │   ├── tech-spec.md
│   │   ├── taskflow-setup.md
│   │   └── readme-generator.md
│   ├── skills/            # Generated skill files (project-specific)
│   ├── tech-spec.md       # Generated technical specification
│   └── architecture/      # Architecture decision records
├── taskflow/              # TaskFlow integration scripts
│   └── setup.sh           # Pull TaskFlow or connect externally
├── .skills/               # Claude Code skills directory
├── README.md              # Project readme (you are here)
└── [your project files]   # Generated based on tech spec
```

-----

## Core Technology Stack

|Category         |Technology                        |Purpose                  |
|-----------------|----------------------------------|-------------------------|
|**Languages**    |TypeScript, Python                |Primary development      |
|**Runtime**      |Bun, Node.js                      |JavaScript execution     |
|**Database**     |PostgreSQL (Neon/Supabase), SQLite|Data persistence         |
|**Auth**         |Clerk                             |Identity management      |
|**Frontend**     |Astro, React/Preact               |UI development           |
|**Event Bus**    |TaskFlow                          |Background job processing|
|**Observability**|PostHog                           |Analytics & monitoring   |
|**Deployment**   |Vercel, Docker                    |Production hosting       |

-----

## Prompt System

### How Prompts Work

Each prompt in `/docs/prompts/` is designed to be executed with Claude (via CLI or claude.ai) to generate specific parts of your project:

|Prompt            |Output                    |Description                            |
|------------------|--------------------------|---------------------------------------|
|`skills-builder`  |`.skills/`, `docs/skills/`|Development best practices and patterns|
|`tech-spec`       |`docs/tech-spec.md`       |Full technical specification           |
|`taskflow-setup`  |`taskflow/` integration   |Background job processing setup        |
|`readme-generator`|`README.md`               |Project documentation                  |

### Chaining Prompts

Prompts can be chained for automated scaffolding:

```bash
# Example: Full project setup
claude --prompt docs/prompts/skills-builder.md
claude --prompt docs/prompts/tech-spec.md
claude --prompt docs/prompts/taskflow-setup.md
```

-----

## TaskFlow Integration

grovv-stack includes [TaskFlow](./taskflow/), a PostgreSQL-native task queue system:

**Features:**

- Zero external dependencies (no Redis/RabbitMQ required)
- ACID guarantees with atomic task creation
- Horizontal scaling via `SKIP LOCKED`
- Dead letter queue for failed tasks
- Idempotency support

**Setup Options:**

```bash
# Option 1: Pull into project
./taskflow/setup.sh --local

# Option 2: Connect to external TaskFlow instance
./taskflow/setup.sh --remote https://your-taskflow.sprites.dev
```

-----

## Development Workflow

### VS Code (Recommended)

```bash
# Open workspace
code grovv-stack.code-workspace

# Run with Claude Code CLI
claude

# Execute prompts and iterate
```

### Local Development

```bash
# Install dependencies
bun install

# Start development server
bun dev

# Run tests
bun test
```

### Docker Development

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

-----

## Core Principles

grovv-stack enforces these principles across all generated code:

|Principle              |Description                                        |
|-----------------------|---------------------------------------------------|
|**Production-First**   |Every implementation is production-ready from start|
|**Zero Data Loss**     |Transactional integrity is non-negotiable          |
|**Security by Default**|Security considerations never deferred             |
|**Test-Driven**        |Tests define contracts and prevent regressions     |
|**Comprehensive Docs** |Code is read more than written                     |
|**Stack Agnostic**     |Solutions work across technology stacks            |

-----

## Generated Skills

After running `skills-builder`, you’ll have:

```
.skills/
├── CLAUDE.md              # Core development philosophy
├── planning/
│   └── ARCHITECTURE.md    # System design patterns
├── frontend/
│   ├── FRONTEND.md        # UI development
│   └── UI-STANDARDS.md    # Bootstrap Minimal Stack
├── backend/
│   └── BACKEND.md         # API & service patterns
├── database/
│   └── DATABASE.md        # PostgreSQL/SQLite patterns
├── security/
│   └── SECURITY.md        # Auth, validation, protection
├── testing/
│   └── TESTING.md         # TDD workflow
└── tooling/
    ├── DEVOPS.md          # CI/CD & deployment
    ├── API-DESIGN.md      # API standards
    └── DEBUGGING.md       # Troubleshooting
```

-----

## UI Standards (New Projects)

grovv-stack uses a **Bootstrap Minimal Stack** for new projects:

- **Font:** Alexandria (fonts.bunny.net)
- **Framework:** Bootstrap 5.3+
- **Colors:** Monochrome (black/white/grey)
- **Background:** White default
- **Animations:** None (Bootstrap built-ins only)

For existing projects, the framework analyzes and matches established patterns.

-----

## Environment Variables

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

# TaskFlow
TASKFLOW_API_KEY="tf_..."
TASKFLOW_URL="https://your-taskflow.sprites.dev"
```

-----

## Integrating into Existing Projects

grovv-stack can align existing projects with the framework:

1. **Analyze current stack** - Run analysis prompts
1. **Generate alignment report** - Identify gaps and recommendations
1. **Incremental refactoring** - Apply changes progressively
1. **Maintain compatibility** - Match existing patterns where appropriate

```bash
# Analyze existing project
claude --prompt docs/prompts/analyze-existing.md

# Generate alignment recommendations
claude --prompt docs/prompts/align-framework.md
```

-----

## Resources

- **[TaskFlow Documentation](./taskflow/README.md)** - Background job processing
- **[Technical Specification Template](./docs/tech-spec-template.md)** - Project specs
- **[Skills Repository](./docs/skills/)** - Development best practices
- **[grovv.ai](https://grovv.ai)** - Framework documentation

-----

## License

Private License - This software is proprietary and confidential.

-----

## Support

For questions and support, contact the project maintainer or visit [dan.com.ai](https://dan.com.ai).

-----

<p align="center">
  <strong>Built with grovv-stack</strong><br>
  Production-first. Zero data loss. Security by default.
</p>