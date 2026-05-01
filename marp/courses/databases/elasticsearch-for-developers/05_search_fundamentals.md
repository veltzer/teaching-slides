---
tags:
  - databases:elasticsearch
  - databases:search
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Search Fundamentals

---
## What This Chapter Covers

- The search API
- Query DSL
- Match vs term
- Bool queries
- Filters vs queries
- Pagination
- Sort

---
## The Search API

```http
POST /products/_search
{
  "query": {
    "match": { "name": "phone" }
  }
}
```

- POST or GET with body
- Returns hits, total, time

---
## Query DSL

- JSON-based query language
- Many query types
- Composable

---
## Match Query

```json
{ "match": { "title": "fast cars" } }
```

- Analysed: tokenises the query
- "fast" or "cars" or both match
- Default for full-text

---
## Term Query

```json
{ "term": { "status.keyword": "active" } }
```

- Exact match; not analysed
- For keyword fields, IDs, exact values

---
## Match Phrase

```json
{ "match_phrase": { "title": "fast cars" } }
```

- Tokens must appear together
- For phrase search

---
## Bool Query

```json
{
  "bool": {
    "must": [{"match": {"title": "phone"}}],
    "filter": [{"term": {"category": "electronics"}}],
    "must_not": [{"term": {"status": "discontinued"}}]
  }
}
```

- Combine multiple clauses

---
## must vs filter

- **must**: scored; affects relevance
- **filter**: not scored; just yes/no
- Filter is faster (cached)
- Use filter for: exact matches, ranges, exists checks

---
## Range Query

```json
{ "range": { "price": { "gte": 10, "lte": 100 } } }
```

- Numeric, date, IP fields

---
## Pagination

- `from`, `size`
- `from + size <= 10000` (default)
- Beyond: search_after (cursor) or scroll
- Don't: deep `from` paging on big indexes

---
## Sort

```json
{ "sort": [{"price": "desc"}, "_score"] }
```

- Multiple fields
- Combine with score

---
## Source Filtering

```json
{ "_source": ["name", "price"] }
```

- Return only specific fields
- Saves bandwidth

---
## Common Search Mistakes

- Term query on analysed text
- Match query on keyword (gets analysed)
- Deep `from` paging
- Querying without filter (slower)
- Sorting on text fields without keyword sub-field
