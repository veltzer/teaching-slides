---
tags:
  - data-and-ai:machine-learning
level: intermediate
category: machine-learning
audience:
  - audiences:data-scientists

---

# Trees, Forests, and Boosting

---

## What This Chapter Covers

- Decision trees
- Splitting criteria
- Pruning
- Bagging
- Random forests
- Boosting and gradient boosting
- XGBoost, LightGBM, CatBoost

---

## Why Trees

- Handle nonlinearity
- Mixed feature types
- No need to scale
- Easy to inspect
- Strong on tabular

---

## Decision Tree Basics

- Series of yes/no splits
- Leaves give predictions
- Greedy top-down construction
- Recursive partitioning

---

## A Tree

![decision_tree](svg/courses/machine_learning/machine-learning/09_trees_and_forests/decision_tree.svg)

---

## How A Split Is Chosen

- For each feature, each threshold
- Compute impurity gain
- Pick the best
- Recurse on each side

---

## Gini Impurity

- Probability of wrong label if labelled by frequency
- Range 0 (pure) to 0.5 (binary balanced)
- Default in sklearn

---

## Entropy

- -sum p_i log p_i
- Information-theoretic measure
- Similar behaviour to Gini
- Use either

---

## Information Gain

- Parent impurity minus weighted child impurity
- Tree picks the split with the most gain

---

## Variance Reduction

- For regression trees
- Variance of y in the node
- Pick split that reduces it most

---

## Stopping Criteria

- Max depth
- Min samples per leaf
- Min samples to split
- Min impurity decrease

---

## Pruning

- Grow full, then trim
- Cost-complexity pruning
- Trade depth for generalisation
- Reduces overfitting

---

## Decision Tree in sklearn

```python
from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier(max_depth=5)
clf.fit(X_train, y_train)
```

---

## Tree Strengths

- Interpretable
- No scaling needed
- Handles mixed types
- Captures interactions

---

## Tree Weaknesses

- High variance
- Overfits easily
- Greedy: may miss global optimum
- Linear relationships waste of structure

---

## Why Ensemble Trees

- A single tree is unstable
- Average many to reduce variance
- Different sources of diversity
- The default for tabular

---

## Bagging

- Bootstrap aggregating
- Train each model on a sample
- Average their predictions
- Reduces variance

---

## Bootstrap Sampling

- Sample with replacement
- Same size as original
- About 63% unique rows
- The rest are out-of-bag

---

## Out-Of-Bag Score

- Predict each row from trees that didn't see it
- Free validation estimate
- No CV needed

---

## Random Forest

- Bagging + random feature subsets
- Decorrelates trees
- Strong default
- Few knobs to tune

---

## Why Random Features

- Trees pick the best split
- Without randomness, all trees pick similarly
- Random subsets force diversity
- Lower variance

---

## RF Hyperparameters

- n_estimators: more is better, slower
- max_features: per-split sample
- max_depth: cap to control overfit
- min_samples_leaf: smoothness

---

## Random Forest in sklearn

```python
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators=500, n_jobs=-1)
clf.fit(X_train, y_train)
```

---

## RF Strengths

- Robust default
- Little tuning
- Handles many features
- Works on small data

---

## RF Weaknesses

- Bigger model, slower predict
- Less interpretable than one tree
- Often beaten by boosting on tabular

---

## Extra Trees

- Even more randomness
- Random splits, not best splits
- Faster, sometimes better
- Same API

---

## Boosting

- Sequential, each model fixes the previous
- Reduces bias
- Different from bagging
- Currently top of the leaderboard for tabular

---

## AdaBoost

- Reweight misclassified examples
- Train next weak learner on weighted data
- Combine with weights
- Original boosting algorithm

---

## Gradient Boosting

- Each tree fits the residual
- Generalises AdaBoost to any loss
- Loss-function flexibility
- Foundation of modern boosters

---

## Gradient Boosting in sklearn

```python
from sklearn.ensemble import GradientBoostingClassifier
clf = GradientBoostingClassifier(n_estimators=200, learning_rate=0.05)
clf.fit(X_train, y_train)
```

---

## Learning Rate

- Shrinks each tree's contribution
- Lower learning rate, more trees
- Lower learning rate generalises better
- Trade time for accuracy

---

## Subsampling

- Train each tree on a fraction
- Reduces variance
- Speeds training
- Stochastic gradient boosting

---

## XGBoost

- Optimised gradient boosting
- Regularised
- Sparse-aware
- Won countless competitions

---

## LightGBM

- Histogram-based splits
- Leaf-wise growth
- Very fast on big data
- Best for many real datasets

---

## CatBoost

