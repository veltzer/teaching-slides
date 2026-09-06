---
tags:
  - data-and-ai:nlp
  - concepts:deep-learning
  - concepts:transformers
level: advanced
category: ai
audience:
  - audiences:developers
  - audiences:data-scientists
  - audiences:architects

---

# Attention and Transformers

---

## What This Chapter Covers

- Attention as the answer to the recurrent bottleneck
- Self-attention, queries, keys, values, and what they buy us
- Multi-head attention and the rest of the transformer block
- Positional encoding flavors and where layer norm goes
- Pre-training objectives and what scaling laws tell us about them

---

## The Bottleneck Problem

- Sequence-to-sequence with `RNN` encoders compresses the entire input into one fixed vector
- That vector becomes the only channel through which the decoder sees the source
- Long inputs lose information; rare details vanish into the average
- Bahdanau and colleagues asked: what if the decoder could look back directly?

---

## From Bottleneck to Soft Alignment

![attention_evolution](svg/courses/ai/natural-language-processing/08_attention_and_transformers/attention_evolution.svg)

---

## Bahdanau Attention

- At each decoder step, score every encoder hidden state against the decoder state
- A small feed-forward network produces the alignment scores
- A `softmax` turns scores into a distribution over source positions
- The context vector is the weighted average of encoder states under that distribution

---

## Luong Attention

- A leaner variant that arrived shortly after Bahdanau
- Scores are computed as a dot product (or bilinear form) instead of a feed-forward step
- Global vs local variants — local attends to a small window around an aligned position
- Faster and simpler; sets the stage for the dot-product attention used everywhere today

---

## Scaled Dot-Product Attention

- Score = query dot key, then divide by square root of the key dimension
- Apply `softmax` over the keys to get attention weights
- Output = weighted sum of values
- The scaling factor keeps the `softmax` from saturating when dimensions grow

---

## The Attention Equation

```python
def attention(Q, K, V, mask=None):
    d_k = Q.size(-1)
    scores = Q @ K.transpose(-2, -1) / math.sqrt(d_k)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
    weights = F.softmax(scores, dim=-1)
    return weights @ V
```

- Three matrix multiplies and a `softmax` — that is the entire mechanism
- Mask future positions for causal models, padding for batched inputs

---

## Self-Attention

- Queries, keys, and values all come from the same sequence
- Each position asks every other position: how relevant are you to me?
- The answer is a weighted blend of the entire context, position by position
- No recurrence, no convolutions — just one global matching step

---

## Queries, Keys, and Values

![qkv_intuition](svg/courses/ai/natural-language-processing/08_attention_and_transformers/qkv_intuition.svg)

---

## Why Self-Attention Captures Long Range

- Every position can attend to every other position in a single layer
- Path length between any two tokens is `O(1)` — no information has to travel through intermediate states
- Recurrent networks have path length `O(n)`; convolutions are `O(n / kernel)`
- Long-range dependencies stop being a structural problem and become a learning problem

---

## Computational Complexity

- Attention is `O(n squared d)` in time and memory for sequence length `n`
- Recurrence is `O(n d squared)` — linear in `n` but sequential
- For typical `n` and `d`, attention dominates only at long contexts
- The quadratic term motivates sparse, linear, and chunked attention variants

---

## Why Three Projections

- Queries, keys, and values are all linear projections of the same input
- Separate projections let the model learn what to match on (keys), what to look for (queries), and what to return (values)
- Without them, attention collapses into a similarity-weighted blend of the input itself
- The projections are where most of the parameters of an attention layer live

---

## Multi-Head Attention

- Run several attention computations in parallel on different projected subspaces
- Each head learns a different relationship — syntactic, semantic, positional
- Concatenate the head outputs and project back to the model dimension
- More heads, smaller per-head dimension; same total parameter budget

---

## Multi-Head Architecture

![multi_head_attention](svg/courses/ai/natural-language-processing/08_attention_and_transformers/multi_head_attention.svg)

