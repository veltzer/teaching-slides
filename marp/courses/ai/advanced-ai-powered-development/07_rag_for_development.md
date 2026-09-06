---
tags:
  - data-and-ai:ai
  - data-and-ai:agents
  - data-and-ai:mcp
  - data-and-ai:rag
  - practices:tools
  - practices:large-codebases
  - data-and-ai:prompt-engineering
  - practices:productivity
level: advanced
category: ai
audience:
  - audiences:developers

---

# RAG (Retrieval-Augmented Generation) for Development

## Grounding AI in Your Codebase

---

## Why RAG Matters for Development

1. LLMs have finite context windows (even large ones fill up fast with code)
1. Models lack knowledge of your private codebase, internal APIs, and conventions
1. RAG grounds AI responses in project-specific, up-to-date knowledge
1. Dramatically reduces hallucinations by providing real source material
1. Enables AI to reference thousands of files without stuffing them into a prompt

---

## The Hallucination Problem Without RAG

Without RAG, an LLM asked about your internal `PaymentService`:
- Invents plausible but wrong method signatures
- Guesses at configuration patterns
- Cannot reference actual error handling logic

With RAG:
- Retrieves the real `PaymentService` source code
- References actual method signatures and docstrings
- Grounds answers in your test cases and usage examples

---

## RAG Architecture

![rag_architecture](svg/courses/ai/advanced-ai-powered-development/07_rag_for_development/rag_architecture.svg)

---

## RAG Architecture Overview

![rag_architecture_overview](svg/courses/ai/advanced-ai-powered-development/07_rag_for_development/rag_architecture_overview.svg)

---

## Document Chunking Strategies for Code

| Strategy | Granularity | Best For |
|----------|------------|----------|
| File-level | Entire files | Small files, configs |
| Function-level | Individual functions/methods | Most source code |
| Class-level | Full class definitions | OOP-heavy codebases |
| Chunk-level | Fixed-size overlapping windows | Documentation, logs |
| AST-based | Syntax tree nodes | Precise semantic units |

**Key insight**: code-aware chunking (using AST parsers) vastly outperforms naive text splitting.

---

## Tree-sitter vs AST Chunking Comparison

| Aspect | `tree-sitter` | Language-Native Parsers (e.g., Python `ast`) |
|--------|---------------|----------------------------------------------|
| Language support | 100+ languages via grammars | One language per parser |
| Error tolerance | Parses incomplete/broken code | Fails on syntax errors |
| Incremental parsing | Yes, re-parses only changes | Full re-parse required |
| Granularity control | Configurable node types | Language-specific APIs |
| Maintenance | Community-maintained grammars | Tied to language version |

```python
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))
tree = parser.parse(bytes(source_code, "utf8"))
# Works across Python, JS, Go, Rust, etc. with grammar swap
```

- Use `tree-sitter` for polyglot codebases
- Use native parsers when you need deep language-specific analysis

---

## AST-Based Chunking Example

```python
import ast

def extract_functions(source: str) -> list[dict]:
    tree = ast.parse(source)
    chunks = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            chunk = {
                "name": node.name,
                "code": ast.get_source_segment(source, node),
                "lineno": node.lineno,
                "docstring": ast.get_docstring(node),
            }
            chunks.append(chunk)
    return chunks
```

- Preserves complete function boundaries
- Captures docstrings as natural language metadata

---

## Embedding Models for Source Code

| Model | Strengths | Dimension |
|-------|-----------|-----------|
| `text-embedding-3-large` | General purpose, good for mixed code+docs | 3072 |
| `voyage-code-3` | Purpose-built for code retrieval | 1024 |
| `codesage-large` | Open-source, multi-language code | 1024 |
| `nomic-embed-code` | Open-source, strong code understanding | 768 |

**Tips**:
- Code-specific models outperform general models by 15-30% on code retrieval
- Always benchmark on your own codebase before committing

---

## Embedding Model Selection Guide

| Criteria | `voyage-code-3` | `text-embedding-3-large` | `nomic-embed-code` |
|----------|-----------------|--------------------------|---------------------|
| Code retrieval accuracy | Highest | Good | Good |
| Dimensions | 1024 | 3072 | 768 |
| Cost per 1M tokens | ~$0.06 | ~$0.13 | Free (open-source) |
| Self-hosting | No | No | Yes |
| Multilingual code | Strong | Moderate | Moderate |

