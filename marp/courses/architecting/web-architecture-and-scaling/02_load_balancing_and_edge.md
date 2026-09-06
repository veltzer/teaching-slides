---
tags:
  - architecting:patterns
  - practices:scalability
level: intermediate
category: architecting
audience:
  - audiences:architects

---

# Load Balancing and Edge

---

## What This Chapter Covers

- Load balancing layers
- Algorithms
- Health checks
- CDNs
- TLS termination

---

## Why Load Balance

- Spread requests across replicas
- Hide failures from clients
- Enable rolling deploys
- Required for horizontal scale

---

## L4 vs L7

- L4: TCP, fast, opaque
- L7: HTTP, smart, slower
- L7 enables routing by path or header
- Modern load balancers do both

---

## L4 vs L7 Visualized

![l4_l7_balancing](svg/courses/architecting/web-architecture-and-scaling/02_load_balancing_and_edge/l4_l7_balancing.svg)

---

## Algorithms

- Round robin
- Least connections
- Latency-based
- Hash-based for stickiness

---

## Health Checks

- Active probes
- Passive observation
- Mark unhealthy nodes
- Drain before removal

---

## Sticky Sessions

- Same client to same node
- Useful for in-memory state
- Hurts scaling and failover
- Prefer external session state

---

## Connection Reuse

- Keep-alive saves handshake cost
- Connection pools to backend
- Tune to backend capacity
- Watch for idle timeouts

---

## TLS Termination

- Often at the edge
- Backend may use plaintext or mTLS
- Certificate management is operational work
- Rotate before expiry

---

## CDN Basics

- Cache at the edge
- Closer to users
- Static assets first
- Dynamic responses with care

---

## Edge Layers

![edge_layers](svg/courses/architecting/web-architecture-and-scaling/02_load_balancing_and_edge/edge_layers.svg)

---

## Cache Keys

- URL plus headers
- Vary headers control duplication
- Personalization breaks cacheability
- Beware cookie pollution

---

## Edge Compute

- Run code at the edge
- A/B tests, simple personalization
- Limited runtime
- Watch cold starts

---

## DNS as a Balancer

- GeoDNS to nearest region
- Health-checked routing
- TTL drives convergence speed
- Pair with regional load balancers

---

## Anycast

- Same IP from many locations
- Routing chooses nearest
- Fast failover
- Common for DNS and CDN

---

## Common Load-Balancing Mistakes

- Sticky sessions everywhere
- No health checks
- TLS only at edge with sensitive data on plaintext backbone
- TTL too long for failover
- One algorithm for everything
