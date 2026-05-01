---
tags:
  - databases:duckdb
level: intermediate
category: databases
audience:
  - audiences:developers
  - audiences:data-engineers

---
# Introduction to DuckDB

---
## What This Chapter Covers

- What DuckDB is
- When to use
- When not to use
- Architecture
- Course outline

---
## What DuckDB Is

- Embedded analytical database
- SQLite shape, OLAP focus
- Single-process, in-memory and on-disk
- Free and open

---
## Tagline

- "SQLite for analytics"
- Runs in your process
- No server, no daemon
- Just a library

---
## Why It Exists

- Notebook analytics need fast SQL
- Cloud warehouse for one row is overkill
- Pandas drags on big-ish data
- DuckDB sits in the middle

---
## When To Use

- Notebooks and CLIs
- Local analytics on Parquet or CSV
- Embedded reporting in apps
- Tests and dev environments

---
## When Not To Use

- Multi-user transactional service
- Concurrent writers
- Distributed analytical workloads
- Replication required

---
## Architecture

- One process holds the data
- Vectorized query engine
- Columnar in-memory and on-disk
- Parallel execution per query

---
## Storage Formats

- Native single-file database
- External Parquet
- External CSV, JSON
- Even Arrow buffers in-memory

---
## SQL Support

- Mostly Postgres-flavored
- Window and CTEs
- LATERAL joins
- Many extensions

---
## Extensions

- HTTP and S3
- JSON, regex, full-text
- Spatial, time-series
- Loaded on demand

---
## Language Bindings

- Python, R, Java, Node, Go, Rust
- Same engine across all
- Embedded inside the app
- No driver-server boundary

---
## Pandas And Friends

- Zero-copy via Arrow
- Query Pandas frames as SQL tables
- Combine SQL and DataFrame work
- Speeds many workflows

---
## Course Outline

- Basics
- Working with files
- Performance
- Use cases
- Operations

---
## Common Beginner Mistakes

- Treating it like a server
- Many concurrent writers
- Loading huge tables fully into memory unnecessarily
- Ignoring Parquet partitioning
- Not pinning extension versions
