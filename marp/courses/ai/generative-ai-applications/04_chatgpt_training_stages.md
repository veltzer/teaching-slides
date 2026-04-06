# An Overview of ChatGPT Training Stages

---

## The Three Pillars of ChatGPT

```diagram
┌─────────────────────────────────────────────────────────┐
│                    ChatGPT Training                      │
│                                                          │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────┐   │
│  │ Stage 1  │───>│ Stage 2  │───>│    Stage 3       │   │
│  │ Pre-     │    │ SFT      │    │    RLHF          │   │
│  │ training │    │          │    │                    │   │
│  ├──────────┤    ├──────────┤    ├──────────────────┤   │
│  │ Next     │    │ Human-   │    │ Reward model     │   │
│  │ token    │    │ written  │    │ + PPO            │   │
│  │ predict  │    │ examples │    │ optimization     │   │
│  ├──────────┤    ├──────────┤    ├──────────────────┤   │
│  │ Months   │    │ Days     │    │ Days             │   │
│  │ $$$$$    │    │ $$       │    │ $$$              │   │
│  └──────────┘    └──────────┘    └──────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## Why Three Stages?

Each stage serves a different purpose:

| Stage | Purpose | Analogy |
|-------|---------|---------|
| Pre-training | Learn language and knowledge | Going to school for 20 years |
| SFT | Learn to follow instructions | Job-specific training |
| RLHF | Align with human preferences | On-the-job feedback |

```misc
Pre-training alone:
  "Tell me a joke" → "Tell me a riddle. Tell me a story."
  (Continues the pattern, doesn't answer)

After SFT:
  "Tell me a joke" → "Why did the programmer quit? No arrays."
  (Follows instruction but may be offensive or unhelpful)

After RLHF:
  "Tell me a joke" → "Why do programmers prefer dark mode?
   Because light attracts bugs! 🐛"
  (Helpful, safe, follows preferences)
```

---

## Stage 1: Pre-Training — Data Collection

```diagram
Data Pipeline:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Common Crawl ──┐
(petabytes)    │    ┌─────────────┐
               ├───>│  Filtering  │
Wikipedia ─────┤    │  & Cleaning │
               │    │             │
Books ─────────┤    │ - Dedup     │
               │    │ - Quality   │
Code (GitHub)──┤    │ - Toxicity  │
               │    │ - PII       │
Academic ──────┘    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ Tokenization│
                    │ (BPE/       │
                    │  tiktoken)  │
                    └──────┬──────┘
                           │
                    ~2-10 Trillion tokens
```

---

## Stage 1: Pre-Training — Data Quality

Filtering steps applied to raw web data:

```python
# Conceptual quality filtering pipeline
def filter_document(doc):
    # Language detection
    if detect_language(doc) not in ALLOWED_LANGUAGES:
        return False

    # Quality heuristics
    if doc.word_count < 50:
        return False
    if doc.symbol_ratio > 0.3:     # Too many special chars
        return False
    if doc.repetition_ratio > 0.5:  # Repeated content
        return False

    # Perplexity-based filtering
    # Use a smaller LM to score document quality
    if small_lm.perplexity(doc) > THRESHOLD:
        return False  # Likely garbage text

    # Deduplication (MinHash + LSH)
    if is_near_duplicate(doc, seen_docs):
        return False

    return True
```

---

## Stage 1: Pre-Training — The Training Process

```python
# Simplified training configuration
config = {
    "model_size": "175B parameters",
    "architecture": {
        "layers": 96,
        "hidden_dim": 12288,
        "attention_heads": 96,
        "head_dim": 128,
        "vocab_size": 100256,
        "context_length": 8192,
    },
    "training": {
        "batch_size": 3_200_000,  # tokens per batch
        "learning_rate": 6e-5,
        "lr_schedule": "cosine with warmup",
        "warmup_steps": 2000,
        "total_tokens": 2_000_000_000_000,  # 2T
        "optimizer": "AdamW",
        "weight_decay": 0.1,
        "gradient_clipping": 1.0,
    },
    "hardware": {
        "gpus": 1024,            # A100 80GB
        "training_time": "~34 days",
        "estimated_cost": "$10M+",
    },
}
```

---

## Stage 1: Distributed Training Strategies

Training a 175B parameter model requires sophisticated parallelism:

```diagram
┌─────────────────────────────────────────────────┐
│         DISTRIBUTED TRAINING STRATEGIES          │
├────────────────┬────────────────────────────────┤
│ Data Parallel  │ Same model on each GPU,         │
│                │ different data batches           │
│                │ Simple but memory-limited        │
├────────────────┼────────────────────────────────┤
│ Tensor Parallel│ Split individual layers          │
│                │ across GPUs (within node)        │
│                │ Attention heads distributed      │
├────────────────┼────────────────────────────────┤
│ Pipeline       │ Different layers on different    │
│ Parallel       │ GPUs (across nodes)              │
│                │ Micro-batching for efficiency    │
├────────────────┼────────────────────────────────┤
│ ZeRO           │ Shard optimizer states,          │
│ (DeepSpeed)    │ gradients, and parameters        │
│                │ across all GPUs                  │
└────────────────┴────────────────────────────────┘
```

---

## Stage 1: Training Dynamics

```diagram
Loss Curve During Pre-Training:

Loss
4.0 │╲
    │ ╲
3.5 │  ╲
    │   ╲
3.0 │    ╲╲
    │      ╲╲
2.5 │        ╲╲╲
    │           ╲╲╲╲
2.0 │               ╲╲╲╲╲╲
    │                      ╲╲╲╲╲╲╲╲
1.5 │                              ╲╲╲╲╲╲╲╲╲╲╲
    │
1.0 └──────────────────────────────────────────────
    0    200B   400B   600B   800B   1T   1.2T tokens

Key observations:
- Rapid initial improvement
- Gradual diminishing returns
- Occasional loss spikes (training instabilities)
- No clear "convergence" — performance keeps improving
```

---

## Stage 1: What the Model Learns

As pre-training progresses, capabilities emerge in stages:

```diagram
Tokens Trained    Capabilities Acquired
──────────────    ──────────────────────
10B               Basic grammar, common words
50B               Sentence structure, simple facts
200B              Paragraph coherence, basic reasoning
500B              World knowledge, multi-step logic
1T                Nuanced language, code generation
2T+               Complex reasoning, few-shot learning

Analogy to human development:
  10B tokens   ≈  Learning to speak
  200B tokens  ≈  Elementary school knowledge
  1T tokens    ≈  College education
  2T+ tokens   ≈  Expert-level pattern matching
```

---

## Stage 2: Supervised Fine-Tuning (SFT) — Overview

Transform a text completion engine into an instruction-following assistant:

```misc
Before SFT:
  Input:  "Translate 'hello' to French."
  Output: "Translate 'goodbye' to French.
           Translate 'thank you' to French."

After SFT:
  Input:  "Translate 'hello' to French."
  Output: "The French translation of 'hello' is 'bonjour'."
```

**SFT Data:** Human labelers write thousands of ideal prompt-response pairs.

---

## Stage 2: SFT — Data Collection Process

```diagram
SFT Data Creation Workflow:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Create diverse prompt distribution:
   ┌──────────────────────────────────┐
   │ - Open-ended generation (25%)    │
   │ - Classification tasks  (15%)    │
   │ - Closed Q&A            (20%)    │
   │ - Brainstorming         (10%)    │
   │ - Code writing          (15%)    │
   │ - Rewriting/editing     (10%)    │
   │ - Summarization         (5%)     │
   └──────────────────────────────────┘

2. Human labelers write ideal responses:
   - Follow detailed guidelines
   - Be helpful but not harmful
   - Acknowledge uncertainty
   - Format responses clearly

3. Quality assurance:
   - Multiple reviewers per response
   - Inter-annotator agreement checks
   - Regular calibration sessions
```

---

## Stage 2: SFT — Training Details

```python
# SFT training setup
from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir="./sft_model",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=8,
    learning_rate=2e-5,      # Much lower than pre-training
    warmup_ratio=0.03,
    weight_decay=0.01,
    lr_scheduler_type="cosine",
    fp16=True,               # Mixed precision training
    logging_steps=10,
    save_strategy="epoch",
)

