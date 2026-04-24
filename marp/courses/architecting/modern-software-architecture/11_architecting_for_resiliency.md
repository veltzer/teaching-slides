---
tags:
  - concepts:architecture
  - concepts:resiliency
  - concepts:design-patterns
level: advanced
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Architecting for Resiliency

---
## What Is Resiliency?

- The ability of a system to handle and recover from failures gracefully
- Not about preventing all failures, but about surviving them
- A resilient system degrades gracefully rather than collapsing entirely
- Critical for systems that run at scale in distributed environments

---
## Why Resiliency Matters

- In distributed systems, failures are not exceptional; they are normal
- A single service failure can cascade across the entire system
- Downtime costs money, reputation, and customer trust
- Resilient systems maintain acceptable service levels during partial failures

---
## Failure Categories

![failure_categories](svg/courses/architecting/modern-software-architecture/11_architecting_for_resiliency/failure_categories.svg)

---
## The Cascade Effect

![the_cascade_effect](svg/courses/architecting/modern-software-architecture/11_architecting_for_resiliency/the_cascade_effect.svg)

---
## The Cascade Effect Explained

- Service C fails; B waits and exhausts its thread pool
- Service A waits for B and also becomes unresponsive
- A single failure propagates through the entire call chain

---
## Resiliency Patterns Overview

![resiliency_patterns_overview](svg/courses/architecting/modern-software-architecture/11_architecting_for_resiliency/resiliency_patterns_overview.svg)

---
## Timeouts

- Set a maximum time a caller will wait for a response
- Prevents threads from being held indefinitely
- Without timeouts, a slow dependency can consume all resources
- Every external call should have a timeout configured

---
## Timeout Best Practices

- Set timeouts based on measured response time percentiles
- Use different timeouts for different operations
- Include connection timeouts and read timeouts separately
- Log timeouts for monitoring and debugging

---
## Timeout Configuration Example

```python
import requests

response = requests.get(
    "https://api.example.com/orders",
    timeout=(3, 10)  # (connect, read)
)
```

- Connection timeout: 3 seconds to establish the connection
- Read timeout: 10 seconds to receive the response

---
## Retries

- Automatically resend a failed request after a delay
- Effective for transient failures like network blips
- Must be combined with timeouts to avoid indefinite waits
- Only retry on errors that are likely to be transient

---
## Retry with Exponential Backoff

![retry_with_exponential_backoff](svg/courses/architecting/modern-software-architecture/11_architecting_for_resiliency/retry_with_exponential_backoff.svg)

---
## Retry Best Practices

- Each retry waits longer than the previous one
- Add random jitter to prevent thundering herd
- Set a maximum number of retries to avoid infinite loops

---
## Retry Code Example

```python
import time
import random

def retry_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except TransientError:
            if attempt == max_retries - 1:
                raise
            delay = (2 ** attempt) + \
                    random.uniform(0, 1)
            time.sleep(delay)
```

---
## When NOT to Retry

- The error is clearly permanent (e.g., `400 Bad Request`, `404 Not Found`)
- The operation is not idempotent (e.g., non-idempotent `POST`)
- The downstream service is overloaded (retries make it worse)
- The retry budget is exhausted
- Always check the HTTP status code before deciding to retry

---
## Circuit Breaker Pattern

- Prevents a caller from repeatedly calling a failing service
- Named after the electrical circuit breaker concept
- Has three states: Closed, Open, and Half-Open
- Protects both the caller and the failing service

---
## Circuit Breaker Overview

![circuit_breaker_pattern](svg/courses/architecting/modern-software-architecture/11_architecting_for_resiliency/circuit_breaker_pattern.svg)

---
## Circuit Breaker States

![circuit_breaker_states](svg/courses/architecting/modern-software-architecture/11_architecting_for_resiliency/circuit_breaker_states.svg)

---
## Circuit Breaker: Closed State

- Normal operation; requests pass through to the service
- Failures are counted against a threshold
- When the failure count exceeds the threshold, the circuit opens
- Success resets the failure counter

---
## Circuit Breaker: Open State

- All requests are immediately rejected without calling the service
- A fallback response is returned to the caller
- After a configured timeout, the circuit transitions to half-open
- Gives the failing service time to recover

---
## Circuit Breaker: Half-Open State

- A limited number of probe requests are sent to the service
- If probes succeed, the circuit closes and normal traffic resumes
- If probes fail, the circuit opens again
- Prevents overwhelming a recovering service with full traffic

