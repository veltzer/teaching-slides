---
tags:
  - architecture:api
  - architecture:rest
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# API Design Best Practices

---
## What This Chapter Covers

- Resource modelling
- HTTP method semantics
- Naming conventions
- Error responses (RFC 7807)
- Pagination patterns
- Filtering and sorting
- Idempotency
- HATEOAS

---
## Four Design Principles

![design_principles](svg/courses/architecting/api-first-development/03_api_design_best_practices/design_principles.svg)

---
## Resource Modelling

- Nouns, not verbs: `/users`, `/orders`, not `/getUsers`
- Collections (`/users`) and items (`/users/{id}`)
- Sub-resources: `/users/{id}/orders`
- Avoid deep nesting beyond 2 levels
- Consistent across the API

---
## HTTP Method Semantics

- **GET**: read, idempotent, safe
- **POST**: create, may have side effects
- **PUT**: replace; idempotent
- **PATCH**: partial update; not necessarily idempotent
- **DELETE**: remove; idempotent
- Match semantics, not just verbs

---
## Naming Conventions

- Plural nouns for collections: `/users`, `/orders`
- Lowercase, hyphenated paths: `/order-items`
- snake_case or camelCase for JSON properties (pick one)
- Avoid: file extensions in paths (`/users.json`)
- Avoid: trailing slashes inconsistently

---
## Status Codes

- 2xx: success (200 OK, 201 Created, 204 No Content)
- 3xx: redirection (301, 302, 304)
- 4xx: client error (400, 401, 403, 404, 409, 422, 429)
- 5xx: server error (500, 503)
- Pick the right one; don't return 200 with `{success: false}`

---
## Error Response Format (RFC 7807)

```json
{
  "type": "https://example.com/errors/insufficient-funds",
  "title": "Insufficient funds",
  "status": 422,
  "detail": "Account ABC123 has $10; transfer would require $50",
  "instance": "/transfers/789"
}
```

- Standardised "Problem Details for HTTP APIs"
- Same shape across all errors
- Type URL identifies the error kind
- Detail is human-readable; type is machine-readable

---
## Pagination: Offset

```http
GET /orders?offset=20&limit=10
```

- Easy to implement
- Easy to misuse: deep pagination is slow
- "Page 50" requires the DB to skip 49 pages of data
- Fine for small data sets; bad for large

---
## Pagination: Cursor

```http
GET /orders?cursor=eyJpZCI6MTIz&limit=10
```

- The cursor is opaque to the client
- Server decodes: "items after this point"
- Constant-time pagination
- Doesn't suffer from offset's deep-page problem
- Slightly more complex client code

---
## Pagination: Keyset

```http
GET /orders?after_id=123&limit=10
```

- Like cursor but with a *meaningful* parameter
- Often the previous page's last ID
- Requires sorting by a unique-and-indexed column
- Best when results are stable and ordered

---
## Filtering, Sorting, Field Selection

- Filtering: `GET /users?status=active&role=admin`
- Sorting: `GET /users?sort=created_at:desc`
- Field selection: `GET /users?fields=id,name`
- Document the supported filters explicitly
- Don't auto-allow arbitrary filters (DB injection risk)

---
## Idempotency

- The same call produces the same result
- GET, PUT, DELETE: idempotent by definition
- POST, PATCH: only if you design for it
- Idempotency keys: client sends a unique ID with each request
- Server dedupes by the key

---
## Idempotency Keys In Practice

```http
POST /payments
Idempotency-Key: 47f8a2b9...
Content-Type: application/json

{ "amount": 100 }
```

- Server stores the response keyed by the idempotency key
- Same key in the next 24 hours &#8594; same response
- Stripe is the canonical example
- Critical for: payments, order creation, anything with side effects

---
## HATEOAS

- "Hypermedia As The Engine Of Application State"
- API responses include links to related resources
- "You can do these things next"
- Theoretical purity high; adoption mixed
- Add when consumers genuinely benefit; skip when they don't

---
## HATEOAS Example

```json
{
  "id": 42,
  "status": "pending",
  "_links": {
    "self": "/orders/42",
    "cancel": "/orders/42/cancel",
    "items": "/orders/42/items"
  }
}
```

- Discoverable
- Loose coupling between client and server URLs
- The cost: more bytes; some complexity in client code
- Levin Richardson Maturity Model level 3

---
## Versioning In Brief

- `/v1/users`, `/v2/users`: URL versioning (most common)
- `Accept: application/vnd.example.v2+json`: header versioning
- Query parameter: `?version=2` (rare)
- Pick one; stick with it
- Covered in detail later

---
## Common Design Mistakes

- Verbs in URLs (`/getUsers`, `/createOrder`)
- Inconsistent status codes
- Different error shapes for different endpoints
- Mixing snake_case and camelCase in JSON
- "Login" as a POST without idempotency considerations
