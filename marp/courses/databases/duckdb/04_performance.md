---
tags:
  - databases:duckdb
level: intermediate
category: databases
audience:
  - audiences:developers
  - audiences:data-engineers

---
# Performance

---
## What This Chapter Covers

- Vectorized engine
- Threads
- Memory
- Storage layout
- Query plans

---
## Vectorized Execution

- Operate on chunks not rows
- Cache-friendly
- Few function calls per row
- Source of speed

---
## Pipeline Visualized

![vectorized_pipeline](svg/courses/databases/duckdb/04_performance/vectorized_pipeline.svg)

---
## Parallelism

- Multi-threaded by default
- One query uses many cores
- Configure thread count
- Profile to verify usage

---
## Performance Tips

![perf_tips](svg/courses/databases/duckdb/04_performance/perf_tips.svg)

---
## Memory Limit

- PRAGMA memory_limit
- Spill to disk when exceeded
- Set to leave headroom for OS
- Avoid OS-killed sessions

---
## Spilling

- Temporary files on disk
- Larger queries still complete
- Slower than in-memory
- Fast SSD strongly preferred

---
## Storage Layout

- Native file is columnar
- Compressed by column
- Persistent and fast to reopen
- Versioned format

---
## Compression

- Choose at write
- Trade size vs CPU
- Defaults are good
- Test on representative data

---
## Statistics

- Min/max per row group
- Drives skipping
- Re-collected on writes
- Helps both Parquet and native

---
## Query Plans

- EXPLAIN
- EXPLAIN ANALYZE for actual times
- Operator costs
- Look for big scans, big joins

---
## Joins

- Hash joins by default
- Build the smaller side
- Memory cost equal to small side
- Filter early to reduce

---
## Aggregations

- Hash aggregate
- Sort aggregate when memory tight
- Combine reduce data sooner
- Window aggregates also vectorized

---
## ORDER BY And LIMIT

- Top-N optimization
- Faster than full sort plus limit
- Use LIMIT when possible
- Saves memory

---
## Caching Layers

- OS page cache
- DuckDB internal caches
- Repeat queries are fast
- Cold runs may be slower

---
## Common Performance Mistakes

- Memory limit too low
- One thread
- Fragmented many-file datasets
- Auto type detect every query
- Skipping EXPLAIN
