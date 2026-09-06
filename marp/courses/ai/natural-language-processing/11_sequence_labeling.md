---
tags:
  - data-and-ai:nlp
  - concepts:machine-learning
level: advanced
category: ai
audience:
  - audiences:developers
  - audiences:data-scientists

---

# Sequence Labeling

---

## What This Chapter Covers

- Sequence labeling as a unifying frame for many `NLP` tasks
- Tagging schemes: `IOB`, `BIOES`, `BILOU` and the constraints they encode
- Hidden Markov Models, Viterbi decoding, forward-backward, Baum-Welch
- Maximum Entropy Markov Models and the label bias problem
- Conditional Random Fields and why they fix that bias
- Neural taggers: BiLSTM-CRF, transformer-based, and span-based approaches

---

## Sequence Labeling As A Unifying Task

- Many problems reduce to assigning a label to every token in a sequence
- Part-of-speech tagging, named entity recognition, chunking, slot filling
- The output is structured: labels at adjacent positions are not independent
- A model that ignores label structure leaves accuracy on the table

---

## Why Per-Token Labels Need Structure

- A label sequence must be consistent — `I-PER` cannot follow `B-LOC`
- Some transitions are illegal under the chosen scheme
- Independent per-token classifiers happily produce illegal outputs
- The decoder must search the space of valid label sequences, not single-position argmax

---

## The IOB Tagging Scheme

- `B-X` marks the beginning of a span of type `X`
- `I-X` marks a token inside that span
- `O` marks a token outside any span
- The classical scheme, simple and widely supported

---

## IOB Edge Cases

- Two adjacent spans of the same type need a `B-X` to mark the second beginning
- Original `IOB1` only used `B-X` to disambiguate adjacent same-type spans
- Modern `IOB2` always uses `B-X` at the start of every span — cleaner and more common
- "IOB" without qualification today usually means `IOB2`

---

## BIOES And BILOU

- `BIOES` adds `E-X` for end-of-span and `S-X` for single-token spans
- `BILOU` is the same idea with different letters: Begin, Inside, Last, Outside, Unit
- Richer schemes give the model more signal about span boundaries
- They also make the label space larger and the data slightly sparser per label

---

## Tagging Schemes Compared

![tagging_schemes](svg/courses/ai/natural-language-processing/11_sequence_labeling/tagging_schemes.svg)

---

## Choosing A Scheme

- `BIOES` and `BILOU` consistently match or beat `IOB2` on entity recognition
- The gain comes from explicit end-of-span signal, not from the extra labels themselves
- For very small datasets, `IOB2` may train more reliably
- Whichever scheme — apply it consistently to training, evaluation, and post-processing

---

## Hidden Markov Models

- A generative model of `(tokens, labels)` jointly
- Hidden states are the labels; observations are the tokens
- Two distributions: transition `P(y_t | y_{t-1})` and emission `P(x_t | y_t)`
- Joint probability factorizes over the chain

---

## HMM Joint Probability

- `P(x, y) = P(y_1) * prod_t P(y_t | y_{t-1}) * P(x_t | y_t)`
- Three sets of parameters: initial, transition, emission
- Trained by counting on labeled data — closed-form maximum likelihood
- Inference is finding the most probable label sequence given the tokens

---

## Viterbi Decoding

- Dynamic programming over the trellis of label states across time
- `delta_t(j) = max_i delta_{t-1}(i) * P(j | i) * P(x_t | j)`
- Keep backpointers; recover the best path at the end
- Linear in sequence length, quadratic in label set size

---

## Viterbi Trellis

![viterbi_trellis](svg/courses/ai/natural-language-processing/11_sequence_labeling/viterbi_trellis.svg)

---

## A Minimal Viterbi In Code

```python
def viterbi(obs, init, trans, emit):
    T, K = len(obs), len(init)
    delta = [[0.0] * K for _ in range(T)]
    back = [[0] * K for _ in range(T)]
    for j in range(K):
        delta[0][j] = init[j] * emit[j][obs[0]]
    for t in range(1, T):
        for j in range(K):
            best = max((delta[t-1][i] * trans[i][j], i) for i in range(K))
            delta[t][j] = best[0] * emit[j][obs[t]]
            back[t][j] = best[1]
    return delta, back
```

- Use log-probabilities in practice to avoid underflow

---

## Forward And Backward Probabilities

- Forward `alpha_t(j)` — total probability of all paths ending in state `j` at time `t`
- Backward `beta_t(j)` — total probability of all suffixes starting from state `j` at time `t`
- Together they give marginals: `P(y_t = j | x) ~ alpha_t(j) * beta_t(j)`
- The same recurrences as Viterbi but with sum instead of max

---

## Baum-Welch Training

- The `EM` algorithm for `HMMs` — used when labels are unobserved
- E-step: compute expected counts of transitions and emissions using forward-backward
- M-step: re-estimate parameters from those expected counts
- Converges to a local optimum; sensitive to initialization

---

## When HMMs Make Sense

- Small labeled corpora — closed-form training is data-efficient
- Tasks where the generative assumption is reasonable
- A solid baseline before reaching for discriminative or neural models
- Pedagogically essential — every later model is a discriminative or neural relaxation

---

## HMM Limitations

- Generative — must model `P(x | y)`, which is wasteful when we only need `P(y | x)`
- Hard to add overlapping features of the input (prefixes, suffixes, gazetteers)
- Strong independence assumptions about emissions
- These limits motivate the discriminative models that follow

---

## Maximum Entropy Markov Models

