---
tags:
  - data-and-ai:deep-learning
level: intermediate
category: machine-learning
audience:
  - audiences:developers
  - audiences:data-scientists

---
# Transformers

---
## What This Chapter Covers

- Attention mechanism
- Self-attention and multi-head attention
- The transformer architecture
- Positional encoding
- BERT, GPT, and their variants
- Hugging Face Transformers library

---
## Why Transformers

- RNNs are sequential and slow
- Hard to learn long-range dependencies
- Attention removes both problems
- Backbone of modern AI

---
## The Attention Idea

- Look at all positions, weight by relevance
- Soft retrieval over the sequence
- Differentiable, so it learns
- Originated as an RNN add-on, took over

---
## Attention as Soft Lookup

- Query: what am I looking for
- Keys: index for each position
- Values: content at each position
- Output: weighted sum of values

---
## Attention Diagram

![attention](svg/courses/machine_learning/deep-learning-fundamentals/05_transformers/attention.svg)

---
## Query, Key, Value

![qkv attention](svg/courses/machine_learning/deep-learning-fundamentals/05_transformers/qkv_attention.svg)

---
## Scaled Dot-Product Attention

- Score = Q dot K^T
- Scale by sqrt(d_k) to stabilize
- Softmax to weights
- Output = weights dot V

---
## Why Scale by Sqrt(d)

- Dot products grow with dimension
- Softmax saturates with large values
- Scaling keeps gradients useful
- Tiny but essential detail

---
## Self-Attention

- Q, K, V all come from the same sequence
- Each position attends to every other
- Captures relationships in one step
- The core building block

---
## Cross-Attention

- Q from one sequence, K and V from another
- Used in encoder-decoder models
- Lets the decoder query the encoder
- Replaces the RNN bottleneck

---
## Multi-Head Attention

- Project to multiple smaller subspaces
- Run attention in each head
- Concatenate and project back
- Different heads focus on different patterns

---
## Multi-Head Attention Diagram

![multi_head_attention](svg/courses/machine_learning/deep-learning-fundamentals/05_transformers/multi_head_attention.svg)

---
## What Heads Learn

- Some track syntax
- Some track positional patterns
- Some attend to special tokens
- Often interpretable, sometimes not

---
## The Transformer Block

- Multi-head self-attention
- Add and layer norm
- Feedforward network
- Add and layer norm again

---
## Transformer Block Diagram

![transformer_block](svg/courses/machine_learning/deep-learning-fundamentals/05_transformers/transformer_block.svg)

---
## Residual Connections

- Skip connection around each sublayer
- Easier gradient flow
- Lets deep stacks train
- Inherited from ResNet ideas

---
## Layer Normalization

- Normalize across features per token
- Stabilizes training of deep stacks
- Pre-norm and post-norm variants
- Pre-norm dominates modern designs

---
## Feedforward Sublayer

- Two linear layers with a nonlinearity
- Independent per token
- Adds capacity between attention layers
- Often 4x the hidden dimension

---
## Positional Encoding

- Attention has no order by itself
- We must inject position information
- Added to token embeddings
- Two main flavors: sinusoidal and learned

---
## Sinusoidal Positions

- Fixed sin and cos patterns
- Different frequencies per dimension
- Can extrapolate to longer sequences
- The original transformer choice

---
## Learned Positions

- One embedding per position
- Simple and effective
- Fixed maximum length
- Used by BERT and many others

---
## Rotary Position Embeddings

- Rotate Q and K by position
- Encodes relative offsets directly
- Strong long-context behavior
- Used by LLaMA and many modern LLMs

---
## The Original Transformer

- Vaswani et al, "Attention Is All You Need", 2017
- Encoder-decoder for translation
- 6 layers each, 8 heads, 512 dim
- Replaced RNNs in seq2seq

---
## Encoder-Decoder Transformer

![transformer_architecture](svg/courses/machine_learning/deep-learning-fundamentals/05_transformers/transformer_architecture.svg)

---
## Encoder Only

- Bidirectional attention
- Good for understanding tasks
- BERT, RoBERTa, DeBERTa
- Output: contextual embeddings

---
## Decoder Only

