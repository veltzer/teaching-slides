# Redis: Introduction

---

## What is Redis?

- **RE**mote **DI**ctionary **S**erver
- Open-source in-memory data structure store
- Created by Salvatore Sanfilippo in 2009
- Written in ANSI C
- BSD licensed

---

## Redis Use Cases

- Caching
- Real-time analytics
- Session store
- Message broker
- Leaderboards and counting
- Job queues
- Geospatial data

---

## Where Redis Fits in the Architecture

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="70" width="110" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="75" y="95" text-anchor="middle" font-size="12" font-weight="bold">Client App</text>
  <text x="75" y="110" text-anchor="middle" font-size="10">Web / API</text>
  <rect x="200" y="30" width="120" height="50" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="260" y="52" text-anchor="middle" font-size="12" font-weight="bold">Redis</text>
  <text x="260" y="68" text-anchor="middle" font-size="10">Cache Layer</text>
  <rect x="200" y="120" width="120" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="260" y="142" text-anchor="middle" font-size="12" font-weight="bold">Database</text>
  <text x="260" y="158" text-anchor="middle" font-size="10">PostgreSQL/MySQL</text>
  <rect x="400" y="70" width="110" height="60" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="455" y="95" text-anchor="middle" font-size="12" font-weight="bold">Response</text>
  <text x="455" y="110" text-anchor="middle" font-size="10">Fast data</text>
  <line x1="130" y1="85" x2="200" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_00_intro)"/>
  <line x1="130" y1="115" x2="200" y2="145" stroke="#999" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#arrowd0_00_intro)"/>
  <line x1="320" y1="55" x2="400" y2="85" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_00_intro)"/>
  <text x="155" y="75" font-size="10" fill="#c62828">fast</text>
  <text x="155" y="135" font-size="10" fill="#999">slow</text>
  <defs>
    <marker id="arrowd0_00_intro" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Why Redis?

- **Speed**: In-memory operations (~100,000 ops/sec)
- **Simplicity**: Easy to use and maintain
- **Versatility**: Multiple data structures
- **Persistence**: Optional durability
- **Replication**: Master-slave architecture
- **High Availability**: Redis Sentinel
- **Scalability**: Redis Cluster

---

## NoSQL Landscape

<svg width="600" height="150" xmlns="http://www.w3.org/2000/svg">
  <rect x="150" y="40" width="300" height="70" fill="#f0f0f0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="80" text-anchor="middle" font-size="14">Diagram</text>
</svg>

---

## Redis vs Traditional Databases

| Feature | Redis | Traditional RDBMS |
|---------|-------|-------------------|
| Data Model | In-memory, NoSQL | Disk-based, SQL |
| Query Language | Command-based | SQL |
| Transaction Support | Limited (MULTI/EXEC) | ACID compliant |
| Data Types | Rich data structures | Tables, rows, columns |
| Performance | Extremely fast | Slower (disk I/O bound) |
| Scalability | Horizontal with sharding | Vertical, then horizontal |

---

## Redis Architecture

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="220" y="10" width="160" height="55" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="32" text-anchor="middle" font-size="13" font-weight="bold">Redis Server</text>
  <text x="300" y="50" text-anchor="middle" font-size="10">Single-threaded Event Loop</text>
  <rect x="30" y="85" width="110" height="45" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="85" y="105" text-anchor="middle" font-size="11" font-weight="bold">RAM</text>
  <text x="85" y="118" text-anchor="middle" font-size="10">In-Memory Store</text>
  <rect x="170" y="85" width="110" height="45" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="225" y="105" text-anchor="middle" font-size="11" font-weight="bold">I/O Multiplexer</text>
  <text x="225" y="118" text-anchor="middle" font-size="10">epoll / kqueue</text>
  <rect x="310" y="85" width="110" height="45" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="365" y="105" text-anchor="middle" font-size="11" font-weight="bold">Command</text>
  <text x="365" y="118" text-anchor="middle" font-size="10">Processor</text>
  <rect x="450" y="85" width="110" height="45" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="505" y="105" text-anchor="middle" font-size="11" font-weight="bold">Persistence</text>
  <text x="505" y="118" text-anchor="middle" font-size="10">RDB / AOF</text>
  <rect x="100" y="150" width="400" height="35" fill="#f0f0f0" stroke="#333" stroke-width="1.5" rx="3" stroke-dasharray="4,2"/>
  <text x="300" y="172" text-anchor="middle" font-size="11">Client Connections (TCP port 6379)</text>
  <line x1="300" y1="65" x2="300" y2="85" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd2_00_intro)"/>
  <defs>
    <marker id="arrowd2_00_intro" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Redis Installation

