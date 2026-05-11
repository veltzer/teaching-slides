---
tags:
  - math:distributions
  - math:probability
level: beginner
category: math
audience:
  - audiences:data-analysts
  - audiences:developers

---
# Common Distributions

---
## What This Chapter Covers

- What a probability distribution is
- Discrete: Bernoulli, binomial, Poisson, geometric
- Continuous: uniform, exponential, normal
- The power-law / long-tail family
- How to recognize which one you're looking at
- Sampling and fitting in Python

---
## Six Distribution Shapes

![six_shapes](svg/courses/math/statistics-applied/07_common_distributions/six_shapes.svg)

---
## What A Distribution Is

- A rule that assigns probability to each possible value of a random variable
- Discrete: a probability *mass* function — P(X = k) for each k
- Continuous: a probability *density* function — area under the curve is probability
- Always sums (or integrates) to 1
- Pick the distribution that matches how your data is *generated*

---
## Bernoulli And Binomial

- **Bernoulli**: one trial, success with probability p — a single coin flip
- **Binomial**: count of successes in n independent Bernoulli trials
- Use for: conversions out of N visitors, defects out of N units
- Mean = np, variance = np(1&minus;p)
- Needs fixed n, constant p, independent trials — check all three

---
## Poisson

- Count of events in a fixed interval, when events happen at a constant average rate independently
- One parameter &lambda; = mean = variance
- Use for: arrivals per minute, typos per page, crashes per day
- If variance &#8811; mean, the data is *overdispersed* — Poisson is the wrong model
- The limit of a binomial with huge n and tiny p

---
## Geometric And Exponential

- **Geometric** (discrete): number of trials until the first success
- **Exponential** (continuous): time until the next event in a Poisson process
- Both are "waiting time" distributions and both are memoryless
- Memoryless: having waited 10 minutes doesn't change the expected remaining wait
- Use exponential for inter-arrival times, time-to-failure of simple components

---
## Uniform

- Every value in [a, b] equally likely (continuous), or each of k outcomes equally likely (discrete)
- Use for: a fair die, a random pick, a "no information" prior
- Rarely a good model for real measured data
- Often the *wrong* default — real "random" data is usually not uniform
- The basis from which other random variates are generated

---
## The Normal Distribution

- The bell curve — symmetric, defined by mean &mu; and SD &sigma;
- Shows up wherever many small independent effects add up (central limit theorem)
- Heights, measurement errors, sums and averages of almost anything
- ~68% within 1&sigma;, ~95% within 2&sigma;, ~99.7% within 3&sigma;
- The default for *averages*, not necessarily for raw data — gets its own chapter

---
## How the Families Relate

![family_relationships](svg/courses/math/statistics-applied/07_common_distributions/family_relationships.svg)

---
## Power Laws And Long Tails

- A few values are enormous; most are tiny — file sizes, city populations, wealth, page views
- Mean and SD are nearly meaningless; the tail dominates everything
- A histogram on a log-log scale looks roughly like a straight line
- Don't apply normal-curve reasoning here — "3 sigma events" happen weekly
- When in doubt with web-scale data, suspect a long tail

---
## Working With Distributions In Python

```python
from scipy import stats
print(stats.binom.pmf(3, n=10, p=0.2))     # P(3 successes in 10)
print(stats.poisson.cdf(2, mu=5))           # P(2 or fewer events)
print(stats.norm.ppf(0.975, 0, 1))          # the 1.96 you keep seeing
sample = stats.expon.rvs(scale=1/0.5, size=1000)   # rate lambda = 0.5
print(stats.expon.fit(sample))              # estimate the parameter back
```

---
## Common Mistakes

- Forcing a normal model onto skewed or long-tailed data
- Using Poisson when variance far exceeds the mean
- Assuming independence (binomial/Poisson both require it)
- Confusing the geometric (count of trials) with the exponential (continuous time)
- Reporting a mean for a power-law variable as if it were typical
