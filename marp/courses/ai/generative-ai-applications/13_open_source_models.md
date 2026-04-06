# Working with Open Source Models

---

## Day 4: Open Source Models

```diagram
Today's Roadmap:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 ┌──────────────────────────────────────────┐
 │ 1. Open source model landscape           │
 │ 2. HuggingFace infrastructure            │
 │ 3. Running models locally                │
 │ 4. Parameter Efficient Fine Tuning       │
 │ 5. LoRA, QLoRA, and Prompt Tuning        │
 └──────────────────────────────────────────┘
```

---

## Why Open Source Models?

| Advantage | Explanation |
|-----------|-------------|
| **Privacy** | Data never leaves your infrastructure |
| **Cost** | No per-token API fees (just compute) |
| **Customization** | Full control over model behavior |
| **No vendor lock-in** | Switch providers freely |
| **Offline capability** | Works without internet |
| **Compliance** | Meet data residency requirements |
| **Transparency** | Inspect model weights and architecture |

```misc
Total Cost of Ownership (1M requests/month):
─────────────────────────────────────────────
  GPT-4o API:          ~$5,000-50,000/month
  GPT-4o-mini API:     ~$300-3,000/month
  Self-hosted 70B:     ~$2,000-5,000/month (GPU rental)
  Self-hosted 7B:      ~$200-500/month (single GPU)
```

---

## The Open Source Model Landscape

```diagram
┌──────────────────────────────────────────────────────┐
│            OPEN SOURCE MODEL FAMILIES                 │
├──────────────┬───────┬──────────┬───────────────────┤
│ Family       │ Sizes │ Provider │ License           │
├──────────────┼───────┼──────────┼───────────────────┤
│ LLaMA 3     │ 8B,   │ Meta     │ LLaMA Community   │
│              │ 70B,  │          │ (commercial OK)   │
│              │ 405B  │          │                    │
├──────────────┼───────┼──────────┼───────────────────┤
│ Mistral /   │ 7B,   │ Mistral  │ Apache 2.0        │
│ Mixtral      │ 8x7B, │ AI       │                    │
│              │ 8x22B │          │                    │
├──────────────┼───────┼──────────┼───────────────────┤
│ Qwen 2.5    │ 0.5B- │ Alibaba  │ Apache 2.0        │
│              │ 72B   │          │                    │
├──────────────┼───────┼──────────┼───────────────────┤
│ Gemma 2     │ 2B,   │ Google   │ Gemma license     │
│              │ 9B,   │          │                    │
│              │ 27B   │          │                    │
├──────────────┼───────┼──────────┼───────────────────┤
│ Phi-3       │ 3.8B, │Microsoft │ MIT               │
│              │ 14B   │          │                    │
└──────────────┴───────┴──────────┴───────────────────┘
```

---

## Model Size vs. Hardware Requirements

```misc
Model Size    VRAM Needed     Suitable Hardware
──────────────────────────────────────────────────────
1-3B          2-4 GB          CPU, laptop GPU
7-8B          6-8 GB          RTX 3060/4060 (consumer)
13B           10-16 GB        RTX 3090/4080
30-34B        24-40 GB        RTX 4090 / A6000
70B           40-80 GB        A100 80GB / 2× A6000
70B (4-bit)   24-40 GB        RTX 4090 (quantized!)
405B          200+ GB         8× A100 or more

Quantization reduces memory requirements:
  FP16 (16-bit): Full precision, full VRAM
  INT8 (8-bit):  ~50% VRAM, minimal quality loss
  INT4 (4-bit):  ~25% VRAM, small quality loss
  GGUF/GPTQ:    Optimized quantization formats
```

---

## Running a Model Locally with Transformers

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "meta-llama/Llama-3.1-8B-Instruct"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,    # Half precision
    device_map="auto",             # Auto GPU placement
)

# Generate text
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Explain list comprehensions in Python."},
]

input_ids = tokenizer.apply_chat_template(
    messages, return_tensors="pt"
).to(model.device)

output = model.generate(
    input_ids,
    max_new_tokens=256,
    temperature=0.7,
    do_sample=True,
)

response = tokenizer.decode(output[0][input_ids.shape[-1]:],
                            skip_special_tokens=True)
print(response)
```

---

## Loading Models with Quantization

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",           # NormalFloat4
    bnb_4bit_compute_dtype=torch.float16, # Compute in FP16
    bnb_4bit_use_double_quant=True,       # Double quantization
)

# Load 70B model in 4-bit (~24GB VRAM instead of ~140GB)
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-70B-Instruct",
    quantization_config=bnb_config,
    device_map="auto",
)

# Memory comparison:
# FP32: 70B × 4 bytes  = 280 GB
# FP16: 70B × 2 bytes  = 140 GB
# INT8: 70B × 1 byte   = 70 GB
# INT4: 70B × 0.5 byte = 35 GB
# NF4 + double quant   ≈ 24 GB (with overhead)
```

