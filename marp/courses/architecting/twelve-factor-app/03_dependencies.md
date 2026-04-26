---
tags:
  - concepts:architecture
  - concepts:best-practices
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# Factor II: Dependencies

---
## The Rule

- Explicitly declare and isolate dependencies
- Never rely on implicit system-wide packages
- The dependency manifest is part of the codebase

---
## Explicit Declaration

- Every dependency the app needs is named in a manifest
- Examples: `requirements.txt`, `package.json`, `go.mod`, `pom.xml`, `Cargo.toml`
- A new clone of the repo plus the manifest is enough to install everything
- Implicit "the OS has it" dependencies are forbidden

---
## Lock Files

- A manifest specifies what; a lock file specifies which exact version
- Examples: `package-lock.json`, `poetry.lock`, `go.sum`, `Cargo.lock`
- Commits the resolved tree of versions
- Reproducible installs across time and machines

---
## Isolation

- The app's dependencies do not leak into the system or each other
- Achieved with virtual environments (Python venv), node_modules (npm), Cargo workspaces
- A second app on the same machine must not see this app's dependencies
- Containers enforce this naturally

---
## Why Isolation Matters

- Prevents "works on my laptop" caused by global packages
- Lets you upgrade dependencies for one app without breaking another
- Lets you delete the app cleanly — no system pollution
- The container model assumes this isolation; it builds on it

---
## Vendoring vs Package Managers

- **Package manager**: declares what's needed; resolves at install time
- **Vendoring**: copies all dependencies into the codebase
- Vendoring trades repo size for build determinism and air-gapped builds
- Most projects use a package manager + lock file; vendoring is for special cases

---
## When to Vendor

- Air-gapped or restricted environments without registry access
- Long-term archival projects (10+ years)
- Reproducibility requirements that exceed lock file guarantees
- Dependencies on packages with unstable upstream

---
## Anti-Patterns

- "It just works because Python 3.10 is on the system" — relies on global state
- Manifest without a lock file — installs drift over time
- "Install Java 8 separately, then run the app" — implicit OS dependency
- `apt-get install` in the README, no Dockerfile — leaks into the OS

---
## Container as Isolation

- A Dockerfile is a manifest at the OS level
- It declares OS packages, language runtime, and app dependencies
- The image is the lock file equivalent at the OS level
- Containerized apps that violate factor II are rare; containers enforce it

---
## Verifying Compliance

- Can a developer clone the repo and `make install` (or equivalent) without manual steps?
- Are lock files committed?
- Does the CI build start from a clean slate every time?
- Are dependency upgrades a single PR with a diff in manifest + lock?

---
## Summary

- Declare every dependency in a manifest
- Lock to specific versions
- Isolate from the system and from other apps
- Containers enforce factor II naturally
- Implicit dependencies are tomorrow's debugging session
