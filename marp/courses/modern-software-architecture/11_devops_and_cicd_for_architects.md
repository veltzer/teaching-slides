# DevOps and CI/CD for Architects

<!-- Add Mermaid.js support -->
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({ startOnLoad: true });
</script>

---
## What Is DevOps?

- A set of practices that combines software development and IT operations
- Aims to shorten the development lifecycle and deliver high-quality software
- Emphasizes collaboration, automation, and continuous improvement
- Not a tool or a team, but a culture and set of principles

---
## DevOps Principles

- Automate everything that can be automated
- Measure and monitor continuously
- Share responsibility between development and operations
- Fail fast and learn from failures
- Deliver small, frequent changes rather than large, infrequent releases

---
## The DevOps Lifecycle

<div class="mermaid">
graph LR
    PLAN[Plan] --> CODE[Code]
    CODE --> BUILD[Build]
    BUILD --> TEST[Test]
    TEST --> RELEASE[Release]
    RELEASE --> DEPLOY[Deploy]
    DEPLOY --> OPERATE[Operate]
    OPERATE --> MONITOR[Monitor]
    MONITOR --> PLAN
</div>

---
## Why Architects Care About DevOps

- Architecture decisions directly impact deployment frequency and reliability
- A good architecture enables fast, safe, independent deployments
- A bad architecture creates deployment bottlenecks and risk
- Architects must design systems that are easy to build, test, and deploy

---
## Continuous Integration (CI)

- Developers merge code changes to a shared repository frequently
- Each merge triggers an automated build and test pipeline
- Catches integration issues early when they are cheap to fix
- Provides fast feedback to developers on code quality

---
## CI Pipeline

<div class="mermaid">
graph LR
    PUSH[Code Push] --> LINT[Lint / Format]
    LINT --> BUILD[Build]
    BUILD --> UNIT[Unit Tests]
    UNIT --> INT[Integration Tests]
    INT --> SCAN[Security Scan]
    SCAN --> ART[Publish Artifact]
</div>

---
## CI Best Practices

- Keep the build fast (under 10 minutes)
- Run tests on every commit, not just on merge
- Fix broken builds immediately as the top priority
- Use feature branches with short lifespans
- Automate code quality checks (linting, formatting, static analysis)

---
## Continuous Delivery (CD)

- Every code change that passes the pipeline is ready for production deployment
- Deployment to production requires a manual approval step
- Ensures the software is always in a releasable state
- Reduces risk by making releases smaller and more frequent

---
## Continuous Deployment

- Every change that passes the pipeline is automatically deployed to production
- No manual approval step; full automation from commit to production
- Requires high confidence in the test suite and monitoring
- Enables multiple deployments per day

---
## CD vs Continuous Deployment

<div class="mermaid">
graph LR
    subgraph Continuous Delivery
        A1[Build] --> A2[Test] --> A3[Stage] --> A4[Manual Approval] --> A5[Production]
    end
    subgraph Continuous Deployment
        B1[Build] --> B2[Test] --> B3[Stage] --> B4[Auto Deploy to Production]
    end
</div>

---
## Infrastructure as Code (IaC)

- Managing and provisioning infrastructure through machine-readable definition files
- Infrastructure is version-controlled alongside application code
- Changes are reviewed, tested, and deployed through the same pipeline
- Eliminates manual configuration and reduces drift between environments

---
## IaC Benefits

- Reproducibility: create identical environments on demand
- Version control: track every infrastructure change
- Automation: provision and update infrastructure programmatically
- Documentation: the code itself documents the infrastructure
- Collaboration: team members review infrastructure changes via pull requests

---
## IaC Tool Categories

<div class="mermaid">
graph TD
    IAC[Infrastructure as Code]
    IAC --> PROV[Provisioning]
    IAC --> CONFIG[Configuration]
    IAC --> ORCH[Orchestration]
    PROV --> TF[Terraform / OpenTofu]
    PROV --> PULUMI[Pulumi]
    PROV --> CFN[CloudFormation]
    CONFIG --> ANS[Ansible]
    CONFIG --> CHEF[Chef / Puppet]
    ORCH --> K8S[Kubernetes Manifests]
    ORCH --> HELM[Helm Charts]
</div>

---
## Terraform Example

