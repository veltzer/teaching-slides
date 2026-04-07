# Caching with Redis

---

## What is Caching?

- Temporarily storing frequently accessed data in fast storage
- Reduces load on primary data source
- Improves response time and application performance
- Reduces costs (database queries, API calls, computation)

![what_is_caching](/svg/courses/databases/redis/03_caching/what_is_caching.svg)

---

## Why Redis for Caching?

- **Speed**: In-memory operations (~100,000 ops/sec)
- **Data structures**: Beyond simple key-value
- **TTL support**: Automatic expiration
- **Distributed**: Shared cache across application instances
- **Persistence**: Optional durability
- **Atomic operations**: No race conditions
- **Pub/Sub**: Cache invalidation support

---

## Cache Patterns

1. **Cache-Aside (Lazy Loading)**
1. **Write-Through**
1. **Write-Behind (Write-Back)**
1. **Read-Through**
1. **Refresh-Ahead**

---

## Cache-Aside Pattern

Application is responsible for cache interactions:

![cache_aside_pattern](/svg/courses/databases/redis/03_caching/cache_aside_pattern.svg)

---

## Cache-Aside Implementation

```python
def get_user(user_id):
    # Try to get from cache first
    cached_user = redis.get(f"user:{user_id}")

    if cached_user:
        return json.loads(cached_user)  # Cache hit

    # Cache miss - get from database
    user = db.query(f"SELECT * FROM users WHERE id = {user_id}")

    if user:
        # Store in cache with expiration
        redis.setex(
            f"user:{user_id}",
            CACHE_EXPIRY_SECONDS,
            json.dumps(user)
        )

    return user
```

---

## Write-Through Pattern

Every write goes to cache and database:

![write_through_pattern](/svg/courses/databases/redis/03_caching/write_through_pattern.svg)

---

## Write-Through Implementation

```python
def update_user(user_id, user_data):
    # Update database first
    db.execute(
        "UPDATE users SET name = %s, email = %s WHERE id = %s",
        user_data['name'], user_data['email'], user_id
    )

    # Update cache
    redis.setex(
        f"user:{user_id}",
        CACHE_EXPIRY_SECONDS,
        json.dumps(user_data)
    )

    return True
```

---

## Write-Behind Pattern

Writes go to cache first, then asynchronously to database:

![write_behind_pattern](/svg/courses/databases/redis/03_caching/write_behind_pattern.svg)

---

## Write-Behind Implementation

```python
def update_user_write_behind(user_id, user_data):
    # Update cache immediately
    redis.setex(
        f"user:{user_id}",
        CACHE_EXPIRY_SECONDS,
        json.dumps(user_data)
    )

    # Queue the database update
    redis.rpush(
        "db:write:queue",
        json.dumps({
            "operation": "update_user",
            "user_id": user_id,
            "data": user_data,
            "timestamp": time.time()
        })
    )

    return True
```

---

## Read-Through Pattern

Cache handles database interaction on miss:

![read_through_pattern](/svg/courses/databases/redis/03_caching/read_through_pattern.svg)

---

## Refresh-Ahead Pattern

Cache proactively refreshes before expiration:

![refresh_ahead_pattern](/svg/courses/databases/redis/03_caching/refresh_ahead_pattern.svg)

---

## Time-To-Live (TTL)

- Sets expiration time for cached items
- After TTL expires, key is automatically deleted
- Balance between freshness and cache hit rate

Commands:
```bash
EXPIRE key seconds        # Set TTL in seconds
EXPIREAT key timestamp    # Set TTL at UNIX timestamp
TTL key                   # Get remaining TTL (seconds)
PEXPIRE key milliseconds  # Set TTL in milliseconds
PERSIST key               # Remove expiration
```

---

## Setting TTL in Redis

Different ways to set TTL:

1. **With SET command**:
```bash
SET key value EX seconds
SET key value PX milliseconds
```

1. **After SET**:
```bash
SET key value
EXPIRE key seconds
```

1. **With pattern-based expiry**:
```bash
# Expire all session keys after 1 hour
SCAN 0 MATCH "session:*" COUNT 100
EXPIRE session:123 3600
```

---

## Cache Eviction Policies

Redis memory limits and eviction:

![cache_eviction_policies](/svg/courses/databases/redis/03_caching/cache_eviction_policies.svg)

---

## LRU vs LFU Eviction

![lru_vs_lfu_eviction](/svg/courses/databases/redis/03_caching/lru_vs_lfu_eviction.svg)

- LRU: `allkeys-lru`, `volatile-lru`
- LFU: `allkeys-lfu`, `volatile-lfu` (Redis 4.0+)

---

## Cache Invalidation Strategies

