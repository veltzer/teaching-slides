---
tags:
  - observability:opentelemetry
  - practices:production
level: intermediate
category: observability
audience:
  - audiences:devops

---

# Practical Use

---

## What This Chapter Covers

- Migration paths
- Common architectures
- Debugging with telemetry
- Team practices
- Wrap-up

---

## Migration From Vendor SDK

- Add OTel SDK alongside
- Export to vendor via OTLP
- Remove vendor SDK
- One-by-one per service

---

## Migration From Prometheus

- Keep Prometheus
- Add OTel collector for traces and logs
- Optionally export Prometheus from OTel
- Coexist forever or migrate

---

## Common Migration Paths

![migration_paths](svg/courses/observability_and_monitoring/opentelemetry/10_practical_use/migration_paths.svg)

---

## Common Architectures

- App SDK to local collector (sidecar)
- Sidecar to gateway cluster
- Gateway to backend(s)
- Standard pattern

---

## Kubernetes Setup

- OpenTelemetry Operator
- Auto-injection of agents
- DaemonSet for node-level data
- StatefulSet for gateway

---

## Auto vs Manual

- Auto for breadth
- Manual for business spans
- Combine

---

## Debugging Workflow

- Alert fires (high latency)
- Open dashboard
- Drill to slow traces
- Identify slow span
- Read logs at that span

---

## Observability-Driven Development

- Add spans as you write code
- Treat instrumentation as first-class
- Review in PRs

---

## Naming Discipline

- Follow semantic conventions
- Custom names: stable, agreed across teams
- Attribute names lowercase, dot.separated

---

## Onboarding New Services

- Instrumentation as part of service template
- service.name from config
- Collector endpoint from env
- Documented checklist

---

## Reviewing Telemetry

- Periodic audit
- Drop unused metrics
- Trim noisy logs
- Keep cost in check

---

## Incident Postmortems

- Use traces and logs
- Save permalinks
- Improve instrumentation based on gaps
- Feed back into tooling

---

## When OTel Is Wrong

- Tiny app, single process: maybe overkill
- Hard real-time: SDK overhead
- Most teams: it is right

---

## Course Wrap-Up

- OTel: standard for telemetry
- Three signals: traces, metrics, logs
- Collector: pipeline
- Vendor-neutral, future-proof
- Production needs sampling, HA, redaction
- Adoption: per-service migration

---

## Common Practical Mistakes

- Treating it as a side project
- No cost dashboards from day one
- All custom names; no semantic conventions
- Replacing all tooling at once
- Skipping incident retros that improve telemetry
