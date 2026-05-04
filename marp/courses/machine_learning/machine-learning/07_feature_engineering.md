---
tags:
  - data-and-ai:machine-learning
level: intermediate
category: machine-learning
audience:
  - audiences:data-scientists

---
# Feature Engineering

---
## What This Chapter Covers

- Why features matter
- Numeric features
- Categorical encoding
- Time and date features
- Text and image features
- Feature selection
- Leakage avoidance

---
## Why Features Matter

- Often more impact than algorithm choice
- A great feature beats a fancy model
- Domain knowledge encoded as inputs
- Cheap wins for the practitioner

---
## What A Feature Is

- A column the model sees
- Numeric, categorical, embedding
- Derived from raw data
- Stable, reproducible

---
## Feature Pipeline

- Raw data
- Clean
- Transform
- Engineer
- Encode
- Scale

---
## Numeric Cleaning

- Missing values
- Wrong types
- Units
- Negatives where impossible

---
## Imputation

- Mean, median, mode
- Constant
- Model-based: kNN, iterative
- Add was-missing indicator

---
## Scaling

- Standardise: zero mean, unit variance
- Min-max to [0, 1]
- Robust scaling: median and IQR
- Log for skewed

---
## Log Transform

- Compresses heavy tails
- Prices, counts, durations
- Use log1p for zeros
- Reverse with expm1

---
## Power Transforms

- Box-Cox: positive only
- Yeo-Johnson: any sign
- Make distributions more normal
- Helps linear models

---
## Binning

- Discretise continuous
- Equal-width or equal-frequency
- Tree models don't need it
- Linear models can benefit

---
## Polynomial Features

- x squared, x times y
- Capture interactions
- Explodes quickly
- Use with regularisation

---
## Categorical Basics

- Models need numbers
- Many strategies
- Choice depends on cardinality
- And on the model

---
## Label Encoding

- Map categories to integers
- Implies ordinality
- Wrong for nominal data
- OK for tree models with care

---
## One-Hot Encoding

- Column per category
- Sparse representation
- Standard for nominal
- Explodes with high cardinality

---
## Ordinal Encoding

- Integers reflect order
- Small, medium, large → 1, 2, 3
- Use only with true ordering
- Good for tree models

---
## Target Encoding

- Replace category with target mean
- Works for high cardinality
- Leakage risk if done naively
- Use out-of-fold

---
## Frequency Encoding

- Replace with category count
- Cheap and useful
- Captures popularity
- No leakage

---
## Hash Encoding

- Hash to a fixed-size bucket
- Bounded memory
- Collisions, but workable
- Used in big-feature spaces

---
## Embedding Encoding

- Learned dense vector per category
- Neural nets, factorisation machines
- Captures similarity
- Needs lots of data

---
## Time Features

- Year, month, day, hour, minute
- Day of week
- Is weekend
- Is holiday

---
## Cyclical Encoding

- Hour wraps 23 to 0
- sin and cos of `(hour / 24 * 2 * pi)`
- Two columns
- Smooth across boundary

---
## Date Differences

- Days since signup
- Time between events
- Time to deadline
- Often very predictive

---
## Lag Features

- Previous value of a series
- Predict tomorrow from yesterday
- Several lags
- Beware leakage

---
## Rolling Features

- Mean, std, min, max over window
- Recent behaviour
- Different window sizes
- Time-based, not row-based

---
## Text Features

- Bag of words
- TF-IDF
- n-grams
- Embeddings: word2vec, BERT

---
## TF-IDF

- Term frequency × inverse document frequency
- Down-weights common words
- Sparse, fast
- Strong baseline for text

---
## Image Features

- Pretrained CNN as feature extractor
- ResNet, ViT embeddings
- Avoids retraining
- Transfer learning

---
## Cross Features

- Combine two columns
- City × time-of-day
- Captures interactions
- Important for linear models

---
## Group Aggregations

- Mean amount per customer
- Max session length per user
- Useful for transactional data
- Beware leakage with target

---
## Feature Generation Tools

- Featuretools
- tsfresh for time series
- Automated ideas
- Validate before trusting

---
## Feature Selection

- Drop irrelevant
- Reduces overfitting
- Faster training and serving
- Easier interpretation

---
## Filter Methods

- Score each feature independently
- Variance threshold
- Correlation with target
- Mutual information

---
## Wrapper Methods

- Try subsets, evaluate model
- Recursive feature elimination
- Forward / backward selection
- Expensive

---
## Embedded Methods

- Selection during training
- L1 sets weights to zero
- Tree feature importance
- Cheapest, often best

---
## Feature Importance

- From tree-based models
- Permutation importance: drop one, retest
- SHAP values: per-instance attributions
- Inspect, debug, communicate

---
## Leakage In Features

- Future values
- Target-derived without folds
- Test data in summaries
- IDs that encode the target

---
## Avoiding Leakage

- Fit transformers on train only
- Group splits for related rows
- Time splits respecting order
- Audit every feature

---
## Pipelines

- Encapsulate steps
- Apply same transform train and serve
- Prevents leakage
- Reproducible

---
## sklearn ColumnTransformer

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
ct = ColumnTransformer([
    ("num", StandardScaler(), num_cols),
    ("cat", OneHotEncoder(),  cat_cols),
])
```

---
## Common Mistakes

- High-cardinality one-hot
- Target encoding without folds
- Future information in lags
- Fitting transformers on full data

---
## One-Hot vs Ordinal

![onehot_vs_ordinal](svg/courses/machine_learning/machine-learning/07_feature_engineering/onehot_vs_ordinal.svg)

---
## Scaling

![scaling](svg/courses/machine_learning/machine-learning/07_feature_engineering/scaling.svg)

---
## Cyclical Encoding

![cyclical_encoding](svg/courses/machine_learning/machine-learning/07_feature_engineering/cyclical_encoding.svg)

---
## Target Encoding

![target_encoding](svg/courses/machine_learning/machine-learning/07_feature_engineering/target_encoding.svg)

---
## Leakage

![leakage](svg/courses/machine_learning/machine-learning/07_feature_engineering/leakage.svg)

---
## Summary

- Features beat algorithms
- Numeric, categorical, time, text need different handling
- Selection trims fat
- Leakage is the silent killer