1. **Time-based invalidation**:
    - Set appropriate TTL values
    - Simplest approach

1. **Event-based invalidation**:
    - Explicitly delete cache entries on data change
    - More complex but more accurate

1. **Version-based invalidation**:
    - Include version in cache key
    - Update version on data change

---

## Event-Based Cache Invalidation

![event_based_cache_invalidation](/svg/courses/databases/redis/03_caching/event_based_cache_invalidation.svg)

---

## Cache Invalidation Implementation

```python
# When updating data
def update_item(item_id, data):
    # Update in database
    db.update_item(item_id, data)

    # Invalidate cache
    redis.delete(f"item:{item_id}")

    # Notify other application instances
    redis.publish("cache:invalidation", json.dumps({
        "type": "item",
        "id": item_id
    }))

# In application startup, subscribe to invalidation events
def setup_cache_invalidation_listener():
    pubsub = redis.pubsub()
    pubsub.subscribe("cache:invalidation")

    for message in pubsub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"])
            if data["type"] == "item":
                redis.delete(f"item:{data['id']}")
```

---

## Cache Stampede Problem

- When many requests try to rebuild cache simultaneously
- Occurs when popular keys expire or are invalidated
- Causes database overload

![cache_stampede_problem](/svg/courses/databases/redis/03_caching/cache_stampede_problem.svg)

---

## Preventing Cache Stampede

1. **Staggered expiration times**:
    - Add random jitter to TTL values

1. **External locking**:
    - One request rebuilds, others wait

1. **Background refresh**:
    - Update before expiration

1. **Early expiration**:
    - Return stale data while refreshing

---

## Cache Stampede Prevention: Locking

![cache_stampede_prevention_locking](/svg/courses/databases/redis/03_caching/cache_stampede_prevention_locking.svg)

---

## Cache Lock Implementation

```python
def get_with_lock(key, rebuild_func, lock_timeout=5, retry_count=3):
    # Try to get from cache first
    value = redis.get(key)
    if value:
        return json.loads(value)

    # Attempt to acquire lock
    lock_key = f"lock:{key}"
    lock_id = str(uuid.uuid4())

    # Use SET NX with timeout for atomic lock
    acquired = redis.set(lock_key, lock_id, ex=lock_timeout, nx=True)

    if acquired:
        try:
            # We got the lock, rebuild the cache
            value = rebuild_func()

            # Store in cache
            redis.setex(key, CACHE_EXPIRY, json.dumps(value))
            return value
        finally:
            # Release lock
            if redis.get(lock_key) == lock_id:
                redis.delete(lock_key)
    else:
        # We didn't get the lock, wait and retry from cache
        for _ in range(retry_count):
            time.sleep(0.1 * (2 ** _))  # Exponential backoff
            value = redis.get(key)
            if value:
                return json.loads(value)

        # Still no value after retries, rebuild without cache
        return rebuild_func()
```

---

## Distributed Caching Architecture

Multiple application instances using shared Redis cache:

![distributed_caching_architecture](/svg/courses/databases/redis/03_caching/distributed_caching_architecture.svg)

---

## Cache Consistency Models

1. **Strong consistency**:
    - Delete cache on write, refresh on read
    - Ensures always-fresh data
    - Higher latency, lower hit rate

1. **Eventual consistency**:
    - Update cache on write, set TTL
    - May serve stale data temporarily
    - Lower latency, higher hit rate

1. **Bounded staleness**:
    - Allow staleness up to a limit
    - Balance between consistency and performance

---

## Cache Hit Ratio Monitoring

![cache_hit_ratio_monitoring](/svg/courses/databases/redis/03_caching/cache_hit_ratio_monitoring.svg)

- Target hit ratio: 80%+ in most applications
- Monitor with `INFO stats` command
- Calculate hit ratio: `keyspace_hits / (keyspace_hits + keyspace_misses)`

---

## Caching Common Pitfalls

1. **Cache penetration**:
    - Queries for non-existent data
    - Solution: Cache negative results

1. **Cache breakdown**:
    - High-load failures when keys expire
    - Solution: Mutex locks or staggered expiry

1. **Cache avalanche**:
    - Many keys expire simultaneously
    - Solution: Add random jitter to TTL

1. **Thundering herd**:
    - Multiple processes rebuild cache at once
    - Solution: Leader election for rebuilds

---

## Caching Large Objects

Strategies for large objects:

1. **Compression**:
    - Store compressed data (gzip, lz4)
    - Trade CPU for memory

1. **Chunking**:
    - Split large objects into smaller pieces
    - `mset`/`mget` for retrieval

1. **Storage references**:
    - Store reference to data in external storage
    - Redis keeps metadata only

---

## Caching Small Objects: Hashes

