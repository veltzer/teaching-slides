---
tags:
  - data-and-ai:nlp
  - languages:python
level: intermediate
category: machine-learning
audience:
  - audiences:data-scientists

---

# Introduction to NLP

---

## What This Chapter Covers

- What NLP is
- Core tasks
- Python ecosystem
- Course outline

---

## What NLP Is

- Computers processing human language
- Text and speech
- Understanding and generation
- A field, not a single technique

---

## Why Python

- Mature libraries
- Strong community
- Works with PyTorch and TF
- De facto standard

---

## Core Tasks

- Classification
- Named entity recognition
- Translation
- Summarization
- Question answering

---

## Classical Pipeline

- Tokenize
- Normalize
- Vectorize
- Model
- Evaluate

---

## Modern Pipeline

- Tokenize
- Encode with pretrained model
- Fine-tune or zero-shot
- Evaluate

---

## Pipelines Compared

![nlp_pipelines](svg/courses/ai/nlp-with-python/01_introduction/nlp_pipelines.svg)

---

## Key Libraries

- spaCy: production NLP
- NLTK: teaching, classical
- transformers library: pretrained models
- scikit-learn: classifiers

---

## Datasets

- IMDB, AG News for classification
- CoNLL for NER
- SQuAD for QA
- WMT for translation

---

## Evaluation Basics

- Accuracy is rarely enough
- Precision, recall, F1
- BLEU for translation
- ROUGE for summarization

---

## Languages and Scripts

- English is privileged
- Tokenization differs by language
- Right-to-left and CJK
- Watch for encoding bugs

---

## Hardware

- Classical: CPU is fine
- Transformers: GPU helps
- Big models: cloud or shared cluster
- Quantize for inference

---

## Course Outline

- Text preprocessing
- Classical models
- Word embeddings
- Transformers
- Production deployment

---

## Common Beginner Mistakes

- Skipping data inspection
- Ignoring class imbalance
- Using accuracy alone
- Training without a baseline
- Forgetting language assumptions
