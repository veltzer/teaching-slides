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
# Source Code Management Strategy

---

## Why SCM Strategy Matters

- Code organization shapes team velocity and collaboration
- Repository structure impacts CI/CD pipeline design
- Branching models affect release cadence and stability
- Ownership models determine accountability and review quality
- Wrong choices create friction that compounds over time

---

## Key Decisions We Will Cover

1. Monorepo vs polyrepo architecture
1. Branching strategies and merge policies
1. Code ownership and review models

Notes:

- Each decision interacts with the others
- There is no universal "best" approach - context matters

---

## Monorepo vs Polyrepo

![monorepo_vs_polyrepo](svg/courses/devops/architectural-decisions-in-devops/02_source_code_management_strategy/monorepo_vs_polyrepo.svg)

---

## What Is a Monorepo?

- A single repository containing multiple projects, services, or libraries
- All code lives in one version-controlled tree
- Used by Google, Meta, Microsoft, and others at massive scale
- Not the same as a monolith - services can be independently deployable

---

## What Is a Polyrepo?

- Each service, library, or project has its own repository
- The default model on platforms like `GitHub` and `GitLab`
- Teams own their repositories independently
- Dependencies are managed through package registries or versioned artifacts

---

## Monorepo Advantages

- Atomic cross-project changes in a single commit
- Unified versioning eliminates dependency hell
- Easier code sharing and refactoring across boundaries
- Single CI/CD configuration to maintain
- Consistent tooling, linting, and formatting rules

---

## Monorepo Disadvantages

- Repository size grows unbounded over time
- Standard `git` operations slow down at scale
- CI/CD must be smart about what to build and test
- Access control is coarser-grained
- Onboarding can be overwhelming

---

## Polyrepo Advantages and Disadvantages

- Advantages:
    - Clear ownership boundaries per repository
    - Independent release cycles and versioning
    - Fine-grained access control per team
    - Smaller repositories are fast to clone and work with
- Disadvantages:
    - Cross-cutting changes require coordinated PRs across repos
    - Dependency version drift between repositories
    - Duplicated CI/CD configuration and tooling

---

## Scaling Considerations

- **Monorepo** - challenge is raw size:
    - `git` sparse checkout for partial working copies
    - `git` virtual filesystem (`VFS for Git` / `GVFS`)
    - Shallow clones to limit history depth
    - Google uses `Piper` (custom VCS) for their monorepo
- **Polyrepo** - challenge is coordination:
    - Automated dependency update bots (`Renovate`, `Dependabot`)
    - Centralized templates for CI/CD pipelines
    - Meta-repositories or manifests to track related repos

---

## Tooling Requirements for Monorepos

- Build system must support incremental and affected-only builds
- Popular tools:
    - `Bazel` - Google's build system, language-agnostic
    - `Nx` - monorepo tooling for JavaScript/TypeScript
    - `Turborepo` - fast build system for JS/TS monorepos
    - `Pants` - Python-focused build system
    - `Buck2` - Meta's build system
- Change detection is critical for CI performance

---

## Monorepo Build: Affected-Only Testing

```bash
# Nx: only test projects affected by changes
nx affected:test --base=origin/main --head=HEAD

# Bazel: query for affected targets
bazel query \
  "rdeps(//..., set($(git diff --name-only main)))"
```

- Avoids rebuilding and retesting the entire repo
- Reduces CI time from hours to minutes

---
## Dependency Management

![dependency_management](svg/courses/devops/architectural-decisions-in-devops/02_source_code_management_strategy/dependency_management.svg)

---
## Dependency Management: Details

- Each repo declares its own dependency versions
- `Dependabot` or `Renovate` automates version bumps

---

## Impact on Team Autonomy and Coupling

| Factor | Monorepo | Polyrepo |
|---|---|---|
| Autonomy | Lower | Higher |
| Coupling | Higher | Lower |
| Consistency | Enforced | Divergent |
| Cross-team changes | Easy | Coordinated |
| Shared standards | Natural | Requires effort |

