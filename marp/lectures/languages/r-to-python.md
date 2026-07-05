---
tags:
- languages:python
- languages:r
- concepts:programming
- concepts:data-science
level: intermediate
category: language
audience:
- audiences:developers
- audiences:data-scientists

---
# From R to Python
## A Migration Guide for R Users
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## From R to Python

![title](svg/lectures/languages/r-to-python/title.svg)

---

## Lecture Roadmap

![overview](svg/lectures/languages/r-to-python/overview.svg)

---

## Overview: Details

**Audience:** R users (data scientists, statisticians, analysts)
**Goal:** Become productive in Python without losing your R instincts
**Approach:** Map every R concept to its Python equivalent

---

## Who Is This For?

- You know R well: `data.frame`, `dplyr`, `ggplot2`, `lm`
- You need Python for a job, a team, or a deployment target
- You want to keep the *ideas* and swap the *syntax*
- You want to know what is genuinely different, not just renamed

---

## Why Move From R to Python?

![why_python](svg/lectures/languages/r-to-python/why_python.svg)

---

## Why Move From R to Python: Details

- Python is a **general-purpose** language, not stats-first
- Dominant in machine learning, deep learning, and MLOps
- Easier to ship: web services, APIs, containers, pipelines
- Huge ecosystem beyond analytics (web, automation, systems)

---

## R and Python: Two Philosophies

![two_philosophies](svg/lectures/languages/r-to-python/two_philosophies.svg)

---

## R and Python: Two Philosophies (Details)

- R was built **by statisticians, for statistics**
- Python was built as a **general-purpose** language
- R is vector-first; Python is object-first
- Python has "one obvious way"; R has many dialects

---

## The Big Mental Shifts

- Indexing starts at **0**, not **1**
- Assignment is `=`, not `<-`
- Blocks use **indentation**, not `{ }`
- Most objects are **mutable** (watch for aliasing)
- Data frames are a **library** (pandas), not a builtin

---

## Development Environment

![environments](svg/lectures/languages/r-to-python/environments.svg)

---

## Development Environment: Details

- RStudio → VS Code, PyCharm, or JupyterLab
- R console → the Python REPL / IPython
- R Markdown / Quarto → Jupyter notebooks (Quarto also works)
- `.RData` workspace → explicit files (pickle, parquet, CSV)

---

## Installing Python and Packages

```bash
# The interpreter
python --version

# A virtual environment (like a project-local library)
python -m venv .venv
source .venv/bin/activate

# Install packages from PyPI (the CRAN of Python)
pip install numpy pandas matplotlib scikit-learn
```

---

## Environments: R vs Python

- R: one global library, `install.packages()` into it
- Python: **isolate per project** with `venv` or `conda`
- Never `pip install` into the system interpreter
- `requirements.txt` / `pyproject.toml` pin your dependencies

---

## Hello, World

```misc
# R
greeting <- "Hello, World"
print(greeting)
cat(greeting, "\n")
```

```python
# Python
greeting = "Hello, World"
print(greeting)
```

---

## Assignment and Comments

```misc
# R: arrow assignment, # comments
x <- 42
y = 42          # allowed but unusual
z <<- 42        # global assignment
```

```python
# Python: equals assignment, # comments
x = 42
y: int = 42     # optional type hint
# no arrow, no <<-
```

---

## Syntax: Blocks and Indentation

```misc
# R uses braces
if (x > 0) {
  print("positive")
} else {
  print("non-positive")
}
```

```python
# Python uses indentation (4 spaces) and a colon
if x > 0:
    print("positive")
else:
    print("non-positive")
```

---

## Basic Types Mapping

![basic_types](svg/lectures/languages/r-to-python/basic_types.svg)

---

## Basic Types: Details

- R `numeric` → Python `float`; R `integer` (`1L`) → `int`
- R `character` → Python `str`
- R `logical` (`TRUE`/`FALSE`) → `bool` (`True`/`False`)
- R `NULL` → `None`; R `NA` → `None` / `NaN` / `pd.NA`

