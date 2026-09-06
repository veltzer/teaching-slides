---
tags:
  - math:statistics
level: beginner
category: math
audience:
  - audiences:data-analysts
  - audiences:developers

---

# Types of Data

---

## What This Chapter Covers

- Categorical vs numerical data
- Nominal, ordinal, interval, ratio
- Discrete vs continuous
- Why the data type dictates the method
- Cross-sectional vs time series
- Structured vs messy reality

---

## Taxonomy of Data Types

![taxonomy](svg/courses/math/statistics-applied/02_types_of_data/taxonomy.svg)

---

## The First Question

- Before any analysis: *what kind of data is this?*
- The data type decides which summary, chart, and test are legal
- Computing a mean of ZIP codes is a classic blunder
- Get the type wrong and everything downstream is nonsense
- Five seconds of thought saves an hour of confusion

---

## Categorical vs Numerical

- **Categorical**: labels — color, country, plan tier, yes/no
- **Numerical**: quantities you can do arithmetic on — age, price, latency
- Categorical: count and proportion make sense
- Numerical: mean, spread, correlation make sense
- "Number of categories" (3 plans) is numerical *about* categorical data

---

## The Four Levels Of Measurement

- **Nominal**: categories with no order — eye color, browser
- **Ordinal**: ordered categories, unequal gaps — survey "poor/ok/good"
- **Interval**: numeric, equal gaps, no true zero — temperature in &deg;C
- **Ratio**: numeric, equal gaps, true zero — height, income, count
- Each level unlocks more operations than the one before

---

## What's Legal at Each Level

![legal_operations](svg/courses/math/statistics-applied/02_types_of_data/legal_operations.svg)

---

## Why The Level Matters

- Nominal: only mode and frequencies
- Ordinal: also median and percentiles — but not mean (gaps aren't equal)
- Interval: also mean, standard deviation — but ratios are meaningless (20&deg;C isn't "twice" 10&deg;C)
- Ratio: everything, including ratios
- Treating ordinal as ratio (averaging 1-5 stars) is common and slightly wrong

---

## Discrete vs Continuous

- **Discrete**: countable values — number of orders, clicks, defects
- **Continuous**: any value in a range — weight, time, voltage
- Discrete often modeled with Poisson or binomial
- Continuous often modeled with normal or exponential
- In practice everything is discrete (finite precision), but the model can be continuous

---

## Inspecting Types In Practice

```python
import pandas as pd
df = pd.DataFrame({
    "plan": ["free", "pro", "pro", "free"],
    "logins": [3, 41, 12, 0],
    "rating": [2, 5, 4, 3],   # ordinal 1-5
})
print(df.dtypes)
print(df["plan"].value_counts())   # categorical -> counts
print(df["logins"].mean())          # ratio -> mean is fine
```

---

## Other Useful Distinctions

- **Cross-sectional**: many units at one point in time (today's users)
- **Time series**: one unit over many time points (daily revenue)
- **Panel**: many units over many time points
- Time series needs its own tools — order matters, observations aren't independent
- Don't apply plain hypothesis tests to autocorrelated time series

---

## Common Mistakes

- Averaging nominal codes (ZIP codes, category IDs)
- Treating ordinal ratings as if gaps were equal
- Storing numbers as strings and never noticing
- Applying cross-sectional methods to time series
- Letting the database type ("it's an int") decide the statistical type
