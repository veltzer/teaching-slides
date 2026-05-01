---
tags:
  - observability:opentelemetry
level: intermediate
category: observability
audience:
  - audiences:devops

---
# Logs

---
## What This Chapter Covers

- Why logs in OTel
- Log model
- Bridging existing loggers
- Correlation with traces
- Best practices

---
## Why Logs in OTel

- Unified telemetry
- Correlate with traces and metrics
- Same pipeline (collector)
- Stable since 2023

---
## Log Model

- Timestamp
- Severity
- Body
- Attributes
- Resource

---
## Body

- The message
- String or structured
- Don't put PII

---
## Attributes

- Structured key-value
- Searchable in backends
- Add request id, user id (at the right level)

---
## Severity

- TRACE, DEBUG, INFO, WARN, ERROR, FATAL
- OTel spec defines numbers
- Backends filter by severity

---
## Bridging Loggers

- log4j, logback (Java)
- logging (Python)
- zap, logrus (Go)
- Bridge appenders forward to OTel

---
## Sample Bridge

- Existing app logs to logback
- Logback OTel appender forwards to collector
- No code changes

---
## Correlation

- Logs include trace_id and span_id
- Backends link logs to traces
- Click trace, see its logs

---
## Structured Logging

- Key-value pairs, not free text
- Parsable, queryable
- Standard practice; OTel embraces it

---
## Sample Structured Log

```json
{
  "severity": "INFO",
  "body": "order processed",
  "attributes": {
    "order.id": 123,
    "duration_ms": 45
  },
  "trace_id": "abc..."
}
```

---
## Don't Log Everything

- INFO for important business events
- DEBUG for development
- Avoid logging high-frequency loops
- Costs add up

---
## Sampling Logs

- Filter at SDK or collector
- Drop noisy debug logs in prod
- Keep all errors

---
## Replacing Old Pipelines

- Many start: Fluentd or Filebeat
- Move to OTel collector
- One pipeline for all signals

---
## Common Log Mistakes

- Logs without trace correlation
- Free-text logs; hard to query
- Logging PII or secrets
- Too verbose at INFO
- Two log pipelines in parallel forever