1. **Linux/macOS**:
```bash
sudo apt-get install redis-server  # Debian/Ubuntu
brew install redis                 # macOS
```

1. **Windows**:
    - Redis doesn't officially support Windows
    - Use WSL (Windows Subsystem for Linux)
    - Use Redis Labs Windows port (unofficial)

1. **Docker**:
```bash
docker run --name redis -p 6379:6379 -d redis
```

---

## Redis CLI Basics

Connect to Redis server:
```bash
redis-cli
```

Test connection:
```bash
127.0.0.1:6379> PING
PONG
```

Get server info:
```bash
127.0.0.1:6379> INFO
# Server
redis_version:7.0.5
...
```

---

## Redis Configuration

Default config file: `/etc/redis/redis.conf`

Key configurations:
- `port 6379` - Default port
- `bind 127.0.0.1` - Interface to listen on
- `maxmemory 100mb` - Memory limit
- `maxmemory-policy allkeys-lru` - Eviction policy
- `appendonly yes` - Enable AOF persistence

---

## Redis Data Types Overview

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="25" width="90" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="55" y="47" text-anchor="middle" font-size="11" font-weight="bold">Strings</text>
  <text x="55" y="62" text-anchor="middle" font-size="10">"hello"</text>
  <rect x="110" y="25" width="90" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="155" y="47" text-anchor="middle" font-size="11" font-weight="bold">Lists</text>
  <text x="155" y="62" text-anchor="middle" font-size="10">[a, b, c]</text>
  <rect x="210" y="25" width="90" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="255" y="47" text-anchor="middle" font-size="11" font-weight="bold">Sets</text>
  <text x="255" y="62" text-anchor="middle" font-size="10">{a, b, c}</text>
  <rect x="310" y="25" width="90" height="50" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="355" y="47" text-anchor="middle" font-size="11" font-weight="bold">Sorted Sets</text>
  <text x="355" y="62" text-anchor="middle" font-size="10">score:member</text>
  <rect x="410" y="25" width="90" height="50" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="455" y="47" text-anchor="middle" font-size="11" font-weight="bold">Hashes</text>
  <text x="455" y="62" text-anchor="middle" font-size="10">field:value</text>
  <rect x="510" y="25" width="80" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="550" y="47" text-anchor="middle" font-size="11" font-weight="bold">Streams</text>
  <text x="550" y="62" text-anchor="middle" font-size="10">time-series</text>
  <rect x="100" y="100" width="400" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="8"/>
  <text x="300" y="122" text-anchor="middle" font-size="13" font-weight="bold">Redis Key-Value Engine</text>
  <text x="300" y="140" text-anchor="middle" font-size="10">All data accessed by unique string keys</text>
  <line x1="55" y1="75" x2="200" y2="100" stroke="#333" stroke-width="1"/>
  <line x1="155" y1="75" x2="230" y2="100" stroke="#333" stroke-width="1"/>
  <line x1="255" y1="75" x2="280" y2="100" stroke="#333" stroke-width="1"/>
  <line x1="355" y1="75" x2="330" y2="100" stroke="#333" stroke-width="1"/>
  <line x1="455" y1="75" x2="390" y2="100" stroke="#333" stroke-width="1"/>
  <line x1="550" y1="75" x2="430" y2="100" stroke="#333" stroke-width="1"/>
  <text x="300" y="180" text-anchor="middle" font-size="11" fill="#555">SET key value | GET key | DEL key | EXISTS key</text>
</svg>

---

## Strings

- Simplest Redis data type
- Can be text, integers, or binary data
- Maximum size: 512MB

Basic operations:
```bash
SET key value
GET key
INCR key
DECR key
APPEND key value
STRLEN key
```

---

## Working with Strings

Examples:
```bash
127.0.0.1:6379> SET greeting "Hello Redis"
OK
127.0.0.1:6379> GET greeting
"Hello Redis"
127.0.0.1:6379> SET counter 10
OK
127.0.0.1:6379> INCR counter
(integer) 11
127.0.0.1:6379> DECR counter
(integer) 10
```

