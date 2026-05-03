---
tags:
  - concepts:api
  - concepts:architecture
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# API Gateways

---
## What an API Gateway Does

- A single entry point in front of multiple backend services
- Routes requests to the right service
- Applies cross-cutting concerns (auth, logging, rate limiting) in one place
- Aggregates or transforms responses if needed

---
## Why Use One

- Without a gateway, every service implements: TLS, auth, rate limiting, logging
- With a gateway, those concerns are centralized
- Backends focus on business logic
- Operations have one place to look at incoming traffic

---
## Gateway Responsibilities Visualised

![gateway_responsibilities](svg/courses/architecting/api-design-best-practices/10_api_gateways/gateway_responsibilities.svg)

---
## Common Gateway Responsibilities

- Request routing (path → service)
- Authentication (validate tokens, inject identity)
- Rate limiting and quota
- Request/response transformation
- Logging, tracing, metrics
- TLS termination
- Compression
- CORS handling

---
## Routing

- Match the request path/host to a backend
- `/api/orders/*` → orders service
- `/api/users/*` → users service
- Configurable; reloads without restart in good gateways

---
## Authentication at the Gateway

- The gateway validates the token
- On success, injects identity into headers passed to the backend
- The backend trusts the identity claims (the gateway is the only entry)
- One implementation, applied to every service

---
## Rate Limiting at the Gateway

- Per-user, per-key, per-route limits
- Limits applied before the backend even sees the request
- Backend gets clean traffic; spikes are absorbed at the edge
- 429 + Retry-After at the gateway is the right pattern

---
## Cross-Cutting Concerns Diagram

![api_gateway](svg/courses/architecting/api-design-best-practices/10_api_gateways/api_gateway.svg)

---
## Popular Gateways

- **Kong**: open-source, plugin ecosystem
- **AWS API Gateway**: managed, deep AWS integration
- **NGINX / OpenResty**: configurable, fast
- **Envoy**: programmable, often used as a building block
- **Traefik**: Kubernetes-native, simple
- **Cloudflare**: edge gateway with global PoPs

---
## Gateway vs Load Balancer

- Load balancer: distributes traffic across instances of one service
- Gateway: routes traffic across many services and applies app-layer concerns
- Often combined: the gateway has load balancing built in

---
## BFF Pattern

- "Backend for Frontend"
- A gateway tailored to one client type (mobile, web, IoT)
- Aggregates responses, shapes data for the specific client
- A specialized API in front of a generic one

---
## Gateway Patterns

- **Aggregator**: one client request, multiple backend calls, single response
- **Translator**: client speaks REST, backend speaks gRPC (or vice versa)
- **Filter**: drops fields the client shouldn't see
- **Throttler**: stops bursts before they reach the backend

---
## Anti-Patterns

- **Smart gateway, dumb services**: business logic creeps into the gateway
- **Gateway lock-in**: vendor-specific features that block migration
- **No gateway at all**: every service reimplements auth and rate limiting
- **Gateway as a middleware monolith**: all 50 plugins enabled, slow

---
## Operational Considerations

- The gateway is a single point of failure — make it highly available
- Latency impact: every request hops through it; keep it fast
- Configuration management: gateway config is like code (versioned, reviewed)
- Observability: the gateway is the best place to measure overall traffic

---
## Internal vs External Gateways

- **External gateway**: faces the internet; high security, rate limits, auth
- **Internal gateway**: faces other services; simpler, focused on routing
- Some systems use both: outer gateway → internal mesh → service

---
## Service Mesh vs API Gateway

- **Gateway**: north-south traffic (clients to services)
- **Mesh**: east-west traffic (service to service)
- They overlap; some systems use one product for both
- Most production systems have both kinds of concerns

---
## Summary

- A gateway centralizes cross-cutting API concerns
- Routing, auth, rate limiting, observability all happen in one place
- Many products to choose from; the responsibility is consistent
- Gateway should be fast, simple, and not a place for business logic
