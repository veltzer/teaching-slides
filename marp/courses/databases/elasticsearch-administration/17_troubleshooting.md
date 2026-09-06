---
tags:
  - databases:elasticsearch
level: intermediate
category: databases
audience:
  - audiences:dbas

---

# Troubleshooting

---

## What This Chapter Covers

- A symptom to diagnosis to fix workflow for common cluster issues
- Out of memory errors: heap pressure, circuit breakers, and GC
- Unassigned shards and the allocation explain API
- Cluster block exceptions from disk watermarks
- Performance degradation: hot threads and slow logs
- Data corruption and recovery procedures
- Collecting support diagnostics for escalation

---

## The Troubleshooting Mindset

- Always work the pattern: symptom, then diagnosis, then fix
- Start with cluster health before drilling into a single node

```bash
GET /_cluster/health
GET /_cat/nodes?v&h=name,heap.percent,ram.percent,cpu,load_1m,disk.used_percent
GET /_cat/indices?v&health=red
```

- `status` of `green`, `yellow`, or `red` frames the urgency
- `yellow` means replicas unassigned; `red` means a primary is missing
- Never restart nodes blindly; identify the cause first

---

## Reading Cluster Health

- `number_of_pending_tasks` rising indicates a backed-up master
- `unassigned_shards` greater than zero needs investigation

```bash
GET /_cluster/health?level=indices
GET /_cluster/pending_tasks
```

- `active_shards_percent_as_number` shows recovery progress
- Check the elected master with `GET /_cat/master?v`
- A flapping master points to network or GC problems

---

## Out of Memory: Heap Pressure

- Symptom: nodes slow, then drop out; logs show `OutOfMemoryError`
- Diagnosis: heap consistently above 85 percent triggers constant GC

```bash
GET /_nodes/stats/jvm?filter_path=**.jvm.mem.heap_used_percent
GET /_cat/nodes?v&h=name,heap.current,heap.max,heap.percent
```

- Fix: reduce shard count, lower aggregation cardinality, add nodes
- Keep heap at no more than 50 percent of RAM and under ~31 GB
- Leave the rest of RAM for the filesystem cache and off-heap data

---

## Circuit Breakers

- Symptom: requests rejected with `circuit_breaking_exception`
- Diagnosis: a breaker tripped to protect the node from OOM

```bash
GET /_nodes/stats/breaker
```

- The parent breaker defaults to 95 percent of heap
- Common culprits: `fielddata`, large `request` aggregations, `inflight_requests`
- Fix: smaller queries, fewer buckets, more nodes; do not just raise limits
- Raising a breaker limit only delays the eventual OOM

---

## Garbage Collection Problems

- Symptom: periodic stalls, node disconnects, master elections
- Diagnosis: long GC pauses logged as `[gc][young]` or `[gc][old]`

```bash
GET /_nodes/stats/jvm?filter_path=**.gc
```

- Look for `collection_time_in_millis` growing rapidly
- Long old-GC pauses usually mean heap is too small for the workload
- Fix: reduce memory demand or scale out; avoid huge heaps that pause longer

---

## Unassigned Shards: Diagnosis

- Symptom: cluster `yellow` or `red`, shards stuck unassigned
- Diagnosis: ask the cluster exactly why

```bash
GET /_cluster/allocation/explain
{ "index": "logs-2026.06.14", "shard": 0, "primary": true }
```

- `_cat/shards` lists every shard and its `UNASSIGNED` reason

```bash
GET /_cat/shards?v&h=index,shard,prirep,state,node,unassigned.reason
```

- The explain output names the deciders that blocked allocation

---

## Unassigned Shards: Common Causes

- `NODE_LEFT`: the node holding the shard is gone
- `ALLOCATION_FAILED`: repeated failures, retry limit reached
- `INDEX_CREATED`: brand new index still being allocated
- `CLUSTER_RECOVERED`: full restart in progress

```bash
POST /_cluster/reroute?retry_failed=true
```

