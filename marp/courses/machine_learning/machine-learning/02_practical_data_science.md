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

- Data cleaning
- Feature engineering
- Train / test split
- Cross validation
- Pipelines

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
## Feature Engineering

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
## Cross Validation

- k-fold: rotate which subset is test
- Stratified k-fold for classification
- More robust estimate
- Standard for model selection

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
## Imbalanced Classes

- Naive accuracy misleading
- Resample (SMOTE, undersample)
- Class weights
- Use precision, recall, F1, AUC

---
## Common Practical Mistakes

- Scaling before split
- Imputing before split
- Ignoring distribution shift between train and prod
- Tuning on test set
- Single train/test split for noisy data