---

## There Is No Scalar in R

```misc
# R: everything is a vector; length-1 vectors are "scalars"
x <- 5
length(x)   # 1
x[1]        # 5
```

```python
# Python: a scalar is a scalar; a list is a container
x = 5
len(x)      # TypeError: int has no len()
x[0]        # TypeError: int not subscriptable
```

---

## Data Structures Mapping

![data_structures](svg/lectures/languages/r-to-python/data_structures.svg)

---

## Vectors → NumPy Arrays

```misc
# R: vectors are the native building block
v <- c(1, 2, 3, 4)
v * 2            # 2 4 6 8  (vectorized)
sum(v)           # 10
```

```python
# Python: use NumPy for vectorized numeric work
import numpy as np
v = np.array([1, 2, 3, 4])
v * 2            # array([2, 4, 6, 8])
v.sum()          # 10
```

---

## Lists: A Word of Warning

```misc
# R list: heterogeneous, named, 1-indexed
lst <- list(a = 1, b = "two", c = TRUE)
lst$a
lst[["b"]]
```

```python
# Python: a dict is the closest match to a named R list
d = {"a": 1, "b": "two", "c": True}
d["a"]
# a Python list is an ordered, mutable sequence (no names)
xs = [1, "two", True]
```

---

## Indexing: The 1 vs 0 Trap

![indexing](svg/lectures/languages/r-to-python/indexing.svg)

---

## Indexing: Details

```misc
# R: 1-based, inclusive on both ends
v <- c(10, 20, 30, 40, 50)
v[1]       # 10  (first)
v[2:4]     # 20 30 40
v[-1]      # drops the first element
```

```python
# Python: 0-based, end-exclusive slices
v = [10, 20, 30, 40, 50]
v[0]       # 10  (first)
v[1:4]     # [20, 30, 40]
v[-1]      # 50  (last element, not "drop first")
```

---

## data.frame → pandas DataFrame

![dataframe](svg/lectures/languages/r-to-python/dataframe.svg)

---

## Creating a DataFrame

```misc
# R base data.frame
df <- data.frame(
  name = c("Ann", "Bob"),
  age  = c(30, 25)
)
df$age
nrow(df)
```

```python
# pandas
import pandas as pd
df = pd.DataFrame({
    "name": ["Ann", "Bob"],
    "age":  [30, 25],
})
df["age"]
len(df)
```

---

## The Library Map

![library_map](svg/lectures/languages/r-to-python/library_map.svg)

---

## The Library Map: Details

- `dplyr` / `data.table` → **pandas** (and **polars**)
- `ggplot2` → **matplotlib** + **seaborn** (or **plotnine**)
- `lm` / `glm` → **statsmodels**
- `caret` / `tidymodels` → **scikit-learn**

---

## dplyr → pandas

```misc
# R: dplyr pipeline
library(dplyr)
result <- df %>%
  filter(age > 25) %>%
  group_by(city) %>%
  summarise(mean_age = mean(age))
```

```python
# Python: pandas method chaining
result = (
    df[df["age"] > 25]
    .groupby("city")
    .agg(mean_age=("age", "mean"))
    .reset_index()
)
```

---

## The Pipe: %>% → Method Chaining

![pipe_chaining](svg/lectures/languages/r-to-python/pipe_chaining.svg)

---

## Vectorization vs Loops

```misc
# R: apply family avoids explicit loops
sapply(1:5, function(x) x^2)     # 1 4 9 16 25
vapply(v, sqrt, numeric(1))
```

```python
# Python: comprehensions and NumPy
[x**2 for x in range(1, 6)]      # [1, 4, 9, 16, 25]
import numpy as np
np.sqrt(np.arange(1, 6))
```

---

## Functions and Arguments

```misc
# R: function keyword, lazy evaluation, invisible return
scale_it <- function(x, factor = 2) {
  x * factor
}
scale_it(10)
```

