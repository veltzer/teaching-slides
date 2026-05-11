---
tags:
  - math:probability
level: advanced
category: math
audience:
  - audiences:data-scientists
  - audiences:ml-engineers

---
# Laws of Large Numbers and the Central Limit Theorem

---
## What This Chapter Covers

- The weak law and a Chebyshev proof
- The strong law (Kolmogorov)
- The classical CLT and its proof via characteristic functions
- Variants: Lindeberg, Lyapunov, multivariate, triangular arrays
- Berry&ndash;Esseen: how fast the CLT kicks in
- When the LLN/CLT fail, and what replaces them

---
## The Weak Law Of Large Numbers

- Let X&#8321;, X&#8322;, ... be i.i.d. with mean &mu; (and, for the easy proof, finite variance &sigma;&sup2;). Let X&#772;&#8345; = (1/n)&Sigma;X&#8345;
- **WLLN**: X&#772;&#8345; &#8597;&#7510; &mu; — for every &epsilon; &gt; 0, P(|X&#772;&#8345; &minus; &mu;| &gt; &epsilon;) &#8594; 0
- One-line proof: E[X&#772;&#8345;] = &mu;, Var(X&#772;&#8345;) = &sigma;&sup2;/n, so Chebyshev gives P(|X&#772;&#8345; &minus; &mu;| &gt; &epsilon;) &leq; &sigma;&sup2;/(n&epsilon;&sup2;) &#8594; 0
- The finite-variance assumption is only for *this* proof — the WLLN actually holds whenever &mu; is finite (truncation argument)
- Foundational reading: averages stabilize; it's what makes "estimate &mu; by the sample mean" legitimate and what justifies Monte Carlo

---
## The Strong Law Of Large Numbers

- **SLLN (Kolmogorov)**: if X&#8345; are i.i.d. with E|X&#8321;| &lt; &infin;, then X&#772;&#8345; &#8594; &mu; **almost surely** — *every* sample path converges (off a null set)
- Conversely, if E|X&#8321;| = &infin;, the sample mean a.s. *fails* to converge to any finite limit — the integrability hypothesis is exactly sharp (Cauchy is the poster child)
- Strictly stronger than the WLLN: it controls trajectories, not just probabilities at each n
- Proof routes: Kolmogorov's maximal inequality + the three-series theorem (classical), or the slick Etemadi argument (works even with only pairwise independence)
- This is *the* theorem behind "long-run frequencies converge to probabilities" — the frequentist interpretation made rigorous

---
## The Classical Central Limit Theorem

- X&#8345; i.i.d., mean &mu;, **finite variance** &sigma;&sup2; &isin; (0, &infin;). Then **&radic;n (X&#772;&#8345; &minus; &mu;) / &sigma; &#8658; N(0, 1)** (convergence in distribution)
- Equivalently: the centered sum S&#8345; &minus; n&mu; has fluctuations of order &radic;n, and on that scale they're Gaussian regardless of the shape of the X&#8345;
- Proof via characteristic functions: with Y&#8345; = (X&#8345; &minus; &mu;)/&sigma;, &phi;_{(&Sigma;Y&#8345;)/&radic;n}(t) = [&phi;_Y(t/&radic;n)]&#8319;; expand &phi;_Y(s) = 1 &minus; s&sup2;/2 + o(s&sup2;) (using E[Y] = 0, E[Y&sup2;] = 1), so the n-th power &#8594; e&#8315;&#8348;&#178;&#8725;&#178;, the standard-normal characteristic function; Lévy's continuity theorem finishes it
- It's why the normal distribution is *everywhere* — anything that's a sum/average of many small independent contributions is approximately normal
- Caveat: it's a statement about the **average / sum**, not about individual observations, and the rate of approach depends on the distribution (slide on Berry&ndash;Esseen)

---
## CLT Variants

- **Lindeberg CLT**: independent but *not* identically distributed X&#8345;; under the **Lindeberg condition** (no single term dominates the variance in the limit), the standardized sum still &#8658; N(0,1) — the modern, definitive form
- **Lyapunov CLT**: a simpler-to-check sufficient condition — for some &delta; &gt; 0, &Sigma; E|X&#8345; &minus; &mu;&#8345;|^{2+&delta;} / (s&#8345;^{2+&delta;}) &#8594; 0 (s&#8345;&sup2; = total variance); Lyapunov &#8658; Lindeberg
- **Triangular arrays**: the row-wise version (entries may change with n) — the right framework for, e.g., the CLT behind the Poisson approximation, m-dependent sequences, and U-statistics
- **Multivariate CLT**: &radic;n(X&#772;&#8345; &minus; &mu;) &#8658; N(0, &Sigma;) in &#8477;&#8316; — proved by the Cramér&ndash;Wold device (reduce to all 1-D linear combinations)
- Dependent data: there are CLTs under mixing / martingale-difference conditions (the **martingale CLT**), but the *long-run variance* replaces &sigma;&sup2; — naive variance estimates are then wrong (need HAC/Newey&ndash;West-type corrections)

---
## How Fast: Berry&ndash;Esseen

- The CLT is a *limit*; for finite n the normal approximation has error. **Berry&ndash;Esseen**: if &rho; = E|X&#8321; &minus; &mu;|&sup3; &lt; &infin;, then sup_x | F&#8345;(x) &minus; &Phi;(x) | &leq; C &rho; / (&sigma;&sup3; &radic;n), with C an absolute constant (&lt; 0.5)
- Two takeaways: the uniform error decays like **1/&radic;n**, and it's worse for **skewed** distributions (large third moment) — symmetry buys you a faster, O(1/n), approach (Edgeworth)
- This is the theory behind rules of thumb like "n &geq; 30": adequate for mildly skewed data, far too optimistic for heavily skewed or heavy-tailed data
- It bounds the *CDF* uniformly; tail probabilities (the region you care about for p-values) can be relatively *much* worse — large-deviation / saddlepoint corrections do better there
- Practical advice: when n is moderate and the data is skewed, prefer a bootstrap or an exact/permutation method over the normal approximation

---
## When The Classical Results Break

- **Infinite mean** (Cauchy, Pareto &alpha; &leq; 1): the SLLN fails outright — X&#772;&#8345; does not settle down; it's as variable as a single observation
- **Infinite variance** (Pareto 1 &lt; &alpha; &lt; 2): the LLN still holds (mean exists), but the CLT does **not** — properly normalized sums converge to a non-Gaussian **&alpha;-stable** law with heavy tails; the right scaling is n^{1/&alpha;}, not &radic;n. The Normal is precisely the &alpha; = 2 stable distribution
- **Strong dependence** (long memory, unit roots): both can fail or change form — the variance of the sum need not grow like n, and limits can be functionals of Brownian motion rather than Gaussian
- **Sums of maxima** rather than averages: governed by **extreme-value theory** (Fréchet / Gumbel / Weibull limits), an entirely different limit law family
- Diagnostic instinct: if the data plausibly has a power-law tail or persistent autocorrelation, don't reach for &radic;n-CLT inference — check the tail index, model the dependence, or resample with blocks

---
## LLN And CLT In Code

```python
import numpy as np
from scipy import stats
rng = np.random.default_rng(7)
# SLLN holds for Exp(1) (mean 1); fails for Cauchy (no mean)
print("Exp running mean:", (np.cumsum(rng.exponential(1, 100_000)) / np.arange(1, 100_001))[-1].round(3))
print("Cauchy running mean:", (np.cumsum(rng.standard_cauchy(100_000)) / np.arange(1, 100_001))[-1].round(3))
# CLT: standardized means of a skewed (Exp) population -> N(0,1); slower convergence than for symmetric data
for n in (5, 30, 200):
    z = (rng.exponential(1, (100_000, n)).mean(axis=1) - 1) * np.sqrt(n)
    print(f"n={n:>3}  KS-vs-N(0,1) p = {stats.kstest(z, 'norm').pvalue:.3f}  (skew of mean ~ {2/np.sqrt(n):.2f})")
# Berry-Esseen flavor: error ~ C/sqrt(n), worse for skew
```

---
## Common Mistakes

- Applying the CLT to *individual* observations instead of to the sample mean / sum
- Trusting "n &geq; 30" for heavily skewed or heavy-tailed data (Berry&ndash;Esseen says the error scales with the third moment)
- Using the &radic;n-normalized CLT when the variance is infinite — the limit is &alpha;-stable, scaled by n^{1/&alpha;}
- Applying the classical (independent) CLT to autocorrelated data without replacing &sigma;&sup2; by the long-run variance
- Forgetting the SLLN's sharp condition: E|X| = &infin; means the sample mean genuinely does not converge
