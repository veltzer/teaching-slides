---
tags:
  - math:random-variables
level: advanced
category: math
audience:
  - audiences:data-scientists
  - audiences:ml-engineers

---

# Expectation and Moments

---

## What This Chapter Covers

- Expectation as a Lebesgue integral
- The law of the unconscious statistician
- Linearity, monotonicity, and the convergence theorems
- Variance, higher moments, and the moment problem
- Moment and cumulant generating functions
- Key inequalities: Markov, Chebyshev, Jensen, Cauchy&ndash;Schwarz

---

## What Each Moment Tells You

![moments](svg/courses/math/statistics-theory/04_expectation_and_moments/moments.svg)

---

## Expectation Is An Integral

- **E[X] = &#8747;_&Omega; X dP** — the Lebesgue integral of the random variable against the probability measure
- Built in stages: define it for indicators (E[1&#8336;] = P(A)), extend by linearity to simple functions, then to X &geq; 0 by a supremum over simple functions below it, then to general X = X&#8314; &minus; X&#8315;
- X is **integrable** (E[X] is defined and finite) iff E|X| &lt; &infin;; otherwise E[X] may be &plusmn;&infin; or genuinely undefined (e.g. Cauchy)
- Crucially this is **not** "&Sigma; x p(x)" or "&#8747; x f(x) dx" by definition — those are *theorems* in the discrete and absolutely-continuous cases
- The single integral unifies all distribution types — discrete, continuous, mixed — under one definition

---

## Law Of The Unconscious Statistician

- To find E[g(X)] you do **not** need the law of g(X): **E[g(X)] = &#8747; g(x) dP_X(x)** — integrate g against X's *own* distribution
- Discrete case: &Sigma;_x g(x) p_X(x). Absolutely continuous case: &#8747; g(x) f_X(x) dx. General case: the Lebesgue&ndash;Stieltjes integral against F_X
- This is the workhorse for moments — E[X&#8319;] = &#8747; x&#8319; dP_X — and for anything else built from X
- Vector version: E[g(X&#8321;,...,X&#8345;)] = &#8747; g dP_(X&#8321;,...,X&#8345;), integrating against the *joint* law
- "Unconscious" because we use it so reflexively we forget it's a substitution theorem (the pushforward / change-of-variables identity)

---

## Core Properties

- **Linearity**: E[aX + bY] = aE[X] + bE[Y] — *always*, no independence needed (whenever the pieces are integrable)
- **Monotonicity**: X &leq; Y a.s. &#8658; E[X] &leq; E[Y]; in particular |E[X]| &leq; E|X|
- **Indicator / tail formula**: for X &geq; 0, E[X] = &#8747;&#8320;&#9034; P(X &gt; t) dt — expectation as the area under the survival curve
- **Product rule under independence**: X &#8869; Y &#8658; E[XY] = E[X]E[Y] (this one *does* need independence)
- **Conditioning (tower / law of total expectation)**: E[X] = E[ E[X | G] ] — average the conditional means

---

## The Convergence Theorems

- These say *when* you may swap a limit and an expectation — the central technical tools of the subject:
- **Monotone Convergence**: 0 &leq; X&#8345; &#8593; X a.s. &#8658; E[X&#8345;] &#8593; E[X]
- **Fatou's Lemma**: X&#8345; &geq; 0 &#8658; E[liminf X&#8345;] &leq; liminf E[X&#8345;]
- **Dominated Convergence**: X&#8345; &#8594; X a.s. and |X&#8345;| &leq; Y with E[Y] &lt; &infin; &#8658; E[X&#8345;] &#8594; E[X] (and E|X&#8345; &minus; X| &#8594; 0)
- Without a hypothesis like these, lim E &ne; E lim in general — "mass escaping to infinity" is the standard counterexample

---

## Variance And Higher Moments

- **Variance**: Var(X) = E[(X &minus; &mu;)&sup2;] = E[X&sup2;] &minus; &mu;&sup2; (when E[X&sup2;] &lt; &infin;); SD = &radic;Var; scaling Var(aX + b) = a&sup2;Var(X)
- **Covariance**: Cov(X, Y) = E[(X&minus;&mu;_X)(Y&minus;&mu;_Y)]; bilinear; Var(X+Y) = Var(X) + Var(Y) + 2Cov(X, Y); independence &#8658; Cov = 0 (the converse is false)
- **Higher moments**: the n-th raw moment E[X&#8319;], central moment E[(X&minus;&mu;)&#8319;]; **skewness** = &mu;&#8323;/&sigma;&sup3;, **(excess) kurtosis** = &mu;&#8324;/&sigma;&#8308; &minus; 3
- Existence is not automatic: a distribution may have a mean but no variance (some Pareto), or no mean at all (Cauchy) — heavy tails kill moments
- **Moment problem**: the moment sequence does *not* always determine the distribution — the classic counterexample is the lognormal, which shares all its moments with a family of other laws (Carleman's condition gives a sufficient condition for uniqueness)

---

## Generating Functions

- **Moment generating function** M_X(t) = E[e&#8348;&#7587;], when finite in a neighborhood of 0 — then moments fall out by differentiation: E[X&#8319;] = M_X&#8317;&#8319;&#8318;(0)
- When the MGF exists near 0 it **determines the distribution uniquely** and turns sums of independents into products: M_(X+Y) = M_X M_Y — the slick proof tool for "sum of Normals is Normal", etc.
- But the MGF often *fails to exist* (lognormal, Cauchy, t) — heavy tails again
- The **characteristic function** &phi;_X(t) = E[e&#8305;&#8348;&#7587;] always exists, always determines the law (uniqueness/inversion theorems), and is the right tool for the CLT (next chapter)
- **Cumulants** &kappa;_n come from log M_X(t) (or log &phi;): &kappa;&#8321; = mean, &kappa;&#8322; = variance, &kappa;&#8323; = third central moment, and cumulants of independent sums simply *add* — which is exactly why the normal (all &kappa;_n = 0 for n &geq; 3) is the natural "additive" limit

---

## The Workhorse Inequalities

- **Markov**: X &geq; 0 &#8658; P(X &geq; a) &leq; E[X]/a — the seed from which the others grow
- **Chebyshev**: P(|X &minus; &mu;| &geq; k&sigma;) &leq; 1/k&sup2; — distribution-free concentration; weak, but enough to *prove* the weak law of large numbers
- **Jensen**: g convex &#8658; g(E[X]) &leq; E[g(X)] (reverse for concave) — gives E[X&sup2;] &geq; (E[X])&sup2;, AM&ndash;GM, log E[X] &geq; E[log X], and the non-negativity of KL divergence
- **Cauchy&ndash;Schwarz**: |E[XY]| &leq; &radic;(E[X&sup2;] E[Y&sup2;]) — yields |Cov(X,Y)| &leq; &sigma;_X &sigma;_Y, hence correlation &isin; [&minus;1, 1]; **Hölder** generalizes it
- Sharper tools — **Chernoff bounds** (optimize over t in Markov applied to e&#8348;&#7587;), **Hoeffding**, **Bernstein** — give *exponential* tail decay for sums and underpie concentration of measure and learning theory

---

## Moments And Bounds In Code

```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(3)
x = rng.standard_t(df=5, size=500_000)             # t_5: has mean & var, kurtosis is large
print("mean~0:", x.mean().round(3), " var~5/3:", x.var(ddof=1).round(3),
      " excess kurtosis~6:", stats.kurtosis(x).round(2))
# Chebyshev is a valid (loose) bound:
for k in (2, 3, 4):
    print(f"P(|X-0| >= {k}*sd) empirical={np.mean(np.abs(x) >= k*x.std()):.4f}  Chebyshev<= {1/k**2:.4f}")
# MGF determines sums: sum of independent Normals is Normal
s = rng.normal(1, 2, (300_000, 3)).sum(axis=1)
print("sum mean~3:", s.mean().round(3), " sum var~12:", s.var(ddof=1).round(3))
```

---

## Common Mistakes

- Assuming E[X] exists — it can be infinite or undefined (Cauchy has no mean; some Paretos have no variance)
- Swapping a limit and an expectation with no MCT/Fatou/DCT hypothesis in force
- Believing the MGF always exists — many standard heavy-tailed laws have none; use the characteristic function
- Reading "Cov(X, Y) = 0" as "X and Y independent" — uncorrelated is strictly weaker
- Thinking the moment sequence pins down the distribution — the lognormal shows it need not (the moment problem)
