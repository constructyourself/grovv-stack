# Prompt: Generate the Project's Invocable Skills

Use this prompt to generate the target project's **invocable Claude Code skills** — a set of development best-practice skills written into the project's `.claude/skills/`, each with proper YAML frontmatter and structure so Claude actually triggers and uses them. This is the most substantial generation step in the grovv stack pipeline (Step 6), run after the specs exist and before the team-design (harness) step.

These are not documentation files. Each skill is a real, loadable skill: a `SKILL.md` with `name` + `description` frontmatter, a lean body, and `references/` for depth. Claude loads a skill's metadata always, its body when triggered, and its references only on demand.

-----

## Where Skills Are Written

Run against the **target project**, this step writes into the target's `.claude/skills/`:

```
target-project/
└── .claude/
    └── skills/
        ├── dev-standards/
        │   └── SKILL.md
        ├── architecture-planning/
        │   ├── SKILL.md
        │   └── references/
        ├── frontend-development/
        │   ├── SKILL.md
        │   └── references/
        ├── ui-standards/
        │   ├── SKILL.md
        │   └── references/
        ├── backend-development/
        │   ├── SKILL.md
        │   └── references/
        ├── database-design/
        │   ├── SKILL.md
        │   └── references/
        ├── security-practices/
        │   ├── SKILL.md
        │   └── references/
        ├── testing-tdd/
        │   ├── SKILL.md
        │   └── references/
        ├── deployment-ops/
        │   ├── SKILL.md
        │   └── references/
        └── debugging/
            ├── SKILL.md
            └── references/
```

This step does **not** write to `docs/skills/` and does **not** create anything under `.claude/commands/`.

-----

## Relationship to the Team-Design (Harness) Step

This step runs **before** team-design. The best-practice skills it writes are the shared foundation the project-specific agent team executes against. The team-design step audits `.claude/skills/` (harness Phase 0) and runs a duplicate review (Phase 4-0) before adding any new skill, so it will see these baseline skills and avoid collisions. Keep the baseline names below stable so that audit is reliable.

-----

## The Baseline Skill Set

Generate these skills by default. Drop one only if it is clearly irrelevant to the project, and add project-specific ones where a domain needs them. For existing projects, customize each to the project's actual stack (see "Existing Projects" below).

| Skill folder | Triggers on | Covers |
|--------------|-------------|--------|
| `dev-standards` | Any feature or code work; "what are our standards / how should I build this" | Core philosophy, the production-first bar, the dev workflow (red-green-refactor), definition of done, when to reach for the other skills |
| `architecture-planning` | Designing a system or feature, data modeling, API contracts, pre-build planning | System design, ER modeling, API contract design, background-job patterns, the pre-development checklist, ADRs |
| `frontend-development` | Building UI, pages, components, forms, client logic | Framework patterns (Astro + React or Next.js), progressive hydration, type-safe components, forms with validation, accessibility (WCAG 2.1 AA) |
| `ui-standards` | Styling, theming, component look-and-feel | Tailwind CSS + shadcn/ui, Alexandria font, monochrome palette, white background, no animations, component examples, existing-project pattern matching; plus the practice of offering three or four disposable directions to react to before a visual question is settled — the standards above are the shipping target the chosen direction is then brought to |
| `backend-development` | APIs, services, background jobs, third-party integrations | REST standards, service and repository patterns, PostgreSQL-native background jobs, webhooks, email (Resend/Plunk), Stripe, Lago usage events |
| `database-design` | Schema, migrations, queries, data access | Schema design, indexing, migrations, query optimization, transactions, Drizzle ORM patterns |
| `security-practices` | Auth, input handling, secrets, anything user-facing | Zod validation, authN/authZ (Clerk), SQLi/XSS/CSRF prevention, secrets management, rate limiting, file-upload safety, dependency audits |
| `testing-tdd` | Writing tests, TDD, coverage, CI test wiring | Red-green-refactor, Vitest, `go test`, integration tests, Playwright E2E (ask-first), CI execution, coverage targets |
| `deployment-ops` | Deploying, CI/CD, environments, monitoring | Docker, GitHub Actions, environment management, health checks, PostHog observability, backups, rollback |
| `debugging` | Bugs, errors, performance issues, incidents | Debugging methodology, profiling, error tracking, production debugging, emergency procedures |

