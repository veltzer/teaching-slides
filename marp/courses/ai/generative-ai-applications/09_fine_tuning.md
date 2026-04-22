---
tags:
  - data-and-ai:ai
  - data-and-ai:generative-ai
  - languages:python
  - data-and-ai:prompt-engineering
  - concepts:ethics
level: intermediate
category: ai
audience:
  - audiences:data-scientists

---
# Fine-Tuning

---

## What is Fine-Tuning?: Overview

Adapting a pre-trained model to your specific task by continuing training on your own data:

---
## What is Fine-Tuning?

![what_is_fine_tuning](svg/courses/ai/generative-ai-applications/09_fine_tuning/what_is_fine_tuning.svg)

---
## What is Fine-Tuning?: Details

**When to fine-tune vs. when to use prompting:**
- Prompting: Quick iteration, small tasks, flexible
- Fine-tuning: Consistent style, large volume, cost optimization

---

## Fine-Tuning vs. Prompt Engineering — Decision Tree

![fine_tuning_vs_prompt_engineering_decision_tree](svg/courses/ai/generative-ai-applications/09_fine_tuning/fine_tuning_vs_prompt_engineering_decision_tree.svg)

---

## Benefits of Fine-Tuning

| Benefit | Explanation |
|---------|-------------|
| **Consistency** | Same style every time (no prompt variance) |
| **Cost reduction** | Shorter prompts needed → fewer tokens |
| **Latency** | Less input processing → faster responses |
| **Custom behavior** | Behaviors hard to describe in prompts |
| **Smaller model** | Fine-tuned mini can match base large model |
| **Privacy** | Train on your data without sending it every call |

```python
# Before fine-tuning: Long prompt needed
messages = [
    {"role": "system", "content": "...500 tokens of instructions..."},
    {"role": "user", "content": "classify this email..."},
]
# Cost: 500 + input tokens per request

# After fine-tuning: Minimal prompt needed
messages = [
    {"role": "user", "content": "classify this email..."},
]
# Cost: Just input tokens per request (saved 500 tokens!)
```

---

## Preparing Fine-Tuning Data

```python
# Fine-tuning data format (JSONL)
# Each line is a complete conversation

training_data = [
    {
        "messages": [
            {"role": "system", "content": "You classify support tickets."},
            {"role": "user", "content": "My app crashes on startup"},
            {"role": "assistant", "content": "bug_report"}
        ]
    },
    {
        "messages": [
            {"role": "system", "content": "You classify support tickets."},
            {"role": "user", "content": "Please add dark mode"},
            {"role": "assistant", "content": "feature_request"}
        ]
    },
    # ... 50-10000 more examples
]

# Save as JSONL
import json
with open("training_data.jsonl", "w") as f:
    for example in training_data:
        f.write(json.dumps(example) + "\n")
```

---

## Data Quality Checklist

![data_quality_checklist](svg/courses/ai/generative-ai-applications/09_fine_tuning/data_quality_checklist.svg)

---

## Launching a Fine-Tuning Job with `OpenAI`

```python
from openai import OpenAI
client = OpenAI()

# Step 1: Upload training file
training_file = client.files.create(
    file=open("training_data.jsonl", "rb"),
    purpose="fine-tune"
)
print(f"File ID: {training_file.id}")

# Step 2: Upload validation file (optional but recommended)
validation_file = client.files.create(
    file=open("validation_data.jsonl", "rb"),
    purpose="fine-tune"
)

# Step 3: Create fine-tuning job
job = client.fine_tuning.jobs.create(
    training_file=training_file.id,
    validation_file=validation_file.id,
    model="gpt-4o-mini-2024-07-18",
    hyperparameters={
        "n_epochs": 3,
        "batch_size": "auto",
        "learning_rate_multiplier": "auto",
    },
    suffix="ticket-classifier",  # Custom model name suffix
)
print(f"Job ID: {job.id}")
```

---

## Monitoring Fine-Tuning Progress

