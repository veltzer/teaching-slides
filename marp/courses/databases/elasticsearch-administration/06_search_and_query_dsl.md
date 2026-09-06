---
tags:
  - databases:elasticsearch
level: intermediate
category: databases
audience:
  - audiences:dbas

---

# Search and Query DSL

---

## What This Chapter Covers

- Query context versus filter context
- Full-text queries: match and multi_match
- Term-level queries: term, terms, range
- Compound queries with bool
- The aggregations framework
- Search performance optimization techniques
- Profiling and validating queries
- Deep pagination with scroll, search_after, and PIT

---

## The Search Request

- Searches go to `_search` with a JSON Query DSL body

```bash
GET /products/_search
{
  "query": { "match": { "name": "widget" } },
  "from": 0,
  "size": 10
}
```

- The coordinating node fans out to shards, gathers, and merges results
- `took` reports milliseconds; `_shards` reports per-shard success and failures
- Each hit carries `_score`, `_id`, and `_source`

---

## Query Context vs Filter Context

- Query context answers "how well does this match?" and computes a relevance `_score`
- Filter context answers "does this match, yes or no?" with no scoring
- Filter results are cacheable; query (scoring) results generally are not

```bash
GET /logs/_search
{ "query": { "bool": {
    "must":   [ { "match": { "message": "error" } } ],
    "filter": [ { "term": { "level": "WARN" } },
                { "range": { "@timestamp": { "gte": "now-1h" } } } ]
} } }
```

- DBA rule: put anything not needed for ranking in `filter` to gain caching and speed

---

## The Node Query Cache

- Filter-context results are cached per segment in the node query cache
- Controlled by `indices.queries.cache.size` (default 10% of heap)
- Caches reusable, repeated filters like `term` and `range` on stable values
- Date filters like `now-1h` are less cacheable because the bound keeps moving
- Round time bounds (e.g. `now-1h/h`) so the filter is stable and cache-friendly

```bash
GET /_nodes/stats/indices/query_cache
```

---

## Full-Text Queries: match

- `match` analyzes the input the same way the field was analyzed, then scores
- Used for human language text fields

```bash
GET /articles/_search
{ "query": { "match": {
    "body": { "query": "fast distributed search", "operator": "and" }
} } }
```

- `operator: and` requires all terms; default `or` matches any
- `minimum_should_match` tunes how many terms must appear
- `match_phrase` requires terms adjacent and in order

---

## Full-Text Queries: multi_match

- `multi_match` runs a match across several fields at once

```bash
GET /articles/_search
{ "query": { "multi_match": {
    "query": "elasticsearch tuning",
    "fields": [ "title^3", "body" ],
    "type": "best_fields"
} } }
```

- `title^3` boosts title matches three times over body
- `best_fields` uses the single best-scoring field; `cross_fields` treats fields as one
- Choose the type to match how the data is structured

---

## Term-Level Queries

- Term-level queries are not analyzed — they match exact terms
- Use them on keyword, numeric, date, and boolean fields, never analyzed text

```bash
GET /products/_search
{ "query": { "term": { "status": "active" } } }

GET /products/_search
{ "query": { "terms": { "category": [ "a", "b", "c" ] } } }
```

- A `term` query on an analyzed `text` field usually returns nothing — a classic gotcha
- Match against the `.keyword` sub-field for exact matching of text

---

## Range Queries

- `range` matches numeric, date, or IP values within bounds

```bash
GET /orders/_search
{ "query": { "range": {
    "created": { "gte": "now-7d/d", "lte": "now/d" }
} } }
```

- Operators: `gte`, `gt`, `lte`, `lt`
- Date math (`now-7d/d`) rounds and improves cacheability
- Range in filter context is cheap and cacheable; prefer it over scored ranges

---

## Compound Queries with bool

- `bool` combines clauses into one query
- `must`: must match, contributes to score
- `should`: optional, boosts score; can be made mandatory via `minimum_should_match`
- `filter`: must match, no score, cacheable
- `must_not`: must not match, no score, cacheable

```bash
GET /products/_search
{ "query": { "bool": {
    "must":     [ { "match": { "name": "phone" } } ],
    "filter":   [ { "range": { "price": { "lte": 500 } } } ],
    "must_not": [ { "term": { "discontinued": true } } ],
    "should":   [ { "term": { "brand": "acme" } } ]
} } }
```

