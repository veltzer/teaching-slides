---
tags:
  - databases:duckdb
level: intermediate
category: databases
audience:
  - audiences:developers
  - audiences:data-engineers

---
# Basics

---
## What This Chapter Covers

- Connections
- Tables and types
- DML
- Views
- Transactions

---
## Opening A Database

- In-memory: empty connection
- File-based: pass a path
- Read-only mode for safety
- Close releases resources

---
## Connection Lifecycle

![connection_lifecycle](svg/courses/databases/duckdb/02_basics/connection_lifecycle.svg)

---
## Tables

- CREATE TABLE like SQL
- Most types familiar
- LIST and STRUCT for nested
- MAP for key-value

---
## Types

- Integers, floats, decimals
- VARCHAR, BLOB
- DATE, TIME, TIMESTAMP
- BOOLEAN, UUID

---
## Inserts

- INSERT INTO ... VALUES
- INSERT INTO ... SELECT
- COPY for bulk load
- Bulk is much faster

---
## Updates and Deletes

- Standard SQL
- Slower than inserts
- Avoid heavy update workloads
- DuckDB is OLAP-flavored

---
## Views

- Logical query stored under a name
- Materialized via temp tables when needed
- Useful for layered analytics
- Cheap to create

---
## Common Table Expressions

- WITH clause
- Recursive supported
- Improve readability
- Same engine optimizes

---
## Window Functions

- OVER clauses
- Partition by, order by
- Many built-in aggregates
- Replace many self-joins

---
## Joins

- All standard join types
- Hash and merge joins
- Engine picks
- Hints rarely needed

---
## Transactions

- BEGIN, COMMIT, ROLLBACK
- ACID for the local file
- Writers serialized
- Read-only allows concurrency

---
## Configuration

- PRAGMA settings
- Memory limits
- Threads
- Storage format options

---
## Importing CSV

- COPY FROM 'file.csv'
- Auto type detect
- Header read
- Override types as needed

---
## Common Basics Mistakes

- Auto type detect for production loads
- Using INSERT row-by-row
- Skipping memory limit
- One thread by default
- Ignoring read-only mode