---

## Using `vLLM` for Production Inference

```python
# vLLM: High-performance inference engine
# pip install vllm

from vllm import LLM, SamplingParams

# Load model with vLLM
llm = LLM(
    model="meta-llama/Llama-3.1-8B-Instruct",
    dtype="float16",
    max_model_len=4096,
    gpu_memory_utilization=0.9,
)

# Batch inference (much faster than sequential)
prompts = [
    "What is machine learning?",
    "Explain neural networks.",
    "What is deep learning?",
]

sampling_params = SamplingParams(
    temperature=0.7,
    max_tokens=256,
    top_p=0.9,
)

outputs = llm.generate(prompts, sampling_params)
for output in outputs:
    print(f"Prompt: {output.prompt[:50]}")
    print(f"Output: {output.outputs[0].text[:100]}\n")

# vLLM benefits: PagedAttention, continuous batching,
# ~10-24× faster than basic HuggingFace generate()
```

---

## Serving Models with OpenAI-Compatible API

```python
# Run vLLM as an OpenAI-compatible server:
# vllm serve meta-llama/Llama-3.1-8B-Instruct --port 8000

# Now use the standard OpenAI client!
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed",
)

response = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[
        {"role": "system", "content": "You are helpful."},
        {"role": "user", "content": "What is PyTorch?"},
    ],
    temperature=0.7,
    max_tokens=200,
)

print(response.choices[0].message.content)

# Benefits:
# - Same code works with OpenAI or local models
# - Easy to switch between providers
# - Compatible with LangChain and other frameworks
```

---

## Ollama — Simplest Local Model Setup

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull and run a model
ollama pull llama3.1:8b
ollama run llama3.1:8b "Explain recursion"

# Run as API server (default port 11434)
ollama serve

# List available models
ollama list
```

```python
# Use Ollama with Python
import requests

response = requests.post("http://localhost:11434/api/chat", json={
    "model": "llama3.1:8b",
    "messages": [
        {"role": "user", "content": "What is a transformer?"}
    ],
    "stream": False,
})
print(response.json()["message"]["content"])

# Or use the OpenAI client
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
```

---

## Using Open Source Models with LangChain

```python
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Using Ollama
llm = ChatOllama(model="llama3.1:8b", temperature=0.7)

# Using HuggingFace
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline

pipe = pipeline(
    "text-generation",
    model="meta-llama/Llama-3.1-8B-Instruct",
    torch_dtype=torch.float16,
    device_map="auto",
)
llm = HuggingFacePipeline(pipeline=pipe)

# Same LangChain code works regardless of model provider
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a Python expert."),
    ("human", "{question}"),
])

chain = prompt | llm | StrOutputParser()
result = chain.invoke({"question": "What are decorators?"})
```

---

## Benchmarking Open Source vs. Closed Source

```misc
Task: Code generation (HumanEval benchmark)

Model              Pass@1    Size      Cost/1M tok
─────────────────────────────────────────────────────
GPT-4o             92.1%     ~200B*    $10 (output)
Claude 3.5 Sonnet  92.0%     ~?        $15 (output)
LLaMA 3.1 405B     89.0%     405B      Self-host
LLaMA 3.1 70B      80.5%     70B       Self-host
Qwen 2.5 72B       86.4%     72B       Self-host
Mistral Large      84.0%     ~123B     $8 (output)
LLaMA 3.1 8B       72.6%     8B        Self-host
Phi-3 14B           82.0%     14B       Self-host
Gemma 2 27B         74.3%     27B       Self-host

Key finding: The gap between open and closed models
is narrowing rapidly. Open 70B models approach
closed model performance on many tasks.
```

---

## Choosing the Right Model

```diagram
Decision Framework:
━━━━━━━━━━━━━━━━━━

Privacy critical? ──YES──> Open source (self-host)
                    │
                    NO
                    │
Budget constrained? ─YES──> Open source or GPT-4o-mini
                    │
                    NO
                    │
Need best quality? ──YES──> GPT-4o / Claude 3.5 Sonnet
                    │
                    NO
                    │
Simple tasks? ──────YES──> Small open source (7-8B)
                    │       or GPT-4o-mini
                    NO
                    │
Complex reasoning? ─YES──> Large open source (70B+)
                            or closed model API
