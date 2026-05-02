---
tags:
  - observability:tracing
level: intermediate
category: observability
audience:
  - audiences:devops
  - audiences:developers

---
# Operations

---
## What This Chapter Covers

- Components
- Deployment patterns
- Monitoring
- Upgrades
- Pitfalls

---
## Components

- Agent or collector receivers
- Collectors aggregate
- Storage backend
- Query and UI

---
## Pipeline Visualized

![collector_pipeline](svg/courses/observability_and_monitoring/jaeger/05_operations/collector_pipeline.svg)

---
## Sidecar Agents

- One per host or pod
- Receive from local apps
- Forward to collectors
- Reduces app coupling

---
## Direct To Collector

- Apps send straight to collector
- Skip the agent
- Fewer moving parts
- Common in cloud-native

---
## Collector Tier

- Stateless workers
- Scale horizontally
- Apply sampling and processing
- Forward to storage

---
## High Availability

- Multiple collectors
- Multiple storage replicas
- Health checks at every layer
- Graceful degradation under load

---
## Monitoring

- Spans received
- Spans dropped
- Storage write latency
- Query latency

---
## Alerts

- Drop rate exceeds threshold
- Backend unavailable
- Query latency high
- Disk near full

---
## Upgrades

- Read release notes
- Test in lower env
- Roll components one tier at a time
- Have rollback plan

---
## Multi-Tenant

- Separate ingestion per tenant
- Or tag-based separation
- Quotas to avoid noisy tenants
- Audit access

---
## Security

- TLS at every hop
- Authentication for ingestion
- Authentication for query
- Strip sensitive tags

---
## OpenTelemetry Migration

- Industry-standard protocol
- Receivers built into collector
- Unified instrumentation
- Less vendor lock-in

---
## Disaster Recovery

- Storage backup
- Collector configs in git
- Test restores
- Document the runbook

---
## Cost Awareness

- Storage dominates
- Network bandwidth secondary
- Tune sampling and retention
- Tag for cost allocation

---
## Common Operational Mistakes

- One collector node
- No drop-rate alert
- Untested upgrades
- Plain HTTP between layers
- No multi-tenant quotas
