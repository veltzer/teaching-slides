---
tags:
  - databases:elasticsearch
level: intermediate
category: databases
audience:
  - audiences:dbas

---
# Document Operations

---
## What This Chapter Covers

- Indexing documents with PUT and POST
- Bulk operations and the NDJSON `_bulk` format
- Update and delete operations, including scripted updates
- Versioning and optimistic concurrency control
- Routing and search preference
- Refresh, flush, and translog durability
- DBA guidance for throughput and durability trade-offs

---
## Indexing a Single Document

- `PUT` with an explicit ID is idempotent for that ID
- `POST` to `_doc` auto-generates an ID

```bash
PUT /products/_doc/1
{ "name": "widget", "price": 9.99, "in_stock": true }

POST /products/_doc
{ "name": "gadget", "price": 19.99 }
```

- Response includes `_index`, `_id`, `_version`, and `result` (`created` or `updated`)
- Use `op_type=create` to fail if the document already exists

---
## Create vs Index Semantics

- `PUT /idx/_doc/1` overwrites any existing document with that ID
- `PUT /idx/_create/1` (or `op_type=create`) fails with 409 if the ID exists

```bash
PUT /products/_create/1
{ "name": "widget" }
```

- DBA note: prefer `_create` when the application must never silently clobber existing data
- Every write bumps `_version` and the sequence number even on overwrite

---
## Bulk Operations and NDJSON

- The `_bulk` API batches many index/create/update/delete actions in one request
- Format is newline-delimited JSON (NDJSON): an action line, then an optional source line
- Each line must end with a newline, including the last one

```bash
POST /_bulk
{ "index": { "_index": "products", "_id": "1" } }
{ "name": "widget", "price": 9.99 }
{ "delete": { "_index": "products", "_id": "2" } }
{ "update": { "_index": "products", "_id": "3" } }
{ "doc": { "price": 5.00 } }
```

---
## Sizing Bulk Batches

- Bulk is the single biggest throughput lever for ingest
- Start around 5-15 MB per request, or a few thousand docs, then tune empirically
- Too small wastes round-trips; too large pressures heap and the bulk thread pool queue
- Send bulk requests concurrently from multiple client threads to saturate nodes
- Always inspect the response: a 200 status does not mean every item succeeded

```bash
# Each item has its own status; check the top-level "errors" flag
{ "errors": true, "items": [ { "index": { "status": 429, ... } } ] }
```

- A 429 means `es_rejected_execution` — back off and retry that item

---
## Partial Updates with _update

- `_update` modifies a document without resending the whole source
- Internally it is a get-then-reindex; the doc is fully rewritten

```bash
POST /products/_update/1
{ "doc": { "price": 7.49 } }
```

- Use `doc_as_upsert: true` to insert when the document is missing
- Use `detect_noop` (default on) to skip writes when nothing changed

---
## Scripted Updates

- Scripts run server-side via Painless, avoiding a read round-trip
- Common for counters, list appends, and conditional logic

```bash
POST /products/_update/1
{
  "script": {
    "source": "ctx._source.views += params.n",
    "params": { "n": 1 }
  },
  "upsert": { "views": 0 }
}
```

- `ctx.op = 'noop'` or `'delete'` can short-circuit the write
- Scripts cost CPU; avoid heavy scripted updates in hot ingest paths

---
## Delete Operations

- Delete by ID is a normal write that creates a tombstone

```bash
DELETE /products/_doc/1
```

- Deleted docs are marked, not immediately removed; space is reclaimed at segment merge
- `_delete_by_query` deletes all docs matching a query

```bash
POST /products/_delete_by_query
{ "query": { "range": { "price": { "lt": 1.0 } } } }
```

---
## Delete and Update by Query Operations

- Both run as background tasks over a snapshot of matching docs
- Use `wait_for_completion=false` to get a task ID and poll `_tasks`
- Tune `scroll_size`, `requests_per_second`, and `slices` for throttling and parallelism

```bash
POST /products/_update_by_query?slices=auto&wait_for_completion=false
{
  "script": { "source": "ctx._source.price *= 1.1" },
  "query": { "term": { "category": "sale" } }
}
```

- Version conflicts mid-run can abort the job; set `conflicts=proceed` to skip them

---
## Document Versioning

- Every document carries an internal `_version` that increments on each write
- `_seq_no` and `_primary_term` track the order and primary that made each change
- These are the basis for optimistic concurrency control
- Internal versioning is automatic; external versioning lets you supply your own numbers

```bash
PUT /products/_doc/1?version=5&version_type=external
{ "name": "widget" }
```

- External versioning is useful when an external system is the source of truth

---
## Optimistic Concurrency Control

- Read a document, then write back conditionally on its `_seq_no` and `_primary_term`
- If another writer changed it first, the write fails with 409 and you retry

```bash
PUT /products/_doc/1?if_seq_no=362&if_primary_term=2
{ "name": "widget", "price": 8.99 }
```

- This is the correct pattern for concurrent updates, not blind overwrites
- Combine with `_update` `retry_on_conflict=N` for automatic retries

```bash
POST /products/_update/1?retry_on_conflict=3
{ "doc": { "stock": 0 } }
```

---
## Routing

- By default a document's shard is `hash(_id) % number_of_primary_shards`
- Custom routing forces related docs onto the same shard

```bash
PUT /orders/_doc/1?routing=customer42
{ "customer": "customer42", "total": 120 }
```

- Routed queries hit one shard instead of all, cutting search cost
- DBA caution: a hot routing key creates a hot shard and uneven sizing
- You must supply the same routing value on get, update, and delete

---
## Search Preference

- `preference` controls which shard copies serve a search
- Default behavior round-robins across primary and replica copies

```bash
GET /products/_search?preference=_local
GET /products/_search?preference=user_session_7
```

- A custom string keeps a user pinned to the same copies for consistent ordering
- `_local` favors the coordinating node's own shards to cut network hops
- Avoid forcing `_primary`; it removes replica read scaling

---
## Refresh: Making Writes Searchable

- Writes are not searchable until a refresh creates a new segment
- Default `index.refresh_interval` is 1s — near real-time, not real-time

```bash
PUT /products/_settings
{ "index": { "refresh_interval": "30s" } }
```

- `?refresh=wait_for` waits for the next refresh; `?refresh=true` forces one
- DBA note: forcing refresh per request kills ingest throughput
- During heavy bulk load, raise or disable the interval, then restore it

---
## Flush and the Translog

- The translog is a per-shard write-ahead log for durability between Lucene commits
- Refresh makes data searchable; flush performs a Lucene commit and trims the translog
- Flush happens automatically; manual flush is rarely needed

```bash
POST /products/_flush
```

- `index.translog.flush_threshold_size` (default 512mb) triggers automatic flush
- Recovery replays the translog, so a large translog slows restart

---
## Translog Durability

- `index.translog.durability` controls when the translog is fsync'd

```bash
PUT /products/_settings
{ "index": { "translog.durability": "async",
             "translog.sync_interval": "5s" } }
```

- `request` (default): fsync after every write — safest, slowest
- `async`: fsync on an interval — higher throughput, risks losing the last interval
- DBA decision: use `async` only when re-ingest on crash is acceptable
- For financial or audit data, keep the default `request` durability

---
## Operational Summary

- Use `_bulk` for ingest; size batches by MB and watch for 429s
- Prefer optimistic concurrency over blind overwrites for shared documents
- Custom routing speeds reads but watch for hot shards
- Tune `refresh_interval` up during bulk loads, restore afterward
- Choose translog durability per data criticality, not globally by habit
- Update/delete-by-query are background tasks — throttle and monitor via `_tasks`
