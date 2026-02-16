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
- Each decision interacts with the others
- There is no universal "best" approach - context matters

---

## Monorepo vs Polyrepo

<svg viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="10" width="350" height="280" rx="10" fill="#e8f4f8" stroke="#333" stroke-width="2"/>
  <text x="185" y="40" text-anchor="middle" font-weight="bold" font-size="16">Monorepo</text>
  <rect x="40" y="60" width="290" height="50" rx="5" fill="#fff" stroke="#555" stroke-width="1"/>
  <text x="185" y="90" text-anchor="middle" font-size="13">Single Repository</text>
  <rect x="50" y="130" width="80" height="40" rx="5" fill="#b3d9ff" stroke="#555" stroke-width="1"/>
  <text x="90" y="155" text-anchor="middle" font-size="11">Service A</text>
  <rect x="145" y="130" width="80" height="40" rx="5" fill="#b3d9ff" stroke="#555" stroke-width="1"/>
  <text x="185" y="155" text-anchor="middle" font-size="11">Service B</text>
  <rect x="240" y="130" width="80" height="40" rx="5" fill="#b3d9ff" stroke="#555" stroke-width="1"/>
  <text x="280" y="155" text-anchor="middle" font-size="11">Lib C</text>
  <rect x="50" y="190" width="270" height="40" rx="5" fill="#d4edda" stroke="#555" stroke-width="1"/>
  <text x="185" y="215" text-anchor="middle" font-size="11">Shared tooling &amp; config</text>
  <rect x="430" y="10" width="360" height="280" rx="10" fill="#fdf2e9" stroke="#333" stroke-width="2"/>
  <text x="610" y="40" text-anchor="middle" font-weight="bold" font-size="16">Polyrepo</text>
  <rect x="450" y="60" width="100" height="70" rx="5" fill="#fff" stroke="#555" stroke-width="1"/>
  <text x="500" y="90" text-anchor="middle" font-size="11">repo-</text>
  <text x="500" y="105" text-anchor="middle" font-size="11">service-a</text>
  <rect x="570" y="60" width="100" height="70" rx="5" fill="#fff" stroke="#555" stroke-width="1"/>
  <text x="620" y="90" text-anchor="middle" font-size="11">repo-</text>
  <text x="620" y="105" text-anchor="middle" font-size="11">service-b</text>
  <rect x="450" y="150" width="100" height="70" rx="5" fill="#fff" stroke="#555" stroke-width="1"/>
  <text x="500" y="180" text-anchor="middle" font-size="11">repo-</text>
  <text x="500" y="195" text-anchor="middle" font-size="11">lib-c</text>
  <rect x="570" y="150" width="100" height="70" rx="5" fill="#fff" stroke="#555" stroke-width="1"/>
  <text x="620" y="180" text-anchor="middle" font-size="11">repo-</text>
  <text x="620" y="195" text-anchor="middle" font-size="11">infra</text>
</svg>

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

<svg viewBox="0 0 700 280" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="20" width="120" height="50" rx="8" fill="#b3d9ff" stroke="#333" stroke-width="2"/>
  <text x="80" y="50" text-anchor="middle" font-size="13">Service A</text>
  <rect x="290" y="20" width="120" height="50" rx="8" fill="#b3d9ff" stroke="#333" stroke-width="2"/>
  <text x="350" y="50" text-anchor="middle" font-size="13">Service B</text>
  <rect x="560" y="20" width="120" height="50" rx="8" fill="#b3d9ff" stroke="#333" stroke-width="2"/>
  <text x="620" y="50" text-anchor="middle" font-size="13">Service C</text>
  <rect x="160" y="140" width="130" height="50" rx="8" fill="#d4edda" stroke="#333" stroke-width="2"/>
  <text x="225" y="170" text-anchor="middle" font-size="13">Shared Lib v2.1</text>
  <rect x="420" y="140" width="130" height="50" rx="8" fill="#f8d7da" stroke="#333" stroke-width="2"/>
  <text x="485" y="170" text-anchor="middle" font-size="13">Shared Lib v1.8</text>
  <rect x="270" y="230" width="160" height="40" rx="8" fill="#fff3cd" stroke="#333" stroke-width="2"/>
  <text x="350" y="255" text-anchor="middle" font-size="12">Package Registry</text>
  <line x1="80" y1="70" x2="200" y2="140" stroke="#333" stroke-width="1.5" marker-end="url(#arrow)"/>
  <line x1="350" y1="70" x2="250" y2="140" stroke="#333" stroke-width="1.5" marker-end="url(#arrow)"/>
  <line x1="620" y1="70" x2="500" y2="140" stroke="#333" stroke-width="1.5" marker-end="url(#arrow)"/>
  <line x1="225" y1="190" x2="310" y2="230" stroke="#555" stroke-width="1" stroke-dasharray="5,3"/>
  <line x1="485" y1="190" x2="390" y2="230" stroke="#555" stroke-width="1" stroke-dasharray="5,3"/>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#333"/>
    </marker>
  </defs>
  <text x="540" y="120" font-size="11" fill="#c00">Version drift!</text>
