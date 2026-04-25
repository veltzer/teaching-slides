---
tags:
  - concepts:architecture
  - concepts:caching
  - infrastructure:cdn
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Caching Strategies and Content Delivery Networks

---

## Agenda

1. Fundamentals of Caching
1. Types of Caches
1. Caching Strategies
1. Content Delivery Networks (CDNs)
1. Edge Computing
1. Future Trends

---

## What is Caching

- Temporary storage of data for faster access
- Reduces load on backend systems
- Improves application performance
- Reduces costs
- Enhances user experience

---

## Cache Hit vs Cache Miss

![cache_hit_vs_cache_miss](svg/courses/architecting/architecture-patterns/10_caching/cache_hit_vs_cache_miss.svg)

---

## Types of Caches

1. Browser Cache
1. Application Cache
1. CDN Cache
1. Database Cache
1. Object Cache
1. API Cache

---

## Browser Caching

```html
<!-- HTTP Headers Example -->
Cache-Control: max-age=31536000
ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"
Last-Modified: Wed, 15 Nov 2023 12:00:00 GMT
```

---

## Application Cache Example

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_user_data(user_id: str):
    # Expensive database operation
    return database.query("SELECT * FROM users WHERE id = %s", (user_id,))
```

---

## Redis Caching Example

```python
import redis

redis_client = redis.Redis(host='localhost', port=6379)

def get_product(product_id):
    # Try to get from cache
    cached = redis_client.get(f"product:{product_id}")
    if cached:
        return json.loads(cached)

    # Get from database
    product = database.get_product(product_id)

    # Store in cache for 1 hour
    redis_client.setex(
        f"product:{product_id}",
        3600,
        json.dumps(product)
    )
    return product
```

---

## Caching Strategies

1. Cache-Aside
1. Write-Through
1. Write-Behind
1. Refresh-Ahead

---

## Cache-Aside Pattern

![cache_aside_pattern](svg/courses/architecting/architecture-patterns/10_caching/cache_aside_pattern.svg)

---

## Write-Through Pattern

![write_through_pattern](svg/courses/architecting/architecture-patterns/10_caching/write_through_pattern.svg)

---

## Write-Behind Pattern

![write_behind_pattern](svg/courses/architecting/architecture-patterns/10_caching/write_behind_pattern.svg)

---

## Cache Invalidation Strategies

1. Time-Based (TTL) — expire entries after a fixed duration
1. Event-Based — invalidate when the underlying data changes
1. Version-Based — bake a version key into the cache key; old versions are ignored
1. LRU (Least Recently Used) — evict by access recency
1. LFU (Least Frequently Used) — evict by access frequency

---

## Why Invalidation Is Hard

- "There are only two hard things in CS: cache invalidation and naming things" — Phil Karlton
- The cache and the source of truth are two systems; they drift
- Invalidation is a distributed-systems problem in disguise
- Every strategy trades freshness against load on the source of truth

---

## Time-Based Invalidation Example

```python
from datetime import timedelta
from django.core.cache import cache

# Cache data with TTL
def get_trending_posts():
    cached = cache.get('trending_posts')
    if cached:
        return cached

    posts = Post.objects.filter(is_trending=True)
    # Cache for 15 minutes
    cache.set('trending_posts', posts, timeout=900)
    return posts
