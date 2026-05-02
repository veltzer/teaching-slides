---
tags:
  - databases:postgresql
level: intermediate
category: databases
audience:
  - audiences:developers

---
# PostgreSQL Architecture and Internals

---
## What This Chapter Covers

- Process architecture
- Storage layout
- WAL and durability
- MVCC
- Background workers
- A high-level mental model

---
## Process Model

- One process per connection (postmaster forks)
- Background processes: writer, checkpointer, autovacuum, WAL writer, archiver
- Shared memory across all
- Each connection: separate Linux process

---
## Process Architecture

![postgres_processes](svg/courses/databases/postgresql-for-developers/01_postgresql_architecture_and_internals/postgres_processes.svg)

---
## Storage Layout

- Database = directory
- Table = files (8KB pages)
- Each row in a page
- TOAST: large values stored separately

---
## Pages

- 8KB blocks
- Tuples (rows) packed in
- Free space map; visibility map
- The fundamental unit of I/O

---
## WAL (Write-Ahead Log)

- Every change logged to WAL first
- Then applied to data files
- Recovery: replay WAL from last checkpoint
- Foundation of durability

---
## Checkpoints

- Periodic flush of dirty pages to disk
- Limits WAL replay on recovery
- Tunable: checkpoint_timeout, max_wal_size
- Trade-off: I/O spike vs recovery time

---
## MVCC

- Multi-Version Concurrency Control
- Each transaction sees a snapshot
- Updates create new row versions
- Old versions kept until no transaction needs them
- Vacuum cleans up

---
## VACUUM

- Reclaims space from dead tuples
- Updates statistics for the planner
- Autovacuum runs in background
- Manual VACUUM for special cases

---
## Background Workers

- Logical replication
- Parallel query workers
- Custom extensions
- Configurable count

---
## Buffers

- shared_buffers: cache
- work_mem: per-operation
- maintenance_work_mem: VACUUM, CREATE INDEX
- Tune for workload

---
## Replication

- Streaming: WAL streamed to replicas
- Logical: row-level changes; cross-version compatible
- Physical: byte-for-byte replica
- Read replicas: read-only physical replicas

---
## Common Misconceptions

- "Postgres is single-threaded": wrong (one process per connection; parallel query exists)
- "Vacuum is optional": no; without it, table bloat
- "MVCC means no locks": wrong; row locks for writes
- "WAL is just for recovery": also for replication, audit