</svg>

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

<svg viewBox="0 0 750 200" xmlns="http://www.w3.org/2000/svg">
  <line x1="50" y1="100" x2="700" y2="100" stroke="#333" stroke-width="3"/>
  <text x="375" y="85" text-anchor="middle" font-size="14" font-weight="bold">Spectrum of Branching Strategies</text>
  <circle cx="120" cy="100" r="8" fill="#28a745"/>
  <text x="120" y="135" text-anchor="middle" font-size="11">Trunk-Based</text>
  <text x="120" y="150" text-anchor="middle" font-size="10">(simplest)</text>
  <circle cx="310" cy="100" r="8" fill="#ffc107"/>
  <text x="310" y="135" text-anchor="middle" font-size="11">GitHub Flow</text>
  <circle cx="480" cy="100" r="8" fill="#fd7e14"/>
  <text x="480" y="135" text-anchor="middle" font-size="11">GitLab Flow</text>
  <circle cx="640" cy="100" r="8" fill="#dc3545"/>
  <text x="640" y="135" text-anchor="middle" font-size="11">Git Flow</text>
  <text x="640" y="150" text-anchor="middle" font-size="10">(most complex)</text>
  <text x="120" y="170" text-anchor="middle" font-size="9" fill="#666">High CI/CD maturity</text>
  <text x="640" y="170" text-anchor="middle" font-size="9" fill="#666">Versioned releases</text>
</svg>

---

## Trunk-Based Development

- All developers commit directly to `main` (or `trunk`)
- Short-lived feature branches (< 1 day) if branches are used at all
- Feature flags hide incomplete work from users
- Requires strong CI and automated testing
- Enables continuous delivery

---

## Trunk-Based Development: Flow

<svg viewBox="0 0 750 180" xmlns="http://www.w3.org/2000/svg">
  <line x1="50" y1="90" x2="700" y2="90" stroke="#28a745" stroke-width="4"/>
  <text x="30" y="95" text-anchor="end" font-size="12" font-weight="bold" fill="#28a745">main</text>
  <circle cx="120" cy="90" r="7" fill="#28a745"/>
  <circle cx="230" cy="90" r="7" fill="#28a745"/>
  <circle cx="340" cy="90" r="7" fill="#28a745"/>
  <circle cx="450" cy="90" r="7" fill="#28a745"/>
  <circle cx="560" cy="90" r="7" fill="#28a745"/>
  <circle cx="670" cy="90" r="7" fill="#28a745"/>
  <line x1="230" y1="90" x2="260" y2="40" stroke="#4a9eff" stroke-width="2"/>
  <circle cx="260" cy="40" r="5" fill="#4a9eff"/>
  <circle cx="300" cy="40" r="5" fill="#4a9eff"/>
  <line x1="260" y1="40" x2="300" y2="40" stroke="#4a9eff" stroke-width="2"/>
  <line x1="300" y1="40" x2="340" y2="90" stroke="#4a9eff" stroke-width="2"/>
  <text x="280" y="30" text-anchor="middle" font-size="10" fill="#4a9eff">short branch</text>
  <text x="120" y="120" text-anchor="middle" font-size="10">commit</text>
  <text x="450" y="120" text-anchor="middle" font-size="10">commit</text>
  <text x="670" y="120" text-anchor="middle" font-size="10">commit</text>
  <text x="375" y="170" text-anchor="middle" font-size="12" fill="#555">Developers commit directly or merge very short branches</text>
