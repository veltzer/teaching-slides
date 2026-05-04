---
tags:
  - data-and-ai:machine-learning
level: intermediate
category: machine-learning
audience:
  - audiences:data-scientists

---
# Supervised Algorithms

---
## What This Chapter Covers

- Linear regression
- Logistic regression
- k-Nearest Neighbours
- Naive Bayes
- Linear Discriminant Analysis
- Support Vector Machines
- Stochastic Gradient Descent
- Picking among them

---
## The Landscape

![algorithm_landscape](svg/courses/machine_learning/machine-learning/08_supervised_algorithms/algo_landscape.svg)

---
## Picking An Algorithm

![algorithm_choice](svg/courses/machine_learning/machine-learning/08_supervised_algorithms/algo_choice.svg)

---
## Linear Regression

- Predict continuous y from linear combination of X
- Loss: squared error
- Closed-form or gradient descent
- Baseline for regression

---
## Linear Regression Math

- y = w · x + b
- Minimise sum (y - y_hat) squared
- Closed form: w = (X^T X)^-1 X^T y
- Or solve with gradient descent

---
## Linear Regression Assumptions

- Linearity in inputs
- Independent errors
- Constant variance
- Normal residuals (for inference)

---
## Linear Regression in sklearn

```python
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)
preds = model.predict(X_test)
```

---
## Linear Regression Strengths

- Interpretable
- Fast to train and predict
- Strong baseline
- Easy to deploy

---
## Linear Regression Weaknesses

- Misses nonlinearity
- Sensitive to outliers
- Assumes additive features
- Multicollinearity issues

---
## Logistic Regression

- Despite the name: classification
- Linear combination through sigmoid
- Output: probability
- Baseline for classification

---
## Logistic Regression Math

- p = sigmoid(w · x + b)
- Loss: log loss / cross-entropy
- No closed form
- Solve with SGD or quasi-Newton

---
## Logistic Regression in sklearn

```python
from sklearn.linear_model import LogisticRegression
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)
clf.predict_proba(X_test)
```

---
## Multinomial Logistic

- Softmax instead of sigmoid
- Multi-class
- Default in sklearn for >2 classes

---
## Logistic Regression Strengths

- Calibrated probabilities
- Interpretable coefficients
- Cheap, scalable
- Fast inference

---
## Regularisation

- L1 (Lasso): sparsity, feature selection
- L2 (Ridge): shrinks all coefficients
- Elastic Net: combines both
- Control overfitting

---
## Ridge

- Linear regression + L2
- Smooth, all features kept small
- Closed form
- Default for linear

---
## Lasso

- Linear regression + L1
- Sparse coefficients
- Feature selection
- Coordinate descent

---
## ElasticNet

- L1 + L2 mix
- Sparse but stable
- Two hyperparameters
- Often the best linear baseline

---
## k-Nearest Neighbours

- Predict from k closest training points
- No training; lazy
- Distance-sensitive: scale features
- Slow at inference for big data

---
## kNN Math

- Distance metric: Euclidean, cosine, Manhattan
- Vote (classification) or average (regression)
- k controls smoothness

---
## Choosing k

- Small k: low bias, high variance
- Large k: high bias, low variance
- Cross-validate
- Odd for binary classification

---
## kNN in sklearn

```python
from sklearn.neighbors import KNeighborsClassifier
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)
```

---
## kNN Strengths

- Simple
- Naturally handles multi-class
- No training step
- Good baseline for small data

---
## kNN Weaknesses

- Slow at inference
- Curse of dimensionality
- Needs scaling
- Memory hungry

---
## Naive Bayes

- Bayes' theorem with feature independence
- Fast, simple
- Strong on text
- Surprisingly effective baseline

---
## Naive Bayes Math

- P(y|x) ∝ P(y) Π P(x_i | y)
- Independence is the "naive" part
- Estimate from frequencies
- Closed form

---
## Variants

- Gaussian: continuous features
- Multinomial: counts (text)
- Bernoulli: binary features

---
## Naive Bayes in sklearn

```python
from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB()
clf.fit(X_train, y_train)
```

---
## Naive Bayes Strengths

- Trains on tiny data
- Very fast
- Calibrated probabilities (often)
- Robust to irrelevant features

---
## Naive Bayes Weaknesses

- Independence assumption violated
- Probabilities can be extreme
- Not for complex interactions

---
## Linear Discriminant Analysis

- Project to maximise class separation
- Assume Gaussian per class, equal covariance
- Closed form
- Both classifier and reducer

---
## LDA Math

- Within-class and between-class scatter
- Find directions that maximise ratio
- Projection then linear classifier

---
## LDA in sklearn

```python
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
lda = LinearDiscriminantAnalysis()
lda.fit(X_train, y_train)
```

---
## LDA Strengths

- Closed form, fast
- Works with small data
- Doubles as dimension reduction
- Stable

---
## LDA Weaknesses

- Gaussian assumption
- Equal covariance per class
- Sensitive to outliers

---
## QDA

- Quadratic Discriminant Analysis
- Per-class covariance
- More flexible than LDA
- More parameters, more data needed

---
## Support Vector Machines

- Find max-margin hyperplane
- Kernel trick: nonlinear via mapping
- Memory hungry on big data
- Once dominant, less so now

---
## SVM Math

- Maximise margin to nearest points
- Support vectors define the boundary
- Hinge loss
- Quadratic programming

