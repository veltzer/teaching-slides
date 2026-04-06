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

<svg width="700" height="120" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow1" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="10" y="35" width="110" height="50" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="65" y="65" text-anchor="middle" font-size="13" font-weight="bold">Dev</text>
  <line x1="120" y1="60" x2="165" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <rect x="170" y="35" width="110" height="50" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="225" y="65" text-anchor="middle" font-size="13" font-weight="bold">QA</text>
  <line x1="280" y1="60" x2="325" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <rect x="330" y="35" width="110" height="50" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="5"/>
  <text x="385" y="65" text-anchor="middle" font-size="13" font-weight="bold">Staging</text>
  <line x1="440" y1="60" x2="485" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <rect x="490" y="35" width="110" height="50" fill="#fce4ec" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="545" y="65" text-anchor="middle" font-size="13" font-weight="bold">Production</text>
</svg>

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

<svg width="700" height="280" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow2" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#555"/>
    </marker>
  </defs>
  <text x="350" y="25" text-anchor="middle" font-size="14" font-weight="bold" fill="#333">Enterprise Environment Topology</text>
  <rect x="10" y="45" width="100" height="40" fill="#bbdefb" stroke="#1565c0" stroke-width="2" rx="4"/>
  <text x="60" y="70" text-anchor="middle" font-size="11">Dev (Team A)</text>
  <rect x="10" y="105" width="100" height="40" fill="#bbdefb" stroke="#1565c0" stroke-width="2" rx="4"/>
  <text x="60" y="130" text-anchor="middle" font-size="11">Dev (Team B)</text>
  <line x1="110" y1="65" x2="175" y2="105" stroke="#555" stroke-width="1.5" marker-end="url(#arrow2)"/>
  <line x1="110" y1="125" x2="175" y2="105" stroke="#555" stroke-width="1.5" marker-end="url(#arrow2)"/>
  <rect x="180" y="85" width="100" height="40" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="4"/>
  <text x="230" y="110" text-anchor="middle" font-size="11">QA</text>
  <line x1="280" y1="105" x2="345" y2="105" stroke="#555" stroke-width="1.5" marker-end="url(#arrow2)"/>
  <rect x="350" y="85" width="100" height="40" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="4"/>
  <text x="400" y="110" text-anchor="middle" font-size="11">Staging</text>
  <line x1="450" y1="95" x2="515" y2="75" stroke="#555" stroke-width="1.5" marker-end="url(#arrow2)"/>
  <line x1="450" y1="115" x2="515" y2="135" stroke="#555" stroke-width="1.5" marker-end="url(#arrow2)"/>
  <rect x="520" y="55" width="100" height="40" fill="#ffe0b2" stroke="#e65100" stroke-width="2" rx="4"/>
  <text x="570" y="80" text-anchor="middle" font-size="11">UAT</text>
  <rect x="520" y="115" width="100" height="40" fill="#ffe0b2" stroke="#e65100" stroke-width="2" rx="4"/>
  <text x="570" y="140" text-anchor="middle" font-size="11">Perf Test</text>
  <line x1="620" y1="75" x2="640" y2="200" stroke="#555" stroke-width="1.5" marker-end="url(#arrow2)"/>
  <line x1="620" y1="135" x2="640" y2="200" stroke="#555" stroke-width="1.5" marker-end="url(#arrow2)"/>
  <rect x="580" y="195" width="120" height="45" fill="#ffcdd2" stroke="#c62828" stroke-width="2" rx="4"/>
  <text x="640" y="222" text-anchor="middle" font-size="12" font-weight="bold">Production</text>
</svg>

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

<svg width="700" height="160" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow3" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="10" y="50" width="110" height="50" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="65" y="70" text-anchor="middle" font-size="11" font-weight="bold">PR Created</text>
  <text x="65" y="85" text-anchor="middle" font-size="9" fill="#555">Trigger</text>
  <line x1="120" y1="75" x2="155" y2="75" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <rect x="160" y="50" width="110" height="50" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="215" y="70" text-anchor="middle" font-size="11" font-weight="bold">Provision</text>
  <text x="215" y="85" text-anchor="middle" font-size="9" fill="#555">Infra + App</text>
  <line x1="270" y1="75" x2="305" y2="75" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <rect x="310" y="50" width="110" height="50" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="5"/>
  <text x="365" y="70" text-anchor="middle" font-size="11" font-weight="bold">Active</text>
  <text x="365" y="85" text-anchor="middle" font-size="9" fill="#555">Test + Review</text>
  <line x1="420" y1="75" x2="455" y2="75" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <rect x="460" y="50" width="110" height="50" fill="#fce4ec" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="515" y="70" text-anchor="middle" font-size="11" font-weight="bold">PR Merged</text>
  <text x="515" y="85" text-anchor="middle" font-size="9" fill="#555">Trigger</text>
  <line x1="570" y1="75" x2="605" y2="75" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <rect x="610" y="50" width="80" height="50" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2" rx="5"/>
  <text x="650" y="70" text-anchor="middle" font-size="11" font-weight="bold">Destroy</text>
  <text x="650" y="85" text-anchor="middle" font-size="9" fill="#555">Cleanup</text>