```python
import time

# Check job status
while True:
    job = client.fine_tuning.jobs.retrieve(job.id)
    print(f"Status: {job.status}")

    if job.status == "succeeded":
        print(f"Fine-tuned model: {job.fine_tuned_model}")
        break
    elif job.status == "failed":
        print(f"Error: {job.error}")
        break

    time.sleep(60)

# List events during training
events = client.fine_tuning.jobs.list_events(
    fine_tuning_job_id=job.id, limit=20
)
for event in events.data:
    print(f"{event.created_at}: {event.message}")

# Typical output:
# "Step 100/300: training loss=0.45"
# "Step 200/300: training loss=0.23"
# "Step 300/300: training loss=0.15"
# "Validating..."
# "Validation loss=0.18"
```

---

## Using Your Fine-Tuned Model

```python
# Use exactly like any other model — just change the model name
response = client.chat.completions.create(
    model="ft:gpt-4o-mini-2024-07-18:my-org:ticket-classifier:abc123",
    messages=[
        {"role": "system", "content": "You classify support tickets."},
        {"role": "user", "content":
            "The search feature returns wrong results "
            "when I use special characters"},
    ],
    temperature=0,
    max_tokens=20,
)

print(response.choices[0].message.content)
# "bug_report"

# Fine-tuned model benefits:
# 1. Shorter system prompt needed
# 2. More consistent outputs
# 3. Faster (less to process)
# 4. Cheaper per request (fewer input tokens)
```

---

## Hyperparameter Tuning

```python
# Key hyperparameters for fine-tuning

hyperparameters = {
    "n_epochs": 3,
    # Number of passes through training data
    # Too few: underfitting (model hasn't learned)
    # Too many: overfitting (memorized training data)
    # Default: auto (OpenAI calculates based on dataset size)

    "batch_size": 1,
    # Examples per gradient update
    # Larger = more stable but slower learning
    # Default: auto

    "learning_rate_multiplier": 1.0,
    # Multiplier on default learning rate
    # Higher = faster learning but risk of instability
    # Lower = slower but more stable
    # Default: auto
}

# Guidelines:
# 50-100 examples  → 3-5 epochs
# 100-500 examples → 2-3 epochs
# 500+ examples    → 1-2 epochs
```

---

## Evaluating Fine-Tuned Models

```python
import json
from sklearn.metrics import classification_report

def evaluate_model(model_name, test_data):
    """Evaluate fine-tuned model on test set."""
    predictions = []
    ground_truth = []

    for example in test_data:
        user_msg = example["messages"][1]["content"]
        expected = example["messages"][2]["content"]

        response = client.chat.completions.create(
            model=model_name,
            messages=[
                example["messages"][0],  # system
                example["messages"][1],  # user
            ],
            temperature=0,
            max_tokens=20,
        )
        predicted = response.choices[0].message.content.strip()

        predictions.append(predicted)
        ground_truth.append(expected)

    print(classification_report(ground_truth, predictions))

# Compare base vs. fine-tuned
evaluate_model("gpt-4o-mini", test_data)           # Base
evaluate_model("ft:gpt-4o-mini:...:abc123", test_data)  # Fine-tuned
```

---

## Fine-Tuning for Different Tasks

![fine_tuning_for_different_tasks](svg/courses/ai/generative-ai-applications/09_fine_tuning/fine_tuning_for_different_tasks.svg)

---

## Fine-Tuning for Style and Tone

```python
# Train the model to write in your company's voice
style_examples = [
    {
        "messages": [
            {"role": "system", "content": "Write customer emails in TechCorp style."},
            {"role": "user", "content": "Customer asked about refund policy"},
            {"role": "assistant", "content":
                "Hi there!\n\n"
                "Thanks for reaching out about our refund policy. "
                "We've got you covered — here's the quick version:\n\n"
                "• Full refund within 30 days, no questions asked\n"
                "• 50% credit after 30 days, up to 90 days\n"
                "• Just reply to this email and we'll start the process\n\n"
                "Anything else I can help with?\n\n"
                "Cheers,\nTechCorp Support"
            }
        ]
    },
    # ... more examples in the same style
]

# The fine-tuned model will adopt:
# - Friendly, casual tone
# - Bullet-point formatting
# - Specific sign-off style
```

