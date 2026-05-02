---
tags:
  - observability:opentelemetry
  - practices:production
level: intermediate
category: observability
audience:
  - audiences:devops

---
# Production Patterns

---
## What This Chapter Covers

- Sampling
- Cost control
- Reliability
- Privacy
- Rollout strategies
- SLOs

---
## Sampling Strategy

- Head: cheap, randomised
- Tail: smart, captures errors
- Combine: head at edge, tail at gateway

---
## Sampling Strategies

![sampling](svg/courses/observability_and_monitoring/opentelemetry/09_production_patterns/sampling.svg)

---
## Tail Sampling Rules

- Always keep errors
- Always keep slow traces
- Sample fast successes lightly
- Per-tenant policies

---
## Cost Drivers

- Span volume
- High-cardinality attributes
- Logs at DEBUG in prod
- Retention period

---
## Reducing Cost

- Drop noisy attributes
- Lower sampling rate
- Shorter retention for low-value telemetry
- Different tiers per signal

---
## Reliability

- Collector HA: multiple replicas
- Persistent queue: don't lose data on restart
- Memory limiter: protect from OOM
- Retry with backoff

---
## Persistent Queue

- Disk-backed buffer in collector
- Survives restarts
- Configurable size

---
## Privacy

- Don't put PII in attributes
- Body of logs especially risky
- Use processors to redact
- Audit periodically

---
## Redaction

- regex patterns in transform processor
- Strip credit cards, emails, tokens
- Apply at agent and gateway

---
## Rollout

- One service first
- Compare with existing tooling
- Expand once stable
- Don't replace all monitoring at once

---
## Versioning

- Pin SDK and collector versions
- Test upgrades in staging
- Spec is stable; some semconv evolving

---
## SLOs From OTel

- Define in semantic terms
- Compute from histograms
- Multi-window burn alerts
- Same as Prometheus pattern

---
## Dashboards

- One per service
- RED metrics
- Top traces by latency / errors
- Drill from metric to trace

---
## Service Maps

- Auto-generated from spans
- See dependencies
- Spot unexpected calls
- Backend feature

---
## Resource Attributes

- service.name (required)
- deployment.environment (prod, staging)
- k8s.pod.name, k8s.namespace.name
- Set by SDK or by collector enrichment

---
## Common Production Mistakes

- 100% sampling in prod
- No collector HA; data loss on restart
- PII in attributes
- Migrating all services at once
- No alerts on collector itself (drops, OOM)