**Selection criteria**:
1. Start with open-source models for prototyping and cost control
1. Move to `voyage-code-3` when retrieval quality is critical
1. Use `text-embedding-3-large` when mixing code with natural language docs
1. Consider storage costs: 3072-dim vectors use 3x more space than 1024-dim

---

## Vector Databases Comparison

| Database | Deployment | Strengths |
|----------|-----------|-----------|
| `ChromaDB` | Embedded / self-hosted | Easy setup, great for prototyping |
| `Qdrant` | Self-hosted / cloud | High performance, rich filtering |
| `Pinecone` | Managed cloud | Zero-ops, serverless option |
| `Weaviate` | Self-hosted / cloud | Hybrid search built-in |

```python
import chromadb

client = chromadb.PersistentClient(path="./codebase_index")
collection = client.get_or_create_collection(
    name="source_code",
    metadata={"hnsw:space": "cosine"},
)
```

---

## Hybrid Search: Vector + Keyword

Pure vector search misses exact matches (e.g., `ERR_CONNECTION_REFUSED`).
Pure keyword search misses semantic similarity.

```python
def hybrid_search(query: str, collection, bm25_index, alpha=0.7):
    # Vector search (semantic)
    vector_results = collection.query(
        query_texts=[query], n_results=20
    )
    # Keyword search (BM25)
    keyword_results = bm25_index.search(query, top_k=20)
    # Reciprocal rank fusion
    fused = reciprocal_rank_fusion(
        vector_results, keyword_results, alpha=alpha
    )
    return fused[:10]
```

- `alpha` controls the weight between semantic and keyword relevance

---

## Multi-Modal RAG: Diagrams, Screenshots, Config Files

Not all project knowledge lives in source code:

| Asset Type | Embedding Approach | Use Case |
|------------|-------------------|----------|
| Architecture diagrams | Vision model captioning + text embed | Design intent retrieval |
| Screenshots (UI bugs) | `CLIP` / vision embeddings | Visual regression context |
| Config files (YAML/JSON) | Flatten to key-value text chunks | Infrastructure questions |
| Database schemas | DDL statement chunking | Data model queries |
| Log files | Time-window chunking with severity tags | Debugging context |

**Pipeline**:
1. Detect asset type by file extension and MIME type
1. Route to appropriate preprocessor (vision model, flattener, parser)
1. Generate text representation, then embed as usual
1. Store original asset reference in metadata for retrieval

---

## Indexing Strategies: Choosing Granularity

### File-level
- Fast to build, coarse retrieval
- Works for small projects (<500 files)

### Function-level
- Best precision for most codebases
- Requires language-aware parsing (`tree-sitter`, `ast`)

### Chunk-level with overlap
- Fallback for binary docs, logs, unstructured text
- Use 512-1024 token chunks with 20% overlap

**Recommendation**: combine function-level for source code with chunk-level for docs.

---

## Metadata Extraction and Enrichment

Metadata dramatically improves retrieval filtering and re-ranking:

```python
def enrich_chunk(chunk: dict, file_path: str) -> dict:
    return {
        **chunk,
        "file_path": file_path,
        "language": detect_language(file_path),
        "module": extract_module(file_path),
        "imports": extract_imports(chunk["code"]),
        "last_modified": git_last_modified(file_path),
        "authors": git_authors(file_path),
        "test_file": "test" in file_path.lower(),
    }
```

- Filter by `language`, `module`, or `test_file` at query time
- Boost recently modified files for relevance

---

## Graph RAG: Motivation

Enhance retrieval by leveraging code dependency graphs:

---

## Graph RAG for Code

![graph_rag_for_code](svg/courses/ai/advanced-ai-powered-development/07_rag_for_development/graph_rag_for_code.svg)

---

## Graph RAG: Implementation Details

- When a query matches `UserService`, also retrieve its dependencies
- Walk the import/call graph 1-2 hops to gather related context
- Tools: `tree-sitter` for imports, `pydeps`, `madge` for dependency graphs
- Store edges as metadata: `{"depends_on": ["AuthModule", "UserRepo"]}`