</svg>

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

<svg width="700" height="250" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow4" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="20" width="120" height="45" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="80" y="47" text-anchor="middle" font-size="12" font-weight="bold">GitHub PR</text>
  <line x1="140" y1="42" x2="195" y2="42" stroke="#333" stroke-width="2" marker-end="url(#arrow4)"/>
  <rect x="200" y="20" width="120" height="45" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="5"/>
  <text x="260" y="47" text-anchor="middle" font-size="12" font-weight="bold">CI Pipeline</text>
  <line x1="320" y1="42" x2="375" y2="42" stroke="#333" stroke-width="2" marker-end="url(#arrow4)"/>
  <rect x="380" y="20" width="140" height="45" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="450" y="47" text-anchor="middle" font-size="12" font-weight="bold">Provision Env</text>
  <line x1="450" y1="65" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrow4)"/>
  <rect x="310" y="105" width="280" height="120" fill="#f5f5f5" stroke="#999" stroke-width="1" rx="5" stroke-dasharray="5,3"/>
  <text x="450" y="125" text-anchor="middle" font-size="11" fill="#555">Ephemeral Namespace</text>
  <rect x="325" y="135" width="80" height="35" fill="#bbdefb" stroke="#1565c0" stroke-width="1.5" rx="3"/>
  <text x="365" y="157" text-anchor="middle" font-size="10">App Pod</text>
  <rect x="420" y="135" width="80" height="35" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1.5" rx="3"/>
  <text x="460" y="157" text-anchor="middle" font-size="10">DB Pod</text>
  <rect x="515" y="135" width="60" height="35" fill="#ffe0b2" stroke="#e65100" stroke-width="1.5" rx="3"/>
  <text x="545" y="157" text-anchor="middle" font-size="10">Cache</text>
  <rect x="325" y="180" width="250" height="30" fill="#e1bee7" stroke="#7b1fa2" stroke-width="1.5" rx="3"/>
  <text x="450" y="200" text-anchor="middle" font-size="10">Ingress: pr-42.preview.example.com</text>
  <line x1="260" y1="65" x2="80" y2="100" stroke="#2e7d32" stroke-width="1.5" marker-end="url(#arrow4)"/>
  <rect x="20" y="105" width="120" height="35" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1.5" rx="3"/>
  <text x="80" y="127" text-anchor="middle" font-size="10">Post URL to PR</text>
</svg>

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

<svg width="700" height="220" xmlns="http://www.w3.org/2000/svg">
  <text x="350" y="20" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Configuration Drift Over Time</text>
  <line x1="60" y1="190" x2="660" y2="190" stroke="#333" stroke-width="2"/>
  <line x1="60" y1="190" x2="60" y2="30" stroke="#333" stroke-width="2"/>
  <text x="360" y="215" text-anchor="middle" font-size="11" fill="#555">Time</text>
  <text x="30" y="110" text-anchor="middle" font-size="11" fill="#555" transform="rotate(-90 30 110)">Divergence</text>
  <polyline points="60,180 160,175 260,160 360,130 460,100 560,60 660,35" fill="none" stroke="#c62828" stroke-width="2.5"/>
  <text x="665" y="30" font-size="10" fill="#c62828">Dev</text>
  <polyline points="60,180 160,178 260,170 360,155 460,140 560,125 660,110" fill="none" stroke="#e65100" stroke-width="2.5"/>
  <text x="665" y="105" font-size="10" fill="#e65100">QA</text>
  <polyline points="60,180 160,180 260,179 360,177 460,175 560,173 660,170" fill="none" stroke="#2e7d32" stroke-width="2.5"/>
  <text x="665" y="165" font-size="10" fill="#2e7d32">Staging</text>
  <polyline points="60,180 160,180 260,180 360,180 460,180 560,180 660,180" fill="none" stroke="#1565c0" stroke-width="2.5" stroke-dasharray="5,3"/>
  <text x="665" y="182" font-size="10" fill="#1565c0">Prod (baseline)</text>
</svg>

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

