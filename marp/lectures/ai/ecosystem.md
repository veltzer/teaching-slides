---
tags:
- concepts:ai
- concepts:llm
- concepts:tools
- concepts:agents
level: intermediate
category: ai
audience:
- audiences:developers

---

# The LLM Ecosystem
## A Survey of the Tools Around Large Language Models
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## Overview

![title](svg/lectures/ai/ecosystem/title.svg)

---

## What This Lecture Covers

1. Reaching models: SDKs, gateways, and local runners
1. Frameworks for building agents and applications
1. Structured output and tool protocols
1. RAG: parsers, embeddings, and vector databases
1. Coding assistants and data-analysis tools
1. Quality: evaluation, observability, guardrails
1. Fine-tuning, UIs, low-code builders — and how to choose

---

## The Model Alone Is Not a Product

- An LLM API gives you one thing: tokens in, tokens out
- Everything else is *your* problem: data, tools, UI, testing, monitoring
- A whole industry of tooling has grown around that gap
- Some of it is essential, some is a thin wrapper you could write in a day
- This lecture maps the landscape so you can tell which is which

---

## The Ecosystem at a Glance

![ecosystem_map](svg/lectures/ai/ecosystem/ecosystem_map.svg)

---

## How to Read This Survey

- The ecosystem churns fast — specific names will age, categories will not
- Every category answers a *recurring engineering problem*
- Learn the problem first; the tool of the month is then easy to evaluate
- Popularity is not fitness: many famous tools are famous for being early
- For each category we name a few representative tools, not all of them

---

## Talking to a Model: Provider SDKs

- Every provider ships an official SDK: Anthropic, OpenAI, Google, Mistral
- They wrap HTTP with retries, streaming, typed requests and responses
- The APIs converged on the same shape: messages, tools, streaming chunks
- Thin by design — you can always drop down to raw HTTP
- Start here: for a single provider, the SDK alone is often enough

---

## One API for Many Models

![gateway](svg/lectures/ai/ecosystem/gateway.svg)

---

## Gateways and Routers

- **LiteLLM** — one client API, ~100 providers behind it; also a proxy server
- **OpenRouter** — a hosted marketplace: one key, many commercial models
- Gateways add: failover, load balancing, spend caps, per-team keys
- They decouple your code from the provider — switching becomes config
- The price: one more moving part between you and the model

---

## Why Run Models Locally

- Privacy: the data never leaves your machine or your network
- Cost: a downloaded open-weights model has no per-token bill
- Latency and offline work: no round trip to a data center
- Freedom to experiment: any checkpoint, any quantization, any patch
- The trade: smaller models, your hardware, your operations

---

## Local Runners

- **Ollama** — one-command model pull and serve; the local default today
- **llama.cpp** — the engine underneath much of it; runs on nearly anything
- **LM Studio** — desktop GUI for downloading and chatting with models
- All expose an OpenAI-compatible HTTP endpoint — tools plug in unchanged
- Quantization (4-bit, 8-bit) is what makes laptops viable at all

---

## From Laptop to Cluster

![serving_spectrum](svg/lectures/ai/ecosystem/serving_spectrum.svg)

---

## Serving at Scale

- Production inference is a throughput problem, not a chat problem
- **vLLM** — the standard open server: paged attention, continuous batching
- **SGLang** and **TensorRT-LLM** — same niche, different trade-offs
- These saturate GPUs by batching many requests into one forward pass
- If you self-host for real traffic, you end up on one of these

---

## Hugging Face: The Model Registry

- The de-facto hub: models, datasets, tokenizers, leaderboards
- `transformers` is the reference library for loading and running weights
- Spaces host demos; the hub hosts fine-tunes of every popular base model
- Think "GitHub for models" — including the long tail of forks
- Even if you never train, you will download from here

---

## Frameworks for Building Agents

![agent_frameworks](svg/lectures/ai/ecosystem/agent_frameworks.svg)

---

## The Big Toolkits

- **LangChain** — the first mover: chains, tools, integrations for everything
- **LangGraph** — its successor for agents: explicit state machines and graphs
- **LlamaIndex** — same breadth, strongest around data and retrieval
- Strength: hundreds of ready integrations and patterns
- Weakness: layers of abstraction between you and the actual prompt

---

## Multi-Agent Frameworks

- **CrewAI** — role-based teams: researcher, writer, reviewer with tasks
- **AutoGen** — Microsoft's take: agents that talk to each other in chats
- They package orchestration: handoffs, shared memory, turn-taking
- Impressive demos; in production the coordination cost is real
- Reach for them only after a single agent has hit a genuine wall

---

## Code-First and Typed

- **Pydantic AI** — agents defined with Python types; validation built in
- **smolagents** — Hugging Face's minimal agents, tools as plain functions
- **Vercel AI SDK** — the TypeScript equivalent for web applications
- Philosophy: a thin, readable layer over the provider API
- You keep control of the loop; the library handles the plumbing

---

## Vendor Agent SDKs

