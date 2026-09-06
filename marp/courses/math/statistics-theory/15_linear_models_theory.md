---
tags:
  - math:regression
level: advanced
category: math
audience:
  - audiences:data-scientists
  - audiences:ml-engineers

---

# Linear Models Theory

---

## What This Chapter Covers

- The linear model in matrix form
- Least squares as orthogonal projection
- The Gauss&ndash;Markov theorem
- Distribution theory under normality
- F-tests, the general linear hypothesis, and the geometry of ANOVA
- Diagnostics, generalized least squares, and ridge/Stein shrinkage

---

## OLS As Orthogonal Projection

![linear model geometry](svg/courses/math/statistics-theory/15_linear_models_theory/linear_model_geometry.svg)

---

## The Linear Model In Matrix Form

- **y = X&beta; + &epsilon;**: y &isin; &#8477;&#8319; the response, X the n&times;p **design matrix** (columns = predictors; usually a column of 1s for the intercept), &beta; &isin; &#8477;&#7510; the unknown coefficients, &epsilon; the random error
- Core (Gauss&ndash;Markov) assumptions: **E[&epsilon;] = 0**, **Cov(&epsilon;) = &sigma;&sup2;I** (errors mean-zero, *homoscedastic and uncorrelated*), and X **fixed and of full column rank** p (so X&#7488;X is invertible — no exact collinearity). Normality of &epsilon; is *added* only for exact distribution theory, not for unbiasedness
- "Linear" means linear *in &beta;* — polynomials, interactions, dummy variables, splines all fit ( the column space of X is what matters, not the shape of the original predictors )
- This single template is the **general linear model**: simple and multiple regression, one-way and factorial ANOVA, ANCOVA, polynomial regression — pick the design matrix and the rest of the theory is identical
- Everything below is geometry in &#8477;&#8319;: y is a point, the columns of X span a p-dimensional **model subspace** C(X), and estimation is "find the point of C(X) closest to y"

---

## Least Squares As Orthogonal Projection

- The OLS estimator minimizes &#8214;y &minus; X&beta;&#8214;&sup2;; setting the gradient to zero gives the **normal equations** X&#7488;X&beta;&#770; = X&#7488;y, hence **&beta;&#770; = (X&#7488;X)&#8315;&sup1;X&#7488;y** (full rank); the **fitted values** are ŷ = X&beta;&#770; = **Hy**, where **H = X(X&#7488;X)&#8315;&sup1;X&#7488;** is the **hat matrix**
- H is the **orthogonal projection onto C(X)**: it's symmetric and idempotent (H&sup2; = H), so ŷ is the foot of the perpendicular from y to the model subspace, and the **residual vector** e = y &minus; ŷ = (I &minus; H)y lies in the orthogonal complement — **e &#8869; C(X)** (in particular e &#8869; every column of X, which is why residuals "sum to zero" when there's an intercept)
- **Pythagoras** in &#8477;&#8319; gives the ANOVA decomposition: &#8214;y &minus; ȳ𝟙&#8214;&sup2; = &#8214;ŷ &minus; ȳ𝟙&#8214;&sup2; + &#8214;e&#8214;&sup2;, i.e. SS_total = SS_regression + SS_residual, and **R&sup2; = &#8214;ŷ &minus; ȳ𝟙&#8214;&sup2; / &#8214;y &minus; ȳ𝟙&#8214;&sup2;** = the squared cosine of the angle between (centered) y and its fit
- The error variance is estimated by **s&sup2; = &#8214;e&#8214;&sup2; / (n &minus; p)** — divide the residual sum of squares by the **residual degrees of freedom** n &minus; p (= dimension of the orthogonal complement); this is unbiased for &sigma;&sup2;
- Rank-deficient or near-deficient X (collinearity): X&#7488;X is singular or ill-conditioned — &beta;&#770; is non-unique or wildly unstable (huge variances), though ŷ = Hy is still well-defined; remedies = drop/combine predictors, use the **pseudoinverse**, or regularize (last slide)

---

## The Gauss&ndash;Markov Theorem

