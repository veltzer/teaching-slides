# Measuring Quality of Text Generation

---

## Why Measure Quality?

![why_measure_quality](svg/courses/ai/generative-ai-applications/18_measuring_quality/why_measure_quality.svg)

---

## Automatic Metrics — Overview

| Metric | Measures | Best For | Range |
|--------|----------|----------|-------|
| `BLEU` | N-gram overlap with reference | Translation | 0-1 |
| `ROUGE` | Recall of reference n-grams | Summarization | 0-1 |
| `METEOR` | Alignment with synonyms | Translation | 0-1 |
| `BERTScore` | Semantic similarity | Any text | -1 to 1 |
| `Perplexity` | Model confidence | Fluency | 1 to ∞ |
| `MAUVE` | Distribution similarity | Open-ended gen | 0-1 |
| `TruthfulQA` | Factual accuracy | Q&A systems | 0-1 |

---

## BLEU Score — Bilingual Evaluation Understudy

Measures n-gram precision between generated and reference text:

```python
from nltk.translate.bleu_score import sentence_bleu, corpus_bleu

reference = [["the", "cat", "sat", "on", "the", "mat"]]
candidate = ["the", "cat", "is", "on", "the", "mat"]

# Sentence-level BLEU
score = sentence_bleu(reference, candidate)
print(f"BLEU: {score:.4f}")  # ~0.61

# BLEU considers different n-gram sizes:
# Unigram (1):  5/6 matching words = 0.833
# Bigram (2):   3/5 matching pairs = 0.600
# Trigram (3):  1/4 matching triples = 0.250
# 4-gram (4):   0/3 = 0.000

# Combined with brevity penalty
# BLEU = BP × exp(Σ wn × log(pn))
```

**Limitations:** Exact word matching ignores synonyms, paraphrasing.

---

## ROUGE Score — Recall-Oriented Understudy

Measures recall — how much of the reference is captured:

```python
from rouge_score import rouge_scorer

scorer = rouge_scorer.RougeScorer(
    ["rouge1", "rouge2", "rougeL"], use_stemmer=True
)

reference = "The quick brown fox jumps over the lazy dog"
generated = "A fast brown fox leaps over a lazy dog"

scores = scorer.score(reference, generated)
for key, value in scores.items():
    print(f"{key}: P={value.precision:.3f} "
          f"R={value.recall:.3f} F={value.fmeasure:.3f}")

# rouge1: P=0.778 R=0.778 F=0.778  (unigram)
# rouge2: P=0.375 R=0.375 F=0.375  (bigram)
# rougeL: P=0.667 R=0.667 F=0.667  (longest common subsequence)

# ROUGE-1: Word overlap
# ROUGE-2: Bigram overlap
# ROUGE-L: Longest Common Subsequence (captures ordering)
```

---

## BERTScore — Semantic Similarity

Uses `BERT` embeddings for meaning-aware comparison:

```python
from bert_score import score

references = [
    "The weather is beautiful today",
    "Machine learning is a subset of AI"
]
candidates = [
    "Today has gorgeous weather",     # Same meaning, different words
    "ML is part of artificial intelligence"
]

P, R, F1 = score(candidates, references, lang="en",
                  model_type="microsoft/deberta-xlarge-mnli")

for i in range(len(references)):
    print(f"Reference: {references[i]}")
    print(f"Candidate: {candidates[i]}")
    print(f"BERTScore F1: {F1[i]:.4f}\n")

# BERTScore captures semantic similarity!
# "gorgeous weather" ↔ "beautiful today" → high score
# Unlike BLEU/ROUGE which need exact word matches
```

---

## Perplexity — Measuring Fluency

How "surprised" the model is by the text (lower = more fluent):

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "gpt2"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def calculate_perplexity(text):
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs, labels=inputs["input_ids"])
    return torch.exp(outputs.loss).item()

