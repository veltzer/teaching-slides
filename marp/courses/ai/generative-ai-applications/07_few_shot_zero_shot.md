# Few-Shot and Zero-Shot Learning

---

## What is In-Context Learning?

`LLM`s can learn new tasks from examples provided in the prompt — no retraining needed:

---

## What is In-Context Learning?

![what_is_in_context_learning](svg/courses/ai/generative-ai-applications/07_few_shot_zero_shot/what_is_in_context_learning.svg)

---

## Zero-Shot vs One-Shot vs Few-Shot

![in_context_learning](svg/courses/ai/generative-ai-applications/07_few_shot_zero_shot/in_context_learning.svg)

---

## Zero-Shot Learning

No examples — the model relies entirely on its pre-training knowledge:

```python
# Zero-shot classification
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content":
            "Classify the sentiment of the following text as "
            "'positive', 'negative', or 'neutral'. "
            "Respond with only the classification."},
        {"role": "user", "content":
            "The new update completely broke my workflow. "
            "I've been struggling with it all day."},
    ],
    temperature=0,
)
print(response.choices[0].message.content)
# "negative"
```

**Works well for:** Common tasks the model has seen during training (sentiment, translation, summarization).

---

## Zero-Shot Limitations

When zero-shot fails:

```python
# Custom classification — zero-shot struggles
prompt = """Classify this support ticket into one of:
L1_BASIC, L2_TECHNICAL, L3_ENGINEERING, ESCALATE_MANAGEMENT

Ticket: "The dashboard shows last month's data but the CSV
export has this month's data. The numbers don't match."
"""

# Zero-shot might give inconsistent results because:
# 1. Model doesn't know your company's classification rules
# 2. The categories are domain-specific
# 3. Edge cases need examples to disambiguate

# Different runs might return:
# "L2_TECHNICAL" or "L3_ENGINEERING" — model is uncertain
```

**Solution:** Provide examples (few-shot) to demonstrate the expected behavior.

---

## One-Shot Learning

A single example can dramatically improve performance:

```python
messages = [
    {"role": "system", "content":
        "Convert natural language dates to ISO format."},
    # One example
    {"role": "user", "content": "next Tuesday"},
    {"role": "assistant", "content": "2026-03-17"},
    # Actual query
    {"role": "user", "content": "the day after tomorrow"},
]

response = client.chat.completions.create(
    model="gpt-4o", messages=messages, temperature=0
)
# "2026-03-12"

# The single example teaches:
# 1. The expected output format (YYYY-MM-DD)
# 2. That relative dates should be resolved
# 3. The level of detail expected (no explanation)
```

---

## Few-Shot Learning — The Core Pattern

```python
def few_shot_classify(text, examples, categories):
    """Generic few-shot classification."""
    messages = [
        {"role": "system", "content":
            f"Classify text into: {', '.join(categories)}. "
            f"Respond with only the category name."}
    ]

    # Add examples as conversation turns
    for example_text, example_label in examples:
        messages.append({"role": "user", "content": example_text})
        messages.append({"role": "assistant", "content": example_label})

    # Add the actual query
    messages.append({"role": "user", "content": text})

    response = client.chat.completions.create(
        model="gpt-4o", messages=messages, temperature=0
    )
    return response.choices[0].message.content

# Usage
examples = [
    ("Server is down, can't access anything", "L2_TECHNICAL"),
    ("How do I change my password?", "L1_BASIC"),
    ("Memory leak in production service", "L3_ENGINEERING"),
    ("CEO needs incident report ASAP", "ESCALATE_MANAGEMENT"),
]
result = few_shot_classify("Dashboard metrics are stale", examples,
    ["L1_BASIC", "L2_TECHNICAL", "L3_ENGINEERING", "ESCALATE_MANAGEMENT"])
```

---

## Choosing Examples — Quality Matters

![choosing_examples_quality_matters](svg/courses/ai/generative-ai-applications/07_few_shot_zero_shot/choosing_examples_quality_matters.svg)

---
## Choosing Examples — Quality Matters