---

## Multi-Head in Code

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, dim, heads):
        super().__init__()
        self.heads = heads
        self.qkv = nn.Linear(dim, 3 * dim)
        self.out = nn.Linear(dim, dim)

    def forward(self, x, mask=None):
        b, n, _ = x.shape
        q, k, v = self.qkv(x).chunk(3, dim=-1)
        q, k, v = [t.view(b, n, self.heads, -1).transpose(1, 2)
                   for t in (q, k, v)]
        out = attention(q, k, v, mask)
        out = out.transpose(1, 2).reshape(b, n, -1)
        return self.out(out)
```

- A single fused `qkv` projection is faster than three separate ones
- The reshape splits the model dimension across heads

---

## What Heads Learn

- Some heads track local syntax — adjacent words, dependency arcs
- Some track coreference — pronouns to their antecedents
- Some attend almost everywhere and average — a soft skip connection
- Most heads are individually useful; some can be pruned with no loss

---

## The Transformer Block

- Multi-head self-attention followed by a position-wise feed-forward network
- Residual connections wrap both sublayers
- Layer normalization stabilizes training
- The block is repeated `L` times — depth comes from stacking, not from recurrence

---

## Encoder, Decoder, and Both

- Encoder-only: `BERT` and friends — bidirectional self-attention, used for understanding
- Decoder-only: `GPT` and friends — causal self-attention, used for generation
- Encoder-decoder: `T5`, original transformer — encoder reads, decoder generates with cross-attention
- Same building block; different masking and connection patterns

---

## Cross-Attention

- In encoder-decoder models, decoder layers attend to encoder outputs
- Queries come from the decoder, keys and values from the encoder
- This is how the decoder grounds its generation in the source
- Functionally, it is the modern replacement for Bahdanau-style alignment

---

## Positional Encoding

- Self-attention is permutation-equivariant — it sees a set, not a sequence
- We have to inject position information explicitly
- Three families dominate: sinusoidal, learned, and rotary
- Each makes different trade-offs between simplicity, length generalization, and inductive bias

---

## Positional Encoding Variants

![positional_encodings](svg/courses/ai/natural-language-processing/08_attention_and_transformers/positional_encodings.svg)

---

## Sinusoidal Positions

- The original transformer used fixed sine and cosine functions of different frequencies
- Each position gets a unique pattern across the embedding dimensions
- Relative offsets are recoverable as linear functions — addition becomes rotation
- Generalizes (somewhat) to lengths longer than seen in training

---

## Learned Positions

- Just an embedding table indexed by position
- Simple, often slightly better in-distribution
- Cannot extrapolate beyond the training context length without retraining
- Used by `BERT` and `GPT-2`

---

## Rotary Positions

- Rotate query and key vectors by an angle that depends on position
- Encodes relative position directly inside the attention scores
- Extrapolates better than learned, plays well with long-context fine-tuning
- The default in `LLaMA`, `Mistral`, and most modern open models

---

## Layer Normalization Placement

- Post-norm: normalize after the residual addition — original transformer
- Pre-norm: normalize before each sublayer — modern default
- Pre-norm is friendlier to deep stacks and large learning rates
- A small change with outsized effects on training stability

---

## Residual Connections

- Each sublayer adds its output to its input rather than replacing it
- Gradients have a direct path through the residual stream from the loss back to every layer
- Without residuals, deep transformers do not train at all
- The "residual stream" is now a useful interpretability frame as well

---

## A Minimal Transformer Block

```python
class Block(nn.Module):
    def __init__(self, dim, heads, ff_mult=4):
        super().__init__()
        self.norm1 = nn.LayerNorm(dim)
        self.attn = MultiHeadAttention(dim, heads)
        self.norm2 = nn.LayerNorm(dim)
        self.ff = nn.Sequential(
            nn.Linear(dim, ff_mult * dim),
            nn.GELU(),
            nn.Linear(ff_mult * dim, dim),
        )

    def forward(self, x, mask=None):
        x = x + self.attn(self.norm1(x), mask)
        x = x + self.ff(self.norm2(x))
        return x