- Strong with categorical features natively
- Ordered boosting reduces leakage
- Good defaults
- Competes with the others

---

## XGBoost Example

```python
from xgboost import XGBClassifier
clf = XGBClassifier(n_estimators=500, learning_rate=0.05)
clf.fit(X_train, y_train)
```

---

## LightGBM Example

```python
import lightgbm as lgb
model = lgb.LGBMClassifier(n_estimators=500, learning_rate=0.05)
model.fit(X_train, y_train)
```

---

## CatBoost Example

```python
from catboost import CatBoostClassifier
clf = CatBoostClassifier(iterations=500, verbose=0)
clf.fit(X_train, y_train, cat_features=cat_cols)
```

---

## Boosting Strengths

- Best on tabular data
- Handles missing values natively
- Captures complex interactions
- Calibrated probabilities

---

## Boosting Weaknesses

- More tuning than RF
- Easy to overfit
- Slower to train
- Less interpretable

---

## Tuning Boosting

- learning_rate
- n_estimators (with early stopping)
- max_depth or num_leaves
- subsample, colsample
- reg_alpha, reg_lambda

---

## Early Stopping

- Stop adding trees when validation stops improving
- Prevents overfitting
- Big speedup
- Use a held-out set

---

## Feature Importance

- Tree models give it free
- Counts of splits
- Gain from splits
- Use cautiously

---

## Permutation Importance

- Shuffle a column, see metric drop
- Model-agnostic
- More reliable than tree gain
- Available in sklearn

---

## SHAP Values

- Per-prediction attributions
- Game-theoretic foundation
- Best practice for explanations
- shap library

---

## Categorical Features

- One-hot for trees works but explodes
- Target / frequency encoding
- CatBoost handles natively
- LightGBM has built-in support

---

## Missing Values

- XGBoost and LightGBM handle natively
- Decide direction at each split
- No imputation needed
- Big practical win

---

## Ensembling Across Algorithms

- Average RF, boosting, linear
- Stacking: meta-model on predictions
- Blending: weighted average
- Often improves Kaggle leaderboards

---

## Stacking

```python
from sklearn.ensemble import StackingClassifier
estimators = [
    ("rf", RandomForestClassifier()),
    ("xgb", XGBClassifier()),
]
stack = StackingClassifier(estimators=estimators, final_estimator=LogisticRegression())
```

---

## Tree-Based Choice

- Small data: random forest
- Tabular competition: gradient boosting
- Categorical heavy: CatBoost
- Big data: LightGBM

---

## Pitfalls

- Overfitting deep boosting models
- Ignoring early stopping
- Interpreting feature importance naively
- One-hot encoding huge cardinality

---

## Common Mistakes

- Choosing deep trees with little data
- Treating tree predictions as probabilities without calibration
- Not using early stopping in boosting
- Ignoring categorical handling

---

## Tree Split

![tree_split](svg/courses/machine_learning/machine-learning/09_trees_and_forests/tree_split.svg)

---

## Gini vs Entropy

![gini_vs_entropy](svg/courses/machine_learning/machine-learning/09_trees_and_forests/gini_vs_entropy.svg)

---

## Bagging vs Boosting

![bagging_vs_boosting](svg/courses/machine_learning/machine-learning/09_trees_and_forests/bagging_vs_boosting.svg)

---

## Random Forest Ensemble

![random_forest_ensemble](svg/courses/machine_learning/machine-learning/09_trees_and_forests/random_forest_ensemble.svg)

---

## Gradient Boosting Sequence

![gradient_boosting_sequence](svg/courses/machine_learning/machine-learning/09_trees_and_forests/gradient_boosting_sequence.svg)

---

## XGBoost / LightGBM / CatBoost

![xgb_lgb_cat](svg/courses/machine_learning/machine-learning/09_trees_and_forests/xgb_lgb_cat.svg)

---

## Feature Importance

![feature_importance](svg/courses/machine_learning/machine-learning/09_trees_and_forests/feature_importance.svg)

---

## Early Stopping

![early_stopping](svg/courses/machine_learning/machine-learning/09_trees_and_forests/early_stopping.svg)

---

## Information Gain

![information_gain](svg/courses/machine_learning/machine-learning/09_trees_and_forests/information_gain.svg)

---

## Learning Rate

![learning_rate](svg/courses/machine_learning/machine-learning/09_trees_and_forests/learning_rate.svg)

---

## Out-of-Bag Score

![oob_score](svg/courses/machine_learning/machine-learning/09_trees_and_forests/oob_score.svg)

---

## Summary

- One tree: interpretable but unstable
- Random forest: solid default
- Gradient boosting: top tabular performance
- Tune learning rate and depth, use early stopping