texts = [
    "The cat sat on the mat.",              # Natural
    "Cat mat the on sat the.",              # Unnatural
    "Quantum entanglement enables faster-than-light communication.",
    # Fluent but factually incorrect!
]

for text in texts:
    ppl = calculate_perplexity(text)
    print(f"PPL: {ppl:8.2f} | {text}")

# PPL:   45.23 | The cat sat on the mat.     ← Low = fluent
# PPL: 1247.89 | Cat mat the on sat the.     ← High = not fluent
# PPL:  112.45 | Quantum entanglement...     ← Fluent but wrong!
```

---

## LLM-as-a-Judge — Using LLMs to Evaluate LLMs

```python
def llm_judge(question, response_a, response_b):
    """Use GPT-4 to compare two responses."""
    judge_prompt = f"""Compare these two responses to the question.

Question: {question}

Response A: {response_a}

Response B: {response_b}

Evaluate on:
1. Accuracy (1-5): Are the facts correct?
2. Completeness (1-5): Does it fully answer the question?
3. Clarity (1-5): Is it well-written and clear?
4. Helpfulness (1-5): Is it practically useful?

Respond as JSON:
{{"winner": "A" or "B" or "tie",
  "scores_a": {{"accuracy": N, "completeness": N, "clarity": N, "helpfulness": N}},
  "scores_b": {{"accuracy": N, "completeness": N, "clarity": N, "helpfulness": N}},
  "reasoning": "brief explanation"}}"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": judge_prompt}],
        response_format={"type": "json_object"},
        temperature=0,
    )
    return json.loads(response.choices[0].message.content)
```

---

## LLM-as-Judge — Position Bias and Mitigation

```misc
Problem: LLMs tend to prefer the first response shown.

Mitigation: Run evaluation TWICE with swapped positions.

Round 1: Compare A vs B
  "Response A: ..." first, "Response B: ..." second
  Result: A wins

Round 2: Compare B vs A (swapped!)
  "Response A: ..." = what was B
  "Response B: ..." = what was A
  Result: A (original B) wins

Analysis:
  If same winner both rounds → confident result
  If different winners → flag as "tie" or uncertain
```

```python
def robust_judge(question, resp_a, resp_b):
    # Round 1: A first
    result_1 = llm_judge(question, resp_a, resp_b)
    # Round 2: B first (swap)
    result_2 = llm_judge(question, resp_b, resp_a)
    # result_2 winner needs to be flipped

    if result_1["winner"] == flip(result_2["winner"]):
        return result_1["winner"]  # Consistent
    else:
        return "tie"  # Position bias detected
```

---

## Human Evaluation — The Gold Standard

![human_evaluation_the_gold_standard](svg/courses/ai/generative-ai-applications/18_measuring_quality/human_evaluation_the_gold_standard.svg)

---

## Evaluation Pipeline Architecture

![evaluation_pipeline_architecture](svg/courses/ai/generative-ai-applications/18_measuring_quality/evaluation_pipeline_architecture.svg)

---

## Building an Evaluation Harness

```python
class EvalHarness:
    """Comprehensive evaluation for text generation."""

    def __init__(self, test_data):
        self.test_data = test_data
        self.results = {}

    def evaluate(self, model_fn, model_name):
        """Run all evaluations for a model."""
        predictions = [model_fn(d["input"]) for d in self.test_data]
        references = [d["expected"] for d in self.test_data]

        self.results[model_name] = {
            "bleu": self._calc_bleu(predictions, references),
            "rouge": self._calc_rouge(predictions, references),
            "bertscore": self._calc_bertscore(predictions, references),
            "llm_judge": self._llm_judge(predictions, references),
            "length_stats": self._length_stats(predictions),
        }

    def compare(self):
        """Print comparison table."""
        print(f"{'Model':<20} {'BLEU':>8} {'ROUGE-L':>8} "
              f"{'BERT-F1':>8} {'Judge':>8}")
        for name, scores in self.results.items():
            print(f"{name:<20} {scores['bleu']:>8.4f} "
                  f"{scores['rouge']:>8.4f} "
                  f"{scores['bertscore']:>8.4f} "
                  f"{scores['llm_judge']:>8.4f}")
```

---

## Exercise: Evaluate Your Models

```python
"""
Exercise: Build and run an evaluation pipeline.

