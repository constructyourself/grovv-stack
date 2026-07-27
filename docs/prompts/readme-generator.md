# Prompt: Project README Generator

Use this prompt to generate a comprehensive, production-ready README for your project.

-----

## Initial Prompt

```
Generate a comprehensive README.md for this project based on the technical specification and codebase.

The README should include:

1. **Project Overview**
   - Clear description of what the project does
   - Key features and capabilities
   - Value proposition

2. **Quick Start Guide**
   - Installation steps
   - Basic usage examples
   - Common workflows

3. **Technology Stack**
   - Languages and frameworks
   - Database and infrastructure
   - Third-party services

4. **Project Structure**
   - Directory layout
   - Key files and folders
   - Module organization

5. **Development Setup**
   - Prerequisites
   - Environment variables
   - Local development workflow

6. **Deployment**
   - Production deployment steps
   - Environment configuration
   - CI/CD pipeline

7. **API Documentation**
   - Endpoint overview
   - Authentication
   - Request/response examples

8. **Contributing**
   - Code standards
   - Development workflow
   - Testing requirements

9. **License and Support**
   - License information
   - Contact details
   - Support resources

Follow these principles:
- Production-first mentality
- Clear, actionable instructions
- Security by default
- Test-driven development
- Comprehensive documentation
```

-----

## Expected Output Format

### Header Section

```markdown
# Project Name

[Brief tagline or description]

[Optional: Project logo or banner]

**[Status badges: build, coverage, version, etc.]**

Quick description paragraph highlighting the core value proposition.
```

### Installation Section

```markdown
## Installation

### Prerequisites

- Node.js 20+ (LTS)
- PostgreSQL 14+
- [Other requirements]

### Quick Start

\`\`\`bash
# Clone repository
git clone https://github.com/org/project.git
cd project

# Install dependencies
npm install

# Set up environment
cp .env.example .env

# Run database migrations
npm run db:migrate

# Start development server
npm run dev
\`\`\`
```

**Every command in that block is a placeholder, and shipping it unchecked is the single most likely defect in a generated README.** It is the first thing a new contributor runs, and the template above assumes npm, a `.env.example`, and a script named `db:migrate` — none of which a Go project, a pnpm project, or a project whose migration script is named anything else will have. Four commands that fail on first use, in the document read first.

Before writing this section, replace every line with a command this project actually has:

- Take the build, test, and run commands from the `Verify` table in the project's `MEMORY.md` if Step 1 recorded one, since those were read from the project rather than assumed.
- Otherwise read them from the project directly — `package.json` scripts, a `Makefile`, a `Taskfile.yml`, or `go.mod` — using the same precedence Step 1 uses.
- Drop any line you cannot substantiate. A missing migration step is a gap someone fills; a wrong one is a bug they debug.
- Name the package manager the project actually uses. A lockfile settles it: `pnpm-lock.yaml`, `yarn.lock`, `bun.lockb`, or `package-lock.json`.

If the project has no runnable commands yet — a fresh scaffold with no code — write the section with a single `@TODO` line rather than plausible-looking commands. An empty quick start is honest; a fictional one is not.

### Technology Stack Table

```markdown
## Technology Stack

| Category | Technology | Purpose |
|----------|------------|---------|
| **Runtime** | Node.js (LTS) | JavaScript execution |
| **Database** | PostgreSQL (Neon) | Data persistence |
| **Auth** | Clerk | Identity management |
| **Frontend** | Astro + React | UI framework |
| **Deployment** | Vercel | Production hosting |
```

### Environment Variables

```markdown
## Environment Variables

Create a `.env` file in the root directory:

\`\`\`bash
# Database
DATABASE_URL="postgresql://..."
DIRECT_URL="postgresql://..."

# Authentication
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY="pk_..."
CLERK_SECRET_KEY="sk_..."

# Observability
NEXT_PUBLIC_POSTHOG_KEY="phc_..."

# Email (Resend preferred; Plunk alternative; SES only if required)
RESEND_API_KEY="re_..."
EMAIL_FROM="no-reply@example.com"

# Payments (Stripe)
STRIPE_SECRET_KEY="sk_..."
STRIPE_WEBHOOK_SECRET="whsec_..."
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY="pk_..."

# Usage tracking (Lago)
LAGO_API_KEY="..."
LAGO_API_URL="https://api.getlago.com"
\`\`\`
```

### Project Structure

```markdown
## Project Structure

\`\`\`
project/
├── src/
│   ├── components/     # React components
│   ├── pages/          # Astro pages
│   ├── lib/            # Utility functions
│   └── api/            # API routes
├── docs/               # Documentation (specs, prompts, architecture)
├── tests/              # Test suites
└── .claude/skills/     # Invocable Claude Code skills
\`\`\`
```

### Development Workflow

```markdown
## Development

### Running Tests

\`\`\`bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test
npm test -- path/to/test.ts
\`\`\`

### Building for Production

\`\`\`bash
# Build
npm run build

# Preview production build
npm run preview
\`\`\`
```

### API Documentation

```markdown
## API Documentation

### Authentication

All API endpoints require authentication via Clerk.

\`\`\`typescript
headers: {
  'Authorization': 'Bearer <clerk-session-token>'
}
\`\`\`

### Endpoints

#### GET /api/users

Returns user profile information.

**Response:**
\`\`\`json
{
  "id": "user_123",
  "email": "user@example.com",
  "createdAt": "2024-01-01T00:00:00Z"
}
\`\`\`
```

-----

## Customization Points

The generator should adapt based on:

1. **Project Type**
   - Web application
   - API service
   - CLI tool
   - Library/package

2. **Technology Stack**
   - Frontend framework (Astro, Next.js, etc.)
   - Backend runtime (Node.js, Go)
   - Database (PostgreSQL, SQLite)

3. **Deployment Target**
   - Vercel
   - Docker/K8s
   - Serverless functions

4. **Special Features**
   - Real-time features
   - Background jobs
   - Webhooks

-----

## Style Guidelines

1. **Clarity Over Cleverness**
   - Use simple, direct language
   - Avoid jargon without explanation
   - Include practical examples

2. **Action-Oriented**
   - Start sections with verbs
   - Provide copy-paste commands
   - Include expected outputs

3. **Visual Hierarchy**
   - Use headers consistently
   - Include tables for structured data
   - Add code blocks with syntax highlighting

4. **Maintenance Friendly**
   - Link to external docs that change frequently
   - Keep version-specific info minimal
   - Use relative links for internal references

-----

## Badges to Include

```markdown
![Build Status](https://img.shields.io/github/workflow/status/org/repo/CI)
![Coverage](https://img.shields.io/codecov/c/github/org/repo)
![Version](https://img.shields.io/npm/v/package)
![License](https://img.shields.io/github/license/org/repo)
```

-----

## Footer Template

```markdown
-----

## License

[License type] - See LICENSE file for details

-----

## Support

- **Documentation**: [Link to docs]
- **Issues**: [GitHub Issues](https://github.com/org/repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/org/repo/discussions)

-----

<p align="center">
  <strong>Built with grovv-stack</strong><br>
  Production-first. Zero data loss. Security by default.
</p>
```

-----

## Next Steps

After generating README:

1. Review for project-specific accuracy
2. Add screenshots or diagrams if helpful
3. Test all commands and code examples
4. Link to additional documentation
5. Keep updated as project evolves
