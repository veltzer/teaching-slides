---
tags:
  - math:bayesian
level: advanced
category: math
audience:
  - audiences:data-scientists
  - audiences:ml-engineers

---

# Bayesian Theory

---

## What This Chapter Covers

- Priors, posteriors, and the formal Bayesian model
- Conjugacy and the exponential family
- Bayes estimators and decision theory
- Credible sets and how they relate to confidence sets
- Asymptotics: the Bernstein&ndash;von Mises theorem
- Admissibility, the complete-class theorems, and objective priors

---

## Prior, Likelihood, Posterior

![prior posterior](svg/courses/math/statistics-theory/14_bayesian_theory/prior_posterior.svg)

---

## The Bayesian Model, Formally

- Add to the sampling model { f(x | &theta;) : &theta; &isin; &Theta; } a **prior** &pi;(&theta;) — a probability distribution on &Theta; encoding beliefs (or a chosen reference) *before* the data; this turns &theta; into a random variable
- **Bayes' theorem** gives the **posterior**: &pi;(&theta; | x) = f(x | &theta;) &pi;(&theta;) / m(x), where m(x) = &#8747; f(x | &theta;) &pi;(&theta;) d&theta; is the **marginal likelihood / evidence**. Compactly: **posterior &prop; likelihood &times; prior**
- The posterior *is* the inference — point estimates (posterior mean/median/mode), interval estimates (credible sets), tests (posterior odds), and predictions (the **posterior predictive** &#8747; f(x_new | &theta;) &pi;(&theta; | x) d&theta;) are all read off it
- It updates **sequentially and coherently**: today's posterior is tomorrow's prior; the order in which i.i.d. data arrive doesn't matter, and (under the likelihood principle) only the observed likelihood matters
- **Improper priors** (&#8747;&pi; = &infin;, e.g. "flat on &#8477;") are allowed *if* the posterior comes out proper — convenient, but check; an improper posterior is a non-result

---

## Conjugacy And The Exponential Family

- A prior family is **conjugate** to a likelihood if the posterior stays in the same family — then Bayes' theorem is just an *update of the prior's parameters*, no integration needed
- Canonical pairs: **Beta&ndash;Binomial** ( Beta(a,b) + s successes, f failures &#8594; Beta(a+s, b+f) ), **Gamma&ndash;Poisson** (rate), **Normal&ndash;Normal** (mean, known variance), **Normal-inverse-Gamma** (mean and variance), **Dirichlet&ndash;Multinomial** — each posterior parameter = prior parameter + a sufficient-statistic contribution from the data
- General fact: **every full-rank exponential family has a conjugate prior**, itself of exponential-family form; the conjugate "hyperparameters" act like a *pseudo-dataset* (prior sample size + prior sufficient statistic), so the posterior mean is a precision-weighted blend of the prior guess and the sample statistic — visibly "shrinkage toward the prior"
- As data accumulates the likelihood dominates: the prior's pseudo-counts become negligible, and the posterior concentrates near the MLE regardless of (any reasonable) prior — quantified by Bernstein&ndash;von Mises below
- Conjugacy is now mostly a *teaching and prototyping* device; real models are non-conjugate and the posterior is approximated numerically (MCMC, variational inference) — but the conjugate cases build the right intuition and are the building blocks of hierarchical models

---

## Bayes Estimators And Decision Theory

- Pick a loss L(&theta;, a); the **Bayes estimator** minimizes the *posterior expected loss* &#8747; L(&theta;, a) &pi;(&theta; | x) d&theta; — equivalently it minimizes the **Bayes risk** r(&pi;, &delta;) = &#8747; R(&theta;, &delta;) &pi;(&theta;) d&theta;, the prior-averaged frequentist risk
- The loss picks the summary: **squared error &#8594; posterior mean**; **absolute error &#8594; posterior median**; **0&ndash;1 loss &#8594; posterior mode (MAP)** — so "which point estimate?" is a *decision*, not a default
- This is the cleanest answer to "how should I choose an estimator?": there's no uniformly best frequentist estimator (risk curves cross), but *fix a prior* and the optimum is unique and constructive
- **Hypothesis testing the Bayesian way**: compare hypotheses by **posterior odds** = **prior odds &times; Bayes factor**, where the Bayes factor B&#8321;&#8320; = m&#8321;(x)/m&#8320;(x) is the ratio of marginal likelihoods — it weighs evidence directly, automatically penalizes complexity (an "Occam factor"), and *can* favor the null (unlike a p-value); but it's sensitive to the prior on the parameters under H&#8321; (the **Jeffreys&ndash;Lindley paradox**: with a very diffuse alternative prior, a fixed p-value can correspond to *strong* evidence *for* H&#8320;)
- Prediction is decision-theoretic too: the posterior predictive minimizes expected predictive loss and correctly propagates **both** parameter uncertainty and irreducible noise — the right thing to report instead of a plug-in forecast

---

## Credible Sets vs Confidence Sets

- A **credible set** C with &#8747;_C &pi;(&theta; | x) d&theta; = 1&minus;&alpha; is, by construction, a *probability statement about &theta; given the data*: P(&theta; &isin; C | x) = 1&minus;&alpha; — the interpretation most people *want* (and wrongly attach to confidence intervals)
- Two standard flavors: the **equal-tailed** interval (&alpha;/2 posterior mass in each tail — transformation-respecting, simple) and the **highest-posterior-density (HPD)** region (the *shortest* set with the given mass — { &theta; : &pi;(&theta; | x) &geq; c } — possibly disconnected for multimodal posteriors). They coincide for symmetric unimodal posteriors and differ for skewed ones
- Frequentist coverage of a credible set is *not* automatically 1&minus;&alpha; — it depends on the prior; with a "matching" or reference prior it can be 1&minus;&alpha; to high order, and with a flat prior it often nearly equals the corresponding confidence interval **numerically** even though the *meaning* differs
- Symmetrically, a confidence set generally has no clean posterior interpretation — the two are different objects that happen to be close in regular large-sample problems and can diverge sharply in small samples, near boundaries, or with strong priors
- Honesty rule: report which one you actually computed and under which prior — don't compute a confidence interval and describe it with the "95% probability the parameter is in here" credible-set language

---

## Asymptotics: Bernstein&ndash;von Mises

- **Bernstein&ndash;von Mises theorem**: in a regular parametric model, as n &#8594; &infin; the posterior is asymptotically **Normal**, centered at the MLE &theta;&#770;&#8345;, with covariance the inverse Fisher information: &pi;(&theta; | x&#8321;,...,x&#8345;) &asymp; N( &theta;&#770;&#8345;, [n I&#8321;(&theta;&#8320;)]&#8315;&sup1; ) — and the dependence on the (continuous, positive) prior **washes out**
- Consequence — **frequentist&ndash;Bayesian reconciliation**: Bayesian credible sets and frequentist confidence sets *agree to leading order* in regular problems; "the data swamps the prior" is a theorem, not a hope, so the prior choice matters most exactly when data is scarce
- Also implies posterior consistency (the posterior concentrates at &theta;&#8320;) and that the posterior mean/median/mode are all asymptotically equivalent to the MLE and asymptotically efficient
- **Where it fails** — and the prior keeps mattering: irregular models (support depending on &theta;, like Uniform(0,&theta;) — posterior is Pareto-shaped, not Normal); parameters on a boundary; **nonparametric / high-dimensional** models (BvM can fail; credible bands need not have the nominal frequentist coverage — a live research area); and of course small n
- Bottom line: in nice large-sample problems Bayesian and frequentist machinery converge; the genuine divergences (and the genuine value-add of priors) are in *small samples, hierarchical pooling, and irregular models*

---

## Admissibility, Complete Classes, Objective Priors

- Bayes meets decision theory: under mild conditions a Bayes estimator (with a proper prior, unique Bayes rule) is **admissible** — not uniformly dominated by any other estimator; conversely the **complete-class theorems** say (essentially) every admissible estimator *is* a Bayes rule or a limit of Bayes rules. So "admissible" &asymp; "Bayes for some prior" — the Bayesian framework *generates* the good frequentist procedures
- A Bayes rule with **constant frequentist risk** is **minimax** — a slick route to minimax estimators (find the "least favorable prior" whose Bayes rule has flat risk); this is how many classical minimax results are actually proved
- The flip side of Stein's paradox: in dimension n &geq; 3 the usual estimator of a normal mean is inadmissible, and the estimators that *dominate* it are (empirical-)Bayes shrinkage rules — admissibility theory *predicts* that shrinkage must win, and the Bayesian/hierarchical viewpoint *constructs* the winners (ridge regression, James&ndash;Stein, hierarchical models are all this idea)
- **Objective / reference priors** when you want "let the data speak": **Jeffreys' prior** &pi;(&theta;) &prop; &radic;det I(&theta;) (invariant under reparametrization — its defining virtue), **reference priors** (Bernardo — maximize the expected information the data adds), **maximum-entropy** priors (least committal given stated constraints); these are often *improper*, so always verify the posterior is proper, and beware that "objective" is a name, not a guarantee — different objective recipes disagree, especially in multiparameter problems
- **Sensitivity analysis is mandatory**: report results under a few defensible priors (an informative one, a weakly-informative one, a reference one); if conclusions swing with the prior, *that* is the finding — say so rather than hiding behind one prior

---

## Bayesian Theory In Code

```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(13)

# Beta-Binomial conjugacy: posterior = Beta(a + s, b + f); posterior mean blends prior & data
a, b = 2, 2                                  # weakly informative prior centered at 0.5
s, f = 9, 41                                 # observed: 9 successes in 50 trials
post = stats.beta(a + s, b + f)
print(f"posterior mean = {post.mean():.3f}   (MLE = {s/(s+f):.3f})")
print(f"equal-tailed 95% credible interval = [{post.ppf(.025):.3f}, {post.ppf(.975):.3f}]")
print(f"P(p > 0.10 | data) = {post.sf(0.10):.3f}")          # a direct probability about p

# Bernstein-von Mises: with lots of data the posterior ~ N(MLE, 1/(n I_1)) regardless of (reasonable) prior
n = 5000; x = rng.binomial(1, 0.10, n)
for (a0, b0) in [(1, 1), (50, 5), (2, 200)]:                # very different priors
    pst = stats.beta(a0 + x.sum(), b0 + n - x.sum())
    print(f"prior Beta({a0},{b0}): post mean {pst.mean():.4f}, sd {pst.std():.4f}  "
          f"vs Normal approx sd {np.sqrt(0.1*0.9/n):.4f}")
```

---

## Common Mistakes

- Pretending a prior is "objective" and assumption-free — it isn't; report it, justify it, and check sensitivity to it
- Forgetting to verify the posterior is proper when using an improper prior
- Treating a frequentist confidence interval as a credible set ("95% probability &theta; is in here") — the guarantees and meanings differ
- Reading off the Bayes factor without noticing its dependence on the alternative-hypothesis prior (the Jeffreys&ndash;Lindley paradox)
- Assuming "the data overwhelms the prior" universally — Bernstein&ndash;von Mises fails for irregular, boundary, and nonparametric/high-dimensional models, exactly where priors matter most
