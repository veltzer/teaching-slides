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

<svg viewBox="0 0 700 200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
  <!-- Centralized side -->
  <text x="170" y="25" text-anchor="middle" font-size="14" font-weight="bold">Centralized</text>
  <rect x="110" y="40" width="120" height="40" fill="#bbdefb" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="170" y="65" text-anchor="middle" font-size="12">Platform Team</text>
  <line x1="170" y1="80" x2="80" y2="130" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="170" y1="80" x2="170" y2="130" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="170" y1="80" x2="260" y2="130" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="30" y="130" width="100" height="35" fill="#c8e6c9" stroke="#388e3c" stroke-width="2" rx="5"/>
  <text x="80" y="152" text-anchor="middle" font-size="11">Team A</text>
  <rect x="140" y="130" width="100" height="35" fill="#c8e6c9" stroke="#388e3c" stroke-width="2" rx="5"/>
  <text x="190" y="152" text-anchor="middle" font-size="11">Team B</text>
  <rect x="250" y="130" width="100" height="35" fill="#c8e6c9" stroke="#388e3c" stroke-width="2" rx="5"/>
  <text x="300" y="152" text-anchor="middle" font-size="11">Team C</text>
  <!-- Decentralized side -->
  <text x="530" y="25" text-anchor="middle" font-size="14" font-weight="bold">Decentralized</text>
  <rect x="400" y="50" width="100" height="50" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="5"/>
  <text x="450" y="72" text-anchor="middle" font-size="11">Team A</text>
  <text x="450" y="88" text-anchor="middle" font-size="10" fill="#555">own pipeline</text>
  <rect x="510" y="50" width="100" height="50" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="5"/>
  <text x="560" y="72" text-anchor="middle" font-size="11">Team B</text>
  <text x="560" y="88" text-anchor="middle" font-size="10" fill="#555">own pipeline</text>
  <rect x="620" y="50" width="100" height="50" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="5"/>
  <text x="670" y="72" text-anchor="middle" font-size="11">Team C</text>
  <text x="670" y="88" text-anchor="middle" font-size="10" fill="#555">own pipeline</text>
</svg>

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

<svg viewBox="0 0 700 160" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr2" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
  <!-- Linear -->
  <text x="110" y="20" text-anchor="middle" font-size="13" font-weight="bold">Linear</text>
  <rect x="10" y="30" width="60" height="30" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="4"/>
  <text x="40" y="50" text-anchor="middle" font-size="10">Build</text>
  <line x1="70" y1="45" x2="90" y2="45" stroke="#333" stroke-width="2" marker-end="url(#arr2)"/>
  <rect x="90" y="30" width="60" height="30" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="4"/>
  <text x="120" y="50" text-anchor="middle" font-size="10">Test</text>
  <line x1="150" y1="45" x2="170" y2="45" stroke="#333" stroke-width="2" marker-end="url(#arr2)"/>
  <rect x="170" y="30" width="60" height="30" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="4"/>
  <text x="200" y="50" text-anchor="middle" font-size="10">Deploy</text>
  <!-- Fan-out / Fan-in -->
  <text x="490" y="20" text-anchor="middle" font-size="13" font-weight="bold">Fan-out / Fan-in</text>
  <rect x="350" y="55" width="60" height="30" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="4"/>
  <text x="380" y="75" text-anchor="middle" font-size="10">Build</text>
  <line x1="410" y1="63" x2="450" y2="45" stroke="#333" stroke-width="2" marker-end="url(#arr2)"/>
  <line x1="410" y1="70" x2="450" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arr2)"/>
  <line x1="410" y1="77" x2="450" y2="95" stroke="#333" stroke-width="2" marker-end="url(#arr2)"/>
  <rect x="450" y="30" width="80" height="25" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="4"/>
  <text x="490" y="47" text-anchor="middle" font-size="9">Unit Tests</text>
  <rect x="450" y="58" width="80" height="25" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="4"/>
  <text x="490" y="75" text-anchor="middle" font-size="9">Integration</text>
  <rect x="450" y="86" width="80" height="25" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="4"/>
  <text x="490" y="103" text-anchor="middle" font-size="9">Security Scan</text>
  <line x1="530" y1="43" x2="570" y2="63" stroke="#333" stroke-width="2" marker-end="url(#arr2)"/>
  <line x1="530" y1="71" x2="570" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arr2)"/>
  <line x1="530" y1="99" x2="570" y2="77" stroke="#333" stroke-width="2" marker-end="url(#arr2)"/>
  <rect x="570" y="55" width="60" height="30" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="4"/>
  <text x="600" y="75" text-anchor="middle" font-size="10">Deploy</text>
