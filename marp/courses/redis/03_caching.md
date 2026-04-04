# Caching with Redis

---

## What is Caching?

- Temporarily storing frequently accessed data in fast storage
- Reduces load on primary data source
- Improves response time and application performance
- Reduces costs (database queries, API calls, computation)

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd0_02_caching" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="60" width="110" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="75" y="82" text-anchor="middle" font-size="11" font-weight="bold">Application</text>
  <text x="75" y="98" text-anchor="middle" font-size="10">Request data</text>
  <rect x="240" y="60" width="120" height="50" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="82" text-anchor="middle" font-size="11" font-weight="bold">Redis Cache</text>
  <text x="300" y="98" text-anchor="middle" font-size="10">Fast in-memory</text>
  <rect x="460" y="60" width="120" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="520" y="82" text-anchor="middle" font-size="11" font-weight="bold">Database</text>
  <text x="520" y="98" text-anchor="middle" font-size="10">Persistent store</text>
  <line x1="130" y1="80" x2="238" y2="80" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_02_caching)"/>
  <line x1="360" y1="80" x2="458" y2="80" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_02_caching)"/>
  <text x="185" y="72" text-anchor="middle" font-size="10" fill="#1565c0">GET</text>
  <text x="410" y="72" text-anchor="middle" font-size="10" fill="#6a1b9a">Miss</text>
  <line x1="238" y1="100" x2="130" y2="100" stroke="#4caf50" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd0_02_caching)"/>
  <text x="185" y="118" text-anchor="middle" font-size="10" fill="#2e7d32">Hit: ~0.5ms</text>
  <text x="410" y="118" text-anchor="middle" font-size="10" fill="#e65100">Fallback: ~10ms</text>
  <rect x="20" y="140" width="560" height="40" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5" opacity="0.5"/>
  <text x="300" y="165" text-anchor="middle" font-size="11">Caching reduces latency and offloads the database</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd1_02_caching" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="10" y="30" width="100" height="45" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="60" y="57" text-anchor="middle" font-size="11" font-weight="bold">Application</text>
  <rect x="200" y="30" width="100" height="45" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="250" y="57" text-anchor="middle" font-size="11" font-weight="bold">Redis Cache</text>
  <rect x="400" y="30" width="100" height="45" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="450" y="57" text-anchor="middle" font-size="11" font-weight="bold">Database</text>
  <!-- Step 1: Check cache -->
  <line x1="110" y1="45" x2="198" y2="45" stroke="#1565c0" stroke-width="2" marker-end="url(#arrowd1_02_caching)"/>
  <text x="155" y="40" text-anchor="middle" font-size="10" fill="#1565c0">1. GET key</text>
  <!-- Step 2: Cache miss -->
  <line x1="198" y1="60" x2="112" y2="60" stroke="#e65100" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrowd1_02_caching)"/>
  <text x="155" y="75" text-anchor="middle" font-size="10" fill="#e65100">2. MISS</text>
  <!-- Step 3: Query DB -->
  <line x1="110" y1="110" x2="398" y2="110" stroke="#6a1b9a" stroke-width="2" marker-end="url(#arrowd1_02_caching)"/>
  <text x="255" y="105" text-anchor="middle" font-size="10" fill="#6a1b9a">3. Query DB</text>
  <!-- Step 4: DB returns -->
  <line x1="398" y1="125" x2="112" y2="125" stroke="#6a1b9a" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrowd1_02_caching)"/>
  <text x="255" y="140" text-anchor="middle" font-size="10" fill="#6a1b9a">4. Return data</text>
  <!-- Step 5: Populate cache -->
  <line x1="110" y1="160" x2="198" y2="160" stroke="#2e7d32" stroke-width="2" marker-end="url(#arrowd1_02_caching)"/>
  <text x="155" y="155" text-anchor="middle" font-size="10" fill="#2e7d32">5. SET key</text>
  <rect x="510" y="30" width="80" height="170" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5" opacity="0.6"/>
  <text x="550" y="55" text-anchor="middle" font-size="10" font-weight="bold">Lazy</text>
  <text x="550" y="70" text-anchor="middle" font-size="10" font-weight="bold">Loading</text>
  <text x="550" y="100" text-anchor="middle" font-size="10">Cache only</text>
  <text x="550" y="115" text-anchor="middle" font-size="10">populated</text>
  <text x="550" y="130" text-anchor="middle" font-size="10">on read</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd2_02_caching" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="10" y="70" width="100" height="45" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="60" y="97" text-anchor="middle" font-size="11" font-weight="bold">Application</text>
  <rect x="200" y="20" width="100" height="45" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="250" y="47" text-anchor="middle" font-size="11" font-weight="bold">Redis Cache</text>
  <rect x="200" y="120" width="100" height="45" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="250" y="147" text-anchor="middle" font-size="11" font-weight="bold">Database</text>
  <!-- Write to cache -->
  <line x1="110" y1="82" x2="198" y2="48" stroke="#e65100" stroke-width="2" marker-end="url(#arrowd2_02_caching)"/>
  <text x="140" y="52" text-anchor="middle" font-size="10" fill="#e65100">1. Write</text>
  <!-- Write to DB -->
  <line x1="110" y1="102" x2="198" y2="135" stroke="#6a1b9a" stroke-width="2" marker-end="url(#arrowd2_02_caching)"/>
  <text x="140" y="135" text-anchor="middle" font-size="10" fill="#6a1b9a">2. Write</text>
  <!-- Sync indicator -->
  <line x1="250" y1="65" x2="250" y2="118" stroke="#333" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="275" y="95" text-anchor="middle" font-size="10" fill="#333">Sync</text>
  <rect x="380" y="20" width="200" height="150" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5" opacity="0.5"/>
  <text x="480" y="45" text-anchor="middle" font-size="11" font-weight="bold">Write-Through</text>
  <text x="480" y="65" text-anchor="middle" font-size="10">+ Data consistency</text>
  <text x="480" y="80" text-anchor="middle" font-size="10">+ Cache always fresh</text>
  <text x="480" y="100" text-anchor="middle" font-size="10">- Higher write latency</text>
  <text x="480" y="115" text-anchor="middle" font-size="10">- Both must succeed</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd3_02_caching" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="10" y="70" width="100" height="45" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="60" y="97" text-anchor="middle" font-size="11" font-weight="bold">Application</text>
  <rect x="180" y="70" width="100" height="45" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="230" y="97" text-anchor="middle" font-size="11" font-weight="bold">Redis Cache</text>
  <rect x="340" y="70" width="80" height="45" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="380" y="90" text-anchor="middle" font-size="10" font-weight="bold">Write</text>
  <text x="380" y="103" text-anchor="middle" font-size="10" font-weight="bold">Queue</text>
  <rect x="480" y="70" width="100" height="45" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="530" y="97" text-anchor="middle" font-size="11" font-weight="bold">Database</text>
  <!-- App writes to cache -->
  <line x1="110" y1="87" x2="178" y2="87" stroke="#e65100" stroke-width="2" marker-end="url(#arrowd3_02_caching)"/>
  <text x="145" y="82" text-anchor="middle" font-size="10" fill="#e65100">1. Write</text>
  <!-- Cache queues write -->
  <line x1="280" y1="92" x2="338" y2="92" stroke="#c62828" stroke-width="2" marker-end="url(#arrowd3_02_caching)"/>
  <text x="310" y="82" text-anchor="middle" font-size="10" fill="#c62828">2. Queue</text>
  <!-- Async write to DB -->
  <line x1="420" y1="92" x2="478" y2="92" stroke="#6a1b9a" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrowd3_02_caching)"/>
  <text x="450" y="82" text-anchor="middle" font-size="10" fill="#6a1b9a">3. Async</text>
  <!-- ACK back -->
  <line x1="178" y1="102" x2="112" y2="102" stroke="#2e7d32" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrowd3_02_caching)"/>
  <text x="145" y="120" text-anchor="middle" font-size="10" fill="#2e7d32">ACK (fast)</text>
  <rect x="10" y="145" width="570" height="40" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5" opacity="0.5"/>
  <text x="300" y="168" text-anchor="middle" font-size="10">Low write latency, eventual DB persistence. Risk: data loss if cache fails before flush.</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd4_02_caching" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="10" y="70" width="100" height="45" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="60" y="97" text-anchor="middle" font-size="11" font-weight="bold">Application</text>
  <rect x="200" y="30" width="120" height="70" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="260" y="52" text-anchor="middle" font-size="11" font-weight="bold">Cache Layer</text>
  <text x="260" y="68" text-anchor="middle" font-size="10">(Read-Through)</text>
  <text x="260" y="84" text-anchor="middle" font-size="10" fill="#e65100">Auto-loads on miss</text>
  <rect x="430" y="70" width="100" height="45" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="480" y="97" text-anchor="middle" font-size="11" font-weight="bold">Database</text>
  <!-- App reads from cache only -->
  <line x1="110" y1="82" x2="198" y2="60" stroke="#1565c0" stroke-width="2" marker-end="url(#arrowd4_02_caching)"/>
  <text x="140" y="60" text-anchor="middle" font-size="10" fill="#1565c0">1. Read</text>
  <!-- Cache fetches from DB on miss -->
  <line x1="320" y1="80" x2="428" y2="87" stroke="#6a1b9a" stroke-width="2" marker-end="url(#arrowd4_02_caching)"/>
  <text x="375" y="72" text-anchor="middle" font-size="10" fill="#6a1b9a">2. Fetch (on miss)</text>
  <!-- DB returns to cache -->
  <line x1="428" y1="100" x2="322" y2="93" stroke="#6a1b9a" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrowd4_02_caching)"/>
  <text x="375" y="115" text-anchor="middle" font-size="10" fill="#6a1b9a">3. Data</text>
  <!-- Cache returns to app -->
  <line x1="198" y1="90" x2="112" y2="97" stroke="#2e7d32" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrowd4_02_caching)"/>
  <text x="145" y="115" text-anchor="middle" font-size="10" fill="#2e7d32">4. Return</text>
  <rect x="10" y="145" width="570" height="40" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5" opacity="0.5"/>
  <text x="300" y="168" text-anchor="middle" font-size="10">App only talks to cache. Cache handles DB interaction transparently.</text>
