# Working with Open Source Models

---

## Day 4: Open Source Models

<svg xmlns="http://www.w3.org/2000/svg" width="520" height="200" font-family="sans-serif">
  <rect x="0" y="0" width="520" height="200" fill="#e3f2fd" rx="6" stroke="#333" stroke-width="1.5"/>
  <text x="260" y="28" text-anchor="middle" font-size="16" font-weight="bold" fill="#1565c0">Today's Roadmap</text>
  <line x1="20" y1="38" x2="500" y2="38" stroke="#1565c0" stroke-width="1.5"/>
  <text x="40" y="62" font-size="14" fill="#222">1. Open source model landscape</text>
  <text x="40" y="86" font-size="14" fill="#222">2. HuggingFace infrastructure</text>
  <text x="40" y="110" font-size="14" fill="#222">3. Running models locally</text>
  <text x="40" y="134" font-size="14" fill="#222">4. Parameter Efficient Fine Tuning</text>
  <text x="40" y="158" font-size="14" fill="#222">5. LoRA, QLoRA, and Prompt Tuning</text>
  <circle cx="24" cy="58" r="4" fill="#1565c0"/>
  <circle cx="24" cy="82" r="4" fill="#1565c0"/>
  <circle cx="24" cy="106" r="4" fill="#1565c0"/>
  <circle cx="24" cy="130" r="4" fill="#1565c0"/>
  <circle cx="24" cy="154" r="4" fill="#1565c0"/>
</svg>

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

<svg xmlns="http://www.w3.org/2000/svg" width="600" height="190" font-family="sans-serif">
  <defs>
    <marker id="ah2" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
    </marker>
  </defs>
  <rect x="0" y="0" width="600" height="190" fill="#fff3e0" rx="6" stroke="#333" stroke-width="1.5"/>
  <text x="300" y="26" text-anchor="middle" font-size="15" font-weight="bold" fill="#e65100">Total Cost of Ownership (1M requests/month)</text>
  <line x1="20" y1="34" x2="580" y2="34" stroke="#e65100" stroke-width="1.5"/>
  <!-- Header row -->
  <rect x="20" y="42" width="250" height="28" fill="#ffe0b2" rx="3" stroke="#ccc" stroke-width="1"/>
  <rect x="272" y="42" width="308" height="28" fill="#ffe0b2" rx="3" stroke="#ccc" stroke-width="1"/>
  <text x="145" y="61" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Option</text>
  <text x="426" y="61" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Cost</text>
  <!-- Rows -->
  <rect x="20" y="72" width="250" height="26" fill="#fff8f0" rx="2" stroke="#ddd" stroke-width="1"/>
  <rect x="272" y="72" width="308" height="26" fill="#fff8f0" rx="2" stroke="#ddd" stroke-width="1"/>
  <text x="35" y="90" font-size="13" fill="#222">GPT-4o API</text>
  <text x="287" y="90" font-size="13" fill="#222">~$5,000–50,000/month</text>
  <rect x="20" y="100" width="250" height="26" fill="#fff3e0" rx="2" stroke="#ddd" stroke-width="1"/>
  <rect x="272" y="100" width="308" height="26" fill="#fff3e0" rx="2" stroke="#ddd" stroke-width="1"/>
  <text x="35" y="118" font-size="13" fill="#222">GPT-4o-mini API</text>
  <text x="287" y="118" font-size="13" fill="#222">~$300–3,000/month</text>
  <rect x="20" y="128" width="250" height="26" fill="#fff8f0" rx="2" stroke="#ddd" stroke-width="1"/>
  <rect x="272" y="128" width="308" height="26" fill="#fff8f0" rx="2" stroke="#ddd" stroke-width="1"/>
  <text x="35" y="146" font-size="13" fill="#222">Self-hosted 70B</text>
  <text x="287" y="146" font-size="13" fill="#222">~$2,000–5,000/month (GPU rental)</text>
  <rect x="20" y="156" width="250" height="26" fill="#fff3e0" rx="2" stroke="#ddd" stroke-width="1"/>
  <rect x="272" y="156" width="308" height="26" fill="#fff3e0" rx="2" stroke="#ddd" stroke-width="1"/>
  <text x="35" y="174" font-size="13" fill="#222">Self-hosted 7B</text>
  <text x="287" y="174" font-size="13" fill="#222">~$200–500/month (single GPU)</text>
</svg>

---

