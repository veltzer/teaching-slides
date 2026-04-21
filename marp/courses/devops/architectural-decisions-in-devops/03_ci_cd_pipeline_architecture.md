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
# CI/CD Pipeline Architecture

---

## What We Will Cover

- Centralized vs decentralized pipeline management
- Build vs buy for CI/CD tooling
- Pipeline design patterns
- Build caching and dependency management
- `GitOps` vs traditional push-based CI/CD

---

## Centralized Pipeline Management

- A single team defines pipeline templates and shared libraries
- All teams consume those templates with minimal customization
- Advantages:
    - Consistent security, compliance, and quality gates
    - Easier auditing and governance
    - Reduced duplication of effort
- Disadvantages:
    - Platform team becomes a bottleneck
    - Slow to respond to individual team needs

---

## Decentralized Pipeline Management

- Each team writes and maintains its own pipeline configuration
- Teams have full autonomy over build, test, and deploy steps
- Advantages:
    - Fast iteration without cross-team dependencies
    - Pipelines tailored to each project's needs
- Disadvantages:
    - Inconsistent practices across the organization
    - Duplicated effort solving the same problems
    - Harder to enforce security baselines

---

## Centralized vs Decentralized Diagram

![centralized_vs_decentralized_diagram](svg/courses/devops/architectural-decisions-in-devops/03_ci_cd_pipeline_architecture/centralized_vs_decentralized_diagram.svg)

---

## Shared Pipeline Libraries

- Reusable code modules that encapsulate common pipeline logic
- Examples: `Jenkins` shared libraries, `GitHub Actions` reusable workflows
- Typically stored in a dedicated repository and versioned
- Teams import and compose them rather than copying configuration

```yaml
# Reusable workflow reference
jobs:
  build:
    uses: org/shared-workflows/.github/workflows/build.yml@v2
    with:
      language: java
    secrets: inherit
```

---

## Platform Teams vs Embedded DevOps

- **Platform team model**: dedicated engineers build and maintain the CI/CD platform
    - Teams consume the platform as a service
    - Clear ownership but potential communication gap
- **Embedded DevOps model**: DevOps engineers sit within product teams
    - Closer alignment with product needs
    - Risk of diverging practices across teams

---

## Balancing Standardization with Autonomy

- Define a "golden path" with sensible defaults
- Allow teams to override specific stages when justified
- Enforce non-negotiable gates (security scans, compliance checks)
- Use policy-as-code tools like `OPA` or `Kyverno` to validate pipelines
- Publish an internal developer portal documenting the golden path

---

## Build vs Buy: Key Questions

- What is the total cost of ownership for self-hosting?
- How critical is pipeline uptime to your business?
- Do you have the team to operate infrastructure?
- How important is data sovereignty and network isolation?
- What is the migration cost if you need to switch later?

---

## Self-Hosted vs SaaS CI/CD

- **Self-hosted**: `Jenkins`, `GitLab` self-managed, `Drone`
- **SaaS**: `GitHub Actions`, `GitLab` SaaS, `CircleCI`, `Buildkite`

| Dimension | Self-Hosted | SaaS |
|---|---|---|
| Setup cost | High | Low |
| Maintenance | Your team | Vendor |
| Customization | Unlimited | Limited |
| Data control | Full | Shared |
| Scaling | Manual | Automatic |

---

## Vendor Lock-in Considerations

- Pipeline configuration syntax is vendor-specific
    - `Jenkinsfile` (Groovy) vs `GitHub Actions` (YAML) vs `GitLab CI` (YAML)
- Proprietary features create switching costs
    - Marketplace actions, built-in caches, deployment targets
- Mitigation strategies:
    - Keep business logic in scripts, not pipeline DSL
    - Wrap vendor-specific steps behind shell scripts or `Makefiles`
    - Use container-based build steps for portability

---

## Migration Cost and Portability

- Rewriting hundreds of pipelines is expensive and risky
- Automated migration tools exist but rarely cover edge cases
- Strategies to reduce future migration cost:
    - Minimize inline pipeline logic
    - Use `Dockerfile`-based build environments
    - Store build logic in `Makefile`, `Taskfile`, or `Just` commands
    - Test pipeline logic locally where possible

---

## Portability Pattern: Script-Driven Builds

```makefile
# Makefile - works on any CI system
.PHONY: build test lint deploy

build:
    docker build -t myapp:$(VERSION) .

test:
    docker run myapp:$(VERSION) make unit-test

lint:
    docker run myapp:$(VERSION) make lint

deploy:
    ./scripts/deploy.sh $(ENV)
```

- The CI pipeline only calls `make build`, `make test`, etc.
- Switching CI systems means rewriting the glue, not the logic

---

## Pipeline Design Patterns Overview

![pipeline_design_patterns_overview](svg/courses/devops/architectural-decisions-in-devops/03_ci_cd_pipeline_architecture/pipeline_design_patterns_overview.svg)

