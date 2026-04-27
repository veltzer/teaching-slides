---
tags:
  - data-and-ai:nlp
  - concepts:embeddings
level: advanced
category: ai
audience:
  - audiences:developers
  - audiences:data-scientists

---
# Word Embeddings

---
## What This Chapter Covers

- From sparse counts to dense vectors and why that shift mattered
- `Word2Vec` — `CBOW`, skip-gram, negative sampling, hierarchical softmax
- `GloVe` — co-occurrence factorization and its loss
- `FastText` — subword embeddings and out-of-vocabulary handling
- Embedding properties — similarity, analogies, visualization, bias
- Cross-lingual embeddings and shared semantic spaces

---
## Why Dense Vectors

- Sparse one-hot or count vectors have no notion of similarity between words
- `cat` and `kitten` are as far apart as `cat` and `bulldozer` in count space
- Dense vectors place related words close together in a low-dimensional space
- A handful of dimensions captures syntactic and semantic regularities at once

---
## The Distributional Hypothesis

- "You shall know a word by the company it keeps" — Firth, 1957
- Words appearing in similar contexts tend to have similar meanings
- All embedding methods are different ways of operationalizing this idea
- Context can be a window of nearby words, a sentence, or a document

---
## From Counts to Dense Vectors

![counts_to_dense](svg/courses/ai/natural-language-processing/05_word_embeddings/counts_to_dense.svg)

---
## Properties We Want From Embeddings

- Similarity — semantically related words have small distance
- Composition — vector arithmetic reflects semantic operations
- Analogy — `king - man + woman` lands near `queen`
- Stability — small changes in training data give nearby vectors
- Compactness — a few hundred dimensions suffice for most tasks

---
## Early Approaches

- Latent Semantic Analysis used `SVD` on a term-document matrix
- Hyperspace Analogue to Language used windowed co-occurrence counts
- Both produced dense vectors before neural methods existed
- They were expensive on large corpora and slow to update with new data

---
## Word2Vec: The Big Idea

- Train a shallow neural network whose hidden layer is the embedding
- Two training objectives — predict context from center, or center from context
- Skip the softmax bottleneck with negative sampling or hierarchical softmax
- The result — embeddings that scale to billions of tokens on commodity hardware

---
## CBOW vs Skip-gram

- `CBOW` — Continuous Bag of Words — predict the center word from context
- Skip-gram — predict the context words given the center word
- `CBOW` trains faster and works better on frequent words
- Skip-gram works better on rare words and small corpora

---
## Word2Vec Architectures

![word2vec_architectures](svg/courses/ai/natural-language-processing/05_word_embeddings/word2vec_architectures.svg)

---
## Negative Sampling

- The full softmax over the vocabulary is prohibitively expensive
- Replace it with a binary classification — real context word vs sampled noise
- Sample a handful of negatives per positive example
- Noise distribution is the unigram distribution raised to the 3/4 power

---
## Hierarchical Softmax

- Build a binary tree over the vocabulary, often a Huffman tree
- Each prediction is a path from root to a leaf — `log(V)` decisions
- Each internal node has its own learned vector
- Faster than full softmax; negative sampling is usually preferred today

---
## Word2Vec Hyperparameters

- Window size — how far the context extends from the center word
- Embedding dimension — typically 100 to 300
- Number of negatives — usually 5 to 20
- Subsampling threshold — discards very frequent words probabilistically
- Minimum word count — drops rare words below a threshold

---
## Hyperparameter Effects

- Larger window — more topical, less syntactic similarity
- Smaller window — more syntactic, captures functional roles
- More dimensions — diminishing returns past a few hundred
- Subsampling — speeds training and improves rare-word quality
- The defaults in `gensim` are sensible starting points

---
## GloVe Motivation

- `Word2Vec` learns from local windows but never sees global statistics directly
- Co-occurrence counts already summarize global context efficiently
- `GloVe` factorizes the co-occurrence matrix into word and context vectors
- Combines the speed of count methods with the geometry of neural methods

---
## The Co-occurrence Matrix

- Entry `X_ij` is how often word `j` appears in the context of word `i`
- Built once from a single pass over the corpus
- Sparse and large — but storage is cheaper than re-reading text
- Captures global statistics that windowed methods only see locally

---
## GloVe Loss

```python
# pair-wise loss summed over non-zero co-occurrences
J = sum(
    f(X_ij) * (w_i.dot(w_j_tilde) + b_i + b_j_tilde - log(X_ij))**2
    for i, j in cooccurrences
)
# f(x) is a weighting function that down-weights rare and very common pairs
```

- Dot product of two vectors approximates the log of their co-occurrence
- Weighting `f(X_ij)` keeps frequent pairs from dominating the loss

