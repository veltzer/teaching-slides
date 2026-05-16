---
tags:
  - math:inferential-statistics
level: advanced
category: math
audience:
  - audiences:data-scientists
  - audiences:ml-engineers

---
# Statistical Models and Sufficiency

---
## What This Chapter Covers

- What a statistical model is, formally
- Statistics, parameters, identifiability
- Sufficiency and the Fisher&ndash;Neyman factorization
- Minimal sufficiency
- Completeness and ancillarity
- Basu's theorem and the exponential-family case

---
## Sufficiency: Lossless Compression

![sufficiency](svg/courses/math/statistics-theory/09_statistical_models_and_sufficiency/sufficiency.svg)

---
## A Statistical Model, Formally

- Data X lives in a sample space &#119987;; a **statistical model** is a family of candidate distributions **P = { P&#952; : &theta; &isin; &Theta; }** for the law of X
- **Parametric**: &Theta; &sube; &#8477;&#7496; finite-dimensional (X ~ N(&mu;,&sigma;&sup2;), &theta; = (&mu;,&sigma;&sup2;)). **Nonparametric**: &Theta; is infinite-dimensional ("X has *some* continuous density"). **Semiparametric**: a finite-dimensional part of interest plus an infinite-dimensional nuisance
- The model is an *assumption* — "all models are wrong, some are useful"; every later guarantee is conditional on P being (approximately) correct
- A **random sample** is the special case X = (X&#8321;,...,X&#8345;) with the X&#8345; i.i.d. from one member; then P&#952; on &#119987; = (P&#952; on the line)&#8319;
- Inference = using the observed X to say which P&#952; (or which feature of it) is in force

---
## Statistics, Parameters, Identifiability

- A **statistic** is any (measurable) function T = T(X) of the *data alone* — no unknown &theta; in it; T has a distribution, derived from P&#952;, that generally *does* depend on &theta;
- A **parameter** (or estimand) is a function &psi;(&theta;) of the index — the thing you want to know (the mean, a quantile, a regression coefficient, P&#952;(X &gt; 0))
- An estimator is a statistic chosen to estimate a parameter; an estimate is its observed value — keep the procedure/realization distinction (it's the source of every "the CI either does or doesn't contain &mu;" subtlety)
- **Identifiability**: the map &theta; &#8614; P&#952; must be injective — distinct parameters must give distinct distributions, else no amount of data can separate them (mixture-label swapping, over-parameterized models)
- Non-identifiability is a *model* defect, not a sample-size problem: fix the parametrization (constraints, reparametrize) before estimating anything

---
## Sufficiency

- A statistic T(X) is **sufficient** for &theta; if the conditional distribution of X given T = t **does not depend on &theta;** — once you know T, the rest of the data carries no further information about &theta;
- Equivalently: you could *throw away* X and keep only T without losing anything for inference about &theta; — and you could even simulate a fresh dataset from the &theta;-free conditional that's just as informative
- The full data X is trivially sufficient; the content of the concept is in finding a *small* (low-dimensional) sufficient statistic — that's data reduction without information loss
- Examples: for X&#8345; i.i.d. Bernoulli(p), &Sigma;X&#8345; is sufficient for p; for N(&mu;,&sigma;&sup2;), (&Sigma;X&#8345;, &Sigma;X&#8345;&sup2;) is sufficient for (&mu;,&sigma;&sup2;); for Uniform(0,&theta;), max X&#8345; is sufficient
- The **likelihood function** &theta; &#8614; L(&theta; | x) is itself the "ultimate" sufficient summary — sufficiency is precisely "T captures everything the likelihood depends on through x"

---
## The Factorization Theorem

- **Fisher&ndash;Neyman factorization**: T(X) is sufficient for &theta; **iff** the joint density/pmf factors as f(x | &theta;) = **g( T(x), &theta; ) &middot; h(x)** — a piece that involves &theta; only through T, times a piece free of &theta;
- This is the *operational* tool: you read sufficiency straight off the form of the likelihood, no conditional distributions to compute
- Worked pattern (exponential family): f(x | &theta;) = h(x) exp( &eta;(&theta;)&#7488; T(x) &minus; A(&theta;) ) — the bracketed T(x) is *immediately* sufficient, and for an i.i.d. sample &Sigma; T(x&#8345;) is sufficient with dimension *not growing in n*
- Worked pattern (Uniform(0,&theta;)): f(x | &theta;) = &theta;&#8315;&#8319; 1{0 &leq; min x&#8345;} 1{max x&#8345; &leq; &theta;} = [&theta;&#8315;&#8319; 1{max x&#8345; &leq; &theta;}] &middot; [1{min x&#8345; &geq; 0}] &#8658; max X&#8345; sufficient
- Caveat: factorization tells you *a* sufficient statistic, not the *smallest* one — that's the next slide

---
## Minimal Sufficiency

- T is **minimal sufficient** if it is sufficient *and* is a function of every other sufficient statistic — the coarsest possible reduction that still loses nothing; it's unique up to one-to-one transformations
- **Lehmann&ndash;Scheffé recipe**: T(x) is minimal sufficient iff [ the likelihood ratio f(x | &theta;)/f(y | &theta;) is constant in &theta; ] &hArr; [ T(x) = T(y) ] — partition the sample space by "same likelihood shape"
- For a **full-rank exponential family**, the natural statistic (&Sigma; T&#8321;(x&#8345;), ..., &Sigma; T&#8344;(x&#8345;)) is minimal sufficient — and its dimension is fixed, no matter the sample size; this is exactly *why* exponential families are so tractable
- Contrast: for many non-exponential families (Cauchy location, Uniform with both endpoints unknown beyond {min, max}) the minimal sufficient statistic has dimension that does **not** shrink to a constant — full data reduction is impossible
- Minimal sufficiency is the floor for *information*; the next concept (completeness) is what you need for *optimality*

---
## Completeness And Ancillarity

- A (sufficient) statistic T is **complete** if the only function g with E&#952;[g(T)] = 0 for *all* &theta; is g &#8801; 0 — informally, T's distribution "moves enough with &theta;" that no non-trivial unbiased estimator of zero can be built from it
- A statistic A is **ancillary** if its distribution **does not depend on &theta; at all** — it carries no marginal information about &theta; (sample range in a location family; n itself; a residual configuration)
- The two are polar opposites: a complete statistic is "maximally informative / non-redundant", an ancillary one is "informationless"
- For a full-rank exponential family, the natural minimal sufficient statistic is also **complete** — the happy case where everything works
- **Conditionality principle** (motivating ancillarity): inference should arguably be carried out *conditional on the observed value of an ancillary statistic* — e.g. condition on the realized design / sample size — which is where many "exact" conditional procedures come from

---
## Basu's Theorem

- **Basu's theorem**: if T is **complete sufficient** for &theta; and A is **ancillary**, then T and A are **independent** — for every &theta;
- It's a striking, "free" independence result that you'd never guess from the joint density; the proof is a two-line application of completeness
- Flagship payoff: for X&#8345; i.i.d. N(&mu;, &sigma;&sup2;) with &sigma;&sup2; known... and more usefully, the sample mean X&#772; (complete sufficient for &mu; when &sigma; known) is independent of the sample variance S&sup2; (whose distribution doesn't depend on &mu;) — *Basu gives this in one stroke*, and that independence is exactly what makes the t-statistic's distribution exact
- General use: to compute E&#952;[ T(X) ] for some statistic, find an ancillary A and a complete sufficient C, write things conditionally, and the &theta;-free pieces decouple — turns ugly expectations into easy ones
- Hidden subtlety: completeness is *essential* — drop it (Uniform-with-both-endpoints, where {min, max} is sufficient but not complete) and the conclusion can fail

---
## Sufficiency In Code

```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(8)
# Bernoulli(p): the count T = sum X_i is sufficient. Given T=t, X is just a uniformly
# random arrangement of t ones -- its conditional law does NOT depend on p.
p, n = 0.3, 12
for p_try in (0.1, 0.3, 0.8):
    samples = (rng.random((200_000, n)) < p_try)
    t = samples.sum(axis=1)
    cond = samples[t == 6]                       # condition on the count = 6
    print(f"p={p_try}: P(X_1=1 | T=6) = {cond[:, 0].mean():.3f}")   # ~ 6/12 = 0.5 regardless of p

# Basu in action: for N(mu, sigma^2), Xbar (complete suff. for mu, sigma known) ⟂ S^2
x = rng.normal(5.0, 2.0, (300_000, 20))
xbar = x.mean(axis=1); s2 = x.var(axis=1, ddof=1)
print("corr(Xbar, S^2) ~ 0:", np.corrcoef(xbar, s2)[0, 1].round(3))
```

---
## Common Mistakes

- Forgetting to check **identifiability** before estimating — non-identifiable parameters can't be recovered from any sample size
- Treating *any* sufficient statistic as the best reduction — you usually want the **minimal** sufficient one
- Assuming a minimal sufficient statistic is **complete** — true for full-rank exponential families, not in general
- Invoking Basu's theorem without verifying **completeness** (sufficient + ancillary alone is not enough)
- Confusing a parameter &psi;(&theta;) (a feature of the model) with a statistic T(X) (a function of the data) — the whole estimation problem is about bridging them
