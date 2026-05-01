---
tags:
  - data-and-ai:statistics
level: beginner
category: data-science
audience:
  - audiences:data-analysts

---
# Statistical Fundamentals

---
## What This Chapter Covers

- Descriptive statistics: mean, median, mode, variance
- Probability basics
- Distributions and sampling
- Hypothesis testing concepts
- Confidence intervals
- Common statistical pitfalls

---
## Why Statistics Matters

- Data is *samples* of a larger reality
- Statistics is the discipline of knowing how *uncertain* your conclusions are
- "The number went up" — was that meaningful or noise?
- Statistical thinking separates analyses from anecdotes
- A little knowledge prevents a lot of embarrassment

---
## Mean

- Sum / count
- Sensitive to outliers — a single CEO salary lifts the company average
- Use when: roughly normal distribution, no extreme values
- Avoid when: skewed data, outliers present

---
## Median

- The middle value when sorted
- Half the data is above, half below
- Robust to outliers
- Use when: skewed data, outliers present
- "Median income" is more honest than "mean income"

---
## Mode

- The most frequent value
- Useful for categorical data
- "What's the most common purchase?"
- Less central in continuous data
- A bimodal distribution has *two* modes

---
## Variance and Standard Deviation

- **Variance**: average squared deviation from the mean
- **Standard deviation**: square root of variance — same units as the data
- Both measure spread
- Standard deviation is more interpretable
- "Mean 50, SD 10" tells you most data is roughly 40-60

---
## Percentiles

- The value below which a given % of data falls
- p50 = median; p25 / p75 = quartiles
- p95 = "the 5% slowest requests"
- Latency reporting almost always uses percentiles, not means
- Use them when extremes matter

---
## Probability Basics

- Probability of an event: 0 (impossible) to 1 (certain)
- P(A and B): both happen
- P(A or B): at least one happens
- Independence: P(A and B) = P(A) * P(B)
- Conditional: P(A | B) = "probability of A given B happened"

---
## Bayes' Theorem, Briefly

- P(A | B) = P(B | A) * P(A) / P(B)
- Updates beliefs based on evidence
- "Given a positive test result, what's the chance I'm sick?" — depends on base rate
- Most people misuse this: ignoring the base rate gives wildly wrong answers
- Worth understanding even if you never compute it manually

---
## Distributions

- **Normal**: bell curve; many natural phenomena
- **Binomial**: count of successes in N trials
- **Poisson**: count of events per interval
- **Exponential**: time between events
- **Power law**: long-tail (file sizes, city populations)
- Match the right distribution to your data before testing

---
## The Central Limit Theorem

- The mean of *many* samples tends toward a normal distribution, even if the underlying data isn't normal
- Why? It's the basis for most "we can use normal-curve maths" assumptions
- Sample size matters: 30+ is the rough rule
- Without CLT, statistics on weird distributions would be nightmare-hard
- One of the most important results in statistics

---
## Sampling

- Take a subset to estimate a property of the whole
- Random sampling: every member equally likely
- Stratified: sample within groups proportionally
- Cluster: sample whole groups
- Convenience sampling (whoever's easy): biased, common, often unfit for purpose

---
## Sample Size

- Bigger samples &#8594; smaller error bars
- Diminishing returns: 4x the sample halves the error
- Power analysis tells you the size you need to detect a given effect
- Underpowered tests waste time and produce false negatives
- Overpowered tests are wasteful but conservative

---
## Hypothesis Testing

- **Null hypothesis (H0)**: no effect / no difference
- **Alternative (H1)**: there is an effect
- Compute a test statistic, get a p-value
- p-value: "probability of seeing this data if H0 were true"
- Small p &#8594; reject H0; large p &#8594; can't distinguish from noise

---
## P-Values, Carefully

- p < 0.05 is the conventional threshold; not magic
- "Statistically significant" &#8800; "important"
- A tiny effect with huge sample size can be "significant" but useless
- Always report effect size, not just p
- p-hacking (testing many things, reporting only the significant) is misuse

---
## Confidence Intervals

- A range likely to contain the true value
- 95% CI: "if we repeated this many times, 95% of intervals would contain the true value"
- Wider interval = less certainty
- More informative than a single estimate
- Always quote with the estimate

---
## A/B Testing

- Random assignment to A or B
- Compare a chosen metric
- Statistically test for a difference
- Run long enough to get sufficient sample size
- Beware: peeking, multiple comparisons, novelty effects, regression to mean

---
## Common Statistical Pitfalls

- Confusing correlation with causation
- p-hacking: testing 20 things, reporting the one significant one
- Simpson's paradox: pattern reverses when data is grouped
- Survivorship bias: only looking at the survivors
- Goodhart's law: "when a measure becomes a target, it ceases to be a good measure"

---
## Common Mistakes

- Quoting means for skewed data
- Treating "p < 0.05" as proof
- Ignoring the base rate
- Sampling poorly, then trusting the conclusions
- Using statistical jargon without understanding it