```python
# Bad: All examples are positive
bad_examples = [
    ("Love it!", "positive"),
    ("Amazing product!", "positive"),
    ("Best purchase ever!", "positive"),
    # Model will be biased toward "positive"
]
# Good: Balanced, diverse, edge cases included
good_examples = [
    ("Love it!", "positive"),
    ("Terrible, returning it", "negative"),
    ("It works as expected", "neutral"),
    ("Great features but poor battery", "mixed"),
]
```

---

## Dynamic Few-Shot Selection

Choose examples similar to the input for better results:

```python
from openai import OpenAI
import numpy as np

client = OpenAI()

def get_embedding(text):
    resp = client.embeddings.create(
        input=text, model="text-embedding-3-small"
    )
    return np.array(resp.data[0].embedding)

# Pre-compute embeddings for example bank
example_bank = [
    {"text": "Server crash at 3am", "label": "critical", "emb": None},
    {"text": "Button color is wrong", "label": "low", "emb": None},
    # ... hundreds of labeled examples
]

for ex in example_bank:
    ex["emb"] = get_embedding(ex["text"])

def select_examples(query, k=5):
    query_emb = get_embedding(query)
    similarities = [
        (np.dot(query_emb, ex["emb"]), ex)
        for ex in example_bank
    ]
    similarities.sort(key=lambda x: -x[0])
    return [ex for _, ex in similarities[:k]]
```

---

## Few-Shot for Code Generation

```python
messages = [
    {"role": "system", "content":
        "Generate Python functions based on descriptions. "
        "Include type hints and docstrings."},

    # Example 1
    {"role": "user", "content":
        "A function that checks if a string is a palindrome"},
    {"role": "assistant", "content": '''def is_palindrome(s: str) -> bool:
    """Check if a string is a palindrome, ignoring case and spaces."""
    cleaned = s.lower().replace(" ", "")
    return cleaned == cleaned[::-1]'''},

    # Example 2
    {"role": "user", "content":
        "A function that flattens a nested list"},
    {"role": "assistant", "content": '''def flatten(lst: list) -> list:
    """Recursively flatten a nested list."""
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result'''},

    # Actual request
    {"role": "user", "content":
        "A function that groups a list of dicts by a key"},
]
```

---

## Few-Shot for Data Extraction

```python
# Extracting structured data from unstructured text
messages = [
    {"role": "system", "content": "Extract product info as JSON."},

    {"role": "user", "content":
        "The new MacBook Pro 16-inch starts at $2,499 "
        "and features the M3 Max chip with 36GB RAM."},
    {"role": "assistant", "content": '''{
  "product": "MacBook Pro 16-inch",
  "price": 2499,
  "currency": "USD",
  "specs": {"chip": "M3 Max", "ram_gb": 36}
}'''},

    {"role": "user", "content":
        "Samsung Galaxy S24 Ultra with 12GB RAM and "
        "200MP camera, priced at €1,449 in Europe."},
    {"role": "assistant", "content": '''{
  "product": "Samsung Galaxy S24 Ultra",
  "price": 1449,
  "currency": "EUR",
  "specs": {"ram_gb": 12, "camera_mp": 200}
}'''},

    {"role": "user", "content":
        "Sony WH-1000XM5 headphones available for $348, "
        "featuring 30-hour battery life and ANC."},
]
```

---

## How Many Examples Do You Need?

![how_many_examples_do_you_need](svg/courses/ai/generative-ai-applications/07_few_shot_zero_shot/how_many_examples_do_you_need.svg)

---

## Zero-Shot vs. Few-Shot — Performance Comparison

```python
"""Benchmark: Compare zero-shot vs few-shot on same task."""
import time

test_cases = [
    ("The battery lasts forever!", "positive"),
    ("Worst purchase I've made", "negative"),
    ("It does what it says", "neutral"),
    ("Great camera but awful battery", "mixed"),
    ("Meh, I've seen better", "negative"),
]

def evaluate(method_name, classify_fn):
    correct = 0
    for text, expected in test_cases:
        predicted = classify_fn(text)
        match = predicted.lower().strip() == expected
        correct += match
        status = "✓" if match else "✗"
        print(f"  {status} '{text[:30]}...' → {predicted} (expected: {expected})")
    accuracy = correct / len(test_cases)
    print(f"  {method_name} Accuracy: {accuracy:.0%}\n")

# Typical results:
# Zero-shot: 60-70% on domain-specific tasks
# Few-shot (5 examples): 85-95% on same tasks
```