---

## Lists

- Linked lists of string values
- Ordered by insertion
- Operations on both ends (head and tail)

Basic operations:
```bash
LPUSH key value [value ...]
RPUSH key value [value ...]
LPOP key
RPOP key
LRANGE key start stop
```

---

## Working with Lists

Examples:
```bash
127.0.0.1:6379> LPUSH tasks "Send email"
(integer) 1
127.0.0.1:6379> LPUSH tasks "Write report"
(integer) 2
127.0.0.1:6379> RPUSH tasks "Call client"
(integer) 3
127.0.0.1:6379> LRANGE tasks 0 -1
1) "Write report"
2) "Send email"
3) "Call client"
```

---

## Sets

- Unordered collections of unique strings
- Fast membership testing
- Set operations: union, intersection, difference

Basic operations:
```bash
SADD key member [member ...]
SREM key member [member ...]
SMEMBERS key
SISMEMBER key member
SINTER key [key ...]
SUNION key [key ...]
```

---

## Working with Sets

Examples:
```bash
127.0.0.1:6379> SADD tags "redis" "database" "nosql"
(integer) 3
127.0.0.1:6379> SADD tags "database"
(integer) 0
127.0.0.1:6379> SMEMBERS tags
1) "nosql"
2) "redis"
3) "database"
127.0.0.1:6379> SISMEMBER tags "redis"
(integer) 1
```

---

## Sorted Sets

- Like sets, but each element has a score
- Elements ordered by score
- Fast operations by score or position

Basic operations:
```bash
ZADD key score member [score member ...]
ZRANGE key start stop [WITHSCORES]
ZRANK key member
ZREM key member [member ...]
```

---

## Working with Sorted Sets

Examples:
```bash
127.0.0.1:6379> ZADD leaderboard 100 "alice"
(integer) 1
127.0.0.1:6379> ZADD leaderboard 75 "bob"
(integer) 1
127.0.0.1:6379> ZADD leaderboard 150 "carol"
(integer) 1
127.0.0.1:6379> ZRANGE leaderboard 0 -1 WITHSCORES
1) "bob"
2) "75"
3) "alice"
4) "100"
5) "carol"
6) "150"
```

---

## Hashes

- Maps of field-value pairs
- Similar to dictionaries/objects
- Efficient for representing objects

Basic operations:
```bash
HSET key field value [field value ...]
HGET key field
HGETALL key
HDEL key field [field ...]
HEXISTS key field
```

---

## Working with Hashes

Examples:
```bash
127.0.0.1:6379> HSET user:1000 username "john" email "john@example.com" visits 10
(integer) 3
127.0.0.1:6379> HGET user:1000 username
"john"
127.0.0.1:6379> HGETALL user:1000
1) "username"
2) "john"
3) "email"
4) "john@example.com"
5) "visits"
6) "10"
```

---

## Redis Key Management

Key operations:
```bash
EXISTS key [key ...]
DEL key [key ...]
EXPIRE key seconds
TTL key
KEYS pattern
SCAN cursor [MATCH pattern] [COUNT count]
```

---

## Key Naming Conventions

Best practices:
- Use namespaces: `object-type:id:field`
- Examples:
    - `user:1000:followers`
    - `product:5:views`
    - `session:abc123`
- Avoid very long keys
- Be consistent

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="20" text-anchor="middle" font-size="13" font-weight="bold">Key Naming: object-type:id:field</text>
  <rect x="30" y="40" width="160" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="4"/>
  <text x="110" y="65" text-anchor="middle" font-size="11" font-family="monospace">user:1000:name</text>
  <rect x="220" y="40" width="160" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="4"/>
  <text x="300" y="65" text-anchor="middle" font-size="11" font-family="monospace">product:42:views</text>
  <rect x="410" y="40" width="160" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="4"/>
  <text x="490" y="65" text-anchor="middle" font-size="11" font-family="monospace">session:abc123</text>
  <rect x="80" y="110" width="90" height="30" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="3"/>
  <text x="125" y="130" text-anchor="middle" font-size="10">object-type</text>
  <rect x="255" y="110" width="90" height="30" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="3"/>
  <text x="300" y="130" text-anchor="middle" font-size="10">id</text>
  <rect x="430" y="110" width="90" height="30" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="3"/>
  <text x="475" y="130" text-anchor="middle" font-size="10">field</text>
  <line x1="110" y1="80" x2="125" y2="110" stroke="#999" stroke-width="1.5" stroke-dasharray="3,2"/>
  <line x1="300" y1="80" x2="300" y2="110" stroke="#999" stroke-width="1.5" stroke-dasharray="3,2"/>
  <line x1="490" y1="80" x2="475" y2="110" stroke="#999" stroke-width="1.5" stroke-dasharray="3,2"/>
  <text x="300" y="170" text-anchor="middle" font-size="10" fill="#555">Colons (:) separate namespace segments for clarity and consistency</text>
  <text x="300" y="190" text-anchor="middle" font-size="10" fill="#c62828">Avoid very long keys -- keep them readable and short</text>
