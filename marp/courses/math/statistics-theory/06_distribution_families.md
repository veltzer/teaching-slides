---
tags:
  - math:distributions
level: advanced
category: math
audience:
  - audiences:data-scientists
  - audiences:ml-engineers

---
# Common Distribution Families

---
## What This Chapter Covers

- The standard discrete families and how they connect
- The standard continuous families and how they connect
- The Gaussian and the distributions derived from it
- The exponential family and why it's special
- Location&ndash;scale families
- Heavy tails and where finite-moment intuition fails

---
## The Discrete Catalogue

- **Bernoulli(p)**: one trial; mean p, variance p(1&minus;p) — the atom everything else is built from
- **Binomial(n, p)**: sum of n i.i.d. Bernoulli(p); mean np, variance np(1&minus;p); closed under convolution in n (same p)
- **Geometric(p)** / **Negative Binomial(r, p)**: trials until the 1st / r-th success; the geometric is the unique *discrete memoryless* law
- **Poisson(&lambda;)**: counts of rare independent events; mean = variance = &lambda;; closed under convolution (&lambda; add); the n&#8594;&infin;, np&#8594;&lambda; limit of the binomial
- **Hypergeometric** (sampling without replacement) and **Multinomial** (k-category counts) round out the basics — note hypergeometric &#8594; binomial as the population grows

---
## The Continuous Catalogue

- **Uniform(a, b)**: maximum entropy on a bounded interval; the substrate of inverse-transform sampling
- **Exponential(&lambda;)**: waiting time in a Poisson process; the unique *continuous memoryless* law; mean 1/&lambda;, variance 1/&lambda;&sup2;
- **Gamma(&alpha;, &beta;)**: sum of &alpha; i.i.d. Exponentials (integer &alpha;); closed under convolution in the shape (same rate); &alpha; = 1 is the exponential
- **Beta(&alpha;, &beta;)**: supported on [0, 1]; the conjugate prior for a binomial proportion; if G&#8321; ~ Gamma(&alpha;,&middot;), G&#8322; ~ Gamma(&beta;,&middot;) independent then G&#8321;/(G&#8321;+G&#8322;) ~ Beta(&alpha;,&beta;)
- **Lognormal**, **Pareto**, **Weibull** cover skew and tails — lognormal = exp(Normal), Pareto = power-law tails, Weibull = the flexible reliability/extreme workhorse

---
## The Gaussian And Its Family

- **Normal(&mu;, &sigma;&sup2;)**: the CLT limit; closed under affine maps and under convolution (means add, variances add); maximum entropy for fixed mean and variance; characterized by all cumulants above the 2nd vanishing
- **Chi-squared** &chi;&sup2;&#8345; = sum of n i.i.d. squared standard Normals = Gamma(n/2, 1/2); mean n, variance 2n; convolution-closed in n
- **Student's t**&#8345; = Z / &radic;(&chi;&sup2;&#8345;/n) with Z &#8869; &chi;&sup2;&#8345;; heavier tails than the Normal, &#8594; Normal as n &#8594; &infin;; t&#8321; is the Cauchy (no mean!)
- **Snedecor's F**(m, n) = (&chi;&sup2;_m/m)/(&chi;&sup2;_n/n) with the two &chi;&sup2; independent; t&#8345;&sup2; = F(1, n); the distribution behind ANOVA and regression model tests
- **Multivariate Normal** N(&mu;, &Sigma;): every affine image is Normal, marginals and conditionals are Normal, and *uncorrelated implies independent* — the uniquely tractable multivariate model

---
## The Exponential Family

