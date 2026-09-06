---
tags:
  - networking:rest
  - practices:performance
level: intermediate
category: networking
audience:
  - audiences:developers

---

# Performance and Best Practices

---

## What This Chapter Covers

- Caching
- Pagination
- Compression
- Batching
- Monitoring
- Putting it together

---

## Performance Levers

![perf_levers](svg/courses/networking/restful-apis/09_performance_and_best_practices/perf_levers.svg)

---

## Caching

- HTTP caching: built-in
- Cache-Control: max-age, public, private
- ETag: validate freshness
- Last-Modified: alternative

---

## ETag Flow

- Server sends ETag
- Client sends If-None-Match
- Server returns 304 Not Modified if unchanged
- Saves bandwidth

---

## Pagination

- Don't return huge lists
- Cap default page size
- Provide cursor or page links
- Document limits

---

## N+1 Problem

- One request per item
- Solution: batch endpoints, embedding, GraphQL
- Common API anti-pattern

---

## Compression

- gzip, brotli
- Big savings for JSON
- Negotiate via Accept-Encoding

---

## Connection Reuse

- HTTP keep-alive
- HTTP/2 multiplexing
- Connection pools client-side

---

## Async Endpoints

- Long jobs: 202 Accepted, return job URL
- Poll or webhook
- Don't block clients

---

## Idempotency

- Safe to retry
- POST: Idempotency-Key header
- Critical for unstable networks
- Used by Stripe, others

---

## Rate Limiting

- Protect server
- Inform client: 429 + Retry-After
- Per-key buckets
- Tiered by plan

---

## Monitoring

- Latency: p50, p95, p99
- Error rate by endpoint
- Throughput
- Alert on regressions

---

## Logging

- Request, status, latency
- Correlation ID for tracing
- Don't log secrets
- Sample at high traffic

---

## Tracing

- Distributed tracing
- OpenTelemetry standard
- Propagate trace headers
- Find bottlenecks across services

---

## Testing

- Contract tests vs OpenAPI
- Load tests for hot paths
- Chaos: simulate failures
- Mock external dependencies

---

## REST Best Practices Recap

- Resources, not actions
- Standard status codes
- Consistent shapes
- Documented and versioned
- HTTPS, auth, rate limits
- Cached, paginated, monitored

---

## Common Performance Mistakes

- No caching headers
- Returning huge unbounded lists
- N+1 patterns forcing many round trips
- Synchronous long-running endpoints
- No latency monitoring

---

## HTTP Caching Layers

![cache_layers](svg/courses/networking/restful-apis/09_performance_and_best_practices/cache_layers.svg)
