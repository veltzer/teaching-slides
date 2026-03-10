# Language Modeling with GPT and ChatGPT

---

## What is a Language Model?

A language model assigns probabilities to sequences of tokens:

```text
P("The cat sat on the mat") = 0.0001
P("The cat sat on the xyz") = 0.0000000001

The model learns: P(next_token | previous_tokens)

Example:
  P("Paris" | "The capital of France is") = 0.85
  P("Lyon"  | "The capital of France is") = 0.03
  P("a"     | "The capital of France is") = 0.02
```

**Core insight:** A good language model must understand grammar, facts, reasoning, and world knowledge.

---

## From N-grams to Neural Language Models

```text
Evolution of Language Modeling:

N-grams (1990s)     → Count word sequences in corpus
                       P(w | w-1, w-2) from frequency tables
                       Problem: sparse data, no generalization

RNNs (2010s)        → Process sequences with hidden state
                       P(w | h_t) where h_t encodes history
                       Problem: forgets long-range dependencies

LSTMs (2014)        → Gated memory cells
                       Better at long-range, still sequential
                       Problem: slow training, limited context

Transformers (2017) → Parallel attention over all positions
                       P(w | all previous tokens simultaneously)
                       Solved: parallelism, long-range, scalable
```

---

## The GPT Family

`GPT` = **G**enerative **P**re-trained **T**ransformer

| Model | Year | Params | Training Data | Key Innovation |
|-------|------|--------|---------------|----------------|
| `GPT-1` | 2018 | 117M | BookCorpus (5GB) | Pretrain + fine-tune |
| `GPT-2` | 2019 | 1.5B | WebText (40GB) | Zero-shot capabilities |
| `GPT-3` | 2020 | 175B | 570GB text | Few-shot learning |
| `GPT-3.5` | 2022 | 175B | + RLHF | Chat capability |
| `GPT-4` | 2023 | ~1.8T* | Massive corpus | Multimodal, reasoning |
| `GPT-4o` | 2024 | ~200B* | + multimodal | Faster, cheaper |

*Estimated, not officially disclosed

---

## GPT Architecture Deep Dive

```text
Input: "Explain quantum computing"

┌──────────────────────────────────────────┐
│            TOKEN EMBEDDING               │
│  "Explain" → [0.12, -0.34, 0.56, ...]   │
│  "quantum" → [0.78, 0.11, -0.45, ...]   │
│  "computing"→[-0.23, 0.67, 0.89, ...]   │
└──────────────────┬───────────────────────┘
                   │
           + Positional Encoding
                   │
┌──────────────────┴───────────────────────┐
│       TRANSFORMER DECODER BLOCK ×N       │
│  ┌────────────────────────────────────┐  │
│  │  Masked Multi-Head Self-Attention  │  │
│  │  (causal: can only look left)      │  │
│  └────────────────┬───────────────────┘  │
│  ┌────────────────┴───────────────────┐  │
│  │  Feed-Forward Network (MLP)        │  │
│  │  FFN(x) = GELU(xW₁ + b₁)W₂ + b₂  │  │
│  └────────────────┬───────────────────┘  │
│  Layer Norm + Residual connections       │
└──────────────────┬───────────────────────┘
                   │
┌──────────────────┴───────────────────────┐
│         LINEAR + SOFTMAX                 │
│  Vocabulary probability distribution     │
│  → next token: "in" (p=0.32)            │
└──────────────────────────────────────────┘
```

---

## Causal (Masked) Self-Attention

GPT uses **causal masking** — each token can only attend to tokens before it:

```text
Attention mask for "The cat sat on"

         The  cat  sat  on
The    [  1    0    0    0  ]
cat    [  1    1    0    0  ]
sat    [  1    1    1    0  ]
on     [  1    1    1    1  ]

1 = can attend, 0 = masked (set to -infinity before softmax)
```

This prevents "information leakage" from future tokens during training.

---