```

- Pre-norm style; everything else is composed of these blocks

---

## Pre-Training Objectives Overview

- The architecture is fixed; the training objective shapes what the model becomes
- Masked LM, causal LM, span corruption, denoising, contrastive — all use the same backbone
- Each objective fits a different family of downstream tasks
- Choosing the objective is choosing a prior over what the model learns

---

## Masked Language Modeling

- Used by `BERT`: mask 15 percent of tokens, predict them from both sides
- Bidirectional context yields strong representations for understanding
- Predictions are over fixed slots, so generation requires extra machinery
- The masking ratio and strategy are tunable knobs

---

## Causal Language Modeling

- Used by `GPT`-style decoders: predict each token from its left context
- Trains every position at once thanks to causal masking
- A natural fit for generation — sampling continues the prefix
- The dominant pre-training objective for current chat and instruction models

---

## Span Corruption

- Used by `T5`: replace contiguous spans with sentinel tokens, then generate the spans
- Bridges masked and causal objectives — encoder sees corrupted input, decoder generates
- Span length and corruption rate are controlled hyperparameters
- Strong on conditional generation tasks

---

## Denoising and Contrastive

- Denoising: reconstruct a clean sequence from a noised version (deletion, permutation, infilling)
- Contrastive: pull representations of related pairs together, push unrelated apart
- `BART` mixes several denoising transformations during pre-training
- Sentence and document embeddings are typically learned with contrastive losses

---

## Choosing an Objective

- Generation-first: causal LM
- Understanding-first: masked LM
- Sequence-to-sequence: span corruption or full denoising
- Embeddings and retrieval: contrastive on top of an encoder

---

## Scaling Laws

- Loss falls as a power law in compute, data, and parameters — within ranges studied
- The three scale together; bottlenecks at any one of them stall progress
- Kaplan and later Chinchilla studies fit clean curves to surprising amounts of data
- Predictability lets us budget large training runs before launching them

---

## Compute, Data, and Parameters

- For a fixed compute budget, there is an optimal pair of model size and tokens trained
- Chinchilla showed earlier large models were undertrained — too big for their data
- A factor-of-two on compute is roughly a factor-of-two on both parameters and tokens
- Cheap inference favors smaller-but-longer-trained models on the same budget

---

## Emergent Capabilities

- Some abilities (arithmetic, multi-step reasoning, instruction following) appear abruptly with scale
- Smooth loss curves can hide step-function jumps in task accuracy
- The "emergence" framing is debated — some effects are artifacts of metric choice
- Either way, capabilities at one scale do not always extrapolate to the next

---

## Attention Anti-Patterns

- Forgetting the causal mask in a causal model — the model cheats and looks ahead
- Inconsistent positional encoding between training and inference
- Mixing pre-norm and post-norm components without checking
- Treating quadratic memory as free — long contexts are expensive

---

## Production Considerations

- `KV` caching during generation turns each step from `O(n)` into `O(1)` per token
- Flash attention rewrites the kernel to avoid materializing the full score matrix
- Quantization (8-bit, 4-bit) is now routine for inference, sometimes for training
- Memory, not flops, is usually the binding constraint at deployment

---

## When Not To Use a Transformer

- Very short sequences with strong locality — a small `CNN` may suffice
- Edge devices with tight memory budgets — distilled or recurrent models still compete
- Strict structured tasks where a pipeline of classical components is auditable
- The transformer is a default, not a law

---

## Summary

- Attention turns a fixed bottleneck into soft, learned alignment over the whole sequence
- Self-attention with multiple heads is the engine; the rest of the block is plumbing
- Positional encoding choice and layer-norm placement matter more than they appear
- Pre-training objectives shape the resulting model; pick by downstream use
- Scaling is real, predictable within ranges, and bounded by the smallest of compute, data, and parameters