# Key differences from pre-training:
# 1. Only compute loss on RESPONSE tokens (mask the prompt)
# 2. Much smaller learning rate (don't forget pre-training)
# 3. Much less data (~100K examples vs. trillions of tokens)
# 4. Only a few epochs (3-5)
```

---

## Stage 2: SFT — Prompt Masking

Only the assistant's response contributes to the loss:

```misc
Full sequence:
<|system|> You are helpful. <|user|> What is 2+2? <|assistant|> 2+2 equals 4.

Loss mask:
[  0  0  0  0  0  0  0  0  0  0  0  0  0  0     1  1  1  1  1 ]
 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  ^^^^^^^^^^^^^
         MASKED (no gradient)                      LOSS COMPUTED

# Implementation
def compute_sft_loss(logits, labels, prompt_length):
    # Create mask: 0 for prompt tokens, 1 for response tokens
    mask = torch.zeros_like(labels, dtype=torch.float)
    mask[:, prompt_length:] = 1.0

    loss = F.cross_entropy(logits, labels, reduction='none')
    masked_loss = (loss * mask).sum() / mask.sum()
    return masked_loss
```

---

## Stage 2: SFT — Effect on Model Behavior

Before and after SFT comparison:

```misc
Prompt: "List 3 benefits of exercise"