---
## Circuit Breaker Code Example

```python
class CircuitBreaker:
    def __init__(self, threshold=5,
                 timeout=30):
        self.threshold = threshold
        self.timeout = timeout
        self.failures = 0
        self.state = "CLOSED"
        self.last_failure_time = None

    def call(self, func):
        if self.state == "OPEN":
            if self._timeout_expired():
                self.state = "HALF_OPEN"
            else:
                raise CircuitOpenError()
        try:
            result = func()
            self._on_success()
            return result
        except Exception:
            self._on_failure()
            raise
```

---
## Circuit Breaker Libraries

- `Resilience4j` - Java library with circuit breaker, retry, rate limiter
- `Polly` - .NET resilience library
- `Hystrix` - Netflix library (now in maintenance mode)
- `pybreaker` - Python circuit breaker
- `Istio` - service mesh with built-in circuit breaking

---
## Bulkhead Pattern

- Isolates different parts of the system to prevent cascade failures
- Named after ship bulkheads that contain flooding to one compartment
- Each critical resource gets its own isolated pool
- A failure in one pool does not affect others

---
## Bulkhead Architecture

![bulkhead_architecture](svg/courses/architecting/modern-software-architecture/11_architecting_for_resiliency/bulkhead_architecture.svg)

---
## Bulkhead Benefits

- Service C is slow but only consumes its own thread pool
- Services A and B continue to operate normally

---
## Bulkhead Implementation Strategies

- Thread pool isolation: separate thread pools per downstream service
- Semaphore isolation: limit concurrent calls without separate threads
- Process isolation: run in separate containers or pods
- Connection pool isolation: separate database connection pools

---
## Rate Limiting

- Controls the number of requests a client can make in a given time window
- Protects services from being overwhelmed by excessive traffic
- Can be applied at the API gateway, service, or infrastructure level
- Essential for public-facing APIs and shared resources

---
## Rate Limiting Algorithms

- Fixed Window: count requests in fixed time intervals
- Sliding Window: smooth counting across time boundaries
- Token Bucket: tokens are added at a fixed rate; each request consumes one
- Leaky Bucket: requests flow out at a constant rate

---
## Token Bucket Diagram

![token_bucket_diagram](svg/courses/architecting/modern-software-architecture/11_architecting_for_resiliency/token_bucket_diagram.svg)

---
## Rate Limiting Response

- Return `HTTP 429 Too Many Requests` when the limit is exceeded
- Include `Retry-After` header to tell the client when to try again
- Include rate limit headers in every response for transparency:
    - `X-RateLimit-Limit` - maximum requests allowed
    - `X-RateLimit-Remaining` - requests remaining in current window
    - `X-RateLimit-Reset` - time when the window resets

---
## Fallback Strategies

- Provide a degraded but acceptable response when a dependency fails
- Return cached data even if it might be slightly stale
- Return default values or simplified responses
- Redirect to a static page or a different service
- Show a meaningful error message instead of a crash

---
## Fallback Decision Tree

![fallback_decision_tree](svg/courses/architecting/modern-software-architecture/11_architecting_for_resiliency/fallback_decision_tree.svg)

---
## Hedging

- Send the same request to multiple instances simultaneously
- Use the first response and discard the rest
- Reduces the impact of slow individual instances
- Useful for latency-sensitive operations

---
## Hedging Diagram

![hedging_diagram](svg/courses/architecting/modern-software-architecture/11_architecting_for_resiliency/hedging_diagram.svg)

---
## Hedging Trade-Offs

- Instance 2 responds first; its response is used
- Trade-off: uses more resources for lower latency

---
## Chaos Engineering

- The discipline of experimenting on a system to build confidence in resilience
- Deliberately introduce failures to discover weaknesses
- Pioneered by Netflix with `Chaos Monkey`
- Based on the principle that untested resilience is not resilience

---
## Chaos Engineering Principles

1. Define the steady state of the system (normal behavior metrics)
1. Hypothesize that the system will maintain steady state during a fault
1. Inject a real-world failure (kill a server, add latency, corrupt data)
1. Observe the system and compare to the hypothesis
1. Fix any weaknesses discovered

---
## Chaos Engineering Process

![chaos_engineering_process](svg/courses/architecting/modern-software-architecture/11_architecting_for_resiliency/chaos_engineering_process.svg)

---
## Chaos Engineering Tools

