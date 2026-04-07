# Environment Strategy
## Architectural Decisions in DevOps
---
## Table of Contents

1. How Many Environments and Why
1. Production-like vs Lightweight Environments
1. Cost Implications of Environment Proliferation
1. Ephemeral vs Persistent Environments
1. Preview Environments for Pull Requests
1. On-demand Staging Environments
1. Cleanup and Lifecycle Management
1. Environment Parity and Configuration Drift
1. Data Management in Non-production Environments
---
## Why Environments Matter

- Environments are the backbone of every software delivery pipeline
- Wrong environment strategy leads to:
    - Bugs escaping to production
    - Slow developer feedback loops
    - Wasted infrastructure costs
    - Configuration drift and "works on my machine" problems
- Getting it right is a foundational architectural decision
---
## The Classic Environment Pipeline

![the_classic_environment_pipeline](/svg/courses/devops/architectural-decisions-in-devops/08_environment_strategy/the_classic_environment_pipeline.svg)

- Code flows through progressively more production-like environments
- Each stage acts as a quality gate
---
## How Many Environments?

- There is no universal answer, but common patterns exist
- Factors that determine the number:
    - Team size and structure
    - Deployment frequency
    - Regulatory requirements
    - Budget constraints
    - Application complexity
- Too few environments means risk; too many means cost and complexity
---
## Minimal Setup: Two Environments

- **Development** and **Production** only
- Suitable for:
    - Small teams (1-3 developers)
    - Early-stage startups
    - Internal tools with low risk
- Risks:
    - No staging means untested changes hit production
    - Hard to reproduce production bugs safely
---
## Standard and Enterprise Setups

- **Three environments**: Dev, Staging, Production
    - Staging mirrors production configuration
    - Most common starting point for growing teams
- **Four or more**: Dev, QA, Staging, UAT, Production
    - `QA` for automated and manual testing
    - `UAT` for business stakeholder sign-off
    - `Performance` for load and stress testing
    - Common in regulated industries (finance, healthcare)
---
## Environment Topology Diagram

![environment_topology_diagram](/svg/courses/devops/architectural-decisions-in-devops/08_environment_strategy/environment_topology_diagram.svg)

---
## Production-like vs Lightweight Environments

- **Production-like**: mirrors production in architecture, config, and scale
    - Same OS, runtime versions, network topology
    - Expensive but catches real issues
- **Lightweight**: simplified for speed and cost savings
    - Shared databases, smaller instance sizes
    - Suitable for feature branches and sandboxes
- Rule of thumb: the closer to production, the more it should resemble production
---
## Cost Implications of Environment Proliferation

- Every persistent environment has ongoing costs:
    - Compute (VMs, containers, serverless invocations)
    - Storage (databases, object stores, caches)
    - Networking (load balancers, DNS, VPN)
    - Licensing (third-party software, SaaS seats)
    - Human cost (maintenance, monitoring, troubleshooting)
---
## Cost Growth Example

| Environments | Monthly Compute | Storage | Networking | Total |
|-------------|----------------|---------|------------|-------|
| 3 (Dev/Stg/Prod) | $3,000 | $500 | $200 | $3,700 |
| 5 (+QA, UAT) | $5,000 | $900 | $350 | $6,250 |
| 8 (+Perf, DR, Demo) | $8,000 | $1,500 | $600 | $10,100 |
| 15 (per-team envs) | $15,000 | $3,000 | $1,200 | $19,200 |

- Costs scale roughly linearly with number of persistent environments
---
## Strategies to Control Environment Costs

1. Use ephemeral environments instead of persistent ones
1. Right-size non-production environments (smaller instances)
1. Schedule environments to shut down outside business hours
1. Share lower environments across teams when possible
1. Use spot/preemptible instances for non-critical environments
1. Set budgets and alerts per environment
---
## Scheduling Non-production Environments

```yaml
# Kubernetes CronJob to scale down staging at night
apiVersion: batch/v1
kind: CronJob
metadata:
  name: scale-down-staging
spec:
  schedule: "0 20 * * 1-5"  # 8 PM weekdays
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: scaler
            image: bitnami/kubectl
            command:
            - kubectl
            - scale
            - deployment
            - --all
            - --replicas=0
            - -n
            - staging
```

---
## Ephemeral vs Persistent Environments

- **Persistent**: always running, manually maintained
    - Examples: `dev`, `staging`, `production`
    - Pros: always available, known state
    - Cons: expensive, prone to drift, manual upkeep
- **Ephemeral**: created on demand, destroyed after use
    - Examples: PR preview environments, test environments
    - Pros: cost-efficient, clean state every time
    - Cons: provisioning latency, setup complexity
