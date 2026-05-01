---
tags:
  - observability:tracing
level: intermediate
category: observability
audience:
  - audiences:devops
  - audiences:developers

---
# Introduction to Jaeger

---
## What This Chapter Covers

- What distributed tracing is
- Why Jaeger
- Core concepts
- Architecture
- Course outline

---
## What Distributed Tracing Is

- Track a request across services
- See where time is spent
- Identify dependencies
- Debug distributed systems

---
## Why Tracing

- Logs are local
- Metrics are aggregated
- Traces follow one request
- Bridge gap between local and global

---
## Why Jaeger

- Open source
- Native to cloud-native systems
- Open standards compatible
- Wide language support

---
## Origins

- Born at Uber
- Donated to CNCF
- Inspired by Dapper
- Strong ecosystem now

---
## Trace

- One request from start to end
- Spans tree across services
- Identified by trace ID
- Stitched from many spans

---
## Span

- Named operation in a trace
- Has start and end times
- Has parent and children
- Has tags and logs

---
## Tags

- Key-value metadata
- HTTP method, status, user ID
- Useful for filtering
- Indexed on storage

---
## Logs Within Spans

- Time-stamped events
- Tied to the span
- Show what happened during the operation
- Smaller than full logs

---
## Sampling

- Most traces dropped to save cost
- Sampling decision at root
- Or tail-based for interesting ones
- Tune to budget

---
## Architecture

- Agents collect spans
- Collectors aggregate
- Storage backend
- Query and UI

---
## Storage Backends

- Cassandra
- Elasticsearch / OpenSearch
- Memory for testing
- Cloud-managed services

---
## OpenTelemetry Compatibility

- Receive standard protocol
- Existing instrumentation libraries work
- Less vendor lock-in
- Industry default

---
## Course Outline

- Instrumentation
- Trace exploration
- Sampling
- Operations
- Pitfalls

---
## Common Beginner Mistakes

- Trace everything at 100%
- No service name conventions
- Missing parent-child links
- Sensitive data in tags
- No retention plan
