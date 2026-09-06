---
tags:
  - databases:mongodb
level: intermediate
category: databases
audience:
  - audiences:developers

---

# Advanced Querying

---

## What This Chapter Covers

- Array queries
- Nested document queries
- Geospatial
- Text search
- $elemMatch
- Cursor methods

---

## Operator Categories

![query_operators](svg/courses/databases/mongodb-for-developers/06_advanced_querying/query_operators.svg)

---

## Operator Categories Detail

![operator_categories](svg/courses/databases/mongodb-for-developers/06_advanced_querying/operator_categories.svg)

---

## Array Queries

```python
db.users.find({"tags": "vip"})  # contains "vip"
db.users.find({"tags": {"$all": ["vip", "premium"]}})
db.users.find({"tags": {"$size": 3}})
```

- Equality: any element matches
- $all: all elements present
- $size: exact length

---

## $elemMatch

```python
db.users.find({
    "addresses": {"$elemMatch": {"city": "NYC", "type": "home"}}
})
```

- Match array elements where multiple conditions on same element
- Without it: conditions can match different elements

---

## Nested Document Queries

```python
db.users.find({"address.city": "NYC"})
```

- Dot notation for nested fields
- Works for filtering and sorting

---

## Geospatial

```python
db.places.create_index([("location", "2dsphere")])
db.places.find({
    "location": {
        "$near": {
            "$geometry": {"type": "Point", "coordinates": [-73.9, 40.7]},
            "$maxDistance": 1000
        }
    }
})
```

- 2dsphere index for true earth coords
- $near, $within, $intersects

---

## Text Search

```python
db.articles.create_index([("title", "text"), ("body", "text")])
db.articles.find({"$text": {"$search": "mongodb tutorial"}})
```

- Full-text search; basic stemming
- Per-collection: one text index
- For richer search: Elasticsearch

---

## Cursor Methods

- `.sort({"name": 1})`: ascending
- `.limit(10)`: first 10
- `.skip(20)`: skip first 20
- `.count_documents()`: total count
- Combine: paginated query

---

## Pagination

- Skip-based: `find().skip(20).limit(10)` — slow at depth
- Cursor-based: use `_id > last_id` for next page
- `_id` is well-indexed; cursor pagination is fast

---

## $regex

```python
db.users.find({"name": {"$regex": "^A", "$options": "i"}})
```

- Pattern match
- Case-insensitive with `i`
- Anchored with `^`: index-friendly
- Unanchored: full collection scan

---

## $expr

```python
db.orders.find({
    "$expr": {"$gt": ["$total", "$cost"]}
})
```

- Compare two fields in same document
- Aggregation expressions in find

---

## Distinct

```python
db.users.distinct("country")
```

- Unique values for a field
- Works with index on the field

---

## Count

```python
db.users.count_documents({"active": True})
db.users.estimated_document_count()
```

- Count: precise, slower
- Estimated: fast, may be slightly off (uses metadata)

---

## Explain

```python
db.users.find({"email": "a@b.com"}).explain("executionStats")
```

- Shows query plan
- Like SQL EXPLAIN
- Reveals: index used, docs examined, time

---

## Common Query Mistakes

- Unanchored $regex (full scan)
- No index on text-search field
- Skip-based pagination on big collections
- Distinct without index (slow)
- Forgetting $elemMatch for array conditions
