# An Overview of Generative AI

---

## What Does "Generative" Mean?

**Discriminative models** learn boundaries between classes:
- Input: image → Output: "cat" or "dog"

**Generative models** learn the underlying data distribution:
- Input: "a photo of a cat" → Output: a new cat image

```misc
Discriminative:  P(label | data)    — What IS this?
Generative:      P(data | label)    — What WOULD this look like?
```

---

## A Brief History of Generative Models

```misc
Timeline of Generative AI
═══════════════════════════════════════════════════════
2014 │ GANs (Goodfellow)          — adversarial image gen
2015 │ VAEs become practical      — latent space learning
2017 │ Transformer architecture   — attention revolution
2018 │ GPT-1, BERT                — pretrained language models
2019 │ GPT-2                      — "too dangerous to release"
2020 │ GPT-3                      — few-shot learning emerges
2021 │ DALL-E, Codex, Copilot     — multimodal & code gen
2022 │ ChatGPT, Stable Diffusion  — mainstream adoption
2023 │ GPT-4, Claude, LLaMA       — open source catches up
2024 │ Mixtral, Gemini, Sora      — MoE, multimodal, video
2025 │ Claude 4, GPT-5, Llama 4   — reasoning & agents
```

---

## Categories of Generative Models

<svg xmlns="http://www.w3.org/2000/svg" width="680" height="275" font-family="sans-serif">
  <!-- Root box -->
  <rect x="230" y="10" width="220" height="36" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="340" y="33" text-anchor="middle" font-size="14" font-weight="bold" fill="#222222">GENERATIVE MODELS</text>
  <!-- Root to children connector -->
  <line x1="340" y1="46" x2="340" y2="62" stroke="#555" stroke-width="1.5"/>
  <line x1="185" y1="62" x2="495" y2="62" stroke="#555" stroke-width="1.5"/>
  <line x1="185" y1="62" x2="185" y2="78" stroke="#555" stroke-width="1.5"/>
  <line x1="495" y1="62" x2="495" y2="78" stroke="#555" stroke-width="1.5"/>
  <!-- AUTOREGRESSIVE box -->
  <rect x="85" y="78" width="200" height="46" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="185" y="98" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">AUTOREGRESSIVE</text>
  <text x="185" y="115" text-anchor="middle" font-size="11" fill="#555555">(sequential)</text>
  <!-- DIFFUSION box -->
  <rect x="395" y="78" width="200" height="46" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="495" y="98" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">DIFFUSION</text>
  <text x="495" y="115" text-anchor="middle" font-size="11" fill="#555555">(iterative denoising)</text>
  <!-- AUTOREGRESSIVE to leaves -->
  <line x1="185" y1="124" x2="185" y2="142" stroke="#555" stroke-width="1.5"/>
  <line x1="110" y1="142" x2="265" y2="142" stroke="#555" stroke-width="1.5"/>
  <line x1="110" y1="142" x2="110" y2="158" stroke="#555" stroke-width="1.5"/>
  <line x1="265" y1="142" x2="265" y2="158" stroke="#555" stroke-width="1.5"/>
  <!-- DIFFUSION to leaves -->
  <line x1="495" y1="124" x2="495" y2="142" stroke="#555" stroke-width="1.5"/>
  <line x1="425" y1="142" x2="575" y2="142" stroke="#555" stroke-width="1.5"/>
  <line x1="425" y1="142" x2="425" y2="158" stroke="#555" stroke-width="1.5"/>
  <line x1="575" y1="142" x2="575" y2="158" stroke="#555" stroke-width="1.5"/>
  <!-- TEXT leaf -->
  <rect x="50" y="158" width="120" height="95" rx="4" fill="#f0f4f8" stroke="#333333" stroke-width="1.5"/>
  <text x="110" y="178" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">TEXT</text>
  <text x="110" y="198" text-anchor="middle" font-size="11" fill="#444444">GPT</text>
  <text x="110" y="214" text-anchor="middle" font-size="11" fill="#444444">Claude</text>
  <text x="110" y="230" text-anchor="middle" font-size="11" fill="#444444">LLaMA</text>
  <!-- CODE leaf -->
  <rect x="205" y="158" width="120" height="95" rx="4" fill="#f0f4f8" stroke="#333333" stroke-width="1.5"/>
  <text x="265" y="178" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">CODE</text>
  <text x="265" y="198" text-anchor="middle" font-size="11" fill="#444444">Codex</text>
  <text x="265" y="214" text-anchor="middle" font-size="11" fill="#444444">Claude</text>
  <text x="265" y="230" text-anchor="middle" font-size="11" fill="#444444">Cursor</text>
  <!-- IMAGE leaf -->
  <rect x="365" y="158" width="120" height="95" rx="4" fill="#f0f4f8" stroke="#333333" stroke-width="1.5"/>
  <text x="425" y="178" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">IMAGE</text>
  <text x="425" y="198" text-anchor="middle" font-size="11" fill="#444444">DALL-E</text>
  <text x="425" y="214" text-anchor="middle" font-size="11" fill="#444444">SD</text>
  <text x="425" y="230" text-anchor="middle" font-size="11" fill="#444444">Flux</text>
  <!-- VIDEO leaf -->
  <rect x="515" y="158" width="120" height="95" rx="4" fill="#f0f4f8" stroke="#333333" stroke-width="1.5"/>
  <text x="575" y="178" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">VIDEO</text>
  <text x="575" y="198" text-anchor="middle" font-size="11" fill="#444444">Sora</text>
  <text x="575" y="214" text-anchor="middle" font-size="11" fill="#444444">Runway</text>
  <text x="575" y="230" text-anchor="middle" font-size="11" fill="#444444">Pika</text>
