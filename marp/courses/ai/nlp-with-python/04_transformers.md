---
tags:
  - data-and-ai:nlp
  - languages:python
level: intermediate
category: machine-learning
audience:
  - audiences:data-scientists

---
# Transformers

---
## What This Chapter Covers

- Why transformers
- Attention
- Pretraining and fine-tuning
- Hugging Face workflow
- Practical sizing

---
## Why Transformers

- State of the art on most tasks
- Transfer learning works
- Strong zero-shot ability
- Open weights and ecosystems

---
## Attention in 60 Seconds

- Each token attends to others
- Weighted sum of values
- Captures long-range context
- No recurrence required

---
## BERT, RoBERTa

- Encoder-only
- Bidirectional context
- Strong for classification, NER, QA
- Fine-tune on labeled data

---
## GPT Family

- Decoder-only
- Autoregressive generation
- Few-shot via prompts
- Foundation for most chat models

---
## Encoder-Decoder

- T5, BART
- Translation, summarization
- Conditional generation
- Cleaner for seq2seq

---
## Hugging Face Transformers

- Unified API across models
- Auto-detected tokenizer and model classes
- Trainer for fine-tuning
- Hub for pretrained weights

---
## Tokenizers

- Subword units
- Vocab fixed at training
- Fast Rust tokenizers in HF
- Match the model exactly

---
## Fine-Tuning

- Take pretrained model
- Add task head
- Train on labeled data
- Few epochs usually enough

---
## Parameter-Efficient Tuning

- LoRA, adapters
- Train small additions
- Keep base frozen
- Cheaper, easier to ship

---
## Inference Sizing

- Quantize to int8 or 4-bit
- Distill to a smaller model
- Batch where possible
- GPU vs CPU based on QPS

---
## Limits

- Hallucination
- Cost
- Bias from pretraining
- Latency

---
## Common Transformer Mistakes

- Fine-tuning when zero-shot suffices
- Mismatched tokenizer
- No early stopping
- Training on tiny data
- Ignoring inference cost
