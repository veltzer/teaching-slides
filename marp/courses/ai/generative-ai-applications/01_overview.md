# Generative AI Applications — Course Overview

---

## Welcome to Generative AI Applications

A comprehensive 5-day course covering the full landscape of generative AI

**Course Goals:**
- Understand the foundations of generative AI models
- Master `API`-based development with `LLM`s
- Build agents and memory-augmented systems with `LangChain`
- Work with open-source models and efficient fine-tuning
- Explore image generation, bias, and AI safety

---

## Course Structure

| Day | Topic | Focus |
|-----|-------|-------|
| 1 | Overview & Foundations | How generative AI works |
| 2 | APIs of Generative Models | Prompt engineering & fine-tuning |
| 3 | Agents, Memory & `LangChain` | Building intelligent systems |
| 4 | Open Source Models | `HuggingFace`, `LoRA`, `QLoRA` |
| 5 | Image Generation & AI Safety | Diffusion, bias, deep fakes |

---

## Prerequisites

To get the most from this course, you should have:

- Working knowledge of `Python` (functions, classes, decorators)
- Familiarity with basic machine learning concepts
- A computer with `Python` 3.10+ installed
- Access to `OpenAI` API key (provided during class)
- Optional: GPU access for Day 4–5 exercises

---

## Environment Setup

```python
# Create a virtual environment
python -m venv genai-course
source genai-course/bin/activate  # Linux/Mac
# genai-course\Scripts\activate   # Windows

# Install core dependencies
pip install openai langchain transformers
pip install torch torchvision
pip install huggingface_hub datasets
pip install chromadb faiss-cpu
pip install diffusers accelerate
```

---

## What is Generative AI?

**Generative AI** = AI systems that create new content

<svg xmlns="http://www.w3.org/2000/svg" width="580" height="220" viewBox="0 0 580 220">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>
  <rect width="580" height="220" fill="#f0f4f8" rx="4" stroke="#333" stroke-width="1.5"/>
  <text x="290" y="24" font-family="sans-serif" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">Generative AI — How It Works</text>
  <!-- input -->
  <rect x="20" y="50" width="150" height="50" fill="#e3f2fd" rx="4" stroke="#1565c0" stroke-width="1.5"/>
  <text x="95" y="72" font-family="sans-serif" font-size="12" font-weight="bold" fill="#1565c0" text-anchor="middle">Input Prompt</text>
  <text x="95" y="89" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">"Write a poem about coding"</text>
  <!-- arrow -->
  <line x1="170" y1="75" x2="208" y2="75" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- model -->
  <rect x="210" y="38" width="160" height="74" fill="#fff3e0" rx="4" stroke="#e65100" stroke-width="2"/>
  <text x="290" y="62" font-family="sans-serif" font-size="13" font-weight="bold" fill="#e65100" text-anchor="middle">Generative Model</text>
  <text x="290" y="80" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">trained on vast</text>
  <text x="290" y="96" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">text corpora</text>
  <!-- arrow -->
  <line x1="370" y1="75" x2="408" y2="75" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- output -->
  <rect x="410" y="38" width="150" height="115" fill="#e8f5e9" rx="4" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="485" y="62" font-family="sans-serif" font-size="12" font-weight="bold" fill="#2e7d32" text-anchor="middle">Output</text>
  <text x="485" y="82" font-family="sans-serif" font-size="11" fill="#333" text-anchor="middle" font-style="italic">"In silicon dreams,</text>
  <text x="485" y="98" font-family="sans-serif" font-size="11" fill="#333" text-anchor="middle" font-style="italic">where logic streams,</text>
  <text x="485" y="114" font-family="sans-serif" font-size="11" fill="#333" text-anchor="middle" font-style="italic">the coder writes</text>
  <text x="485" y="130" font-family="sans-serif" font-size="11" fill="#333" text-anchor="middle" font-style="italic">through endless nights..."</text>
</svg>

Unlike **discriminative** models (classify existing data), generative models **produce** new data.

---