## The Open Source Model Landscape

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="360" font-family="sans-serif">
  <!-- Column widths: 150, 100, 110, 270 = 630, offset x=15 -->
  <rect x="0" y="0" width="660" height="360" fill="#f0f4f8" rx="6" stroke="#333" stroke-width="1.5"/>
  <!-- Title -->
  <rect x="0" y="0" width="660" height="36" fill="#1565c0" rx="6" stroke="#333" stroke-width="1.5"/>
  <rect x="0" y="18" width="660" height="18" fill="#1565c0"/>
  <text x="330" y="24" text-anchor="middle" font-size="15" font-weight="bold" fill="white">OPEN SOURCE MODEL FAMILIES</text>
  <!-- Header row -->
  <rect x="15" y="42" width="150" height="30" fill="#bbdefb" stroke="#333" stroke-width="1"/>
  <rect x="165" y="42" width="100" height="30" fill="#bbdefb" stroke="#333" stroke-width="1"/>
  <rect x="265" y="42" width="110" height="30" fill="#bbdefb" stroke="#333" stroke-width="1"/>
  <rect x="375" y="42" width="270" height="30" fill="#bbdefb" stroke="#333" stroke-width="1"/>
  <text x="90" y="62" text-anchor="middle" font-size="13" font-weight="bold" fill="#222">Family</text>
  <text x="215" y="62" text-anchor="middle" font-size="13" font-weight="bold" fill="#222">Sizes</text>
  <text x="320" y="62" text-anchor="middle" font-size="13" font-weight="bold" fill="#222">Provider</text>
  <text x="510" y="62" text-anchor="middle" font-size="13" font-weight="bold" fill="#222">License</text>
  <!-- LLaMA 3 row (3 lines) -->
  <rect x="15" y="72" width="150" height="56" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <rect x="165" y="72" width="100" height="56" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <rect x="265" y="72" width="110" height="56" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <rect x="375" y="72" width="270" height="56" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <text x="30" y="96" font-size="13" fill="#222">LLaMA 3</text>
  <text x="180" y="89" font-size="13" fill="#222">8B,</text>
  <text x="180" y="107" font-size="13" fill="#222">70B, 405B</text>
  <text x="280" y="100" font-size="13" fill="#222">Meta</text>
  <text x="390" y="89" font-size="13" fill="#222">LLaMA Community</text>
  <text x="390" y="107" font-size="13" fill="#555">(commercial OK)</text>
  <!-- Mistral row -->
  <rect x="15" y="128" width="150" height="56" fill="#f5f5f5" stroke="#333" stroke-width="1"/>
  <rect x="165" y="128" width="100" height="56" fill="#f5f5f5" stroke="#333" stroke-width="1"/>
  <rect x="265" y="128" width="110" height="56" fill="#f5f5f5" stroke="#333" stroke-width="1"/>
  <rect x="375" y="128" width="270" height="56" fill="#f5f5f5" stroke="#333" stroke-width="1"/>
  <text x="30" y="148" font-size="13" fill="#222">Mistral /</text>
  <text x="30" y="165" font-size="13" fill="#222">Mixtral</text>
  <text x="180" y="148" font-size="13" fill="#222">7B, 8x7B,</text>
  <text x="180" y="166" font-size="13" fill="#222">8x22B</text>
  <text x="280" y="148" font-size="13" fill="#222">Mistral</text>
  <text x="280" y="166" font-size="13" fill="#222">AI</text>
  <text x="390" y="156" font-size="13" fill="#222">Apache 2.0</text>
  <!-- Qwen row -->
  <rect x="15" y="184" width="150" height="42" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <rect x="165" y="184" width="100" height="42" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <rect x="265" y="184" width="110" height="42" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <rect x="375" y="184" width="270" height="42" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <text x="30" y="204" font-size="13" fill="#222">Qwen 2.5</text>
  <text x="180" y="200" font-size="13" fill="#222">0.5B–72B</text>
  <text x="280" y="204" font-size="13" fill="#222">Alibaba</text>
  <text x="390" y="204" font-size="13" fill="#222">Apache 2.0</text>
  <!-- Gemma row -->
  <rect x="15" y="226" width="150" height="56" fill="#f5f5f5" stroke="#333" stroke-width="1"/>
  <rect x="165" y="226" width="100" height="56" fill="#f5f5f5" stroke="#333" stroke-width="1"/>
  <rect x="265" y="226" width="110" height="56" fill="#f5f5f5" stroke="#333" stroke-width="1"/>
  <rect x="375" y="226" width="270" height="56" fill="#f5f5f5" stroke="#333" stroke-width="1"/>
  <text x="30" y="246" font-size="13" fill="#222">Gemma 2</text>
  <text x="180" y="242" font-size="13" fill="#222">2B, 9B,</text>
  <text x="180" y="260" font-size="13" fill="#222">27B</text>
  <text x="280" y="254" font-size="13" fill="#222">Google</text>
  <text x="390" y="254" font-size="13" fill="#222">Gemma license</text>
  <!-- Phi-3 row -->
  <rect x="15" y="282" width="150" height="42" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <rect x="165" y="282" width="100" height="42" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <rect x="265" y="282" width="110" height="42" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <rect x="375" y="282" width="270" height="42" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <text x="30" y="302" font-size="13" fill="#222">Phi-3</text>
  <text x="180" y="298" font-size="13" fill="#222">3.8B, 14B</text>
  <text x="280" y="302" font-size="13" fill="#222">Microsoft</text>
  <text x="390" y="302" font-size="13" fill="#222">MIT</text>
  <!-- Bottom border line -->
  <rect x="15" y="324" width="630" height="2" fill="#333"/>
</svg>

---

