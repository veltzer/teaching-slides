---
tags:
  - practices:technical-writing
level: beginner
category: methodology
audience:
  - audiences:developers

---
# Document Types

---
## What This Chapter Covers

- READMEs
- API documentation
- Architecture Decision Records (ADRs)
- Runbooks and playbooks
- Tutorials and how-to guides
- Reference documentation
- Release notes and changelogs

---
## Different Docs, Different Jobs

- A README isn't a spec
- A tutorial isn't a reference
- A runbook isn't a design doc
- Confusing types is the most common doc failure
- Pick the right type for the job

---
## Four Doc Modes

![doc_modes](svg/courses/development_methodologies/technical-writing/03_document_types/diataxis.svg)

---
## The Diátaxis Framework

- Four kinds of docs:
    - **Tutorials**: learning-oriented (lessons)
    - **How-to guides**: task-oriented (recipes)
    - **Reference**: information-oriented (lookup)
    - **Explanation**: understanding-oriented (background)
- Each has a different shape
- Mixing them confuses readers

---
## READMEs

- The first thing readers see
- Should answer: what is this? why use it? how to start?
- 80% of READMEs do this badly
- Aim for under 500 lines
- Link to deeper docs for the rest

---
## What A README Should Contain

- One-line description
- "Why" and "for whom"
- Quick install
- Quickstart example (working code)
- Where to learn more
- Contributing guide link
- License

---
## API Documentation

- Reference for every public function/method
- Parameters, return values, errors, examples
- Auto-generated from source comments where possible
- Examples for *common* uses, not all uses
- Versioned alongside the code

---
## Architecture Decision Records (ADRs)

- A short document recording one decision
- Why we chose X over Y, in this context, at this time
- Lives in the repo: `docs/adr/`
- Numbered and immutable (write a new ADR to change a previous decision)
- Future engineers can answer "why is it this way?" in seconds

---
## A Sample ADR

```markdown
# ADR 0007: Use Postgres over MongoDB

Status: Accepted (2026-03-15)

## Context
We need a primary store for orders.

## Decision
Postgres.

## Consequences
- + Mature ecosystem, ACID guarantees
- + Team familiarity
- - JSON columns are less ergonomic
```

---
## Runbooks

- Step-by-step instructions for operating procedures
- "How to restart the cluster", "How to handle a paged alert"
- Used by on-call, possibly at 3 AM
- Tested by following them literally
- Each step a single action; no judgement required

---
## Runbook Anti-Patterns

- "Use your judgement" steps
- Out-of-date commands
- Assumes deep system knowledge
- Buried in wiki pages no one can find
- Not exercised regularly

---
## Tutorials

- Take the reader from zero to a working result
- Step-by-step, hand-holding, complete
- Working code examples that match the prose
- Not the place for advanced features
- Build confidence first; teach features later

---
## How-To Guides

- Solve a specific problem
- Assume basic familiarity
- Get to the answer fast
- "How do I add authentication?"
- Different from a tutorial: focused on a task, not learning

---
## Reference Documentation

- Comprehensive, alphabetised, searchable
- Each entry stands alone
- The encyclopaedia, not the textbook
- Auto-generated where feasible
- Brevity is a feature

---
## Release Notes / Changelogs

- What changed in this release
- For users, not developers
- Format: Added / Changed / Deprecated / Removed / Fixed / Security
- Keep a Changelog (keepachangelog.com) is the standard
- Customers actually read these — write them well

---
## A CHANGELOG.md Sample

```markdown
## [1.4.0] - 2026-05-01
### Added
- TLS 1.3 support
- Configurable connection timeout

### Fixed
- Memory leak in long-running connections (#234)

### Deprecated
- The `legacy_auth` parameter (will be removed in 2.0)
```

---
## Choosing the Right Type

- A user trying to learn &#8594; tutorial
- A user solving a specific problem &#8594; how-to
- A user looking up details &#8594; reference
- A user wanting context &#8594; explanation (or ADR)
- An on-caller in an incident &#8594; runbook
- A user upgrading &#8594; changelog

---
## Common Mistakes

- A README that's secretly a tutorial
- An ADR with no decision (just discussion)
- A reference that's incomplete (90% complete is 100% useless for the missing 10%)
- A runbook that's actually an essay
- All docs in one giant wiki page
