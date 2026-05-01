---
tags:
  - data-and-ai:data-cleaning
level: beginner
category: data-science
audience:
  - audiences:data-analysts

---
# Data Cleaning

---
## What This Chapter Covers

- Identifying data quality issues
- Missing values: detect and handle
- Duplicates and how they sneak in
- Type conversions and formatting
- Outliers: detect and treat
- Standardisation and normalisation
- Validation techniques

---
## Why Cleaning Matters

- Most analysis time goes here
- Bad data = bad answers
- Stakeholders trust *consistent* numbers more than *correct* ones initially
- A clean 1000-row dataset beats a dirty 10M-row one
- The skill of catching data issues separates senior from junior analysts

---
## Common Quality Issues

- **Missing values**: NULL, empty string, "N/A", 0 (often wrong)
- **Duplicates**: same record entered twice
- **Inconsistent formats**: "United States", "USA", "U.S.A."
- **Wrong types**: numbers stored as strings
- **Outliers**: bots, glitches, edge cases
- **Encoding**: UTF-8 vs Latin-1 mojibake

---
## Detecting Missing Data

```python
df.isnull().sum()                  # missing count per column
df.isnull().mean()                 # missing fraction per column
df[df['email'].isnull()].head()    # rows with missing email
```

- Missing data has many forms — check for empty strings, "?", "Unknown"
- Different missingness mechanisms need different responses
- Document what you found; surprise stakeholders early

---
## Handling Missing Data

- **Drop rows**: simple, but biases toward complete records
- **Drop columns**: if a column is mostly missing
- **Impute mean / median / mode**: cheap, distorts the distribution
- **Impute by group**: median age within country
- **Model-based imputation**: predict missing from other columns
- **Treat missing as a value**: sometimes the most honest

---
## Dealing With Duplicates

```python
df.duplicated().sum()                       # how many?
df.drop_duplicates(inplace=True)            # all-column dedup
df.drop_duplicates(subset=['email'], keep='last')
```

- Beware: rows that look identical may differ in one timestamp
- Decide what *you* mean by "duplicate" — full row, or by ID?
- Keep first / keep last / aggregate may all be valid choices

---
## Type Conversions

```python
df['age'] = pd.to_numeric(df['age'], errors='coerce')
df['signup_date'] = pd.to_datetime(df['signup_date'])
df['price'] = df['price'].str.replace('$', '').astype(float)
```

- `errors='coerce'`: invalid values become NaN (don't crash)
- Parsing dates is a frequent source of bugs (timezone, format)
- Currency strings, "1,000.00" formats — clean before converting

---
## Detecting Outliers

```python
import numpy as np

q1, q3 = df['amount'].quantile([0.25, 0.75])
iqr = q3 - q1
mask = (df['amount'] < q1 - 1.5 * iqr) | (df['amount'] > q3 + 1.5 * iqr)
df_clean = df[~mask]
```

- IQR rule: anything beyond 1.5 IQR from Q1/Q3 is "unusual"
- Z-score: more than 3 standard deviations from the mean
- Domain knowledge often beats either: an analyst should sanity-check
- Outliers may be data errors *or* real and important — investigate before discarding

---
## Treating Outliers

- **Remove**: only if you're sure they're errors
- **Cap (winsorise)**: clip at the 5th/95th percentile
- **Transform**: log of skewed data calms long tails
- **Report separately**: top customers analysed alongside everyone else
- Document the choice — "we excluded the top 0.5% of orders"

---
## Standardisation

- Same value, many representations: "USA", "U.S.A.", "United States"
- Pick a canonical form; convert
- Country codes (ISO 3166), currency codes (ISO 4217), language codes (BCP 47)
- Use existing standards — don't invent your own
- Build a "lookup table" for common transformations

---
## Normalisation

- Rescaling numbers to a comparable range
- **Min-max**: scale to [0, 1]
- **Z-score**: mean 0, standard deviation 1
- Useful for plotting and for ML features
- Be careful: normalising changes interpretability

---
## Encoding Issues

- "café" rendered as "café" = UTF-8 bytes interpreted as Latin-1
- The fix: detect actual encoding (`chardet`), re-decode correctly
- Source files often lie about their encoding
- Pandas: `pd.read_csv(... , encoding='utf-8')` and try alternatives if it fails
- Save outputs as UTF-8 — the modern standard

---
## Validation Rules

- Each column has *constraints*: type, range, format
- Codify them: `0 <= age <= 120`, `email matches /.+@.+/`
- Tools: Great Expectations, Pandera, Pydantic
- Run validations as part of every load
- Catch bad data at the source, not in the dashboard

---
## Idempotent Cleaning

- The same cleaning script should produce the same output every time
- No random sampling without a seed
- No timestamps in filenames
- Deterministic transformations
- This is what makes pipelines trustworthy

---
## Document Everything

- Every cleaning decision changes the dataset
- A "clean" file should come with a list of *what was done to it*
- Why: future analysts (often you) need to reproduce
- Why: stakeholders need to interpret correctly
- A README plus a versioned cleaning script is the minimum

---
## Common Mistakes

- Cleaning silently — nobody knows what changed
- Treating missing as zero
- Removing outliers without checking they're errors
- Inconsistent dedup rules across analyses
- Skipping cleaning "just for this one chart" — that chart goes to the CEO
