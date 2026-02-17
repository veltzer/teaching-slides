# Architecting for Resiliency

<!-- Add Mermaid.js support -->
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({ startOnLoad: true });
</script>

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

<div class="mermaid">
graph TD
    F[Failures]
    F --> TR[Transient]
    F --> INT[Intermittent]
    F --> PERM[Permanent]
    TR --> TR1[Network blip, timeout]
    INT --> INT1[Flaky dependency, resource contention]
    PERM --> PERM1[Hardware failure, bug, data corruption]
</div>

---
## The Cascade Effect

<div class="mermaid">
graph LR
    A[Service A] -->|Calls| B[Service B]
    B -->|Calls| C[Service C - Down]
    C -.->|Timeout| B
    B -.->|Threads exhausted| A
    A -.->|Unresponsive| CLIENT[Client]
</div>

- Service C fails; B waits and exhausts its thread pool
- Service A waits for B and also becomes unresponsive
- A single failure propagates through the entire call chain

---
## Resiliency Patterns Overview

<div class="mermaid">
graph TD
    R[Resiliency Patterns]
    R --> CB[Circuit Breaker]
    R --> RT[Retries]
    R --> TO[Timeouts]
    R --> BH[Bulkheads]
    R --> RL[Rate Limiting]
    R --> FB[Fallbacks]
    R --> HG[Hedging]
</div>

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

<div class="mermaid">
graph LR
    R1[Request - Fail] -->|Wait 1s| R2[Retry 1 - Fail]
    R2 -->|Wait 2s| R3[Retry 2 - Fail]
    R3 -->|Wait 4s| R4[Retry 3 - Success]
</div>

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
## Circuit Breaker States

<div class="mermaid">
stateDiagram-v2
    [*] --> Closed
    Closed --> Open: Failure threshold exceeded
    Open --> HalfOpen: Timeout expires
    HalfOpen --> Closed: Probe succeeds
    HalfOpen --> Open: Probe fails
</div>

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

<div class="mermaid">
graph TD
    APP[Application]
    APP --> BP1[Thread Pool: Service A - 10 threads]
    APP --> BP2[Thread Pool: Service B - 5 threads]
    APP --> BP3[Thread Pool: Service C - 8 threads]
    BP1 --> SA[Service A]
    BP2 --> SB[Service B]
    BP3 --> SC[Service C - Slow]
</div>

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

<svg viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg">
  <rect x="130" y="50" width="140" height="150" fill="none" stroke="#333" stroke-width="2" rx="5"/>
  <text x="200" y="40" text-anchor="middle" font-size="12" font-weight="bold">Token Bucket</text>
  <circle cx="160" cy="80" r="10" fill="#4CAF50"/>
  <circle cx="200" cy="80" r="10" fill="#4CAF50"/>
  <circle cx="240" cy="80" r="10" fill="#4CAF50"/>
  <circle cx="160" cy="110" r="10" fill="#4CAF50"/>
  <circle cx="200" cy="110" r="10" fill="#4CAF50"/>
  <circle cx="160" cy="140" r="10" fill="#ccc" stroke="#999"/>
  <circle cx="200" cy="140" r="10" fill="#ccc" stroke="#999"/>
  <circle cx="240" cy="140" r="10" fill="#ccc" stroke="#999"/>
  <text x="200" y="175" text-anchor="middle" font-size="10">5 tokens / 3 empty</text>
  <line x1="50" y1="80" x2="130" y2="80" stroke="#333" stroke-width="1" marker-end="url(#arr)"/>
  <text x="90" y="70" text-anchor="middle" font-size="10">Refill</text>
  <line x1="270" y1="80" x2="350" y2="80" stroke="#333" stroke-width="1" marker-end="url(#arr)"/>
  <text x="310" y="70" text-anchor="middle" font-size="10">Request</text>
  <defs>
    <marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
      <path d="M0,0 L0,8 L8,4 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<div class="mermaid">
graph TD
    A{Primary service available?}
    A -->|Yes| B[Return fresh data]
    A -->|No| C{Cache available?}
    C -->|Yes| D[Return cached data]
    C -->|No| E{Default value sensible?}
    E -->|Yes| F[Return default]
    E -->|No| G[Return graceful error]
</div>

---
## Hedging

- Send the same request to multiple instances simultaneously
- Use the first response and discard the rest
- Reduces the impact of slow individual instances
- Useful for latency-sensitive operations

---
## Hedging Diagram

<div class="mermaid">
graph TD
    C[Client] -->|Same Request| I1[Instance 1]
    C -->|Same Request| I2[Instance 2]
    C -->|Same Request| I3[Instance 3]
    I1 -->|150ms| C
    I2 -->|50ms - Winner| C
    I3 -->|200ms| C
</div>

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

<div class="mermaid">
graph LR
    A[Define Steady State] --> B[Form Hypothesis]
    B --> C[Design Experiment]
    C --> D[Inject Failure]
    D --> E[Observe Results]
    E --> F{Steady state maintained?}
    F -->|Yes| G[Increase scope]
    F -->|No| H[Fix weakness]
    H --> A
    G --> B
</div>

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

<svg viewBox="0 0 400 280" xmlns="http://www.w3.org/2000/svg">
  <polygon points="200,20 50,260 350,260" fill="none" stroke="#333" stroke-width="2"/>
  <line x1="100" y1="160" x2="300" y2="160" stroke="#333" stroke-width="1"/>
  <line x1="135" y1="100" x2="265" y2="100" stroke="#333" stroke-width="1"/>
  <text x="200" y="230" text-anchor="middle" font-size="12">Unit Tests with Mocks</text>
  <text x="200" y="140" text-anchor="middle" font-size="12">Integration Tests</text>
  <text x="200" y="80" text-anchor="middle" font-size="12">Chaos Experiments</text>
</svg>

---
## Service Mesh for Resiliency

- A dedicated infrastructure layer for service-to-service communication
- Provides circuit breaking, retries, and timeouts without code changes
- Examples: `Istio`, `Linkerd`, `Consul Connect`
- Resiliency policies are configured declaratively, not coded

---
## Service Mesh Architecture

<div class="mermaid">
graph TD
    subgraph Service A Pod
        A[App Container] --- PA[Sidecar Proxy]
    end
    subgraph Service B Pod
        B[App Container] --- PB[Sidecar Proxy]
    end
    PA -->|Encrypted, Resilient| PB
    CP[Control Plane] -.->|Config| PA
    CP -.->|Config| PB
</div>

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