- `Chaos Monkey` - randomly terminates VM instances (Netflix)
- `Gremlin` - commercial chaos engineering platform
- `Litmus` - cloud-native chaos engineering for Kubernetes
- `Chaos Mesh` - open-source chaos engineering for Kubernetes
- `Toxiproxy` - simulate network conditions between services

---
## Common Chaos Experiments

- Kill random pods or nodes in a Kubernetes cluster
- Inject network latency between specific services
- Simulate DNS failures
- Fill up disk space on a node
- Exhaust CPU or memory on selected instances
- Block network traffic between availability zones

---
## Chaos Engineering in Practice

- Start in non-production environments to build confidence
- Gradually move to production with small blast radius
- Always have a kill switch to stop the experiment immediately
- Run experiments during business hours when the team is available
- Automate experiments and integrate them into CI/CD

---
## Resiliency Testing Pyramid

![resiliency_testing_pyramid](svg/courses/architecting/modern-software-architecture/11_architecting_for_resiliency/resiliency_testing_pyramid.svg)

---
## Service Mesh for Resiliency

- A dedicated infrastructure layer for service-to-service communication
- Provides circuit breaking, retries, and timeouts without code changes
- Examples: `Istio`, `Linkerd`, `Consul Connect`
- Resiliency policies are configured declaratively, not coded

---
## Service Mesh Architecture

![service_mesh_architecture](svg/courses/architecting/modern-software-architecture/11_architecting_for_resiliency/service_mesh_architecture.svg)

---
## Sidecar vs Sidecarless Meshes

- **Sidecar model** — a proxy (usually `Envoy`) runs next to every app container
    - Pros: full feature set, per-workload policy, language-agnostic
    - Cons: one extra pod per workload, higher memory overhead
- **Sidecarless / ambient mode** — proxies run per-node or per-identity, not per-pod
    - Pros: lower overhead, simpler pod spec
    - Cons: newer, fewer features, coarser policy granularity
- Istio ambient mesh and Cilium service mesh exemplify the sidecarless direction

---
## Mesh Capabilities

- **Traffic management** — weighted routing, canary splits, fault injection
- **Security** — automatic mTLS between workloads, identity-based authorization
- **Observability** — L7 metrics, distributed traces, and access logs without app changes
- **Resiliency** — retries, timeouts, circuit breakers configured as policy
- **Policy** — quota, rate limits, and allow/deny rules at the edge of each service

---
## Mutual TLS in a Mesh

- Every workload gets a SPIFFE-style cryptographic identity
- Mesh issues short-lived certificates automatically (no app-side key management)
- All service-to-service traffic is encrypted and authenticated by default
- Authorization policies reference workload identity, not IPs
- Rotates certs on a schedule so a leaked key has a small blast radius

---
## Traffic Shaping

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: checkout
spec:
  hosts: ["checkout"]
  http:
    - route:
        - destination: { host: checkout, subset: v1 }
          weight: 90
        - destination: { host: checkout, subset: v2 }
          weight: 10
```

- Shift a fraction of traffic to a new version — the canary lives in the mesh config, not in the app

---
## When NOT to Use a Mesh

- Small systems (< 10 services) — the operational overhead outweighs the benefits
- Workloads outside Kubernetes without multi-cluster mesh support
- Teams that cannot operate the mesh itself (it is another distributed system to run)
- Language-native libraries already provide what you need (e.g., gRPC's built-ins)

---
## Building a Resiliency Strategy

1. Identify critical paths and dependencies
1. Apply timeouts to all external calls
1. Add retries with exponential backoff for transient failures
1. Implement circuit breakers for downstream services
1. Use bulkheads to isolate failure domains
1. Define fallback responses for degraded operation
1. Test with chaos experiments

---
## Resiliency Checklist

- Every external call has a timeout configured
- Retries use exponential backoff with jitter
- Circuit breakers protect against failing dependencies
- Thread pools or connection pools are isolated per dependency
- Rate limits protect services from excessive load
- Fallbacks provide degraded but functional responses
- Chaos experiments validate resilience regularly

---
## Summary

- Resiliency is about surviving failures, not preventing them
- Timeouts prevent indefinite waits; retries handle transient failures
- Circuit breakers stop cascade failures from propagating
- Bulkheads isolate failure domains within a system
- Rate limiting protects services from being overwhelmed
- Chaos engineering validates resilience through controlled experiments
- Service meshes provide resiliency features without application code changes
