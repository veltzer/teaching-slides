---
tags:
  - observability:opentelemetry
level: intermediate
category: observability
audience:
  - audiences:devops

---
# Collector

---
## Pipeline

![collector_pipeline](svg/courses/observability_and_monitoring/opentelemetry/06_collector/collector_pipeline.svg)

---
## What This Chapter Covers

- What the collector is
- Receivers, processors, exporters
- Pipelines
- Deployment patterns
- Configuration

---
## What the Collector Is

- Vendor-agnostic agent and gateway
- Receives, processes, exports telemetry
- Decouples apps from backends
- Written in Go

---
## Why Use It

- Apps export OTLP locally
- Collector sends to backend(s)
- Switch backends without redeploying apps
- Add processing centrally

---
## Components

- Receivers: ingest
- Processors: transform / batch / sample
- Exporters: send to backends
- Combined into pipelines

---
## Component Roles

![collector_components](svg/courses/observability_and_monitoring/opentelemetry/06_collector/collector_components.svg)

---
## Receivers

- otlp: native protocol
- prometheus: scrape
- jaeger, zipkin: legacy
- filelog: tail logs
- many more

---
## Processors

- batch: efficient export
- memory_limiter: protect collector
- attributes: edit / drop
- tail_sampling: smart sampling
- transform: rewrite

---
## Exporters

- otlp: forward to another collector
- prometheus: expose for scraping
- jaeger, datadog, ...
- Multiple in parallel

---
## Pipelines

```yaml
service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlp/jaeger]
```

- One per signal
- Compose receivers, processors, exporters

---
## Agent Pattern

- Collector per host or pod sidecar
- Apps export locally
- Cheap, low-latency

---
## Gateway Pattern

- Central collector cluster
- Agents forward
- Tail sampling, enrichment, fan-out
- Standard production setup

---
## Both Together

- Agent for collection
- Gateway for processing
- Most production deployments

---
## Sample Configuration

- receivers.otlp: receive on default port
- processors.batch: batch by 5s or 8K
- exporters.otlp: send to vendor
- service.pipelines: stitch together

---
## Scaling

- Horizontal: multiple gateways behind LB
- Tail sampling: needs consistent hashing
- Some processors need single instance

---
## Resource Limits

- memory_limiter processor
- Drops new data when full
- Protects from death spirals

---
## Hot Reload

- SIGHUP to reload config
- Or: file_provider + file watch
- Avoid restarts in production

---
## Common Collector Mistakes

- No memory_limiter; OOM under load
- Tail sampling without consistent hashing
- Too many processors; latency
- Single collector; SPOF
- Untested config changes in production
