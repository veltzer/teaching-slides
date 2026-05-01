---
tags:
  - databases:neo4j
level: intermediate
category: databases
audience:
  - audiences:developers
  - audiences:dba

---
# Performance

---
## What This Chapter Covers

- Index usage
- Query plans
- Hot paths
- Heap and page cache
- Transaction sizing

---
## Index Use

- EXPLAIN shows index hits
- Without index, full label scan
- Watch for missing indexes
- Use where you filter most

---
## Query Plans

- EXPLAIN: plan only
- PROFILE: actual rows and DB hits
- Look for high DB hits
- Match expansion order matters

---
## Match Expansion

- Start at most selective node
- Expand outward
- Hint with start node when needed
- Cardinality stats drive plan

---
## Variable Length Paths

- Bound depth
- Use the shortest-path function where possible
- Watch combinatorial explosion
- Filter early

---
## Cartesian Products

- Two unrelated patterns in same MATCH
- Cross-product of rows
- Almost always a bug
- Engine warns when detected

---
## Heap And Page Cache

- Heap for queries and transactions
- Page cache for graph data
- Rule of thumb: page cache big as graph
- Heap moderate, GC tuned

---
## GC Tuning

- G1 default
- Long pauses hurt throughput
- Profile under load
- Adjust heap size with care

---
## Transaction Size

- Smaller transactions commit faster
- Big batches stress memory
- Batch in 1k to 10k operations
- Use procedure libraries for huge writes

---
## Read Concurrency

- Multiple readers fine
- Transactions are single-threaded
- More cores help concurrent queries
- Watch for cache contention

---
## Hot Spot Nodes

- Super-nodes with many edges
- Slow expansions
- Use relationship type filter
- Or model differently

---
## Caching

- OS page cache helps
- Query result cache for repeated reads
- Application caches when appropriate
- Beware staleness

---
## Bulk Imports

- neo4j-admin import for greenfield
- Order of magnitude faster than Cypher
- Plan format upfront
- Skip for incremental

---
## Common Performance Mistakes

- No index on key properties
- Unbounded variable-length paths
- Cartesian products
- Over-allocated heap
- Many tiny transactions
