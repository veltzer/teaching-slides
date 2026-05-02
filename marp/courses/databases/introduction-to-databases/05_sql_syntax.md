---
tags:
  - databases:sql
level: beginner
category: databases
audience:
  - audiences:developers

---
# SQL Syntax

---
## What This Chapter Covers

- SELECT, FROM, WHERE
- ORDER BY, LIMIT
- INSERT, UPDATE, DELETE
- JOINs
- GROUP BY, HAVING
- Subqueries

---
## Statement Categories

![sql_categories](svg/courses/databases/introduction-to-databases/05_sql_syntax/sql_categories.svg)

---
## SELECT

```sql
SELECT name, email FROM users;
SELECT * FROM orders WHERE total > 100;
```

- Pick columns; from where; with conditions

---
## WHERE Clauses

- `=`, `!=`, `<`, `>`, `<=`, `>=`
- `IN`, `NOT IN`, `BETWEEN`
- `LIKE` for pattern; `ILIKE` for case-insensitive (PG)
- `IS NULL` (not `= NULL`!)
- Combine with AND, OR, NOT

---
## ORDER BY, LIMIT

```sql
SELECT * FROM orders ORDER BY total DESC LIMIT 10;
```

- Sort; cap rows

---
## INSERT

```sql
INSERT INTO users (email, name) VALUES ('a@b.com', 'Alice');
INSERT INTO users (email, name) VALUES ('a@b.com', 'A'), ('b@c.com', 'B');
```

---
## UPDATE

```sql
UPDATE users SET name = 'Alice Smith' WHERE id = 1;
```

- Always WHERE!
- Without it: all rows updated

---
## DELETE

```sql
DELETE FROM users WHERE id = 1;
```

- Always WHERE!
- Without it: all rows deleted

---
## INNER JOIN

```sql
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id;
```

- Only matching rows from both

---
## LEFT JOIN

```sql
SELECT u.name, o.total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;
```

- All users; orders if any (NULL if not)

---
## GROUP BY

```sql
SELECT country, COUNT(*) AS users
FROM users
GROUP BY country
ORDER BY users DESC;
```

- Aggregate per group

---
## HAVING

```sql
SELECT country, COUNT(*) AS users
FROM users
GROUP BY country
HAVING COUNT(*) > 100;
```

- Filter on aggregate; after grouping

---
## Subqueries

```sql
SELECT name FROM users
WHERE id IN (SELECT user_id FROM orders WHERE total > 1000);
```

- Query inside a query

---
## Aliases

- AS for columns and tables
- "FROM users u" is shorter than "FROM users users"
- Required for derived tables

---
## DISTINCT

```sql
SELECT DISTINCT country FROM users;
```

- Unique values

---
## Common SQL Mistakes

- `WHERE col = NULL` (always false; use `IS NULL`)
- UPDATE / DELETE without WHERE
- JOIN without ON (cartesian product)
- GROUP BY missing non-aggregated columns
- Mixing case sensitivity (depends on DB)
