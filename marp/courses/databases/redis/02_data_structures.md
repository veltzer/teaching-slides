# Redis Data Structures

---

## Redis Data Structures Overview

- Data structures are the foundation of Redis
- Each structure optimized for specific use cases
- Atomic operations on all data types
- Commands named by structure prefix:
    - `STR...` for Strings
    - `L...` for Lists
    - `H...` for Hashes
    - `S...` for Sets
    - `Z...` for Sorted Sets

---

## String Operations Recap

Strings are the most basic Redis data type:

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="25" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Redis String: Key-Value Storage</text>
  <rect x="30" y="50" width="120" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="75" text-anchor="middle" font-size="11" font-weight="bold">Key</text>
  <rect x="160" y="50" width="160" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="240" y="75" text-anchor="middle" font-size="11">Value (up to 512MB)</text>
  <rect x="30" y="105" width="120" height="35" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="127" text-anchor="middle" font-size="10">"user:name"</text>
  <rect x="160" y="105" width="160" height="35" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="240" y="127" text-anchor="middle" font-size="10">"Alice"</text>
  <rect x="30" y="150" width="120" height="35" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="172" text-anchor="middle" font-size="10">"counter"</text>
  <rect x="160" y="150" width="160" height="35" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="240" y="172" text-anchor="middle" font-size="10">42 (integer)</text>
  <rect x="370" y="70" width="200" height="110" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="470" y="95" text-anchor="middle" font-size="11" font-weight="bold">Operations</text>
  <text x="470" y="115" text-anchor="middle" font-size="10">SET / GET</text>
  <text x="470" y="133" text-anchor="middle" font-size="10">INCR / DECR</text>
  <text x="470" y="151" text-anchor="middle" font-size="10">MSET / MGET</text>
  <text x="470" y="169" text-anchor="middle" font-size="10">APPEND / STRLEN</text>
</svg>

Basic operations:
```bash
SET key value [EX seconds] [PX milliseconds] [NX|XX]
GET key
MSET key value [key value ...]
MGET key [key ...]
```

---

## String Advanced Operations

```bash
# Incrementing/decrementing
INCR key              # Increment integer by 1
INCRBY key increment  # Increment by specific amount
INCRBYFLOAT key increment # Increment by float value
DECR key              # Decrement integer by 1
DECRBY key decrement  # Decrement by specific amount

# String manipulation
APPEND key value      # Append to string
GETRANGE key start end # Get substring
SETRANGE key offset value # Overwrite part of string
STRLEN key            # Get string length
```

---

## String Use Cases

1. **Caching**:
    - Cache API responses, HTML fragments, user data

1. **Counters**:
    - Page views, likes, votes
    - Atomic increments/decrements

1. **Rate limiting**:
    - Track API calls per user
    - Use `INCR` with `EXPIRE`

1. **Locks**:
    - Distributed locks with `SET key value NX PX milliseconds`

---

## Implementing a Counter with Redis Strings

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <line x1="150" y1="50" x2="150" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="450" y1="50" x2="450" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="100" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="400" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-size="12">Actor A</text>
  <text x="450" y="55" text-anchor="middle" font-size="12">Actor B</text>
  <line x1="150" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_01_data_structures)"/>
  <line x1="450" y1="150" x2="150" y2="150" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd1_01_data_structures)"/>
  <defs>
    <marker id="arrowd1_01_data_structures" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## String Bit Operations

Strings can be used as bit arrays:

```bash
SETBIT key offset value   # Set bit at offset
GETBIT key offset         # Get bit at offset
BITCOUNT key [start] [end] # Count set bits
BITOP operation destkey key [key ...] # Bitwise operations
BITPOS key bit [start] [end] # Find first set/unset bit
```

Use cases:
- User presence tracking (online/offline)
- Feature flags
- Real-time analytics

---

## List Operations Recap

