---
tags:
- languages:python
- concepts:data-science
- concepts:dataframes
- tools:pandas
level: intermediate
category: language
audience:
- audiences:developers
- audiences:data-scientists

---

# pandas and Python
## Practical Data Analysis with DataFrames
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## What This Lecture Covers

1. What pandas is and where it fits
1. Series, DataFrame, and the index
1. Selecting data: `loc`, `iloc`, and boolean filters
1. Cleaning: missing data, types, strings, dates
1. `groupby`, merging, and reshaping
1. Time series essentials
1. Performance pitfalls and how to avoid them
1. Modern pandas: Arrow types and copy-on-write

---

## What Is pandas?

- The most widely used DataFrame library in Python
- Built on top of **NumPy** — typed columns, vectorized operations
- Made for messy, labeled, mixed-type tabular data
- The default dialect of data science tutorials and notebooks
- Enormous ecosystem: nearly every data tool accepts a DataFrame

---

## Series and DataFrame

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["alice", "bob", "carol"],
    "dept": ["dev", "ops", "dev"],
    "salary": [98_000, 84_000, 121_000],
})
s = df["salary"]        # a Series
```

- A **Series** is one typed column with labels
- A **DataFrame** is a set of Series sharing one **index**

---

## Anatomy of a DataFrame

![anatomy](svg/lectures/languages/python/pandas/anatomy.svg)

---

## Reading and Writing Data

```python
df = pd.read_csv("people.csv")
df = pd.read_parquet("events.parquet")
df = pd.read_sql("SELECT * FROM users", conn)

df.to_parquet("out.parquet")
df.to_csv("out.csv", index=False)
```

- Readers exist for almost anything — CSV, Excel, SQL, JSON
- `index=False` on export avoids writing a meaningless column

---

## First Look at a Frame

```python
df.head()
df.info()
df.describe()
df.shape, df.dtypes
```

- `info` shows types, non-null counts, and memory — read it first
- `describe` gives quick statistics for numeric columns
- A minute of inspection saves an hour of confused debugging

---

## Selecting: loc and iloc

```python
df.loc[2, "salary"]                 # by label
df.loc[df["dept"] == "dev", ["name", "salary"]]

df.iloc[0, 2]                       # by position
df.iloc[0:2, 0:2]
```

- `loc` speaks **index labels**; `iloc` speaks **integer positions**
- Plain `df[...]` is fine for columns — use `loc`/`iloc` for rows

---

## Labels vs Positions

![loc_iloc](svg/lectures/languages/python/pandas/loc_iloc.svg)

---

## The Index

```python
df = df.set_index("name")
df.loc["carol"]
df = df.reset_index()
```

- Row labels — any column can be promoted to the index
- Operations **align on the index**, not on row order
- A meaningful index makes lookups and joins natural
- When it gets in the way, `reset_index` and move on

---

## Filtering Rows

```python
df[df["salary"] > 90_000]

df[(df["dept"] == "dev") & (df["salary"] > 100_000)]

df.query("dept == 'dev' and salary > 100_000")
```

- Boolean masks with `&`, `|`, `~` — parentheses required
- `query` trades a little magic for a lot of readability

---

## Adding Columns

```python
df["monthly"] = df["salary"] / 12

df = df.assign(
    band=np.where(df["salary"] > 100_000, "senior", "junior"),
)
```

- Column math is vectorized — NumPy does the actual work
- `assign` returns a new frame — friendly to method chains

---

## Missing Data

```python
df["score"].isna().sum()
df["score"] = df["score"].fillna(0)
df = df.dropna(subset=["score"])
```

- Missing is `NaN` (float) or `NaT` (time) — check with `isna`
- Decide explicitly: fill, drop, or keep and let functions skip it
- Watch out: `NaN` silently turns integer columns into floats

---

## Group By

```python
df.groupby("dept")["salary"].mean()

