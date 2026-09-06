---
tags:
  - architecture:system-design
  - databases:scaling
level: intermediate
category: architecture
audience:
  - audiences:developers

---

# Database Design and Scaling

---

## Scaling Paths

![scaling_paths](svg/courses/architecting/system-design/05_database_design_and_scaling/scaling_paths.svg)

---

## Sharding Styles

![sharding_styles](svg/courses/architecting/system-design/05_database_design_and_scaling/sharding_styles.svg)

---

## What This Chapter Covers

- SQL vs NoSQL choice
- Normalisation and denormalisation
- Indexes
- Read replicas
- Sharding
- Caching layers
- Database connection pooling

---

## SQL vs NoSQL

- SQL: relational, ACID, schema-on-write, joins
- NoSQL: various models (document, key-value, wide-column, graph)
- SQL: best when relations matter
- NoSQL: best when scaling reads / writes is the constraint
- Most apps: SQL is enough

---

## Normalisation

- Reduce redundancy
- 1NF, 2NF, 3NF... most apps stop at 3NF
- Saves storage; complicates queries
- Default for transactional systems

---

## Denormalisation

- Duplicate data for read speed
- Common in: read-heavy systems, NoSQL, analytics
- Trade-off: storage and update complexity for query speed
- Modern: often denormalise for the read path

---

## Indexes

- Trade write speed for read speed
- B-tree, hash, GIN, GiST...
- Each index slows writes
- Per-table: 3-5 indexes typical
- Composite indexes for compound queries

---

## Index Mistakes

- Indexing every column (slow writes)
- Wrong column order in composite indexes
- Indexes that aren't used (waste)
- Missing index on frequently-queried column

---

## Read Replicas

- Followers replicate from leader
- Reads can hit replicas; scales reads
- Replication lag: stale reads possible
- Async vs sync replication
- Standard in cloud DBs

---

## Sharding

- Split data across nodes
- Hash-based, range-based, directory-based
- Cross-shard queries: expensive
- Operational complexity high
- Consider only when single-node hits limits

---

## Connection Pooling

- DB connections expensive
- App pools connections; reuses
- Tools: pgbouncer (Postgres), ProxySQL (MySQL), RDS Proxy
- Avoid: thousands of clients connecting directly

---

## Caching In Front Of DB

- Redis / Memcached
- Most-read data in RAM
- Reduces DB load drastically
- Cache invalidation: the hard part
- Often: 90%+ hit ratio possible

---

## Vertical vs Horizontal Scaling

- Vertical: bigger machine
- Horizontal: more machines
- Vertical: simpler, hits limits
- Horizontal: complex, scales further
- Most apps: vertical first; horizontal when needed

---

## ACID vs BASE

- **ACID**: Atomicity, Consistency, Isolation, Durability (SQL)
- **BASE**: Basically Available, Soft state, Eventually consistent (NoSQL)
- Different trade-offs
- Pick by requirements, not by hype

---

## Choosing A DB

- Transactional, complex queries: PostgreSQL / MySQL
- Schema-flexible, document: MongoDB / DynamoDB
- Time-series: TimescaleDB / InfluxDB
- Graph: Neo4j
- Search: Elasticsearch / OpenSearch
- Often: multiple, each for its strength

---

## Common DB Scaling Mistakes

- Sharding before needing it
- Index every column
- One database for everything
- No connection pooling
- Read-replica reads expecting strong consistency
