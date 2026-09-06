---
tags:
  - math:regression
level: beginner
category: math
audience:
  - audiences:data-analysts
  - audiences:developers

---

# Correlation and Simple Regression

---

## What This Chapter Covers

- Covariance and the correlation coefficient
- What r does and doesn't tell you
- Correlation is not causation
- Fitting a line: simple linear regression
- Interpreting the slope, intercept, and R&sup2;
- Residuals, and when the line is the wrong model

---

## What Different Correlations Look Like

![correlations](svg/courses/math/statistics-applied/13_correlation_and_regression/correlations.svg)

---

## Two Variables Moving Together

- Do taller people weigh more? Does ad spend track revenue?
- **Covariance** measures whether two variables move together — but its units are weird
- **Correlation** r rescales covariance to a clean [&minus;1, +1]
- r &gt; 0: they tend to rise together; r &lt; 0: one rises as the other falls; r &asymp; 0: no *linear* relation
- |r| near 1 means the points hug a straight line

---

## What r Tells You — And Doesn't

- r measures the strength of a *linear* relationship — only linear
- A perfect parabola can have r &asymp; 0; r near 0 does not mean "unrelated"
- r is dimensionless and unaffected by rescaling units
- r&sup2; is the fraction of variance "explained" — r = 0.7 means ~49%, not 70%
- One outlier can manufacture or destroy a correlation — always plot the scatter

---

## Correlation Is Not Causation

- A&ndash;B correlated could mean: A causes B, B causes A, a third thing C causes both, or coincidence
- Ice cream sales correlate with drownings — both driven by hot weather
- Establishing causation needs an experiment (randomization) or careful causal design
- "Controlling for" variables in observational data helps but rarely settles it
- State correlations *as* correlations; don't smuggle in causal language

---

## Fitting A Line

- **Simple linear regression**: y &asymp; b&#8320; + b&#8321;x — predict y from x with a straight line
- "Least squares" picks the line that minimizes the sum of squared vertical gaps (residuals)
- b&#8321; is the **slope**: expected change in y per one-unit increase in x
- b&#8320; is the **intercept**: predicted y when x = 0 (often not meaningful on its own)
- It's the simplest predictive model and the foundation for everything fancier

---

## Regression Line and Residuals

![regression_residuals](svg/courses/math/statistics-applied/13_correlation_and_regression/regression_residuals.svg)

---

## Reading The Output

- **Slope**: "each extra $1k of ad spend is associated with ~$3.2k more revenue" — *associated with*, not "causes"
- **p-value on the slope**: is the slope distinguishable from zero?
- **R&sup2;**: fraction of y's variance the line accounts for — 0 (useless) to 1 (perfect)
- **Confidence interval on the slope**: the plausible range for that per-unit effect
- High R&sup2; with a meaningless model still predicts badly out of sample — beware

---

## Residuals Tell The Truth

- A **residual** is actual y minus predicted y — what the line missed
- Plot residuals vs the fitted values: you want a shapeless cloud around zero
- A curve in the residuals &#8594; the relationship isn't linear; transform x or use a curve
- A funnel shape &#8594; non-constant variance; standard errors are off
- Big isolated residuals &#8594; outliers worth investigating

---

## When The Line Is Wrong

- Clearly curved relationship — fit a polynomial or transform a variable
- y is a count or a 0/1 outcome — use Poisson or logistic regression instead
- Extreme outliers dominating the fit — robust regression, or fix the data
- Extrapolating far outside the range of x you actually observed — don't
- Time series with trend and autocorrelation — needs time-series methods

---

## Correlation And Regression In Python

```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(3)
x = rng.uniform(0, 10, 50)
y = 2.0 + 1.5*x + rng.normal(0, 2, 50)
r, p_r = stats.pearsonr(x, y)
res = stats.linregress(x, y)
print(f"r = {r:.2f}  (r^2 = {r**2:.2f})")
print(f"y = {res.intercept:.2f} + {res.slope:.2f}*x   slope p = {res.pvalue:.1e}")
```

---

## Common Mistakes

- Reading a correlation as a cause
- Concluding "no relationship" from r &asymp; 0 without plotting (it might be curved)
- Quoting r when you mean r&sup2; (explained variance)
- Trusting a fit without ever looking at the residuals
- Extrapolating the line well outside the observed range of x
