---
tags:
  - data-and-ai:data-engineering
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers
  - audiences:architects

---
# Storage and File Formats

---
## What This Chapter Covers

- Object storage basics
- Row vs columnar
- File formats
- Compression
- Layout

---
## Object Storage Model

- Buckets and objects
- Flat namespace
- HTTP API
- Strong durability, eventual list

---
## Why It Wins

- Cheap per byte
- Scales without ops
- Multi-region replicas
- Decoupled from compute

---
## Row vs Column

- Row: write-friendly
- Column: read-friendly for analytics
- Lakehouse uses columnar
- Queries scan only needed columns

---
## Columnar Formats

- Parquet
- ORC
- Both open
- Both widely supported

---
## Parquet

- Default in lakehouse
- Row groups
- Column chunks
- Page-level compression

---
## ORC

- Origin in Hive ecosystem
- Strong predicate pushdown
- Less universal support
- Still in use

---
## Avro

- Row-oriented
- Good for streaming
- Schema embedded
- Used at the edge

---
## Compression

- Snappy: fast, average ratio
- Zstd: balanced
- Gzip: high ratio, slow
- Lz4: fastest

---
## File Size

- Small files are an anti-pattern
- Listing cost dominates
- Aim for hundreds of MB
- Compaction is a maintenance task

---
## Partitioning

- Folder-based by date or region
- Limits scan
- Too many partitions hurt
- Tune to query patterns

---
## Clustering and Sort

- Co-locate values within files
- Helps skipping unread data
- Less rigid than partitioning
- Modern table formats handle it

---
## Schema Encoding

- Field types
- Nullability
- Nested structs and lists
- Match producer language types

---
## Common Format Mistakes

- Many small files
- Wrong compression for workload
- Over-partitioning
- No clustering
- Mixing formats per table
