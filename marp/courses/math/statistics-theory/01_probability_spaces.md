---
tags:
  - math:probability
level: advanced
category: math
audience:
  - audiences:data-scientists
  - audiences:ml-engineers

---
# Probability Spaces and Axioms

---
## What This Chapter Covers

- Why we need a careful foundation at all
- Sample spaces, events, and &sigma;-algebras
- The Kolmogorov axioms
- Probability measures and their basic properties
- Continuity of measure and Borel&ndash;Cantelli
- Why "probability of every subset" fails on the line

---
## Why Be Rigorous

- Naive probability ("favorable over total") collapses on continuous spaces — every single point has probability 0, yet intervals don't
- Paradoxes (Bertrand, Banach&ndash;Tarski-flavored ones) show "obvious" reasoning can contradict itself
- The fix, due to Kolmogorov (1933): build probability as a special case of **measure theory**
- That gives one consistent framework for dice, the real line, function spaces, and stochastic processes alike
- Everything later — random variables, expectation, the CLT — is defined on top of this scaffold

---
## The Probability Triple

![probability triple](svg/courses/math/statistics-theory/01_probability_spaces/probability_triple.svg)

---
## Sample Space And Events

- The **sample space** &Omega; is the set of all possible outcomes &omega; of the experiment
- An **event** is a subset of &Omega; — but, crucially, *not necessarily every* subset
- We single out a collection **F** of "measurable" events that we're allowed to assign probability to
- For a finite or countable &Omega;, F can be the full power set; for &Omega; = &#8477;, it cannot (see the last slide)
- The triple to keep in mind is (&Omega;, F, P) — outcomes, allowed events, the probability of each

---
## &sigma;-Algebras

- A **&sigma;-algebra** F on &Omega; is a collection of subsets that is: (i) contains &Omega;; (ii) closed under complement; (iii) closed under **countable** unions
- Consequences: it also contains &empty; and is closed under countable intersections and set differences
- The closure under *countable* (not just finite) operations is exactly what makes limits — "the event happens infinitely often" — well-defined
- Generated &sigma;-algebra: &sigma;(C) is the smallest &sigma;-algebra containing a given family C of sets
- The **Borel &sigma;-algebra** B(&#8477;) = &sigma;(open intervals): the standard event collection on the real line — big enough for everything you'll meet, small enough to avoid pathologies

---
## The Kolmogorov Axioms

- A **probability measure** P : F &#8594; [0, 1] satisfies:
- **(A1) Non-negativity**: P(A) &geq; 0 for every A &isin; F
- **(A2) Normalization**: P(&Omega;) = 1
- **(A3) Countable additivity**: for pairwise disjoint A&#8321;, A&#8322;, ... in F, P(&#8899; A&#8345;) = &Sigma; P(A&#8345;)
- That's the entire definition — three lines. Everything else about probability is a *theorem*, derived from these

---
## Properties That Follow

- P(&empty;) = 0, and P(A&#7580;) = 1 &minus; P(A) (complement rule)
- **Monotonicity**: A &sube; B &#8658; P(A) &leq; P(B)
- **Finite additivity** is a special case of (A3); and P(A &cup; B) = P(A) + P(B) &minus; P(A &cap; B) (inclusion&ndash;exclusion)
- **Union bound (Boole)**: P(&#8899; A&#8345;) &leq; &Sigma; P(A&#8345;) — crude but endlessly useful
- None of these are assumed; each is proved from (A1)&ndash;(A3)

---
## Continuity Of Measure

- For an increasing sequence A&#8321; &sube; A&#8322; &sube; ... : P(&#8899; A&#8345;) = lim P(A&#8345;) ("continuity from below")
- For a decreasing sequence A&#8321; &supe; A&#8322; &supe; ... : P(&#8898; A&#8345;) = lim P(A&#8345;) ("continuity from above")
- These are equivalent to countable additivity (given finite additivity) — and they're what let us pass to limits inside P(&middot;)
- **Borel&ndash;Cantelli, part 1**: if &Sigma; P(A&#8345;) &lt; &infin;, then P(A&#8345; infinitely often) = 0
- **Borel&ndash;Cantelli, part 2**: if the A&#8345; are independent and &Sigma; P(A&#8345;) = &infin;, then P(A&#8345; infinitely often) = 1 — together, a sharp 0&ndash;1 dichotomy

---
## Borel&ndash;Cantelli Visualized

![borel cantelli](svg/courses/math/statistics-theory/01_probability_spaces/borel_cantelli.svg)

---
## Why Not All Subsets Of &#8477;?

- Suppose a translation-invariant probability (a "uniform distribution") existed on *every* subset of [0, 1)
- Using the axiom of choice, build a **Vitali set** V; its rational translates partition [0, 1) into countably many disjoint congruent copies
- Countable additivity then forces P([0,1)) = &Sigma; P(translate of V) — a countable sum of *equal* numbers, which is either 0 or &infin;, never 1. Contradiction
- Conclusion: such a set V *cannot* be measurable — so we restrict to a &sigma;-algebra (the Borel or Lebesgue sets) where no contradiction arises
- This is the whole reason F is part of the definition, not an afterthought

---
## A Quick Computational Illustration

```python
import numpy as np
rng = np.random.default_rng(0)
# Borel-Cantelli I: P(A_n) = 1/n^2 is summable -> A_n stops happening
N = 200_000
hits = sum(rng.random() < 1.0/n**2 for n in range(1, N))
print("times A_n occurred up to N:", hits)        # finite, small -- as predicted
# union bound sanity check: P(at least one of m rare events) <= sum of probs
p, m = 1e-4, 50
emp = np.mean([(rng.random(m) < p).any() for _ in range(100_000)])
print(f"empirical P(union) = {emp:.5f}  <=  bound {m*p}")
```

---
## Common Mistakes

- Assuming every subset of an uncountable &Omega; can be assigned a probability
- Treating finite additivity as enough — countable additivity is what powers limits and the LLN
- Forgetting that &sigma;-algebras require closure under *countable*, not merely finite, unions
- Using the union bound where you need an exact value (it's only an upper bound)
- Mixing up the two halves of Borel&ndash;Cantelli — the second needs independence
