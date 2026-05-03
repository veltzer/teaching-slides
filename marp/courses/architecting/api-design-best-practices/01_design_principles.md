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
# API Design Principles

---
## What Makes a Good API

- Predictable: similar things look similar
- Consistent: same conventions throughout
- Discoverable: a well-named endpoint hints at related ones
- Documented: contracts are explicit
- Versioned: change is expected and managed
- Hard to misuse: defaults are safe

---
## Quality Pillars

![api_qualities](svg/courses/architecting/api-design-best-practices/01_design_principles/api_qualities.svg)

---
## API as a Product

- An API has consumers — users, even when those users are developers
- Every API decision is a UX decision
- Bad APIs are abandoned; good APIs grow ecosystems
- Think of consumers when you make decisions, not just implementers

---
## API-First Development

- Design the contract before writing code
- Producers and consumers can build in parallel against mocks
- Breaking changes are caught at design time, not runtime
- The API spec is the source of truth

---
## API-First Workflow

- Draft the API spec (OpenAPI, gRPC proto, GraphQL schema)
- Review with stakeholders
- Generate mocks; consumers build against them
- Implement the producer; verify against the spec
- Deploy with confidence that contracts are met

---
## API First Workflow

![api_first_workflow](svg/courses/architecting/api-design-best-practices/01_design_principles/api_first_workflow.svg)

---
## Consumer-Driven Design

- The consumer's needs shape the API, not the producer's internals
- "What does the consumer have to do to call you?" is the design question
- Avoid leaking implementation details into the contract
- Avoid forcing the consumer to understand your domain to use it

---
## The Principle of Least Surprise

- Names mean what they look like they mean
- Behaviors match common conventions
- Errors are descriptive
- "What does this do?" should be answerable from the signature alone

---
## Consistency Across the API

- One naming convention: snake_case or camelCase, pick one
- One pagination model
- One error format
- One date/time format (ISO 8601, with timezone)
- Consistency is more important than which convention you pick

---
## Consistency Dimensions

![consistency_dimensions](svg/courses/architecting/api-design-best-practices/01_design_principles/consistency_dimensions.svg)

---
## Discoverability

- A good URL hints at what's nearby
- `/users/42/orders` suggests `/users/42/orders/123`
- The schema describes what fields exist
- Hypermedia (HATEOAS) embeds links — but is rarely worth the cost in practice

---
## Versioning Awareness From Day One

- Don't ship `v1` and hope to never make a breaking change
- Plan for change; version explicitly
- We cover versioning in chapter 4

---
## Security by Default

- Authentication is required, not optional
- Authorization checks happen on the server, not the client
- Sensitive data is filtered from responses
- We cover this in chapter 9

---
## Anti-Patterns

- "RPC over HTTP" disguised as REST
- Verbs in URLs: `/getUserById?id=42`
- Inconsistent naming: `/users` and `/Order`
- Returning 200 OK with `{"error": ...}`
- "Internal" details exposed: `/sql_users_table_v3`

---
## Summary

- An API is a contract, a product, and a UX surface
- Predictability, consistency, discoverability are the goals
- API-first development makes the contract explicit
- Consistency beats cleverness
- Plan for change before you need to
