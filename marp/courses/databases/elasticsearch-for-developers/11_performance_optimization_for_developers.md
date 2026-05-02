---
tags:
  - databases:elasticsearch
  - databases:performance
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Performance Optimisation for Developers

---
## What This Chapter Covers

- Query profiling
- Filter context
- doc_values
- Caching
- Index settings
- Common slow queries

---
## Performance Levers

![perf_levers](svg/courses/databases/elasticsearch-for-developers/11_performance_optimization_for_developers/perf_levers.svg)

---
## Profile API

```json
{
  "profile": true,
  "query": {...}
}
```

- Returns timing per Lucene operation
- Shows where time goes
- Use sparingly (overhead)

---
## Filter Context

- Filters cached
- Use for: yes/no checks
- Don't score
- Wrap in `bool.filter`

---
## doc_values

- Column-store for aggregations and sorting
- Default on for most fields
- Off saves space; can't aggregate on
- Set `doc_values: false` only when sure

---
## Source Field

- _source: original document
- Saved by default
- Can disable to save space; can't reindex from ES then
- Most: keep enabled

---
## Caching

- Filter cache
- Query cache (per-segment)
- Field data / doc_values cache
- Disk cache (OS)
- Many layers

---
## Force Merge

- Merge segments in an index
- For time-series (older indexes): merge to 1 segment
- Faster queries; less memory
- Don't on actively-written indexes

---
## Pagination Performance

- `from + size > 10000`: error by default
- Use `search_after`
- Or scroll for batch processing

---
## Aggregation Performance

- Aggregations on huge indexes: slow
- Filter first
- Sample (use sampler aggregation)
- Pre-aggregate at index time

---
## Multi-Index Searches

- Search many indexes at once
- Pattern: `logs-*`
- Cross-cluster search for federated

---
## Mappings For Speed

- `keyword` not `text` if exact match
- Disable `_all` (gone in 8+)
- Don't index unused fields
- Match field to query pattern

---
## Refresh Interval

- Default: 1s
- Higher for bulk loading: 30s or -1
- After load: re-enable
- Saves segment churn

---
## Number Of Shards

- Each shard is overhead
- Too few: can't scale write
- Too many: small queries hit many shards
- Rule of thumb: 1 shard per 10-50GB data

---
## Number Of Replicas

- 1 for production (HA)
- 0 during big bulk loads (then restore to 1)
- More replicas = more read scaling

---
## Common Performance Mistakes

- Wildcard query on text field (slow)
- Heavy aggregations without filter
- Sorting on text field without keyword sub-field
- Too many tiny shards
- Refresh interval default during bulk loads