---

## Common Fine-Tuning Pitfalls

```misc
1. OVERFITTING
   Symptom: Perfect on training data, poor on new inputs
   Fix: Use validation set, reduce epochs, add more diverse data

2. CATASTROPHIC FORGETTING
   Symptom: Model loses general capabilities
   Fix: Mix general-purpose examples with task-specific ones

3. DISTRIBUTION MISMATCH
   Symptom: Works on test set, fails in production
   Fix: Ensure training data matches production distribution

4. INSUFFICIENT DATA
   Symptom: Model shows no improvement over base
   Fix: Collect more data, or use few-shot instead

5. LABEL NOISE
   Symptom: Inconsistent outputs, low accuracy
   Fix: Audit and clean your training data

6. WRONG BASE MODEL
   Symptom: Fine-tuned model is too slow/expensive
   Fix: Start with the smallest model that can handle the task
```

---

## Cost Analysis: Fine-Tuning Economics

```python
# Fine-tuning cost calculation
training_config = {
    "base_model": "gpt-4o-mini",
    "training_tokens": 500_000,  # ~500 examples × 1000 tokens
    "epochs": 3,
    "training_cost_per_1M": 3.00,  # Fine-tuning pricing
}

training_cost = (
    training_config["training_tokens"]
    * training_config["epochs"]
    * training_config["training_cost_per_1M"]
    / 1_000_000
)
print(f"Training cost: ${training_cost:.2f}")  # $4.50

# Inference cost comparison (per 1K requests)
# Base model with long prompt (500 tokens system prompt):
base_cost = 1000 * 500 * 0.15 / 1_000_000  # $0.075
# Fine-tuned with short prompt (50 tokens):
ft_cost = 1000 * 50 * 0.30 / 1_000_000     # $0.015

# Break-even: training pays off after ~90K requests
breakeven = training_cost / (base_cost - ft_cost)
print(f"Break-even at: {breakeven:.0f} batches of 1K requests")
```

---

## Continued Fine-Tuning (Iterative)

```python
# Fine-tune on top of your already fine-tuned model
job = client.fine_tuning.jobs.create(
    training_file=new_training_file.id,
    model="ft:gpt-4o-mini:my-org:v1:abc123",  # Start from v1
    suffix="ticket-classifier-v2",
)

# Iterative fine-tuning workflow:
#
# V1: Initial 200 examples → Deploy
#      │
#      ▼
# Collect production failures
#      │
#      ▼
# V2: V1 + 100 failure corrections → Deploy
#      │
#      ▼
# Collect more edge cases
#      │
#      ▼
# V3: V2 + edge cases → Deploy
#
# Each iteration improves on specific weaknesses
```

---

## Exercise: Fine-Tuning a Classifier

```python
"""
Exercise: Fine-tune GPT-4o-mini for email classification.

Categories: urgent, normal, spam, automated

Steps:
1. Create 50 training examples (JSONL format)
2. Create 10 validation examples
3. Upload files and start fine-tuning job
4. Monitor training progress
5. Evaluate on test set vs. base model with few-shot
6. Calculate cost savings vs. prompt-based approach

Starter data generation:
"""
import random

templates = {
    "urgent": [
        "URGENT: Server is down, all customers affected",
        "Critical security breach detected at {time}",
        "Production database corrupted, need immediate help",
    ],
    "normal": [
        "Can you help me reset my password?",
        "Question about our subscription plans",
        "How do I export my data?",
    ],
```

---

## Exercise: Classifier Templates (Spam and Automated)

```python
    "spam": [
        "Congratulations! You've won a free iPhone!",
        "Buy cheap medications online now!!!",
        "Make $10000/day working from home",
    ],
    "automated": [
        "Your weekly report is ready for review",
        "Deployment to staging completed successfully",
        "Scheduled maintenance tonight at 2am UTC",
    ],
}
```

