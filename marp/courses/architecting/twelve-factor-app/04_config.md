---
tags:
  - concepts:architecture
  - concepts:best-practices
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:devops

---
# Factor III: Config

---
## Config in Environment

![config_in_env](svg/courses/architecting/twelve-factor-app/04_config/config_in_env.svg)

---
## Config Practices

![config_practices](svg/courses/architecting/twelve-factor-app/04_config/config_practices.svg)

---
## The Rule

- Strict separation of config from code
- Store config in environment variables
- The same code runs in every environment with different config

---
## What Config Includes

- Database URLs and credentials
- API keys for third-party services
- Per-environment values (dev/staging/prod)
- Hostnames, ports, feature flags
- Anything that varies between deploys

---
## What Config Does Not Include

- Internal application config that doesn't vary by deploy
- Constants compiled into the app
- Routing tables, request validators, business logic
- "Config" by twelve-factor means deploy-specific values only

---
## Why Environment Variables

- Language-agnostic — every runtime can read them
- Granular — set per-deploy without touching files
- Standard — widely supported by container orchestrators
- Easy to inject from secret managers
- Easy to override locally for testing

---
## Anti-Patterns

- Config files committed to the repo
- Config in code: `if env == "prod": ... else: ...`
- Hardcoded URLs and credentials
- Config files generated at build time and baked into the image
- "Just edit `prod.config` on the server"

---
## The Litmus Test

- Could the codebase be open-sourced without leaking credentials?
- If yes, config separation is correct
- If no, secrets are mixed in

---
## Reading Config in Code

```python
import os

DATABASE_URL = os.environ["DATABASE_URL"]
LOG_LEVEL    = os.environ.get("LOG_LEVEL", "INFO")
FEATURE_X    = os.environ.get("FEATURE_X", "false") == "true"
```

- Required values use `os.environ["..."]` — fail fast if missing
- Optional values have explicit defaults
- Type coercion is explicit, not magic

---
## Validation at Startup

- Read all config at startup
- Validate each value (URL is well-formed, port is a number, etc.)
- Fail loudly with a clear message if anything is wrong
- "App started but feature broken because env var was misspelled" is the failure mode to avoid

---
## Secrets vs Plain Config

- Secrets are sensitive: API keys, passwords, certificates
- Plain config is non-sensitive: log levels, feature flags
- Both go through environment variables in twelve-factor
- The injection mechanism differs (secret manager vs. plain config map)

---
## Where to Put Configuration

![config_storage_options](svg/courses/architecting/twelve-factor-app/04_config/config_storage_options.svg)

---
## Secrets Management

- Secrets stored in a vault (AWS Secrets Manager, HashiCorp Vault, GCP Secret Manager)
- Injected as env vars at process start
- Rotated without code changes
- Audited: who read which secret when

---
## Kubernetes Config Patterns

- `ConfigMap` for plain config
- `Secret` for sensitive config
- Both injected as env vars or files
- The app reads env vars uniformly; the deployment manifest knows what's secret

---
## Anti-Pattern: Bundled Config Per Environment

- `config/prod.yaml`, `config/staging.yaml` in the repo
- Selected at startup by `APP_ENV=prod`
- Looks tidy; violates factor III
- New environments require code changes; secrets still leak

---
## Why That Anti-Pattern Persists

- Editor support for structured files
- Type safety at parse time
- Easier to read than env vars in some languages
- The right answer: parse env vars into a typed config object at startup

---
## A Reasonable Compromise

- Environment variables drive config
- A small startup function reads them and produces a typed Config object
- The Config object is passed around; nothing else reads env vars
- Single source of truth in code; clean factor-III compliance at the boundary

---
## Summary

- Config = anything that varies between deploys
- Store in environment variables
- Validate at startup
- Secrets via vaults, injected as env vars
- The same image deploys to dev, staging, prod with different config