---

## Incremental Indexing

Full re-indexing is expensive. Use `git diff` to index only changes:

```python
import subprocess

def get_changed_files(since_commit: str) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", since_commit, "HEAD"],
        capture_output=True, text=True,
    )
    return [f for f in result.stdout.splitlines()
            if not f.startswith("vendor/")]

def incremental_index(collection, since_commit: str):
    changed = get_changed_files(since_commit)
    for file_path in changed:
        collection.delete(where={"file_path": file_path})
        chunks = parse_and_chunk(file_path)
        collection.add(**prepare_batch(chunks))
```

---

## RAG for Documentation Sources

Index more than just source code:

| Source | Chunking Strategy | Value |
|--------|-------------------|-------|
| READMEs / design docs | Section-level by headings | Architecture context |
| API documentation | Endpoint-level | Interface contracts |
| Slack / Teams threads | Thread-level | Decision rationale |
| Jira / Linear tickets | Ticket-level | Requirements context |
| PR reviews | Comment-level | Code review patterns |

**Key**: decision logs and "why" documentation are often more valuable than code itself for answering architectural questions.

---

## RAG vs Fine-Tuning: When to Use Which

| Criteria | RAG | Fine-Tuning |
|----------|-----|-------------|
| Knowledge updates | Instant (re-index) | Requires retraining |
| Cost | Low (embedding + storage) | High (GPU training) |
| Traceability | Citations to source | Black-box answers |
| Private data safety | Data stays in your infra | Data used in training |
| Coding style adoption | Weak | Strong |
| Factual accuracy | High (grounded) | Risk of hallucination |

**Decision guide**:
- Use **RAG** when answers must reference specific files, APIs, or docs
- Use **fine-tuning** when you want the model to internalize coding style or patterns
- Use **both** together for maximum quality: fine-tune for style, RAG for facts

---

## Building the Ingestion Pipeline

```python
from dataclasses import dataclass

@dataclass
class IngestionConfig:
    repo_path: str
    embedding_model: str = "voyage-code-3"
    chunk_strategy: str = "function_level"
    file_patterns: list[str] = None

def ingest(config: IngestionConfig):
    files = discover_files(config.repo_path, config.file_patterns)
    for file_path in files:
        chunks = chunk_file(file_path, config.chunk_strategy)
        enriched = [enrich_chunk(c, file_path) for c in chunks]
        embeddings = embed_batch([c["code"] for c in enriched])
        upsert_to_vector_db(enriched, embeddings)
```

- Run on CI/CD after each merge to `main`
- Store the last indexed commit SHA for incremental updates

---

## Query Construction and Rewriting

Raw user queries often perform poorly. Rewrite them before retrieval:

```python
def rewrite_query(user_query: str, llm) -> list[str]:
    prompt = f"""Generate 3 search queries to find relevant
    source code for this question:
    "{user_query}"
    Include: a code-focused query, a doc-focused query,
    and an error/log-focused query."""
    queries = llm.generate(prompt)
    return queries
```

**Techniques**:
1. Multi-query expansion (generate 3-5 variants)
1. HyDE (Hypothetical Document Embeddings): ask the LLM to write a hypothetical answer, then embed that
1. Step-back prompting: generalize the query first

---

## Retrieval, Re-Ranking, and Context Assembly

```python
def rag_pipeline(query: str, collection, reranker, llm):
    # 1. Retrieve candidates broadly
    candidates = collection.query(
        query_texts=[query], n_results=30
    )
    # 2. Re-rank with a cross-encoder
    reranked = reranker.rank(query, candidates, top_k=8)
    # 3. Assemble context with token budget
    context = assemble_context(reranked, max_tokens=6000)
    # 4. Generate answer
    prompt = f"Given this context:\n{context}\n\nQ: {query}"
    return llm.generate(prompt)
```

- Cross-encoder re-rankers (`ms-marco-MiniLM`) significantly improve precision
- Always enforce a token budget to avoid context overflow

---

## Context Window Budgeting Diagram

