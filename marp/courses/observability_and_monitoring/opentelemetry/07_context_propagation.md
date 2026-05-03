---
tags:
  - observability:opentelemetry
level: intermediate
category: observability
audience:
  - audiences:devops

---
# Context Propagation

---
## traceparent header

![w3c_traceparent](svg/courses/observability_and_monitoring/opentelemetry/07_context_propagation/w3c_traceparent.svg)

---
## What This Chapter Covers

- Why context matters
- W3C trace context
- Baggage
- Cross-protocol propagation
- Async boundaries
- Common pitfalls

---
## Why Context Matters

- Trace must span services
- Context flows alongside data
- Without it: each service is its own island

---
## W3C Trace Context

- traceparent header: trace_id, span_id, flags
- tracestate header: vendor-specific data
- Standard across libraries and vendors

---
## traceparent Format

- Version-traceID-spanID-flags
- e.g., 00-abc...-def...-01
- Server reads incoming; outgoing requests use child span

---
## Baggage

- Key-value data alongside trace context
- Propagated across boundaries
- Use for: user id, tenant, feature flag

---
## Two Headers Compared

![baggage_vs_traceparent](svg/courses/observability_and_monitoring/opentelemetry/07_context_propagation/baggage.svg)

---
## Sample Baggage

- "user.tenant=acme"
- "feature.v2=enabled"
- Carried through all services
- Don't put secrets

---
## HTTP Propagation

- Auto by instrumented libraries
- Reads incoming traceparent
- Writes outgoing for every HTTP call

---
## gRPC Propagation

- Metadata carries headers
- Auto in instrumented gRPC
- Same format as HTTP

---
## Messaging

- Kafka: headers
- RabbitMQ: properties
- SQS: message attributes
- Producer adds; consumer reads

---
## Async Workers

- Job published with context
- Worker reads context, starts span as child
- Trace spans the async boundary

---
## Goroutines / Threads

- Context passes via parameter
- Don't lose it across thread boundaries
- Some SDKs need explicit handoff

---
## Cross-Language

- Same standard headers
- Java client to Python service: still one trace
- Standardisation is the win

---
## Common Propagation Mistakes

- Reading body before context
- Not propagating across queues; broken traces
- Overusing baggage; large headers
- Propagator misconfigured (B3 vs W3C)
- Lost context across thread pools
