# Parameter Efficient Fine Tuning — LoRA, QLoRA, Prompt Tuning

---

## The Problem: Full Fine-Tuning is Expensive

![the_problem_full_fine_tuning_is_expensive](svg/courses/ai/generative-ai-applications/15_peft_lora_qlora/the_problem_full_fine_tuning_is_expensive.svg)

---

## The Problem: Full Fine-Tuning is Expensive

**PEFT** solves this by training only a tiny fraction of parameters.

---

## PEFT Overview

![peft_overview](svg/courses/ai/generative-ai-applications/15_peft_lora_qlora/peft_overview.svg)

---

## LoRA — Low-Rank Adaptation

The key insight: weight updates during fine-tuning have low rank.
```misc
Standard fine-tuning:
  W_new = W_original + ΔW
  ΔW is a full d×d matrix (millions of parameters)
LoRA:
  W_new = W_original + B × A
  Where B is d×r and A is r×d, with r << d
  d = 4096 (hidden dimension)
  r = 16   (LoRA rank — much smaller!)
  ΔW parameters: 4096 × 4096 = 16,777,216
  LoRA parameters: 4096 × 16 + 16 × 4096 = 131,072
  Reduction: 128× fewer trainable parameters!
```

---
## LoRA — Low-Rank Adaptation

![lora_low_rank_adaptation](svg/courses/ai/generative-ai-applications/15_peft_lora_qlora/lora_low_rank_adaptation.svg)

---

## LoRA — How It Works During Forward Pass

![lora_how_it_works_during_forward_pass](svg/courses/ai/generative-ai-applications/15_peft_lora_qlora/lora_how_it_works_during_forward_pass.svg)

---

## LoRA — How It Works During Forward Pass

At inference, you can merge: W_new = W + B·A (no extra latency!)

---

## Implementing LoRA with PEFT Library

```python
from peft import LoraConfig, get_peft_model, TaskType
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load base model
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct",
    torch_dtype=torch.float16,
    device_map="auto",
)

# Configure LoRA
lora_config = LoraConfig(
    r=16,                      # Rank (4-64, higher = more capacity)
    lora_alpha=32,             # Scaling factor (usually 2×r)
    target_modules=[           # Which layers to adapt
        "q_proj", "k_proj",    # Attention query & key
        "v_proj", "o_proj",    # Attention value & output
        "gate_proj",           # MLP layers
        "up_proj", "down_proj",
    ],
    lora_dropout=0.05,         # Dropout for regularization
    bias="none",               # Don't train bias terms
    task_type=TaskType.CAUSAL_LM,
)

# Apply LoRA
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# trainable params: 83,886,080 || all params: 8,114,769,920
# trainable%: 1.03%
```

---

## LoRA Rank Selection

![lora_rank_selection](svg/courses/ai/generative-ai-applications/15_peft_lora_qlora/lora_rank_selection.svg)

---

## Training with LoRA

```python
from transformers import TrainingArguments, Trainer
from datasets import load_dataset

# Load and prepare dataset
dataset = load_dataset("my_dataset")

def format_example(example):
    return {
        "text": f"### Instruction:\n{example['instruction']}\n\n"
                f"### Response:\n{example['response']}"
    }

dataset = dataset.map(format_example)

# Training configuration
training_args = TrainingArguments(
    output_dir="./lora-output",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,  # Effective batch: 16
    learning_rate=2e-4,             # Higher than full FT
    warmup_steps=100,
    logging_steps=10,
    save_strategy="epoch",
    fp16=True,
    optim="paged_adamw_8bit",       # Memory-efficient optimizer
    report_to="tensorboard",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["validation"],
)

trainer.train()
```

---

## Saving and Loading LoRA Adapters

```python
# Save LoRA adapter (only ~80MB instead of 16GB!)
model.save_pretrained("./my-lora-adapter")

# Directory structure:
# my-lora-adapter/
# ├── adapter_config.json     (1KB)
# ├── adapter_model.safetensors  (80MB)
# └── README.md

# Load adapter onto base model
from peft import PeftModel

base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct",
    torch_dtype=torch.float16,
    device_map="auto",
)

model = PeftModel.from_pretrained(base_model, "./my-lora-adapter")

# Merge adapter into base model (for faster inference)
merged_model = model.merge_and_unload()
merged_model.save_pretrained("./merged-model")

# Benefits of keeping adapters separate:
# - Swap adapters at runtime for different tasks
# - Multiple adapters on one base model
# - Easy version control (track small adapter files)
```

