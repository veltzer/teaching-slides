---
tags:
  - networking:graphql
level: intermediate
category: networking
audience:
  - audiences:developers

---
# Federation

---
## What This Chapter Covers

- Why federation
- Subgraphs
- Gateway
- Entities and keys
- Migration paths

---
## Why Federation

- Single GraphQL API across services
- Each team owns its piece
- Composable schema
- Avoid monolith

---
## Subgraphs

- Each service: a subgraph
- Defines its types and resolvers
- Independent deploys

---
## Gateway

- Composes subgraphs into one schema
- Routes fields to owners
- Single endpoint to clients

---
## Entities

- Types shared across subgraphs
- Identified by keys
- Each subgraph extends with more fields

---
## Sample Subgraph A

```graphql
type User @key(fields: "id") {
    id: ID!
    name: String!
}
```

---
## Sample Subgraph B

```graphql
extend type User @key(fields: "id") {
    id: ID! @external
    orders: [Order!]!
}
```

- Adds orders to User
- Resolved from B's data

---
## How Composition Works

- Gateway plans query across subgraphs
- Calls owner of each field
- Stitches results

---
## Apollo Federation 2

- Improved over v1
- Better composition rules
- Standard now
- Most production setups use it

---
## Federation vs Stitching

- Stitching: ad-hoc, gateway maintained
- Federation: typed, owned by subgraphs
- Federation is the modern approach

---
## Migration Paths

- Start: single schema
- Split: services own pieces
- Add: gateway, federation
- Iterate

---
## Operational Concerns

- Schema registry: versioned, validated
- Schema checks in CI
- Deploy subgraphs independently

---
## Distributed Tracing

- Track query across subgraphs
- OpenTelemetry
- Find which subgraph is slow

---
## Versioning

- Subgraphs deploy independently
- Schema must compose
- Breaking changes blocked at registry

---
## When Federation Is Wrong

- Small team, small schema
- Single backend
- Latency-sensitive: more hops
- Start monolithic, federate later

---
## Common Federation Mistakes

- Federating too early
- Wrong ownership boundaries
- Breaking schema deploys without registry checks
- N+1 across subgraphs
- No tracing across services
