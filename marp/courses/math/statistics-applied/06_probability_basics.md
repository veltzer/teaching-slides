---
tags:
  - math:probability
level: beginner
category: math
audience:
  - audiences:data-analysts
  - audiences:developers

---

# Probability Basics

---

## What This Chapter Covers

- What a probability is
- Events, sample spaces, and the basic rules
- Independence and conditional probability
- The multiplication and addition rules
- Bayes' theorem and base rates
- Where intuition goes wrong

---

## Events, Unions, Intersections

![events_venn](svg/courses/math/statistics-applied/06_probability_basics/events_venn.svg)

---

## What A Probability Is

- A number from 0 (impossible) to 1 (certain) attached to an event
- Frequentist reading: the long-run fraction of times it happens
- Bayesian reading: a degree of belief, updatable by evidence
- Both give the same arithmetic — the rules below
- Probabilities of all distinct outcomes sum to 1

---

## Events And Sample Spaces

- **Sample space**: every possible outcome — {heads, tails} for a coin
- **Event**: a subset of the sample space — "an even number" on a die is {2, 4, 6}
- P(event) = (favorable outcomes) / (all outcomes), *if* outcomes are equally likely
- Complement rule: P(not A) = 1 &minus; P(A)
- Often the complement is far easier to compute — "at least one" problems especially

---

## Combining Events

- **Addition rule**: P(A or B) = P(A) + P(B) &minus; P(A and B)
- Subtract the overlap or you double-count it
- If A and B can't both happen (mutually exclusive), P(A and B) = 0
- **Multiplication rule**: P(A and B) = P(A) &times; P(B | A)
- These two rules, plus the complement, handle most everyday problems

---

## Independence

- A and B are **independent** if knowing one tells you nothing about the other
- Then P(A and B) = P(A) &times; P(B) — the simple product
- Two coin flips: independent. Drawing two cards without replacement: not
- Independence is an *assumption* you should justify, not assume by default
- Many wrong analyses come from pretending dependent events are independent

---

## Conditional Probability

- P(A | B) = P(A and B) / P(B) — "probability of A given B happened"
- It rescales the world to "the cases where B is true"
- P(A | B) is generally *not* equal to P(B | A) — confusing them is the "prosecutor's fallacy"
- "P(positive test | sick)" and "P(sick | positive test)" are very different numbers
- Conditioning is how evidence enters a probability calculation

---

## Bayes' Theorem

- P(A | B) = P(B | A) &times; P(A) / P(B)
- Flips a conditional you know into the one you want
- P(A) is the **base rate** (prior); P(A | B) is the updated belief (posterior)
- The classic trap: a rare disease, a good-but-imperfect test, and a "positive" result is *still* probably a false alarm
- Always start from the base rate, then update

---

## Bayes and the Base Rate

![bayes_base_rate](svg/courses/math/statistics-applied/06_probability_basics/bayes_base_rate.svg)

---

## A Worked Bayes Example

```python
prevalence   = 0.01     # 1% of people are sick
sensitivity  = 0.99     # P(test+ | sick)
specificity  = 0.95     # P(test- | healthy)
p_pos = sensitivity*prevalence + (1-specificity)*(1-prevalence)
p_sick_given_pos = sensitivity*prevalence / p_pos
print(f"P(sick | positive) = {p_sick_given_pos:.2%}")  # ~16.7%
```

- A "positive" still leaves >80% chance you're fine — base rate dominates

---

## Where Intuition Fails

- Ignoring the base rate (the example above)
- Believing "due for a win" — independent trials have no memory (gambler's fallacy)
- Confusing P(A | B) with P(B | A)
- Underestimating "at least one" probabilities (birthday paradox)
- Treating correlated events as independent and multiplying anyway

---

## Common Mistakes

- Adding probabilities without subtracting the overlap
- Multiplying probabilities of events that aren't independent
- Quoting P(evidence | hypothesis) as if it were P(hypothesis | evidence)
- Forgetting the base rate in screening / detection problems
- Assuming "random" means "uniform" when it often doesn't
