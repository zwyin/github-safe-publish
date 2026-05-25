#!/usr/bin/env bash
set -euo pipefail

echo "=== github-safe-publish skill validation ==="
echo ""

echo "1. Running pytest..."
if python3 -m pytest tests/ -v --tb=short; then
    echo ""
    echo "2. Checking file structure..."
    SKILL="skills/github-safe-publish/SKILL.md"
    RULES="docs/scanning-rules.md"

    for f in "$SKILL" "$RULES" "CLAUDE.md" "LICENSE"; do
        if [ -f "$f" ]; then
            echo "   ✓ $f"
        else
            echo "   ✗ $f MISSING"
            exit 1
        fi
    done

    echo ""
    echo "3. Checking SKILL.md version..."
    version=$(grep '^version:' "$SKILL" | head -1 | awk '{print $2}' | tr -d '"')
    if echo "$version" | grep -qE '^\d+\.\d+\.\d+$'; then
        echo "   ✓ version: $version"
    else
        echo "   ✗ Invalid version: $version"
        exit 1
    fi

    echo ""
    echo "=== All validations passed ==="
else
    echo "Tests failed!"
    exit 1
fi
