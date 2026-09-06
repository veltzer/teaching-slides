---
tags:
  - databases:elasticsearch
level: intermediate
category: databases
audience:
  - audiences:dbas

---

# Cluster Operations

---

## What This Chapter Covers

- Performing safe rolling upgrades node by node
- Full cluster restart procedures
- Decommissioning and draining nodes
- The cluster reroute and allocation explain APIs
- Task management: listing and cancelling tasks
- Maintenance mode and flushing
- License management with the `_license` API

---

## Day-Two Operations Overview

- Production clusters need routine, low-risk change procedures
- Most operations revolve around shard allocation control
- Goal: change the cluster without losing data or availability
- Always check cluster health before and after each step
- Version compatibility governs every upgrade decision
- Automate where possible, but understand every API call

```bash
GET _cluster/health?pretty
```

---

## Version Compatibility Rules

- Rolling upgrades supported between adjacent major versions
- Nodes may run a newer version than the elected master briefly
- Never downgrade a node once it has joined an upgraded cluster
- A node on a newer major version cannot rejoin an older master
- Snapshots from a newer cluster cannot restore to an older one
- Check the official upgrade matrix before starting

---

## Rolling Upgrade: Preparation

- Verify cluster health is green before you begin
- Take a snapshot as a rollback safety net
- Stop non-essential indexing if possible to reduce churn
- Review breaking changes and deprecation logs first
- Plan to upgrade data nodes last among each role group

```bash
GET _snapshot/my_repo/_all
POST _snapshot/my_repo/pre_upgrade_snap?wait_for_completion=false
```

---

## Rolling Upgrade: Disable Allocation

- Stop the cluster from rebalancing shards while a node is down
- Set allocation to `primaries` so only primaries can move
- This prevents wasteful shard copying during the restart
- Skipping this step causes large I/O and slow recovery

```bash
PUT _cluster/settings
{
  "persistent": {
    "cluster.routing.allocation.enable": "primaries"
  }
}
```

---

## Rolling Upgrade: Stop and Upgrade a Node

- Optionally perform a synced or normal flush to speed recovery
- Stop the Elasticsearch service on one node only
- Upgrade the package and plugins to the matching version
- Keep config (`elasticsearch.yml`, `jvm.options`) consistent
- Start the node and wait for it to rejoin the cluster

```bash
POST _flush
sudo systemctl stop elasticsearch
sudo apt-get install elasticsearch=9.0.1
sudo systemctl start elasticsearch
```

---

## Rolling Upgrade: Re-enable Allocation

- After the node rejoins, allow shards to allocate again
- Wait for the cluster to return to green before the next node
- Watch recovery progress to confirm shards are settling
- Repeat the whole cycle for each remaining node

```bash
PUT _cluster/settings
{
  "persistent": {
    "cluster.routing.allocation.enable": null
  }
}
GET _cat/recovery?active_only=true&v
```

---

## Rolling Upgrade: Verify Each Node

- Confirm the upgraded node reports the new version
- Ensure cluster health is green before touching the next node
- Check that no shards remain unassigned unexpectedly
- Master-eligible nodes: keep a quorum online at all times

```bash
GET _cat/nodes?v&h=name,version,node.role
GET _cluster/health?wait_for_status=green&timeout=300s
```

---

## Full Cluster Restart

- Used for major changes that cannot be done node by node
- Causes downtime — schedule a maintenance window
- Disable allocation, then stop all nodes
- Start master-eligible nodes first, then data nodes
- Re-enable allocation only after enough nodes have joined

```bash
PUT _cluster/settings
{ "persistent": { "cluster.routing.allocation.enable": "none" } }
```

---

## Node Decommissioning: Exclude Allocation

- Gracefully move all shards off a node before removal
- Use allocation filtering by node name, IP, or attribute
- Elasticsearch drains shards to other eligible nodes
- The node stays in the cluster while it empties

```bash
PUT _cluster/settings
{
  "transient": {
    "cluster.routing.allocation.exclude._name": "data-node-07"
  }
}
```

---

## Node Decommissioning: Confirm the Drain

- Watch the node until it holds zero shards
- Only then stop the service and remove the host
- Clear the exclude setting afterward to keep config clean
- Verify capacity remains sufficient on the remaining nodes

```bash
GET _cat/shards?v&h=index,shard,prirep,node | grep data-node-07
GET _cat/allocation?v
```

---

## Cluster Reroute API

- Manually move, cancel, or allocate individual shards
- Useful when automatic allocation cannot place a shard
- `move` relocates a shard between nodes
- `allocate_replica` forces a replica onto a node
- Use sparingly — let automatic allocation work normally

```bash
POST _cluster/reroute
{
  "commands": [
    { "move": { "index": "logs-2026", "shard": 0,
                "from_node": "data-01", "to_node": "data-02" } }
  ]
}
```

---

## Retry Failed Allocations

- Shards that fail allocation too many times are abandoned
- A reroute with `retry_failed` retriggers the attempt
- Common after fixing disk space or permission issues
- Combine with allocation explain to find the root cause

```bash
POST _cluster/reroute?retry_failed=true
```

---

## Allocation Explain API

- Explains why a shard is or is not allocated
- The first stop for diagnosing yellow or red clusters
- Without a body, it picks an arbitrary unassigned shard
- With a body, it targets a specific index and shard

```bash
GET _cluster/allocation/explain
{
  "index": "logs-2026",
  "shard": 0,
  "primary": true
}
```

---

## Reading Allocation Decisions

- The response lists each node and its allocation decision
- `decider` names the rule that blocked allocation
- Common blockers: disk watermark, allocation filter, awareness
- `allocate_explanation` summarizes the verdict in plain text
- Fix the underlying decider, then retry failed allocations

---

## Task Management API

- Every long-running operation runs as a cancellable task
- List all tasks or filter by action, node, or parent
- Identify runaway searches, reindex jobs, or merges
- Each task has an id of the form `node_id:task_number`

```bash
GET _tasks?detailed=true&group_by=parents
GET _tasks?actions=*search&detailed
```

---

## Cancelling Tasks

- Cancel a task that is overloading the cluster
- Only cancellable tasks (search, reindex, etc.) will stop
- Cancel by task id or by matching action and node
- Verify the task disappears from the task list afterward

```bash
POST _tasks/oTUltX4IQMOUUVeiohTt8A:124/_cancel
POST _tasks/_cancel?actions=*reindex
```

---

## Maintenance Mode

- Before risky maintenance, freeze cluster movement
- Disable allocation so shards stay put during work
- Flush to commit the translog to Lucene and speed restart
- Disable Curator or ILM-driven changes if needed
- Re-enable allocation and ILM when work is complete

```bash
PUT _cluster/settings
{ "transient": { "cluster.routing.allocation.enable": "none" } }
POST _flush
```

---

## License Management

- View the current license type, status, and expiry date
- Self-managed clusters start on a basic (free) license
- Apply a trial or a purchased enterprise license via API
- Monitor expiry — features degrade when a license lapses

```bash
GET _license
POST _license/start_trial?acknowledge=true
PUT _license
{ "license": { "uid": "...", "type": "platinum", "signature": "..." } }
```

---

## Operations Checklist

- Always confirm health green before and after changes
- Disable allocation for any planned node downtime
- Drain nodes with allocation excludes, never abrupt removal
- Use allocation explain before forcing reroutes
- Cancel rogue tasks rather than restarting nodes
- Keep snapshots current as your rollback path

```bash
GET _cluster/health
GET _cat/allocation?v
```