Using Redis hashes for small objects:

![caching_small_objects_hashes](/svg/courses/databases/redis/03_caching/caching_small_objects_hashes.svg)

- Memory efficient for small objects
- Hash fields compression when appropriate

---

## Caching with Redis and Sessions

Session management with Redis:

```bash
# Store session
SETEX "session:$sessionId" 1800 "{userId: 123, role: 'user', ...}"

# Get session
GET "session:$sessionId"

# Update session (reset TTL)
SETEX "session:$sessionId" 1800 "{updatedData...}"

# Delete session on logout
DEL "session:$sessionId"
```

Benefits:
- Fast access
- Automatic expiration
- Centralized session storage
- Scalable across application instances

---

## Implementing Rate Limiting with Redis

![implementing_rate_limiting_with_redis](/svg/courses/databases/redis/03_caching/implementing_rate_limiting_with_redis.svg)

---

## Rate Limiting Implementation

```python
def rate_limit(user_id, limit=5, window=60):
    # Create a window key (user:window_timestamp)
    window_key = f"rate:{user_id}:{int(time.time() / window)}"

    # Increment counter for this window
    current = redis.incr(window_key)

    # Set expiration if this is first request in window
    if current == 1:
        redis.expire(window_key, window)

    # Check if over limit
    return current <= limit
```

Alternative using sorted sets:
- Track exact timestamps
- Sliding window instead of fixed window
- More precise but more complex

---

## Implementing Response Caching in Web Apps

```python
def get_product(product_id):
    # Try to get from cache
    cache_key = f"product:{product_id}"
    cached = redis.get(cache_key)

    if cached:
        return json.loads(cached)

    # Cache miss - get from database
    product = db.query(f"SELECT * FROM products WHERE id = {product_id}")

    if product:
        # Cache for 5 minutes
        redis.setex(cache_key, 300, json.dumps(product))

        # Also update product list cache expiry
        redis.expire("product:list", 300)

    return product

def invalidate_product_cache(product_id):
    # Delete specific product cache
    redis.delete(f"product:{product_id}")

    # Delete any lists that might contain this product
    redis.delete("product:list")
    redis.delete("product:featured")
```

---

## Implementing Cache Tags

Using Redis sets to manage cache tags:

```python
def set_with_tags(key, value, tags, ttl=3600):
    # Store the value
    redis.setex(key, ttl, value)

    # Add this key to each tag set
    for tag in tags:
        redis.sadd(f"tag:{tag}", key)

def invalidate_by_tag(tag):
    # Get all keys with this tag
    keys = redis.smembers(f"tag:{tag}")

    # Delete all keys
    if keys:
        redis.delete(*keys)

    # Delete the tag set itself
    redis.delete(f"tag:{tag}")
```

---

## Implementing a Tiered Cache

![implementing_a_tiered_cache](/svg/courses/databases/redis/03_caching/implementing_a_tiered_cache.svg)

Benefits:
- Reduced network calls
- Protect Redis from high load
- Better response times
- Fallback if Redis unavailable

---

## Monitoring Cache Performance

Key metrics to monitor:

1. **Hit rate**: Percentage of successful cache hits
1. **Miss rate**: Percentage of cache misses
1. **Latency**: Response time for cache operations
1. **Memory usage**: Current and peak memory usage
1. **Eviction rate**: Keys evicted due to memory pressure
1. **Expiration rate**: Keys expired naturally

Tools:
- Redis INFO command
- Redis-specific monitoring (Redis Insight, redis-cli)
- APM solutions (New Relic, Datadog)

---

## Cache Warming Strategies

1. **Pre-populating cache on startup**:
    - Load common data before serving requests

1. **Shadow caching**:
    - Build cache in parallel to production

1. **Intelligent prefetching**:
    - Predict and preload likely-needed data

1. **Keep-alive strategy**:
    - Reset TTL on frequently used keys

---

## Lab: Implementing Caching with Redis

1. **Exercise 1**: Implement a cache-aside pattern
1. **Exercise 2**: Create a write-through cache
1. **Exercise 3**: Implement cache invalidation
1. **Exercise 4**: Build a rate limiter using Redis
1. **Exercise 5**: Create a tiered caching system
1. **Exercise 6**: Implement cache tags for invalidation
1. **Exercise 7**: Handle cache stampede prevention

---

## Summary

- Redis is ideal for caching due to speed and features
- Cache patterns: cache-aside, write-through, read-through
- TTL management is essential for freshness
- Cache invalidation strategies: time-based, event-based
- Prevent cache stampede with locks and jitter
- Monitor cache performance for optimization
- Use appropriate eviction policies based on needs

Next chapter: Pub/Sub Messaging with Redis