</svg>

Other types: `VAE`s, `GAN`s, Flow-based, Energy-based

---

## The Transformer — Foundation of Modern GenAI

Published in 2017: "Attention Is All You Need"

<svg xmlns="http://www.w3.org/2000/svg" width="620" height="375" font-family="sans-serif">
  <defs>
    <marker id="arr2" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
    </marker>
  </defs>
  <!-- Input tokens text -->
  <text x="30" y="22" font-size="13" fill="#222222">Input tokens: ["The", "cat", "sat", "on", "the", "___"]</text>
  <!-- Outer TRANSFORMER BLOCK box -->
  <rect x="20" y="34" width="580" height="260" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="2"/>
  <text x="310" y="54" text-anchor="middle" font-size="14" font-weight="bold" fill="#222222">TRANSFORMER BLOCK</text>
  <!-- Inner box 1: Multi-Head Self-Attention -->
  <rect x="50" y="64" width="520" height="56" rx="4" fill="#f0f4f8" stroke="#333333" stroke-width="1.5"/>
  <text x="310" y="86" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Multi-Head Self-Attention</text>
  <text x="310" y="106" text-anchor="middle" font-size="12" fill="#444444">(each token attends to every other token)</text>
  <!-- Arrow 1 → 2 -->
  <line x1="310" y1="120" x2="310" y2="138" stroke="#555" stroke-width="1.5" marker-end="url(#arr2)"/>
  <!-- Inner box 2: Feed-Forward Network -->
  <rect x="50" y="140" width="520" height="52" rx="4" fill="#f0f4f8" stroke="#333333" stroke-width="1.5"/>
  <text x="310" y="162" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Feed-Forward Network</text>
  <text x="310" y="180" text-anchor="middle" font-size="12" fill="#444444">(process each position)</text>
  <!-- Arrow 2 → 3 -->
  <line x1="310" y1="192" x2="310" y2="210" stroke="#555" stroke-width="1.5" marker-end="url(#arr2)"/>
  <!-- Inner box 3: Layer Normalization -->
  <rect x="50" y="212" width="520" height="52" rx="4" fill="#f0f4f8" stroke="#333333" stroke-width="1.5"/>
  <text x="310" y="234" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Layer Normalization</text>
  <text x="310" y="252" text-anchor="middle" font-size="12" fill="#444444">+ Residual Connection</text>
  <!-- Arrow exits outer box -->
  <line x1="310" y1="294" x2="310" y2="322" stroke="#555" stroke-width="1.5" marker-end="url(#arr2)"/>
  <text x="318" y="313" font-size="12" fill="#555555">× N layers</text>
  <!-- Output text -->
  <text x="310" y="348" text-anchor="middle" font-size="13" fill="#222222">Output: "mat" (probability 0.87)</text>
</svg>

---

## Self-Attention Mechanism — Intuition

