---
tags:
  - math:estimation
level: advanced
category: math
audience:
  - audiences:data-scientists
  - audiences:ml-engineers

---
# Maximum Likelihood and Asymptotics

---
## What This Chapter Covers

- The likelihood function and the MLE
- Invariance and the score equations
- Consistency of the MLE
- Asymptotic normality and efficiency
- Observed vs expected information; Wald, score, LR statistics
- Where the MLE misbehaves

---
## The Likelihood Surface

![mle likelihood](svg/courses/math/statistics-theory/11_maximum_likelihood/mle_likelihood.svg)

---
## The Likelihood And The MLE

- Given data x and a model { f(&middot; | &theta;) : &theta; &isin; &Theta; }, the **likelihood function** is L(&theta; | x) = f(x | &theta;) — the *same* density, but read as a function of &theta; with x fixed; it is **not** a probability distribution over &theta;
- The **maximum likelihood estimator** is &theta;&#770; = argmax_&theta; L(&theta; | x) — the parameter value under which the observed data is most probable
- Almost always one maximizes the **log-likelihood** &#8467;(&theta;) = log L(&theta; | x) = &Sigma; log f(x&#8345; | &theta;) (i.i.d. case): sums beat products numerically, and the derivatives are cleaner
- The **likelihood principle**: two datasets with proportional likelihood functions carry the same information about &theta; — a stance many frequentist procedures (which look at the whole sample space) quietly violate
- Sufficiency connection: &theta;&#770; depends on x only through any sufficient statistic, since the likelihood does

---
## Invariance And The Score Equations

