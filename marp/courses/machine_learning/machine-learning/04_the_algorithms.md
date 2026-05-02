---
tags:
  - data-and-ai:machine-learning
level: intermediate
category: machine-learning
audience:
  - audiences:data-scientists

---
# The Algorithms

---
## What This Chapter Covers

- Linear models
- Trees and forests
- Boosting
- SVMs
- Neural networks
- Clustering

---
## The Landscape

![algorithm_landscape](svg/courses/machine_learning/machine-learning/04_the_algorithms/algo_landscape.svg)

---
## Linear Regression

- Predict continuous y from linear combination of X
- Loss: squared error
- Closed-form or gradient descent
- Baseline for regression

---
## Logistic Regression

- Despite the name: classification
- Linear combination through sigmoid
- Output: probability
- Baseline for classification

---
## Regularisation

- L1 (Lasso): sparsity, feature selection
- L2 (Ridge): shrinks all coefficients
- Elastic Net: combines both
- Control overfitting

---
## Decision Trees

- Split data on features
- Greedy: maximise information gain
- Interpretable
- Prone to overfitting

---
## Random Forests

- Ensemble of trees
- Bagging: bootstrap samples
- Random feature subsets
- Robust, low tuning, good baseline

---
## Gradient Boosting

- Sequential trees correcting errors
- XGBoost, LightGBM, CatBoost
- Best for tabular data
- More tuning than RF

---
## Support Vector Machines

- Find max-margin hyperplane
- Kernel trick: nonlinear via mapping
- Memory hungry on big data
- Once dominant, less so now

---
## k-Nearest Neighbours

- Predict from k closest training points
- No training; lazy
- Distance-sensitive: scale features
- Slow at inference for big data

---
## Naive Bayes

- Bayes' theorem with feature independence
- Fast, simple
- Strong on text
- Surprisingly effective baseline

---
## Neural Networks

- Layers of units with non-linearities
- Train via backpropagation
- Universal approximators
- Need lots of data

---
## Deep Learning

- Many layers, automatic features
- CNNs: vision
- RNNs / Transformers: sequences
- State of the art on unstructured data

---
## k-Means Clustering

- Partition into k clusters
- Iterative: assign, update centroids
- Need to choose k
- Sensitive to initialisation

---
## Hierarchical Clustering

- Nested clusters
- Agglomerative or divisive
- Dendrogram visualisation
- O(n squared) memory

---
## PCA

- Project to lower dimensions
- Maximise variance
- Useful for: visualisation, denoising, speedup
- Linear

---
## Picking An Algorithm

- Tabular data: gradient boosting
- Vision: CNNs
- Text: Transformers
- Small data: simpler models
- Try multiple

---
## Common Algorithm Mistakes

- Defaulting to deep learning for tabular
- Not scaling features for distance models
- Choosing k arbitrarily for k-means
- Treating tree predictions as probabilities
- Ignoring computational cost at inference
