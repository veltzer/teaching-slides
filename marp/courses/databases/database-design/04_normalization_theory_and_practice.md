---
tags:
  - databases:design
  - databases:normalization
level: intermediate
category: databases
audience:
  - audiences:developers

---

# Normalisation: Theory and Practice

---

## What This Chapter Covers

- Why normalise
- 1NF, 2NF, 3NF, BCNF
- Anomalies they prevent
- When to denormalise
- Practical guidance

---

## Normal Forms

![normalization_forms](svg/courses/databases/database-design/04_normalization_theory_and_practice/normalization_forms.svg)

---

## Why Normalise

- Eliminate redundancy
- Avoid update anomalies
- Reduce storage
- Simplify queries (sometimes)

---

## 1NF: Atomic Values

- Each cell holds one value
- No arrays, no comma-separated lists
- "tags = 'red,green,blue'" violates 1NF
- Move to a separate table

---

## 2NF: Full Functional Dependency

- Every non-key column depends on the *whole* primary key
- Composite key: each non-key column depends on all parts
- Fix: split tables

---

## 3NF: No Transitive Dependencies

- Non-key columns don't depend on other non-key columns
- "user_id, dept_id, dept_name": dept_name &#8594; dept (split out)
- Fix: extract

---

## BCNF

- Stronger than 3NF
- Every determinant is a candidate key
- Rare in practice
- 3NF is usually enough

---

## Update Anomalies

- Update a value in one place; missed in another
- Insert anomaly: can't add data without related data
- Delete anomaly: lose data when removing related
- Normalisation prevents these

---

## Denormalisation

- Add redundancy back
- For read performance
- Common: counters, summaries, audit fields
- Trade-off: query speed vs update complexity

---

## When To Denormalise

- Read-heavy workload
- Joins are too slow
- Counter columns (likes, views)
- Reporting tables alongside transactional

---

## Denormalisation Trade-offs

![denormalization_tradeoffs](svg/courses/databases/database-design/04_normalization_theory_and_practice/denormalization_tradeoffs.svg)

---

## Hybrid Approach

- Normalise transactional tables
- Denormalise reporting tables
- Keep them in sync via triggers, ETL, CDC
- Best of both

---

## A Practical Example

- Order: order_id, customer_id, total
- OrderLine: line_id, order_id, product_id, quantity, price
- Both normalised; total denormalised (sum of lines)

---

## Common Normalisation Mistakes

- Extreme normalisation that hurts queries
- No normalisation; redundancy everywhere
- Denormalising before measuring
- Inconsistent denormalised data (sync issues)