- A family has **exponential-family** form if its density/pmf is f(x | &theta;) = h(x) exp( &eta;(&theta;)&#7488; T(x) &minus; A(&theta;) ) — natural parameter &eta;, sufficient statistic T, log-partition / cumulant function A, carrier h
- Members: Bernoulli, binomial, Poisson, geometric, normal (known or unknown variance), exponential, gamma, beta, &chi;&sup2;, multinomial, Dirichlet, ... — most of the catalogue above
- Why it matters: **T(x) is a (low-dimensional) sufficient statistic** for any sample size; A is the cumulant generating function of T (E[T] = &nabla;A, Cov(T) = &nabla;&sup2;A); there's a **conjugate prior** of matching form; and the MLE solves the moment equation E_&theta;[T] = T_observed
- It's the backbone of **generalized linear models** (the "exponential dispersion" subfamily), of variational inference, and of much of modern statistical machinery
- Heavy-tailed families (Cauchy, t, Pareto) are *not* exponential-family — which is exactly why they're harder

---
## Location&ndash;Scale Families

- A **location&ndash;scale family** is {X = &mu; + &sigma;Z : &mu; &isin; &#8477;, &sigma; &gt; 0} for a fixed "standard" Z — so F(x | &mu;,&sigma;) = F&#8320;((x&minus;&mu;)/&sigma;) and f(x | &mu;,&sigma;) = (1/&sigma;) f&#8320;((x&minus;&mu;)/&sigma;)
- Examples: Normal (Z = standard Normal), Cauchy, Logistic, Laplace, Uniform; the exponential is *scale-only*, the Gamma with known shape is scale-only
- Consequences: standardized estimators are *pivotal* (their distribution doesn't depend on &mu;, &sigma;) — this is where the t-statistic's exact distribution comes from; equivariant estimators (sample mean, sample SD) transform the obvious way
- Q&ndash;Q plots are most natural here: plotting sample quantiles against F&#8320;'s quantiles is a straight line iff the data is from that location&ndash;scale family
- Inference for &mu; given &sigma; (or vice versa) reduces to the single standard member Z

---
## Heavy Tails

- A law is **heavy-tailed** when its tail decays slower than any exponential; **power-law / regularly-varying** tails P(X &gt; x) &sim; x&#8315;&#945; are the canonical case
- Moment ladder: a Pareto with index &alpha; has finite k-th moment iff k &lt; &alpha; — so the mean fails for &alpha; &leq; 1, the variance for &alpha; &leq; 2; the **Cauchy** (&alpha; = 1) has *no mean* and the sample mean does **not** converge
- The CLT can fail: sums of i.i.d. infinite-variance variables converge (after the right scaling) to **&alpha;-stable** laws, not the Normal — the Normal is just the &alpha; = 2 stable case
- Practical fallout: "3-sigma events" are common, sample means and SDs are unstable and misleading, tail risk is systematically underestimated by Gaussian intuition; estimate the **tail index** instead (Hill estimator), report quantiles not moments
- Where you meet them: file sizes, city sizes, wealth, network degrees, insurance claims, financial returns, queueing delays — "web-scale" data is heavy-tailed by default

---
## Distribution Relationships In Code

```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(5)
# t_n -> Normal; t_1 is Cauchy (no mean -> running average wanders)
print("t_30 vs N(0,1) KS p:", stats.ks_2samp(rng.standard_t(30, 50_000), rng.standard_normal(50_000)).pvalue.round(3))
c = rng.standard_cauchy(200_000); print("Cauchy running mean (last):", np.cumsum(c)[-1] / c.size)
# sum of k iid Exp(rate=2) is Gamma(shape=k, scale=1/2)
k = 4; s = rng.exponential(scale=0.5, size=(200_000, k)).sum(axis=1)
print("Gamma fit (shape, _, scale) ~ (4, 0, 0.5):", np.round(stats.gamma.fit(s, floc=0), 2))
# chi^2_n = sum of n squared standard normals
n = 5; q = (rng.standard_normal((200_000, n))**2).sum(axis=1)
print("mean~n, var~2n:", q.mean().round(2), q.var(ddof=1).round(2))
```

---
## Common Mistakes

- Forcing a Normal (or any finite-variance) model onto heavy-tailed data
- Forgetting which families are convolution-closed — only some sums stay in the family
- Confusing t&#8345; with the Normal at small n (and forgetting t&#8321; = Cauchy has no mean)
- Treating Cauchy / t / Pareto as exponential-family — they aren't, so the usual sufficiency/conjugacy machinery doesn't apply
- Reporting a sample mean and SD for a power-law variable as if they were stable, meaningful summaries