---
## Ephemeral Environment Lifecycle

![ephemeral_environment_lifecycle](/svg/courses/devops/architectural-decisions-in-devops/08_environment_strategy/ephemeral_environment_lifecycle.svg)

- Entire lifecycle is automated and tied to the PR workflow
---
## Preview Environments for Pull Requests

- A dedicated environment spun up for every PR
- Allows reviewers to:
    - Click a link and see the running application
    - Test feature behavior without checking out the branch
    - Validate UI changes visually
- Popular tools: `Vercel`, `Netlify`, `Argo CD`, `Crossplane`, `Terraform`
---
## Preview Environment Architecture

![preview_environment_architecture](/svg/courses/devops/architectural-decisions-in-devops/08_environment_strategy/preview_environment_architecture.svg)

---
## Setting Up PR Preview Environments

```yaml
# GitHub Actions workflow snippet
on:
  pull_request:
    types: [opened, synchronize]
jobs:
  preview:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Create preview namespace
      run: |
        kubectl create ns pr-${{ github.event.number }}
    - name: Deploy preview
      run: |
        helm install preview ./chart \
          -n pr-${{ github.event.number }} \
          --set image.tag=${{ github.sha }} \
          --set ingress.host=pr-${{ github.event.number }}.preview.example.com
    - name: Post URL to PR
      uses: actions/github-script@v7
      with:
        script: |
          github.rest.issues.createComment({
            owner: context.repo.owner,
            repo: context.repo.repo,
            issue_number: context.issue.number,
            body: 'Preview: https://pr-${{ github.event.number }}.preview.example.com'
          })
```

---
## On-demand Staging Environments

- A full staging environment created when needed
- Use cases:
    - Release candidate validation
    - Large feature integration testing
    - Customer demo environments
    - Load testing sessions
- Triggered manually or by specific pipeline events
- Destroyed after a defined TTL or manual teardown
---
## On-demand Environment with `Terraform`

```hcl
variable "env_name" {
  description = "Unique environment identifier"
}

variable "ttl_hours" {
  default = 24
}

resource "aws_ecs_cluster" "staging" {
  name = "staging-${var.env_name}"
  tags = {
    Environment = "staging"
    TTL         = var.ttl_hours
    CreatedAt   = timestamp()
  }
}

resource "aws_ecs_service" "app" {
  name            = "app-${var.env_name}"
  cluster         = aws_ecs_cluster.staging.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 2
}
```

---
## Cleanup and Lifecycle Management

- Ephemeral environments must be cleaned up or they become persistent costs
- Common cleanup triggers:
    - PR merged or closed
    - TTL (time-to-live) expiration
    - Manual teardown via CLI or dashboard
    - Scheduled garbage collection jobs
- Always tag resources with metadata for tracking
---
## Tagging Strategy for Lifecycle Management

```yaml
# Tags every ephemeral resource should carry
tags:
  environment: ephemeral
  created-by: ci-pipeline
  pr-number: "42"
  branch: feature/user-auth
  created-at: "2026-02-16T10:30:00Z"
  ttl: "24h"
  owner: team-platform
  cost-center: engineering
```

- Tags enable automated cleanup scripts to find and destroy stale resources
---
## Automated Cleanup Script

```bash
#!/bin/bash
# Find and delete environments past their TTL
CURRENT_TIME=$(date +%s)

for ns in $(kubectl get ns -l environment=ephemeral \
  -o jsonpath='{.items[*].metadata.name}'); do

  CREATED=$(kubectl get ns "$ns" \
    -o jsonpath='{.metadata.annotations.created-at}')
  TTL=$(kubectl get ns "$ns" \
    -o jsonpath='{.metadata.annotations.ttl-hours}')

  CREATED_EPOCH=$(date -d "$CREATED" +%s)
  EXPIRY=$((CREATED_EPOCH + TTL * 3600))

  if [ "$CURRENT_TIME" -gt "$EXPIRY" ]; then
    echo "Deleting expired namespace: $ns"
    kubectl delete ns "$ns"
  fi
done
```

---
## Cleanup on PR Close

```yaml
# GitHub Actions cleanup workflow
on:
  pull_request:
    types: [closed]
jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
    - name: Delete preview namespace
      run: |
        kubectl delete ns pr-${{ github.event.number }} \
          --ignore-not-found
    - name: Remove DNS record
      run: |
        aws route53 change-resource-record-sets \
          --hosted-zone-id $ZONE_ID \
          --change-batch '{
            "Changes": [{
              "Action": "DELETE",
              "ResourceRecordSet": {
                "Name": "pr-${{ github.event.number }}.preview.example.com",
                "Type": "CNAME",
                "TTL": 300,
                "ResourceRecords": [{"Value": "lb.example.com"}]
              }
            }]
          }'
```

