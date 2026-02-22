# Prompt: Generate Claude Code Skills Repository

Use this prompt to create a comprehensive development best practices repository for Claude.

-----

## Initial Prompt

```
Create a repository of Claude code skills including a Claude.md that focuses on development best practices, security, and test driven development. 

Notably planning, frontend design, backend design. 

Technology agnostic, but primarily using JavaScript/TypeScript and Python. 

Postgres/SQLite for database - using Neon or Supabase as provider. 

Bun and Node.js runtimes.

Clerk for identity management when needed. 

Astro framework for content based websites.
```

-----

## Expected Repository Structure

Claude will create a comprehensive repository with the following structure:

```
claude-code-skills/
├── Core Documentation (5 files)
│   ├── Claude.md              # Core philosophy and development principles
│   ├── README.md              # Repository overview and quick start
│   ├── INDEX.md               # Complete navigation index
│   ├── QUICK-REFERENCE.md     # Cheat sheet for common patterns
│   ├── EXAMPLES.md            # Project templates
│   └── REPOSITORY-SUMMARY.md  # Comprehensive overview
│
├── Planning and Design
│   └── planning/
│       └── ARCHITECTURE.md    # System design, data modeling, API contracts
│
├── Implementation Guides
│   ├── frontend/
│   │   ├── FRONTEND.md        # Astro, React/Preact, accessibility
│   │   └── UI-STANDARDS.md    # UI design and technology standards
│   ├── backend/
│   │   └── BACKEND.md         # API design, services, background jobs
│   ├── database/
│   │   └── DATABASE.md        # PostgreSQL/SQLite patterns, migrations
│   └── security/
│       └── SECURITY.md        # Authentication, validation, secure patterns
│
├── Quality Assurance
│   └── testing/
│       └── TESTING.md         # TDD workflow, unit/integration/E2E
│
└── Operations and Tooling
    └── tooling/
        ├── DEVOPS.md          # Deployment, CI/CD, monitoring
        ├── API-DESIGN.md      # API versioning, documentation, webhooks
        ├── DEBUGGING.md       # Troubleshooting methodology
        └── DESIGN-ITERATOR.md # Iterative design refinement
```

-----

## Key Requirements

### Core Philosophy

The repository must emphasize:

1. **Production-First Mindset**: Every implementation production-ready from start
1. **Zero Data Loss**: Transactional integrity is non-negotiable
1. **Security by Default**: Never defer security considerations
1. **Test-Driven Development**: Tests define contracts and prevent regressions
1. **Comprehensive Documentation**: Code is read more than written
1. **Stack Agnostic**: Solutions work across technology stacks

### Technology Stack Coverage

**Primary Languages:**

- TypeScript/JavaScript (with strict type checking)
- Python (with type hints)

**Runtimes:**

- Bun (preferred for new projects)
- Node.js (LTS versions)

**Databases:**

- PostgreSQL (via Neon or Supabase)
- SQLite (for embedded use)
- Include migration strategies
- Query optimization patterns

**Frameworks:**

- Astro (static-first content sites)
- React/Preact (interactive components)

**Authentication:**

- Clerk (user management)
- Session handling
- Authorization patterns

**Additional Tools:**

- Drizzle ORM (type-safe queries)
- Zod (validation)
- Bun Test (testing framework)

**UI Framework (New Projects):**

- Bootstrap 5.3+ (CSS framework)
- Alexandria font (fonts.bunny.net)
- Monochrome design system (black/white/grey)
- White background default
- No custom animations

**UI Approach (Existing Projects):**

- Analyze existing frontend stack first
- Match established patterns and conventions
- Follow project’s design system
- Maintain consistency with current codebase

### Content Requirements

Each guide must include:

✅ **Production-Ready Examples**

- Fully typed (TypeScript/Python)
- Comprehensive error handling
- Security considerations built-in
- Test coverage provided
- Performance optimized

✅ **Real-World Patterns**

