---
tags:
  - databases:elasticsearch
level: intermediate
category: databases
audience:
  - audiences:dbas

---

# Cluster Architecture

---

## What This Chapter Covers

- Node roles and types
- Master nodes, elections, and quorum
- Data nodes and data tiers
- Ingest nodes and pipelines
- Coordinating-only nodes
- Machine learning nodes
- Cluster state management
- Discovery and cluster formation

---

## Node Roles Overview

- Each node can hold one or more roles
- Roles determine what work a node performs
- Common roles: master, data, ingest, ml, coordinating
- Specialized data tiers: data_content, data_hot, data_warm, data_cold, data_frozen
- Also: remote_cluster_client for cross-cluster search/replication
- Configured via `node.roles` in elasticsearch.yml

---

## Configuring node.roles

- An explicit list assigns precise responsibilities
- An empty list creates a coordinating-only node

```yaml
# Dedicated master
node.roles: [ master ]

# Hot data node that can also ingest
node.roles: [ data_hot, data_content, ingest ]

# Coordinating-only node
node.roles: [ ]
```

---

## Master-Eligible Nodes

- Master-eligible nodes can be elected cluster master
- The elected master manages the cluster state
- Master handles index creation, shard allocation, and node membership
- The master does not route or execute search/index data work
- Keep master duties lightweight and stable

---

## Master Elections and Quorum

- One master is elected from the master-eligible nodes
- A quorum (majority) of voting nodes is required to elect/operate
- Quorum prevents split-brain when the network partitions
- Voting configuration tracks the current set of voting nodes
- Loss of quorum makes the cluster read-unavailable for writes/changes

```bash
GET _cluster/state/metadata/cluster_coordination
```

---

## Why Three Dedicated Masters

- Three master-eligible nodes tolerate one failure and keep quorum
- Quorum of three is two; one node can be lost safely
- Two masters cannot form a safe majority on partition
- Use an odd number to avoid tie scenarios
- In large clusters, dedicate masters away from data load

```yaml
node.roles: [ master ]
```

---

## Voting Configuration

- Elasticsearch maintains the set of voting master-eligible nodes
- It auto-adjusts as master-eligible nodes join or leave
- Voting exclusions let you safely remove a master-eligible node

```bash
POST _cluster/voting_config_exclusions?node_names=es-master-3
DELETE _cluster/voting_config_exclusions
```

---

## Data Nodes

- Data nodes store shards and execute index/search/aggregation work
- The heaviest consumers of CPU, RAM, and disk I/O
- Scale horizontally by adding more data nodes
- Storage and heap should be sized for the data they hold
- Generic data role vs specialized tier roles

```yaml
node.roles: [ data, ingest ]
```

---

## Data Tiers

- data_content: non-time-series content (e.g. product catalogs)
- data_hot: most recent, frequently queried, write-heavy data
- data_warm: less frequently queried, read-mostly data
- data_cold: rarely queried, often searchable snapshots
- data_frozen: archival data backed by searchable snapshots
- Index Lifecycle Management moves indices across tiers

---

## Configuring Data Tiers

- Assign tier roles to align hardware with access patterns
- Hot tiers use fast SSDs; cold/frozen use cheaper storage

```yaml
# Hot tier node
node.roles: [ data_hot, data_content ]

# Warm tier node
node.roles: [ data_warm ]
```

---

## Ingest Nodes

- Ingest nodes run pipelines that transform documents before indexing
- Pipelines apply processors (grok, set, rename, geoip, etc.)
- Useful for enrichment and parsing without external ETL

```bash
PUT _ingest/pipeline/add-timestamp
{
  "processors": [
    { "set": { "field": "ingested_at", "value": "{{_ingest.timestamp}}" } }
  ]
}
```

---

## Using an Ingest Pipeline

- Reference the pipeline when indexing documents

```bash
PUT logs/_doc/1?pipeline=add-timestamp
{ "message": "service started" }
```

```bash
# Or set a default pipeline on the index
PUT logs/_settings
{ "index.default_pipeline": "add-timestamp" }
```

---

## Coordinating-Only Nodes

- Created with an empty `node.roles: []`
- Hold no data and are not master-eligible
- Receive client requests, fan out to data nodes, merge results
- Act as smart load balancers and reduce search load on data nodes
- Useful as dedicated query routers for heavy search traffic

```yaml
node.roles: [ ]
```

---

## Machine Learning Nodes

- The `ml` role runs anomaly detection and data frame analytics jobs
- ML work is CPU and memory intensive
- Dedicate ML nodes to isolate that load from data nodes
- Often paired with `remote_cluster_client` for cross-cluster ML

```yaml
node.roles: [ ml, remote_cluster_client ]
```

---

## Cluster State Management

- Cluster state holds metadata: indices, mappings, settings, routing
- The elected master is the authority for cluster state
- Changes are published from the master to all nodes
- State is persisted so the cluster can recover after restart
- Keep state small: avoid excessive indices/fields/templates

```bash
GET _cluster/state?filter_path=metadata.indices.*.settings
```

---

## Discovery and Formation

- Discovery is how nodes find each other and form a cluster
- `discovery.seed_hosts` lists addresses to contact at startup
- Nodes exchange information to elect a master and join

```yaml
discovery.seed_hosts:
  - es-master-1:9300
  - es-master-2:9300
  - es-master-3:9300
```

---

## First-Time Bootstrap

- `cluster.initial_master_nodes` is used only on the very first start
- It seeds the initial voting configuration for a brand-new cluster
- Set it to the `node.name` of the initial master-eligible nodes
- Never set it when adding nodes to an existing cluster

```yaml
cluster.initial_master_nodes:
  - es-master-1
  - es-master-2
  - es-master-3
```

---

## A Production Topology Example

- 3 dedicated master-eligible nodes (quorum, stability)
- Multiple hot/warm/cold data nodes sized per tier
- 2+ coordinating-only nodes for query routing
- Dedicated ML nodes if ML features are used
- Inspect roles and layout with the cat APIs

```bash
GET _cat/nodes?v&h=name,node.role,master,heap.percent
```
