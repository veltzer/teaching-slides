---
tags:
  - math:descriptive-statistics
level: beginner
category: math
audience:
  - audiences:data-analysts
  - audiences:developers

---
# Visualizing Data

---
## What This Chapter Covers

- Why a picture beats a summary statistic
- Histograms and density plots
- Box plots and violin plots
- Scatter plots and the danger of summaries alone
- Bar charts vs the things people misuse them for
- A few honesty rules for axes

---
## Anscombe's Quartet

![anscombe](svg/courses/math/statistics-applied/05_visualizing_data/anscombe.svg)

---
## Anscombe's Lesson

- Four datasets, identical means, variances, correlations, and regression lines
- They look *completely* different when plotted
- One is linear, one curved, two are dominated by a single point
- Summary statistics are a lossy compression — always look first
- "Plot the data" is the cheapest, highest-value habit in statistics

---
## Histograms

- Bins the data and draws a bar per bin — the workhorse for one numeric variable
- Shows center, spread, skew, gaps, and multiple peaks at a glance
- Bin width matters: too wide hides structure, too narrow shows noise
- A density plot is a smoothed histogram — nicer for overlaying groups
- Always check your data with a histogram before testing anything

---
## Box And Violin Plots

- **Box plot**: the five-number summary as a box with whiskers and outlier dots
- Compact — fits many groups side by side
- Hides multimodality (a box can't show two peaks)
- **Violin plot**: a box plot with a density curve on each side — shows shape
- Use box plots to compare, violin plots when shape matters

---
## Scatter Plots

- Two numeric variables, one dot per observation
- Shows relationship, curvature, clusters, and outliers
- The only honest way to "see" a correlation
- Add a fitted line for trend, but keep the dots
- Overplotting? Use transparency or hexbin so density is visible

---
## Bar Charts And Their Misuse

- Bar charts compare a numeric value *across categories* — sales by region
- Bars start at zero, always — truncating the axis lies about ratios
- Don't use a bar chart for a distribution (that's a histogram) or a time trend (that's a line)
- Don't stack more than a handful of segments — nobody can compare them
- Sort bars by value unless the category has a natural order

---
## Truncated vs Honest Axes

![axis_honesty](svg/courses/math/statistics-applied/05_visualizing_data/axis_honesty.svg)

---
## A Minimal matplotlib Example

```python
import numpy as np, matplotlib.pyplot as plt
rng = np.random.default_rng(0)
x = rng.normal(50, 10, 500)
fig, ax = plt.subplots(1, 2, figsize=(8, 3))
ax[0].hist(x, bins=25)
ax[0].set_title("histogram")
ax[1].boxplot(x, vert=False)
ax[1].set_title("box plot")
fig.tight_layout()
```

---
## Honesty Rules For Charts

- Bar and area charts: y-axis starts at zero, no exceptions
- Don't use dual y-axes to fake a correlation
- Label units; a number with no unit is a riddle
- Same scale when comparing panels side by side
- One message per chart — if you need a legend with eight entries, split it

---
## Common Mistakes

- Reporting summary statistics without ever plotting the data
- Truncated y-axes on bar charts to exaggerate a change
- Pie charts with ten slices nobody can compare
- Line charts of unordered categories
- Overplotted scatter plots that hide where the mass is
