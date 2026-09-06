---
tags:
  - math:descriptive-statistics
level: beginner
category: math
audience:
  - audiences:data-analysts
  - audiences:developers

---

# Summarizing Data: Spread and Shape

---

## What This Chapter Covers

- Range, IQR, variance, standard deviation
- Why we square deviations
- Percentiles and quartiles
- The five-number summary and box plots
- Skewness and kurtosis, briefly
- Coefficient of variation

---

## Same Mean, Different Spread

![same_mean_different_spread](svg/courses/math/statistics-applied/04_summarizing_spread/same_mean_different_spread.svg)

---

## Center Is Not Enough

- "Average wait time: 5 minutes" — every time, or sometimes 1 and sometimes 20?
- Spread tells you how *reliable* the center is
- Two datasets with the same mean can behave completely differently
- Decisions live in the spread: capacity, risk, SLAs
- Always report center *and* spread together

---

## Range And IQR

- **Range**: max &minus; min — simple, but driven entirely by the two extremes
- **Interquartile range (IQR)**: Q3 &minus; Q1 — the spread of the middle 50%
- IQR ignores the tails, so it's robust to outliers
- Range is fine for "what's the worst case"; IQR for "what's typical scatter"
- IQR is the basis of the box-plot whiskers

---

## Variance And Standard Deviation

- **Variance** s&sup2;: average of squared deviations from the mean
- **Standard deviation** s: square root of variance — back in the original units
- Squaring makes all deviations positive and punishes big ones harder
- "Mean 50, SD 10" &#8594; most values roughly 30&ndash;70
- SD is *the* spread measure for roughly-normal data

---

## n vs n&minus;1

- Sample variance divides by **n&minus;1**, not n (Bessel's correction)
- Dividing by n underestimates the population variance
- The sample mean is "too close" to its own data, so we compensate
- `numpy.std` defaults to n; `numpy.std(x, ddof=1)` uses n&minus;1
- For real samples, use n&minus;1 — pandas does this by default

---

## Percentiles And Quartiles

- The **p-th percentile**: the value below which p% of the data falls
- p25, p50 (median), p75 are the **quartiles**
- p95, p99 describe the tail — "the slowest 1% of requests"
- Latency and SLA reporting is almost always percentile-based, not mean-based
- A mean latency of 100ms can hide a p99 of 4 seconds

---

## Five-Number Summary And Box Plots

- Min, Q1, median, Q3, max — a compact shape sketch
- A box plot draws exactly this: box from Q1 to Q3, line at median, whiskers to the data, dots for outliers
- Great for comparing several groups side by side
- Skew shows up as an off-center median inside the box
- One box plot per group beats a table of means

---

## Anatomy of a Box Plot

![boxplot_anatomy](svg/courses/math/statistics-applied/04_summarizing_spread/boxplot_anatomy.svg)

---

## Shape: Skewness And Kurtosis

- **Skewness**: asymmetry — positive = long right tail, negative = long left tail
- **Kurtosis**: tailedness — high kurtosis means fat tails and frequent extremes
- You rarely report the numbers; you do care about the *behavior*
- Fat tails wreck assumptions and underestimate risk
- A histogram tells you most of this faster than the statistics do

---

## Computing Spread

```python
import numpy as np
x = np.array([4, 8, 6, 5, 3, 50, 7, 6, 5, 4])
print("range :", x.max() - x.min())
print("IQR   :", np.percentile(x, 75) - np.percentile(x, 25))
print("std   :", np.std(x, ddof=1))             # sample SD, n-1
print("p95   :", np.percentile(x, 95))
print("CV    :", np.std(x, ddof=1) / x.mean())  # unitless spread
```

---

## Common Mistakes

- Reporting a mean with no SD or IQR beside it
- Using the range when one outlier dominates it
- Forgetting ddof=1 and underestimating variance
- Quoting mean latency instead of p95/p99
- Ignoring fat tails because the SD "looked fine"
