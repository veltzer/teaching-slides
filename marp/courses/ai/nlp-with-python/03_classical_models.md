---
tags:
  - data-and-ai:nlp
  - languages:python
level: intermediate
category: machine-learning
audience:
  - audiences:data-scientists

---
# Classical NLP Models

---
## What This Chapter Covers

- Bag of words
- TF-IDF
- Naive Bayes
- Logistic regression
- Why classical still matters

---
## Bag of Words

- Count of each word
- Ignores order
- Sparse vectors
- Easy to interpret

---
## TF-IDF

- Term frequency times inverse document frequency
- Down-weights common words
- Highlights distinctive words
- Strong baseline for classification

---
## Vocabulary Decisions

- Min and max document frequency
- N-grams of unigrams, bigrams
- Cap vocab size
- Hashing trick avoids vocab altogether

---
## Naive Bayes

- Assumes feature independence
- Fast to train and predict
- Works well on text
- Multinomial variant for counts

---
## Logistic Regression

- Linear model with sigmoid
- Strong baseline
- Good calibration
- Coefficient inspection is interpretable

---
## TF-IDF Plus Logistic Regression

![pipeline](svg/courses/ai/nlp-with-python/03_classical_models/tfidf_to_lr.svg)

---
## SVM

- Margin maximization
- Linear kernels work well on text
- Slower than logistic regression
- Strong on small data

---
## Random Forests

- Tree ensembles
- Handle non-linearity
- Less elegant on bag of words
- Useful when features mix text and numerics

---
## Sequence Models: HMM

- Hidden Markov models
- Tagging tasks
- POS tagging
- NER baseline

---
## CRF

- Conditional random fields
- Better than HMM for tagging
- Used in spaCy small models
- Trains well on labeled data

---
## When Classical Wins

- Small data
- Interpretability
- Tight latency budget
- Tabular plus text mix

---
## Baseline Discipline

- Always start with TF-IDF logistic regression
- Beats most over-engineered solutions
- Cheap to deploy
- Hard for transformers to justify cost when it works

---
## Common Classical Mistakes

- Over-tuning on validation
- Class imbalance ignored
- Leaking labels through preprocessing
- Skipping the baseline
- Using accuracy alone