---
## Environment Parity: The Goal

- Environment parity means all environments behave the same way
- **Dev/prod parity** is one of the Twelve-Factor App principles
- Dimensions of parity:
    - Infrastructure (OS, runtime, networking)
    - Configuration (env vars, feature flags)
    - Data (schema, volume, realistic content)
    - Dependencies (service versions, API contracts)
---
## What Is Configuration Drift?

- Configuration drift occurs when environments diverge from their intended state
- Common causes:
    - Manual changes ("just this once" SSH fixes)
    - Different provisioning scripts per environment
    - Untracked secrets or environment variables
    - Skipped upgrades in non-production
    - Different cloud regions or instance types
---
## Configuration Drift Visualization

![configuration_drift_visualization](/svg/courses/devops/architectural-decisions-in-devops/08_environment_strategy/configuration_drift_visualization.svg)

- Without active management, every environment drifts away from production
---
## Consequences of Configuration Drift

- "It works in staging but breaks in production"
- Security patches applied inconsistently
- Debugging becomes harder when environments differ
- Compliance audits fail due to inconsistent configurations
- Rollbacks behave differently than expected
- Team confidence in the pipeline erodes
---
## Preventing Drift: Infrastructure as Code

- Define all infrastructure in version-controlled code
- Use the same `Terraform`/`Pulumi`/`CloudFormation` modules across environments
- Parameterize environment-specific values, not structure

```hcl
# Same module, different parameters
module "environment" {
  source        = "./modules/app-stack"
  env_name      = var.env_name       # "dev", "staging", "prod"
  instance_type = var.instance_type  # "t3.small" vs "m5.xlarge"
  replicas      = var.replicas       # 1 vs 3
  domain        = var.domain         # "dev.example.com"
}
```

---
## Preventing Drift: Continuous Reconciliation

- Actively detect and correct drift
- Tools and approaches:
    - `Terraform` plan in CI to detect infrastructure drift
    - `Argo CD` or `Flux` for `GitOps`-based reconciliation
    - `AWS Config Rules` for compliance monitoring
    - `Chef InSpec` or `Open Policy Agent` for policy enforcement
- Alert on drift; auto-remediate when safe
---
## Drift Detection Pipeline

```yaml
name: Detect Infrastructure Drift
on:
  schedule:
    - cron: '0 6 * * *'  # Daily at 6 AM
jobs:
  drift-check:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        env: [dev, staging, production]
    steps:
    - uses: actions/checkout@v4
    - name: Terraform plan
      run: |
        cd infra/environments/${{ matrix.env }}
        terraform init
        terraform plan -detailed-exitcode
      continue-on-error: true
    - name: Alert on drift
      if: failure()
      run: |
        curl -X POST "$SLACK_WEBHOOK" \
          -d '{"text":"Drift detected in ${{ matrix.env }}"}'
```

---
## Ensuring Consistency: Container Images

- Use the exact same container image across all environments
- Build once, deploy everywhere
- Never rebuild for different environments

```bash
# Build and tag once
docker build -t myapp:abc123 .
docker push registry.example.com/myapp:abc123

# Deploy the same image to every environment
# Only configuration changes between environments
helm upgrade app ./chart \
  --set image.tag=abc123 \
  --set env=staging
```

---
## Ensuring Consistency: Dependency Pinning

- Pin every dependency to exact versions
- Applies to:
    - Application dependencies (`package-lock.json`, `Pipfile.lock`, `go.sum`)
    - Base container images (`FROM node:20.11.1-alpine3.19`)
    - Infrastructure provider versions
    - CI/CD tool versions

```dockerfile
# Bad: floating tag
FROM python:3.12
# Good: pinned digest
FROM python:3.12.2-slim@sha256:abcdef123456
```

---
## Data Management in Non-production Environments

- Non-production environments need realistic data to be useful
- Challenges:
    - Production data contains PII and sensitive information
    - Copying full datasets is expensive and slow
    - Schema changes must propagate consistently
    - Test data must cover edge cases
---
## Data Strategies for Non-production

| Strategy | Pros | Cons |
|----------|------|------|
| Production clone | Most realistic | PII risk, expensive |
| Anonymized copy | Realistic + safe | Complex to maintain |
| Synthetic data | Safe, customizable | May miss edge cases |
| Subset sampling | Balanced | May miss data patterns |
| Seed scripts | Repeatable, fast | Requires maintenance |

