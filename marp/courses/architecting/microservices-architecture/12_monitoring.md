---
tags:
  - concepts:microservices
  - concepts:observability
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:devops

---
# Monitoring and Observability

---
## Three Pillars

- **Logs**: discrete events, time-stamped
- **Metrics**: numerical time series (rate, latency, error count)
- **Traces**: distributed call paths across services
- All three together = observability

---
## Why Observability Matters in Microservices

- A single user request touches many services
- Local logs don't tell the full story
- "Where did it slow down?" needs a trace
- "How often does this happen?" needs metrics
- "What was the user-visible message?" needs logs

---
## Structured Logs

- One log line = one JSON object
- Searchable, filterable, alertable
- Common fields: timestamp, level, service, trace_id, message
- See twelve-factor course chapter 11

---
## Correlation IDs

- A unique id for a user request, propagated across all services it touches
- Tied to all logs, metrics, traces for that request
- The ability to ask "everything that happened for request X" follows from this
- Without correlation IDs, distributed debugging is guesswork

---
## Metrics

- Counters: rate of events (requests/sec, errors/sec)
- Gauges: current value (active connections, queue depth)
- Histograms: distributions (request duration p50, p99)
- Tools: Prometheus, Datadog, CloudWatch, OpenTelemetry

---
## The RED Method

- **Rate**: how many requests per second
- **Errors**: how many of them failed
- **Duration**: how long they took
- A good baseline for service-level metrics
- Pair with USE (Utilization, Saturation, Errors) for resources

---
## Distributed Tracing

- Each cross-service call adds a span to a trace
- Spans show parent-child relationships and timing
- The full trace shows the entire path of a request
- Tools: OpenTelemetry, Jaeger, Zipkin, Tempo

---
## Trace Propagation

- The first service generates a trace_id
- It includes the trace_id in headers when calling the next service
- Each service adds spans under that trace_id
- One id ties the whole flow together

---
## Tracing Headers

- W3C Trace Context: `traceparent`, `tracestate`
- Standard across vendors
- Most modern HTTP libraries propagate it automatically
- Make sure async messages also carry trace context

---
## OpenTelemetry

- Vendor-neutral standard for telemetry
- One instrumentation library; many backends
- Logs, metrics, and traces all under one model
- Increasingly the default for new systems

---
## Alerts

- Alerts come from metrics, occasionally logs
- Alert on user-visible symptoms first (latency, errors)
- Avoid alerting on every minor anomaly
- Each alert should have a runbook

---
## Service-Level Indicators (SLIs)

- A measurable property of the service
- "99% of requests complete under 200ms"
- "0.01% of requests return 5xx"
- The numbers behind your SLOs

---
## Service-Level Objectives (SLOs)

- A target for an SLI
- "p99 latency under 200ms, measured monthly"
- A breach triggers attention; persistent breaches block deploys
- Communicates reliability goals across teams

---
## Error Budgets

- "We allow 0.1% of requests to fail per month"
- If you stay under, you can deploy aggressively
- If you exceed, you slow down and fix reliability
- Aligns dev and ops on a shared metric

---
## Dashboards

- One per service: RED metrics, dependencies, error rates
- One global: overall system health
- One per critical user flow: end-to-end
- Built before incidents, not during

---
## Anti-Patterns

- "We'll add observability later"
- Logs without correlation IDs
- Metrics without alerts
- Alerts without runbooks
- Tracing in only some services (trace breaks at the boundary)

---
## Summary

- Logs, metrics, traces — all three from day one
- Correlation IDs propagate across services
- OpenTelemetry is the standard
- SLIs/SLOs/error budgets align teams
- Build dashboards before you need them