---

## Aggregations Framework

- Aggregations summarize data rather than returning documents
- Metric aggs compute values; bucket aggs group documents
- Set `size: 0` to skip hits and return only aggregation results

```bash
GET /orders/_search
{ "size": 0,
  "aggs": {
    "avg_total": { "avg": { "field": "total" } },
    "max_total": { "max": { "field": "total" } }
} }
```

- Metric examples: `avg`, `sum`, `min`, `max`, `stats`, `cardinality`, `percentiles`

---

## Bucket Aggregations

- `terms` groups by field value; `date_histogram` groups by time interval
- Aggregations nest: put metrics inside buckets

```bash
GET /orders/_search
{ "size": 0,
  "aggs": {
    "per_day": {
      "date_histogram": { "field": "created", "calendar_interval": "day" },
      "aggs": { "revenue": { "sum": { "field": "total" } } }
} } }
```

- `terms` is approximate on distributed data; raise `shard_size` for accuracy
- High-cardinality `terms` aggs are heavy — they load `doc_values` and use memory

---

## Search Performance Optimization

- Move non-scoring conditions to `filter` context for caching
- Use `_source` filtering to return only needed fields, cutting network and CPU

```bash
GET /products/_search
{ "_source": [ "name", "price" ],
  "query": { "match_all": {} } }
```

- Disable `_source` retrieval with `"_source": false` when you only need IDs
- Aggregations and sorts use `doc_values` (on by default) — keep them enabled
- Avoid `script` queries and `wildcard`/leading-wildcard patterns on hot paths

---

## doc_values and fielddata

- `doc_values` are an on-disk columnar store used for sorting and aggregations
- They are enabled by default for all non-analyzed fields
- `text` fields have no `doc_values`; aggregating on them needs in-memory `fielddata`
- `fielddata` on `text` is expensive and off by default — aggregate on `.keyword` instead
- DBA rule: never enable `fielddata` on large text fields to "make a sort work"

```bash
# Disable doc_values only for fields you never sort or aggregate on
"tags": { "type": "keyword", "doc_values": false }
```

---

## Search Profiling

- `_profile` returns a detailed per-shard breakdown of query and collector time

```bash
GET /products/_search
{ "profile": true,
  "query": { "match": { "name": "widget" } } }
```

- Profiling shows which clauses dominate and where time is spent
- It adds overhead; use it for diagnosis, not in production traffic
- `_validate/query?explain=true` checks a query and shows how it rewrites

```bash
GET /products/_validate/query?explain=true
{ "query": { "match": { "name": "widget" } } }
```

---

## Deep Pagination Problem

- `from + size` must gather and sort `from + size` hits on every shard
- Default `index.max_result_window` caps `from + size` at 10000
- Deep paging with large `from` is expensive and memory-hungry
- Three better options: scroll, search_after, and Point In Time
- DBA guidance: never raise `max_result_window` to brute-force deep paging

---

## Scroll

- Scroll snapshots the index and pages through a large result set sequentially

```bash
POST /products/_search?scroll=2m
{ "size": 1000, "query": { "match_all": {} } }

POST /_search/scroll
{ "scroll": "2m", "scroll_id": "DXF1ZXJ5..." }
```

- Each call returns the next batch; the snapshot pins segments from merging
- Open scrolls hold resources — always clear them when done

```bash
DELETE /_search/scroll
{ "scroll_id": "DXF1ZXJ5..." }
```

- Scroll is for batch export, not for live user pagination

---

## search_after and Point In Time

- `search_after` pages forward using the last hit's sort values — stateless and scalable
- Combine with a Point In Time (PIT) for a consistent view across pages

```bash
POST /products/_pit?keep_alive=1m

GET /_search
{ "size": 1000,
  "pit": { "id": "46To...", "keep_alive": "1m" },
  "sort": [ { "price": "asc" }, { "_shard_doc": "asc" } ],
  "search_after": [ 9.99, 12345 ] }
```

- This is the modern recommended approach for deep, consistent pagination
- Always close the PIT when finished to release resources
