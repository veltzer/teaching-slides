---
tags:
  - data-and-ai:machine-learning
level: intermediate
category: machine-learning
audience:
  - audiences:data-scientists

---
# Data Science

---
## What This Chapter Covers

- What is data science
- Roles and pipeline
- Languages and tools
- Statistics primer
- Visualisation
- Data quality and bias

---
## What Data Science Is

- Extracting insight from data
- Mix of: stats, programming, domain knowledge
- Outcome: decisions, predictions, products

---
## Why Now

- Storage is cheap
- Compute is cheap
- Data is everywhere
- Open-source toolchain matured

---
## Data Science vs ML vs Stats

- Stats: estimation, inference, uncertainty
- ML: prediction, generalisation
- DS: the umbrella that uses both
- Overlap is large

---
## Data Science Roles

- Data analyst: descriptive, dashboards
- Data scientist: predictive, modelling
- ML engineer: production, deployment
- Data engineer: pipelines, infrastructure

---
## Who Does What

- Analyst: SQL, BI tools
- Scientist: notebooks, models
- ML eng: serving, monitoring
- Data eng: ETL, warehouses

---
## The Pipeline

- Acquire
- Clean
- Explore
- Model
- Communicate

---
## Pipeline at a Glance

![ml_pipeline](svg/courses/machine_learning/machine-learning/01_data_science/ml_pipeline.svg)

---
## Acquire

- Databases, APIs, files
- Logs and events
- Sensors and IoT
- Third-party providers

---
## Clean

- Missing values
- Duplicates
- Wrong types
- Outliers
- Often 70% of the work

---
## Explore

- Distributions
- Relationships
- Anomalies
- Hypotheses to test

---
## Model

- Pick algorithm
- Train, validate, tune
- Compare candidates

---
## Communicate

- Stakeholders matter
- Plots beat tables
- Quantify uncertainty
- Recommend an action

---
## Tools

- Python: pandas, scikit-learn, matplotlib
- R: tidyverse, ggplot
- SQL: ubiquitous
- Notebooks: Jupyter, Colab

---
## Why Python

- Huge ecosystem
- Glue language
- Production-friendly
- Community

---
## Statistics Primer

- Mean, median, mode
- Variance, standard deviation
- Distributions: normal, binomial, Poisson
- Hypothesis testing, p-values

---
## Mean vs Median

- Mean: sum/n, sensitive to outliers
- Median: middle, robust
- Pick by data shape
- Skewed data: prefer median

---
## Variance and Std

- Variance: average squared deviation
- Std: same units as data
- Spread metric
- Heavy-tailed needs care

---
## The Normal Distribution

- Bell curve
- Mean and std define it
- Many natural phenomena approximate it
- Central Limit Theorem behind it

---
## Other Distributions

- Binomial: yes/no trials
- Poisson: counts in interval
- Exponential: time between events
- Power-law: web, social

---
## Hypothesis Testing

- Null and alternative
- Test statistic
- p-value: probability under null
- Reject when p < threshold

---
## p-Values Are Tricky

- Not "probability hypothesis is true"
- Sensitive to sample size
- Multiple testing inflates them
- Effect size matters more

---
## Confidence Intervals

- Range plausible for the parameter
- Wider when data noisy
- Often more useful than p-values
- Communicate uncertainty

---
## Correlation vs Causation

- Correlation: variables move together
- Causation: one causes the other
- Common pitfall: confusing the two
- Causal inference is hard

---
## Compared

![correlation_causation](svg/courses/machine_learning/machine-learning/01_data_science/correlation_causation.svg)

---
## Probability Basics

- Conditional: P(A|B)
- Bayes' theorem
- Independence
- Foundation of ML

---
## Bayes' Theorem

- P(A|B) = P(B|A) P(A) / P(B)
- Update beliefs with evidence
- Powers Naive Bayes
- Behind probabilistic ML

---
## Visualisation

- Histogram: distribution
- Scatter: relationship
- Box plot: spread, outliers
- Line: time series

---
## More Plot Types

- Bar: categorical comparison
- Heatmap: matrix data
- Violin: distribution shape
- Pair plot: many variables at once

---
## Plotting Pitfalls

- Truncated y-axis
- 3D where 2D works
- Pie charts beyond 3 slices
- Colour for ordered data

---
## Exploratory Data Analysis

- Look before modelling
- Summary stats
- Plot every variable
- Check assumptions

---
## EDA Checklist

- Shape and column types
- Missing per column
- Range and distribution
- Pairwise correlations

---
## Data Quality

- Accuracy: are values right
- Completeness: missing rate
- Consistency: same units, conventions
- Timeliness: how stale

---
## Bias Sources

- Selection bias: who is in the sample
- Survivorship bias: only winners visible
- Measurement bias: tools that distort
- Confirmation bias: looking for the answer

---
## Outliers

- Real or error
- Robust stats: median, IQR
- Visualise to decide
- Removing changes conclusions

---
## Sampling

- Random samples generalise
- Stratified for balance
- Cluster for cost
- Bad sampling beats any model

---
## Communicating Results

- Audience matters
- Show uncertainty
- Tell a story
- Visualisation > tables

---
## Reproducibility

- Pin versions
- Seed random number generators
- Track data versions
- Notebooks plus scripts

---
## Common Data Science Mistakes

- Skipping EDA; modelling blindly
- p-hacking; testing many hypotheses without correction
- Ignoring base rates and class imbalance
- Reporting accuracy on imbalanced data
- Not communicating uncertainty

---
## Summary

- Data science combines stats, code, domain
- Pipeline: acquire, clean, explore, model, communicate
- Cleaning is most of the work
- Quality and bias decide the outcome
