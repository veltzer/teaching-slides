---
tags:
  - math:random-variables
level: advanced
category: math
audience:
  - audiences:data-scientists
  - audiences:ml-engineers

---

# Random Variables and Distributions

---

## What This Chapter Covers

- Random variables as measurable functions
- The distribution (law) of a random variable
- The cumulative distribution function and its properties
- Discrete, absolutely continuous, and the general case
- The probability integral transform
- Functions of a random variable

---

## Distribution Functions: CDF, PMF, PDF

![cdf pmf pdf](svg/courses/math/statistics-theory/03_random_variables/cdf_pmf_pdf.svg)

---

## A Random Variable Is A Function

- Given (&Omega;, F, P), a **random variable** X is a function X : &Omega; &#8594; &#8477; that is **measurable**: for every Borel set B, X&#8315;&sup1;(B) = {&omega; : X(&omega;) &isin; B} &isin; F
- Measurability is exactly the condition that lets us *ask* "what is P(X &isin; B)?" — the preimage has to be an allowed event
- Equivalent, easier-to-check criterion: X&#8315;&sup1;((&minus;&infin;, x]) &isin; F for every real x
- Intuition: X is a numerical readout of the random outcome; the &omega; itself usually fades into the background once X is defined
- A **random vector** is a measurable map into &#8477;&#8319;; same definition, Borel sets of &#8477;&#8319;

---

## The Distribution Of X

- X pushes the measure P forward to a measure **P_X on (&#8477;, B)** defined by P_X(B) = P(X &isin; B) — the **distribution** or **law** of X
- (&#8477;, B, P_X) is itself a probability space — so we can, and almost always do, work *with the distribution* and forget the original &Omega;
- Two random variables (possibly on different spaces) are **equal in distribution**, X =&#x1D48;= Y, if P_X = P_Y — they may be very different functions yet statistically interchangeable
- This is why "let X ~ N(0,1)" is a complete specification: it names the law, which is all that matters for probabilities of X
- Every statement about X's probabilities is really a statement about P_X

---

## The Cumulative Distribution Function

- The **CDF** F_X(x) = P(X &leq; x) = P_X((&minus;&infin;, x]) — a single function of a real variable that *encodes the entire law*
- Characterizing properties: (i) non-decreasing; (ii) right-continuous; (iii) F(&minus;&infin;) = 0, F(+&infin;) = 1
- Conversely, **any** function with those three properties is the CDF of some random variable (build P_X via Lebesgue&ndash;Stieltjes) — so "CDF" and "distribution on &#8477;" are interchangeable
- Useful read-offs: P(a &lt; X &leq; b) = F(b) &minus; F(a); P(X = x) = F(x) &minus; F(x&#8315;) = the jump of F at x (zero where F is continuous)
- The CDF always exists, even when there's no density and no mass function — it's the universal description

---

## Three Kinds Of Distribution

- **Discrete**: X takes values in a countable set; described by a **probability mass function** p(x) = P(X = x) with &Sigma; p(x) = 1; the CDF is a step function
- **Absolutely continuous**: F is an integral, F(x) = &#8747;&#8331;&#8336;&#9143; f(t) dt, for a **density** f &geq; 0 with &#8747; f = 1; then P(X = x) = 0 for every x, and P(X &isin; B) = &#8747;&#8336; f
- **Singular continuous**: F is continuous (no jumps) yet has zero derivative almost everywhere — the Cantor distribution is the standard example; rare in practice but it shows the trichotomy is real
- **Lebesgue decomposition**: *every* distribution on &#8477; is uniquely a mixture of these three pieces — discrete + absolutely continuous + singular
- Densities are derivatives (Radon&ndash;Nikodym) of P_X with respect to Lebesgue measure; mass functions are derivatives with respect to counting measure — same idea, different reference measure

---

## The Probability Integral Transform

- If X is continuous with CDF F, then **U = F(X) ~ Uniform(0, 1)** — the "PIT"
- Conversely, if U ~ Uniform(0,1), then **X = F&#8315;&sup1;(U)** has CDF F — *inverse-transform sampling*, the basic way to generate a variate with any prescribed distribution from a uniform source
- F&#8315;&sup1; here is the **quantile function** (generalized inverse: F&#8315;&sup1;(u) = inf{x : F(x) &geq; u}), which works even when F has flat spots or jumps
- Consequences everywhere: it's behind copulas (model dependence on the uniform scale), Q&ndash;Q plots (does F(data) look uniform?), and many goodness-of-fit and simulation methods
- One-line slogan: the quantile function turns "uniform randomness" into "any randomness you want"

---

## Functions Of A Random Variable

- If X is a random variable and g : &#8477; &#8594; &#8477; is measurable (e.g. continuous), then Y = g(X) is again a random variable; its law is the pushforward of P_X by g
- General recipe via the CDF: F_Y(y) = P(g(X) &leq; y) = P_X({x : g(x) &leq; y}) — describe that x-set, then differentiate if you want a density
- **Monotone smooth g** (the change-of-variables formula): if g is strictly increasing/decreasing and differentiable, f_Y(y) = f_X(g&#8315;&sup1;(y)) &middot; |d/dy g&#8315;&sup1;(y)| — the familiar Jacobian rule
- **Non-monotone g**: sum the contributions over all branches of g&#8315;&sup1;(y) — e.g. Y = X&sup2; gets a term from +&radic;y and one from &minus;&radic;y
- Non-invertible or discrete/continuous-mixing g: fall back to the CDF method — it never fails, the formulas are just shortcuts

---

## Distributions In Code

```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(2)

# inverse-transform sampling: build Exp(rate=1.5) from uniforms via the quantile fn
u = rng.random(100_000)
x = stats.expon(scale=1/1.5).ppf(u)        # F^{-1}(U)
print("mean ~ 1/1.5 =", x.mean().round(3), " KS p:", stats.kstest(x, stats.expon(scale=1/1.5).cdf).pvalue.round(3))

# probability integral transform: F(X) should be Uniform(0,1)
y = rng.standard_normal(100_000)
u2 = stats.norm.cdf(y)
print("PIT mean ~ 0.5:", u2.mean().round(3), " KS-vs-uniform p:", stats.kstest(u2, "uniform").pvalue.round(3))
```

---

## Common Mistakes

- Forgetting the measurability requirement — without it "P(X &isin; B)" need not even be defined
- Treating "density" as universal — many distributions (any with atoms, or the singular ones) have no density
- Confusing the density f with a probability — f(x) can exceed 1; only its *integral* over a set is a probability, and P(X = x) = 0 in the continuous case
- Applying the smooth change-of-variables formula to a non-monotone g (you must add all the branches)
- Using F&#8315;&sup1; carelessly when F is flat or jumps — use the generalized (quantile-function) inverse
