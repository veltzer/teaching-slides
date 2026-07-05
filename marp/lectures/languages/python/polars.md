---
tags:
- languages:python
- concepts:data-science
- concepts:dataframes
- concepts:performance
- tools:polars
level: intermediate
category: language
audience:
- audiences:developers
- audiences:data-scientists

---
# Polars and Python
## Fast, Modern DataFrames Beyond pandas
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## What This Lecture Covers

1. What Polars is and why it exists
1. The engine: Rust, Apache Arrow, and parallelism
1. DataFrames, expressions, and the core contexts
1. Lazy evaluation and query optimization
1. Joins, windows, and reshaping
1. Streaming datasets larger than memory
1. Interop with pandas, NumPy, and SQL
1. Migrating from pandas — what changes and what to watch

---

## What Is Polars?

- A DataFrame library for Python — the same problem space as pandas
- Written in **Rust**, exposed to Python through native bindings
- Built on the **Apache Arrow** columnar memory format
- **Multi-threaded by default** — uses all your cores without asking
- Ships a **lazy engine** with a real query optimizer

---

## Why Not Just pandas?

- pandas is single-threaded — one core works, the rest watch
- Eager execution: every step materializes a full intermediate result
- The index adds complexity that most workloads never need
- Mixed types and silent copies make memory use hard to predict
- pandas is fine for small data — the pain starts as data grows

---

## The Engine Underneath

- Rust core: no interpreter in the hot path, no GIL to fight
- Arrow layout: columns are contiguous buffers, cheap to scan
- Work is split across threads automatically — per column, per group
- Vectorized kernels process whole columns at once
- The result: order-of-magnitude speedups on typical workloads

---

## Getting Started

```bash
pip install polars
```

```python
import polars as pl

df = pl.DataFrame({
    "name": ["alice", "bob", "carol"],
    "dept": ["dev", "ops", "dev"],
    "salary": [98_000, 84_000, 121_000],
})
print(df)
```

- The printed frame shows column **names and types** in the header

---

## Reading and Writing Data

```python
df = pl.read_csv("people.csv")
df = pl.read_parquet("events.parquet")
df = pl.read_json("records.json")

df.write_parquet("out.parquet")
df.write_csv("out.csv")
```

- Readers infer types from the data and are fast — CSV parsing is parallel
- Prefer **Parquet** for anything you read more than once

---

## Expressions — The Core Idea

- An expression describes a computation on columns: `pl.col("salary") * 1.1`
- Expressions are **declarative** — they build a plan, not a result
- The engine runs them in parallel and optimizes them as a group
- The same expression works in every context: select, filter, group by
- This is the single most important concept in Polars

---

## Selecting Columns

```python
df.select(
    pl.col("name"),
    pl.col("salary"),
    (pl.col("salary") * 1.1).alias("raised"),
)
```

- `select` keeps only what you name — the output is a new frame
- `alias` names a computed column
- Every expression in the call runs **in parallel**

---

## Filtering Rows

```python
df.filter(pl.col("salary") > 90_000)

df.filter(
    (pl.col("dept") == "dev") & (pl.col("salary") > 100_000)
)
```

- Conditions are expressions too — combine with `&`, `|`, `~`
- No `.loc`, no boolean index gymnastics — one method, one meaning

---

## Adding and Transforming Columns

```python
df.with_columns(
    (pl.col("salary") / 12).alias("monthly"),
    pl.col("name").str.to_uppercase().alias("upper_name"),
)
```

- `with_columns` keeps existing columns and adds the new ones
- Namespaces group type-specific operations: `.str`, `.dt`, `.list`
- Frames are **immutable** — every operation returns a new frame

---

## Group By and Aggregation

```python
df.group_by("dept").agg(
    pl.col("salary").mean().alias("avg_salary"),
    pl.col("salary").max().alias("top_salary"),
    pl.len().alias("headcount"),
)
```

- `agg` takes any list of expressions — each one runs per group
- Groups are processed in parallel across threads
- No "split-apply-combine" ceremony — one call does it all

---

## Conditional Logic

```python
df.with_columns(
    pl.when(pl.col("salary") > 100_000)
    .then(pl.lit("senior"))
    .otherwise(pl.lit("junior"))
    .alias("band"),
)
```

- `when / then / otherwise` is the expression form of if-else
- Chains of `when` clauses handle multiple cases
- `pl.lit` wraps a literal value as an expression

---

## Eager vs Lazy

- Everything so far was **eager**: each call computes immediately
- Lazy mode builds a **query plan** instead and runs it once
- The optimizer sees the whole plan before any work starts
- Eager is great for exploration; lazy is what you ship
- Switching is one method call in either direction

---

## The LazyFrame

```python
result = (
    pl.scan_parquet("events.parquet")
    .filter(pl.col("country") == "IL")
    .group_by("city")
    .agg(pl.col("amount").sum())
    .collect()
)
```

- `scan_*` returns a **LazyFrame** — nothing is read yet
- `collect()` triggers optimization and execution
- `df.lazy()` converts an existing eager frame

---

## What the Optimizer Does

- **Predicate pushdown** — filters run at the file scan, not after
- **Projection pushdown** — only referenced columns are read at all
- Common subexpressions are computed once and reused
- Redundant operations are removed from the plan entirely
- Inspect it yourself: `lf.explain()` prints the optimized plan

---

## Why Pushdown Matters

- A Parquet file stores columns separately with per-block statistics
- Projection pushdown: 3 columns referenced from 80 — read only 3
- Predicate pushdown: skip whole blocks that cannot match the filter
- The fastest work is the work that never happens
- On wide tables this alone can dwarf every other speedup

---

## Joins