Every token asks: "Which other tokens should I pay attention to?"

<svg xmlns="http://www.w3.org/2000/svg" width="620" height="330" font-family="sans-serif">
  <!-- Title text -->
  <text x="30" y="18" font-size="13" fill="#222222">Sentence: "The animal didn't cross the street because it was too tired"</text>
  <text x="30" y="38" font-size="13" fill="#555555">What does "it" refer to?</text>
  <text x="30" y="60" font-size="13" font-weight="bold" fill="#222222">Attention weights for "it":</text>
  <!-- Bars: label right-aligned at x=110, bar starts at x=120 -->
  <!-- The -->
  <text x="110" y="84" text-anchor="end" font-size="12" fill="#222222">The</text>
  <rect x="120" y="72" width="37" height="16" rx="2" fill="#90caf9"/>
  <!-- animal – high attention -->
  <text x="110" y="106" text-anchor="end" font-size="12" fill="#222222">animal</text>
  <rect x="120" y="94" width="220" height="16" rx="2" fill="#1565c0"/>
  <text x="346" y="106" font-size="11" fill="#1565c0"> ← high attention</text>
  <!-- didn't -->
  <text x="110" y="128" text-anchor="end" font-size="12" fill="#222222">didn't</text>
  <rect x="120" y="116" width="37" height="16" rx="2" fill="#90caf9"/>
  <!-- cross -->
  <text x="110" y="150" text-anchor="end" font-size="12" fill="#222222">cross</text>
  <rect x="120" y="138" width="55" height="16" rx="2" fill="#90caf9"/>
  <!-- the -->
  <text x="110" y="172" text-anchor="end" font-size="12" fill="#222222">the</text>
  <rect x="120" y="160" width="18" height="16" rx="2" fill="#90caf9"/>
  <!-- street -->
  <text x="110" y="194" text-anchor="end" font-size="12" fill="#222222">street</text>
  <rect x="120" y="182" width="73" height="16" rx="2" fill="#90caf9"/>
  <!-- because -->
  <text x="110" y="216" text-anchor="end" font-size="12" fill="#222222">because</text>
  <rect x="120" y="204" width="18" height="16" rx="2" fill="#90caf9"/>
  <!-- it -->
  <text x="110" y="238" text-anchor="end" font-size="12" fill="#222222">it</text>
  <rect x="120" y="226" width="55" height="16" rx="2" fill="#90caf9"/>
  <!-- was -->
  <text x="110" y="260" text-anchor="end" font-size="12" fill="#222222">was</text>
  <rect x="120" y="248" width="37" height="16" rx="2" fill="#90caf9"/>
  <!-- too -->
  <text x="110" y="282" text-anchor="end" font-size="12" fill="#222222">too</text>
  <rect x="120" y="270" width="37" height="16" rx="2" fill="#90caf9"/>
  <!-- tired – medium, annotation -->
  <text x="110" y="304" text-anchor="end" font-size="12" fill="#222222">tired</text>
  <rect x="120" y="292" width="92" height="16" rx="2" fill="#64b5f6"/>
  <text x="218" y="304" font-size="11" fill="#1565c0"> ← helps disambiguate "it" = "animal"</text>
</svg>

---

## Self-Attention — The Math

For each token, compute **Query**, **Key**, **Value** vectors:

```misc
Q = X · W_Q    (What am I looking for?)
K = X · W_K    (What do I contain?)
V = X · W_V    (What information do I provide?)

Attention(Q, K, V) = softmax(Q · K^T / √d_k) · V
```

```python
import torch
import torch.nn.functional as F

def self_attention(Q, K, V):
    d_k = Q.size(-1)
    scores = torch.matmul(Q, K.transpose(-2, -1)) / (d_k ** 0.5)
    weights = F.softmax(scores, dim=-1)
    return torch.matmul(weights, V)
```

---

## Multi-Head Attention

Instead of one attention function, use multiple "heads" in parallel:

```diagram
          Input
     ┌─────┼─────┐
   Head 1 Head 2 Head 3 ... Head h
     │      │      │           │
   Attn   Attn   Attn       Attn
     │      │      │           │
     └──────┴──────┴───────────┘
              │
          Concatenate
              │
        Linear projection
              │
          Output
```

Each head can learn different relationship patterns:
- Head 1: syntactic relationships
- Head 2: semantic relationships
- Head 3: positional relationships

