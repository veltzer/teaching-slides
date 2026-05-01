---
tags:
  - architecture:system-design
  - architecture:hashing
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# Consistent Hashing

---
## What This Chapter Covers

- The problem: rebalancing
- Hash modulo's failure mode
- The ring
- Virtual nodes
- Replicas on the ring
- Where it's used

---
## The Problem

- N servers, hash(key) % N decides which
- Add/remove a server: most keys remap
- Cache miss storm
- Consistent hashing: minimal remapping

---
## Hash Modulo

- `partition = hash(key) % N`
- N=4 &#8594; 5: ~80% of keys move
- Bad for cache, sharded DBs

---
## The Ring

- Hash space arranged in a circle
- Servers placed on ring at hashed positions
- Keys hash to a position
- Assigned to next server clockwise
- Adding a server: only nearby keys move

---
## Virtual Nodes

- Each physical server owns many virtual positions
- More even distribution
- Smoother rebalance
- Common: 100-256 virtual nodes per server

---
## Replicas

- Key mapped to N adjacent servers
- All N hold a copy
- Primary: first; secondaries: next
- Used in: Cassandra, DynamoDB

---
## Removing A Server

- Server dies / drained
- Its keys move to neighbours
- Other keys unaffected
- Fast recovery

---
## Adding A Server

- New server takes over some range
- Only keys in that range move
- Smooth, online operation
- vs hash modulo: massive movement

---
## Performance

- Hashing: O(1)
- Lookup: O(log N) with sorted ring
- Constant in practice
- Fast even with thousands of nodes

---
## Where It's Used

- Memcached clients (consistent hashing)
- DynamoDB internal
- Cassandra
- Akamai (CDN)
- Standard pattern at scale

---
## Implementation

- Hash function: murmur3, FNV, SHA-1 truncated
- Sorted set / sorted map for the ring
- Bisect to find next server
- Library exists in most languages

---
## Pitfalls

- Skewed key distribution: hot servers
- Mitigate: better hash; salt the keys
- Virtual nodes help; don't fully solve
- Monitor per-server load

---
## Beyond Consistent Hashing

- Rendezvous (highest random weight) hashing: alternative
- Jump hash: very compact; less flexible
- Maglev: Google's; fast under failures
- Each fits different needs

---
## Common Mistakes

- Hash modulo at scale
- Too few virtual nodes (uneven distribution)
- No replicas (no fault tolerance)
- Manual placement instead of hash-based
