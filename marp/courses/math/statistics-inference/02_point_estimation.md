---
tags:
  - math:estimation
level: intermediate
category: math
audience:
  - audiences:data-analysts
  - audiences:data-scientists

---

# Point Estimation

---

## What This Chapter Covers

- Estimators as recipes, estimates as numbers
- Bias, variance, and mean squared error
- Consistency
- The method of moments
- Maximum likelihood estimation
- Standard errors of estimators

---

## Bias / Variance Tradeoff

![bias_variance](svg/courses/math/statistics-inference/02_point_estimation/bias_variance.svg)

---

## Estimator vs Estimate

- An **estimator** is a rule — a function of the sample — like "take the sample mean"
- An **estimate** is the number you get when you feed in a particular sample
- The estimator is a random variable (it varies sample to sample); the estimate is a fixed value
- We judge estimators by their *behavior over many samples*, not by one estimate
- "x&#772; is an estimator of &mu;" — and a good one, as we'll see

---

## Bias

- The **bias** of an estimator is E[estimator] &minus; (true parameter): on average, does it hit the target?
- **Unbiased**: average over all samples equals the true value (the sample mean is unbiased for &mu;)
- The sample variance with n in the denominator is *biased* low; dividing by n&minus;1 fixes it
- Unbiasedness is nice but not sacred — a slightly biased estimator with much smaller variance can be better
- "Unbiased" is a statement about the long-run average, not about your one estimate

---

## Variance And Mean Squared Error

- The **variance** of an estimator measures how much it bounces around from sample to sample
- **Mean squared error (MSE)** = variance + bias&sup2; — the single number that captures both
- The **bias&ndash;variance tradeoff**: you can sometimes trade a little bias for a lot less variance and win on MSE
- This tradeoff is everywhere in statistics and machine learning (regularization, shrinkage)
- Prefer the estimator with the smaller MSE for *your* sample size

---

## Consistency

- An estimator is **consistent** if it converges to the true parameter as n &#8594; &infin;
- Informally: feed it enough data and it gets arbitrarily close
- The sample mean is consistent (law of large numbers); so are most sensible estimators
- A *biased* estimator can still be consistent if the bias shrinks to zero (like the n-denominator variance)
- Consistency is a minimum bar — an inconsistent estimator is broken; "consistent" alone doesn't make one good at small n

---

## The Method Of Moments

- Idea: set sample moments equal to theoretical moments, solve for the parameters
- One parameter? Set the sample mean equal to the model's mean and solve
- Two parameters? Add the second moment (variance) and solve the pair
- Pros: simple, always gives *an* answer; Cons: often less efficient than maximum likelihood
- A solid fallback when the likelihood is awkward, and a good starting point for iterative methods

---

## Maximum Likelihood Estimation

- The **likelihood** is the probability of the observed data, viewed as a function of the parameters
- The **MLE** is the parameter value that makes the observed data most probable
- Usually found by maximizing the *log*-likelihood (sums beat products numerically)
- Properties under regularity conditions: consistent, asymptotically unbiased, asymptotically normal, and asymptotically efficient (smallest possible variance)
- The default estimation principle behind logistic regression, GLMs, and much of modern statistics

---

## Standard Errors

- An estimate without a standard error is half a result
- The **standard error** is the standard deviation of the estimator's sampling distribution — its "give or take"
- Closed-form for the mean (s/&radic;n); for MLEs, from the curvature of the log-likelihood (the Fisher information)
- When formulas are hard, the **bootstrap** estimates the standard error by resampling
- Report estimate &plusmn; (a multiple of) the standard error, or the matching interval

---

## The Cramér-Rao Bound

![cramer_rao](svg/courses/math/statistics-inference/02_point_estimation/cramer_rao.svg)

---

## Estimation In Python

```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(1)
data = rng.gamma(shape=2.0, scale=3.0, size=500)

# method of moments for the gamma: shape = mean^2/var, scale = var/mean
m, v = data.mean(), data.var(ddof=1)
print("MoM  shape, scale:", m**2/v, v/m)
print("MLE  shape, _, scale:", stats.gamma.fit(data, floc=0))   # MLE via scipy
boot = [stats.gamma.fit(rng.choice(data, len(data), True), floc=0)[0]
        for _ in range(300)]
print("SE of shape (bootstrap):", np.std(boot, ddof=1))
```

---

## Common Mistakes

- Confusing the estimator (a procedure) with the estimate (a number)
- Insisting on unbiasedness when a biased estimator has far smaller MSE
- Treating "consistent" as "good for my sample size"
- Maximizing the likelihood instead of the log-likelihood and hitting numerical trouble
- Reporting an estimate with no standard error or interval