-----

## How to Author Each Skill

Every skill must be a properly structured, invocable Claude Code skill. Follow the same conventions the bundled harness skill-writing guide uses (`.claude/skills/harness/references/skill-writing-guide.md`):

### Frontmatter (required)

```yaml
---
name: backend-development
description: "..."
---
```

- `name` — lowercase with dashes, matching the folder name.
- `description` — the **only** trigger mechanism. Write it actively ("pushy"): state what the skill does **and** the concrete situations that should trigger it, so Claude reaches for it instead of guessing. Distinguish it from sibling skills so near-miss requests route correctly.
  - Weak: `"Backend development guidance."`
  - Strong: `"Building APIs, services, background jobs, or third-party integrations (email, Stripe, Lago) in TypeScript or Go. Covers REST design, service/repository patterns, PostgreSQL-native job queues, webhook verification, and idempotency. Use whenever adding or changing a server-side endpoint, job, or integration."`

### Body (`SKILL.md`, under 500 lines)

- Lead with the principles and the decision rules, then the highest-value patterns inline. Explain the **why**, not just "ALWAYS/NEVER" — Claude generalizes correctly from reasons.
- Write in the imperative ("validate input at the boundary", "wrap multi-step writes in a transaction").
- Keep complete, working, typed examples — never pseudo-code. The rule governs the skill's own examples and the shipping code they teach; exploratory artifacts in the throwaway tier are exempt by definition. Show the anti-pattern beside the correct pattern where it teaches something.
- When the body approaches 500 lines, move depth into `references/` and leave a one-line pointer ("for the full Stripe webhook flow, read `references/stripe.md`").

### references/ (as needed)

- Long-form examples, full code listings, and stack- or framework-specific variants go here and load only when needed.
- Reference files over ~300 lines get a table of contents at the top.
- Split by variant so only the relevant file loads (e.g. `references/astro.md` vs `references/nextjs.md`).

-----

## Content Requirements

Across the skill set:

- **Stack** — technology-agnostic, defaulting to the Core Technology Stack Reference in `grovv-stack-scaffold.md`. Read the defaults there; do not restate them here, so the stack has one copy to keep current.
- **Production-first** — every example is complete, typed, and error-handled, with security considerations built in. That is the bar for everything that ships; exploratory artifacts are exempt (see below).
- **Anti-patterns** — show what not to do and why, next to the correct alternative.
- **Traceability** — skills reference the project's `docs/tech-spec.md` for project-specific customization.

### The Throwaway Tier (state it wherever a skill implies otherwise)

Production-first governs what ships. It does not govern what is built to find out what should ship. Any generated skill that would otherwise imply everything built must clear the production bar has to say so and carry the tier — `dev-standards` above all, and `ui-standards`, `frontend-development`, `architecture-planning`, and `testing-tdd` where they touch exploration:

- An **exploratory artifact** — prototype, mockup, brainstorm, or spike — exists to be reacted to and then deleted. It may be untyped, unwired, hard-coded, hand-styled, and built from fake data. What it may never be is merged.
- It lives on a `proto/*` or `spike/*` branch, or in a gitignored `prototypes/` directory, and is deleted once the decision it informed is written down. The decision survives, not the artifact.
- It never satisfies an ask-first rule. Four mockups built in React is not a decision to use Next.js — that question is still asked, and still answered by the user.
- Code review applies three checks to it, not the production checklist: unmerged, contained, decision recorded.

The full statement of the tier is in `grovv-stack-scaffold.md`. Keep the generated wording consistent with it rather than inventing a second rule set.

