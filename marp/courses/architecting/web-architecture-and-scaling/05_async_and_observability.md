---
tags:
  - architecting:patterns
  - practices:scalability
level: intermediate
category: architecting
audience:
  - audiences:architects

---
# Async Patterns and Observability

---
## What This Chapter Covers

- Why async
- Queues in web architectures
- Background jobs
- Observability basics
- Capacity tests

---
## Why Go Async

- Decouple slow work
- Smooth load
- Survive downstream failures
- Better user experience

---
## Sync to Async Boundaries

- Save user-facing latency
- Email send, image resize, indexing
- Return early with status
- Polling or webhooks for completion

---
## Background Workers

- Read from queue
- Idempotent processing
- Auto-scale by depth
- Independent failure domain

---
## Job Scheduling

- Cron-style for fixed times
- Triggered by events
- Watch for overlap with retries
- Track success and failure

---
## Idempotency in Web Calls

- Idempotency keys
- Stored result for replay
- Required for safe retry
- Standard for payments

---
## Retries and Backoff

- Network errors retry
- Exponential backoff
- Jitter to spread retries
- Cap to avoid death spirals

---
## Circuit Breakers

- Trip on consecutive failures
- Skip calls while open
- Half-open probes recovery
- Restores under load gracefully

---
## State Machine

![circuit_breaker](svg/courses/architecting/web-architecture-and-scaling/05_async_and_observability/circuit_breaker.svg)

---
## Observability Layers

- Metrics
- Logs
- Traces
- Profiles

---
## Observability Pillars

![observability_pillars](svg/courses/architecting/web-architecture-and-scaling/05_async_and_observability/observability_pillars.svg)

---
## Metrics That Matter

- Request rate
- Error rate
- Duration p50, p95, p99
- Saturation (queue depth, CPU)

---
## Tracing

- Request ID across hops
- Span per operation
- Find slow hops fast
- Required for distributed systems

---
## Logging Discipline

- Structured logs
- Trace ID included
- Sample where volume too high
- Retention by sensitivity

---
## Load Testing

- Reproduce production traffic
- Find ceiling before users do
- Run regularly
- Profile during tests

---
## Capacity Reviews

- Compare load to capacity
- Project growth
- Order capacity early
- Document the model

---
## Common Async and Observability Mistakes

- Hidden retries amplifying load
- No trace ID
- Logs without structure
- Capacity review once a year
- Load tests only on launch