## Model Size vs. Hardware Requirements

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="390" font-family="sans-serif">
  <rect x="0" y="0" width="660" height="390" fill="#f0f4f8" rx="6" stroke="#333" stroke-width="1.5"/>
  <!-- Header row -->
  <rect x="10" y="10" width="200" height="30" fill="#b0bec5" stroke="#333" stroke-width="1"/>
  <rect x="210" y="10" width="160" height="30" fill="#b0bec5" stroke="#333" stroke-width="1"/>
  <rect x="370" y="10" width="280" height="30" fill="#b0bec5" stroke="#333" stroke-width="1"/>
  <text x="110" y="30" text-anchor="middle" font-size="13" font-weight="bold" fill="#222">Model Size</text>
  <text x="290" y="30" text-anchor="middle" font-size="13" font-weight="bold" fill="#222">VRAM Needed</text>
  <text x="510" y="30" text-anchor="middle" font-size="13" font-weight="bold" fill="#222">Suitable Hardware</text>
  <!-- Data rows -->
  <rect x="10" y="40" width="200" height="28" fill="#e8f5e9" stroke="#ddd" stroke-width="1"/>
  <rect x="210" y="40" width="160" height="28" fill="#e8f5e9" stroke="#ddd" stroke-width="1"/>
  <rect x="370" y="40" width="280" height="28" fill="#e8f5e9" stroke="#ddd" stroke-width="1"/>
  <text x="22" y="59" font-size="13" fill="#222">1–3B</text>
  <text x="222" y="59" font-size="13" fill="#222">2–4 GB</text>
  <text x="382" y="59" font-size="13" fill="#222">CPU, laptop GPU</text>
  <rect x="10" y="68" width="200" height="28" fill="#f5f5f5" stroke="#ddd" stroke-width="1"/>
  <rect x="210" y="68" width="160" height="28" fill="#f5f5f5" stroke="#ddd" stroke-width="1"/>
  <rect x="370" y="68" width="280" height="28" fill="#f5f5f5" stroke="#ddd" stroke-width="1"/>
  <text x="22" y="87" font-size="13" fill="#222">7–8B</text>
  <text x="222" y="87" font-size="13" fill="#222">6–8 GB</text>
  <text x="382" y="87" font-size="13" fill="#222">RTX 3060/4060 (consumer)</text>
  <rect x="10" y="96" width="200" height="28" fill="#e8f5e9" stroke="#ddd" stroke-width="1"/>
  <rect x="210" y="96" width="160" height="28" fill="#e8f5e9" stroke="#ddd" stroke-width="1"/>
  <rect x="370" y="96" width="280" height="28" fill="#e8f5e9" stroke="#ddd" stroke-width="1"/>
  <text x="22" y="115" font-size="13" fill="#222">13B</text>
  <text x="222" y="115" font-size="13" fill="#222">10–16 GB</text>
  <text x="382" y="115" font-size="13" fill="#222">RTX 3090/4080</text>
  <rect x="10" y="124" width="200" height="28" fill="#f5f5f5" stroke="#ddd" stroke-width="1"/>
  <rect x="210" y="124" width="160" height="28" fill="#f5f5f5" stroke="#ddd" stroke-width="1"/>
  <rect x="370" y="124" width="280" height="28" fill="#f5f5f5" stroke="#ddd" stroke-width="1"/>
  <text x="22" y="143" font-size="13" fill="#222">30–34B</text>
  <text x="222" y="143" font-size="13" fill="#222">24–40 GB</text>
  <text x="382" y="143" font-size="13" fill="#222">RTX 4090 / A6000</text>
  <rect x="10" y="152" width="200" height="28" fill="#e8f5e9" stroke="#ddd" stroke-width="1"/>
  <rect x="210" y="152" width="160" height="28" fill="#e8f5e9" stroke="#ddd" stroke-width="1"/>
  <rect x="370" y="152" width="280" height="28" fill="#e8f5e9" stroke="#ddd" stroke-width="1"/>
  <text x="22" y="171" font-size="13" fill="#222">70B</text>
  <text x="222" y="171" font-size="13" fill="#222">40–80 GB</text>
  <text x="382" y="171" font-size="13" fill="#222">A100 80GB / 2× A6000</text>
  <rect x="10" y="180" width="200" height="28" fill="#fff3e0" stroke="#ddd" stroke-width="1"/>
  <rect x="210" y="180" width="160" height="28" fill="#fff3e0" stroke="#ddd" stroke-width="1"/>
  <rect x="370" y="180" width="280" height="28" fill="#fff3e0" stroke="#ddd" stroke-width="1"/>
  <text x="22" y="199" font-size="13" fill="#222">70B (4-bit)</text>
  <text x="222" y="199" font-size="13" fill="#222">24–40 GB</text>
  <text x="382" y="199" font-size="13" fill="#e65100" font-weight="bold">RTX 4090 (quantized!)</text>
  <rect x="10" y="208" width="200" height="28" fill="#f5f5f5" stroke="#ddd" stroke-width="1"/>
  <rect x="210" y="208" width="160" height="28" fill="#f5f5f5" stroke="#ddd" stroke-width="1"/>
  <rect x="370" y="208" width="280" height="28" fill="#f5f5f5" stroke="#ddd" stroke-width="1"/>
  <text x="22" y="227" font-size="13" fill="#222">405B</text>
  <text x="222" y="227" font-size="13" fill="#222">200+ GB</text>
  <text x="382" y="227" font-size="13" fill="#222">8× A100 or more</text>
  <!-- Quantization note section -->
  <rect x="10" y="248" width="640" height="130" fill="#fffde7" rx="4" stroke="#f9a825" stroke-width="1.5"/>
  <text x="22" y="268" font-size="13" font-weight="bold" fill="#f57f17">Quantization reduces memory requirements:</text>
  <text x="22" y="292" font-size="13" fill="#222">FP16 (16-bit):  Full precision, full VRAM</text>
  <text x="22" y="314" font-size="13" fill="#222">INT8 (8-bit):   ~50% VRAM, minimal quality loss</text>
  <text x="22" y="336" font-size="13" fill="#222">INT4 (4-bit):   ~25% VRAM, small quality loss</text>
  <text x="22" y="358" font-size="13" fill="#222">GGUF/GPTQ:     Optimized quantization formats</text>
</svg>

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

