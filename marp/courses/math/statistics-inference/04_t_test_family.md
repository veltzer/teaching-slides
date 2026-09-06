---
tags:
  - math:hypothesis-testing
level: intermediate
category: math
audience:
  - audiences:data-analysts
  - audiences:data-scientists

---

# The t-Test Family

---

## What This Chapter Covers

- Where the t-distribution comes from
- The one-sample t-test
- The paired t-test
- Independent two-sample: Student's vs Welch's
- Assumptions and how robust the test really is
- Effect sizes and the test&ndash;interval connection

---

## t Distribution vs Normal

![t_vs_normal](svg/courses/math/statistics-inference/04_t_test_family/t_vs_normal.svg)

---

## Why "t" And Not "z"

- Standardizing a mean needs &sigma;, which we don't know — we plug in s, the sample SD
- That substitution adds noise, so (x&#772; &minus; &mu;)/(s/&radic;n) is *not* standard normal
- It follows **Student's t-distribution** with n&minus;1 degrees of freedom: same bell shape, heavier tails
- Fewer df &#8594; heavier tails &#8594; larger critical values; df &geq; ~30 and it's essentially the normal
- "Degrees of freedom" &asymp; how many independent pieces of information are left after estimating the mean

---

## One-Sample t-Test

- Question: is the population mean equal to some reference value &mu;&#8320;?
- Statistic: t = (x&#772; &minus; &mu;&#8320;) / (s/&radic;n), compared to a t-distribution with n&minus;1 df
- Use it for: "is the average response time still 200ms?", "did the process drift off target?"
- Equivalent to checking whether &mu;&#8320; lies outside the t confidence interval for the mean
- One-sided variant when only one direction is of interest — decide before looking

---

## Paired t-Test

- Two measurements on the *same* units: before/after, left/right, matched pairs
- Compute the within-pair differences, then run a one-sample t-test on those differences against 0
- Pairing removes between-unit variability &#8594; much higher power than treating the data as independent
- The classic mistake: feeding paired data to an independent two-sample test and losing that power
- Test: "is each value in group 1 naturally matched to exactly one in group 2?" — if yes, pair

---

## Independent Two-Sample: Student vs Welch

- Question: do two *separate* groups have the same mean?
- **Student's t-test** assumes equal variances and pools them — slightly more power *if* that holds
- **Welch's t-test** allows unequal variances, uses a fractional df — robust, almost free
- **Default to Welch.** Don't run a preliminary F-test to "decide" — that two-step procedure misbehaves
- `scipy.stats.ttest_ind(a, b, equal_var=False)` — and many argue it should be the default

---

## Assumptions, And Robustness

- **Independence** within and between groups — the non-negotiable one; clustered or repeated data needs other models
- **Normality** of the data (or, by the CLT, of the sample means) — matters mainly for small n
- **Equal variances** — only for Student's; Welch waives it
- The t-test is fairly robust to mild non-normality at moderate n; it is *not* robust to dependence or to a few wild outliers
- Tiny, heavily skewed samples: use a permutation test or a rank test instead (later chapters)

---

## Effect Size

- p answers "is there a difference"; **Cohen's d** answers "how big" — d = (difference in means)/(pooled SD)
- Rough anchors: ~0.2 small, ~0.5 medium, ~0.8 large — but always interpret in context
- For a one-sample or paired test, d uses the relevant SD (of the data, or of the differences)
- A statistically significant d of 0.03 is real and unimportant; report it as such
- Pair every t-test with d (or the raw difference) and its confidence interval

---

## Choosing the Right t-Test

![test_decision_tree](svg/courses/math/statistics-inference/04_t_test_family/test_decision_tree.svg)

---

## Tests And Intervals, Again

- A two-sided t-test at level &alpha; rejects H&#8320;: "&mu; = &mu;&#8320;" exactly when &mu;&#8320; is outside the (1&minus;&alpha;) t-interval
- For two samples: "0 is outside the 95% CI for the difference" &#8801; "significant at 0.05, two-sided"
- So the interval gives the test result *and* the magnitude — strictly more useful than a bare p
- Report the difference and its CI as the headline; the p-value is secondary
- This generalizes: most parametric tests have a matching interval

---

## The t-Test Family In Python

```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(3)
before = rng.normal(50, 8, 30); after = before + rng.normal(2, 5, 30)  # paired
print("paired   :", stats.ttest_rel(after, before).pvalue)

a = rng.normal(100, 10, 60); b = rng.normal(104, 16, 50)               # two-sample
print("Welch    :", stats.ttest_ind(a, b, equal_var=False).pvalue)
d = (b.mean()-a.mean()) / np.sqrt((a.var(ddof=1)+b.var(ddof=1))/2)
print("Cohen d  :", round(d, 2))
```

---

## Common Mistakes

- Treating paired data as independent (or vice versa)
- Choosing Student's t-test by way of a preliminary variance test instead of just using Welch
- Trusting a t-test on a tiny, badly skewed sample with outliers
- Reporting significance with no effect size
- Forgetting that the matching confidence interval already contains the test result, with more detail
