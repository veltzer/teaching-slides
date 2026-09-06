---
tags:
  - data-and-ai:big-data
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---

# Performance and Tuning

---

## What This Chapter Covers

- Partitions
- Shuffle
- Skew
- Caching
- Profiling

---

## Partitions

- Unit of parallelism
- One task per partition
- Default 200 for shuffles
- Tune to data size

---

## Coalesce vs Repartition

- coalesce: reduce, no shuffle
- repartition: any change, with shuffle
- Coalesce before write
- Repartition before wide ops

---

## Shuffle

- Data crosses network
- Most expensive step
- Triggered by joins, groupBy, distinct
- Minimize where possible

---

## Skew

- One partition far bigger
- One task slows the job
- Salt the key
- Adaptive query execution mitigates

---

## Skew Solutions

![skew_solutions](svg/courses/data_engineering/spark/03_performance_and_tuning/skew_solutions.svg)

---

## Shuffle and Skew

![shuffle_skew](svg/courses/data_engineering/spark/03_performance_and_tuning/shuffle_skew.svg)

---

## Broadcast Joins

- Avoid shuffle
- Up to small-table threshold
- Hint when planner fails
- Watch driver heap

---

## Caching

- Cache reused DataFrames
- Memory and disk levels
- Release when done
- Watch executor memory

---

## Persistence Levels

- MEMORY_ONLY
- MEMORY_AND_DISK
- DISK_ONLY
- Pick by data size and reuse

---

## File Sizes

- Many small files cost listing time
- One huge file limits parallelism
- Aim for 100MB to 1GB per file
- Compaction is a maintenance task

---

## Predicate Pushdown

- Filter pushed to data source
- Parquet, Delta support
- Less data read
- Inspect plan to verify

---

## Profiling

- Spark UI
- Stages and tasks
- Shuffle metrics
- GC time

---

## GC Tuning

- Long GCs hurt latency
- G1 in modern Java runtimes
- Right-size heap
- Off-heap for big caches

---

## Driver Pitfalls

- collect() to driver
- Broadcast huge tables
- Logging gigabytes per job
- Run heavy code in tasks

---

## Resource Allocation

- Cores per executor
- Memory per executor
- Number of executors
- Match cluster manager limits

---

## Common Tuning Mistakes

- Default partitions for huge data
- Caching cold paths
- collect() in production
- One executor too big
- Ignoring shuffle metrics
