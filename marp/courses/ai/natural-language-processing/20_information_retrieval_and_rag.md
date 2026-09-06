---
tags:
  - data-and-ai:nlp
  - concepts:information-retrieval
level: advanced
category: ai
audience:
  - audiences:developers
  - audiences:data-scientists

---

# Information Retrieval and RAG

---

## What This Chapter Covers

- Classical information retrieval and the metrics that anchor it
- Sparse retrieval with `BM25` and inverted indexes
- Dense retrieval with bi-encoders and approximate nearest neighbor search
- Reranking with cross-encoders and learned rerankers
- Retrieval-augmented generation as the modern grounding pattern
- Production realities: chunking, freshness, evaluation, and cost

---

## Why Information Retrieval Still Matters

- The world has more text than any model can memorize
- Retrieval is how we hand the right context to a model at inference time
- Search engines, e-commerce, and `RAG` all share the same machinery
- Cheap, scalable, well-understood, and embarrassingly parallel
- The piece of `LLM` infrastructure that runs at the largest scale

---

## The IR Setup

- A query, a corpus of documents, and a need to rank documents by relevance
- Relevance is judged by humans or learned from click signals
- Modern systems are pipelines: retrieve, rerank, optionally generate
- The same architecture serves web search, enterprise search, and `RAG`
- Domain shifts the relevance signal, not the architecture

---

## Classical IR: Boolean Retrieval

- Documents are sets of terms; queries combine terms with `AND`, `OR`, `NOT`
- An inverted index maps each term to the documents containing it
- Fast, deterministic, and exactly what you want for legal discovery
- No notion of ranking — every match is equally relevant
- The foundation that all later systems sit on

---

## TF-IDF Retrieval

- Score documents by term frequency weighted by inverse document frequency
- Common terms contribute less; rare terms contribute more
- Vector-space model represents documents and queries as sparse vectors
- Cosine similarity ranks documents
- The strong baseline that survived for decades before neural retrievers

---

## BM25

- A probabilistic refinement of `TF-IDF` from the 1990s
- Term frequency saturates so very common terms do not dominate
- Length normalization compares short and long documents fairly
- The standard sparse retrieval baseline
- Often beats neural retrievers in the cold-start, out-of-domain regime

---

## BM25 Formula at a Glance

- score(D, Q) = sum over terms in Q of `idf` × normalized term frequency
- Normalized term frequency: f / (f + k1 × (1 - b + b × |D| / avgdl))
- `k1` controls saturation; `b` controls length normalization
- Default tuning works well across many domains
- Implementations: `Lucene`, `Elasticsearch`, `Tantivy`, `Pyserini`

---

## Inverted Index Internals

![inverted_index](svg/courses/ai/natural-language-processing/20_information_retrieval_and_rag/inverted_index.svg)

---

## Dense Retrieval

- Encode queries and documents into the same vector space
- Inner product or cosine similarity measures relevance
- An approximate nearest neighbor index handles search at scale
- Trained on (query, positive document) pairs with negatives
- Captures semantic similarity that lexical methods miss

---

## Bi-Encoders

- Two transformer encoders, one for queries and one for documents
- Encoding is independent — documents are precomputed once
- Search is a vector lookup, fast even for billions of documents
- The architecture that powers most production dense retrievers
- Trade-off: less expressive than cross-encoders, much faster

---

## Sentence-Transformers

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

docs = ["Apples are red.", "The sky is blue.", "Pythagoras was Greek."]
doc_vecs = model.encode(docs, normalize_embeddings=True)

