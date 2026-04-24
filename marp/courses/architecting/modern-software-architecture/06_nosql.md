---
tags:
  - concepts:nosql
  - concepts:distributed-systems
  - concepts:consistency
  - concepts:data-modeling
level: advanced
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# NoSQL Databases

---
## Why NoSQL Emerged

By the mid-2000s, the web outgrew the single-node RDBMS:

- **Scale** — social feeds, search indexes, and event streams produce more writes than one server can handle
- **Schema flexibility** — rapidly evolving products can't afford an `ALTER TABLE` on billions of rows
- **Impedance mismatch** — objects in code don't map cleanly to normalized tables
- **Geographic distribution** — users in multiple regions need nearby replicas
- **Operational simplicity** — auto-sharding and replication instead of DBAs

NoSQL is not one thing. It's four distinct families that each relax a different part of the relational contract in exchange for one of these properties.

---
## What NoSQL Gives Up

- **Joins across entities** — most NoSQL stores don't support them, or only within limits
- **ACID across multiple records** — usually per-document, not cross-document
- **Declarative queries over arbitrary fields** — you design for specific access patterns
- **Strong consistency by default** — often eventual, with stronger levels available by opt-in

In return you get horizontal scalability, flexible schemas, and models that fit specific problems better than rows and columns.

---
## CAP Recap

From chapter 2: during a network partition, a distributed system can guarantee either **Consistency** or **Availability**, not both.

- **CP** systems — refuse writes during partition to preserve correctness (HBase, MongoDB with majority writes)
- **AP** systems — stay available and reconcile later (Cassandra, DynamoDB, Riak)

Most real systems are tunable — you pick consistency level per operation, not per database.

---
## BASE vs ACID

![base_vs_acid](svg/courses/architecting/modern-software-architecture/06_nosql/base_vs_acid.svg)

---
## Consistency Is a Spectrum

"Eventually consistent" is a family, not a single guarantee. Applications care about which ordering promises hold.

---
## Consistency Models

![consistency_models](svg/courses/architecting/modern-software-architecture/06_nosql/consistency_models.svg)

---
## Picking a Consistency Level

- **Linearizable** — bank balance, inventory count. Slow across regions.
- **Causal** — messaging, collaborative documents. "Reply appears after message."
- **Read-your-writes** — user-facing writes where the user's next request must see it.
- **Monotonic** — analytics, feeds. The count shouldn't go down.
- **Eventual** — DNS, counters, recommendations. Freshness doesn't matter short-term.

Most NoSQL systems let you pick per query — the default is usually eventual.

---
## The Four Families

![four_families](svg/courses/architecting/modern-software-architecture/06_nosql/four_families.svg)

---
## Family 1: Key-Value Stores

The simplest NoSQL model: a dictionary that persists. The value is opaque to the database.

- Single-key operations: `GET`, `SET`, `DEL`, `INCR`
- No queries over the value — you know the key or you don't find it
- Extremely fast: hash lookup, no parsing, no planning
- Examples: **Redis, Memcached, DynamoDB (single-key mode), etcd**

Redis extends the model with typed values — lists, sets, sorted sets, streams — while keeping single-key semantics.

---
## Key-Value Example: Redis

```bash
# Session storage
SET session:abc123 '{"user_id":42,"expires":1714000000}' EX 3600

# Rate limiting
INCR ratelimit:user:42:minute
EXPIRE ratelimit:user:42:minute 60

# Leaderboard (sorted set)
ZADD scores 1500 "alice"
ZADD scores 1200 "bob"
ZREVRANGE scores 0 9 WITHSCORES   # top 10
```

All O(log N) or O(1) per operation. Millions of ops/sec on a single node.

---
## Family 2: Document Stores

Documents are self-describing — each is a JSON-like object with nested structure.

- Unit of storage: a document, not a row
- Schema is per-document, not per-collection
- Secondary indexes on fields within the document
- Transactions usually per-document (MongoDB added multi-document transactions in 4.0)
- Examples: **MongoDB, Couchbase, Firestore, DocumentDB**

The data model matches what most applications already serialize over the wire.

---
## Relational vs. Document

![relational_vs_document](svg/courses/architecting/modern-software-architecture/06_nosql/relational_vs_document.svg)

---
## Document Example: MongoDB