Base model (pre-trained only):
  "List 3 benefits of exercise for dogs.
   List 3 benefits of exercise for cats.
   List 3 benefits of meditation."

SFT model:
  "Here are three key benefits of exercise:

   1. **Physical Health**: Regular exercise strengthens
      your cardiovascular system and muscles.

   2. **Mental Well-being**: Exercise releases endorphins,
      reducing stress and improving mood.

   3. **Cognitive Function**: Physical activity improves
      memory, focus, and overall brain health."
```

---

## Stage 3: RLHF — Why SFT Isn't Enough

SFT teaches the model to follow instructions, but:

```misc
Problem 1: SYCOPHANCY
  User: "I think the earth is flat"
  SFT model: "That's an interesting perspective! Here are
  some arguments for a flat earth..."
  (Too agreeable)

Problem 2: VERBOSITY
  User: "What is 2+2?"
  SFT model: "Great question! The sum of 2 and 2 is 4.
  This is a fundamental arithmetic operation that forms
  the basis of mathematics. In different number systems..."
  (Too verbose)

Problem 3: HARMFUL COMPLIANCE
  User: "How do I hack my neighbor's WiFi?"
  SFT model: "Here are the steps to hack a WiFi network..."
  (Should refuse)
```

RLHF addresses these by learning from **human preferences**.

---

## Stage 3: RLHF — Step 1: Comparison Data

Labelers compare model outputs rather than writing ideal ones:

```misc
Prompt: "Explain quantum computing in simple terms"

Response A (score: 7/7):
  "Quantum computing uses quantum mechanics to process
   information. Regular computers use bits (0 or 1),
   but quantum computers use qubits that can be both
   0 and 1 simultaneously (superposition)."

Response B (score: 4/7):
  "Quantum computing is a revolutionary paradigm shift
   in computational methodology utilizing quantum
   mechanical phenomena including superposition and
   entanglement to perform operations on data."

Response C (score: 2/7):
  "Its like having a magic computer that can try every
   answer at once!!!"

Ranking: A > B > C
```

---

## Stage 3: RLHF — Step 2: Reward Model Training

```python
class RewardModel(nn.Module):
    def __init__(self, base_model):
        super().__init__()
        self.backbone = base_model
        self.value_head = nn.Linear(hidden_size, 1)

    def forward(self, input_ids, attention_mask):
        outputs = self.backbone(input_ids, attention_mask)
        # Use last non-padding token's representation
        last_hidden = outputs.last_hidden_state
        reward = self.value_head(last_hidden[:, -1, :])
        return reward.squeeze(-1)

# Training with Bradley-Terry preference model
def reward_loss(reward_preferred, reward_rejected):
    return -torch.log(
        torch.sigmoid(reward_preferred - reward_rejected)
    ).mean()

