---
tags:
  - databases:elasticsearch
level: intermediate
category: databases
audience:
  - audiences:developers

---

# Client Libraries and Integration

---

## Client Library Options

![client_options](svg/courses/databases/elasticsearch-for-developers/12_client_libraries_and_integration/client_options.svg)

---

## What This Chapter Covers

- Official clients
- Connection management
- Retries and timeouts
- Bulk helpers
- Async clients
- Common pitfalls

---

## Official Clients

- Java, JavaScript / Node, Python, .NET, Go, Ruby, PHP, Rust
- Maintained by Elastic
- API parity
- Standard for production

---

## Connection

```python
from elasticsearch import Elasticsearch
es = Elasticsearch(["http://localhost:9200"])
```

- Or with cluster nodes
- Auth, TLS configurable

---

## Connection Pool

- Reuse client across requests
- Don't construct per-call
- Driver handles pooling

---

## Retries

- Transient errors: client retries
- Configurable
- Idempotent ops only
- Circuit-break on chronic failures

---

## Timeouts

- Connect timeout
- Read timeout
- Per-request override possible
- Set both; never infinite

---

## Bulk Helpers

```python
from elasticsearch.helpers import bulk

actions = [{"_index": "logs", "_source": doc} for doc in docs]
bulk(es, actions)
```

- Handles batching, retries, errors
- Use for any batch ingestion

---

## Async Clients

- Python: AsyncElasticsearch
- Node: built-in async
- For: high-concurrency apps
- Match your app's concurrency model

---

## Search Helpers

- Scan: scroll through large results
- search_after: cursor-based
- Bulk doesn't apply to search

---

## High-Level Clients

- Elasticsearch DSL (Python): query builder
- Elastic transport: lower-level
- Pick: convenience vs control

---

## ORM-Like Layers

- elasticsearch-dsl-py: Python
- olivere/elastic: Go
- Type-safe builders
- Less raw JSON

---

## Configuration

- `verify_certs`: TLS verification
- `request_timeout`: per-call default
- `max_retries`: retry count
- Clean configuration in app code

---

## Authentication

- API key
- Username + password
- Service tokens
- Configure in client; rotate periodically

---

## Multi-Cluster

- Separate clients per cluster
- Or: cross-cluster search at the cluster level
- Manage via service discovery

---

## Common Client Mistakes

- New client per request
- No retries
- Logging request bodies (sensitive data)
- Synchronous calls in async apps
- Hardcoded endpoints