---

## Positional Encoding

Transformers have no inherent sense of order. We add position information:

```python
import numpy as np

def positional_encoding(seq_len, d_model):
    """Generate sinusoidal positional encoding."""
    pe = np.zeros((seq_len, d_model))
    position = np.arange(seq_len)[:, np.newaxis]
    div_term = np.exp(
        np.arange(0, d_model, 2) * -(np.log(10000.0) / d_model)
    )
    pe[:, 0::2] = np.sin(position * div_term)
    pe[:, 1::2] = np.cos(position * div_term)
    return pe

# Each position gets a unique encoding vector
# Nearby positions have similar encodings
```

Modern models use **Rotary Position Embeddings** (`RoPE`) instead.

---

## Tokenization — How Text Becomes Numbers

Models don't see text — they see token IDs:

```python
from transformers import GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

text = "Generative AI is transforming software development"
tokens = tokenizer.encode(text)
print(tokens)
# [8645, 876, 4208, 318, 16327, 3788, 2478]

# Decode individual tokens
for t in tokens:
    print(f"  {t:5d} → '{tokenizer.decode([t])}'")
# 8645  → 'Gener'
# 876   → 'ative'
# 4208  → ' AI'
# 318   → ' is'
# 16327 → ' transforming'
# 3788  → ' software'
# 2478  → ' development'
```

---

## Tokenization Methods

| Method | Description | Used By |
|--------|-------------|---------|
| `BPE` | Byte-Pair Encoding — merge frequent pairs | `GPT`, `LLaMA` |
| `WordPiece` | Similar to BPE, uses likelihood | `BERT` |
| `SentencePiece` | Language-agnostic, works on raw text | `T5`, `LLaMA` |
| `Tiktoken` | Fast BPE implementation | `GPT-3.5/4` |

```diagram
BPE example — learning merges:
  Step 0: ['l', 'o', 'w', 'e', 'r']     → frequency analysis
  Step 1: ['lo', 'w', 'e', 'r']          → merge 'l'+'o'
  Step 2: ['low', 'e', 'r']              → merge 'lo'+'w'
  Step 3: ['low', 'er']                  → merge 'e'+'r'
  Step 4: ['lower']                      → merge 'low'+'er'
```

---

## Why Tokenization Matters

Token count affects **cost**, **context window**, and **performance**:

```python
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4")

examples = [
    "Hello world",           # 2 tokens
    "supercalifragilistic",  # 5 tokens (split into subwords)
    "こんにちは",               # 3 tokens (non-English = more tokens)
    "def f(x): return x+1",  # 9 tokens
]

for text in examples:
    tokens = enc.encode(text)
    print(f"{len(tokens):2d} tokens: {text}")
    # Cost = tokens × price_per_token
```

**Rule of thumb:** ~4 characters ≈ 1 token (English text)

---

## Encoder vs. Decoder vs. Encoder-Decoder

```diagram
┌─────────────────────────────────────────────────────────┐
│ ENCODER-ONLY          │ Full bidirectional attention     │
│ (BERT, RoBERTa)       │ Good for: classification,       │
│                        │ embeddings, NER                 │
├─────────────────────────────────────────────────────────┤
│ DECODER-ONLY          │ Causal (left-to-right) attention│
│ (GPT, LLaMA, Claude)  │ Good for: text generation,      │
│                        │ chat, code                      │
├─────────────────────────────────────────────────────────┤
│ ENCODER-DECODER       │ Encode full input, then decode  │
│ (T5, BART)             │ Good for: translation,          │
│                        │ summarization                   │
└─────────────────────────────────────────────────────────┘
```

**Modern generative models are almost all decoder-only.**

---

## How Text Generation Works — Autoregressive Decoding

The model generates one token at a time, feeding output back as input:

```misc
Step 1: Input:  "The capital of France is"
        Output: "Paris"   (most probable next token)

Step 2: Input:  "The capital of France is Paris"
        Output: ","       (next most probable)

Step 3: Input:  "The capital of France is Paris,"
        Output: " known"

... and so on until <EOS> or max_length
```

```python
# Simplified generation loop
tokens = tokenize(prompt)
for _ in range(max_new_tokens):
    logits = model(tokens)          # forward pass
    next_token = sample(logits[-1]) # pick next token
    tokens.append(next_token)
    if next_token == EOS:
        break
```