---

## Many-Shot Learning (Using Long Context)

With 128K+ context windows, we can include many more examples:

```python
def many_shot_classify(text, example_bank, k=50):
    """Use many examples for complex classification."""

    # Build a large example section
    example_text = "Here are labeled examples:\n\n"
    for i, (ex_text, ex_label) in enumerate(example_bank[:k]):
        example_text += f"Text: {ex_text}\nLabel: {ex_label}\n\n"

    messages = [
        {"role": "system", "content":
            "You are a text classifier. Based on the examples "
            "provided, classify the new text. Respond with only "
            "the label."},
        {"role": "user", "content":
            f"{example_text}\n---\n\n"
            f"Now classify this text:\n{text}"},
    ]

    response = client.chat.completions.create(
        model="gpt-4o", messages=messages, temperature=0
    )
    return response.choices[0].message.content

# 50 examples can approach fine-tuned model performance
# for well-defined classification tasks
```

---

## Few-Shot for Different Task Types

| Task | Zero-shot | Few-shot Gains | Notes |
|------|-----------|---------------|-------|
| Sentiment | Good | Moderate | Well-represented in training |
| Translation | Good | Small | Strong pre-training on this |
| Summarization | Good | Moderate | Format examples help |
| Custom classification | Poor | Large | Domain-specific labels need examples |
| Data extraction | Moderate | Large | Format specification helps a lot |
| Code generation | Good | Moderate | Style/convention examples help |
| Creative writing | Good | Large | Tone/style examples are critical |

---

## Practical Pattern: Few-Shot Pipeline

```python
class FewShotPipeline:
    def __init__(self, task_description, examples, model="gpt-4o"):
        self.model = model
        self.system_prompt = task_description
        self.examples = examples

    def run(self, inputs, batch_size=5):
        results = []
        for i in range(0, len(inputs), batch_size):
            batch = inputs[i:i+batch_size]
            for text in batch:
                result = self._classify_one(text)
                results.append(result)
        return results

    def _classify_one(self, text):
        messages = [{"role": "system", "content": self.system_prompt}]
        for ex_input, ex_output in self.examples:
            messages.append({"role": "user", "content": ex_input})
            messages.append({"role": "assistant", "content": ex_output})
        messages.append({"role": "user", "content": text})

        response = client.chat.completions.create(
            model=self.model, messages=messages, temperature=0
        )
        return response.choices[0].message.content
```

---

## Exercise: Few-Shot Learning Challenge

```python
"""
Exercise: Build a few-shot classifier for technical support tickets.

Categories: bug_report, feature_request, question, praise, complaint

1. Create 3 examples per category (15 total)
2. Test with 10 unlabeled tickets (provided below)
3. Compare zero-shot vs 3-shot vs 15-shot accuracy
4. Try dynamic example selection and measure improvement

Test tickets:
- "The app crashes when I click the settings icon"
- "Can you add dark mode please?"
- "How do I export my data as CSV?"
- "Your support team is amazing, thanks!"
- "I've been waiting 3 weeks for a response"
- "Login page shows a 500 error"
- "Would be great to have keyboard shortcuts"
- "What formats does the export support?"
- "Best tool I've ever used for project management"
- "This is unacceptable, I want a refund"
"""
```

---

## Key Takeaways — Few-Shot and Zero-Shot Learning

1. **Zero-shot** works for common, well-defined tasks
1. **Few-shot** dramatically improves performance on custom/domain tasks
1. **Example quality** matters more than quantity
1. **Dynamic selection** of examples based on similarity boosts results
1. **5-8 examples** is typically the sweet spot
1. **Balance** examples across all categories
1. **Many-shot** (50+) with long context windows approaches fine-tuning quality
1. When few-shot isn't enough, consider **fine-tuning** (covered later today)

