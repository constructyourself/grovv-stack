---
description: Kick off grovv stack scaffolding in the current project. Auto-detects new vs existing. Optional argument — new | adopt — to force the mode.
argument-hint: [new|adopt]
---

# /grovv — start grovv stack scaffolding

You are kicking off the **gro\\/\\/ stack** scaffolding process for the project in the current working directory.

## Step 1 — Read the directive

Read the master directive bundled with this plugin before writing any file:

```
${CLAUDE_PLUGIN_ROOT}/grovv-stack-scaffold.md
```

It defines the full workflow (Steps 0–9). It is authoritative — follow it end to end. Also honor the conventions in this plugin's `CLAUDE.md` and `.claude/CLAUDE.md`.

## Step 2 — Determine the mode

The argument is: `$ARGUMENTS`

- `new` — treat this as a brand-new project; start at Step 1.
- `adopt` — treat this as an existing project; start at Step 0 (assess the codebase, then propose an adoption plan and wait for approval before changing anything).
- empty — **auto-detect**: inspect the working directory. If it already contains source code, configs (`package.json`, `go.mod`, `tsconfig.json`, etc.), or a populated `docs/`, treat it as **existing** and start at Step 0. If the directory is essentially empty (or only this plugin/config is present), treat it as **new** and start at Step 1.

State which mode you detected and why before proceeding.

## Step 3 — Run the workflow, ask first

Follow the directive's steps in order, pausing for confirmation at each major artifact. Do not generate ahead of understanding:

- Ask about the product, users, core features, constraints, stack, and deployment target before generating specs.
- For existing projects, never overwrite or break working code — the approach is additive and requires an approved adoption plan.
- Standing ask-first rules: ask which frontend framework (Astro + React or Next.js) before any frontend work, and ask what Playwright should test before writing any E2E test.
- Mark unknowns with `@TODO` and revisit them.
- Apply gro\\/\\/ stack branding and document conventions to everything you generate.

The pipeline includes the **team-design (harness)** step after the skills repository is built — it designs a project-specific agent team additive to the six grovv defaults. See `docs/prompts/team-design.md`.

Begin now.
