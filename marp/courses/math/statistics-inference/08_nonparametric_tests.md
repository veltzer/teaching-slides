---
tags:
  - math:hypothesis-testing
level: intermediate
category: math
audience:
  - audiences:data-analysts
  - audiences:data-scientists

---

# Non-Parametric Tests

---

## What This Chapter Covers

- When to abandon the normality assumption
- The sign test and Wilcoxon signed-rank test
- The Mann&ndash;Whitney U test
- The Kruskal&ndash;Wallis test
- Permutation tests
- Costs, benefits, and what these tests actually test

---

## Parametric ↔ Non-Parametric Pairings

![parametric_to_rank](svg/courses/math/statistics-inference/08_nonparametric_tests/parametric_to_rank.svg)

---

## When Parametric Assumptions Fail

- Small samples *and* clearly non-normal data: heavy skew, fat tails, outliers, ordinal scales
- The CLT can't rescue you when n is small, and a single outlier can dominate a t-test
- **Non-parametric** tests assume far less — usually just that the data is continuous (and exchangeable)
- They work on **ranks** (or on resampling), so extreme values lose their leverage
- The trade: a little less power when normality *does* hold; much more reliability when it doesn't

---

## What These Tests Actually Test

- They're often *not* tests about the mean — and that matters for interpretation
- Most are about whether one distribution is **stochastically shifted** relative to another — "values in A tend to be larger than in B"
- Under an added assumption (same shape, just shifted), that becomes a statement about the **median**
- So report medians, not means, alongside them
- Don't claim "the means differ" from a rank test — claim "one group tends to be larger"

---

## Sign Test And Wilcoxon Signed-Rank

- Both replace the **one-sample / paired t-test** (work on the differences, or on data vs a reference value)
- **Sign test**: count how many differences are positive vs negative; ignores magnitude entirely — robust but low power
- **Wilcoxon signed-rank**: rank the differences by absolute size, sum the ranks of the positives — uses magnitude info, more power than the sign test
- Wilcoxon assumes the differences are symmetric about their center; the sign test assumes nothing about shape
- Use Wilcoxon by default for paired non-normal data; fall back to the sign test if symmetry is doubtful

---

## Mann&ndash;Whitney U Test

- Replaces the **independent two-sample t-test** (also called the Wilcoxon rank-sum test — same thing)
- Pool both groups, rank everything, then ask whether one group's ranks are systematically higher
- H&#8320;: a randomly drawn value from A is equally likely to be above or below one from B
- Robust to outliers and skew; valid for ordinal data too
- With ties or small samples, use the exact version; `scipy` handles this

---

## Kruskal&ndash;Wallis Test

- The **non-parametric one-way ANOVA** — three or more independent groups
- Rank all observations together, compare the average rank across groups
- H&#8320;: all groups have the same distribution (loosely, the same median)
- Significant &#8594; follow with pairwise Mann&ndash;Whitney tests, **corrected** for multiple comparisons (Bonferroni/Holm) — same discipline as Tukey after ANOVA
- For repeated measures across 3+ conditions, the **Friedman test** is the analog

---

## Permutation Tests

- The most flexible option: build the null distribution by *shuffling* the data, no distributional assumption at all
- For a two-group difference: pool the data, randomly relabel into "A" and "B" thousands of times, recompute the statistic each time
- The p-value is the fraction of shuffles with a statistic at least as extreme as the observed one
- Works for *any* statistic — difference of means, difference of medians, a weird custom metric
- Only real assumption: **exchangeability** under H&#8320; (which is what randomized experiments give you for free); costs CPU, not cleverness

---

## How a Permutation Test Works

![permutation_test](svg/courses/math/statistics-inference/08_nonparametric_tests/permutation_test.svg)

---

## Costs And Benefits

- **Benefits**: few assumptions, robust to outliers and skew, valid for ordinal data, often exact for small samples
- **Costs**: ~5% less power than the t-test/ANOVA *when normality genuinely holds*; tests a shift in distribution, not specifically the mean; effect sizes are less familiar (rank-biserial r, Cliff's delta)
- **Rule of thumb**: large n &#8594; lean parametric (CLT helps, more power, familiar effect sizes); small + non-normal &#8594; non-parametric or permutation
- When unsure, run both and report the parametric one if they agree — if they disagree, trust the non-parametric one and investigate why
- Permutation tests are a great default middle ground: assumption-light *and* you choose the statistic

---

## Non-Parametric Tests In Python

```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(6)
a = rng.lognormal(0, 0.6, 25); b = rng.lognormal(0.4, 0.6, 25)   # skewed
print("Mann-Whitney p:", stats.mannwhitneyu(a, b).pvalue)
print("Kruskal p     :", stats.kruskal(a, b, rng.lognormal(0.8, 0.6, 25)).pvalue)
# permutation test on the difference of means - no distributional assumption
print("permutation p :",
      stats.permutation_test((a, b), lambda x, y: x.mean() - y.mean(),
                             n_resamples=10000, random_state=rng).pvalue)
```

---

## Common Mistakes

- Reaching for a rank test at large n when a parametric test would be more powerful and just as valid
- Reporting "the means differ" from Mann&ndash;Whitney/Kruskal&ndash;Wallis (it's about a distributional shift)
- Skipping the multiple-comparison correction on post-Kruskal&ndash;Wallis pairwise tests
- Using the sign test (very low power) when Wilcoxon signed-rank would do
- Forgetting that permutation tests still require exchangeability under the null