---

## Multiple LoRA Adapters

![multiple_lora_adapters](svg/courses/ai/generative-ai-applications/15_peft_lora_qlora/multiple_lora_adapters.svg)

---

## QLoRA — Quantized LoRA

Combine 4-bit quantization with LoRA for maximum memory efficiency:

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

# Load model in 4-bit
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-70B-Instruct",
    quantization_config=bnb_config,
    device_map="auto",
)

# Prepare for k-bit training
model = prepare_model_for_kbit_training(model)

# Apply LoRA on top of quantized model
lora_config = LoraConfig(r=16, lora_alpha=32, target_modules="all-linear")
model = get_peft_model(model, lora_config)

# Now you can fine-tune a 70B model on a single 24GB GPU!
```

---

## QLoRA Memory Breakdown

```misc
Fine-tuning LLaMA 70B:

Full Fine-Tuning:
  Model (FP16):        140 GB
  Gradients:           140 GB
  Optimizer (Adam):    280 GB
  Activations:          50 GB
  Total:              ~610 GB  ← 8× A100 80GB ($200/hr)

LoRA (FP16 base):
  Model (FP16):        140 GB
  LoRA weights:          0.2 GB
  Gradients (LoRA only): 0.2 GB
  Optimizer (LoRA only): 0.4 GB
  Activations:          20 GB
  Total:              ~161 GB  ← 2× A100 80GB ($50/hr)

QLoRA (4-bit base):
  Model (4-bit):        35 GB
  LoRA weights (FP16):   0.2 GB
  Gradients (LoRA):      0.2 GB
  Optimizer (paged):     0.4 GB
  Activations:          10 GB
  Total:               ~46 GB  ← 1× A100 80GB ($25/hr)
                   or   ~24 GB  with gradient checkpointing
                               ← 1× RTX 4090 ($2/hr!)
```

---

## QLoRA — Key Innovations

![qlora_key_innovations](svg/courses/ai/generative-ai-applications/15_peft_lora_qlora/qlora_key_innovations.svg)

---

## Prompt Tuning

Instead of modifying model weights, learn **virtual tokens** prepended to the input:

---

## Prompt Tuning

![prompt_tuning](svg/courses/ai/generative-ai-applications/15_peft_lora_qlora/prompt_tuning.svg)

---

## Implementing Prompt Tuning

```python
from peft import PromptTuningConfig, get_peft_model, TaskType
from peft import PromptTuningInit

# Configure prompt tuning
prompt_config = PromptTuningConfig(
    task_type=TaskType.CAUSAL_LM,
    num_virtual_tokens=20,          # Number of learned tokens
    prompt_tuning_init=PromptTuningInit.TEXT,  # Init from text
    prompt_tuning_init_text="Classify the sentiment of this text: ",
    tokenizer_name_or_path="meta-llama/Llama-3.1-8B-Instruct",
)

model = get_peft_model(base_model, prompt_config)
model.print_trainable_parameters()
# trainable params: 81,920 || all params: 8,030,343,168
# trainable%: 0.001%  ← Extremely parameter efficient!

# Trainable parameter count:
# 20 virtual tokens × 4096 hidden dim = 81,920 parameters
# That's ~0.3 MB to store!
```

---

## Prompt Tuning vs. LoRA vs. Full FT

![prompt_tuning_vs_lora_vs_full_ft](svg/courses/ai/generative-ai-applications/15_peft_lora_qlora/prompt_tuning_vs_lora_vs_full_ft.svg)

---

## Prefix Tuning

Similar to prompt tuning but adds learned vectors to every layer:

```misc
Prompt Tuning: learned tokens at input layer only
  Layer 1: [v1 v2 ... vN] [input tokens]
  Layer 2: [         normal hidden states          ]
  Layer 3: [         normal hidden states          ]