Lists are linked lists of string values:

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="25" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Redis List: Doubly-Linked List</text>
  <text x="35" y="80" text-anchor="middle" font-size="10" fill="#333">HEAD</text>
  <text x="565" y="80" text-anchor="middle" font-size="10" fill="#333">TAIL</text>
  <rect x="60" y="65" width="90" height="45" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="83" text-anchor="middle" font-size="10">"task1"</text>
  <text x="105" y="100" text-anchor="middle" font-size="9" fill="#666">index 0</text>
  <rect x="195" y="65" width="90" height="45" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="240" y="83" text-anchor="middle" font-size="10">"task2"</text>
  <text x="240" y="100" text-anchor="middle" font-size="9" fill="#666">index 1</text>
  <rect x="330" y="65" width="90" height="45" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="375" y="83" text-anchor="middle" font-size="10">"task3"</text>
  <text x="375" y="100" text-anchor="middle" font-size="9" fill="#666">index 2</text>
  <rect x="465" y="65" width="90" height="45" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="83" text-anchor="middle" font-size="10">"task4"</text>
  <text x="510" y="100" text-anchor="middle" font-size="9" fill="#666">index 3</text>
  <line x1="150" y1="87" x2="193" y2="87" stroke="#333" stroke-width="2" marker-end="url(#arrowd2)"/>
  <line x1="285" y1="87" x2="328" y2="87" stroke="#333" stroke-width="2" marker-end="url(#arrowd2)"/>
  <line x1="420" y1="87" x2="463" y2="87" stroke="#333" stroke-width="2" marker-end="url(#arrowd2)"/>
  <line x1="193" y1="93" x2="150" y2="93" stroke="#333" stroke-width="2" marker-end="url(#arrowd2)"/>
  <line x1="328" y1="93" x2="285" y2="93" stroke="#333" stroke-width="2" marker-end="url(#arrowd2)"/>
  <line x1="463" y1="93" x2="420" y2="93" stroke="#333" stroke-width="2" marker-end="url(#arrowd2)"/>
  <text x="105" y="145" text-anchor="middle" font-size="10" fill="#1565c0">LPUSH</text>
  <path d="M105,148 L105,165 L70,165" stroke="#1565c0" stroke-width="1.5" fill="none" marker-end="url(#arrowblue2)"/>
  <text x="510" y="145" text-anchor="middle" font-size="10" fill="#4a148c">RPUSH</text>
  <path d="M510,148 L510,165 L545,165" stroke="#4a148c" stroke-width="1.5" fill="none" marker-end="url(#arrowpurp2)"/>
  <text x="300" y="185" text-anchor="middle" font-size="10" fill="#333">LPOP / RPOP remove from head / tail</text>
  <defs>
    <marker id="arrowd2" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#333"/></marker>
    <marker id="arrowblue2" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#1565c0"/></marker>
    <marker id="arrowpurp2" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#4a148c"/></marker>
  </defs>
</svg>

Basic operations:
```bash
LPUSH key value [value ...]  # Push to head
RPUSH key value [value ...]  # Push to tail
LPOP key [count]             # Pop from head
RPOP key [count]             # Pop from tail
LRANGE key start stop        # Get range of elements
```

---

## List Advanced Operations

```bash
# Element manipulation
LINDEX key index           # Get element at index
LINSERT key BEFORE|AFTER pivot value # Insert element
LLEN key                   # Get list length
LSET key index value       # Set element at index
LTRIM key start stop       # Trim list to range

# Blocking operations
BLPOP key [key ...] timeout # Blocking pop from head
BRPOP key [key ...] timeout # Blocking pop from tail
BRPOPLPUSH source destination timeout # Pop from one list, push to another
```

---

## List Use Cases

1. **Activity feeds**:
    - Recent user actions
    - Latest posts or notifications

1. **Job/task queues**:
    - Workers consume tasks with `LPOP` or `BLPOP`
    - Tasks added with `RPUSH`

1. **Limited collections**:
    - Latest news articles
    - Recent searches
    - Use `LPUSH` + `LTRIM` pattern

---

