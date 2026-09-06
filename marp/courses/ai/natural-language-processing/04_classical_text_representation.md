---
tags:
  - data-and-ai:nlp
  - concepts:bag-of-words
  - concepts:tf-idf
  - concepts:n-grams
  - concepts:topic-modeling
level: advanced
category: ai
audience:
  - audiences:developers
  - audiences:data-scientists

---

# Classical Text Representation

---

## What This Chapter Covers

- Bag-of-words and the document-term matrix
- N-gram features and the explosion they cause
- Term weighting from raw counts to `TF-IDF` and `BM25`
- Latent semantic analysis and topic modeling
- The distributional hypothesis and co-occurrence vectors

---

## Why Classical Methods Still Matter

- Many production pipelines still run on `TF-IDF` and friends
- Strong baselines that often beat fancier models on small data
- The vocabulary they expose is a transparent debugging surface
- Understanding them is the only way to read the embeddings literature
- Cheap to train, cheap to serve, easy to inspect

---

## From Tokens to Vectors

- Tokenization gives a stream of discrete tokens
- Models operate on numeric vectors, not strings
- Classical representations build a fixed-dimensional vector per document
- Each dimension corresponds to a word, an n-gram, or a latent topic
- The choice of representation shapes everything downstream

---

## Bag-of-Words: The Core Idea

- Treat a document as an unordered multiset of tokens
- Discard word order entirely
- Count how often each vocabulary term appears
- The resulting vector lives in a space whose dimension equals the vocabulary size
- Surprisingly effective for many classification and retrieval tasks

---

## The Document-Term Matrix

![document_term_matrix](svg/courses/ai/natural-language-processing/04_classical_text_representation/document_term_matrix.svg)

---

## Vocabulary Construction

- Scan the corpus and collect distinct tokens
- Apply minimum and maximum document frequency cutoffs
- Cap the vocabulary at a fixed size — keep the most frequent terms
- Reserve indices for unknown and padding tokens
- The vocabulary is part of the model — version it with the weights

---

## Sparse Storage

- Vocabularies have tens to hundreds of thousands of terms
- A single document touches a tiny fraction of them
- Dense storage wastes memory; almost all entries are zero
- Use compressed sparse row (`CSR`) or column (`CSC`) formats
- `scipy.sparse` and `sklearn` use sparse matrices throughout

---

## Bag-of-Words Code

```python
from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(
    min_df=2,
    max_df=0.95,
    max_features=50000,
)
X = vectorizer.fit_transform(documents)
# X is a sparse (n_documents, vocab_size) matrix
```

- `min_df` removes rare typos and noise
- `max_df` removes overly common terms close to stop words
- `max_features` caps the dimensionality

---

## What Bag-of-Words Loses

- Word order: `dog bites man` and `man bites dog` map to the same vector
- Negation: `not good` collapses into separate `not` and `good` counts
- Compositional meaning: idioms become bags of unrelated tokens
- Long-range structure: nothing connects words across a paragraph
- And yet: enough signal remains to classify topics, sentiment, language

---

## N-Gram Features

- Capture local order by counting contiguous token sequences
- Unigrams: single tokens (`bag`, `of`, `words`)
- Bigrams: pairs (`bag of`, `of words`)
- Trigrams: triples (`bag of words`)
- Higher orders are possible but rapidly impractical

---

## Why N-Grams Help

- `not good` becomes its own feature, distinct from `good`
- Domain phrases (`machine learning`, `New York`) are preserved as units
- Local syntactic patterns become observable
- A simple linear classifier on n-grams handles a surprising amount of structure
- Often combined: unigrams plus bigrams as a single feature space

---

## Skip-Grams

- Allow gaps between the tokens that form the n-gram
- `the quick brown fox` yields skip-bigrams like `quick fox` (skip 1)
- Captures longer-range associations without exploding to full n-grams
- Useful when relevant relationships span function words
- Will reappear in `word2vec` as a training objective rather than a feature

---

## The Feature Explosion

![feature_explosion](svg/courses/ai/natural-language-processing/04_classical_text_representation/feature_explosion.svg)

---

## Feature Selection

