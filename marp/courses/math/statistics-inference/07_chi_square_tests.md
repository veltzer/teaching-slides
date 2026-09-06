---
tags:
  - math:hypothesis-testing
level: intermediate
category: math
audience:
  - audiences:data-analysts
  - audiences:data-scientists

---

# Chi-Square Tests

---

## What This Chapter Covers

- Categorical data and contingency tables
- The chi-square goodness-of-fit test
- The chi-square test of independence
- Expected counts and the assumptions
- Fisher's exact test for small samples
- Effect size for categorical associations

---

## A Contingency Table

![contingency_table](svg/courses/math/statistics-inference/07_chi_square_tests/contingency_table.svg)

---

## When The Data Is Counts In Categories

- No means here — just *how many* fall in each category: browsers, plan tiers, pass/fail, region
- Organized as a frequency table (one row) or a **contingency table** (rows &times; columns)
- The questions: does the distribution match what we expected? are two categorical variables related?
- The chi-square family answers both by comparing **observed** counts to **expected** counts
- Statistic: &chi;&sup2; = &Sigma; (observed &minus; expected)&sup2; / expected — sum over all cells

---

## Goodness-Of-Fit Test

- One categorical variable; H&#8320;: the category proportions equal a specified set (e.g. "die is fair: 1/6 each", "traffic split is 25/25/25/25")
- Expected count per cell = (total n) &times; (hypothesized proportion)
- Compare &chi;&sup2; to a chi-square distribution with (k &minus; 1) degrees of freedom (k = number of categories)
- Big &chi;&sup2; &#8594; small p &#8594; observed counts don't match the claimed proportions
- Use it for: dice fairness, "does our user mix match the population", checking a randomizer

---

## Test Of Independence

- Two categorical variables in a contingency table; H&#8320;: the two variables are **independent** (no association)
- Expected count for a cell = (row total &times; column total) / grand total — what you'd see if rows and columns were unrelated
- Degrees of freedom = (rows &minus; 1) &times; (columns &minus; 1)
- Big &chi;&sup2; &#8594; the variables are associated — e.g. plan tier is related to churn, device is related to conversion
- A **test of homogeneity** (do several groups have the same category distribution?) uses the identical arithmetic — just a different sampling story

---

## Expected Counts And Assumptions

- **Independence** of observations — each unit counted once, no repeated measures
- The chi-square approximation needs **expected counts that aren't tiny**: rule of thumb, all expected &geq; 5 (a few &geq; ~1 is tolerable)
- It uses the *expected* counts for this rule, not the observed ones — check after computing the expected table
- Small expected counts &#8594; the approximation is poor &#8594; use **Fisher's exact test** instead
- For 2&times;2 tables some software applies **Yates' continuity correction**; it's conservative — fine to report, or just use Fisher

---

## Fisher's Exact Test

- Computes the *exact* probability of the observed table (and more extreme ones) given the margins — no large-sample approximation
- The go-to when expected counts are small, classically for 2&times;2 tables (now feasible for larger ones too)
- More conservative than chi-square; gives a trustworthy p-value when chi-square's would be unreliable
- No "minimum count" requirement — that's the whole point
- `scipy.stats.fisher_exact` for 2&times;2; `scipy.stats.chi2_contingency` warns you when counts are small

---

## Chi-Square vs Fisher's Exact

![chi_vs_fisher](svg/courses/math/statistics-inference/07_chi_square_tests/chi_vs_fisher.svg)

---

## Effect Size For Categorical Data

- &chi;&sup2; itself grows with sample size — a huge n makes trivial associations "significant"
- **Phi (&phi;)** for 2&times;2 tables: &radic;(&chi;&sup2;/n) — behaves like a correlation, 0 to 1
- **Cramér's V** for larger tables: &radic;(&chi;&sup2; / (n &times; min(rows&minus;1, cols&minus;1))) — 0 (no association) to 1 (perfect)
- For 2&times;2 you can also report the **odds ratio** or **risk ratio** — often the most interpretable
- Always pair the p-value with one of these; "significant" without a magnitude is half a result

---

## Chi-Square Tests In Python

```python
import numpy as np
from scipy import stats
# goodness of fit: is the 4-way traffic split even? observed 240/260/255/245
obs = np.array([240, 260, 255, 245])
print("GoF p:", stats.chisquare(obs, f_exp=np.full(4, obs.sum()/4)).pvalue)

# independence: device (rows) vs converted? (cols)
table = np.array([[200, 1800],     # desktop: yes, no
                  [150, 2350]])    # mobile : yes, no
chi2, p, dof, expected = stats.chi2_contingency(table)
V = np.sqrt(chi2 / (table.sum() * (min(table.shape) - 1)))
print(f"independence p = {p:.3g}, Cramer's V = {V:.3f}")
print("exact (2x2):", stats.fisher_exact(table)[1])    # cross-check
```

---

## Common Mistakes

- Running chi-square when several expected counts are below ~5 instead of Fisher's exact test
- Checking the *observed* counts against the "&geq; 5" rule instead of the *expected* counts
- Using chi-square on data where the same unit appears in several cells (non-independence)
- Reporting a "significant" &chi;&sup2; with no Cramér's V / odds ratio — significance grows with n
- Confusing the test of independence with comparing means — it's about category counts only
