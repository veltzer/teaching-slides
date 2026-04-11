---
tags:
  - practices:devops
  - concepts:architecture
  - practices:ci-cd
  - infrastructure:infrastructure-as-code
level: advanced
category: devops
audience:
  - audiences:architects
  - audiences:devops
  - audiences:managers

---
# Configuration and Secrets Management

---
## Why Configuration Management Matters

- Applications need different settings per environment
- Hardcoding values leads to inflexible, insecure deployments
- Configuration drift causes "works on my machine" problems
- Secrets leaked in code are a top security incident cause
- Proper management enables reproducibility and auditability

---
## The Configuration Spectrum

![the_configuration_spectrum](svg/courses/devops/architectural-decisions-in-devops/10_configuration_and_secrets_management/the_configuration_spectrum.svg)

---
## Baked-in vs Runtime Configuration

- **Baked-in**: configuration embedded into the artifact at build time
- **Runtime**: configuration injected when the application starts or while running
- Each approach has distinct tradeoffs in flexibility, safety, and complexity
- Most production systems use a combination of both

---
## Baked-in Configuration

- Configuration values are set during the build or packaging step
- The resulting artifact (container image, binary) is self-contained
- Examples: compiled feature flags, bundled `config.json`, baked `ENV` in `Dockerfile`

```dockerfile
FROM node:20-alpine
ENV APP_MODE=production
COPY config/prod.json /app/config.json
RUN npm run build
```

---
## Immutable Deployments with Baked Config

- Each environment gets its own built artifact
- Rolling back means deploying a previous artifact, not changing config
- No configuration drift between what was tested and what runs

---
## Immutable Deployments with Baked Config

![immutable_deployments_with_baked_config](svg/courses/devops/architectural-decisions-in-devops/10_configuration_and_secrets_management/immutable_deployments_with_baked_config.svg)

---
## Baked-in Config: Pros and Cons

- Pros:
    - Artifact is fully testable as-is -- what you test is what you deploy
    - No external dependencies at startup
    - Simplifies debugging -- config is inside the artifact
    - Works well with immutable infrastructure patterns
- Cons:
    - Separate build per environment increases CI/CD time
    - Changing a single config value requires a full rebuild
    - Secrets should never be baked into artifacts

---
## Runtime Configuration

- Configuration is provided when the application starts
- Common mechanisms: environment variables, mounted files, config servers
- The same artifact can run in different environments

```yaml
# docker-compose.yml
services:
  app:
    image: myapp:v1.2
    environment:
      - DB_HOST=prod-db.example.com
      - LOG_LEVEL=warn
    volumes:
      - ./config/prod.yaml:/app/config.yaml
```

---
## Runtime Config Injection Flow

![runtime_config_injection_flow](svg/courses/devops/architectural-decisions-in-devops/10_configuration_and_secrets_management/runtime_config_injection_flow.svg)

---
## Runtime Config: Pros and Cons

- Pros:
    - Single artifact across all environments (build once, deploy many)
    - Quick config changes without rebuilding
    - Enables dynamic tuning in production
    - Easier secret injection at deploy time
- Cons:
    - External dependency at startup
    - Config drift risk between environments
    - Harder to reproduce exact deployment state

---
## Baked vs Runtime: Decision Matrix

![baked_vs_runtime_decision_matrix](svg/courses/devops/architectural-decisions-in-devops/10_configuration_and_secrets_management/baked_vs_runtime_decision_matrix.svg)

---
## Dynamic Configuration and Feature Toggles

- Config values can change while the application is running
- No restart required -- the app watches for changes
- Feature toggles decouple deployment from feature release
- Categories: release toggles, experiment toggles, ops toggles, permission toggles

```json
{
  "features": {
    "new_checkout_flow": {
      "enabled": true,
      "rollout_percentage": 25
    },
    "dark_mode": { "enabled": false }
  }
}
```

---
## Feature Toggle Platforms

- `LaunchDarkly` -- commercial, full-featured
- `Unleash` -- open source, self-hosted
- `Flagsmith` -- open source with hosted option
- `AWS AppConfig` -- AWS-native feature flags
- `ConfigCat` -- simple, developer-friendly
- Custom solutions using config stores like `etcd` or `Consul`

---
## Restart vs Hot-Reload Tradeoffs

| Aspect | Restart | Hot-Reload |
|--------|---------|------------|
| Downtime | Brief interruption | Zero downtime |
| Complexity | Simple, stateless | Must handle state |
| Safety | Clean slate | Risk of partial state |
| Config validation | At startup | Must validate in-flight |
| Debugging | Easier | Harder to reproduce |