---

## Sampling Strategies

| Strategy | Description | Effect |
|----------|-------------|--------|
| **Greedy** | Always pick highest probability token | Deterministic, can be repetitive |
| **Temperature** | Scale logits before softmax | Low=focused, High=creative |
| **Top-k** | Only consider k most likely tokens | Reduces unlikely outputs |
| **Top-p (nucleus)** | Consider tokens summing to probability p | Adaptive vocabulary size |

```python
# Temperature scaling
def temperature_sample(logits, temperature=1.0):
    scaled = logits / temperature
    probs = softmax(scaled)
    return np.random.choice(len(probs), p=probs)

# temperature=0.1 → very focused (almost greedy)
# temperature=1.0 → balanced
# temperature=2.0 → very creative/random
```

---

## Top-p (Nucleus) Sampling Visualized

```diagram
Token probabilities (sorted):

"Paris"    ████████████████████ 0.40
"Lyon"     ████████████         0.24
"the"      ██████               0.12
"a"        ████                 0.08
"Marseille"███                  0.06
"Berlin"   ██                   0.04
"one"      █                    0.02
"London"   ░                    0.01
...        ░                    ...

Top-p = 0.9: Include tokens until cumulative prob ≥ 0.9
→ Select from: {Paris, Lyon, the, a, Marseille, Berlin}
→ Exclude: {one, London, ...}
```

---

## Emergence — Surprising Capabilities at Scale

Some abilities only appear when models reach sufficient size:

```diagram
Capability          Small    Medium    Large
────────────────────────────────────────────
Basic grammar       ✓        ✓         ✓
Simple Q&A          ✗        ✓         ✓
Translation         ✗        ~         ✓
Chain-of-thought    ✗        ✗         ✓
Math reasoning      ✗        ✗         ✓
Code generation     ✗        ✗         ✓
Theory of mind      ✗        ✗         ~
```

This is called **emergent behavior** — capabilities that cannot be predicted by extrapolating from smaller models.

---

## Scaling Laws

Research shows predictable relationships between model size and performance:

```diagram
Loss
 │
 │╲
 │ ╲
 │  ╲
 │   ╲
 │    ╲          ← Power law: L(N) = (N_c / N)^α
 │     ╲╲
 │       ╲╲
 │         ╲╲╲
 │            ╲╲╲╲╲
 │                  ╲╲╲╲╲╲╲╲
 └─────────────────────────────── Parameters (N)
  1M    10M   100M   1B    10B   100B

Three axes of scaling:
  1. Model size (parameters)
  2. Dataset size (tokens)
  3. Compute budget (FLOPs)
```

**Chinchilla law:** Optimal training uses ~20 tokens per parameter.

---

## The Chinchilla Insight

Many early models were **undertrained** relative to their size:

| Model | Parameters | Training Tokens | Ratio |
|-------|-----------|-----------------|-------|
| `GPT-3` | 175B | 300B | 1.7× |
| `Chinchilla` | 70B | 1.4T | 20× |
| `LLaMA` | 65B | 1.4T | 21.5× |
| `LLaMA 2` | 70B | 2T | 28.6× |

**Chinchilla (70B)** outperformed **Gopher (280B)** because it was trained on 4× more data despite being 4× smaller.

**Lesson:** Data quality and quantity matter as much as model size.

---

## Hallucinations — The Core Challenge

`LLM`s generate plausible-sounding but incorrect information:

```python
# Example of hallucination
prompt = "Who won the 2026 Nobel Prize in Physics?"
# Model might confidently generate a plausible but
# completely fabricated answer

# Types of hallucination:
# 1. Factual errors     — wrong facts stated confidently
# 2. Fabricated sources  — citing papers that don't exist
# 3. Logical errors      — correct premises, wrong conclusion
# 4. Temporal confusion  — mixing up time periods
```

**Why it happens:**
- Models learn **statistical patterns**, not **truth**
- Training data contains contradictions
- No built-in fact-checking mechanism
- Models are trained to be **fluent**, not **accurate**

---

## Context Windows — How Much Can a Model "See"?