</svg>

---

## Redis Persistence

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="200" y="10" width="200" height="45" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="30" text-anchor="middle" font-size="12" font-weight="bold">Redis Server (RAM)</text>
  <text x="300" y="45" text-anchor="middle" font-size="10">In-Memory Data</text>
  <rect x="50" y="100" width="140" height="55" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="120" y="120" text-anchor="middle" font-size="12" font-weight="bold">RDB Snapshot</text>
  <text x="120" y="135" text-anchor="middle" font-size="10">Point-in-time .rdb file</text>
  <text x="120" y="148" text-anchor="middle" font-size="10">Compact, fast restart</text>
  <rect x="230" y="100" width="140" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="120" text-anchor="middle" font-size="12" font-weight="bold">AOF Log</text>
  <text x="300" y="135" text-anchor="middle" font-size="10">Append-only file</text>
  <text x="300" y="148" text-anchor="middle" font-size="10">Every write logged</text>
  <rect x="410" y="100" width="140" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="480" y="120" text-anchor="middle" font-size="12" font-weight="bold">RDB + AOF</text>
  <text x="480" y="135" text-anchor="middle" font-size="10">Combined approach</text>
  <text x="480" y="148" text-anchor="middle" font-size="10">Best durability</text>
  <line x1="230" y1="55" x2="120" y2="100" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd5_00_intro)"/>
  <line x1="300" y1="55" x2="300" y2="100" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd5_00_intro)"/>
  <line x1="370" y1="55" x2="480" y2="100" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd5_00_intro)"/>
  <rect x="170" y="170" width="260" height="25" fill="#f0f0f0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="187" text-anchor="middle" font-size="11">Disk Storage (survives restart)</text>
  <defs>
    <marker id="arrowd5_00_intro" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

1. **RDB (Redis Database)**: Point-in-time snapshots
1. **AOF (Append Only File)**: Logs every write operation
1. **Both**: Combined approach
1. **None**: No persistence (pure cache)

---

## Redis Security Basics

Security considerations:
- Bind to specific interfaces
- Password authentication with `requirepass`
- Disable/rename dangerous commands
- Use TLS encryption (Redis 6+)
- Network security (firewalls)

---