- Background job processing (PG-TaskFlow style)
- Authentication flows
- API versioning
- Database migrations
- Rate limiting

✅ **Anti-Patterns**

- Show what NOT to do
- Explain why it’s wrong
- Provide correct alternative

✅ **Code Examples**

- Complete, working code
- Not pseudo-code
- Include imports and types
- Show file structure context

### Specific Guide Requirements

**Claude.md** should cover:

- Core development workflow
- Technology stack guidance
- Code quality standards
- Security best practices overview
- Testing philosophy
- Performance considerations
- Deployment checklist

**ARCHITECTURE.md** should include:

- Pre-development checklist
- System design components
- Data modeling (ER design)
- API design principles
- Background job patterns
- Service layer patterns
- Specification templates
- Architecture Decision Records (ADR)

**FRONTEND.md** should cover:

- Astro framework patterns
- Progressive hydration
- Type-safe components
- Accessibility (WCAG 2.1 AA)
- Performance optimization
- Form handling with validation
- Semantic HTML and ARIA

**UI-STANDARDS.md** should include:

- UI design philosophy and technology choices
- Bootstrap Minimal Stack for new projects
- Alexandria font from fonts.bunny.net
- Monochrome color scheme (black/white/grey)
- White background default
- No custom animations policy
- Existing project analysis and pattern matching
- Complete component examples (navigation, forms, cards, tables)
- Performance optimization guidelines
- Decision tree for new vs existing projects

**BACKEND.md** should include:

- RESTful API standards
- Service layer pattern
- Repository pattern
- Background job processing
- Error handling strategies
- Rate limiting
- Webhook patterns

**DATABASE.md** should cover:

- Schema design principles
- Indexing strategies
- Migration best practices
- Query optimization
- Transaction management
- Drizzle ORM patterns
- Monitoring and maintenance

**SECURITY.md** should include:

- Input validation (Zod schemas)
- SQL injection prevention
- XSS prevention
- CSRF protection
- Secrets management
- Rate limiting strategies
- File upload security
- Security event logging

**TESTING.md** should cover:

- TDD workflow (red-green-refactor)
- Unit testing patterns
- Integration testing
- E2E testing
- Test coverage targets
- Continuous integration
- Performance testing

**DEVOPS.md** should include:

- Docker configuration
- CI/CD pipelines (GitHub Actions)
- Environment management
- Health check endpoints
- Monitoring and logging
- Backup strategies
- Platform-specific guides

**API-DESIGN.md** should cover:

- API versioning strategies
- OpenAPI/Swagger documentation
- Pagination patterns
- Filtering and searching
- Bulk operations
- Webhook systems
- SDK generation

**DEBUGGING.md** should include:

- Debugging methodology
- Common issues and solutions
- Performance profiling
- Error tracking
- Production debugging
- Emergency procedures

**DESIGN-ITERATOR.md** should cover:

- Iterative design refinement methodology
- Focused screenshot techniques
- Design principles to apply
- Avoiding “AI slop” aesthetic
- Competitor research patterns
- Typography, color, motion, backgrounds

### Mobile-Friendly Output

Additionally create:

**CLAUDE-CODE-SKILLS-COMPLETE.md**

- Single comprehensive markdown file
- All essential content consolidated
- Viewable as artifact on mobile
- Complete table of contents
- Quick reference sections
- All key code examples

-----

## Expected Statistics

The final repository should contain:

- **15-17 comprehensive guides** (including UI-STANDARDS.md)
- **200+ production-ready code examples**
- **500+ documented best practices**
- **50+ security patterns**
- **100+ test examples**
- **3,500+ lines of documentation**

-----

## Quality Standards

### Code Examples Must:

- Be complete and working (not pseudo-code)
- Include proper error handling
- Show security considerations
- Include type annotations
- Be production-ready

### Documentation Must:

- Explain the “why” not just “how”
- Include anti-patterns to avoid
- Provide complete context
- Cross-reference related guides
- Include real-world examples

### Patterns Must:

