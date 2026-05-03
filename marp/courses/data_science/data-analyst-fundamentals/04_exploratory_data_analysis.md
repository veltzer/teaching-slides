---
tags:
  - data-and-ai:eda
  - data-and-ai:pandas
level: beginner
category: data-science
audience:
  - audiences:data-analysts

---
# Exploratory Data Analysis

---
## What This Chapter Covers

- What EDA is and why it matters
- Summary statistics
- Univariate and bivariate analysis
- Correlation analysis
- Pattern recognition
- Using Python and pandas for EDA
- Documenting findings

---
## What EDA Is

- *Looking around* before deciding what to do
- Coined by John Tukey (1977)
- Skip it &#8594; you'll model the wrong thing or miss the obvious
- Quick visual + summary stats; no formal hypotheses yet
- Most insights come from EDA, not from formal modelling

---
## Steps

![eda_steps](svg/courses/data_science/data-analyst-fundamentals/04_exploratory_data_analysis/eda_steps.svg)

---
## Why EDA First

- The data is rarely what you expected
- Distributions, scales, missingness all matter for next steps
- Patterns surface that nobody mentioned
- Bugs surface before they reach reports
- Time spent here saves multiples later

---
## Summary Statistics

```python
df.describe()                     # numeric summary
df.describe(include='object')     # categorical summary
df['country'].value_counts()      # category counts
df['amount'].quantile([0.1, 0.5, 0.9])
```

- `describe()` is the first command in every EDA session
- Mean and median together hint at skew
- Min and max often reveal data errors

---
## Distribution Shapes

- **Normal / bell**: classic, mean = median
- **Right-skewed**: long tail to the right (income, file sizes)
- **Left-skewed**: long tail to the left (rare in business data)
- **Bimodal**: two peaks (often two populations mixed)
- **Uniform**: equal across the range (rare; often suspicious)

---
## Histograms

```python
df['age'].hist(bins=30)
```

- The most-useful first plot
- Bin count matters: too few hides detail, too many is noise
- Try a few; pick the one that shows the structure
- For wide ranges: log-scale on the y-axis

---
## Box Plots

```python
df.boxplot(column='salary', by='department')
```

- Show median, quartiles, and outliers in one glance
- Great for comparing groups
- Adjacent box plots reveal differences fast
- Add the data points (`stripplot` in Seaborn) for small samples

---
## Categorical Counts

```python
df['country'].value_counts(normalize=True).head(10)
sns.countplot(data=df, x='status', order=df['status'].value_counts().index)
```

- Top-N is usually enough
- Long tails: bucket the rest into "Other"
- Sort by frequency for readability

---
## Bivariate Analysis

- Two variables at a time
- Numeric + numeric: scatter plot
- Numeric + categorical: box plot, violin
- Categorical + categorical: cross-tab, heatmap
- Look for: relationships, clusters, gaps

---
## Scatter Plots

```python
df.plot.scatter(x='age', y='spend', alpha=0.5)
```

- Best for two numeric variables
- Add transparency (`alpha`) to reveal density
- Add a regression line (`sns.regplot`) for trend
- Watch for: nonlinear shapes, clusters, outliers

---
## Correlation

```python
df.corr()                   # all pairs
df['x'].corr(df['y'])       # one pair
sns.heatmap(df.corr(), annot=True)
```

- Pearson correlation: linear relationship, [-1, 1]
- Spearman: rank-based, robust to outliers
- High correlation &#8800; causation
- Heatmap: spot pairs that move together

---
## Cross-Tabulation

```python
pd.crosstab(df['country'], df['plan_type'], normalize='index')
```

- Rows = one category, columns = another, cells = counts or percentages
- `normalize='index'`: each row sums to 1 — proportion within group
- Reveals "more X among Y" patterns
- Pair with a heatmap for visualisation

---
## Pattern Recognition

- Time trends: line plots over a date column
- Seasonality: weekly, monthly, yearly cycles
- Cohort patterns: behaviour by signup date
- Regime shifts: sudden changes in behaviour
- Train your eye on real data; intuition improves with reps

---
## Pandas Idioms

```python
# group + aggregate
df.groupby('country')['spend'].agg(['count', 'mean', 'sum'])

# pivot
df.pivot_table(index='country', columns='month', values='spend')

# top N within group
df.groupby('country').apply(lambda g: g.nlargest(3, 'spend'))
```

- These three patterns cover most aggregation needs
- Build the muscle of "split-apply-combine" thinking

---
## Documenting Findings

- Notebook with text + chart + commentary
- One finding per cell, named clearly
- Save the cleaned dataset alongside the notebook
- Numbered sections; future readers (you) need to navigate
- Notebooks are documentation as much as analysis

---
## Exploratory Outputs Visualised

![eda_outputs](svg/courses/data_science/data-analyst-fundamentals/04_exploratory_data_analysis/eda_outputs.svg)

---
## EDA Output

- A short writeup (the analyst's report)
- A few key charts that illustrate the findings
- A list of follow-up questions
- A list of data quality issues to fix
- A recommendation for the next step

---
## Common Mistakes

- Skipping EDA; jumping to a model
- One chart per cell, no narrative
- Drawing causal conclusions from EDA correlations
- Showing every chart you made in the final report
- Not documenting — three months later, no one knows what you found