## Implementing a Task Queue with Redis Lists

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <line x1="150" y1="50" x2="150" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="450" y1="50" x2="450" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="100" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="400" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-size="12">Actor A</text>
  <text x="450" y="55" text-anchor="middle" font-size="12">Actor B</text>
  <line x1="150" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_01_data_structures)"/>
  <line x1="450" y1="150" x2="150" y2="150" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd3_01_data_structures)"/>
  <defs>
    <marker id="arrowd3_01_data_structures" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Set Operations Recap

Sets are unordered collections of unique strings:

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Redis Set: Unordered Unique Members</text>
  <text x="120" y="45" text-anchor="middle" font-size="11" fill="#333">tags:article:42</text>
  <ellipse cx="120" cy="120" rx="105" ry="70" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="80" y="85" text-anchor="middle" font-size="10">"redis"</text>
  <text x="140" y="100" text-anchor="middle" font-size="10">"nosql"</text>
  <text x="95" y="120" text-anchor="middle" font-size="10">"database"</text>
  <text x="150" y="140" text-anchor="middle" font-size="10">"cache"</text>
  <text x="105" y="155" text-anchor="middle" font-size="10">"fast"</text>
  <rect x="280" y="60" width="130" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="345" y="80" text-anchor="middle" font-size="10">SADD "python"</text>
  <rect x="280" y="100" width="130" height="30" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="345" y="120" text-anchor="middle" font-size="10">SREM "cache"</text>
  <rect x="280" y="140" width="130" height="30" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="345" y="160" text-anchor="middle" font-size="10">SISMEMBER "redis"</text>
  <text x="460" y="80" text-anchor="middle" font-size="10" fill="#2e7d32">+ added</text>
  <text x="460" y="120" text-anchor="middle" font-size="10" fill="#e65100">- removed</text>
  <text x="460" y="160" text-anchor="middle" font-size="10" fill="#4a148c">= true</text>
  <text x="300" y="195" text-anchor="middle" font-size="10" fill="#666">No duplicates allowed; O(1) membership check</text>
</svg>

Basic operations:
```bash
SADD key member [member ...]    # Add members
SREM key member [member ...]    # Remove members
SMEMBERS key                    # Get all members
SISMEMBER key member            # Check if member exists
```

---

## Set Advanced Operations

```bash
# Set operations
SINTER key [key ...]           # Intersection of sets
SINTERSTORE destination key [key ...] # Store intersection
SUNION key [key ...]           # Union of sets
SUNIONSTORE destination key [key ...] # Store union
SDIFF key [key ...]            # Difference of sets
SDIFFSTORE destination key [key ...] # Store difference

# Other operations
SCARD key                      # Get set cardinality (size)
SPOP key [count]               # Remove and return random members
SRANDMEMBER key [count]        # Get random members
```

---

## Set Operations Visualization

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Set Operations: SINTER, SUNION, SDIFF</text>
  <ellipse cx="180" cy="115" rx="100" ry="70" fill="#e3f2fd" stroke="#333" stroke-width="2" fill-opacity="0.7"/>
  <ellipse cx="340" cy="115" rx="100" ry="70" fill="#f3e5f5" stroke="#333" stroke-width="2" fill-opacity="0.7"/>
  <text x="180" y="50" text-anchor="middle" font-size="11" font-weight="bold">Set A</text>
  <text x="340" y="50" text-anchor="middle" font-size="11" font-weight="bold">Set B</text>
  <text x="130" y="105" text-anchor="middle" font-size="10">"alice"</text>
  <text x="130" y="125" text-anchor="middle" font-size="10">"bob"</text>
  <text x="260" y="105" text-anchor="middle" font-size="10" font-weight="bold" fill="#c62828">"carol"</text>
  <text x="260" y="125" text-anchor="middle" font-size="10" font-weight="bold" fill="#c62828">"dave"</text>
  <text x="385" y="105" text-anchor="middle" font-size="10">"eve"</text>
  <text x="385" y="125" text-anchor="middle" font-size="10">"frank"</text>
  <rect x="460" y="55" width="130" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="4"/>
  <text x="525" y="74" text-anchor="middle" font-size="10">SINTER: carol, dave</text>
  <rect x="460" y="95" width="130" height="30" fill="#fff3e0" stroke="#333" stroke-width="1" rx="4"/>
  <text x="525" y="114" text-anchor="middle" font-size="10">SDIFF A B: alice, bob</text>
  <rect x="460" y="135" width="130" height="30" fill="#ffebee" stroke="#333" stroke-width="1" rx="4"/>
  <text x="525" y="154" text-anchor="middle" font-size="10">SUNION: all six</text>
  <text x="260" y="195" text-anchor="middle" font-size="10" fill="#c62828">Intersection (shared members)</text>
