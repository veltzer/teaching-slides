---
tags:
  - math:distributions
  - math:probability
level: beginner
category: math
audience:
  - audiences:data-analysts
  - audiences:developers

---

# The Normal Distribution

---

## What This Chapter Covers

- The shape and its two parameters
- The 68&ndash;95&ndash;99.7 rule
- Standardizing: z-scores
- Reading and using the standard normal
- Why "normal" is everywhere — and where it isn't
- Checking normality

---

## The 68-95-99.7 Rule

![empirical_rule](svg/courses/math/statistics-applied/08_normal_distribution/empirical_rule.svg)

---

## The Bell Curve

- Symmetric, single peak at the mean, tails that never quite touch zero
- Fully described by two numbers: mean &mu; (where it's centered) and SD &sigma; (how wide)
- Change &mu;: the curve slides. Change &sigma;: it stretches or pinches
- The most-used distribution in all of statistics
- "Gaussian" is the same thing

---

## The Empirical Rule

- About **68%** of values fall within &mu; &plusmn; 1&sigma;
- About **95%** within &mu; &plusmn; 2&sigma; (more precisely 1.96&sigma;)
- About **99.7%** within &mu; &plusmn; 3&sigma;
- This is why a "3-sigma event" is supposed to be rare (~1 in 370)
- These numbers only hold *if the data is actually normal*

---

## Z-Scores

- z = (x &minus; &mu;) / &sigma; — how many SDs above or below the mean a value is
- z = 0 is the mean; z = 2 is "two SDs above"; z = &minus;1.5 is "1.5 SDs below"
- Strips away units — a z-score is comparable across different variables
- Standardizing turns *any* normal into the **standard normal** (mean 0, SD 1)
- All normal-curve probabilities are looked up on that one standard curve

---

## z-Scores in Pictures

![z_score](svg/courses/math/statistics-applied/08_normal_distribution/z_score.svg)

---

## Using The Standard Normal

- P(Z &lt; z) is the cumulative probability — "the fraction below z"
- z = 1.96 cuts off the top 2.5%; z = &plusmn;1.96 brackets the middle 95%
- z = 1.645 cuts off the top 5%; z = 2.576 the top 0.5%
- These exact numbers reappear in confidence intervals and hypothesis tests — memorize 1.96
- Old courses used printed "z-tables"; now it's one function call

---

## Why Normal Shows Up Everywhere

- The central limit theorem (next chapter): *sums and averages* tend to be normal, whatever the raw data looks like
- Many measurements are the sum of many small independent influences
- That's why heights, errors, totals, and especially *sample means* look bell-shaped
- It is the reason most of inferential statistics works at all
- It does **not** mean your raw data is normal — averages, not individuals

---

## Where Normal Fails

- Skewed data: incomes, response times, sales — long right tail
- Bounded data: proportions near 0 or 1, percentages
- Counts, especially of rare events — Poisson, not normal
- Heavy-tailed data: financial returns, file sizes — extremes far too common for a normal
- Multimodal data: two populations mixed together

---

## Standardizing And Checking In Python

```python
import numpy as np
from scipy import stats
x = np.array([61, 64, 67, 70, 73, 76, 79])
z = (x - x.mean()) / x.std(ddof=1)
print("z-scores:", np.round(z, 2))
print("P(Z < 1.96) =", stats.norm.cdf(1.96))     # ~0.975
print("Shapiro p  =", stats.shapiro(x).pvalue)    # >0.05 -> consistent with normal
```

- Also eyeball a Q-Q plot — points on a straight line means roughly normal

---

## Common Mistakes

- Assuming raw business data is normal because "data usually is" — it usually isn't
- Applying the 68&ndash;95&ndash;99.7 rule to skewed data
- Treating a "3-sigma" threshold as rare when the data is heavy-tailed
- Forgetting that z-scores require knowing (or estimating) &sigma;
- Confusing "the sample mean is normal" with "the sample is normal"
