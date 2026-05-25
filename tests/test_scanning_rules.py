"""Validate scanning rules in docs/scanning-rules.md."""
import re


def test_rules_file_exists(rules_text):
    assert len(rules_text) > 200


def test_all_five_dimensions_covered(rules_text):
    dimensions = ["密钥", "PII", "内部基础设施", "文件黑名单", "Git 历史"]
    for dim in dimensions:
        assert dim in rules_text, f"Missing dimension: {dim}"


def test_regex_patterns_are_valid(rules_text):
    """All regex patterns in backtick blocks that look like regexes must be valid."""
    pattern_blocks = re.findall(r"`([^`]+)`", rules_text)
    for p in pattern_blocks:
        # Skip non-regex strings: plain words, URLs, file paths, quoted strings
        if p.startswith("http") or p.startswith(".") or p.startswith("/"):
            continue
        # Must contain regex metacharacters to be considered a regex
        if not any(c in p for c in r"\[](){}*+?.^$|"):
            continue
        # Skip patterns that are clearly not regex (e.g., markdown formatting)
        stripped = p.strip('"\'')
        if stripped in ('***', '**', '___', '---', '*'):
            continue
        try:
            re.compile(p)
        except re.error as e:
            assert False, f"Invalid regex: {p!r} — {e}"


def test_entropy_detection_defined(rules_text):
    assert "熵" in rules_text or "entropy" in rules_text.lower()
    assert "4.5" in rules_text


def test_secret_detection_covers_major_providers(rules_text):
    providers = ["AWS", "GitHub", "OpenAI", "Stripe"]
    lower_text = rules_text.lower()
    for provider in providers:
        assert provider.lower() in lower_text, f"Missing provider: {provider}"


def test_pii_covers_chinese_patterns(rules_text):
    assert "1[3-9]" in rules_text or "手机" in rules_text
    assert "身份证" in rules_text or "ID number" in rules_text


def test_infrastructure_covers_internal_patterns(rules_text):
    assert "192.168" in rules_text
    assert "/Users/" in rules_text or "C:\\\\Users" in rules_text