- Work across technology stacks
- Be tested in production
- Follow security best practices
- Include performance considerations
- Be maintainable long-term

-----

## Example Code Quality

**Good Example (Include):**

```typescript
// ✅ GOOD: Explicit types, comprehensive error handling
interface CreateUserParams {
  email: string;
  name: string;
  role: 'admin' | 'user';
}

interface CreateUserResult {
  userId: string;
  success: true;
}

interface CreateUserError {
  error: string;
  code: 'DUPLICATE_EMAIL' | 'INVALID_INPUT';
  success: false;
}

type CreateUserResponse = CreateUserResult | CreateUserError;

async function createUser(
  params: CreateUserParams
): Promise<CreateUserResponse> {
  try {
    // Validate input
    if (!isValidEmail(params.email)) {
      return { 
        success: false, 
        error: 'Invalid email format',
        code: 'INVALID_INPUT' 
      };
    }

    // Database operation with transaction
    const result = await db.transaction(async (tx) => {
      const existing = await tx.query.users.findFirst({
        where: eq(users.email, params.email)
      });

      if (existing) {
        throw new Error('DUPLICATE_EMAIL');
      }

      const [user] = await tx.insert(users).values({
        email: params.email,
        name: params.name,
        role: params.role,
        createdAt: new Date()
      }).returning({ id: users.id });

      return user;
    });

    return { success: true, userId: result.id };
  } catch (error) {
    if (error.message === 'DUPLICATE_EMAIL') {
      return {
        success: false,
        error: 'Email already exists',
        code: 'DUPLICATE_EMAIL'
      };
    }
    throw error; // Re-throw unexpected errors
  }
}
```

**Bad Example (Show as anti-pattern):**

```typescript
// ❌ BAD: Untyped, poor error handling
async function createUser(email, name, role) {
  const user = await db.insert(users).values({ email, name, role });
  return user.id;
}
```

-----

## Special Patterns to Include

### PG-TaskFlow Pattern

Background job processing using PostgreSQL as task queue:

```typescript
// Atomic task creation with business operation
async function createOrder(orderData: CreateOrderInput) {
  const client = await pool.connect();
  
  try {
    await client.query('BEGIN');
    
    // Create order
    const [order] = await client.query(
      'INSERT INTO orders (...) VALUES (...) RETURNING *',
      [...]
    );
    
    // Queue confirmation email
    await client.query(
      'SELECT pg_taskflow.enqueue($1, $2)',
      ['SEND_EMAIL', JSON.stringify({ orderId: order.id })]
    );
    
    await client.query('COMMIT');
    return order;
  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  } finally {
    client.release();
  }
}
```

### Clerk Authentication Pattern

```typescript
import { auth } from '@clerk/nextjs';

export async function GET(request: Request) {
  const { userId } = auth();
  
  if (!userId) {
    return new Response('Unauthorized', { status: 401 });
  }
  
  // Protected route logic
}
```

### Zod Validation Pattern

```typescript
const CreateUserSchema = z.object({
  email: z.string().email().max(255),
  name: z.string().min(1).max(100),
  role: z.enum(['admin', 'user'])
});

const result = CreateUserSchema.safeParse(input);
if (!result.success) {
  return { errors: result.error.format() };
}
```

### Bootstrap Minimal UI Pattern (New Projects)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Project Name</title>
  
  <!-- Alexandria Font from Bunny Fonts -->
  <link rel="preconnect" href="https://fonts.bunny.net">
  <link href="https://fonts.bunny.net/css?family=alexandria:400,500,600,700" rel="stylesheet">
  
  <!-- Bootstrap 5.3+ -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  
  <style>
    :root {
      --bs-body-font-family: 'Alexandria', system-ui, sans-serif;
      --bs-body-bg: #ffffff;
      --bs-body-color: #212529;
      --bs-primary: #212529;
    }
    body { font-family: 'Alexandria', sans-serif; }
  </style>
