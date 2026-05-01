---
tags:
  - architecture:api-gateway
  - practices:observability
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# Monitoring and Observability

---
## What This Chapter Covers

- Why observability matters at the gateway
- Logging
- Metrics
- Distributed tracing
- Alerting
- Tools and integrations
- A solid baseline

---
## Why At The Gateway

- The gateway sees every request
- One place to instrument
- Knows: latency, status, route, consumer
- Single source of truth for API traffic
- The most-leveraged observability point

---
## What To Log

- Request: method, path, query params, headers (selectively)
- Response: status, latency, size
- Consumer: user / API key
- Trace ID for correlation
- Don't log: bodies, secrets, PII

---
## Structured Logging

- JSON, not free text
- Parseable by log tools
- Consistent fields across all logs
- Standard fields: timestamp, level, trace_id, request_id, ...
- The modern default

---
## Sampling

- High-traffic APIs generate too much log
- Sample: log 1 in 100, or 100% of errors
- Keep all errors; sample successes
- Reduces cost; preserves the signal
- Most gateways support this

---
## Metrics

- Request rate (per route, per consumer)
- Error rate (per status code)
- Latency (p50, p95, p99)
- Cache hit ratio
- Active connections
- All emitted by the gateway

---
## RED Method

- **Rate**: requests per second
- **Errors**: failed request rate
- **Duration**: how long requests take
- Three metrics; covers 80% of monitoring needs
- Per route, per consumer

---
## USE Method

- **Utilisation**: how busy is each resource
- **Saturation**: how queued is each resource
- **Errors**: failure count
- For the gateway itself (CPU, memory, connections)
- RED for the API; USE for the host

---
## Distributed Tracing

- One request &#8594; many service calls
- Trace ID propagates across services
- Each service emits spans
- Reconstruct the full call graph
- Tools: Jaeger, Tempo, Honeycomb, AWS X-Ray

---
## OpenTelemetry

- Industry-standard tracing / metrics SDK
- Vendor-neutral
- Most gateways have OTel integrations
- Propagates trace context (`traceparent` header)
- The strategic bet for observability

---
## Trace Context Propagation

- Gateway adds trace ID if missing; passes along
- Backend services see the same trace ID
- Tools stitch spans into a tree
- "What happened in this single request" — visible at a glance

---
## Alerts

- Error rate > X% for 5 minutes
- p99 latency > Y ms for 5 minutes
- Drop in request rate (suggests outage upstream)
- Cache hit ratio collapses (cache problem)
- Tune thresholds over time

---
## Dashboards

- Standard: requests, errors, latency over time
- Per route, per consumer
- Drill-down to individual traces
- Public: dashboard for SLA reporting
- Internal: detailed for ops

---
## Tools

- **Prometheus + Grafana**: open-source standard
- **Datadog**: hosted; expensive; polished
- **New Relic**: hosted; APM-focused
- **Honeycomb**: tracing-focused; high cardinality
- **Cloud-native**: CloudWatch, Stackdriver, Azure Monitor

---
## Common Observability Mistakes

- Logging request bodies (storage cost; PII risk)
- No trace context propagation (siloed traces)
- Metrics without dashboards
- Alerts that fire constantly (alert fatigue)
- Sampling without preserving errors

---
## Course Wrap-Up

- API gateways centralise cross-cutting concerns
- Architecture: monolith, microservices, BFF, multi-region
- Tools: Kong, AWS API Gateway, Envoy, others
- Rate limiting, auth, transformation, caching: per-route policy
- Observability is the gateway's superpower
- Done well: one team owns the gateway; everyone benefits
