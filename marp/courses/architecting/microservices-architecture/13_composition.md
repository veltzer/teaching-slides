---
tags:
  - concepts:microservices
  - concepts:design-patterns
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Composition Patterns

---
## Composition Patterns

![composition_patterns](svg/courses/architecting/microservices-architecture/13_composition/composition_patterns.svg)

---
## What Composition Means

- A user request often needs data from multiple services
- "Who composes the response?" is the design question
- Several patterns; trade-offs between client, gateway, and aggregator

---
## API Gateway as Aggregator

- The gateway receives the request
- Calls multiple backend services
- Combines responses into one
- Returns to the client

---
## Backend for Frontend (BFF)

- A gateway tailored to one client type (mobile, web, partner)
- Aggregates and shapes data for that client
- Different BFFs may exist for different clients
- The BFF owns the client-specific composition

---
## Why BFF

- Mobile clients need small, focused responses (bandwidth)
- Web clients need larger, denormalized data
- Partner APIs may need yet another shape
- One BFF per client lets each be optimized

---
## Composition at the Client

- Client makes multiple calls; combines locally
- Each call is to a different service
- The client owns the workflow
- Can be brittle: many calls, complex logic in the client

---
## Composition at the Server (Aggregator)

- One service is the aggregator: it calls others, returns a unified response
- Less logic in the client
- Aggregator becomes a hot service
- Most production systems use this pattern

---
## Choreography vs Orchestration

- **Choreography**: services react to events; no central coordinator
- **Orchestration**: a coordinator drives the flow
- Same vocabulary as the saga pattern (separate course)
- Composition often uses orchestration; choreography is more for workflows

---
## GraphQL as a Composition Layer

- A single GraphQL endpoint
- Clients ask for exactly the fields they need
- The GraphQL server resolves each field, calling backends as needed
- Powerful but complex; not always the right answer

---
## Request Aggregation Patterns

- Parallel: call N services in parallel; combine results
- Sequential: each call depends on the previous
- Fan-out + reduce: call many services, aggregate in code
- Pick based on dependencies between the calls

---
## Caching Aggregated Responses

- The aggregated response can be cached at the gateway
- Cache key includes user identity, parameters, version
- TTL based on staleness tolerance
- Reduces load on backends; speeds up the client

---
## API Composition Anti-Pattern

- "We need data from 10 services for this one screen"
- Probably the boundaries are wrong
- Or the screen is asking too much
- Refactor: a dedicated read model that aggregates the data ahead of time

---
## CQRS as Composition

- A read model maintained by event subscribers
- Pre-aggregates data from multiple services
- Queries hit the read model; no real-time aggregation needed
- Trades freshness for read performance

---
## Composition and Failure

- An aggregated response fails if any backend fails
- Can the response be partial? "Cart loaded; recommendations failed"
- Decide per case: critical vs nice-to-have
- Failure handling in composition is a design decision

---
## Anti-Patterns

- A single composition layer that becomes a monolith
- Synchronous chains across many services for one request
- Client orchestrating complex workflows
- "Just call all the services and combine" without thinking about failure

---
## Summary

- Aggregation belongs at gateway, BFF, or aggregator service
- BFFs tailor the API per client
- GraphQL as a composition layer is powerful but complex
- CQRS read models pre-aggregate for performance
- Failure handling in composition is explicit, not accidental
