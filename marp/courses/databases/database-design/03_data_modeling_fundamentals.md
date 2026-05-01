---
tags:
  - databases:design
  - databases:modeling
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Data Modeling Fundamentals

---
## What This Chapter Covers

- Data types
- Primary keys
- Foreign keys
- Constraints
- Nullability
- Defaults

---
## Choosing Data Types

- Integer types: SMALLINT, INTEGER, BIGINT
- Decimals: NUMERIC, DECIMAL (exact); FLOAT (approximate)
- Strings: CHAR, VARCHAR, TEXT
- Dates: DATE, TIMESTAMP, TIMESTAMPTZ
- Pick the smallest that fits

---
## Primary Keys

- Uniquely identify a row
- Common: integer auto-increment
- Modern: UUIDs (universally unique, no central allocation)
- Composite keys: rare; junction tables

---
## UUID vs Auto-Increment

- UUID: distributed-friendly; larger
- Auto-increment: smaller; sequential
- UUID v7: time-ordered; best of both
- Pick by needs

---
## Foreign Keys

- Reference another table's primary key
- Enforces referential integrity
- ON DELETE: CASCADE, SET NULL, RESTRICT
- ON UPDATE: similar

---
## Constraints

- NOT NULL: required
- UNIQUE: no duplicates
- CHECK: arbitrary expression
- Use them; the database is your validator

---
## Defaults

- DEFAULT clause for columns
- "created_at TIMESTAMPTZ DEFAULT now()"
- Cleaner than app-side defaults
- Same default everywhere

---
## Nullability

- NULL means "unknown" or "not applicable"
- Different from "" or 0
- Choose deliberately
- Default to NOT NULL; opt-in to NULL

---
## Generated Columns

- Computed from other columns
- "full_name AS (first || ' ' || last) STORED"
- Saves recomputation
- Postgres, MySQL support

---
## Sequences

- Postgres: explicit sequences for auto-increment
- Allocate before insert
- Resilient to gaps
- Auto-increment in MySQL is similar idea

---
## Naming Conventions

- snake_case for table and column names
- Avoid reserved words
- Be consistent across the schema
- Document the convention

---
## Common Modeling Mistakes

- Strings for dates
- Float for money
- VARCHAR(255) when 50 would do
- Missing NOT NULL on required fields
- Inconsistent column naming
