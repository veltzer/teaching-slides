---
tags:
  - databases:elasticsearch
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Introduction to Elasticsearch

---
## What This Chapter Covers

- What Elasticsearch is
- The ELK / Elastic stack
- Use cases
- Versus alternatives
- A short history

---
## What Elasticsearch Is

- Distributed, full-text search engine
- Built on Apache Lucene
- JSON over HTTP
- Real-time search
- Industry standard for search and log analytics

---
## The Elastic Stack

- **Elasticsearch**: search and analytics
- **Logstash**: data pipeline (legacy / heavy)
- **Beats**: lightweight shippers
- **Kibana**: visualisation
- "ELK" or "Elastic stack"

---
## Use Cases

- Full-text search (websites, products)
- Log aggregation (centralised logs)
- Metrics and observability
- Security (SIEM)
- Geospatial search
- Vector / semantic search

---
## ES vs Solr

- Both built on Lucene
- ES: cloud-native, API-first
- Solr: older, deeper customisation
- ES has won most of the market

---
## ES vs OpenSearch

- AWS forked ES after license change
- OpenSearch: AWS-driven; Apache 2.0
- API-compatible largely
- Pick by: cloud preference, license needs

---
## Versions

- 7.x is widely deployed
- 8.x is the modern; security-on by default
- Major changes between major versions
- Run a recent version

---
## Document-Oriented

- Each "row" is a JSON document
- Documents go into indexes
- Schema (mapping) optional but recommended
- Inverted index for fast text search

---
## Inverted Index

- Term &#8594; list of documents containing it
- The data structure that makes search fast
- Built per-field
- Updated as documents are indexed

---
## Distributed By Design

- Cluster of nodes
- Indexes split into shards
- Each shard replicated
- Survives node failure

---
## REST API

- Everything is HTTP + JSON
- Clusters expose: index, search, aggregate, manage
- Curl-friendly
- No SQL by default (ES|QL added later)

---
## Hosted Options

- Elastic Cloud (official)
- AWS OpenSearch Service
- Self-hosted on Kubernetes
- Docker for dev

---
## Common Misconceptions

- "ES is a database" — primary store risky; usually paired with one
- "ES handles transactions" — no
- "Schemaless" — sort of; mappings recommended
- "Free" — Apache 2 is gone for 7.11+; SSPL or Elastic License
