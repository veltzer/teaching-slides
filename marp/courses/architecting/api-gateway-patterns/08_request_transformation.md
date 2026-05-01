---
tags:
  - architecture:api-gateway
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# Request and Response Transformation

---
## What This Chapter Covers

- When to transform
- Header manipulation
- URL rewriting
- Body transformation
- Aggregation across services
- Anti-patterns
- Real-world examples

---
## Why Transform

- Legacy backends with awkward shapes
- Combine multiple services into one response
- Strip internal headers before responding
- Add headers for tracing / auth
- Bridge protocol differences (JSON in / XML out)

---
## Transforming Requests

- Add headers: tracing IDs, auth context
- Strip headers: internal metadata
- Rewrite URLs: legacy paths to new ones
- Modify body: rare; expensive
- Most transforms are header-level

---
## Transforming Responses

- Strip internal fields before returning
- Reshape: rename, restructure, filter
- Combine fields from multiple service responses
- Add caching / CORS headers
- Standardise error envelopes

---
## Header Manipulation Examples

```yaml
plugins:
  - name: request-transformer
    config:
      add:
        headers: ["X-Trace-Id:${request_id}"]
      remove:
        headers: ["X-Internal-Token"]
```

- Add tracing ID for downstream
- Remove internal-only auth
- Plugin-driven in most gateways

---
## URL Rewriting

```misc
/legacy/api/users/123 -> /v2/users/123
```

- Map old URLs to new services
- Useful during migrations
- Keep old URLs working; new traffic goes to new
- Strip-path option: include / exclude the prefix

---
## Body Transformation

- More expensive than header manipulation
- Requires parsing the body
- For JSON: pluck fields; rename; restructure
- For XML: usually don't bother — let services handle
- Use sparingly

---
## Aggregation

- One client request &#8594; multiple backend calls
- Gateway combines responses
- Saves round trips for the client
- Examples: BFF for mobile (one call gets profile + orders + notifications)
- Common for slow / mobile clients

---
## Aggregation Risks

- Slowest backend determines latency
- Partial failures complicate the response
- Caching is harder
- Often a sign that BFF should own this, not the gateway
- Gateway aggregation: keep simple

---
## GraphQL At The Gateway

- A different model: one endpoint; field-level resolution
- Backend can be many services
- GraphQL gateway aggregates
- Tools: Apollo Federation, GraphQL Mesh
- Powerful; significant complexity

---
## CORS

```yaml
plugins:
  - name: cors
    config:
      origins: ["https://example.com"]
      methods: [GET, POST]
      headers: [Content-Type, Authorization]
      credentials: true
```

- Browser-only concern
- Configure at the gateway
- Wildcards (`*`) only for public APIs
- Misconfigured CORS = mysterious frontend errors

---
## Compression

- Decompress request bodies
- Compress response bodies (gzip, br)
- Reduces bandwidth; small CPU cost
- Most gateways do this transparently
- Verify it's enabled

---
## Logging Sensitive Data

- Default request/response logging may include passwords, tokens
- Configure: redact specific fields
- Or: log only what you need (URL, method, status, latency)
- Compliance requirement
- Audit periodically

---
## Anti-Patterns

- Business logic in transformations
- Heavy body transforms in the hot path
- Aggregating tens of services in one request
- Using gateway as a microservice bus
- Transformations that hide rather than help

---
## Common Mistakes

- CORS misconfigured (missing methods, headers, origins)
- Transformations duplicating service logic
- Logging full request bodies including PII
- Aggregation where BFF would be cleaner
- Plugin order matters; getting it wrong (auth after rate limit, for example)