```

---

## Exercise: Running Models Locally

```python
"""
Exercise: Set up and compare local models.

1. Install Ollama and pull 2 models:
   - ollama pull llama3.1:8b
   - ollama pull mistral:7b

2. Send the same 5 prompts to both models:
   a. "Explain the difference between a list and tuple in Python"
   b. "Write a function to find the median of a list"
   c. "What is the time complexity of binary search?"
   d. "Debug: why does 0.1 + 0.2 != 0.3 in Python?"
   e. "Convert this SQL to a pandas operation:
       SELECT name, AVG(score) FROM students GROUP BY name"

3. Compare:
   - Response quality (1-5 rating)
   - Response time
   - Token count

4. Try the same prompts with GPT-4o-mini via API
5. Create a comparison table of results
"""
```

---

## Key Takeaways — Open Source Models

1. Open source models offer **privacy**, **cost savings**, and **full control**
1. **LLaMA 3**, **Mistral**, and **Qwen** lead the open source landscape
1. **Quantization** (4-bit, 8-bit) dramatically reduces memory requirements
1. **vLLM** and **Ollama** make deployment simple
1. **OpenAI-compatible APIs** enable code portability between providers
1. The quality gap between open and closed models is **shrinking rapidly**
1. Model choice depends on task complexity, privacy needs, and budget
1. A 70B 4-bit model on a single GPU can match many API-based models

---

## Model Formats and Quantization Types

```diagram
┌──────────────────────────────────────────────────────┐
│           MODEL FILE FORMATS                         │
├────────────┬─────────────────────────────────────────┤
│ PyTorch    │ .bin / .pt — native PyTorch format      │
│ (.bin)     │ Widely supported, large file sizes       │
├────────────┼─────────────────────────────────────────┤
│ SafeTensors│ .safetensors — safe, fast loading       │
│            │ No code execution risk, faster I/O       │
│            │ Becoming the new standard                │
├────────────┼─────────────────────────────────────────┤
│ GGUF       │ .gguf — llama.cpp format                │
│            │ CPU-optimized, supports quantization     │
│            │ Used by Ollama, LM Studio                │
├────────────┼─────────────────────────────────────────┤
│ GPTQ       │ GPU-optimized quantization              │
│            │ Post-training quantization               │
│            │ Good quality at 4-bit                    │
├────────────┼─────────────────────────────────────────┤
│ AWQ        │ Activation-aware quantization           │
│            │ Better quality than GPTQ at same bits   │
│            │ Preserves important weights              │
├────────────┼─────────────────────────────────────────┤
│ EXL2       │ ExLlamaV2 format                        │
│            │ Flexible per-layer quantization          │
│            │ Fastest inference on GPU                 │
└────────────┴─────────────────────────────────────────┘
```

---

## Quantization Quality Comparison

```misc
Performance retention at different quantization levels:
(Measured on MMLU benchmark, LLaMA 3.1 70B)

Precision    Size    MMLU    Relative Quality
─────────────────────────────────────────────
FP16         140 GB  82.0%   100% (baseline)
INT8         70 GB   81.8%   99.8%
INT4 (GPTQ)  35 GB   80.5%   98.2%
INT4 (AWQ)   35 GB   81.0%   98.8%
INT4 (NF4)   35 GB   81.2%   99.0%
INT3          26 GB   77.5%   94.5%
INT2          18 GB   68.0%   82.9%

Sweet spot: 4-bit quantization
  - 4× smaller than FP16
  - <2% quality loss
  - Significant speedup on modern GPUs
```

---

## Building an Inference Server

```python
# Production inference server with FastAPI + vLLM

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from vllm import LLM, SamplingParams
from typing import List, Optional

app = FastAPI()
llm = LLM(model="meta-llama/Llama-3.1-8B-Instruct",
           dtype="float16", max_model_len=4096)

class ChatRequest(BaseModel):
    messages: List[dict]
    temperature: float = 0.7
    max_tokens: int = 256

class ChatResponse(BaseModel):
    content: str
    tokens_used: int