</svg>

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

<svg viewBox="0 0 600 200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr3" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="50" width="120" height="40" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="80" y="75" text-anchor="middle" font-size="12">CI Runner A</text>
  <rect x="20" y="120" width="120" height="40" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="80" y="145" text-anchor="middle" font-size="12">CI Runner B</text>
  <rect x="240" y="70" width="140" height="60" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="5"/>
  <text x="310" y="98" text-anchor="middle" font-size="13" font-weight="bold">Remote Cache</text>
  <text x="310" y="118" text-anchor="middle" font-size="10" fill="#555">(S3, GCS, Artifactory)</text>
  <rect x="460" y="50" width="120" height="40" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="520" y="75" text-anchor="middle" font-size="12">CI Runner C</text>
  <rect x="460" y="120" width="120" height="40" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="520" y="145" text-anchor="middle" font-size="12">CI Runner D</text>
  <line x1="140" y1="70" x2="238" y2="90" stroke="#333" stroke-width="2" marker-end="url(#arr3)"/>
  <line x1="140" y1="140" x2="238" y2="110" stroke="#333" stroke-width="2" marker-end="url(#arr3)"/>
  <line x1="382" y1="90" x2="458" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arr3)"/>
  <line x1="382" y1="110" x2="458" y2="140" stroke="#333" stroke-width="2" marker-end="url(#arr3)"/>
  <text x="170" y="62" font-size="10" fill="#1565c0">push</text>
  <text x="170" y="145" font-size="10" fill="#1565c0">push</text>
  <text x="415" y="70" font-size="10" fill="#2e7d32">pull</text>
  <text x="415" y="140" font-size="10" fill="#2e7d32">pull</text>
</svg>

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

<svg viewBox="0 0 700 250" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr4" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="90" width="100" height="40" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="70" y="115" text-anchor="middle" font-size="12">Developer</text>
  <rect x="180" y="90" width="120" height="40" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="5"/>
  <text x="240" y="115" text-anchor="middle" font-size="12">Git Repository</text>
  <rect x="370" y="90" width="130" height="40" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="435" y="115" text-anchor="middle" font-size="12">GitOps Operator</text>
  <rect x="570" y="70" width="110" height="80" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2" rx="5"/>
  <text x="625" y="100" text-anchor="middle" font-size="12">Kubernetes</text>
  <text x="625" y="118" text-anchor="middle" font-size="12">Cluster</text>
  <text x="625" y="138" text-anchor="middle" font-size="10" fill="#555">(actual state)</text>
  <line x1="120" y1="110" x2="178" y2="110" stroke="#333" stroke-width="2" marker-end="url(#arr4)"/>
  <text x="150" y="102" text-anchor="middle" font-size="9" fill="#555">push</text>
  <line x1="300" y1="105" x2="368" y2="105" stroke="#333" stroke-width="2" marker-end="url(#arr4)"/>
  <text x="334" y="98" text-anchor="middle" font-size="9" fill="#555">pull</text>
  <line x1="500" y1="110" x2="568" y2="110" stroke="#2e7d32" stroke-width="2" marker-end="url(#arr4)"/>
  <text x="534" y="102" text-anchor="middle" font-size="9" fill="#2e7d32">reconcile</text>
  <path d="M 570 150 Q 435 210 370 130" stroke="#7b1fa2" stroke-width="1.5" fill="none" stroke-dasharray="5,4" marker-end="url(#arr4)"/>
  <text x="460" y="195" text-anchor="middle" font-size="9" fill="#7b1fa2">observe actual state</text>