![context_window_budgeting_diagram](svg/courses/ai/advanced-ai-powered-development/07_rag_for_development/context_window_budgeting_diagram.svg)

---

## Context Window Budgeting: Allocation Rules

**Budget allocation rules**:
1. Reserve 10-15% for system prompt and instructions
1. Allocate 50-60% for retrieved code chunks
1. Reserve 5-10% for the user query and conversation history
1. Leave 20-30% for the model response generation
- Always count tokens before sending: truncate lowest-ranked chunks first

---

## Prompt Construction Best Practices

```python
def build_prompt(query: str, chunks: list[dict]) -> str:
    context_parts = []
    for c in chunks:
        header = f"# {c['file_path']}:{c['lineno']}"
        context_parts.append(f"{header}\n```\n{c['code']}\n```")
    context = "\n\n".join(context_parts)
    return f"""You are a senior developer assistant.
Use ONLY the following code context to answer.
If the answer is not in the context, say so.

{context}

Question: {query}
Answer:"""
```

- Always include file paths and line numbers for traceability
- Instruct the model to stay grounded in the provided context

---

## Measuring Retrieval Quality

| Metric | What It Measures | Target |
|--------|-----------------|--------|
| `Recall@k` | % of relevant docs in top-k results | > 0.85 |
| `MRR` (Mean Reciprocal Rank) | Rank of first relevant result | > 0.70 |
| `nDCG@k` | Ranking quality weighted by position | > 0.75 |

```python
def recall_at_k(retrieved_ids, relevant_ids, k=10):
    top_k = set(retrieved_ids[:k])
    relevant = set(relevant_ids)
    return len(top_k & relevant) / len(relevant)
```

- Build a golden dataset of 50-100 query/relevant-doc pairs from real developer questions
- Automate evaluation in CI when chunking or embedding config changes

---

## Common RAG Failure Modes and Debugging

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Irrelevant chunks retrieved | Poor chunking boundaries | Switch to AST-based chunking |
| Correct file missed entirely | Embedding model mismatch | Try code-specific embedding model |
| Top result is always the same file | Metadata not diverse enough | Add file-path diversity re-ranking |
| Answer hallucinates despite context | Context too noisy / too much | Reduce `k`, improve re-ranker |
| Exact identifier not found | Vector search misses literals | Enable hybrid search (BM25 + vector) |
| Stale results after code changes | Index not updated | Implement incremental indexing via `git diff` |

**Debugging tip**: log the retrieved chunks alongside every LLM response so you can trace failures back to retrieval vs generation.

---

## Measuring Answer Quality

Retrieval quality alone is insufficient. Measure end-to-end:

1. **Faithfulness**: does the answer only use information from retrieved context?
1. **Relevance**: does the answer address the original question?
1. **Completeness**: does it cover all aspects of the question?

Use frameworks like `ragas` for automated evaluation:

```python
from ragas.metrics import faithfulness, answer_relevancy
from ragas import evaluate

result = evaluate(
    dataset=eval_dataset,
    metrics=[faithfulness, answer_relevancy],
)
print(result)  # {'faithfulness': 0.92, 'answer_relevancy': 0.87}
```

---

## Caching and Performance Optimization

```python
from functools import lru_cache
import hashlib

class EmbeddingCache:
    def __init__(self, cache_dir: str = ".embed_cache"):
        self.cache_dir = cache_dir

    def get_or_embed(self, text: str, embed_fn):
        key = hashlib.sha256(text.encode()).hexdigest()
        cached = self._load(key)
        if cached is not None:
            return cached
        embedding = embed_fn(text)
        self._save(key, embedding)
        return embedding
```

**Optimization strategies**:
1. Cache embeddings on disk keyed by content hash
1. Cache query results with short TTL (5-15 minutes)
1. Use incremental indexing to avoid re-embedding unchanged files
1. Batch embedding calls (process 100+ chunks per API request)
- Typical speedup: 10-50x on re-indexing with warm cache

---

## RAG Pipeline Monitoring in Production

