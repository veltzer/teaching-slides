---
tags:
  - observability:prometheus
level: intermediate
category: observability
audience:
  - audiences:devops

---
# Prometheus Basics

---
## What This Chapter Covers

- Architecture
- Pull model
- Targets and scraping
- Time series
- Metric types
- Labels

---
## Architecture Overview

![architecture](svg/courses/observability_and_monitoring/prometheus-and-grafana/02_prometheus_basics/architecture.svg)

---
## Architecture

- Prometheus server: scrapes targets, stores TSDB
- Targets: applications expose /metrics
- Alertmanager: routes alerts
- Push gateway: for short-lived jobs
- Exporters: bridge non-native systems

---
## Pull Model

- Prometheus scrapes targets on interval
- Targets expose HTTP /metrics endpoint
- Server-controlled cadence
- Push model is the exception

---
## Why Pull

- Service discovery
- Fail loudly: missing scrape = down
- No dependency on every client to push
- Centralised config

---
## Configuration

```yaml
scrape_configs:
  - job_name: 'app'
    scrape_interval: 15s
    static_configs:
      - targets: ['localhost:8080']
```

- prometheus.yml
- Reload via SIGHUP

---
## Time Series

- Series identified by name + labels
- Sample: timestamp + value
- Stored in TSDB
- Retention configurable

---
## Sample Metric

```misc
http_requests_total{method="GET", status="200"} 1234
```

- Name: http_requests_total
- Labels: method, status
- Value: 1234

---
## Metric Types

- Counter: monotonic; only goes up
- Gauge: arbitrary value; up or down
- Histogram: distribution of values
- Summary: percentiles client-side

---
## Counter

- Requests, errors, bytes sent
- Reset on restart
- Use rate() for "per second"

---
## Gauge

- Memory, queue length, temperature
- Up and down
- Use directly

---
## Histogram

- Buckets for value ranges
- Server-side aggregation
- Compute percentiles in queries
- Standard for latency

---
## Labels

- Key-value tags
- Slice and dice
- High cardinality is bad
- One series per unique label combo

---
## Cardinality Pitfall

- user_id as label: millions of series
- Memory explosion
- Slow queries
- Use coarse labels (region, status)

---
## Common Prometheus Mistakes

- High-cardinality labels (user id, request id)
- No retention policy; unbounded disk
- Forgetting to use rate() on counters
- Push gateway for normal services
- Too-frequent scraping