Prefix Tuning: learned vectors at every layer
  Layer 1: [p1₁ p1₂ ... p1_N] [input tokens]
  Layer 2: [p2₁ p2₂ ... p2_N] [hidden states]
  Layer 3: [p3₁ p3₂ ... p3_N] [hidden states]

More parameters than prompt tuning, better quality.
```

```python
from peft import PrefixTuningConfig

prefix_config = PrefixTuningConfig(
    task_type=TaskType.CAUSAL_LM,
    num_virtual_tokens=20,
    # Trainable params = 20 × num_layers × 2 × d_model
    # For 32-layer model: 20 × 32 × 2 × 4096 = 5.2M params
)
```

---

## IA³ — Infused Adapter by Inhibiting and Amplifying

Learned scaling vectors for keys, values, and FFN outputs:

```misc
Standard attention:
  Attention = softmax(QK^T / √d) × V

IA³:
  Attention = softmax(Q × (l_k ⊙ K)^T / √d) × (l_v ⊙ V)
  FFN output = l_ff ⊙ FFN(x)

  l_k, l_v, l_ff are learned scaling vectors
  ⊙ = element-wise multiplication
```

```python
from peft import IA3Config

ia3_config = IA3Config(
    task_type=TaskType.CAUSAL_LM,
    target_modules=["k_proj", "v_proj", "down_proj"],
    feedforward_modules=["down_proj"],
)
model = get_peft_model(base_model, ia3_config)
# Even fewer parameters than LoRA
# But works best for classification, less for generation
```

---

## Training with TRL (Transformer Reinforcement Learning)

```python
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset
from peft import LoraConfig

# Load dataset
dataset = load_dataset("timdettmers/openassistant-guanaco")

# LoRA configuration
lora_config = LoraConfig(
    r=16, lora_alpha=32,
    target_modules="all-linear",
    lora_dropout=0.05,
)

# SFT training with LoRA
training_config = SFTConfig(
    output_dir="./sft-lora",
    num_train_epochs=1,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    max_seq_length=2048,
    fp16=True,
    logging_steps=10,
)

trainer = SFTTrainer(
    model=model_name,
    args=training_config,
    train_dataset=dataset["train"],
    peft_config=lora_config,
)

trainer.train()
```

---

## DPO Training with TRL and LoRA

```python
from trl import DPOTrainer, DPOConfig

# DPO dataset format
# Each example has: prompt, chosen (preferred), rejected
dpo_dataset = load_dataset("my_preference_data")
# {"prompt": "...", "chosen": "good response", "rejected": "bad response"}

dpo_config = DPOConfig(
    output_dir="./dpo-lora",
    num_train_epochs=1,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    learning_rate=5e-5,
    beta=0.1,              # KL penalty strength
    fp16=True,
    logging_steps=10,
)

trainer = DPOTrainer(
    model=model,
    ref_model=None,        # Use implicit reference (LoRA base)
    args=dpo_config,
    train_dataset=dpo_dataset["train"],
    peft_config=lora_config,
    tokenizer=tokenizer,
)

trainer.train()
# Result: Model aligned to your preferences via DPO + LoRA
# All on a single GPU!
```

---

## Practical Tips for PEFT Training

![practical_tips_for_peft_training](svg/courses/ai/generative-ai-applications/15_peft_lora_qlora/practical_tips_for_peft_training.svg)

---

## Exercise: Fine-Tune with QLoRA

```python
"""
Exercise: Fine-tune a model with QLoRA on a custom dataset.

1. Choose a base model:
   - Mistral 7B or LLaMA 3.1 8B

2. Create a small training dataset (50+ examples):
   - Choose a task: sentiment, classification, or Q&A
   - Format as instruction-response pairs
   - Save as JSONL

3. Apply QLoRA:
   - 4-bit quantization with NF4
   - LoRA rank 16, alpha 32
   - Target all linear layers

4. Train for 3 epochs

5. Evaluate:
   - Compare base model vs. fine-tuned on 10 test examples
   - Measure accuracy improvement
   - Report training time and memory usage

6. Save and reload the adapter

Bonus:
- Try different ranks (4, 8, 16, 32) and compare
- Merge the adapter and test inference speed
"""
```

---

## Key Takeaways — PEFT, LoRA, QLoRA

1. **PEFT** enables fine-tuning large models on consumer hardware
1. **LoRA** adds low-rank adapter matrices, training <1% of parameters
1. **QLoRA** combines 4-bit quantization with LoRA for 6-10x memory savings
1. **70B models** can be fine-tuned on a single 24GB GPU with QLoRA
1. **Prompt Tuning** is the most parameter-efficient but limited in quality
1. **LoRA adapters** are tiny (~80MB) and swappable at runtime
1. **TRL** library simplifies SFT and DPO training with PEFT
1. Start with **r=16, all-linear, lr=2e-4** as a default configuration

---

## DoRA — Weight-Decomposed Low-Rank Adaptation

An improvement over LoRA that decomposes weight into magnitude and direction:

```misc
LoRA:
  W' = W + BA    (add low-rank update)