- Monorepo: less autonomy, more consistency
- Polyrepo: more autonomy, less consistency

---

## Choosing: Monorepo vs Polyrepo

| Factor | Monorepo | Polyrepo |
|---|---|---|
| Team size | Small-medium | Any |
| Shared code | Heavy | Minimal |
| Release cadence | Unified | Independent |
| Tooling investment | High | Low |
| Access control | Coarse | Fine |

- Hybrid approach: core platform in monorepo, satellites in polyrepos
- Use `git submodules` or `git subtree` to bridge repos

---

## Branching Strategies Overview

![branching_strategies_overview](svg/courses/devops/architectural-decisions-in-devops/02_source_code_management_strategy/branching_strategies_overview.svg)

---

## Trunk-Based Development

- All developers commit directly to `main` (or `trunk`)
- Short-lived feature branches (< 1 day) if branches are used at all
- Feature flags hide incomplete work from users
- Requires strong CI and automated testing
- Enables continuous delivery

---

## Trunk-Based Development: Flow

![trunk_based_development_flow](svg/courses/devops/architectural-decisions-in-devops/02_source_code_management_strategy/trunk_based_development_flow.svg)

---

## Trunk-Based: When to Use

- Teams with high CI/CD maturity and test coverage
- Continuous deployment environments
- Small teams with high trust
- Products that deploy frequently (multiple times per day)
- When feature flags are already part of the workflow

---

## Feature Branch Development

- Each feature or task gets its own branch from `main`
- Branches live for days or weeks
- Code review via pull request before merging
- `main` is always in a deployable state
- The most common model in open-source and enterprise teams

---

## Feature Branching: Flow

![feature_branching_flow](svg/courses/devops/architectural-decisions-in-devops/02_source_code_management_strategy/feature_branching_flow.svg)

---

## Trunk-Based vs Feature Branching

| Aspect | Trunk-Based | Feature Branch |
|---|---|---|
| Branch lifetime | Hours | Days to weeks |
| Merge conflicts | Rare | Common |
| Code review | Post-commit or pair | Pre-merge PR |
| Feature flags | Required | Optional |
| CI requirements | Very high | Moderate |
| Merge risk | Low per commit | Higher per branch |

---

## Git Flow Overview

- Introduced by Vincent Driessen in 2010
- Two long-lived branches: `main` and `develop`
- Supporting branches: `feature/*`, `release/*`, `hotfix/*`
- Designed for projects with scheduled releases

---

## Git Flow Visualization

![git_flow_visualization](svg/courses/devops/architectural-decisions-in-devops/02_source_code_management_strategy/git_flow_visualization.svg)

---

## Git Flow: When to Use

- Projects with scheduled, versioned releases
- Software distributed to customers (mobile apps, on-prem)
- Teams that need clear release preparation phases
- When multiple versions must be maintained simultaneously
- Not ideal for continuous deployment workflows

---

## Git Flow Variations

- **GitHub Flow**: simplified, only `main` + feature branches
    - Branch, commit, PR, merge, deploy - simplest model
- **GitLab Flow**: adds environment branches (`staging`, `production`)
- **OneFlow**: single long-lived branch with release branches
- **Release Flow**: Microsoft's model, trunk-based with release branches
- Choose based on your release cadence and deployment model

---

## Release Branching vs Release from Trunk

![release_branching_vs_release_from_trunk](svg/courses/devops/architectural-decisions-in-devops/02_source_code_management_strategy/release_branching_vs_release_from_trunk.svg)

---

## Release Branch vs Release from Trunk

- **Release branch**:
    - Cut from `main` or `develop` for stabilization
    - Only bug fixes go into the release branch
    - Required when supporting multiple versions (e.g., `v1.x` and `v2.x`)
- **Release from trunk**:
    - Tag a commit on `main` to create a release
    - Requires `main` to always be deployable
    - Best for SaaS and continuous deployment workflows

---

## Branch Protection Rules

