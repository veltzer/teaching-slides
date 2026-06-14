---
tags:
  - databases:elasticsearch
level: intermediate
category: databases
audience:
  - audiences:dbas

---

# Monitoring and Diagnostics

---

## What This Chapter Covers

- Cluster health and statistics APIs for at-a-glance state
- Node and index stats, plus the human-friendly `_cat` APIs
- Stack Monitoring and Metricbeat-based metrics collection
- Elastic APM for application-level observability
- Watcher for automated alerting on cluster conditions
- Diagnostic tools: support diagnostics and hot threads
- A practical performance troubleshooting workflow

---

## Cluster Health: The First Look

- `GET _cluster/health` returns the overall cluster status
- Status is one of three colors:
    - `green` — all primary and replica shards allocated
    - `yellow` — all primaries allocated, some replicas missing
    - `red` — at least one primary shard is unallocated
- Yellow is normal on a single node (replicas cannot place)
- Red means data is unavailable — investigate immediately

```bash
GET _cluster/health
GET _cluster/health/my-index?level=shards
```

---

## Interpreting Cluster Health Fields

- `number_of_nodes` / `number_of_data_nodes` — current membership
- `active_shards` and `active_primary_shards` — what is online
- `unassigned_shards` — shards with no home (drives yellow/red)
- `initializing_shards` / `relocating_shards` — work in progress
- `number_of_pending_tasks` — master queue backlog (watch for spikes)
- `active_shards_percent_as_number` — quick overall progress gauge

```bash
GET _cluster/health?wait_for_status=green&timeout=30s
```

---

## Why Are Shards Unassigned?

- The allocation explain API gives the precise reason
- Common causes: disk watermark, node left, allocation filtering
- Returns a human-readable decision per allocation decider

```bash
GET _cluster/allocation/explain
{
  "index": "my-index",
  "shard": 0,
  "primary": true
}
```

---

## Cluster Statistics

- `GET _cluster/stats` aggregates the whole cluster in one call
- Indices section: doc count, store size, field/mapping totals
- Nodes section: OS, JVM, file system, process counts
- Useful for capacity planning and trend snapshots
- Heavier than `_cluster/health` — do not poll at high frequency

```bash
GET _cluster/stats?human
```

---

## Node Statistics

- `GET _nodes/stats` exposes deep per-node metrics
- Filter to the parts you need to keep responses small
- Key sections: `jvm` (heap, GC), `os`, `fs`, `thread_pool`
- `indices` section shows indexing, search, merge, refresh stats
- `breakers` reveals circuit breaker trips (memory pressure)

```bash
GET _nodes/stats/jvm,os,thread_pool
GET _nodes/stats/indices/search,indexing?human
```

---

## The `_cat` APIs: Human-Readable Ops

- Compact tabular output, ideal for terminals and scripts
- Add `?v` for a header row, `?help` to list all columns
- Add `&s=column` to sort, `&format=json` for machine parsing

```bash
GET _cat/health?v
GET _cat/nodes?v
GET _cat/indices?v&s=store.size:desc
```

---

## `_cat/nodes` and `_cat/allocation`

- `_cat/nodes` shows heap, RAM, CPU, load, and node roles
- The `master` column marks the elected master with `*`
- `_cat/allocation` shows disk usage and shard count per node
- Use these to spot hot nodes and disk imbalance fast

```bash
GET _cat/nodes?v&h=name,heap.percent,ram.percent,cpu,load_1m,node.role,master
GET _cat/allocation?v&s=disk.percent:desc
```

---

## `_cat/indices` and `_cat/shards`

- `_cat/indices` lists health, status, docs, and store per index
- Look for `red`/`yellow` rows and oversized indices
- `_cat/shards` shows every shard, its state, and its node
- Filter `_cat/shards` to find `UNASSIGNED` shards quickly

```bash
GET _cat/indices?v&health=red
GET _cat/shards?v&s=state
GET _cat/shards/my-index?v&h=index,shard,prirep,state,node,unassigned.reason
```

---

## Other Useful `_cat` Endpoints

- `_cat/thread_pool` — queue and rejection counts per pool
- `_cat/pending_tasks` — master tasks awaiting execution
- `_cat/recovery` — shard recovery progress and throughput
- `_cat/segments` — segment counts (merge pressure indicator)

