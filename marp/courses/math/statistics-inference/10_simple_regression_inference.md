---
tags:
  - math:regression
level: intermediate
category: math
audience:
  - audiences:data-analysts
  - audiences:data-scientists

---

# Simple Linear Regression: Inference

---

## What This Chapter Covers

- The regression model and its assumptions
- Least squares and what it estimates
- Standard errors, t-tests, and confidence intervals for the coefficients
- Confidence intervals vs prediction intervals
- Residual diagnostics
- Transformations and the limits of a straight line

---

## Confidence vs Prediction Interval

![ci_vs_pi](svg/courses/math/statistics-inference/10_simple_regression_inference/ci_vs_pi.svg)

---

## The Model

- y = &beta;&#8320; + &beta;&#8321;x + &epsilon; — a true line plus random noise &epsilon;
- &beta;&#8320; (intercept) and &beta;&#8321; (slope) are the population parameters we estimate
- The noise &epsilon; is assumed to have mean 0, constant variance &sigma;&sup2;, and to be independent across observations (and roughly normal, for small-sample inference)
- We observe noisy points and want to recover (and bound) &beta;&#8320; and &beta;&#8321;, and predict new y's
- "Simple" = one predictor; the next chapter does many

---

## Least Squares

- The fitted line minimizes the sum of **squared vertical residuals** &Sigma;(y&#7522; &minus; y&#770;&#7522;)&sup2;
- Closed-form solution: slope b&#8321; = (covariance of x, y) / (variance of x); intercept b&#8320; = y&#772; &minus; b&#8321;x&#772;
- Under the model assumptions, b&#8320; and b&#8321; are **unbiased** and have the smallest variance among linear unbiased estimators (Gauss&ndash;Markov)
- They're also the maximum-likelihood estimates when the noise is normal
- Squared residuals make the math clean — but also make the fit sensitive to outliers

---

## Inference On The Slope

- Each coefficient has a **standard error** — how much it would vary across repeated samples
- SE of the slope shrinks with more data, with more spread in x, and with less noise (smaller residual SD)
- **t-test**: t = b&#8321; / SE(b&#8321;), df = n&minus;2 — H&#8320;: &beta;&#8321; = 0 (x carries no linear information about y)
- **Confidence interval**: b&#8321; &plusmn; t&#8901;&middot;SE(b&#8321;) — the plausible range for "change in y per unit of x"
- Report the slope and its CI as the headline; "slope = 3.2 [2.1, 4.3]" beats "p &lt; 0.001"

---

## The Regression F-Test And R&sup2;

- For simple regression the model F-test is just the square of the slope's t-test — same p-value
- **R&sup2;** = fraction of y's variance the line explains, 0 to 1; equals r&sup2; here
- High R&sup2; doesn't mean the model is *right* — it can be high with a curved relationship the line is faking
- Low R&sup2; doesn't mean the slope is meaningless — a real, precisely estimated small effect can have low R&sup2;
- Look at R&sup2;, the slope's CI, *and* the residual plots — no single number suffices

---

## Confidence Interval vs Prediction Interval

- **Confidence interval for the mean response** at x&#8320;: where the *average* y sits for that x — narrow, shrinks as n grows
- **Prediction interval for a new observation** at x&#8320;: where a *single new* y will land — always wider, because it includes the irreducible noise &sigma; on top of estimation error
- They're routinely confused; the prediction interval is the one you want for "what will the next one be?"
- Both fan out as x&#8320; moves away from x&#772; — you're least sure at the edges of your data
- Never report a fitted value without one of these intervals attached

---

## Residual Diagnostics

- The residuals are where the model's sins show up — always plot them
- **Residuals vs fitted**: want a shapeless band around 0. A curve &#8594; non-linearity. A funnel &#8594; non-constant variance
- **Q-Q plot of residuals**: roughly straight &#8594; normality is fine for the small-sample inference
- **Residuals vs order / time**: a pattern &#8594; the observations aren't independent (autocorrelation)
- **Leverage and Cook's distance**: flag points that single-handedly steer the fit — investigate, don't auto-delete

---

## Four Residual Patterns

![residual_diagnostics](svg/courses/math/statistics-inference/10_simple_regression_inference/residual_diagnostics.svg)

---

## Transformations And The Line's Limits

- Curved relationship? Try a **log transform** of y, of x, or both — `log(y) ~ log(x)` fits a power law as a line
- Non-constant variance often improves under a log or square-root transform of y
- y is a count or a 0/1 outcome? A straight line is the wrong model — use Poisson or logistic regression (next chapters)
- Extreme outliers? Robust regression, or fix the data — don't just hope
- **Never extrapolate** far beyond the observed range of x; the line is a local approximation, not a law of nature

---

## Regression Inference In Python

```python
import numpy as np, statsmodels.api as sm
rng = np.random.default_rng(8)
x = rng.uniform(0, 10, 60)
y = 2.0 + 1.5*x + rng.normal(0, 2, 60)
X = sm.add_constant(x)
fit = sm.OLS(y, X).fit()
print(fit.summary().tables[1])                 # coefficients, SEs, t, p, 95% CI
pred = fit.get_prediction(sm.add_constant([5.0]))
print("mean CI :", pred.conf_int())             # CI for mean response at x=5
print("pred PI :", pred.conf_int(obs=True))     # prediction interval, wider
```

---

## Common Mistakes

- Reporting only a p-value when the slope and its confidence interval are the real result
- Confusing a confidence interval for the mean response with a prediction interval for a new point
- Trusting a high R&sup2; without ever looking at the residual plots
- Extrapolating the fitted line outside the range of x you actually observed
- Letting a couple of high-leverage outliers quietly determine the slope
