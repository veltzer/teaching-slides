---
tags:
  - math:bayesian
level: intermediate
category: math
audience:
  - audiences:data-analysts
  - audiences:data-scientists

---

# Bayesian Inference Basics

---

## What This Chapter Covers

- The Bayesian view: parameters have distributions
- Prior, likelihood, posterior
- Conjugate priors and a worked example
- Credible intervals vs confidence intervals
- Posterior predictive checks
- When and why to compute the posterior numerically (MCMC)

---

## Prior × Likelihood → Posterior

![prior_likelihood_posterior](svg/courses/math/statistics-inference/14_bayesian_basics/prior_likelihood_posterior.svg)

---

## A Different Stance On Uncertainty

- **Frequentist**: the parameter is a fixed unknown; probability describes the *procedure* (over hypothetical repeated samples)
- **Bayesian**: the parameter is uncertain, so we give it a *probability distribution* that we update with data
- Both use the same likelihoods; they differ in what they're willing to put a probability on
- Bayesian inference lets you say "there's a 95% probability the rate is between 3% and 5%" — literally, about *this* dataset
- Neither is universally "right" — pick the one whose outputs answer your actual question

---

## Prior, Likelihood, Posterior

- **Prior** P(&theta;): what you believe about the parameter *before* seeing this data — from past studies, domain knowledge, or deliberately vague ("weakly informative")
- **Likelihood** P(data | &theta;): how probable the observed data is for each parameter value — the same likelihood used everywhere in this course
- **Posterior** P(&theta; | data) &prop; likelihood &times; prior — your updated belief after the data; this *is* the inference
- The denominator (the marginal likelihood / evidence) just normalizes things to sum to 1
- One slogan: **posterior &prop; prior &times; likelihood** — Bayes' theorem doing its job on parameters

---

## Conjugate Priors

- A prior is **conjugate** to a likelihood if the posterior is in the same family — the update is then just arithmetic on the parameters, no integration
- The classic: **Beta prior + Binomial likelihood &#8594; Beta posterior**. Start with Beta(a, b); observe s successes and f failures; posterior is Beta(a + s, b + f)
- Beta(1, 1) is the uniform prior — "I know nothing"; Beta(2, 2) is a gentle nudge toward 0.5; large a, b is a confident prior
- Other pairs: Normal&ndash;Normal (for a mean with known variance), Gamma&ndash;Poisson (for a rate)
- Conjugacy is mostly a teaching and prototyping convenience now — real models use numerical methods — but it builds the right intuition

---

## A Worked Beta&ndash;Binomial Example

```python
import numpy as np
from scipy import stats
a0, b0 = 1, 1                       # Beta(1,1): uniform prior on the conversion rate
successes, failures = 8, 142        # observed: 8 conversions in 150 visitors
a, b = a0 + successes, b0 + failures
post = stats.beta(a, b)
print(f"posterior mean = {post.mean():.3%}")
print(f"95% credible interval = "
      f"[{post.ppf(0.025):.3%}, {post.ppf(0.975):.3%}]")
print(f"P(rate > 4%) = {1 - post.cdf(0.04):.2%}")   # a question frequentists can't phrase
```

- The posterior is a full distribution — summarize it however the decision needs

---

## Credible Intervals vs Confidence Intervals

- A **credible interval** is a range that contains the parameter with stated *probability* — "95% probability &theta; is in [a, b]", a direct statement about &theta; given this data
- A **confidence interval** is the frequentist analog with a *procedural* guarantee — "95% of intervals built this way would contain &theta;" — *not* a probability about this particular interval
- With a flat prior and enough data, the two often nearly coincide numerically — but they *mean* different things
- Two flavors of credible interval: the **equal-tailed** one (2.5% in each tail) and the **highest-posterior-density (HPD)** one (the shortest interval with the given mass) — they differ for skewed posteriors
- Most people *want* the credible-interval interpretation — just be honest about which one you actually computed

---

## Credible vs Confidence Interval

![credible_vs_confidence](svg/courses/math/statistics-inference/14_bayesian_basics/credible_vs_confidence.svg)

---

## Posterior Predictive Checks

- Beyond estimating &theta;, simulate **new data** from the fitted model (draw &theta; from the posterior, then data from the likelihood) — that's the **posterior predictive distribution**
- Compare those simulated datasets to the real one: do key features (max, variance, number of zeros, a relevant tail probability) look alike?
- A glaring mismatch means the model is misspecified — wrong likelihood, missing structure — no amount of "but the posterior is tight" saves it
- It's the Bayesian counterpart to residual diagnostics in regression: check the model, don't just report it
- Also use the posterior predictive for honest forecasts — it bakes in *both* parameter uncertainty and irreducible noise

---

## When Conjugacy Runs Out: MCMC

- Real models (many parameters, hierarchical structure, non-conjugate priors) have posteriors with no closed form and impossible-to-do integrals
- **Markov chain Monte Carlo (MCMC)** — and modern variants like Hamiltonian Monte Carlo / NUTS — *draws samples* from the posterior instead of computing it analytically; you summarize the samples
- Probabilistic programming tools (PyMC, Stan, NumPyro) let you write the model declaratively and handle the sampling for you
- Always check the diagnostics: trace plots that look like "fuzzy caterpillars", R-hat near 1.0, adequate effective sample size — a chain that hasn't converged gives garbage that *looks* like an answer
- **Hierarchical (multilevel) models** are where Bayesian methods especially shine — partial pooling across groups, principled shrinkage, honest uncertainty when some groups have little data

---

## Common Mistakes

- Pretending the prior is "objective" — every analysis has assumptions; state the prior and check sensitivity to it
- Reporting a frequentist confidence interval but describing it as a credible interval (the "95% probability" phrasing)
- Treating MCMC output as trustworthy without checking R-hat, effective sample size, and trace plots
- Skipping posterior predictive checks — a tight posterior on a wrong model is still wrong
- Reaching for heavy Bayesian machinery when a conjugate update or a frequentist method answers the question just as well