</svg>

---

## Set Use Cases

1. **Unique items**:
    - Unique visitors
    - User permissions

1. **Tagging systems**:
    - Articles, posts, products
    - Efficient lookups by tag

1. **Common relationships**:
    - Find mutual friends: `SINTER friends:user1 friends:user2`
    - Recommendation systems

1. **Random selection**:
    - Randomly select winners from contest entries
    - Poll sampling

---

## Implementing Tag Filtering with Redis Sets

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <line x1="150" y1="50" x2="150" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="450" y1="50" x2="450" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="100" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="400" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-size="12">Actor A</text>
  <text x="450" y="55" text-anchor="middle" font-size="12">Actor B</text>
  <line x1="150" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_01_data_structures)"/>
  <line x1="450" y1="150" x2="150" y2="150" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd6_01_data_structures)"/>
  <defs>
    <marker id="arrowd6_01_data_structures" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Sorted Set Operations Recap

Sorted sets are sets with scores (ordering values):

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Redis Sorted Set: Members Ordered by Score</text>
  <text x="300" y="45" text-anchor="middle" font-size="11" fill="#333">leaderboard:game1</text>
  <rect x="30" y="60" width="100" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="80" y="80" text-anchor="middle" font-size="10" font-weight="bold">score: 150</text>
  <text x="80" y="100" text-anchor="middle" font-size="10">"alice"</text>
  <rect x="155" y="60" width="100" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="205" y="80" text-anchor="middle" font-size="10" font-weight="bold">score: 320</text>
  <text x="205" y="100" text-anchor="middle" font-size="10">"bob"</text>
  <rect x="280" y="60" width="100" height="55" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="330" y="80" text-anchor="middle" font-size="10" font-weight="bold">score: 475</text>
  <text x="330" y="100" text-anchor="middle" font-size="10">"carol"</text>
  <rect x="405" y="60" width="100" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="455" y="80" text-anchor="middle" font-size="10" font-weight="bold">score: 890</text>
  <text x="455" y="100" text-anchor="middle" font-size="10">"dave"</text>
  <line x1="30" y1="130" x2="505" y2="130" stroke="#333" stroke-width="1"/>
  <text x="30" y="145" font-size="10" fill="#666">low score</text>
  <text x="505" y="145" text-anchor="end" font-size="10" fill="#666">high score</text>
  <text x="80" y="170" text-anchor="middle" font-size="10" fill="#2e7d32">rank 0</text>
  <text x="205" y="170" text-anchor="middle" font-size="10" fill="#1565c0">rank 1</text>
  <text x="330" y="170" text-anchor="middle" font-size="10" fill="#4a148c">rank 2</text>
  <text x="455" y="170" text-anchor="middle" font-size="10" fill="#e65100">rank 3</text>
  <text x="300" y="195" text-anchor="middle" font-size="10" fill="#666">ZRANGE returns by rank; ZRANGEBYSCORE returns by score range</text>
</svg>

Basic operations:
```bash
ZADD key score member [score member ...] # Add members with scores
ZRANGE key start stop [WITHSCORES]      # Get range by index
ZRANGEBYSCORE key min max [WITHSCORES]  # Get range by score
ZREM key member [member ...]            # Remove members
```

---

## Sorted Set Advanced Operations