## Implementing Causal Attention in `Python`

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class CausalSelfAttention(nn.Module):
    def __init__(self, d_model, n_heads):
        super().__init__()
        self.n_heads = n_heads
        self.d_head = d_model // n_heads
        self.qkv = nn.Linear(d_model, 3 * d_model)
        self.proj = nn.Linear(d_model, d_model)

    def forward(self, x):
        B, T, C = x.size()
        qkv = self.qkv(x).reshape(B, T, 3, self.n_heads, self.d_head)
        q, k, v = qkv.permute(2, 0, 3, 1, 4)  # 3 × B × H × T × D

        att = (q @ k.transpose(-2, -1)) / (self.d_head ** 0.5)
        # Apply causal mask
        mask = torch.triu(torch.ones(T, T), diagonal=1).bool()
        att = att.masked_fill(mask, float('-inf'))
        att = F.softmax(att, dim=-1)

        out = (att @ v).transpose(1, 2).reshape(B, T, C)
        return self.proj(out)
```

---

## GPT Pre-Training Objective

The training objective is simple: **predict the next token**.

```text
Training example:
  Input:  "The weather today is"
  Target: "very sunny and warm"

Loss calculation (cross-entropy):
  Position 5: model predicts → P("very")  = 0.12 → loss = -log(0.12)
  Position 6: model predicts → P("sunny") = 0.08 → loss = -log(0.08)
  Position 7: model predicts → P("and")   = 0.45 → loss = -log(0.45)
  Position 8: model predicts → P("warm")  = 0.15 → loss = -log(0.15)

Total loss = average of all position losses
```

```python
# In PyTorch
loss_fn = nn.CrossEntropyLoss()
logits = model(input_ids)  # shape: [batch, seq_len, vocab_size]
loss = loss_fn(
    logits[:, :-1, :].reshape(-1, vocab_size),
    input_ids[:, 1:].reshape(-1)
)
```

---

## Pre-Training Data

What GPT models are trained on:

```text
┌───────────────────────────────────────────┐
│           TRAINING DATA MIX               │
├───────────────────┬───────────────────────┤
│ Web crawl data    │ ████████████████ 60%  │
│ Books             │ ████████ 16%          │
│ Wikipedia         │ ███ 6%                │
│ Code (GitHub)     │ █████ 10%             │
│ Academic papers   │ ██ 4%                 │
│ Curated datasets  │ ██ 4%                 │
└───────────────────┴───────────────────────┘
```

**Data quality matters enormously:**
- Deduplication reduces memorization
- Filtering removes toxic/low-quality content
- Domain mixing affects model capabilities
- Data cutoff date limits knowledge

---

## From GPT to ChatGPT — The Alignment Gap

Raw `GPT-3` is a **text completion** engine, not an **assistant**:

```text
User: "What is the capital of France?"

GPT-3 (base model) might continue:
  "What is the capital of Germany?
   What is the capital of Spain?
   What is the capital of Italy?"
   (It sees this as a list pattern!)

ChatGPT (aligned model):
  "The capital of France is Paris. It is located
   in the north-central part of the country..."
   (Helpful, relevant answer)
```

**Alignment** = making the model behave as intended (helpful, harmless, honest).

---

## ChatGPT Training — Three Stages

```text
Stage 1: PRE-TRAINING (unsupervised)
┌──────────────────────────────────┐
│ Predict next token on web text   │
│ Billions of parameters           │
│ Trillions of tokens              │
│ Result: capable but unaligned    │
└──────────────────┬───────────────┘
                   ▼
Stage 2: SUPERVISED FINE-TUNING (SFT)
┌──────────────────────────────────┐
│ Human-written ideal responses    │
│ Prompt → desired response pairs  │
│ ~100K examples                   │
│ Result: follows instructions     │
└──────────────────┬───────────────┘
                   ▼
Stage 3: RLHF (Reinforcement Learning from Human Feedback)
┌──────────────────────────────────┐
│ Humans rank model outputs        │
│ Train reward model on rankings   │
│ Optimize policy with PPO         │
│ Result: aligned, safe, helpful   │
└──────────────────────────────────┘
```

---

## Stage 1: Pre-Training in Detail

```python
# Conceptual pre-training loop
model = GPT(vocab_size=50257, n_layers=96, d_model=12288)
optimizer = AdamW(model.parameters(), lr=6e-5)

