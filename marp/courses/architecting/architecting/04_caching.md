# Caching Strategies and Content Delivery Networks
## Modern Architecture Course

<!-- Add Mermaid.js support -->
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({ startOnLoad: true });
</script>

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

<div class="mermaid">
graph LR
Client[Client] --> Cache[Cache]
Cache -->|Hit| Client
Cache -->|Miss| DB[(Database)]
DB -->|Data| Cache
Cache -->|Data| Client
Cache -.->|Update| TTL[TTL/Expiry]
</div>

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
    return database.query(f"SELECT * FROM users WHERE id = {user_id}")
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

<div class="mermaid">
sequenceDiagram
participant App
participant Cache
participant DB
App->>Cache: 1. Check cache
alt Cache miss
Cache-->>App: Not found
App->>DB: 2. Query database
DB-->>App: Return data
App->>Cache: 3. Update cache
else Cache hit
Cache-->>App: Return cached data
end
</div>

---

## Write-Through Pattern

<div class="mermaid">
sequenceDiagram
participant App
participant Cache
participant DB
App->>Cache: 1. Write data
Cache->>DB: 2. Write to database
DB-->>Cache: Confirm write
Cache-->>App: 3. Confirm write
Note over Cache: Data written to both<br/>cache and DB synchronously
</div>

---

## Write-Behind Pattern

<div class="mermaid">
sequenceDiagram
participant App
participant Cache
participant Queue
participant DB
App->>Cache: 1. Write data
Cache-->>App: 2. Confirm write
Cache->>Queue: 3. Queue write
Note over Queue: Async processing
Queue->>DB: 4. Write to database (later)
DB-->>Queue: Confirm write
</div>

---

## Cache Invalidation Strategies

1. Time-Based (TTL)
1. Event-Based
1. Version-Based
1. LRU (Least Recently Used)
1. LFU (Least Frequently Used)

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

## Content Delivery Networks (CDNs)

- Distributed network of servers
- Caches content closer to users
- Reduces latency
- Improves availability
- Provides DDoS protection

---

## CDN Architecture

<div class="mermaid">
graph TB
U1[User US] --> E1[Edge Server US]
U2[User EU] --> E2[Edge Server EU]
U3[User Asia] --> E3[Edge Server Asia]
E1 --> O[Origin Server]
E2 --> O
E3 --> O
E1 -.->|Cache| C1[(Cache)]
E2 -.->|Cache| C2[(Cache)]
E3 -.->|Cache| C3[(Cache)]
</div>

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

<div class="mermaid">
graph LR
subgraph "Edge Layer"
D1[IoT Device] --> EC1[Edge Compute]
D2[Sensor] --> EC1
EC1 --> EG[Edge Gateway]
end
subgraph "Cloud Layer"
EG --> CS[Cloud Services]
CS --> AI[AI/ML Processing]
CS --> ST[(Storage)]
end
EC1 -.->|Local Processing| LP[Low Latency]
CS -.->|Heavy Processing| HP[High Compute]
</div>

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

<div class="mermaid">
graph TB
subgraph "Metrics Collection"
C[Cache] --> M[Metrics Collector]
M --> HR[Hit Rate]
M --> MR[Miss Rate]
M --> L[Latency]
M --> E[Eviction Rate]
end
HR --> D[Dashboard]
MR --> D
L --> D
E --> D
D --> A[Alerts]
D --> R[Reports]
</div>

---

## Best Practices

1. Set Appropriate TTLs
1. Use Cache Keys Wisely
1. Implement Circuit Breakers
1. Monitor Performance
1. Plan for Failures
1. Regular Cache Maintenance
