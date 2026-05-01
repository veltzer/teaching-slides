---
tags:
  - observability:opentelemetry
level: intermediate
category: observability
audience:
  - audiences:devops

---
# Instrumentation

---
## What This Chapter Covers

- Auto vs manual
- Per-language SDKs
- Instrumenting frameworks
- Custom spans
- Best practices

---
## Auto-Instrumentation

- Agent or library wraps frameworks
- No code changes
- Common frameworks supported
- Fast onboarding

---
## Manual Instrumentation

- Explicit span creation
- For business-specific operations
- Combines with auto

---
## Per-Language SDKs

- Go, Python, Java, .NET, Node, Ruby
- Each: API + SDK packages
- Maturity varies

---
## Java Auto-Agent

- Attach JAR at JVM start
- Captures: HTTP, DB, queues, RPC
- Zero code change
- Most mature

---
## Sample Manual Span (Go)

```go
ctx, span := tracer.Start(ctx, "process-order")
defer span.End()

span.SetAttributes(attribute.String("order.id", id))
```

- Pass ctx; child spans link automatically

---
## Sample Manual Span (Python)

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("process-order") as span:
    span.set_attribute("order.id", id)
```

---
## Naming Spans

- Verb + noun: "process-order", "fetch-user"
- Same name across instances of same operation
- Aggregate well in backends

---
## Semantic Conventions

- Standard attribute names
- http.method, db.system, messaging.system
- Consistent across services and vendors

---
## Errors

- Mark span status ERROR
- Record exception as event
- Backends highlight automatically

---
## Span Granularity

- Too fine: noisy, expensive
- Too coarse: less insight
- Aim: one per logical operation

---
## Cross-Cutting Concerns

- Add common attributes globally
- service.name, deployment.environment
- Resource attributes apply to all telemetry

---
## Resource

- Identifies the producer
- service.name, host, container, k8s pod
- Set once at SDK init

---
## Library Instrumentation

- Many libraries publish OTel hooks
- Pick official packages
- Integrations registry: open-telemetry/instrumentation-*

---
## Common Instrumentation Mistakes

- Skipping auto-instrumentation; reinventing
- Forgetting resource attributes (service.name etc)
- Custom names where conventions exist
- Sensitive data in span attributes
- No tracing across async boundaries (workers, queues)