---

## Few-Shot for Text Transformation

```python
# Transform text style using few-shot examples

messages = [
    {"role": "system", "content":
        "Rewrite technical text for a non-technical audience."},

    {"role": "user", "content":
        "The API endpoint returns a 429 status code when "
        "the rate limit is exceeded."},
    {"role": "assistant", "content":
        "When you send too many requests too quickly, "
        "the service will temporarily block new requests. "
        "Just wait a moment and try again."},

    {"role": "user", "content":
        "The database uses B-tree indices for O(log n) "
        "lookup performance on primary keys."},
    {"role": "assistant", "content":
        "The database organizes data in a way that makes "
        "finding records extremely fast, even when there "
        "are millions of entries."},

    # Now transform new text
    {"role": "user", "content":
        "The container orchestration layer manages pod "
        "scheduling, horizontal autoscaling, and rolling "
        "deployments across the cluster."},
]
```

---

## Few-Shot for Structured Data Conversion

```python
# Convert between data formats using few-shot
messages = [
    {"role": "system", "content":
        "Convert natural language descriptions to SQL CREATE TABLE statements."},

    {"role": "user", "content":
        "A users table with ID, email, name, and when they signed up"},
    {"role": "assistant", "content":
        "CREATE TABLE users (\n"
        "    id SERIAL PRIMARY KEY,\n"
        "    email VARCHAR(255) UNIQUE NOT NULL,\n"
        "    name VARCHAR(100) NOT NULL,\n"
        "    signed_up_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n"
        ");"},

    {"role": "user", "content":
        "An orders table linked to users, with product name, "
        "quantity, price, and order date"},
    {"role": "assistant", "content":
        "CREATE TABLE orders (\n"
        "    id SERIAL PRIMARY KEY,\n"
        "    user_id INTEGER REFERENCES users(id),\n"
        "    product_name VARCHAR(255) NOT NULL,\n"
        "    quantity INTEGER NOT NULL DEFAULT 1,\n"
        "    price DECIMAL(10,2) NOT NULL,\n"
        "    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n"
        ");"},

    {"role": "user", "content":
        "A reviews table with user, product, rating 1-5, "
        "and review text, linked to both users and orders"},
]
```

---

## Few-Shot Calibration Techniques

```python
def calibrate_few_shot(examples, test_input, model="gpt-4o"):
    """Calibrate few-shot predictions by adjusting for
    content-free bias."""

    # Step 1: Get prediction with actual input
    pred = few_shot_classify(test_input, examples)

    # Step 2: Get prediction with empty/neutral input
    # This reveals the model's prior bias
    null_input = "N/A"
    null_pred = few_shot_classify(null_input, examples)

    # If the model predicts "positive" even for null input,
    # there's a bias toward "positive" in the examples

    # Step 3: Adjust probabilities
    # Use logit-space calibration:
    # P_calibrated(y|x) ∝ P(y|x) / P(y|null)

    return {
        "raw_prediction": pred,
        "null_prediction": null_pred,
        "bias_detected": pred == null_pred,
    }

# This technique from Zhao et al. (2021) can improve
# few-shot accuracy by 10-30% on some tasks
```

---

## In-Context Learning — Why Does It Work?

```misc
Several theories for why few-shot learning works:

1. TASK IDENTIFICATION
   Examples help the model identify which "task"
   from pre-training to apply.
   "Oh, these look like sentiment labels → do sentiment"

2. INPUT-OUTPUT MAPPING
   The model learns the mapping function from
   the examples themselves.
   "Input format → output format, apply to new input"

3. IMPLICIT FINE-TUNING
   Forward pass through examples acts like a
   single gradient step.
   (Theoretical connection to gradient descent)

4. BAYESIAN INFERENCE
   The model performs approximate Bayesian inference
   over possible tasks given the examples.

Current consensus: Combination of all four,
depending on the task and model size.
```
