---
tags:
  - math:estimation
level: advanced
category: math
audience:
  - audiences:data-scientists
  - audiences:ml-engineers

---

# Point Estimation Theory

---

## What This Chapter Covers

- Risk, loss, and how we rank estimators
- Bias, variance, and the bias&ndash;variance decomposition
- The Fisher information and the Cramér&ndash;Rao bound
- Efficiency and UMVU estimators
- Rao&ndash;Blackwell and Lehmann&ndash;Scheffé
- Admissibility, minimaxity, and Stein's surprise

---

## Bias, Variance, And MSE

![bias variance mse](svg/courses/math/statistics-theory/10_point_estimation_theory/bias_variance_mse.svg)

---

## Loss, Risk, And How To Rank Estimators

- Fix a parameter &psi;(&theta;) and an estimator &delta;(X). A **loss function** L(&theta;, a) &geq; 0 prices the error of guessing a; the **risk** is the expected loss R(&theta;, &delta;) = E&#952;[ L(&theta;, &delta;(X)) ]
- The default is **squared-error loss**, L(&theta;, a) = (a &minus; &psi;(&theta;))&sup2;, whose risk is the **mean squared error** MSE&#952;(&delta;) = E&#952;[ (&delta;(X) &minus; &psi;(&theta;))&sup2; ]
- The problem: R(&theta;, &delta;) is a *function of &theta;*, so two estimators' risk curves usually cross — there is generally **no uniformly best estimator**
- Ways out: (i) restrict the class (e.g. unbiased, or equivariant) and seek the best *within* it; (ii) summarize the risk curve to a number — average it against a prior (**Bayes risk**) or take its worst case (**minimax risk**)
- &delta; is **inadmissible** if some other estimator has risk &leq; R(&theta;, &delta;) for all &theta; and strictly smaller somewhere — a baseline sanity check, not a guarantee of being good

---

## The Bias&ndash;Variance Decomposition

