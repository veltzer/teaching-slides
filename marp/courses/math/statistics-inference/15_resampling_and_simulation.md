---
tags:
  - math:inferential-statistics
level: intermediate
category: math
audience:
  - audiences:data-analysts
  - audiences:data-scientists

---

# Resampling and Simulation

---

## What This Chapter Covers

- Trading formulas for compute
- The bootstrap, in detail
- Jackknife
- Permutation (randomization) tests
- Cross-validation
- Monte Carlo simulation, power, and a few pitfalls

---

## How the Bootstrap Works

![bootstrap](svg/courses/math/statistics-inference/15_resampling_and_simulation/bootstrap.svg)

---

## Let The Computer Do The Statistics

- Classical inference derives a sampling distribution by math — often only possible under strong assumptions
- **Resampling** builds it empirically: repeatedly draw new "datasets" from your data (or from a model) and watch how the statistic varies
- Works for medians, ratios, correlations, R&sup2;, a custom business metric — anything you can compute
- Costs CPU instead of cleverness; with modern hardware that's usually a great trade
- Three workhorses: the **bootstrap** (standard errors and CIs), **permutation tests** (p-values), **cross-validation** (predictive error)

---

## The Bootstrap

- To estimate the sampling variability of a statistic: resample your n data points **with replacement** to get a "bootstrap sample" of size n; recompute the statistic; repeat B times (B = a few thousand)
- The spread of those B values estimates the **standard error**; their percentiles give a **confidence interval**
- The logic: your sample is your best stand-in for the population, so resampling *from it* mimics drawing fresh samples *from the population*
- Confidence-interval flavors: **percentile** (simple), **basic/pivotal**, and **BCa** (bias-corrected and accelerated — most accurate, the recommended default)
- It breaks down for statistics that depend on extreme order values (the sample max/min) and for strongly dependent data — for time series use a **block bootstrap**

---

## The Jackknife

- The bootstrap's older, simpler cousin: form n datasets by leaving out **one** observation at a time, recompute the statistic on each
- The variability across those n "leave-one-out" estimates yields a standard error (and a bias estimate)
- Cheaper and fully deterministic, but less accurate than the bootstrap — and it can fail for non-smooth statistics like the median
- Mostly of historical and pedagogical interest now; the bootstrap superseded it for general use
- Its "leave-one-out" idea, though, is exactly what reappears in cross-validation

---

## Permutation Tests

- The most assumption-light hypothesis test: under H&#8320; the group labels are arbitrary, so **shuffle them**
- Two-group example: pool all the data, randomly reassign units to "A" and "B" (keeping the group sizes), recompute the statistic (difference of means, of medians, whatever); repeat thousands of times
- The **p-value** is the fraction of shuffles whose statistic is at least as extreme as the one you actually observed
- Exact (up to Monte Carlo error), no normality or large-n needed; you pick the test statistic freely
- The one requirement is **exchangeability under H&#8320;** — which a randomized experiment hands you for free; it generalizes naturally to paired data (shuffle *within* pairs) and to multi-group designs

---

## Cross-Validation

- The honest way to estimate how well a model will predict **new** data — because in-sample error (training R&sup2;, training accuracy) is optimistically biased
- **k-fold CV**: split the data into k parts; train on k&minus;1, test on the held-out one; rotate so each part is the test set once; average the test errors. **Leave-one-out** is the k = n extreme
- Use it to compare models and to tune hyperparameters — pick the model/setting with the best *cross-validated* error, not the best fit
- Pitfalls: any preprocessing fitted on the data (scaling, feature selection, imputation) must happen **inside** each fold, or you've leaked the test set; for time series use forward-chaining (no peeking into the future); for grouped data, keep whole groups together
- "Tuned on CV, then also reported CV error as the final estimate" is mild double-dipping — keep a separate untouched test set for the final number

---

## k-fold Cross-Validation

![k_fold_cv](svg/courses/math/statistics-inference/15_resampling_and_simulation/k_fold_cv.svg)

---

## Monte Carlo Simulation

- When you *do* have a model, simulate from it to answer questions that resist pencil-and-paper
- **Power analysis for any design**: simulate the experiment many times under a plausible effect, run your planned analysis each time, count how often it rejects H&#8320; — that fraction is the power
- Also: propagate uncertainty through a complex calculation, price a contingent payoff, estimate a probability with no closed form, stress-test a method's coverage
- The error of a Monte Carlo estimate shrinks like 1/&radic;(number of simulations) — want one more digit of precision, run ~100&times; more reps
- **Always set and record a random seed** — reproducibility, and the ability to debug a weird run

---

## Resampling In Python

```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(12)
a = rng.lognormal(0, 0.6, 30); b = rng.lognormal(0.3, 0.6, 30)

# bootstrap CI for the median of group a (BCa)
ci = stats.bootstrap((a,), np.median, method="BCa", n_resamples=5000,
                     random_state=rng).confidence_interval
print("median(a) 95% CI:", (round(ci.low, 2), round(ci.high, 2)))

# permutation test: difference of means, no distributional assumption
p = stats.permutation_test((a, b), lambda x, y: x.mean() - y.mean(),
                           n_resamples=10000, random_state=rng).pvalue
print("permutation p:", round(p, 3))
```

---

## Common Mistakes

- Bootstrapping a statistic that depends on extreme values (max/min), or bootstrapping dependent data without blocking
- Reporting a bootstrap percentile interval for a biased, skewed statistic instead of using BCa
- Leaking information by doing preprocessing or feature selection *outside* the cross-validation folds
- Using a permutation test where exchangeability under H&#8320; doesn't actually hold
- Forgetting to set a random seed — irreproducible results and unrepeatable bugs
