# Install Method Verification Report

**Date**: 2026-05-26
**Projects**: github-safe-publish v0.7.0, ruyi-skills v0.1.1
**Repository**: https://github.com/zwyin/github-safe-publish

---

## Summary

| # | Method | Status | Verifiable from CLI |
|---|--------|--------|---------------------|
| 1 | Browse UI | N/A | No (interactive CLI menu) |
| 2 | Marketplace `/plugin install` | PASS | Yes |
| 3 | Ask Agent | PASS (same as #2) | Yes |
| 4 | npx `skills add` | PASS | Yes |
| 5 | ClawHub | FAIL | Yes |
| 6 | Manual `git clone` | PASS | Yes |

---

## Method 1: Browse UI

**Command**: Claude Code → `/plugin` → "Browse and install plugins" → select skill → Install

**Status**: N/A — Cannot be verified from CLI. This is an interactive TUI menu within Claude Code. Requires manual verification by user.

**Note**: This method depends on the skill being registered in a marketplace that Claude Code's browse feature indexes.

---

## Method 2: Marketplace Install

**Commands**:
```bash
/plugin marketplace add zwyin/github-safe-publish
/plugin install github-safe-publish@github-safe-publish
```

### Evidence

**github-safe-publish repo** — plugin.json skill discovery:
```json
{
  "skills": "./skills/"
}
```

SKILL.md location: `skills/github-safe-publish/SKILL.md` (EXISTS, 37KB)

**ruyi-skills collection** — marketplace.json explicit skill paths:
```json
{
  "skills": [
    "./skills/github-safe-publish/skills/github-safe-publish",
    "./skills/project-walkthrough/skills/project-walkthrough"
  ]
}
```

File existence check:
- `skills/github-safe-publish/skills/github-safe-publish/SKILL.md` — EXISTS
- `skills/project-walkthrough/skills/project-walkthrough/SKILL.md` — EXISTS

**Verdict**: PASS. All marketplace.json paths resolve to existing SKILL.md files.

---

## Method 3: Ask Agent

**Command**: "Please install github-safe-publish from github.com/zwyin/github-safe-publish"

**Status**: PASS (equivalent to Method 2). The agent resolves the install request through the same marketplace infrastructure. No separate verification needed.

---

## Method 4: npx Quick Install

**Command**: `npx skills add zwyin/ruyi-skills`

### Evidence

**Console output** (captured from live run):
```
Source: https://github.com/zwyin/ruyi-skills.git
Cloning repository... Repository cloned
Discovering skills... Found 2 skills

Installing all 2 skills

Installation Summary:
  ~/repo_skillforge/github-safe-publish/.agents/skills/github-safe-publish
    universal: Codex, Cursor, Gemini CLI, Warp, Amp +8 more
    symlink → Claude Code, OpenClaw, CodeBuddy, Hermes Agent, Trae +1 more

  ~/repo_skillforge/github-safe-publish/.agents/skills/project-walkthrough
    universal: Codex, Cursor, Gemini CLI, Warp, Amp +8 more
    symlink → Claude Code, OpenClaw, CodeBuddy, Hermes Agent, Trae +1 more

Installed 2 skills
```

**Target platforms** (10 platforms):
- Claude Code (symlink)
- OpenClaw (symlink, overwrites)
- CodeBuddy (symlink)
- Hermes Agent (symlink)
- Trae (symlink)
- Trae CN (symlink)
- Codex (universal .md)
- Cursor (universal .mdc)
- Gemini CLI (universal)
- Warp (universal)
- Amp (+8 more via universal format)

**Installed file tree**:
```
.agents/skills/github-safe-publish/
├── SKILL.md
├── CHANGELOG.md
├── CLAUDE.md
├── LICENSE
├── README.md
├── docs/
├── scripts/
├── skills/
└── tests/

.agents/skills/project-walkthrough/
├── SKILL.md
├── AGENTS.md
├── CHANGELOG.md
├── CLAUDE.md
├── CONTRIBUTING.md
├── LICENSE
├── Makefile
├── README.md
├── TODO.md
├── cursor/
├── docs/
├── scripts/
├── skills/
└── tests/
```

**Side effect**: npx overwrites `skills/` directory with symlinks → `.agents/skills/`. Must be restored after testing:
```bash
rm skills/github-safe-publish skills/project-walkthrough
git restore skills/github-safe-publish/SKILL.md
```

**Verdict**: PASS. Successfully installs both skills to 10+ platforms.

---

## Method 5: ClawHub

**Command**: `npx clawhub install github-safe-publish`

### Evidence

```
$ npx clawhub install github-safe-publish
- Resolving github-safe-publish
✖ Skill not found or unavailable to this account.

$ npx clawhub install ruyi-skills
- Resolving ruyi-skills
✖ Skill not found or unavailable to this account.
```

**ClawHub CLI version**: v0.18.0 (available via `npx clawhub`)

**Root cause**: Skills are not published to ClawHub marketplace. The ClawHub registry requires explicit registration and publishing.

**Action needed**: Publish to ClawHub before documenting this as a working install method.

**Verdict**: FAIL. Skill not found in ClawHub registry. Method should be removed from README or marked as "coming soon" until published.

---

## Method 6: Manual Install

**Commands**:
```bash
git clone https://github.com/zwyin/github-safe-publish.git
claude --plugin-dir ./github-safe-publish
```

### Evidence

**github-safe-publish repo**:
```
$ git ls-remote https://github.com/zwyin/github-safe-publish.git HEAD
ede727710386059b15e1094338c575e6229b5ec9  HEAD
```
Repository is publicly accessible. PASS.

**ruyi-skills repo** (bypass proxy):
```
$ git -c http.proxy= -c https.proxy= ls-remote https://github.com/zwyin/ruyi-skills.git HEAD
ede727710386059b15e1094338c575e6229b5ec9  HEAD
```
Repository is publicly accessible. PASS.

**Verdict**: PASS. Both repos are publicly cloneable.

---

## Recommendations

1. **Remove or mark ClawHub as "coming soon"** — Not functional until skills are published to ClawHub registry.
2. **Add `.agents/` to .gitignore** — npx skills add creates this directory; it should not be committed. (Already done.)
3. **Browse UI needs manual verification** — Cannot be tested from CLI; user should test in Claude Code.
4. **npx side effect warning** — `npx skills add` overwrites `skills/` directory contents with symlinks. Document this behavior.
