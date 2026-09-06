---
tags:
  - concepts:partitioning
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---

# Partitioning (Sharding)

---

## What This Chapter Covers

- What partitioning is
- Hash partitioning
- Range partitioning
- Consistent hashing
- Rebalancing
- Hot partitions
- Practical guidance

---

## What Partitioning Is

- Split data across multiple nodes
- Each node holds a subset
- Total system capacity = sum of nodes
- Standard scaling pattern past one machine
- Also called *sharding*

---

## Strategies

![partitioning_strategies](svg/courses/architecting/distributed-systems-fundamentals/08_partitioning/partitioning_strategies.svg)

---

## Rebalancing

![rebalancing](svg/courses/architecting/distributed-systems-fundamentals/08_partitioning/rebalancing.svg)

---

## Why Partition

- Scale beyond one machine's capacity
- Localise data (nearer to users)
- Isolate failure (one shard down, others up)
- Improve write throughput
- Foundation for many big-data systems

---

## Hash Partitioning

- Hash the key; modulo by N partitions
- `partition = hash(key) % N`
- Even distribution
- Adding/removing partitions: most keys move
- Mitigated by consistent hashing

---

## Range Partitioning

- Each partition handles a contiguous range
- "Keys A-F on partition 1; G-M on partition 2"
- Good for: range queries
- Bad for: hot ranges (all writes to recent dates land on one partition)
- BigTable, HBase use this

---

## Consistent Hashing

- Hash space arranged in a ring
- Partitions placed on the ring
- Keys hash to a position; assigned to next partition clockwise
- Adding a partition: only nearby keys move
- Used in: DynamoDB, Cassandra, memcached

---

## Virtual Nodes

- Each physical node owns many virtual nodes
- Spreads load more evenly
- Smoother rebalancing
- Cassandra: 256 virtual nodes per physical
- Standard practice

---

## Rebalancing

- Adding / removing nodes triggers data movement
- Naive: lots of data moved
- With consistent hashing: minimal movement
- Still: takes time; can affect performance
- Plan during low-traffic windows

---

## Hot Partitions

- One partition gets disproportionate traffic
- Causes: skewed key distribution
- "Top 10 customers do 80% of orders"
- Mitigation: composite keys, salting, splitting
- Watch: per-partition metrics

---

## Salting

- Add a random prefix to keys
- "user:42" becomes "0:user:42", "1:user:42", "2:user:42"
- Each prefix lands on a different partition
- Trade-off: must query all prefixes to read all of user 42's data
- Use when one entity is unusually hot

---

## Composite Keys

- Partition by `(user_id, date)`, not `(user_id)`
- Spreads one user's data across partitions
- Range queries on date still work per user
- More complex but solves hot-partition problem

---

## Cross-Partition Operations

- Joins across partitions: expensive
- Distributed transactions: doubly expensive
- Best: design schema so most operations stay within one partition
- Hard: requires careful key design upfront

---

## Partition Awareness

- Clients knowing which partition a key lives on
- Direct connection to the right node
- Saves a hop through a coordinator
- Cassandra, MongoDB, DynamoDB: client routing
- Reduces latency

---

## Resharding

- The original number of partitions was wrong
- Need more (or fewer) partitions
- Massive operation; days of data movement
- Tools (e.g., Vitess for MySQL) automate
- Plan capacity well; don't reshard often

---

## Common Partitioning Mistakes

- Using user_id as the partition key when one user dominates
- Range partitioning by date (most writes hit the latest partition)
- Forgetting cross-partition queries are expensive
- No metrics on per-partition load
- Resharding under-tested in production

---

## Practical Tips

- Partition by something that distributes evenly
- Watch for skew; alert on hot partitions
- Use consistent hashing for online rebalancing
- Test schema with realistic data distribution
- Keep most queries within one partition