q_vec = model.encode("What color is the sky?", normalize_embeddings=True)
scores = doc_vecs @ q_vec
print(docs[scores.argmax()])
# 'The sky is blue.'
```

- Three lines and you have a competitive dense retrieval baseline
- Drop in a stronger model when quality matters more than latency

---

## Approximate Nearest Neighbor Search

- Exact search over millions of vectors is too slow at query time
- `HNSW`, `IVF`, `PQ` trade a small recall hit for huge speedups
- `FAISS`, `ScaNN`, `Annoy`, `Vespa`, `Qdrant`, `Weaviate` all implement these
- Index build time is the bottleneck for very large corpora
- Recall and latency tuning is part of every retrieval system

---

## Sparse vs Dense Retrieval

![sparse_vs_dense](svg/courses/ai/natural-language-processing/20_information_retrieval_and_rag/sparse_vs_dense.svg)

---

## Hybrid Retrieval

- Combine `BM25` and dense retrieval scores
- Reciprocal rank fusion is the simplest combination
- Captures both lexical match and semantic similarity
- Often the best single configuration for unknown queries
- Worth the small extra infrastructure cost

---

## Reranking

- Take the top-100 results from retrieval and reorder them
- A cross-encoder scores (query, document) jointly
- Slower per-pair but more accurate than bi-encoder ranking
- Top-N retrieved is small enough that cross-encoding is feasible
- Standard pattern in modern search and `RAG` pipelines

---

## Cross-Encoders

- One transformer takes (query, document) as input and outputs a score
- Trained on relevance pairs from search logs or human labels
- Cannot pre-encode documents — every (query, doc) needs a forward pass
- Use only for reranking the top-K, never for first-stage retrieval
- The accuracy ceiling for current retrieval systems

---

## Retrieval Evaluation Metrics

- `Recall@K` — fraction of queries with the right document in the top K
- `MRR` (Mean Reciprocal Rank) — averaged inverse rank of the first hit
- `NDCG` (Normalized Discounted Cumulative Gain) — graded relevance
- `MAP` (Mean Average Precision) — averaged precision across recall levels
- Pick the metric that matches your downstream consumer

---

## Where RAG Fits

- Use retrieval to pull relevant text into the prompt
- Generate the answer conditioned on the retrieved context
- Combines the long memory of search with the synthesis of an `LLM`
- Avoids fine-tuning when the corpus changes faster than retraining cycles
- The dominant pattern for grounded `LLM` applications

---

## RAG Architecture

![rag_architecture](svg/courses/ai/natural-language-processing/20_information_retrieval_and_rag/rag_architecture.svg)

---

## Document Chunking

- Documents are split into passages of a few hundred tokens
- Chunk size trades recall against context budget at generation time
- Overlap between chunks recovers context that crosses boundaries
- Semantic chunking on sentence or section boundaries beats fixed splits
- Bad chunking is the hidden cause of most underperforming `RAG` systems

---

## Embedding Models for RAG

- Choice of embedding model dominates retrieval quality
- Pretrained sentence-transformers, `OpenAI text-embedding-3`, `BGE`, `E5`
- Domain-adapted embeddings outperform generic ones in narrow corpora
- Periodic re-embedding when the corpus changes
- Watch out for embedding model drift between runs

---

## Query Rewriting

- Raw user queries are often noisy or under-specified
- An `LLM` can rewrite the query to improve retrieval
- Hyde — generate a hypothetical document and embed that instead
- Decompose complex queries into multiple sub-queries
- Especially useful for conversational `RAG`

---

## Retrieval-Augmented Generation in Practice

```python
# minimal RAG loop
def answer(query, retriever, llm):
    passages = retriever.search(query, k=5)
    context = "\n\n".join(p.text for p in passages)
    prompt = f"""Answer using only the context.
Context:
{context}

Question: {query}
Answer:"""
    return llm.complete(prompt)
```

- The structure that production `RAG` systems all extend
- Variations: rerank after retrieve, multi-hop, citation requirements

---

## Citations and Grounding

- Make the model cite the chunk it relied on
- Verify that cited content actually supports the claim
- Highlight unsupported sentences for human review
- Faithful citations are an explicit anti-hallucination layer
- A trustworthy `RAG` system shows its sources

---

## RAG Failure Modes

- Retrieval misses — the right chunk is not in the top-K
- Retrieval hits but the model ignores the context
- Conflicting passages confuse the generator
- Stale corpus serves outdated information confidently
- Long context windows do not always cure these — they sometimes hide them

---

## Long Context vs RAG

- Modern `LLMs` accept hundreds of thousands of tokens
- Why retrieve at all if everything fits in context
- Cost: long-context inference is expensive and quadratic in many backends
- Quality: relevant tokens still need to be foregrounded by retrieval
- Reality: hybrid is the answer for almost every production system

---

## Caching and Cost

- Cache embeddings — they are expensive to compute and rarely change
- Cache LLM completions for repeated questions
- Reuse retrieval results within a session when the user is iterating
- Approximate index choices are cost levers, not just quality knobs
- Cost dominates `RAG` infrastructure planning

---

## RAG Evaluation

- Retrieval metrics measure whether the right context was found
- Generation metrics measure whether the answer is faithful and complete
- `RAGAS`, `TruLens`, and similar frameworks score both
- Human eval still dominates for high-stakes systems
- Evaluate on real user questions, not curated benchmarks

---

## Common Production Pitfalls

- Treating embeddings as a black box and never re-evaluating them
- Chunk sizes copied from a tutorial that does not match your corpus
- Adding a reranker when retrieval was the actual bottleneck
- Trusting an `LLM` to answer when retrieval found nothing
- Skipping incremental updates and rebuilding the index on every change

---

## Anti-Patterns

- Embedding the entire web because storage is cheap
- Single-vector representations for documents that span many topics
- Treating `BM25` as obsolete when it remains the strongest cold-start baseline
- Cross-encoder rerank on the entire corpus, not the top-K
- Reporting `NDCG` from one corpus and inferring user satisfaction

---

## Summary

- Information retrieval underpins both search and `RAG`
- Sparse `BM25` is still the baseline that beats most things in cold start
- Dense retrievers excel on semantic and out-of-vocabulary queries
- Reranking with cross-encoders is the accuracy ceiling
- `RAG` weaves retrieval into generation and dominates grounded `LLM` apps
