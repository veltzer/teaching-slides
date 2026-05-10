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
- Web scraping
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

![data_kinds](svg/courses/machine_learning/machine-learning/13_unstructured_data_analytics/data_kinds.svg)

---
## Why It Matters

- Reviews, social media
- Documents, contracts
- Photos, videos
- Medical scans, sensors

---
## Sources

- Public web
- Internal documents
- APIs
- Mobile and IoT
- Scraping with consent and care

---
## Web Scraping

- Fetch HTML, parse
- Respect robots.txt
- Rate-limit yourself
- Cache aggressively

---
## BeautifulSoup

```python
import requests
from bs4 import BeautifulSoup
html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")
titles = [h2.text for h2 in soup.find_all("h2")]
```

---
## Selecting Elements

- find / find_all
- CSS selectors with select
- XPath via lxml
- Composable

---
## Headless Browsers

- Playwright, Selenium
- Render JavaScript
- Slower, heavier
- Use only when needed

---
## Scraping Ethics

- Robots.txt and Terms of Service
- Don't hammer servers
- Personal data: GDPR applies
- Get explicit consent when possible

---
## Text Preprocessing

- Tokenisation: words / subwords
- Lowercase, punctuation
- Stop words
- Stemming / lemmatisation

---
## Tokenisation

- Word-level: split on whitespace and punctuation
- Subword: BPE, WordPiece, SentencePiece
- Character-level: rare
- Match the model's tokeniser

---
## Stop Words

- Common words: "the", "and", "is"
- Often removed for bag-of-words
- Kept for transformers
- Domain-specific lists

---
## Stemming vs Lemmatisation

- Stemming: chop endings (running → run)
- Lemmatisation: dictionary-based (better → good)
- Lemmatisation is slower, more accurate
- Both reduce vocabulary

---
## Bag-of-Words

- Vocabulary of words
- Count occurrences per document
- Sparse vector
- Order ignored

---
## TF-IDF

- Term frequency: count in doc
- Inverse document frequency: rarity across corpus
- Multiply: down-weight common words
- Sparse, fast, baseline

---
## n-Grams

- Single words: unigrams
- Pairs: bigrams
- Captures local order
- Vocabulary explodes

---
## sklearn Text

```python
from sklearn.feature_extraction.text import TfidfVectorizer
vec = TfidfVectorizer(ngram_range=(1, 2), max_features=10000)
X = vec.fit_transform(documents)
```

---
## Word Embeddings

- Dense vectors per word
- Word2Vec, GloVe
- Captures semantic similarity
- "king" - "man" + "woman" = "queen"

---
## Sentence Embeddings

- One vector per sentence or document
- Sentence-BERT
- Universal Sentence Encoder
- Use for semantic search

---
## Transformers

- Attention mechanism
- Process sequences in parallel
- BERT, GPT, T5
- State of the art for NLP

---
## Hugging Face

- Models, datasets, tokenisers
- Pipelines for common tasks
- Free and paid hosting
- Fine-tuning APIs

---
## Hugging Face Pipeline

```python
from transformers import pipeline
clf = pipeline("sentiment-analysis")
clf("I love this product")
```

---
## NLP Tasks

- Classification: sentiment, intent
- NER: named entity recognition
- Translation
- Summarisation
- Question answering

---
## Sentiment Analysis

- Positive, negative, neutral
- Domain-specific lexicons
- Pre-trained models exist
- Fine-tune for your domain

---
## Named Entity Recognition

- People, places, organisations
- BIO tagging scheme
- spaCy, transformers
- Useful for extraction

---
## Topic Modelling

- LDA: Latent Dirichlet Allocation
- NMF
- BERTopic
- Discover themes in a corpus

---
## Text Classification Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
pipe = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf",   LogisticRegression()),
])
```

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
## Image Augmentation

- Rotations, flips, crops
- Colour jitter
- Mixup, cutout
- Doubles dataset effectively

---
## Transfer Learning Vision

- Pretrained backbone
- Replace head
- Fine-tune
- Saves orders of magnitude of data

---
## Audio

- Spectrograms: time-frequency
- Treat like images or sequences
- Speech recognition: audio to text
- Speech synthesis: text to audio

---
## Audio Pipeline

- Resample
- Spectrogram
- Mel filter banks
- CNN or transformer

---
## Embeddings

- Map any data to a vector
- Similar things, similar vectors
- Use for: search, clustering, retrieval
- Vector databases

---
## Vector Databases

- FAISS, Pinecone, Weaviate, pgvector
- Approximate nearest neighbour
- Scale to millions
- Power semantic search

---
## Foundation Models

- Pre-trained on massive data
- GPT, CLIP, DINO
- Adapt via fine-tuning or prompting
- Transfer learning at scale

---
## Fine-Tuning

- Small data, big pretrained model
- Add task head
- Train briefly
- Often best for accuracy

---
## Prompting

- Use the model as-is
- Craft inputs
- Few-shot examples
- Cheaper than fine-tuning

---
## Multimodal

- Multiple input types
- CLIP: image + text
- Vision-language models
- Search image with text query

---
## RAG

- Retrieval-Augmented Generation
- Fetch relevant docs, prepend to prompt
- Reduces hallucination
- Standard pattern for LLM apps

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

---
## Spectrogram

![spectrogram](svg/courses/machine_learning/machine-learning/13_unstructured_data_analytics/spectrogram.svg)

---
## RAG Pipeline

![rag_pipeline](svg/courses/machine_learning/machine-learning/13_unstructured_data_analytics/rag_pipeline.svg)

---
## Summary

- Unstructured data dominates the wild
- Use pretrained models when possible
- Embeddings turn anything into vectors
- Match tokenisers and preprocessing across train and serve
