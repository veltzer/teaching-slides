---
tags:
  - concepts:microservices
  - concepts:resiliency
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# Resilience Patterns

---
## Why Resilience

- Services fail; networks blip; dependencies are slow
- Without resilience patterns, one bad dependency takes everything down
- These patterns are how distributed systems survive

---
## Timeouts

- Every cross-service call must have a timeout
- Without one, a slow B blocks A indefinitely
- The default timeout in most HTTP libraries is "infinite" — set it explicitly
- Pick timeouts based on the called service's SLA, not a guess

---
## Retries

- Retry on transient failures (network blip, 503)
- Don't retry on permanent failures (400, 404)
- Use exponential backoff with jitter
- Bound the retry count; don't retry forever

---
## Retry Anti-Patterns

- Tight retry loops: 1000 retries in a second amplifies the problem
- Retrying non-idempotent operations without idempotency keys
- Retrying everything regardless of error type
- "Just retry" without thinking about the error model

---
## Circuit Breaker

- Track recent failure rate to a dependency
- If too high, "open the circuit" — fast-fail without making the call
- After a cooldown, "half-open" — let one call through to test
- Restore to closed if it succeeds

---
## Circuit Breaker States

- **Closed**: normal operation, calls go through
- **Open**: dependency is unhealthy, fail fast without calling
- **Half-Open**: probe to see if dependency recovered
- States transition based on success/failure rates

---
## Bulkhead

- Isolate failure domains so one bad area doesn't sink the rest
- Separate thread pools or connection pools per dependency
- Or: separate queues, separate processes, separate clusters
- Inspired by ship hull design

---
## Bulkhead Example

- Service A has 100 worker threads
- Without bulkheads: one slow dependency holds all 100 threads
- With bulkheads: 25 threads per dependency, others stay free
- One bad dependency degrades 25%, not 100%

---
## Fallbacks

- When a dependency fails, return something useful (not just an error)
- "Recommendations are unavailable, here's a default list"
- "User profile is slow; show a basic placeholder"
- Fallbacks turn outages into degraded modes

---
## Graceful Degradation

- Identify each feature's importance
- Critical features fail loudly
- Nice-to-have features fail silently with fallbacks
- The system stays usable even when parts are down

---
## Health Endpoints

- Each service exposes `/healthz` and `/ready`
- Monitoring uses these to detect failure
- Load balancers use these to route traffic
- Treat them as part of the API

---
## Rate Limiting (Self-Protection)

- A service should limit how fast it accepts work
- Beyond a threshold, return 429 with backoff
- Better to reject than to crash trying
- Backpressure protects everyone

---
## Service Mesh Resilience

- A mesh handles timeouts, retries, circuit breakers transparently
- Configured per route, applied to every call
- Reduces boilerplate; centralizes the policy
- Examples: Istio, Linkerd

---
## Chaos Engineering

- Deliberately inject failures in production-like environments
- Verify the resilience patterns actually work
- "Kill a random pod every Friday at 3pm"
- Tools: Chaos Monkey, Litmus, Gremlin

---
## Anti-Patterns

- No timeouts (infinite waits)
- Retry storms (no backoff, no jitter)
- "Just throw more replicas at it" (doesn't help if dependencies are bad)
- Hidden cascading failures because no one tested under failure conditions

---
## Summary

- Timeouts, retries, circuit breakers, bulkheads, fallbacks
- Each is small; together they make distributed systems survivable
- Service mesh can centralize them
- Chaos engineering verifies they work
- A microservice without resilience patterns is a liability