- **Theorem (BLUE)**: under the core assumptions ( E[&epsilon;] = 0, Cov(&epsilon;) = &sigma;&sup2;I, X full rank ) and **without any normality assumption**, the OLS estimator &beta;&#770; is the **Best Linear Unbiased Estimator** of &beta; — among all estimators that are *linear in y* and *unbiased*, it has the smallest variance (and more strongly, the smallest covariance matrix, in the Loewner order); the same holds for any **estimable linear combination** c&#7488;&beta;
- Proof sketch: write any competing linear unbiased estimator as (X&#7488;X)&#8315;&sup1;X&#7488;y + Ay with AX = 0 (unbiasedness forces this); its covariance is &sigma;&sup2;[(X&#7488;X)&#8315;&sup1; + AA&#7488;] &succeq; &sigma;&sup2;(X&#7488;X)&#8315;&sup1;, since AA&#7488; is positive semidefinite — extra terms only add variance
- The exact covariance of the OLS estimator: **Cov(&beta;&#770;) = &sigma;&sup2;(X&#7488;X)&#8315;&sup1;**, estimated by s&sup2;(X&#7488;X)&#8315;&sup1;; the standard error of &beta;&#770;&#7522; is the square root of its diagonal entry — small when predictors are well-spread and not collinear
- The fine print on "best": only among **linear unbiased** estimators, and only when the assumptions hold. Drop them and OLS can be beaten — **heteroscedastic / correlated errors &#8658; GLS** is BLUE instead; **allowing bias &#8658; ridge / James&ndash;Stein** can dominate OLS in mean-squared error (last slide); **heavy-tailed errors &#8658;** robust (M-, quantile-) estimators are better
- Note what it does *not* claim: nothing about *which* parametrization, nothing about prediction beyond the data, and nothing requiring &epsilon; to be Normal — Gauss&ndash;Markov is a second-moment result

---

## Distribution Theory Under Normality

- **Add** &epsilon; ~ N(0, &sigma;&sup2;I). Then, because linear maps of a Gaussian are Gaussian: **&beta;&#770; ~ N( &beta;, &sigma;&sup2;(X&#7488;X)&#8315;&sup1; )** exactly, in *every* sample size
- The residual structure: **(n &minus; p) s&sup2; / &sigma;&sup2; ~ &chi;&sup2;_{n&minus;p}**, and — crucially — **&beta;&#770; and s&sup2; are independent** (the projection ŷ and the residual e live in orthogonal subspaces of a spherical Gaussian, hence are independent; this is the multivariate generalization of "X&#772; &#8869; S&sup2;", and Cochran's theorem packages it). This independence is *exactly* what makes the next line a genuine t
- Therefore each coefficient has an **exact t pivot**: ( &beta;&#770;&#7522; &minus; &beta;&#7522; ) / se(&beta;&#770;&#7522;) ~ **t_{n&minus;p}** — invert it for a confidence interval &beta;&#770;&#7522; &plusmn; t*&middot;se(&beta;&#770;&#7522;), or test &beta;&#7522; = 0; likewise c&#7488;&beta;&#770; gives an exact t for any contrast c&#7488;&beta;
- Prediction at a new x&#8320;: ŷ&#8320; = x&#8320;&#7488;&beta;&#770; ~ N( x&#8320;&#7488;&beta;, &sigma;&sup2; x&#8320;&#7488;(X&#7488;X)&#8315;&sup1;x&#8320; ); the **confidence interval for the mean response** uses that variance, the **prediction interval for a new observation** adds &sigma;&sup2; (the new &epsilon;) — always wider, and both fan out as x&#8320; leaves the data's centroid
- Large n without normality: by the CLT &beta;&#770; is *approximately* Normal anyway (under regularity), so the t-intervals are asymptotically valid — normality buys you *exactness in small samples*, the CLT covers the rest

---

## F-Tests And The Geometry Of ANOVA

- **General linear hypothesis** H&#8320;: **R&beta; = r** (R a q&times;p matrix of full row rank — encodes "these q linear restrictions on &beta;": a coefficient is zero, two are equal, a block of dummies all vanish, etc.). The test statistic is **F = [ (R&beta;&#770; &minus; r)&#7488; ( R(X&#7488;X)&#8315;&sup1;R&#7488; )&#8315;&sup1; (R&beta;&#770; &minus; r) / q ] / s&sup2;**, which under H&#8320; (and normality) is **exactly F_{q, n&minus;p}**
- The **geometric / "extra sum of squares" form**: fit the full model and the restricted (null) model, F = [ (SS_residual,restricted &minus; SS_residual,full) / q ] / [ SS_residual,full / (n&minus;p) ] — i.e. (drop in residual norm per restriction) over (residual variance); &chi;&sup2; numerator and denominator, independent (orthogonal subspaces again), so their scaled ratio is F. Special cases: q = 1 gives F = t&sup2;; "all slopes = 0" gives the overall model F = (R&sup2;/(p&minus;1)) / ((1&minus;R&sup2;)/(n&minus;p))
- **One-way ANOVA is this with R encoding "all group means equal"**: the design matrix has a dummy per group, C(X) is the space of "constant within group" vectors, the projection replaces each observation by its group mean, SS_between and SS_within are squared lengths in orthogonal subspaces — the F-test is literally the angle test between "group-mean fit" and "grand-mean fit". Factorial ANOVA = nested projections (main-effect subspace ⊂ main-effects-plus-interaction subspace), which is *why* unbalanced designs make the subspaces non-orthogonal and the "type I/II/III SS" ambiguity appear
- Sequential vs. simultaneous: adding predictors corresponds to **nesting subspaces** C(X&#8321;) ⊆ C(X&#8321;,X&#8322;) ⊆ ...; "Type I SS" decomposes &#8214;ŷ&#8214;&sup2; along this chain (order-dependent unless the columns are orthogonal), "Type III SS" tests each block last — pure linear algebra, no new statistics
- Power and non-null behavior: under the alternative the numerator follows a **non-central F** with non-centrality &lambda; = (R&beta; &minus; r)&#7488;(...)&#8315;&sup1;(R&beta; &minus; r)/&sigma;&sup2; — that's what drives sample-size / power calculations for ANOVA and regression tests

---

## Beyond OLS: Diagnostics, GLS, Shrinkage

- **Leverage** = the diagonal h&#7522;&#7522; of the hat matrix H — "how much of its own fitted value point i pulls" (0 &leq; h&#7522;&#7522; &leq; 1, &Sigma;h&#7522;&#7522; = p, so the average is p/n; flag h&#7522;&#7522; &gt; 2p/n or 3p/n). High leverage is a property of the **x**'s alone; combine it with a large residual and you get **influence** — quantified by **Cook's distance** D&#7522; (effect of deleting i on the whole &beta;&#770;) and **DFBETAS** (effect on each coefficient). Always plot residuals vs fitted (linearity, equal variance), a Q&ndash;Q plot of residuals (normality), residuals vs order (independence), and check **VIFs = 1/(1&minus;R&sup2;&#7522;)** for collinearity — *investigate* influential points, don't reflexively delete them
- **Generalized least squares (GLS)**: if Cov(&epsilon;) = &sigma;&sup2;V with V known (≠ I) — heteroscedasticity, autocorrelated/clustered errors, repeated measures — then OLS is unbiased but **no longer BLUE**; the BLUE is &beta;&#770;_GLS = (X&#7488;V&#8315;&sup1;X)&#8315;&sup1;X&#7488;V&#8315;&sup1;y (= OLS on the "whitened" data V&#8315;½y, V&#8315;½X — projection in a *re-weighted* inner product). V unknown &#8658; estimate it &#8658; **feasible GLS** (weighted least squares for pure heteroscedasticity; Cochrane&ndash;Orcutt / mixed models for correlation). Cheaper alternative: keep OLS &beta;&#770; but report **heteroscedasticity/cluster-robust ("sandwich", White/Newey&ndash;West) standard errors** — the estimator is the same, only its variance is re-estimated honestly
- **Ridge regression / shrinkage**: &beta;&#770;_ridge = (X&#7488;X + &lambda;I)&#8315;&sup1;X&#7488;y — a *biased* estimator that, for a suitable &lambda; &gt; 0, has **smaller mean-squared error than OLS** (especially when X is ill-conditioned or p is large relative to n); it's the **posterior mean under a Gaussian prior** &beta; ~ N(0, &tau;&sup2;I) (the Bayesian face of regularization) and the regression incarnation of **Stein's paradox** — pulling the OLS estimate toward 0 (or toward a common value) provably wins in p &geq; 3. LASSO (an &#8467;&#8321; penalty) does this *and* zeroes out coefficients (selection); elastic net blends both. The price of all of them: the classical exact t/F distribution theory no longer applies — inference needs bootstrap, selective-inference, or Bayesian tools
- Other escapes when assumptions break: **robust regression** (M-estimators, MM-estimators) for heavy-tailed errors / outliers; **quantile regression** when you care about a quantile (or the whole conditional distribution) rather than the mean; **GLMs** (next-level generalization: a link function + an exponential-family response) for binary, count, or positive-skewed responses — logistic and Poisson regression are the headline cases, and they reduce to *iteratively reweighted least squares*, i.e. weighted projections again
- The throughline: OLS is the **orthogonal projection** answer, optimal under the spherical-Gaussian-error story; change the error geometry &#8658; project in a different inner product (GLS); allow bias &#8658; shrink the projection (ridge/Stein); change the response type &#8658; project iteratively on a transformed scale (GLMs) — one geometric idea, many statistical models

---

## Linear Model Theory In Code

```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(14)
n, p = 80, 3
X = np.column_stack([np.ones(n), rng.normal(size=n), rng.normal(size=n)])
beta = np.array([2.0, 1.5, -0.7])
y = X @ beta + rng.normal(0, 1.5, n)

# OLS via the normal equations; H is the projection onto C(X)
XtX_inv = np.linalg.inv(X.T @ X)
b = XtX_inv @ X.T @ y
H = X @ XtX_inv @ X.T
e = y - H @ y
s2 = e @ e / (n - p)                                 # unbiased for sigma^2
se = np.sqrt(np.diag(s2 * XtX_inv))
print("beta_hat:", b.round(3), "  SE:", se.round(3))
print("t-stats :", (b/se).round(2), "  R^2:", round(1 - (e@e)/((y-y.mean())@(y-y.mean())), 3))

# F-test for H0: beta_1 = beta_2 = 0  (slopes all zero) via the extra-sum-of-squares form
b0 = y.mean(); SSR_restr = ((y - b0) @ (y - b0)); SSR_full = e @ e
F = ((SSR_restr - SSR_full) / 2) / (SSR_full / (n - p))
print(f"overall F = {F:.2f},  p = {stats.f.sf(F, 2, n - p):.2e}")

# Gauss-Markov sanity check: OLS variance matches sigma^2 (X'X)^{-1} over many samples
B = np.array([np.linalg.solve(X.T @ X, X.T @ (X @ beta + rng.normal(0, 1.5, n))) for _ in range(30_000)])
print("empirical Cov(beta_hat) diag:", B.var(axis=0).round(4),
      "  theory:", (1.5**2 * np.diag(XtX_inv)).round(4))

# ridge: biased, but smaller MSE here than OLS for beta_1, beta_2
lam = 5.0
Br = np.array([np.linalg.solve(X.T @ X + lam*np.eye(p), X.T @ (X @ beta + rng.normal(0, 1.5, n))) for _ in range(30_000)])
mse_ols   = ((B  - beta)**2).mean(axis=0)
mse_ridge = ((Br - beta)**2).mean(axis=0)
print("MSE OLS  :", mse_ols.round(4), "\nMSE ridge:", mse_ridge.round(4))
```

---

## Common Mistakes

- Forgetting that Gauss&ndash;Markov is only "best among *linear unbiased*" estimators — under heteroscedasticity/correlation GLS wins, and allowing bias (ridge/Stein) can beat OLS in MSE
- Trusting the exact t/F distribution theory when errors are heteroscedastic, correlated, or heavy-tailed — use GLS, robust ("sandwich") standard errors, or robust regression
- Confusing a confidence interval for the mean response with a prediction interval for a new observation (the latter adds &sigma;&sup2; and is always wider)
- Reading a coefficient table without checking residual plots, leverage/Cook's distance, and VIFs — and deleting "influential" points reflexively instead of investigating them
- Running stepwise selection or LASSO and then quoting the classical t-test p-values — model selection invalidates them; use bootstrap, selective-inference, or Bayesian methods
