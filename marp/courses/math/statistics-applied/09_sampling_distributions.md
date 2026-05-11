---
tags:
  - math:inferential-statistics
level: beginner
category: math
audience:
  - audiences:data-analysts
  - audiences:developers

---
# Sampling and Sampling Distributions

---
## What This Chapter Covers

- Why we sample at all
- Sampling methods — and how they go wrong
- The sampling distribution of a statistic
- Standard error
- The central limit theorem
- Bootstrapping as a shortcut

---
## Central Limit Theorem in Action

![clt](svg/courses/math/statistics-applied/09_sampling_distributions/clt.svg)

---
## Why Sample

- Measuring the whole population is usually impossible, slow, or expensive
- A well-chosen sample answers the question well enough — at a fraction of the cost
- The catch: a *badly* chosen sample answers a different question, confidently
- Sample size controls *precision*; sampling *method* controls *bias*
- No amount of data fixes a biased sampling method — only a better method does

---
## Sampling Methods

- **Simple random**: every unit equally likely — the gold standard, often hard in practice
- **Stratified**: split into groups, sample within each proportionally — guarantees coverage
- **Cluster**: randomly pick whole groups (towns, stores), measure everyone in them — cheap logistics
- **Systematic**: every k-th unit — fine unless there's a hidden periodicity
- **Convenience**: whoever's easy to reach — biased, common, usually unfit for inference

---
## Four Sampling Methods

![sampling_methods](svg/courses/math/statistics-applied/09_sampling_distributions/sampling_methods.svg)

---
## How Sampling Goes Wrong

- **Selection bias**: the sampling frame misses part of the population (online-only survey)
- **Non-response bias**: who answers differs systematically from who doesn't
- **Survivorship bias**: you only see the units that made it (returned planes, surviving funds)
- **Voluntary response**: angry and delighted people self-select; the middle stays silent
- Each of these biases the *expected* answer — bigger samples don't help

---
## The Sampling Distribution

- Imagine taking many samples and computing the statistic (say the mean) for each
- Those values themselves form a distribution — the **sampling distribution** of the statistic
- It's centered (for the mean) on the true population value
- Its spread shrinks as sample size grows
- This is the conceptual heart of every confidence interval and p-value

---
## Standard Error

- The **standard error (SE)** is the standard deviation *of the sampling distribution*
- For a sample mean: SE = &sigma; / &radic;n (use s if &sigma; is unknown)
- It's "how much the sample mean wobbles from sample to sample"
- Quadruple the sample &#8594; halve the SE — diminishing returns
- Don't confuse SE (precision of the estimate) with SD (spread of the data)

---
## The Central Limit Theorem

- The sampling distribution of the **mean** is approximately **normal** for large n — *no matter* the shape of the original data
- That's why we can use normal-curve maths for confidence intervals even on skewed data
- Rough rule: n &geq; 30 is usually enough; skewer data needs more
- It applies to sums and means, not to individual values or to maxima
- One of the most consequential results in the whole subject

---
## Bootstrapping

- Don't want to derive the sampling distribution? *Simulate* it
- Resample your data *with replacement*, recompute the statistic, repeat thousands of times
- The spread of those resampled statistics estimates the standard error
- Works for medians, ratios, and weird statistics with no tidy formula
- Costs CPU instead of cleverness — a great default in practice

---
## CLT And Bootstrap In Python

```python
import numpy as np
rng = np.random.default_rng(0)
data = rng.exponential(scale=2.0, size=200)   # very skewed raw data
boot = [rng.choice(data, size=len(data), replace=True).mean()
        for _ in range(10000)]
print("estimate of mean :", np.mean(boot))
print("standard error   :", np.std(boot, ddof=1))   # ~ s/sqrt(n)
print("95% interval     :", np.percentile(boot, [2.5, 97.5]))
```

---
## Common Mistakes

- Trusting a convenience sample for population inference
- Believing a huge sample fixes a biased sampling method
- Confusing the standard error with the standard deviation
- Applying the CLT to individual values instead of to the mean
- Forgetting bootstrap resampling must be *with* replacement