@app.post("/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    prompt = format_messages(request.messages)
    params = SamplingParams(
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )
    outputs = llm.generate([prompt], params)
    return ChatResponse(
        content=outputs[0].outputs[0].text,
        tokens_used=len(outputs[0].outputs[0].token_ids),
    )

# Run: uvicorn server:app --host 0.0.0.0 --port 8000
```

---

## Model Merging — Combining Expertise

```misc
A technique to combine multiple fine-tuned models:

Model A: Fine-tuned for coding
Model B: Fine-tuned for creative writing
Model C: Fine-tuned for math

MERGING METHODS:
─────────────────────────────────────────
1. Linear merge (average weights)
   W_merged = α·W_A + β·W_B + γ·W_C
   Simple but effective

2. SLERP (Spherical Linear Interpolation)
   Interpolate on the hypersphere
   Better for 2-model merges

3. TIES (Trim, Elect Sign, Merge)
   Only merge significant changes
   Reduces interference between models

4. DARE (Drop And REscale)
   Randomly drop changes, rescale rest
   Works well with 3+ models
```

```python
# Using mergekit
# mergekit-yaml merge.yml --out-path merged_model
```

---

## Speculative Decoding

Use a small model to speed up a large model:

```misc
Standard decoding (slow):
  Large model generates 1 token at a time
  Each token = 1 full forward pass of 70B model

Speculative decoding (fast):
  1. Small model (7B) generates K draft tokens quickly
  2. Large model (70B) verifies ALL K tokens in one pass
  3. Accept correct tokens, reject wrong ones, continue

Example:
  Draft model generates: "The capital of France is Paris"
  Large model verifies in ONE pass:
    "The" ✓ "capital" ✓ "of" ✓ "France" ✓ "is" ✓ "Paris" ✓
  → 6 tokens for the cost of ~2 large model passes

Speedup: 2-3× with no quality loss!
(Quality is identical — only verified tokens are used)
```

---

## Exercise: Model Deployment Pipeline

```python
"""
Exercise: Set up a complete local model deployment.

1. SETUP
   - Install Ollama
   - Pull llama3.1:8b and mistral:7b

2. BENCHMARKING
   Create a test suite with 20 prompts across categories:
   - Factual Q&A (5 prompts)
   - Code generation (5 prompts)
   - Creative writing (5 prompts)
   - Reasoning/math (5 prompts)

3. EVALUATION
   For each model, measure:
   - Response quality (use LLM-as-judge or manual)
   - Average response time
   - Token throughput (tokens/second)
   - Memory usage

4. API SERVER
   - Set up a simple API server
   - Implement request routing (easy tasks → 7B, hard → 8B)
   - Add basic caching for repeated queries

5. REPORT
   Write up your findings: which model for which task?
"""
```

---

## Structured Generation with Local Models

```python
# Force local models to output valid JSON/structured data

from outlines import generate, models

# Load model with outlines
model = models.transformers("mistralai/Mistral-7B-Instruct-v0.3")

# Define schema
from pydantic import BaseModel
from typing import List

class Review(BaseModel):
    sentiment: str  # "positive", "negative", "neutral"
    score: float    # 0.0 to 1.0
    keywords: List[str]

# Generate guaranteed valid structured output
generator = generate.json(model, Review)

result = generator(
    "Analyze this review: 'Great product, fast shipping, "
    "but the packaging was damaged'"
)
print(result)
# Review(sentiment='positive', score=0.7,
#        keywords=['great product', 'fast shipping', 'damaged packaging'])

# The output is GUARANTEED to match the schema
# No parsing errors, no invalid JSON!
```

---

## Running Models on Apple Silicon

```python
# Apple M1/M2/M3 chips can run LLMs efficiently

# Option 1: MLX (Apple's framework)
# pip install mlx mlx-lm

from mlx_lm import load, generate

model, tokenizer = load("mlx-community/Mistral-7B-Instruct-v0.3-4bit")

response = generate(
    model, tokenizer,
    prompt="Explain transformers in 3 sentences.",
    max_tokens=200,
)
print(response)

# MLX performance on M3 Max (128GB):
# Mistral 7B 4-bit:  ~40 tokens/second
# LLaMA 3.1 8B 4-bit: ~35 tokens/second
# LLaMA 3.1 70B 4-bit: ~8 tokens/second

# Option 2: Ollama (uses Metal acceleration automatically)
# ollama run llama3.1:8b
# Performance comparable to MLX

# Option 3: llama.cpp (C++ with Metal support)
# Most memory-efficient option
# Can run 70B models on 64GB M-series Macs
```

---

## Model Evaluation at Scale

```python
from lm_eval import evaluator, tasks

# Use lm-evaluation-harness for standardized benchmarks
results = evaluator.simple_evaluate(
    model="hf",
    model_args="pretrained=meta-llama/Llama-3.1-8B-Instruct",
    tasks=["mmlu", "hellaswag", "arc_challenge", "truthfulqa_mc2"],
    batch_size=4,
    device="cuda",
)

# Print results
for task, metrics in results["results"].items():
    print(f"{task}:")
    for metric, value in metrics.items():
        if isinstance(value, float):
            print(f"  {metric}: {value:.4f}")

# Compare multiple models
models_to_compare = [
    "meta-llama/Llama-3.1-8B-Instruct",
    "mistralai/Mistral-7B-Instruct-v0.3",
    "google/gemma-2-9b-it",
]

# Run the same benchmarks on each model
# and create a comparison table
```

---

## Model Licensing — Understanding the Terms

```diagram
┌──────────────────────────────────────────────────────┐
│              MODEL LICENSE COMPARISON                  │
├──────────────┬───────────────────────────────────────┤
│ Apache 2.0   │ ✓ Commercial use                      │
│ (Mistral,    │ ✓ Modification and distribution       │
│  Qwen)       │ ✓ Patent grant                        │
│              │ ✓ No royalties                        │
│              │ Must include license notice            │
├──────────────┼───────────────────────────────────────┤
│ MIT          │ ✓ Nearly unrestricted use             │
│ (Phi-3)      │ ✓ Commercial use                      │
│              │ ✓ Minimal obligations                 │
├──────────────┼───────────────────────────────────────┤
│ LLaMA 3.1   │ ✓ Commercial use (with conditions)    │
│ Community    │ ✓ Modification                        │
│              │ ✗ Must accept Meta's terms             │
│              │ ✗ Monthly active users > 700M:        │
│              │   need Meta's permission               │
├──────────────┼───────────────────────────────────────┤
│ Gemma        │ ✓ Commercial use                      │
│ (Google)     │ ✗ Cannot use to train competing models│
│              │ ✗ Must accept Google's terms           │
└──────────────┴───────────────────────────────────────┘
```

---

## Deploying with Docker

```dockerfile
# Dockerfile for LLM inference server
FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

# Install Python and dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install vllm fastapi uvicorn

# Copy your server code
COPY server.py /app/server.py

# Download model at build time (or mount at runtime)
# RUN huggingface-cli download meta-llama/Llama-3.1-8B-Instruct

# Expose API port
EXPOSE 8000

# Run the server
CMD ["python3", "-m", "vllm.entrypoints.openai.api_server", \
     "--model", "meta-llama/Llama-3.1-8B-Instruct", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--dtype", "float16"]
```

```bash
# Build and run
docker build -t llm-server .
docker run --gpus all -p 8000:8000 llm-server

# Now accessible at http://localhost:8000/v1/chat/completions
# Compatible with any OpenAI client!
```

---

## Embedding Models — Open Source Options

```diagram
┌────────────────────────────────┬──────┬───────────┬──────────┐
│ Model                          │ Dims │ MTEB Avg  │ Size     │
├────────────────────────────────┼──────┼───────────┼──────────┤
│ all-MiniLM-L6-v2               │ 384  │ 56.3      │ 80 MB    │
│ bge-large-en-v1.5              │ 1024 │ 64.2      │ 1.3 GB   │
│ e5-large-v2                    │ 1024 │ 62.0      │ 1.3 GB   │
│ gte-Qwen2-7B-instruct         │ 3584 │ 72.1      │ 14 GB    │
│ nomic-embed-text-v1.5          │ 768  │ 62.3      │ 548 MB   │
│ text-embedding-3-small (OpenAI)│ 1536 │ 62.3      │ API only │
│ text-embedding-3-large (OpenAI)│ 3072 │ 64.6      │ API only │
└────────────────────────────────┴──────┴───────────┴──────────┘

Key insight: Open source embedding models match or
exceed OpenAI embeddings on many tasks, and you can
run them locally with zero API cost.

For RAG applications:
  - Budget: all-MiniLM-L6-v2 (fast, decent quality)
  - Quality: bge-large-en-v1.5 (best quality/size ratio)
  - Maximum: gte-Qwen2-7B (highest quality, needs GPU)
```

---

## Multi-GPU Inference with Model Parallelism

```python
# When a model doesn't fit on one GPU

from transformers import AutoModelForCausalLM

# Automatic device mapping
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-70B-Instruct",
    torch_dtype=torch.float16,
    device_map="auto",       # Automatically split across GPUs
)

# Check how layers are distributed
print(model.hf_device_map)
# {
#   'model.embed_tokens': 0,       # GPU 0
#   'model.layers.0': 0,            # GPU 0
#   'model.layers.1': 0,            # GPU 0
#   ...
#   'model.layers.40': 1,           # GPU 1
#   'model.layers.41': 1,           # GPU 1
#   ...
#   'model.norm': 1,                # GPU 1
#   'lm_head': 1,                   # GPU 1
# }

# Custom device map for specific layer placement
device_map = {
    "model.embed_tokens": "cuda:0",
    **{f"model.layers.{i}": f"cuda:{i // 40}" for i in range(80)},
    "model.norm": "cuda:1",
    "lm_head": "cuda:1",
}
```
