---
tags:
  - math:inferential-statistics
level: intermediate
category: math
audience:
  - audiences:data-analysts
  - audiences:data-scientists

---

# The Inference Toolkit

---

## What This Chapter Covers

- What inference adds on top of descriptive statistics
- Estimation, testing, and prediction as three jobs
- The role of a statistical model
- Assumptions and what breaks when they fail
- Parametric vs non-parametric vs resampling approaches
- A map of the rest of the course

---

## The Three Jobs of Inference

![three_jobs](svg/courses/math/statistics-inference/01_inference_toolkit/three_jobs.svg)

---

## What Inference Is For

- You have a sample; you want a statement about the population (or the data-generating process)
- Inference is the disciplined leap from "what I saw" to "what is probably true"
- It always carries quantified uncertainty — that's the deliverable, not an afterthought
- Three recurring jobs: **estimate** a quantity, **test** a claim, **predict** a future value
- Everything in this course is a special case of one of those three

---

## The Three Jobs

- **Estimation**: best guess for a parameter, plus a confidence/credible interval — "the mean is 4.2 [3.9, 4.5]"
- **Hypothesis testing**: is a specific claim compatible with the data? — "is the mean 4.0? p = 0.03"
- **Prediction**: what value will a *new* observation take, with what uncertainty? — "next month: 1200 &plusmn; 150"
- They're connected: an interval implies a test; a model used for testing can also predict
- Know which job you're doing before picking a method

---

## What A Statistical Model Is

- A model is an assumed *family* of data-generating mechanisms, with unknown parameters
- "Observations are i.i.d. Normal(&mu;, &sigma;&sup2;)" — &mu; and &sigma; are what you estimate
- "y = &beta;&#8320; + &beta;&#8321;x + noise" — the &beta;s are the parameters
- The model is a deliberate simplification; "all models are wrong, some are useful"
- Every p-value, interval, and prediction is *conditional on the model being roughly right*

---

## Assumptions, And What They Buy You

- Common assumptions: independence, identical distribution, a particular shape (often normality), constant variance, correct functional form
- They're the price of clean formulas — fewer assumptions, weaker conclusions, more computation
- **Independence** is the one you can almost never sacrifice — violate it and standard errors are simply wrong
- Normality matters most for *small* samples (the CLT rescues large ones for means)
- Always state your assumptions and check the ones that matter

---

## When Assumptions Fail

- Non-independence (time series, clustered data, repeated measures): use models built for it (mixed models, time-series methods), not plain tests
- Non-normality with small n: use non-parametric or permutation tests
- Non-constant variance (heteroscedasticity): robust standard errors, transformations, or weighted methods
- Wrong functional form (a curve fit with a line): residual plots catch it; transform or use a flexible model
- "The test still ran" is not evidence the assumptions held

---

## Three Families Of Methods

- **Parametric**: assume a distribution family, estimate its parameters — t-tests, ANOVA, linear/logistic regression. Powerful when the assumptions hold
- **Non-parametric**: assume far less (often just continuity) — rank tests, the bootstrap. Robust, slightly less powerful when parametric assumptions *do* hold
- **Resampling/simulation**: let the computer build the sampling distribution — bootstrap, permutation tests. Few assumptions, costs CPU
- They're complementary, not rivals — many real analyses use two of them as a cross-check
- This course covers all three

---

## Three Method Families

![three_method_families](svg/courses/math/statistics-inference/01_inference_toolkit/three_method_families.svg)

---

## A Tiny End-To-End Example

```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(0)
x = rng.normal(10, 3, 40)
print("estimate:", x.mean(),
      "95% CI:", stats.t.interval(0.95, len(x)-1, x.mean(), stats.sem(x)))
print("test mu=9:", stats.ttest_1samp(x, 9).pvalue)
boot = [rng.choice(x, len(x), replace=True).mean() for _ in range(5000)]
print("bootstrap CI:", np.percentile(boot, [2.5, 97.5]))   # cross-check
```

---

## The Rest Of This Course

- Estimation theory; better interval estimates
- The t-test family; one-way and factorial ANOVA
- Chi-square tests for categorical data; non-parametric alternatives
- Correlation analysis; simple, multiple, and logistic regression
- Experimental design; Bayesian inference; resampling and simulation

---

## Common Mistakes

- Running a method without knowing which of the three jobs it's for
- Forgetting that every result is conditional on the model
- Sacrificing independence "because the test still produces a number"
- Worrying about normality on a huge sample (CLT) while ignoring it on a tiny one
- Treating parametric, non-parametric, and resampling methods as enemies rather than tools
