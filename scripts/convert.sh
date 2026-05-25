#!/usr/bin/env bash
# convert.sh — Convert SKILL.md to platform-specific formats
#
# Usage:
#   ./scripts/convert.sh --cursor     # Generate .cursor/rules/*.mdc
#   ./scripts/convert.sh --windsurf   # Generate .windsurfrules
#   ./scripts/convert.sh --opencode   # Generate AGENTS.md
#   ./scripts/convert.sh --all        # Generate all formats
#   ./scripts/convert.sh --list       # List supported platforms

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_MD="$ROOT/skills/github-safe-publish/SKILL.md"
OUT_DIR="$ROOT/dist"

# Extract SKILL.md body (everything after YAML frontmatter)
_skill_body() {
    # Find the end of frontmatter (second ---) and print everything after
    awk '/^---/{n++; next} n>=2' "$SKILL_MD"
}

# Extract version from frontmatter
_skill_version() {
    grep '^version:' "$SKILL_MD" | head -1 | sed 's/version: *//;s/"//g'
}

# Extract description from frontmatter (first line only)
_skill_description() {
    awk '/^description:/{found=1; next} found && /^\s+\|/{gsub(/^[ \t]+/, ""); print; exit} found && !/^\s+\|/{exit}' "$SKILL_MD"
}

# --- Cursor ---
_convert_cursor() {
    local cursor_dir="$OUT_DIR/cursor/.cursor/rules"
    mkdir -p "$cursor_dir"

    local version
    version=$(_skill_version)
    local desc
    desc=$(_skill_description)

    # Split into 2 files:
    # 1. Core workflow (Steps 1-6)
    # 2. Optional modules (--seo, --ci)

    local body
    body=$(_skill_body)

    # Find line numbers for section splits
    local modules_line
    modules_line=$(echo "$body" | grep -n '^## 可选模块' | head -1 | cut -d: -f1)
    local notes_line
    notes_line=$(echo "$body" | grep -n '^## 注意事项' | head -1 | cut -d: -f1)

    if [ -z "$modules_line" ]; then
        modules_line=$(echo "$body" | wc -l | tr -d ' ')
    fi

    # Core workflow file (everything before 可选模块)
    cat > "$cursor_dir/github-safe-publish.mdc" <<HEREDOC
---
description: Safely publish local Git projects to GitHub with two-layer desensitization scanning, auto-fix, backup, and end-to-end publishing workflow (v${version})
globs:
alwaysApply: false
---

$(echo "$body" | head -n $((modules_line - 1)))
HEREDOC

    # Optional modules file
    if [ -n "$modules_line" ] && [ "$modules_line" -gt 0 ]; then
        cat > "$cursor_dir/github-safe-publish-modules.mdc" <<HEREDOC
---
description: Optional SEO and CI modules for github-safe-publish (v${version})
globs:
alwaysApply: false
---

$(echo "$body" | tail -n +"$modules_line")
HEREDOC
    fi

    echo "Cursor: $cursor_dir/"
    ls -la "$cursor_dir/"
}

# --- Windsurf ---
_convert_windsurf() {
    mkdir -p "$OUT_DIR/windsurf"

    cat > "$OUT_DIR/windsurf/.windsurfrules" <<HEREDOC
# GitHub Safe Publish ($(date +%Y-%m-%d))
# Generated from skills/github-safe-publish/SKILL.md v$(_skill_version)
# Manual invokation: ask the AI to "publish to github" or "github safe publish"

$(_skill_body)
HEREDOC

    echo "Windsurf: $OUT_DIR/windsurf/.windsurfrules"
}

# --- OpenCode ---
_convert_opencode() {
    mkdir -p "$OUT_DIR/opencode"

    cat > "$OUT_DIR/opencode/AGENTS.md" <<HEREDOC
# GitHub Safe Publish ($(date +%Y-%m-%d))
# Generated from skills/github-safe-publish/SKILL.md v$(_skill_version)

$(_skill_body)
HEREDOC

    echo "OpenCode: $OUT_DIR/opencode/AGENTS.md"
}

# --- Main ---
case "${1:-}" in
    --cursor)
        _convert_cursor
        ;;
    --windsurf)
        _convert_windsurf
        ;;
    --opencode)
        _convert_opencode
        ;;
    --all)
        _convert_cursor
        _convert_windsurf
        _convert_opencode
        ;;
    --list)
        echo "Supported platforms:"
        echo "  --cursor    .cursor/rules/*.mdc (YAML frontmatter + markdown)"
        echo "  --windsurf  .windsurfrules (markdown)"
        echo "  --opencode  AGENTS.md (markdown)"
        echo "  --all       Generate all formats"
        ;;
    *)
        echo "Usage: $0 --cursor|--windsurf|--opencode|--all|--list"
        exit 1
        ;;
esac
