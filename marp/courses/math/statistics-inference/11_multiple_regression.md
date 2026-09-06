---
tags:
  - math:regression
level: intermediate
category: math
audience:
  - audiences:data-analysts
  - audiences:data-scientists

---

# Multiple Regression

---

## What This Chapter Covers

- Extending regression to many predictors
- Interpreting coefficients "holding the others constant"
- Categorical predictors and interactions
- Multicollinearity
- Adjusted R&sup2;, model selection, and overfitting
- Diagnostics specific to the multivariable case

---

## Multicollinearity (VIF)

![multicollinearity_vif](svg/courses/math/statistics-inference/11_multiple_regression/multicollinearity_vif.svg)

---

## More Than One Predictor

- y = &beta;&#8320; + &beta;&#8321;x&#8321; + &beta;&#8322;x&#8322; + ... + &beta;&#8345;x&#8345; + &epsilon;
- Fit by least squares, exactly as before — just with several slopes to estimate at once
- Each &beta;&#8332; has a standard error, a t-test (H&#8320;: that coefficient is 0), and a confidence interval
- The model F-test now asks "do *any* of the predictors help?"; the per-coefficient t-tests ask about each one individually
- Same machinery as simple regression, more dials

---

## Interpreting A Coefficient

- &beta;&#8332; is the expected change in y for a one-unit increase in x&#8332; **holding all other predictors fixed**
- That conditional clause is everything — a coefficient can flip sign once other variables are in the model (this is exactly Simpson's paradox in regression form)
- It's an *associational* statement within this model and this dataset, not a causal one
- A predictor's coefficient depends on which *other* predictors are present — there is no "the" effect of x&#8332; in isolation
- Always interpret coefficients in the context of the full model, never one at a time as if alone

---

## Categorical Predictors And Interactions

- A categorical variable with k levels enters as k&minus;1 **dummy (indicator)** variables; one level is the baseline, and each coefficient is "this level vs the baseline"
- This is why one-way ANOVA *is* a regression with a categorical predictor
- An **interaction** term x&#8321;&middot;x&#8322; lets the slope on x&#8321; depend on x&#8322; — fit it when you believe the effects aren't additive
- Interaction present &#8594; don't interpret the main-effect coefficients alone (their meaning becomes "effect when the other variable is 0")
- Center continuous predictors before forming interactions — it makes the main-effect coefficients interpretable

---

## Multicollinearity

- Predictors that are highly correlated with *each other* carry overlapping information
- Symptom: the model fits fine and predicts fine, but individual coefficients become unstable — huge standard errors, wild signs, big swings when you add/drop a variable
- Diagnose with the **variance inflation factor (VIF)**: VIF > ~5&ndash;10 on a predictor flags trouble
- Remedies: drop one of the redundant predictors, combine them (e.g. an index), or use ridge regression (shrinkage)
- It hurts *interpretation of individual coefficients*, not prediction — if you only care about predictions, you may not need to act

---

## Adjusted R&sup2; And Overfitting

- Plain **R&sup2; only ever goes up** when you add predictors — even pure-noise ones — so it can't be used to compare models of different sizes
- **Adjusted R&sup2;** penalizes for the number of predictors; it can go *down* when you add a useless one — use it for comparison
- **AIC** and **BIC** balance fit against complexity (BIC penalizes size more harshly) — lower is better
- Real overfitting check: hold out data, or use cross-validation, and compare *test* error — in-sample R&sup2; is optimistic
- A model that nails the training data and flops on new data has learned noise, not signal

---

## Model Selection — Carefully

- Stepwise selection (forward/backward by p-value) is convenient and statistically dangerous: it inflates R&sup2;, biases coefficients, and produces p-values that no longer mean what they say
- Better: choose predictors from domain knowledge; compare a *small* number of pre-specified models by cross-validated error or AIC/BIC
- For prediction with many candidate predictors, **regularization** (LASSO for selection, ridge for shrinkage, elastic net for both) is the principled route
- Whatever you do, validate on data the selection never saw
- "We tried 40 predictor combinations and report the best one's p-values" is p-hacking in a lab coat

---

## Diagnostics For Multiple Regression

- All the simple-regression diagnostics still apply: residuals vs fitted (linearity, equal variance), Q-Q plot (normality), residuals vs order (independence)
- **Partial regression (added-variable) plots**: show each predictor's relationship with y *after* adjusting for the others — the right way to eyeball one coefficient
- **Leverage, Cook's distance, DFBETAS**: identify points that disproportionately move the fit or a specific coefficient
- Check **VIFs** for multicollinearity as a matter of routine
- A clean coefficient table over un-checked residuals is a trap

---

## Multiple Regression In Python

```python
import numpy as np, pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor
rng = np.random.default_rng(9)
n = 200
df = pd.DataFrame({"x1": rng.normal(size=n), "x2": rng.normal(size=n)})
df["x3"] = df.x1 + rng.normal(0, 0.1, n)               # nearly collinear with x1
df["y"]  = 1 + 2*df.x1 - 1.5*df.x2 + rng.normal(0, 1, n)
fit = smf.ols("y ~ x1 + x2 + x3", df).fit()
print(fit.summary().tables[1])
X = np.column_stack([np.ones(n), df.x1, df.x2, df.x3])
print("VIFs:", [round(variance_inflation_factor(X, i), 1) for i in range(1, 4)])
```

---

## Adjusted R² vs Plain R²

![r2_vs_adjusted](svg/courses/math/statistics-inference/11_multiple_regression/r2_vs_adjusted.svg)

---

## Common Mistakes

- Interpreting a coefficient without the "holding the others constant" caveat (sign flips will surprise you)
- Comparing models by plain R&sup2; instead of adjusted R&sup2; / AIC / cross-validated error
- Running stepwise selection and then trusting the resulting p-values
- Ignoring multicollinearity and puzzling over unstable, wrong-signed coefficients
- Reporting a coefficient table without checking residuals, leverage, and VIFs