DoRA:
  W' = m · (W + BA) / ||W + BA||
  Where m = learned magnitude scalar

Intuition: Separate WHAT to change (direction via LoRA)
           from HOW MUCH to change (magnitude via m)

Benefits:
  - Matches full fine-tuning quality more closely
  - Same memory cost as LoRA
  - Only adds one scalar per output dimension
  - 1-3% improvement over LoRA on most tasks
```

```python
from peft import LoraConfig

# Enable DoRA in PEFT
config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules="all-linear",
    use_dora=True,  # Enable DoRA
)
```

---

## LoRA+ — Optimized Learning Rates

```misc
Standard LoRA uses same learning rate for A and B matrices:
  lr_A = lr_B = 2e-4

LoRA+ uses DIFFERENT learning rates:
  lr_B = 2e-4
  lr_A = lr_B × ratio  (ratio = 8-16 typically)

Why? The A matrix (down-projection) benefits from
faster learning, while B matrix (up-projection)
needs slower, more careful updates.

Result: 1-2% improvement on benchmarks, no extra cost
```

```python
# LoRA+ implementation with custom optimizer groups
def get_lora_plus_optimizer(model, lr=2e-4, ratio=16):
    params_A = []
    params_B = []
    params_other = []

    for name, param in model.named_parameters():
        if "lora_A" in name:
            params_A.append(param)
        elif "lora_B" in name:
            params_B.append(param)
        elif param.requires_grad:
            params_other.append(param)

    return torch.optim.AdamW([
        {"params": params_A, "lr": lr * ratio},
        {"params": params_B, "lr": lr},
        {"params": params_other, "lr": lr},
    ])
```

---

## Practical: Full QLoRA Training Script

```python
"""Complete QLoRA fine-tuning script."""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset

# 1. Configuration
MODEL = "meta-llama/Llama-3.1-8B-Instruct"
DATASET = "timdettmers/openassistant-guanaco"
OUTPUT = "./qlora-output"

# 2. Quantization
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True, bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

# 3. Load model
model = AutoModelForCausalLM.from_pretrained(
    MODEL, quantization_config=bnb_config, device_map="auto"
)
model = prepare_model_for_kbit_training(model)
tokenizer = AutoTokenizer.from_pretrained(MODEL)
tokenizer.pad_token = tokenizer.eos_token

# 4. LoRA
lora_config = LoraConfig(
    r=16, lora_alpha=32, target_modules="all-linear",
    lora_dropout=0.05, bias="none",
)

# 5. Training
dataset = load_dataset(DATASET, split="train")
training_config = SFTConfig(
    output_dir=OUTPUT, num_train_epochs=1,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    learning_rate=2e-4, max_seq_length=2048,
    fp16=True, logging_steps=10,
    save_strategy="steps", save_steps=200,
)