- Prevent direct pushes to critical branches (`main`, `develop`)
- Require pull request reviews before merging
- Enforce status checks (CI must pass)
- Require up-to-date branches before merging
- Prevent force pushes and branch deletion

---

## Configuring Branch Protection

```json
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["ci/build", "ci/test"]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 2,
    "dismiss_stale_reviews": true
  },
  "allow_force_pushes": false,
  "allow_deletions": false
}
```

---

## Merge Policies

- **Merge commit**: preserves full branch history, creates merge node
- **Squash merge**: condenses branch into a single commit on `main`
- **Rebase merge**: replays commits on top of `main`, linear history

| Policy | History | Bisectability | Simplicity |
|---|---|---|---|
| Merge commit | Full context | Good | Complex graph |
| Squash merge | Clean, linear | Per-feature | Loses detail |
| Rebase merge | Linear | Per-commit | Rewrites SHAs |

---

## Merge Queue

- A queue of PRs waiting to be merged into `main`
- Each PR is tested against the latest `main` plus other queued PRs
- Prevents "merge skew" where independently passing PRs break together
- Available in `GitHub`, `GitLab`, and `Mergify`
- Essential for high-traffic monorepos

---

## Code Ownership Models

- Who is responsible for reviewing and maintaining code?
- Strong ownership: specific teams own specific directories
- Collective ownership: anyone can modify any code
- Most organizations use a hybrid approach
- Ownership affects review speed, quality, and bottlenecks

---

## Strong Code Ownership

- Each module or service has a designated owner team
- Only owners can approve changes to their code
- Benefits:
    - Deep expertise in owned areas
    - Clear accountability for quality and bugs
    - Predictable review assignments
- Risks:
    - Bottlenecks when owners are unavailable
    - Silos and knowledge concentration

---

## Collective Code Ownership

- Any developer can modify any part of the codebase
- Promoted by Extreme Programming (XP)
- Benefits:
    - No single point of failure for reviews
    - Broader understanding of the system
    - Faster cross-cutting changes
- Risks:
    - Lack of deep expertise in specific areas
    - Inconsistent code quality without standards

---

## CODEOWNERS File

```misc
# .github/CODEOWNERS

# Default owner for everything
*                       @org/platform-team

# Frontend code
/src/frontend/          @org/frontend-team

# API layer
/src/api/               @org/backend-team

# Infrastructure as code
/terraform/             @org/infra-team
```

- Patterns follow `.gitignore` syntax, last matching pattern wins
- Combined with branch protection to require owner approval
- Automatically assigns reviewers on pull requests

---

## CODEOWNERS: Advanced Patterns

```gitignore
# Per-file ownership
*.js                    @org/frontend-team
*.go                    @org/backend-team
Dockerfile              @org/devops-team

# Specific critical files
/src/auth/**            @org/security-team

# Multiple owners (any can approve)
/src/shared/            @org/frontend-team @org/backend-team
```

---

## Review Policies

- Minimum number of approvals (typically 1-2)
- Require review from code owners
- Dismiss stale reviews when new commits are pushed
- Require review from specific teams for sensitive areas
- Auto-assign reviewers based on `CODEOWNERS` or round-robin

---

## Anti-Patterns to Avoid

- **Long-lived feature branches**: lead to painful merges and integration risk
- **No branch protection**: allows broken code on `main`
- **Unclear ownership**: nobody reviews, nobody is accountable
- **Over-complex branching**: Git Flow for a SaaS product is overkill
- **No CI on PRs**: code review without automated checks is incomplete

---

## Putting It All Together

![putting_it_all_together](svg/courses/devops/architectural-decisions-in-devops/02_source_code_management_strategy/putting_it_all_together.svg)

---

## Key Takeaways

- Monorepo simplifies sharing but requires build tooling investment
- Polyrepo gives autonomy but complicates cross-cutting changes
- Trunk-based development enables continuous delivery
- Git Flow suits scheduled, versioned releases
- `CODEOWNERS` enforces accountability without bottlenecks
- Branch protection and merge policies guard code quality
- Revisit your strategy as your team and product evolve
