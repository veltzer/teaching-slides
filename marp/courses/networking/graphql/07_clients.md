---
tags:
  - networking:graphql
level: intermediate
category: networking
audience:
  - audiences:developers

---
# Clients

---
## What This Chapter Covers

- Client landscape
- Apollo Client
- Relay
- urql
- Codegen
- Caching

---
## Client Landscape

- Apollo Client: most popular
- Relay: Facebook's, advanced
- urql: lightweight
- Many language-specific

---
## What Clients Provide

- Query execution
- Caching
- Local state
- Optimistic updates
- React / framework integration

---
## Apollo Client

- Mature, large ecosystem
- React, Vue, Angular bindings
- Normalised cache
- DevTools

---
## Apollo Cache

- Normalise by `__typename` + id
- Updates one place; everywhere reflects
- Powerful but tricky

---
## Relay

- Designed with GraphQL servers
- Strict conventions: connections, node interface
- Compiler-driven
- Optimised for big apps

---
## urql

- Smaller, simpler
- Document or normalised cache
- Easier learning curve

---
## Code Generation

- Generate types from schema and queries
- TypeScript types
- Hooks per query
- Less runtime error

---
## Sample Codegen Hook

```typescript
const { data } = useGetUserQuery({ variables: { id } });
data?.user?.name; // typed
```

- Compile-time safety
- IDE autocomplete

---
## Cache Invalidation

- Refetch query
- Update cache directly
- Subscriptions to live-update

---
## Optimistic Updates

- Apply mutation result before server confirms
- Roll back on error
- Better perceived latency

---
## Local State

- Client-side fields in schema
- Same query model for local and remote
- Less context spread

---
## Persisted Queries

- Hash queries; send hash + variables
- Smaller payloads
- Allow-list at server: security
- Shared by many clients

---
## Common Client Mistakes

- Not using codegen; runtime errors
- Manual cache updates that drift
- Refetching everything after every mutation
- Storing JWTs in cache
- Mixing fetch policies inconsistently
