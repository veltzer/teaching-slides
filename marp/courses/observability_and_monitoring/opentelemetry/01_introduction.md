---
tags:
  - observability:opentelemetry
level: intermediate
category: observability
audience:
  - audiences:devops

---
# Introduction to OpenTelemetry

---
## What This Chapter Covers

- What OpenTelemetry is
- History
- Components
- Signals
- Why use it
- Adoption

---
## What OpenTelemetry Is

- Open standard for observability
- APIs, SDKs, conventions
- Vendor-neutral
- CNCF graduated project

---
## History

- Merger of OpenCensus + OpenTracing (2019)
- Replaced both
- Backed by major vendors
- De facto standard now

---
## Three Signals

- Traces: request flows
- Metrics: numerical time series
- Logs: discrete events
- All in one toolkit

---
## Components

- API: instrumentation surface
- SDK: implementation
- Collector: pipeline
- Exporters: send to backends
- Auto-instrumentation: agents

---
## Why Use OTel

- One instrumentation; many backends
- Switch vendors without recoding
- Standardised semantics
- Future-proof

---
## Vendor-Neutral

- Send to Jaeger, Tempo, Datadog, New Relic, ...
- Avoid lock-in
- Mix and match

---
## Adoption

- Most cloud vendors support OTLP
- All major APMs ship OTel SDKs
- Default in Kubernetes ecosystem
- 2024+: standard expectation

---
## Compared to Prometheus

- Prometheus: pull, metrics-focused
- OTel: push, all signals
- Coexist: OTel can export to Prometheus

---
## Compared to Vendor SDKs

- Vendor SDK: tight integration, lock-in
- OTel: open, switchable
- OTel SDK with vendor exporter: best of both

---
## OTLP

- OpenTelemetry Protocol
- Wire format for telemetry
- gRPC or HTTP
- Backends accept it directly

---
## Course Plan

- Tracing details
- Metrics
- Logs
- Collector
- Production deployment

---
## Common Introduction Mistakes

- Adopting all signals at once; too much change
- Ignoring sampling; data costs explode
- Treating OTel as a vendor product
- Not pinning SDK versions
- Building before learning semantic conventions
