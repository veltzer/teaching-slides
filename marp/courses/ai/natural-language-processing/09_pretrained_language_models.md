---
tags:
  - data-and-ai:nlp
  - data-and-ai:llm
  - concepts:transformers
  - concepts:fine-tuning
  - concepts:pretraining
level: advanced
category: ai
audience:
  - audiences:developers
  - audiences:data-scientists

---

# Pre-trained Language Models

---

## What This Chapter Covers

- Encoder, decoder, and encoder-decoder transformer families
- Pre-training objectives and the data that powers them
- Tokenizers as part of the model contract
- Fine-tuning, parameter-efficient adaptation, and forgetting
- Few-shot, zero-shot, and the boundary between prompting and training

---

## Why Pre-training Changed Everything

- A single model trained once, adapted many times
- Self-supervised objectives unlock unlabeled text at web scale
- Downstream tasks need orders of magnitude less labeled data
- Quality on small datasets often exceeds older fully-supervised systems

---

## The Three Architectural Families

![architecture_families](svg/courses/ai/natural-language-processing/09_pretrained_language_models/architecture_families.svg)

---

## Encoder Models: BERT

- Bidirectional transformer — every token attends to every other token
- Pre-trained with masked language modeling (`MLM`) and next-sentence prediction
- Outputs contextual embeddings; no native generation capability
- Strongest on classification, tagging, and span-extraction tasks

---

## BERT Pre-training Objectives

- `MLM`: 15% of input tokens are corrupted; the model predicts the original
    - 80% of the time replaced with `[MASK]`
    - 10% replaced with a random token
    - 10% left unchanged
- `NSP`: predict whether sentence B follows sentence A in the corpus
- The `[CLS]` token aggregates a sequence-level representation

---

## RoBERTa

- Same architecture as `BERT`, retrained with better recipe
- Drops `NSP`; trains longer on more data with bigger batches
- Dynamic masking — a different mask each epoch
- Demonstrated that `BERT` was undertrained, not underdesigned

---

## ALBERT

- Cross-layer parameter sharing — one transformer block reused at every depth
- Factorized embedding matrix decouples vocabulary size from hidden size
- Replaces `NSP` with sentence-order prediction
- Smaller parameter count, similar quality, slower inference per step

---

## DistilBERT

- A student model trained to match a `BERT` teacher
- Roughly half the parameters, around 60% faster, 97% of accuracy
- Distillation loss combines soft targets, hard labels, and embedding similarity
- A common production baseline when latency matters

---

## ELECTRA

- Replaces `MLM` with replaced-token detection
- A small generator proposes replacements; the discriminator predicts which tokens were swapped
- Every input position contributes a training signal — not just the masked 15%
- Better sample efficiency than `BERT` at the same compute budget

---

## ELECTRA Versus MLM

![electra_vs_mlm](svg/courses/ai/natural-language-processing/09_pretrained_language_models/electra_vs_mlm.svg)

---

## Decoder Models: GPT Family

- Causal (left-to-right) transformer — each position attends only to past positions
- Pre-trained with next-token prediction on raw text
- Generation is the native operation; prompting is the interface
- Scales smoothly with parameters, data, and compute

---

## Causal Language Modeling at Scale

- Single objective, single architecture, vast quantities of data
- Loss decreases predictably as a power law in compute
- Larger models become qualitatively more capable, not just quantitatively
- In-context learning emerges around the multi-billion parameter range

---

## The GPT Lineage

- `GPT-1`: proof of concept that generative pre-training transfers
- `GPT-2`: zero-shot transfer becomes interesting at the billion-parameter scale
- `GPT-3`: in-context few-shot learning at 175B parameters
- Subsequent generations add instruction tuning, alignment, and tool use

---

## Encoder-Decoder Models: T5

- Reframes every task as text-to-text
- Inputs prefixed with a task tag: `translate English to German: ...`
- Pre-trained with span corruption — contiguous spans replaced by sentinel tokens
- One unified architecture and loss for classification, generation, and translation

---

## T5 Span Corruption

- Pick spans of consecutive tokens at random
- Replace each span with a unique sentinel token in the input
- The target is the sentinels followed by their original spans
- Forces the model to predict structured chunks rather than isolated tokens

---

## BART and mBART

- Encoder-decoder with denoising auto-encoder pre-training
- Corruptions include token masking, deletion, infilling, sentence shuffling
- Strong on summarization, translation, and dialogue
- `mBART` extends the recipe to many languages with a shared vocabulary

---

## Multilingual Variants

- `mBERT`, `XLM-R`, `mT5`, `mBART` — one model across many languages
- Shared subword vocabulary lets representations align across scripts
- Cross-lingual transfer: fine-tune in one language, evaluate in another
- Performance varies sharply with how well a language was represented in pre-training

---

## Tokenizers Recap

- `WordPiece` — `BERT` and descendants; `##` continuation marks
- `BPE` — `GPT` family, `RoBERTa`, `BART`; merge frequent pairs
- `SentencePiece` — `T5`, `ALBERT`, multilingual models; raw bytes, no whitespace assumption
- The tokenizer is part of the weights — never swap it out

---

## Pre-training Corpora

