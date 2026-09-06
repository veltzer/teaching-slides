---
tags:
  - math:inferential-statistics
  - math:estimation
level: beginner
category: math
audience:
  - audiences:data-analysts
  - audiences:developers

---

# Confidence Intervals

---

## What This Chapter Covers

- Point estimates vs interval estimates
- What "95% confidence" actually means
- The mean &plusmn; margin-of-error recipe
- Why the t-distribution shows up
- Intervals for proportions
- Width, sample size, and what changes it

---

## 20 Confidence Intervals, One True Mean

![repeated_samples](svg/courses/math/statistics-applied/10_confidence_intervals/repeated_samples.svg)

---

## A Single Number Lies By Omission

- "The conversion rate is 4.2%" — measured exactly, or 4.2% &plusmn; 3%?
- A **point estimate** is the best single guess; an **interval estimate** adds the uncertainty
- A confidence interval is a range that plausibly contains the true value
- Always report the interval — the point alone invites overconfidence
- "X, 95% CI [a, b]" is the professional way to state a result

---

## What "95% Confidence" Means

- *Procedure-level* guarantee: if you repeated the whole study many times, ~95% of the intervals you'd construct would contain the true value
- It is **not** "95% probability the true value is in *this* interval" — the true value is fixed, not random (in the frequentist view)
- In practice: "we'd be surprised if the truth were outside this range"
- 95% is a convention, not a law — 90% is narrower, 99% wider
- The confidence level is about the *method*, not any single interval

---

## The Recipe For A Mean

- CI = x&#772; &plusmn; (critical value) &times; (standard error)
- Standard error = s / &radic;n
- Critical value &asymp; 1.96 for 95% (when n is large)
- Bigger n &#8594; smaller SE &#8594; narrower interval
- More variable data (bigger s) &#8594; wider interval

---

## Why The t-Distribution

- We rarely know the true SD &sigma;, so we plug in the sample SD s — an extra source of error
- The **t-distribution** compensates: same bell shape, fatter tails, especially for small n
- The critical value is a bit bigger than 1.96 for small samples (e.g. ~2.26 at n = 10)
- As n grows, t converges to the normal — by n &asymp; 30 the difference is tiny
- Use t for means of small samples; software does this automatically

---

## Intervals For Proportions

- For a proportion p&#770; (conversion rate, defect rate): SE = &radic;( p&#770;(1&minus;p&#770;) / n )
- CI = p&#770; &plusmn; 1.96 &times; SE for a 95% interval
- Needs a decent number of successes *and* failures (rule of thumb: at least ~10 of each)
- Near 0% or 100%, the simple formula breaks — use Wilson or Clopper&ndash;Pearson intervals
- This is the workhorse for "what fraction of users..." questions

---

## What Controls The Width

- **Sample size**: width &prop; 1/&radic;n — to halve it, quadruple n
- **Variability**: more spread in the data &#8594; wider interval
- **Confidence level**: 99% is wider than 95% is wider than 90%
- You trade certainty for precision — you can't have both for free
- Plan sample size *before* collecting data, from a target width

---

## How CI Width Shrinks with n

![width_vs_n](svg/courses/math/statistics-applied/10_confidence_intervals/width_vs_n.svg)

---

## Confidence Intervals In Python

```python
import numpy as np
from scipy import stats
x = np.array([4.1, 5.2, 3.9, 6.0, 4.8, 5.5, 4.2, 5.1])
n, mean, se = len(x), x.mean(), stats.sem(x)
lo, hi = stats.t.interval(0.95, df=n-1, loc=mean, scale=se)
print(f"mean = {mean:.2f}, 95% CI = [{lo:.2f}, {hi:.2f}]")

# proportion: 84 conversions out of 2000 visitors
res = stats.binomtest(84, 2000).proportion_ci(0.95)
print(f"rate 95% CI = [{res.low:.3%}, {res.high:.3%}]")
```

---

## Common Mistakes

- Reporting the point estimate with no interval
- Saying "95% chance the truth is in this interval" (it isn't a probability about *this* one)
- Using z = 1.96 for tiny samples instead of the t critical value
- Using the simple proportion formula when successes or failures are very few
- Treating two overlapping intervals as automatically "not different" — that test is more subtle
