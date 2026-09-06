---
tags:
  - concepts:architecture
  - concepts:api-design
  - concepts:contracts
level: advanced
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---

# API Design

---

## Why API Design Is Architectural

- APIs are the externally visible contracts of every service
- A bad API is harder to fix than a bad internal implementation — clients depend on it
- Architects set API standards once and save every team a year of rediscovery
- Service boundaries are defined by APIs, not by code directories

---

## API-First Development

- Design the API before writing the implementation
- Review the spec with consumers and domain experts
- Generate server stubs and client SDKs from the spec
- Implementation follows a frozen contract, not the other way around

---

## API-First Benefits

- Parallel work — frontend and backend teams start simultaneously
- Testable contract — mock servers from the spec
- Machine-readable — generate SDKs, docs, and tests
- Versionable — the spec itself is versioned in Git

---

## Contract-First for Synchronous APIs

- **OpenAPI** (formerly Swagger) — the de facto standard for REST APIs
- Describes paths, methods, parameters, request/response schemas
- Tooling: `Swagger UI`, `Redoc`, `openapi-generator`, `Spectral` (linting)
- Validate every implementation against the spec in CI

---

## OpenAPI Example

```yaml
openapi: 3.1.0
info: { title: Orders API, version: 1.0.0 }
paths:
  /orders/{id}:
    get:
      parameters:
        - name: id
          in: path
          required: true
          schema: { type: string }
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Order' }
```

---

## Contract-First for Async APIs

- **AsyncAPI** — the OpenAPI analog for event-driven and message-based APIs
- Describes channels (topics/queues), message schemas, bindings (Kafka, AMQP, MQTT)
- Fills the gap left by OpenAPI, which only covers request/response
- Same benefits: generated SDKs, validation, testable contracts

---

## AsyncAPI Example

```yaml
asyncapi: 3.0.0
info: { title: Orders Events, version: 1.0.0 }
channels:
  order.placed:
    address: orders.placed
    messages:
      placed:
        payload:
          type: object
          properties:
            orderId: { type: string }
            amount:  { type: number }
```

---

## Versioning: The Three Common Strategies

- **URI path** — `/v1/orders`, `/v2/orders`
    - Pro: visible, cacheable; Con: duplicates every URL
- **Header** — `Accept: application/vnd.api.v2+json`
    - Pro: clean URLs; Con: harder to test in a browser, caching subtleties
- **Query parameter** — `/orders?version=2`
    - Pro: trivial to try; Con: sprays versioning across codebases

Pick one convention organization-wide.

---

## Breaking vs Non-Breaking Changes

- **Safe (non-breaking)** — adding optional fields, new endpoints, new enum values *if consumers handle unknowns*
- **Breaking** — removing fields, renaming fields, tightening validation, changing types, changing semantics
- Most fights about versioning are really fights about whether a change is breaking

---

## Evolving an API Without Breaking

- **Expand-then-contract** — add the new form alongside the old; migrate consumers; remove the old
- **Tolerant readers** — clients ignore unknown fields; servers accept missing optional fields
- **Deprecation headers** — `Deprecation: <date>` and `Sunset: <date>` per RFC 8594
- **Version aliases** — serve `/v1` as a translation layer over the `/v2` implementation

---

## Deprecation Process

- Announce deprecation with a sunset date at least 6 months out
- Emit `Deprecation` and `Sunset` headers on every response
- Monitor per-consumer usage and reach out to stragglers
- Remove the old API after confirmed zero usage — not on schedule alone

---

## REST Revisited

- Still the right default for resource-oriented CRUD
- Use nouns, standard HTTP methods, correct status codes
- Hypermedia (HATEOAS) is valuable in exactly three cases and hurts elsewhere
- Pagination: use opaque cursors, not integer offsets, for mutable collections

---

## When REST Is Not the Answer

- High-throughput internal RPC — prefer gRPC with Protocol Buffers
- Client picks the fields — GraphQL
- Long-lived streams — Server-Sent Events or WebSockets
- Fire-and-forget events — an event bus (Kafka, NATS, SNS)
- Files and large blobs — direct object-storage URLs (S3 presigned)