</svg>

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

<svg viewBox="0 0 750 220" xmlns="http://www.w3.org/2000/svg">
  <line x1="50" y1="100" x2="700" y2="100" stroke="#28a745" stroke-width="4"/>
  <text x="30" y="105" text-anchor="end" font-size="12" font-weight="bold" fill="#28a745">main</text>
  <circle cx="100" cy="100" r="7" fill="#28a745"/>
  <circle cx="300" cy="100" r="7" fill="#28a745"/>
  <circle cx="500" cy="100" r="7" fill="#28a745"/>
  <circle cx="680" cy="100" r="7" fill="#28a745"/>
  <line x1="100" y1="100" x2="140" y2="40" stroke="#4a9eff" stroke-width="2"/>
  <line x1="140" y1="40" x2="200" y2="40" stroke="#4a9eff" stroke-width="2"/>
  <line x1="200" y1="40" x2="260" y2="40" stroke="#4a9eff" stroke-width="2"/>
  <line x1="260" y1="40" x2="300" y2="100" stroke="#4a9eff" stroke-width="2"/>
  <circle cx="140" cy="40" r="5" fill="#4a9eff"/>
  <circle cx="200" cy="40" r="5" fill="#4a9eff"/>
  <circle cx="260" cy="40" r="5" fill="#4a9eff"/>
  <text x="200" y="28" text-anchor="middle" font-size="10" fill="#4a9eff">feature/login</text>
  <line x1="300" y1="100" x2="360" y2="170" stroke="#e36209" stroke-width="2"/>
  <line x1="360" y1="170" x2="440" y2="170" stroke="#e36209" stroke-width="2"/>
  <line x1="440" y1="170" x2="500" y2="100" stroke="#e36209" stroke-width="2"/>
  <circle cx="360" cy="170" r="5" fill="#e36209"/>
  <circle cx="440" cy="170" r="5" fill="#e36209"/>
  <text x="400" y="195" text-anchor="middle" font-size="10" fill="#e36209">feature/search</text>
  <text x="290" y="85" font-size="10" fill="#28a745">PR merge</text>
  <text x="490" y="85" font-size="10" fill="#28a745">PR merge</text>
</svg>

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

