---
tags:
  - concepts:microservices
  - concepts:distributed-systems
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:devops

---
# Service Discovery

---
## The Problem

- Service A wants to call service B
- B has multiple instances at varying IPs
- Instances come and go (deploys, autoscaling, failures)
- A needs to find current B instances at any time

---
## Discovery Modes

![discovery_modes](svg/courses/architecting/microservices-architecture/08_service_discovery/discovery_modes.svg)

---
## Static Configuration

- A's config has B's URL: `http://b.example.com`
- DNS resolves to current B instances
- Simplest; works for most cases
- Requires DNS to be up to date

---
## Client-Side Discovery

- A queries a registry to find B's instances
- A picks one (load balancing logic in A)
- A makes the call directly
- Examples: Eureka, Consul + client SDK

---
## Server-Side Discovery

- A calls a load balancer or service proxy
- The proxy queries the registry and routes
- A doesn't need any discovery logic
- Examples: Kubernetes Service objects, AWS ELB

---
## Kubernetes Service Discovery

- Each Service object gets a stable DNS name
- DNS resolves to a virtual IP that load balances to pods
- The pod set changes; the Service name doesn't
- Handles registration and deregistration automatically

---
## Service Registry

- Central database of "service X has instances at these endpoints"
- Updates as instances start, stop, fail
- Examples: etcd, Consul, Zookeeper, Kubernetes API server
- Most platforms have one built in

---
## Health Checks

- Instances mark themselves healthy/unhealthy
- Discovery only returns healthy instances
- Implementations: HTTP probe, TCP probe, custom command
- Crucial: an unhealthy instance must be removed from rotation quickly

---
## Health vs Readiness

- **Liveness**: is the process alive? (restart if not)
- **Readiness**: is the process ready to serve traffic? (don't route if not)
- A starting instance is alive but not ready
- Distinguish them; misconfigured probes cause incidents

---
## Load Balancing

- Round-robin: simple, fair under uniform conditions
- Least connections: good for variable request durations
- Random: surprisingly effective at scale
- Latency-aware: routes to fastest healthy instance
- Most platforms default to round-robin or least connections

---
## Client Load Balancing

- The client picks an instance from the registry
- More flexible: client knows about retries, circuit breakers, latencies
- Less centralized: each client implements the logic
- Common in service mesh setups

---
## Service Mesh and Discovery

- Service mesh proxies handle discovery transparently
- Each service makes a "local" call; the mesh resolves and routes
- mTLS, retries, circuit breakers handled by the mesh
- Adds operational complexity but standardizes the cross-cutting concerns

---
## DNS-Based Discovery

- Simple: just DNS records that resolve to instance IPs
- Updates via DNS TTL
- Limitation: TTLs are coarse (seconds-minutes)
- Often combined with a load balancer for finer control

---
## Anti-Patterns

- Hardcoded IPs in config
- Long DNS TTLs that delay failure detection
- Discovery that requires manual update on each deploy
- No health checks; routing to dead instances
- Single point of failure in the registry

---
## Summary

- Multiple instances of each service; need a way to find them
- Client-side or server-side discovery; both work
- Kubernetes Services are the most common modern setup
- Health and readiness probes are mandatory
- Service mesh centralizes the concerns at the cost of complexity