## Redis in a Multi-Application Environment

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="20" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="60" y="45" text-anchor="middle" font-size="11" font-weight="bold">Web App</text>
  <rect x="10" y="80" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="60" y="105" text-anchor="middle" font-size="11" font-weight="bold">API Service</text>
  <rect x="10" y="140" width="100" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="60" y="165" text-anchor="middle" font-size="11" font-weight="bold">Worker</text>
  <rect x="220" y="55" width="160" height="90" fill="#ffebee" stroke="#333" stroke-width="2" rx="8"/>
  <text x="300" y="85" text-anchor="middle" font-size="13" font-weight="bold">Redis</text>
  <text x="300" y="100" text-anchor="middle" font-size="10">Shared cache</text>
  <text x="300" y="115" text-anchor="middle" font-size="10">Session store</text>
  <text x="300" y="130" text-anchor="middle" font-size="10">Message broker</text>
  <rect x="470" y="40" width="110" height="50" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="525" y="62" text-anchor="middle" font-size="11" font-weight="bold">Database</text>
  <text x="525" y="77" text-anchor="middle" font-size="10">Primary store</text>
  <rect x="470" y="110" width="110" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="525" y="132" text-anchor="middle" font-size="11" font-weight="bold">Queue</text>
  <text x="525" y="147" text-anchor="middle" font-size="10">Job processing</text>
  <line x1="110" y1="40" x2="220" y2="80" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd6_00_intro)"/>
  <line x1="110" y1="100" x2="220" y2="100" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd6_00_intro)"/>
  <line x1="110" y1="160" x2="220" y2="120" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd6_00_intro)"/>
  <line x1="380" y1="80" x2="470" y2="65" stroke="#999" stroke-width="1.5" stroke-dasharray="4,2" marker-end="url(#arrowd6_00_intro)"/>
  <line x1="380" y1="120" x2="470" y2="135" stroke="#999" stroke-width="1.5" stroke-dasharray="4,2" marker-end="url(#arrowd6_00_intro)"/>
  <defs>
    <marker id="arrowd6_00_intro" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Basic Redis Use Case: Caching

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <line x1="150" y1="50" x2="150" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="450" y1="50" x2="450" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="100" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="400" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-size="12">Actor A</text>
  <text x="450" y="55" text-anchor="middle" font-size="12">Actor B</text>
  <line x1="150" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd7_00_intro)"/>
  <line x1="450" y1="150" x2="150" y2="150" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd7_00_intro)"/>
  <defs>
    <marker id="arrowd7_00_intro" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Basic Redis Use Case: Rate Limiting

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="60" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="70" y="82" text-anchor="middle" font-size="11" font-weight="bold">Client</text>
  <text x="70" y="98" text-anchor="middle" font-size="10">API Request</text>
  <rect x="180" y="30" width="140" height="90" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="250" y="52" text-anchor="middle" font-size="12" font-weight="bold">Redis</text>
  <text x="250" y="68" text-anchor="middle" font-size="10" font-family="monospace">INCR rate:ip:x</text>
  <text x="250" y="83" text-anchor="middle" font-size="10" font-family="monospace">EXPIRE rate:ip:x 60</text>
  <rect x="195" y="96" width="50" height="18" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="2"/>
  <text x="220" y="109" text-anchor="middle" font-size="10">count</text>
  <rect x="255" y="96" width="50" height="18" fill="#fff3e0" stroke="#333" stroke-width="1" rx="2"/>
  <text x="280" y="109" text-anchor="middle" font-size="10">TTL</text>
  <rect x="400" y="25" width="130" height="45" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="465" y="42" text-anchor="middle" font-size="11" font-weight="bold">count &lt; limit</text>
  <text x="465" y="58" text-anchor="middle" font-size="11" fill="#2e7d32">ALLOW</text>
  <rect x="400" y="90" width="130" height="45" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="465" y="108" text-anchor="middle" font-size="11" font-weight="bold">count >= limit</text>
  <text x="465" y="124" text-anchor="middle" font-size="11" fill="#c62828">REJECT 429</text>
  <line x1="120" y1="85" x2="180" y2="75" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd8_00_intro)"/>
  <line x1="320" y1="55" x2="400" y2="47" stroke="#2e7d32" stroke-width="1.5" marker-end="url(#arrowd8_00_intro)"/>
  <line x1="320" y1="95" x2="400" y2="112" stroke="#c62828" stroke-width="1.5" marker-end="url(#arrowd8_00_intro)"/>
  <text x="300" y="165" text-anchor="middle" font-size="10" fill="#555">Each key tracks request count per IP with auto-expiring TTL window</text>
  <text x="300" y="185" text-anchor="middle" font-size="10" fill="#555">Atomic INCR ensures accuracy under concurrent requests</text>
  <defs>
    <marker id="arrowd8_00_intro" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Redis Monitoring

Key commands:
```bash
MONITOR  # Stream of commands (high overhead)
INFO     # Server statistics
SLOWLOG  # Slow query log
CLIENT LIST  # Connected clients
```

Monitoring tools:
- redis-cli
- Redis Dashboard
- Prometheus + Redis Exporter
- Grafana

---

## Lab: Getting Started with Redis

1. Install Redis
1. Connect using redis-cli
1. Try basic commands:
    - SET/GET a key
    - Create a list
    - Add members to a set
    - Create a hash with multiple fields
    - Set expiration on keys
1. Monitor operations using INFO command

---

## Summary

- Redis is an in-memory data structure store
- Supports multiple data types (strings, lists, sets, etc.)
- Fast and versatile, used for caching, messaging, etc.
- Simple to use but powerful
- Offers optional persistence

Next chapter: Redis Data Structures in Depth