- Disk watermarks or awareness rules can also forbid allocation
- Fix only after the explain output tells you which decider said no

---

## Disk Watermarks

- Three thresholds govern shard placement based on free disk
- `cluster.routing.allocation.disk.watermark.low` (default 85 percent)
- `cluster.routing.allocation.disk.watermark.high` (default 90 percent)
- `cluster.routing.allocation.disk.watermark.flood_stage` (default 95 percent)
- Low: stop allocating new shards to this node
- High: relocate shards away from this node
- Flood stage: enforce a read-only block on affected indices

---

## Cluster Block: read_only_allow_delete

- Symptom: writes fail with `cluster_block_exception` and `read_only_allow_delete`
- Diagnosis: flood stage watermark was crossed on a node

```bash
GET /_cat/allocation?v&h=node,disk.used_percent,disk.avail
```

- Fix step one: free disk by deleting old indices or adding capacity
- Fix step two: clear the auto-applied block once disk is healthy

```bash
PUT /_all/_settings
{ "index.blocks.read_only_allow_delete": null }
```

- The block does not clear by itself; you must reset it after recovery

---

## Performance Degradation: Hot Threads

- Symptom: high CPU, slow responses, but no errors
- Diagnosis: see what threads are actually burning CPU right now

```bash
GET /_nodes/hot_threads?threads=5&interval=500ms
```

- Output shows stack traces of the busiest threads per node
- Repeated `search` or `merge` frames point to the bottleneck
- Fix: tune queries, throttle merges, or scale the hot tier
- Run it twice a few seconds apart to confirm a sustained pattern

---

## Performance Degradation: Slow Logs

- Slow logs capture queries and indexing that exceed thresholds
- Configure per index with tiered warn, info, debug levels

```bash
PUT /myindex/_settings
{
  "index.search.slowlog.threshold.query.warn": "5s",
  "index.search.slowlog.threshold.fetch.warn": "1s",
  "index.indexing.slowlog.threshold.index.warn": "10s"
}
```

- Logs land in the node `*_index_search_slowlog` files
- Use them to find the specific slow query shapes, not just symptoms

---

## Data Corruption

- Symptom: shard fails to start; logs show `CorruptIndexException`
- Diagnosis: usually bad disk, abrupt power loss, or filesystem issues

```bash
GET /_cat/shards?v&h=index,shard,prirep,state,unassigned.reason
```

- First choice: recover from a healthy replica or a snapshot
- Confirm a good replica exists before touching the primary
- Replacing the disk and re-replicating is safer than forcing a corrupt shard

---

## Recovery Procedures

- Prefer restoring from snapshots over salvaging corrupt data
- `POST /_snapshot/repo/snap/_restore` recovers known-good state
- Monitor ongoing recovery to estimate completion

```bash
GET /_cat/recovery?v&active_only=true
```

- As a last resort only, `allocate_empty_primary` accepts data loss

```bash
POST /_cluster/reroute
{ "commands": [ { "allocate_empty_primary":
  { "index": "idx", "shard": 0, "node": "node-1", "accept_data_loss": true } } ] }
```

- Treat `accept_data_loss` as deliberate, documented data loss

---

## Support Diagnostics

- For escalation, capture a full point-in-time snapshot of the cluster
- The Elasticsearch support diagnostics tool bundles logs, stats, and config

```bash
./diagnostics.sh --host localhost:9200 --type local
```

- It collects `_cluster/state`, `_nodes/stats`, hot threads, and node logs
- Run it from a node so it can also gather local logs and the GC log
- Attach the resulting archive to the support case
- Redact sensitive data before sharing externally

---

## Troubleshooting Checklist

- Check cluster health and identify `red` or `yellow` first
- For OOM, look at heap percent, breakers, and GC together
- For unassigned shards, always run allocation explain
- For write failures, suspect disk watermarks and read-only blocks
- For slowness, combine hot threads with slow logs
- Recover from snapshots or replicas before forcing risky allocations
- Capture diagnostics early when escalating to support
