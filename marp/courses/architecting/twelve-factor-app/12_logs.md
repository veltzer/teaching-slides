---
tags:
  - concepts:architecture
  - concepts:observability
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:devops

---
# Factor XI: Logs

---
## The Rule

- Treat logs as event streams
- Write to stdout/stderr
- The app does not manage log files

---
## Streams Not Files

![logs_as_streams](svg/courses/architecting/twelve-factor-app/12_logs/logs_as_streams.svg)

---
## Logs Are Streams

- A log is a time-ordered stream of events
- The app produces events; something else collects, routes, and stores them
- The app should not know or care where logs end up
- Decoupling: the app's job is to emit; routing is operational

---
## Writing to stdout/stderr

- Every language can write to stdout
- Every container runtime captures stdout
- Every Kubernetes setup forwards stdout to a log aggregator
- It's the universal standard

---
## What the App Does NOT Do

- Open log files
- Rotate log files
- Compress old logs
- Ship logs to a remote service from inside the app
- All of these are the platform's responsibility

---
## Why This Decoupling Helps

- Replace log routing without changing the app
- Send logs to local file in dev, to ELK in staging, to Datadog in prod
- The app is portable across all of them
- Aggregation, filtering, alerting are all infrastructure concerns

---
## Structured Logging

- One log line = one event = one JSON object
- Fields: timestamp, severity, message, correlation_id, custom attributes
- Machines parse them; humans skim them
- Searchable, filterable, alertable

---
## Structured Log Example

```json
{"ts": "2026-01-15T14:23:00Z", "level": "info", "msg": "order placed",
 "order_id": "42", "customer_id": "c1", "total": 95}
```

- Easy to query: `level:info AND msg:"order placed"`
- Easy to alert: `level:error AND service:payments`
- Plain-text logs are harder to query at scale

---
## Log Levels

- `DEBUG`: developer detail; off in production by default
- `INFO`: normal operation milestones
- `WARN`: unexpected but recoverable
- `ERROR`: something failed and the user might be affected
- `FATAL`: the process is going down
- Use them deliberately, not as commentary

---
## Anti-Patterns

- Hardcoded log file paths
- Log shipping logic inside the app
- Plain-text logs at scale (impossible to search)
- Log levels that mean nothing (`INFO` for "the loop iterated")
- Sensitive data in logs (passwords, tokens, full credit card numbers)

---
## Log Aggregation Stack

- App writes to stdout
- Container runtime captures stdout per container
- Log shipper (Fluent Bit, Promtail) tails container logs
- Aggregator (Elasticsearch, Loki, Datadog) stores and indexes them
- UI (Kibana, Grafana, Datadog) queries and alerts

---
## Tracing Complements Logging

- Logs answer "what happened?"
- Traces answer "what called what, and how long?"
- Metrics answer "how often, how much?"
- All three together = observability
- Correlation IDs tie them together

---
## Summary

- Logs are event streams; write to stdout
- Don't manage log files inside the app
- Use structured JSON
- Apply log levels with discipline
- The platform handles aggregation and alerting
