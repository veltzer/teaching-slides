---
tags:
  - math:hypothesis-testing
level: advanced
category: math
audience:
  - audiences:data-scientists
  - audiences:ml-engineers

---

# Hypothesis Testing Theory

---

## What This Chapter Covers

- Tests as decision rules; size, level, power
- The Neyman&ndash;Pearson lemma
- Uniformly most powerful tests and monotone likelihood ratio
- One-sided vs two-sided; unbiased and invariant tests
- Likelihood-ratio tests and Wilks' theorem
- p-values, multiplicity, and the duality with confidence sets

---

## Type I And Type II Errors

![type errors](svg/courses/math/statistics-theory/12_hypothesis_testing_theory/type_errors.svg)

---

## Tests As Decision Rules

- A hypothesis test partitions the parameter space: **null** H&#8320;: &theta; &isin; &Theta;&#8320; vs **alternative** H&#8321;: &theta; &isin; &Theta;&#8321;; a (possibly randomized) **test** is a function &phi;(x) &isin; [0, 1] giving the probability of rejecting H&#8320; when x is observed
- Two error types: **Type I** (reject H&#8320; when true) and **Type II** (fail to reject when false). The **power function** is &beta;&#966;(&theta;) = E&#952;[&phi;(X)] = P&#952;(reject)
- **Size** = sup over &theta; &isin; &Theta;&#8320; of &beta;&#966;(&theta;) (the worst-case Type I rate); a test "has level &alpha;" if its size &leq; &alpha;. We *fix* &alpha; (control Type I) and then *maximize power* &beta;&#966;(&theta;) over &theta; &isin; &Theta;&#8321; — the asymmetry is the whole game
- The asymmetry is deliberate: "fail to reject" is **not** "accept" — it means the data didn't supply enough evidence against H&#8320;, not that H&#8320; is true
- Randomized tests look strange but are needed for *exact* size in discrete problems (where no non-randomized rejection region hits &alpha; precisely) — and they appear in the Neyman&ndash;Pearson optimum below

---

## The Neyman&ndash;Pearson Lemma

- **Simple vs simple**: H&#8320;: &theta; = &theta;&#8320; against H&#8321;: &theta; = &theta;&#8321;. Among all tests of level &alpha;, the **most powerful** one rejects when the **likelihood ratio** &Lambda;(x) = f(x | &theta;&#8321;) / f(x | &theta;&#8320;) is large: &phi;(x) = 1 if &Lambda; &gt; k, = &gamma; if &Lambda; = k, = 0 if &Lambda; &lt; k, with k and &gamma; chosen so E_{&theta;&#8320;}[&phi;] = &alpha;
- It is both **sufficient** (any LR test of that form is most powerful) and **necessary** (any most-powerful level-&alpha; test must be of this form, a.e.) — a complete characterization
- The proof is a one-paragraph "if &phi; rejects exactly where &Lambda; &gt; k, then (&phi; &minus; &phi;')(f&#8321; &minus; k f&#8320;) &geq; 0 everywhere, integrate" argument — short and worth knowing
- Moral: **the data should be reduced to the likelihood ratio**, and you reject for extreme values of it; everything else in testing theory is about extending this beyond the simple-vs-simple case
- The threshold k controls size; nothing about the *form* of the optimal test changes with &alpha;

---

## UMP Tests And Monotone Likelihood Ratio

- For composite hypotheses, a **uniformly most powerful (UMP)** level-&alpha; test is one whose power &beta;&#966;(&theta;) is &geq; that of *every* other level-&alpha; test, simultaneously for **all** &theta; &isin; &Theta;&#8321; — a single test that's optimal against the entire alternative
- UMP tests usually **do not exist** for two-sided alternatives (the best test against &theta; &gt; &theta;&#8320; differs from the best against &theta; &lt; &theta;&#8320;) — which is exactly why we then restrict to *unbiased* or *invariant* tests (next slide)
- They **do** exist for **one-sided** hypotheses (H&#8320;: &theta; &leq; &theta;&#8320; vs H&#8321;: &theta; &gt; &theta;&#8320;) whenever the model has **monotone likelihood ratio (MLR)** in a statistic T(x): f(x|&theta;')/f(x|&theta;) is non-decreasing in T for every &theta;' &gt; &theta; — then "reject when T &gt; c" is UMP (Karlin&ndash;Rubin theorem)
- The **one-parameter exponential family** has MLR in its natural statistic, so it covers most textbook one-sided problems: the z-test, the one-sided t-test (after conditioning), tests for a binomial p, a Poisson &lambda;, an exponential rate — all are UMP
- Practical reading: for one-sided questions in a nice family there's a *provably best* test, and it's the obvious one; for two-sided questions you must add a fairness criterion to single out a "best" test

---

## Two-Sided, Unbiased, And Invariant Tests

- A test is **unbiased** if &beta;&#966;(&theta;) &geq; &alpha; for all &theta; &isin; &Theta;&#8321; (and &leq; &alpha; on &Theta;&#8320;) — you're at least as likely to reject under the alternative as under the null; a "biased" two-sided test could actually be *less* likely to reject for some true alternatives, which is absurd, so we exclude those
- For two-sided problems in an exponential family there is a **uniformly most powerful unbiased (UMPU)** test — typically a two-sided rejection region with the two tail probabilities chosen so the *power function is flat at &alpha;* on the boundary (not just so each tail is &alpha;/2 — that's an approximation that's exact only under symmetry)
- The **invariance principle**: if the problem is unchanged under a group of transformations (location shifts, rescalings, relabelings), restrict to tests that respect that symmetry; among those, a **uniformly most powerful invariant (UMPI)** test often exists — this is how the two-sample t-test, the F-test, and many multivariate tests are derived and justified
- These two principles (unbiasedness, invariance) are *restriction* devices: they shrink the class of candidate tests until a uniformly best one re-emerges — the same trick used for estimators (restrict to unbiased &#8594; UMVUE)
- When even these don't pin down a unique optimum, fall back to **asymptotic optimality** (the likelihood-ratio family below) or to **most stringent** / minimax-power criteria

---

## Likelihood-Ratio Tests And Wilks' Theorem

- The **generalized likelihood ratio statistic** for H&#8320;: &theta; &isin; &Theta;&#8320; vs H&#8321;: &theta; &isin; &Theta; is &lambda;(x) = sup_{&theta; &isin; &Theta;&#8320;} L(&theta; | x) / sup_{&theta; &isin; &Theta;} L(&theta; | x) &isin; (0, 1]; reject when &lambda;(x) is small (the null fits much worse than the unrestricted model)
- **Wilks' theorem**: under H&#8320; and regularity conditions, **&minus;2 log &lambda;(X) &#8658; &chi;&sup2; with df = dim(&Theta;) &minus; dim(&Theta;&#8320;)** (the number of free parameters the null fixes) — a universal, model-free way to get an (asymptotic) test from *any* parametric model
- It's the parent of a huge family of applied tests: the **deviance** difference in GLMs, nested-model F-tests in regression (the small-sample exact version), tests in survival and log-linear models — all "&minus;2 &times; (log-lik gap)" compared to a &chi;&sup2;
- Asymptotically the LR statistic is equivalent to the **Wald** and **score** statistics from the previous chapter; they can disagree in finite samples, and when they do the LR test usually behaves best (parametrization-invariant, better calibrated) — prefer it
- Caveats: it's *asymptotic* (use exact/bootstrap versions for small n), and the &chi;&sup2; limit **fails on the boundary** — if H&#8320; sits at the edge of the parameter space (e.g. a variance component = 0), the limit is a *mixture* of &chi;&sup2;'s (Self&ndash;Liang, Chernoff), not a plain &chi;&sup2;

---

## p-Values And Multiplicity

- The **p-value** is p(X) = sup_{&theta; &isin; &Theta;&#8320;} P&#952;( T(X') is at least as extreme as T(X) ) — the probability, under the *most favorable* null, of a test statistic as or more extreme than the observed one; equivalently, the smallest &alpha; at which you'd reject. Under a simple H&#8320; with continuous T it is **exactly Uniform(0,1)**; in discrete or composite cases it's stochastically &geq; uniform (conservative)
- What it is **not**: P(H&#8320; is true | data) (that needs a prior), nor 1 &minus; P(H&#8321;), nor a measure of effect size; "p &lt; 0.05" is a convention, not a law of nature, and a "significant" tiny effect can be utterly unimportant — always pair p with an effect size and a confidence interval
- **Multiple testing**: run m independent level-&alpha; tests under all-true nulls and you expect &alpha;m false rejections; control the **family-wise error rate** P(any false rejection) by Bonferroni (use &alpha;/m — simple, conservative), Holm (uniformly better, still FWER), or Šidák; or control the **false discovery rate** E[false rejections / total rejections] by Benjamini&ndash;Hochberg — far more powerful when m is large (genomics, many metrics, many subgroups)
- The garden of forking paths / **p-hacking**: choosing the hypothesis, the test, the covariates, or the stopping rule *after* seeing the data inflates the true Type I rate without ever printing a "corrected" number — *pre-register* the analysis, or treat post-hoc findings as hypotheses for fresh data
- **Optional stopping**: peeking at the data and stopping the first time p &lt; 0.05 makes the actual Type I rate balloon (toward 1 as you peek indefinitely) — use a procedure *designed* for sequential looks: group-sequential boundaries (O'Brien&ndash;Fleming, Pocock), alpha-spending functions, or always-valid e-values / e-processes

---

## The Duality With Confidence Sets

- **Inverting tests &#8658; confidence sets**: if for each &theta;&#8320; you have a level-&alpha; test of H&#8320;: &theta; = &theta;&#8320; with acceptance region A(&theta;&#8320;), then C(X) = { &theta;&#8320; : X &isin; A(&theta;&#8320;) } — the set of null values *not* rejected — is a **(1&minus;&alpha;) confidence set**: P&#952;( &theta; &isin; C(X) ) &geq; 1&minus;&alpha; for all &theta;
- The converse holds too: from any confidence set you read off a test of each point null — "reject &theta;&#8320; iff &theta;&#8320; &notin; C(X)" — so **tests and confidence sets are two views of one object**
- Optimality transfers: inverting a UMP/UMPU test family yields a confidence set that's optimal in the matching sense (uniformly most accurate / shortest expected length); the t-interval is the inversion of the UMPU t-test, the binomial Clopper&ndash;Pearson interval inverts exact binomial tests, profile-likelihood intervals invert LR tests, Wald intervals invert Wald tests
- Practical upshot: **report the confidence set**, not just the p-value — it answers "is &theta;&#8320; rejected?" for *every* &theta;&#8320; at once *and* delivers the magnitude and precision; "0 &notin; 95% CI for the difference" is exactly "reject equality at 0.05, two-sided"
- This duality is also the engine behind *bootstrap* and *permutation* confidence intervals: invert the corresponding resampling test

---

## Testing Theory In Code

```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(11)
# Neyman-Pearson for N(theta,1), n=25: most powerful test of theta=0 vs theta=0.5 rejects for large Xbar.
# Its size is exactly alpha and (by NP) no level-alpha test beats its power.
n, alpha, R = 25, 0.05, 200_000
crit = stats.norm.ppf(1-alpha) / np.sqrt(n)                 # reject if Xbar > crit
size  = np.mean(rng.normal(0.0, 1, (R, n)).mean(axis=1) > crit)
power = np.mean(rng.normal(0.5, 1, (R, n)).mean(axis=1) > crit)
print(f"size ~ {alpha}: {size:.3f}   power at theta=0.5: {power:.3f}")

# Wilks: -2 log LR for H0: variance = 1 in N(0, sigma^2), n=40, is ~ chi^2_1 under H0
x = rng.normal(0, 1, (R, 40))
s2 = x.var(axis=1, ddof=0)                                   # MLE of sigma^2 (mean known = 0)
LR = 40 * (s2 - 1 - np.log(s2))                              # = -2 log lambda for this model
print("Wilks KS-vs-chi2_1 p:", stats.kstest(LR, "chi2", args=(1,)).pvalue.round(3))
```

---

## Common Mistakes

- Reading the p-value as P(H&#8320; true | data), or treating "not significant" as "H&#8320; is true"
- Expecting a UMP test for a two-sided alternative — they generally don't exist; you must restrict to unbiased or invariant tests
- Applying Wilks' &chi;&sup2; limit on the parameter boundary (variance components, one-sided nulls) — the limit is a &chi;&sup2; *mixture* there
- Running many tests (subgroups, metrics, model variants) and reporting the smallest p without FWER/FDR control — and peeking/optional stopping without a sequential design
- Reporting only a p-value when the dual confidence set carries the test result *plus* the effect size and precision
