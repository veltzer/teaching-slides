---
tags:
  - networking:graphql
level: intermediate
category: networking
audience:
  - audiences:developers

---

# Servers

---

## What This Chapter Covers

- Server landscape
- Apollo Server
- GraphQL Yoga
- Mercurius
- Schema-first vs code-first
- Tooling

---

## Server Landscape

- Apollo Server: Node, popular
- GraphQL Yoga: Node, simpler
- Mercurius: Fastify-based, fast
- Many language: graphql-go, graphene (Python), graphql-java

---

## Server Choices

![server_choices](svg/courses/networking/graphql/08_servers/server_choices.svg)

---

## Server Pipeline

![server_pipeline](svg/courses/networking/graphql/08_servers/server_pipeline.svg)

---

## Apollo Server

- Mature, large ecosystem
- Federation support
- Plugins, telemetry
- Standard

---

## Sample Apollo Server

```javascript
const server = new ApolloServer({
    typeDefs,
    resolvers
});
await server.listen({ port: 4000 });
```

- Schema + resolvers
- Express, Fastify, Lambda variants

---

## Yoga

- Lighter, less opinionated
- HTTP / WS by default
- Plugin model

---

## Schema-First

- SDL is source of truth
- Resolvers fill in
- Easy to read
- Standard

---

## Code-First

- Define types in code (decorators / classes)
- Generate schema
- Type-safe in code; one source
- Nexus, TypeGraphQL, Pothos

---

## Schema Stitching vs Federation

- Stitching: combine schemas at gateway
- Federation: typed, versioned subgraph composition
- Federation is the modern approach

---

## DataLoader

- Batches and caches per request
- Solves n+1
- Wrap data sources

---

## Validation Phase

- Parse query
- Validate against schema
- Reject before resolving
- Built-in

---

## Plugins / Middleware

- Logging
- Tracing
- Auth checks
- Caching

---

## Mocking

- Default values per type
- Bootstrap frontends without backend
- Built into Apollo

---

## Production Concerns

- Query complexity limits
- Depth limits
- Query allow-list
- Persisted queries

---

## Common Server Mistakes

- No depth or complexity limits; DoS risk
- N+1 queries without DataLoader
- Logic in resolvers instead of services
- Federation without ownership boundaries
- Returning internal error messages
