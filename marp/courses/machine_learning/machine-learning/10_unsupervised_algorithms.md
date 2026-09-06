---
tags:
  - data-and-ai:machine-learning
level: intermediate
category: machine-learning
audience:
  - audiences:data-scientists

---

# Unsupervised Algorithms

---

## What This Chapter Covers

- Clustering
- k-Means
- Hierarchical
- DBSCAN
- Gaussian mixtures
- Association rules
- Dimensionality reduction
- Anomaly detection

---

## What Unsupervised Means

- No labels
- Find structure
- Group, compress, summarise
- Often for exploration

---

## When To Use

- Customer segmentation
- Topic discovery
- Anomaly detection
- Dimensionality reduction
- Pre-processing for supervised

---

## Clustering Goals

- Group similar points
- Separate dissimilar ones
- "Similar" is the modeller's choice
- Distance metric matters

---

## Distance Metrics

- Euclidean
- Manhattan
- Cosine
- Mahalanobis
- Domain-specific

---

## k-Means

- Partition into k clusters
- Iterative: assign, update centroids
- Need to choose k
- Sensitive to initialisation

---

## k-Means Algorithm

- Pick k random centroids
- Assign each point to nearest centroid
- Recompute centroids as means
- Repeat until stable

---

## k-Means Picture

![kmeans](svg/courses/machine_learning/machine-learning/10_unsupervised_algorithms/kmeans.svg)

---

## k-Means in sklearn

```python
from sklearn.cluster import KMeans
km = KMeans(n_clusters=5, n_init=10, random_state=42)
km.fit(X)
labels = km.labels_
```

---

## Choosing k

- Elbow method: inertia vs k
- Silhouette score
- Domain knowledge
- Try a few values

---

## Elbow Method

- Plot within-cluster sum of squares
- Look for the bend
- Often ambiguous
- Combine with silhouette

---

## Silhouette Score

- Per-point: how well it fits its cluster vs others
- Range -1 to 1
- Higher is better
- Average for cluster quality

---

## k-Means Strengths

- Fast, scales well
- Simple
- Good for spherical clusters

---

## k-Means Weaknesses

- Need k
- Assumes spherical, equal-size
- Sensitive to outliers
- Local optima

---

## k-Means++

- Smart initialisation
- Spread centroids out
- Default in sklearn
- Faster convergence

---

## Mini-Batch k-Means

- Update on small batches
- Big speedup for huge data
- Slightly worse clusters
- Production-friendly

---

## Hierarchical Clustering

- Nested clusters
- Agglomerative: bottom-up
- Divisive: top-down
- Dendrogram visualisation

---

## Linkage Methods

- Single: closest pair
- Complete: farthest pair
- Average: mean distance
- Ward: minimise variance

---

## Dendrogram

- Tree of merges
- Cut at a height for clusters
- Visual exploration
- Doesn't scale to huge data

---

## Hierarchical in sklearn

```python
from sklearn.cluster import AgglomerativeClustering
hc = AgglomerativeClustering(n_clusters=5, linkage="ward")
labels = hc.fit_predict(X)
```

---

## Hierarchical Strengths

- No need to choose k upfront
- Dendrogram is informative
- Captures nested structure

---

## Hierarchical Weaknesses

- O(n squared) memory
- Slow on big data
- Greedy: bad merges stick

---

## DBSCAN

- Density-based clustering
- Find dense regions
- Outliers labelled noise
- No need for k

---

## DBSCAN Parameters

- eps: neighbourhood radius
- min_samples: density threshold
- Tune by domain
- Sensitive to scaling

---

## DBSCAN in sklearn

```python
from sklearn.cluster import DBSCAN
labels = DBSCAN(eps=0.5, min_samples=5).fit_predict(X)
```

---

## DBSCAN Strengths

- Arbitrary cluster shapes
- No k needed
- Built-in outlier detection

---

## DBSCAN Weaknesses

- Density assumption
- Bad for varying densities
- High dim: distances flatten

---

## HDBSCAN

- Hierarchical version of DBSCAN
- Handles varying density
- Less parameter sensitivity
- Strong default these days

---

## Gaussian Mixture Models

- Each cluster is a Gaussian
- Soft assignment: probability
- Fit with EM algorithm
- More flexible than k-means

---

## EM Algorithm

- E-step: compute responsibilities
- M-step: update parameters
- Iterate to convergence
- Local optima

---

## GMM in sklearn

```python
from sklearn.mixture import GaussianMixture
gmm = GaussianMixture(n_components=5)
gmm.fit(X)
probs = gmm.predict_proba(X)
```

---

## GMM Strengths

- Soft cluster assignment
- Elliptical clusters
- Probabilistic
- Good for density estimation