```python
# Python: def keyword, eager evaluation, explicit return
def scale_it(x, factor=2):
    return x * factor

scale_it(10)
```

---

## Beware: Mutable Default Arguments

```misc
# R copies on modification, so this is safe
f <- function(x = c()) { x <- c(x, 1); x }
```

```python
# Python: NEVER use a mutable default; it is shared across calls
def bad(x=[]):        # the same list persists between calls!
    x.append(1)
    return x

def good(x=None):     # the correct idiom
    if x is None:
        x = []
    x.append(1)
    return x
```

---

## Missing Values: NA vs NaN vs None

![missing_values](svg/lectures/languages/r-to-python/missing_values.svg)

---

## Missing Values: Details

- R has one first-class `NA` woven into every operation
- Python spreads the idea across `None`, `float('nan')`, `pd.NA`
- `NaN != NaN` — use `pd.isna()`, never `== NaN`
- pandas skips `NaN` in `mean()`/`sum()` like R's `na.rm = TRUE`

---

## Plotting

```misc
# R: ggplot2 grammar of graphics
library(ggplot2)
ggplot(df, aes(x = age, y = income)) +
  geom_point() +
  geom_smooth(method = "lm")
```

```python
# Python: matplotlib + seaborn
import seaborn as sns
import matplotlib.pyplot as plt
sns.regplot(data=df, x="age", y="income")
plt.show()
```

---

## Statistics and Modeling

![modeling](svg/lectures/languages/r-to-python/modeling.svg)

---

## Linear Models: lm → statsmodels

```misc
# R: formula interface is first-class
model <- lm(income ~ age + education, data = df)
summary(model)
predict(model, newdata)
```

```python
# Python: statsmodels gives you the R-style formula + summary
import statsmodels.formula.api as smf
model = smf.ols("income ~ age + education", data=df).fit()
model.summary()
model.predict(new_df)
```

---

## Machine Learning: scikit-learn

```python
# The estimator API: fit / predict / score
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y)
model = LinearRegression().fit(X_train, y_train)
model.predict(X_test)
model.score(X_test, y_test)
```

---

## Reproducibility and Randomness

```misc
# R
set.seed(42)
sample(1:100, 5)
```

```python
# Python: seed the library you actually use
import numpy as np
rng = np.random.default_rng(42)
rng.integers(1, 101, size=5)
```

---

## Common Gotchas

![gotchas](svg/lectures/languages/r-to-python/gotchas.svg)

---

## Common Gotchas: Details

- **Copy vs view:** pandas may return a view; use `.copy()`
- **Integer division:** `/` is float, `//` is floor in Python
- **Recycling:** R recycles vectors; NumPy broadcasts by rules
- **`&&` vs `&`:** Python has `and`/`or` and elementwise `&`/`|`

---

## Interop: Keep Using R From Python

```python
# You do not have to abandon R overnight
# reticulate calls Python from R; rpy2 calls R from Python
import rpy2.robjects as ro
ro.r("summary(lm(mpg ~ wt, data = mtcars))")
```

- Run both languages during the transition
- Port pipelines one stage at a time
- Share data via **parquet**, **feather**, or **CSV**

---

## Migration Strategy

![migration_strategy](svg/lectures/languages/r-to-python/migration_strategy.svg)

---

## Migration Strategy: Details

- Start with a virtual environment and pandas
- Reimplement one analysis end-to-end for confidence
- Learn the scikit-learn `fit`/`predict` pattern early
- Keep R around for interop until you are fluent

---

## Key Takeaways

![key_takeaways](svg/lectures/languages/r-to-python/key_takeaways.svg)

---

## Key Takeaways: Details

- The *ideas* transfer; only the *syntax* and *libraries* change
- pandas + NumPy + scikit-learn cover most of your R workflow
- Mind the 0-based indexing and mutable objects
- Isolate projects with virtual environments from day one

---

## Thank You

- Practice: port one real R script this week
- Reference: pandas, NumPy, scikit-learn, statsmodels docs
- Questions? [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)