<svg viewBox="0 0 780 300" xmlns="http://www.w3.org/2000/svg">
  <line x1="50" y1="40" x2="730" y2="40" stroke="#dc3545" stroke-width="3"/>
  <text x="30" y="45" text-anchor="end" font-size="11" font-weight="bold" fill="#dc3545">main</text>
  <line x1="50" y1="120" x2="730" y2="120" stroke="#28a745" stroke-width="3"/>
  <text x="30" y="125" text-anchor="end" font-size="11" font-weight="bold" fill="#28a745">develop</text>
  <circle cx="100" cy="40" r="6" fill="#dc3545"/>
  <circle cx="400" cy="40" r="6" fill="#dc3545"/>
  <circle cx="680" cy="40" r="6" fill="#dc3545"/>
  <text x="100" y="25" text-anchor="middle" font-size="9">v1.0</text>
  <text x="400" y="25" text-anchor="middle" font-size="9">v1.1</text>
  <text x="680" y="25" text-anchor="middle" font-size="9">v2.0</text>
  <circle cx="100" cy="120" r="5" fill="#28a745"/>
  <circle cx="200" cy="120" r="5" fill="#28a745"/>
  <circle cx="350" cy="120" r="5" fill="#28a745"/>
  <circle cx="500" cy="120" r="5" fill="#28a745"/>
  <circle cx="650" cy="120" r="5" fill="#28a745"/>
  <line x1="120" y1="120" x2="140" y2="200" stroke="#4a9eff" stroke-width="1.5"/>
  <line x1="140" y1="200" x2="180" y2="200" stroke="#4a9eff" stroke-width="1.5"/>
  <line x1="180" y1="200" x2="200" y2="120" stroke="#4a9eff" stroke-width="1.5"/>
  <circle cx="140" cy="200" r="4" fill="#4a9eff"/>
  <circle cx="180" cy="200" r="4" fill="#4a9eff"/>
  <text x="160" y="225" text-anchor="middle" font-size="9" fill="#4a9eff">feature</text>
  <line x1="350" y1="120" x2="370" y2="80" stroke="#ffc107" stroke-width="1.5"/>
  <line x1="370" y1="80" x2="390" y2="80" stroke="#ffc107" stroke-width="1.5"/>
  <line x1="390" y1="80" x2="400" y2="40" stroke="#ffc107" stroke-width="1.5"/>
  <line x1="390" y1="80" x2="400" y2="120" stroke="#ffc107" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="380" y="72" text-anchor="middle" font-size="9" fill="#b38600">release</text>
  <line x1="400" y1="40" x2="420" y2="80" stroke="#e83e8c" stroke-width="1.5"/>
  <circle cx="420" cy="80" r="4" fill="#e83e8c"/>
  <line x1="420" y1="80" x2="440" y2="40" stroke="#e83e8c" stroke-width="1.5" stroke-dasharray="3,3"/>
  <line x1="420" y1="80" x2="440" y2="120" stroke="#e83e8c" stroke-width="1.5" stroke-dasharray="3,3"/>
  <text x="430" y="72" text-anchor="middle" font-size="9" fill="#e83e8c">hotfix</text>
  <line x1="500" y1="120" x2="540" y2="200" stroke="#4a9eff" stroke-width="1.5"/>
  <line x1="540" y1="200" x2="600" y2="200" stroke="#4a9eff" stroke-width="1.5"/>
  <line x1="600" y1="200" x2="650" y2="120" stroke="#4a9eff" stroke-width="1.5"/>
  <circle cx="540" cy="200" r="4" fill="#4a9eff"/>
  <circle cx="570" cy="200" r="4" fill="#4a9eff"/>
  <circle cx="600" cy="200" r="4" fill="#4a9eff"/>
  <text x="570" y="225" text-anchor="middle" font-size="9" fill="#4a9eff">feature</text>
  <rect x="200" y="260" width="400" height="30" rx="5" fill="#f8f9fa" stroke="#ccc" stroke-width="1"/>
  <text x="400" y="280" text-anchor="middle" font-size="10">main: releases only | develop: integration | feature: work</text>
</svg>

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

<svg viewBox="0 0 780 260" xmlns="http://www.w3.org/2000/svg">
  <text x="200" y="20" text-anchor="middle" font-size="13" font-weight="bold">Release Branch</text>
  <line x1="50" y1="60" x2="370" y2="60" stroke="#28a745" stroke-width="3"/>
  <text x="40" y="65" text-anchor="end" font-size="10" fill="#28a745">main</text>
  <circle cx="100" cy="60" r="5" fill="#28a745"/>
  <circle cx="200" cy="60" r="5" fill="#28a745"/>
  <circle cx="300" cy="60" r="5" fill="#28a745"/>
  <line x1="150" y1="60" x2="170" y2="120" stroke="#dc3545" stroke-width="2"/>
  <line x1="170" y1="120" x2="280" y2="120" stroke="#dc3545" stroke-width="2"/>
  <circle cx="170" cy="120" r="4" fill="#dc3545"/>
  <circle cx="220" cy="120" r="4" fill="#dc3545"/>
  <circle cx="280" cy="120" r="4" fill="#dc3545"/>
  <text x="225" y="145" text-anchor="middle" font-size="10" fill="#dc3545">release/1.0</text>
  <text x="220" y="108" text-anchor="middle" font-size="9" fill="#999">bugfixes only</text>
  <text x="590" y="20" text-anchor="middle" font-size="13" font-weight="bold">Release from Trunk</text>
  <line x1="430" y1="60" x2="750" y2="60" stroke="#28a745" stroke-width="3"/>
  <text x="420" y="65" text-anchor="end" font-size="10" fill="#28a745">main</text>
  <circle cx="480" cy="60" r="5" fill="#28a745"/>
  <circle cx="560" cy="60" r="5" fill="#28a745"/>
  <circle cx="640" cy="60" r="5" fill="#28a745"/>
  <circle cx="720" cy="60" r="5" fill="#28a745"/>
  <rect x="545" y="75" width="30" height="18" rx="3" fill="#ffc107" stroke="#b38600" stroke-width="1"/>
  <text x="560" y="88" text-anchor="middle" font-size="8" fill="#333">tag</text>
  <text x="560" y="110" text-anchor="middle" font-size="9" fill="#b38600">v1.0</text>
  <rect x="705" y="75" width="30" height="18" rx="3" fill="#ffc107" stroke="#b38600" stroke-width="1"/>
  <text x="720" y="88" text-anchor="middle" font-size="8" fill="#333">tag</text>
  <text x="720" y="110" text-anchor="middle" font-size="9" fill="#b38600">v1.1</text>
  <text x="590" y="145" text-anchor="middle" font-size="10" fill="#555">Tag commits on main for releases</text>
