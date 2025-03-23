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

![0](../../../out/mermaid/marp/courses/redis/00_intro.md/0.png)

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

![1](../../../out/mermaid/marp/courses/redis/00_intro.md/1.png)

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

![2](../../../out/mermaid/marp/courses/redis/00_intro.md/2.png)

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

![3](../../../out/mermaid/marp/courses/redis/00_intro.md/3.png)

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

![4](../../../out/mermaid/marp/courses/redis/00_intro.md/4.png)

---

## Redis Persistence

![5](../../../out/mermaid/marp/courses/redis/00_intro.md/5.png)

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

![6](../../../out/mermaid/marp/courses/redis/00_intro.md/6.png)

---

## Basic Redis Use Case: Caching

![7](../../../out/mermaid/marp/courses/redis/00_intro.md/7.png)

---

## Basic Redis Use Case: Rate Limiting

![8](../../../out/mermaid/marp/courses/redis/00_intro.md/8.png)

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