```javascript
// Insert with nested structure — no join table needed
db.users.insertOne({
  _id: 42,
  name: "Alice",
  email: "a@x.io",
  orders: [
    { id: 1, total: 50.00, items: [{ product: "book", qty: 1 }] },
    { id: 2, total: 30.00, items: [{ product: "pen",  qty: 5 }] }
  ]
})

// Query with dot notation into the nested array
db.users.find({ "orders.items.product": "book" })

// Atomic update on a nested field
db.users.updateOne(
  { _id: 42, "orders.id": 1 },
  { $inc: { "orders.$.total": 10.00 } }
)
```

The nested array lives inside the user document. One fetch returns everything.

---
## Document Trade-offs

**Pros**:
- No joins for aggregate reads
- Schema evolves per-document; no migrations
- Developer model matches application objects

**Cons**:
- Duplication if the same entity appears in many parents
- Document size limits (MongoDB: 16 MB)
- Cross-document transactions are expensive or unavailable
- Bad fit for many-to-many relationships

Rule of thumb: embed when the child is always fetched with the parent; reference when the child is shared or grows unbounded.

---
## Family 3: Column-Family (Wide-Column)

A sparse, two-dimensional map: `row_key → column_family → (column_name → value)`.

- Rows are keyed; columns *within* a row are sorted and can be sparse
- Each row can have millions of columns — columns are part of the data, not the schema
- Writes append to a log; reads merge layers (LSM-tree)
- Examples: **Cassandra, HBase, ScyllaDB, Bigtable**

The row is the unit of locality. Queries within one row are cheap; queries across rows usually require knowing the row key.

---
## Wide-Column Row Structure

![wide_column_row](svg/courses/architecting/modern-software-architecture/06_nosql/wide_column_row.svg)

---
## Wide-Column Example: Cassandra

```sql
CREATE TABLE events (
    user_id    uuid,
    event_time timestamp,
    event_type text,
    payload    text,
    PRIMARY KEY (user_id, event_time)
) WITH CLUSTERING ORDER BY (event_time DESC);

-- Insert (write is always fast — appends to commit log)
INSERT INTO events (user_id, event_time, event_type, payload)
VALUES (uuid(), now(), 'login', '{...}');

-- Query a specific user's recent events (uses partition key)
SELECT * FROM events
WHERE user_id = ? AND event_time > '2026-04-01'
LIMIT 100;
```

The partition key (`user_id`) determines which node stores the data. The clustering key (`event_time`) orders columns within the partition. You design the schema around the queries you need.

---
## Wide-Column Trade-offs

**Pros**:
- Massive write throughput (LSM-trees optimize for appends)
- Scales linearly with nodes (Cassandra)
- Time-series and event data fit naturally

**Cons**:
- Query patterns must be known upfront
- Ad-hoc queries require full scan or secondary indexes
- Eventual consistency by default; strong reads cost latency
- Compactions need tuning for write-heavy workloads

---
## Family 4: Graph Databases

Data is modeled as **nodes** (entities) and **edges** (typed, directed relationships).

- Both nodes and edges can have properties
- Queries traverse relationships, not tables
- A "friend of a friend" query is O(d^k) where d is degree and k is depth — not a join explosion
- Examples: **Neo4j, JanusGraph, Neptune, ArangoDB**

The shape of the data *is* the query plan.

---
## Graph Model

![graph_example](svg/courses/architecting/modern-software-architecture/06_nosql/graph_example.svg)

---
## Graph Example: Cypher (Neo4j)

```sql
// Create
CREATE (alice:User {name: "Alice"})
CREATE (bob:User   {name: "Bob"})
CREATE (book:Item  {name: "Book"})
CREATE (alice)-[:FOLLOWS]->(bob)
CREATE (bob)-[:BOUGHT]->(book)

// "Items bought by people Alice follows"
MATCH (a:User {name: "Alice"})-[:FOLLOWS]->(:User)-[:BOUGHT]->(i:Item)
RETURN DISTINCT i.name

// Shortest path
MATCH p = shortestPath((a:User {name:"Alice"})-[*..6]-(c:User {name:"Carol"}))
RETURN p
```

The same traversal in SQL would be a self-join per hop — at six hops, the planner gives up.

---
## Schema Flexibility — Pros and Pitfalls

**Pro**: add a field to new records without touching old ones. No `ALTER TABLE`.

**Pitfall**: your application now owns schema enforcement. Three classes of bug:

1. 1. 1. **Typos become fields** — `emial` silently stored; reads miss the user
1. 1. 1. **Type drift** — half the records have `age: 30`, half `age: "30"`
1. 1. 1. **Evolution tangles** — fields renamed over years; every read handles N variants

Mitigations: schema validation (MongoDB `$jsonSchema`, Couchbase enforces via app), versioned documents, regular cleanup jobs.

The flexibility is real. So is the cost.

