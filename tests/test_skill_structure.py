"""Validate SKILL.md structure: frontmatter, step numbering, parameter consistency."""
import re


def _extract_step(text, step_num):
    """Extract content of a specific step from SKILL.md."""
    pattern = rf"## Step {step_num}:.*?\n(.*?)(?=\n## Step |\n## [^#]|\Z)"
    match = re.search(pattern, text, re.DOTALL)
    assert match, f"Step {step_num} not found"
    return match.group(1)


# --- Frontmatter ---

def test_frontmatter_has_required_fields(skill_frontmatter):
    required = ["name", "version", "description"]
    for field in required:
        assert field in skill_frontmatter, f"Missing frontmatter field: {field}"


def test_frontmatter_name_matches_skill(skill_frontmatter):
    assert skill_frontmatter.get("name") == "github-safe-publish"


def test_frontmatter_version_is_semver(skill_frontmatter):
    version = skill_frontmatter.get("version", "")
    assert re.match(r"\d+\.\d+\.\d+", version), f"Version '{version}' is not semver"


# --- Parameters ---

def test_skill_contains_all_parameters(skill_text):
    params = ["--seo", "--ci", "--scan-only", "--dry-run"]
    for param in params:
        assert param in skill_text, f"Missing parameter: {param}"


def test_skill_contains_flow_control_matrix(skill_text):
    assert "流程控制矩阵" in skill_text


# --- Step structure ---

def test_skill_has_step_headings(skill_text):
    for i in range(1, 5):
        pattern = f"## Step {i}:"
        assert pattern in skill_text, f"Missing step heading: {pattern}"


# --- Step 1: Pre-flight ---

def test_step1_contains_preflight_checks(skill_text):
    step1 = _extract_step(skill_text, 1)
    assert "git" in step1.lower()
    assert "commit" in step1.lower()
    assert "gh" in step1.lower() or "CLI" in step1


def test_step1_contains_interactive_confirmation(skill_text):
    step1 = _extract_step(skill_text, 1)
    assert "AskUserQuestion" in step1 or "交互" in step1
    assert "工作模式" in step1 or "mode" in step1.lower()


def test_step1_contains_push_method_options(skill_text):
    step1 = _extract_step(skill_text, 1)
    assert "手动推送" in step1 or "manual" in step1.lower()
    assert "自动" in step1 or "auto" in step1.lower()


def test_step1_contains_nongit_directory_handling(skill_text):
    step1 = _extract_step(skill_text, 1)
    assert "git init" in step1 or "初始化" in step1
    assert ".gitignore" in step1


# --- Step 2: Backup ---

def test_step2_defines_backup_branch(skill_text):
    step2 = _extract_step(skill_text, 2)
    assert "pre-publish-backup" in step2


def test_step2_handles_uncommitted_changes(skill_text):
    step2 = _extract_step(skill_text, 2)
    assert "stash" in step2.lower()


def test_step2_handles_stash_conflict(skill_text):
    step2 = _extract_step(skill_text, 2)
    assert "冲突" in step2 or "conflict" in step2.lower()


def test_step2_skips_in_scan_modes(skill_text):
    step2 = _extract_step(skill_text, 2)
    assert "scan-only" in step2 or "dry-run" in step2


# --- Step 3: Scanning ---

def test_step3_defines_two_layer_architecture(skill_text):
    step3 = _extract_step(skill_text, 3)
    assert "规则扫描" in step3 or "第 1 层" in step3 or "Layer 1" in step3
    assert "AI" in step3 or "语义" in step3 or "第 2 层" in step3 or "Layer 2" in step3


def test_step3_covers_five_dimensions(skill_text):
    step3 = _extract_step(skill_text, 3)
    for dim_label in ["密钥", "PII", "基础设施", "文件黑名单", "Git 历史"]:
        assert dim_label in step3, f"Missing dimension: {dim_label}"


def test_step3_references_scanning_rules_doc(skill_text):
    step3 = _extract_step(skill_text, 3)
    assert "scanning-rules" in step3


def test_step3_defines_scan_scope(skill_text):
    step3 = _extract_step(skill_text, 3)
    assert "git ls-files" in step3 or "git 跟踪" in step3 or "跟踪文件" in step3


def test_step3_ai_scan_uses_subagent(skill_text):
    step3 = _extract_step(skill_text, 3)
    assert "子 agent" in step3 or "Agent" in step3


def test_step3_defines_convergence(skill_text):
    step3 = _extract_step(skill_text, 3)
    assert "收敛" in step3 or "convergence" in step3.lower()
    assert "最多 2 轮" in step3 or "max 2" in step3.lower()


# --- Step 4: Fix ---

def test_step4_defines_severity_levels(skill_text):
    step4 = _extract_step(skill_text, 4)
    assert "CRITICAL" in step4
    assert "WARNING" in step4
    assert "SAFE" in step4


def test_step4_defines_fix_options(skill_text):
    step4 = _extract_step(skill_text, 4)
    assert "自动替换" in step4
    assert "手动修复" in step4
    assert "删除文件" in step4
    assert "确认安全" in step4


def test_step4_defines_replacement_rules(skill_text):
    step4 = _extract_step(skill_text, 4)
    assert "REPLACE_ME" in step4


def test_step4_handles_git_history(skill_text):
    step4 = _extract_step(skill_text, 4)
    assert "filter-repo" in step4 or "历史" in step4


def test_step4_defines_fix_verify_loop(skill_text):
    step4 = _extract_step(skill_text, 4)
    assert "验证" in step4
    assert "3 次" in step4


def test_step4_dry_run_shows_suggestions(skill_text):
    step4 = _extract_step(skill_text, 4)
    assert "dry-run" in step4 or "修复建议" in step4