### Ask-First Rules (embed these in the skills)

These standing grovv non-negotiables must live inside the relevant skills so they are enforced at the point of use:

- `frontend-development` and `ui-standards` must instruct the agent to **ask which frontend framework** (Astro + React or Next.js) before writing frontend code, unless the project has already committed to one.
- `testing-tdd` must instruct the agent to **ask what Playwright should test** before writing any E2E test — never auto-generate E2E flows.

### Quality Bar (one illustration)

```typescript
// GOOD: explicit types, validation at the boundary, transactional, typed errors
interface CreateUserParams { email: string; name: string; role: 'admin' | 'user'; }
type CreateUserResponse =
  | { success: true; userId: string }
  | { success: false; code: 'DUPLICATE_EMAIL' | 'INVALID_INPUT'; error: string };

async function createUser(params: CreateUserParams): Promise<CreateUserResponse> {
  if (!isValidEmail(params.email)) {
    return { success: false, code: 'INVALID_INPUT', error: 'Invalid email format' };
  }
  try {
    const user = await db.transaction(async (tx) => {
      const existing = await tx.query.users.findFirst({ where: eq(users.email, params.email) });
      if (existing) throw new Error('DUPLICATE_EMAIL');
      const [created] = await tx.insert(users)
        .values({ ...params, createdAt: new Date() })
        .returning({ id: users.id });
      return created;
    });
    return { success: true, userId: user.id };
  } catch (error) {
    if (error instanceof Error && error.message === 'DUPLICATE_EMAIL') {
      return { success: false, code: 'DUPLICATE_EMAIL', error: 'Email already exists' };
    }
    throw error;
  }
}
```

```typescript
// BAD (anti-pattern): untyped, no validation, no transaction, no error handling
async function createUser(email, name, role) {
  const user = await db.insert(users).values({ email, name, role });
  return user.id;
}
```

-----

## Existing Projects

Customize, don't templatize. Before generating:

- Read the actual stack (`package.json`, `go.mod`, framework configs) and the existing code conventions.
- Make each skill reflect what the project really uses — if it is Next.js, `frontend-development` covers Next.js, not Astro; if auth is not Clerk, `security-practices` covers the real provider.
- Match the project's established patterns and naming. The skills are a reference for *this* project, not a generic template.
- If the project already has skills in `.claude/skills/`, extend or update them rather than overwriting; surface conflicts instead of silently replacing.

-----

## grovv Conventions for Generated Output

- Skill and folder names are lowercase with dashes.
- Document style inside skill bodies: `-----` horizontal rules, tables for reference data, `@TODO` for unknowns, language-hinted code fences, no emoji in headings.
- Apply the gro\\/\\/ stack footer to grovv-authored skill bodies where it reads naturally (it is fine to omit on terse reference files).

-----

## Deliverable Checklist

This step is complete when, for the target project:

- [ ] Each baseline skill exists at `.claude/skills/{name}/SKILL.md` (irrelevant ones consciously dropped, project-specific ones added)
- [ ] Every `SKILL.md` has valid frontmatter (`name` matching the folder, a pushy trigger-rich `description`)
- [ ] Every body is under 500 lines, with depth pushed to `references/`
- [ ] Examples are complete, typed, and production-ready, with anti-patterns shown where useful
- [ ] Skills reflect the project's actual stack (existing projects) and reference `docs/tech-spec.md`
- [ ] The frontend-framework ask-first rule lives in `frontend-development` / `ui-standards`; the Playwright ask-first rule lives in `testing-tdd`
- [ ] The throwaway tier is stated in `dev-standards` and in every other skill that would otherwise imply everything built must clear the production bar
- [ ] Nothing was written to `docs/skills/` or `.claude/commands/`
- [ ] Baseline skill names are stable so the team-design audit can dedupe against them

-----
gro\\/\\/ stack — Skills Builder
