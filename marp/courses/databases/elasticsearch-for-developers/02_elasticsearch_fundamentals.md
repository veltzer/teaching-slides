---
tags:
  - databases:elasticsearch
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Elasticsearch Fundamentals

---
## What This Chapter Covers

- Cluster, node, index, shard
- Documents and types
- Replicas
- The REST API basics
- Health states

---
## Cluster

- A group of nodes that share data
- Has a name; nodes join by name
- One master node coordinates metadata

---
## Node

- A single Elasticsearch instance
- Roles: master, data, ingest, ML, coordinating
- Most production: dedicated master + data nodes

---
## Index

- A namespace for documents
- Like a "database" in SQL terms
- Sharded across nodes
- One mapping (schema)

---
## Shard

- A subset of an index's data
- One Lucene index instance
- Number set at index creation; can be reindexed
- Distributes load and storage

---
## Primary And Replica Shards

- Each shard: 1 primary + N replicas
- Writes to primary; replicated to replicas
- Reads can hit any
- Replicas survive node failure

---
## Cluster Topology

![cluster_nodes_shards](svg/courses/databases/elasticsearch-for-developers/02_elasticsearch_fundamentals/cluster_nodes_shards.svg)

---
## Documents

- JSON objects
- Stored in an index
- Have an _id (auto-generated or assigned)
- Versioned for optimistic concurrency

---
## A Simple Example

```bash
PUT /products/_doc/1
{ "name": "Phone", "price": 599 }

GET /products/_doc/1

GET /products/_search?q=phone
```

---
## Health States

- **green**: all primaries and replicas allocated
- **yellow**: all primaries allocated; some replicas missing
- **red**: some primaries missing
- Yellow is OK in dev; not in prod

---
## Types (Deprecated)

- Older versions: types within an index (like sub-tables)
- Modern (7+): one type per index
- _doc placeholder for compatibility
- Often: one logical "thing" per index

---
## Mapping

- The schema for an index
- Field types: text, keyword, long, date, etc.
- Auto-detected on first index (dynamic mapping)
- Better: define explicitly

---
## Refresh

- New / changed documents not searchable until refreshed
- Default: every 1 second
- Trade-off: real-time search vs throughput
- Manual refresh for tests

---
## CRUD APIs

- PUT /index/_doc/id (insert / replace)
- POST /index/_doc (insert; auto-id)
- POST /index/_update/id (partial update)
- DELETE /index/_doc/id
- GET /index/_doc/id

---
## Common Fundamental Mistakes

- Letting auto-mapping run; weird inferred types
- Too many shards (overhead)
- Too few shards (can't scale write)
- Mixing different document shapes in one index
- Treating ES as primary store without backup