```python
orders.join(customers, on="customer_id", how="inner")

orders.join(
    customers.select("customer_id", "segment"),
    on="customer_id",
    how="left",
)
```

- `how` accepts `inner`, `left`, `full`, `semi`, `anti`, `cross`
- `semi` and `anti` filter one side by the other — no columns added
- Joins are parallel and work in both eager and lazy mode

---

## Window Functions

```python
df.with_columns(
    pl.col("salary").mean().over("dept").alias("dept_avg"),
    pl.col("salary").rank().over("dept").alias("dept_rank"),
)
```

- `over` computes per group **without collapsing rows**
- The SQL equivalent is a window function — same mental model
- Combine any aggregation with `over` — mean, rank, sum, first

---

## Reshaping Data

```python
long = df.unpivot(index="name", on=["q1", "q2", "q3"])

wide = long.pivot(on="variable", index="name", values="value")
```

- `unpivot` turns columns into rows — wide to long
- `pivot` goes the other way — long to wide (eager frames only)
- Most pipelines prefer long data; pivot at the very end for display

---

## Missing Data

```python
df.with_columns(
    pl.col("score").fill_null(0),
    pl.col("score").is_null().alias("was_missing"),
)
df.drop_nulls()
```

- Missing values are `null` — one concept for **every** type
- `NaN` is a separate float value, not "missing" — a common gotcha
- Aggregations skip nulls by default and do it consistently

---

## Data Types

- Explicit and strict: `Int64`, `Float64`, `String`, `Boolean`
- Temporal types: `Date`, `Datetime`, `Duration`, `Time`
- Nested types: `List`, `Array`, `Struct` — first-class, not objects
- `Categorical` and `Enum` for low-cardinality strings
- Strictness catches type bugs early instead of coercing silently

---

## Strings and Dates

```python
df.with_columns(
    pl.col("email").str.contains("@corp.com").alias("internal"),
    pl.col("ts").str.to_datetime("%Y-%m-%d %H:%M"),
).with_columns(
    pl.col("ts").dt.weekday().alias("weekday"),
)
```

- `.str` and `.dt` mirror what pandas offers — but run in parallel
- Parsing formats are explicit — no guessing, no surprise locales

---

## Time-Series Grouping

```python
df.sort("ts").group_by_dynamic(
    "ts", every="1h"
).agg(
    pl.col("amount").sum().alias("hourly_total"),
)
```

- `group_by_dynamic` buckets rows into time windows
- `every`, `period`, and `offset` control window shape and overlap
- Rolling and resampling workflows replace pandas `resample`

---

## Larger Than Memory: Streaming

```python
result = (
    pl.scan_parquet("huge/*.parquet")
    .filter(pl.col("status") == "ok")
    .group_by("user_id")
    .agg(pl.col("bytes").sum())
    .collect(engine="streaming")
)
```

- The streaming engine processes data in **batches**
- Datasets far larger than RAM become workable on one machine
- Same query — only the `collect` call changes

---

## Interop: pandas, NumPy, Arrow

```python
pdf = df.to_pandas()
df2 = pl.from_pandas(pdf)

arr = df.select("salary").to_numpy()
tbl = df.to_arrow()
```

- Arrow makes conversion cheap — often zero-copy
- Keep the pipeline in Polars; convert at the edges when a
  library demands pandas or NumPy

---

## The SQL Interface

```python
result = pl.sql(
    """
    SELECT dept, AVG(salary) AS avg_salary
    FROM df
    GROUP BY dept
    """
).collect()
```

- SQL queries run on frames in scope — same engine, same optimizer
- Great for teams where SQL is the shared language
- Mix freely: SQL for the query, expressions for the cleanup

---

## Coming from pandas

| pandas | Polars |
|---|---|
| `df[df.x > 3]` | `df.filter(pl.col("x") > 3)` |
| `df.assign(y=...)` | `df.with_columns(...)` |
| `df.groupby().agg()` | `df.group_by().agg()` |
| `df.merge(other)` | `df.join(other)` |
| `df.melt()` | `df.unpivot()` |

---

## What You Give Up

- **No index** — rows are just rows; use columns and joins instead
- Smaller ecosystem — some libraries still expect pandas input
- Plotting usually means converting to pandas first
- Different muscle memory — method names and idioms differ
- Very small data won't feel faster — overhead dominates

---

## Performance Habits

- Prefer `scan_*` over `read_*` — let pushdown do its job
- Stay lazy end-to-end; `collect()` once at the end
- Avoid `map_elements` with Python functions — it kills parallelism
- Use expressions for everything the API can express natively
- Check `lf.explain()` when a query is slower than expected

---

## When to Choose What

- **Polars**: pipelines, feature engineering, files in the gigabytes
- **Polars streaming**: bigger than RAM, still one machine
- **pandas**: tiny data, quick plots, libraries that require it
- **Spark**: data that outgrows one machine entirely
- Polars covers the wide middle ground with the least machinery

---

## Summary

- Polars is a **Rust-powered, Arrow-native** DataFrame library
- **Expressions** describe work; the engine parallelizes it
- **Lazy mode** adds a query optimizer — pushdown is the big win
- Streaming handles larger-than-memory data on a single machine
- Interop with pandas, NumPy, and SQL keeps migration incremental

---

## Where to Start

1. `pip install polars` and rewrite one small pandas script
1. Learn `select`, `filter`, `with_columns`, `group_by` — the core four
1. Switch the pipeline to `scan_*` + `collect()` and read `explain()`
1. Reach for streaming only when memory actually runs out

Start with one real pipeline; the API will carry you from there.

---

## Questions?

- Polars brings modern engine design to everyday Python data work
- Expressions and lazy plans are the two ideas that matter most
- Migrate one pipeline at a time — interop makes it painless

## Thank You
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)
