---
tags:
  - math:hypothesis-testing
level: beginner
category: math
audience:
  - audiences:data-analysts
  - audiences:developers

---

# Comparing Two Groups

---

## What This Chapter Covers

- The two-sample t-test
- Paired vs independent samples
- Equal-variance vs Welch's test
- Comparing two proportions
- Effect size for a difference (Cohen's d)
- When to reach for a non-parametric test instead

---

## Paired vs Independent Samples

![paired_vs_independent](svg/courses/math/statistics-applied/12_comparing_two_groups/paired_vs_independent.svg)

---

## The Most Common Question In Practice

- "Group A vs group B — is the difference real?"
- Treatment vs control, variant vs baseline, region vs region
- The tool is almost always some flavor of the **two-sample test**
- The differences between the flavors matter — pick the right one
- And always look at the *size* of the difference, not just whether it's "significant"

---

## The Two-Sample t-Test

- H&#8320;: the two population means are equal; H&#8321;: they differ
- Test statistic: (difference in sample means) / (standard error of that difference)
- Big difference relative to the noise &#8594; small p &#8594; evidence the means differ
- Assumes roughly normal data *or* large samples (CLT), and independent observations
- The default for comparing the average of a numeric metric between two groups

---

## Paired vs Independent

- **Independent samples**: two separate groups — users in A vs users in B
- **Paired samples**: the *same* units measured twice — before vs after, left vs right
- Paired data: analyze the *differences* with a one-sample test — far more powerful
- Using an independent-samples test on paired data throws away that power
- Ask: "is each value in group 1 naturally matched to one in group 2?" If yes, pair them

---

## Equal Variance Or Not

- The classic ("Student's") t-test assumes the two groups have equal variance
- **Welch's t-test** does not — it's more robust and barely costs anything
- Default to Welch unless you have a strong reason to assume equal variances
- In `scipy`, that's `ttest_ind(..., equal_var=False)` — and it should arguably be the default
- Don't run a preliminary variance test to "decide" — just use Welch

---

## Comparing Two Proportions

- Conversion rate in A vs B, defect rate this batch vs last
- H&#8320;: the two population proportions are equal
- Use a two-proportion z-test, or equivalently a 2&times;2 chi-square test
- Needs enough successes *and* failures in each group (~10+ each as a rule of thumb)
- Report the **difference** (and its CI), or the relative lift — not just "significant"

---

## Effect Size For A Difference

- p tells you "is there a difference"; effect size tells you "how big"
- **Cohen's d** = (difference in means) / (pooled SD) — difference measured in SDs
- Rough labels: ~0.2 small, ~0.5 medium, ~0.8 large — context-dependent
- For proportions: report the absolute difference and the relative lift
- A "significant" d of 0.02 is real and useless; say so

---

## When To Go Non-Parametric

- Small samples *and* clearly non-normal, heavily skewed, or outlier-ridden data
- **Mann&ndash;Whitney U** replaces the independent two-sample t-test
- **Wilcoxon signed-rank** replaces the paired t-test
- These test whether one group tends to be larger, using ranks instead of raw values
- Slightly less power when normality *does* hold — but much safer when it doesn't

---

## Two-Group Comparisons In Python

```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(2)
a = rng.normal(100, 12, 60)
b = rng.normal(105, 15, 55)
t, p = stats.ttest_ind(a, b, equal_var=False)        # Welch
d = (b.mean() - a.mean()) / np.sqrt((a.var(ddof=1)+b.var(ddof=1))/2)
print(f"Welch t={t:.2f}, p={p:.3f}, Cohen d={d:.2f}")

# proportions: 84/2000 vs 110/2050
print(stats.chi2_contingency([[84, 2000-84], [110, 2050-110]])[1])
```

---

## Effect Size: How Big is the Shift?

![effect_size](svg/courses/math/statistics-applied/12_comparing_two_groups/effect_size.svg)

---

## Common Mistakes

- Using an independent-samples test on paired data (or vice versa)
- Assuming equal variances instead of just using Welch
- Comparing proportions with too few successes or failures
- Reporting "significant" with no effect size or difference estimate
- Forcing a t-test onto tiny, wildly skewed samples instead of a rank test
