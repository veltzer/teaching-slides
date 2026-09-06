---
tags:
  - data-and-ai:llm
level: intermediate
category: machine-learning
audience:
  - audiences:developers
  - audiences:data-scientists

---

# Production RAG

---

## What This Chapter Covers

- Ingestion pipelines
- Permissions
- Monitoring
- Cost control
- Failure modes

---

## Ingestion Pipeline

- Pull from source
- Parse and clean
- Chunk
- Embed
- Index

---

## Pipeline Visualized

![ingestion_pipeline](svg/courses/ai/rag-applications/05_production_rag/ingestion_pipeline.svg)

---

## Source Connectors

- File systems
- Confluence, Notion
- Google Drive
- Internal APIs

---

## Incremental Updates

- Detect new and changed docs
- Re-embed only changed chunks
- Delete on source delete
- Track lineage

---

## Freshness Pipeline

![freshness_pipeline](svg/courses/ai/rag-applications/05_production_rag/freshness_pipeline.svg)

---

## Permissions

- Store ACL with each chunk
- Filter at query time
- Per-user index views
- Test for leakage

---

## Audit Logging

- Query
- Retrieved chunks
- Final answer
- Per-user retention

---

## Latency Budget

- Embedding: tens of ms
- Retrieval: tens of ms
- Generation: hundreds of ms to seconds
- Stream the answer

---

## Cost Levers

- Cache embeddings
- Cache popular answers
- Smaller LLM for routing
- Larger LLM only on hard queries

---

## Caching Layers

- Query embedding cache
- Retrieval cache
- Final answer cache
- Salt by user permissions

---

## Drift

- New docs, new vocabulary
- Old chunks rotate out
- Eval set drifts too
- Re-evaluate on a schedule

---

## Hallucination Defense

- Require citations
- Reject unsupported answers
- Confidence score
- Human escalation

---

## Multi-Tenant

- Per-tenant index
- Or shared index with strict filters
- Quota per tenant
- Separate eval per tenant

---

## Failure Modes

- Index unavailable
- Embedding service down
- LLM rate-limited
- Have a graceful fallback for each

---

## Common Production Mistakes

- No incremental ingestion
- No permission filter
- No answer cache
- No drift evaluation
- One LLM for every query