---
## Implementing Hot-Reload

- File watchers: `inotify`, `fsnotify`, `chokidar`
- Signal handlers: send `SIGHUP` to trigger reload
- Polling: periodically check config source for changes

```python
import signal
import json

def reload_config(signum, frame):
    with open("/app/config.json") as f:
        global config
        config = json.load(f)

signal.signal(signal.SIGHUP, reload_config)
```

---
## When to Restart vs Hot-Reload

- **Restart** when:
    - Config changes are infrequent
    - Application is stateless or easily drained
    - You need guaranteed clean state
    - Rolling deployments handle zero-downtime already
- **Hot-reload** when:
    - Changes are frequent (feature toggles, rate limits)
    - Application holds long-lived connections
    - Restart cost is high (JVM warm-up, cache rebuild)

---
## Secrets Management: The Problem

- Secrets include: database passwords, API keys, TLS certificates, tokens
- Secrets in source code get leaked via `git` history, logs, or error messages
- Secrets in environment variables can be exposed via `/proc`, `ps`, or crash dumps
- Shared secrets across teams are hard to rotate and audit

---
## Common Anti-Patterns for Secrets

1. Committing secrets to `git` repositories
1. Storing secrets in plaintext config files
1. Sharing secrets via email, Slack, or sticky notes
1. Using the same secret across all environments
1. Never rotating secrets after team member departures
1. Embedding secrets in container images

---
## Secrets Management Approaches

![secrets_management_approaches](svg/courses/devops/architectural-decisions-in-devops/10_configuration_and_secrets_management/secrets_management_approaches.svg)

---
## HashiCorp Vault Overview

- Centralized secrets management platform
- Provides dynamic secrets, encryption as a service, and identity-based access
- Supports multiple auth methods: `LDAP`, `OIDC`, `Kubernetes`, tokens
- Secrets engines: `KV`, `database`, `PKI`, `SSH`, `transit`
- Audit logging for every secret access

---
## Vault Architecture

![vault_architecture](svg/courses/devops/architectural-decisions-in-devops/10_configuration_and_secrets_management/vault_architecture.svg)

---
## Using Vault: Basic Workflow

```bash
# Authenticate
vault login -method=oidc

# Write a secret
vault kv put secret/myapp/db \
  username="admin" \
  password="s3cur3P@ss"

# Read a secret
vault kv get secret/myapp/db

# Application fetches at startup
export DB_PASS=$(vault kv get \
  -field=password secret/myapp/db)
```

---
## Vault Dynamic Secrets

- Vault generates short-lived credentials on demand
- Credentials are unique per client and automatically revoked
- Supported backends: `PostgreSQL`, `MySQL`, `MongoDB`, `AWS IAM`, `Azure`, `GCP`

```bash
# Configure database secrets engine
vault write database/config/mydb \
  plugin_name=postgresql-database-plugin \
  connection_url="postgresql://{{username}}:{{password}}@db:5432"

# Get dynamic credentials (auto-expire)
vault read database/creds/readonly
# Returns: username=v-token-readonly-abc, password=xyz, ttl=1h
```

---
## Cloud-Native Secrets Managers

- **AWS Secrets Manager**: automatic rotation, RDS integration, cross-account sharing
- **AWS SSM Parameter Store**: free tier, simple key-value, integrated with IAM
- **GCP Secret Manager**: versioned secrets, IAM-based access, audit logging
- **Azure Key Vault**: HSM-backed, certificate management, RBAC integration
- All provide SDK-based access, encryption at rest, and API-driven retrieval

---
## Encrypted Config Files

- Secrets are encrypted and stored alongside code in `git`
- Decryption key is managed separately (KMS, GPG, age)
- Tools: `SOPS`, `git-crypt`, `age`, `Sealed Secrets`
- Good for small teams or when a full secrets manager is overkill

```yaml
# .sops.yaml
creation_rules:
  - path_regex: secrets/.*\.yaml$
    kms: arn:aws:kms:us-east-1:123:key/abc-def
```

```bash
# Encrypt and decrypt at deploy time
sops -e secrets/prod.yaml > secrets/prod.enc.yaml
sops -d secrets/prod.enc.yaml
```

---
## Vault vs Encrypted Config: When to Use Each

| Criteria | Vault / Secrets Mgr | Encrypted Config |
|----------|---------------------|------------------|
| Team size | Large, multiple teams | Small, single team |
| Rotation needs | Frequent, automated | Infrequent, manual |
| Audit requirements | Strict compliance | Basic tracking |
| Dynamic secrets | Yes | No |
| Infrastructure | Requires running service | No extra infra |
| Learning curve | Steeper | Lower |