---

## Day 2 Summary and Q&A

**What we covered today:**
- `OpenAI` `API` fundamentals: chat completions, streaming, function calling
- Prompt engineering: structure, roles, templates, injection defense
- Few-shot and zero-shot learning: when and how to use examples
- Chain-of-thought reasoning: CoT, self-consistency, Tree of Thoughts
- Fine-tuning: data preparation, training, evaluation, cost analysis

**Key insight:** Start with prompt engineering, move to few-shot, and only fine-tune when you have sufficient data and a clear need for consistency.

**Tomorrow:** We build agents with memory and `LangChain`.

---

## Data Augmentation for Fine-Tuning

```python
def augment_training_data(seed_examples, target_count=500):
    """Use an LLM to generate more training examples."""

    augmented = list(seed_examples)  # Start with originals

    while len(augmented) < target_count:
        # Select a random seed example
        seed = random.choice(seed_examples)

        # Generate a variation
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content":
                    "Generate a new training example similar in "
                    "format and difficulty but with different content. "
                    "Return as JSON: {\"input\": ..., \"output\": ...}"},
                {"role": "user", "content":
                    f"Example to base on:\n"
                    f"Input: {seed['input']}\n"
                    f"Output: {seed['output']}"},
            ],
            response_format={"type": "json_object"},
            temperature=1.0,  # High temperature for diversity
        )

        new_example = json.loads(response.choices[0].message.content)

        # Validate before adding
        if validate_example(new_example):
            augmented.append(new_example)

    return augmented
```

---

## Fine-Tuning for Function Calling

```python
# Train a model to reliably call your specific functions

function_calling_examples = [
    {
        "messages": [
            {"role": "system", "content": "You have access to tools."},
            {"role": "user", "content": "What's the weather in NYC?"},
            {"role": "assistant", "content": None,
             "function_call": {
                 "name": "get_weather",
                 "arguments": '{"city": "New York", "units": "fahrenheit"}'
             }},
            {"role": "function", "name": "get_weather",
             "content": '{"temp": 72, "condition": "sunny"}'},
            {"role": "assistant",
             "content": "It's currently 72°F and sunny in New York City."},
        ]
    },
    {
        "messages": [
            {"role": "system", "content": "You have access to tools."},
            {"role": "user", "content": "I don't need any tools, "
                                         "just say hello"},
            {"role": "assistant",
             "content": "Hello! How can I help you today?"},
            # No function call — model learns WHEN to use tools
        ]
    },
]

# Fine-tuned model will:
# 1. Know WHEN to call functions
# 2. Use correct argument formats
# 3. Handle results naturally
```

---

## Fine-Tuning Evaluation Strategy

```python
class FineTuneEvaluator:
    """Comprehensive evaluation for fine-tuned models."""

    def __init__(self, base_model, ft_model, test_data):
        self.base_model = base_model
        self.ft_model = ft_model
        self.test_data = test_data

    def run_comparison(self):
        results = {"base": [], "fine_tuned": []}

        for example in self.test_data:
            # Test both models
            base_resp = self._generate(self.base_model, example)
            ft_resp = self._generate(self.ft_model, example)

            results["base"].append({
                "input": example["input"],
                "expected": example["output"],
                "predicted": base_resp,
                "correct": self._is_correct(base_resp, example["output"]),
            })
            results["fine_tuned"].append({
                "input": example["input"],
                "expected": example["output"],
                "predicted": ft_resp,
                "correct": self._is_correct(ft_resp, example["output"]),
            })

        # Summary
        base_acc = sum(r["correct"] for r in results["base"]) / len(results["base"])
        ft_acc = sum(r["correct"] for r in results["fine_tuned"]) / len(results["fine_tuned"])
        print(f"Base model accuracy:       {base_acc:.1%}")
        print(f"Fine-tuned model accuracy: {ft_acc:.1%}")
        print(f"Improvement:               {ft_acc - base_acc:+.1%}")
```
