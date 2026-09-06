---
tags:
  - networking:graphql
  - practices:performance
level: intermediate
category: networking
audience:
  - audiences:developers

---

# Performance

---

## What This Chapter Covers

- N+1 problem
- DataLoader
- Caching
- Persisted queries
- Complexity analysis

---

## N+1 Problem

- Query for posts, then per post: query author
- 1 + N queries
- Slow at scale
- Classic GraphQL pitfall

---

## Performance Levers

![perf_levers](svg/courses/networking/graphql/09_performance/perf_levers.svg)

---

## Caching Layers

![caching_layers](svg/courses/networking/graphql/09_performance/caching_layers.svg)

---

## DataLoader

- Batches keys within a tick
- Caches within request
- Returns Promise per key
- Standard solution

---

## Sample DataLoader

```javascript
const userLoader = new DataLoader(
    (ids) => db.usersByIds(ids)
);

// resolver
ctx.userLoader.load(post.authorId);
```

- Batched DB call

---

## Per-Request Cache

- DataLoader cache scoped to one request
- Avoids stale data
- Don't reuse across requests

---

## Response Caching

- Apollo Cache Control directives
- Whole or partial responses cached
- CDN integration with persisted queries

---

## Persisted Queries

- Pre-register query strings; send hash
- Smaller request payload
- Allow-list at server
- CDN-friendly

---

## CDN

- GET with persisted query hash
- Cacheable at edge
- Massive perf win for read-heavy

---

## Query Complexity Analysis

- Score each field
- Reject queries above threshold
- Prevent expensive queries
- Standard plugins

---

## Depth Limit

- Reject deeply nested queries
- Protect against malicious recursion
- Easy to add

---

## Server Tracing

- Apollo Tracing extension
- Per-resolver timing
- Find slow paths

---

## Database Optimisation

- Indexes on join keys
- Avoid SELECT *
- Project only needed columns

---

## Avoid Over-Fetching at the DB

- Field selection: GraphQL knows what is needed
- Use info to project
- Or: dedicated services per type

---

## Common Performance Mistakes

- Skipping DataLoader; n+1 in production
- No complexity or depth limit
- Returning whole rows when only id is needed
- Caching with PII baked in
- Sending huge query strings every request
