---
tags:
  - concepts:architecture
  - concepts:best-practices
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---

# Factor I: Codebase

---

## The Rule

- One codebase tracked in revision control
- Many deploys
- The same codebase produces every environment's deploy

---

## Mental Model

![one_repo_many_deploys](svg/courses/architecting/twelve-factor-app/02_codebase/one_repo_many_deploys.svg)

---

## What "One Codebase" Means

- A single git repository (or equivalent) per app
- Every deploy of that app traces back to this codebase
- A change made in code reaches every environment via the same path
- No "production branch" diverging from "the code" — only deploys differ

---

## What "Many Deploys" Means

- Production, staging, dev, per-developer, per-CI-job — all are deploys
- Each deploy is the same codebase plus some configuration
- Deploys differ in config and possibly version, never in source

---

## Codebase, App, Deploy

- **Codebase**: the source code in version control
- **App**: an instance of the codebase running somewhere
- **Deploy**: a specific running instance with its own config and state
- One codebase → one app → many deploys

---

## Multiple Apps Sharing Code

- Sharing code via a shared codebase across apps violates the factor
- Extract shared code to a library; depend on it as a dependency (factor 2)
- Each app has its own codebase

---

## Repository Topologies

![repo_topologies](svg/courses/architecting/twelve-factor-app/02_codebase/repo_topologies.svg)

---

## Monorepo Considerations

- A monorepo can hold multiple codebases — that's fine
- Each codebase within the monorepo is its own app
- The discipline: if it deploys separately, it has its own build, lock file, and history within the monorepo
- Monorepo is an organizational choice, not a violation

---

## Multi-Repo Considerations

- One repo per app is the canonical interpretation
- Easier to enforce factor I; harder to share code without a package registry
- Either approach works; pick one and be consistent

---

## Anti-Patterns

- "Production has special files" — versioning skew between environments
- "Live edit on the server" — production has no traceable origin
- "Dev only branch" that never merges — environments diverge silently
- "Code shared between apps via copy-paste" — bug fixes don't propagate

---

## Verifying Compliance

- Can you redeploy any environment from the codebase plus its config?
- Can you reproduce any past deploy from a tag and config snapshot?
- Are dev, staging, prod the same code with different configs?
- If yes to all three, you're compliant with factor I

---

## Summary

- One codebase per app, in version control
- Many deploys come from the same codebase
- Differences between environments live in config, never in source
- Multi-repo or monorepo both work; consistency is what matters
