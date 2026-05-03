---
tags:
  - observability:prometheus
level: intermediate
category: observability
audience:
  - audiences:devops

---
# Exporters and Instrumentation

---
## What This Chapter Covers

- Exporters
- Common exporters
- Direct instrumentation
- Client libraries
- Best practices

---
## Exporters

- Bridge non-Prometheus sources
- Read system data, expose /metrics
- Many official and community

---
## Exporter Categories

![exporter_kinds](svg/courses/observability_and_monitoring/prometheus-and-grafana/04_exporters_and_instrumentation/exporter_kinds.svg)

---
## Node Exporter

- Linux host metrics
- CPU, memory, disk, network
- One per node
- Standard

---
## kube-state-metrics

- Kubernetes object state
- Pod counts, deployment status
- Different from cAdvisor (resource usage)

---
## Database Exporters

- MySQL exporter, Postgres exporter
- Query stats, connection counts
- Run alongside DB

---
## Black Box Exporter

- Probes endpoints
- HTTP, TCP, ICMP, DNS
- "Is this URL up?"
- External monitoring

---
## Custom Exporters

- Write your own
- Read from any source, expose /metrics
- Use client libraries

---
## Direct Instrumentation

- Best option when possible
- Add metrics inside your app
- Client libraries: Go, Python, Java, ...

---
## Sample (Python)

```python
from prometheus_client import Counter, start_http_server

reqs = Counter('http_requests_total', 'Requests', ['method'])
reqs.labels(method='GET').inc()
start_http_server(8000)
```

---
## Naming Conventions

- snake_case
- Suffix unit: `_seconds`, `_bytes`
- Suffix `_total` for counters
- Subsystem prefix: `http_`, `db_`

---
## What to Measure

- The four golden signals
- Latency, traffic, errors, saturation
- Cover these for any service

---
## RED Method

- Rate, Errors, Duration
- For request-driven services
- Quick observability win

---
## USE Method

- Utilisation, Saturation, Errors
- For resources (CPU, disk)
- Brendan Gregg

---
## Histogram Buckets

- Pick by your latency profile
- Default buckets often too narrow or wide
- Don't change buckets often (breaks comparisons)

---
## Avoid High Cardinality

- No user_id, request_id labels
- Coarse-grained labels only
- Prometheus is not for tracing

---
## Common Instrumentation Mistakes

- High-cardinality labels in tight loops
- Counters exposed as gauges
- No unit suffix; ambiguous
- Reusing the same metric for unrelated things
- Adding labels per ad-hoc need