</svg>

---

## Push vs Pull Deployment Models

<svg viewBox="0 0 700 120" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr5" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
  <text x="170" y="20" text-anchor="middle" font-size="13" font-weight="bold">Push Model</text>
  <rect x="30" y="35" width="100" height="35" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="80" y="57" text-anchor="middle" font-size="11">CI Server</text>
  <rect x="200" y="35" width="110" height="35" fill="#ffcdd2" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="255" y="57" text-anchor="middle" font-size="11">Production</text>
  <line x1="130" y1="52" x2="198" y2="52" stroke="#c62828" stroke-width="2" marker-end="url(#arr5)"/>
  <text x="164" y="45" text-anchor="middle" font-size="9" fill="#c62828">push + creds</text>
  <text x="530" y="20" text-anchor="middle" font-size="13" font-weight="bold">Pull Model (GitOps)</text>
  <rect x="400" y="35" width="100" height="35" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="5"/>
  <text x="450" y="57" text-anchor="middle" font-size="11">Git Repo</text>
  <rect x="570" y="35" width="110" height="35" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="625" y="57" text-anchor="middle" font-size="11">Production</text>
  <line x1="568" y1="52" x2="502" y2="52" stroke="#2e7d32" stroke-width="2" marker-end="url(#arr5)"/>
  <text x="535" y="45" text-anchor="middle" font-size="9" fill="#2e7d32">pull desired state</text>
</svg>

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

<svg viewBox="0 0 600 180" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr6" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="50" width="110" height="45" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="5"/>
  <text x="75" y="68" text-anchor="middle" font-size="11">Desired State</text>
  <text x="75" y="83" text-anchor="middle" font-size="9" fill="#555">(git)</text>
  <rect x="180" y="50" width="110" height="45" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="235" y="68" text-anchor="middle" font-size="11">Operator</text>
  <text x="235" y="83" text-anchor="middle" font-size="9" fill="#555">compare</text>
  <rect x="340" y="50" width="110" height="45" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="395" y="68" text-anchor="middle" font-size="11">Actual State</text>
  <text x="395" y="83" text-anchor="middle" font-size="9" fill="#555">(cluster)</text>
  <rect x="480" y="50" width="100" height="45" fill="#ffcdd2" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="530" y="68" text-anchor="middle" font-size="11" fill="#c62828">Drift!</text>
  <text x="530" y="83" text-anchor="middle" font-size="9" fill="#c62828">auto-heal</text>
  <line x1="130" y1="72" x2="178" y2="72" stroke="#333" stroke-width="2" marker-end="url(#arr6)"/>
  <line x1="338" y1="72" x2="292" y2="72" stroke="#333" stroke-width="2" marker-end="url(#arr6)"/>
  <path d="M 235 95 Q 235 150 530 150 Q 530 95 530 95" stroke="#c62828" stroke-width="1.5" fill="none" stroke-dasharray="5,4" marker-end="url(#arr6)"/>
  <text x="380" y="165" text-anchor="middle" font-size="9" fill="#c62828">reconcile to desired state</text>
</svg>

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