- **Functional invariance**: if &theta;&#770; is the MLE of &theta;, then g(&theta;&#770;) is the MLE of g(&theta;) for *any* function g — a property no other major estimation principle shares (Bayes posterior means, UMVUEs are *not* invariant). Want the MLE of &sigma; instead of &sigma;&sup2;? Just take the square root
- Interior maxima of a smooth log-likelihood satisfy the **score (likelihood) equations** &nabla;&#8467;(&theta;) = 0, i.e. &Sigma; &part;/&part;&theta; log f(x&#8345; | &theta;) = 0 — solve these (often only numerically: Newton&ndash;Raphson, Fisher scoring, EM, gradient methods)
- A solution is only a *candidate*: check the second-order condition (negative-definite Hessian), and beware of **boundary** maxima (Uniform(0,&theta;): &#8467; is decreasing in &theta;, so &theta;&#770; = max x&#8345;, *not* a stationary point) and of **multiple local maxima** (mixture models — restart from many seeds)
- Exponential-family payoff: the score equation reduces to **E&#952;[T(X)] = T(x_observed)** — "set the model's expected sufficient statistic equal to its observed value"; for the natural parametrization the log-likelihood is concave, so the maximizer is unique
- The score is also the link to Fisher information: E&#952;[score] = 0, Var&#952;(score) = I(&theta;) — which is what the asymptotics below run on

---
## Consistency

- Under regularity conditions (correct, identifiable model; common support; some compactness/uniformity), the MLE is **consistent**: &theta;&#770;&#8345; &#8594; &theta;&#8320; (in probability, often a.s.) at the true &theta;&#8320; as n &#8594; &infin;
- Intuition (Wald's argument): (1/n)&#8467;(&theta;) converges by the LLN to E_{&theta;&#8320;}[ log f(X | &theta;) ], which by Jensen's inequality (equivalently, non-negativity of the **Kullback&ndash;Leibler divergence** KL(&theta;&#8320; &#8214; &theta;)) is *uniquely maximized at* &theta; = &theta;&#8320; — so the empirical maximizer homes in on the true value
- Reframed: the MLE minimizes the empirical KL divergence to the data — it's the "closest model member in KL" to the truth, and that target is the truth itself when the model is correct
- **Misspecified case** (truth not in the model): &theta;&#770; still converges — but to the **pseudo-true** &theta;* that minimizes KL(truth &#8214; f(&middot;|&theta;)), the best-fitting wrong model; "consistency" then means consistent *for &theta;*, not for anything real
- Failure modes: non-identifiability (no unique maximizer), parameter dimension growing with n (Neyman&ndash;Scott — incidental parameters spoil consistency), heavy irregularity

---
## Asymptotic Normality And Efficiency

- Under stronger regularity (twice-differentiable log-likelihood, finite non-singular information, etc.), the MLE is **asymptotically normal**: **&radic;n ( &theta;&#770;&#8345; &minus; &theta;&#8320; ) &#8658; N( 0, I&#8321;(&theta;&#8320;)&#8315;&sup1; )** — so &theta;&#770;&#8345; &asymp; N( &theta;&#8320;, [n I&#8321;(&theta;&#8320;)]&#8315;&sup1; ) for large n
- One-line derivation: Taylor-expand the score equation 0 = &#8467;'(&theta;&#770;) = &#8467;'(&theta;&#8320;) + &#8467;''(&theta;&#771;)(&theta;&#770; &minus; &theta;&#8320;); the CLT makes &#8467;'(&theta;&#8320;)/&radic;n &#8658; N(0, I&#8321;), the LLN makes &minus;&#8467;''/n &#8594; I&#8321;, and Slutsky combines them
- **Asymptotic efficiency**: the limiting variance I&#8321;(&theta;&#8320;)&#8315;&sup1; is exactly the Cramér&ndash;Rao bound — *no* consistent, asymptotically-normal estimator can do better (Hájek&ndash;Le Cam convolution / local-asymptotic-minimax theorems make "no better" precise, modulo measure-zero "superefficient" exceptions à la Hodges)
- Multivariate version: &radic;n(&theta;&#770; &minus; &theta;&#8320;) &#8658; N(0, I&#8321;(&theta;&#8320;)&#8315;&sup1;) with the *information matrix*; combine with the **delta method** to get the asymptotic law of any smooth g(&theta;&#770;): variance &nabla;g&#7488; I&#8321;&#8315;&sup1; &nabla;g / n
- Under misspecification the limit is N(&theta;*, sandwich), variance A&#8315;&sup1; B A&#8315;&sup1; with A = &minus;E[Hessian], B = Var[score] — the **robust ("sandwich") standard errors** that don't assume the model is right

---
## Information In Practice; The Three Asymptotic Tests

- For interval estimates and tests you need to *estimate* the information. **Expected (Fisher) information** I_n(&theta;&#770;) = &minus;E&#952;[&#8467;''] |_{&theta;&#770;} requires knowing the expectation; **observed information** J_n(&theta;&#770;) = &minus;&#8467;''(&theta;&#770;) is just (minus) the Hessian at the optimum — cheap, and often the *better* finite-sample choice (Efron&ndash;Hinkley). A **Wald CI** for &theta; is &theta;&#770; &plusmn; z&#8901; / &radic;J_n(&theta;&#770;)
- Three asymptotically-equivalent (&#8658; &chi;&sup2;) tests of H&#8320;: &theta; = &theta;&#8320; (or of nested restrictions), each "measuring distance from H&#8320;" differently:
    - **Wald**: ( &theta;&#770; &minus; &theta;&#8320; )&sup2; I_n(&theta;&#770;) — uses the *unrestricted* fit; simple, but not invariant to reparametrization and unreliable near the boundary
    - **Score (Rao / Lagrange-multiplier)**: &#8467;'(&theta;&#8320;)&sup2; / I_n(&theta;&#8320;) — uses *only* the restricted fit (no need to estimate the full model); great when the alternative is hard to fit
    - **Likelihood-ratio**: 2[ &#8467;(&theta;&#770;) &minus; &#8467;(&theta;&#8320;) ] — uses *both* fits; parametrization-invariant, generally the best small-sample behavior (this is **Wilks' theorem**: the LR statistic &#8658; &chi;&sup2; with df = number of restrictions)
- They agree to first order but can disagree noticeably in finite samples — when they do, trust the **likelihood-ratio** statistic; for variance-component / boundary nulls the limit is a *mixture* of &chi;&sup2;'s, not a plain &chi;&sup2;
- Same trio reappears throughout applied statistics: t-tests, ANOVA F-tests, the deviance tests in GLMs, the LM tests in econometrics — all instances of Wald / score / LR
- Caveat: all of this is *asymptotic* — for small n, near boundaries, or with weak identification, prefer exact, conditional, or bootstrap procedures

---
## Where The MLE Misbehaves

- **Boundary / irregular models**: support depends on &theta; (Uniform(0,&theta;)) — &theta;&#770; isn't a stationary point, isn't asymptotically normal, and converges at rate n rather than &radic;n; the standard CRLB/asymptotic theory simply doesn't apply
- **Multiple local maxima**: mixture models, neural-network-style likelihoods — the global MLE may be ill-defined (likelihood can diverge as a component variance &#8594; 0); use multiple random restarts, penalization, or settle for a good local maximum (the EM algorithm only guarantees a local one)
- **Many parameters (Neyman&ndash;Scott)**: when the number of nuisance parameters grows with n (one per observation), the MLE of the parameter of interest can be *inconsistent* — fix with conditional, marginal, or profile/integrated likelihoods
- **Misspecification**: &theta;&#770; converges to the pseudo-true value, model-based standard errors are wrong — report sandwich SEs, and remember "the MLE" then estimates "the best-fitting wrong model", not reality
- **Small samples / weak information**: a nearly flat log-likelihood &#8658; huge variance, unstable estimates, normal approximation poor — and **separation** in logistic regression sends the MLE to &plusmn;&infin; (use penalized likelihood, e.g. Firth, or a Bayesian prior)

---
## MLE Asymptotics In Code

```python
import numpy as np
from scipy import stats, optimize
rng = np.random.default_rng(10)
# Exponential(rate=lambda): MLE is 1/Xbar; I_1(lambda)=1/lambda^2, so Var(lambda_hat) ~ lambda^2/n
lam, n, R = 2.0, 300, 50_000
xbar = rng.exponential(1/lam, (R, n)).mean(axis=1)
lam_hat = 1/xbar
print("E[lam_hat] ~ 2:", lam_hat.mean().round(3),
      " Var ~ lam^2/n =", round(lam**2/n, 5), " empirical:", lam_hat.var().round(5))

# generic numeric MLE + Wilks LR test for H0: lambda = 1.7, using one dataset
x = rng.exponential(1/lam, n)
negll = lambda L: -np.sum(stats.expon(scale=1/L[0]).logpdf(x))
Lh = optimize.minimize(negll, x0=[1.0], bounds=[(1e-6, None)]).x[0]
LR = 2*(negll([1.7]) - negll([Lh]))               # ~ chi^2_1 under H0
print(f"MLE lambda_hat = {Lh:.3f}   LR stat = {LR:.2f}   p = {stats.chi2.sf(LR, df=1):.3f}")
```

---
## Common Mistakes

- Treating the likelihood L(&theta; | x) as a probability distribution over &theta; (it doesn't integrate to 1, and "P(&theta; &isin; A)" is meaningless without a prior)
- Solving the score equations and accepting any root — ignoring boundary maxima, second-order conditions, and multiple local optima
- Quoting model-based MLE standard errors when the model is misspecified — use robust/sandwich SEs
- Applying Wald intervals/tests near a parameter boundary or under weak identification — prefer the likelihood-ratio statistic, or an exact/bootstrap method
- Forgetting these results are *asymptotic*: small n, growing parameter dimension (Neyman&ndash;Scott), or separation can break consistency and normality outright
