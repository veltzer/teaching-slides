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
- When to use ML

---

## Three Flavors

![ml_categories](svg/courses/machine_learning/machine-learning/03_machine_learning_overview/ml_categories.svg)

---

## What ML Is

- Algorithms learn patterns from data
- No explicit rules programmed
- Generalises to unseen data
- Predict or decide

---

## ML vs Traditional Programming

- Traditional: rules + data → answers
- ML: data + answers → rules
- ML wins when rules are hard to write

---

## A Brief History

- 1950s: perceptron
- 1980s: backprop, decision trees
- 2000s: SVM, ensembles
- 2010s: deep learning
- 2020s: foundation models

---

## Why ML Now

- Data abundance
- GPU compute
- Open source frameworks
- Cloud infrastructure

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

## Examples Supervised

- Spam detection
- House price prediction
- Credit scoring
- Medical diagnosis

---

## Unsupervised Learning

- Only X, no labels
- Clustering: group similar
- Dimensionality reduction
- Anomaly detection

---

## Examples Unsupervised

- Customer segmentation
- Topic modelling
- Compression
- Fraud signals from outliers

---

## Reinforcement Learning

- Agent, environment, rewards
- Trial-and-error
- Games, robotics, recommendation
- Hard to train, sparse rewards

---

## Examples Reinforcement

- AlphaGo, chess engines
- Robot control
- Ad bidding
- Inventory management

---

## Semi-Supervised

- Few labels, many unlabelled
- Use the unlabelled for structure
- Pseudo-labelling
- Often realistic case

---

## Self-Supervised

- Labels invented from data
- Predict next word, masked pixel
- Foundation of modern NLP
- Pretrain then fine-tune

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

## Define the Problem

- What do we predict
- What does success look like
- What's the cost of an error
- Is ML even the right tool

---

## Collect Data

- Sources, volume, quality
- Labels: human, weak, programmatic
- Privacy and consent
- Bias in collection

---

## Train Models

- Pick a baseline
- Try a few algorithms
- Hyperparameter tuning
- Compare on validation

---

## Evaluate

- Right metric for the problem
- Multiple metrics, not one
- Calibration matters
- Slice by subgroup

---

## Deploy

- Latency, throughput
- Versioning, rollback
- Logging predictions
- Feature parity train and serve

---

## Monitor

- Input drift
- Output drift
- Performance decay
- Retrain triggers

---

## The Math Underneath

- Linear algebra: vectors, matrices
- Calculus: gradients
- Probability: likelihoods, Bayes
- Optimisation: minimise a loss

---

## Loss Functions

- Squared error: regression
- Cross-entropy: classification
- Hinge: SVM
- Custom: tailor to business cost

---

## Optimisation

- Find weights that minimise loss
- Closed form: linear regression
- Gradient descent: most others
- Stochastic, mini-batch, batch

---

## Gradient Descent

- Compute gradient of loss
- Step in opposite direction
- Step size = learning rate
- Repeat until converged

---

## Bias vs Variance

- Bias: model too simple, underfits
- Variance: model too complex, overfits
- Tradeoff: simpler vs more flexible
- Balance with regularisation, more data

---

## Bias vs Variance

![bias_variance](svg/courses/machine_learning/machine-learning/03_machine_learning_overview/bias_variance.svg)

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

## Generalisation

- Performance on new data
- The whole point of ML
- Theory: PAC, VC dimension
- Practice: holdout, CV

---

## No Free Lunch

- No single algorithm best always
- Choice depends on data, task, constraints
- Try several, compare honestly

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

## Calibration

- Predicted probabilities should match observed
- Many models output ranks, not probs
- Calibration plots
- Platt scaling, isotonic

---

## Choosing a Model

- Linear: interpretable, fast
- Tree-based: handle nonlinearity, robust
- Neural: huge data, complex patterns
- Ensemble: often best in practice

---

## scikit-learn

- The Python ML standard
- Consistent API: fit, predict, transform
- Algorithms, preprocessing, evaluation
- Pipelines, model selection

---

## sklearn API

```python
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train, y_train)
preds = model.predict(X_test)
probs = model.predict_proba(X_test)
```

---

## Try Multiple Algorithms

```python
for clf in [LogisticRegression(), RandomForestClassifier(), GradientBoostingClassifier()]:
    clf.fit(X_train, y_train)
    print(clf.__class__.__name__, clf.score(X_test, y_test))
```

---

## When ML Is Not The Answer

- Small data
- Need full interpretability
- Rules already work
- Cost of errors very high

---

## ML vs Rules

- Rules: stable problem, known logic
- ML: fuzzy, evolving, statistical
- Hybrid: rules with ML overrides

---

## Cost of Mistakes

- Some errors are cheap
- Some errors are catastrophic
- Match metric to consequence
- Asymmetric losses

---

## Common Overview Mistakes

- Choosing complex model with little data
- Optimising wrong metric for the business
- Ignoring train/serve skew
- Forgetting baseline (e.g., majority class predictor)
- Not retraining on shifting distributions

---

## Supervised vs Unsupervised

![supervised_vs_unsupervised](svg/courses/machine_learning/machine-learning/03_machine_learning_overview/supervised_vs_unsupervised.svg)

---

## Loss Landscape

![loss_landscape](svg/courses/machine_learning/machine-learning/03_machine_learning_overview/loss_landscape.svg)

---

## Gradient Descent

![gradient_descent](svg/courses/machine_learning/machine-learning/03_machine_learning_overview/gradient_descent.svg)

---

## Summary

- ML learns from data, not rules
- Three big types; supervised dominates production
- Bias-variance tradeoff is everywhere
- Pick the right metric for your problem