<svg xmlns="http://www.w3.org/2000/svg" width="680" height="400" font-family="sans-serif">
  <rect x="0" y="0" width="680" height="400" fill="#f0f4f8" rx="6" stroke="#333" stroke-width="1.5"/>
  <text x="340" y="24" text-anchor="middle" font-size="14" font-weight="bold" fill="#1565c0">Task: Code Generation (HumanEval Benchmark)</text>
  <!-- Header -->
  <rect x="10" y="34" width="260" height="28" fill="#bbdefb" stroke="#333" stroke-width="1"/>
  <rect x="270" y="34" width="100" height="28" fill="#bbdefb" stroke="#333" stroke-width="1"/>
  <rect x="370" y="34" width="120" height="28" fill="#bbdefb" stroke="#333" stroke-width="1"/>
  <rect x="490" y="34" width="180" height="28" fill="#bbdefb" stroke="#333" stroke-width="1"/>
  <text x="140" y="53" text-anchor="middle" font-size="13" font-weight="bold" fill="#222">Model</text>
  <text x="320" y="53" text-anchor="middle" font-size="13" font-weight="bold" fill="#222">Pass@1</text>
  <text x="430" y="53" text-anchor="middle" font-size="13" font-weight="bold" fill="#222">Size</text>
  <text x="580" y="53" text-anchor="middle" font-size="13" font-weight="bold" fill="#222">Cost/1M tok</text>
  <!-- Closed models (highlighted) -->
  <rect x="10" y="62" width="260" height="26" fill="#fff9c4" stroke="#ddd" stroke-width="1"/>
  <rect x="270" y="62" width="100" height="26" fill="#fff9c4" stroke="#ddd" stroke-width="1"/>
  <rect x="370" y="62" width="120" height="26" fill="#fff9c4" stroke="#ddd" stroke-width="1"/>
  <rect x="490" y="62" width="180" height="26" fill="#fff9c4" stroke="#ddd" stroke-width="1"/>
  <text x="22" y="80" font-size="13" fill="#222">GPT-4o</text>
  <text x="320" y="80" text-anchor="middle" font-size="13" fill="#222">92.1%</text>
  <text x="382" y="80" font-size="13" fill="#222">~200B*</text>
  <text x="502" y="80" font-size="13" fill="#c62828">$10 (output)</text>
  <rect x="10" y="88" width="260" height="26" fill="#fff9c4" stroke="#ddd" stroke-width="1"/>
  <rect x="270" y="88" width="100" height="26" fill="#fff9c4" stroke="#ddd" stroke-width="1"/>
  <rect x="370" y="88" width="120" height="26" fill="#fff9c4" stroke="#ddd" stroke-width="1"/>
  <rect x="490" y="88" width="180" height="26" fill="#fff9c4" stroke="#ddd" stroke-width="1"/>
  <text x="22" y="106" font-size="13" fill="#222">Claude 3.5 Sonnet</text>
  <text x="320" y="106" text-anchor="middle" font-size="13" fill="#222">92.0%</text>
  <text x="382" y="106" font-size="13" fill="#222">~?</text>
  <text x="502" y="106" font-size="13" fill="#c62828">$15 (output)</text>
  <!-- Open source models -->
  <rect x="10" y="114" width="260" height="26" fill="#e8f5e9" stroke="#ddd" stroke-width="1"/>
  <rect x="270" y="114" width="100" height="26" fill="#e8f5e9" stroke="#ddd" stroke-width="1"/>
  <rect x="370" y="114" width="120" height="26" fill="#e8f5e9" stroke="#ddd" stroke-width="1"/>
  <rect x="490" y="114" width="180" height="26" fill="#e8f5e9" stroke="#ddd" stroke-width="1"/>
  <text x="22" y="132" font-size="13" fill="#222">LLaMA 3.1 405B</text>
  <text x="320" y="132" text-anchor="middle" font-size="13" fill="#222">89.0%</text>
  <text x="382" y="132" font-size="13" fill="#222">405B</text>
  <text x="502" y="132" font-size="13" fill="#2e7d32">Self-host</text>
  <rect x="10" y="140" width="260" height="26" fill="#f5f5f5" stroke="#ddd" stroke-width="1"/>
  <rect x="270" y="140" width="100" height="26" fill="#f5f5f5" stroke="#ddd" stroke-width="1"/>
  <rect x="370" y="140" width="120" height="26" fill="#f5f5f5" stroke="#ddd" stroke-width="1"/>
  <rect x="490" y="140" width="180" height="26" fill="#f5f5f5" stroke="#ddd" stroke-width="1"/>
  <text x="22" y="158" font-size="13" fill="#222">Qwen 2.5 72B</text>
  <text x="320" y="158" text-anchor="middle" font-size="13" fill="#222">86.4%</text>
  <text x="382" y="158" font-size="13" fill="#222">72B</text>
  <text x="502" y="158" font-size="13" fill="#2e7d32">Self-host</text>
  <rect x="10" y="166" width="260" height="26" fill="#e8f5e9" stroke="#ddd" stroke-width="1"/>
  <rect x="270" y="166" width="100" height="26" fill="#e8f5e9" stroke="#ddd" stroke-width="1"/>
  <rect x="370" y="166" width="120" height="26" fill="#e8f5e9" stroke="#ddd" stroke-width="1"/>
  <rect x="490" y="166" width="180" height="26" fill="#e8f5e9" stroke="#ddd" stroke-width="1"/>
  <text x="22" y="184" font-size="13" fill="#222">Mistral Large</text>
  <text x="320" y="184" text-anchor="middle" font-size="13" fill="#222">84.0%</text>
  <text x="382" y="184" font-size="13" fill="#222">~123B</text>
  <text x="502" y="184" font-size="13" fill="#c62828">$8 (output)</text>
  <rect x="10" y="192" width="260" height="26" fill="#f5f5f5" stroke="#ddd" stroke-width="1"/>
  <rect x="270" y="192" width="100" height="26" fill="#f5f5f5" stroke="#ddd" stroke-width="1"/>
  <rect x="370" y="192" width="120" height="26" fill="#f5f5f5" stroke="#ddd" stroke-width="1"/>
  <rect x="490" y="192" width="180" height="26" fill="#f5f5f5" stroke="#ddd" stroke-width="1"/>
  <text x="22" y="210" font-size="13" fill="#222">Phi-3 14B</text>
  <text x="320" y="210" text-anchor="middle" font-size="13" fill="#222">82.0%</text>
  <text x="382" y="210" font-size="13" fill="#222">14B</text>
  <text x="502" y="210" font-size="13" fill="#2e7d32">Self-host</text>
  <rect x="10" y="218" width="260" height="26" fill="#e8f5e9" stroke="#ddd" stroke-width="1"/>
  <rect x="270" y="218" width="100" height="26" fill="#e8f5e9" stroke="#ddd" stroke-width="1"/>
  <rect x="370" y="218" width="120" height="26" fill="#e8f5e9" stroke="#ddd" stroke-width="1"/>
  <rect x="490" y="218" width="180" height="26" fill="#e8f5e9" stroke="#ddd" stroke-width="1"/>
  <text x="22" y="236" font-size="13" fill="#222">LLaMA 3.1 70B</text>
  <text x="320" y="236" text-anchor="middle" font-size="13" fill="#222">80.5%</text>
  <text x="382" y="236" font-size="13" fill="#222">70B</text>
  <text x="502" y="236" font-size="13" fill="#2e7d32">Self-host</text>
  <rect x="10" y="244" width="260" height="26" fill="#f5f5f5" stroke="#ddd" stroke-width="1"/>
  <rect x="270" y="244" width="100" height="26" fill="#f5f5f5" stroke="#ddd" stroke-width="1"/>
  <rect x="370" y="244" width="120" height="26" fill="#f5f5f5" stroke="#ddd" stroke-width="1"/>
  <rect x="490" y="244" width="180" height="26" fill="#f5f5f5" stroke="#ddd" stroke-width="1"/>
  <text x="22" y="262" font-size="13" fill="#222">Gemma 2 27B</text>
  <text x="320" y="262" text-anchor="middle" font-size="13" fill="#222">74.3%</text>
  <text x="382" y="262" font-size="13" fill="#222">27B</text>
  <text x="502" y="262" font-size="13" fill="#2e7d32">Self-host</text>
  <rect x="10" y="270" width="260" height="26" fill="#e8f5e9" stroke="#ddd" stroke-width="1"/>
  <rect x="270" y="270" width="100" height="26" fill="#e8f5e9" stroke="#ddd" stroke-width="1"/>
  <rect x="370" y="270" width="120" height="26" fill="#e8f5e9" stroke="#ddd" stroke-width="1"/>
  <rect x="490" y="270" width="180" height="26" fill="#e8f5e9" stroke="#ddd" stroke-width="1"/>
  <text x="22" y="288" font-size="13" fill="#222">LLaMA 3.1 8B</text>
  <text x="320" y="288" text-anchor="middle" font-size="13" fill="#222">72.6%</text>
  <text x="382" y="288" font-size="13" fill="#222">8B</text>
  <text x="502" y="288" font-size="13" fill="#2e7d32">Self-host</text>
  <!-- Key finding -->
  <rect x="10" y="308" width="660" height="80" fill="#e8f5e9" rx="4" stroke="#388e3c" stroke-width="1.5"/>
  <text x="22" y="328" font-size="13" font-weight="bold" fill="#1b5e20">Key finding:</text>
  <text x="22" y="348" font-size="13" fill="#222">The gap between open and closed models is narrowing rapidly.</text>
  <text x="22" y="368" font-size="13" fill="#222">Open 70B models approach closed model performance on many tasks.</text>