trainer = SFTTrainer(
    model=model, args=training_config,
    train_dataset=dataset, peft_config=lora_config,
)
trainer.train()
trainer.save_model()
```

---

## Day 4 Summary and Q&A

**What we covered today:**
- Open source model landscape and choosing the right model
- Running models locally with `Transformers`, `vLLM`, and `Ollama`
- `HuggingFace` Hub, Datasets, and Spaces
- `LangChain` integration with local models
- `LoRA`: low-rank adaptation for efficient fine-tuning
- `QLoRA`: 4-bit quantization + LoRA for single-GPU training
- Prompt Tuning, Prefix Tuning, and `IA3`
- Advanced techniques: `DoRA`, `LoRA+`, multiple adapters

**Key insight:** With `QLoRA`, you can fine-tune a 70B parameter model on a single consumer GPU, achieving near-full-fine-tuning quality at a fraction of the cost.

**Tomorrow:** Image generation, personalization, quality measurement, bias, and AI safety.

---

## Merging LoRA Adapters

```python
# Combine multiple LoRA adapters into one

from peft import PeftModel

# Load base model
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct",
    torch_dtype=torch.float16,
    device_map="auto",
)

# Load first adapter
model = PeftModel.from_pretrained(base_model, "adapter_1/")

# Merge first adapter into base weights
model = model.merge_and_unload()

# Load second adapter on top of merged model
model = PeftModel.from_pretrained(model, "adapter_2/")

# Merge second adapter
model = model.merge_and_unload()

# Save the fully merged model
model.save_pretrained("merged_model/")

# Alternative: Weighted merge
# adapter_weights = {"adapter_1": 0.7, "adapter_2": 0.3}
# Useful when one adapter is more important than the other
```

---

## Evaluating PEFT Models — A/B Comparison

```python
def compare_peft_models(base_model_name, adapter_path, test_data):
    """Compare base model vs PEFT-adapted model."""
    # Load base model
    base = AutoModelForCausalLM.from_pretrained(
        base_model_name, torch_dtype=torch.float16, device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(base_model_name)

    # Load adapted model
    adapted = PeftModel.from_pretrained(base, adapter_path)

    results = {"base": [], "adapted": []}

    for example in test_data:
        prompt = example["prompt"]
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to("cuda")

        # Generate from base
        with torch.no_grad():
            base_out = base.generate(input_ids, max_new_tokens=200)
        results["base"].append(tokenizer.decode(base_out[0], skip_special_tokens=True))

        # Generate from adapted
        with torch.no_grad():
            adapted_out = adapted.generate(input_ids, max_new_tokens=200)
        results["adapted"].append(tokenizer.decode(adapted_out[0], skip_special_tokens=True))

    # Compare using your evaluation metrics
    print("Base model scores:", evaluate(results["base"], test_data))
    print("Adapted model scores:", evaluate(results["adapted"], test_data))
```

---

## PEFT for Sequence Classification

```python
from transformers import AutoModelForSequenceClassification
from peft import get_peft_model, LoraConfig, TaskType

# Load a model for classification
model = AutoModelForSequenceClassification.from_pretrained(
    "meta-llama/Llama-3.1-8B",
    num_labels=5,  # 5-class classification
    torch_dtype=torch.float16,
    device_map="auto",
)

# Apply LoRA for classification
config = LoraConfig(
    task_type=TaskType.SEQ_CLS,  # Sequence classification
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
    modules_to_save=["classifier"],  # Also train classification head
)

model = get_peft_model(model, config)
model.print_trainable_parameters()
# trainable: classifier head + LoRA adapters
# ~0.5% of total parameters

# Train with standard Trainer
# Much faster than fine-tuning the full model
# And often achieves comparable accuracy
```

---

## Troubleshooting PEFT Training

```misc
COMMON ISSUES AND FIXES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Issue: Training loss doesn't decrease
Fix:   • Increase learning rate (try 5e-4)
       • Increase LoRA rank (try r=32)
       • Check data formatting (prompt masking correct?)
       • Ensure data quality (no label noise)

Issue: CUDA out of memory
Fix:   • Enable gradient checkpointing
       • Reduce batch size (increase gradient accumulation)
       • Use QLoRA instead of LoRA
       • Reduce max sequence length

Issue: Model outputs are incoherent
Fix:   • Reduce learning rate (try 1e-5)
       • Train for fewer epochs
       • Check for data contamination
       • Verify tokenizer matches base model

Issue: Model forgets base capabilities
Fix:   • Reduce epochs (1-2 instead of 3+)
       • Lower learning rate
       • Mix in general-purpose examples
       • Use smaller LoRA rank
```
