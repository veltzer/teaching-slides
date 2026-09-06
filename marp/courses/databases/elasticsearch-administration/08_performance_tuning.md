---
tags:
  - databases:elasticsearch
level: intermediate
category: databases
audience:
  - audiences:dbas

---

# Performance Tuning

---

## What This Chapter Covers

- Hardware considerations: storage, RAM, filesystem cache, CPU
- Index optimization strategies for fast bulk loads
- Query optimization techniques
- Cache management: query cache, request cache, fielddata
- Thread pool tuning
- Circuit breakers
- Slow log analysis
- Hot-warm-cold tiered architecture

---

## Hardware: Storage

- Use local SSDs (NVMe preferred) for hot indexing and search workloads
- Avoid network-attached storage for hot data; latency dominates search time
- Spinning disks are acceptable only for cold, rarely-queried tiers
- RAID 0 or JBOD with multiple data paths spreads I/O across devices
- DBA rule: storage latency is usually the first bottleneck under search load

---

## Hardware: RAM and Filesystem Cache

- Split RAM between the JVM heap and the OS filesystem cache
- Set heap to at most 50% of RAM, and keep it under ~31 GB to retain compressed pointers

```bash
# jvm.options
-Xms31g
-Xmx31g
```

- Always set `Xms` equal to `Xmx` to avoid heap resize pauses
- The other ~50% of RAM feeds the OS page cache, which holds hot Lucene segments
- Lucene relies on the filesystem cache, so leaving RAM free is not waste

---

## Hardware: CPU

- More cores help concurrent search and aggregation throughput
- CPU usually matters most for complex aggregations and analyzed-text indexing
- Pin thread pool sizes to the processor count rather than oversubscribing
- Disable swap entirely (`bootstrap.memory_lock: true`) to avoid GC-killing page-outs

```yaml
# elasticsearch.yml
bootstrap.memory_lock: true
```

---

## Index Optimization for Bulk Load

- Use the `_bulk` API and parallel client threads to saturate ingest
- Disable or raise the refresh interval while loading

```bash
PUT /bulk-target/_settings
{ "index": {
    "refresh_interval": "-1",
    "number_of_replicas": 0
} }
```

- Set replicas to 0 during load, then restore — replicas double indexing work
- After the load, force a refresh and restore both settings

```bash
PUT /bulk-target/_settings
{ "index": { "refresh_interval": "1s", "number_of_replicas": 1 } }
```

---

## More Index-Time Tuning

- Let Elasticsearch auto-generate IDs when possible; explicit IDs force an existence check
- Avoid unnecessary fields; disable `_source` only if you never need reindex or update
- Use `index: false` on fields you never query, and `doc_values: false` on fields you never sort or aggregate
- Match analyzers to need; heavy custom analysis raises indexing CPU cost
- Increase `index.translog.flush_threshold_size` for very heavy ingest bursts

---

## Query Optimization

- Prefer filter context for non-scoring conditions to enable caching
- Return only needed fields with `_source` filtering; avoid fetching large documents
- Round date ranges (`now-1h/h`) so filters stay cacheable
- Avoid leading wildcards, regex, and scripted scoring on hot paths
- Use `search_after` with PIT instead of deep `from + size` pagination
- Pre-aggregate or use rollups for repetitive dashboard queries over old data

---

## Node Query Cache

- Caches results of filter-context clauses per segment
- Sized by `indices.queries.cache.size`, default 10% of heap

```bash
PUT /_cluster/settings
{ "persistent": { "indices.queries.cache.size": "15%" } }
```

- Effective for repeated, stable filters across many requests
- Inspect hit ratio to judge whether it is helping

```bash
GET /_nodes/stats/indices/query_cache?human
```

---

## Shard Request Cache

- Caches the full response of search requests where `size: 0` (aggregations only)
- Enabled by default; keyed on the whole request body per shard
- Ideal for dashboards that re-run identical aggregations over stable indices

```bash
PUT /metrics/_settings
{ "index.requests.cache.enable": true }

GET /metrics/_search?request_cache=true
{ "size": 0, "aggs": { "avg_v": { "avg": { "field": "v" } } } }
```

- The cache is invalidated on refresh, so it favors read-mostly indices