</svg>

---

## Choosing the Right Model

<svg xmlns="http://www.w3.org/2000/svg" width="680" height="460" font-family="sans-serif">
  <defs>
    <marker id="ah" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
    </marker>
  </defs>
  <rect x="0" y="0" width="680" height="460" fill="#f0f4f8" rx="6" stroke="#333" stroke-width="1.5"/>
  <text x="340" y="26" text-anchor="middle" font-size="16" font-weight="bold" fill="#1565c0">Decision Framework</text>
  <!-- Q1: Privacy critical? -->
  <rect x="40" y="44" width="200" height="36" fill="#fff9c4" rx="4" stroke="#f9a825" stroke-width="1.5"/>
  <text x="140" y="67" text-anchor="middle" font-size="13" fill="#222">Privacy critical?</text>
  <!-- YES arrow right -->
  <line x1="240" y1="62" x2="310" y2="62" stroke="#555" stroke-width="1.5" marker-end="url(#ah)"/>
  <text x="272" y="55" text-anchor="middle" font-size="11" fill="#2e7d32" font-weight="bold">YES</text>
  <rect x="312" y="44" width="200" height="36" fill="#c8e6c9" rx="4" stroke="#388e3c" stroke-width="1.5"/>
  <text x="412" y="67" text-anchor="middle" font-size="12" fill="#1b5e20">Open source (self-host)</text>
  <!-- NO arrow down -->
  <line x1="140" y1="80" x2="140" y2="118" stroke="#555" stroke-width="1.5" marker-end="url(#ah)"/>
  <text x="150" y="103" font-size="11" fill="#c62828" font-weight="bold">NO</text>
  <!-- Q2: Budget constrained? -->
  <rect x="40" y="120" width="200" height="36" fill="#fff9c4" rx="4" stroke="#f9a825" stroke-width="1.5"/>
  <text x="140" y="143" text-anchor="middle" font-size="13" fill="#222">Budget constrained?</text>
  <line x1="240" y1="138" x2="310" y2="138" stroke="#555" stroke-width="1.5" marker-end="url(#ah)"/>
  <text x="272" y="131" text-anchor="middle" font-size="11" fill="#2e7d32" font-weight="bold">YES</text>
  <rect x="312" y="120" width="240" height="36" fill="#c8e6c9" rx="4" stroke="#388e3c" stroke-width="1.5"/>
  <text x="432" y="143" text-anchor="middle" font-size="12" fill="#1b5e20">Open source or GPT-4o-mini</text>
  <line x1="140" y1="156" x2="140" y2="194" stroke="#555" stroke-width="1.5" marker-end="url(#ah)"/>
  <text x="150" y="179" font-size="11" fill="#c62828" font-weight="bold">NO</text>
  <!-- Q3: Need best quality? -->
  <rect x="40" y="196" width="200" height="36" fill="#fff9c4" rx="4" stroke="#f9a825" stroke-width="1.5"/>
  <text x="140" y="219" text-anchor="middle" font-size="13" fill="#222">Need best quality?</text>
  <line x1="240" y1="214" x2="310" y2="214" stroke="#555" stroke-width="1.5" marker-end="url(#ah)"/>
  <text x="272" y="207" text-anchor="middle" font-size="11" fill="#2e7d32" font-weight="bold">YES</text>
  <rect x="312" y="196" width="240" height="36" fill="#c8e6c9" rx="4" stroke="#388e3c" stroke-width="1.5"/>
  <text x="432" y="219" text-anchor="middle" font-size="12" fill="#1b5e20">GPT-4o / Claude 3.5 Sonnet</text>
  <line x1="140" y1="232" x2="140" y2="270" stroke="#555" stroke-width="1.5" marker-end="url(#ah)"/>
  <text x="150" y="255" font-size="11" fill="#c62828" font-weight="bold">NO</text>
  <!-- Q4: Simple tasks? -->
  <rect x="40" y="272" width="200" height="36" fill="#fff9c4" rx="4" stroke="#f9a825" stroke-width="1.5"/>
  <text x="140" y="295" text-anchor="middle" font-size="13" fill="#222">Simple tasks?</text>
  <line x1="240" y1="290" x2="310" y2="290" stroke="#555" stroke-width="1.5" marker-end="url(#ah)"/>
  <text x="272" y="283" text-anchor="middle" font-size="11" fill="#2e7d32" font-weight="bold">YES</text>
  <rect x="312" y="272" width="240" height="36" fill="#c8e6c9" rx="4" stroke="#388e3c" stroke-width="1.5"/>
  <text x="432" y="289" text-anchor="middle" font-size="12" fill="#1b5e20">Small open source (7–8B)</text>
  <text x="432" y="305" text-anchor="middle" font-size="12" fill="#1b5e20">or GPT-4o-mini</text>
  <line x1="140" y1="308" x2="140" y2="346" stroke="#555" stroke-width="1.5" marker-end="url(#ah)"/>
  <text x="150" y="331" font-size="11" fill="#c62828" font-weight="bold">NO</text>
  <!-- Q5: Complex reasoning? -->
  <rect x="40" y="348" width="200" height="36" fill="#fff9c4" rx="4" stroke="#f9a825" stroke-width="1.5"/>
  <text x="140" y="371" text-anchor="middle" font-size="13" fill="#222">Complex reasoning?</text>
  <line x1="240" y1="366" x2="310" y2="366" stroke="#555" stroke-width="1.5" marker-end="url(#ah)"/>
  <text x="272" y="359" text-anchor="middle" font-size="11" fill="#2e7d32" font-weight="bold">YES</text>
  <rect x="312" y="348" width="260" height="50" fill="#c8e6c9" rx="4" stroke="#388e3c" stroke-width="1.5"/>
  <text x="442" y="368" text-anchor="middle" font-size="12" fill="#1b5e20">Large open source (70B+)</text>
  <text x="442" y="388" text-anchor="middle" font-size="12" fill="#1b5e20">or closed model API</text>
