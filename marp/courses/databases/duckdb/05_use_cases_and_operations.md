---
tags:
  - databases:duckdb
level: intermediate
category: databases
audience:
  - audiences:developers
  - audiences:data-engineers

---
# Use Cases and Operations

---
## What This Chapter Covers

- Notebook analytics
- Embedded reporting
- ETL on a laptop
- Tests
- Operational notes

---
## Notebook Analytics

- Replace heavy DataFrame work
- Run SQL directly in Python or R
- Mix DataFrames and SQL
- Faster than loading into memory

---
## Embedded Reporting

- Ship DuckDB in your application
- Run reports without server
- Read user data files
- Useful for desktop and CLI tools

---
## ETL On A Laptop

- Read CSV or JSON
- Transform with SQL
- Write Parquet
- Many real workflows fit in one process

---
## Tests

- Replace Postgres in unit tests
- Faster startup
- Isolated per test
- Use Postgres for integration where flavor matters

---
## Lakehouse Querying

- Read open table formats
- Query without warehouse compute
- Useful for ad-hoc exploration
- Combine with Python tooling

---
## Concurrent Access

- One writer at a time
- Many readers in read-only mode
- File lock arbitrates
- Not a multi-user server

---
## Backups

- Copy the database file
- Quiesce writes first
- Use VACUUM before for compaction
- Or rely on Parquet snapshots

---
## Versioning

- Pin DuckDB version in dependencies
- Native format may evolve
- Test upgrade in lower env
- Read release notes

---
## Extensions

- Loaded per-session
- Some download on first use
- Pin version for reproducibility
- Watch for network access in extensions

---
## Security

- Library inside your process
- No network surface by default
- Be careful with HTTP and S3 extensions
- Manage credentials cleanly

---
## Limits

- Single host scale
- One writer
- No replication
- No multi-tenant isolation

---
## Mixing With Bigger Systems

- Pull subsets from a warehouse
- Process locally
- Push back results
- Saves cost

---
## Embedding Tips

- Reuse connections
- Set memory limit
- Use prepared statements where applicable
- Catch errors per query

---
## Common Use-Case Mistakes

- Treating it as a server
- One global mutable database in concurrent code
- No memory limit
- Ignoring partitioning when reading from object storage
- Pinning to old version forever