- Discriminative — model `P(y_t | y_{t-1}, x)` directly
- Each transition is a log-linear classifier over rich features of input and prior label
- `P(y | x) = prod_t P(y_t | y_{t-1}, x)`
- Allows arbitrary input features without modeling the input distribution

---

## MEMM Features

- Word identity, prefixes, suffixes, capitalization, shape
- Surrounding context tokens within a window
- Gazetteers and external lexicons
- Previous label is just another feature — no need for a generative emission model

---

## The Label Bias Problem

- Each step's distribution is locally normalized — sums to one over next labels
- A state with few outgoing transitions cannot "express dissatisfaction" with the input
- Probability mass is funneled forward regardless of how badly the input fits
- The model can ignore observations that contradict a confident path

---

## Label Bias Illustrated

![label_bias](svg/courses/ai/natural-language-processing/11_sequence_labeling/label_bias.svg)

---

## Conditional Random Fields

- Discriminative like `MEMM` but globally normalized
- Score the entire label sequence, not each transition independently
- `P(y | x) = exp(sum_t score(y_{t-1}, y_t, x, t)) / Z(x)`
- The partition function `Z(x)` sums over all label sequences

---

## Linear-Chain CRF

- Most common form — features couple adjacent labels and the input
- Score factorizes: emission features `f(y_t, x, t)` plus transition features `g(y_{t-1}, y_t)`
- Inference uses the same forward-backward and Viterbi recurrences as `HMMs`
- Training maximizes conditional log-likelihood with gradient descent

---

## Why CRFs Solve Label Bias

- Global normalization compares whole sequences, not local steps
- A bad path's score competes against all other paths through `Z(x)`
- The model can downweight a confident-looking transition when the rest of the sequence disagrees
- No state is forced to push probability forward — it can simply receive less mass overall

---

## CRF Training

- Compute the gradient of conditional log-likelihood
- Empirical feature counts minus expected feature counts under the model
- Expected counts come from forward-backward over the input
- L-BFGS, SGD, or Adam — any convex optimizer works since the objective is concave in features

---

## CRF Inference

- Viterbi for the most likely label sequence
- Forward-backward for marginal label probabilities
- N-best paths with a small modification to Viterbi
- All linear in sequence length, quadratic in label count

---

## Neural Sequence Labelers

- Replace hand-crafted features with learned representations
- A `BiLSTM` or transformer produces a contextual vector per token
- A linear head emits per-token scores
- Pair with a `CRF` layer to enforce label structure at decode time

---

## BiLSTM-CRF

![bilstm_crf](svg/courses/ai/natural-language-processing/11_sequence_labeling/bilstm_crf.svg)

---

## BiLSTM-CRF In Practice

```python
class BilstmCrf(nn.Module):
    def __init__(self, vocab, dim, n_tags):
        super().__init__()
        self.embed = nn.Embedding(vocab, dim)
        self.lstm = nn.LSTM(dim, dim, batch_first=True, bidirectional=True)
        self.head = nn.Linear(2 * dim, n_tags)
        self.crf = CRF(n_tags, batch_first=True)

    def loss(self, ids, tags, mask):
        emit = self.head(self.lstm(self.embed(ids))[0])
        return -self.crf(emit, tags, mask=mask)
```

- Emission scores from the network; transition scores learned by the `CRF`

---

## Transformer-Based Labelers

- Fine-tune a pretrained encoder (`BERT`, `RoBERTa`, `DeBERTa`) with a token classification head
- Subword tokenization complicates labeling — only the first subword of a word carries the label
- Often a soft-label or `CRF` layer on top still helps with boundary consistency
- The dominant approach for production sequence labeling today

---

## Subword Alignment

- Pretrained tokenizers split words into subwords; gold labels are word-level
- Standard practice: assign the gold label to the first subword and a special ignore label to the rest
- Loss masks the ignored positions during training
- At inference, aggregate subword predictions back to word level

---

## Span-Based Approaches

- Predict spans directly instead of token-by-token labels
- Enumerate candidate spans up to a max length and classify each
- Naturally handles overlapping or nested entities — multiple spans can fire on the same token
- Used in modern entity recognition and event extraction systems

---

## Span vs Token Labeling

- Token labeling — fast, well-understood, struggles with nested entities
- Span labeling — flexible, handles overlap, scales as `O(n^2)` candidate spans
- Hybrid: token labeling for flat entities, span labeling on top for nested
- Choice depends on the dataset's annotation guidelines

---

## Evaluating Sequence Labelers

- Token-level accuracy is misleading — `O` dominates the label distribution
- Standard metrics: span-level precision, recall, `F1` — exact match on type and boundaries
- `seqeval` is the canonical implementation
- Report per-type breakdown — average `F1` can hide collapsed performance on rare types

---

## Common Anti-Patterns

- Reporting token accuracy instead of span `F1`
- Mixing tagging schemes between data, model, and evaluation
- Letting an independent per-token classifier emit illegal label sequences
- Ignoring subword alignment — the model trains on a different label structure than expected

---

## When To Use Which Model

- Tiny dataset, fast deployment — `HMM` or `CRF` with hand-crafted features
- Medium data, no pretrained encoder available — `BiLSTM-CRF`
- Most production work — fine-tuned transformer with token classification head
- Nested or overlapping entities — span-based model on top of a transformer

---

## Summary

- Sequence labeling unifies tagging, chunking, and entity recognition under one frame
- Tagging schemes encode structural constraints — apply them consistently
- `HMM`, `MEMM`, `CRF` form a ladder of increasing expressiveness and decreasing bias
- `CRF` solves label bias by globally normalizing whole-sequence scores
- Neural taggers replace features with learned vectors; a `CRF` head still helps
- Span-based models extend the framework to nested and overlapping structure
