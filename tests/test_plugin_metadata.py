"""Validate plugin.json and marketplace.json metadata."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN_JSON = ROOT / ".claude-plugin" / "plugin.json"
MARKETPLACE_JSON = ROOT / ".claude-plugin" / "marketplace.json"
SKILL_MD = ROOT / "skills" / "github-safe-publish" / "SKILL.md"


def _load_json(path):
    return json.loads(Path(path).read_text())


def _skill_version():
    text = SKILL_MD.read_text()
    match = re.search(r'^version:\s*"?(\d+\.\d+\.\d+)"?', text, re.MULTILINE)
    assert match, "Cannot find version in SKILL.md frontmatter"
    return match.group(1)


# --- plugin.json ---

def test_plugin_json_exists():
    assert PLUGIN_JSON.exists()


def test_plugin_json_is_valid_json():
    _load_json(PLUGIN_JSON)


def test_plugin_json_has_required_fields():
    data = _load_json(PLUGIN_JSON)
    for field in ["name", "description", "version", "author", "license", "skills"]:
        assert field in data, f"plugin.json missing field: {field}"


def test_plugin_json_version_matches_skill():
    data = _load_json(PLUGIN_JSON)
    assert data["version"] == _skill_version()


def test_plugin_json_has_github_urls():
    data = _load_json(PLUGIN_JSON)
    assert "github.com" in data.get("homepage", "")
    assert "github.com" in data.get("repository", "")


# --- marketplace.json ---

def test_marketplace_json_exists():
    assert MARKETPLACE_JSON.exists()


def test_marketplace_json_is_valid_json():
    _load_json(MARKETPLACE_JSON)


def test_marketplace_json_has_required_fields():
    data = _load_json(MARKETPLACE_JSON)
    for field in ["name", "description", "version", "owner", "plugins"]:
        assert field in data, f"marketplace.json missing field: {field}"


def test_marketplace_json_version_matches_skill():
    data = _load_json(MARKETPLACE_JSON)
    assert data["version"] == _skill_version()


def test_marketplace_json_has_plugins():
    data = _load_json(MARKETPLACE_JSON)
    plugins = data["plugins"]
    assert len(plugins) >= 1
    assert plugins[0]["name"] == "github-safe-publish"
    assert "tags" in plugins[0]
    assert len(plugins[0]["tags"]) >= 3


def test_marketplace_json_category_is_security():
    data = _load_json(MARKETPLACE_JSON)
    assert data["plugins"][0].get("category") == "security"


# --- Version synchronization ---

def test_versions_synchronized():
    skill_ver = _skill_version()
    plugin_ver = _load_json(PLUGIN_JSON)["version"]
    market_ver = _load_json(MARKETPLACE_JSON)["version"]
    assert skill_ver == plugin_ver == market_ver, \
        f"Version mismatch: SKILL.md={skill_ver}, plugin.json={plugin_ver}, marketplace.json={market_ver}"
