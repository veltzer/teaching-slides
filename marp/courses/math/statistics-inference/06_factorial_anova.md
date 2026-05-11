---
tags:
  - math:hypothesis-testing
level: intermediate
category: math
audience:
  - audiences:data-analysts
  - audiences:data-scientists

---
# Factorial ANOVA and Interactions

---
## What This Chapter Covers

- Two or more factors at once
- Main effects vs interaction effects
- Reading an interaction plot
- Balanced vs unbalanced designs and the "type" of sums of squares
- Repeated-measures designs
- ANCOVA: adding a continuous covariate

---
## Interaction Plots

![interaction_plots](svg/courses/math/statistics-inference/06_factorial_anova/interaction_plots.svg)

---
## Why More Than One Factor

- Real outcomes depend on several things at once: layout *and* device, drug *and* dose, region *and* season
- Testing one factor at a time misses how they combine — and wastes data
- A **factorial design** crosses every level of every factor: 2 layouts &times; 3 devices = 6 cells
- One experiment then answers: does layout matter? does device matter? do they interact?
- More efficient and more informative than a pile of one-factor studies

---
## Main Effects vs Interaction

- A **main effect** is the average effect of one factor, collapsing over the others — "on average, layout B beats A by 4 points"
- An **interaction** means the effect of one factor *depends on the level of another* — "B beats A on desktop but loses on mobile"
- When an interaction is present, the main effects can be misleading on their own — always interpret the interaction first
- No interaction &#8594; the factors act additively; you can talk about each separately
- Factorial ANOVA gives an F-test for each main effect *and* for each interaction

---
## Reading An Interaction Plot

- Plot the cell means: one factor on the x-axis, separate lines for the other factor's levels
- **Parallel lines** &#8594; no interaction (the gap between lines is constant)
- **Non-parallel / crossing lines** &#8594; interaction (the effect changes, or even reverses)
- This single plot is usually more informative than the F-table
- Always draw it before writing the interpretation

---
## Balanced vs Unbalanced

- **Balanced**: equal sample size in every cell — the sums of squares partition cleanly and the analysis is unambiguous
- **Unbalanced**: unequal cell sizes (the common real-world case) — the factors' contributions overlap, so order of entry matters
- Hence "types" of sums of squares: **Type I** (sequential, order-dependent), **Type II** (each effect after the other main effects), **Type III** (each effect after everything else, including interactions)
- For unbalanced data with interactions, Type II or III is standard — know which your software uses (R's `aov` defaults to Type I; `statsmodels` lets you pick)
- Design balanced if you possibly can; it sidesteps the whole issue

---
## Types I / II / III Sums of Squares

![types_of_ss](svg/courses/math/statistics-inference/06_factorial_anova/types_of_ss.svg)

---
## Repeated-Measures Designs

- The same subjects are measured under every condition (within-subjects), not different subjects per condition
- Like the paired t-test generalized — removes between-subject variability, big power gain
- But observations within a subject are correlated, so plain ANOVA's independence assumption fails
- Use **repeated-measures ANOVA** (with a sphericity check / Greenhouse&ndash;Geisser correction) or, better, a **linear mixed-effects model** with a random subject effect
- Mixed models also handle missing cells and unequal numbers of observations gracefully

---
## ANCOVA

- **Analysis of covariance**: factorial ANOVA plus one (or more) continuous **covariate**
- The covariate (a pre-test score, baseline value, age) soaks up nuisance variation &#8594; smaller error variance &#8594; more power
- It also adjusts group comparisons for differences in the covariate — useful when randomization wasn't perfect
- Key assumption: the covariate's slope is the same in every group (no covariate&times;factor interaction) — check it
- In the linear-model view it's just `y ~ C(group) + covariate` — nothing new under the hood

---
## It's Still The Linear Model

- Two-way ANOVA, repeated measures, ANCOVA, unbalanced designs — all special cases of the linear (or linear mixed) model
- Practically: write a model formula, fit it, read the ANOVA table and the coefficients, check residuals
- `statsmodels` formula API: `y ~ C(A) * C(B)` expands to A, B, and the A:B interaction
- Random effects (subjects, sites) go through mixed-model tools (`statsmodels` `mixedlm`, or R's `lme4`)
- Learn the linear-model lens once and the zoo of ANOVA designs collapses into it

---
## Factorial ANOVA In Python

```python
import numpy as np, pandas as pd, statsmodels.api as sm
from statsmodels.formula.api import ols
rng = np.random.default_rng(5)
rows = []
for layout in ("A", "B"):
    for device in ("desktop", "mobile"):
        base = {"A": 100, "B": 104}[layout] + (3 if device == "desktop" else -5)*(layout == "B")
        rows += [{"layout": layout, "device": device, "y": v}
                 for v in rng.normal(base, 8, 50)]
df = pd.DataFrame(rows)
model = ols("y ~ C(layout) * C(device)", df).fit()
print(sm.stats.anova_lm(model, typ=2))     # main effects + interaction
```

---
## Common Mistakes

- Interpreting main effects while ignoring a real interaction
- Skipping the interaction plot and reasoning from the F-table alone
- Using Type I sums of squares on unbalanced data without realizing order matters
- Running plain ANOVA on repeated-measures data (correlated observations)
- Forgetting to check the equal-slopes assumption in ANCOVA