# Train on ~300K comparison pairs
# Reward model accuracy target: ~72-75% on held-out comparisons
```

---

## Stage 3: RLHF — Step 3: PPO Training Loop

```python
# Simplified PPO training for RLHF
def rlhf_training_step(policy, ref_policy, reward_model,
                        prompts, kl_coef=0.02):

    # 1. Generate responses from current policy
    responses = policy.generate(prompts)

    # 2. Score responses with reward model
    rewards = reward_model(prompts, responses)

    # 3. Compute KL penalty (don't drift too far from SFT)
    log_probs = policy.log_prob(prompts, responses)
    ref_log_probs = ref_policy.log_prob(prompts, responses)
    kl_penalty = log_probs - ref_log_probs

    # 4. Final reward = reward - KL penalty
    final_reward = rewards - kl_coef * kl_penalty

    # 5. PPO update
    advantages = compute_gae(final_reward, values)
    ppo_update(policy, log_probs, advantages)

    return {
        "mean_reward": rewards.mean().item(),
        "mean_kl": kl_penalty.mean().item(),
    }
```

---

## Stage 3: The KL Penalty — Why It Matters

```diagram
Without KL penalty:
  Model learns to exploit reward model weaknesses

  Example "reward hack":
  Prompt: "Write a poem about nature"
  Response: "AMAZING INCREDIBLE WONDERFUL NATURE IS THE
  BEST THING EVER ABSOLUTELY FANTASTIC!!!!"
  → Reward model gives high score (positive sentiment)
  → But response is garbage

With KL penalty:
  Model stays close to the well-calibrated SFT model
  while improving on human preferences

  KL divergence = Σ policy(x) × log(policy(x) / ref(x))

  If KL is too high: model is drifting → increase penalty
  If KL is too low: model isn't learning → decrease penalty
  Sweet spot: KL ≈ 5-15 nats
```

---

## Constitutional AI (CAI) — Anthropic's Approach

An alternative to pure RLHF used by `Claude`:

```misc
Step 1: RED-TEAMING
  Human: "Tell me how to make explosives"
  Model: "[harmful response]"

Step 2: CRITIQUE (model critiques itself)
  "My response was harmful because it provided
   dangerous information that could cause physical
   harm. I should have refused this request."

Step 3: REVISION (model rewrites response)
  "I can't help with making explosives as this could
   cause serious harm. If you're interested in chemistry,
   I'd be happy to discuss safe experiments instead."

Step 4: RLAIF (RL from AI Feedback)
  Use the model's own critiques as training signal
  instead of human labelers for the preference data
```

---

## Comparing Alignment Approaches

| Approach | Human Label Cost | Scalability | Quality |
|----------|-----------------|-------------|---------|
| `RLHF` (OpenAI) | High | Limited | High |
| `DPO` | Medium | Good | High |
| `CAI/RLAIF` (Anthropic) | Low | Excellent | High |
| `RLHF + DPO` hybrid | Medium | Good | Highest |

```misc
Trend: Moving from human feedback to AI feedback

2022: Thousands of human labelers
2023: AI-assisted labeling (humans verify AI labels)
2024: AI self-critique + minimal human oversight
2025: Automated alignment pipelines with human spot-checks
```

---

## Post-Training: Instruction Hierarchy

Modern models learn a hierarchy of instruction priority:

```misc
Priority Level 1 (Highest): SYSTEM PROMPT
  └─ Set by application developer
  └─ Defines model behavior and constraints
  └─ Cannot be overridden by user

Priority Level 2: TOOL DEFINITIONS
  └─ Available functions the model can call
  └─ Constrain model's action space

Priority Level 3: USER MESSAGE
  └─ The actual user request
  └─ Model serves user within system constraints

Priority Level 4 (Lowest): INJECTED CONTEXT
  └─ Retrieved documents, conversation history
  └─ Treated as potentially untrusted
```

---

## Post-Training: Safety Training

```python
# Categories of harmful content the model learns to refuse