```bash
GET _cat/thread_pool/write,search?v&h=node_name,name,active,queue,rejected
GET _cat/recovery?v&active_only=true
```

---

## Stack Monitoring

- Collects time-series metrics into a dedicated monitoring cluster
- Best practice: ship metrics to a separate monitoring cluster
- Avoids the monitored cluster's problems hiding its own metrics
- Powers Kibana's Stack Monitoring UI: nodes, indices, shards
- Two collection paths: legacy internal collection or Metricbeat
- Metricbeat collection is the recommended, decoupled approach

---

## Metricbeat Integration

- Metricbeat's `elasticsearch-xpack` module scrapes the APIs
- Runs alongside (or external to) each node, pulling stats
- Decouples collection from the cluster being monitored
- Ships to the monitoring cluster over the HTTP interface

```yaml
metricbeat.modules:
  - module: elasticsearch
    xpack.enabled: true
    period: 10s
    hosts: ["https://localhost:9200"]
    username: "remote_monitoring_user"
    password: "${ES_PWD}"
```

---

## Elastic APM

- Captures application-level traces, errors, and metrics
- APM agents instrument app code; data flows to the APM Server
- APM Server indexes traces into Elasticsearch for Kibana APM UI
- Correlates slow application transactions with ES query latency
- Distributed tracing links app spans to backend service calls
- Complements infrastructure metrics with request-level detail

---

## Watcher and Alerting

- Watcher runs scheduled queries and triggers actions on conditions
- A watch has: `trigger`, `input`, `condition`, and `actions`
- Inputs can be a search, an HTTP call, or chained inputs
- Actions: email, Slack, webhook, index, PagerDuty
- Kibana Alerting offers a rule-based UI alternative

```bash
PUT _watcher/watch/cluster_red
{
  "trigger": { "schedule": { "interval": "1m" } },
  "input": { "http": { "request": {
    "host": "localhost", "port": 9200, "path": "/_cluster/health"
  } } },
  "condition": { "compare": { "ctx.payload.status": { "eq": "red" } } },
  "actions": { "notify": { "webhook": { "host": "alertmgr",
    "port": 9000, "method": "post", "path": "/alert" } } }
}
```

---

## Support Diagnostics

- The `support-diagnostics` tool gathers a full cluster snapshot
- Bundles `_cluster`, `_nodes`, `_cat`, settings, and logs
- Produces a single archive to share with support or to analyze
- Run from a host with API access to the cluster

```bash
./diagnostics.sh --host localhost --port 9200 \
  --type local -u elastic --ssl
```

---

## Hot Threads

- `GET _nodes/hot_threads` samples the busiest threads per node
- Reveals what the CPU is actually spending time on
- Essential when a node shows high CPU or slow responses
- Output shows stack traces and the percentage of time consumed

```bash
GET _nodes/hot_threads
GET _nodes/hot_threads?threads=5&interval=500ms&type=cpu
```

---

## Performance Troubleshooting Workflow

- Start broad with `_cluster/health` and `_cat/nodes`
- Confirm no disk watermark via `_cat/allocation`
- Check JVM heap and GC pressure in `_nodes/stats/jvm`
- Inspect `_cat/thread_pool` for queue buildup and rejections
- Use `_nodes/hot_threads` to find the CPU culprit
- Review slow logs for expensive queries and indexing

```bash
PUT my-index/_settings
{ "index.search.slowlog.threshold.query.warn": "5s" }
```

---

## Key Metrics to Watch Continuously

- JVM heap usage — sustained > 75% signals memory pressure
- GC pause frequency and duration — long pauses stall the node
- Disk usage versus the low/high/flood watermarks
- Thread pool rejections — capacity or query inefficiency
- Indexing and search latency trends over time
- Pending tasks and unassigned shards as red flags

---

## Chapter Summary

- `_cluster/health` and `_cluster/stats` give the big picture
- `_nodes/stats` and `_cat` APIs drill into nodes and shards
- Stack Monitoring with Metricbeat is the recommended pipeline
- Elastic APM adds application-level tracing and correlation
- Watcher and Kibana Alerting automate condition-based alerts
- Support diagnostics and hot threads pinpoint hard problems
