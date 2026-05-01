---
tags:
  - architecture:api
  - practices:governance
level: intermediate
category: architecture
audience:
  - audiences:architects
  - audiences:developers

---
# API Governance and Style Guides

---
## What This Chapter Covers

- What API governance is
- Style guides for APIs
- Spectral rules
- Review processes
- Cross-team consistency
- The trade-off between freedom and consistency

---
## Why Governance

- One company; many teams; many APIs
- Each team's API done differently &#8594; consumers struggle
- Errors look different; pagination looks different; auth looks different
- Governance keeps a baseline of consistency
- Without it: a fragmented API surface

---
## What To Standardise

- Naming: paths, fields, query params
- Errors: shape, status codes, error codes
- Pagination: pattern (cursor / offset)
- Authentication: bearer tokens, header names
- Versioning: scheme and policy
- Documentation: what's required (description, examples)

---
## What NOT To Standardise

- Business logic
- Domain models (each domain has its own shape)
- Implementation choices
- Aim for consistency where consumers see it
- Leave teams free where they don't

---
## A Style Guide

- A short document: "how we design APIs at $COMPANY"
- Live in a repo; reviewed and updated
- Linked from API design checklists
- Code examples (do this, not that)
- One source of truth

---
## Spectral For Enforcement

- OpenAPI linter
- Custom rules per organisation
- Run in CI
- Fail PRs that violate the style guide
- Automation beats meetings

---
## Sample Spectral Rules

```yaml
rules:
  paths-kebab-case:
    description: Paths should be kebab-case
    given: $.paths.*
    then:
      function: pattern
      functionOptions:
        match: ^(/[a-z0-9-]+)+$
  required-error-schema:
    given: $.paths.*.*.responses['4??','5??'].content.application/json.schema
    then:
      field: $ref
      function: defined
```

- Each rule has a description and a check
- Fails the build with a clear error

---
## Review Processes

- New APIs: design review before implementation
- Breaking changes: explicit approval
- Cross-team APIs: more scrutiny
- Reviewers: senior engineers, API owner, security
- Lightweight is fine; rituals breed cynicism

---
## API Design Reviews

- 30-60 minute meeting
- Designer presents the OpenAPI spec
- Reviewers ask: consistency, evolution, security, performance
- Feedback in the spec PR (annotations)
- Async first; sync only when needed

---
## API Catalogues

- Internal directory of all APIs
- Each entry: name, owner, OpenAPI spec, docs link
- Tools: Backstage, Kong Konnect, custom
- Discoverability: stop reinventing
- Especially valuable at companies with many teams

---
## Producer-Consumer Relationships

- Document who consumes each API
- Avoids surprise breaks
- Pact / consumer registries help
- Inventory of "if I change X, who do I need to tell"
- Critical for safe deprecations

---
## Versioning Policy

- Maximum supported versions (often 2: current + previous)
- Minimum support window (e.g., 12 months)
- Deprecation notice period (e.g., 6 months)
- Communication channels
- Set policy; enforce; don't surprise consumers

---
## Security Standards

- Authentication: which mechanisms allowed
- Authorisation: how to express
- Required headers (CORS, rate-limiting)
- TLS minimum version
- Standard 401/403 responses

---
## Performance Standards

- Latency targets (p50, p99)
- Rate-limit headers
- Pagination max page size
- Long operations: async patterns (202 + status endpoint)
- Performance is part of the contract

---
## Centralised Tooling

- One blessed Spectral config
- Shared OpenAPI templates
- Shared client SDK generators
- Shared docs renderer
- Reduces variance; standardises onboarding

---
## Common Governance Mistakes

- Heavyweight process; nothing ships
- No process; chaos
- Style guide that's never updated
- Reviewers as gatekeepers (block without explaining)
- Governance as bureaucracy instead of enablement

---
## Course Wrap-Up

- API-first means design before implementation
- OpenAPI is the contract; tooling derives from it
- Best practices: REST conventions, error shapes, pagination, idempotency
- Code generation, mock servers, contract testing
- Versioning carefully; documentation seriously
- Governance keeps the surface coherent across teams
- Done well: APIs become a competitive advantage
