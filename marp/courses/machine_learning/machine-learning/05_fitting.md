---
tags:
  - data-and-ai:machine-learning
level: intermediate
category: machine-learning
audience:
  - audiences:data-scientists

---

# Overfitting and Underfitting

---

## What This Chapter Covers

- The two failure modes
- Bias-variance decomposition
- Causes and detection
- Mitigations
- Learning curves
- Regularisation in depth

---

## The Goal

- A model that generalises
- Performs well on unseen data
- Not just on the training set
- Generalisation gap is what we fight

---

## Underfitting

- Model too simple to capture the pattern
- High bias
- Bad on training and bad on test
- Increase capacity

---

## Overfitting

- Model captured noise, not signal
- High variance
- Great on training, bad on test
- Reduce capacity or add data

---

## Just Right

- Captures real pattern
- Ignores noise
- Train and test close
- Sweet spot

---

## Visualising the Three

![overfit_underfit](svg/courses/machine_learning/machine-learning/05_fitting/overfit_underfit.svg)

---

## Bias-Variance Decomposition

- Expected error = bias squared + variance + noise
- Bias: systematic error from oversimplification
- Variance: error from sensitivity to training data
- Noise: irreducible

---

## Bias

- Model can't represent the truth
- Linear model on a curve
- Reduce by: more capacity, better features

---

## Variance

- Model overreacts to training data
- Different sample, very different model
- Reduce by: more data, regularisation, ensembling

---

## Noise

- Inherent randomness
- Cannot be reduced by modelling
- Sometimes mislabelled as overfitting

---

## How To Detect Underfitting

- Training loss high
- Test loss high
- Both move together
- Plot learning curves

---

## How To Detect Overfitting

- Training loss low
- Test loss much higher
- Gap opens with more training
- Cross-validation reveals it

---

## Learning Curves

- Plot loss vs training size
- Underfit: both curves high, close
- Overfit: training low, test high, big gap
- Just right: both low and close

---

## Learning Curves Plot

![learning_curves](svg/courses/machine_learning/machine-learning/05_fitting/learning_curves.svg)

---

## Validation Curves

- Plot loss vs hyperparameter
- Sweep one knob
- Identify the sweet spot
- Catches over- and under-fitting

---

## Causes Of Overfitting

- Too many parameters
- Too few examples
- Noise in labels
- Irrelevant features
- Training too long

---

## Causes Of Underfitting

- Model too simple
- Too few features
- Wrong feature representation
- Too much regularisation
- Training stopped too early

---

## Mitigations Overview

- More data
- Regularisation
- Cross-validation
- Early stopping
- Ensembling
- Feature engineering

---

## More Data

- The most reliable cure for overfitting
- Hard to get
- Cleaning matters
- Augmentation in vision, NLP

---

## Augmentation

- Generate new training examples
- Vision: rotate, flip, crop
- NLP: paraphrase, back-translate
- Tabular: SMOTE for minority class

---

## Regularisation

- Penalise complexity in the loss
- Smaller weights
- Sparser models
- Trades fit for generalisation

---

## L2 Regularisation

- Loss + lambda * sum(weights squared)
- Shrinks all weights toward zero
- Smooth, differentiable
- Default in many models

---

## L1 Regularisation

- Loss + lambda * sum(|weights|)
- Drives some weights to exactly zero
- Feature selection
- Lasso

---

## Elastic Net

- Mix of L1 and L2
- Sparsity plus stability
- Two hyperparameters
- Often best of both

---

## Regularisation Strength

- Too low: overfits anyway
- Too high: underfits
- Sweep with cross-validation
- Plot validation curve

---

## Early Stopping

- Train until validation stops improving
- Cheap and effective
- Standard in neural nets
- Form of regularisation

---

## Dropout

- Randomly zero units during training
- Forces redundancy
- Strong regularisation in neural nets
- No effect at inference

---

## Weight Decay

- L2 by another name
- Standard in deep learning optimisers
- Independent of learning rate

---

## Cross-Validation

- Honest estimate of generalisation
- k-fold rotates train/validation
- Reduces variance of the estimate
- Use it for selection

---

## Train, Validate, Test

- Train: fit weights
- Validate: pick model and hyperparameters
- Test: final estimate, never tuned on
- Three sets, three roles

---

## Test Set Discipline

- Never look until you're done
- Multiple peeks = overfitting to test
- One number, then stop
- Or fresh holdouts

---

## Ensembling

- Combine many models
- Bagging reduces variance
- Boosting reduces bias
- Stacking does both

---

## Capacity Control

- Tree depth
- Number of neurons
- Polynomial degree
- Number of features

---

## Polynomial Example

- Degree 1: probably underfits
- Degree 20: probably overfits
- Degree 3-5: usually fine
- Validation curve picks

---

## Curse Of Dimensionality

- Many features, few samples
- Distances become meaningless
- Models overfit easily
- Reduce or regularise

---

## Feature Selection

- Drop irrelevant features
- Reduces overfitting
- Improves interpretability
- Methods: filter, wrapper, embedded

---

## Noisy Labels

- Looks like overfitting
- Actually limits achievable accuracy
- Robust losses, label smoothing
- Better labelling helps more

---

## Diagnosis Flow

- Train loss high → underfit
- Train low, test high → overfit
- Both low → done
- Match diagnosis to fix

---

## sklearn Validation Curve

```python
from sklearn.model_selection import validation_curve
train_scores, test_scores = validation_curve(
    model, X, y, param_name="alpha",
    param_range=alphas, cv=5
)
```

---

## sklearn Learning Curve

```python
from sklearn.model_selection import learning_curve
sizes, train, test = learning_curve(
    model, X, y, train_sizes=np.linspace(0.1, 1.0, 5)
)
```

---

## Common Mistakes

- Picking model on test set
- Not splitting before scaling
- Training too long without early stopping
- Ignoring class imbalance in CV folds

---

## Bias-Variance Dartboard

![bias_variance_dartboard](svg/courses/machine_learning/machine-learning/05_fitting/bias_variance_dartboard.svg)

---

## Regularisation Path

![regularization_path](svg/courses/machine_learning/machine-learning/05_fitting/regularization_path.svg)

---

## Dropout

![dropout](svg/courses/machine_learning/machine-learning/05_fitting/dropout.svg)

---

## Polynomial Capacity

![polynomial_capacity](svg/courses/machine_learning/machine-learning/05_fitting/polynomial_capacity.svg)

---

## Noise Decomposition

![noise_decomposition](svg/courses/machine_learning/machine-learning/05_fitting/noise_decomposition.svg)

---

## Curse of Dimensionality

![curse_of_dimensionality](svg/courses/machine_learning/machine-learning/05_fitting/curse_of_dimensionality.svg)

---

## Summary

- Underfit and overfit are the two failure modes
- Bias-variance is the lens
- Diagnose with curves, fix with regularisation, data, ensembling
- Test set is sacred
