---
tags:
  - networking:grpc
  - concepts:metadata
level: intermediate
category: networking
audience:
  - audiences:developers

---
# Metadata, Errors, and Deadlines

---
## What This Chapter Covers

- Metadata: headers and trailers
- Status codes and rich error details
- Deadlines and propagation
- Cancellation
- Best practices for resilient calls

---
## What Is Metadata?

- Key-value pairs attached to a call
- Like HTTP headers, but typed for gRPC
- Sent at start (initial) and end (trailing) of a call
- Standard place for cross-cutting concerns
- Auth tokens, request IDs, tracing context

---
## Deadlines Propagate

![deadlines](svg/courses/networking/grpc/04_metadata_errors_deadlines/deadlines.svg)

---
## Initial vs Trailing Metadata

- Initial metadata — sent before the response body
- Trailing metadata — sent after the response (or stream)
- Most metadata is initial
- Trailing useful for "summary" data after a stream
- gRPC status code itself is a special trailer

---
## Setting Metadata (Client)

```go
ctx := metadata.AppendToOutgoingContext(ctx,
    "authorization", "Bearer "+token,
    "x-request-id", reqID,
)
resp, err := client.Method(ctx, req)
```

- Outgoing metadata via context
- Multiple values per key are allowed
- Bin-suffixed keys (`-bin`) are binary

---
## Reading Metadata (Server)

```go
md, ok := metadata.FromIncomingContext(ctx)
if !ok {
    return nil, status.Error(codes.InvalidArgument, "no metadata")
}
tokens := md.Get("authorization")
```

- From the request context
- Always check presence
- Multi-value friendly

---
## gRPC Status Codes

- `OK` — success
- `CANCELLED` — caller cancelled
- `INVALID_ARGUMENT` — bad request
- `NOT_FOUND` — entity missing
- `PERMISSION_DENIED` — auth ok but not allowed
- `UNAUTHENTICATED` — no/bad credentials
- `RESOURCE_EXHAUSTED` — quota/rate limit
- `INTERNAL` — server bug
- `UNAVAILABLE` — try again later

---
## Status Codes Visualized

![status_codes](svg/courses/networking/grpc/05_metadata_errors_deadlines/status_codes.svg)

---
## Returning Errors (Server)

```go
return nil, status.Error(codes.NotFound, "user 42 not found")
```

- Use the `status` package
- Code + message for client
- Avoid leaking internal details
- Map domain errors to status codes consistently

---
## Reading Errors (Client)

```go
resp, err := client.GetUser(ctx, req)
if err != nil {
    st, ok := status.FromError(err)
    if ok && st.Code() == codes.NotFound {
        // handle 404
    }
}
```

- Extract the status from the error
- Switch on the code
- Branch your retry logic accordingly

---
## Rich Error Details

- Status can carry typed details
- Use `errdetails` package: `RetryInfo`, `BadRequest`, etc
- Custom messages for domain-specific info
- Encoded as protobuf in the trailer
- Cleaner than parsing error strings

---
## Mapping to HTTP Codes

- `INVALID_ARGUMENT` → 400
- `UNAUTHENTICATED` → 401
- `PERMISSION_DENIED` → 403
- `NOT_FOUND` → 404
- `INTERNAL` → 500
- `UNAVAILABLE` → 503
- gRPC-Gateway and similar use these mappings

---
## What Is a Deadline?

- An absolute time by which the call must complete
- Different from a timeout (relative)
- Propagated across services automatically (with care)
- Server respects it; cancels work when reached
- The standard way to bound RPC calls

---
## Setting a Deadline

```go
ctx, cancel := context.WithDeadline(ctx, time.Now().Add(2*time.Second))
defer cancel()
resp, err := client.Method(ctx, req)
```

- Deadline is part of the context
- `cancel` releases resources promptly
- Callee inherits the deadline

---
## Deadline Propagation

- A receives request from B; A calls C
- Deadline from B's call should propagate to C
- Pass the same context — gRPC handles propagation
- Otherwise C might run after B has given up
- Wasted work; orphaned resources

---
## Detecting Deadline Exceeded (Server)

```go
select {
case <-ctx.Done():
    return ctx.Err()
default:
    // continue work
}
```

- Periodically check context cancellation
- Fast loops should still check
- Slow operations should be cancellable

---
## Cancellation

- Client can cancel before completion
- Manifests as ctx.Done() server-side
- Server should stop work and return
- Avoids wasted CPU and DB load
- A core resilience pattern

---
## Client-Side Cancellation

- `cancel()` on the context
- Useful when user navigates away
- Useful when one of many parallel calls succeeds
- Gracefully aborts the in-flight RPC

---
## Best Practices for Deadlines

- Set deadlines on every RPC; no infinite waits
- Tighter deadlines for retries
- Pass through inherited deadlines
- Monitor deadline-exceeded as a SLO breach
- Default deadlines per service tier

---
## The Deadline Hierarchy

- User-facing call: 5s budget
- Internal call A: 4s
- Internal call B (called by A): 3s
- Each step shrinks the budget
- Final services see the smallest deadline

---
## Common Pitfalls

- No deadline → calls hang under failure
- Generous deadlines that don't propagate
- Servers ignoring ctx.Done() and finishing dead work
- Returning generic INTERNAL for everything — losing semantics
- Putting auth tokens in proto fields instead of metadata

---
## Tracing via Metadata

- W3C Trace Context headers (`traceparent`, `tracestate`)
- gRPC libraries can propagate automatically
- Carries across service boundaries
- Pair with OpenTelemetry for end-to-end traces
- Critical for debugging async calls

---
## Summary

- Metadata: headers and trailers for cross-cutting concerns
- Status codes: standard semantic errors with rich details
- Deadlines: absolute time, propagated, respected
- Cancellation: stop work when client gives up
- Get these right and your RPC system will be debuggable