---
## Kubernetes Secrets

- Native `Secret` objects stored in `etcd`
- Base64-encoded by default (not encrypted)
- Should enable encryption at rest via `EncryptionConfiguration`
- Better alternatives: `External Secrets Operator`, `Sealed Secrets`, CSI driver

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
type: Opaque
data:
  username: YWRtaW4=
  password: cEBzc3dvcmQ=
```

---
## External Secrets Operator

- Syncs secrets from external providers into Kubernetes `Secret` objects
- Supports `Vault`, `AWS Secrets Manager`, `GCP SM`, `Azure KV`
- Keeps Kubernetes secrets in sync with the source of truth

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-secret
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: ClusterSecretStore
  target:
    name: db-credentials
  data:
    - secretKey: password
      remoteRef:
        key: secret/myapp/db
        property: password
```

---
## Secret Rotation: Why It Matters

- Limits the blast radius of a compromised credential
- Compliance frameworks (SOC2, PCI-DSS, HIPAA) require periodic rotation
- Former employees may retain knowledge of static secrets
- Automated rotation reduces human error and operational burden
- Short-lived credentials are inherently more secure

---
## Secret Rotation Strategies

1. **Manual rotation**: human-initiated, error-prone, infrequent
1. **Scheduled rotation**: automated on a fixed cadence (30, 60, 90 days)
1. **Event-driven rotation**: triggered by security events or personnel changes
1. **Dynamic / ephemeral secrets**: generated per-session, auto-expire
1. **Zero-standing privileges**: credentials exist only during active use

---
## Secrets Rotation Lifecycle

![secrets_rotation_lifecycle](svg/courses/devops/architectural-decisions-in-devops/10_configuration_and_secrets_management/secrets_rotation_lifecycle.svg)

---
## Dual-Secret Rotation Pattern

- Maintain two active versions of a secret simultaneously
- Rotate by introducing a new version while the old one is still valid
- Consumers gradually pick up the new version
- Revoke the old version only after all consumers have switched
- Prevents downtime during rotation windows

---
## Implementing Automated Rotation

```python
# AWS Secrets Manager rotation Lambda
import boto3, secrets, string

def lambda_handler(event, context):
    sm = boto3.client("secretsmanager")
    step = event["Step"]

    if step == "createSecret":
        new_pass = "".join(
            secrets.choice(string.ascii_letters)
            for _ in range(32)
        )
        sm.put_secret_value(
            SecretId=event["SecretId"],
            ClientRequestToken=event["Token"],
            SecretString=new_pass,
            VersionStages=["AWSPENDING"]
        )
    elif step == "finishSecret":
        sm.update_secret_version_stage(
            SecretId=event["SecretId"],
            VersionStage="AWSCURRENT",
            MoveToVersionId=event["Token"]
        )
```

---
## Secrets in CI/CD Pipelines

- CI/CD systems need secrets for deployments, testing, and artifact publishing
- Secrets must never appear in logs, artifacts, or build outputs
- Use platform-native secret storage, not hardcoded values

---
## Secrets in CI/CD Pipelines

![secrets_in_ci_cd_pipelines](svg/courses/devops/architectural-decisions-in-devops/10_configuration_and_secrets_management/secrets_in_ci_cd_pipelines.svg)

---
## GitHub Actions Secrets

```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to production
        env:
          DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
          API_KEY: ${{ secrets.API_KEY }}
        run: ./deploy.sh
```

- Secrets are masked in logs automatically
- Scoped to repository or organization level

---
## OIDC-Based Secret Access in CI/CD

- CI/CD pipelines authenticate to cloud providers via `OIDC` tokens
- No long-lived credentials stored in the CI platform
- GitHub Actions, GitLab CI, and CircleCI all support `OIDC` federation

```yaml
# GitHub Actions with AWS OIDC
permissions:
  id-token: write
steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123:role/deploy
      aws-region: us-east-1
  - run: |
      aws secretsmanager get-secret-value \
        --secret-id prod/db-password
```

---
## CI/CD Secrets Best Practices

1. Never echo or print secrets in build logs
1. Use short-lived, scoped credentials over long-lived keys
1. Prefer `OIDC` federation over static tokens
1. Limit secret access to specific branches or environments
1. Rotate CI/CD secrets on a regular schedule
1. Audit who added or modified pipeline secrets
1. Use secret scanning tools (`trufflehog`, `gitleaks`) in CI

---
## Configuration as Code

