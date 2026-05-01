---
tags:
  - data-and-ai:sql
  - languages:sql
level: beginner
category: data-science
audience:
  - audiences:data-analysts

---
# SQL for Analysts

---
## What This Chapter Covers

- Relational database basics
- SELECT, WHERE, ORDER BY
- JOINs and subqueries
- GROUP BY and aggregation
- Window functions for analysis
- Common Table Expressions (CTEs)
- Writing efficient queries

---
## Relational Basics

- Data lives in **tables** (rows + columns)
- Each row = one record; each column = one attribute
- Tables relate via *keys* (one table's primary key = another's foreign key)
- SQL = the language to query and manipulate
- Most warehouses speak SQL — learn it once, use it everywhere

---
## SELECT, WHERE

```sql
SELECT customer_id, order_total
FROM orders
WHERE order_date >= '2026-01-01'
  AND status = 'completed'
ORDER BY order_total DESC
LIMIT 10;
```

- `SELECT`: which columns to return
- `WHERE`: which rows to include
- `ORDER BY`: how to sort
- `LIMIT`: how many to return
- The first SQL most analysts learn — and the most-used

---
## Filtering Patterns

```sql
WHERE country IN ('US', 'CA', 'UK')
WHERE name LIKE 'A%'              -- starts with A
WHERE created_at IS NULL          -- missing
WHERE age BETWEEN 18 AND 30
WHERE NOT (status = 'archived')
```

- Combine with `AND`, `OR`, `NOT`
- `IN` for sets; `LIKE` for patterns
- `IS NULL` (not `= NULL`) for missing values
- Complex filters benefit from CTEs

---
## JOINs

```sql
SELECT o.id, c.name, o.total
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
WHERE o.status = 'completed';
```

- **INNER JOIN**: only matching rows from both
- **LEFT JOIN**: all rows from left, matching from right (NULL if none)
- **RIGHT JOIN**: rare; same as LEFT with operands swapped
- **FULL OUTER JOIN**: all rows from both
- Pick by which side's missing data matters

---
## When To Use Which JOIN

- Customers with orders (only matched) &#8594; INNER
- All customers, with their order counts (zero if none) &#8594; LEFT
- All orders, with customer info if available &#8594; LEFT (orders is left)
- A diagram on paper before writing the JOIN saves bugs

---
## Subqueries

```sql
SELECT name FROM customers
WHERE id IN (SELECT customer_id
             FROM orders
             WHERE total > 1000);
```

- A query inside a query
- Often replaceable with a JOIN — sometimes clearer, sometimes not
- Correlated subqueries (referencing the outer query) can be slow
- Database optimisers usually handle them well; profile if in doubt

---
## Aggregation

```sql
SELECT country, COUNT(*) AS users, AVG(age) AS avg_age
FROM customers
GROUP BY country
HAVING COUNT(*) > 100
ORDER BY users DESC;
```

- `GROUP BY`: split rows into groups
- Aggregate functions: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`
- `HAVING`: filter on aggregates (after grouping)
- `WHERE` filters rows before grouping; `HAVING` filters groups after

---
## Distinct vs Group By

```sql
SELECT DISTINCT country FROM customers;
-- equivalent to:
SELECT country FROM customers GROUP BY country;
```

- Both deduplicate
- `GROUP BY` is more flexible — can attach aggregates
- `DISTINCT` is shorter when you just want unique values

---
## Window Functions

```sql
SELECT
    order_id, customer_id, order_total,
    ROW_NUMBER() OVER (PARTITION BY customer_id
                       ORDER BY order_total DESC) AS rank_in_customer
FROM orders;
```

- Compute aggregates *without* collapsing rows
- Useful for: rank within group, running totals, moving averages
- `PARTITION BY` defines the group; `ORDER BY` defines the sequence
- The analyst's secret weapon — learn these well

---
## Useful Window Functions

- `ROW_NUMBER()`: rank with no ties
- `RANK()`: rank with gaps after ties
- `DENSE_RANK()`: rank with no gaps after ties
- `LAG()` / `LEAD()`: previous / next row's value
- `SUM() OVER (...)` / `AVG() OVER (...)`: running aggregates

---
## Running Totals Example

```sql
SELECT
    order_date,
    daily_total,
    SUM(daily_total) OVER (ORDER BY order_date) AS running_total
FROM (SELECT order_date, SUM(total) AS daily_total
      FROM orders GROUP BY order_date) d;
```

- Window function turns a daily-total query into a running-total chart
- No external code needed; pure SQL
- Great for cumulative metrics: revenue YTD, signups to date

---
## Common Table Expressions (CTEs)

```sql
WITH high_value AS (
    SELECT customer_id FROM orders
    GROUP BY customer_id HAVING SUM(total) > 5000
)
SELECT c.* FROM customers c
INNER JOIN high_value h ON c.id = h.customer_id;
```

- Named subquery, defined at the top of the statement
- Makes complex queries readable
- Multiple CTEs in one query (chained with commas)
- Most modern warehouses support recursive CTEs too

---
## CTEs Are Better Than Nested Subqueries

```sql
-- Nested (hard to read)
SELECT * FROM (SELECT * FROM (SELECT ...)) AS x;

-- CTEs (clear)
WITH a AS (SELECT ...),
     b AS (SELECT ... FROM a),
     c AS (SELECT ... FROM b)
SELECT * FROM c;
```

- Each step has a name and a clear purpose
- Easier to debug — comment out one CTE at a time

---
## Writing Efficient Queries

- Filter early (`WHERE` before `JOIN` if possible)
- Avoid `SELECT *` in production queries
- Use indexes (the warehouse layer) — partition columns, clustering
- Prefer JOINs over correlated subqueries
- Run `EXPLAIN` to see what the optimiser is doing

---
## Common Mistakes

- Comparing with `= NULL` instead of `IS NULL`
- Using INNER JOIN when LEFT JOIN was needed (silently dropping rows)
- Aggregating without `GROUP BY` (works in some dialects with weird results)
- Not aliasing tables &#8594; ambiguous column references
- Trusting the first query you write — always sanity-check counts