---

## Fielddata Cache

- `fielddata` is the in-memory store for sorting and aggregating on `text` fields
- It is off by default because it can consume large amounts of heap
- Aggregate and sort on `keyword` fields, which use on-disk `doc_values` instead
- If fielddata is unavoidable, bound it to protect the node

```bash
PUT /_cluster/settings
{ "persistent": { "indices.fielddata.cache.size": "20%" } }
```

- DBA rule: uncontrolled fielddata is a leading cause of heap exhaustion

---

## Thread Pool Tuning

- Elasticsearch maintains separate thread pools for `search`, `write`, and others
- Each pool has a fixed size and a bounded queue; defaults derive from CPU count
- A full queue returns 429 `es_rejected_execution` — a signal to back off, not to grow queues blindly

```bash
GET /_cat/thread_pool/search,write?v&h=node_name,name,active,queue,rejected
```

- Persistent `write` rejections usually mean ingest is too aggressive or shards too many
- Persistent `search` rejections usually mean too many concurrent or too-broad queries
- Prefer fixing the workload over inflating pool sizes

---

## Circuit Breakers

- Circuit breakers abort operations that would exceed memory limits, preventing OOM
- The parent breaker caps total memory across all child breakers

```bash
GET /_nodes/stats/breakers?human
```

- `indices.breaker.total.limit` — parent breaker, default ~95% of heap
- `indices.breaker.fielddata.limit` — caps fielddata memory
- `indices.breaker.request.limit` — caps per-request data structures (aggs)
- A tripped breaker raises `circuit_breaking_exception` — investigate the query, do not just raise the limit

---

## Index Slow Log

- Logs indexing operations slower than configured thresholds, per shard

```bash
PUT /products/_settings
{ "index": {
    "indexing.slowlog.threshold.index.warn": "1s",
    "indexing.slowlog.threshold.index.info": "500ms"
} }
```

- Thresholds let you separate warn, info, debug, and trace severities
- Use it to find pathological documents or overly heavy analysis chains

---

## Search Slow Log

- Logs queries slower than thresholds, separately for the query and fetch phases

```bash
PUT /products/_settings
{ "index": {
    "search.slowlog.threshold.query.warn": "2s",
    "search.slowlog.threshold.query.info": "1s",
    "search.slowlog.threshold.fetch.warn": "1s"
} }
```

- Slow query phase points to expensive matching or aggregations
- Slow fetch phase points to large `_source` documents or many hits
- Feed slow log output into `_profile` to find the offending clauses

---

## Hot-Warm-Cold Architecture

- Tier nodes by hardware and assign indices by age and access frequency
- Hot: newest, actively indexed and queried — fast SSD, more CPU and RAM
- Warm: older, read-only, queried occasionally — denser, cheaper storage
- Cold: rarely queried, often searchable snapshots — cheapest storage
- Nodes carry data tier roles; ILM moves indices between tiers automatically

```bash
PUT /_cluster/settings
{ "persistent": {
    "cluster.routing.allocation.exclude._tier_preference": null } }
```

---

## Index Lifecycle Management

- ILM automates rollover, tier migration, force-merge, shrink, and deletion
- A policy defines phases (hot, warm, cold, delete) and the actions in each

```bash
PUT /_ilm/policy/logs-policy
{ "policy": { "phases": {
    "hot":    { "actions": { "rollover": { "max_primary_shard_size": "50gb" } } },
    "warm":   { "min_age": "7d",  "actions": { "forcemerge": { "max_num_segments": 1 } } },
    "cold":   { "min_age": "30d", "actions": { "freeze": {} } },
    "delete": { "min_age": "90d", "actions": { "delete": {} } }
} } }
```

- Rollover by size keeps shards near the 50 GB target automatically

---

## Operational Summary

- Leave half of RAM for the filesystem cache; cap heap near 31 GB and lock memory
- Disable refresh and replicas during bulk loads, restore them after
- Push non-scoring conditions into filter context and trim `_source`
- Aggregate on keyword/doc_values; treat fielddata as a last resort
- Treat 429s and tripped breakers as workload signals, not limits to raise
- Use slow logs plus `_profile` to find offenders, and ILM tiering to control cost
