---
tags:
  - databases:postgresql
  - databases:sql
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Advanced SQL Techniques

---
## UPSERT and RETURNING

![upsert_returning](svg/courses/databases/postgresql-for-developers/02_advanced_sql_techniques/upsert_returning.svg)

---
## What This Chapter Covers

- CTEs and recursive queries
- Lateral joins
- Window functions overview
- DISTINCT ON
- UPSERT
- Returning clauses

---
## CTE and Window at a Glance

![cte_window](svg/courses/databases/postgresql-for-developers/02_advanced_sql_techniques/cte_window.svg)

---
## CTEs

```sql
WITH active AS (
    SELECT * FROM users WHERE status = 'active'
)
SELECT * FROM active WHERE created_at > '2026-01-01';
```

- Named subquery
- Readable; chained CTEs build complex queries
- Modern Postgres: CTEs can be inlined

---
## Recursive CTEs

```sql
WITH RECURSIVE tree AS (
    SELECT id, parent_id, 1 AS depth FROM nodes WHERE parent_id IS NULL
    UNION ALL
    SELECT n.id, n.parent_id, t.depth + 1
    FROM nodes n JOIN tree t ON n.parent_id = t.id
)
SELECT * FROM tree;
```

- Tree / graph traversal
- Hierarchies, dependency chains

---
## Lateral Joins

```sql
SELECT u.id, recent.title
FROM users u
LEFT JOIN LATERAL (
    SELECT title FROM posts p
    WHERE p.user_id = u.id
    ORDER BY p.created_at DESC LIMIT 1
) recent ON true;
```

- Inner subquery references outer
- "For each user, top post"

---
## DISTINCT ON

```sql
SELECT DISTINCT ON (user_id) user_id, created_at, status
FROM events
ORDER BY user_id, created_at DESC;
```

- Postgres-specific
- "First per group" cleanly
- Faster than window-function alternatives

---
## UPSERT

```sql
INSERT INTO users (email, name) VALUES ('a@b.com', 'Alice')
ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name;
```

- Insert or update
- Atomic
- The right way to "upsert"

---
## RETURNING

```sql
INSERT INTO orders (...) VALUES (...) RETURNING id, created_at;
UPDATE orders SET status = 'shipped' WHERE id = 1 RETURNING *;
DELETE FROM orders WHERE id = 1 RETURNING *;
```

- Get the changed rows back
- Saves a separate SELECT
- Postgres-specific

---
## Subqueries

- Scalar: returns one value
- Row: returns one row
- Table: returns many rows
- IN, EXISTS, NOT EXISTS

---
## EXISTS vs IN

- `WHERE id IN (SELECT id FROM ...)`
- `WHERE EXISTS (SELECT 1 FROM ... WHERE ...)`
- Often equivalent; planner picks
- EXISTS slightly clearer for correlated subqueries

---
## Aggregations

- GROUP BY ... HAVING
- FILTER (WHERE ...) within aggregate
- "COUNT(*) FILTER (WHERE active)"
- More expressive than CASE WHEN

---
## Set Operations

- UNION, INTERSECT, EXCEPT
- ALL: keep duplicates
- Useful for: comparing two queries

---
## CASE Expressions

```sql
SELECT
    name,
    CASE
        WHEN age < 18 THEN 'minor'
        WHEN age < 65 THEN 'adult'
        ELSE 'senior'
    END AS age_group
FROM users;
```

- Conditional logic in queries

---
## Common SQL Mistakes

- Forgetting to filter NULL (`= NULL` doesn't work)
- DISTINCT vs GROUP BY confusion
- N+1 queries that could be one JOIN
- Not using RETURNING (extra round trip)
- CTEs everywhere when subqueries would do