## The Generative AI Landscape

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="220" viewBox="0 0 660 220">
  <rect width="660" height="220" fill="#f0f4f8" rx="4" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="24" font-family="sans-serif" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">Generative AI Ecosystem</text>
  <!-- col headers -->
  <rect x="20" y="36" width="145" height="28" fill="#1565c0" rx="4"/>
  <text x="92" y="55" font-family="sans-serif" font-size="13" font-weight="bold" fill="#fff" text-anchor="middle">TEXT</text>
  <rect x="172" y="36" width="145" height="28" fill="#7b1fa2" rx="4"/>
  <text x="244" y="55" font-family="sans-serif" font-size="13" font-weight="bold" fill="#fff" text-anchor="middle">IMAGE</text>
  <rect x="324" y="36" width="145" height="28" fill="#e65100" rx="4"/>
  <text x="396" y="55" font-family="sans-serif" font-size="13" font-weight="bold" fill="#fff" text-anchor="middle">AUDIO</text>
  <rect x="476" y="36" width="164" height="28" fill="#2e7d32" rx="4"/>
  <text x="558" y="55" font-family="sans-serif" font-size="13" font-weight="bold" fill="#fff" text-anchor="middle">VIDEO</text>
  <!-- data rows -->
  <text x="92" y="86" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">GPT-4 / GPT-5</text>
  <text x="244" y="86" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">DALL-E 3</text>
  <text x="396" y="86" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Whisper</text>
  <text x="558" y="86" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Sora</text>
  <text x="92" y="108" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Claude</text>
  <text x="244" y="108" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Midjourney</text>
  <text x="396" y="108" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Bark</text>
  <text x="558" y="108" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Runway Gen-2</text>
  <text x="92" y="130" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Gemini</text>
  <text x="244" y="130" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Stable Diffusion</text>
  <text x="396" y="130" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">MusicLM</text>
  <text x="558" y="130" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Pika Labs</text>
  <text x="92" y="152" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">LLaMA / Mistral</text>
  <text x="244" y="152" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Flux</text>
  <text x="396" y="152" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Eleven Labs</text>
  <text x="558" y="152" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Stable Video Diff.</text>
  <!-- grid lines -->
  <line x1="20" y1="64" x2="640" y2="64" stroke="#ccc" stroke-width="1"/>
  <line x1="20" y1="96" x2="640" y2="96" stroke="#eee" stroke-width="1"/>
  <line x1="20" y1="118" x2="640" y2="118" stroke="#eee" stroke-width="1"/>
  <line x1="20" y1="140" x2="640" y2="140" stroke="#eee" stroke-width="1"/>
  <line x1="170" y1="36" x2="170" y2="165" stroke="#ccc" stroke-width="1"/>
  <line x1="322" y1="36" x2="322" y2="165" stroke="#ccc" stroke-width="1"/>
  <line x1="474" y1="36" x2="474" y2="165" stroke="#ccc" stroke-width="1"/>
</svg>

---

## Why Generative AI Matters Now

Three converging factors enabled the current explosion:

1. **Scale of data** — Trillions of tokens from the internet
1. **Scale of compute** — Thousands of GPUs training for months
1. **Architectural breakthroughs** — The Transformer (2017)

<svg xmlns="http://www.w3.org/2000/svg" width="580" height="230" viewBox="0 0 580 230">
  <rect width="580" height="230" fill="#f0f4f8" rx="4" stroke="#333" stroke-width="1.5"/>
  <text x="290" y="24" font-family="sans-serif" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">LLM Performance Growth Over Time</text>
  <!-- axes -->
  <line x1="60" y1="40" x2="60" y2="180" stroke="#333" stroke-width="2"/>
  <line x1="60" y1="180" x2="540" y2="180" stroke="#333" stroke-width="2"/>
  <text x="25" y="110" font-family="sans-serif" font-size="12" fill="#555" text-anchor="middle" transform="rotate(-90,25,110)">Performance</text>
  <!-- x labels -->
  <text x="80" y="196" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">2019</text>
  <text x="155" y="196" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">2020</text>
  <text x="235" y="196" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">2021</text>
  <text x="315" y="196" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">2022</text>
  <text x="395" y="196" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">2023</text>
  <text x="475" y="196" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">2024</text>
  <!-- exponential curve approximated with polyline -->
  <polyline points="80,170 155,155 235,138 315,115 395,82 475,45" fill="none" stroke="#1565c0" stroke-width="2.5"/>
  <!-- model labels -->
  <circle cx="80" cy="170" r="4" fill="#1565c0"/>
  <text x="85" y="165" font-family="sans-serif" font-size="11" fill="#333">GPT-2</text>
  <circle cx="155" cy="155" r="4" fill="#1565c0"/>
  <text x="160" y="150" font-family="sans-serif" font-size="11" fill="#333">GPT-3</text>
  <circle cx="315" cy="115" r="4" fill="#1565c0"/>
  <text x="320" y="110" font-family="sans-serif" font-size="11" fill="#333">GPT-3.5</text>
  <circle cx="395" cy="82" r="4" fill="#1565c0"/>
  <text x="400" y="77" font-family="sans-serif" font-size="11" fill="#333">GPT-4</text>
  <circle cx="475" cy="45" r="4" fill="#e65100"/>
  <text x="440" y="42" font-family="sans-serif" font-size="11" fill="#e65100">GPT-5 / Claude</text>
