---
tags:
  - data-and-ai:nlp
  - languages:python
level: intermediate
category: machine-learning
audience:
  - audiences:data-scientists

---
# Text Preprocessing

---
## What This Chapter Covers

- Tokenization
- Normalization
- Stop words
- Stemming and lemmatization
- Subword units

---
## Tokenization

- Split text into units
- Whitespace is naive
- Punctuation matters
- Language matters

---
## Word Tokenization

- spaCy: rule-based, language-aware
- NLTK: many tokenizers
- Regex: quick but fragile
- Use a library, not your own

---
## Sentence Tokenization

- Period is ambiguous
- Use a trained sentence segmenter
- Spans for downstream tasks
- Watch out for abbreviations

---
## Normalization

- Lowercasing
- Unicode normalization
- Removing accents
- Number handling

---
## Stop Words

- Common low-content words
- Often removed for bag-of-words
- Keep for language models
- Domain-specific lists matter

---
## Stemming

- Crude root extraction
- Porter, Snowball stemmers
- Fast but lossy
- Rarely used today

---
## Lemmatization

- Real dictionary form
- Needs POS tag
- Slower but accurate
- spaCy does it well

---
## Regex Cleaning

- Strip HTML
- Strip URLs
- Normalize whitespace
- Be careful with emojis

---
## Subword Tokenization

- BPE, WordPiece, SentencePiece
- Handles unknowns
- Standard for transformers
- Vocab is part of the model

---
## Strategies Compared

![tokenization](svg/courses/ai/nlp-with-python/02_text_preprocessing/tokenization.svg)

---
## Vectorization

- Bag of words
- TF-IDF
- Word embeddings
- Contextual embeddings

---
## Pipelines

- Compose steps
- spaCy.pipe for batch
- scikit-learn Pipeline for training
- Same code train and predict

---
## Common Preprocessing Mistakes

- Lowercasing for NER
- Stripping punctuation for parsing
- Mixing tokenizers train vs serve
- Different vocab in production
- Forgetting to fit on training only
