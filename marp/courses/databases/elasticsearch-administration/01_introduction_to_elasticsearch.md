---
tags:
  - databases:elasticsearch
level: intermediate
category: databases
audience:
  - audiences:dbas

---

# Introduction to Elasticsearch

---

## What This Chapter Covers

- Elasticsearch architecture and core concepts
- Documents, indices, and shards
- Nodes and cluster topology
- Lucene fundamentals and the inverted index
- Comparison with traditional relational databases
- Use cases and deployment patterns
- Self-managed vs Elastic Cloud vs Kubernetes (ECK)

---

## What Is Elasticsearch?

- Distributed, RESTful search and analytics engine
- Built on top of Apache Lucene
- Stores schema-flexible JSON documents
- Designed for near real-time search at scale
- Part of the Elastic Stack (Elasticsearch, Kibana, Beats, Logstash)
- Common for search, observability (logs/metrics/traces), and security (SIEM)

---

## Core Architectural Concepts

- Everything is exposed over a JSON HTTP REST API
- Horizontally scalable: add nodes to grow capacity
- Data is sharded and replicated automatically
- Highly available: replicas survive node loss
- Near real-time: documents searchable ~1s after indexing
- Distributed by default — no single point of failure when sized correctly

---

## Documents

- The basic unit of information is a JSON document
- Each document belongs to exactly one index
- Documents have an `_id` (provided or auto-generated)
- Internally stored with metadata: `_index`, `_id`, `_version`, `_source`
- Schema-flexible but governed by the index mapping

```json
{
  "_index": "products",
  "_id": "1",
  "_source": { "name": "Widget", "price": 9.99, "in_stock": true }
}
```

---

## Indices

- An index is a logical collection of related documents
- Conceptually similar to a table, but schema-on-write via mappings
- Identified by a lowercase name (e.g. `logs-2026.06`)
- Each index has settings (shards, replicas) and mappings (fields)
- Indices are physically composed of one or more shards

```bash
GET _cat/indices?v
```

---

## Shards

- A shard is a self-contained Lucene index
- An index is split into one or more primary shards
- Sharding enables horizontal scale and parallelism
- Primary shard count is fixed at creation time
- Each shard holds a subset of the index's documents
- A document is routed to a shard by hashing its routing value (default `_id`)

---

## Replica Shards

- Each primary shard can have zero or more replicas
- Replicas are exact copies of a primary on a different node
- Provide high availability if a node fails
- Serve read/search traffic to increase throughput
- Replica count can be changed at any time

```bash
PUT products/_settings
{ "index.number_of_replicas": 2 }
```

---

## Nodes

- A node is a single running Elasticsearch instance (one JVM)
- Each node has a name and belongs to one cluster
- Nodes hold data shards and/or perform cluster duties
- Nodes have roles (master, data, ingest, coordinating, ML, etc.)
- Multiple nodes typically run on separate hosts for resilience

```bash
GET _cat/nodes?v
```

---

## Cluster Topology

- A cluster is one or more nodes sharing a `cluster.name`
- One elected master node manages the cluster state
- Data nodes store shards and execute search/index operations
- Coordinating nodes route requests and merge results
- Cluster health is reported as green, yellow, or red

```bash
GET _cluster/health
```

---

## Cluster Health States

- Green: all primary and replica shards are allocated
- Yellow: all primaries allocated, some replicas unassigned
- Red: at least one primary shard is unassigned (data unavailable)
- Single-node clusters are typically yellow (no place for replicas)
- Investigate unassigned shards with the allocation explain API

```bash
GET _cluster/allocation/explain
```

---

## Apache Lucene Fundamentals

- Elasticsearch is a distributed layer over Lucene
- Lucene provides indexing, storage, and search on a single machine
- Each shard is one Lucene index made of immutable segments
- Segments are merged over time into larger segments
- Lucene handles the inverted index, scoring, and term storage

---

## Segments and Merging

- Indexing creates small immutable segments
- New segments become searchable on refresh (default every 1s)
- Deletes are marked, not removed, until merge reclaims space
- Background merges combine segments and purge deleted docs
- Force merge can reduce segment count on read-only indices

```bash
POST logs-2026.06/_forcemerge?max_num_segments=1
```

---

## The Inverted Index

- Maps each term to the list of documents containing it
- Built per field by the analysis (tokenization) pipeline
- Enables fast full-text lookup without scanning every document
- Stores term frequencies and positions for ranking and phrases
- Complemented by doc values (columnar) for sorting and aggregations

---

## Inverted Index Example

- Source documents are analyzed into terms
- Terms point back to document IDs

```output
Doc 1: "the quick brown fox"
Doc 2: "the lazy brown dog"

term   -> postings
brown  -> [1, 2]
quick  -> [1]
fox    -> [1]
lazy   -> [2]
dog    -> [2]
```

---

## Comparison With Relational Databases

- Index ≈ table, document ≈ row, field ≈ column (loosely)
- Schema-on-write via mappings, but flexible and additive
- No SQL joins; denormalization and nested/parent-child instead
- No multi-document ACID transactions
- Optimized for search and aggregation, not OLTP updates
- Eventual consistency for search; per-document operations are strongly consistent

---

## When To Use Elasticsearch

- Full-text and faceted search applications
- Log and event analytics (observability)
- Metrics and APM / tracing data
- Security analytics and SIEM
- Real-time dashboards over large datasets
- Not a replacement for a transactional system of record

---

## Deployment Patterns: Self-Managed

- Install on bare metal or VMs you operate
- Full control over OS, JVM, storage, and network
- You own upgrades, backups, security, and monitoring
- Best when you need on-prem or strict data control
- Highest operational effort

---

## Deployment Patterns: Elastic Cloud

- Managed Elasticsearch Service hosted by Elastic
- Provisioning, scaling, upgrades, and backups handled for you
- Hot/warm/cold/frozen tiers configured through the console
- Available across major cloud providers and regions
- Trades control for reduced operational burden

---

## Deployment Patterns: Kubernetes (ECK)

- Elastic Cloud on Kubernetes operator manages clusters in K8s
- Declarative CRDs describe clusters, nodes, and topology
- Operator handles orchestration, upgrades, and certificates
- Good fit for teams already standardized on Kubernetes
- Combines self-managed control with operator automation