<svg width="700" height="150" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow5" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="10" y="45" width="120" height="50" fill="#ffcdd2" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="70" y="65" text-anchor="middle" font-size="11" font-weight="bold">Prod DB</text>
  <text x="70" y="80" text-anchor="middle" font-size="9" fill="#555">Real PII</text>
  <line x1="130" y1="70" x2="175" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrow5)"/>
  <rect x="180" y="45" width="120" height="50" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="5"/>
  <text x="240" y="65" text-anchor="middle" font-size="11" font-weight="bold">Export</text>
  <text x="240" y="80" text-anchor="middle" font-size="9" fill="#555">Snapshot</text>
  <line x1="300" y1="70" x2="345" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrow5)"/>
  <rect x="350" y="45" width="120" height="50" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="410" y="65" text-anchor="middle" font-size="11" font-weight="bold">Anonymize</text>
  <text x="410" y="80" text-anchor="middle" font-size="9" fill="#555">Mask/Hash PII</text>
  <line x1="470" y1="70" x2="515" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrow5)"/>
  <rect x="520" y="45" width="120" height="50" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="580" y="65" text-anchor="middle" font-size="11" font-weight="bold">Non-prod DB</text>
  <text x="580" y="80" text-anchor="middle" font-size="9" fill="#555">Safe data</text>
</svg>

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

<svg width="700" height="220" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow6" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="250" y="10" width="200" height="50" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="5"/>
  <text x="350" y="40" text-anchor="middle" font-size="13" font-weight="bold">Secrets Manager</text>
  <line x1="290" y1="60" x2="120" y2="100" stroke="#555" stroke-width="1.5" marker-end="url(#arrow6)"/>
  <line x1="350" y1="60" x2="350" y2="100" stroke="#555" stroke-width="1.5" marker-end="url(#arrow6)"/>
  <line x1="410" y1="60" x2="580" y2="100" stroke="#555" stroke-width="1.5" marker-end="url(#arrow6)"/>
  <rect x="50" y="105" width="140" height="40" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="4"/>
  <text x="120" y="130" text-anchor="middle" font-size="11">secret/dev/*</text>
  <rect x="280" y="105" width="140" height="40" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="4"/>
  <text x="350" y="130" text-anchor="middle" font-size="11">secret/staging/*</text>
  <rect x="510" y="105" width="140" height="40" fill="#ffcdd2" stroke="#c62828" stroke-width="2" rx="4"/>
  <text x="580" y="130" text-anchor="middle" font-size="11">secret/prod/*</text>
  <line x1="120" y1="145" x2="120" y2="175" stroke="#555" stroke-width="1.5" marker-end="url(#arrow6)"/>
  <line x1="350" y1="145" x2="350" y2="175" stroke="#555" stroke-width="1.5" marker-end="url(#arrow6)"/>
  <line x1="580" y1="145" x2="580" y2="175" stroke="#555" stroke-width="1.5" marker-end="url(#arrow6)"/>
  <rect x="50" y="180" width="140" height="30" fill="#bbdefb" stroke="#1565c0" stroke-width="1.5" rx="3"/>
  <text x="120" y="200" text-anchor="middle" font-size="10">Dev Workloads</text>
  <rect x="280" y="180" width="140" height="30" fill="#ffe0b2" stroke="#e65100" stroke-width="1.5" rx="3"/>
  <text x="350" y="200" text-anchor="middle" font-size="10">Staging Workloads</text>
  <rect x="510" y="180" width="140" height="30" fill="#ffcdd2" stroke="#c62828" stroke-width="1.5" rx="3"/>
  <text x="580" y="200" text-anchor="middle" font-size="10">Prod Workloads</text>
</svg>

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

<svg width="700" height="180" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow7" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="350" y="20" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Artifact Promotion (Not Code Promotion)</text>
  <rect x="30" y="40" width="130" height="55" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="95" y="62" text-anchor="middle" font-size="11" font-weight="bold">Build</text>
  <text x="95" y="80" text-anchor="middle" font-size="9" fill="#555">image:abc123</text>
  <line x1="160" y1="67" x2="205" y2="67" stroke="#333" stroke-width="2" marker-end="url(#arrow7)"/>
  <rect x="210" y="40" width="130" height="55" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="275" y="62" text-anchor="middle" font-size="11" font-weight="bold">Dev Tests</text>
  <text x="275" y="80" text-anchor="middle" font-size="9" fill="#2e7d32">PASS</text>
  <line x1="340" y1="67" x2="385" y2="67" stroke="#333" stroke-width="2" marker-end="url(#arrow7)"/>
  <rect x="390" y="40" width="130" height="55" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="5"/>
  <text x="455" y="62" text-anchor="middle" font-size="11" font-weight="bold">Staging Tests</text>
  <text x="455" y="80" text-anchor="middle" font-size="9" fill="#2e7d32">PASS</text>
  <line x1="520" y1="67" x2="565" y2="67" stroke="#333" stroke-width="2" marker-end="url(#arrow7)"/>
  <rect x="570" y="40" width="110" height="55" fill="#ffcdd2" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="625" y="62" text-anchor="middle" font-size="11" font-weight="bold">Production</text>
  <text x="625" y="80" text-anchor="middle" font-size="9" fill="#555">Deploy</text>
  <text x="350" y="130" text-anchor="middle" font-size="11" fill="#555">Same artifact promoted through each stage</text>
  <text x="350" y="150" text-anchor="middle" font-size="11" fill="#555">Only configuration differs between environments</text>
</svg>

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