<svg viewBox="0 0 700 180" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr7" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="60" width="100" height="40" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="70" y="85" text-anchor="middle" font-size="11">Developer</text>
  <rect x="160" y="60" width="100" height="40" fill="#bbdefb" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="210" y="85" text-anchor="middle" font-size="11">CI Pipeline</text>
  <rect x="310" y="40" width="110" height="35" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="5"/>
  <text x="365" y="62" text-anchor="middle" font-size="10">App Repo</text>
  <rect x="310" y="90" width="110" height="35" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="5"/>
  <text x="365" y="112" text-anchor="middle" font-size="10">Config Repo</text>
  <rect x="470" y="60" width="100" height="40" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="520" y="85" text-anchor="middle" font-size="11">Argo CD</text>
  <rect x="610" y="60" width="80" height="40" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2" rx="5"/>
  <text x="650" y="85" text-anchor="middle" font-size="11">Cluster</text>
  <line x1="120" y1="80" x2="158" y2="80" stroke="#333" stroke-width="2" marker-end="url(#arr7)"/>
  <line x1="260" y1="70" x2="308" y2="58" stroke="#333" stroke-width="2" marker-end="url(#arr7)"/>
  <line x1="260" y1="90" x2="308" y2="107" stroke="#1565c0" stroke-width="2" marker-end="url(#arr7)"/>
  <text x="270" y="115" font-size="8" fill="#1565c0">update image tag</text>
  <line x1="420" y1="107" x2="468" y2="85" stroke="#333" stroke-width="2" marker-end="url(#arr7)"/>
  <line x1="570" y1="80" x2="608" y2="80" stroke="#2e7d32" stroke-width="2" marker-end="url(#arr7)"/>
</svg>

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

<svg viewBox="0 0 600 180" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="15" width="260" height="65" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="8"/>
  <text x="150" y="38" text-anchor="middle" font-size="12" font-weight="bold" fill="#2e7d32">Throughput</text>
  <text x="150" y="55" text-anchor="middle" font-size="10">Deployment Frequency</text>
  <text x="150" y="70" text-anchor="middle" font-size="10">Lead Time for Changes</text>
  <rect x="320" y="15" width="260" height="65" fill="#ffcdd2" stroke="#c62828" stroke-width="2" rx="8"/>
  <text x="450" y="38" text-anchor="middle" font-size="12" font-weight="bold" fill="#c62828">Stability</text>
  <text x="450" y="55" text-anchor="middle" font-size="10">Change Failure Rate</text>
  <text x="450" y="70" text-anchor="middle" font-size="10">Mean Time to Recovery</text>
  <rect x="100" y="105" width="400" height="50" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="8"/>
  <text x="300" y="128" text-anchor="middle" font-size="11" font-weight="bold">CI/CD architecture directly impacts all four metrics</text>
  <text x="300" y="145" text-anchor="middle" font-size="10" fill="#555">Faster pipelines = shorter lead time = higher deploy frequency</text>
</svg>

- Track build duration, success rate, queue time, flaky test rate
- Export metrics to `Prometheus`, `Datadog`, or `Grafana`

---

## Multi-Stage Deployment Pipelines

<svg viewBox="0 0 700 130" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr8" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="40" width="90" height="40" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="65" y="65" text-anchor="middle" font-size="11">Build</text>
  <rect x="150" y="40" width="90" height="40" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="195" y="65" text-anchor="middle" font-size="11">Test</text>
  <rect x="280" y="40" width="110" height="40" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="335" y="65" text-anchor="middle" font-size="11">Deploy Dev</text>
  <rect x="430" y="40" width="110" height="40" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="5"/>
  <text x="485" y="58" text-anchor="middle" font-size="11">Deploy Staging</text>
  <text x="485" y="72" text-anchor="middle" font-size="9" fill="#555">(approval gate)</text>
  <rect x="580" y="40" width="110" height="40" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2" rx="5"/>
  <text x="635" y="65" text-anchor="middle" font-size="11">Deploy Prod</text>
  <line x1="110" y1="60" x2="148" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arr8)"/>
  <line x1="240" y1="60" x2="278" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arr8)"/>
  <line x1="390" y1="60" x2="428" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arr8)"/>
  <line x1="540" y1="60" x2="578" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arr8)"/>
</svg>

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