| Model | Context Window | Equivalent |
|-------|---------------|------------|
| `GPT-3` | 4K tokens | ~3 pages |
| `GPT-3.5` | 16K tokens | ~12 pages |
| `GPT-4` | 128K tokens | ~100 pages |
| `Claude 3.5` | 200K tokens | ~150 pages |
| `Gemini 1.5` | 1M tokens | ~750 pages |

```diagram
┌─────────────────────────────────────┐
│     CONTEXT WINDOW (128K tokens)    │
│ ┌─────────────┐ ┌────────────────┐  │
│ │  System      │ │  Conversation  │  │
│ │  Prompt      │ │  History       │  │
│ │  (500 tok)   │ │  (50K tok)     │  │
│ └─────────────┘ └────────────────┘  │
│ ┌─────────────┐ ┌────────────────┐  │
│ │  Retrieved   │ │  User Query    │  │
│ │  Context     │ │  (200 tok)     │  │
│ │  (70K tok)   │ │                │  │
│ └─────────────┘ └────────────────┘  │
│ Remaining for generation: ~7.3K tok │
└─────────────────────────────────────┘
```

---

## Real-World Applications of Generative AI

```diagram
┌─────────────────┬──────────────────────────────────────┐
│ Domain          │ Applications                          │
├─────────────────┼──────────────────────────────────────┤
│ Software Dev    │ Code generation, debugging, review    │
│ Content         │ Writing, marketing, translation       │
│ Customer Svc    │ Chatbots, email drafting, FAQ         │
│ Healthcare      │ Clinical notes, drug discovery        │
│ Legal           │ Contract review, case research        │
│ Finance         │ Report generation, risk analysis      │
│ Education       │ Tutoring, curriculum design           │
│ Research        │ Literature review, hypothesis gen     │
└─────────────────┴──────────────────────────────────────┘
```

---

## The Cost of Generative AI

Understanding the economics:

```python
# Typical API pricing (as of 2025)
pricing = {
    "gpt-4o": {
        "input": 2.50,    # per 1M tokens
        "output": 10.00,
    },
    "gpt-4o-mini": {
        "input": 0.15,
        "output": 0.60,
    },
    "claude-3.5-sonnet": {
        "input": 3.00,
        "output": 15.00,
    },
}

# Example: Processing 1000 customer emails
# Average email: ~500 tokens input, ~200 tokens output
# GPT-4o cost: (500K × $2.50 + 200K × $10.00) / 1M = $3.25
# GPT-4o-mini: (500K × $0.15 + 200K × $0.60) / 1M = $0.20
```

---

## Generative AI vs. Traditional ML

| Aspect | Traditional ML | Generative AI |
|--------|---------------|---------------|
| Training data | Labeled, structured | Unlabeled text corpus |
| Task specification | Feature engineering | Natural language prompt |
| Adaptation | Retrain model | Prompt / few examples |
| Output | Classification/number | Free-form text/image |
| Interpretability | Often analyzable | Black box |
| Compute cost | Moderate | Very high |
| Development time | Weeks–months | Minutes–hours |

---

## Hands-On: Your First API Call

```python
from openai import OpenAI

client = OpenAI()  # Uses OPENAI_API_KEY env variable

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "What is generative AI in one sentence?"
        }
    ],
    temperature=0.7,
    max_tokens=100,
)

print(response.choices[0].message.content)
# "Generative AI refers to artificial intelligence systems
#  that can create new content such as text, images, audio,
#  and video by learning patterns from training data."
```

---

## Key Takeaways — Overview of Generative AI

1. **Generative AI** creates new content by learning data distributions
1. The **Transformer** architecture (2017) is the foundation
1. **Self-attention** allows models to understand relationships between all tokens
1. **Autoregressive generation** produces one token at a time
1. **Scaling laws** predict performance from model size, data, and compute
1. **Hallucinations** remain the biggest practical challenge
1. **Context windows** define how much information a model can process
1. **Cost** varies dramatically between model sizes and providers

---

## Exercise: Exploring Tokenization

```python
"""
Exercise: Explore how different text is tokenized.

1. Install tiktoken: pip install tiktoken
1. Try tokenizing the following and observe token counts:
   - English text vs. code vs. other languages
   - Common words vs. rare technical terms
   - Numbers and dates
1. Calculate the cost of processing a document
"""
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

texts = [
    "The quick brown fox jumps over the lazy dog",
    "def fibonacci(n): return n if n < 2 else fibonacci(n-1) + fibonacci(n-2)",
    "SELECT * FROM users WHERE age > 25 ORDER BY name",
    "2024-01-15T14:30:00Z",
]

for text in texts:
    tokens = enc.encode(text)
    print(f"Tokens: {len(tokens):3d} | Text: {text[:50]}")
```

