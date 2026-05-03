---
tags:
  - databases:design
  - databases:physical
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Physical Database Design

---
## What This Chapter Covers

- Indexes
- Partitioning
- Clustering
- Table layout
- Storage parameters

---
## Indexes

- Trade write speed for read speed
- B-tree default
- Hash, GIN, GiST, BRIN for specific cases
- Each adds storage and slows writes

---
## Index Kinds

![index_kinds](svg/courses/databases/database-design/05_physical_database_design/index_kinds.svg)

---
## Index Choice

- B-tree: equality and range queries
- Hash: equality only
- GIN: full-text, JSONB
- BRIN: very large tables, sorted data
- Match to query pattern

---
## Composite Indexes

- Index on multiple columns
- Order matters: (a, b) vs (b, a)
- Best for: WHERE a = ? AND b = ?
- Useful: WHERE a = ?
- Useless: WHERE b = ? alone

---
## Partial Indexes

- Index only rows matching a condition
- "WHERE status = 'active'"
- Smaller; faster
- Postgres feature

---
## Covering Indexes

- Include all columns the query needs
- Avoid the table lookup
- Postgres: INCLUDE clause
- Reads complete from index alone

---
## Partitioning

- Split table into smaller pieces
- By range (date), list (region), hash (ID)
- Query optimiser prunes irrelevant partitions
- Per-partition operations (vacuum, drop)

---
## When To Partition

- Tables &gt; 100M rows
- Queries with date-range or other natural split
- Need to drop old data en masse
- Adds complexity; not free

---
## Clustering

- Physical row order matches index order
- Improves range scan performance
- Postgres: CLUSTER command (one-shot)
- MySQL: clustered primary key (default)

---
## Storage Layouts Compared

![storage_layouts](svg/courses/databases/database-design/05_physical_database_design/storage_layouts.svg)

---
## Storage Parameters

- Fillfactor: leave space for updates
- TOAST (Postgres): big values stored separately
- Compression: per-column or per-table
- Match to workload

---
## Tablespaces

- Distribute tables across storage devices
- Hot tables on SSD; cold on HDD
- Less common with cloud storage
- Useful in on-prem setups

---
## Common Physical Design Mistakes

- No indexes
- Too many indexes
- Wrong index type
- No partitioning on huge tables
- Default settings everywhere