- Causal attention (masked future)
- Good for generation
- GPT family, LLaMA, Mistral
- One model handles many tasks

---
## Encoder-Decoder

- Encoder reads input, decoder writes output
- T5, BART, original transformer
- Strong for translation and summarization
- Less popular than decoder-only for chat

---
## Causal Masking

- Each position only sees prior positions
- Implemented with a -infinity mask before softmax
- Lets the model train as a language model
- Essential for autoregressive generation

---
## Tokenization

- Models see token IDs, not characters
- Subword tokenizers handle rare words
- BPE, WordPiece, SentencePiece
- Same model, different tokenizer, different behavior

---
## BERT

- Bidirectional Encoder Representations
- Trained with masked language modeling
- Plus next sentence prediction (later dropped)
- Fine-tune for classification, QA, NER

---
## Masked Language Modeling

- Hide 15% of tokens
- Predict them from context
- Teaches bidirectional understanding
- Cheap, parallel pretraining objective

---
## Using BERT

- Add a small head on top
- Fine-tune end to end
- Or freeze and use as embeddings
- Workhorse of NLP for years

---
## GPT

- Generative Pretrained Transformer
- Decoder-only, autoregressive
- Trained on next-token prediction
- Same architecture, many sizes

---
## Next-Token Prediction

- Read tokens left to right
- Predict the next one
- Loss: cross-entropy on the vocabulary
- Simple objective, huge capability

---
## GPT-2, GPT-3, GPT-4

- Same idea, much more scale
- More data, more parameters, more compute
- Emergent behaviors at scale
- The chat models you use daily

---
## Scaling Laws

- Loss decreases with model size, data, compute
- Predictable curves over orders of magnitude
- Guides how to spend compute budgets
- Famously due to Kaplan et al, Hoffmann et al

---
## Instruction Tuning

- Pretrained model knows language
- Fine-tune on instruction-response pairs
- Teaches it to follow tasks
- Step toward useful assistants

---
## RLHF

- Reinforcement Learning from Human Feedback
- Humans rank model outputs
- Train a reward model
- Optimize policy against the reward

---
## Transformer Variants

- T5: text-to-text everything
- BART: denoising encoder-decoder
- LLaMA: open decoder-only series
- Mistral, Falcon, Qwen, Gemma

---
## Multimodal Transformers

- Same architecture, mixed inputs
- Vision Transformer for images
- CLIP for text-image alignment
- Audio, video, robotics

---
## Vision Transformer

- Split image into patches
- Treat patches as tokens
- Run a transformer encoder
- Competitive with CNNs at scale

---
## Hugging Face Transformers

- Library with thousands of pretrained models
- One API across architectures
- Tokenizers, models, training utilities
- Most NLP starts here today

---
## Loading a Model

```python
from transformers import AutoTokenizer, AutoModel

tok = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

x = tok("hello world", return_tensors="pt")
out = model(**x)
```

---
## Text Classification with HF

```python
from transformers import pipeline

cls = pipeline("sentiment-analysis")
print(cls("I love this course"))
```

- One line gets a working pipeline
- Great for prototyping

---
## Fine-Tuning with HF

```python
from transformers import Trainer, TrainingArguments

args = TrainingArguments(output_dir="out", num_train_epochs=3)
trainer = Trainer(model=model, args=args,
                  train_dataset=ds_train, eval_dataset=ds_val)
trainer.train()
```

---
## Inference Tricks

- KV cache: reuse past attention keys and values
- Speeds up generation enormously
- Speculative decoding: small model guesses
- Quantization: 8-bit or 4-bit weights

---
## Context Length

- How many tokens the model can attend to
- Cost grows quadratically with length
- Many tricks: sliding window, sparse attention
- Modern models reach 100k tokens and beyond

---
## Limitations

- Quadratic attention cost
- Hallucinations in generation
- Outdated training data
- Expensive to train from scratch

---
## When to Use a Transformer

- Any NLP task: almost always
- Vision: increasingly often
- Sequences with long-range structure
- When a strong pretrained model exists

---
## Summary

- Attention replaces recurrence with parallel lookups
- Self-attention plus feedforward stacks into transformers
- BERT, GPT, T5: same building blocks, different objectives
- Hugging Face makes them all easy to use
