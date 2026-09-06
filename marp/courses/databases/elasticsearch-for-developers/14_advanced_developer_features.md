---
tags:
  - databases:elasticsearch
level: intermediate
category: databases
audience:
  - audiences:developers

---

# Advanced Developer Features

---

## What This Chapter Covers

- Scripted fields
- Painless scripting
- Update by query
- Reindex API
- Snapshot and restore
- Cross-cluster search

---

## Scripted Fields

- Computed at search time
- "rate = count / total"
- Slower than indexed fields
- For: rare or one-off computations

---

## Painless Scripting

- Elasticsearch's scripting language
- Sandboxed Java-like
- Used in: scripted fields, update scripts, function scores
- Default; safe by design

---

## Painless Example

```json
{
  "script": {
    "source": "ctx._source.counter += params.delta",
    "params": { "delta": 1 }
  }
}
```

---

## Update By Query

- Update many documents matching a query
- "Set field X = Y for all docs matching ..."
- Run async; wait for completion
- Beware: long-running

---

## Reindex API

```http
POST _reindex
{
  "source": { "index": "old" },
  "dest": { "index": "new" }
}
```

- Copy from one index to another
- Optional: script to transform
- Async; check status

---

## Snapshot And Restore

- Backup to S3 / GCS / local
- Per-index or whole cluster
- Point-in-time recovery
- Standard for ops

---

## Snapshot Schedule

- ILM can trigger snapshots
- Or: cron + API call
- Test restore periodically

---

## Cross-Cluster Search

- Query multiple clusters from one
- Add remote cluster
- Use `cluster:index` syntax
- For: federation, multi-region

---

## Cross-Cluster Replication

- Active-passive replication
- Hot cluster &#8594; warm in another region
- For: DR, geo
- Commercial feature

---

## Field Capabilities API

- Discover fields available
- Across multiple indexes
- For: dynamic UI, query builders

---

## Multi-Search

```http
POST /_msearch
{}
{ "query": {...} }
{ "index": "products" }
{ "query": {...} }
```

- Multiple searches in one request
- Saves round trips

---

## Async Search

- Long-running queries
- Submit; get an ID; check status; retrieve
- For: large analytics, time-out-prone queries

---

## Watcher / Alerting

- Run a query on schedule
- Trigger an action if condition met
- Email, webhook, Slack
- Commercial feature; OpenSearch has alternative

---

## Common Advanced Mistakes

- Scripted fields in hot search paths (slow)
- Update_by_query without bounded query (huge ops)
- Reindex without alias swap
- Snapshots never tested
- Cross-cluster search across slow networks
