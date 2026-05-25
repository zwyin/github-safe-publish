"""Validate scripts/convert.sh output for all platforms."""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONVERT_SH = ROOT / "scripts" / "convert.sh"
DIST = ROOT / "dist"


def _run_convert(flag):
    result = subprocess.run(
        ["bash", str(CONVERT_SH), flag],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert result.returncode == 0, f"convert.sh {flag} failed: {result.stderr}"
    return result.stdout


def _skill_version():
    import re
    text = (ROOT / "skills" / "github-safe-publish" / "SKILL.md").read_text()
    match = re.search(r'^version:\s*"?(\d+\.\d+\.\d+)"?', text, re.MULTILINE)
    assert match
    return match.group(1)


class TestConvertCursor:
    def test_generates_mdc_files(self):
        _run_convert("--cursor")
        rules_dir = DIST / "cursor" / ".cursor" / "rules"
        assert (rules_dir / "github-safe-publish.mdc").exists()
        assert (rules_dir / "github-safe-publish-modules.mdc").exists()

    def test_mdc_has_yaml_frontmatter(self):
        _run_convert("--cursor")
        content = (DIST / "cursor" / ".cursor" / "rules" / "github-safe-publish.mdc").read_text()
        assert content.startswith("---\n")
        assert "description:" in content
        assert "alwaysApply: false" in content
        # Second --- closes frontmatter
        assert content.index("---", 3) > 0

    def test_mdc_contains_steps(self):
        _run_convert("--cursor")
        content = (DIST / "cursor" / ".cursor" / "rules" / "github-safe-publish.mdc").read_text()
        for step in ["Step 1", "Step 2", "Step 3", "Step 4", "Step 5", "Step 6"]:
            assert step in content, f"Missing {step} in core workflow"

    def test_modules_mdc_contains_optional_modules(self):
        _run_convert("--cursor")
        content = (DIST / "cursor" / ".cursor" / "rules" / "github-safe-publish-modules.mdc").read_text()
        assert "SEO" in content or "seo" in content.lower()
        assert "CI" in content or "ci" in content.lower()

    def test_mdc_version_in_description(self):
        _run_convert("--cursor")
        content = (DIST / "cursor" / ".cursor" / "rules" / "github-safe-publish.mdc").read_text()
        version = _skill_version()
        assert version in content


class TestConvertWindsurf:
    def test_generates_windsurfrules(self):
        _run_convert("--windsurf")
        assert (DIST / "windsurf" / ".windsurfrules").exists()

    def test_windsurfrules_is_markdown(self):
        _run_convert("--windsurf")
        content = (DIST / "windsurf" / ".windsurfrules").read_text()
        assert content.startswith("#")
        assert "GitHub Safe Publish" in content

    def test_windsurfrules_has_version(self):
        _run_convert("--windsurf")
        content = (DIST / "windsurf" / ".windsurfrules").read_text()
        version = _skill_version()
        assert version in content


class TestConvertOpenCode:
    def test_generates_agents_md(self):
        _run_convert("--opencode")
        assert (DIST / "opencode" / "AGENTS.md").exists()

    def test_agents_md_is_markdown(self):
        _run_convert("--opencode")
        content = (DIST / "opencode" / "AGENTS.md").read_text()
        assert content.startswith("#")
        assert "GitHub Safe Publish" in content

    def test_agents_md_has_version(self):
        _run_convert("--opencode")
        content = (DIST / "opencode" / "AGENTS.md").read_text()
        version = _skill_version()
        assert version in content


class TestConvertAll:
    def test_all_generates_all_formats(self):
        _run_convert("--all")
        assert (DIST / "cursor" / ".cursor" / "rules" / "github-safe-publish.mdc").exists()
        assert (DIST / "windsurf" / ".windsurfrules").exists()
        assert (DIST / "opencode" / "AGENTS.md").exists()

    def test_list_flag(self):
        output = _run_convert("--list")
        assert "cursor" in output.lower()
        assert "windsurf" in output.lower()
        assert "opencode" in output.lower()