</head>
<body>
  <!-- Clean monochrome navbar -->
  <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom">
    <div class="container">
      <a class="navbar-brand fw-semibold" href="/">Brand</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <a class="nav-link" href="#features">Features</a>
          </li>
          <li class="nav-item">
            <a class="btn btn-dark ms-2" href="#signup">Sign Up</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <!-- Hero Section -->
  <section class="py-5 bg-white">
    <div class="container py-5 text-center">
      <h1 class="display-4 fw-semibold mb-3">Clean & Simple</h1>
      <p class="lead text-secondary mb-4">Fast, minimal, production-ready.</p>
      <a href="#start" class="btn btn-dark btn-lg">Get Started</a>
    </div>
  </section>

  <!-- Feature Cards -->
  <section class="py-5 bg-light">
    <div class="container">
      <div class="row g-4">
        <div class="col-md-4">
          <div class="card h-100 border-0 shadow-sm">
            <div class="card-body">
              <h3 class="h5 fw-semibold mb-3">Fast Performance</h3>
              <p class="text-secondary mb-0">Optimized for speed.</p>
            </div>
          </div>
        </div>
        <!-- More cards... -->
      </div>
    </div>
  </section>

  <!-- Bootstrap JS Bundle (no jQuery needed) -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

**Key Principles:**

- Monochrome color palette (black/white/grey)
- Alexandria font for clean typography
- White background default
- No custom animations - Bootstrap built-ins only
- Minimal dependencies for maximum performance
- Use vanilla JavaScript, not jQuery

-----

## Success Criteria

The repository is complete when:

✅ All 15-17 guides are comprehensive and production-ready  
✅ Every code example works without modification  
✅ Security is integrated into every layer  
✅ Testing patterns are clear and actionable  
✅ Mobile-friendly consolidated document exists  
✅ Cross-references between guides work  
✅ INDEX.md provides complete navigation  
✅ QUICK-REFERENCE.md serves as effective cheat sheet  
✅ EXAMPLES.md provides working project templates

-----

## Usage Instructions

1. Provide this prompt to Claude
1. Claude will create the complete repository structure
1. All files will be in `/mnt/user-data/outputs/claude-code-skills/`
1. Mobile-friendly version: `CLAUDE-CODE-SKILLS-COMPLETE.md`
1. Navigate using `INDEX.md` for desktop use

-----

## Additional Considerations

**For Mobile Users:**

- Create single comprehensive markdown artifact
- Include complete table of contents
- All essential patterns in one file
- Viewable directly in Claude interface

**For Desktop Users:**

- Full repository with 14-16 separate guides
- Detailed cross-referencing
- Complete code examples
- Project templates

**Philosophy:**
Every decision should optimize for **reliability, security, and developer experience**.

Production readiness is the default expectation, not an aspirational goal.

-----

## Expected Deliverables

After running this prompt, you should receive:

1. **Complete repository** (15-17 markdown files)
1. **Mobile-friendly artifact** (single comprehensive file)
1. **Navigation tools** (INDEX.md, QUICK-REFERENCE.md)
1. **Project templates** (EXAMPLES.md)
1. **Summary document** (REPOSITORY-SUMMARY.md)

Total documentation: **3,500+ lines** across all guides.

-----

## UI Design Standards

For new projects, the repository includes a **Bootstrap Minimal Stack** approach:

- Clean, monochrome design (black/white/grey)
- Alexandria font from fonts.bunny.net
- Bootstrap 5.3+ for all UI components
- White background by default
- No custom animations - Bootstrap built-ins only
- Minimal CSS/JS for maximum performance

For existing projects, the guide emphasizes:

- Analyze codebase first (check package.json, components, patterns)
- Match established conventions and patterns
- Follow existing design system
- Maintain consistency with current styling

The UI Standards guide provides complete examples for navigation, forms, cards, tables, and more - all using pure Bootstrap classes with the monochrome aesthetic.

-----

*This prompt generates a production-tested, comprehensive development reference covering all aspects of modern software development with Claude.*