- Web crawl: `Common Crawl` cleaned into corpora like `C4`, `OSCAR`, `RefinedWeb`
- Curated sources: books, encyclopedias, code repositories, scientific papers
- Trillions of tokens for the largest open and closed models
- Composition decisions silently shape the resulting model's voice and knowledge

---

## Data Filtering and Quality

- Deduplication: near-duplicate documents inflate memorization without adding signal
- Toxicity and personally identifiable information filtering
- Quality classifiers trained on reference corpora score and prune
- Heuristic filters: line length, language detection, perplexity-based outlier removal

---

## Data Quality Effects Downstream

- Garbage at scale is still garbage — bigger does not fix dirty data
- Domain composition drives the model's defaults — code-heavy training improves coding
- Repeated copies become memorized verbatim — privacy and licensing risks
- Subtle filtering choices propagate as biases into every downstream task

---

## Fine-tuning: The Classical Recipe

- Replace the pre-training head with a task-specific head
- Train end-to-end on labeled data with a small learning rate
- Reuse the tokenizer, model weights, and special tokens unchanged
- Often a few epochs over a few thousand examples is enough

---

## Task-Specific Heads

- Classification: linear layer on top of `[CLS]` or pooled output
- Token tagging: per-token linear layer with cross-entropy
- Span prediction: two heads predicting start and end indices
- Generation: reuse the pre-training language modeling head with new prompts

---

## Learning Rate and Warmup

- Pre-trained weights are fragile — large updates erase what was learned
- Typical fine-tuning learning rates are 10 to 100 times smaller than pre-training
- A linear warmup over the first few hundred steps avoids early instability
- A linear or cosine decay over the remaining steps anneals to convergence

---

## Catastrophic Forgetting

- Aggressive fine-tuning overwrites general competence with task-specific patterns
- Symptom: high in-domain accuracy, sharply degraded out-of-domain behavior
- Mitigations: smaller learning rates, fewer epochs, mixing in pre-training data
- Parameter-efficient methods sidestep the problem by leaving most weights untouched

---

## Parameter-Efficient Fine-tuning

![peft_methods](svg/courses/ai/natural-language-processing/09_pretrained_language_models/peft_methods.svg)

---

## LoRA

- Low-rank adaptation — freeze the base weights, add small trainable matrices
- Each weight matrix `W` is adapted as `W + B A` with `A` and `B` of low rank
- Trains a tiny fraction of parameters with quality close to full fine-tuning
- Adapters merge back into the base weights at inference — zero added latency

---

## Adapters

- Insert small bottleneck modules between transformer layers
- Train only the adapter; freeze the rest
- One adapter per task — swap them in and out at inference
- Slight inference overhead from the extra layer per block

---

## Prefix and Prompt Tuning

- Prepend trainable continuous vectors to the key and value sequences
- The base model never sees its weights change
- Works best at scale; fragile on smaller models
- A natural bridge between fine-tuning and prompting

---

## Code Example: LoRA With PEFT

```python
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForSequenceClassification

base = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")
config = LoraConfig(r=8, lora_alpha=16, target_modules=["query", "value"])
model = get_peft_model(base, config)
model.print_trainable_parameters()
```

- Trainable parameters drop from hundreds of millions to a few million
- Same training loop as full fine-tuning, much smaller checkpoints

---

## Zero-Shot Learning

- Ask a pre-trained model to perform a task it was never explicitly trained on
- The task is described in natural language; no labeled examples are provided
- Works because pre-training corpora contain countless implicit task demonstrations
- Quality scales sharply with model size

---

## Few-Shot In-Context Learning

- Place a handful of input-output examples inside the prompt
- The model induces the task pattern and continues it on the new input
- No parameter updates — the prompt itself is the adaptation
- Sensitive to example order, formatting, and choice

---

## Prompt Design as an Alternative to Fine-tuning

- For many tasks, a careful prompt rivals or beats fine-tuned smaller models
- Iteration is faster — no training loop, no GPU, no checkpoint management
- Costs shift from training to inference: every call pays the prompt token bill
- Reproducibility is harder; small prompt edits can move the model

---

## Limits of Zero-Shot Generalization

- Tasks far outside the training distribution still need supervised signal
- Numerical reasoning, structured extraction, and precise formatting often fail
- Hallucination is the default when the model is uncertain
- Specialist domains (medical, legal, low-resource languages) benefit from fine-tuning

---

## Choosing Between Fine-tuning and Prompting

- Few labeled examples and frequent prompt changes — prompt
- Many labeled examples and stable schema — fine-tune (often parameter-efficient)
- Strict latency or privacy constraints — fine-tune a smaller model on premise
- Hybrid: use prompting to bootstrap labels, then distill into a smaller model

---

## Adaptation Decision Map

![adaptation_decision](svg/courses/ai/natural-language-processing/09_pretrained_language_models/adaptation_decision.svg)

---

## Anti-Patterns

- Mixing tokenizers between training and inference
- Fine-tuning at the pre-training learning rate
- Evaluating only on in-domain data and missing forgetting
- Trusting a zero-shot answer without verification on a held-out set

---

## Summary

- Encoder, decoder, and encoder-decoder serve different downstream shapes
- Pre-training objectives and data composition determine the model's character
- Fine-tuning is powerful; parameter-efficient variants are the modern default
- Prompting and fine-tuning are complementary tools, not competitors
- The tokenizer, weights, and pre-training data form an inseparable contract
