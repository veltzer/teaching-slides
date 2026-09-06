---
tags:
  - observability:opentelemetry
level: intermediate
category: observability
audience:
  - audiences:devops

---

# Tracing Concepts

---

## What This Chapter Covers

- What tracing is
- Spans
- Traces
- Context propagation
- Span attributes
- Events and links

---

## Spans, Traces, Propagation

![spans_and_traces](svg/courses/observability_and_monitoring/opentelemetry/02_tracing_concepts/spans_and_traces.svg)

---

## What Tracing Is

- Track a request through services
- Identify bottlenecks
- Understand causality
- Distributed-systems debugging tool

---

## Span

- One unit of work
- Has: name, start, end, attributes, status
- Building block of traces

---

## What Lives Inside a Span

![span_anatomy](svg/courses/observability_and_monitoring/opentelemetry/02_tracing_concepts/span_anatomy.svg)

---

## Trace

- Tree of spans
- One root span
- Parent-child relationships
- Identified by trace_id

---

## Trace Diagram

- Service A starts root span
- Calls B; B is a child span
- B calls C; C is a child of B
- All share trace_id

---

## Context Propagation

- trace_id and parent span_id passed across boundaries
- Headers: traceparent (W3C)
- Carries context across HTTP, gRPC, queues

---

## W3C Trace Context

- Standard headers
- traceparent and tracestate
- Cross-vendor compatibility
- Replaces older formats

---

## Span Attributes

- Key-value tags
- service.name, http.method, db.statement
- Standard names: semantic conventions
- Searchable in backends

---

## Events

- Timestamped log within a span
- "Cache miss", "retry"
- Lighter than separate spans

---

## Links

- Connect spans across traces
- Batch of jobs from many traces
- Less common

---

## Status

- OK or ERROR
- Set on spans where appropriate
- Helps backends highlight failures

---

## Sampling

- Don't capture every trace
- Sample by rate, by tail decision, or by attribute
- Saves cost and storage

---

## Head Sampling

- Decide at trace start
- Random or rate-based
- Simple, cheap

---

## Tail Sampling

- Decide after trace finishes
- Keep errors and slow traces
- More expensive but smarter

---

## Common Tracing Mistakes

- No context propagation; broken traces across services
- Sampling at 100%; cost explosion
- Span names too generic
- Sensitive data in attributes
- Sampling at 0.001%; can't find problems