for batch in data_loader:  # Trillions of tokens
    input_ids = batch["input_ids"]     # [B, seq_len]

    logits = model(input_ids[:, :-1])  # Predict next token
    targets = input_ids[:, 1:]         # Shifted by 1

    loss = cross_entropy(logits, targets)
    loss.backward()
    optimizer.step()

# Training details for GPT-3 175B:
# - 300 billion tokens
# - 3.14 × 10^23 FLOPs
# - Estimated cost: $4-12 million
# - Training time: ~34 days on 1024 A100 GPUs
```

---

## Stage 2: Supervised Fine-Tuning (SFT)

Human labelers write ideal responses to prompts:

```python
# SFT training data format
sft_examples = [
    {
        "prompt": "Explain photosynthesis to a 5-year-old.",
        "response": "Plants eat sunlight! They take in light "
                    "from the sun through their green leaves, "
                    "mix it with water from the ground and air, "
                    "and make food for themselves. The green "
                    "color in leaves is what catches the sunlight."
    },
    {
        "prompt": "Write a Python function to reverse a string.",
        "response": "```python\ndef reverse_string(s):\n"
                    "    return s[::-1]\n```\n"
                    "This uses Python's slice notation with a "
                    "step of -1 to reverse the string."
    },
]

# Fine-tune on ~100K such examples
# Same loss function as pre-training (next token prediction)
# But only on the response tokens (mask the prompt)
```

---

## Stage 3: RLHF — Reinforcement Learning from Human Feedback

```text
Step 1: Collect comparison data
┌─────────────────────────────────────────┐
│ Prompt: "Write a haiku about coding"    │
│                                         │
│ Response A: "Fingers on the keys        │
│              Logic flows like a river    │
│              Bug found, start again"     │
│                                         │
│ Response B: "Code code code today        │
│              I like to write the code    │
│              Code is very fun"           │
│                                         │
│ Human ranks: A > B                      │
└─────────────────────────────────────────┘

Step 2: Train reward model on rankings
  reward_model(prompt, response) → scalar score

Step 3: Optimize with PPO
  Maximize reward while staying close to SFT model
```

---

## RLHF — The Reward Model

```python
class RewardModel(nn.Module):
    """Predicts a scalar reward for a (prompt, response) pair."""

    def __init__(self, base_model):
        super().__init__()
        self.backbone = base_model  # Start from SFT model
        self.reward_head = nn.Linear(d_model, 1)

    def forward(self, input_ids):
        hidden = self.backbone(input_ids)
        # Take the last token's hidden state
        reward = self.reward_head(hidden[:, -1, :])
        return reward

# Training objective (Bradley-Terry model):
# loss = -log(sigmoid(reward_preferred - reward_rejected))

# For each comparison pair:
r_w = reward_model(prompt + preferred_response)
r_l = reward_model(prompt + rejected_response)
loss = -torch.log(torch.sigmoid(r_w - r_l))
```

---

## RLHF — PPO Optimization

```text
PPO (Proximal Policy Optimization) loop:

┌──────────────────────────────────────┐
│  1. Sample prompt from dataset       │
│  2. Generate response with policy    │
│  3. Score with reward model          │
│  4. Compute advantage                │
│  5. Update policy (with KL penalty)  │
└──────────────────────────────────────┘

Objective:
  maximize  E[reward(prompt, response)]
  subject to  KL(policy || sft_model) < δ

The KL constraint prevents the model from
"reward hacking" — finding degenerate responses
that score high on the reward model but are
actually low quality.
```

---

## DPO — A Simpler Alternative to RLHF

**Direct Preference Optimization** (`DPO`) skips the reward model:

```python
# DPO loss function
def dpo_loss(policy_logprobs_w, policy_logprobs_l,
             ref_logprobs_w, ref_logprobs_l, beta=0.1):
    """
    w = preferred (winning) response
    l = rejected (losing) response
    """
    log_ratio_w = policy_logprobs_w - ref_logprobs_w
    log_ratio_l = policy_logprobs_l - ref_logprobs_l

    loss = -F.logsigmoid(beta * (log_ratio_w - log_ratio_l))
    return loss.mean()

