# Attribution — harness

This skill is vendored, mostly verbatim, from a third-party open-source project. It is bundled here so the grovv stack team-design step can generate project-specific agent teams and skills.

-----

## Source

| Field | Value |
|-------|-------|
| Project | harness — the team-architecture factory for Claude Code |
| Author | robin (revfactory) |
| Repository | https://github.com/revfactory/harness |
| Upstream version | 1.2.0 |
| Vendored commit | `cceac68ea1d0ad198ef4b7b906cd238375836387` (2026-06-10) |
| License | Apache-2.0 (see `LICENSE` in this directory) |
| Vendored on | 2026-06-12 |

-----

## What Was Vendored

- `SKILL.md` — the harness meta-skill. The workflow body and the full methodology are verbatim; only the YAML frontmatter `description` and a short top-of-body note were localized to English (see "grovv Modifications" below).
- `references/` — agent design patterns, orchestrator template, QA agent guide, skill writing/testing guides, team examples (verbatim)
- `LICENSE` — Apache-2.0 license text (verbatim)

The upstream `.claude-plugin/` manifests (`plugin.json`, `marketplace.json`) and marketing assets were intentionally not vendored — grovv stack consumes harness as an installed skill, not as a marketplace plugin.

-----

## How grovv Uses It

grovv stack does not modify the vendored **methodology**. The grovv-facing interface is `docs/prompts/team-design.md`, which adapts the harness workflow to grovv conventions (English voice, gro\\/\\/ stack branding, ask-first rules, the default stack) and points into these references for the deep pattern detail.

The vendored content is the source of truth for harness patterns. To update, re-vendor from upstream and bump the table above — do not hand-edit the workflow body or the `references/` files.

-----

## grovv Modifications

The vendored files are kept verbatim with one deliberate, documented exception in `SKILL.md`:

| Element | Change | Why |
|---------|--------|-----|
| Frontmatter `description` | Korean → English | The description is the skill's trigger text and is shown in the Claude Code skill picker; the original Korean rendered as opaque text for English users. The English version preserves the trigger intent and adds this attribution. |
| Top-of-body note | Added a short English note under the title | Surfaces the attribution and points to the English `team-design.md` interface, while leaving the workflow body untouched. |

The workflow body, the methodology, and every file under `references/` remain verbatim. When re-vendoring from upstream, re-apply these two localizations.

-----

## License Notice

```
Copyright (c) robin (revfactory)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use these files except in compliance with the License.
A copy of the License is provided in LICENSE in this directory, or at:

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
```

-----
gro\\/\\/ stack — harness attribution