---

## The Training Compute Frontier

```diagram
Model         Training Compute (FLOPs)    Year
───────────────────────────────────────────────
GPT-2         1.5 × 10^19                 2019
GPT-3         3.1 × 10^23                 2020
PaLM          2.5 × 10^24                 2022
GPT-4         ~2.1 × 10^25 (est.)        2023
Gemini Ultra  ~5 × 10^25 (est.)          2023
LLaMA 3 405B  ~3.8 × 10^25 (est.)       2024

Compute doubles approximately every 6-8 months.
The cost of frontier training runs is growing
faster than Moore's Law.
```

---

## Attention Patterns — What the Model "Sees"

```python
# Visualizing attention weights
from transformers import AutoModel, AutoTokenizer
import matplotlib.pyplot as plt

model = AutoModel.from_pretrained("bert-base-uncased",
                                   output_attentions=True)
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

text = "The bank by the river had steep walls"
inputs = tokenizer(text, return_tensors="pt")
outputs = model(**inputs)

# outputs.attentions: tuple of (batch, heads, seq, seq)
# Layer 6, Head 3 might focus on syntactic relations
# Layer 11, Head 8 might focus on semantic relations

attn = outputs.attentions[6][0, 3]  # Layer 6, Head 3
tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
# Visualize as heatmap: which tokens attend to which

# Key insight: different heads specialize in different
# types of relationships (syntax, coreference, position)
```

---

## The Mixture-of-Experts (MoE) Architecture

Used by `Mixtral`, `GPT-4` (rumored), and `Switch Transformer`:

```diagram
Standard Transformer FFN:
  Every token processed by ALL parameters

MoE FFN:
  Each token routed to TOP-K experts (e.g., 2 of 8)

┌──────────────────────────────────────┐
│           ROUTER (gate)               │
│  Decides which experts to activate    │
│  Based on token's hidden state        │
└───┬────┬────┬────┬────┬────┬───┬────┘
    │    │    │    │    │    │   │
  ┌─▼─┐┌─▼─┐┌─▼─┐┌─▼─┐┌─▼─┐┌▼──┐┌▼──┐┌───┐
  │E1 ││E2 ││E3 ││E4 ││E5 ││E6 ││E7 ││E8 │
  │   ││ ★ ││   ││   ││ ★ ││   ││   ││   │
  └───┘└─┬─┘└───┘└───┘└─┬─┘└───┘└───┘└───┘
         │               │     ★ = selected
         └───────┬───────┘
              combine

Mixtral 8×7B: 8 experts × 7B each = 47B total params
  But only 2 experts active = ~13B params per token
  Speed of a 13B model, quality of a 47B model!
```

---

## Training Data Controversies

```misc
Key debates around LLM training data:

1. COPYRIGHT
   Models trained on copyrighted material without permission
   └─ NYT v. OpenAI (2024): lawsuit over article reproduction
   └─ Getty v. Stability AI: image copyright claims
   └─ Authors Guild v. OpenAI: book reproduction

2. DATA CONTAMINATION
   Test benchmarks may be in training data
   └─ Inflated benchmark scores
   └─ Models memorize rather than generalize
   └─ Contamination detection is an active research area

3. PERSONAL DATA
   Web scraping captures personal information
   └─ GDPR right to be forgotten vs. training data
   └─ Models can sometimes reproduce personal info
   └─ Deduplication helps but doesn't eliminate

4. DATA LAUNDERING
   Using LLM outputs as training data for other LLMs
   └─ "Model collapse" — quality degrades over generations
   └─ Reinforces existing biases and errors
```

---

## Understanding Model Sizes