# DPO advantages:
# - No reward model needed
# - No RL training loop (PPO is unstable)
# - Simpler implementation
# - Comparable or better results
```

---

## The Chat Format

`ChatGPT` uses a structured message format:

```python
messages = [
    {
        "role": "system",
        "content": "You are a helpful coding assistant. "
                   "Always include code examples."
    },
    {
        "role": "user",
        "content": "How do I read a CSV file in Python?"
    },
    {
        "role": "assistant",
        "content": "Here's how to read a CSV file..."
    },
    {
        "role": "user",
        "content": "How do I filter rows?"
    }
]

# Internally, this becomes a single token sequence:
# <|system|>You are...<|user|>How do I...<|assistant|>
```

---

## Understanding Model Parameters

Key parameters that control generation:

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    temperature=0.7,     # 0-2: randomness control
    max_tokens=500,      # Max output length
    top_p=0.9,           # Nucleus sampling threshold
    frequency_penalty=0.5,  # Reduce repetition
    presence_penalty=0.3,   # Encourage topic diversity
    stop=["\n\n"],       # Stop generation at this string
    n=1,                 # Number of completions to generate
    seed=42,             # For reproducible outputs
)
```

| Parameter | Low Value | High Value |
|-----------|-----------|------------|
| `temperature` | Focused, deterministic | Creative, diverse |
| `top_p` | Very selective | More options considered |
| `frequency_penalty` | May repeat phrases | Avoids repetition |
| `presence_penalty` | Stays on topic | Explores new topics |

---

## Temperature vs. Top-p — When to Use Which

```text
Task-Based Recommendations:
─────────────────────────────────────────────
Code generation:    temp=0.0-0.2, top_p=0.1
Factual Q&A:        temp=0.0-0.3, top_p=0.3
Business writing:   temp=0.3-0.5, top_p=0.5
Creative writing:   temp=0.7-1.0, top_p=0.9
Brainstorming:      temp=1.0-1.5, top_p=0.95
─────────────────────────────────────────────

General rule: Adjust ONE of temperature or top_p, not both.
Setting both can lead to unexpected behavior.
```

```python
# Deterministic (always same output)
response = client.chat.completions.create(
    model="gpt-4o", messages=messages,
    temperature=0, seed=42
)
```

---

## Comparing GPT with Other LLMs

```text
┌─────────────┬──────────┬──────────┬──────────┬──────────┐
│ Feature     │ GPT-4o   │ Claude 3 │ Gemini   │ LLaMA 3  │
│             │          │ Opus     │ 1.5 Pro  │ 70B      │
├─────────────┼──────────┼──────────┼──────────┼──────────┤
│ Provider    │ OpenAI   │Anthropic │ Google   │ Meta     │
│ Context     │ 128K     │ 200K     │ 1M       │ 128K     │
│ Open source │ No       │ No       │ No       │ Yes      │
│ Multimodal  │ Yes      │ Yes      │ Yes      │ Yes      │
│ Code        │ ★★★★★   │ ★★★★★   │ ★★★★    │ ★★★★    │
│ Reasoning   │ ★★★★★   │ ★★★★★   │ ★★★★    │ ★★★★    │
│ Cost        │ Medium   │ High     │ Medium   │ Free*    │
│ Speed       │ Fast     │ Medium   │ Fast     │ Varies   │
└─────────────┴──────────┴──────────┴──────────┴──────────┘
* Compute costs still apply for self-hosting
```

---

## The "Reasoning" Models — o1, o3, DeepSeek-R1

A new category: models that "think step by step" internally

```text
Standard model:
  Input → [single forward pass] → Output

Reasoning model:
  Input → [think...] → [think more...] → [verify...] → Output

Example:
  User: "How many r's in 'strawberry'?"

  Standard GPT-4: "There are 2 r's" (WRONG)

  o1-preview thinking:
    "Let me spell it out: s-t-r-a-w-b-e-r-r-y
     Position 3: r
     Position 8: r
     Position 9: r
     There are 3 r's." (CORRECT)
```

The model uses **chain-of-thought at inference time**, trading compute for accuracy.

---

## Model Distillation

Smaller models can learn from larger ones:

