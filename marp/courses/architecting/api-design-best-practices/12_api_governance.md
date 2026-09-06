---
tags:
  - concepts:api
  - concepts:best-practices
level: intermediate
category: architecture
audience:
  - audiences:architects
  - audiences:developers

---

# API Governance

---

## What Governance Means

- A set of standards, processes, and tools that keep APIs consistent
- Not bureaucracy — guardrails
- The goal: every API across the organization feels like part of one design
- Important when more than a few teams ship APIs

---

## Why It Matters

- Without governance: each team invents its own conventions
- Result: 50 different error formats, 50 different pagination styles
- Consumer experience degrades; integration cost rises
- The cost is invisible until it isn't

---

## Governance Pillars

![governance_pillars](svg/courses/architecting/api-design-best-practices/12_api_governance/governance_pillars.svg)

---

## API Design Guidelines

- A document that specifies the standards
- Naming conventions, error format, versioning, pagination, etc.
- Living document, owned by an architecture group
- Public if possible — your guidelines are also a recruiting signal

---

## Sample Guidelines Coverage

- URL structure (lowercase, hyphens, plural nouns)
- Naming (snake_case JSON fields, ISO 8601 dates)
- HTTP status codes
- Error response format
- Pagination (cursor preferred)
- Authentication (OAuth 2.0)
- Versioning (URL-based)
- Documentation (OpenAPI required)

---

## Linting Tools

- **Spectral**: lint OpenAPI specs against rules
- **Vacuum**: linter for OpenAPI
- **Redocly CLI**: validation and linting
- Catch violations before review
- Run in CI; fail builds on violations

---

## API Review Process

- New APIs go through design review before implementation
- A small group of reviewers (architects, senior engineers)
- Checks: alignment with guidelines, consistency, edge cases
- Reviews are fast (30 minutes) and frequent — not gatekeeping

---

## What Reviews Look At

- Naming and resource modeling
- Error format and status codes
- Pagination, filtering, sorting
- Versioning approach
- Authentication and authorization
- Documentation quality

---

## Automated Validation

- CI runs the linter on every spec change
- Contract tests run on every implementation change
- Drift detection: the spec and the implementation match
- Manual review focuses on judgment, automation handles rules

---

## API Lifecycle Management

- Stages: design → implement → release → deprecate → sunset
- Each stage has clear entry and exit criteria
- The lifecycle is visible — anyone can see where any API is
- Forgotten APIs are caught early

---

## API Catalog

- A central registry of all APIs in the organization
- Each entry: owner, purpose, status, link to spec, link to docs
- Searchable by team or topic
- Tools: Backstage (Spotify), Postman API Network, internal portals

---

## Standards vs Autonomy

- Standardize what matters for consumers (naming, errors, auth)
- Leave teams autonomous on what doesn't (internal architecture, deployment)
- Too much governance: every change needs approval
- Too little: every consumer fights inconsistency

---

## API Maturity Levels

- Level 0: no governance — each team does its own thing
- Level 1: design guidelines exist; reviews are ad-hoc
- Level 2: linting in CI; reviews mandatory for new APIs
- Level 3: spec-first development; full lifecycle management
- Move up incrementally; don't try to skip levels

---

## Cultural Aspects

- Governance only works with developer buy-in
- Show the value: faster integration, fewer support tickets
- Punish violations only after teaching what's expected
- Architects should be helpers, not police

---

## Tooling Stack

- API spec format: OpenAPI 3
- Linter: Spectral or Vacuum
- Review: GitHub PR + checklist
- Catalog: Backstage or similar
- Mock server: Prism or Stoplight
- Contract testing: Pact

---

## When to Skip Governance

- A small team with a single API
- Internal tooling APIs nobody else uses
- Throwaway prototypes
- Don't impose governance on the wrong scale

---

## Course Recap

- API design is a contract with consumers
- REST, URL structure, versioning, pagination, errors — all design choices
- Auth, rate limiting, idempotency — production necessities
- Documentation is part of the API
- Backward compatibility and deprecation are processes, not features
- Governance keeps APIs consistent at scale

---

## Summary

- Governance = standards + reviews + tooling
- Lint to enforce; review to teach
- Maturity grows in stages
- The goal: APIs that feel like one product, not many
- Skip governance when it's not needed; embrace it when it is