---

## Fan-Out and Fan-In Pattern

- **Fan-out**: a single stage spawns multiple parallel jobs
    - Run unit tests, integration tests, and linting concurrently
    - Reduces total pipeline duration
- **Fan-in**: parallel jobs converge before the next stage proceeds
    - Deployment only happens after all checks pass
- Most CI systems support this natively with `needs` or `depends_on`

---

## Fan-Out Example (`GitHub Actions`)

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: make build
  unit-test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: make unit-test
  lint:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: make lint
  deploy:
    needs: [unit-test, lint]
    runs-on: ubuntu-latest
    steps:
      - run: make deploy
```

---

## Pipeline as Code vs UI-Configured Pipelines

- **Pipeline as code**: definition lives in the repository
    - Examples: `Jenkinsfile`, `.github/workflows/*.yml`, `.gitlab-ci.yml`
    - Versioned, reviewed in PRs, testable on branches
- **UI-configured**: defined through a web interface
    - Examples: `Azure DevOps` classic pipelines, `Bamboo` plans
    - Easier onboarding but harder to audit and reproduce
- Pipeline as code is the industry standard because it enables version control, code review, and `DRY` through templates

---

## Triggered vs Scheduled vs Event-Driven Pipelines

| Type | Trigger | Use Case |
|---|---|---|
| Triggered | `git push`, PR open | Standard CI builds |
| Scheduled | Cron expression | Nightly builds, dependency checks |
| Event-driven | Webhook, message queue | Cross-repo orchestration |

- Most pipelines are triggered by `git` events
- Scheduled pipelines catch time-dependent regressions
- Event-driven pipelines enable complex multi-service workflows

---

## Pipeline Trigger Examples

```yaml
# Triggered by git push
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```

```yaml
# Scheduled nightly build
on:
  schedule:
    - cron: "0 2 * * *"
```

```yaml
# Event-driven via API
on:
  repository_dispatch:
    types: [deploy-request]
```

---

## Build Caching Fundamentals

- Caching avoids redundant work by reusing previous outputs
- Key cache targets:
    - Compiled artifacts and object files
    - Downloaded dependencies (`npm`, `pip`, `maven`)
    - Docker image layers
- Effective caching can reduce build times by 50-90%

---
## Remote Build Caches

![remote_build_caches](svg/courses/devops/architectural-decisions-in-devops/03_ci_cd_pipeline_architecture/remote_build_caches.svg)

---
## Remote Build Caches: Details

- Runners share a centralized cache over the network
- Tools: `Bazel` remote cache, `Gradle` build cache, `sccache`, `Turborepo`

---

## Dependency Vendoring vs Dynamic Resolution

- **Vendoring**: dependencies are committed into the repository
    - Builds are fully self-contained, no network calls needed
    - Repository size grows significantly
- **Dynamic resolution**: dependencies are fetched at build time
    - Smaller repository
    - Requires network access and a reliable registry
    - Risk of upstream changes or registry outages

| Factor | Vendoring | Dynamic |
|---|---|---|
| Reproducibility | High | Medium |
| Repo size | Large | Small |
| Build speed (cold) | Fast | Slow |

---

## Reproducible Builds

- A build is reproducible if given the same source, it produces bit-for-bit identical output
- Why it matters:
    - Verifiable supply chain integrity
    - Easier debugging of production issues
    - Required for some compliance frameworks
- Key requirements:
    - Pinned dependency versions with lock files
    - Deterministic build tools (no timestamps in output)
    - Controlled build environment (containers, `Nix`)

---

## Achieving Reproducible Builds

1. Use lock files (`package-lock.json`, `go.sum`, `Cargo.lock`)
1. Pin base images with digest (`sha256:...`), not tags
1. Set `SOURCE_DATE_EPOCH` to strip timestamps
1. Use hermetic build systems like `Bazel` or `Nix`
1. Verify builds with tools like `diffoscope`

```json
{
  "packages": {
    "node_modules/express": {
      "version": "4.18.2",
      "integrity": "sha512-abc123..."
    }
  }
}
```

---

## GitOps: Core Concept

- `GitOps` uses `git` as the single source of truth for infrastructure and application state
- A `GitOps` operator watches a `git` repository and reconciles the live system to match
- Changes are made via pull requests, not manual commands
- The operator continuously ensures the desired state matches the actual state

---

## GitOps Architecture

![gitops_architecture](svg/courses/devops/architectural-decisions-in-devops/03_ci_cd_pipeline_architecture/gitops_architecture.svg)

---
## Push vs Pull Deployment Models

![push_vs_pull_deployment_models](svg/courses/devops/architectural-decisions-in-devops/03_ci_cd_pipeline_architecture/push_vs_pull_deployment_models.svg)

---
## Push vs Pull Deployment Models: Details

- **Push**: CI needs production credentials, runs `kubectl apply`
- **Pull**: operator inside cluster pulls state, credentials stay internal

---

## Pull-Based Reconciliation Model

- The `GitOps` operator runs a continuous reconciliation loop:
    1. Fetch desired state from `git`
    1. Compare with actual state in the cluster
    1. Apply changes to close the gap
    1. Report status back (success, drift detected, error)
- Common operators: `Argo CD`, `Flux CD`

---

## Reconciliation Loop in `Argo CD`

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  source:
    repoURL: https://github.com/org/manifests
    targetRevision: main
    path: apps/my-app
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

---

## Drift Detection and Self-Healing

- **Drift**: the actual state diverges from the desired state in `git`
- Causes of drift:
    - Manual `kubectl` edits
    - Operators or controllers modifying resources
    - External systems changing state
- **Self-healing**: the operator automatically reverts drift
    - `selfHeal: true` in `Argo CD`
    - Prevents "snowflake" environments

---

## Drift Detection Flow

![drift_detection_flow](svg/courses/devops/architectural-decisions-in-devops/03_ci_cd_pipeline_architecture/drift_detection_flow.svg)

---

## When to Use GitOps (and When Not)

- **Good fit**:
    - `Kubernetes`-native workloads with declarative manifests
    - Environments where audit trails are mandatory
    - Multi-cluster deployments needing a single source of truth
- **Poor fit**:
    - Non-declarative systems without a reconciliation API
    - Stateful deployments with complex migration steps
    - Small teams where the tooling overhead is not justified

---
## Hybrid Approach: CI + GitOps

![hybrid_approach_ci_gitops](svg/courses/devops/architectural-decisions-in-devops/03_ci_cd_pipeline_architecture/hybrid_approach_ci_gitops.svg)

---
## Hybrid Approach: CI + GitOps: Details

- CI builds and tests the application, then updates the config repo
- `Argo CD` picks up the change and deploys to the cluster

---

## Pipeline Security Best Practices

- Never store secrets in pipeline configuration files
- Use short-lived credentials (`OIDC`, workload identity)
- Pin action versions by `SHA`, not tag
- Enable branch protection and required reviews
- Scan pipeline definitions for misconfigurations (`Checkov`, `Trivy`)

```yaml
# Pin by SHA, not tag (tags are mutable)
- uses: actions/checkout@b4ffde65f46336ab88eb53b
```

---
## Pipeline Observability and DORA Metrics

![pipeline_observability_and_dora_metrics](svg/courses/devops/architectural-decisions-in-devops/03_ci_cd_pipeline_architecture/pipeline_observability_and_dora_metrics.svg)

---
## Pipeline Observability and DORA Metrics: Details

- Track build duration, success rate, queue time, flaky test rate
- Export metrics to `Prometheus`, `Datadog`, or `Grafana`

---
## Multi-Stage Deployment Pipelines

![multi_stage_deployment_pipelines](svg/courses/devops/architectural-decisions-in-devops/03_ci_cd_pipeline_architecture/multi_stage_deployment_pipelines.svg)

---
## Multi-Stage Deployment Pipelines: Details

- Promote the same artifact through `dev` -> `staging` -> `production`
- Gate promotions with automated tests, manual approvals, or canary analysis

---

## Monorepo Pipeline Strategies

- Monorepos require pipelines that only build what changed
- Techniques:
    - Path-based triggering (`paths` filter in `GitHub Actions`)
    - Dependency graph analysis (`Nx`, `Turborepo`, `Bazel`)
    - Affected target detection to skip unchanged modules

```yaml
on:
  push:
    paths:
      - "services/api/**"
      - "libs/shared/**"
```

---

## Container Image Build Optimization

- Use multi-stage `Dockerfile` builds to minimize image size
- Order layers from least to most frequently changing
- Use `BuildKit` cache mounts for package manager caches

```dockerfile
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm npm ci
COPY . .
RUN npm run build

FROM node:20-alpine
COPY --from=build /app/dist /app
CMD ["node", "/app/index.js"]
```

---

## Pipeline Anti-Patterns

- **Snowflake pipelines**: every team has a unique, undocumented pipeline
- **God pipeline**: one massive pipeline that does everything
- **Secret sprawl**: credentials scattered across pipeline configs
- **Ignoring failures**: `continue-on-error: true` used everywhere
- **No timeout**: builds that run indefinitely consuming resources

---

## Key Decisions and Framework

| Decision | Trade-off |
|---|---|
| Centralized vs decentralized | Control vs autonomy |
| Build vs buy | Flexibility vs operational cost |
| Pipeline as code vs UI | Auditability vs ease of use |
| Vendoring vs dynamic deps | Reproducibility vs repo size |
| `GitOps` vs push-based | Security vs complexity |

1. Start simple, measure from day one, invest in caching early
1. Keep build logic in scripts, not CI-specific syntax
1. Adopt `GitOps` when you have `Kubernetes` and need audit trails
