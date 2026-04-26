---
tags:
  - concepts:microservices
  - concepts:api
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# API Design for Microservices

---
## What's Different About Microservice APIs

- Internal APIs serve other services, not end users
- Volume is higher; latency tolerance is lower
- Schema discipline matters more — consumers are other code, not browsers
- See the API Design Best Practices course for the general principles

---
## Internal vs External APIs

- External: public, versioned carefully, documented for outsiders
- Internal: between known services; can evolve more freely
- Both still need contracts; internal "freer" doesn't mean unstructured

---
## Contract First

- Write the API spec before the implementation
- OpenAPI for HTTP; protobuf for gRPC
- Both producer and consumer build against the spec
- Mocks come from the spec for parallel work

---
## Versioning Internally

- Internal APIs change more often than external
- Backward-compatible changes need no version bump
- Breaking changes still need versioning
- Roll out producers before consumers, or vice versa, depending on direction

---
## Idempotency

- Every state-changing endpoint should accept an idempotency key
- Retries are inevitable; without idempotency they cause damage
- This is non-negotiable for any production microservice

---
## Authentication Between Services

- mTLS: mutual TLS; each service has its own cert
- JWT: a service-to-service token signed by an internal CA
- Service mesh: handles mTLS uniformly
- Don't roll your own; use a standard

---
## Authorization Between Services

- Even internal calls need auth: "is service A allowed to call service B?"
- Per-method policies in a service mesh
- Or: every call carries the original user's identity, services check
- Defense in depth: don't trust internal callers blindly

---
## Pagination, Filtering, Sorting

- Same as external APIs (cursor pagination, etc.)
- Internal services often have higher data volumes — pagination is even more important
- Don't expose unbounded lists to internal callers either

---
## Error Handling

- Same principles as external APIs
- Consistent error format across all services
- Distinct error codes for retryable vs permanent failures
- Help the caller decide what to do

---
## Documentation

- OpenAPI specs in the repo
- Per-service documentation portal (or one for all services)
- A consumer should be able to integrate without talking to the producer team
- Self-service is the goal

---
## Anti-Patterns

- Internal APIs without specs ("we'll just call the producer's tech lead")
- Different error formats per service
- Inconsistent auth schemes across services
- "Internal so we don't need versioning" — wrong
- "Internal so we don't need rate limits" — also wrong

---
## Summary

- Internal APIs follow the same principles as external ones, with more room to evolve
- Contract-first development; OpenAPI or protobuf
- Idempotency, authn/authz, consistent error handling — all mandatory
- For depth, see the API Design Best Practices course
