---
tags:
  - data-and-ai:machine-learning
level: intermediate
category: machine-learning
audience:
  - audiences:data-scientists

---
# Machine Learning Overview

---
## What This Chapter Covers

- What is ML
- Types of learning
- Workflow
- Evaluation metrics
- Tradeoffs

---
## What ML Is

- Algorithms learn patterns from data
- No explicit rules programmed
- Generalises to unseen data
- Predict or decide

---
## Three Types

- Supervised: labelled data
- Unsupervised: no labels, find structure
- Reinforcement: agent learns from rewards

---
## Supervised Learning

- Input X, target y
- Classification: discrete y
- Regression: continuous y
- Most production ML

---
## Unsupervised Learning

- Only X, no labels
- Clustering: group similar
- Dimensionality reduction
- Anomaly detection

---
## Reinforcement Learning

- Agent, environment, rewards
- Trial-and-error
- Games, robotics, recommendation
- Hard to train, sparse rewards

---
## ML Workflow

- Define problem
- Collect data
- Engineer features
- Train models
- Evaluate
- Deploy
- Monitor

---
## Bias vs Variance

- Bias: model too simple, underfits
- Variance: model too complex, overfits
- Tradeoff: simpler vs more flexible
- Balance with regularisation, more data

---
## Overfitting

- Model memorises training data
- Poor generalisation
- Symptoms: high train acc, low test acc
- Mitigate: regularisation, more data, cross-validation

---
## Underfitting

- Model too simple
- Both train and test perform poorly
- Mitigate: richer features, deeper model

---
## Classification Metrics

- Accuracy: % correct
- Precision: of predicted positives, how many right
- Recall: of actual positives, how many caught
- F1: harmonic mean
- AUC-ROC: threshold-independent

---
## Regression Metrics

- MAE: mean absolute error
- MSE / RMSE: squared error, penalises outliers
- R squared: variance explained
- Use multiple

---
## Choosing a Model

- Linear: interpretable, fast
- Tree-based: handle nonlinearity, robust
- Neural: huge data, complex patterns
- Ensemble: often best in practice

---
## When ML Is Not The Answer

- Small data
- Need full interpretability
- Rules already work
- Cost of errors very high

---
## Common Overview Mistakes

- Choosing complex model with little data
- Optimising wrong metric for the business
- Ignoring train/serve skew
- Forgetting baseline (e.g., majority class predictor)
- Not retraining on shifting distributions
