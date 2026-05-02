---
tags:
  - data-and-ai:llm
level: intermediate
category: machine-learning
audience:
  - audiences:developers
  - audiences:data-scientists

---
# Embeddings and Chunking

---
## What This Chapter Covers

- What embeddings are
- Choosing a model
- Chunking strategies
- Metadata
- Pitfalls

---
## What an Embedding Is

- Vector representation of text
- Similar text yields close vectors
- Distance metric: cosine usually
- Numerical, fixed length

---
## Choosing an Embedding Model

- General purpose vs domain
- Open vs hosted
- Dimension and cost
- Latency to embed

---
## Popular Models

- Hosted embedding APIs
- Open-source embedding models
- Domain models for code or medical text

---
## Embedding Quality

- Test on your queries
- Public benchmarks as a starting point
- Domain match beats benchmark wins
- Re-test when models update

---
## Chunking Why

- Documents are too long for context
- Embedding granularity matters
- Trade specificity vs context
- Wrong chunks ruin retrieval

---
## Chunk Sizes

- 200 to 1000 tokens typical
- Overlap of 10 to 20 percent
- Larger for narrative, smaller for FAQ
- Always evaluate

---
## Chunking Strategies

- Fixed window
- Sentence boundaries
- Section headers
- Semantic boundaries

---
## Strategies Compared

![chunking_strategies](svg/courses/ai/rag-applications/02_embeddings_and_chunking/chunking_strategies.svg)

---
## Structure-Aware Chunking

- Use headings
- Code: by function or class
- Tables: rows or whole table
- Preserve titles in each chunk

---
## Metadata

- Source URL
- Section heading
- Date
- Permissions
- Use for filtering and citation

---
## Updates

- Re-embed when model changes
- Re-embed when chunking changes
- Track version per chunk
- Treat the index as a build artifact

---
## Multilingual

- Some embeddings are multilingual
- Others are English first
- Test cross-lingual retrieval
- Consider per-language indexes

---
## Common Embedding Mistakes

- One chunk size for all docs
- Stripping headings
- Mixing models in one index
- No metadata
- No re-embed on doc updates
