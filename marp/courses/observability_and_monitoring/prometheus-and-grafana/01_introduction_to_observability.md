---
tags:
  - observability:prometheus
  - observability:grafana
level: intermediate
category: observability
audience:
  - audiences:devops

---
# Introduction to Observability

---
## What This Chapter Covers

- Observability concepts
- Three pillars
- Metrics, logs, traces
- Why Prometheus and Grafana
- Stack overview

---
## What Observability Is

- Ability to understand a system from outside
- Answer: what, why, when
- More than monitoring
- Critical for distributed systems

---
## Monitoring vs Observability

- Monitoring: known unknowns; alerts you set
- Observability: unknown unknowns; explore freely
- Overlap; observability is the broader concept

---
## Three Pillars

- Metrics: numerical, time-series
- Logs: discrete events
- Traces: request flows
- Different questions, different tools

---
## Three Pillars Visualized

![three_pillars](svg/courses/observability_and_monitoring/prometheus-and-grafana/01_introduction_to_observability/three_pillars.svg)

---
## Metrics

- CPU, memory, requests/sec
- Cheap to store
- Aggregated
- Best for dashboards and alerts

---
## Logs

- "What happened at this moment?"
- Verbose, expensive at scale
- Debugging
- Structured logs preferred

---
## Traces

- "How did this request travel?"
- Across services
- Spot bottlenecks
- OpenTelemetry standard

---
## Why Prometheus

- Open source
- Pull-based
- Time-series database
- Query language: PromQL
- Standard for cloud-native

---
## Why Grafana

- Visualises Prometheus and many others
- Dashboards
- Alerts
- Multi-source

---
## The Stack

- Prometheus: collection + storage
- Grafana: visualisation
- Alertmanager: routing
- Exporters: bridge to non-native sources

---
## Cloud-Native Standard

- CNCF projects
- Default in Kubernetes
- Huge ecosystem of exporters

---
## Course Plan

- Prometheus setup and queries
- Grafana dashboards
- Alerting
- Production patterns

---
## Common Observability Mistakes

- Logging everything; cost explosion
- Metrics for what should be logs (high cardinality)
- No tracing in distributed systems
- Dashboards nobody looks at
- Alerts that always fire (noise)