```bash
# Retrieving by rank/score
ZRANK key member                 # Get rank of member (ascending)
ZREVRANK key member              # Get rank of member (descending)
ZREVRANGE key start stop [WITHSCORES] # Get range by index, descending
ZREVRANGEBYSCORE key max min [WITHSCORES] # Get range by score, descending

# Score manipulation
ZINCRBY key increment member     # Increment score of member
ZSCORE key member                # Get score of member

# Other operations
ZCARD key                        # Get sorted set cardinality
ZCOUNT key min max               # Count members with scores in range
ZPOPMIN key [count]              # Remove and return members with lowest scores
ZPOPMAX key [count]              # Remove and return members with highest scores
```

---

## Sorted Set Use Cases

1. **Leaderboards**:
    - Game scores
    - Social media metrics

1. **Time-series data**:
    - Use timestamp as score
    - Range queries by time

1. **Weighted queues**:
    - Priority processing
    - Task scheduling

1. **Ranking systems**:
    - Product ratings
    - Search suggestions with weights

---

## Implementing a Leaderboard with Redis Sorted Sets

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <line x1="150" y1="50" x2="150" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="450" y1="50" x2="450" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="100" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="400" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-size="12">Actor A</text>
  <text x="450" y="55" text-anchor="middle" font-size="12">Actor B</text>
  <line x1="150" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd8_01_data_structures)"/>
  <line x1="450" y1="150" x2="150" y2="150" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd8_01_data_structures)"/>
  <defs>
    <marker id="arrowd8_01_data_structures" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Hash Operations Recap

Hashes are maps of field-value pairs:

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Redis Hash: Field-Value Map</text>
  <rect x="30" y="40" width="130" height="30" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="95" y="60" text-anchor="middle" font-size="11" font-weight="bold">user:1001</text>
  <line x1="160" y1="55" x2="190" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arrowd9)"/>
  <rect x="195" y="35" width="380" height="155" fill="#fff" stroke="#333" stroke-width="2" rx="5"/>
  <text x="385" y="55" text-anchor="middle" font-size="11" font-weight="bold" fill="#333">Hash Fields</text>
  <rect x="210" y="65" width="100" height="28" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="260" y="84" text-anchor="middle" font-size="10">name</text>
  <rect x="320" y="65" width="240" height="28" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="440" y="84" text-anchor="middle" font-size="10">"Alice Smith"</text>
  <rect x="210" y="100" width="100" height="28" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="260" y="119" text-anchor="middle" font-size="10">email</text>
  <rect x="320" y="100" width="240" height="28" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="440" y="119" text-anchor="middle" font-size="10">"alice@example.com"</text>
  <rect x="210" y="135" width="100" height="28" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="260" y="154" text-anchor="middle" font-size="10">login_count</text>
  <rect x="320" y="135" width="240" height="28" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="440" y="154" text-anchor="middle" font-size="10">47 (HINCRBY increments this)</text>
  <text x="95" y="195" text-anchor="middle" font-size="10" fill="#666">HSET / HGET</text>
  <text x="300" y="195" text-anchor="middle" font-size="10" fill="#666">HGETALL returns all pairs</text>
  <defs>
    <marker id="arrowd9" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#333"/></marker>
  </defs>
</svg>

Basic operations:
```bash
HSET key field value [field value ...] # Set hash fields
HGET key field                        # Get value of field
HMGET key field [field ...]           # Get values of multiple fields
HGETALL key                           # Get all fields and values
```

---

## Hash Advanced Operations

```bash
# Field manipulation
HDEL key field [field ...]           # Delete fields
HEXISTS key field                    # Check if field exists
HINCRBY key field increment          # Increment integer field
HINCRBYFLOAT key field increment     # Increment float field

# Other operations
HKEYS key                            # Get all fields
HVALS key                            # Get all values
HLEN key                             # Get number of fields
HSTRLEN key field                    # Get length of field value
HSCAN key cursor [MATCH pattern] [COUNT count] # Scan through fields
```

---

## Hash Use Cases

