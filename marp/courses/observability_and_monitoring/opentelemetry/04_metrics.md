---
tags:
  - observability:opentelemetry
level: intermediate
category: observability
audience:
  - audiences:devops

---
# Metrics

---
## What This Chapter Covers

- OTel metrics model
- Instrument types
- Aggregations
- Views
- Push vs pull
- Best practices

---
## OTel Metrics Model

- Synchronous and asynchronous instruments
- Aggregation chosen at SDK
- Exported as OTLP, Prometheus, or other

---
## Instrument Types

- Counter: monotonic
- UpDownCounter: increases or decreases
- Histogram: distribution
- Gauge (async): observed value

---
## Counter

- Total requests, bytes sent
- Only goes up
- Reset on restart

---
## UpDownCounter

- Active connections, queue depth
- Increase / decrease
- Replaces gauges for sync paths

---
## Histogram

- Latency, request size
- Buckets for distribution
- Compute percentiles in backend

---
## Asynchronous Gauge

- Read on demand
- Memory used, CPU temperature
- Callback at export time

---
## Sample Counter (Go)

```go
counter, _ := meter.Int64Counter("orders.processed")
counter.Add(ctx, 1, attribute.String("status", "ok"))
```

---
## Aggregations

- Built into SDK
- Sum, last value, histogram
- Per-instrument default

---
## Views

- Customise aggregation
- Drop attributes
- Rename instruments
- Customise histogram buckets

---
## Sample View

- Drop high-cardinality attribute
- Override default histogram buckets
- Per-export pipeline

---
## Push vs Pull

- Push: SDK sends to collector
- Pull: scraped Prometheus-style
- OTel supports both via exporters

---
## Cardinality

- Limit attribute values
- High cardinality: cost and slow queries
- Same pitfall as Prometheus

---
## OTel + Prometheus

- Export OTel metrics in Prometheus format
- Or scrape Prometheus exporter from OTel collector
- Coexist easily

---
## Semantic Conventions

- http.server.duration
- messaging.publish.duration
- Standard names; portable dashboards

---
## Common Metric Mistakes

- High-cardinality attributes
- Counters as gauges (or vice versa)
- No views; defaults inappropriate
- Mixing OTel and Prometheus naming styles
- Buckets unsuitable for app's latency profile