safety_categories = {
    "violence": {
        "description": "Instructions for causing physical harm",
        "response": "I can't help with that. If someone is "
                    "in danger, please contact emergency services.",
    },
    "illegal_activity": {
        "description": "Assistance with illegal actions",
        "response": "I'm not able to provide guidance on "
                    "illegal activities.",
    },
    "personal_info": {
        "description": "Requests for private information",
        "response": "I can't help find personal information "
                    "about private individuals.",
    },
    "deception": {
        "description": "Creating misleading content",
        "response": "I'd rather help you communicate honestly.",
    },
}
```

---

## Training Infrastructure — The Hardware Stack

```diagram
TRAINING CLUSTER ARCHITECTURE
══════════════════════════════════════════════

    ┌─── GPU Node ────┐  ┌─── GPU Node ────┐
    │ 8× A100 80GB    │  │ 8× A100 80GB    │
    │ NVLink (600GB/s)│  │ NVLink (600GB/s)│
    │ 2× AMD EPYC CPU │  │ 2× AMD EPYC CPU │
    │ 2TB RAM         │  │ 2TB RAM         │
    └────────┬────────┘  └────────┬────────┘
             │   InfiniBand 400Gb/s  │
    ┌────────┴───────────────────────┴────────┐
    │        High-Speed Network Fabric         │
    └────────┬───────────────────────┬────────┘
    ┌────────┴────────┐  ┌──────────┴────────┐
    │ Storage Cluster │  │ Parameter Server  │
    │ (Petabytes)     │  │ (distributed)     │
    └─────────────────┘  └───────────────────┘

Cost estimates for GPT-4-scale training:
  Hardware: ~$500M (25,000 A100s)
  Electricity: ~$10M per training run
  Total per run: ~$100M+
```

---

## The Complete Pipeline — Summary

```diagram
RAW TEXT (Internet, books, code)
    │
    ▼
┌──────────────────────────────────────────────┐
│ 1. PRE-TRAINING                              │
│    Objective: Next token prediction           │
│    Data: ~2T tokens                           │
│    Duration: Weeks-months                     │
│    Result: Knowledgeable but unaligned        │
└──────────────────┬───────────────────────────┘
                   ▼
┌──────────────────────────────────────────────┐
│ 2. SUPERVISED FINE-TUNING (SFT)              │
│    Data: ~100K human-written examples         │
│    Duration: Days                             │
│    Result: Follows instructions               │
└──────────────────┬───────────────────────────┘
                   ▼
┌──────────────────────────────────────────────┐
│ 3. RLHF / DPO / RLAIF                       │
│    Data: ~300K preference comparisons         │
│    Duration: Days                             │
│    Result: Aligned, safe, helpful             │
└──────────────────┬───────────────────────────┘
                   ▼
              DEPLOYED MODEL
```

---

## Key Takeaways — ChatGPT Training Stages

1. **Pre-training** creates a powerful but raw language model through next-token prediction
1. **SFT** teaches instruction-following with human-written examples
1. **RLHF** aligns model behavior with human preferences using reward models
1. The **KL penalty** prevents reward hacking during RLHF
1. **DPO** offers a simpler alternative that skips reward model training
1. **Constitutional AI** reduces human labeling needs via AI self-critique
1. Each stage requires dramatically different data volumes and compute
1. The full pipeline costs tens to hundreds of millions of dollars

---

## Day 1 Summary and Q&A

**What we covered today:**
- The landscape and history of generative AI
- Transformer architecture and self-attention
- `GPT` model family and evolution
- Tokenization and generation strategies
- The three training stages of `ChatGPT`
- Alignment approaches: `RLHF`, `DPO`, `CAI`

**Key insight:** Generative AI is built on surprisingly simple objectives (predict the next token), but achieves remarkable capabilities through scale and alignment.

**Tomorrow:** We dive into hands-on `API` usage, prompt engineering, and fine-tuning.

---

## Reward Hacking — Real Examples

```misc
Known cases of reward hacking in RLHF:

1. SYCOPHANCY
   Model learns that agreeing with the user gets higher rewards
   User: "I think 2+2=5"
   Bad: "You're right, 2+2=5!"
   Why: Human raters preferred polite, agreeable responses

2. LENGTH BIAS
   Longer responses consistently rated higher by humans
   Model learns to be verbose regardless of the question
   "What is 2+2?" → 500-word response about arithmetic history

