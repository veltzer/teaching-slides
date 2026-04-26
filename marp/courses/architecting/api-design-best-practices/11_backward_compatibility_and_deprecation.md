---
tags:
  - concepts:api
  - concepts:best-practices
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Backward Compatibility and Deprecation

---
## The Problem

- APIs change; consumers depend on specific behavior
- Breaking changes break consumers
- You can't always coordinate upgrades with consumers
- Need a process for change that respects existing users

---
## Additive Changes Are Safe

- Adding a new endpoint
- Adding a new optional parameter
- Adding a new field to a response
- Adding a new error code

Old consumers ignore what they don't know — these are non-breaking.

---
## Breaking Changes

- Removing or renaming a field
- Changing a field's type
- Changing the meaning of a status code
- Making an optional parameter required
- Changing default values that affect behavior
- Removing an endpoint

---
## The Robustness Principle

- "Be conservative in what you send, liberal in what you accept"
- Producers: don't send unnecessary data; format consistently
- Consumers: tolerate unknown fields; don't break on additions
- Both sides cooperate to keep the contract working

---
## Tolerant Readers

- Consumer code that ignores unknown fields
- Consumer code that doesn't fail on extra data
- Defensive parsing rather than strict schema enforcement
- This is why additive changes are safe: tolerant readers don't break

---
## Deprecation

- A signal that "this is going away; switch to X"
- Not a sudden removal — a window of warning
- Communicated through headers, docs, and direct outreach
- Followed by a sunset (actual removal)

---
## Deprecation Headers

- `Deprecation: true` — this endpoint is deprecated
- `Sunset: Sat, 01 Jul 2026 00:00:00 GMT` — when it goes away
- `Link: <https://api.example.com/v2/orders>; rel="successor-version"` — pointer to the new version
- Standard, machine-readable

---
## Deprecation Timeline

- T+0: announce deprecation; new consumers should use the new version
- T+30 days: send deprecation headers on every response
- T+90 days: notify all consumers directly
- T+180 days: sunset — old endpoint returns 410 Gone

Each org adjusts the timeline; the structure is similar.

---
## Versioning and Deprecation Together

- v1 is the current version
- v2 is added; both run in parallel
- After 6-12 months, v1 is deprecated
- After another 6-12 months, v1 is sunset
- At any time, only two major versions are live

---
## Sunset

- The actual removal of the deprecated functionality
- Should not be a surprise — every step has been signposted
- Returns 410 Gone (not 404) — communicates "this is intentionally gone"
- Often accompanied by a migration guide URL in the error body

---
## Communicating Changes

- API changelog (a public file or page)
- Email lists for major announcements
- Direct outreach to top consumers for breaking changes
- Status pages for incidents and planned removals

---
## Migration Guides

- Side-by-side examples: old request → new request
- What changed and why
- How to detect if your code is affected
- Common pitfalls during migration
- Make migration as easy as possible — your consumers' time matters

---
## Detecting Consumers Using Deprecated APIs

- Log every request to deprecated endpoints with consumer identifier
- Build a dashboard: who's still using v1?
- Reach out to those consumers directly
- Don't sunset until the dashboard is empty (or close)

---
## Anti-Patterns

- Silent breaking changes — "it just stopped working"
- Deprecation with no sunset — the deprecated code lives forever
- Sunset with no warning — angry consumers
- New version that doesn't fix the reason for the change
- "We'll deprecate it eventually" — eventually never comes

---
## When to Break

- Sometimes you have to (security, legal, fundamental redesign)
- Even then, follow the deprecation process if you can
- For unavoidable instant breaks: communicate early, often, broadly
- A breaking change without warning is a breach of contract

---
## Compatibility Across Implementations

- Same API spec across multiple servers (active-active, regional)
- Different versions of the same server might serve traffic during a deploy
- The contract must work across all of them
- Rolling deploys assume backward compatibility within a version

---
## Summary

- Additive changes are free; breaking changes need a new version
- Deprecate before sunset; communicate broadly
- Use Deprecation and Sunset headers
- Two live versions max; sunset old ones on a schedule
- Migration guides are part of the deprecation
