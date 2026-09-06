---
tags:
  - tools:git
  - concepts:monorepo
level: advanced
category: version-control
audience:
  - audiences:developers
  - audiences:devops

---

# Monorepo Strategies

---

## What This Chapter Covers

- Monorepo vs multi-repo: trade-offs, not religion
- Where Git struggles at scale, and what to do
- Sparse checkout and partial clone
- Monorepo tooling: build systems, code ownership, CI
- Operational realities at very large scale

---

## What Is a Monorepo?

- One Git repository for many projects
- All related code lives together: services, libs, infra, docs
- One source of truth, one place to land changes
- Atomic cross-cutting refactors are possible
- Famous practitioners: Google, Facebook, Microsoft (parts), Twitter

---

## Multi-Repo: The Common Default

- One repo per service or library
- Independent release cycles, owners, and branch strategies
- Cross-cutting changes require coordinated PRs across repos
- Good when teams are independent and stacks are heterogeneous
- The path of least resistance for most organizations

---

## Trade Off Summary

![monorepo_tradeoffs](svg/courses/git/advanced-git/06_monorepo_strategies/monorepo_tradeoffs.svg)

---

## Why Choose Monorepo?

- One change, one PR, even when it spans services
- Atomic refactors of shared APIs
- Single CI pipeline as the source of truth
- Easier code sharing — everything is in `import "..."` reach
- Cultural: one team, one tree

---

## Why Avoid Monorepo?

- Git wasn't designed for repos with millions of files
- Build, test, and CI must be smart about what changed
- Tooling expectations rise sharply
- Access control becomes coarser
- Off-the-shelf workflows assume per-repo

---

## Monorepo Structure Visualized

![monorepo_structure](svg/courses/git/advanced-git/06_monorepo_strategies/monorepo_structure.svg)

---

## The Scaling Walls

- Repo size — clone time and disk usage
- Working tree size — `git status` becomes slow
- History depth — log operations slow with millions of commits
- Index size — every operation that scans the index is hit
- Each wall has a Git feature designed to climb it

---

## Partial Clone

```bash
git clone --filter=blob:none https://example/repo
```

- Skips downloading file blobs at clone time
- Blobs fetched on demand when checked out
- Drastically reduces clone time and disk
- Trade-off: needs network access for some operations
- Best for CI, dev machines with reliable network

---

## Shallow Clone

```bash
git clone --depth=1 https://example/repo
```

- Only the most recent commit's history is fetched
- Dramatic speedup for clone
- Many history operations don't work (`git log`, `git blame` past depth)
- Useful for CI builds; not for daily development
- Can be deepened later with `git fetch --deepen=N`

---

## Sparse Checkout

```bash
git sparse-checkout init --cone
git sparse-checkout set frontend/ shared/
```

- Working tree contains only specified subdirectories
- Repo metadata is full; only files on disk are filtered
- `--cone` mode is faster and more predictable
- Great for "I only work on frontend" in a 10M-file repo
- Combine with partial clone for maximum speedup

---

## Sparse Checkout in Practice

- `git sparse-checkout add path/` — include a path
- `git sparse-checkout reapply` — rebuild after `.gitignore`-style file change
- `git sparse-checkout disable` — back to full checkout
- IDEs may need configuration to not search excluded paths
- Builds in monorepos are designed for partial trees

---

## Build Systems for Monorepos

- Bazel, Buck2, Pants — build only what changed
- Use a dependency graph to compute affected targets
- Cache aggressively: same inputs, same outputs
- Distributed builds: shared remote cache across the org
- Without a smart build, monorepo CI grinds to a halt

---

## CI for Monorepos

- Don't run every test on every PR — too slow, too expensive
- Compute affected targets from the diff
- Run tests only for changed and dependent code
- Required checks include "did you forget to mark this dependency?"
- Build cache hits on unchanged code save hours

---

## Code Ownership: CODEOWNERS

```output
/services/auth/      @auth-team
/services/payments/  @payments-team
/libs/shared/        @platform-team
*.proto              @api-council
```

- File at `.github/CODEOWNERS` (or platform equivalent)
- Auto-requests review from owning team
- Required reviews enforce ownership
- Critical for monorepos — otherwise nothing is anyone's problem

---

## Branching in Monorepos

- Trunk-based development is the dominant pattern
- Short-lived feature branches, frequent merges to main
- Long-lived branches don't scale — too much code drifting
- Release tags or release branches when needed
- The cost of a long branch grows with monorepo size

---

## Atomic Cross-Cutting Changes

- Rename a function used by 200 services in one PR
- Update a shared protobuf and all consumers together
- Couldn't do this with multi-repo without choreography
- The killer feature of monorepos
- Requires good test coverage to be safe

---

## Refactor Tools for Monorepos

- Code-mod tools: rewrite syntax across millions of files
- `gh-prefetcher`, `comby`, `ast-grep`, language-specific tools
- Reviewer tools that show "what kind of change is this" at scale
- Without these, large refactors are infeasible
- Tooling investment is part of the monorepo cost

---

## Hooks at Monorepo Scale

- Pre-commit hooks must be incremental — only check changed files
- Server hooks enforce repo-wide policy at push time
- Per-team policies via `core.hooksPath` overrides
- A 30-second hook in a monorepo blocks 100 developers
- Performance budgets are real engineering constraints

---

## Special Git Features for Scale

- File system monitor (FSMonitor) — speeds `git status` by trusting watchers
- Commit-graph file — speeds reachability and log queries
- Multi-pack index — efficient lookups across many packfiles
- Scalar (Microsoft) — preconfigured wrapper for these features
- Enable in `git config feature.manyFiles=true`

---

## Search at Scale

- `git grep` works but slows on huge trees
- Indexed code search (Hound, Sourcegraph, Livegrep) becomes essential
- Build a "code map" service for cross-references
- Developers grep less, query more
- Search infrastructure is a first-class monorepo investment

---

## Multi-Repo With Monorepo Workflows

- Some teams approximate monorepo via super-projects with submodules
- Trade-off: less atomicity, more familiar tooling
- Tools like Repo (Android) or ghorg manage many repos as one
- Works until you need a truly atomic change — then it doesn't
- Pick monorepo when you need its atomicity, not because it's fashionable

---

## Common Mistakes

- Going monorepo without investing in build/test tooling
- Letting binaries and generated files into the repo
- One CI job runs everything — death by minutes
- No CODEOWNERS — nobody enforces architecture
- Hoping `git` features alone will scale infinite repo growth

---

## When Monorepo Goes Wrong

- 30-minute clones, 5-minute `git status`
- CI takes hours and fails on unrelated tests
- Reviewers can't keep up with cross-team PRs
- Reverting a bad commit reverts unrelated work
- These symptoms mean the *tooling* didn't scale, not git itself

---

## Best Practices

- Adopt monorepo with the tooling investment up front
- Sparse checkout and partial clone for everyday work
- Smart build systems that compute affected targets
- Strict CODEOWNERS and required reviews
- Strong CI with caching, sharding, and target-based test selection

---

## Summary

- Monorepo trades coordination for tooling complexity
- Git scales with effort: partial clone, sparse checkout, FSMonitor, commit-graph
- Build systems and CI must be monorepo-aware
- Atomic cross-cutting changes are the killer feature
- Don't go monorepo for fashion; go for the atomicity, then invest accordingly