- **Claude Agent SDK** — the loop behind Claude Code, offered as a library
- **OpenAI Agents SDK** — first-party agents, handoffs, and tracing
- Vendor SDKs track their platform's newest features on day one
- Best-integrated option if you are committed to that provider
- The obvious cost: moving away later means rewriting the harness

---

## Choosing an Agent Framework

1. Prototype with the raw SDK first — learn what the loop really does
1. Adopt a framework for its integrations, not its abstractions
1. Prefer libraries you can read in an afternoon
1. Check that you can always see the exact prompt that was sent
1. Any framework you cannot debug at 2 AM is the wrong framework

---

## Structured Output

![structured_output](svg/lectures/ai/ecosystem/structured_output.svg)

---

## Structured Output Libraries

- The problem: you need JSON matching a schema, not prose
- **Instructor** — define a Pydantic model; it prompts, validates, retries
- **Outlines** — constrains local model *decoding* so output must match
- Providers now offer native structured output modes as well
- Whatever the tool: always validate — never trust, always parse

---

## MCP: Sharing Tools Across Agents

- The Model Context Protocol standardizes how tools are served to models
- A server exposes tools and resources; any MCP client can use them
- Write the integration once — every agent host reuses it
- Servers already exist for databases, browsers, filesystems, SaaS APIs
- MCP is doing for tools what HTTP did for documents

---

## RAG: The Standard Pipeline

![rag_pipeline](svg/lectures/ai/ecosystem/rag_pipeline.svg)

---

## Document Parsing

- Real knowledge lives in PDFs, Office files, HTML, scans — not clean text
- **unstructured** — one API to extract text and layout from many formats
- **Docling** — IBM's parser, strong on tables and complex PDF layout
- **marker** — fast PDF to markdown conversion
- Parsing quality bounds RAG quality — garbage in, garbage retrieved

---

## Chunking and Embeddings

- Documents are split into chunks; each chunk becomes a vector
- Chunk size is a real tuning knob: too small loses context, too big blurs
- Embedding models are a separate market: provider APIs and open models
- The **MTEB leaderboard** ranks embedding models on retrieval quality
- Changing the embedding model means re-indexing everything — choose early

---

## Vector Databases

- **Chroma** — embedded and simple; the prototyping default
- **Qdrant**, **Weaviate**, **Milvus** — standalone servers built for scale
- **FAISS** — not a database, a library: raw similarity search in memory
- **Pinecone** — the managed SaaS option
- All do the same core job: nearest-neighbor search over vectors, with filters

---

## When Postgres Is Enough

- **pgvector** adds a vector type and similarity indexes to Postgres
- Your vectors live next to your relational data — one database, one backup
- Joins, transactions, and access control come for free
- For most applications short of huge scale, this is the sane choice
- Adopt a dedicated vector store when measurements say you must

---

## RAG Frameworks

- **LlamaIndex** — ingestion, indexing, and query engines end to end
- **Haystack** — pipeline-oriented, mature, strong in production use
- **RAGFlow** and friends — full RAG products with UI and pipelines built in
- They save weeks at the start; the ceiling is their flexibility
- A plain pipeline you own is still a respectable alternative

---

## LLMs for Writing Code

- Autocomplete assistants: **GitHub Copilot** — suggestions inside the editor
- AI-first editors: **Cursor**, **Windsurf** — the IDE itself talks to the model
- Terminal agents: **Claude Code**, **Aider**, **Codex** — they edit, run, iterate
- The shift: from completing lines to executing whole tasks
- Same skills apply: clear specs, small steps, review everything

---

## Data Analysis: The Code Interpreter Pattern

![data_analysis](svg/lectures/ai/ecosystem/data_analysis.svg)

---

## Data Analysis Tools

- The winning pattern: the model writes pandas/SQL, a sandbox runs it
- Numbers come from executed code — the model never does the arithmetic
- **PandasAI** — ask questions of a dataframe in natural language
- **Jupyter AI** — the assistant living inside your notebooks
- Provider "code interpreter" and "analysis" modes package the same loop

---

## Text-to-SQL

- The dream: business users ask questions, the model writes the SQL
- **Vanna** and similar tools train on your schema and past queries
- Works well on clean schemas with good names; struggles on legacy mess
- Guard it: read-only connections, row limits, query review
- Best deployed as an analyst's accelerator, not an unsupervised oracle

---

## Sandboxes for Generated Code

- Never run model-written code in your own process — ever
- **E2B** and similar services sell disposable cloud sandboxes for agents
- Self-hosted route: containers or microVMs with no network by default
- Time limits, memory limits, and a throwaway filesystem are the baseline
- The sandbox is what turns "the model writes code" into a safe feature

---

## Testing LLM Applications

- Outputs are stochastic — classic assert-equal testing does not survive
- You need: a task set, a grading method, and a habit of running both
- Regressions come from everywhere: prompts, models, retrieval, tools
- Evals are to LLM apps what unit tests are to code
- The tools below exist to make that loop cheap enough to actually run

---

## Evaluation Tools

- **promptfoo** — declarative test suites for prompts; diffs across models
- **Ragas** — RAG-specific metrics: faithfulness, relevance, recall
- **DeepEval** — pytest-style assertions over LLM outputs
- **lm-evaluation-harness** — academic benchmarks for comparing models
- Common trick: an LLM judges the output — cheap, useful, and imperfect

