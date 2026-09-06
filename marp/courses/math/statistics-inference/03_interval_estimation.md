---
tags:
  - math:estimation
  - math:inferential-statistics
level: intermediate
category: math
audience:
  - audiences:data-analysts
  - audiences:data-scientists

---

# Interval Estimation Revisited

---

## What This Chapter Covers

- Confidence intervals as a procedure, recapped precisely
- Pivotal quantities — where the formulas come from
- Intervals for means, variances, and proportions
- One-sided and equivalence intervals
- Bootstrap confidence intervals
- Coverage and what "95%" guarantees

---

## The Pivot Method

![pivot_method](svg/courses/math/statistics-inference/03_interval_estimation/pivot_method.svg)

---

## The Procedural Meaning, Sharpened

- A 95% confidence procedure produces an interval such that, *over repeated samples*, ~95% of the intervals it produces contain the true parameter
- The randomness lives in the *interval*, not the parameter — the parameter is a fixed unknown
- "There's a 95% chance &mu; is in [a, b]" is the Bayesian phrasing; it needs a prior (chapter on Bayesian inference)
- Practically: a recipe you trust to be right 19 times out of 20
- A *single* interval is either right or wrong — you just don't know which

---

## Pivotal Quantities

- A **pivot** is a function of the data *and* the parameter whose distribution doesn't depend on the parameter
- Example: (x&#772; &minus; &mu;) / (s/&radic;n) follows a t-distribution with n&minus;1 df — for *any* &mu;
- Knowing the pivot's distribution, you bracket the middle 95% of it, then algebra-rearrange to bracket &mu;
- That's literally where x&#772; &plusmn; t&#8901;(s/&radic;n) comes from — it's not arbitrary
- Most classical CIs are "find a pivot, invert it"

---

## Intervals For Means

- Known &sigma; (rare): x&#772; &plusmn; z&#8901;(&sigma;/&radic;n)
- Unknown &sigma; (the real case): x&#772; &plusmn; t&#8801;&#8901;(s/&radic;n), df = n&minus;1 — fatter critical value, especially for small n
- Difference of two means: estimate &plusmn; t&#8901;(SE of the difference); use the Welch df unless variances are known equal
- Large n: t &#8594; z, so the distinction stops mattering
- Always pair the estimate with this interval, not a bare number

---

## Intervals For Variances And Proportions

- **Variance**: the pivot (n&minus;1)s&sup2;/&sigma;&sup2; is chi-square with n&minus;1 df &#8594; an asymmetric interval for &sigma;&sup2;. Very sensitive to non-normality — use with care
- **Proportion**: the simple Wald interval p&#770; &plusmn; z&#8901;&radic;(p&#770;(1&minus;p&#770;)/n) is poor near 0 or 1 and for small n
- Prefer the **Wilson** score interval (well-behaved, recommended default) or **Clopper&ndash;Pearson** (exact, conservative)
- For a difference of proportions, similar story — use a method designed for it, not back-of-envelope
- The "rule of three": if 0 successes in n trials, the 95% upper bound is roughly 3/n

---

## CIs for a Proportion

![ci_for_proportion](svg/courses/math/statistics-inference/03_interval_estimation/ci_for_proportion.svg)

---

## One-Sided And Equivalence Intervals

- **One-sided** interval: only a lower (or only an upper) bound — "the failure rate is at most 0.3% with 95% confidence". Use when only one direction matters
- **Equivalence testing** (TOST): show the effect lies *within* a pre-specified "close enough" margin — proving *similarity*, not difference
- "Not significant" never proves "no effect"; an equivalence test can — if the whole CI is inside the margin
- Bioequivalence, non-inferiority trials, "the redesign didn't hurt conversion" all use this
- Decide one-sided vs two-sided, and the margin, *before* seeing data

---

## Bootstrap Confidence Intervals

- When no clean pivot exists (medians, ratios, correlations, custom statistics), resample
- **Percentile interval**: take the 2.5th and 97.5th percentiles of the bootstrap distribution — simple, decent
- **BCa** (bias-corrected and accelerated): adjusts for bias and skew — more accurate, the recommended default in `scipy.stats.bootstrap`
- **Basic/pivotal** bootstrap interval: reflects the percentiles about the estimate
- Use a few thousand resamples; more for the tails of BCa

---

## Coverage

- **Coverage** = the actual long-run fraction of intervals that contain the truth
- A "95% interval" with 88% coverage is lying; with 99% it's needlessly wide
- The Wald proportion interval famously under-covers; that's why Wilson exists
- Heavy skew, tiny n, or violated assumptions all degrade coverage — simulate to check if it matters
- "Nominal" (what it claims) vs "actual" (what it delivers) coverage — know the gap for your method

---

## Bootstrap And Wilson Intervals In Python

```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(2)
x = rng.lognormal(0, 0.5, 80)        # skewed -> bootstrap the median
res = stats.bootstrap((x,), np.median, confidence_level=0.95,
                      n_resamples=5000, method="BCa", random_state=rng)
print("median 95% CI (BCa):", res.confidence_interval)

# proportion: 7 successes in 50 trials -> Wilson, not Wald
ci = stats.binomtest(7, 50).proportion_ci(0.95, method="wilson")
print("Wilson 95% CI:", (round(ci.low, 3), round(ci.high, 3)))
```

---

## Common Mistakes

- Saying "95% probability the parameter is in this interval" without a Bayesian setup
- Using the Wald proportion interval near 0 or 1, or for tiny samples
- Trusting a chi-square variance interval on clearly non-normal data
- Concluding "equivalent" from a non-significant test instead of an equivalence test
- Reporting a bootstrap percentile interval when the statistic is biased and skewed (use BCa)