1. **Object representation**:
    - User profiles
    - Product details
    - Session data

1. **Counters per category**:
    - Page views by section
    - Votes by category

1. **Rate limiting**:
    - Track multiple limits for single entity
    - Different time windows

1. **Configuration storage**:
    - Application settings
    - Feature toggles

---

## Implementing User Profiles with Redis Hashes

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <line x1="150" y1="50" x2="150" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="450" y1="50" x2="450" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="100" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="400" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-size="12">Actor A</text>
  <text x="450" y="55" text-anchor="middle" font-size="12">Actor B</text>
  <line x1="150" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd10_01_data_structures)"/>
  <line x1="450" y1="150" x2="150" y2="150" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd10_01_data_structures)"/>
  <defs>
    <marker id="arrowd10_01_data_structures" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Streams Introduction

Streams (added in Redis 5.0):
- Append-only log data structures
- Similar to Kafka/messaging systems
- Support consumer groups

Basic operations:
```bash
XADD key ID field value [field value ...] # Add entry to stream
XREAD [COUNT count] [BLOCK milliseconds] STREAMS key [key ...] ID [ID ...] # Read from streams
XRANGE key start end [COUNT count]       # Read range of entries
XLEN key                                 # Get stream length
```

---

## HyperLogLog Introduction

HyperLogLog:
- Probabilistic data structure
- Estimates cardinality (unique elements)
- Very memory efficient (12kB max)

Basic operations:
```bash
PFADD key element [element ...]         # Add elements
PFCOUNT key [key ...]                   # Get estimated cardinality
PFMERGE destkey sourcekey [sourcekey ...] # Merge HyperLogLogs
```

Use cases:
- Unique visitors
- Metrics on large datasets
- When approximate count is acceptable

---

## Geospatial Data Introduction

Geospatial commands:
- Store and query points on Earth
- Implemented using sorted sets

Basic operations:
```bash
GEOADD key longitude latitude member [longitude latitude member ...] # Add locations
GEODIST key member1 member2 [unit]      # Get distance between points
GEOSEARCH key [FROMMEMBER member | FROMLONLAT longitude latitude] [BYRADIUS radius unit | BYBOX width height unit] [ASC | DESC] [WITHCOORD] [WITHDIST] [WITHHASH] [COUNT count] # Search within area
```

---

## Bitmaps Introduction

Bitmaps (implemented using strings):
- String operations treating strings as bit arrays
- Very memory efficient

Basic operations:
```bash
SETBIT key offset value                 # Set bit at offset
GETBIT key offset                       # Get bit at offset
BITCOUNT key [start end]                # Count set bits
BITOP operation destkey key [key ...]   # Bitwise operations
```