```python
# What does "175 billion parameters" actually mean?

def model_size_breakdown(name, params_b, layers, hidden, heads):
    """Calculate where parameters live in a transformer."""
    head_dim = hidden // heads
    per_layer = {
        "self_attention": {
            "Q,K,V projections": 3 * hidden * hidden,
            "output projection": hidden * hidden,
        },
        "feed_forward": {
            "up projection": hidden * 4 * hidden,
            "down projection": 4 * hidden * hidden,
        },
        "layer_norms": 4 * hidden,
    }

    total_per_layer = sum(
        sum(v.values()) if isinstance(v, dict) else v
        for v in per_layer.values()
    )

    embedding = 50257 * hidden  # vocab × hidden
    total = layers * total_per_layer + embedding

    print(f"{name}: {params_b}B parameters")
    print(f"  {layers} layers × {total_per_layer:,} params/layer")
    print(f"  Embedding: {embedding:,}")
    print(f"  Calculated: {total:,}")

model_size_breakdown("GPT-3", 175, 96, 12288, 96)
model_size_breakdown("LLaMA-3-8B", 8, 32, 4096, 32)
```

---

## The Inference Cost Problem

```misc
Inference costs at scale:

Scenario: 1 million users, 10 queries/day, 500 tokens each

Daily token volume: 10M queries × 500 tokens = 5 billion tokens

Cost per day:
  GPT-4o:      5B × $10/1M = $50,000/day = $1.5M/month
  GPT-4o-mini: 5B × $0.60/1M = $3,000/day = $90K/month
  Self-hosted 70B: ~$5,000/day = $150K/month (+ hardware)
  Self-hosted 7B:  ~$500/day = $15K/month

Optimization strategies:
  1. Speculative decoding (draft model + verify)
  2. KV cache optimization (PagedAttention)
  3. Model distillation (smaller model, similar quality)
  4. Prompt caching (reuse system prompt computation)
  5. Batching (process multiple requests together)
  6. Quantization (4-bit inference for 3-4× speedup)
```

---

## Retrieval-Augmented Generation (RAG) — Preview

```diagram
Why RAG matters (covered in depth on Day 3):

Problem: LLMs have knowledge cutoffs and hallucinate

Solution: Give the model relevant documents at query time

┌─────────────────────────────────────────────┐
│  User: "What was our Q4 revenue?"           │
│                                              │
│  Step 1: Search company docs                │
│  Step 2: Retrieve: "Q4 revenue: $12.3M..."  │
│  Step 3: Generate response WITH the document│
│  Step 4: "Based on the financial report,    │
│           Q4 revenue was $12.3 million."     │
│                                              │
│  Benefits:                                   │
│  - Grounded in actual data (less hallucination)│
│  - Up-to-date information (no cutoff)        │
│  - Auditable (can cite sources)              │
│  - Domain-specific without fine-tuning       │
└─────────────────────────────────────────────┘
```

---

## Multimodal Models

Models that process multiple types of input:

```template
MULTIMODAL CAPABILITIES
━━━━━━━━━━━━━━━━━━━━━━━━

Text + Image → Text
  "Describe this diagram" + [image] → description
  Used for: visual Q&A, accessibility, document analysis

Text → Image
  "A sunset over mountains" → [generated image]
  Used for: creative design, prototyping, content creation

Text + Audio → Text
  "Transcribe and summarize" + [audio] → text summary
  Used for: meeting notes, podcast summaries

Text → Audio
  "Read this aloud in a calm voice" → [speech audio]
  Used for: accessibility, audiobooks, voice assistants

Text + Video → Text (emerging)
  "What happens in this video?" + [video] → description
  Used for: video analysis, content moderation
```

```python
# GPT-4o handles text, image, and audio natively
# All modalities share the same model architecture
```

---

## Practical Exercise: End of Day 1

```python
"""
Day 1 Comprehensive Exercise:

Part 1: Tokenization Exploration
  - Compare token counts across 3 languages
  - Calculate cost of processing a 10-page document
  - Find the longest single-token English word

Part 2: Model Comparison
  - Send the same 5 prompts to GPT-4o-mini and GPT-4o
  - Compare: response quality, token usage, latency
  - Calculate the cost difference

Part 3: Parameter Analysis
  - Given a model with 32 layers, hidden_dim=4096,
    and 32 attention heads:
  - Calculate total parameters
  - Estimate memory needed for FP16, INT8, and INT4
  - What GPU would you need for each?

Part 4: Discussion
  - What are 3 applications where generative AI
    would NOT be appropriate? Why?
  - What are the biggest risks of deploying an
    LLM without proper evaluation?
"""
```
