---
tags:
  - databases:basics
level: beginner
category: databases
audience:
  - audiences:developers

---
# What Are Databases?

---
## What This Chapter Covers

- What a database is
- Why we use them
- Types: SQL, NoSQL
- File-based vs server-based
- A short tour

---
## What A Database Is

- A structured way to store and retrieve data
- Persistent (survives restart)
- Concurrent access
- Queryable
- Versus: ad-hoc files

---
## Major Database Kinds

![db_kinds](svg/courses/databases/introduction-to-databases/01_what_are_databases/db_kinds.svg)

---
## Why Databases

- Persistence beyond memory
- Multiple users at once
- Querying without writing data-handling code
- Integrity constraints
- Backup and recovery
- The standard for non-trivial apps

---
## SQL vs NoSQL

- SQL: relational, schema-on-write
- NoSQL: many models (document, key-value, wide-column, graph)
- SQL: best for relations
- NoSQL: best for specific access patterns
- Most apps: SQL is enough

---
## File-Based

- SQLite: a database in one file
- Great for: dev, embedded, mobile
- Not for: many concurrent writers
- Surprisingly capable

---
## Server-Based

- Postgres, MySQL, MongoDB, etc.
- Process running; clients connect
- Concurrent reads and writes
- Standard for production

---
## ACID

- **A**tomicity: all or nothing
- **C**onsistency: invariants hold
- **I**solation: concurrent txns don't see partial state
- **D**urability: committed data survives crash
- Relational DBs: full ACID

---
## CAP

- For distributed systems
- Consistency, Availability, Partition tolerance
- Pick two
- Mostly: CP or AP

---
## Storage Models

- Relational: tables, rows, columns
- Document: JSON-like docs
- Key-Value: simple lookup
- Wide-Column: tables with sparse columns
- Graph: nodes and edges

---
## Use Cases

- Transactional: banking, e-commerce
- Analytical: reporting, BI
- Search: full-text, faceting
- Time-series: metrics, logs
- Different DBs for different needs

---
## Vocabulary

- Schema: structure of the data
- Index: fast lookup data structure
- Query: a request for data
- Transaction: atomic group of operations

---
## Common DB Misconceptions

- "All databases are the same" — wildly different in trade-offs
- "NoSQL means no SQL" — most NoSQL has query languages
- "Schemaless = no schema" — your app has one
- "MongoDB is faster than Postgres" — depends entirely on the workload

---
## What's Next

- Relational concepts
- Schemas and migrations
- SQL basics
- MySQL and MongoDB
- ORMs
- Choosing the right database