</svg>

---

## Refresh-Ahead Pattern

Cache proactively refreshes before expiration:

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd5_02_caching" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- TTL timeline bar -->
  <rect x="30" y="20" width="540" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="40" text-anchor="middle" font-size="11" font-weight="bold">Key TTL Timeline</text>
  <!-- Active zone -->
  <rect x="30" y="60" width="300" height="35" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="3"/>
  <text x="180" y="82" text-anchor="middle" font-size="11" fill="#2e7d32">Active (serving reads)</text>
  <!-- Refresh threshold zone -->
  <rect x="330" y="60" width="120" height="35" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="3"/>
  <text x="390" y="78" text-anchor="middle" font-size="10" fill="#e65100">Refresh</text>
  <text x="390" y="90" text-anchor="middle" font-size="10" fill="#e65100">Threshold</text>
  <!-- Expired zone -->
  <rect x="450" y="60" width="120" height="35" fill="#ffebee" stroke="#c62828" stroke-width="2" rx="3"/>
  <text x="510" y="82" text-anchor="middle" font-size="10" fill="#c62828">Expired</text>
  <!-- Arrows -->
  <line x1="390" y1="95" x2="390" y2="130" stroke="#e65100" stroke-width="2" marker-end="url(#arrowd5_02_caching)"/>
  <rect x="310" y="130" width="160" height="50" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="390" y="150" text-anchor="middle" font-size="10" font-weight="bold">Background refresh</text>
  <text x="390" y="165" text-anchor="middle" font-size="10">fetches from DB before</text>
  <text x="390" y="178" text-anchor="middle" font-size="10">key actually expires</text>
  <!-- DB icon -->
  <rect x="50" y="120" width="120" height="50" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5"/>
  <text x="110" y="142" text-anchor="middle" font-size="10" font-weight="bold">Result:</text>
  <text x="110" y="158" text-anchor="middle" font-size="10">Zero cache misses</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd6_02_caching" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- Memory bar -->
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold">Redis Memory (maxmemory reached)</text>
  <rect x="30" y="25" width="540" height="25" fill="#ffebee" stroke="#c62828" stroke-width="2" rx="3"/>
  <rect x="30" y="25" width="480" height="25" fill="#fff3e0" stroke="#e65100" stroke-width="1" rx="3"/>
  <rect x="30" y="25" width="360" height="25" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1" rx="3"/>
  <text x="200" y="42" text-anchor="middle" font-size="10">Used: 3.6 GB</text>
  <text x="540" y="42" text-anchor="middle" font-size="10" fill="#c62828">4 GB limit</text>
  <!-- Eviction policies -->
  <rect x="20" y="65" width="130" height="55" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="85" y="82" text-anchor="middle" font-size="10" font-weight="bold">noeviction</text>
  <text x="85" y="95" text-anchor="middle" font-size="10">Returns error</text>
  <text x="85" y="108" text-anchor="middle" font-size="10">on new writes</text>
  <rect x="160" y="65" width="130" height="55" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="225" y="82" text-anchor="middle" font-size="10" font-weight="bold">allkeys-lru</text>
  <text x="225" y="95" text-anchor="middle" font-size="10">Evict least</text>
  <text x="225" y="108" text-anchor="middle" font-size="10">recently used</text>
  <rect x="300" y="65" width="130" height="55" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5"/>
  <text x="365" y="82" text-anchor="middle" font-size="10" font-weight="bold">volatile-ttl</text>
  <text x="365" y="95" text-anchor="middle" font-size="10">Evict nearest</text>
  <text x="365" y="108" text-anchor="middle" font-size="10">expiration</text>
  <rect x="440" y="65" width="140" height="55" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="510" y="82" text-anchor="middle" font-size="10" font-weight="bold">allkeys-random</text>
  <text x="510" y="95" text-anchor="middle" font-size="10">Evict random</text>
  <text x="510" y="108" text-anchor="middle" font-size="10">keys</text>
  <!-- New key arrow -->
  <rect x="20" y="140" width="560" height="45" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5" opacity="0.4"/>
  <text x="300" y="160" text-anchor="middle" font-size="10">Set maxmemory-policy in redis.conf: <tspan font-weight="bold">maxmemory-policy allkeys-lru</tspan></text>
  <text x="300" y="175" text-anchor="middle" font-size="10">volatile-* policies only evict keys with TTL set</text>
