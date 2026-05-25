"""Validate that scanning rules actually detect their target patterns."""
import re
from pathlib import Path

RULES_TEXT = (Path(__file__).resolve().parent.parent / "docs" / "scanning-rules.md").read_text()


def _extract_regex(rule_name):
    """Extract the regex pattern for a given rule name from scanning-rules.md."""
    pattern = re.compile(
        rf'### {re.escape(rule_name)}\s*\n.*?- \*\*正则\*\*: `([^`]+)`',
        re.DOTALL,
    )
    match = pattern.search(RULES_TEXT)
    assert match, f"Rule '{rule_name}' not found in scanning-rules.md"
    return match.group(1)


def _detects(rule_name, test_string):
    """Assert that the rule's regex matches the test string."""
    pattern = _extract_regex(rule_name)
    assert re.search(pattern, test_string), \
        f"Rule '{rule_name}' failed to match in: {test_string[:80]}"


# --- Dimension A: Keys/Credentials ---

class TestKeyDetection:
    def test_aws_access_token(self):
        _detects("aws-access-token", "AKIAIOSFODNN7EXAMPLE")

    def test_github_pat(self):
        _detects("github-pat", "ghp_" + "A" * 36)

    def test_openai_api_key(self):
        _detects("openai-api-key", "sk-proj-" + "a" * 74 + "T3BlbkFJ" + "b" * 74)

    def test_stripe_access_token(self):
        _detects("stripe-access-token", "sk_live_" + "a" * 24)

    def test_slack_bot_token(self):
        # Split to avoid GitHub push protection flagging test data
        prefix = "xox" + "b-"
        _detects("slack-bot-token", f"{prefix}0000000000-0000000000000-TESTFAKETOKEN")

    def test_slack_webhook_url(self):
        _detects("slack-webhook-url",
                 "https://hooks.slack.com/services/TXXXXXXX/BXXXXXXX/xxxxxxxxxxxxxxxxxxxxxxxxx")

    def test_twilio_api_key(self):
        _detects("twilio-api-key", "SK" + "a" * 32)

    def test_anthropic_api_key(self):
        _detects("anthropic-api-key", "sk-ant-api03-" + "a" * 93 + "AA")

    def test_sendgrid_api_token(self):
        _detects("sendgrid-api-token", "SG." + "a" * 22 + "." + "b" * 43)

    def test_npm_access_token(self):
        _detects("npm-access-token", "npm_" + "a" * 36)

    def test_pypi_upload_token(self):
        _detects("pypi-upload-token", "pypi-AgEIcHlwaS5vcmc" + "a" * 60)

    def test_gitlab_pat(self):
        _detects("gitlab-pat", "glpat-" + "a" * 20)


# --- Dimension A2: Database Connection Strings ---

class TestDatabaseDetection:
    def test_postgres(self):
        _detects("postgres-connection-string", "postgresql://user:pass@host:5432/db")

    def test_mysql(self):
        _detects("mysql-connection-string", "mysql://root:password@localhost:3306/testdb")

    def test_mongodb(self):
        _detects("mongodb-connection-string",
                 "mongodb://admin:secret@cluster.example.com:27017/prod")

    def test_redis(self):
        _detects("redis-connection-string", "redis://:password@localhost:6379/0")

    def test_jdbc(self):
        _detects("jdbc-connection-string",
                 "jdbc:postgresql://db.example.com:5432/mydb?user=admin&password=secret")


# --- Dimension B: PII ---

class TestPIIDetection:
    def test_chinese_phone(self):
        _detects("chinese-phone-number", "13912345678")

    def test_email(self):
        _detects("email-address", "user@example.com")


# --- Dimension C: Infrastructure ---

class TestInfraDetection:
    def test_internal_domain(self):
        _detects("internal-domain-pattern", "http://nas.company.local:8080")


# --- Dimension A: Additional providers ---

class TestAdditionalProviders:
    def test_vault_service_token(self):
        _detects("vault-service-token", "hvs." + "a" * 24)

    def test_vault_batch_token(self):
        _detects("vault-batch-token", "hvb." + "a" * 24)

    def test_vault_recovery_token(self):
        _detects("vault-recovery-token", "hvr." + "a" * 24)

    def test_heroku_api_key(self):
        _detects("heroku-api-key",
                 "heroku_api_key = 12345678-1234-1234-1234-123456789012")

    def test_bitbucket_client_secret(self):
        _detects("bitbucket-client-secret",
                 'BITBUCKET_CLIENT_SECRET = "' + "a" * 45 + '"')
