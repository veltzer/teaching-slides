---
tags:
  - databases:postgresql
  - databases:sql
level: intermediate
category: databases
audience:
  - audiences:developers

---

# Window Functions

---

## Windows vs GROUP BY

![window_basics](svg/courses/databases/postgresql-for-developers/03_window_functions/window_basics.svg)

---

## Common Window Functions

![window_functions_overview](svg/courses/databases/postgresql-for-developers/03_window_functions/window_functions_overview.svg)

---

## What This Chapter Covers

- What window functions are
- OVER, PARTITION BY, ORDER BY
- Common functions: ROW_NUMBER, RANK, LAG, LEAD
- Aggregates as window functions
- Frames

---

## What Window Functions Are

- Compute across a set of rows without collapsing
- Like aggregates, but each row stays
- Game-changing for analytics

---

## OVER Clause

```sql
SELECT
    name,
    salary,
    RANK() OVER (ORDER BY salary DESC) AS rank
FROM employees;
```

- Defines the window
- ORDER BY: sequence within window
- PARTITION BY: split into groups

---

## PARTITION BY

```sql
SELECT
    department,
    name,
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank
FROM employees;
```

- Reset the function per partition
- "Rank within department"

---

## Common Functions

- `ROW_NUMBER()`: unique sequence
- `RANK()`: ties get same rank; gaps after
- `DENSE_RANK()`: ties get same rank; no gaps
- `LAG(col, n)`: previous row
- `LEAD(col, n)`: next row

---

## LAG and LEAD

```sql
SELECT
    date,
    revenue,
    revenue - LAG(revenue) OVER (ORDER BY date) AS daily_change
FROM daily_revenue;
```

- Compare with previous row
- Day-over-day metrics

---

## Aggregates As Window

```sql
SELECT
    name,
    salary,
    AVG(salary) OVER (PARTITION BY department) AS dept_avg
FROM employees;
```

- SUM, AVG, COUNT, MIN, MAX
- All work as window functions

---

## Running Totals

```sql
SELECT
    date,
    daily,
    SUM(daily) OVER (ORDER BY date) AS running_total
FROM sales;
```

- Cumulative sum
- Common in financial / activity analysis

---

## Frames

- "ROWS BETWEEN n PRECEDING AND m FOLLOWING"
- Restrict the window
- Defaults: depends on ORDER BY presence
- Be explicit when needed

---

## Moving Average

```sql
SELECT
    date,
    revenue,
    AVG(revenue) OVER (
        ORDER BY date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS week_avg
FROM daily;
```

- 7-day moving average
- Smooths noisy data

---

## Top N Per Group

```sql
WITH ranked AS (
    SELECT *,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY price DESC) AS rn
    FROM products
)
SELECT * FROM ranked WHERE rn <= 3;
```

- Top 3 products per category

---

## Performance

- Windows can be expensive (sort + scan)
- Indexes on ORDER BY columns help
- EXPLAIN ANALYZE to verify

---

## Common Window Mistakes

- Forgetting PARTITION BY (one big window)
- Missing ORDER BY for ranking functions
- Wrong frame default (RANGE vs ROWS)
- Using subqueries when a window would be cleaner
