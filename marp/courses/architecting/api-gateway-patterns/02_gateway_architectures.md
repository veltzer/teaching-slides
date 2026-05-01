---
tags:
  - architecture:api-gateway
level: intermediate
category: architecture
audience:
  - audiences:architects

---
# Gateway Architectures

---
## What This Chapter Covers

- Monolith + gateway
- Microservices + gateway
- BFF (Backend For Frontend)
- Multi-region gateways
- Sidecar gateways (service mesh)
- Architecture trade-offs

---
## Monolith + Gateway

- A single backend; gateway in front
- Reasons: SSL termination, WAF, rate limiting, caching
- Lightweight gateway is enough
- Don't need full-featured (no routing complexity)
- nginx + a few Lua scripts often suffices

---
## Microservices + Gateway

- The classic case
- Many services; one entry point
- Routing: URL prefix &#8594; service
- Cross-cutting concerns at the gateway
- Standard pattern in cloud-native architectures

---
## BFF (Backend for Frontend)

- Per-client gateway
- Web BFF: tuned for the web app
- Mobile BFF: optimised for mobile (smaller payloads, fewer round-trips)
- Partner BFF: different auth, different shapes
- More gateways; better client experience

---
## When BFF Wins

- Different clients have very different needs
- Web vs mobile: latency-sensitive vs payload-sensitive
- Public vs partner: very different auth and SLAs
- Each BFF can evolve independently
- Trade-off: more services to maintain

---
## Multi-Region

- Gateway in each region
- Route by client geography (latency)
- DNS-based: GeoDNS, Anycast
- Failover: traffic redirects on regional outage
- Standard for global services

---
## Active-Active Multi-Region

- All regions serve traffic simultaneously
- Eventually consistent backend (or sticky-session per region)
- Highest availability
- Complexity: data replication, conflict resolution
- Pay the cost; reap the resilience

---
## Active-Passive

- Primary region serves; secondary on standby
- Failover triggered manually or automatically
- Simpler than active-active
- RTO (recovery time): minutes, not seconds
- Adequate for many use cases

---
## Sidecar / Service Mesh

- Each service has a sidecar proxy
- Sidecars handle: mTLS, retry, circuit-breaker, telemetry
- Centralised gateway for north-south; sidecar for east-west
- Tools: Istio, Linkerd, Consul Connect
- Complementary, not replacement

---
## Gateway Inside Kubernetes

- Ingress controllers: NGINX Ingress, Traefik, Kong, Contour
- Manage external traffic into the cluster
- Configure via Kubernetes manifests (Ingress, IngressRoute)
- The Kubernetes-native pattern
- Often combined with a service mesh

---
## Single Gateway vs Multiple

- One gateway: simpler operations, single point of (failure / config)
- Many gateways: BFF model; per-team
- Pick by team structure and traffic shape
- Conway's Law applies

---
## Trade-Offs

- Gateway complexity vs service simplicity
- Centralised control vs team autonomy
- Operational burden vs developer productivity
- Cost: hosted is high; self-hosted needs ops
- No free lunch

---
## A Decision Framework

- 1 service: nginx is fine
- 3-10 services: a single API gateway
- Multiple client types: BFF
- Multi-region: gateway per region + DNS
- Many languages, deep observability: + service mesh

---
## Common Architectural Mistakes

- "We need a gateway" before having services to gateway
- Gateway as a god-component (business logic creeps in)
- One gateway when BFFs would help
- BFFs everywhere when one would do
- Gateway and mesh duplicating responsibilities
