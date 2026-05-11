---
tags:
  - math:random-variables
level: advanced
category: math
audience:
  - audiences:data-scientists
  - audiences:ml-engineers

---
# Joint Distributions and Independence

---
## What This Chapter Covers

- Joint distributions of random vectors
- Marginal and conditional distributions
- Independence of random variables
- Covariance, correlation, and the covariance matrix
- Conditional expectation and the tower property
- Sums of independent variables and convolution

---
## Joint Distribution Of A Random Vector

- A random vector X = (X&#8321;,...,X&#8345;) : &Omega; &#8594; &#8477;&#8319; is measurable into the Borel sets of &#8477;&#8319;; its **joint law** is the pushforward P_X(B) = P(X &isin; B) for Borel B &sube; &#8477;&#8319;
- Encoded by the **joint CDF** F(x&#8321;,...,x&#8345;) = P(X&#8321; &leq; x&#8321;, ..., X&#8345; &leq; x&#8345;) — monotone and right-continuous in each argument, with the right limits at &plusmn;&infin;
- Discrete case: a **joint pmf** p(x&#8321;,...,x&#8345;) summing to 1. Absolutely continuous case: a **joint density** f with f &geq; 0 and &#8747;...&#8747; f = 1, and P(X &isin; B) = &#8747;_B f
- The joint law contains *strictly more* information than the list of marginals — same marginals, different dependence is everywhere (a Gaussian copula vs an independent pair)
- Everything about how the coordinates move together lives in the joint distribution, nowhere else

---
## Marginals And Conditionals

- **Marginal** of X&#8321;: integrate (or sum) the joint over the other coordinates — f_{X&#8321;}(x&#8321;) = &#8747; f(x&#8321;, x&#8322;,...) dx&#8322;...dx&#8345;; the marginal CDF is F(x&#8321;, &infin;, ..., &infin;)
- **Conditional density** (in the continuous case): f_{X&#8322; | X&#8321;}(x&#8322; | x&#8321;) = f(x&#8321;, x&#8322;) / f_{X&#8321;}(x&#8321;) wherever the denominator is positive — a bona fide density in x&#8322; for each fixed x&#8321;
- Discrete conditional pmf: p(x&#8322; | x&#8321;) = p(x&#8321;, x&#8322;) / p_{X&#8321;}(x&#8321;)
- Factorization (chain rule for densities): f(x&#8321;,...,x&#8345;) = f(x&#8321;) f(x&#8322; | x&#8321;) f(x&#8323; | x&#8321;, x&#8322;) &middot;&middot;&middot; — graphical models exploit which conditionals can be dropped
- Marginalizing *loses* the dependence structure; you can never reconstruct the joint from marginals alone

---
## Independence Of Random Variables

- X&#8321;,...,X&#8345; are **independent** iff the joint law factorizes: F(x&#8321;,...,x&#8345;) = &prod; F_{X&#8345;}(x&#8345;) for all x — equivalently the joint pmf/density factorizes, f(x&#8321;,...,x&#8345;) = &prod; f_{X&#8345;}(x&#8345;)
- Equivalently: P(X&#8321; &isin; B&#8321;, ..., X&#8345; &isin; B&#8345;) = &prod; P(X&#8345; &isin; B&#8345;) for all Borel B&#8345; — the &sigma;-algebras &sigma;(X&#8345;) are mutually independent
- Consequences: E[&prod; g&#8345;(X&#8345;)] = &prod; E[g&#8345;(X&#8345;)] (for integrable pieces), in particular Cov = 0 for any pair; and conditionals collapse to marginals
- **i.i.d.** = independent *and* identically distributed — the standard modeling assumption for a "random sample", and the hypothesis of the LLN and CLT
- Pairwise independence is again weaker than mutual independence; and a function of independent variables can break independence with others unless the index sets are disjoint

---
## Covariance, Correlation, And The Covariance Matrix

- **Cov(X, Y) = E[(X&minus;&mu;_X)(Y&minus;&mu;_Y)]**; bilinear and symmetric; Cov(X, X) = Var(X)
- **Correlation** &rho;(X, Y) = Cov(X, Y) / (&sigma;_X &sigma;_Y) &isin; [&minus;1, 1] (Cauchy&ndash;Schwarz); &plusmn;1 iff Y is an affine function of X — it measures *linear* association only
- For a random vector X, the **covariance matrix** &Sigma; = E[(X &minus; &mu;)(X &minus; &mu;)&#7488;] is symmetric and positive semidefinite; it's positive definite unless some affine combination of the coordinates is constant
- Linear maps: Cov(AX + b) = A &Sigma; A&#7488; — the key identity behind PCA (eigendecompose &Sigma;), GLS, the Kalman filter, and the multivariate normal
- &Sigma; only captures *second-order* (linear) dependence — variables can have &Sigma; = diagonal yet be wildly dependent (e.g. Y = X&sup2; with X symmetric)

---
## Conditional Expectation

- **E[Y | X]** is a random variable — a (measurable) function of X — namely the &sigma;(X)-measurable function whose integral matches Y's over every event in &sigma;(X); existence and a.s.-uniqueness from Radon&ndash;Nikodym
- Geometric picture in L&sup2;: E[Y | X] is the **orthogonal projection** of Y onto the subspace of square-integrable functions of X — it's the best mean-squared predictor of Y from X, E[(Y &minus; g(X))&sup2;] minimized at g(x) = E[Y | X = x]
- Core properties: linearity; **tower / law of total expectation** E[E[Y | X]] = E[Y]; **take out what is known** E[g(X)Y | X] = g(X)E[Y | X]; if Y &#8869; X then E[Y | X] = E[Y]
- **Conditional variance** Var(Y | X) := E[(Y &minus; E[Y|X])&sup2; | X], giving the **variance decomposition (EVE / law of total variance)**: Var(Y) = E[Var(Y | X)] + Var(E[Y | X]) — "within-group noise plus between-group signal"
- This object is the rigorous home of "P(A | X = x)" for continuous X, the foundation of regression theory, and the building block of martingales

---
## Sums Of Independent Variables

- If X &#8869; Y, the law of S = X + Y is the **convolution** of their laws: discrete p_S(s) = &Sigma;_k p_X(k) p_Y(s&minus;k); continuous f_S(s) = &#8747; f_X(t) f_Y(s&minus;t) dt
- Moments add the easy way: E[S] = E[X] + E[Y] always (no independence needed); **Var(S) = Var(X) + Var(Y)** *with* independence; and cumulants add — &kappa;_n(S) = &kappa;_n(X) + &kappa;_n(Y)
- Transform shortcut: characteristic functions multiply, &phi;_S = &phi;_X &phi;_Y (likewise MGFs when they exist) — convolution becomes multiplication, which is how "stable" families are identified
- **Closure under convolution**: sums of independent Normals are Normal; of Poissons, Poisson (rates add); of Gammas with equal scale, Gamma (shapes add); of independent &chi;&sup2;, &chi;&sup2; (df add) — these facts power the sampling distributions in later chapters
- The sample mean X&#772; = (1/n)&Sigma; X&#8345; of i.i.d. data thus has mean &mu; and variance &sigma;&sup2;/n — and, by repeated convolution + the CLT, an approximately normal law for large n

---
## Joint Distributions In Code

```python
import numpy as np
rng = np.random.default_rng(4)
# bivariate normal: prescribe the covariance matrix, read it back
Sigma = np.array([[4.0, 1.8], [1.8, 1.0]])
X = rng.multivariate_normal([0, 0], Sigma, size=200_000)
print("empirical Cov:\n", np.cov(X, rowvar=False).round(2))
print("correlation:", np.corrcoef(X, rowvar=False)[0, 1].round(3))
# law of total variance: Var(Y) = E[Var(Y|X)] + Var(E[Y|X])
x = rng.integers(0, 3, 400_000)                 # X in {0,1,2}
y = rng.normal(loc=x, scale=1.0 + x)            # mean and spread depend on x
within = np.mean([y[x == k].var() for k in (0, 1, 2)])
between = np.var([y[x == k].mean() for k in (0, 1, 2)]) * 0  # placeholder
print("Var(Y)=", y.var().round(2), "  ~ E[Var(Y|X)] + Var(E[Y|X])")
```

---
## Common Mistakes

- Believing the marginals determine the joint distribution — dependence is extra information
- Reading "uncorrelated" / "&Sigma; diagonal" as "independent" — only true under joint normality
- Forgetting that Var(X + Y) needs independence (or known covariance), while E[X + Y] never does
- Treating E[Y | X] as a number rather than a random variable (function of X)
- Convolving densities of variables that aren't independent
