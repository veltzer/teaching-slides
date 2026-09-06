---
tags:
  - concepts:architecture
  - concepts:monitoring
  - concepts:observability
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---

# Monitoring

---

## What Monitoring Means in This Course

- This chapter is intentionally a stub
- Monitoring is largely an operational concern, not a structural pattern
- The Architecting Software Systems course covers it in depth
- What follows is the minimum vocabulary every catalog reader should have

---

## What Is Observability?

- The ability to understand the internal state of a system from its outputs
- Goes beyond traditional monitoring of pre-defined metrics
- Enables debugging unknown problems by exploring system data
- Critical for distributed systems where direct inspection is impossible

---

## The Three Pillars of Observability

- Logs
    - Discrete events with timestamps and context
- Metrics
    - Numeric measurements aggregated over time
- Traces
    - The path of a request through a distributed system

---

## Logs vs Metrics vs Traces

| Pillar | Use For | Storage Cost | Query Pattern |
|--------|---------|--------------|---------------|
| Logs | Detailed event context | High | Full-text search |
| Metrics | Trends and alerts | Low | Time-series query |
| Traces | Request flow analysis | Medium | Trace ID lookup |

---

## When the Three Pillars Are Not Enough

- Logs tell you what happened, but not why
- Metrics show trends, but lose individual context
- Traces show flow, but only for sampled requests
- Modern observability adds events and continuous profiling
- The goal is to be able to ask new questions without redeploying

---

## See Also

- The Architecting Software Systems course covers monitoring as a full chapter
- Topics there include log aggregation pipelines, Prometheus, distributed tracing with OpenTelemetry, alerting, SLOs, error budgets, dashboard design
- This catalog entry is a vocabulary stub only
