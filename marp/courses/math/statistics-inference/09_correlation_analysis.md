---
tags:
  - math:inferential-statistics
level: intermediate
category: math
audience:
  - audiences:data-analysts
  - audiences:data-scientists

---
# Correlation Analysis

---
## What This Chapter Covers

- Pearson correlation and inference on it
- Spearman and Kendall: rank correlations
- Partial and semi-partial correlation
- The correlation matrix and its pitfalls
- Attenuation, range restriction, and outliers
- Correlation vs causation, one more time

---
## Pearson, Spearman, Kendall

![three_correlations](svg/courses/math/statistics-inference/09_correlation_analysis/three_correlations.svg)

---
## Pearson Correlation, Recapped

- r measures the strength of a **linear** relationship between two numeric variables, on [&minus;1, +1]
- It's the covariance divided by the product of the two SDs — units cancel out
- r&sup2; is the fraction of variance the linear fit shares — r = 0.6 means ~36%, not 60%
- r is symmetric in x and y, and unchanged by linear rescaling of either
- It is *blind* to non-linear relationships and *very* sensitive to outliers — always plot the scatter

---
## Inference On r

- The sample r estimates the population correlation &rho;; we can test and bound &rho;
- H&#8320;: &rho; = 0 — there's a t-test for this with n&minus;2 df (the one `scipy.stats.pearsonr` reports)
- For confidence intervals, use **Fisher's z-transformation**: z = arctanh(r) is approximately normal with SD 1/&radic;(n&minus;3); build the interval there, then transform back
- Assumptions for the test: bivariate normality (or large n), independent observations
- A "significant" r of 0.05 in a million-row dataset is real and useless — report the value, not just the p

---
## Spearman And Kendall

- **Spearman's &rho;**: Pearson correlation computed on the *ranks* — measures any **monotonic** relationship, not just linear
- **Kendall's &tau;**: based on concordant vs discordant pairs — also monotonic, more robust to outliers, with a cleaner probabilistic meaning, but slower to compute
- Both are resistant to outliers and valid for ordinal data
- Use them when the relationship is monotonic-but-curved, the data is ranked, or outliers are a worry
- If Pearson and Spearman disagree a lot, suspect non-linearity or outliers — and go look at the plot

---
## Partial And Semi-Partial Correlation

- A raw correlation between X and Y can be entirely due to a third variable Z driving both
- **Partial correlation** r_{XY&middot;Z}: the correlation between X and Y after removing Z's linear influence from *both*
- **Semi-partial (part) correlation**: removes Z from one of them only — used in regression to gauge a predictor's unique contribution
- It's the right tool when you suspect a confounder and have measured it
- Caveat: it only controls for the variables you *included* — unmeasured confounders still lurk

---
## Partial Correlation Explained

![partial_correlation](svg/courses/math/statistics-inference/09_correlation_analysis/partial_correlation.svg)

---
## The Correlation Matrix

- For p variables, the p&times;p table of pairwise correlations — a quick map of relationships
- Read it before modeling: spot redundant predictors, candidate confounders, surprising links
- Pitfalls: with p variables you have p(p&minus;1)/2 correlations &#8594; many "significant by chance" — don't go fishing
- High pairwise correlations among predictors warn of **multicollinearity** in upcoming regression
- A heatmap of the matrix is far more readable than the raw numbers

---
## What Quietly Distorts Correlations

- **Outliers**: a single point can create a correlation from noise or destroy a real one
- **Range restriction**: if you only see a narrow slice of X (e.g. only hired applicants), r shrinks toward 0 — the relationship is still there, you've just truncated the evidence
- **Measurement error (attenuation)**: noisy measurements pull r toward 0 — the *true* correlation is larger than the observed one
- **Aggregation**: correlations computed on group averages are usually much higher than on individuals (ecological correlation) — don't transfer one to the other
- **Non-linearity**: r &asymp; 0 can hide a strong U-shape — Pearson simply can't see it

---
## Correlation Is Not Causation

- X&ndash;Y correlated permits four stories: X&#8594;Y, Y&#8594;X, a common cause Z&#8594;X and Z&#8594;Y, or coincidence
- Partial correlation rules out *measured* confounders only — never the unmeasured ones
- Causation needs a randomized experiment, or a credible causal-inference design (instrumental variables, regression discontinuity, difference-in-differences)
- In observational data, the honest verb is "associated with", not "causes" or "leads to"
- "Controlling for covariates" strengthens a causal *argument*; it does not, by itself, establish causation

---
## Correlation Analysis In Python

```python
import numpy as np, pandas as pd
from scipy import stats
rng = np.random.default_rng(7)
z = rng.normal(0, 1, 200)
x = z + rng.normal(0, 0.5, 200)
y = z + rng.normal(0, 0.5, 200)        # x,y correlated only via z
print("Pearson r(x,y):", round(stats.pearsonr(x, y).statistic, 2))
print("Spearman    :", round(stats.spearmanr(x, y).statistic, 2))
# partial correlation of x,y given z = correlation of their residuals
rx = x - np.polyval(np.polyfit(z, x, 1), z)
ry = y - np.polyval(np.polyfit(z, y, 1), z)
print("partial r(x,y | z):", round(stats.pearsonr(rx, ry).statistic, 2))   # ~0
```

---
## Common Mistakes

- Reporting Pearson r without plotting the scatter (missing non-linearity or an outlier)
- Treating a "significant" tiny r in a huge dataset as meaningful
- Reading a correlation as causation, or as "controlled" when key confounders weren't measured
- Comparing a correlation of group averages to one of individuals
- Forgetting that range restriction and measurement error bias r *toward zero* — the truth may be stronger