df.groupby("dept").agg(
    avg_salary=("salary", "mean"),
    headcount=("name", "count"),
)
```

- Named aggregations keep output columns tidy
- Group keys become the index of the result — `reset_index` if needed

---

## Split, Apply, Combine

![groupby](svg/lectures/languages/python/pandas/split_apply_combine.svg)

---

## Merging Frames

```python
orders.merge(customers, on="customer_id", how="inner")

orders.merge(
    customers[["customer_id", "segment"]],
    on="customer_id",
    how="left",
)
```

- `how` is `inner`, `left`, `right`, or `outer`
- Select the columns you need **before** merging — smaller and clearer

---

## How Joins Match Rows

![joins](svg/lectures/languages/python/pandas/joins.svg)

---

## Stacking Frames

```python
all_quarters = pd.concat([q1, q2, q3], ignore_index=True)
```

- `concat` stacks frames vertically (or side by side with `axis=1`)
- `ignore_index=True` renumbers instead of keeping duplicate labels
- Collect frames in a list and concatenate **once** — never in a loop

---

## Reshaping: Wide and Long

```python
long = df.melt(id_vars="name", value_vars=["q1", "q2", "q3"])

wide = long.pivot(index="name", columns="variable", values="value")
```

- `melt` turns columns into rows — wide to long
- `pivot` goes back — long to wide, great for final tables
- Analysis prefers long data; presentation prefers wide

---

## Wide and Long

![wide_long](svg/lectures/languages/python/pandas/wide_long.svg)

---

## Time Series

```python
df["ts"] = pd.to_datetime(df["ts"])
df = df.set_index("ts").sort_index()

hourly = df["amount"].resample("1h").sum()
df["weekday"] = df.index.weekday
```

- Parse first — strings are not dates
- A datetime index unlocks `resample`, slicing by date, rolling windows
- `df.loc["2026-07"]` selects a whole month by label

---

## Strings and Categories

```python
df["email"].str.contains("@corp.com")
df["name"].str.upper()

df["dept"] = df["dept"].astype("category")
```

- The `.str` accessor vectorizes string operations
- `category` stores repeated strings once — big memory savings
- Low-cardinality text columns should almost always be categorical

---

## Performance Pitfalls

- `iterrows` — a Python loop in disguise; almost always the wrong tool
- `apply` with a lambda is a loop too — prefer vectorized column math
- Growing a frame row by row is quadratic — collect, then `concat`
- Chained indexing (`df[a][b] = x`) may silently edit a **copy**
- Use `loc` for assignment and keep operations whole-column

---

## Under the Hood

![under_hood](svg/lectures/languages/python/pandas/under_hood.svg)

---

## Modern pandas

```python
df = pd.read_csv("people.csv", dtype_backend="pyarrow")
```

- PyArrow-backed dtypes: real strings, proper missing values, speed
- **Copy-on-write** removes the classic chained-assignment surprises
- Method chains and `assign` are the house style of modern code
- If you learned pandas years ago, it reads better today

---

## When to Choose What

- **pandas**: exploration, notebooks, small-to-medium labeled data
- **NumPy**: pure numeric arrays, no labels needed
- **Polars**: bigger data, pipelines, parallel and lazy execution
- **Spark**: data that outgrows one machine
- They interoperate — moving between them is routine, not rewrite

---

## Summary

- pandas is labeled, mixed-type data done practically
- `loc`/`iloc`, masks, and the index are the core selection tools
- `groupby`, `merge`, `melt`/`pivot` cover most table reshaping
- Stay vectorized — loops and `apply` are the enemy of speed
- Arrow types and copy-on-write make modern pandas safer and faster

---

## Where to Start

1. Load a real CSV and live in `head`, `info`, `describe`
1. Practice `loc` vs `iloc` until the difference is reflex
1. Redo one spreadsheet workflow with `groupby` and `merge`
1. Hunt down one `iterrows` in your code and vectorize it

One real dataset teaches more than ten tutorials.

---

## Questions?

- DataFrames are labeled, typed columns sharing an index
- Select with intent, stay vectorized, reshape freely
- pandas is the lingua franca — speak it well before optimizing

## Thank You
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)
