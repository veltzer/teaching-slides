---
tags:
  - math:statistics
level: beginner
category: math
audience:
  - audiences:data-analysts
  - audiences:developers

---
# What Statistics Is

---
## What This Chapter Covers

- What statistics actually does for you
- Population vs sample
- Descriptive vs inferential statistics
- Parameters vs statistics
- Why uncertainty is the whole point
- Where statistics shows up in real work

---
## Population vs Sample

![population_vs_sample](svg/courses/math/statistics-applied/01_what_statistics_is/population_vs_sample.svg)

---
## The One-Sentence Definition

- Statistics is the science of learning from data *in the presence of uncertainty*
- You almost never see the whole picture — only a slice
- The job: say something useful about the whole from the slice
- And say *how sure* you are
- Everything else is technique in service of that

---
## Population vs Sample

- **Population**: every unit you care about — all users, all transactions, all widgets ever made
- **Sample**: the subset you actually measured
- You study the sample to learn about the population
- The population is usually unknowable in full
- A good sample *represents* the population; a bad one misleads confidently

---
## Descriptive vs Inferential

- **Descriptive statistics**: summarize the data you have — mean, median, charts
- **Inferential statistics**: draw conclusions about the population from the sample
- Descriptive is "here is what happened"
- Inferential is "here is what is probably true in general"
- This course does both; the second is where the care is needed

---
## Parameters vs Statistics

- A **parameter** describes a population — true mean &mu;, true proportion p
- A **statistic** describes a sample — sample mean x&#772;, sample proportion p&#770;
- Parameters are fixed but unknown; statistics are known but vary by sample
- We use statistics to *estimate* parameters
- Greek letters = population; Latin letters = sample (rough convention)

---
## Why Uncertainty Is The Point

- "Revenue went up 3%" — real change, or noise?
- A different sample would give a slightly different number
- Statistics quantifies *how much* the number could wobble
- Without that, every number is just a vibe
- "The number, plus or minus what" is the actual deliverable

---
## A First Look At Variability

```python
import numpy as np
rng = np.random.default_rng(0)
truth = 100.0
for _ in range(5):
    sample = rng.normal(truth, 15, size=30)
    print(f"sample mean = {sample.mean():.2f}")
```

- The true mean is 100, but each sample mean differs
- This wobble is *sampling variability* — the central concern of inference

---
## Sampling Variability

![sampling_variability](svg/courses/math/statistics-applied/01_what_statistics_is/sampling_variability.svg)

---
## Where You Will Meet Statistics

- A/B tests: did the new button actually help?
- Forecasting: how many servers next quarter?
- Quality control: is this batch within spec?
- Surveys and polls: what does the population think?
- Anywhere a decision rests on incomplete data

---
## Common Mistakes

- Treating the sample as if it were the population
- Reporting a number with no sense of its uncertainty
- Confusing "we measured a difference" with "there is a difference"
- Skipping descriptive statistics and jumping to fancy tests
- Forgetting that a biased sample can't be fixed by more data