- For squared-error loss, **MSE&#952;(&delta;) = Var&#952;(&delta;) + ( bias&#952;(&delta;) )&sup2;**, where bias&#952;(&delta;) = E&#952;[&delta;] &minus; &psi;(&theta;)
- **Unbiased** means bias &#8801; 0, so MSE = Var — clean, but unbiasedness is *not* sacred: a slightly biased estimator with much smaller variance can dominate the best unbiased one (shrinkage, ridge, Stein)
- Classic instance: for N(&mu;,&sigma;&sup2;), the MLE of &sigma;&sup2; (divide by n) is biased low; the unbiased version divides by n&minus;1; but the *minimum-MSE* estimator of the form &Sigma;(X&#8345;&minus;X&#772;)&sup2;/c uses c = n+1
- The same tradeoff is the organizing principle of regularization and of generalization in machine learning — pay a little bias to buy a lot of variance reduction
- Practical upshot: compare estimators by **risk (MSE)**, not by unbiasedness alone

---

## Fisher Information

- For a model with density f(x | &theta;) (regularity conditions: support free of &theta;, smooth, can differentiate under the integral), the **score** is U(&theta;) = &part;/&part;&theta; log f(X | &theta;); it has mean zero, E&#952;[U(&theta;)] = 0
- The **Fisher information** is its variance: **I(&theta;) = Var&#952;( U(&theta;) ) = E&#952;[ U(&theta;)&sup2; ] = &minus;E&#952;[ &part;&sup2;/&part;&theta;&sup2; log f(X | &theta;) ]** — the curvature of the expected log-likelihood
- Interpretation: how *sharply* the data pins down &theta; — a steep, narrow log-likelihood (large I) means precise estimation is possible; a flat one means little information
- It is **additive over independent observations**: an i.i.d. sample of size n has information n&middot;I&#8321;(&theta;) — twice the data, twice the information, hence (asymptotically) half the variance
- Multivariate &theta;: I(&theta;) is the **information matrix** E&#952;[ U U&#7488; ] = &minus;E&#952;[ Hessian of log f ], positive semidefinite; it reparametrizes by the Jacobian rule

---

## The Cramér&ndash;Rao Lower Bound

- Under the regularity conditions, **any unbiased estimator** &delta; of &psi;(&theta;) satisfies **Var&#952;(&delta;) &geq; ( &psi;'(&theta;) )&sup2; / I_n(&theta;)** — a floor on precision no unbiased procedure can beat
- For estimating &theta; itself in an i.i.d. sample: Var&#952;(&delta;) &geq; 1 / ( n I&#8321;(&theta;) ) — the canonical "1/n, scaled by the inverse information" rate
- Proof in one line: Cauchy&ndash;Schwarz on Cov&#952;(&delta;, score) = &psi;'(&theta;) (the latter from differentiating the unbiasedness identity under the integral)
- Equality holds **iff** &delta; is an affine function of the score for every &theta; — which forces an exponential-family structure; outside that, the bound need not be attainable
- Biased estimators *can* have variance below the unbiased CRLB (no contradiction — different target); there are CRLB-type bounds for the biased case too, with a (1 + bias')&sup2; numerator

---

## Efficiency And UMVU Estimators

- An unbiased estimator is **efficient** if it attains the Cramér&ndash;Rao bound; its **efficiency** is the ratio (CRLB) / Var&#952;(&delta;) &isin; (0, 1] — how close to the floor it sits
- A **uniformly minimum-variance unbiased estimator (UMVUE)** has, among *all* unbiased estimators, the smallest variance for **every** &theta; — the best you can do if you insist on unbiasedness
- An efficient estimator is automatically UMVU; but a UMVUE may exist and still *not* reach the CRLB (the bound is a sufficient, not necessary, certificate of optimality) — Uniform(0,&theta;) is the standard example, where the UMVUE has variance below any naive guess yet the CRLB is irrelevant (irregular model)
- UMVUEs needn't exist at all for some models; when they do, the next two slides give the machine to *construct* them
- Asymptotically, the MLE is efficient (it attains the CRLB in the limit) — the finite-sample story is what this slide is about

---

## Rao&ndash;Blackwell And Lehmann&ndash;Scheffé

- **Rao&ndash;Blackwell theorem**: take *any* unbiased estimator &delta;(X) and a sufficient statistic T; define &delta;*(T) = E[ &delta;(X) | T ]. Then &delta;* is unbiased for the same &psi;(&theta;) and **Var&#952;(&delta;*) &leq; Var&#952;(&delta;)** for all &theta; — conditioning on a sufficient statistic *never hurts and usually helps* ("Rao&ndash;Blackwellization")
- Why it works: the tower property keeps the mean; the conditional-variance decomposition Var(&delta;) = E[Var(&delta;|T)] + Var(E[&delta;|T]) shows you've shed the first, non-negative term
- It also says the search for good estimators can be **confined to functions of a sufficient statistic** — no loss in doing so
- **Lehmann&ndash;Scheffé theorem**: if in addition T is **complete**, then &delta;*(T) is the *unique* UMVUE — completeness removes the wiggle room (no two distinct functions of T can both be unbiased), pinning down the best one
- Construction recipe, in practice: (1) find a complete sufficient T (full-rank exponential family &#8658; the natural statistic); (2) write down *any* simple unbiased estimator; (3) take its conditional expectation given T — or, often easier, directly find the function of T that is unbiased

---

## Beyond Unbiasedness: Admissibility, Minimax, Stein

- Dropping the unbiasedness straitjacket, the relevant optimality notions are **admissibility** (not uniformly dominated) and **minimaxity** (smallest worst-case risk, min over &delta; of max over &theta; of R)
- **Bayes estimators** — minimizers of the Bayes risk, i.e. the posterior mean under squared-error loss — are admissible under mild conditions; conversely most admissible estimators are Bayes or limits of Bayes ("complete class" theorems). A Bayes rule with *constant* frequentist risk is minimax — a handy way to find minimax procedures
- **Stein's paradox / James&ndash;Stein**: for estimating the mean vector of N(&theta;, I&#8345;) in dimension **n &geq; 3**, the obvious estimator X itself is **inadmissible** — the shrinkage estimator (1 &minus; (n&minus;2)/&#8214;X&#8214;&sup2;) X has strictly smaller total MSE for *every* &theta;, even though it borrows strength across coordinates that are independent and unrelated
- The lesson: "estimate each component by its own data" is not optimal in high dimensions; deliberate bias toward a center (a prior, zero, a common mean) pays off — this is the theoretical seed of **ridge regression, empirical Bayes, hierarchical shrinkage, and regularized ML**
- So: UMVUE is the right target *if you've decided to be unbiased*; once you care about risk per se, shrinkage is often strictly better

---

## Estimation Theory In Code

```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(9)
# CRLB for Bernoulli(p): I_1(p)=1/(p(1-p)), so Var(p_hat) >= p(1-p)/n -- and p_hat = mean attains it
p, n, R = 0.3, 200, 100_000
phat = (rng.random((R, n)) < p).mean(axis=1)
print("Var(p_hat):", phat.var().round(6), "  CRLB:", round(p*(1-p)/n, 6))   # equal: efficient

# Rao-Blackwell: estimate theta^2 for X~Poisson(theta) from one obs by X(X-1); RB it onto T=sum X_i
theta, m = 4.0, 8
x = rng.poisson(theta, (R, m)); T = x.sum(axis=1)
naive = x[:, 0]*(x[:, 0]-1)                     # unbiased for theta^2 but high variance
rb = T*(T-1)/m**2                               # E[naive | T] for Poisson; unbiased, far smaller variance
print(f"E ~ {theta**2}: naive {naive.mean():.2f} (var {naive.var():.1f})  vs RB {rb.mean():.2f} (var {rb.var():.2f})")
```

---

## Common Mistakes

- Hunting for a "uniformly best" estimator — risk curves cross; you must restrict the class or summarize the risk
- Treating unbiasedness as the goal instead of low **MSE** — a biased estimator can dominate the best unbiased one
- Reading the Cramér&ndash;Rao bound as always attainable, or as applying to *biased* estimators in its plain form
- Forgetting that Rao&ndash;Blackwell needs a **sufficient** statistic, and Lehmann&ndash;Scheffé additionally needs **completeness**
- Defaulting to component-wise estimation in high dimensions — Stein's paradox shows shrinkage strictly wins for n &geq; 3
