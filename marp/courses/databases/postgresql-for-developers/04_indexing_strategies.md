---
tags:
  - databases:postgresql
  - databases:indexes
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Indexing Strategies

---
## What This Chapter Covers

- Index types in Postgres
- B-tree, hash, GIN, GiST, BRIN
- Composite indexes
- Partial indexes
- Covering indexes (INCLUDE)
- Maintenance

---
## B-Tree

- Default
- Equality and range
- Order-preserving
- 95% of indexes are B-tree

---
## Hash

- Equality only
- Smaller than B-tree
- Postgres 10+: WAL-logged (safe)
- Rare benefit over B-tree

---
## GIN

- Generalised Inverted Index
- For: arrays, JSONB, full-text
- Slower writes; fast reads
- Standard for tsvector, JSONB

---
## GiST

- Generalised Search Tree
- For: geometry, ranges, full-text
- Less precise than GIN; smaller
- PostGIS uses extensively

---
## BRIN

- Block Range Index
- Tiny; good for huge tables with sorted data
- Time-series / log tables
- Trade-off: less precise

---
## Composite Indexes

- Multiple columns: (a, b, c)
- Used by: WHERE a=?, WHERE a=? AND b=?, WHERE a=? AND b=? AND c=?
- Not used by: WHERE b=? alone
- Order matters

---
## Partial Indexes

```sql
CREATE INDEX idx_active ON users (email) WHERE active = true;
```

- Index a subset
- Smaller; faster
- Only for queries matching the WHERE

---
## Covering Indexes (INCLUDE)

```sql
CREATE INDEX idx_user_email ON users (email) INCLUDE (name);
```

- Index includes extra columns
- Index-only scan possible
- No table lookup

---
## Expression Indexes

```sql
CREATE INDEX idx_lower_email ON users (LOWER(email));
```

- Index a computed expression
- Useful for case-insensitive search
- Query must use same expression

---
## Unique Indexes

- Enforce uniqueness
- Implicit for primary keys
- Combined with partial: "unique among non-deleted rows"

---
## Index Maintenance

- Vacuum keeps indexes healthy
- REINDEX for bloat
- Periodic check: pg_stat_user_indexes
- Drop unused indexes

---
## Concurrent Index Creation

```sql
CREATE INDEX CONCURRENTLY idx_foo ON bar (baz);
```

- Doesn't block writes
- Slower; use in production
- Standard practice

---
## Common Index Mistakes

- Indexing every column
- Wrong column order in composite
- No index on FK columns
- Indexes never used (waste of space and write speed)
- Not using EXPLAIN to verify
