---
tags:
  - databases:mongodb
  - databases:indexes
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Indexing for Developers

---
## What This Chapter Covers

- Index types in MongoDB
- Single-field, compound, multi-key
- Text and geo
- TTL indexes
- Choosing the order
- Maintenance

---
## Index Types

![index_types](svg/courses/databases/mongodb-for-developers/08_indexing_for_developers/index_types.svg)

---
## Single-Field Index

```javascript
db.users.createIndex({ email: 1 });
```

- Most basic
- 1 = ascending; -1 = descending (rarely matters)

---
## Compound Index

```javascript
db.orders.createIndex({ customer_id: 1, created_at: -1 });
```

- Index on multiple fields
- Order matters
- ESR rule: Equality, Sort, Range

---
## ESR Rule

- Equality fields first
- Sort fields next
- Range fields last
- "find email = X, sort by date desc" &#8594; (email, date)

---
## Multi-Key Index

- Index over array fields
- Each element gets its own index entry
- "tags": ["a","b","c"] &#8594; 3 entries
- Watch: cardinality

---
## Text Index

```javascript
db.articles.createIndex({ title: "text", body: "text" });
```

- One per collection
- Multiple fields supported
- `$text` queries use it

---
## Geospatial Index

- 2dsphere for true earth coords
- 2d for plane coordinates
- Required for $near, $within
- Standard for location-based queries

---
## TTL Index

```javascript
db.sessions.createIndex({ expiresAt: 1 }, { expireAfterSeconds: 0 });
```

- Auto-delete documents past their TTL
- Useful: sessions, OTPs, ephemeral data
- Background cleanup

---
## Hashed Index

- For sharding by hash
- Even data distribution
- Doesn't support range queries

---
## Wildcard Index

```javascript
db.events.createIndex({ "$**": 1 });
```

- Indexes all fields
- Useful for: heterogeneous documents
- Bigger than targeted indexes

---
## Index Hints

```javascript
db.users.find({...}).hint({ email: 1 });
```

- Force a specific index
- Use when planner picks wrong
- Last resort

---
## Index Build

- Foreground: blocks the collection (avoid in prod)
- Background (default in modern Mongo): non-blocking
- Long for big collections; show progress

---
## Index Stats

```javascript
db.users.aggregate([{ $indexStats: {} }]);
```

- Per-index usage stats
- Drop unused indexes
- Heavy ops on writes

---
## Index Cardinality

- Low cardinality: few unique values; index less useful
- High cardinality: many unique; index very effective
- "is_active boolean" &#8594; low; "user_id" &#8594; high

---
## Common Index Mistakes

- Indexing every field
- Wrong order in compound index (ignoring ESR)
- Multiple text indexes (only one allowed)
- TTL on the wrong field
- Dropping unused indexes never; bloat
