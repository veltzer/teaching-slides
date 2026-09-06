---
tags:
  - math:hypothesis-testing
level: beginner
category: math
audience:
  - audiences:data-analysts
  - audiences:developers

---

# A/B Testing in Practice

---

## What This Chapter Covers

- What an A/B test is and why randomization matters
- Choosing a metric and a minimum detectable effect
- Sample size and how long to run
- The peeking problem
- Multiple variants and multiple metrics
- Threats: novelty, seasonality, regression to the mean

---

## An A/B Test, End to End

![ab_flow](svg/courses/math/statistics-applied/14_ab_testing/ab_flow.svg)

---

## What An A/B Test Is

- Randomly split users into A (control) and B (variant), ship the change to B, compare a metric
- **Randomization** is the whole trick — it makes the groups comparable on *everything*, known and unknown
- That's what turns a correlation ("B users converted more") into a causal claim ("B *caused* more conversions")
- It's a designed experiment, not an observational analysis — far stronger
- Everything else in this chapter is about not blowing that advantage

---

## Pick The Metric First

- Decide the **primary metric** before launching — conversion rate, revenue per user, retention
- One primary metric; a small set of guardrail metrics; everything else is exploratory
- Choosing the metric *after* seeing results is how you fool yourself
- Prefer a metric tied to real value, not a vanity proxy (Goodhart's law applies)
- Define exactly how it's computed, including edge cases, *in writing*

---

## Minimum Detectable Effect And Sample Size

- The **minimum detectable effect (MDE)** is the smallest lift worth caring about — set it from business value, not hope
- Sample size grows roughly with 1 / MDE&sup2; — detecting a 1% lift needs ~4&times; the users of a 2% lift
- A power calculation turns (baseline rate, MDE, &alpha;, power) into "n users per arm"
- Run the calculation *before* launch; an underpowered test is wasted traffic
- If you can't get the sample size, test a bigger change instead

---

## How Long To Run

- Run for whole numbers of weeks to average over day-of-week effects
- Hit the pre-computed sample size *and* a full business cycle — whichever is longer
- Don't stop early because it "looks good"; don't run forever hunting for significance
- Account for weekly and seasonal patterns — a Black Friday week is not a typical week
- Decide the stopping rule before you start, then follow it

---

## The Peeking Problem

- Checking the p-value repeatedly and stopping the moment it dips below 0.05 inflates the false-positive rate badly — easily to 20%+
- Each peek is another chance for noise to cross the line
- Fixes: a fixed sample size you commit to, or proper **sequential testing** (alpha-spending, group-sequential designs) built for early looks
- "We saw significance on day 2" with a fixed-n design means almost nothing
- Build the dashboard so it *doesn't* tempt you to peek

---

## Peeking Inflates the False-Positive Rate

![peeking_alpha_inflation](svg/courses/math/statistics-applied/14_ab_testing/peeking_alpha_inflation.svg)

---

## Many Variants, Many Metrics

- Testing A vs B vs C vs D? More comparisons &#8594; more chances for a fluke "winner"
- Testing 10 metrics? At &alpha; = 0.05 you expect ~1 spurious "significant" result by chance
- Correct for it (Bonferroni, Holm, or false-discovery-rate control) or pre-register one comparison
- Reporting only the metric/variant that "won" is p-hacking with extra steps
- Fewer, sharper tests beat a buffet of underpowered ones

---

## Threats To Validity

- **Novelty effect**: users click the new thing because it's new; the lift fades — run long enough to see past it
- **Seasonality**: the test window isn't representative of normal conditions
- **Regression to the mean**: a metric picked because it was extreme will drift back regardless of the change
- **Sample ratio mismatch**: the 50/50 split isn't 50/50 — your randomization or logging is broken; stop and fix it
- **Interference**: A and B users affect each other (social features, shared inventory) — naive A/B breaks down

---

## A Power And Test Calculation In Python

```python
import numpy as np
from statsmodels.stats.proportion import proportions_ztest
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize
es = proportion_effectsize(0.10, 0.11)               # baseline 10%, MDE = +1pt
n = NormalIndPower().solve_power(es, alpha=0.05, power=0.8, alternative="two-sided")
print(f"users per arm: {int(np.ceil(n))}")
# after the test: 1000/10000 control vs 1120/10000 variant
z, p = proportions_ztest([1000, 1120], [10000, 10000])
print(f"z = {z:.2f}, p = {p:.3f}")
```

---

## Common Mistakes

- Peeking and stopping the instant p &lt; 0.05
- Picking the metric (or the winning variant) after seeing the data
- Running an underpowered test, then trusting "not significant"
- Ignoring day-of-week and seasonal effects
- Shrugging off a sample ratio mismatch instead of treating it as a bug
