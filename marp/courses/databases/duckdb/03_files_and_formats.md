---
tags:
  - databases:duckdb
level: intermediate
category: databases
audience:
  - audiences:developers
  - audiences:data-engineers

---

# Files and Formats

---

## What This Chapter Covers

- Reading Parquet
- Reading CSV and JSON
- Writing files
- Globs and partitions
- Remote files

---

## Why Files

- Most analytics data lives as files
- Parquet is the standard
- DuckDB queries them in place
- No import step needed

---

## File Sources

![file_sources](svg/courses/databases/duckdb/03_files_and_formats/file_sources.svg)

---

## Reading Parquet

- read_parquet('file.parquet')
- Or just SELECT * FROM 'file.parquet'
- Predicate pushdown supported
- Column pruning supported

---

## Query Path

![reading_parquet](svg/courses/databases/duckdb/03_files_and_formats/reading_parquet.svg)

---

## Globs

- read_parquet('data/*.parquet')
- Subdirectories with **
- Combine many files into one logical table
- Order is not guaranteed

---

## Partitioned Datasets

- Folder structure encodes partitions
- DuckDB infers from path
- Filters can prune partitions
- Hive-style is common

---

## Reading CSV

- read_csv with options
- read_csv_auto for inference
- Specify schema for production
- Watch out for ambiguous types

---

## Reading JSON

- read_json
- Nested data preserved
- Useful for log files
- Slower than columnar formats

---

## Writing Files

- COPY ... TO 'file.parquet'
- FORMAT parquet, csv, or json
- Partition by columns
- Compression options

---

## Remote Files

- HTTPS and S3 supported
- HTTP filesystem extension
- Credentials via env or settings
- Practical for cloud data lakes

---

## Iceberg And Delta

- Extensions read open table formats
- Time travel where supported
- Schema evolution honored
- Query without materializing

---

## Arrow Integration

- Zero-copy with Arrow buffers
- Pandas DataFrames work too
- DataFrame libraries can be queried
- Mix and match per workflow

---

## Streaming Through DuckDB

- Read from file, write to file
- No need to fit in memory
- Aggregate or transform
- Cheap ETL for one machine

---

## Caching

- Persistent file caches some metadata
- HTTP range requests for partial reads
- Local cache for remote files in extensions
- Repeat queries are fast

---

## Common File Mistakes

- Auto type detect in production
- Querying many tiny files repeatedly
- No partition pruning
- Wide unfiltered scans of remote files
- Ignoring projection pruning