1. Create a test set of 20 question-answer pairs
   covering different topics (factual, coding, creative)

2. Generate responses from:
   - GPT-4o-mini (baseline)
   - Your fine-tuned model (from Day 2/4)
   - A local model (Mistral 7B via Ollama)

3. Compute automatic metrics:
   - ROUGE-L
   - BERTScore
   - Perplexity (if applicable)

4. Run LLM-as-Judge evaluation:
   - Compare each pair of models
   - Use position-swapping for robustness

5. Create a results dashboard showing:
   - Metric comparison table
   - Win/loss/tie matrix
   - Per-category breakdown

Bonus: Add human evaluation for a subset of 10 examples
"""
```

---

## Key Takeaways — Measuring Quality

1. **No single metric** captures all aspects of text quality
1. **BLEU** and **ROUGE** measure surface-level similarity
1. **BERTScore** captures semantic meaning but not factual accuracy
1. **Perplexity** measures fluency, not correctness
1. **LLM-as-Judge** is flexible but susceptible to position bias
1. **Human evaluation** is the gold standard but expensive
1. Always use **multiple metrics** and evaluation approaches
1. Build **automated evaluation pipelines** for continuous testing

---

## MAUVE Score — Distribution-Level Evaluation

Measures how close the generated text distribution is to human text:

```python
import mauve

# Compare distributions of generated vs. human text
p_text = [  # Human-written text samples
    "The meeting concluded with a discussion of Q3 targets.",
    "Research findings indicate a strong correlation.",
    # ... 100+ samples
]

q_text = [  # Model-generated text samples
    "The session ended with an overview of quarterly objectives.",
    "Study results demonstrate a significant relationship.",
    # ... 100+ samples
]

result = mauve.compute_mauve(
    p_text=p_text,
    q_text=q_text,
    device_id=0,
    max_text_length=256,
    verbose=True,
)

print(f"MAUVE score: {result.mauve:.4f}")
# Closer to 1.0 = generated text is more human-like
# Useful for evaluating open-ended generation quality
```

---

## Evaluation for Specific Tasks

```python
# Task-specific evaluation strategies

evaluation_strategies = {
    "summarization": {
        "auto_metrics": ["ROUGE-1", "ROUGE-2", "ROUGE-L", "BERTScore"],
        "human_eval": ["faithfulness", "coverage", "conciseness"],
        "key_test": "Does the summary contain hallucinated info?",
    },
    "translation": {
        "auto_metrics": ["BLEU", "COMET", "chrF++"],
        "human_eval": ["adequacy", "fluency"],
        "key_test": "Are technical terms correctly translated?",
    },
    "code_generation": {
        "auto_metrics": ["pass@k", "CodeBLEU"],
        "human_eval": ["correctness", "readability", "efficiency"],
        "key_test": "Do generated tests pass? Does code compile?",
    },
    "question_answering": {
        "auto_metrics": ["Exact Match", "F1", "BERTScore"],
        "human_eval": ["correctness", "completeness"],
        "key_test": "Is the answer factually verifiable?",
    },
    "dialogue": {
        "auto_metrics": ["BLEU", "Distinct-n", "BERTScore"],
        "human_eval": ["coherence", "engagement", "safety"],
        "key_test": "Does the conversation stay on topic?",
    },
}
```

---

## A/B Testing LLM Applications

```python
import random
from collections import defaultdict

class LLMABTest:
    """A/B test different LLM configurations."""

    def __init__(self, variants):
        self.variants = variants  # {"A": config_a, "B": config_b}
        self.results = defaultdict(list)

    def get_variant(self, user_id):
        """Deterministic assignment based on user ID."""
        return "A" if hash(user_id) % 2 == 0 else "B"

    def generate(self, user_id, prompt):
        variant = self.get_variant(user_id)
        config = self.variants[variant]

        response = client.chat.completions.create(
            model=config["model"],
            messages=[{"role": "user", "content": prompt}],
            temperature=config.get("temperature", 0.7),
        )
        return variant, response.choices[0].message.content

    def record_feedback(self, variant, score):
        self.results[variant].append(score)

    def analyze(self):
        for variant, scores in self.results.items():
            avg = sum(scores) / len(scores)
            print(f"Variant {variant}: avg={avg:.3f}, n={len(scores)}")
```

---

## Continuous Evaluation Pipeline

```python
# Automated evaluation running in production

class ContinuousEval:
    """Monitor model quality in production."""

    def __init__(self, thresholds):
        self.thresholds = thresholds
        self.metrics_history = []

    def evaluate_batch(self, inputs, outputs, references=None):
        metrics = {}

        # Response quality (length, format compliance)
        metrics["avg_length"] = sum(len(o) for o in outputs) / len(outputs)
        metrics["empty_responses"] = sum(1 for o in outputs if not o.strip())

        # Safety check
        flagged = sum(1 for o in outputs if is_flagged(o))
        metrics["safety_flag_rate"] = flagged / len(outputs)

        # Reference-based metrics (if available)
        if references:
            metrics["bertscore"] = compute_bertscore(outputs, references)

        # Check against thresholds
        alerts = []
        for metric, value in metrics.items():
            if metric in self.thresholds:
                if value < self.thresholds[metric]["min"]:
                    alerts.append(f"LOW {metric}: {value}")
                if value > self.thresholds[metric]["max"]:
                    alerts.append(f"HIGH {metric}: {value}")

        self.metrics_history.append(metrics)
        return metrics, alerts
```

---

## CodeBLEU — Evaluating Code Generation

```python
# CodeBLEU: specialized metric for code quality

# Components:
# 1. Standard BLEU (n-gram overlap)
# 2. Weighted BLEU (gives more weight to keywords)
# 3. Syntax match (AST similarity)
# 4. Data flow match (variable usage patterns)

# CodeBLEU = α·BLEU + β·BLEU_weight + γ·syntax_match + δ·dataflow_match

def evaluate_code_generation(predictions, references):
    """Evaluate generated code quality."""
    from codebleu import calc_codebleu

    result = calc_codebleu(
        references=[[ref] for ref in references],
        predictions=predictions,
        lang="python",
        weights=(0.25, 0.25, 0.25, 0.25),  # Equal weight
    )

    print(f"CodeBLEU:     {result['codebleu']:.4f}")
    print(f"BLEU:         {result['ngram_match_score']:.4f}")
    print(f"Weighted:     {result['weighted_ngram_match_score']:.4f}")
    print(f"Syntax:       {result['syntax_match_score']:.4f}")
    print(f"Dataflow:     {result['dataflow_match_score']:.4f}")

    return result

# Also useful: pass@k metric
# Generate k solutions, check if any pass all tests
# pass@1: probability that a single generation is correct
```

---

## Factuality Evaluation

```python
def evaluate_factuality(question, response, evidence=None):
    """Check if the response contains factual errors."""

    # Method 1: Self-consistency check
    # Generate multiple responses and check agreement
    responses = []
    for _ in range(5):
        r = client.chat.completions.create(
            model="gpt-4o", temperature=0.7,
            messages=[{"role": "user", "content": question}],
        )
        responses.append(r.choices[0].message.content)

    # Check claims in the original response against consensus
    fact_check = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content":
                "Check each factual claim in the RESPONSE against "
                "the EVIDENCE responses. Flag any inconsistencies."},
            {"role": "user", "content":
                f"RESPONSE to check:\n{response}\n\n"
                f"EVIDENCE (multiple independent responses):\n"
                + "\n---\n".join(responses)},
        ],
    )
    return fact_check.choices[0].message.content
```
