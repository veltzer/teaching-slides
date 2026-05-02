---
tags:
  - architecture:api
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Introduction to API-First Design

---
## What This Chapter Covers

- What API-first means
- API-first vs code-first
- Benefits and parallel development
- The contract as a communication tool
- The workflow at a high level
- Common adoption challenges

---
## API-First Workflow

![api_first_flow](svg/courses/architecting/api-first-development/01_introduction_to_api_first_design/api_first_flow.svg)

---
## What API-First Means

- Design the API *before* writing the implementation
- The API contract (an OpenAPI document) is the source of truth
- Implementation and consumers both work *from* the contract
- Contract gets reviewed and agreed before code is written
- The opposite of code-first ("ship code; doc it later")

---
## Code-First vs API-First

- **Code-first**: implementation defines the API; doc is generated after
- **API-first**: contract defines the API; implementation matches it
- Code-first is faster early, painful later
- API-first is slower early, faster long-term
- Most modern teams converge to API-first as they scale

---
## Benefits

- Frontend / mobile teams can start *immediately* against the contract
- Backend builds against the same contract
- Mock servers fill the gap before backend exists
- Contract diffs reveal breaking changes
- Clearer ownership of the API surface

---
## The Contract As Communication

- OpenAPI document is the canonical agreement
- Reviewers can see exactly what's being built
- Stakeholders can read it (with renderers like Swagger UI)
- Lives in version control; diffs for every change
- Replaces hand-written API docs that always go stale

---
## The Workflow

- Designers / architects draft the OpenAPI spec
- Reviewers (consumers, tech leads) provide feedback
- Spec is approved
- Backend generates server stubs; frontend generates client SDKs
- Mock server runs; consumers integrate against it
- Backend implements; CI verifies it matches the spec

---
## API As A Product

- Treat the API like any product: users, journeys, evolution
- Care about developer experience: error messages, examples, docs
- Versioning policies users can rely on
- Backward compatibility unless absolutely necessary
- "Customer-zero" mindset: dogfood your own API

---
## Common Challenges

- Engineers used to code-first feel slowed down at first
- Specs go stale if not enforced in CI
- Tooling learning curve (OpenAPI, generators, Spectral)
- Stakeholders without OpenAPI literacy struggle to review
- Initial investment is real; pays back over a year

---
## Adoption Strategies

- Start with one new API; not "rewrite everything"
- Pick a champion to maintain the spec quality
- Set CI gates: spec must be valid; code must conform
- Train one or two engineers; they teach the rest
- Write a short style guide

---
## Tools You'll Use

- **Swagger Editor / Stoplight Studio**: write specs visually
- **OpenAPI Generator**: generate server stubs and client SDKs
- **Prism**: mock server from OpenAPI spec
- **Pact**: consumer-driven contract testing
- **Spectral**: lint OpenAPI specs

---
## What's Next

- OpenAPI 3.x in detail
- API design best practices (REST, errors, pagination)
- Code generation
- Mock servers and contract testing
- Versioning strategies
- Documentation tools and governance

---
## When NOT API-First

- One-off internal scripts
- Throwaway prototypes
- Very early-stage product (you don't know what the API is yet)
- Non-API code (tasks, jobs, batch processing)
- Match the discipline to the longevity of the API

---
## Common Mistakes

- API-first as a slogan; specs that drift from code
- No CI to enforce spec compliance
- Specs designed without consumer input
- Ignoring developer experience (no examples, terse errors)
- Treating the spec as final; never updating