---

## GraphQL

- Single endpoint; clients specify exactly the fields they need
- Strong typed schema, introspectable
- Avoids over-fetching and under-fetching
- Tooling is excellent: codegen, IDE integration, schema registries

---

## GraphQL Trade-Offs

- **Pros**: flexible queries, strong typing, single round trip for nested data
- **Cons**: N+1 queries without DataLoader, caching is harder (no URL-per-resource), authorization is per-field
- **Federation** — stitch multiple GraphQL services behind one gateway; powerful but operationally heavy

---

## gRPC in Context

- Binary protocol over HTTP/2
- Code generation from `.proto` files for many languages
- Great for internal service-to-service; poor for browser clients without a proxy
- Forces contract-first by construction — schema is the source of truth

---

## Consumer-Driven Contract Testing

- Each consumer declares the contract it expects from the provider
- The provider runs those contracts as tests in its own CI
- Catches breaking changes at the provider's CI, not at runtime in staging
- Tools: `Pact`, `Spring Cloud Contract`

---

## Contract Test Flow

- Consumer writes test: "I expect GET /orders/42 to return `{ id, total }`"
- Pact broker stores the contract
- Provider CI pulls all consumer contracts and runs them against the real service
- Breaking changes fail the provider's build before deploy

---

## Pagination Patterns

| Pattern | Good for | Avoid when |
|---------|----------|-----------|
| Offset/limit | Small static collections | Large or mutable collections |
| Cursor (opaque) | Mutable, large, sorted collections | Random-access UIs |
| Keyset (seek) | Known-column sorts | Complex dynamic filters |
| Token-based | Any streaming case | Simple back-and-forth UIs |

Opaque cursor is the safe default.

---

## Idempotency and Safe Retries

- Make mutations idempotent — accept an `Idempotency-Key` header on POSTs
- Server stores the key → response mapping for a window (24h typical)
- Same key replay returns the same result; no duplicate charges
- Stripe popularized the pattern; now a standard expectation for commerce APIs

---

## Rate Limiting Conventions

- Return `429 Too Many Requests` on limit exceeded
- Include `Retry-After` header
- Include rate-limit status on every response:
    - `X-RateLimit-Limit`
    - `X-RateLimit-Remaining`
    - `X-RateLimit-Reset`
- Document limits per endpoint class; do not hide them

---

## Error Response Design

- Use the **Problem Details for HTTP APIs** format (RFC 9457)

```json
{
  "type": "https://example.com/errors/insufficient-balance",
  "title": "Insufficient Balance",
  "status": 402,
  "detail": "Your balance is $5; required $10",
  "instance": "/transactions/123"
}
```

- Stable `type` URIs let clients branch on errors without parsing prose

---

## API Discoverability

- Publish specs to a developer portal (SwaggerHub, Readme, Backstage)
- Include examples, not just schemas
- Maintain a changelog per API
- Link every error response `type` to a live docs page

---

## API Governance

- Design review before implementation for every new API
- Automated linting (`Spectral`, `Vacuum`) in CI — reject specs that violate style rules
- Shared schema registry for common types (Money, Address, Timestamp)
- Deprecation policy enforced by tooling, not by memory

---

## Common Anti-Patterns

- **Verbs in URIs** — `/getOrder`, `/updateUser`; use HTTP methods
- **Returning 200 with an error body** — breaks every HTTP intermediary
- **Chatty interfaces** — one call per field; batch or expand
- **Exposing internal IDs** — use opaque external IDs that won't change on migration
- **No versioning plan** — the first breaking change turns into a migration project

---

## Summary

- APIs are architectural contracts — design them first, implement second
- OpenAPI for sync, AsyncAPI for async; both are contract-first
- Versioning is inevitable — pick a strategy organization-wide
- Consumer-driven contract tests catch breakage at provider CI
- Use Problem Details for errors, opaque cursors for pagination, idempotency keys for POSTs
- REST is the default; pick gRPC, GraphQL, or streams only when REST cannot carry the load
- API governance belongs in CI, not in a wiki page
