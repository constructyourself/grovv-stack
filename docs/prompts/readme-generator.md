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

- Node.js 18+ / Bun 1.0+
- PostgreSQL 14+
- [Other requirements]

### Quick Start

\`\`\`bash
# Clone repository
git clone https://github.com/org/project.git
cd project

# Install dependencies
bun install

# Set up environment
cp .env.example .env

# Run database migrations
bun db:migrate

# Start development server
bun dev
\`\`\`
```

### Technology Stack Table

```markdown
## Technology Stack

| Category | Technology | Purpose |
|----------|------------|---------|
| **Runtime** | Bun | JavaScript execution |
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
├── docs/               # Documentation
├── tests/              # Test suites
└── .skills/            # Claude Code skills
\`\`\`
```

### Development Workflow

```markdown
## Development

### Running Tests

\`\`\`bash
# Run all tests
bun test

# Run with coverage
bun test --coverage

# Run specific test
bun test path/to/test.ts
\`\`\`

### Building for Production

\`\`\`bash
# Build
bun run build

# Preview production build
bun preview
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
   - Backend runtime (Bun, Node.js, Go)
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
