---
tags:
  - databases:relational
level: beginner
category: databases
audience:
  - audiences:developers

---

# Relational Database Concepts

---

## Tables &amp; Foreign Keys

![relational_concepts](svg/courses/databases/introduction-to-databases/02_relational_database_concepts/relational_concepts.svg)

---

## What This Chapter Covers

- Tables, rows, columns
- Primary keys and foreign keys
- Relationships
- Normalisation basics
- Data types
- Constraints

---

## Tables, Rows, Columns

- Table: like a spreadsheet
- Row: one record
- Column: one attribute
- Each cell: one value (atomic)

---

## Primary Key

- Uniquely identifies a row
- Common: auto-increment integer, UUID
- One per table
- Indexed automatically

---

## Foreign Key

- References another table's primary key
- Establishes relationships
- Enforces referential integrity
- "Order.customer_id REFERENCES Customer.id"

---

## Relationships

- 1:1: one row in A relates to one in B
- 1:N: one A has many B
- M:N: many A relate to many B; needs junction table

---

## Junction Tables

- For M:N relationships
- StudentCourse(student_id, course_id)
- Composite primary key

---

## Normalisation

- Reduce redundancy
- 1NF: atomic values
- 2NF, 3NF: progressively stricter
- Most apps: 3NF is fine

---

## Normal Forms

![normal_forms](svg/courses/databases/introduction-to-databases/02_relational_database_concepts/normal_forms.svg)

---

## Data Types

- Integer: TINYINT, INT, BIGINT
- Decimal: NUMERIC, DECIMAL
- Float: FLOAT, DOUBLE
- String: VARCHAR, TEXT
- Date: DATE, TIMESTAMP

---

## Constraints

- NOT NULL: required
- UNIQUE: no duplicates
- CHECK: arbitrary expression
- DEFAULT: default value
- Database enforces

---

## Indexes

- Speed up queries
- Trade write speed for read speed
- B-tree default
- Per-table: 3-10 typical

---

## Transactions

- Group of operations
- All succeed or all fail
- BEGIN, COMMIT, ROLLBACK

---

## Joins

- Combine rows from multiple tables
- INNER JOIN: only matching
- LEFT JOIN: all from left
- RIGHT JOIN: all from right (rare)
- FULL OUTER JOIN: all from both

---

## Views

- Saved query that looks like a table
- Reusable; abstracts complex queries
- Can be materialised for performance

---

## Common Relational Mistakes

- Storing arrays / lists in one column
- Floats for money
- VARCHAR(255) when shorter would do
- No indexes on foreign keys
- Missing NOT NULL on required fields
