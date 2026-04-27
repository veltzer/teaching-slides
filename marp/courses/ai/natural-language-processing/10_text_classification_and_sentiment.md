---
tags:
  - data-and-ai:nlp
  - concepts:classification
level: advanced
category: ai
audience:
  - audiences:developers
  - audiences:data-scientists

---
# Text Classification and Sentiment Analysis

---
## What This Chapter Covers

- Classification fundamentals and class imbalance realities
- Classical and neural classifiers from `Naive Bayes` to transformers
- Sentiment, polarity, intensity, and emotion beyond the binary view
- Domain adaptation when the test data does not look like training
- Evaluation that survives skewed labels and adversarial reviewers

---
## Why Text Classification Still Matters

- Most production NLP is classification under the hood
- Spam, intent detection, content moderation, sentiment, triage, routing
- The labels look easy; the data distribution rarely cooperates
- A simple model that ships beats a transformer that does not generalize

---
## Binary, Multi-Class, Multi-Label

- Binary: one of two labels — `spam` or `not spam`
- Multi-class: one of many — language detection across 100 classes
- Multi-label: any subset — a news article can be `politics` and `economy` and `tech`
- The loss function and metric must match the regime; mismatching them silently rewards the wrong thing

---
## Classification Regimes

![classification_regimes](svg/courses/ai/natural-language-processing/10_text_classification_and_sentiment/classification_regimes.svg)

---
## Class Imbalance

- Real-world labels are rarely balanced — fraud is 0.1%, abuse is 2%, sentiment is 70/20/10
- A model that predicts the majority class scores 99% accuracy and is useless
- Imbalance shows up in loss gradients, calibration, and threshold choice
- Treat imbalance as a first-class design constraint, not a postprocessing knob

---
## Sampling Strategies

- Random oversampling of the minority class — risk of overfit on duplicates
- Random undersampling of the majority class — risk of throwing away signal
- `SMOTE` and variants synthesize minority examples in feature space
- Class weights in the loss avoid touching the data at all

---
## Threshold and Operating Points

- A binary classifier outputs a probability; the threshold turns it into a decision
- The default 0.5 is rarely optimal — pick the threshold from the validation curve
- The threshold encodes a business trade-off: precision versus recall, false alarms versus misses
- Pick a different threshold per deployment context, not globally

---
## Naive Bayes for Text

- Assume features (words) are independent given the class — wrong but useful
- Compute log-probabilities; sum across tokens; pick the highest class
- Trains in one pass, uses no GPU, and is hard to beat on small data
- Still the right baseline for a quick spam filter or topic classifier

---
## Logistic Regression with N-Grams

- Linear model on bag-of-n-grams features — interpretable and fast
- N-grams capture short-range structure that bag-of-words loses
- `L2` regularization keeps weights small; `L1` produces sparse, readable models
- Often within a few points of much larger neural models on standard benchmarks

---
## SVMs for Text

- Maximum-margin separator in a high-dimensional sparse space
- Linear `SVM` is the historical workhorse for text — see `LIBLINEAR`
- Robust to many irrelevant features, which is exactly what bag-of-words gives you
- Kernels rarely help on text; the linear case is usually enough

---
## Classical Classifiers Compared

![classical_classifiers](svg/courses/ai/natural-language-processing/10_text_classification_and_sentiment/classical_classifiers.svg)

---
## Feature Engineering vs Feature Learning

- Classical pipelines: hand-crafted features, lexicons, length, punctuation counts
- Neural pipelines: learn features from raw tokens through embeddings and layers
- Feature engineering still wins on small data and narrow domains
- The right question is not "which" but "how much labeled data do I have"

---
## CNNs for Text

- 1D convolutions over word embeddings — each filter learns a phrase pattern
- Multiple filter widths capture bigrams, trigrams, and longer windows
- Max-pooling picks the strongest activation per filter across the sentence
- Fast, parallel, and competitive with recurrent models on classification

---
## LSTMs and BiLSTMs

- `LSTM` reads left-to-right and accumulates context in a hidden state
- `BiLSTM` reads both directions and concatenates — every position sees full context
- Good at variable-length inputs and ordering-sensitive labels
- Largely superseded by transformers but still useful for small models and edge devices

---
## Transformer-Based Classifiers

- Take a pretrained encoder like `BERT` or `RoBERTa`, add a classification head
- The `[CLS]` token's final hidden state is the sentence representation
- Fine-tune on labeled data — usually a few epochs is enough
- The default modern choice when labeled data is in the thousands and up

---
## Sentiment Analysis Dimensions

- Polarity: positive, negative, neutral — the textbook task
- Intensity: how strongly positive or negative — a 5-star rating, not a thumbs-up
- Subjectivity: opinion versus fact — many "negative" sentences are just descriptions
- Treating sentiment as binary throws away most of the signal a real review carries

---
## Sentiment Beyond Polarity

![sentiment_dimensions](svg/courses/ai/natural-language-processing/10_text_classification_and_sentiment/sentiment_dimensions.svg)