```

---

## TTL Trade-Offs

- Simple to implement; no coordination needed between writers and cache
- Stale reads are bounded by the TTL value
- Short TTL: fresher data, more load on the source
- Long TTL: less load, more stale reads
- Cannot react to writes between TTL expirations
- Best for data where bounded staleness is acceptable (rankings, counts, summaries)

---

## Event-Based Invalidation

- Writers publish an invalidation event when data changes
- Cache subscribes and evicts the affected key
- Reduces stale reads compared to TTL alone
- Failure modes:
    - Lost events leave the cache permanently stale
    - Out-of-order events can re-cache stale data after a write
    - Network partitions split cache and writers
- Often combined with a TTL backstop to bound staleness if events are lost

---

## Version-Based Invalidation

- The cache key includes a version (`user:42:v17`)
- A new write bumps the version; old keys are no longer read
- Old entries linger until evicted by capacity policy (LRU/LFU)
- Pros: never serve stale data; eviction is automatic
- Cons: cache fills with dead entries; needs aggressive capacity eviction
- Useful when writes are rare and stale reads are unacceptable

---

## Cache Coherence in Distributed Caches

- Multiple cache nodes must agree on invalidation
- Common approaches:
    - Broadcast invalidate to all nodes (works at small scale)
    - Consistent hashing — each key has one owner; only that node caches it
    - Quorum reads/writes against the cache (rare, expensive)
- The harder the coherence guarantee, the more it looks like a database

---

## Stampedes and the Thundering Herd

- A popular key expires; many requests miss simultaneously
- All of them hit the source of truth at once
- Mitigations:
    - Probabilistic early expiration (refresh shortly before TTL)
    - Single-flight: one request fetches, others wait
    - Stale-while-revalidate: serve stale, refresh in background
    - Lock or lease for the duration of the recompute

---

## Choosing an Invalidation Strategy

| Strategy | Freshness | Complexity | When to use |
|---|---|---|---|
| TTL | bounded by TTL | low | bounded staleness OK; rankings/aggregates |
| Event-based | near-real-time | medium | writes drive cache; loss is tolerable |
| Version-based | strong | medium | rare writes; no stale reads allowed |
| TTL + events | near-real-time + bounded | medium-high | events with safety net |
| LRU/LFU | n/a (capacity) | low | always pair with one of the above |

---

## Content Delivery Networks (CDNs)

- Distributed network of servers
- Caches content closer to users
- Reduces latency
- Improves availability
- Provides DDoS protection

---

## CDN Architecture

![cdn_architecture](svg/courses/architecting/architecture-patterns/10_caching/cdn_architecture.svg)

---

## CDN Configuration Example

```nginx
# Nginx CDN Configuration
location /static/ {
    proxy_cache my_cache;
    proxy_cache_use_stale error timeout http_500 http_502 http_503 http_504;
    proxy_cache_valid 200 302 1h;
    proxy_cache_valid 404 1m;
    proxy_cache_key $scheme$proxy_host$request_uri;
}
```

---

## Cache Headers in CDN

```http
# Response Headers
X-Cache: HIT
X-Cache-Hit: 1
X-Cache-Location: dal
Cache-Control: public, max-age=86400
Vary: Accept-Encoding
```

---

## Edge Computing

- Processing at network edge
- Reduces latency further
- Enables real-time applications
- Supports IoT and 5G use cases

---

## Edge Computing Architecture

![edge_computing_architecture](svg/courses/architecting/architecture-patterns/10_caching/edge_computing_architecture.svg)

---

## Edge Function Example

```javascript
// Cloudflare Worker Example
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  // Get from cache first
  const cache = caches.default
  let response = await cache.match(request)

  if (!response) {
    // Process at edge
    response = await processAtEdge(request)
    // Cache the response
    await cache.put(request, response.clone())
  }

  return response
}
```

---

## Cache Warming Strategies

1. Preemptive Caching
1. Progressive Loading
1. Predictive Caching
1. Background Refresh

---

## Predictive Caching Example

```python
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

def predict_cache_needs():
    # Analyze access patterns
    access_patterns = get_access_logs()

    # Train model
    model = LogisticRegression()
    model.fit(access_patterns)

    # Predict future needs
    future_needs = model.predict(upcoming_timeframe)

    # Warm up cache
    precache_content(future_needs)
```

---

## Future Trends in Caching

1. AI-Driven Cache Optimization
1. Edge Computing Integration
1. Serverless CDN Functions
1. Machine Learning for Prediction
1. Dynamic Content Caching

---

## AI-Driven Caching

```python
class SmartCache:
    def __init__(self):
        self.cache = {}
        self.ml_model = train_cache_model()

    def should_cache(self, content):
        features = extract_features(content)
        return self.ml_model.predict(features)[0]

    def cache_content(self, key, content):
        if self.should_cache(content):
            self.cache[key] = content
```

---

## Monitoring Cache Performance

Key Metrics:
- Hit Rate
- Miss Rate
- Latency
- Storage Usage
- Eviction Rate

---

## Cache Monitoring Dashboard

![cache_monitoring_dashboard](svg/courses/architecting/architecture-patterns/10_caching/cache_monitoring_dashboard.svg)

---

## Best Practices

1. Set Appropriate TTLs
1. Use Cache Keys Wisely
1. Implement Circuit Breakers
1. Monitor Performance
1. Plan for Failures
1. Regular Cache Maintenance
