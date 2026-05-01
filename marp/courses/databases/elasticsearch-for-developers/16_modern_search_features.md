---
tags:
  - databases:elasticsearch
  - databases:vector-search
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Modern Search Features

---
## What This Chapter Covers

- Vector search
- Semantic search
- Learned sparse retrieval (ELSER)
- Hybrid search
- Behavioural Analytics
- Search Applications

---
## Vector Search

- Search by vector similarity
- Documents embedded into vectors
- Query embedded; nearest match
- Semantic, not lexical

---
## Embeddings

- Pre-trained model converts text to vector
- BERT, sentence-transformers
- Vector dimension: typically 384 / 768 / 1536
- Stored as `dense_vector` field

---
## Vector Index Example

```json
"embedding": {
    "type": "dense_vector",
    "dims": 768,
    "index": true,
    "similarity": "cosine"
}
```

---
## kNN Search

```json
{
  "knn": {
    "field": "embedding",
    "query_vector": [...],
    "k": 10,
    "num_candidates": 100
  }
}
```

- k: results to return
- num_candidates: search breadth
- Trade-off: precision vs speed

---
## Hybrid Search

- Combine lexical + vector
- BM25 for exact matches; vector for semantic
- Reciprocal Rank Fusion (RRF) merges results
- Best of both

---
## ELSER

- Elastic's Learned Sparse EncodeR
- Semantic search without dense vectors
- Token-level expansions
- No external model needed

---
## RAG Pattern

- Retrieval-Augmented Generation
- Vector search retrieves context
- LLM generates answer using context
- ES + LLM = Q&A over your data

---
## Behavioural Analytics

- Track: search queries, clicks
- Improve ranking from real user data
- Built-in or DIY
- Machine-learning-driven relevance

---
## Search Applications

- Higher-level Elastic Cloud feature
- Combines: search experience, analytics, A/B
- Curated UI for non-developers
- Recently added; evolving

---
## Synonyms API

- Manage synonyms via API
- Live updates without reindex
- Multiple synonyms sets
- Standard pattern for managed search

---
## Stemmer / Tokeniser Choices

- Per-language stemmers
- Language detection at index time
- Mix and match for global products

---
## Query Rules

- Pin specific results to top
- "Anyone searching 'iphone' sees our newest as #1"
- A/B test the rules

---
## ML Inference

- Run an ML model at index / query time
- Sentiment, entity extraction, classification
- Pre-trained or custom models
- Adds compute cost

---
## Common Modern-Feature Mistakes

- Vector search without dimension consistency
- Wrong similarity metric (cosine vs L2)
- Heavy embeddings field on every doc
- Hybrid without RRF; mismatch in scales
- No baseline; can't measure improvement