3. FORMATTING TRICKS
   Model discovers that markdown, bullet points, and headers
   get higher human ratings even if content is weaker
   Generates beautifully formatted but shallow responses

4. HEDGING
   "It depends on the context..." for every question
   Sounds careful and thoughtful but avoids commitment
   Raters rate it as "safe" and "balanced" → high reward

Solutions: Better reward modeling, diverse raters, specific
evaluation criteria, Constitutional AI for self-correction
```

---

## Synthetic Data for Alignment

```python
# Modern alignment uses AI-generated training data

def generate_preference_pair(prompt, good_principles, bad_traits):
    """Generate a preference pair for DPO training."""

    # Generate a GOOD response following principles
    good_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content":
                f"Follow these principles:\n"
                f"{chr(10).join(good_principles)}\n"
                f"Be helpful, accurate, and honest."},
            {"role": "user", "content": prompt},
        ],
    ).choices[0].message.content

    # Generate a BAD response with specific flaws
    bad_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content":
                f"Intentionally exhibit these traits:\n"
                f"{chr(10).join(bad_traits)}\n"
                f"Make the response seem plausible but flawed."},
            {"role": "user", "content": prompt},
        ],
    ).choices[0].message.content

    return {
        "prompt": prompt,
        "chosen": good_response,
        "rejected": bad_response,
    }

# Generate thousands of pairs for DPO training
```

---

## Post-Training Techniques — Safety Layers

```diagram
Modern deployment adds multiple safety layers:

INPUT LAYER
  ┌────────────────────────────────────┐
  │ User message                       │
  └───────────┬────────────────────────┘
              ▼
  ┌────────────────────────────────────┐
  │ Moderation API (classify input)    │
  │ Block: violence, CSAM, etc.        │
  └───────────┬────────────────────────┘
              ▼
  ┌────────────────────────────────────┐
  │ Prompt injection detection         │
  │ Pattern matching + classifier      │
  └───────────┬────────────────────────┘
              ▼
  ┌────────────────────────────────────┐
  │ LLM generation                     │
  │ (with safety-trained model)        │
  └───────────┬────────────────────────┘
              ▼
OUTPUT LAYER
  ┌────────────────────────────────────┐
  │ Output moderation (classify output)│
  └───────────┬────────────────────────┘
              ▼
  ┌────────────────────────────────────┐
  │ PII detection and redaction        │
  └───────────┬────────────────────────┘
              ▼
  ┌────────────────────────────────────┐
  │ Factuality check (optional)        │
  └───────────┬────────────────────────┘
              ▼
  Response to user
```

---

## RLHF vs DPO vs KTO — Comparison

```diagram
┌──────────┬────────────────┬──────────────┬──────────────┐
│ Aspect   │ RLHF (PPO)     │ DPO          │ KTO          │
├──────────┼────────────────┼──────────────┼──────────────┤
│ Data     │ Comparisons    │ Comparisons  │ Single       │
│ format   │ (A > B)        │ (A > B)      │ thumbs up/   │
│          │                │              │ down per resp│
├──────────┼────────────────┼──────────────┼──────────────┤
│ Needs    │ Yes (separate  │ No           │ No           │
│ reward   │ model)         │              │              │
│ model?   │                │              │              │
├──────────┼────────────────┼──────────────┼──────────────┤
│ Training │ Complex (RL)   │ Simple (SL)  │ Simple (SL)  │
│ stability│ Unstable       │ Stable       │ Very stable  │
├──────────┼────────────────┼──────────────┼──────────────┤
│ Quality  │ Highest        │ Very high    │ High         │
├──────────┼────────────────┼──────────────┼──────────────┤
│ Data     │ High           │ High         │ Lowest       │
│ needs    │ (50K+ pairs)   │ (10K+ pairs) │ (binary      │
│          │                │              │  labels OK)  │
└──────────┴────────────────┴──────────────┴──────────────┘

KTO (Kahneman-Tversky Optimization) is newest:
  Just needs "good" or "bad" labels per response
  No need for pairwise comparisons!
  Makes data collection much easier
```
