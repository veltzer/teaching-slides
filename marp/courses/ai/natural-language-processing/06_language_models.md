---
tags:
  - data-and-ai:nlp
  - concepts:language-modeling
level: advanced
category: ai
audience:
  - audiences:developers
  - audiences:data-scientists

---
# Language Models

---
## What This Chapter Covers

- What a language model actually is — probability over sequences
- `n-gram` models, smoothing, back-off and interpolation
- Neural language models from Bengio onward
- Causal vs masked objectives and the pretrain-then-finetune paradigm
- Evaluation: perplexity, cross-entropy, bits-per-character, downstream tasks

---
## What Is a Language Model

- A distribution over sequences of tokens: `P(w_1, w_2, ..., w_n)`
- By the chain rule: `P(w_t | w_1, ..., w_{t-1})` at each step
- Training reduces to next-token prediction over a corpus
- Everything else — generation, scoring, ranking — falls out of that one distribution

---
## Why Sequence Probabilities Matter

- Speech recognition: pick the transcript with the highest probability
- Machine translation: among candidate translations, prefer the most probable
- Spelling correction: rank fixes by which sequence is more likely
- Generation: sample the next token from the conditional distribution

---
## The Three Eras

![lm_taxonomy](svg/courses/ai/natural-language-processing/06_language_models/lm_taxonomy.svg)

---
## Next-Token Prediction

- Given a prefix, predict the distribution over the next token
- Each prediction is a softmax over the entire vocabulary
- Training loss is the negative log-likelihood of the actual next token
- Decoding turns the distribution into text — greedy, sampling, or beam search

---
## n-gram Language Models

- Approximate `P(w_t | history)` by truncating the history to the last `n-1` tokens
- A bigram model conditions only on the previous word
- A trigram model conditions on the previous two
- Counts come from a training corpus; probabilities are ratios of counts

---
## Maximum Likelihood Estimation

- For a bigram model: `P(w_t | w_{t-1}) = count(w_{t-1}, w_t) / count(w_{t-1})`
- The estimate that makes the training data as likely as possible
- Simple, intuitive, and catastrophically wrong on unseen `n-grams`
- Any `n-gram` not in training gets probability zero — and zero kills the whole sequence

---
## The Sparsity Problem

- Vocabulary of 50k words means 2.5 billion possible bigrams
- Training corpora cover a small fraction of them
- Most plausible `n-grams` simply never appear in training
- We need to redistribute probability mass to events we have not yet seen

---
## Laplace Smoothing

- Add one (or a small alpha) to every count before normalizing
- Equivalent to a uniform prior over the vocabulary
- Easy to implement, easy to reason about
- Over-corrects badly: rare-but-real events get too little, unseen events get too much

---
## Good-Turing Smoothing

- Use the count of `n-grams` that occur `r` times to estimate the probability of `n-grams` that occur `r-1` times
- Total mass for unseen events equals the proportion of singletons
- Better than Laplace, but unstable for high counts
- Usually combined with another method for the high-count tail

---
## Kneser-Ney Smoothing

- Backs off based on how many distinct contexts a word appears in, not raw frequency
- A common word like `Francisco` is frequent but only after `San` — its back-off probability should be low
- Modified Kneser-Ney was the state of the art for `n-gram` LMs for years
- Still a sensible baseline when you cannot afford a neural model

---
## Smoothing Compared

![ngram_smoothing](svg/courses/ai/natural-language-processing/06_language_models/ngram_smoothing.svg)

---
## Back-off vs Interpolation

- Back-off: if the trigram is unseen, fall back to the bigram, then the unigram
- Interpolation: always use a weighted mix of trigram, bigram, and unigram estimates
- Interpolation tends to produce more stable estimates
- Both need a held-out set to tune the back-off weights or interpolation lambdas

---
## Limits of n-gram Models

- Long-range dependencies are invisible — anything beyond `n-1` tokens is ignored
- Vocabulary mismatches (rare words, morphological variants) hurt sharply
- Storage scales with the number of seen `n-grams` — gigabytes for a serious model
- No sharing of statistical strength between similar contexts

---
## The Neural Turn

- Represent each word as a dense vector — an embedding
- Similar words get similar vectors, so the model can generalize across contexts
- The conditional distribution becomes a neural function of the embeddings
- Bengio et al. (2003) introduced this with a feed-forward neural language model

---
## Bengio Feed-Forward LM

![neural_lm_architecture](svg/courses/ai/natural-language-processing/06_language_models/neural_lm_architecture.svg)

---
## Why the FFN LM Worked

- Embeddings let `cat` and `dog` share statistical strength
- The hidden layer learned non-linear interactions between context words
- Perplexity beat Kneser-Ney trigrams on the same data
- And it gave us word embeddings for free as a side effect

---
## Recurrent Language Models

- A recurrent network processes the sequence one token at a time
- The hidden state carries information from arbitrary-distance history
- No fixed context window — in principle, all of it is available
- `LSTM` and `GRU` cells made training stable enough to be useful at scale

---
## RNN Strengths and Weaknesses

- Strength: variable-length context, parameter sharing across positions
- Weakness: sequential computation — hard to parallelize across the time axis
- Weakness: vanishing gradients still bite for very long contexts
- The transformer eventually replaced them, but the conceptual leap was the RNN

