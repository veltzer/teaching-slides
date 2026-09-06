---
tags:
  - data-and-ai:machine-learning
level: intermediate
category: machine-learning
audience:
  - audiences:data-scientists

---

# Practical Data Science

---

## ML Workflow

![ml_workflow](svg/courses/machine_learning/machine-learning/02_practical_data_science/ml_workflow.svg)

---

## What This Chapter Covers

- numpy
- pandas
- matplotlib
- scipy
- Cleaning, splits, pipelines

---

## numpy

- Array library for Python
- Vectorised, fast
- Foundation of the stack
- C under the hood

---

## numpy Arrays

```python
import numpy as np
a = np.array([1, 2, 3])
b = np.zeros((3, 4))
c = np.arange(10)
d = np.linspace(0, 1, 5)
```

---

## numpy Operations

```python
a + b       # elementwise
a @ b       # matrix mul
np.mean(a)
np.std(a)
a.reshape(2, 2)
```

---

## Broadcasting

```python
m = np.ones((3, 4))
v = np.array([1, 2, 3, 4])
m + v       # row-wise add
```

- Rules: align trailing dims
- Avoids loops

---

## numpy Indexing

```python
a[0]
a[1:3]
a[a > 5]    # boolean
a[[0, 2]]   # fancy
```

---

## Random Numbers

```python
rng = np.random.default_rng(42)
rng.normal(size=100)
rng.choice([0, 1], size=10)
```

- Seed for reproducibility

---

## pandas

- Tabular data, like a spreadsheet
- Two cores: Series and DataFrame
- Reads CSV, Parquet, SQL
- Foundation of cleaning work

---

## DataFrame Basics

```python
import pandas as pd
df = pd.read_csv("data.csv")
df.head()
df.info()
df.describe()
```

---

## Selecting Columns

```python
df["name"]
df[["a", "b"]]
df.loc[:, "a":"c"]
df.iloc[:, 0:3]
```

---

## Filtering Rows

```python
df[df["age"] > 30]
df[df["dept"].isin(["A", "B"])]
df.query("age > 30 and dept == 'A'")
```

---

## Missing Data

```python
df.isna().sum()
df.dropna()
df.fillna(0)
df["col"].fillna(df["col"].mean())
```

---

## GroupBy

```python
df.groupby("dept")["salary"].mean()
df.groupby(["dept", "level"]).agg({"salary": "mean", "id": "count"})
```

---

## Joins

```python
left.merge(right, on="key", how="inner")
left.merge(right, on="key", how="left")
pd.concat([df1, df2], axis=0)
```

---

## Reshaping

```python
df.pivot_table(index="dept", columns="year", values="salary")
df.melt(id_vars="id", value_vars=["a", "b"])
```

---

## Time Series

```python
df["ts"] = pd.to_datetime(df["ts"])
df.set_index("ts").resample("D").mean()
df["lag1"] = df["x"].shift(1)
```

---

## Apply

```python
df["x2"] = df["x"].apply(lambda v: v * 2)
df.apply(np.mean, axis=0)
```

- Slow vs vectorised; prefer built-ins

---

## matplotlib

- The plotting workhorse
- Imperative API
- Customisable
- Foundation for seaborn, others

---

## Basic Plot

```python
import matplotlib.pyplot as plt
plt.plot([1, 2, 3], [1, 4, 9])
plt.xlabel("x")
plt.ylabel("y")
plt.show()
```

---

## Histogram

```python
plt.hist(df["age"], bins=30)
plt.title("Age distribution")
plt.show()
```

---

## Scatter

```python
plt.scatter(df["x"], df["y"], alpha=0.3)
plt.show()
```

---

## Subplots

```python
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes[0, 0].plot(x, y)
axes[0, 1].hist(df["age"])
plt.tight_layout()
```

---

## scipy

- Scientific computing
- Stats, optimisation, signal, sparse
- Built on numpy
- Used inside scikit-learn

---

## scipy.stats

```python
from scipy import stats
stats.norm.pdf(0)
stats.ttest_ind(a, b)
stats.pearsonr(x, y)
```

---

## Optimisation

```python
from scipy.optimize import minimize
res = minimize(lambda x: (x - 3) ** 2, x0=0)
res.x
```

---

## Sparse Matrices

```python
from scipy.sparse import csr_matrix
m = csr_matrix(dense)
```

- Memory-efficient for many zeros
- Used in NLP, recommenders

---

## Data Cleaning

- Missing values
- Outliers
- Duplicates
- Type conversions
- 80% of the work

---

## Feature Engineering

![feature_engineering](svg/courses/machine_learning/machine-learning/02_practical_data_science/feature_engineering.svg)

---

## Missing Values

- Drop rows / columns
- Impute: mean, median, model-based
- Indicator: was-missing flag
- Choice depends on data

---

## Outliers

- Visual: box plots, scatter
- Statistical: z-score, IQR
- Domain: sensor errors vs real extremes
- Decide: drop, cap, or keep

---

## Feature Engineering Basics

- Create new variables
- Domain-driven
- Often more impact than model choice
- Examples: ratios, time-of-day, lags

---

## Encoding

- Categorical to numeric
- One-hot for nominal
- Ordinal for ordered
- Target encoding (with care; leakage risk)

---

## Scaling

- Standardise: zero mean, unit variance
- Min-max: [0, 1]
- Required for: SVM, neural nets, distance-based
- Tree models: unaffected

---

## Train / Test Split

- Holdout set: never touched until final
- Typical: 70/15/15 or 80/20
- Stratify on target for classification
- Time series: respect temporal order

---

## Split with sklearn

```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
```

---

## Cross Validation

- k-fold: rotate which subset is test
- Stratified k-fold for classification
- More robust estimate
- Standard for model selection

---

## CV with sklearn

```python
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")
scores.mean(), scores.std()
```

---

## Data Leakage

- Test info contaminates training
- Common: scaling on full data
- Common: target encoding without folds
- Catastrophic; fit and transform per fold

---

## Pipelines

- Chain: preprocessing + model
- scikit-learn Pipeline
- Prevents leakage
- Reproducible

---

## Pipeline Example

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("clf",    LogisticRegression()),
])
pipe.fit(X_train, y_train)
```

---

## ColumnTransformer

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
ct = ColumnTransformer([
    ("num", StandardScaler(), num_cols),
    ("cat", OneHotEncoder(),  cat_cols),
])
```

---

## Imbalanced Classes

- Naive accuracy misleading
- Resample (SMOTE, undersample)
- Class weights
- Use precision, recall, F1, AUC

---

## Saving Models

```python
import joblib
joblib.dump(pipe, "model.pkl")
loaded = joblib.load("model.pkl")
```

- Pin sklearn version

---

## Common Practical Mistakes

- Scaling before split
- Imputing before split
- Ignoring distribution shift between train and prod
- Tuning on test set
- Single train/test split for noisy data

---

## NumPy Broadcasting

![numpy_broadcasting](svg/courses/machine_learning/machine-learning/02_practical_data_science/numpy_broadcasting.svg)

---

## Pandas GroupBy

![pandas_groupby](svg/courses/machine_learning/machine-learning/02_practical_data_science/pandas_groupby.svg)

---

## Train / Test Split Visualised

![train_test_split](svg/courses/machine_learning/machine-learning/02_practical_data_science/train_test_split.svg)

---

## Cross Validation Visualised

![cross_validation](svg/courses/machine_learning/machine-learning/02_practical_data_science/cross_validation.svg)

---

## Summary

- numpy, pandas, matplotlib, scipy are the toolkit
- Pipelines prevent leakage
- Cross-validation gives reliable estimates
- Cleaning dominates effort