---

## Observability and Tracing

![observability](svg/lectures/ai/ecosystem/observability.svg)

---

## Tracing Platforms

- **LangSmith** — traces, datasets, and evals from the LangChain team
- **Langfuse** — open-source tracing and prompt management; self-hostable
- **Arize Phoenix**, **W&B Weave** — same category, different pedigrees
- OpenTelemetry now has GenAI conventions — vendor-neutral trace data
- Whatever you pick: if you cannot see the trace, you cannot debug it

---

## Prompt Management

- Prompts are code: they need versions, reviews, and rollbacks
- Registries store prompts outside the binary, with history and labels
- Deploy a prompt change without redeploying the application
- Every change should link to an eval run — numbers, not vibes
- Most tracing platforms bundle this; git alone also works fine

---

## Guardrails

- Input side: block injection attempts, off-topic use, secrets in prompts
- Output side: schema checks, toxicity filters, PII redaction
- **Guardrails AI** — declarative validators on inputs and outputs
- **NeMo Guardrails** — conversation-level rails from NVIDIA
- **Llama Guard** — an open model that classifies content for safety
- Layer them: guardrails complement, never replace, least privilege

---

## When Prompting Is Not Enough

![finetuning](svg/lectures/ai/ecosystem/finetuning.svg)

---

## Fine-Tuning Tools

- **PEFT / LoRA** — train small adapter matrices, not the whole model
- **Axolotl** and **LLaMA-Factory** — config-driven training pipelines
- **Unsloth** — the same, tuned for speed on a single GPU
- Providers offer hosted fine-tuning where weights never reach you
- Rule of thumb: exhaust prompting and RAG first — they are cheaper to undo

---

## Building a UI Fast

- **Streamlit** and **Gradio** — a data app or demo in an afternoon of Python
- **Chainlit** — the same idea, purpose-built for chat interfaces
- Gradio powers most Hugging Face Spaces demos
- Perfect for internal tools and proofs of concept
- For customer-facing products you will still build a real frontend

---

## Ready-Made Chat Frontends

- **Open WebUI** — self-hosted chat UI, pairs naturally with Ollama
- **LibreChat** — one chat interface over many providers, multi-user
- Auth, history, model switching, file upload — already built
- Deploying one of these beats writing yet another chat page
- Good fit: giving a team internal access to models with control

---

## Low-Code Builders

- **Dify**, **Flowise**, **Langflow** — drag-and-drop LLM pipelines with hosting
- **n8n** — general automation platform with strong LLM nodes
- Great for prototypes and for non-developers who own a workflow
- The ceiling arrives fast: version control, testing, and debugging suffer
- A common path: prototype in low-code, rebuild in code when it sticks

---

## Cost Control and Caching

- Token spend is the cloud bill of this decade — meter it per feature
- Gateways enforce budgets, quotas, and per-team keys
- Prompt caching: keep the stable prefix identical and reuse it
- Semantic caching returns yesterday's answer to today's similar question
- Route by difficulty: cheap model by default, strong model on demand

---

## Speech and Beyond Text

- **Whisper** — open speech-to-text; runs locally, many optimized forks
- Text-to-speech: ElevenLabs and a fast-moving field of open models
- Voice agents: speech in, LLM in the middle, speech out — latency is king
- Image generation and vision models plug into the same app patterns
- Multimodal pipelines reuse everything in this lecture — plus a codec

---

## A Sane Default Stack

1. Provider SDK, straight — no framework until it earns its place
1. Postgres + pgvector for retrieval; a parser like unstructured in front
1. Instructor (or native structured output) for anything machine-read
1. Langfuse or LangSmith for traces; promptfoo for evals in CI
1. Streamlit or a ready chat frontend for the first UI
1. Add gateways, fine-tuning, and multi-agent only under measured pressure

---

## Build or Adopt?

- Adopt where the problem is generic: tracing, serving, vector search
- Build where the problem is yours: prompts, tools, evals, domain logic
- Wrappers age fast; protocols and databases age slowly
- Every dependency is a bet on someone else's roadmap
- The skill being tested is judgement, not tool collection

---

## Keeping Up with the Churn

- Half the names in this lecture will fade within a few years — expect it
- The categories are stable: access, orchestration, retrieval, quality, UI
- Follow problems, not products: "how do we eval?" outlives any vendor
- Re-evaluate the stack on a schedule, not on every launch announcement
- Boring, replaceable components are the ones that survive churn

---

## Summary

- The model is the engine; the ecosystem is everything around it
- Access and serving: SDKs, gateways, Ollama, vLLM
- Building: agent frameworks, structured output, MCP, RAG stacks
- Trust: evals, tracing, guardrails — the difference from a demo
- Choose few tools, understand them deeply, keep the exits open

---

## Questions?

- Map the category to the problem, and the tool of the month is easy
- Start thin, measure, and let pain justify every new dependency
- The best stack is the one your team can debug

## Thank You
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)