---
## A Simple RNN LM in Code

```python
class RnnLM(nn.Module):
    def __init__(self, vocab, dim):
        super().__init__()
        self.embed = nn.Embedding(vocab, dim)
        self.rnn = nn.LSTM(dim, dim, batch_first=True)
        self.head = nn.Linear(dim, vocab)

    def forward(self, ids):
        x = self.embed(ids)
        h, _ = self.rnn(x)
        return self.head(h)
```

- Embeds tokens, runs an `LSTM`, projects back to vocabulary logits
- The same `forward` is used for training and for autoregressive sampling

---
## Modern Language Models

- Transformer architectures replaced recurrence with self-attention
- Two dominant training objectives: causal (left-to-right) and masked (fill-in-the-blank)
- Same architecture, different objective — `GPT` is causal, `BERT` is masked
- Scale changed everything: more data, more parameters, more compute

---
## Causal vs Masked

![causal_vs_masked](svg/courses/ai/natural-language-processing/06_language_models/causal_vs_masked.svg)

---
## Causal Language Modeling

- Predict each token from the tokens to its left
- A natural fit for generation — sampling continues the prefix
- Used by `GPT`, `LLaMA`, `Mistral`, almost every chat model
- Also used as a pure pretraining objective even when generation is not the end goal

---
## Masked Language Modeling

- Mask out 15 percent of tokens; predict them from both sides of context
- Bidirectional context is richer for understanding tasks
- Used by `BERT`, `RoBERTa`, `DeBERTa`, encoder-only models
- Not directly usable for generation — it predicts a fixed slot, not a continuation

---
## The Paradigm Shift

- Old way: design a task-specific model, train it from scratch on labeled data
- New way: pretrain a general LM on raw text, then finetune (or prompt) for the task
- Labeled data is expensive; unlabeled text is essentially free
- The general model often beats the specialist, even with much less labeled data

---
## Pretrain Then Finetune

- Pretraining: huge unlabeled corpus, expensive, done once per architecture
- Finetuning: small labeled set, cheap, repeated per downstream task
- Modern variants: prompting, in-context learning, parameter-efficient tuning
- The pretrained checkpoint is the artifact you actually share and reuse

---
## Evaluation: Perplexity

- Perplexity is the exponentiated average negative log-likelihood per token
- Intuition: the effective branching factor at each step
- A perplexity of 20 means the model is "as confused as if choosing among 20 equally likely tokens"
- Lower is better; only comparable across models on the exact same tokenization

---
## Cross-Entropy and Bits-per-Character

- Cross-entropy in nats is just the average negative log-likelihood
- Convert to bits by dividing by `ln(2)` — bits-per-token
- Bits-per-character normalizes by characters, not tokens — fair across tokenizers
- The two units are interchangeable; pick whichever is conventional in your subfield

---
## Why Tokenization Affects Perplexity

- Perplexity is per-token; smaller tokens mean more tokens per sentence
- A character-level model and a `BPE` model cannot be compared by perplexity directly
- Bits-per-character was invented to make these comparisons fair
- When in doubt, report both perplexity and bits-per-character

---
## Intrinsic vs Extrinsic Evaluation

- Intrinsic: how well the model fits text it has not seen — perplexity
- Extrinsic: how well it does on a real downstream task — accuracy, F1, BLEU
- Lower perplexity often correlates with better downstream performance — but not always
- For deployed systems, extrinsic numbers are what matter

---
## Downstream Task Evaluation

- Question answering, summarization, classification, translation, code generation
- Standard benchmarks: `GLUE`, `SuperGLUE`, `MMLU`, `HellaSwag`, `HumanEval`
- Each benchmark probes a different ability — none of them measure "intelligence"
- Always look at multiple benchmarks before drawing a conclusion about a model

---
## Computing Perplexity

```python
def perplexity(model, ids):
    logits = model(ids[:, :-1])
    targets = ids[:, 1:]
    loss = F.cross_entropy(
        logits.reshape(-1, logits.size(-1)),
        targets.reshape(-1),
    )
    return torch.exp(loss)
```

- Standard cross-entropy loss, then exponentiate
- Make sure the loss does not include padding or special tokens

---
## Common Evaluation Pitfalls

- Reporting perplexity across different tokenizers — not comparable
- Evaluating on data the model saw during pretraining — leakage inflates numbers
- Single-benchmark optimization — the model overfits to that benchmark
- Comparing models trained on different amounts of data without saying so

---
## When n-gram Models Still Make Sense

- Edge devices with no GPU and tight latency budgets
- Strict interpretability requirements — counts you can audit
- As features in larger systems (e.g., reranking, anomaly detection)
- As baselines — if a neural model does not beat Kneser-Ney, something is wrong

---
## Anti-Patterns

- Treating perplexity as the only signal — it misses many failure modes
- Comparing perplexities across tokenizations
- Smoothing parameters tuned on the test set
- Reporting downstream numbers without held-out evaluation

---
## Summary

- A language model is a distribution over sequences; everything else follows
- `n-gram` models are simple, sparse, and limited; smoothing and back-off mitigate but do not solve
- Neural LMs share strength via embeddings; transformers replaced recurrence at scale
- Causal and masked are two faces of the same architecture, suited to different uses
- Evaluate with perplexity intrinsically and downstream tasks extrinsically — and never confuse the two
