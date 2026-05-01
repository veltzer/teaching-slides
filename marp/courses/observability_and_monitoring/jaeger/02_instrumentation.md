---
tags:
  - observability:tracing
level: intermediate
category: observability
audience:
  - audiences:devops
  - audiences:developers

---
# Instrumentation

---
## What This Chapter Covers

- Auto-instrumentation
- Manual spans
- Context propagation
- Tags and logs
- Common pitfalls

---
## Auto-Instrumentation

- Library hooks into HTTP, DB, queues
- No code changes needed
- Quick win
- Good baseline

---
## Manual Spans

- Wrap units of work
- Custom names
- Specific to your domain
- Add value beyond auto

---
## Span Lifecycle

- Start
- Set tags and logs
- Finish
- Sent asynchronously to collector

---
## Context Propagation

- Trace ID flows across calls
- Carried in HTTP headers
- Or message metadata
- Required for stitching

---
## Standard Headers

- W3C Trace Context preferred
- Older formats still common
- Mix carefully
- Test cross-service flows

---
## Service Names

- Stable naming convention
- Per service, not per process
- Useful for grouping
- Avoid renaming

---
## Span Names

- Operation, not URL
- "GET /users/:id" not full URL
- Low cardinality
- Stable across requests

---
## Tags

- Stable, low-cardinality keys
- HTTP status, method, route
- User ID only if needed and safe
- Avoid raw payloads

---
## Sensitive Data

- No PII in tags
- No secrets in tags
- Strip before sending
- Compliance dictates

---
## Errors

- Set error tag
- Add log with stack trace
- Helps trace search
- Distinguish from successes

---
## Sampling

- Head-based: decide at root
- Tail-based: decide after seeing trace
- Probabilistic by default
- Force-sample interesting requests

---
## Async Work

- Background workers create new spans
- Linked to parent
- Or new trace if conceptually separate
- Document the choice

---
## Common Instrumentation Mistakes

- High-cardinality span names
- Missing context propagation
- Sensitive data in tags
- 100% sampling everywhere
- No error tagging
