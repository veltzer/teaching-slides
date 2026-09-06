---
tags:
  - math:descriptive-statistics
level: beginner
category: math
audience:
  - audiences:data-analysts
  - audiences:developers

---

# Summarizing Data: Center

---

## What This Chapter Covers

- Mean, median, mode — what each one is
- When each is the honest choice
- Weighted means
- Trimmed means and robustness
- Skew and how it pulls the mean
- The "average" trap

---

## Mean, Median, Mode on a Skewed Distribution

![skewed_three_centers](svg/courses/math/statistics-applied/03_summarizing_center/skewed_three_centers.svg)

---

## Why We Summarize

- A column of 10,000 numbers tells you nothing at a glance
- A single "typical value" is the first compression
- But "typical" has three different meanings
- Pick the wrong one and you mislead — sometimes on purpose
- Always pair center with spread (next chapter)

---

## The Mean

- Sum divided by count: x&#772; = (&Sigma; x&#7522;) / n
- The "balance point" of the data
- Uses every value — sensitive to all of them, including outliers
- Best for roughly symmetric data with no extreme values
- One billionaire ruins the "average net worth" of a room

---

## The Median

- The middle value when sorted (average of the two middles if n is even)
- Half the data below, half above
- Ignores how extreme the extremes are — only their *side* counts
- Robust: changing the max to a million doesn't move it
- "Median household income" is the honest headline number

---

## The Mode

- The most frequently occurring value
- The only center that works for nominal data ("most common browser")
- Can be undefined (all unique) or multiple (bimodal)
- Useful for "what should we stock the most of?"
- Less informative for continuous data — bin first, then it's the tallest bar

---

## Mean vs Median And Skew

- **Right-skewed** (long tail to the right): mean > median — incomes, response times
- **Left-skewed** (long tail to the left): mean < median — exam scores near a ceiling
- **Symmetric**: mean &asymp; median
- The gap between them is a quick skew detector
- Report the median for skewed money and time data

---

## How an Outlier Drags the Mean

![outlier_pulls_mean](svg/courses/math/statistics-applied/03_summarizing_center/outlier_pulls_mean.svg)

---

## Weighted And Trimmed Means

- **Weighted mean**: each value carries a weight — average price weighted by quantity sold
- **Trimmed mean**: drop the top and bottom k% before averaging — Olympic scoring
- Trimming buys robustness without going all the way to the median
- Use weighted means whenever units aren't equally important
- A 10% trimmed mean is a good default when a few outliers are suspect

---

## Computing Centers

```python
import numpy as np
from scipy import stats
x = np.array([2, 3, 3, 4, 5, 5, 5, 6, 7, 200])
print("mean   :", np.mean(x))            # dragged up by 200
print("median :", np.median(x))          # unmoved
print("mode   :", stats.mode(x, keepdims=False).mode)
print("trim10 :", stats.trim_mean(x, 0.1))
```

---

## Common Mistakes

- Quoting the mean for skewed money or latency data
- Saying "average" without saying *which* average
- Forgetting the mode is the only option for categories
- Reporting a center with no spread alongside it
- Letting outliers silently inflate a headline number
