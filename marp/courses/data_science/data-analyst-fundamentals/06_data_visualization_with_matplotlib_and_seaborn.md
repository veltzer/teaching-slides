---
tags:
  - data-and-ai:visualization
  - languages:python
level: beginner
category: data-science
audience:
  - audiences:data-analysts

---
# Data Visualization with Matplotlib and Seaborn

---
## What This Chapter Covers

- Visualisation principles
- Matplotlib basics: lines, bars, scatter, histograms
- Customising plots
- Seaborn for statistical visualisations
- Heatmaps, pair plots, categorical plots
- Choosing the right chart

---
## Visualisation Principles

- A chart is for *communication*, not decoration
- Every visual element should encode information
- Less ink, more signal
- Match the chart type to the question
- Read Tufte; the principles outlast any tool

---
## Common Chart Types

- **Bar / column**: compare categories
- **Line**: change over time
- **Scatter**: relationship between two numerics
- **Histogram**: distribution of one variable
- **Box / violin**: distribution + comparison
- **Heatmap**: relationships across many pairs

---
## Matplotlib Basics

```python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [2, 4, 1, 5, 3]
plt.plot(x, y)
plt.title("My First Plot")
plt.xlabel("Day")
plt.ylabel("Value")
plt.show()
```

- The foundational Python plotting library
- Verbose; you spell out every detail
- Total control; sometimes too much

---
## Bar Charts

```python
df.groupby('country')['orders'].sum().plot.bar()
plt.ylabel("Total orders")
plt.title("Orders by country")
```

- Default plot for categorical comparisons
- Sort bars by value (descending) for readability
- Horizontal bars (`barh`) for many categories or long labels
- Avoid 3D bars — they distort perception

---
## Line Charts

```python
df.set_index('date')['daily_users'].plot()
plt.title("Daily users over time")
```

- For time series and continuous trends
- Multiple lines on one chart for comparison
- Label the lines, not just a legend, when there are 2-3
- Smooth heavy noise with a rolling average

---
## Scatter Plots

```python
df.plot.scatter(x='age', y='spend', alpha=0.3)
```

- Two-numeric relationship
- Add transparency (`alpha`) to handle overplotting
- Add color/size for a third dimension
- Add a regression line for trend (`sns.regplot`)

---
## Histograms

```python
df['age'].plot.hist(bins=30)
```

- One numeric distribution
- Bin count matters; experiment
- Two histograms overlaid (with transparency) for comparison
- For categorical, use bar chart instead

---
## Customising Plots

```python
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, y, color='steelblue', linewidth=2, marker='o')
ax.set_title("Title", fontsize=16)
ax.set_xlabel("X label")
ax.grid(True, alpha=0.3)
ax.spines['top'].set_visible(False)
plt.tight_layout()
plt.savefig('out.png', dpi=150)
```

- `figsize` for size; `tight_layout` to avoid clipping
- Remove top/right spines for a cleaner look
- Save as PNG (raster) or SVG (vector) depending on use

---
## Seaborn

```python
import seaborn as sns

sns.set_theme()                   # nicer defaults
sns.scatterplot(data=df, x='age', y='spend', hue='country')
sns.boxplot(data=df, x='dept', y='salary')
sns.histplot(data=df, x='age', kde=True)
```

- Built on top of matplotlib
- Less verbose; sensible defaults
- Statistical extras: regression lines, KDE, distributions
- The default for most analyst plotting in Python

---
## Heatmaps

```python
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0)
```

- Great for correlation matrices
- Pivot tables visualised
- `annot=True` shows values in cells
- `center=0` for diverging color scales

---
## Pair Plots

```python
sns.pairplot(df[['age', 'income', 'spend', 'churn']], hue='churn')
```

- Every numeric column vs every other
- Diagonal: distribution of each column
- Off-diagonal: scatter of pairs
- Quickly spot relationships in a small dataset

---
## Categorical Plots

```python
sns.catplot(data=df, x='dept', y='salary', kind='box')
sns.catplot(data=df, x='country', kind='count', order=top10)
sns.violinplot(data=df, x='dept', y='salary')
```

- `kind` argument switches plot type
- Box: shows median, quartiles, outliers
- Violin: shows full distribution shape
- Strip / swarm: every data point shown

---
## Color Choices

- Default palettes: `viridis`, `plasma` for sequential
- `coolwarm`, `RdBu` for diverging
- `tab10`, `Set2` for categorical
- Avoid red-green for accessibility (colour-blindness)
- Stick to one palette per report

---
## Choosing the Right Chart

- Comparing categories &#8594; bar
- Trend over time &#8594; line
- Two numeric variables &#8594; scatter
- Distribution of one variable &#8594; histogram or KDE
- Distribution by group &#8594; box / violin
- Many pairwise relationships &#8594; heatmap or pair plot

---
## When NOT to Use a Pie Chart

- More than 5 slices: unreadable
- Slices that are similar in size: hard to compare
- For comparison across a third dimension: impossible
- Use a bar chart instead, sorted by value
- 3D pie charts: never

---
## Common Mistakes

- Decorative chart junk that hides the data
- Truncated y-axes that exaggerate small differences
- Too many series on one chart
- Default rotated labels that overlap
- Saving low-resolution images for print or projection
