---
tags:
  - architecture:api-gateway
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Introduction to API Gateways

---
## What This Chapter Covers

- What an API gateway is
- Why one matters in microservices
- Single-purpose vs full-featured gateways
- Gateway-included responsibilities
- What gateways shouldn't do
- A short tour of the landscape

---
## What An API Gateway Is

- A single entry point in front of multiple services
- Clients call the gateway; the gateway routes to services
- The "front door" for your APIs
- Often the only thing exposed to the internet
- Inside the gateway: many services, all internal

---
## Why Bother

- Without it: clients call N services directly
- N changes &#8594; N client updates
- Gateway centralises: auth, rate limiting, logging, routing
- Services stay simple; gateway handles cross-cutting concerns
- Consumers see one API, even though many services back it

---
## Common Gateway Responsibilities

- Routing: URL &#8594; service mapping
- Authentication: who is the caller?
- Authorisation: what can they do?
- Rate limiting: how many requests / second?
- Caching: serve repeated requests fast
- Request / response transformation
- Logging, metrics, tracing

---
## Cross-Cutting Concerns

- Same logic that every service would need
- Implement once, in the gateway
- Each service trusts the gateway has done it
- Reduces duplication; improves consistency
- Trade-off: services become slightly less standalone

---
## What Gateways Shouldn't Do

- Business logic
- Service-specific data manipulation
- Long-running operations
- Heavy computation
- "If it took more than a few ms, the gateway shouldn't do it"

---
## Gateway vs Service Mesh

- **Gateway**: north-south traffic (external &#8596; internal)
- **Service mesh**: east-west traffic (service &#8596; service)
- Both add observability and policy
- Different tools (Kong vs Istio)
- Modern stacks often have both

---
## BFF Pattern

- Backend for Frontend
- One gateway per client type (web, mobile, partner)
- Each tailors the API to its consumer
- More complex than one gateway; better DX per client
- Common in customer-facing public APIs

---
## Edge vs Internal Gateways

- **Edge gateway**: at the internet boundary; SSL termination, WAF
- **Internal gateway**: between zones inside the company
- Different concerns (security depth, performance)
- Larger orgs have both
- Smaller: one gateway covers both

---
## Hosted vs Self-Hosted

- **Hosted**: AWS API Gateway, Azure API Management, Apigee
- **Self-hosted**: Kong, Tyk, Krakend
- **Cloud-native (serverless)**: AWS API Gateway native
- Pick by: cloud lock-in tolerance, operational capacity, feature requirements
- All capable for typical needs

---
## Gateway Landscape

- **Kong**: open-source, plugin-rich, well-known
- **AWS API Gateway**: managed; tightly integrated with AWS
- **Apigee**: enterprise; expensive; powerful
- **Envoy**: high-performance proxy; building block
- **Traefik**: dynamic routing; cloud-native
- **Tyk**: open-source competitor to Kong

---
## When You DON'T Need One

- Single service; no microservices
- Internal-only API with one client
- Simple proxy can do (nginx, Caddy)
- Avoid premature complexity
- "Add a gateway when you have ~3+ services and external consumers"

---
## What's Next

- Architectures: monolith with gateway, microservices, serverless
- Specific tools: Kong, AWS API Gateway
- Cross-cutting: rate limiting, auth, transformation, caching
- Observability: tracing, metrics, logging
