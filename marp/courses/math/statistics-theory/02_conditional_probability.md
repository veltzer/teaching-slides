---
tags:
  - math:probability
level: advanced
category: math
audience:
  - audiences:data-scientists
  - audiences:ml-engineers

---

# Conditional Probability and Independence

---

## What This Chapter Covers

- Conditional probability as a new measure
- The chain rule and the law of total probability
- Bayes' theorem in general form
- Independence of events and of families
- Conditional independence
- A glimpse of conditioning on &sigma;-algebras

---

## Bayes' Theorem

![bayes rule](svg/courses/math/statistics-theory/02_conditional_probability/bayes_rule.svg)

---

## Conditioning Restricts The World

- Given an event B with P(B) &gt; 0, define **P(A | B) = P(A &cap; B) / P(B)**
- This is "the probability of A, in a world where B is known to have happened" — it renormalizes mass to B
- Key fact: for fixed B, the map A &#8614; P(A | B) is *itself* a probability measure on (&Omega;, F) — it satisfies all of Kolmogorov's axioms
- So everything proved for P holds for P(&middot; | B) — complement rule, additivity, monotonicity, the lot
- When P(B) = 0 the elementary definition fails; we'll need conditional expectation (last slide) to handle it

---

## The Chain Rule

- Rearranging the definition: P(A &cap; B) = P(A | B) P(B)
- Iterating gives the **multiplication / chain rule**: P(A&#8321; &cap; ... &cap; A&#8345;) = P(A&#8321;) P(A&#8322; | A&#8321;) P(A&#8323; | A&#8321; &cap; A&#8322;) &middot;&middot;&middot; P(A&#8345; | A&#8321; &cap; ... &cap; A&#8345;&#8331;&#8321;)
- Valid whenever the conditioning events have positive probability
- It's the backbone of sequential models — Markov chains, Bayesian networks, autoregressive models all factor a joint law this way
- The order of the chain is arbitrary; choose whichever ordering makes the conditionals easy

---

## The Law Of Total Probability

- Let {B&#8345;} be a **partition** of &Omega; (disjoint, exhaustive, each with positive probability)
- Then for any event A: **P(A) = &Sigma;&#8345; P(A | B&#8345;) P(B&#8345;)**
- Reading: split the world into cases, find A's probability within each case, average weighted by how likely each case is
- It's how you compute "messy" probabilities by conditioning on a convenient variable (first step, the disease test &#8594; B = sick / healthy)
- The continuous analog replaces the sum by an integral against the conditioning density

---

## Bayes' Theorem, General Form

- Combine the chain rule with total probability: for a partition {B&#8345;},
- **P(B&#8459; | A) = P(A | B&#8459;) P(B&#8459;) / &Sigma;&#8345; P(A | B&#8345;) P(B&#8345;)**
- Vocabulary: P(B&#8459;) prior, P(A | B&#8459;) likelihood, P(B&#8459; | A) posterior, the denominator the normalizing "evidence"
- It *inverts* the conditional — turns "P(data | hypothesis)" into "P(hypothesis | data)" — which is the entire move in Bayesian inference
- The classic trap is ignoring the prior P(B&#8459;): a rare condition + an imperfect test &#8594; a "positive" is still probably a false alarm

---

## Independence Of Events

- Events A and B are **independent** iff P(A &cap; B) = P(A) P(B) — equivalently (when defined) P(A | B) = P(A): B carries no information about A
- It is a *symmetric* relation, and a property of the *measure*, not of set geometry — disjoint events with positive probability are the *opposite* of independent
- Independence is not transitive, and pairwise independence does **not** imply joint independence (the textbook example: three events, every pair independent, yet P(A&cap;B&cap;C) &ne; P(A)P(B)P(C))
- A family {A&#7522;} is **(mutually) independent** iff P(&#8898;&#8345;&isin;S A&#8345;) = &prod;&#8345;&isin;S P(A&#8345;) for *every* finite subset S — the full product condition, not just pairs
- Always check whether independence is a modeling *assumption* or a derived fact — most wrong analyses assume it for free

---

## Conditional Independence

- A and B are **conditionally independent given C** iff P(A &cap; B | C) = P(A | C) P(B | C) — they're independent *inside the world where C is known*
- This neither implies nor is implied by ordinary (marginal) independence — variables can be dependent overall yet independent once you condition (a common cause explains the link), or vice versa
- It is the structural assumption behind **graphical models**: a Bayesian network asserts exactly a list of conditional independencies, which is what makes the joint factorize compactly
- "Explaining away": two independent causes of a common effect become *dependent* once that effect is observed
- Spurious correlations often vanish under the right conditioning — and genuine ones can appear — so the conditioning set matters enormously

---

## Conditioning On A &sigma;-Algebra

- When P(B) = 0 (e.g. conditioning a continuous variable on "X = x"), P(A | B) = P(A&cap;B)/P(B) is the indeterminate 0/0 — the elementary definition simply doesn't apply
- The fix: define **conditional expectation** E[1&#8336; | G] with respect to a *sub-&sigma;-algebra* G — the G-measurable random variable whose integral matches P over every set in G (existence and a.s.-uniqueness from the Radon&ndash;Nikodym theorem)
- "Conditional probability given X = x" is then read off this object as a **regular conditional distribution**, defined for almost every x
- This resolves classical paradoxes (Borel&ndash;Kolmogorov): "condition on a measure-zero event" is ambiguous *unless* you say which &sigma;-algebra you're conditioning on
- We'll develop conditional expectation properly when we have integration in hand; for now, just know the elementary formula is a special case, not the whole story

---

## Bayes In Code

```python
# screening: prevalence 0.5%, sensitivity 99%, specificity 98%
prior = {"sick": 0.005, "healthy": 0.995}
like_pos = {"sick": 0.99, "healthy": 0.02}
evidence = sum(like_pos[h] * prior[h] for h in prior)        # total probability
post_pos = {h: like_pos[h] * prior[h] / evidence for h in prior}
print({h: round(p, 4) for h, p in post_pos.items()})        # P(sick | +) ~ 0.20
# law of total probability check via simulation
import numpy as np; rng = np.random.default_rng(1)
sick = rng.random(2_000_000) < prior["sick"]
pos = np.where(sick, rng.random(sick.size) < like_pos["sick"],
                     rng.random(sick.size) < like_pos["healthy"])
print("P(+) empirical:", pos.mean(), " formula:", evidence)
```

---

## Common Mistakes

- Forgetting the prior in Bayes' theorem (the base-rate fallacy)
- Confusing P(A | B) with P(B | A) — the "prosecutor's fallacy"
- Inferring joint independence from pairwise independence
- Conflating marginal and conditional independence — conditioning can create *or* destroy dependence
- Writing "P(A | X = x)" for a continuous X as though the elementary quotient defined it, ignoring the &sigma;-algebra subtlety