</svg>

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

```text
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

```text
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

<svg viewBox="0 0 750 260" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="20" width="220" height="220" rx="10" fill="#e8f4f8" stroke="#333" stroke-width="2"/>
  <text x="130" y="50" text-anchor="middle" font-weight="bold" font-size="13">Repository Structure</text>
  <text x="130" y="80" text-anchor="middle" font-size="11">Monorepo / Polyrepo</text>
  <text x="130" y="100" text-anchor="middle" font-size="11">Hybrid</text>
  <rect x="270" y="20" width="220" height="220" rx="10" fill="#fdf2e9" stroke="#333" stroke-width="2"/>
  <text x="380" y="50" text-anchor="middle" font-weight="bold" font-size="13">Branching Model</text>
  <text x="380" y="80" text-anchor="middle" font-size="11">Trunk-based</text>
  <text x="380" y="100" text-anchor="middle" font-size="11">Feature branching</text>
  <text x="380" y="120" text-anchor="middle" font-size="11">Git Flow</text>
  <rect x="520" y="20" width="220" height="220" rx="10" fill="#d4edda" stroke="#333" stroke-width="2"/>
  <text x="630" y="50" text-anchor="middle" font-weight="bold" font-size="13">Ownership Model</text>
  <text x="630" y="80" text-anchor="middle" font-size="11">CODEOWNERS</text>
  <text x="630" y="100" text-anchor="middle" font-size="11">Review policies</text>
  <text x="630" y="120" text-anchor="middle" font-size="11">Merge policies</text>
  <line x1="240" y1="130" x2="270" y2="130" stroke="#333" stroke-width="2" marker-end="url(#arr2)"/>
  <line x1="490" y1="130" x2="520" y2="130" stroke="#333" stroke-width="2" marker-end="url(#arr2)"/>
  <defs>
    <marker id="arr2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#333"/>
    </marker>
  </defs>
  <text x="130" y="190" text-anchor="middle" font-size="10" fill="#555">Shapes CI/CD</text>
  <text x="130" y="210" text-anchor="middle" font-size="10" fill="#555">and dependencies</text>
  <text x="380" y="190" text-anchor="middle" font-size="10" fill="#555">Shapes release</text>
  <text x="380" y="210" text-anchor="middle" font-size="10" fill="#555">cadence</text>
  <text x="630" y="190" text-anchor="middle" font-size="10" fill="#555">Shapes quality</text>
  <text x="630" y="210" text-anchor="middle" font-size="10" fill="#555">and accountability</text>
</svg>

---

## Key Takeaways

- Monorepo simplifies sharing but requires build tooling investment
- Polyrepo gives autonomy but complicates cross-cutting changes
- Trunk-based development enables continuous delivery
- Git Flow suits scheduled, versioned releases
- `CODEOWNERS` enforces accountability without bottlenecks
- Branch protection and merge policies guard code quality
- Revisit your strategy as your team and product evolve