```text
Teacher Model (GPT-4 level, 1T+ params)
         │
         │ Generate training data
         │ (responses to diverse prompts)
         ▼
  ┌──────────────────┐
  │  Distillation     │
  │  Training         │
  │                   │
  │  Student learns   │
  │  to mimic teacher │
  └────────┬──────────┘
           │
           ▼
Student Model (7B params)
  - 99% of teacher quality on common tasks
  - 100× cheaper to run
  - Can run on consumer hardware
```

Examples: `GPT-4o-mini`, `Claude 3.5 Haiku`, `Phi-3`

---

## Benchmarks — How We Measure LLMs

| Benchmark | What It Measures | Top Score |
|-----------|-----------------|-----------|
| `MMLU` | Multitask knowledge (57 subjects) | ~90% |
| `HumanEval` | Code generation (`Python`) | ~95% |
| `GSM8K` | Grade school math | ~97% |
| `HellaSwag` | Commonsense reasoning | ~98% |
| `TruthfulQA` | Resistance to misconceptions | ~75% |
| `MATH` | Competition math problems | ~85% |
| `ARC-AGI` | Novel reasoning patterns | ~50% |

```text
Benchmark saturation problem:
  As models approach 100% on existing benchmarks,
  we need harder tests. This is an ongoing arms race.

  2022: "MMLU is the gold standard"
  2023: "MMLU is too easy, use MMLU-Pro"
  2024: "We need entirely new evaluation paradigms"
```

---

## Limitations of Current GPT Models

1. **Knowledge cutoff** — No information after training date
1. **Hallucinations** — Confidently states false information
1. **Math/logic** — Still makes basic arithmetic errors
1. **Consistency** — Different runs may give different answers
1. **Long context** — Performance degrades with very long inputs
1. **Bias** — Reflects biases in training data
1. **No true understanding** — Pattern matching vs. comprehension debate

```python
# Example of a limitation
prompt = "What is 3847 × 2918?"
# GPT might get this wrong without a calculator tool
# Solution: Tool use (function calling) to handle math
```

---

## Exercise: Comparing Model Behaviors

```python
"""
Exercise: Compare responses across different settings.

1. Send the same prompt with temperature 0 vs 1.5
2. Compare responses to the same factual question
3. Test a math problem with and without chain-of-thought
4. Observe how the system message changes behavior
"""
from openai import OpenAI
client = OpenAI()

prompt = "Explain how a neural network learns"

for temp in [0.0, 0.5, 1.0, 1.5]:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=temp,
        max_tokens=200
    )
    print(f"\n--- Temperature: {temp} ---")
    print(response.choices[0].message.content[:200])
```

---

## Key Takeaways — Language Modeling with GPT

1. `GPT` models are **decoder-only transformers** using causal attention
1. Pre-training objective: **predict the next token**
1. `ChatGPT` = `GPT` + **SFT** + **RLHF** (or `DPO`)
1. The three training stages progressively align the model
1. **Temperature** and **top-p** control generation randomness
1. Reasoning models trade **inference compute** for accuracy
1. Model distillation enables smaller, cheaper models
1. Benchmarks help compare but are increasingly saturated

---

## The Feed-Forward Network (FFN) Layer

The other major component in each transformer block:

```python
class FeedForward(nn.Module):
    """Position-wise feed-forward network."""

    def __init__(self, d_model, d_ff=None):
        super().__init__()
        d_ff = d_ff or 4 * d_model  # Typically 4× hidden dim

        # GPT-style FFN with GELU activation
        self.w1 = nn.Linear(d_model, d_ff)
        self.w2 = nn.Linear(d_ff, d_model)
        self.activation = nn.GELU()

    def forward(self, x):
        return self.w2(self.activation(self.w1(x)))

# Modern models use SwiGLU (LLaMA, Mistral):
class SwiGLU(nn.Module):
    def __init__(self, d_model, d_ff):
        super().__init__()
        self.gate = nn.Linear(d_model, d_ff, bias=False)
        self.up = nn.Linear(d_model, d_ff, bias=False)
        self.down = nn.Linear(d_ff, d_model, bias=False)

    def forward(self, x):
        return self.down(F.silu(self.gate(x)) * self.up(x))
```

