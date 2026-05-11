---
tags:
  - math:hypothesis-testing
level: intermediate
category: math
audience:
  - audiences:data-analysts
  - audiences:data-scientists

---
# Analysis of Variance

---
## What This Chapter Covers

- Why not just run many t-tests
- Partitioning variance: between vs within
- The F-statistic and the F-distribution
- One-way ANOVA assumptions
- Post-hoc comparisons
- Effect size and the ANOVA&ndash;regression connection

---
## Partitioning Variance

![between_vs_within](svg/courses/math/statistics-inference/05_anova/between_vs_within.svg)

---
## The Many-Groups Problem

- You have a numeric metric across *k* groups (3+ ad creatives, 4 server configs) and want to know if any differ
- Running all pairwise t-tests inflates the false-positive rate — 6 tests at &alpha; = 0.05 gives ~26% chance of a fluke
- **ANOVA** does one global test first: "are *all* the group means equal?"
- Reject &#8594; *something* differs &#8594; then do controlled follow-up comparisons
- It's an omnibus test, a gatekeeper for the pairwise questions

---
## Partitioning The Variance

- Total variability in the data = variability **between** group means + variability **within** groups
- Algebraically: SS_total = SS_between + SS_within (the sums of squares add up exactly)
- If the groups truly have the same mean, "between" reflects only noise — same scale as "within"
- If they differ, "between" is inflated by the real differences
- ANOVA compares these two sources of variability — hence the name

---
## The F-Statistic

- Convert each SS to a **mean square** by dividing by its degrees of freedom: MS_between (df = k&minus;1), MS_within (df = N&minus;k)
- **F = MS_between / MS_within** — a ratio of variances
- Under H&#8320; (all means equal), F is around 1 and follows an **F-distribution** with (k&minus;1, N&minus;k) df
- Large F (well above 1) &#8594; small p &#8594; the group means aren't all equal
- The F-distribution is right-skewed and lives on [0, &infin;) — it's the ratio of two scaled chi-squares

---
## One-Way ANOVA Assumptions

- **Independence** of observations within and across groups — the critical one
- **Normality** of residuals (or large groups, via the CLT)
- **Homogeneity of variance** (homoscedasticity) — roughly equal spread across groups; check with Levene's test or a residual plot
- Unequal variances? Use **Welch's ANOVA** — the multi-group analog of Welch's t-test
- Badly non-normal with small groups? Use the **Kruskal&ndash;Wallis** test (later chapter)

---
## Post-Hoc Comparisons

- A significant ANOVA says "not all equal" — not *which* ones differ
- Follow with pairwise comparisons that *control the family-wise error rate*: **Tukey's HSD** is the standard choice
- Other options: Bonferroni (conservative, simple), Scheffé (very conservative, allows arbitrary contrasts)
- Don't just run uncorrected t-tests afterward — that throws away ANOVA's protection
- If you only care about specific pre-planned comparisons, you can sometimes skip the omnibus test entirely

---
## ANOVA Workflow

![workflow](svg/courses/math/statistics-inference/05_anova/workflow.svg)

---
## Effect Size For ANOVA

- p (and F) depend on sample size; effect size doesn't
- **eta-squared** (&eta;&sup2;) = SS_between / SS_total — fraction of total variance explained by the grouping
- **omega-squared** (&omega;&sup2;) — a less biased version, preferred for reporting
- Rough anchors: &eta;&sup2; ~0.01 small, ~0.06 medium, ~0.14 large
- A "highly significant" ANOVA with &eta;&sup2; = 0.005 means the grouping barely matters

---
## ANOVA Is Regression

- One-way ANOVA is exactly a linear regression with the group as a categorical predictor (dummy variables)
- The F-test for the model equals the ANOVA F-test; the residual variance equals MS_within
- This is why statisticians talk about "the general linear model" — t-tests, ANOVA, and regression are one framework
- Practical upshot: once you know regression, two-way ANOVA, covariates (ANCOVA), and unbalanced designs are easy
- Use `statsmodels` formulas (`y ~ C(group)`) and you get ANOVA, regression, and diagnostics from one fit

---
## One-Way ANOVA In Python

```python
import numpy as np, pandas as pd, statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
rng = np.random.default_rng(4)
g = np.repeat(["A", "B", "C"], 40)
y = np.concatenate([rng.normal(m, 10, 40) for m in (100, 103, 110)])
df = pd.DataFrame({"y": y, "g": g})
print(sm.stats.anova_lm(ols("y ~ C(g)", df).fit(), typ=2))   # F-test
print(pairwise_tukeyhsd(df.y, df.g))                          # which pairs differ
```

---
## Common Mistakes

- Running all pairwise t-tests instead of an omnibus test first
- Following a significant ANOVA with uncorrected pairwise t-tests
- Ignoring unequal variances instead of switching to Welch's ANOVA
- Reporting F and p with no eta-squared / omega-squared
- Forcing a one-way ANOVA onto small, heavily skewed groups instead of Kruskal&ndash;Wallis