---
## Aspect-Based Sentiment

- A review is rarely uniformly positive or negative
- "Great food, terrible service" is positive about `food` and negative about `service`
- Aspect-based sentiment extracts the target and the polarity per target
- Useful for product analytics, support triage, and competitive intelligence

---
## Emotion Detection

- Polarity collapses anger, sadness, and fear into a single negative score
- Emotion taxonomies (Ekman, Plutchik) give a richer label space
- Useful in mental health, customer support, and conversational systems
- Annotation is harder; agreement between annotators is lower

---
## Lexicon-Based Sentiment

- Hand-built lists assign a polarity score to each word — `VADER`, `SentiWordNet`, `LIWC`
- Sum or average word scores, with simple negation and intensifier rules
- Transparent, deterministic, no training data needed
- Brittle on sarcasm, domain-specific vocabulary, and code-switched text

---
## Learned vs Lexicon-Based

- Lexicons capture surface vocabulary; learned models capture context
- A learned model knows that `sick` is positive in skating reviews and negative in clinics
- Lexicons remain useful as features inside a learned model
- The hybrid usually beats either alone

---
## Domain Adaptation: The Problem

- Training on movie reviews, deploying on product reviews — out-of-distribution drift
- Vocabulary, length, register, and label distribution all shift
- Accuracy on the source domain says little about the target
- Always evaluate on the target domain, even if labels are scarce

---
## Out-of-Domain Generalization

- Models that look identical in-domain can differ wildly out-of-domain
- Spurious correlations in training data fail silently on a different distribution
- Robustness checks: paraphrase, back-translation, adversarial examples
- The right baseline is the worst-case domain, not the average

---
## Transfer Learning for Classifiers

- Pretrain a large model on unlabeled text; fine-tune on a small labeled set
- The pretrained model already knows syntax, semantics, and world facts
- Few-shot or even zero-shot classification is plausible with strong base models
- Has effectively replaced training from scratch for most production tasks

---
## Continued Pretraining on Domain Text

- When the target domain differs sharply (legal, biomedical, code)
- Continue masked language modeling on unlabeled domain text before fine-tuning
- Closes most of the in-domain gap without needing more labels
- Cheap relative to from-scratch pretraining; expensive relative to plain fine-tuning

---
## Domain Adaptation Strategies

![domain_adaptation](svg/courses/ai/natural-language-processing/10_text_classification_and_sentiment/domain_adaptation.svg)

---
## Accuracy Is Not Enough

- Accuracy is the headline metric and the most misleading one under imbalance
- Precision: of predicted positives, how many were correct
- Recall: of actual positives, how many were caught
- `F1`: harmonic mean of precision and recall — penalizes imbalance between them

---
## Confusion Matrices for Multi-Class

- Rows are true labels; columns are predictions; diagonal is correct
- Off-diagonals reveal which classes the model confuses with which
- Common pattern: confusion clusters along semantically similar classes
- Often the most useful single artifact for debugging a classifier

---
## Confusion Matrix Example

```diagram
              predicted
                pos   neu   neg
true   pos    [180    15     5]
       neu    [ 25   140    35]
       neg    [  3    20   177]
```

- High diagonal mass — the model mostly works
- `neutral` leaks into both `pos` and `neg` — a known weak spot

---
## ROC and PR Curves

- `ROC`: true positive rate against false positive rate as the threshold moves
- `PR`: precision against recall — more informative under heavy imbalance
- The area under each curve summarizes performance across all thresholds
- Pick PR over ROC when positives are rare; ROC can look great while PR is dismal

---
## Stratified Cross-Validation

- Random folds can put all the rare class into one fold by accident
- Stratified folds preserve the class distribution per fold
- Essential for imbalanced data and small datasets
- Combine with repeated runs for tight confidence intervals on small test sets

---
## A Minimal Classification Pipeline

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
    ("clf", LogisticRegression(class_weight="balanced", max_iter=1000)),
])
pipe.fit(train_texts, train_labels)
preds = pipe.predict(test_texts)
```

- A solid baseline in a dozen lines — beat this before reaching for transformers

---
## Anti-Patterns

- Reporting accuracy on imbalanced data without a baseline
- Tuning the threshold on the test set
- Mixing train and test by deduping after splitting
- Treating sentiment as binary on multi-aspect reviews
- Ignoring domain shift until the model meets production traffic

---
## When To Use Which Classifier

- Tens of examples: prompt a strong pretrained model, no fine-tuning
- Hundreds: fine-tune a small pretrained encoder
- Thousands and up: classical baseline plus a fine-tuned transformer to compare
- Millions: train a domain-specific encoder from scratch may pay off

---
## Summary

- Match the model to the data scale, not to the conference paper of the year
- Imbalance and domain shift are not edge cases; they are the default
- Sentiment is richer than polarity; treat it that way when the product needs it
- Choose metrics and threshold from the validation curve, not from defaults
- Always evaluate on the target domain, with stratified folds and a clear baseline