</svg>

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

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="430" font-family="sans-serif">
  <rect x="0" y="0" width="660" height="430" fill="#f0f4f8" rx="6" stroke="#333" stroke-width="1.5"/>
  <!-- Title bar -->
  <rect x="0" y="0" width="660" height="36" fill="#37474f" rx="6" stroke="#333" stroke-width="1.5"/>
  <rect x="0" y="18" width="660" height="18" fill="#37474f"/>
  <text x="330" y="24" text-anchor="middle" font-size="15" font-weight="bold" fill="white">MODEL FILE FORMATS</text>
  <!-- Header -->
  <rect x="10" y="42" width="130" height="28" fill="#b0bec5" stroke="#333" stroke-width="1"/>
  <rect x="140" y="42" width="510" height="28" fill="#b0bec5" stroke="#333" stroke-width="1"/>
  <text x="75" y="61" text-anchor="middle" font-size="13" font-weight="bold" fill="#222">Format</text>
  <text x="395" y="61" text-anchor="middle" font-size="13" font-weight="bold" fill="#222">Description</text>
  <!-- PyTorch row -->
  <rect x="10" y="70" width="130" height="48" fill="#e8eaf6" stroke="#ddd" stroke-width="1"/>
  <rect x="140" y="70" width="510" height="48" fill="#e8eaf6" stroke="#ddd" stroke-width="1"/>
  <text x="75" y="90" text-anchor="middle" font-size="13" font-weight="bold" fill="#222">PyTorch</text>
  <text x="75" y="108" text-anchor="middle" font-size="12" fill="#555">(.bin)</text>
  <text x="152" y="88" font-size="13" fill="#222">.bin / .pt — native PyTorch format</text>
  <text x="152" y="108" font-size="13" fill="#555">Widely supported, large file sizes</text>
  <!-- SafeTensors row -->
  <rect x="10" y="118" width="130" height="62" fill="#f5f5f5" stroke="#ddd" stroke-width="1"/>
  <rect x="140" y="118" width="510" height="62" fill="#f5f5f5" stroke="#ddd" stroke-width="1"/>
  <text x="75" y="140" text-anchor="middle" font-size="13" font-weight="bold" fill="#222">SafeTensors</text>
  <text x="152" y="136" font-size="13" fill="#222">.safetensors — safe, fast loading</text>
  <text x="152" y="154" font-size="13" fill="#555">No code execution risk, faster I/O</text>
  <text x="152" y="172" font-size="13" fill="#555">Becoming the new standard</text>
  <!-- GGUF row -->
  <rect x="10" y="180" width="130" height="62" fill="#e8eaf6" stroke="#ddd" stroke-width="1"/>
  <rect x="140" y="180" width="510" height="62" fill="#e8eaf6" stroke="#ddd" stroke-width="1"/>
  <text x="75" y="202" text-anchor="middle" font-size="13" font-weight="bold" fill="#222">GGUF</text>
  <text x="152" y="198" font-size="13" fill="#222">.gguf — llama.cpp format</text>
  <text x="152" y="216" font-size="13" fill="#555">CPU-optimized, supports quantization</text>
  <text x="152" y="234" font-size="13" fill="#555">Used by Ollama, LM Studio</text>
  <!-- GPTQ row -->
  <rect x="10" y="242" width="130" height="62" fill="#f5f5f5" stroke="#ddd" stroke-width="1"/>
  <rect x="140" y="242" width="510" height="62" fill="#f5f5f5" stroke="#ddd" stroke-width="1"/>
  <text x="75" y="264" text-anchor="middle" font-size="13" font-weight="bold" fill="#222">GPTQ</text>
  <text x="152" y="260" font-size="13" fill="#222">GPU-optimized quantization</text>
  <text x="152" y="278" font-size="13" fill="#555">Post-training quantization</text>
  <text x="152" y="296" font-size="13" fill="#555">Good quality at 4-bit</text>
  <!-- AWQ row -->
  <rect x="10" y="304" width="130" height="62" fill="#e8eaf6" stroke="#ddd" stroke-width="1"/>
  <rect x="140" y="304" width="510" height="62" fill="#e8eaf6" stroke="#ddd" stroke-width="1"/>
  <text x="75" y="326" text-anchor="middle" font-size="13" font-weight="bold" fill="#222">AWQ</text>
  <text x="152" y="322" font-size="13" fill="#222">Activation-aware quantization</text>
  <text x="152" y="340" font-size="13" fill="#555">Better quality than GPTQ at same bits</text>
  <text x="152" y="358" font-size="13" fill="#555">Preserves important weights</text>
  <!-- EXL2 row -->
  <rect x="10" y="366" width="130" height="54" fill="#f5f5f5" stroke="#ddd" stroke-width="1"/>
  <rect x="140" y="366" width="510" height="54" fill="#f5f5f5" stroke="#ddd" stroke-width="1"/>
  <text x="75" y="388" text-anchor="middle" font-size="13" font-weight="bold" fill="#222">EXL2</text>
  <text x="152" y="384" font-size="13" fill="#222">ExLlamaV2 format</text>
  <text x="152" y="402" font-size="13" fill="#555">Flexible per-layer quantization; fastest inference on GPU</text>