Use case: User online status tracking

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Bitmap: User Online Status Tracking</text>
  <text x="300" y="42" text-anchor="middle" font-size="10" fill="#666">Key: "online:2024-03-23" -- each bit = one user ID</text>
  <text x="35" y="78" text-anchor="middle" font-size="10" fill="#333">Bit offset:</text>
  <text x="110" y="78" text-anchor="middle" font-size="10">0</text>
  <text x="150" y="78" text-anchor="middle" font-size="10">1</text>
  <text x="190" y="78" text-anchor="middle" font-size="10">2</text>
  <text x="230" y="78" text-anchor="middle" font-size="10">3</text>
  <text x="270" y="78" text-anchor="middle" font-size="10">4</text>
  <text x="310" y="78" text-anchor="middle" font-size="10">5</text>
  <text x="350" y="78" text-anchor="middle" font-size="10">6</text>
  <text x="390" y="78" text-anchor="middle" font-size="10">7</text>
  <rect x="90" y="85" width="40" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="110" y="105" text-anchor="middle" font-size="12" font-weight="bold" fill="#2e7d32">1</text>
  <rect x="130" y="85" width="40" height="30" fill="#ffebee" stroke="#333" stroke-width="1.5"/>
  <text x="150" y="105" text-anchor="middle" font-size="12" fill="#c62828">0</text>
  <rect x="170" y="85" width="40" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="190" y="105" text-anchor="middle" font-size="12" font-weight="bold" fill="#2e7d32">1</text>
  <rect x="210" y="85" width="40" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="230" y="105" text-anchor="middle" font-size="12" font-weight="bold" fill="#2e7d32">1</text>
  <rect x="250" y="85" width="40" height="30" fill="#ffebee" stroke="#333" stroke-width="1.5"/>
  <text x="270" y="105" text-anchor="middle" font-size="12" fill="#c62828">0</text>
  <rect x="290" y="85" width="40" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="310" y="105" text-anchor="middle" font-size="12" font-weight="bold" fill="#2e7d32">1</text>
  <rect x="330" y="85" width="40" height="30" fill="#ffebee" stroke="#333" stroke-width="1.5"/>
  <text x="350" y="105" text-anchor="middle" font-size="12" fill="#c62828">0</text>
  <rect x="370" y="85" width="40" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="390" y="105" text-anchor="middle" font-size="12" font-weight="bold" fill="#2e7d32">1</text>
  <text x="110" y="130" text-anchor="middle" font-size="9" fill="#2e7d32">online</text>
  <text x="150" y="130" text-anchor="middle" font-size="9" fill="#c62828">offline</text>
  <text x="300" y="155" text-anchor="middle" font-size="10" fill="#333">SETBIT online:2024-03-23 0 1  -- mark user 0 as online</text>
  <text x="300" y="172" text-anchor="middle" font-size="10" fill="#333">BITCOUNT online:2024-03-23    -- returns 5 (users online)</text>
  <text x="300" y="192" text-anchor="middle" font-size="10" fill="#666">1 million users = only 125 KB of memory</text>
</svg>

---

## Choosing the Right Data Structure

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="20" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Choosing the Right Data Structure</text>
  <rect x="15" y="35" width="105" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="67" y="52" text-anchor="middle" font-size="10" font-weight="bold">String</text>
  <text x="67" y="66" text-anchor="middle" font-size="9">simple values</text>
  <rect x="130" y="35" width="105" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="182" y="52" text-anchor="middle" font-size="10" font-weight="bold">List</text>
  <text x="182" y="66" text-anchor="middle" font-size="9">ordered, queues</text>
  <rect x="245" y="35" width="105" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="297" y="52" text-anchor="middle" font-size="10" font-weight="bold">Set</text>
  <text x="297" y="66" text-anchor="middle" font-size="9">unique, unordered</text>
  <rect x="360" y="35" width="105" height="40" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="412" y="52" text-anchor="middle" font-size="10" font-weight="bold">Sorted Set</text>
  <text x="412" y="66" text-anchor="middle" font-size="9">ranked, scored</text>
  <rect x="475" y="35" width="105" height="40" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="527" y="52" text-anchor="middle" font-size="10" font-weight="bold">Hash</text>
  <text x="527" y="66" text-anchor="middle" font-size="9">objects, fields</text>
  <rect x="30" y="90" width="540" height="100" fill="#f5f5f5" stroke="#333" stroke-width="1" rx="5"/>
  <text x="50" y="110" font-size="10" fill="#333">Need a counter or cache?</text>
  <text x="370" y="110" font-size="10" font-weight="bold" fill="#1565c0">String</text>
  <text x="50" y="128" font-size="10" fill="#333">Need FIFO queue or recent items?</text>
  <text x="370" y="128" font-size="10" font-weight="bold" fill="#4a148c">List</text>
  <text x="50" y="146" font-size="10" fill="#333">Need unique members or set operations?</text>
  <text x="370" y="146" font-size="10" font-weight="bold" fill="#2e7d32">Set</text>
  <text x="50" y="164" font-size="10" fill="#333">Need ranking or score-based queries?</text>
  <text x="370" y="164" font-size="10" font-weight="bold" fill="#e65100">Sorted Set</text>
  <text x="50" y="182" font-size="10" fill="#333">Need to store object with multiple fields?</text>
  <text x="370" y="182" font-size="10" font-weight="bold" fill="#c62828">Hash</text>
