---
tags:
  - math:inferential-statistics
level: advanced
category: math
audience:
  - audiences:data-scientists
  - audiences:ml-engineers

---
# Confidence Sets and Duality

---
## What This Chapter Covers

- The formal definition of a confidence set
- Construction via pivots
- Construction by inverting tests
- Optimality: most accurate and shortest sets
- Asymptotic intervals: Wald, score, likelihood-ratio
- Simultaneous confidence regions and multiplicity

---
## What A Confidence Set Is

- A **confidence set** of level 1&minus;&alpha; for &psi;(&theta;) is a *data-dependent* set C(X) with **coverage** P&#952;( &psi;(&theta;) &isin; C(X) ) &geq; 1&minus;&alpha; for **every** &theta; — the guarantee is uniform over the parameter space, and it's a statement about the *procedure*
- The randomness lives in C(X), not in &theta;: "a 95% CI" means the *recipe* traps the truth in 95% of repetitions; a *particular* realized interval [a, b] either contains &psi;(&theta;) or doesn't — "95% probability &psi; &isin; [a,b]" is the Bayesian (credible-set) reading and needs a prior
- **Exact** coverage = 1&minus;&alpha; (continuous, regular problems); **conservative** coverage &gt; 1&minus;&alpha; (often forced in discrete problems — e.g. Clopper&ndash;Pearson for a binomial — where no recipe hits &alpha; on the nose without randomization)
- A confidence set need not be an interval: it can be a half-line (one-sided bound), a disconnected set, a region in &#8477;&#7496; (joint), or even empty (a legitimate, if unsettling, outcome for some likelihood-based sets)
- Three knobs you trade against each other: **coverage** (raise it &#8658; wider), **size/length** (precision), and which **direction(s)** you bound (one- vs two-sided)

---
## Construction Via Pivots

- A **pivotal quantity** Q(X, &theta;) is a function of data *and* parameter whose distribution is **completely known** — it does not depend on &theta; (nor on any nuisance parameter)
- Recipe: find a pivot, bracket its central 1&minus;&alpha; probability ( a &leq; Q(X, &theta;) &leq; b ), then **solve the inequalities for &theta;** — the resulting &theta;-set is a 1&minus;&alpha; confidence set, automatically, by construction
- Canonical example: X&#8345; i.i.d. N(&mu;,&sigma;&sup2;) &#8658; Q = (X&#772; &minus; &mu;)/(S/&radic;n) ~ t&#8345;&#8331;&#8321; (a pivot — distribution free of both &mu; and &sigma;); bracketing the central 1&minus;&alpha; probability of Q and solving for &mu; gives X&#772; &plusmn; t&#8901;&middot;S/&radic;n. Likewise (n&minus;1)S&sup2;/&sigma;&sup2; ~ &chi;&sup2;&#8345;&#8331;&#8321; yields the variance interval
- **Approximate / asymptotic pivots**: &radic;n(&theta;&#770; &minus; &theta;)/se(&theta;&#770;) &#8658; N(0,1) (Wald), the **probability integral transform** F&#952;(X) ~ Uniform (when it can be inverted in &theta;), and bootstrap "studentized" statistics — same machinery, coverage now only ~1&minus;&alpha;
- When no pivot exists (most nuisance-parameter problems), you fall back to **inverting a test** — which always works

---
## Construction By Inverting Tests

- **The universal recipe** (the duality of the previous chapter, run as a *construction*): for each candidate value &psi;&#8320;, take a level-&alpha; test of H&#8320;: &psi;(&theta;) = &psi;&#8320; with acceptance region A(&psi;&#8320;); then **C(X) = { &psi;&#8320; : X &isin; A(&psi;&#8320;) }** — the set of values *not rejected* — has coverage &geq; 1&minus;&alpha; for free
- It needs *no pivot* and handles **nuisance parameters** cleanly: use a test that already does (a t-test, an exact conditional test, a profile-likelihood test), and the nuisance is dealt with inside the test
- Conversely every confidence set defines a family of tests ("reject &psi;&#8320; iff &psi;&#8320; &notin; C(X)") — tests and confidence sets are **the same object viewed two ways**; "&psi;&#8320; &notin; 95% CI" &hArr; "reject &psi; = &psi;&#8320; at level 0.05"
- Worked examples: Clopper&ndash;Pearson binomial interval = invert exact binomial tests; the **profile-likelihood interval** = invert the likelihood-ratio test ( { &psi;&#8320; : 2[&#8467;(&theta;&#770;) &minus; sup_{&psi;=&psi;&#8320;} &#8467;] &leq; &chi;&sup2;&#8321;,&#8321;&#8331;&#945; } ); Fieller's interval for a ratio of means = invert the natural test; **bootstrap and permutation CIs** = invert the corresponding resampling test
- This is *the* method to reach for when the textbook formula fails — it can't, structurally, miscover

---
## Optimality: Most Accurate, Shortest

- "Has correct coverage" is a *floor*, not a goal — a half-line, or [&minus;&infin;, &infin;] with probability 1&minus;&alpha; and &empty; otherwise, both "cover". Among correctly-covering sets we want the one that **excludes wrong values most often**
- **Uniformly most accurate (UMA)**: a set whose probability of covering any *false* value &psi;' &ne; &psi;(&theta;), i.e. P&#952;( &psi;' &isin; C(X) ), is minimized — uniformly over &theta; and &psi;'. By duality, **inverting a UMP test &#8658; a UMA confidence set**; inverting a UMPU (unbiased) test &#8658; a **UMA-unbiased** set (the right notion for two-sided problems, since plain UMA sets usually don't exist there)
- **Shortest / smallest**: among 1&minus;&alpha; intervals, minimize length (or expected length, or volume in &#8477;&#7496;). In a *symmetric* problem the equal-tailed and shortest intervals coincide; in a *skewed* one they differ — the shortest interval is *unbalanced*, and (likelihood-based) **highest-density**-type regions are the natural "smallest" choice
- For a location parameter the **equivariant** requirement (the interval shifts with the data) is what singles out the optimal interval — the invariance principle again, mirroring how it pinned down optimal tests and estimators
- Practical translation: prefer **likelihood-ratio / score** intervals (which respect the model's geometry, transform correctly, and are near-shortest) over crude **Wald** intervals when they disagree

---
## Asymptotic Intervals: Wald, Score, Likelihood-Ratio

- Three asymptotically-equivalent 1&minus;&alpha; intervals for a scalar &theta;, dual to the three tests of Chapter 11&ndash;12, each "centered" differently:
    - **Wald**: &theta;&#770; &plusmn; z&#8901; / &radic;( I_n(&theta;&#770;) ) (or use observed information / a robust sandwich SE) — trivial to compute, but **not parametrization-invariant** (a Wald interval for &sigma; isn't the square root of one for &sigma;&sup2;), can stray outside the parameter space (negative variances, probabilities &gt; 1), and is poor near boundaries or under weak identification
    - **Score (Rao)**: { &theta;&#8320; : &#8467;'(&theta;&#8320;)&sup2; / I_n(&theta;&#8320;) &leq; z&#8901;&sup2; } — needs only the *restricted* fit, naturally respects the parameter range; the Wilson interval for a binomial p is exactly the score interval (and far out-performs the Wald "p&#770; &plusmn; z&radic;(p&#770;(1&minus;p&#770;)/n)" near 0 and 1)
    - **Likelihood-ratio (profile)**: { &theta;&#8320; : 2[ &#8467;(&theta;&#770;) &minus; &#8467;_profile(&theta;&#8320;) ] &leq; &chi;&sup2;&#8321;,&#8321;&#8331;&#945; } — **parametrization-invariant**, generally the best finite-sample coverage, the recommended default; just possibly disconnected or asymmetric (which is *honest* when the likelihood is)
- All three deliver coverage &#8594; 1&minus;&alpha; *as n &#8594; &infin;*; for small n, near a boundary (the &chi;&sup2; becomes a mixture), or with separation, they can each miscover — then use **exact**, **conditional**, or **bootstrap** intervals (the studentized / BCa bootstrap intervals are second-order accurate, better than first-order Wald)
- Multivariate version: an asymptotic **confidence ellipsoid** { &theta; : (&theta;&#770; &minus; &theta;)&#7488; I_n(&theta;&#770;) (&theta;&#770; &minus; &theta;) &leq; &chi;&sup2;&#7496;,&#8321;&#8331;&#945; } — Wald-flavored; the LR version uses the joint profile

---
## Simultaneous Confidence Regions

- A *joint* 1&minus;&alpha; set for a **vector** &psi; = (&psi;&#8321;,...,&psi;&#8344;) must cover **all** components at once: P&#952;( &psi; &isin; C(X) ) &geq; 1&minus;&alpha; — not the same as p separate 1&minus;&alpha; intervals, which jointly cover only roughly (1&minus;&alpha;)&#7510; (much less than 1&minus;&alpha;)
- This is the *confidence-set* face of the **multiple-comparisons** problem: building k intervals that *simultaneously* hold needs each to be wider. Tools: **Bonferroni** (use level &alpha;/k each — simple, conservative), **Šidák** (slightly tighter under independence), **Scheffé** ( for *all* linear contrasts at once — uses a &radic;(p F) constant, very wide but unlimited contrasts), **Tukey's HSD** (all pairwise differences after ANOVA — optimal for *that* family)
- A natural simultaneous region is the **confidence ellipsoid** above (the Wald or LR region for the whole parameter vector) — its 1-D "shadows" are the simultaneous Scheffé intervals; the ellipsoid can declare the vector different from a point even when *every* individual interval contains its null coordinate (and vice versa) — a geometric cousin of Simpson-style surprises
- **Confidence bands** are the function-valued case: a region covering an entire curve f(&middot;) (a regression line, a survival curve, a CDF) with simultaneous probability 1&minus;&alpha; — e.g. the Kolmogorov&ndash;Smirnov band around the empirical CDF, Working&ndash;Hotelling bands for a regression line; **pointwise** bands (one CI per x) are narrower but only cover *that x*, not the whole curve
- Rule of thumb: decide *up front* whether you need pointwise or simultaneous coverage, and over how many quantities — then widen accordingly; reporting many "95%" intervals and acting on the most extreme one is multiplicity by the back door

---
## Confidence Sets In Code

```python
import numpy as np
from scipy import stats, optimize
rng = np.random.default_rng(12)

# (1) pivot-based vs (2) bootstrap CI for a normal mean, and the matching test
x = rng.normal(5.0, 2.0, 40)
piv = stats.t.interval(0.95, len(x)-1, loc=x.mean(), scale=stats.sem(x))
boot = stats.bootstrap((x,), np.mean, confidence_level=0.95, method="BCa",
                       n_resamples=5000, random_state=rng).confidence_interval
print("t-pivot 95% CI:", np.round(piv, 3), "  BCa bootstrap 95% CI:", np.round(boot, 3))

# (3) profile-likelihood (LR) interval for an exponential rate -- invert the LR test
data = rng.exponential(scale=1/2.0, size=60)
negll = lambda L: -np.sum(stats.expon(scale=1/L).logpdf(data))
Lh = 1.0 / data.mean()                                   # MLE
g = lambda L: 2*(negll(L) - negll(Lh)) - stats.chi2.ppf(0.95, 1)   # = 0 at interval endpoints
lo = optimize.brentq(g, 1e-6, Lh); hi = optimize.brentq(g, Lh, 10*Lh)
print(f"MLE rate {Lh:.3f}  ->  LR 95% CI [{lo:.3f}, {hi:.3f}]   (Wald: {Lh*(1-1.96/np.sqrt(60)):.3f}..{Lh*(1+1.96/np.sqrt(60)):.3f})")
```

---
## Common Mistakes

- Saying "95% probability the parameter lies in *this* interval" — that's a credible set; a confidence set's guarantee is about the *procedure*, over repetitions
- Stopping at "correct coverage" — many silly sets cover; aim for **most accurate / shortest** (prefer LR/score over Wald when they disagree)
- Using the **Wald** interval near a boundary or for a bounded parameter (negative variances, p&#770; &plusmn; z&radic;(...) escaping [0,1]) instead of the score/LR/exact interval
- Treating asymptotic intervals as exact for small n, near a boundary (&chi;&sup2;-mixture issue), or under separation — switch to exact, conditional, or bootstrap procedures
- Reporting p separate 95% intervals and acting as if they hold *jointly* — that needs Bonferroni/Scheffé/Tukey-type widening or an explicit confidence region
