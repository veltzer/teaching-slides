---
tags:
  - databases:elasticsearch
level: intermediate
category: databases
audience:
  - audiences:dbas

---

# Vector and Semantic Search

---

## What This Chapter Covers

- The `dense_vector` field type and how vectors are indexed
- kNN search and approximate kNN with HNSW
- Building semantic search with embeddings
- Inference endpoints and the `_inference` API
- Hybrid search combining kNN and BM25 with RRF
- Sizing and performance for vector workloads
- Quantization options to control memory

---

## Why Vector Search Matters for DBAs

- Semantic search ranks by meaning, not just keyword overlap
- Embeddings turn text or images into numeric vectors
- Similar items sit close together in vector space
- The ops challenge is memory and latency, not relevance theory
- HNSW graphs are large and want to live in RAM
- Treat vector indices as a distinct, memory-hungry workload tier

---

## The dense_vector Field Type

- Store an embedding per document as a `dense_vector`
- `dims` must match your model output dimension
- `similarity` defines how distance becomes a score

```json
PUT /articles
{
  "mappings": {
    "properties": {
      "embedding": {
        "type": "dense_vector",
        "dims": 768,
        "similarity": "cosine"
      }
    }
  }
}
```

- Common `similarity` values: `cosine`, `dot_product`, `l2_norm`
- `dot_product` is fastest but expects normalized vectors

---

## HNSW Index Options

- By default `dense_vector` builds an HNSW graph for approximate search
- `m` controls connections per node; higher means better recall, more memory
- `ef_construction` controls build-time quality versus indexing speed

```json
"embedding": {
  "type": "dense_vector",
  "dims": 768,
  "index": true,
  "similarity": "cosine",
  "index_options": {
    "type": "hnsw",
    "m": 16,
    "ef_construction": 100
  }
}
```

- Larger `m` and `ef_construction` raise recall at a memory and CPU cost
- Tune these against a recall benchmark, not by guesswork

---

## Approximate kNN Search

- The `knn` query searches the HNSW graph efficiently
- `k` is how many neighbors to return
- `num_candidates` is how many to explore per shard

```json
POST /articles/_search
{
  "knn": {
    "field": "embedding",
    "query_vector": [0.12, -0.04, 0.88],
    "k": 10,
    "num_candidates": 100
  }
}
```

- Higher `num_candidates` improves recall but costs latency
- Keep `num_candidates` at least as large as `k`, usually much larger

---

## Exact versus Approximate kNN

- Approximate kNN uses the HNSW graph and is the default at scale
- Exact kNN scans every vector with a script-based query
- Exact is accurate but linear in document count, so it is slow

```json
POST /articles/_search
{
  "query": {
    "script_score": {
      "query": { "term": { "category": "news" } },
      "script": {
        "source": "cosineSimilarity(params.q, 'embedding') + 1.0",
        "params": { "q": [0.12, -0.04, 0.88] }
      }
    }
  }
}
```

- Use exact kNN only on small, pre-filtered candidate sets

---

## Embeddings and Inference Endpoints

- Embeddings can be generated outside or inside Elasticsearch
- The `_inference` API registers a model endpoint to call
- This keeps indexing and query embeddings consistent

```json
PUT /_inference/text_embedding/my-embeddings
{
  "service": "elasticsearch",
  "service_settings": {
    "num_allocations": 1,
    "num_threads": 1,
    "model_id": ".multilingual-e5-small"
  }
}
```

- Inference runs on ML nodes; size them for embedding throughput
- One endpoint serves both ingest-time and query-time embeddings

---

## Semantic Search Pipelines

- An ingest pipeline can embed text automatically on write
- The `inference` processor calls the registered endpoint

```json
PUT /_ingest/pipeline/embed
{
  "processors": [
    {
      "inference": {
        "model_id": "my-embeddings",
        "input_output": {
          "input_field": "body",
          "output_field": "embedding"
        }
      }
    }
  ]
}
```

- Index with `?pipeline=embed` so documents get vectors automatically
- The `semantic_text` field type can manage this end to end

---

## Querying with semantic_text

- `semantic_text` hides chunking and embedding behind one field
- It auto-creates vectors using its associated inference endpoint

```json
PUT /docs
{
  "mappings": {
    "properties": {
      "content": { "type": "semantic_text", "inference_id": "my-embeddings" }
    }
  }
}
```

- Query it naturally with a `semantic` query and plain text

```json
POST /docs/_search
{ "query": { "semantic": { "field": "content", "query": "how to reduce heap" } } }
```

- This is the lowest-effort path to semantic search

---

## Hybrid Search with RRF

- Hybrid search blends lexical BM25 with semantic kNN
- Reciprocal Rank Fusion merges result lists without score tuning
- RRF needs no score normalization between the two methods

```json
POST /articles/_search
{
  "retriever": {
    "rrf": {
      "retrievers": [
        { "standard": { "query": { "match": { "body": "heap pressure" } } } },
        { "knn": { "field": "embedding", "query_vector": [0.1, 0.2],
                   "k": 50, "num_candidates": 200 } }
      ],
      "rank_window_size": 100
    }
  }
}
```

- RRF gives robust relevance that beats either method alone

---

## Tuning RRF

- `rank_window_size` is how deep each retriever contributes
- `rank_constant` dampens the influence of top ranks
- Larger windows improve recall but cost more work

```json
"rrf": {
  "retrievers": [ "..." ],
  "rank_window_size": 100,
  "rank_constant": 60
}
```

- Start with defaults and adjust only against measured relevance
- Keep the window large enough to surface semantic matches BM25 misses

---

## Sizing: Memory for HNSW

- HNSW graphs are most effective when they fit in RAM
- A raw float vector costs `dims` times 4 bytes per document
- One million 768-dim vectors is roughly 3 GB of raw float data
- The HNSW graph adds connection overhead on top of that
- Elasticsearch loads vectors off-heap into the filesystem cache
- Size node RAM so vectors plus graph stay cached, not paged from disk

---

## Off-Heap and the Filesystem Cache

- Vector data lives off-heap, served from the OS page cache
- This is why heap should stay small and RAM stay generous
- Cold reads from disk make approximate kNN latency spike
- Monitor cache behavior under realistic query load

```bash
GET /_nodes/stats/indices/dense_vector
```

- If queries hit disk often, add RAM or apply quantization
- Provision dedicated vector nodes when the working set is large

---

## Quantization: int8 and bbq

- Quantization shrinks vectors to cut memory dramatically
- `int8_hnsw` stores 8-bit values, about a 4x reduction
- `bbq_hnsw` is binary quantization, far smaller still

```json
"embedding": {
  "type": "dense_vector",
  "dims": 768,
  "index_options": { "type": "int8_hnsw" }
}
```

- Quantization trades a small recall drop for big memory savings
- BBQ suits very large corpora where RAM is the binding constraint
- Always validate recall after enabling quantization

---

## Vector Workload Checklist

- Match `dims` to the embedding model exactly
- Pick `similarity` that matches the model, normalize for `dot_product`
- Set `num_candidates` well above `k` for recall
- Use RRF to combine semantic and lexical retrieval
- Size RAM so vectors and HNSW graphs stay cached off-heap
- Apply int8 or BBQ quantization when memory is tight
- Benchmark recall and latency before and after every change
