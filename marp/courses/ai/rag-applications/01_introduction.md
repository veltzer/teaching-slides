---
tags:
  - data-and-ai:llm
level: intermediate
category: machine-learning
audience:
  - audiences:developers
  - audiences:data-scientists

---

# Introduction to RAG

---

## What This Chapter Covers

- What RAG is
- Why RAG over fine-tuning
- Components
- Use cases
- Course outline

---

## What RAG Is

- Retrieval-Augmented Generation
- Look up relevant text
- Stuff it into the prompt
- Let the model answer with grounding

---

## Why RAG

- Knowledge can be updated
- Cite sources
- Cheaper than fine-tuning
- Less hallucination

---

## RAG vs Fine-Tuning

- Fine-tune: change behavior
- RAG: change knowledge
- They are complementary
- Most teams start with RAG

---

## Components

- Document store
- Chunking step
- Embedding model
- Vector index
- LLM

---

## Lifecycle

- Ingest documents
- Embed chunks
- Index
- At query: embed, retrieve, prompt
- Return answer with citations

---

## RAG Flow Visualized

![rag_flow](svg/courses/ai/rag-applications/01_introduction/rag_flow.svg)

---

## Use Cases

- Internal knowledge base
- Customer support
- Legal and compliance lookup
- Code search and explain

---

## Quality Levers

- Better chunks
- Better embeddings
- Better retrieval
- Better prompts

---

## When RAG Struggles

- Multi-hop reasoning
- Aggregation queries
- Math and counting
- Up-to-the-second freshness

---

## Hybrid With Fine-Tuning

- Fine-tune for tone and format
- RAG for facts
- Combine in production
- Evaluate end-to-end

---

## Hosted vs Self-Hosted

- Hosted is fast to start
- Self-hosted gives control
- Cost models differ
- Pick by data sensitivity

---

## Course Outline

- Embeddings
- Indexing and retrieval
- Prompting with context
- Evaluation
- Production

---

## Common Beginner Mistakes

- Treating RAG as a database query
- Skipping evaluation
- Hand-tuning chunks for one query
- Ignoring source freshness
- Not citing sources