| Metric | What to Track | Alert Threshold |
|--------|--------------|-----------------|
| Retrieval latency (p95) | Time from query to chunks returned | > 500ms |
| End-to-end latency (p95) | Time from query to final answer | > 5s |
| Retrieval hit rate | % of queries with at least 1 relevant chunk | < 80% |
| Relevance drift | Weekly `nDCG@10` on golden dataset | Drop > 5% |
| Index freshness | Time since last incremental index | > 1 hour |

**Implementation checklist**:
1. Log every query, retrieved chunk IDs, and response
1. Track embedding API costs per day/week
1. Set up weekly automated evaluation against golden dataset
1. Monitor vector DB disk usage and query throughput
- Use `Prometheus` + `Grafana` or your existing observability stack

---

## Security and Access Control in RAG

Retrieving code across a large organization requires access boundaries:

1. **Index-level isolation**: separate vector collections per team or repo
1. **Query-time filtering**: attach user permissions as metadata filters
    - Only retrieve chunks the querying user has read access to
1. **Secrets scanning**: strip API keys, tokens, and credentials before indexing
1. **Audit logging**: record who queried what and which chunks were returned

```python
def secure_query(query: str, user: User, collection):
    allowed_repos = get_user_repos(user)
    return collection.query(
        query_texts=[query],
        where={"repo": {"$in": allowed_repos}},
        n_results=10,
    )
```

- Never index `.env`, `credentials.json`, or files in `.gitignore`

---

## Scaling RAG to Large Organizations

| Challenge | Solution |
|-----------|---------|
| Thousands of repositories | Federated indexes: one collection per repo, cross-repo query router |
| Multiple programming languages | Per-language chunking pipelines with shared embedding model |
| Teams with different needs | Scoped indexes with team-specific metadata filters |
| High query volume | Read replicas for vector DB, horizontal scaling |
| Index size (millions of chunks) | Tiered storage: hot (recent) vs cold (archived) indexes |

**Architecture pattern**:
1. Each team owns and maintains their repository index
1. A central query router fans out searches across relevant indexes
1. Results are merged, re-ranked, and filtered by access control
1. Shared embedding model ensures cross-repo semantic consistency

---

## Hands-On: Building a RAG Pipeline from Scratch

Build a working code RAG pipeline in 6 steps using `ChromaDB`:

1. **Install dependencies**:
    - `pip install chromadb tree-sitter sentence-transformers`
1. **Parse your codebase**: walk the repo, extract functions with `tree-sitter`
1. **Generate embeddings**: embed each chunk with `sentence-transformers`
1. **Store in ChromaDB**: upsert chunks with metadata (file path, language, line number)
1. **Query**: embed user question, retrieve top-k chunks, re-rank
1. **Generate answer**: pass retrieved chunks + question to an LLM

```python
import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("nomic-ai/nomic-embed-code-v1")
client = chromadb.PersistentClient(path="./my_rag_index")
collection = client.get_or_create_collection("code")
# Add chunks, query, and build from here
```

- Target: a working prototype in under 60 minutes

---

## Exercise: Evaluate Your RAG with a Golden Dataset

**Goal**: create a reusable evaluation set and measure retrieval quality.

**Steps**:
1. Collect 20 real developer questions about your codebase
1. For each question, manually identify the 1-3 source files/functions that answer it
1. Store as query/document pairs in a JSON file:

```json
[
  {
    "query": "How does authentication middleware validate JWT tokens?",
    "relevant_docs": ["src/middleware/auth.py:validate_jwt"]
  }
]
```

1. Run your RAG pipeline on each query, record retrieved chunk IDs
1. Compute `Recall@5`, `MRR`, and `nDCG@10` against the golden set

**Success criteria**: `Recall@5` > 0.8, `MRR` > 0.6 on your dataset.

---

## Iterating on RAG Performance

Common tuning levers and their impact:

| Lever | When to Adjust |
|-------|---------------|
| Chunk size | Recall is low, chunks too large or too small |
| Chunk overlap | Relevant code split across chunk boundaries |
| Embedding model | Semantic search missing obvious matches |
| Re-ranker | Top results not the most relevant |
| Metadata filters | Too much noise from irrelevant file types |
| Query rewriting | Raw queries too vague or ambiguous |

**Workflow**: measure baseline, change one variable, re-evaluate, repeat.
