#!/usr/bin/env bash
# Structural consistency checks for grovv-stack. No dependencies beyond bash,
# coreutils, git and jq (all present on GitHub-hosted runners).
#
# Usage: scripts/check-consistency.sh [base-ref]
#   base-ref  optional git ref to diff against for the version-bump reminder
#             (CI passes the PR base, e.g. origin/main)
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

fail=0
err() { echo "::error::$*"; fail=1; }
warn() { echo "::warning::$*"; }

list_names() { # list_names <dir> <find args...> -> sorted basenames
  local dir=$1; shift
  [ -d "$dir" ] || { echo "__missing__"; return; }
  find "$dir" -mindepth 1 -maxdepth 1 "$@" -printf '%f\n' | sort
}

# 1. Every tool directory carries the same agents and skills as the canonical .grovv/.
canon_agents=$(list_names .grovv/agents -name '*.md')
canon_skills=$(list_names .grovv/skills -type d)
for tool in .claude .vibe .codex; do
  agents=$(list_names "$tool/agents" -name '*.md')
  skills=$(list_names "$tool/skills" -type d)
  [ "$agents" = "$canon_agents" ] || err "$tool/agents does not match .grovv/agents: $(diff <(echo "$canon_agents") <(echo "$agents") | grep '^[<>]' | tr '\n' ' ')"
  [ "$skills" = "$canon_skills" ] || err "$tool/skills does not match .grovv/skills: $(diff <(echo "$canon_skills") <(echo "$skills") | grep '^[<>]' | tr '\n' ' ')"
done

# 2. The Claude plugin manifest lists exactly the agents in .claude/agents/.
manifest_agents=$(jq -r '.agents[]' .claude-plugin/plugin.json | sed 's#^\./\.claude/agents/##' | sort)
claude_agents=$(list_names .claude/agents -name '*.md')
[ "$manifest_agents" = "$claude_agents" ] || err ".claude-plugin/plugin.json agents array does not match .claude/agents/*.md"
while read -r p; do
  [ -f "$p" ] || err ".claude-plugin/plugin.json references missing file $p"
done < <(jq -r '.agents[]' .claude-plugin/plugin.json)

# 3. Both plugin manifests carry the same version.
v_claude=$(jq -r '.version' .claude-plugin/plugin.json)
v_root=$(jq -r '.version' plugin.json)
[ "$v_claude" = "$v_root" ] || err "version mismatch: .claude-plugin/plugin.json=$v_claude plugin.json=$v_root"

# 4. Reminder (warning only): behavior-bearing files changed without a version bump.
base=${1:-}
if [ -n "$base" ] && git rev-parse --verify -q "$base" >/dev/null; then
  changed=$(git diff --name-only "$base"...HEAD)
  behavior=$(echo "$changed" | grep -E '^(\.grovv/|\.claude/(agents|skills)/|\.vibe/|\.codex/|docs/prompts/|grovv-stack-scaffold\.md$)' || true)
  if [ -n "$behavior" ]; then
    base_v=$(git show "$base:.claude-plugin/plugin.json" 2>/dev/null | jq -r '.version' || echo "")
    if [ "$base_v" = "$v_claude" ]; then
      warn "behavior files changed but plugin version is still $v_claude — bump it if installed users should receive this change: $(echo "$behavior" | tr '\n' ' ')"
    fi
  fi
fi

if [ "$fail" -ne 0 ]; then
  echo "consistency check failed"
  exit 1
fi
echo "consistency check passed"
