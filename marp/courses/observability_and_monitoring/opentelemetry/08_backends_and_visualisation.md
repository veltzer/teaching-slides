---
tags:
  - observability:opentelemetry
level: intermediate
category: observability
audience:
  - audiences:devops

---

# Backends and Visualisation

---

## What This Chapter Covers

- Where telemetry goes
- Open-source backends
- Vendor backends
- Choosing
- Switching backends

---

## Backends

- Receive OTLP
- Store telemetry
- Provide UI
- Backend choice independent of OTel

---

## Where Telemetry Lands

![backend_choices](svg/courses/observability_and_monitoring/opentelemetry/08_backends_and_visualisation/backend_choices.svg)

---

## Open-Source: Jaeger

- Tracing-focused
- Mature, Kubernetes-friendly
- Limited storage backends
- Often used with collector

---

## Open-Source: Tempo

- Grafana stack
- Cheap object-storage backend
- Pairs with Loki and Mimir
- Trace search

---

## Open-Source: SigNoz

- All-in-one
- Traces, metrics, logs
- ClickHouse backend
- Self-host alternative to APMs

---

## Open-Source: Grafana

- Frontend for many backends
- Dashboards over Tempo, Mimir, Loki
- Common cloud-native choice

---

## Vendor: Datadog

- Mature APM
- Receives OTLP
- Strong UI and AIOps

---

## Vendor: New Relic

- One platform across signals
- Receives OTLP
- Distributed tracing UI

---

## Vendor: Dynatrace

- Auto-instrumentation strong
- Receives OTLP
- Enterprise focus

---

## Vendor: Honeycomb

- High-cardinality first
- Excellent for tracing-heavy debugging
- OTel-native

---

## Choosing

- Open-source: control, ops burden
- Vendor: less ops, $
- Hybrid: collector forwards to both
- Migrate over time

---

## Decision Lenses

![backend_picker](svg/courses/observability_and_monitoring/opentelemetry/08_backends_and_visualisation/backend_picker.svg)

---

## Switching Backends

- Reconfigure collector exporter
- App code unchanged
- The OTel value proposition

---

## Multi-Backend

- Send to two simultaneously
- During migration
- Or: one for traces, another for metrics
- Common in practice

---

## Cost

- Volume-based pricing typical
- Sample heavily in production
- Drop noisy attributes
- Watch cost dashboards

---

## SLOs Across Backends

- Define SLIs in OTel attributes
- Compute in any backend
- Portable definitions

---

## Common Backend Mistakes

- Picking before knowing volume
- Not testing capacity at peak
- Vendor lock-in via custom attributes
- Two SaaS APMs in parallel "until decided"
- Ignoring egress cost from cloud