- Most teams use a combination of these approaches
---
## Data Anonymization Pipeline

![data_anonymization_pipeline](/svg/courses/devops/architectural-decisions-in-devops/08_environment_strategy/data_anonymization_pipeline.svg)

- Automate the pipeline so non-prod data stays fresh and safe
---
## Data Anonymization Techniques

- **Masking**: replace sensitive values with realistic fakes
    - Email: `john@example.com` becomes `user_7f3a@masked.test`
    - Phone: `555-123-4567` becomes `555-000-0000`
- **Hashing**: one-way transformation preserving uniqueness
- **Tokenization**: replace with tokens, store mapping securely
- **Subsetting**: take a representative sample of records
- **Synthetic generation**: create entirely fake but realistic data
---
## Database Schema Consistency

- Schema must match across all environments
- Use migration tools to enforce this:
    - `Flyway`, `Liquibase` for relational databases
    - `mongosh` scripts for `MongoDB`
    - `Alembic` for `SQLAlchemy`-based apps
- Run migrations as part of the deployment pipeline
- Never apply schema changes manually
---
## Environment-specific Secrets Management

- Secrets must differ per environment but be managed consistently
- Best practices:
    - Use a secrets manager (`Vault`, `AWS Secrets Manager`, `GCP Secret Manager`)
    - Path-based organization: `secret/dev/db-password`, `secret/prod/db-password`
    - Rotate secrets automatically
    - Never store secrets in environment definition files
---
## Secrets Architecture

![secrets_architecture](/svg/courses/devops/architectural-decisions-in-devops/08_environment_strategy/secrets_architecture.svg)

---
## Feature Flags Across Environments

- Feature flags let you decouple deployment from release
- Environment-aware flag configuration:
    - Enable experimental features in `dev` only
    - Gradually roll out in `staging` before `production`
    - Kill switches for instant rollback without redeployment
- Tools: `LaunchDarkly`, `Unleash`, `Flagsmith`, `ConfigCat`
---
## Feature Flag Configuration Example

```json
{
  "flags": {
    "new-checkout-flow": {
      "dev": { "enabled": true, "rollout": 100 },
      "staging": { "enabled": true, "rollout": 50 },
      "production": { "enabled": false, "rollout": 0 }
    },
    "dark-mode": {
      "dev": { "enabled": true, "rollout": 100 },
      "staging": { "enabled": true, "rollout": 100 },
      "production": { "enabled": true, "rollout": 25 }
    }
  }
}
```

- Same codebase, different behavior per environment
---
## Environment Promotion Strategy

![environment_promotion_strategy](/svg/courses/devops/architectural-decisions-in-devops/08_environment_strategy/environment_promotion_strategy.svg)

---
## `GitOps` for Environment Management

- Declare desired state of each environment in `Git`
- Repository structure:

```tree
environments/
  base/                  # Shared resources
    deployment.yaml
    service.yaml
  overlays/
    dev/
      kustomization.yaml
    staging/
      kustomization.yaml
    production/
      kustomization.yaml
```

- Changes to any environment go through code review
---
## Environment Strategy Decision Matrix

| Factor | Fewer Environments | More Environments |
|--------|-------------------|-------------------|
| Team size | Small (< 10) | Large (> 50) |
| Deploy frequency | Weekly or less | Multiple times daily |
| Regulation | Low | High (SOC2, HIPAA) |
| Budget | Tight | Flexible |
| Architecture | Monolith | Microservices |
| Risk tolerance | Higher | Lower |

---
## Anti-patterns to Avoid

1. Long-lived "shared dev" environments that nobody owns
1. Manual SSH changes to fix environment issues
1. Different provisioning tools per environment
1. Skipping environments to "ship faster"
1. Copying production data without anonymization
1. No cleanup policy for ephemeral environments
1. Treating environment configuration as an afterthought
---
## Best Practices Summary

1. Start with the minimum viable number of environments
1. Use `IaC` to ensure environments are reproducible
1. Prefer ephemeral over persistent for non-production
1. Build container images once, deploy everywhere
1. Automate cleanup with TTLs and garbage collection
1. Detect and alert on configuration drift daily
1. Anonymize production data before copying to lower environments
1. Isolate environments at the network level
---
## Choosing Your Environment Strategy

- Step 1: Assess your team size, deployment frequency, and risk profile
- Step 2: Define the minimum set of persistent environments
- Step 3: Implement ephemeral environments for developer workflows
- Step 4: Establish `IaC` and `GitOps` as the configuration standard
- Step 5: Set up drift detection and automated cleanup
- Step 6: Continuously review costs and optimize