</svg>

---

## Key Terminology

| Term | Meaning |
|------|---------|
| `LLM` | Large Language Model — neural network trained on text |
| `Token` | Basic unit of text (word or subword piece) |
| `Prompt` | Input text given to the model |
| `Completion` | Output text generated by the model |
| `Context window` | Maximum tokens the model can process at once |
| `Temperature` | Controls randomness of output (0 = deterministic) |
| `Fine-tuning` | Further training on domain-specific data |
| `RAG` | Retrieval-Augmented Generation |
| `Embedding` | Dense vector representation of text |

---

## How This Course Fits Together

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="340" viewBox="0 0 660 340">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>
  <rect width="660" height="340" fill="#f0f4f8" rx="4" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="24" font-family="sans-serif" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">Course Outline — 5-Day Schedule</text>
  <!-- Day 1 -->
  <rect x="20" y="40" width="175" height="80" fill="#e3f2fd" rx="4" stroke="#1565c0" stroke-width="1.5"/>
  <text x="107" y="60" font-family="sans-serif" font-size="12" font-weight="bold" fill="#1565c0" text-anchor="middle">Day 1: FOUNDATIONS</text>
  <text x="107" y="78" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">How LLMs work</text>
  <text x="107" y="95" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">GPT architecture</text>
  <!-- arrow D1->D2 -->
  <line x1="195" y1="80" x2="223" y2="80" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- Day 2 -->
  <rect x="225" y="40" width="175" height="80" fill="#e8f5e9" rx="4" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="312" y="60" font-family="sans-serif" font-size="12" font-weight="bold" fill="#2e7d32" text-anchor="middle">Day 2: APIs &amp; PROMPTS</text>
  <text x="312" y="78" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">OpenAI API</text>
  <text x="312" y="95" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Prompt Engineering</text>
  <text x="312" y="112" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Fine-tuning</text>
  <!-- arrow D2->D3 -->
  <line x1="400" y1="80" x2="428" y2="80" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- Day 4 -->
  <rect x="430" y="40" width="200" height="80" fill="#fff3e0" rx="4" stroke="#e65100" stroke-width="1.5"/>
  <text x="530" y="60" font-family="sans-serif" font-size="12" font-weight="bold" fill="#e65100" text-anchor="middle">Day 4: OPEN SOURCE</text>
  <text x="530" y="78" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">HuggingFace</text>
  <text x="530" y="95" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">LoRA / QLoRA</text>
  <text x="530" y="112" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Local models</text>
  <!-- Day 3 -->
  <rect x="225" y="170" width="175" height="80" fill="#f3e5f5" rx="4" stroke="#7b1fa2" stroke-width="1.5"/>
  <text x="312" y="190" font-family="sans-serif" font-size="12" font-weight="bold" fill="#7b1fa2" text-anchor="middle">Day 3: AGENTS</text>
  <text x="312" y="208" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">LangChain</text>
  <text x="312" y="225" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Memory &amp; Custom DB</text>
  <!-- arrow D2->D3 vertical -->
  <line x1="312" y1="120" x2="312" y2="168" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- arrow D4->D3 -->
  <line x1="530" y1="120" x2="400" y2="208" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- Day 5 -->
  <rect x="225" y="295" width="200" height="35" fill="#ffebee" rx="4" stroke="#c62828" stroke-width="1.5"/>
  <text x="325" y="317" font-family="sans-serif" font-size="12" font-weight="bold" fill="#c62828" text-anchor="middle">Day 5: IMAGES &amp; SAFETY — Diffusion · DreamBooth · Bias &amp; Safety</text>
  <line x1="312" y1="250" x2="312" y2="293" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
