---
tags:
  - data-and-ai:ai
  - data-and-ai:llm
  - data-and-ai:rag
level: intermediate
category: ai
audience:
  - audiences:developers
  - audiences:senior-developers

---
# RAG: Grounding Claude in Your Data

---
## What This Chapter Covers

- The problem RAG solves
- Anatomy of a RAG pipeline
- Choosing the moving parts
- Retrieval quality
- Wiring RAG into Claude
- RAG vs long context vs fine-tuning

---
## The Problem

- Claude does not know your private data
- The web does not index your wiki
- Your secrets are not in the weights
- The model is blind to your corpus

---
## Why "Just Paste It In" Stops Working

- Your corpus is bigger than the window
- Even 1M tokens fills up fast
- Costs grow linearly with input
- Latency grows with input

---
## Why Fine-Tuning Is Usually Wrong

- Slow and expensive to update
- Hard to cite sources
- Changes the model's behavior, not just facts
- Most teams do not need it

---
## RAG In One Sentence

- Retrieve relevant text, then generate
- The model reads what was retrieved
- Answers ground in retrieved chunks
- Sources can be cited

---
## Anatomy Of A RAG Pipeline

- Ingestion
- Chunking
- Embedding
- Indexing
- Retrieval
- Generation

---
## The Pipeline Visualized

![rag_pipeline](svg/courses/ai/claude-workshop/07_rag/rag_pipeline.svg)

---
## Ingestion

- Crawl or pull source documents
- Normalize formats
- Strip noise
- Track provenance

---
## Chunking

- Break docs into retrievable pieces
- Chunk size is a knob
- Overlap is a knob
- Boundaries should not destroy meaning

---
## Chunking With Overlap

![chunking](svg/courses/ai/claude-workshop/07_rag/chunking.svg)

---
## Embeddings

- Turn text into a vector
- Similar text gets similar vectors
- A specific model defines "similar"
- Cost per token applies

---
## The Vector Store

- A database that does vector search
- Returns top-k nearest neighbors
- Often supports metadata filters
- Often supports hybrid search

---
## Retrieval At Query Time

- Embed the user query
- Look up nearest chunks
- Optionally rerank
- Pass to the model

---
## Composing The Final Prompt

- A system prompt with rules
- The retrieved chunks
- The user question
- Maybe a few-shot example

---
## Choosing The Embedding Model

- Quality varies dramatically
- Multilingual or not
- Cost per million tokens
- Re-embedding is expensive

---
## Choosing The Vector Store

- Postgres + pgvector for small scale
- Dedicated stores for serious scale
- Hosted vs self-hosted
- Filter support matters

---
## Chunk Size And Overlap

- Too small: lose context
- Too big: dilute relevance
- Overlap helps boundary words
- Tune on real queries

---
## Retrieval Quality

- The whole pipeline rides on this
- Bad retrieval beats good generation
- Evaluate it on its own
- Iterate before going further

---
## Why Naive Cosine Disappoints

- Embeddings encode similarity, not relevance
- Synonyms cluster, but so does noise
- Rare keywords get lost
- Hybrid helps

---
## Hybrid Search With BM25

- BM25 catches keyword matches
- Embeddings catch semantic matches
- Combine both, rerank
- Hybrid beats either alone

---
## Reranking

- A second pass over top-k
- Cross-encoder rates pairs
- Slow but precise
- Use on top-50 to pick top-5

---
## Evaluating Retrieval

- Build a labeled set of queries
- Measure recall at k
- Measure precision at k
- Fix retrieval before fixing prompts

---
## Wiring RAG Into Claude

- Expose retrieval as an MCP tool
- The model calls it when needed
- Results enter the prompt
- The model cites the source

---
## Letting Claude Decide When To Retrieve

- Describe the tool clearly
- Trust the model to call it
- Watch when it forgets
- Sometimes force it via instructions

---
## Citing Sources

- Each chunk has an ID and a URL
- The model cites in the answer
- The user can verify
- Hallucinations get caught

---
## RAG Vs Long Context

- Long context: stuff it all in
- RAG: pick what is relevant
- Long context: simpler, expensive
- RAG: complex, scales further

---
## RAG Vs Fine-Tuning

- Fine-tune for style and behavior
- RAG for facts and freshness
- They are complementary
- Most teams need RAG before tuning

---
## Three Approaches Compared

![rag_vs_alternatives](svg/courses/ai/claude-workshop/07_rag/rag_vs_alternatives.svg)

---
## Combining Sensibly

- Tune a small model for tone
- Retrieve facts at query time
- Compose in the prompt
- Measure end-to-end

---
## Common Failure Modes

- Stale indexes
- Chunk boundaries that destroy meaning
- Confident hallucinations on bad retrieval
- No evaluation at all

---
## Hands-On Exercise

- Build a minimal RAG pipeline
- Index a small docs folder
- Expose retrieval as an MCP tool
- Ask Claude a grounded question and verify the cite
