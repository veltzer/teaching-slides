---
tags:
  - databases:elasticsearch
level: intermediate
category: databases
audience:
  - audiences:dbas

---
# Sharding and Replication

---
## What This Chapter Covers

- Shard allocation and cluster balancing
- Replica configuration and why replicas matter
- Shard allocation filtering by node attributes
- Forced awareness for rack and zone resilience
- Split and shrink index operations
- Reindex, including remote reindex
- Cross-cluster replication with leader and follower indices
- Shard sizing best practices

---
## Shards: The Unit of Distribution

- An index is split into primary shards, each a self-contained Lucene index
- `number_of_primary_shards` is fixed at index creation and cannot be changed later
- Replicas are copies of primaries; the replica count can change anytime
- Shards are spread across nodes for parallelism and resilience

```bash
PUT /metrics
{ "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1
} }
```

---
## Shard Allocation and Balancing

- The allocator decides which node holds each shard, primary and replica
- A primary and its replica are never placed on the same node
- The balancer spreads shards to even out count and disk usage across nodes

```bash
PUT /_cluster/settings
{ "persistent": {
    "cluster.routing.allocation.enable": "all",
    "cluster.routing.allocation.balance.disk_usage": 2.0e-11
} }
```

- `enable` can be `all`, `primaries`, `new_primaries`, or `none`
- Set `none` temporarily during a rolling restart to avoid needless rebalancing

---
## Disk-Based Allocation Watermarks

- The allocator stops placing shards on nodes that are running low on disk

```bash
PUT /_cluster/settings
{ "persistent": {
    "cluster.routing.allocation.disk.watermark.low":  "85%",
    "cluster.routing.allocation.disk.watermark.high": "90%",
    "cluster.routing.allocation.disk.watermark.flood_stage": "95%"
} }
```

- Low: stop allocating new shards to the node
- High: actively move shards off the node
- Flood stage: indices go read-only to prevent a full disk — a serious incident
- DBA note: monitor disk headroom; flood-stage read-only blocks indexing

---
## Replica Configuration

- Replicas provide redundancy and serve read traffic in parallel with primaries
- They protect against node loss; a primary's data survives if a replica exists
- Increasing replicas raises read throughput and storage cost linearly

```bash
PUT /metrics/_settings
{ "index": { "number_of_replicas": 2 } }
```

- With zero replicas, losing one node loses data and turns the cluster red
- DBA rule: production indices need at least one replica
- You can drop replicas to 0 during bulk load, then restore them

---
## Shard Allocation Filtering

- Filter which nodes an index's shards may live on, using node attributes
- Nodes advertise attributes (e.g. `node.attr.box_type: hot`)

```bash
PUT /logs-2026/_settings
{ "index.routing.allocation.require.box_type": "hot" }
```

- `require`: shard must be on nodes with all listed attributes
- `include`: shard may be on nodes with any listed attribute
- `exclude`: shard must avoid nodes with listed attributes
- Use `exclude._name` or `exclude._ip` to drain a node before decommissioning

---
## Draining a Node for Maintenance

- Exclude a node so the allocator relocates its shards elsewhere

```bash
PUT /_cluster/settings
{ "transient": {
    "cluster.routing.allocation.exclude._ip": "10.0.0.7"
} }
```

- Wait for the node to hold no shards, then take it down safely
- Clear the setting afterward to let the node rejoin allocation
- This avoids a red cluster compared to simply killing the node

---
## Forced Awareness

- Allocation awareness spreads replicas across failure domains like racks or zones

```bash
PUT /_cluster/settings
{ "persistent": {
    "cluster.routing.allocation.awareness.attributes": "zone"
} }
```

- With awareness, a primary and replica land in different `zone` values when possible
- Forced awareness guarantees it and reserves capacity for the missing zone

```bash
PUT /_cluster/settings
{ "persistent": {
    "cluster.routing.allocation.awareness.force.zone.values": "z1,z2"
} }
```

- This prevents one zone from holding both copies of a shard

---
## Shard Sizing Best Practices

- Target roughly 10-50 GB per shard for most workloads
- Too many tiny shards (oversharding) wastes heap and cluster-state overhead
- Too few huge shards slow recovery, relocation, and snapshots
- Rough guideline: keep shards per node proportional to heap, around 20 per GB of heap
- Size indices with time-based rollover rather than one ever-growing index
- DBA rule: plan shard count up front — primaries cannot be changed in place

---
## Shrinking an Index

- `_shrink` reduces primary shard count by merging shards into fewer, larger ones
- Target shard count must divide the source count (e.g. 6 to 3, or 6 to 1)
- Preconditions: index read-only, all primaries on one node, green health

```bash
PUT /logs/_settings
{ "settings": {
    "index.blocks.write": true,
    "index.routing.allocation.require._name": "node-1"
} }

POST /logs/_shrink/logs-small
{ "settings": { "index.number_of_shards": 1 } }
```

- Good for shrinking old, oversharded indices before moving them to cold storage

---
## Splitting an Index

- `_split` increases primary shard count for an index that grew larger than planned
- The index must have been created with `index.number_of_routing_shards` headroom
- Target count must be a multiple of the source count

```bash
PUT /logs/_settings
{ "settings": { "index.blocks.write": true } }

POST /logs/_split/logs-big
{ "settings": { "index.number_of_shards": 6 } }
```

- Splitting copies segments efficiently rather than re-indexing documents
- Use it when shards have grown well past the 50 GB guideline

---
## Reindex

- `_reindex` copies documents from a source index to a destination index
- Used to change mappings, analyzers, or shard count that cannot change in place

```bash
POST /_reindex
{
  "source": { "index": "products-v1",
              "query": { "term": { "active": true } } },
  "dest":   { "index": "products-v2" }
}
```

- Run with `wait_for_completion=false` for large jobs and poll `_tasks`
- Tune with `slices=auto` for parallelism and `requests_per_second` to throttle

---
## Remote Reindex

- `_reindex` can pull from a remote cluster, useful for migrations and upgrades
- The remote host must be allowlisted via `reindex.remote.whitelist` in config

```bash
POST /_reindex
{
  "source": {
    "remote": { "host": "https://old-cluster:9200",
                "username": "elastic", "password": "***" },
    "index": "products"
  },
  "dest": { "index": "products" }
}
```

- Throttle remote reindex; it competes with the source cluster's resources

---
## Cross-Cluster Replication

- CCR replicates indices from a leader cluster to follower clusters
- Use cases: disaster recovery, data locality, and read scaling across regions
- Replication is asynchronous; followers are read-only copies of the leader
- The follower pulls operations from the leader's shards using sequence numbers
- CCR requires the appropriate license tier

---
## Configuring a Follower Index

- Register the remote (leader) cluster, then create a follower index

```bash
PUT /_cluster/settings
{ "persistent": { "cluster": { "remote": {
    "leader": { "seeds": [ "leader-node:9300" ] }
} } } }

PUT /products-follower/_ccr/follow
{ "remote_cluster": "leader", "leader_index": "products" }
```

- Auto-follow patterns can replicate new indices matching a name pattern automatically
- For failover, pause and unfollow to convert the follower into a normal writable index

```bash
POST /products-follower/_ccr/pause_follow
```

---
## Operational Summary

- Choose primary shard count carefully; it is fixed for the life of the index
- Always run at least one replica in production for resilience and read scaling
- Use allocation filtering to drain nodes and awareness to survive zone loss
- Shrink oversharded old indices; split indices that outgrew their plan
- Reindex to change mappings; use remote reindex for cross-cluster migration
- Use CCR for cross-region DR and data locality with read-only followers