</svg>

---

## Learning Approach

Each topic follows this pattern:

1. **Concept** — Understand the theory
1. **Code** — See working `Python` examples
1. **Practice** — Hands-on exercises
1. **Discussion** — Real-world applications and limitations

**Every day includes:**
- Live coding demonstrations
- Guided exercises
- Open Q&A sessions
- Take-home challenges

---

## Resources & References

| Resource | URL |
|----------|-----|
| OpenAI API Docs | `platform.openai.com/docs` |
| LangChain Docs | `python.langchain.com` |
| HuggingFace Hub | `huggingface.co` |
| Course Repository | (provided separately) |

**Key Papers:**
- "Attention Is All You Need" (Vaswani et al., 2017)
- "Language Models are Few-Shot Learners" (Brown et al., 2020)
- "Training language models to follow instructions" (Ouyang et al., 2022)

---

## Hands-On Tools We'll Use

```python
# Core libraries used throughout the course

# Day 1-2: API and prompting
from openai import OpenAI       # OpenAI API client
import tiktoken                 # Token counting

# Day 2: Evaluation
from rouge_score import rouge_scorer  # Text evaluation
from bert_score import score          # Semantic evaluation

# Day 3: Agents and RAG
import langchain                # LLM application framework
import chromadb                 # Vector database

# Day 4: Open source models
from transformers import (      # HuggingFace models
    AutoModelForCausalLM,
    AutoTokenizer,
    pipeline,
)
from peft import (              # Parameter efficient fine-tuning
    LoraConfig,
    get_peft_model,
)
from datasets import load_dataset  # HuggingFace datasets

# Day 5: Image generation
from diffusers import (         # Image generation
    StableDiffusionPipeline,
    StableDiffusionXLPipeline,
)
```

---

## How to Get the Most from This Course

- **Ask questions** at any time — there are no bad questions
- **Code along** during demonstrations when possible
- **Experiment** with parameters — change temperature, model, prompts
- **Break things** intentionally — understanding failure modes is valuable
- **Take notes** on patterns that apply to your specific use cases
- **Pair up** for exercises — discussing approaches helps learning
- **Share findings** — your experiments help everyone learn

**Remember:** The field changes rapidly. The *principles* you learn (attention, tokenization, alignment, PEFT) are durable. Specific APIs and model names will evolve.

---

## Daily Schedule

```output
Each day follows this structure:

09:00 - 10:30  │ Morning session (theory + demos)
10:30 - 10:45  │ Break
10:45 - 12:15  │ Deep dive (code examples + practice)
12:15 - 13:15  │ Lunch
13:15 - 14:45  │ Afternoon session (hands-on exercises)
14:45 - 15:00  │ Break
15:00 - 16:30  │ Advanced topics + Q&A
16:30 - 17:00  │ Day summary + preview of tomorrow

Exercises: Work at your own pace.
  ★      = Essential (everyone should complete)
  ★★     = Recommended (solidifies understanding)
  ★★★    = Challenge (for those who finish early)
```

---

## Connecting the Dots

```misc
Real-world GenAI application uses ALL the skills:

EXAMPLE: Customer support chatbot

Day 1 knowledge:
  └─ Choose the right model for cost/quality tradeoff

Day 2 knowledge:
  └─ Design effective system prompts
  └─ Use function calling for ticket creation
  └─ Fine-tune for your company's tone

Day 3 knowledge:
  └─ RAG over your knowledge base
  └─ Conversation memory for context
  └─ Agent routing for complex queries

Day 4 knowledge:
  └─ Deploy locally for data privacy
  └─ LoRA fine-tune for your domain

Day 5 knowledge:
  └─ Evaluate response quality
  └─ Monitor for bias
  └─ Implement safety guardrails
```