---
## Soft Margin

- Allow some misclassifications
- Slack variables
- C controls tradeoff
- Tuning matters

---
## Kernel Trick

- Implicit mapping to higher space
- Compute dot products via kernel
- Linear, polynomial, RBF, sigmoid
- RBF is the default

---
## RBF Kernel

- exp(-gamma * ||x - x'||^2)
- Local similarity
- gamma controls smoothness
- Tune with C

---
## SVM in sklearn

```python
from sklearn.svm import SVC
clf = SVC(kernel="rbf", C=1.0, gamma="scale")
clf.fit(X_train, y_train)
```

---
## SVM for Regression

- SVR: epsilon-insensitive loss
- Same kernels apply
- Less common in practice

---
## SVM Strengths

- High accuracy with little tuning
- Effective in high dimensions
- Kernel flexibility
- Strong theory

---
## SVM Weaknesses

- Slow on big data
- Memory heavy
- No native probabilities
- Sensitive to scale

---
## Stochastic Gradient Descent

- Train any linear model on huge data
- One sample (or mini-batch) per update
- Online learning
- Foundation of deep learning too

---
## SGD Math

- w = w - eta * gradient(loss(sample))
- eta is the learning rate
- Noisy steps, average behaviour converges
- Many tricks: momentum, Adam

---
## SGD in sklearn

```python
from sklearn.linear_model import SGDClassifier
clf = SGDClassifier(loss="log_loss", alpha=1e-4)
clf.fit(X_train, y_train)
```

---
## SGD Loss Choices

- log_loss: logistic regression
- hinge: SVM
- squared_error: regression
- huber: robust regression

---
## SGD Strengths

- Scales to millions of samples
- Online and incremental
- Memory efficient
- Foundation of deep learning

---
## SGD Weaknesses

- Sensitive to learning rate
- Needs feature scaling
- Random ordering matters
- Tuning required

---
## Perceptron

- Original neural building block
- Linear classifier
- Updates on errors
- Historical, but instructive

---
## Linear Models Summary

- Logistic regression: solid baseline
- Ridge / Lasso / ElasticNet for regression
- SGD for big data
- Linear is always a fair starting point

---
## Distance Models Summary

- kNN: simple, slow at inference
- SVM: powerful, scaling-sensitive
- Both need scaled features

---
## Probabilistic Models Summary

- Naive Bayes: text and small data
- LDA: stable, low-data
- Logistic regression: calibrated, scalable

---
## Choosing An Algorithm

- Small tabular: logistic regression, NB
- Bigger tabular: try linear and trees
- Text: NB, logistic with TF-IDF
- High dim: linear with regularisation

---
## Multiple Models

```python
for clf in [LogisticRegression(), GaussianNB(), KNeighborsClassifier()]:
    clf.fit(X_train, y_train)
    print(clf.__class__.__name__, clf.score(X_test, y_test))
```

---
## Hyperparameter Tuning

- Grid search
- Random search
- Bayesian search
- Always with cross-validation

---
## GridSearchCV

```python
from sklearn.model_selection import GridSearchCV
params = {"C": [0.01, 0.1, 1, 10]}
gs = GridSearchCV(LogisticRegression(), params, cv=5)
gs.fit(X_train, y_train)
```

---
## RandomizedSearchCV

- Sample random configs
- Better than grid for many hyperparameters
- Cheaper, often as good

---
## Common Algorithm Mistakes

- Skipping the linear baseline
- Forgetting to scale for SVM, kNN
- Using SVM on millions of rows
- Overfitting kNN with k=1

---
## Linear Regression Fit

![linear_regression_fit](svg/courses/machine_learning/machine-learning/08_supervised_algorithms/linear_regression_fit.svg)

---
## Sigmoid Curve

![sigmoid_curve](svg/courses/machine_learning/machine-learning/08_supervised_algorithms/sigmoid_curve.svg)

---
## Regularisation

![regularization](svg/courses/machine_learning/machine-learning/08_supervised_algorithms/regularization.svg)

---
## kNN Neighbourhood

![knn_neighborhood](svg/courses/machine_learning/machine-learning/08_supervised_algorithms/knn_neighborhood.svg)

---
## Naive Bayes

![naive_bayes](svg/courses/machine_learning/machine-learning/08_supervised_algorithms/naive_bayes.svg)

---
## LDA Projection

![lda_projection](svg/courses/machine_learning/machine-learning/08_supervised_algorithms/lda_projection.svg)

---
## SVM Margin

![svm_margin](svg/courses/machine_learning/machine-learning/08_supervised_algorithms/svm_margin.svg)

---
## Kernel Trick

![kernel_trick](svg/courses/machine_learning/machine-learning/08_supervised_algorithms/kernel_trick.svg)

---
## SGD Steps

![sgd_steps](svg/courses/machine_learning/machine-learning/08_supervised_algorithms/sgd_steps.svg)

---
## Perceptron

![perceptron](svg/courses/machine_learning/machine-learning/08_supervised_algorithms/perceptron.svg)

---
## Grid vs Random Search

![grid_vs_random_search](svg/courses/machine_learning/machine-learning/08_supervised_algorithms/grid_vs_random_search.svg)

---
## Summary

- Linear models are strong baselines
- kNN is simple but slow at scale
- SVM is powerful but heavy
- SGD scales to anything
- Always start simple
