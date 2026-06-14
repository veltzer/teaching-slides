---
tags:
  - databases:elasticsearch
level: intermediate
category: databases
audience:
  - audiences:dbas

---

# Index Lifecycle Management

---

## What This Chapter Covers

- ILM policies and the hot, warm, cold, frozen, and delete phases
- Data tiers and the node roles that back each tier
- Data streams and rollover driven by ILM
- Automated index management and retention policies
- The snapshot and delete phase actions
- Wiring policies through index templates
- Inspecting policy progress with the `_ilm` APIs

---

## Why ILM Exists

- Time-series data (logs, metrics) grows without bound
- Different ages of data have different cost/performance needs
- ILM automates moving and removing data as it ages
- It rolls over, shrinks, force-merges, freezes, and deletes
- Replaces fragile cron jobs with cluster-managed automation

---

## The Lifecycle Phases

- `hot` — actively written and queried; fastest hardware
- `warm` — no longer written, still queried occasionally
- `cold` — rarely queried; optimized for storage cost
- `frozen` — searchable snapshots, minimal local storage
- `delete` — removed at end of retention
- A policy can skip phases; only `hot` and `delete` are common minimums

---

## Data Tiers and Node Roles

- Each phase targets a matching data tier via node roles
- Node roles: `data_hot`, `data_warm`, `data_cold`, `data_frozen`
- ILM allocates shards to nodes carrying the phase's role
- A small cluster may use generic `data` nodes for all tiers
- The frozen tier relies on searchable snapshots, not full copies

```bash
GET _cat/nodes?v&h=name,node.role
```

---

## A Hot-Warm-Cold-Delete Policy

- Each phase has a `min_age` measured from rollover
- Actions within a phase run when the phase is entered

```bash
PUT _ilm/policy/logs-policy
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": { "max_primary_shard_size": "50gb", "max_age": "1d" }
        }
      },
      "warm": {
        "min_age": "7d",
        "actions": { "forcemerge": { "max_num_segments": 1 },
          "shrink": { "number_of_shards": 1 } }
      },
      "cold": { "min_age": "30d", "actions": {
        "searchable_snapshot": { "snapshot_repository": "my_repo" } } },
      "delete": { "min_age": "90d", "actions": { "delete": {} } }
    }
  }
}
```

---

## Rollover Explained

- Rollover creates a fresh write index when limits are hit
- Triggers: `max_age`, `max_primary_shard_size`, `max_docs`
- Keeps individual indices a manageable, queryable size
- The alias or data stream always points reads/writes correctly
- Aim for primary shards in the tens-of-GB range

```bash
POST logs-write/_rollover
{ "conditions": { "max_primary_shard_size": "50gb", "max_age": "1d" } }
```

---

## Data Streams

- A data stream is an abstraction over many backing indices
- Append-only: you index into the stream, ES manages backing indices
- Each rollover creates a new hidden backing index
- The stream name is what apps write to and query
- Backing indices follow the naming `.ds-<stream>-<date>-<gen>`

```bash
PUT _data_stream/logs-app
GET _data_stream/logs-app
```

---

## Data Streams Plus ILM

- Data streams require an index template with ILM settings
- ILM rolls over the stream's write index automatically
- No manual alias management — the stream handles it
- This is the recommended pattern for time-series data

```bash
GET _data_stream/logs-app/_stats
```

---

## Wiring a Policy via an Index Template

- ILM is attached through the template, not per index
- Set `index.lifecycle.name` to the policy
- For data streams, define `data_stream` in the template
- New indices/streams matching the pattern inherit the policy

```bash
PUT _index_template/logs-template
{
  "index_patterns": ["logs-app*"],
  "data_stream": {},
  "template": {
    "settings": {
      "index.lifecycle.name": "logs-policy",
      "number_of_shards": 1,
      "number_of_replicas": 1
    }
  }
}
```

---

## Applying ILM to a Plain Index

- For non-stream indices, use a rollover alias
- Set both the policy name and the rollover alias in settings
- The bootstrap index must be marked as the write index

```bash
PUT logs-000001
{
  "aliases": { "logs-write": { "is_write_index": true } },
  "settings": {
    "index.lifecycle.name": "logs-policy",
    "index.lifecycle.rollover_alias": "logs-write"
  }
}
```

---

## Common Phase Actions

- `rollover` — start a new write index (hot phase)
- `forcemerge` — reduce segments to speed up reads (warm)
- `shrink` — reduce primary shard count (warm/cold)
- `allocate` — change replicas or steer allocation
- `searchable_snapshot` — mount from a repo (cold/frozen)
- `readonly` and `delete` — freeze writes, then remove

---

## Retention Policies

- Retention is expressed as the `delete` phase `min_age`
- `min_age` counts from rollover, not from index creation
- Combine with the `wait_for_snapshot` action to keep a backup
- Align retention with compliance and storage budgets
- For data streams, ILM deletes old backing indices automatically

---

## Snapshot and Delete Phase Actions

- `searchable_snapshot` snapshots then mounts the index read-only
- It frees local primary storage while keeping data queryable
- `wait_for_snapshot` in delete phase ensures an SLM snapshot exists
- This prevents deleting data that was never backed up

```bash
"delete": {
  "min_age": "90d",
  "actions": {
    "wait_for_snapshot": { "policy": "nightly-snapshots" },
    "delete": {}
  }
}
```

---

## Managing and Inspecting Policies

- `_ilm/explain` shows each index's phase, step, and any error
- Use it first when an index is stuck or not progressing
- Start, stop, and retry ILM at the cluster level

```bash
GET logs-app*/_ilm/explain
GET _ilm/policy/logs-policy
POST logs-000005/_ilm/retry
```

---

## Operating ILM

- ILM runs a periodic check (`indices.lifecycle.poll_interval`)
- A stuck step usually means a missing repo, role, or capacity
- `_ilm/explain` exposes `step_info` with the failure reason
- Pause ILM during maintenance with `_ilm/stop`, resume with `_ilm/start`

```bash
GET _ilm/status
POST _ilm/stop
POST _ilm/start
```

---

## ILM Best Practices

- Drive rollover by primary shard size, not just age
- Keep shards in the tens of GB; avoid tiny or huge shards
- Use data streams for new time-series workloads
- Force-merge only in warm/cold, never on a writing index
- Always pair long retention with a tested snapshot strategy
- Monitor `_ilm/explain` and alert on errored indices

---

## Chapter Summary

- ILM automates the hot, warm, cold, frozen, and delete phases
- Phases map to data tiers backed by specific node roles
- Rollover keeps shards sized right; data streams manage backing indices
- Policies attach via index templates, not per index by hand
- Snapshot and delete actions enforce backed-up retention
- `_ilm/explain` and `_ilm/status` are your operational lifeline