- Filter by document frequency: drop terms seen in too few or too many documents
- Score by mutual information with the target label
- Use chi-squared tests to keep terms that distinguish classes
- L1-regularized linear models prune features as part of training
- Better features beat more features for classical methods

---

## Term Weighting: Raw Counts

- The simplest weighting: cell value equals the count
- Long documents dominate by sheer volume
- Frequent function words drown out informative terms
- Works for some tasks but is rarely optimal
- Forms the baseline against which other weightings are measured

---

## Binary Weighting

- Cell is 1 if the term appears, 0 otherwise
- Ignores how often a term repeats inside a document
- Robust when raw counts are noisy or document lengths vary widely
- The default for some Naive Bayes variants
- A useful sanity check before reaching for `TF-IDF`

---

## Term Frequency Variants

- Raw count: `tf = count`
- Normalized: `tf = count / document_length`
- Log-scaled: `tf = 1 + log(count)` — a single mention is informative, the tenth is not
- Augmented: `tf = 0.5 + 0.5 * count / max_count`
- Sublinear scaling tames the influence of repeated terms

---

## Inverse Document Frequency

- A term that appears in every document carries no discriminative signal
- A term that appears in few documents is probably specific
- `idf(t) = log(N / df(t))` — high for rare terms, low for common ones
- Smoothed variant: `log((1 + N) / (1 + df(t))) + 1` to avoid divide-by-zero
- Combines with `tf` multiplicatively: `tfidf = tf * idf`

---

## TF-IDF Derivation

```python
import numpy as np

def tfidf(tf_matrix):
    n_docs = tf_matrix.shape[0]
    df = (tf_matrix > 0).sum(axis=0)
    idf = np.log((1 + n_docs) / (1 + df)) + 1
    tfidf = tf_matrix.multiply(idf)
    return normalize(tfidf, norm="l2", axis=1)
```

- L2 normalization makes cosine similarity equivalent to dot product
- Sklearn's `TfidfVectorizer` rolls all of this into one call

---

## TF-IDF Intuition

- Up-weight terms that are frequent in this document but rare across the corpus
- Down-weight terms that are common everywhere
- The result: a sparse vector emphasizing each document's distinctive vocabulary
- Cosine similarity over `TF-IDF` vectors is a strong retrieval baseline
- Decades of `IR` systems rely on this exact recipe

---

## Sublinear Scaling

- Raw `tf` over-rewards repetition: ten mentions are not ten times more informative
- `1 + log(tf)` flattens the influence of repeated terms
- Pairs naturally with `IDF` to give well-behaved scores
- Used by default in many modern `IR` toolkits
- A small change with measurable retrieval quality gains

---

## BM25 and Probabilistic Weighting

- `BM25` extends `TF-IDF` with explicit term saturation and length normalization
- Saturation: marginal value of repetitions diminishes with a tunable `k1`
- Length: longer documents are penalized via a `b` parameter
- Derived from probabilistic retrieval models, not just heuristics
- Still the default ranking function in `Elasticsearch` and `Lucene`

---

## BM25 Formula

```python
def bm25(tf, idf, doc_len, avg_len, k1=1.5, b=0.75):
    norm = 1 - b + b * (doc_len / avg_len)
    saturation = (k1 + 1) * tf / (k1 * norm + tf)
    return idf * saturation
```

- `k1` controls how quickly the score saturates with term frequency
- `b` controls how much document length matters
- Tuning matters less than people think — defaults are robust

---

## Why BM25 Beats Plain TF-IDF

- Saturates the contribution of any single term — no single word can dominate
- Penalizes very long documents that would otherwise rack up matches
- Has a probabilistic justification, not just an empirical recipe
- Produces a single scalar score per document — easy to rank
- Modern hybrid retrieval blends `BM25` with dense embeddings

---

## Weighting Schemes Compared

![weighting_schemes](svg/courses/ai/natural-language-processing/04_classical_text_representation/weighting_schemes.svg)

---

## The Curse of High Dimensions

- Vocabularies of 100k+ make distance metrics behave badly
- Sparse vectors dodge most issues — distances live on the support
- But correlations between related terms are still ignored
- `synonyms` like `car` and `automobile` end up orthogonal
- Latent representations address exactly this problem

---

## Latent Semantic Analysis

