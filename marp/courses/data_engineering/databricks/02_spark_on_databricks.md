---
tags:
  - data-and-ai:data-engineering
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---
# Spark on Databricks

---
## What This Chapter Covers

- Spark recap
- DataFrames and Datasets
- SQL on Spark
- Performance basics
- UDFs

---
## Spark in 60 Seconds

- Distributed compute engine
- In-memory where possible
- Lazy evaluation
- Driver coordinates workers

---
## DataFrames

- Tabular abstraction
- Logical plan optimized
- Catalyst plans physical execution
- Same API across languages

---
## Datasets

- Typed rows, JVM languages
- Compile-time checks
- Slower than DataFrames in Python
- Use where types matter

---
## Spark SQL

- ANSI-style SQL
- Same engine as DataFrames
- Table abstraction over files
- Familiar to analysts

---
## Reads and Writes

- Read CSV, Parquet, Delta, JSON
- Schema inference is risky
- Provide schemas
- Write modes: append, overwrite, error

---
## Partitions

- Unit of parallelism
- Default 200 for shuffle
- Tune to data size
- Skew is a common problem

---
## Joins

- Broadcast for small tables
- Shuffle hash for medium
- Sort-merge for large
- Hint when needed

---
## Skew

- One key dominates
- One task too slow
- Salt the key
- Adaptive query execution helps

---
## Caching

- Cache DataFrame for reuse
- Memory or disk
- Watch RAM
- Release when done

---
## UDFs

- Custom logic
- Slow in Python
- Pandas UDFs faster
- Native SQL faster still

---
## Adaptive Query Execution

- Re-plans at runtime
- Coalesces partitions
- Handles skew
- Often a free win

---
## Cost vs Performance

- Bigger clusters not always faster
- Disk spill is expensive
- Cache the right things
- Profile before scaling

---
## Common Spark Mistakes

- Schema inference in production
- collect() on large data
- Caching everything
- Ignoring shuffle metrics
- One partition for huge data
