---
tags:
  - math:inferential-statistics
level: intermediate
category: math
audience:
  - audiences:data-analysts
  - audiences:data-scientists

---
# Experimental Design

---
## What This Chapter Covers

- Why design beats analysis
- Randomization, replication, and control
- Blocking and stratification
- Factorial designs and why they're efficient
- Confounding, nuisance variables, and how to neutralize them
- Power analysis and choosing the sample size up front

---
## Fisher's Three Pillars

![three_pillars](svg/courses/math/statistics-inference/13_experimental_design/three_pillars.svg)

---
## You Can't Fix A Bad Design Afterward

- "We'll figure out the statistics later" is how studies die — no analysis rescues a confounded or underpowered experiment
- The design decides which questions your data can *answer* and how precisely
- Three pillars (Fisher's): **randomization**, **replication**, **local control (blocking)**
- Spend your cleverness before data collection, not after
- A clean design with a simple test beats a messy one with a fancy test, every time

---
## Randomization

- Randomly assign units to treatments — the single most important step
- It makes the groups comparable on *every* variable, measured or not, known or not — that's what licenses a causal claim
- It also justifies the probability model behind the test (permutation/randomization inference falls right out)
- "Randomize" means a real random mechanism, not "alternate" or "whoever showed up first" — those carry hidden patterns
- Without randomization you have an *observational* study; causal claims then need much heavier machinery

---
## Replication And Control

- **Replication**: multiple independent units per treatment — gives you an estimate of noise, hence standard errors and power. (Measuring the *same* unit repeatedly is *pseudo-replication* — it doesn't count.)
- **Control group**: a baseline (placebo, current system, do-nothing) measured under the same conditions — without it you can't separate the treatment effect from time trends, learning, or regression to the mean
- The control must differ from the treatment *only* in the factor of interest — same everything else
- More replicates &#8594; tighter estimates &#8594; ability to detect smaller effects
- "Before vs after, no control" is one of the most common — and most misleading — designs

---
## Blocking And Stratification

- A **nuisance variable** affects the outcome but isn't of interest — day of week, machine, lab, batch, site
- **Blocking**: group units into homogeneous blocks (same day, same machine), then randomize treatments *within* each block — "block what you can, randomize what you can't"
- This removes the block-to-block variation from the error term &#8594; a more sensitive test (a **randomized complete block design**)
- The matched-pairs / paired t-test design is the simplest case: block size 2
- Stratification in surveys plays the same role — ensure coverage, reduce variance

---
## Factorial Designs

- Vary several factors **simultaneously**, crossing all their levels — 2 factors &times; 2 levels = 4 treatment combinations
- Far more efficient than one-factor-at-a-time: every observation contributes to every main effect, *and* you get the interactions for free
- Interactions are often the interesting part ("the new layout helps on mobile but not desktop") and OFAT designs can't see them at all
- For many factors, **fractional factorial** designs run a cleverly chosen subset — screen lots of factors cheaply, accepting some aliasing
- This is the backbone of industrial experimentation (DOE) and well-run A/B/n testing

---
## Confounding And How To Neutralize It

- A **confounder** is associated with both the treatment assignment and the outcome — it makes the treatment effect inseparable from its effect
- Neutralize it by *design*: **randomize** (handles all confounders, even unknown ones), **block/stratify** on it, **match** treated and control units on it, or **hold it constant**
- Or adjust by *analysis* — include it as a covariate (ANCOVA, regression) — but this only handles confounders you *measured and modeled correctly*
- Design-based control is strictly better: it doesn't depend on getting the model right or measuring everything
- Before running anything, list the plausible confounders and write down how each is handled

---
## Power Analysis — Plan The Sample Size

- Decide *before* collecting data how many units you need, from four quantities: the **effect size** worth detecting, the **significance level** &alpha; (usually 0.05), the desired **power** 1&minus;&beta; (usually 0.80 or 0.90), and the data's variability
- Required n grows roughly with 1/(effect size)&sup2; — detecting half the effect needs ~4&times; the units
- Run the calculation with software (`statsmodels.stats.power`, or G*Power); for complex designs, **simulate** the experiment and count rejections
- Underpowered &#8594; you'll likely miss a real effect and waste the whole study; wildly overpowered &#8594; you'll "detect" trivialities — both are design failures
- Pre-register the design, the primary outcome, the sample size, and the analysis — it's the cheapest insurance against fooling yourself

---
## Sample Size vs Detectable Effect

![power_curve](svg/courses/math/statistics-inference/13_experimental_design/power_curve.svg)

---
## Design And Power In Python

```python
import numpy as np
from statsmodels.stats.power import TTestIndPower
# how many per group to detect Cohen's d = 0.4 at alpha=0.05, power=0.8?
n = TTestIndPower().solve_power(effect_size=0.4, alpha=0.05, power=0.8,
                                alternative="two-sided")
print(f"n per group = {int(np.ceil(n))}")

# randomized complete block design: 4 blocks (days), 3 treatments, randomized within block
rng = np.random.default_rng(11)
for day in range(4):
    order = rng.permutation(["A", "B", "C"])
    print(f"day {day}: {list(order)}")
```

---
## Common Mistakes

- "We'll sort out the analysis later" — the design already limited what you can conclude
- A before/after study with no control group, then crediting the treatment for a time trend or regression to the mean
- Pseudo-replication: many measurements of one unit treated as many independent units
- "Randomly" assigning by alternating or by convenience — that's not randomization
- Skipping the power calculation and discovering, too late, that the study could never have detected the effect
