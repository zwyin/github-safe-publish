# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.4.0] - 2026-05-25

### Added

- **--seo module**: Description optimization, topic tags, shields.io badges, README structure check (SEO-1 to SEO-5)
- **--ci module**: Project type detection, platform matrix decision, `.github/workflows/test.yml` generation (CI-1 to CI-4)
- Plugin metadata: `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` for Claude Code marketplace
- Release script: `scripts/release.sh` for automated version bump + PR + tag workflow
- Plugin metadata tests: `tests/test_plugin_metadata.py` for validating plugin.json and marketplace.json

## [0.3.0] - 2026-05-25

### Added

- **Step 5**: Repository decision + push — interactive confirmation (visibility, name, description), placeholder URL replacement, auto-push via gh CLI with conflict handling, manual-push fallback
- **Step 6**: Verification + output report — auto-verify via gh repo view, three report formats (full / --scan-only / --dry-run)
- Step 5-6 structure tests (11 new tests)

## [0.2.0] - 2026-05-25

### Added

- **44 new scanning rules** based on Gitleaks (120+ rules) and TruffleHog (800+ detectors) source code analysis
- New dimension **A2: Database Connection Strings** (5 rules): PostgreSQL, MySQL, MongoDB, Redis, JDBC
- **Cloud/deploy platforms**: Vercel, Netlify, Supabase, Fly.io, Deno, Cloudflare Global/Origin CA, DigitalOcean, Scaleway
- **HashiCorp Vault**: service token (hvs.) + batch token (hvb.)
- **Source control**: Bitbucket (Client ID/Secret), GitLab (CI Job/Feed/K8s Agent tokens)
- **AI providers**: Google Gemini, DeepSeek, xAI, Replicate
- **Infra/DevOps**: Confluent, Fastly, LaunchDarkly, Codecov, Doppler, ClickHouse, PlanetScale, ngrok
- **Others**: Dropbox, GCP Service Account, Shopify Shared Secret, Sentry DSN, Sendinblue, Mattermost, MS Teams, Contentful
- 6 new scanning rule tests (database strings, vault tokens, cloud platforms, AI providers, bitbucket, connection string dimension)
- Rule count: 88 → 132

## [0.1.0] - 2026-05-25

### Added

- **Two-layer desensitization scanning architecture**: Layer 1 (88 deterministic regex rules, 5 dimensions) + Layer 2 (AI semantic scan via independent sub-agents)
- **5 scanning dimensions**: Keys/Credentials (58), PII (8), Internal Infrastructure (6), File Blacklist (12), Git History (4)
- **Step 1**: Pre-flight checks + centralized interactive confirmation (mode, push method, config summary)
- **Step 2**: Backup branch (`pre-publish-backup`) with stash handling and conflict resolution
- **Step 3**: Two-layer scanning with convergence (max 2 AI rounds)
- **Step 4**: Auto-fix + user confirmation (CRITICAL/WARNING/SAFE severity, 4 fix options, fix-verify loop)
- **Flow control matrix**: full / --scan-only / --dry-run modes
- Shannon entropy detection (threshold 4.5) for generic API key filtering
- `docs/scanning-rules.md`: complete regex reference for Layer 1 rules
- `tests/`: 33 structure and scanning rule tests
- `scripts/validate_skill.sh`: one-click validation script
- Competitive research: Gitleaks + TruffleHog analysis
