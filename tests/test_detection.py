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


# --- Dimension A: GitHub tokens ---

class TestGitHubTokens:
    def test_github_app_token(self):
        _detects("github-app-token", "ghs_" + "a" * 36)

    def test_github_fine_grained_pat(self):
        _detects("github-fine-grained-pat", "github_pat_" + "a" * 82)

    def test_github_oauth(self):
        _detects("github-oauth", "gho_" + "a" * 36)

    def test_github_refresh_token(self):
        _detects("github-refresh-token", "ghr_" + "a" * 36)


# --- Dimension A: Cloud providers ---

class TestCloudProviders:
    def test_gcp_api_key(self):
        _detects("gcp-api-key", "AIza" + "a" * 35)

    def test_digitalocean_pat(self):
        _detects("digitalocean-pat", "dop_v1_" + "a" * 64)

    def test_digitalocean_access_token(self):
        _detects("digitalocean-access-token", "doo_v1_" + "a" * 64)

    def test_vercel_access_token(self):
        _detects("vercel-access-token", "VERCEL_" + "a" * 32)

    def test_netlify_access_token(self):
        _detects("netlify-access-token", "nfp_" + "a" * 42)

    def test_supabase_access_token(self):
        _detects("supabase-access-token", "sbp_" + "a" * 32)

    def test_flyio_access_token(self):
        _detects("flyio-access-token", "fo1_" + "a" * 32)

    def test_deno_access_token(self):
        _detects("deno-access-token", "deno_" + "a" * 32)

    def test_scaleway_api_key(self):
        _detects("scaleway-api-key", "SCW" + "a" * 32)


# --- Dimension A: AI providers ---

class TestAIProviders:
    def test_anthropic_admin_api_key(self):
        _detects("anthropic-admin-api-key",
                 "sk-ant-admin01-" + "a" * 93 + "AA")

    def test_huggingface_token(self):
        _detects("huggingface-access-token", "hf_" + "a" * 34)

    def test_perplexity_api_key(self):
        _detects("perplexity-api-key", "pplx-" + "a" * 48)

    def test_xai_api_key(self):
        _detects("xai-api-key", "xai-" + "a" * 42)

    def test_replicate_api_token(self):
        _detects("replicate-api-token", "r8_" + "a" * 32)

    def test_deepseek_api_token(self):
        _detects("deepseek-api-token", "sk-" + "a" * 32)


# --- Dimension A: DevOps / CI ---

class TestDevOpsTokens:
    def test_gitlab_deploy_token(self):
        _detects("gitlab-deploy-token", "gldt-" + "a" * 20)

    def test_gitlab_runner_token(self):
        _detects("gitlab-runner-token", "glrt-" + "a" * 20)

    def test_gitlab_cicd_job_token(self):
        _detects("gitlab-cicd-job-token", "glcbt-" + "a" * 20)

    def test_gitlab_feed_token(self):
        _detects("gitlab-feed-token", "glft-" + "a" * 20)

    def test_gitlab_kubernetes_agent_token(self):
        _detects("gitlab-kubernetes-agent-token", "glagent-" + "a" * 20)

    def test_databricks_token(self):
        _detects("databricks-api-token", "dapi" + "a" * 32)

    def test_planetscale_token(self):
        _detects("planetscale-api-token", "pscale_tkn_" + "a" * 42)

    def test_pulumi_api_token(self):
        _detects("pulumi-api-token", "pul-" + "a" * 40)

    def test_linear_api_key(self):
        _detects("linear-api-key", "lin_api_" + "a" * 40)


# --- Dimension A: SaaS / Communication ---

class TestSaaSTokens:
    def test_notion_api_token(self):
        _detects("notion-api-token",
                 "ntn_00000000000" + "a" * 32 + "abc")

    def test_shopify_access_token(self):
        _detects("shopify-access-token", "shpat_" + "a" * 32)

    def test_shopify_shared_secret(self):
        _detects("shopify-shared-secret", "shpss_" + "a" * 32)

    def test_sendinblue_token(self):
        _detects("sendinblue-api-token", "xkeysib-" + "a" * 64)

    def test_rubygems_token(self):
        _detects("rubygems-api-token", "rubygems_" + "a" * 48)

    def test_postman_token(self):
        _detects("postman-api-token",
                 "PMAK-" + "a" * 24 + "-" + "b" * 34)

    def test_artifactory_token(self):
        _detects("artifactory-api-key", "AKCp" + "a" * 69)


# --- Dimension A: Private key / JWT ---

class TestCryptoPatterns:
    def test_private_key(self):
        _detects("private-key",
                 "-----BEGIN RSA PRIVATE KEY-----\n" + "a" * 64 + "\n-----END RSA PRIVATE KEY-----")

    def test_jwt_token(self):
        _detects("jwt-token",
                 "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.abc123def456")

    def test_kubernetes_secret_yaml(self):
        _detects("kubernetes-secret-yaml",
                 "kind: Secret\ndata:\n  password: " + "a" * 20)


# --- Dimension B: PII extended ---

class TestPIIDetectionExtended:
    def test_chinese_id_card(self):
        _detects("chinese-id-card", "110101199001011234")

    def test_us_ssn(self):
        _detects("us-ssn", "123-45-6789")

    def test_password_in_code(self):
        _detects("password-in-code", 'password = "mysecretpassword123"')


# --- Dimension C: Infrastructure extended ---

class TestInfraDetectionExtended:
    def test_internal_ip(self):
        _detects("internal-ip-address", "192.168.1.100")

    def test_internal_hostname(self):
        _detects("internal-hostname", "gitlab.internal")

    def test_local_filesystem_path(self):
        _detects("local-filesystem-path", "/Users/john/projects/secret/")

    def test_vpn_or_proxy_config(self):
        _detects("vpn-or-proxy-config", 'proxy = "10.0.0.1"')
