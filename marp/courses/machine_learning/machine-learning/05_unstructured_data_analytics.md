---
tags:
  - data-and-ai:machine-learning
level: intermediate
category: machine-learning
audience:
  - audiences:data-scientists

---
# Unstructured Data Analytics

---
## What This Chapter Covers

- What is unstructured data
- Text: NLP basics
- Images: computer vision
- Audio
- Embeddings
- Foundation models

---
## Unstructured Data

- No fixed schema
- Text, images, audio, video
- Most data in the world
- Harder to model than tabular

---
## Data Kinds

![data_kinds](svg/courses/machine_learning/machine-learning/05_unstructured_data_analytics/data_kinds.svg)

---
## Text Preprocessing

- Tokenisation: words / subwords
- Lowercase, punctuation
- Stop words
- Stemming / lemmatisation

---
## Bag-of-Words / TF-IDF

- Count words per document
- TF-IDF: term frequency, inverse document frequency
- Sparse vectors
- Baseline for text classification

---
## Word Embeddings

- Dense vectors per word
- Word2Vec, GloVe
- Captures semantic similarity
- "king" - "man" + "woman" = "queen"

---
## Transformers

- Attention mechanism
- Process sequences in parallel
- BERT, GPT, T5
- State of the art for NLP

---
## NLP Tasks

- Classification: sentiment, intent
- NER: named entity recognition
- Translation
- Summarisation
- Question answering

---
## Computer Vision Basics

- Pixels, channels, resolution
- Convolutions: local patterns
- Pooling: downsample
- Stack into CNNs

---
## CNN Architectures

- LeNet, AlexNet, VGG
- ResNet: skip connections
- EfficientNet
- Vision Transformers (ViT)

---
## Vision Tasks

- Classification: what is in the image
- Detection: where are the objects
- Segmentation: pixel-level labels
- Generation: create images

---
## Audio

- Spectrograms: time-frequency
- Treat like images or sequences
- Speech recognition: audio to text
- Speech synthesis: text to audio

---
## Embeddings

- Map any data to a vector
- Similar things, similar vectors
- Use for: search, clustering, retrieval
- Vector databases

---
## Foundation Models

- Pre-trained on massive data
- GPT, CLIP, DINO
- Adapt via fine-tuning or prompting
- Transfer learning at scale

---
## Multimodal

- Multiple input types
- CLIP: image + text
- Vision-language models
- Search image with text query

---
## Practical Considerations

- Compute cost is real
- Hosted APIs vs self-host
- Latency matters at inference
- Data labelling is expensive

---
## Common Unstructured Data Mistakes

- Training from scratch when pre-trained exists
- Ignoring data augmentation for vision
- Tokenisation mismatches between train and serve
- Embeddings without normalisation for similarity
- Not measuring inference latency
