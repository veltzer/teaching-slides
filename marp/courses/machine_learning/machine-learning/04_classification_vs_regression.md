---
tags:
  - data-and-ai:machine-learning
level: intermediate
category: machine-learning
audience:
  - audiences:data-scientists

---
# Classification vs Regression

---
## What This Chapter Covers

- The two big supervised tasks
- When to use which
- Multi-class and multi-label
- Probabilities and thresholds
- Ordinal regression
- Conversion between them

---
## The Core Distinction

- Classification: discrete output
- Regression: continuous output
- Same algorithms, different head
- Same workflow, different metrics

---
## Classification Examples

- Email: spam or ham
- Image: cat, dog, or bird
- Patient: disease yes/no
- Loan: default or not

---
## Regression Examples

- House price
- Tomorrow's temperature
- Demand forecast
- Time-to-failure

---
## Output Type Matters

- Classifier: a label, sometimes with a probability
- Regressor: a number, with uncertainty if you ask
- Confuse the two and your metrics break

---
## Binary Classification

- Two classes
- Often imbalanced
- Choose a threshold
- Measure with AUC, F1

---
## Multi-Class Classification

- Three or more classes, exclusive
- Softmax output for neural nets
- One-vs-rest or one-vs-one for binary models
- Confusion matrix is bigger

---
## Multi-Label Classification

- Multiple labels can be true at once
- Tags, topics, attributes
- Predict each as independent binary
- Or use chain models

---
## Multi-Class vs Multi-Label

![multiclass_multilabel](svg/courses/machine_learning/machine-learning/04_classification_vs_regression/multiclass_multilabel.svg)

---
## Ordinal Targets

- Ordered categories: low, medium, high
- Distance between is unknown
- Treat as classification or regression
- Specialised algorithms exist

---
## Predicting Probabilities

- Many problems need a probability, not just a label
- Risk scoring, ranking, calibration
- Use predict_proba in sklearn
- Calibrate if needed

---
## Probability vs Score

- Some models output a score, not a probability
- SVM decision_function
- Trees give frequency, not calibrated
- Calibration converts scores to probabilities

---
## Choosing a Threshold

- Default 0.5 is rarely optimal
- Match to business costs
- Sweep thresholds, pick by metric
- Document the choice

---
## Threshold Tradeoffs

- High threshold: high precision, low recall
- Low threshold: high recall, low precision
- ROC and PR curves visualise the tradeoff

---
## Class Imbalance

- 99% one class, 1% another
- Accuracy meaningless
- Use AUC, PR-AUC
- Resample or weight classes

---
## Cost-Sensitive

- Different errors cost different amounts
- Weight classes
- Custom loss
- Calibrate threshold to costs

---
## Regression Output

- A real number
- Often with a confidence interval
- Sometimes a distribution
- Sometimes quantiles

---
## Linear Regression

- Output: weighted sum of features
- Loss: squared error
- Closed form
- Strong baseline

---
## Logistic Regression

- Despite the name: classification
- Output: probability via sigmoid
- Loss: log loss
- Strong baseline

---
## Sigmoid

- f(x) = 1 / (1 + exp(-x))
- Maps reals to (0, 1)
- Smooth threshold
- Interpretable

---
## Softmax

- Multi-class generalisation of sigmoid
- Output sums to 1
- Standard in neural nets
- Can be miscalibrated

---
## Quantile Regression

- Predict median, percentiles
- Robust to outliers
- Direct uncertainty
- Pinball loss

---
## Poisson Regression

- For count data
- Output is a rate
- Log link, exponential family
- Use when data are counts

---
## Survival Analysis

- Time to event
- Censored data: event hasn't happened yet
- Specialised models: Cox, accelerated failure time
- Common in medicine, churn

---
## Choosing Classification vs Regression

- Bin a continuous target if categories are decisions
- But: lose information
- Predict the number, then threshold for the decision
- Default to regression for continuous

---
## Discretisation Tradeoff

- Binning is lossy
- Easier business rules
- Worse statistical performance
- Decide late, predict raw

---
## Convert Regression to Classification

- Predict the number
- Apply a threshold
- Reuse calibration
- Decision is downstream

---
## Convert Classification to Regression

- Predict probability instead of label
- Predict expected value
- Often more useful in practice

---
## Common Confusions

- Calling logistic regression a regressor
- Reporting accuracy on imbalanced data
- One threshold for all decisions
- Treating ordinal as nominal

---
## Sklearn Classes

- Classifier: ends with Classifier or LogisticRegression
- Regressor: ends with Regressor
- Always check the type

---
## sklearn Examples

```python
from sklearn.linear_model import LogisticRegression, LinearRegression
clf = LogisticRegression()
reg = LinearRegression()
```

---
## Predicting With Both

```python
clf.fit(X, y_class).predict_proba(X_new)
reg.fit(X, y_real).predict(X_new)
```

---
## Evaluation Metrics

- Classification: accuracy, F1, AUC
- Regression: MAE, RMSE, R squared
- Don't mix them up

---
## Common Mistakes

- Threshold = 0.5 always
- Imbalanced data with accuracy
- Discretising too early
- Treating probs as calibrated

---
## Threshold Tradeoff

![threshold_tradeoff](svg/courses/machine_learning/machine-learning/04_classification_vs_regression/threshold_tradeoff.svg)

---
## Sigmoid vs Softmax

![sigmoid_vs_softmax](svg/courses/machine_learning/machine-learning/04_classification_vs_regression/sigmoid_vs_softmax.svg)

---
## Binary vs Multiclass

![binary_vs_multiclass](svg/courses/machine_learning/machine-learning/04_classification_vs_regression/binary_vs_multiclass.svg)

---
## Class Imbalance

![class_imbalance](svg/courses/machine_learning/machine-learning/04_classification_vs_regression/class_imbalance.svg)

---
## Summary

- Classification = label; regression = number
- Match the problem, not just the algorithm
- Probabilities give flexibility
- Threshold choice is part of the system
