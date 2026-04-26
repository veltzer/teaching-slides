---
tags:
  - concepts:api
  - concepts:performance
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# Pagination, Filtering, Sorting, and Searching

---
## Why Pagination

- Lists grow; full-list responses don't scale
- Server protects itself from runaway queries
- Client gets a manageable chunk
- Required for any list endpoint that could grow

---
## Offset-Based Pagination

- `/orders?offset=20&limit=10`
- Easy to understand
- Works with arbitrary sort orders
- Doesn't require special schema

---
## Offset Problems

- Inefficient at scale: `OFFSET 1000000` skips a million rows
- Inconsistent under writes: rows shift between pages
- The same offset can return different items as data changes
- Fine for small datasets; bad above thousands of rows

---
## Cursor-Based Pagination

- `/orders?cursor=abc123&limit=10`
- The cursor encodes the position in a stable way
- Server hands back the next cursor with each page
- Client doesn't construct cursors; treats them as opaque

---
## Cursor: Pros

- Stable under concurrent writes
- Efficient at any scale
- Works for streaming or infinite scroll
- The default for production APIs

---
## Cursor: Cons

- Can't jump to "page 5" — only sequential
- Cursors are tied to one sort order
- Requires careful schema design (need a sortable, unique key)

---
## Keyset Pagination

- A specific cursor implementation
- The cursor is a value from the sort key (often timestamp + id)
- "Give me orders created before 2026-01-15T10:00 with id < 100"
- Performant, stable, simple

---
## Keyset Example

```
GET /orders?cursor=created_at:2026-01-15T10:00:00,id:100&limit=20

Response:
{
  "items": [...],
  "next_cursor": "created_at:2026-01-14T15:30:00,id:42"
}
```

---
## Filtering

- Query parameters become filters: `?status=pending&customer_id=c1`
- Multiple values: `?status=pending,shipped` or repeat the param
- Operators: rare in REST; common in query languages
- Keep simple cases simple; reach for query languages only when needed

---
## Filtering Conventions

- `?status=pending` — exact match
- `?created_after=2026-01-01` — range
- `?total_min=100&total_max=500` — bounded range
- Document each filter; don't expose every database column

---
## Sorting

- `?sort=created_at` — ascending
- `?sort=-created_at` or `?sort=created_at&order=desc` — descending
- Multiple keys: `?sort=status,-created_at`
- Document which fields are sortable

---
## Searching

- Free-text search: `?q=red+shoes`
- Backed by a search engine (Elasticsearch, OpenSearch, Algolia)
- Different from filtering — "approximate match" vs "exact match"
- Returns ranked results

---
## Search vs Filter

- Filter: structured, exact, predictable
- Search: ranked, fuzzy, recall-oriented
- Use both: search to find candidates, filter to narrow them
- `/products/search?q=shoes&filter=in_stock`

---
## Field Selection (Sparse Fieldsets)

- Client requests only the fields it needs
- `?fields=id,name,total`
- Reduces response size significantly for large objects
- Enable when responses are large; don't bother for tiny resources

---
## Combining Concerns

- `/orders?status=pending&sort=-created_at&cursor=abc&limit=20&fields=id,total`
- Each parameter does one thing
- The combination is composable
- Document each separately; the combinations are obvious

---
## Anti-Patterns

- No pagination at all on a growing collection
- Returning page count as `total_pages` (forces a count query, slow at scale)
- Magic field selection ("if you pass `verbose=true` you get more")
- Inventing a custom query language (use SQL or a known DSL if needed)

---
## Summary

- Cursor-based pagination is the safe default
- Offset is fine for small, static lists
- Filters are structured; search is fuzzy
- Document every query parameter
- Compose, don't conflate
