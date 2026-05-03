---
tags:
  - data-and-ai:big-data
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---
# DataFrames and SQL

---
## What This Chapter Covers

- DataFrames basics
- Reading and writing
- SQL on Spark
- Aggregations
- Window functions

---
## What a DataFrame Is

- Distributed table abstraction
- Named columns with types
- Lazy under the hood
- Same API across languages

---
## Transform vs Action

![transform_action](svg/courses/data_engineering/spark/02_dataframes_and_sql/transform_action.svg)

---
## Reading Data

- CSV, JSON, Parquet, Delta
- Schema inference is expensive
- Pass schemas in production
- Handle bad records explicitly

---
## Writing Data

- Modes: append, overwrite, error
- Partition by columns
- Bucketing for join optimization
- Compression chosen at write

---
## Selecting and Filtering

- select, filter, where
- Column expressions
- Functions for casting and dates
- Avoid Python-side logic in hot paths

---
## Joins

- Inner, left, right, outer
- Cross for cartesian
- Anti and semi for membership
- Pick by data size

---
## Join Strategies

![join_strategies](svg/courses/data_engineering/spark/02_dataframes_and_sql/join_strategies.svg)

---
## Broadcast Join

- Send small table to all executors
- Avoids shuffle
- Hint when planner misses it
- Watch driver memory

---
## Aggregations

- groupBy
- Aggregate functions: count, sum, avg
- Multiple aggregations per group
- Watch shuffle cost

---
## Window Functions

- Compute over related rows
- Partition by, order by
- Row number, rank, lag, lead
- Replace many self-joins

---
## SQL on Spark

- Register DataFrame as temp view
- spark.sql("...")
- Reuse SQL skills
- Same Catalyst engine

---
## UDFs

- Custom Python or Scala functions
- Slow in Python without arrow
- Pandas UDFs much faster
- Prefer built-ins when possible

---
## Catalyst Optimizer

- Logical plan
- Optimized logical plan
- Physical plans
- Picks cheapest

---
## Adaptive Query Execution

- Re-plans at runtime
- Coalesces partitions
- Handles skew
- On by default in modern Spark

---
## Common DataFrame Mistakes

- Schema inference in production
- Python loops over rows
- collect() before filter
- Joining without partition strategy
- Wide aggregations on huge groups
