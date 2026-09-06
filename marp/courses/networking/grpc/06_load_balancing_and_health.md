---
tags:
  - networking:grpc
  - concepts:load-balancing
level: intermediate
category: networking
audience:
  - audiences:developers
  - audiences:devops

---

# Load Balancing, Service Discovery, and Health

---

## What This Chapter Covers

- Why HTTP/1 load balancers don't work well for gRPC
- Client-side load balancing
- Service discovery: DNS, mesh, registry
- The gRPC health checking protocol
- Server reflection

---

## The Long-Lived Connection Problem

- gRPC uses HTTP/2 with persistent connections
- L4 (TCP) load balancers pick a backend once
- All traffic for that connection sticks to one backend
- Result: uneven load, no rebalancing
- L7 load balancers help, but with caveats

---

## Two Approaches

- Client-side LB: client picks the backend per call
- Proxy-based LB: a smart proxy routes traffic
- Both work; trade-offs differ
- Service mesh combines proxy with mTLS and observability
- Cloud platforms favor proxy approaches

---

## LB Approaches Visualized

![lb_approaches](svg/courses/networking/grpc/06_load_balancing_health/lb_approaches.svg)

---

## Health Checking

![health_check](svg/courses/networking/grpc/06_load_balancing_and_health/health_check.svg)

---

## Client-Side Load Balancing

- Client knows all backends
- Picks one per call (or per stream)
- Library handles connection pooling
- Best for low-latency, high-throughput
- Requires service discovery integration

---

## Pick-First

- The default in some clients
- Picks the first backend; falls over only on failure
- Simple, but no real load balancing
- Only useful for single-instance services
- Move to round-robin for production

---

## Round-Robin

- Cycles through backends
- Simple and even under uniform load
- Can pile up on slow backends
- Default when client-side LB is enabled
- Adequate for most internal services

---

## Weighted Round-Robin

- Backends have weights
- Higher weight = more traffic
- Useful when capacities differ
- Requires backend metadata
- Common in mesh-managed deployments

---

## Latency-Aware Algorithms

- Track per-backend latency
- Prefer faster backends
- More sophisticated; less predictable
- Library or mesh implements this
- Good when backends vary in performance

---

## DNS-Based Discovery

- Client queries DNS for backend addresses
- gRPC clients re-resolve periodically
- Simple; works without extra infrastructure
- Use with `dns:///` URI scheme
- Limited control: just an A record list

---

## Registry-Based Discovery

- Service registry (Consul, etcd, ZooKeeper)
- Client queries the registry for backends
- Dynamic updates as instances change
- More features than DNS — health, metadata, weights
- Operational complexity is the cost

---

## Service Mesh Discovery

- Mesh handles discovery transparently
- Sidecars (Envoy, etc) intercept calls
- Client connects to localhost; sidecar routes
- Discovery, mTLS, retries, observability all there
- Consul, Istio, Linkerd are common

---

## Envoy-Based LB

- Envoy as a smart L7 proxy
- Understands gRPC and HTTP/2
- Manages connections to backends
- Per-RPC routing, not per-connection
- The default in many cloud setups

---

## Kubernetes and gRPC

- Service IPs are L4 — not great for gRPC
- Use headless services + client-side LB
- Or Envoy/Linkerd as a sidecar
- Or expose via ingress with HTTP/2 awareness
- Plain ClusterIP is the trap

---

## The Health Checking Protocol

- A standard gRPC service: `grpc.health.v1.Health`
- Two methods: `Check` and `Watch`
- Returns SERVING, NOT_SERVING, UNKNOWN
- Used by load balancers and orchestrators
- Implement on every server

---

## Implementing Health Checks

```go
import "google.golang.org/grpc/health"
import healthpb "google.golang.org/grpc/health/grpc_health_v1"

healthSrv := health.NewServer()
healthpb.RegisterHealthServer(server, healthSrv)
healthSrv.SetServingStatus("", healthpb.HealthCheckResponse_SERVING)
```

- Library provides a default implementation
- Set status per service
- Update on dependency changes

---

## Kubernetes Probes

- gRPC liveness/readiness via `grpc-health-probe` binary
- Or using K8s 1.24+ native gRPC probes
- Pass `--addr=:8080` to the probe
- Returns 0 for SERVING, non-zero otherwise
- Standard pattern for production

---

## Server Reflection

- Server exposes its service definitions at runtime
- Tools (grpcurl, Evans) introspect available methods
- No need to ship .proto files to clients for tooling
- Disabled by default — enable for debugging
- Can leak info; gate on environment

---

## Enabling Reflection (Server)

```go
import "google.golang.org/grpc/reflection"

reflection.Register(server)
```

- One line to register
- Tools like grpcurl now discover methods
- Disable in production unless you understand the trade-offs

---

## Connection Management

- Long-lived connections vs reconnection
- Keepalive pings detect dead connections
- HTTP/2 GOAWAY frames for graceful shutdown
- Avoid thundering herds on reconnect
- Each language has different defaults

---

## Keepalive Configuration

```go
opts := []grpc.DialOption{
    grpc.WithKeepaliveParams(keepalive.ClientParameters{
        Time:    10 * time.Second,
        Timeout: 5 * time.Second,
    }),
}
```

- Periodic pings keep connections alive
- Detect dead servers faster
- Tune to your network and SLOs

---

## Common Pitfalls

- Using a TCP load balancer for gRPC — uneven load
- DNS without re-resolution — stale endpoints
- No health check — orchestrator can't drain bad pods
- Reflection enabled in production by accident
- Keepalive too aggressive — wastes resources

---

## Service Mesh Trade-Offs

- Wins: mTLS, observability, retries, rate limiting
- Costs: another moving part, latency, complexity
- Adopt when the wins outweigh the operational burden
- Many teams overcommit too early
- Start simple; add mesh when needed

---

## Best Practices

- Always implement health checks
- Use client-side LB or service mesh — not L4 LB
- Set keepalives appropriately
- Enable reflection in dev; disable in prod
- Monitor connection counts and per-backend latency

---

## Summary

- gRPC's HTTP/2 connections need smarter load balancing
- Client-side LB or proxy/mesh — pick one
- DNS, registry, mesh — three discovery approaches
- Health protocol is standard; implement it
- Reflection is great for debugging — be careful in prod
