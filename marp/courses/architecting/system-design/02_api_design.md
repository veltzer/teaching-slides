---
tags:
  - architecture:system-design
  - architecture:api
level: intermediate
category: architecture
audience:
  - audiences:developers

---

# API Design

---

## What This Chapter Covers

- API styles
- REST vs RPC vs GraphQL
- Designing endpoints
- Versioning
- Authentication
- Documentation
- Choosing the right style

---

## API Styles

- REST: resource-oriented, HTTP
- gRPC: function calls, Protobuf
- GraphQL: query language for APIs
- WebSockets: persistent, bidirectional
- Each fits different needs

---

## Style Choices

![api_design_choices](svg/courses/architecting/system-design/02_api_design/api_design_choices.svg)

---

## Methods And Idempotency

![rest_idempotency](svg/courses/architecting/system-design/02_api_design/rest_idempotency.svg)

---

## REST

- Resources are nouns: `/users`, `/orders`
- HTTP methods: GET, POST, PUT, DELETE
- Stateless
- Cacheable
- Industry default

---

## gRPC

- Protocol buffers; binary; fast
- Strongly typed
- HTTP/2 streaming
- Best for: internal service-to-service
- Less browser-friendly

---

## GraphQL

- Single endpoint; client specifies fields
- Solves over-fetching / under-fetching
- Trade-off: caching is harder, complexity higher
- Best for: many clients with varied needs
- Apollo, Hasura ecosystems

---

## When To Use Each

- Public API for diverse clients: REST
- Internal between services: gRPC
- Rich client (mobile, SPA): GraphQL
- Real-time chat: WebSockets
- Don't pick by hype

---

## Designing Endpoints

- Nouns, not verbs
- Plural for collections
- Sub-resources for relationships: `/users/42/orders`
- Keep flat where possible
- Consistency is more important than purity

---

## Versioning

- URL: `/v1/users` (most common)
- Header: `Accept: application/vnd.x.v2+json`
- Make breaking changes rarely
- Deprecate before removing

---

## Authentication

- API keys: server-to-server
- JWT: stateless, signed tokens
- OAuth 2.0: delegated auth
- mTLS: certificate-based
- Document: how to auth, on every endpoint

---

## Pagination

- Always paginate list endpoints
- Cursor-based: better for large data
- Offset-based: simpler, slower at depth
- Include total count when cheap

---

## Errors

- HTTP status codes for category
- JSON body for detail (RFC 7807)
- Don't return 200 with `{success: false}`
- Document each error type

---

## Documentation

- OpenAPI spec for REST
- Protobuf for gRPC (self-documenting)
- Schema for GraphQL (introspectable)
- Auto-generate docs from spec
- Stale docs are worse than no docs

---

## Backward Compatibility

- Add fields freely
- Don't remove or rename
- Don't change types
- Don't tighten validation
- Most changes can be additive

---

## Common API Mistakes

- Verbs in URLs
- Mixing styles in one API
- No versioning
- Pagination missing
- Inconsistent error formats