---
## GloVe vs Word2Vec

- `Word2Vec` — local context, online stochastic updates
- `GloVe` — global statistics, batch matrix factorization
- Both produce vectors with similar geometric properties
- In practice the gap is small; the choice often comes down to tooling

---
## FastText: Subword Embeddings

- A word is represented as the sum of its character n-gram vectors
- `apple` decomposes into `<ap`, `app`, `ppl`, `ple`, `le>` and the whole word
- The model learns vectors for n-grams, not just words
- Morphologically rich languages benefit dramatically

---
## FastText and Out-of-Vocabulary

- Truly novel words still have an embedding — sum of their n-grams
- Misspellings inherit some of their correct neighbors' geometry
- Domain-specific terms compose from familiar pieces
- The classical `OOV` problem largely disappears

---
## FastText for Cross-lingual Use

- Subword sharing extends to typologically related languages
- Pretrained vectors are released for over 150 languages
- Aligned variants give a shared space across languages
- Practical default for low-resource and code-switched text

---
## Embedding Properties

![embedding_properties](svg/courses/ai/natural-language-processing/05_word_embeddings/embedding_properties.svg)

---
## Similarity Benchmarks

- `WordSim-353` — pairs rated for similarity by humans
- `SimLex-999` — emphasizes similarity over relatedness
- `MEN` — larger and broader than `WordSim-353`
- Correlation with human ratings is the standard intrinsic metric

---
## Analogy Tasks

- `king - man + woman` should land near `queen`
- `Paris - France + Germany` should land near `Berlin`
- `walking - walked + swam` should land near `swimming`
- The Google analogy set covers semantic and syntactic relations

---
## Analogy Caveats

- The arithmetic only works on average across many examples
- Results depend heavily on whether the target is excluded from the candidate set
- Many "successes" are partly an artifact of vector length normalization
- Analogies are an intrinsic probe, not a downstream task

---
## Visualization with t-SNE and UMAP

- `t-SNE` preserves local neighborhoods; clusters look meaningful
- `UMAP` is faster and preserves more global structure
- Both produce visually striking 2D maps of high-dimensional vectors
- Both can show patterns that are not actually present — interpret with care

---
## Bias in Embeddings

- Embeddings absorb the statistical biases of their training corpus
- `man : programmer :: woman : homemaker` — the analogy fires
- Geographic, racial, and occupational stereotypes appear in measurable form
- Debiasing methods reduce projections onto bias subspaces but rarely eliminate them

---
## Cross-lingual Embeddings

- Goal — a shared vector space where translations are nearby
- Enables transfer of classifiers from high-resource to low-resource languages
- Three families — mapping, joint training, and pivoting through a shared anchor
- Quality varies enormously with typological distance between language pairs

---
## Mapping Monolingual Spaces

- Train embeddings independently for each language
- Learn a linear transformation between the two spaces
- Procrustes alignment minimizes distance over a small bilingual dictionary
- Surprisingly effective when languages share enough structure

---
## MUSE Adversarial Alignment

- Learn the mapping without any bilingual dictionary
- A discriminator tries to tell mapped source vectors from real target vectors
- The mapping is trained to fool the discriminator
- A refinement step uses the induced dictionary to polish the alignment

---
## Multilingual Joint Training

- Train a single embedding model on a mix of languages
- Shared subword vocabulary (`SentencePiece`) ties the spaces together
- No explicit alignment step — the shared parameters do the work
- The basis for modern multilingual transformer models

---
## Cross-lingual Embedding Approaches

![crosslingual_approaches](svg/courses/ai/natural-language-processing/05_word_embeddings/crosslingual_approaches.svg)

---
## Embeddings in Practice

- Pretrained vectors are a strong baseline for many tasks
- Fine-tune on domain text when the domain shifts vocabulary
- Average word vectors give a serviceable sentence representation
- Modern pipelines mostly use contextual embeddings — but static vectors still work

---
## When Static Embeddings Are Enough

- Strict latency or memory budgets
- Simple classification with limited training data
- Lookup-table semantics where context is irrelevant
- Cross-lingual transfer for low-resource languages

---
## Anti-Patterns

- Mixing tokenizations between embedding training and downstream use
- Reporting analogy accuracy as a proxy for downstream quality
- Treating `t-SNE` clusters as ground truth
- Ignoring bias measurements until production complaints surface

---
## Summary

- Dense vectors replaced sparse counts because geometry encodes meaning
- `Word2Vec`, `GloVe`, and `FastText` reach similar geometry by different routes
- Subword embeddings dissolve the out-of-vocabulary problem
- Embeddings inherit corpus bias — measure it, do not assume it is absent
- Cross-lingual spaces are the foundation of modern multilingual models
