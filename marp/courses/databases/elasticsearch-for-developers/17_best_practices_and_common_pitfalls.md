---
tags:
  - databases:elasticsearch
  - practices:best-practices
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Best Practices and Common Pitfalls

---
## What This Chapter Covers

- Mapping pitfalls
- Query pitfalls
- Operational pitfalls
- Anti-patterns
- A checklist

---
## Common Pitfalls

![pitfalls](svg/courses/databases/elasticsearch-for-developers/17_best_practices_and_common_pitfalls/pitfalls.svg)

---
## Mapping Pitfalls

- Letting auto-mapping run uncritically
- Dynamic mapping with bad field types
- Same field name, different types in different indexes
- Reindex headaches later

---
## Best: Explicit Mappings

- Define every field
- Pick: text vs keyword vs numeric
- Multi-fields where needed
- Strict dynamic mapping for new fields

---
## Query Pitfalls

- Term query on text fields
- Match query on keyword fields (analysed)
- Wildcards with leading `*`
- Deep `from` paging

---
## Best: Match Type To Query

- Exact: term on keyword
- Full-text: match on text
- Range: range on numeric / date
- Geo: geo_distance / geo_bounding_box

---
## Bulk Pitfalls

- Bulk too large (memory)
- Bulk too small (overhead)
- No retries on rejection
- Synchronous bulk in hot path

---
## Best: Bulk Operations

- 5-15MB per request
- Async pipeline (queue + worker)
- Retry on rejection
- Disable refresh during big loads

---
## Operational Pitfalls

- One node clusters in production
- No backups (or untested)
- No ILM; index keeps growing
- Stack monitoring not configured

---
## Best: Operations

- 3+ master-eligible nodes
- Dedicated master nodes for big clusters
- Snapshots tested
- ILM for time-based data

---
## Capacity Pitfalls

- Working set exceeds RAM (cold queries)
- Heap too large (>30GB causes GC issues)
- Disk fills (no ILM)
- Hot shards (uneven write distribution)

---
## Best: Capacity

- Heap = 50% of RAM, max 30GB
- Disk: leave 20% headroom
- Watch shard count growth
- Plan capacity quarterly

---
## Anti-Pattern: ES As Database

- No transactions
- Hard to back up
- Schema migration pain
- Use a real DB; ES for search

---
## Anti-Pattern: Too Many Shards

- Each shard has fixed cost
- Too many: can't open new index
- Aim: 1 shard per 10-50GB of data
- Reduce by reindexing if too many

---
## Anti-Pattern: Sync Search In Hot Path

- ES query latency: 10-100ms typical
- Blocks request thread
- Use async client; or cache results
- Not a database; not for every request

---
## A Checklist

- [ ] Explicit mappings defined
- [ ] Multi-fields where needed
- [ ] Filter context for non-scoring conditions
- [ ] Bulk operations for ingestion
- [ ] Async pipeline for high-throughput
- [ ] ILM for time-based indexes
- [ ] Snapshots configured and tested
- [ ] Stack monitoring on
- [ ] Slow logs enabled
- [ ] Alerts on cluster health

---
## Course Wrap-Up

- Elasticsearch: powerful search and analytics
- Mappings matter; define explicitly
- Filter context for non-scoring criteria
- Bulk operations for any ingestion
- Vector and hybrid search are the modern frontier
- Operations is half the job; plan for it