---

## KV Cache — Speeding Up Inference

```text
Without KV cache (naive):
  Step 1: Process ["The"]          → compute K,V for all
  Step 2: Process ["The", "cat"]   → RECOMPUTE K,V for all
  Step 3: Process ["The", "cat", "sat"] → RECOMPUTE again
  Quadratic complexity!

With KV cache:
  Step 1: Process ["The"]          → cache K₁,V₁
  Step 2: Process ["cat"]          → cache K₂,V₂ (reuse K₁,V₁)
  Step 3: Process ["sat"]          → cache K₃,V₃ (reuse K₁,V₁,K₂,V₂)
  Linear complexity per token!
```

```python
# KV cache in practice
past_key_values = None
for token in generated_tokens:
    outputs = model(
        input_ids=token,
        past_key_values=past_key_values,  # Reuse cached K,V
        use_cache=True,
    )
    past_key_values = outputs.past_key_values
    next_token = sample(outputs.logits)
```

---

## Rotary Position Embeddings (RoPE)

Used by `LLaMA`, `Mistral`, and most modern models:

```text
Traditional position encoding:
  Add a fixed vector based on position
  x' = x + PE(position)

RoPE:
  ROTATE the query and key vectors based on position
  Applies 2D rotation in each dimension pair

Benefits over traditional:
  - Relative position information is built in
  - Generalizes to unseen sequence lengths
  - Better at long-range dependencies
  - No learned parameters (purely mathematical)
```

```python
def apply_rope(x, positions, dim):
    """Apply Rotary Position Embeddings."""
    freqs = 1.0 / (10000 ** (torch.arange(0, dim, 2) / dim))
    angles = positions[:, None] * freqs[None, :]
    cos = torch.cos(angles)
    sin = torch.sin(angles)
    x1, x2 = x[..., ::2], x[..., 1::2]
    return torch.cat([x1 * cos - x2 * sin,
                      x1 * sin + x2 * cos], dim=-1)
```

---

## Group Query Attention (GQA)

Memory-efficient attention used in `LLaMA 2/3`, `Mistral`:

```text
Multi-Head Attention (MHA):
  Q: 32 heads    K: 32 heads    V: 32 heads
  Each head has its own Q, K, V projections
  Memory: 3 × 32 × d_head = 96 × d_head

Grouped Query Attention (GQA):
  Q: 32 heads    K: 8 groups    V: 8 groups
  Multiple Q heads share the same K,V
  Memory: 32 × d_head + 2 × 8 × d_head = 48 × d_head

Multi-Query Attention (MQA):
  Q: 32 heads    K: 1 shared    V: 1 shared
  ALL Q heads share ONE K,V
  Memory: 32 × d_head + 2 × d_head = 34 × d_head

┌──────────┬──────────┬──────────┬───────────┐
│ Method   │ KV Heads │ KV Cache │ Quality   │
├──────────┼──────────┼──────────┼───────────┤
│ MHA      │ 32       │ 100%     │ Baseline  │
│ GQA-8    │ 8        │ 25%      │ ~99.5%    │
│ MQA      │ 1        │ 3%       │ ~98%      │
└──────────┴──────────┴──────────┴───────────┘
```

---

## Understanding Tokens and Pricing

```python
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

# Cost calculation example
def estimate_cost(prompt, expected_output_tokens=500,
                  model="gpt-4o"):
    pricing = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    }

    input_tokens = len(enc.encode(prompt))
    prices = pricing[model]

    input_cost = input_tokens * prices["input"] / 1_000_000
    output_cost = expected_output_tokens * prices["output"] / 1_000_000
    total = input_cost + output_cost

    print(f"Input:  {input_tokens:,} tokens = ${input_cost:.6f}")
    print(f"Output: {expected_output_tokens:,} tokens = ${output_cost:.6f}")
    print(f"Total:  ${total:.6f}")

    # At scale: 1M requests/month
    monthly = total * 1_000_000
    print(f"Monthly (1M requests): ${monthly:,.2f}")

estimate_cost("Explain quantum computing in 3 paragraphs")
```
