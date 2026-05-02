---
tags:
  - data-and-ai:llm
level: intermediate
category: machine-learning
audience:
  - audiences:developers
  - audiences:data-scientists

---
# Retrieval and Indexes

---
## What This Chapter Covers

- Vector indexes
- ANN algorithms
- Hybrid search
- Filtering
- Reranking

---
## Vector Indexes

- Store vectors
- Find nearest neighbors
- Approximate for speed
- Scale to billions

---
## ANN Algorithms

- Graph-based methods
- Inverted file methods
- Quantization methods
- Disk-resident variants

---
## Vector Stores

- Hosted vector databases
- Postgres extensions for vectors
- Self-hosted clusters
- Embedded libraries

---
## Choosing a Store

- Dataset size
- QPS and latency
- Operational fit
- Cost model

---
## Cosine Similarity

- Dot product on normalized vectors
- Angle, not magnitude
- Default for most embeddings
- Inner product or L2 sometimes

---
## Filtering

- Pre-filter by metadata
- Post-filter after kNN
- Pre-filter is faster but tricky with ANN
- Test both for your data

---
## Hybrid Search

- Keyword search plus vector
- Combine via weighted sum or rank fusion
- Helps with rare terms
- Strong default in production

---
## Hybrid Visualized

![hybrid_search](svg/courses/ai/rag-applications/03_retrieval_and_indexes/hybrid_search.svg)

---
## Reranking

- Take top N from retrieval
- Cross-encoder scores them
- Slower but more accurate
- Use a dedicated reranker model

---
## Top-K Choice

- Too low: miss the right chunk
- Too high: noisy context
- Tune with evaluation set
- Often 5 to 20

---
## Diversity

- Maximal Marginal Relevance
- Avoids near-duplicates
- Useful for broad queries
- Tunes recall vs novelty

---
## Query Rewriting

- Expand abbreviations
- Add context from history
- Multi-query for recall
- Use a small LLM for cost

---
## Multi-Index

- One index per domain
- Route via classifier
- Cleaner permissions
- Cheaper updates

---
## Common Retrieval Mistakes

- Using vector only
- Too small top-K
- No filter for permissions
- No reranker for accuracy
- Stale index
