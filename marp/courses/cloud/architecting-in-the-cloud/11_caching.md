---
tags:
  - infrastructure:cloud
  - concepts:architecture
  - concepts:performance
level: intermediate
category: cloud
audience:
  - audiences:developers
  - audiences:architects
  - audiences:devops

---

# Caching

---

## Why Caching?
- Reduce latency (milliseconds -> microseconds)
- Reduce load on databases and backends
- Handle more traffic without scaling backend
- Save money (fewer database queries, less compute)
- Improve user experience

---

## Caching Layers

![layers](svg/courses/cloud/architecting-in-the-cloud/11_caching/caching_layers.svg)

---

## Caching Close to the Client
- CDN caching (CloudFront, Akamai, Fastly)
- Cache static assets at edge locations globally
- Reduce origin server load
- Lower latency for end users
- Cache HTML, CSS, JS, images, videos, API responses

---

## CDN Cache Behavior
- TTL (Time to Live): how long to cache
- Cache-Control headers from origin
- Cache invalidation when content changes
- Cache hit ratio: percentage served from cache
- Goal: high cache hit ratio (>90%)

---

## CDN Cache Strategies
- Cache everything with long TTL + invalidation on deploy
- Use versioned URLs (style.v2.css) for immutable assets
- Short TTL for dynamic content
- Cache personalized content with caution
- Separate static and dynamic paths

---

## Browser Caching
- Cache-Control and Expires headers
- ETags for conditional requests (304 Not Modified)
- Immutable assets with cache-busting URLs
- Service Workers for offline caching
- Reduces requests to CDN and origin

---

## API Gateway Caching
- Cache API responses at the gateway level
- AWS API Gateway: built-in caching
- TTL per endpoint
- Cache key based on request parameters
- Reduce backend invocations for repeated requests

---

## Application-Level Caching
- In-memory caches within the application
- Local cache: fastest, but per-instance only
- Distributed cache: shared across instances (Redis, Memcached)
- Cache database query results
- Cache computed values and aggregations

---

## Managed Cache Services
- AWS ElastiCache (Redis, Memcached)
- Azure Cache for Redis
- GCP Memorystore
- Fully managed: patching, failover, scaling
- Multi-AZ for high availability

---

## Redis Cache Example

```python
import redis

r = redis.Redis(host='my-cache.abc.cache.amazonaws.com',
                port=6379, decode_responses=True)

# Cache-aside pattern
def get_user(user_id):
    cached = r.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)

    user = db.query(f"SELECT * FROM users WHERE id={user_id}")
    r.setex(f"user:{user_id}", 3600, json.dumps(user))
    return user
```

---

## Redis vs Memcached
- Redis: rich data structures (lists, sets, sorted sets, hashes)
- Redis: persistence, replication, pub/sub
- Memcached: simpler, multi-threaded, pure caching
- Redis: better for most use cases
- Memcached: better for simple key-value at high throughput

---

## Cache-Aside Pattern: Details
1. Application checks cache for data
1. Cache hit: return data
1. Cache miss: query database
1. Store result in cache with TTL
1. Return data to caller

---

## Cache-Aside Pattern

![cache_aside](svg/courses/cloud/architecting-in-the-cloud/11_caching/cache_aside_pattern.svg)

---

## Write-Through Pattern
- Write to cache and database simultaneously
- Cache always has latest data
- Higher write latency (two writes)
- Guarantees cache consistency
- Good when reads significantly outnumber writes

---

## Write-Behind (Write-Back) Pattern
- Write to cache immediately
- Asynchronously write to database
- Very low write latency
- Risk of data loss if cache fails before flush
- Use for non-critical or recoverable data

---

## Cache Invalidation
- "The two hard things in CS: cache invalidation and naming things"
- TTL-based: simplest, eventual staleness
- Event-based: invalidate on data change
- Write-through: cache always current
- Versioned keys: new version = new cache key

---

## Cache Eviction Policies
- LRU (Least Recently Used): most common
- LFU (Least Frequently Used): keep popular items
- TTL (Time to Live): expire after time
- FIFO (First In, First Out): simple
- Choose based on access patterns

---

## Caching Anti-Patterns
- Caching everything (wastes memory)
- No TTL (stale data forever)
- Cache stampede (many misses at once overwhelm DB)
- Caching too little (cache hit ratio too low)
- Not monitoring cache effectiveness

---

## Cache Stampede Prevention
- Lock on cache miss (only one request refreshes)
- Probabilistic early expiration
- Background refresh before TTL expires
- Fallback to stale data while refreshing
- Critical for high-traffic applications

---

## Monitoring Cache Performance
- Cache hit ratio (target: >90%)
- Latency (cache hit vs miss)
- Memory utilization
- Eviction rate
- Number of connections

---

## DAX: DynamoDB Accelerator
- In-memory cache purpose-built for DynamoDB
- Microsecond read latency
- API compatible (drop-in replacement)
- Handles cache invalidation automatically
- Ideal for read-heavy DynamoDB workloads

---

## ElastiCache Architecture: Details
- Cluster mode: shard data across nodes
- Replication: primary + replicas per shard
- Multi-AZ for high availability
- Automatic failover to replicas
- Scale reads with replicas, data with shards

---

## ElastiCache Architecture

![elasticache](svg/courses/cloud/architecting-in-the-cloud/11_caching/elasticache_architecture.svg)

---

## Session Caching Pattern
- Store user sessions in Redis
- Faster than database lookups
- Shared across all application instances
- TTL for automatic session expiration
- Reduces database load significantly

---

## Full-Page Caching
- Cache entire rendered HTML pages
- Serve without hitting application code
- Varnish, CloudFront, or Redis
- Dramatically reduces server load
- Invalidate on content change

---

## Caching for Microservices
- Each service may have its own cache
- Shared cache for common data
- Distributed cache prevents data duplication
- Cache invalidation across services is complex
- Use events to propagate invalidation

---

## Warm-Up Strategies
- Pre-populate cache on deployment
- Gradual traffic shift to new instances
- Cache warming scripts run before going live
- Avoid cold cache causing database spike
- Critical for cache-dependent applications

---

## Caching Cost Considerations
- ElastiCache: instance cost per hour
- Right-size cache nodes based on data volume
- Use reserved nodes for steady-state caches
- Monitor memory utilization (target 70-80%)
- Over-provisioning cache is cheaper than DB overload

---

## Caching Best Practices
- Cache close to the consumer (CDN > app cache > DB cache)
- Set appropriate TTLs for each data type
- Monitor and tune cache hit ratios
- Plan for cache failure (fall back to database)
- Use consistent hashing for distributed caches
- Start caching early, optimize continuously