```hcl
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.medium"
  tags = {
    Name        = "web-server"
    Environment = "production"
  }
}

resource "aws_security_group" "web_sg" {
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

---
## IaC Best Practices

- Store all infrastructure code in version control
- Use modules to avoid duplication
- Separate state per environment (dev, staging, production)
- Use remote state backends with locking (`S3` + `DynamoDB`)
- Run `terraform plan` in CI to preview changes before applying
- Never make manual changes to infrastructure managed by IaC

---
## GitOps

- An operational framework that uses `Git` as the single source of truth
- Infrastructure and application state are declared in Git
- Automated agents reconcile the actual state with the desired state
- Changes are made through pull requests, providing audit trails

---
## GitOps Workflow

<div class="mermaid">
graph LR
    DEV[Developer] -->|PR| GIT[Git Repository]
    GIT -->|Webhook| AGENT[GitOps Agent]
    AGENT -->|Reconcile| K8S[Kubernetes Cluster]
    K8S -->|Status| AGENT
    AGENT -->|Sync Status| GIT
</div>

---
## GitOps Tools

- `ArgoCD` - declarative GitOps for Kubernetes
- `Flux` - GitOps toolkit for Kubernetes
- Both watch a Git repository and apply changes automatically
- Support rollback by reverting Git commits

---
## Deployment Strategies Overview

<div class="mermaid">
graph TD
    DS[Deployment Strategies]
    DS --> REC[Recreate]
    DS --> ROLL[Rolling Update]
    DS --> BG[Blue/Green]
    DS --> CAN[Canary]
    DS --> AF[A/B Testing]
</div>

---
## Recreate Deployment

- Shut down all old instances, then start all new instances
- Simple but causes downtime during the transition
- Useful for non-production environments or batch jobs
- Not suitable for user-facing services that need availability

---
## Rolling Update

- Gradually replace old instances with new ones
- At any point, both old and new versions may be running
- Zero downtime if configured correctly
- Default strategy in Kubernetes Deployments

---
## Rolling Update Visualization

<div class="mermaid">
graph LR
    subgraph T0
        A1[v1] & A2[v1] & A3[v1] & A4[v1]
    end
    subgraph T1
        B1[v2] & B2[v1] & B3[v1] & B4[v1]
    end
    subgraph T2
        C1[v2] & C2[v2] & C3[v1] & C4[v1]
    end
    subgraph T3
        D1[v2] & D2[v2] & D3[v2] & D4[v2]
    end
    T0 --> T1 --> T2 --> T3
</div>

---
## Blue/Green Deployment

- Maintain two identical production environments: Blue and Green
- Blue runs the current version; Green has the new version
- Switch traffic from Blue to Green when ready
- Instant rollback by switching traffic back to Blue

---
## Blue/Green Architecture

<div class="mermaid">
graph TD
    LB[Load Balancer / Router]
    LB -->|100% Traffic| BLUE[Blue Environment - v1.0]
    GREEN[Green Environment - v1.1]
    BLUE --> DB[(Shared Database)]
    GREEN --> DB
    LB -.->|Switch| GREEN
</div>

---
## Blue/Green Pros and Cons

- Pros:
    - Zero-downtime deployment
    - Instant rollback by switching traffic
    - Full testing of new version in production environment
    - Simple to understand and implement
- Cons:
    - Requires double the infrastructure
    - Database schema changes need careful coordination
    - Higher cost due to duplicate environments

---
## Canary Deployment

- Roll out the new version to a small subset of users first
- Monitor the canary for errors, latency, and business metrics
- Gradually increase the percentage if metrics are healthy
- Roll back immediately if problems are detected

---
## Canary Deployment Flow

<div class="mermaid">
graph TD
    LB[Load Balancer]
    LB -->|95% Traffic| STABLE[Stable - v1.0]
    LB -->|5% Traffic| CANARY[Canary - v1.1]
    CANARY --> MON[Monitor Metrics]
    MON -->|Healthy| INC[Increase to 25%, 50%, 100%]
    MON -->|Unhealthy| RB[Rollback]
</div>

---
## Canary Metrics to Watch

- Error rate compared to the stable version
- Latency percentiles (p50, p95, p99)
- CPU and memory utilization
- Business metrics (conversion rate, checkout success)
- Automated analysis can compare canary vs baseline

---
## Progressive Delivery

- An umbrella term for advanced deployment techniques
- Combines canary deployments with automated analysis
- Tools gradually shift traffic based on real-time metrics
- Examples: `Flagger`, `Argo Rollouts`, `Spinnaker`

---
## Feature Flags

- Decouple deployment from release
- Deploy new code to production with the feature disabled
- Enable the feature for specific users, regions, or percentages
- Roll back instantly by toggling the flag, without redeploying

---
## Feature Flag Architecture

<div class="mermaid">
graph LR
    APP[Application] -->|Check Flag| FFS[Feature Flag Service]
    FFS -->|Enabled for 10%| APP
    APP -->|Feature ON| NEW[New Code Path]
    APP -->|Feature OFF| OLD[Old Code Path]
</div>

---
## Feature Flag Tools

- `LaunchDarkly` - commercial feature management platform
- `Unleash` - open-source feature toggle service
- `Flagsmith` - open-source feature flag and remote config
- `Split` - feature delivery with experimentation
- Simple config-based flags for small teams

---
## The Architect's Role in DevOps

- Design systems that support independent, fast deployments
- Define service boundaries that minimize deployment coupling
- Choose infrastructure patterns that enable automation
- Establish standards for CI/CD pipelines across teams
- Balance velocity with reliability through architectural guardrails

---
## Architectural Guardrails

- Automated fitness functions that run in the CI pipeline
- Dependency checks: prevent services from importing internal packages
- Performance budgets: reject builds that exceed latency thresholds
- Security gates: block deployments with critical vulnerabilities
- API compatibility checks: prevent breaking changes

---
## Pipeline Architecture for Microservices

<div class="mermaid">
graph TD
    subgraph Per Service
        SRC[Source Code] --> CI_SVC[CI Pipeline]
        CI_SVC --> IMG[Container Image]
        IMG --> REG[Registry]
    end
    subgraph Shared
        REG --> CD[CD Pipeline]
        CD --> DEV[Dev Cluster]
        DEV -->|Promote| STG[Staging Cluster]
        STG -->|Approve| PRD[Production Cluster]
    end
</div>

---
## Environment Promotion Strategy

- Each service has its own CI pipeline that produces an artifact
- Artifacts are promoted through environments: dev, staging, production
- Same artifact is deployed to all environments (only config changes)
- Promotion gates: automated tests, security scans, manual approval

---
## Immutable Infrastructure

- Never modify running infrastructure; replace it instead
- Build new machine images or containers for every change
- Reduces configuration drift and "works on my machine" problems
- Enables reliable rollbacks by deploying the previous image

---
## Database Migration Strategies

- Schema changes are one of the hardest parts of deployment
- Use migration tools: `Flyway`, `Liquibase`, `Alembic`
- Apply backward-compatible changes first (add column, not rename)
- Use expand-and-contract pattern for breaking schema changes
- Separate database migration from application deployment

---
## Expand and Contract Pattern

<div class="mermaid">
graph LR
    A[Step 1: Add new column] --> B[Step 2: App writes to both]
    B --> C[Step 3: Migrate data]
    C --> D[Step 4: App reads from new]
    D --> E[Step 5: Drop old column]
</div>

- Allows zero-downtime schema changes
- Each step is a separate deployment

---
## Secrets Management in CI/CD

- Never store secrets in source code or CI configuration files
- Use dedicated secret managers: `Vault`, `AWS Secrets Manager`, `GCP Secret Manager`
- Inject secrets at runtime, not at build time
- Rotate secrets automatically and audit access

---
## CI/CD Security Practices

- Sign container images and verify signatures before deployment
- Scan dependencies for known vulnerabilities (`Snyk`, `Dependabot`)
- Use least-privilege access for CI/CD service accounts
- Audit all pipeline runs and deployment activities
- Implement branch protection rules for production branches

---
## Summary

- DevOps culture enables fast, reliable software delivery
- CI ensures code quality through automated builds and tests
- CD automates the path from commit to production
- Infrastructure as Code makes environments reproducible and auditable
- Blue/Green, Canary, and Rolling updates each have different trade-offs
- Feature flags decouple deployment from release
- Architects shape the systems and standards that make DevOps possible
- Security, secrets management, and guardrails protect the pipeline