</svg>

---

## LRU vs LFU Eviction

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd7_02_caching" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- LRU side -->
  <text x="150" y="18" text-anchor="middle" font-size="12" font-weight="bold">LRU (Least Recently Used)</text>
  <rect x="20" y="25" width="260" height="160" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5" opacity="0.3"/>
  <rect x="30" y="35" width="55" height="30" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1" rx="3"/>
  <text x="57" y="54" text-anchor="middle" font-size="10">Key A</text>
  <text x="57" y="78" text-anchor="middle" font-size="10" fill="#2e7d32">1s ago</text>
  <rect x="95" y="35" width="55" height="30" fill="#fff3e0" stroke="#e65100" stroke-width="1" rx="3"/>
  <text x="122" y="54" text-anchor="middle" font-size="10">Key B</text>
  <text x="122" y="78" text-anchor="middle" font-size="10" fill="#e65100">30s ago</text>
  <rect x="160" y="35" width="55" height="30" fill="#fff3e0" stroke="#e65100" stroke-width="1" rx="3"/>
  <text x="187" y="54" text-anchor="middle" font-size="10">Key C</text>
  <text x="187" y="78" text-anchor="middle" font-size="10" fill="#e65100">2m ago</text>
  <rect x="225" y="35" width="55" height="30" fill="#ffebee" stroke="#c62828" stroke-width="2" rx="3"/>
  <text x="252" y="54" text-anchor="middle" font-size="10">Key D</text>
  <text x="252" y="78" text-anchor="middle" font-size="10" fill="#c62828">5m ago</text>
  <text x="252" y="100" text-anchor="middle" font-size="10" fill="#c62828">EVICTED</text>
  <line x1="252" y1="65" x2="252" y2="90" stroke="#c62828" stroke-width="2" marker-end="url(#arrowd7_02_caching)"/>
  <text x="150" y="130" text-anchor="middle" font-size="10">Evicts key not used for</text>
  <text x="150" y="145" text-anchor="middle" font-size="10">the longest time</text>
  <!-- LFU side -->
  <text x="450" y="18" text-anchor="middle" font-size="12" font-weight="bold">LFU (Least Frequently Used)</text>
  <rect x="320" y="25" width="260" height="160" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5" opacity="0.3"/>
  <rect x="330" y="35" width="55" height="30" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1" rx="3"/>
  <text x="357" y="54" text-anchor="middle" font-size="10">Key A</text>
  <text x="357" y="78" text-anchor="middle" font-size="10" fill="#2e7d32">100 hits</text>
  <rect x="395" y="35" width="55" height="30" fill="#fff3e0" stroke="#e65100" stroke-width="1" rx="3"/>
  <text x="422" y="54" text-anchor="middle" font-size="10">Key B</text>
  <text x="422" y="78" text-anchor="middle" font-size="10" fill="#e65100">25 hits</text>
  <rect x="460" y="35" width="55" height="30" fill="#fff3e0" stroke="#e65100" stroke-width="1" rx="3"/>
  <text x="487" y="54" text-anchor="middle" font-size="10">Key C</text>
  <text x="487" y="78" text-anchor="middle" font-size="10" fill="#e65100">10 hits</text>
  <rect x="525" y="35" width="55" height="30" fill="#ffebee" stroke="#c62828" stroke-width="2" rx="3"/>
  <text x="552" y="54" text-anchor="middle" font-size="10">Key D</text>
  <text x="552" y="78" text-anchor="middle" font-size="10" fill="#c62828">2 hits</text>
  <text x="552" y="100" text-anchor="middle" font-size="10" fill="#c62828">EVICTED</text>
  <line x1="552" y1="65" x2="552" y2="90" stroke="#c62828" stroke-width="2" marker-end="url(#arrowd7_02_caching)"/>
  <text x="450" y="130" text-anchor="middle" font-size="10">Evicts key with fewest</text>
  <text x="450" y="145" text-anchor="middle" font-size="10">access count</text>
  <text x="300" y="180" text-anchor="middle" font-size="10" font-weight="bold">LFU (Redis 4.0+) better for frequency-skewed workloads</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd8_02_caching" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- Writer app -->
  <rect x="10" y="20" width="90" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="55" y="44" text-anchor="middle" font-size="10" font-weight="bold">Writer App</text>
  <!-- Database -->
  <rect x="160" y="20" width="90" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="205" y="44" text-anchor="middle" font-size="10" font-weight="bold">Database</text>
  <!-- Redis Pub/Sub -->
  <rect x="310" y="10" width="110" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="365" y="32" text-anchor="middle" font-size="10" font-weight="bold">Redis Pub/Sub</text>
  <text x="365" y="48" text-anchor="middle" font-size="10" fill="#e65100">invalidation channel</text>
  <!-- Reader apps -->
  <rect x="490" y="10" width="90" height="35" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="535" y="32" text-anchor="middle" font-size="10">App Instance 1</text>
  <rect x="490" y="50" width="90" height="35" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="535" y="72" text-anchor="middle" font-size="10">App Instance 2</text>
  <!-- Step 1: Write to DB -->
  <line x1="100" y1="35" x2="158" y2="35" stroke="#6a1b9a" stroke-width="2" marker-end="url(#arrowd8_02_caching)"/>
  <text x="130" y="30" text-anchor="middle" font-size="10" fill="#6a1b9a">1. Write</text>
  <!-- Step 2: Publish invalidation -->
  <line x1="100" y1="55" x2="308" y2="45" stroke="#e65100" stroke-width="2" marker-end="url(#arrowd8_02_caching)"/>
  <text x="200" y="68" text-anchor="middle" font-size="10" fill="#e65100">2. PUBLISH "invalidate:item:42"</text>
  <!-- Step 3: Notify subscribers -->
  <line x1="420" y1="28" x2="488" y2="28" stroke="#2e7d32" stroke-width="2" marker-end="url(#arrowd8_02_caching)"/>
  <line x1="420" y1="50" x2="488" y2="65" stroke="#2e7d32" stroke-width="2" marker-end="url(#arrowd8_02_caching)"/>
  <text x="455" y="18" text-anchor="middle" font-size="10" fill="#2e7d32">3. Notify</text>
  <!-- Step 4: DEL from local cache -->
  <rect x="490" y="100" width="90" height="30" fill="#ffebee" stroke="#c62828" stroke-width="1" rx="3"/>
  <text x="535" y="119" text-anchor="middle" font-size="10" fill="#c62828">DEL item:42</text>
  <line x1="535" y1="85" x2="535" y2="98" stroke="#c62828" stroke-width="2" marker-end="url(#arrowd8_02_caching)"/>
  <rect x="10" y="145" width="570" height="40" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5" opacity="0.4"/>
  <text x="300" y="168" text-anchor="middle" font-size="10">All instances invalidate stale data on event. More accurate than TTL-based expiry.</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd9_02_caching" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- Popular key expires -->
  <rect x="220" y="5" width="160" height="30" fill="#ffebee" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="300" y="25" text-anchor="middle" font-size="11" fill="#c62828" font-weight="bold">Popular key EXPIRES!</text>
  <!-- Multiple requests -->
  <rect x="10" y="50" width="80" height="25" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="50" y="67" text-anchor="middle" font-size="10">Request 1</text>
  <rect x="10" y="80" width="80" height="25" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="50" y="97" text-anchor="middle" font-size="10">Request 2</text>
  <rect x="10" y="110" width="80" height="25" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="50" y="127" text-anchor="middle" font-size="10">Request 3</text>
  <rect x="10" y="140" width="80" height="25" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="50" y="157" text-anchor="middle" font-size="10">Request N</text>
  <!-- Cache MISS -->
  <rect x="150" y="55" width="90" height="105" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="5"/>
  <text x="195" y="80" text-anchor="middle" font-size="10" font-weight="bold" fill="#e65100">Redis</text>
  <text x="195" y="95" text-anchor="middle" font-size="11" fill="#c62828">MISS!</text>
  <text x="195" y="110" text-anchor="middle" font-size="11" fill="#c62828">MISS!</text>
  <text x="195" y="125" text-anchor="middle" font-size="11" fill="#c62828">MISS!</text>
  <text x="195" y="145" text-anchor="middle" font-size="11" fill="#c62828">MISS!</text>
  <!-- All hit DB simultaneously -->
  <line x1="90" y1="62" x2="148" y2="75" stroke="#333" stroke-width="1" marker-end="url(#arrowd9_02_caching)"/>
  <line x1="90" y1="92" x2="148" y2="92" stroke="#333" stroke-width="1" marker-end="url(#arrowd9_02_caching)"/>
  <line x1="90" y1="122" x2="148" y2="110" stroke="#333" stroke-width="1" marker-end="url(#arrowd9_02_caching)"/>
  <line x1="90" y1="152" x2="148" y2="130" stroke="#333" stroke-width="1" marker-end="url(#arrowd9_02_caching)"/>
  <!-- DB overloaded -->
  <rect x="310" y="55" width="100" height="105" fill="#ffebee" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="360" y="80" text-anchor="middle" font-size="10" font-weight="bold">Database</text>
  <text x="360" y="100" text-anchor="middle" font-size="12" fill="#c62828">OVERLOAD</text>
  <text x="360" y="120" text-anchor="middle" font-size="10" fill="#c62828">N identical</text>
  <text x="360" y="135" text-anchor="middle" font-size="10" fill="#c62828">queries!</text>
  <line x1="240" y1="80" x2="308" y2="80" stroke="#c62828" stroke-width="2" marker-end="url(#arrowd9_02_caching)"/>
  <line x1="240" y1="100" x2="308" y2="100" stroke="#c62828" stroke-width="2" marker-end="url(#arrowd9_02_caching)"/>
  <line x1="240" y1="120" x2="308" y2="120" stroke="#c62828" stroke-width="2" marker-end="url(#arrowd9_02_caching)"/>
  <line x1="240" y1="140" x2="308" y2="140" stroke="#c62828" stroke-width="2" marker-end="url(#arrowd9_02_caching)"/>
  <!-- Result -->
  <rect x="440" y="55" width="145" height="105" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5" opacity="0.6"/>
  <text x="512" y="80" text-anchor="middle" font-size="10" font-weight="bold">Result:</text>
  <text x="512" y="100" text-anchor="middle" font-size="10">Cascading failures</text>
  <text x="512" y="115" text-anchor="middle" font-size="10">Slow responses</text>
  <text x="512" y="130" text-anchor="middle" font-size="10">Possible DB crash</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd10_02_caching" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- Request 1 gets lock -->
  <rect x="10" y="15" width="75" height="25" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="3"/>
  <text x="47" y="32" text-anchor="middle" font-size="10">Req 1</text>
  <!-- Request 2 waits -->
  <rect x="10" y="55" width="75" height="25" fill="#fff3e0" stroke="#e65100" stroke-width="1" rx="3"/>
  <text x="47" y="72" text-anchor="middle" font-size="10">Req 2</text>
  <!-- Request 3 waits -->
  <rect x="10" y="90" width="75" height="25" fill="#fff3e0" stroke="#e65100" stroke-width="1" rx="3"/>
  <text x="47" y="107" text-anchor="middle" font-size="10">Req 3</text>
  <!-- Lock in Redis -->
  <rect x="130" y="10" width="110" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="185" y="30" text-anchor="middle" font-size="10" font-weight="bold">Redis Lock</text>
  <text x="185" y="48" text-anchor="middle" font-size="10" fill="#2e7d32">SET NX EX 5</text>
  <!-- Req 1 acquires lock -->
  <line x1="85" y1="27" x2="128" y2="30" stroke="#2e7d32" stroke-width="2" marker-end="url(#arrowd10_02_caching)"/>
  <text x="107" y="20" text-anchor="middle" font-size="10" fill="#2e7d32">Lock OK</text>
  <!-- Req 2,3 wait -->
  <line x1="85" y1="67" x2="128" y2="50" stroke="#e65100" stroke-width="1" stroke-dasharray="4,4" marker-end="url(#arrowd10_02_caching)"/>
  <line x1="85" y1="102" x2="128" y2="55" stroke="#e65100" stroke-width="1" stroke-dasharray="4,4" marker-end="url(#arrowd10_02_caching)"/>
  <text x="107" y="82" text-anchor="middle" font-size="10" fill="#e65100">Wait...</text>
  <!-- Only Req 1 queries DB -->
  <rect x="300" y="10" width="90" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="345" y="34" text-anchor="middle" font-size="10" font-weight="bold">Database</text>
  <line x1="240" y1="30" x2="298" y2="30" stroke="#2e7d32" stroke-width="2" marker-end="url(#arrowd10_02_caching)"/>
  <text x="270" y="22" text-anchor="middle" font-size="10" fill="#2e7d32">1 query</text>
  <!-- Req 1 populates cache -->
  <rect x="300" y="70" width="90" height="40" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="345" y="87" text-anchor="middle" font-size="10" font-weight="bold">Cache SET</text>
  <text x="345" y="102" text-anchor="middle" font-size="10" fill="#2e7d32">+ Release lock</text>
  <line x1="345" y1="50" x2="345" y2="68" stroke="#2e7d32" stroke-width="2" marker-end="url(#arrowd10_02_caching)"/>
  <!-- Req 2,3 get from cache -->
  <rect x="440" y="55" width="140" height="55" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="510" y="72" text-anchor="middle" font-size="10" font-weight="bold">Req 2, 3 retry</text>
  <text x="510" y="88" text-anchor="middle" font-size="10" fill="#2e7d32">Cache HIT!</text>
  <text x="510" y="103" text-anchor="middle" font-size="10">No DB query needed</text>
  <line x1="390" y1="90" x2="438" y2="85" stroke="#333" stroke-width="1" marker-end="url(#arrowd10_02_caching)"/>
  <!-- Summary -->
  <rect x="10" y="140" width="570" height="45" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5" opacity="0.4"/>
  <text x="300" y="158" text-anchor="middle" font-size="10" font-weight="bold">Only 1 request rebuilds cache. Others wait and read from cache.</text>
  <text x="300" y="175" text-anchor="middle" font-size="10">Uses SET key lock_id NX EX timeout for atomic lock acquisition.</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd11_02_caching" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- App instances -->
  <rect x="10" y="15" width="90" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="55" y="37" text-anchor="middle" font-size="10" font-weight="bold">App Server 1</text>
  <rect x="10" y="60" width="90" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="55" y="82" text-anchor="middle" font-size="10" font-weight="bold">App Server 2</text>
  <rect x="10" y="105" width="90" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="55" y="127" text-anchor="middle" font-size="10" font-weight="bold">App Server 3</text>
  <!-- Shared Redis cache -->
  <rect x="180" y="25" width="140" height="110" fill="#fff3e0" stroke="#333" stroke-width="2" rx="8"/>
  <text x="250" y="50" text-anchor="middle" font-size="12" font-weight="bold">Redis Cache</text>
  <text x="250" y="68" text-anchor="middle" font-size="10">(shared instance)</text>
  <rect x="195" y="78" width="110" height="20" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="250" y="93" text-anchor="middle" font-size="10">user:42 = {...}</text>
  <rect x="195" y="102" width="110" height="20" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="250" y="117" text-anchor="middle" font-size="10">product:7 = {...}</text>
  <!-- Database -->
  <rect x="430" y="45" width="120" height="60" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="490" y="72" text-anchor="middle" font-size="11" font-weight="bold">Database</text>
  <text x="490" y="92" text-anchor="middle" font-size="10">Source of truth</text>
  <!-- Arrows: apps to cache -->
  <line x1="100" y1="32" x2="178" y2="60" stroke="#333" stroke-width="1" marker-end="url(#arrowd11_02_caching)"/>
  <line x1="100" y1="77" x2="178" y2="77" stroke="#333" stroke-width="1" marker-end="url(#arrowd11_02_caching)"/>
  <line x1="100" y1="122" x2="178" y2="100" stroke="#333" stroke-width="1" marker-end="url(#arrowd11_02_caching)"/>
  <!-- Arrow: cache to DB -->
  <line x1="320" y1="77" x2="428" y2="77" stroke="#6a1b9a" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrowd11_02_caching)"/>
  <text x="375" y="70" text-anchor="middle" font-size="10" fill="#6a1b9a">On miss</text>
  <!-- Note -->
  <rect x="10" y="155" width="570" height="35" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5" opacity="0.4"/>
  <text x="300" y="177" text-anchor="middle" font-size="10">All app servers share one Redis cache -- consistent view, no local cache drift</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd12_02_caching" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold">Cache Hit Ratio Visualization</text>
  <!-- Hit ratio bar -->
  <text x="30" y="45" font-size="10" font-weight="bold">Hits:</text>
  <rect x="70" y="32" width="400" height="20" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="3"/>
  <text x="270" y="47" text-anchor="middle" font-size="11" fill="#2e7d32" font-weight="bold">keyspace_hits: 85,000</text>
  <!-- Miss ratio bar -->
  <text x="30" y="75" font-size="10" font-weight="bold">Miss:</text>
  <rect x="70" y="62" width="80" height="20" fill="#ffebee" stroke="#c62828" stroke-width="2" rx="3"/>
  <text x="110" y="77" text-anchor="middle" font-size="11" fill="#c62828" font-weight="bold">15,000</text>
  <!-- Result -->
  <rect x="490" y="32" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="540" y="52" text-anchor="middle" font-size="11" font-weight="bold">Hit Ratio</text>
  <text x="540" y="72" text-anchor="middle" font-size="13" fill="#2e7d32" font-weight="bold">85%</text>
  <!-- Gauge-like indicators -->
  <rect x="30" y="100" width="110" height="45" fill="#ffebee" stroke="#c62828" stroke-width="1" rx="5"/>
  <text x="85" y="118" text-anchor="middle" font-size="10" fill="#c62828" font-weight="bold">Poor &lt; 60%</text>
  <text x="85" y="135" text-anchor="middle" font-size="10">Review TTL, size</text>
  <rect x="160" y="100" width="110" height="45" fill="#fff3e0" stroke="#e65100" stroke-width="1" rx="5"/>
  <text x="215" y="118" text-anchor="middle" font-size="10" fill="#e65100" font-weight="bold">OK 60-80%</text>
  <text x="215" y="135" text-anchor="middle" font-size="10">Room to improve</text>
  <rect x="290" y="100" width="110" height="45" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="345" y="118" text-anchor="middle" font-size="10" fill="#2e7d32" font-weight="bold">Good 80-95%</text>
  <text x="345" y="135" text-anchor="middle" font-size="10">Target range</text>
  <rect x="420" y="100" width="110" height="45" fill="#e3f2fd" stroke="#1565c0" stroke-width="1" rx="5"/>
  <text x="475" y="118" text-anchor="middle" font-size="10" fill="#1565c0" font-weight="bold">Excellent &gt;95%</text>
  <text x="475" y="135" text-anchor="middle" font-size="10">Well optimized</text>
  <text x="300" y="175" text-anchor="middle" font-size="10">Formula: keyspace_hits / (keyspace_hits + keyspace_misses) x 100</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd13_02_caching" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- String keys approach -->
  <text x="150" y="18" text-anchor="middle" font-size="11" font-weight="bold">String Keys (wasteful)</text>
  <rect x="20" y="25" width="260" height="100" fill="#ffebee" stroke="#c62828" stroke-width="1" rx="5" opacity="0.3"/>
  <rect x="30" y="32" width="240" height="20" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="150" y="47" text-anchor="middle" font-size="10">user:42:name = "Alice"</text>
  <rect x="30" y="57" width="240" height="20" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="150" y="72" text-anchor="middle" font-size="10">user:42:email = "a@b.com"</text>
  <rect x="30" y="82" width="240" height="20" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="150" y="97" text-anchor="middle" font-size="10">user:42:role = "admin"</text>
  <text x="150" y="120" text-anchor="middle" font-size="10" fill="#c62828">3 keys x overhead each</text>
  <!-- Hash approach -->
  <text x="450" y="18" text-anchor="middle" font-size="11" font-weight="bold">Hash (efficient)</text>
  <rect x="320" y="25" width="260" height="100" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1" rx="5" opacity="0.3"/>
  <rect x="330" y="32" width="240" height="85" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="450" y="50" text-anchor="middle" font-size="10" font-weight="bold">HSET user:42</text>
  <rect x="345" y="58" width="100" height="18" fill="#fff3e0" stroke="#333" stroke-width="1" rx="2"/>
  <text x="395" y="71" text-anchor="middle" font-size="10">name: "Alice"</text>
  <rect x="345" y="78" width="100" height="18" fill="#fff3e0" stroke="#333" stroke-width="1" rx="2"/>
  <text x="395" y="91" text-anchor="middle" font-size="10">email: "a@b.com"</text>
  <rect x="455" y="58" width="100" height="18" fill="#fff3e0" stroke="#333" stroke-width="1" rx="2"/>
  <text x="505" y="71" text-anchor="middle" font-size="10">role: "admin"</text>
  <text x="450" y="120" text-anchor="middle" font-size="10" fill="#2e7d32">1 key, ziplist encoding</text>
  <!-- Arrow showing improvement -->
  <line x1="280" y1="75" x2="318" y2="75" stroke="#2e7d32" stroke-width="2" marker-end="url(#arrowd13_02_caching)"/>
  <!-- Savings -->
  <rect x="150" y="140" width="300" height="45" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1" rx="5"/>
  <text x="300" y="158" text-anchor="middle" font-size="10" font-weight="bold">Memory savings: up to 10x fewer bytes</text>
  <text x="300" y="175" text-anchor="middle" font-size="10">HGETALL user:42 retrieves all fields at once</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd14_02_caching" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- Client -->
  <rect x="10" y="50" width="80" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="50" y="74" text-anchor="middle" font-size="10" font-weight="bold">Client</text>
  <!-- Redis counter -->
  <rect x="160" y="25" width="170" height="90" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="245" y="45" text-anchor="middle" font-size="11" font-weight="bold">Redis Counter</text>
  <text x="245" y="62" text-anchor="middle" font-size="10">rate:user42:1710000</text>
  <rect x="175" y="70" width="140" height="18" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="2"/>
  <text x="245" y="84" text-anchor="middle" font-size="10">INCR = 3 (limit: 5)</text>
  <text x="245" y="108" text-anchor="middle" font-size="10" fill="#e65100">EXPIRE 60s (window)</text>
  <!-- API -->
  <rect x="420" y="50" width="80" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="460" y="74" text-anchor="middle" font-size="10" font-weight="bold">API</text>
  <!-- Flow: allowed -->
  <line x1="90" y1="65" x2="158" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arrowd14_02_caching)"/>
  <text x="125" y="55" text-anchor="middle" font-size="10">Request</text>
  <line x1="330" y1="60" x2="418" y2="65" stroke="#2e7d32" stroke-width="2" marker-end="url(#arrowd14_02_caching)"/>
  <text x="375" y="55" text-anchor="middle" font-size="10" fill="#2e7d32">count &lt; limit</text>
  <!-- Flow: blocked -->
  <rect x="160" y="130" width="170" height="55" fill="#ffebee" stroke="#c62828" stroke-width="1" rx="5"/>
  <text x="245" y="150" text-anchor="middle" font-size="10" font-weight="bold" fill="#c62828">When count >= limit:</text>
  <text x="245" y="168" text-anchor="middle" font-size="10" fill="#c62828">HTTP 429 Too Many Requests</text>
  <text x="245" y="180" text-anchor="middle" font-size="10">Retry-After: remaining TTL</text>
  <!-- Allowed indicator -->
  <rect x="420" y="130" width="160" height="55" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5" opacity="0.5"/>
  <text x="500" y="148" text-anchor="middle" font-size="10" font-weight="bold">Sliding Window:</text>
  <text x="500" y="163" text-anchor="middle" font-size="10">INCR + EXPIRE = atomic</text>
  <text x="500" y="178" text-anchor="middle" font-size="10">counter per time window</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd15_02_caching)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd15_02_caching)"/>
  <defs>
    <marker id="arrowd15_02_caching" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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
