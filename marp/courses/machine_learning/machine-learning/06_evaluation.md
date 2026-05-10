---
tags:
  - data-and-ai:machine-learning
level: intermediate
category: machine-learning
audience:
  - audiences:data-scientists

---
# Evaluation

---
## What This Chapter Covers

- Classification metrics
- Regression metrics
- Confusion matrix
- ROC and PR curves
- Cross-validation strategies
- Leakage avoidance

---
## Why Evaluation Matters

- Models are only useful if measured
- Pick a metric that maps to the business
- One number isn't enough
- Slice the results

---
## Pick The Right Metric

- Classification: accuracy is rarely it
- Regression: which error matters
- Imbalanced: AUC, PR-AUC, F1
- Match cost of each error

---
## Accuracy

- (TP + TN) / total
- Easy, but misleading on imbalance
- Use only when classes balanced
- Always report alongside others

---
## Confusion Matrix

- Rows: true labels
- Columns: predicted
- Counts in each cell
- Foundation of classification metrics

---
## Confusion Matrix Diagram

![confusion_matrix](svg/courses/machine_learning/machine-learning/06_evaluation/confusion_matrix.svg)

---
## TP, TN, FP, FN

- TP: correctly predicted positive
- TN: correctly predicted negative
- FP: false alarm
- FN: miss

---
## Precision

- Of predicted positives, how many real
- TP / (TP + FP)
- High precision: few false alarms
- Care when FPs are costly

---
## Recall

- Of actual positives, how many caught
- TP / (TP + FN)
- High recall: few misses
- Care when FNs are costly

---
## Precision vs Recall Tradeoff

- Lower threshold: more recall, less precision
- Higher threshold: more precision, less recall
- Application decides which matters

---
## F1 Score

- Harmonic mean of precision and recall
- Single number balance
- F-beta weights one more
- Useful default for imbalanced

---
## Specificity

- Of actual negatives, how many predicted negative
- TN / (TN + FP)
- Used in medical screening
- The "negative recall"

---
## ROC Curve

- True positive rate vs false positive rate
- Sweep all thresholds
- Diagonal = random
- Upper left = perfect

---
## ROC Diagram

![roc_curve](svg/courses/machine_learning/machine-learning/06_evaluation/roc_curve.svg)

---
## AUC-ROC

- Area under ROC curve
- 0.5 = random, 1.0 = perfect
- Threshold-independent
- Misleading on heavy imbalance

---
## PR Curve

- Precision vs recall, all thresholds
- Better for imbalanced
- Random baseline = positive class rate
- AUC-PR

---
## When To Use Which

- Balanced: ROC fine
- Imbalanced positive class: PR is better
- Both can be reported
- Pair with confusion matrix

---
## Multi-Class Metrics

- Confusion matrix is bigger
- Per-class precision, recall, F1
- Averaging: macro, micro, weighted
- Accuracy is still valid

---
## Macro vs Micro

- Macro: average of per-class scores
- Micro: pool then compute
- Macro favours rare classes equally
- Micro favours frequent classes

---
## Multi-Label Metrics

- Hamming loss
- Subset accuracy
- Per-label precision, recall, F1
- Harder to summarise

---
## Calibration

- Predicted probabilities vs observed rates
- Reliability diagram
- Brier score
- Important when probabilities used downstream

---
## Calibration Methods

- Platt scaling: logistic on outputs
- Isotonic regression: non-parametric
- Apply on a held-out set
- Don't recalibrate on training

---
## Regression Metrics

- MAE: mean absolute error
- MSE: mean squared error
- RMSE: square root of MSE
- R squared: variance explained

---
## MAE vs MSE

- MAE: equal weight to all errors
- MSE: penalises big errors more
- RMSE: same units as target
- Pick by what you fear

---
## R Squared

- 1 - (SS_residual / SS_total)
- 1 = perfect, 0 = predicting the mean
- Negative = worse than mean
- Misleading on tiny variance

---
## MAPE

- Mean absolute percentage error
- Scale-free
- Breaks at zero
- Use cautiously

---
## Quantile Loss

- Pinball loss
- Penalises one side more
- For predicting medians, percentiles
- Robust to outliers

---
## Train / Validation / Test

- Train: fit
- Validation: choose
- Test: estimate
- Three roles, three sets

---
## Holdout Method

- Single split
- Cheap
- High variance
- Use only with lots of data

---
## k-Fold Cross-Validation

- Split into k parts
- Rotate which is validation
- Average the metric
- Robust estimate

---
## CV Diagram

![kfold](svg/courses/machine_learning/machine-learning/06_evaluation/kfold.svg)

---
## Stratified k-Fold

- Preserve class ratios in each fold
- Important for imbalanced classification
- sklearn's default for classifiers

---
## Time Series CV

- No future leak into past
- Forward chaining
- Walk-forward
- Respect temporal order

---
## Group k-Fold

- Same group always in same fold
- Patients, customers, sessions
- Avoid leakage across related rows

---
## Leave-One-Out

- k = n
- Maximum data for training
- Expensive, high variance
- Tiny datasets only

---
## Repeated CV

- k-fold many times with different splits
- Lower variance estimate
- Expensive
- Useful for noisy metrics

---
## Nested CV

- Outer: estimate generalisation
- Inner: pick hyperparameters
- Honest comparison of pipelines
- Expensive but defensible

---
## Common Leakage

- Scaling on full data
- Imputing on full data
- Target encoding without folds
- Test info in features

---
## Avoiding Leakage

- Fit transformers on train only
- Use Pipelines
- Group/time splits when applicable
- Audit features

---
## Statistical Significance

- Difference between models real
- McNemar's test for classifiers
- Paired t-test on CV scores
- Beware multiple comparisons

---
## Subgroup Analysis

- Slice by demographic, geography, time
- Average metrics hide failures
- Fairness implications
- Always slice

---
## Reporting Results

- Mean and standard deviation across folds
- Confidence intervals
- Confusion matrix
- A few example errors

---
## sklearn Metrics

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix,
    classification_report
)
```

---
## Common Evaluation Mistakes

- Reporting accuracy on imbalanced
- One holdout, no CV
- Tuning on test set
- Ignoring subgroup performance

---
## Precision-Recall Curve

![pr_curve](svg/courses/machine_learning/machine-learning/06_evaluation/pr_curve.svg)

---
## Calibration

![calibration](svg/courses/machine_learning/machine-learning/06_evaluation/calibration.svg)

---
## Multi-Class Confusion

![multiclass_confusion](svg/courses/machine_learning/machine-learning/06_evaluation/multiclass_confusion.svg)

---
## Train / Validate / Test

![train_val_test_split](svg/courses/machine_learning/machine-learning/06_evaluation/train_val_test_split.svg)

---
## Precision-Recall Tradeoff

![precision_recall_tradeoff](svg/courses/machine_learning/machine-learning/06_evaluation/precision_recall_tradeoff.svg)

---
## Time Series CV

![time_series_cv](svg/courses/machine_learning/machine-learning/06_evaluation/time_series_cv.svg)

---
## Leakage in Pipelines

![leakage_pipeline](svg/courses/machine_learning/machine-learning/06_evaluation/leakage_pipeline.svg)

---
## Summary

- Match metric to business cost
- Confusion matrix is the foundation
- Cross-validation, not a single split
- Slice your evaluation; one number lies