</svg>

---

## Quantization Quality Comparison

<svg xmlns="http://www.w3.org/2000/svg" width="640" height="380" font-family="sans-serif">
  <rect x="0" y="0" width="640" height="380" fill="#f0f4f8" rx="6" stroke="#333" stroke-width="1.5"/>
  <text x="320" y="22" text-anchor="middle" font-size="14" font-weight="bold" fill="#1565c0">Performance Retention at Different Quantization Levels</text>
  <text x="320" y="40" text-anchor="middle" font-size="12" fill="#555">(Measured on MMLU benchmark, LLaMA 3.1 70B)</text>
  <!-- Header -->
  <rect x="10" y="48" width="140" height="28" fill="#bbdefb" stroke="#333" stroke-width="1"/>
  <rect x="150" y="48" width="100" height="28" fill="#bbdefb" stroke="#333" stroke-width="1"/>
  <rect x="250" y="48" width="100" height="28" fill="#bbdefb" stroke="#333" stroke-width="1"/>
  <rect x="350" y="48" width="280" height="28" fill="#bbdefb" stroke="#333" stroke-width="1"/>
  <text x="80" y="67" text-anchor="middle" font-size="13" font-weight="bold" fill="#222">Precision</text>
  <text x="200" y="67" text-anchor="middle" font-size="13" font-weight="bold" fill="#222">Size</text>
  <text x="300" y="67" text-anchor="middle" font-size="13" font-weight="bold" fill="#222">MMLU</text>
  <text x="490" y="67" text-anchor="middle" font-size="13" font-weight="bold" fill="#222">Relative Quality</text>
  <!-- Data rows -->
  <rect x="10" y="76" width="140" height="26" fill="#c8e6c9" stroke="#ddd" stroke-width="1"/>
  <rect x="150" y="76" width="100" height="26" fill="#c8e6c9" stroke="#ddd" stroke-width="1"/>
  <rect x="250" y="76" width="100" height="26" fill="#c8e6c9" stroke="#ddd" stroke-width="1"/>
  <rect x="350" y="76" width="280" height="26" fill="#c8e6c9" stroke="#ddd" stroke-width="1"/>
  <text x="22" y="94" font-size="13" font-weight="bold" fill="#222">FP16</text>
  <text x="162" y="94" font-size="13" fill="#222">140 GB</text>
  <text x="262" y="94" font-size="13" fill="#222">82.0%</text>
  <text x="362" y="94" font-size="13" fill="#2e7d32" font-weight="bold">100% (baseline)</text>
  <rect x="10" y="102" width="140" height="26" fill="#e8f5e9" stroke="#ddd" stroke-width="1"/>
  <rect x="150" y="102" width="100" height="26" fill="#e8f5e9" stroke="#ddd" stroke-width="1"/>
  <rect x="250" y="102" width="100" height="26" fill="#e8f5e9" stroke="#ddd" stroke-width="1"/>
  <rect x="350" y="102" width="280" height="26" fill="#e8f5e9" stroke="#ddd" stroke-width="1"/>
  <text x="22" y="120" font-size="13" fill="#222">INT8</text>
  <text x="162" y="120" font-size="13" fill="#222">70 GB</text>
  <text x="262" y="120" font-size="13" fill="#222">81.8%</text>
  <text x="362" y="120" font-size="13" fill="#222">99.8%</text>
  <rect x="10" y="128" width="140" height="26" fill="#fff3e0" stroke="#ddd" stroke-width="1"/>
  <rect x="150" y="128" width="100" height="26" fill="#fff3e0" stroke="#ddd" stroke-width="1"/>
  <rect x="250" y="128" width="100" height="26" fill="#fff3e0" stroke="#ddd" stroke-width="1"/>
  <rect x="350" y="128" width="280" height="26" fill="#fff3e0" stroke="#ddd" stroke-width="1"/>
  <text x="22" y="146" font-size="13" fill="#222">INT4 (GPTQ)</text>
  <text x="162" y="146" font-size="13" fill="#222">35 GB</text>
  <text x="262" y="146" font-size="13" fill="#222">80.5%</text>
  <text x="362" y="146" font-size="13" fill="#e65100" font-weight="bold">98.2% ⭐</text>
  <rect x="10" y="154" width="140" height="26" fill="#fff8f0" stroke="#ddd" stroke-width="1"/>
  <rect x="150" y="154" width="100" height="26" fill="#fff8f0" stroke="#ddd" stroke-width="1"/>
  <rect x="250" y="154" width="100" height="26" fill="#fff8f0" stroke="#ddd" stroke-width="1"/>
  <rect x="350" y="154" width="280" height="26" fill="#fff8f0" stroke="#ddd" stroke-width="1"/>
  <text x="22" y="172" font-size="13" fill="#222">INT4 (AWQ)</text>
  <text x="162" y="172" font-size="13" fill="#222">35 GB</text>
  <text x="262" y="172" font-size="13" fill="#222">81.0%</text>
  <text x="362" y="172" font-size="13" fill="#e65100" font-weight="bold">98.8% ⭐</text>
  <rect x="10" y="180" width="140" height="26" fill="#fff8f0" stroke="#ddd" stroke-width="1"/>
  <rect x="150" y="180" width="100" height="26" fill="#fff8f0" stroke="#ddd" stroke-width="1"/>
  <rect x="250" y="180" width="100" height="26" fill="#fff8f0" stroke="#ddd" stroke-width="1"/>
  <rect x="350" y="180" width="280" height="26" fill="#fff8f0" stroke="#ddd" stroke-width="1"/>
  <text x="22" y="198" font-size="13" fill="#222">INT4 (NF4)</text>
  <text x="162" y="198" font-size="13" fill="#222">35 GB</text>
  <text x="262" y="198" font-size="13" fill="#222">81.2%</text>
  <text x="362" y="198" font-size="13" fill="#e65100" font-weight="bold">99.0% ⭐</text>
  <rect x="10" y="206" width="140" height="26" fill="#ffebee" stroke="#ddd" stroke-width="1"/>
  <rect x="150" y="206" width="100" height="26" fill="#ffebee" stroke="#ddd" stroke-width="1"/>
  <rect x="250" y="206" width="100" height="26" fill="#ffebee" stroke="#ddd" stroke-width="1"/>
  <rect x="350" y="206" width="280" height="26" fill="#ffebee" stroke="#ddd" stroke-width="1"/>
  <text x="22" y="224" font-size="13" fill="#222">INT3</text>
  <text x="162" y="224" font-size="13" fill="#222">26 GB</text>
  <text x="262" y="224" font-size="13" fill="#222">77.5%</text>
  <text x="362" y="224" font-size="13" fill="#c62828">94.5%</text>
  <rect x="10" y="232" width="140" height="26" fill="#ffcdd2" stroke="#ddd" stroke-width="1"/>
  <rect x="150" y="232" width="100" height="26" fill="#ffcdd2" stroke="#ddd" stroke-width="1"/>
  <rect x="250" y="232" width="100" height="26" fill="#ffcdd2" stroke="#ddd" stroke-width="1"/>
  <rect x="350" y="232" width="280" height="26" fill="#ffcdd2" stroke="#ddd" stroke-width="1"/>
  <text x="22" y="250" font-size="13" fill="#222">INT2</text>
  <text x="162" y="250" font-size="13" fill="#222">18 GB</text>
  <text x="262" y="250" font-size="13" fill="#222">68.0%</text>
  <text x="362" y="250" font-size="13" fill="#c62828">82.9%</text>
  <!-- Sweet spot note -->
  <rect x="10" y="270" width="620" height="98" fill="#fff9c4" rx="4" stroke="#f9a825" stroke-width="1.5"/>
  <text x="22" y="290" font-size="13" font-weight="bold" fill="#e65100">Sweet spot: 4-bit quantization</text>
  <text x="22" y="314" font-size="13" fill="#222">• 4× smaller than FP16</text>
  <text x="22" y="334" font-size="13" fill="#222">• &lt;2% quality loss</text>
  <text x="22" y="354" font-size="13" fill="#222">• Significant speedup on modern GPUs</text>
</svg>

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

```diagram
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

```diagram
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