- Apply truncated `SVD` to the document-term matrix
- Decompose `X` into `U Sigma V^T` with rank `k` much smaller than vocabulary
- Documents and terms project into the same `k`-dimensional latent space
- Synonyms cluster; unrelated words separate
- A linear, deterministic precursor to neural embeddings

---

## LSA via SVD

```python
from sklearn.decomposition import TruncatedSVD

svd = TruncatedSVD(n_components=300)
doc_topics = svd.fit_transform(tfidf_matrix)
# each document now has a 300-dimensional dense representation
```

- Typical `k`: 100 to 500 components
- Run on a `TF-IDF` matrix, not raw counts
- Cosine similarity in the latent space captures semantic closeness

---

## Latent Dirichlet Allocation

- Generative probabilistic model: documents are mixtures of topics
- Each topic is a distribution over words
- Each document is a distribution over topics
- Inference recovers the latent topics from observed word counts
- More interpretable than `SVD` but slower and harder to tune

---

## Topic Modeling as Dimensionality Reduction

![topic_modeling](svg/courses/ai/natural-language-processing/04_classical_text_representation/topic_modeling.svg)

---

## When to Use Topic Models

- Exploratory analysis of large corpora
- Soft clustering when documents straddle multiple themes
- Feature engineering when downstream models need lower-dimensional input
- Trend tracking: how topic mixtures shift over time
- Less useful as a direct classifier — `TF-IDF` plus linear is usually stronger

---

## The Distributional Hypothesis

- Firth, 1957: "you shall know a word by the company it keeps"
- Words that appear in similar contexts tend to mean similar things
- A word's representation can be derived from its co-occurrences
- The foundation under everything from `LSA` to `word2vec` to modern `LLMs`
- Counts in, vectors out — the recipe is older than it looks

---

## Co-occurrence Matrices

- Slide a context window over the corpus
- For each target word, count which words appear nearby
- Result: a symmetric matrix indexed by vocabulary on both axes
- Each row is a word's distributional fingerprint
- Cosine similarity over rows captures semantic similarity surprisingly well

---

## Pointwise Mutual Information

- Raw co-occurrence counts favor frequent words
- `PMI(a, b) = log(P(a, b) / (P(a) * P(b)))`
- Positive when words co-occur more than chance, negative otherwise
- Negative `PMI` is unreliable; people use `PPMI = max(PMI, 0)`
- A simple `PPMI` matrix already contains much of what neural embeddings learn

---

## From Counts to Vectors

- Start with a sparse co-occurrence or `PPMI` matrix
- Apply truncated `SVD` to compress it to a few hundred dimensions
- The resulting word vectors capture analogical structure
- Levy and Goldberg, 2014: `word2vec` is approximately `SVD` on a shifted `PPMI` matrix
- The classical and neural approaches are not as different as they appear

---

## Practical Pipeline

- Tokenize and normalize as in the previous chapter
- Build a vocabulary with sensible frequency cutoffs
- Choose a weighting scheme: `TF-IDF` for retrieval, raw or binary for some classifiers
- Pick a dimensionality reduction if the downstream model needs dense inputs
- Cache the fitted vectorizer — it is part of the model

---

## Anti-Patterns

- Refitting the vectorizer at inference instead of loading the trained one
- Using raw counts when document lengths vary by orders of magnitude
- Treating `LDA` topics as ground truth labels rather than soft features
- Ignoring n-gram order: `not good` and `good` should not be the same vector
- Skipping `IDF` because "the model will figure it out"

---

## When Classical Methods Are Still Right

- Small corpora where neural models overfit
- Latency or cost budgets that rule out transformers
- Highly interpretable systems where every dimension must be explainable
- Strong baselines for any new neural approach
- Hybrid retrieval: `BM25` plus dense embeddings beats either alone

---

## Summary

- Bag-of-words remains a transparent and powerful representation
- N-grams recover local order; feature selection keeps them tractable
- `TF-IDF` and `BM25` weight terms by their discriminative power
- `LSA` and `LDA` compress sparse counts into latent semantic spaces
- The distributional hypothesis ties classical and neural methods together
- Always run a `TF-IDF` plus linear baseline before reaching for anything fancier