---

## GMM Weaknesses

- Assumes Gaussian
- Slower than k-means
- Number of components is a knob

---

## Cluster Evaluation Without Labels

- Silhouette
- Davies-Bouldin
- Calinski-Harabasz
- All have biases

---

## Cluster Evaluation With Labels

- Adjusted rand index
- Mutual information
- V-measure
- When ground truth available

---

## Association Rules

- Find frequent co-occurrences
- "Customers who bought X also bought Y"
- Apriori, FP-Growth
- Market basket analysis

---

## Apriori Concepts

- Support: how often items appear
- Confidence: P(B|A)
- Lift: confidence / P(B)
- Filter by minimums

---

## Association in mlxtend

```python
from mlxtend.frequent_patterns import apriori, association_rules
items = apriori(df, min_support=0.05, use_colnames=True)
rules = association_rules(items, metric="lift", min_threshold=1.0)
```

---

## Dimensionality Reduction

- Project to fewer dimensions
- Visualisation
- Speed
- Denoising

---

## PCA

- Project to lower dimensions
- Maximise variance
- Useful for: visualisation, denoising, speedup
- Linear

---

## PCA Math

- Eigenvectors of covariance matrix
- Top k components
- Cumulative explained variance
- Decide k by threshold

---

## PCA in sklearn

```python
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
X2 = pca.fit_transform(X)
```

---

## PCA Strengths

- Fast, deterministic
- Linear, well-understood
- Useful preprocessing

---

## PCA Weaknesses

- Linear only
- Components hard to interpret
- Sensitive to scale

---

## t-SNE

- Nonlinear, for visualisation
- Preserves local structure
- Slow on big data
- Stochastic

---

## UMAP

- Newer than t-SNE
- Faster, often better
- Preserves more global structure
- Default for high-dim viz

---

## Autoencoders

- Neural net compression
- Encoder + decoder
- Learn embeddings
- Used for anomaly detection too

---

## Anomaly Detection

- Find points unlike the rest
- Outliers, fraud, faults
- Often unsupervised

---

## Isolation Forest

- Random partitioning
- Anomalies isolated quickly
- Fast, scalable
- Good default

---

## One-Class SVM

- Boundary around normal data
- Anything outside is anomaly
- Slow on big data
- Kernel choice matters

---

## Local Outlier Factor

- Density-based outliers
- Compare local density to neighbours
- Catches local anomalies

---

## Anomaly in sklearn

```python
from sklearn.ensemble import IsolationForest
iso = IsolationForest(contamination=0.01)
preds = iso.fit_predict(X)
```

---

## Common Unsupervised Mistakes

- Choosing k arbitrarily
- Not scaling features
- Believing every cluster is real
- Confusing exploration with conclusions

---

## Dendrogram

![dendrogram](svg/courses/machine_learning/machine-learning/10_unsupervised_algorithms/dendrogram.svg)

---

## DBSCAN

![dbscan](svg/courses/machine_learning/machine-learning/10_unsupervised_algorithms/dbscan.svg)

---

## Gaussian Mixtures

![gmm](svg/courses/machine_learning/machine-learning/10_unsupervised_algorithms/gmm.svg)

---

## PCA

![pca](svg/courses/machine_learning/machine-learning/10_unsupervised_algorithms/pca.svg)

---

## t-SNE vs UMAP

![tsne_vs_umap](svg/courses/machine_learning/machine-learning/10_unsupervised_algorithms/tsne_vs_umap.svg)

---

## Association Rules

![association_rules](svg/courses/machine_learning/machine-learning/10_unsupervised_algorithms/association_rules.svg)

---

## Isolation Forest

![isolation_forest](svg/courses/machine_learning/machine-learning/10_unsupervised_algorithms/isolation_forest.svg)

---

## Anomaly Types

![anomaly_types](svg/courses/machine_learning/machine-learning/10_unsupervised_algorithms/anomaly_types.svg)

---

## Elbow Method

![elbow_method](svg/courses/machine_learning/machine-learning/10_unsupervised_algorithms/elbow_method.svg)

---

## Silhouette

![silhouette](svg/courses/machine_learning/machine-learning/10_unsupervised_algorithms/silhouette.svg)

---

## EM Algorithm

![em_algorithm](svg/courses/machine_learning/machine-learning/10_unsupervised_algorithms/em_algorithm.svg)

---

## Vector Distance

![vector_distance](svg/courses/machine_learning/machine-learning/10_unsupervised_algorithms/vector_distance.svg)

---

## Summary

- Clustering, association, dimensionality reduction, anomaly
- k-means is the workhorse
- DBSCAN/HDBSCAN handle shape
- PCA + UMAP for visualisation
- Validate with multiple metrics