- All configuration is stored in version-controlled files
- Changes go through the same review process as application code
- Provides audit trail, rollback capability, and reproducibility
- Tools: `Terraform`, `Ansible`, `Helm` values, `Kustomize` overlays

```tree
repo/
  config/
    base.yaml
    environments/
      dev.yaml
      staging.yaml
      prod.yaml
```

---
## Benefits of Configuration as Code

1. Full change history via `git log`
1. Code review for config changes (pull request approval)
1. Automated validation in CI (linting, schema checks)
1. Easy rollback with `git revert`
1. Self-documenting -- the repo is the source of truth
1. Drift detection when compared against live state

---
## Configuration Services

- Centralized services that store and serve configuration
- Applications query the service at runtime for their config
- Examples: `Consul KV`, `etcd`, `AWS AppConfig`, `Spring Cloud Config`
- Provide features like versioning, namespaces, and change notifications

```bash
# Consul KV store
consul kv put myapp/db/host "prod-db.example.com"
consul kv put myapp/db/port "5432"

# Application reads at startup
consul kv get myapp/db/host
```

---
## Config as Code vs Config Services

![config_as_code_vs_config_services](svg/courses/devops/architectural-decisions-in-devops/10_configuration_and_secrets_management/config_as_code_vs_config_services.svg)

---
## Hybrid Approach: Best of Both Worlds

- Use config-as-code for baseline and environment-specific settings
- Use a config service for dynamic values and feature toggles
- Use a secrets manager for all sensitive values
- Application reads from multiple sources with a priority order

```misc
Priority (highest to lowest):
1. Secrets Manager (DB passwords, API keys)
2. Config Service (feature flags, rate limits)
3. Environment Variables (deployment context)
4. Config Files (defaults, static settings)
```

---
## The Twelve-Factor App: Config

- Factor III: "Store config in the environment"
- Config is everything that varies between deploys
- Strict separation of config from code
- Config should not be bundled inside the app
- Environment variables are the recommended mechanism
- Litmus test: could the codebase be open-sourced without leaking any credentials?

---
## Configuration Validation

- Validate configuration at startup to fail fast
- Use schema validation (`JSON Schema`, `Pydantic`, `Joi`)
- Check for required fields, valid ranges, and format constraints

```python
from pydantic import BaseSettings, Field

class AppConfig(BaseSettings):
    db_host: str
    db_port: int = Field(ge=1, le=65535)
    log_level: str = Field(
        pattern="^(debug|info|warn|error)$"
    )
    max_connections: int = Field(ge=1, le=1000)

    class Config:
        env_prefix = "APP_"
```

---
## Secret Scanning and Prevention

- Scan repositories for accidentally committed secrets
- Run scanners in CI to block PRs with exposed secrets
- Tools: `trufflehog`, `gitleaks`, `detect-secrets`, `git-secrets`

```bash
# Pre-commit hook with gitleaks
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
```

---
## Handling Secret Leaks

1. **Immediately revoke** the compromised credential
1. Generate a new secret and update all consumers
1. Audit access logs for unauthorized usage
1. Investigate how the leak occurred
1. Rewrite `git` history if the secret is in a commit
1. Post-mortem: improve processes to prevent recurrence

```bash
# Remove secret from git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch secrets.yaml" \
  --prune-empty --tag-name-filter cat -- --all
```

---
## `Helm` and `Kustomize` for Config Management

- `Helm` charts use `values.yaml` with per-environment overrides
- `Kustomize` uses patch-based overlays -- no templating language

```yaml
# Helm values-prod.yaml
replicaCount: 3
image:
  repository: myapp
  tag: v1.2.0
config:
  logLevel: warn
  dbHost: prod-db.internal
```

```bash
# Kustomize overlay
kubectl apply -k kustomize/overlays/prod/
```

---
## Config Drift Detection

- Compare live configuration against the declared source of truth
- Alert when drift is detected
- Tools: `Terraform` plan, `ArgoCD` sync status, custom scripts
- Automated remediation: reconcile drift back to desired state

```bash
# Terraform drift detection
terraform plan -detailed-exitcode
# Exit code 0: no changes
# Exit code 2: changes detected (drift)
```

---
## Summary: Configuration Best Practices

1. Separate config from code -- never hardcode values
1. Use baked-in config for stable, well-tested settings
1. Use runtime config for environment-specific and dynamic values
1. Store all secrets in a dedicated secrets manager
1. Automate secret rotation with short TTLs
1. Validate configuration at startup
1. Scan for leaked secrets in CI/CD
1. Treat configuration changes with the same rigor as code changes