</svg>

---

## Memory Usage Comparison

Data structure efficiency (for 1 million items):

1. **Strings**: ~80-120MB (depends on value size)
1. **Lists**: ~100MB (linked list overhead)
1. **Sets**: ~80MB (hash table implementation)
1. **Sorted Sets**: ~120MB (skip list + hash table)
1. **Hashes**: ~70MB (with small fields, very efficient)
1. **HyperLogLog**: 12kB (regardless of cardinality)
1. **Bitmaps**: ~125kB (for 1M bits)

---

## Performance Considerations

---

## Data Structure Patterns: Composite Keys

Using multiple data structures together:

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="20" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Composite Keys: E-commerce Product Example</text>
  <rect x="20" y="35" width="130" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="85" y="55" text-anchor="middle" font-size="10" font-weight="bold">Hash</text>
  <text x="85" y="73" text-anchor="middle" font-size="9">product:42:details</text>
  <rect x="20" y="95" width="130" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="85" y="115" text-anchor="middle" font-size="10" font-weight="bold">Sorted Set</text>
  <text x="85" y="133" text-anchor="middle" font-size="9">product:42:reviews</text>
  <rect x="20" y="155" width="130" height="35" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="85" y="177" text-anchor="middle" font-size="10" font-weight="bold">Set</text>
  <line x1="150" y1="60" x2="190" y2="60" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd14)"/>
  <line x1="150" y1="120" x2="190" y2="120" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd14)"/>
  <line x1="150" y1="172" x2="190" y2="172" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd14)"/>
  <text x="380" y="50" font-size="10" fill="#333">name="Widget" price="29.99" stock="150"</text>
  <text x="380" y="70" font-size="9" fill="#666">HSET / HGET / HINCRBY stock</text>
  <text x="380" y="110" font-size="10" fill="#333">user:7 score:5, user:12 score:3, ...</text>
  <text x="380" y="130" font-size="9" fill="#666">ZADD / ZRANGEBYSCORE for filtering</text>
  <text x="380" y="168" font-size="10" fill="#333">product:42:tags = {"electronics","sale"}</text>
  <text x="380" y="185" font-size="9" fill="#666">SADD / SINTER for tag-based search</text>
  <rect x="190" y="40" width="400" height="40" fill="none" stroke="#e3f2fd" stroke-width="1" rx="3"/>
  <rect x="190" y="100" width="400" height="40" fill="none" stroke="#f3e5f5" stroke-width="1" rx="3"/>
  <rect x="190" y="155" width="400" height="40" fill="none" stroke="#e8f5e9" stroke-width="1" rx="3"/>
  <defs>
    <marker id="arrowd14" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#333"/></marker>
  </defs>
</svg>

---

## Data Structure Patterns: Counters

Different counter implementations:

1. **Simple Counter**: `INCR counter:visits`
1. **Time-based Counter**: `HINCRBY counter:daily:20240323 visits 1`
1. **Per-entity Counter**: `HINCRBY counter:article:1234 views 1`
1. **Atomic Counter**: `INCR counter:global`

Counters can be:
- Global vs. scoped
- Persistent vs. temporary
- Simple vs. time-windowed

---

## Lab: Redis Data Structures

1. **Strings**: Implement a view counter for a page
1. **Lists**: Create a simple task queue
1. **Sets**: Build a tag system for articles
1. **Sorted Sets**: Create a leaderboard
1. **Hashes**: Store and retrieve user profiles
1. **Streams**: Log user actions
1. Advanced: Combine multiple data structures

---

## Summary

- Redis provides specialized data structures
- Each structure has optimal use cases
- Strings: simple values, counters
- Lists: ordered elements, queues
- Sets: unique elements, relationships
- Sorted Sets: scored elements, rankings
- Hashes: field-value pairs, objects
- Special types: Streams, HyperLogLog, Geospatial, Bitmaps

Next chapter: Caching with Redis
