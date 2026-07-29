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
        ├── debugging/
        │   ├── SKILL.md
        │   └── references/
        ├── blind-spot-pass/
        │   └── SKILL.md
        ├── interviews/
        │   └── SKILL.md
        ├── implementation-notes/
        │   └── SKILL.md
        └── change-quiz/
            └── SKILL.md
```

The last four need no `references/` — each body is well under the 500-line limit on its own.

This step does **not** write to `docs/skills/` and does **not** create anything under `.claude/commands/`.

-----

## Relationship to the Team-Design (Harness) Step

This step runs **before** team-design. The best-practice skills it writes are the shared foundation the project-specific agent team executes against. The team-design step audits `.claude/skills/` (harness Phase 0) and runs a duplicate review (Phase 4-0) before adding any new skill, so it will see these baseline skills and avoid collisions. Keep the baseline names below stable so that audit is reliable.

-----

## The Baseline Skill Set

Generate these skills by default. Drop one only if it is clearly irrelevant to the project, and add project-specific ones where a domain needs them. For existing projects, customize each to the project's actual stack (see "Existing Projects" below).

| Skill folder | Triggers on | Covers |
|--------------|-------------|--------|
| `dev-standards` | Any feature or code work; "what are our standards / how should I build this" | Core philosophy, the production-first bar, the dev workflow (red-green-refactor), using source code as a reference, definition of done, packaging a change for review and buy-in, when to reach for the other skills |
| `architecture-planning` | Designing a system or feature, data modeling, API contracts, pre-build planning | System design, ER modeling, API contract design, background-job patterns, the pre-development checklist, brainstorming and throwaway prototypes, implementation plans ordered by what is most likely to change, ADRs |
| `frontend-development` | Building UI, pages, components, forms, client logic | Framework patterns (Astro + React or Next.js), progressive hydration, type-safe components, forms with validation, accessibility (WCAG 2.1 AA) |
| `ui-standards` | Styling, theming, component look-and-feel | Tailwind CSS + shadcn/ui, Alexandria font, monochrome palette, white background, no animations, component examples, existing-project pattern matching; plus the practice of offering three or four disposable directions to react to before a visual question is settled — the standards above are the shipping target the chosen direction is then brought to |
| `backend-development` | APIs, services, background jobs, third-party integrations | REST standards, service and repository patterns, PostgreSQL-native background jobs, webhooks, email (Resend/Plunk), Stripe, Lago usage events |
| `database-design` | Schema, migrations, queries, data access | Schema design, indexing, migrations, query optimization, transactions, Drizzle ORM patterns |
| `security-practices` | Auth, input handling, secrets, anything user-facing | Zod validation, authN/authZ (Clerk), SQLi/XSS/CSRF prevention, secrets management, rate limiting, file-upload safety, dependency audits |
| `testing-tdd` | Writing tests, TDD, coverage, CI test wiring | Red-green-refactor, Vitest, `go test`, integration tests, Playwright E2E (ask-first), CI execution, coverage targets |
| `deployment-ops` | Deploying, CI/CD, environments, monitoring | Docker, GitHub Actions, environment management, health checks, PostHog observability, backups, rollback |
| `debugging` | Bugs, errors, performance issues, incidents | Debugging methodology, profiling, error tracking, production debugging, emergency procedures |
| `blind-spot-pass` | "blind spot pass", "unknown unknowns", "what am I missing", entering an unfamiliar module or domain | Pre-work reconnaissance; establishing the user's starting point before investigating, then naming what they have not considered. **Must state where its findings came from** — supplied documents, a live search, or the model's own knowledge of the category — and say plainly when it had none of the first two. A pass that presents parametric knowledge as research is indistinguishable from one that read something, and is the more dangerous artifact. Ask for material the user already has before reasoning about what they might |
| `interviews` | "interview me", "ask me questions", an underspecified request, open `@TODO`s | One-question-at-a-time elicitation, ordered by architectural leverage, with an explicit stopping rule — questions exhausted, eight asked, or **the user stops answering**, whichever comes first; the third fires most often. Unanswered questions are recorded open, never answered on the user's behalf. **A question that went unanswered may never have arrived**: re-put it in plain prose before recording it, and record *unanswered* separately from *declined* — those are different facts and a later reader acts on them differently |
| `implementation-notes` | Starting a build from a plan; "keep implementation notes", "log deviations" | The working notes file, the Deviations log, and the conservative-default rule for a forced departure |
| `change-quiz` | "quiz me", "explain this change", pre-merge review after a long session | A change report plus a quiz on the parts a reader could get wrong; advisory by default |

**Fourteen skills, and the count is load-bearing.** `grovv-stack-scaffold.md` carries its own copy of this list and is read end to end before any file is written, so the two enumerations must agree. A change here that is not mirrored there ships a directive advertising ten baseline skills against a prompt that generates fourteen.

The last four are folder names the team-design duplicate review dedupes against, so they are as fixed as the original ten.

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

- `name` — lowercase with dashes, **matching the folder name exactly**. A mismatch means the skill never loads.
- `description` — the **only** trigger mechanism. Write it actively ("pushy"): state what the skill does **and** the concrete situations that should trigger it, so Claude reaches for it instead of guessing. Distinguish it from sibling skills so near-miss requests route correctly.
  - Weak: `"Backend development guidance."`
  - Strong: `"Building APIs, services, background jobs, or third-party integrations (email, Stripe, Lago) in TypeScript or Go. Covers REST design, service/repository patterns, PostgreSQL-native job queues, webhook verification, and idempotency. Use whenever adding or changing a server-side endpoint, job, or integration."`
  - **Keep it short enough to survive.** A few hundred characters of literal trigger phrases beats a thousand characters of prose. Because the description is the only trigger mechanism, one long enough to be truncated or rejected does not degrade the skill — it silently switches the skill off, and nothing reports that. Put the explanation in the body, where there is room for it. A smoke-test run produced four descriptions over 1024 characters, and the two worst were the skills owning the Playwright ask-first rule and the authorization gate: the two rules most expensive to lose, sitting in the two skills least likely to load.

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

### Required Sections in Two Existing Skills

Four techniques are sections inside skills that already own the subject rather than skills of their own, which keeps the trigger surface small. Each must appear in the generated body:

| Section | Goes in | Placed | Must state |
|---------|---------|--------|-----------|
| Brainstorms and prototypes | `architecture-planning` | After the pre-development checklist, before ADRs | Ask for a spread of genuinely different directions, not one idea respaced. Keep them disposable — one self-contained file, fake data, nothing wired, outside `src/`. Record the decision and delete the artifact. Production-first still governs what ships; do not harden a mock into the implementation |
| Implementation plans | `architecture-planning` | Immediately after brainstorms and prototypes | Order a plan by what is most likely to change: data model first, then types and interfaces, then anything user-facing, with mechanical refactoring last. The point is surfacing the decisions still worth altering, not the plan |
| References | `dev-standards` | After the dev workflow, before the definition of done | When you cannot describe what you want, point at something. Source code is the best reference — even in another language — because it carries structure a screenshot loses. Read it for its semantics and reimplement; do not transliterate |
| Pitches and explainers | `dev-standards` | After the definition of done | Package the prototype, spec, implementation notes and tests into one self-contained document that leads with the demo and reads in five minutes. Reviewers start with the unknowns you started with |

The prototype section carries a hard boundary that has been read wrong before, and it is stated there rather than only in the register below: **building a throwaway mock never answers the frontend-framework question.** Ask which framework before writing any real frontend code — even when a prototype exists, even when the user liked it, even when it happens to resemble one of the options. A single HTML file expresses a layout, not an architecture. Nor does a prototype get E2E tests: it is being deleted, and the Playwright rule is not satisfied by a flow that was never real.

### Ask-First Rules (embed these in the skills)

These standing grovv non-negotiables must live inside the relevant skills so they are enforced at the point of use:

- `frontend-development`, `ui-standards`, and `architecture-planning` must instruct the agent to **ask which frontend framework** (Astro + React or Next.js) before writing frontend code, unless the project has already committed to one. In `architecture-planning` the rule is stated for the prototype case: building a throwaway mock never answers the framework question, however much the user liked the mock.
- `testing-tdd` and `architecture-planning` must instruct the agent to **ask what Playwright should test** before writing any E2E test — never auto-generate E2E flows. In `architecture-planning` the rule is stated as a prohibition: a prototype gets no E2E tests at all.

**When two generated artifacts disagree about an ask-first answer, report the disagreement — never resolve it.** A skill asserting Astro while `docs/tech-spec.md` names Next.js is a real conflict, and both files are generated, so neither settles it. Picking the spec because it is "more authoritative" answers the framework question with an artifact this pipeline wrote, which is the exact pre-emption the rule exists to prevent — and picking the skill is the same error facing the other way. Name both files, quote what each asserts, and ask the user which is right. Write nothing to either until they answer. The same holds for Playwright scope.

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

## Generated CI

After the skills exist, this step asks how much continuous integration the project should have and generates it. The question, its four options, and the rules governing the answer are in `grovv-stack-scaffold.md` under Step 6 — ask it there, in those words. What follows is how to build what the answer asks for.

**Only from recorded commands.** Step 1 discovered the project's verify commands and their sources. Those are the only commands that may appear in a generated workflow. If the user picks a check Step 1 did not find, say so and offer to add the underlying script first — do not write a job that invokes a command the project cannot run.

| Stack | Checks available | Notes |
|-------|-----------------|-------|
| TypeScript | the project's test runner, `tsc --noEmit`, the project's linter, `build` | Use whatever the project actually uses. Do not substitute Vitest into a project on another runner, or `npm` into a project on pnpm |
| Go | `go test ./...`, `go vet ./...`, `golangci-lint run` | Include `golangci-lint` only when its config file is present |
| Both | The union, as separate jobs | A Go failure and a TypeScript failure should be separately legible |

**Workflow shape:**

- Each check is its own named step, so a failure names itself in the interface rather than requiring a log read.
- Later steps run even after an earlier one fails, so one run reports every problem instead of only the first.
- Triggers are push and pull request, unless the user says otherwise.
- Install and cache dependencies. A generated workflow runs against a real toolchain and must actually be able to run.
- Pin actions to major version tags.

**Never generate:** a Playwright or E2E job (the ask-first rule is not answered by a workflow file — see Step 6), or any deploy, release, or publish job. This is a verification loop, not a delivery pipeline, and a generated deploy job touches credentials and live systems.

**When the project already has CI**, this becomes a proposal. Report what the existing workflow runs, name the specific gap the addition would close, and write nothing until the user approves. Preserving an existing job — including an existing E2E job — is the user's prior decision standing, not this step generating one.

Record the outcome either way: the commands wired up, or that CI was offered and declined and why. Step 8 writes it into the project's `MEMORY.md` Verify table.

-----

## Existing Projects

Customize, don't templatize. Before generating:

- Read the actual stack (`package.json`, `go.mod`, framework configs) and the existing code conventions.
- Make each skill reflect what the project really uses — if it is Next.js, `frontend-development` covers Next.js, not Astro; if auth is not Clerk, `security-practices` covers the real provider.
- Match the project's established patterns and naming. The skills are a reference for *this* project, not a generic template.
- If the project already has skills in `.claude/skills/`, extend or update them rather than overwriting; surface conflicts instead of silently replacing.

-----

## Re-entry

A later run of this prompt does not regenerate the skill set. It reconciles the
skills already in `.claude/skills/` against the current `docs/tech-spec.md`.
These are the standing rules about how, and they hold on every run after the
first — on run 2 and on run 12.

The question a re-entry asks is one question:

> Given a specification that has moved since these artifacts were generated,
> which of them are still implied by it?

Three answers, three actions:

| Verdict | Meaning | Action |
|---------|---------|--------|
| Unchanged | The skill's assumptions still match the spec | Leave it alone and say so |
| Drifted | The spec changed under it — a different database, a dropped integration, a renamed component | Propose the specific revision, name the spec line that moved |
| Orphaned | Nothing in the current spec justifies it | Surface it for removal; never delete without approval |

- **Audit before writing.** List every folder in `.claude/skills/`, and for each
  one the stack its body asserts — framework, database, auth provider,
  integrations, test runner. Separate the skills this pipeline generated from
  skills the project already had; the latter are governed by "Existing Projects"
  above and are audited, never rewritten. Nothing is written until that list
  exists.
- **Diff against the current spec.** Re-read `docs/tech-spec.md` and give every
  generated skill exactly one verdict from the table above. A drifted verdict
  names the line of the spec that moved, so the report can be checked rather
  than trusted. This is the only check that catches a skill teaching the wrong
  stack.
- **Report before acting.** Present the three lists and **wait**. Never delete
  silently. Report the unchanged skills too — a report that names only what will
  change cannot be told from a report that skipped half the directory.
- **Update, never append blindly.** A skill whose folder name already exists is
  revised in place. Never create a suffixed sibling — no `testing-tdd-v2`, no
  `testing-tdd-new`. The baseline names are fixed so the team-design audit can
  dedupe against them, and a duplicate folder breaks exactly that.
- **Absence is a question, not a fact.** A baseline folder that is missing is
  either explained by the current spec — a project with no database needs no
  `database-design` — or it is unexplained. Explained, say so and move on.
  Unexplained, ask before regenerating. A re-entry never silently resurrects a
  skill a previous run consciously dropped, and never silently removes one.
- **Preserve hand edits.** A generated skill that has been edited by hand is
  reported as hand-edited and asked about. It is never overwritten and never
  skipped. Name what drifted and what the edit appears to protect, and let the
  user decide. When the signal is ambiguous, report it as possibly hand-edited;
  a false alarm costs a turn, a missed one costs someone's work.
- **A previous run is not an answer to an ask-first rule.** The frontend
  framework (Astro + React or Next.js) and the Playwright E2E scope are
  inherited from the user, never from an earlier run's output. A re-entry
  decides neither and re-litigates neither: it does not treat a generated
  artifact as evidence that a choice was made, and it does not re-ask a
  question the user has already answered. Where the record is genuinely
  absent, it asks. Where two generated artifacts disagree, the rule above
  applies — report both, resolve neither.
- **A re-entry does not advance the pipeline on its own.** Reconciling this step
  is a complete outcome. Continue to `team-design.md` (Step 7) only if the user
  asks for it.

A re-entry that changes nothing and returns a list of questions has succeeded.
No action is a valid result of this step.

-----

## grovv Conventions for Generated Output

- Skill and folder names are lowercase with dashes.
- Document style inside skill bodies: `-----` horizontal rules, tables for reference data, `@TODO` for unknowns, language-hinted code fences, no emoji in headings.
- Apply the gro\\/\\/ stack footer to grovv-authored skill bodies where it reads naturally (it is fine to omit on terse reference files, and on `blind-spot-pass`, `interviews`, `implementation-notes` and `change-quiz`, which carry a one-line technique attribution instead).

-----

## Deliverable Checklist

This step is complete when, for the target project:

- [ ] Each baseline skill exists at `.claude/skills/{name}/SKILL.md` (irrelevant ones consciously dropped, project-specific ones added)
- [ ] Every `SKILL.md` has valid frontmatter (`name` matching the folder **exactly**, a pushy trigger-rich `description`)
- [ ] **Every skill folder actually contains a `SKILL.md`** — count the folders, count the files, compare. A folder holding only `references/` is a skill that never loads. If generation ran concurrently, confirm it has *finished* before concluding anything is missing: a folder appears when its first reference file lands, well before its skill, and an absence observed mid-flight is not evidence of a defect
- [ ] No `description` is long enough to risk truncation — literal triggers, not prose
- [ ] Every body is under 500 lines, with depth pushed to `references/`
- [ ] **Where tool directories are derived from `.grovv/`, they were refreshed after generation settled and the refresh was verified** — `.grovv/` is canonical but `.claude/`, `.vibe/` and `.codex/` are what the tools load, so a mirror taken mid-generation leaves the loadable copy stale and every later audit reads the copy that does not run. Compare canonical against each derived tree; where the project adapts files per tool rather than copying them byte for byte, confirm that the *only* differences are those deliberate adaptations. A plain byte-comparison will flag intended per-tool content as drift, so decide which model the project uses before treating any difference as a fault
- [ ] Examples are complete, typed, and production-ready, with anti-patterns shown where useful
- [ ] Skills reflect the project's actual stack (existing projects) and reference `docs/tech-spec.md`
- [ ] The frontend-framework ask-first rule lives in `frontend-development`, `ui-standards` and `architecture-planning`; the Playwright ask-first rule lives in `testing-tdd` and `architecture-planning`
- [ ] The four unknowns skills exist: `blind-spot-pass`, `interviews`, `implementation-notes`, `change-quiz`
- [ ] `blind-spot-pass` triggers on the literal phrases "blind spot pass" and "unknown unknowns", and establishes the user's starting point before investigating
- [ ] `interviews` carries the stopping rule; `change-quiz` is advisory and states the one line that makes it blocking
- [ ] `architecture-planning` carries the brainstorms/prototypes and implementation-plan sections, including the statement that a prototype is not a frontend-framework commitment
- [ ] `dev-standards` carries the references and pitches/explainers sections
- [ ] Both baseline enumerations say fourteen — the table above and the mirrored one in `grovv-stack-scaffold.md`, with its project tree and its expected-output count
- [ ] The throwaway tier is stated in `dev-standards` and in every other skill that would otherwise imply everything built must clear the production bar
- [ ] Nothing was written to `docs/skills/` or `.claude/commands/`
- [ ] Baseline skill names are stable so the team-design audit can dedupe against them, and `team-design.md` lists the same fourteen
- [ ] Any disagreement between a generated artifact and `docs/tech-spec.md` about an ask-first answer was reported to the user and resolved by them, not by this step
- [ ] The CI question was asked with the project's real commands, and the generated workflow runs only commands Step 1 recorded — or CI was explicitly declined and the reason carried forward
- [ ] The generated workflow contains no Playwright/E2E job and no deploy, release, or publish job
- [ ] On a re-entry, every generated skill carried a verdict — unchanged, drifted, or orphaned — and the report was presented before anything was written
- [ ] No hand-edited skill was overwritten, and no baseline skill was silently resurrected or silently removed
- [ ] No skill folder was duplicated with a suffix

-----
gro\\/\\/ stack — Skills Builder
