---
tags:
  - math:probability
level: advanced
category: math
audience:
  - audiences:data-scientists
  - audiences:ml-engineers

---
# Modes of Convergence

---
## What This Chapter Covers

- Four notions: a.s., in probability, in L^p, in distribution
- The implication lattice between them
- Counterexamples that separate the modes
- Uniform integrability and when L^p follows
- Continuous mapping and Slutsky's theorem
- The delta method

---
## Why "Converges" Needs Qualifying

- For sequences of *random variables* X&#8345;, "X&#8345; &#8594; X" can mean several genuinely different things
- They differ in *what* is being controlled — a set of bad outcomes, a probability, an average error, or just the distribution
- Choosing the wrong mode is a classic source of false "theorems" — e.g. assuming a limit of expectations equals the expectation of the limit
- The whole asymptotic theory of statistics (consistency, asymptotic normality, the bootstrap) is phrased in these terms
- Master the lattice of implications and the toolbox (CMT, Slutsky, delta method) and most asymptotic arguments become routine

---
## Almost Sure Convergence

- **X&#8345; &#8594; X a.s.** iff P( {&omega; : X&#8345;(&omega;) &#8594; X(&omega;)} ) = 1 — for almost every outcome, the *numerical sequence* converges
- The strongest of the "to a limit r.v." modes; it's pointwise convergence off a null set
- Equivalent (via Borel&ndash;Cantelli) to: for every &epsilon; &gt; 0, P(|X&#8345; &minus; X| &gt; &epsilon; infinitely often) = 0
- This is the conclusion of the **Strong** Law of Large Numbers and of martingale convergence
- It does **not** by itself control E[X&#8345;] — for that you need an integrability hypothesis (next slide)

---
## Convergence In Probability And In L^p

- **In probability**, X&#8345; &#8597;&#7510; X: for every &epsilon; &gt; 0, P(|X&#8345; &minus; X| &gt; &epsilon;) &#8594; 0 — the *probability* of a non-trivial gap vanishes (a single sequence can be far off, just rarely)
- **In L^p** (p &geq; 1), X&#8345; &#8594;_{L^p} X: E[|X&#8345; &minus; X|^p] &#8594; 0 — the p-th-moment error vanishes; p = 2 is mean-square convergence, p = 1 controls expectations directly
- Higher p is stronger: L^q &#8658; L^p for q &gt; p (Jensen / Lyapunov); L^1 convergence gives E[X&#8345;] &#8594; E[X]
- These are the modes that appear in **consistency** statements (estimator &#8594;&#7510; parameter) and in mean-square prediction theory
- Both are *weaker* than a.s. convergence — they say nothing about the trajectory of any individual &omega;

---
## Convergence In Distribution

- **X&#8345; &#8658; X** (in law / weakly) iff F&#8345;(x) &#8594; F(x) at every continuity point x of F; equivalently E[g(X&#8345;)] &#8594; E[g(X)] for all bounded continuous g; equivalently &phi;&#8345;(t) &#8594; &phi;(t) pointwise (Lévy)
- The weakest mode — and the only one where X&#8345; and X needn't even live on the same probability space; only the *distributions* matter
- It's exactly the convergence in the **Central Limit Theorem**: &radic;n(X&#772;&#8345; &minus; &mu;)/&sigma; &#8658; N(0, 1)
- Special case: if X&#8345; &#8658; c (a constant), that's equivalent to X&#8345; &#8597;&#7510; c — the only time "in distribution" upgrades for free
- The right tool for *approximate* statements ("the test statistic is approximately &chi;&sup2;"), confidence intervals, and p-values in large samples

---
## The Implication Lattice

- **a.s. &#8658; in probability &#8658; in distribution** — and **L^p &#8658; in probability &#8658; in distribution**
- None of the reverse arrows hold in general; a.s. and L^p are *not* comparable (neither implies the other)
- Bridges back up: in probability + **uniform integrability** of {|X&#8345;|^p} &#8658; convergence in L^p; in distribution to a *constant* &#8658; in probability
- Skorokhod representation: if X&#8345; &#8658; X, there exist copies X&#8345;' =&#x1D48;= X&#8345;, X' =&#x1D48;= X on a common space with X&#8345;' &#8594; X' a.s. — a frequent technical convenience
- From any mode you can extract an a.s.-convergent subsequence — useful when you only need *some* subsequence

---
## Counterexamples That Pin Down The Differences

- **In probability but not a.s.** — the "typewriter" sequence: indicators of intervals [j/2&#7466;, (j+1)/2&#7466;] sweeping [0,1]; P(X&#8345; = 1) = 1/2&#7466; &#8594; 0, yet every &omega; has X&#8345;(&omega;) = 1 infinitely often
- **a.s. but not in L^1** — X&#8345; = n on a set of probability 1/n, 0 elsewhere: X&#8345; &#8594; 0 a.s. (and in probability) but E[X&#8345;] = 1 &#8642; 0 (mass escapes to infinity)
- **In L^1 but not a.s.** — the typewriter sequence again works, with appropriate scaling
- **In distribution but not in probability** — X&#8345; ~ N(0,1) i.i.d. all converge in law to N(0,1), but |X&#8345; &minus; X_{n+1}| does not shrink
- Moral: the modes are genuinely distinct; an argument valid for one need not transfer

---
## The Working Toolbox

- **Continuous Mapping Theorem**: if X&#8345; &#8594; X (a.s. / in prob / in dist) and g is continuous (more generally, continuous on a set of probability 1 under X), then g(X&#8345;) &#8594; g(X) *in the same mode*
- **Slutsky's theorem**: if X&#8345; &#8658; X and Y&#8345; &#8597;&#7510; c (a constant), then X&#8345; + Y&#8345; &#8658; X + c, X&#8345;Y&#8345; &#8658; cX, and X&#8345;/Y&#8345; &#8658; X/c (c &ne; 0) — this is what lets you replace an unknown &sigma; by a consistent estimate s in &radic;n(X&#772;&minus;&mu;)/s and still get N(0,1)
- **Delta method**: if &radic;n(&theta;&#770;&#8345; &minus; &theta;) &#8658; N(0, &sigma;&sup2;) and g is differentiable at &theta; with g'(&theta;) &ne; 0, then &radic;n(g(&theta;&#770;&#8345;) &minus; g(&theta;)) &#8658; N(0, g'(&theta;)&sup2;&sigma;&sup2;) — propagate asymptotic normality through a smooth transform (multivariate version uses the gradient: variance &nabla;g&#7488;&Sigma;&nabla;g)
- Second-order delta method when g'(&theta;) = 0: scale by n and get a &chi;&sup2;-type limit instead
- These three, plus the CLT and the LLN, are the entire engine of classical large-sample inference

---
## Convergence In Code

```python
import numpy as np
rng = np.random.default_rng(6)
# a.s. (SLLN): running mean of iid -> mu, every path
m = np.cumsum(rng.normal(3, 5, 50_000)) / np.arange(1, 50_001)
print("running mean tail:", m[-1].round(3))                      # ~ 3
# in distribution (CLT): standardized sums of Exp(1) -> N(0,1)
n = 40
z = (rng.exponential(1.0, (200_000, n)).mean(axis=1) - 1.0) / (1.0/np.sqrt(n))
from scipy import stats
print("CLT KS-vs-N(0,1) p:", stats.kstest(z, "norm").pvalue.round(3))
# delta method: sqrt(n)(g(Xbar)-g(mu)) ~ N(0, g'(mu)^2 sigma^2), g = exp
xbar = rng.normal(2.0, 1.0, 200_000) / 1.0
emp_var = np.var(np.exp(xbar) - np.exp(2.0))
print("delta-method var ~ exp(2)^2 * 1^2 =", round(np.exp(2.0)**2, 2), " empirical:", round(emp_var, 2))
```

---
## Common Mistakes

- Concluding E[X&#8345;] &#8594; E[X] from a.s. (or in-probability) convergence without uniform integrability / a dominating function
- Treating convergence in distribution as if it controlled the random variables (it only constrains their laws)
- Applying Slutsky when the second sequence converges to a non-degenerate random variable, not a constant
- Using the delta method at a point where g'(&theta;) = 0 (the first-order limit is degenerate — use the second-order version)
- Assuming the reverse implications hold — in particular that "in distribution" upgrades to "in probability" for a non-constant limit
