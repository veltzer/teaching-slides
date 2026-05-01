---
tags:
  - networking:graphql
level: intermediate
category: networking
audience:
  - audiences:developers

---
# Introduction to GraphQL

---
## What This Chapter Covers

- What GraphQL is
- Origin
- Comparison with REST
- Core ideas
- Adoption

---
## What GraphQL Is

- Query language for APIs
- Runtime for executing queries
- Strongly typed schema
- Single endpoint, one POST per request

---
## Origin

- Built at Facebook, 2012
- Open-sourced 2015
- Now: GraphQL Foundation
- Used by Shopify, GitHub, Netflix, others

---
## REST vs GraphQL

- REST: many endpoints, server-defined shape
- GraphQL: one endpoint, client-defined shape
- REST: over- and under-fetch
- GraphQL: ask for what you need

---
## The Hello Query

```graphql
query {
    user(id: "123") {
        name
        email
    }
}
```

- Returns exactly: name and email
- Nothing more

---
## Same Endpoint

- POST /graphql
- All queries to one URL
- Different queries return different shapes
- HTTP becomes a transport

---
## Schema

- Types, fields, queries, mutations
- Strongly typed
- Self-documenting
- Foundation of GraphQL

---
## Three Operations

- Query: read
- Mutation: write
- Subscription: live updates

---
## Why Adopted

- Mobile clients with bandwidth limits
- Frontend-driven shapes
- Microservice federation
- Generated typed clients

---
## Why Not Adopted

- Caching is harder
- Learning curve
- Server complexity
- REST often is enough

---
## Common Misconceptions

- "Replaces REST": no, choose by fit
- "Faster": depends on resolver design
- "Simpler": shifts complexity to server
- "No need for versioning": still need to deprecate

---
## Common Introduction Mistakes

- Adopting GraphQL because it is trendy
- Treating it as a pure protocol; ignoring schema design
- Expecting REST patterns (caching, status codes) to apply directly
- Not understanding the n+1 risk before going to production