---
## Indexing in NoSQL

The primary key index is free. Everything else is explicit.

- **Secondary indexes** — MongoDB, Cassandra, DynamoDB all support them, with caveats
- **Local vs. global** — local indexes live with the partition (cheap writes); global indexes are distributed (extra round trips)
- **Consistency** — secondary indexes may lag the primary data (eventually consistent)
- **Materialized views** — denormalized copies maintained by the database (Cassandra) or by the app

Design rule: if you haven't planned how a query is served, it probably requires a full scan.

---
## Sharding Strategies

![sharding_strategies](svg/courses/architecting/modern-software-architecture/06_nosql/sharding_strategies.svg)

---
## Replication Models

![replication_models](svg/courses/architecting/modern-software-architecture/06_nosql/replication_models.svg)

---
## Quorum: R + W > N

In leaderless replication, consistency is tunable per operation.

- **N** — total replicas for a key
- **W** — replicas that must acknowledge a write
- **R** — replicas consulted on a read

If `R + W > N`, at least one replica in the read set has the latest write → strong consistency.

Common settings (N = 3):
- **W = 1, R = 1** — fast, eventual consistency
- **W = 3, R = 1** — fast reads, slow writes
- **W = 2, R = 2** — balanced, strong reads
- **W = 3, R = 3** — both slow, survives no failures

Cassandra, DynamoDB, and Riak all expose these as tunable knobs.

---
## Transactions in NoSQL

**Per-document** is the common denominator. Most NoSQL systems guarantee atomicity of a single document/row update.

**Multi-document transactions** — supported, with restrictions:
- **MongoDB** — since 4.0, multi-document ACID transactions (slower, still per-replica-set)
- **DynamoDB** — `TransactWriteItems`, up to 100 items, same region
- **Cassandra** — lightweight transactions (`IF NOT EXISTS`) via Paxos, one partition
- **FaunaDB, Spanner** — full cross-shard distributed transactions (the exception, not the rule)

If you need cross-entity ACID, an RDBMS is probably still the right tool.

---
## Query Languages

NoSQL didn't abolish query languages — it fragmented them.

- **Redis** — command-based, no general query language
- **MongoDB** — JSON query documents, aggregation pipelines
- **Cassandra** — CQL, intentionally SQL-like but missing JOIN and GROUP BY across partitions
- **Neo4j** — Cypher, pattern-matching syntax
- **Couchbase** — N1QL, a SQL dialect over JSON
- **DynamoDB** — PartiQL (SQL) or native API with expressions

SQL-like surface syntax doesn't mean SQL semantics — CQL's `WHERE` rejects any clause the partition design can't satisfy.

---
## When to Pick Each Family

![when_to_pick_each](svg/courses/architecting/modern-software-architecture/06_nosql/when_to_pick_each.svg)

---
## Polyglot Persistence

Few real systems use a single database. A typical architecture might run:

- **PostgreSQL** — user accounts, orders, financial records (ACID-critical)
- **Redis** — session cache, rate limiter, leaderboards
- **Elasticsearch** — full-text search over product catalog
- **Cassandra** — event log, clickstream, time-series metrics
- **Neo4j** — social graph, recommendation engine
- **S3** — blobs, uploads, backups

Each store solves one problem well. The cost is operational complexity: backups, monitoring, and data-pipeline integration multiply per system.

---
## Common NoSQL Mistakes

- **"NoSQL means no schema"** — no, it means the schema is your app's job. Write validators.
- **Picking by hype** — MongoDB isn't universally right any more than PostgreSQL is universally wrong.
- **Treating Cassandra like PostgreSQL** — you can't add a WHERE clause and hope. Model by query first.
- **Ignoring consistency defaults** — eventual consistency surprises users. Audit every read path.
- **Skipping capacity planning** — NoSQL scales horizontally, but auto-sharding is not free.
- **One giant document** — MongoDB 16 MB limit; Cassandra wide rows can get unworkable; DynamoDB 400 KB item.

NoSQL databases are sharp tools. Sharp both ways.

---
## Chapter Takeaways

- NoSQL is four families, not one alternative — key-value, document, column-family, graph
- ACID traded for BASE — eventual consistency, horizontal scale, flexible schema
- Consistency models are a spectrum; most systems let you pick per operation
- Design for the access pattern — schema follows queries, not the other way around
- Quorum tuning (R+W > N) gives per-operation consistency in leaderless systems
- Cross-entity transactions remain the RDBMS's strong point
- Real systems are usually polyglot — match the store to the workload

An RDBMS is the right default. NoSQL is the right answer for specific, measured problems.
