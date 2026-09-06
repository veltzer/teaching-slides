---
tags:
  - data-and-ai:nlp
  - concepts:deep-learning
level: advanced
category: ai
audience:
  - audiences:developers
  - audiences:data-scientists

---

# Sequence Models: RNN, LSTM, GRU

---

## What This Chapter Covers

- Why sequences need architectures different from feed-forward networks
- Recurrent Neural Networks: math, training via `BPTT`, the gradient problem
- `LSTM` cells and the gating mechanism that mitigates vanishing gradients
- `GRU` as a leaner alternative — what it gains, what it gives up
- Bidirectional models and encoder-decoder framing as a bridge to attention

---

## Why Sequences Need Special Architectures

- Inputs are variable in length — sentences, documents, conversations
- Order matters — `dog bites man` is not `man bites dog`
- Information must flow over time — earlier tokens condition later predictions
- A fixed-size feed-forward window cannot capture arbitrary context

---

## The Failure of Feed-Forward Models on Sequences

- Padding to a fixed length wastes compute on short inputs and truncates long ones
- Position-by-position parameters explode the parameter count
- No reuse of structure across positions — `cat` learned at position 3 is useless at position 7
- Recurrence solves all three problems with a single mechanism: parameter sharing across time

---

## The Recurrent Idea

- One small network is applied repeatedly along the sequence
- It carries a hidden state forward — a running summary of what it has seen
- The same weights are used at every step — translation invariance in time
- The output at step `t` depends on every input from `1` to `t`

---

## RNN Math Formulation

- `h_t = tanh(W_xh x_t + W_hh h_{t-1} + b_h)` — hidden state update
- `y_t = W_hy h_t + b_y` — output projection at step `t`
- Three weight matrices, shared across all time steps
- The initial hidden state `h_0` is usually a zero vector or a learned parameter

---

## RNN Cell Unrolled

![rnn_unroll](svg/courses/ai/natural-language-processing/07_sequence_models/rnn_unroll.svg)

---

## A Minimal RNN in Code

```python
class SimpleRNN(nn.Module):
    def __init__(self, vocab, dim):
        super().__init__()
        self.embed = nn.Embedding(vocab, dim)
        self.W_xh = nn.Linear(dim, dim)
        self.W_hh = nn.Linear(dim, dim, bias=False)

    def forward(self, ids):
        h = torch.zeros(ids.size(0), self.W_hh.out_features)
        for t in range(ids.size(1)):
            x = self.embed(ids[:, t])
            h = torch.tanh(self.W_xh(x) + self.W_hh(h))
        return h
```

- The loop is the recurrence — one cell, applied at every time step

---

## Backpropagation Through Time

- Unroll the recurrence into a deep computation graph — one layer per time step
- Apply standard backprop through that unrolled graph
- Gradients flow from later steps back through every earlier step
- This is `BPTT` — backpropagation through time

---

## Truncated BPTT

- Full `BPTT` over a 1000-token sequence is a 1000-deep network in disguise
- Memory and compute scale with sequence length
- Truncated `BPTT` cuts the graph every `k` steps and detaches the gradient
- A trade-off: shorter gradients are faster and more stable, but lose long-range learning signal

---

## The Vanishing Gradient Problem

- Repeated multiplication by the recurrent weight matrix `W_hh` shrinks gradients exponentially
- After 50 steps, the gradient magnitude can be effectively zero
- The network simply cannot learn dependencies more than a handful of steps apart
- This is the core reason vanilla `RNN` models do not work on real-world sequences

---

## The Exploding Gradient Problem

- The same multiplication can also amplify gradients exponentially
- Loss spikes to `NaN` after a few updates — training diverges
- The standard fix is gradient clipping: rescale the gradient when its norm exceeds a threshold
- Cheap, effective, and almost always enabled when training any recurrent network

---

## Why Vanilla RNN Models Fail

- Long-range dependencies are common in language — subject and verb separated by many words
- Sentiment of a paragraph depends on tokens far from the end
- Vanilla `RNN` models forget what they saw 20 steps ago, no matter how important
- We need a cell that decides what to remember, not one that mixes everything together

---

## The LSTM Idea

- Add a separate cell state that flows along the sequence with minimal interference
- Use gates — small neural networks producing values in `[0, 1]` — to control flow
- Information can be written, kept, or erased deliberately at each step
- Gradients flow along the cell state with far less attenuation than through `tanh` repeatedly

---

## LSTM Cell Internals

![lstm_cell](svg/courses/ai/natural-language-processing/07_sequence_models/lstm_cell.svg)

---

## LSTM Equations

- Forget gate: `f_t = sigma(W_f [h_{t-1}, x_t] + b_f)`
- Input gate: `i_t = sigma(W_i [h_{t-1}, x_t] + b_i)`
- Candidate: `g_t = tanh(W_g [h_{t-1}, x_t] + b_g)`
- Cell state: `c_t = f_t * c_{t-1} + i_t * g_t`
- Output gate: `o_t = sigma(W_o [h_{t-1}, x_t] + b_o)`, then `h_t = o_t * tanh(c_t)`

---

## Cell State vs Hidden State

- The cell state `c_t` is the long-term memory — it is the highway that runs through time
- The hidden state `h_t` is the gated view of the cell state — what the network exposes at each step
- Outputs and downstream layers see `h_t`, not `c_t`
- The cell state is read and written through gates; it is not directly produced as output

---

## Why LSTM Mitigates Vanishing Gradients

- Cell state updates are additive: `c_t = f_t * c_{t-1} + i_t * g_t`
- When the forget gate stays near `1`, gradients propagate along the cell state nearly unchanged
- This is the "constant error carousel" — a path along which gradients neither vanish nor explode
- Multiplicative gates instead of dense matrix products at every step

---

## A Small LSTM in PyTorch

```python
class LstmTagger(nn.Module):
    def __init__(self, vocab, dim, n_tags):
        super().__init__()
        self.embed = nn.Embedding(vocab, dim)
        self.lstm = nn.LSTM(dim, dim, batch_first=True)
        self.head = nn.Linear(dim, n_tags)

    def forward(self, ids):
        x = self.embed(ids)
        h, _ = self.lstm(x)
        return self.head(h)
```

- The framework hides the gates; the equations are the same as on the previous slide

---

## The GRU

- Gated recurrent unit — a streamlined cell with two gates instead of three
- Update gate `z_t` blends old hidden state with a new candidate
- Reset gate `r_t` decides how much of the old state contributes to the candidate
- No separate cell state — `GRU` keeps a single hidden state

---

## GRU Equations

- Reset gate: `r_t = sigma(W_r [h_{t-1}, x_t])`
- Update gate: `z_t = sigma(W_z [h_{t-1}, x_t])`
- Candidate: `h_tilde = tanh(W [r_t * h_{t-1}, x_t])`
- New state: `h_t = (1 - z_t) * h_{t-1} + z_t * h_tilde`

---

## GRU vs LSTM

![gru_vs_lstm](svg/courses/ai/natural-language-processing/07_sequence_models/gru_vs_lstm.svg)

---

## GRU vs LSTM Empirically

- `GRU` has fewer parameters — about 75 percent of an `LSTM` at the same hidden size
- Trains slightly faster and uses less memory
- On most tasks the two are within noise; choice is often dictated by convention
- `LSTM` tends to win when very long-range dependencies dominate; `GRU` is fine elsewhere

---

## Stacking and Dropout

- Multiple recurrent layers stacked vertically — output of one feeds input of the next
- Two to four layers is typical; more rarely helps and often hurts
- Dropout between layers, not within the recurrence — disturbing the recurrent path hurts
- Variational dropout fixes the mask along the time axis to be safer for recurrent paths

---

## The Problem With One-Directional Models

- A vanilla `RNN`, `LSTM`, or `GRU` only sees the past
- For tagging or classification, the future of the sequence is also informative
- "Bank" in `I sat on the bank` is disambiguated by `river` two tokens later
- We want representations that combine left and right context

---

## Bidirectional Models

- Run one recurrent network forward, another backward
- Concatenate the two hidden states at each position
- Each output now sees the entire sequence — past and future
- Standard for tagging, parsing, and any task without a generative left-to-right constraint

---

## BiLSTM Architecture

![bilstm](svg/courses/ai/natural-language-processing/07_sequence_models/bilstm.svg)

---

## BiLSTM Use Cases

- Named entity recognition — labels depend on right context
- Part-of-speech tagging — `book` as noun or verb depends on surrounding words
- Sentence classification — pool over both directions for a stronger summary
- Reading comprehension — every span benefits from full-sentence context

---

## BiLSTM Limitations

- Not usable for autoregressive generation — the future leaks into the prediction
- Doubles the parameter count and the inference cost
- Still sequential along each direction — no parallelism along the time axis
- Long-range dependencies still attenuate, just from both ends now

---

## Encoder-Decoder Architectures

- Two recurrent networks: an encoder that reads input, a decoder that writes output
- Used for tasks where input and output sequences differ in length and alignment
- Translation, summarization, dialogue — the canonical seq2seq setup
- The encoder produces a single context vector handed to the decoder

---

## Seq2Seq Framing

- Encoder runs over the source: `h_1, h_2, ..., h_T`
- Final hidden state `h_T` becomes the initial state of the decoder
- Decoder generates the target one token at a time, conditioned on its own past
- Trained by teacher forcing — feed the true previous target token at each step during training

---

## A Tiny Seq2Seq in PyTorch

```python
class Seq2Seq(nn.Module):
    def __init__(self, src_vocab, tgt_vocab, dim):
        super().__init__()
        self.src_embed = nn.Embedding(src_vocab, dim)
        self.tgt_embed = nn.Embedding(tgt_vocab, dim)
        self.encoder = nn.LSTM(dim, dim, batch_first=True)
        self.decoder = nn.LSTM(dim, dim, batch_first=True)
        self.head = nn.Linear(dim, tgt_vocab)

    def forward(self, src_ids, tgt_ids):
        _, state = self.encoder(self.src_embed(src_ids))
        out, _ = self.decoder(self.tgt_embed(tgt_ids), state)
        return self.head(out)
```

---

## The Bottleneck Problem

- The entire source sentence is squeezed into a single fixed-size context vector
- Long sentences lose detail — the decoder cannot recover what the encoder dropped
- Performance degrades sharply as input length grows
- This was the practical ceiling of seq2seq before attention

---

## The Setup For Attention

- The decoder needs access to every encoder hidden state, not just the final one
- It should be able to look back selectively — focus on the source positions relevant to the next output token
- That selective look is attention — coming up next chapter
- Recurrence carried us this far; attention is what removed the bottleneck

---

## Common Anti-Patterns

- Forgetting gradient clipping — exploding gradients quietly nuke training
- Using dropout on the recurrent path itself — kills the long-range signal
- Bidirectional models for autoregressive generation — leaks the future into the present
- Treating cell state as the model's output — clients should see the gated hidden state

---

## When to Use RNN-Family Models Today

- Edge devices where transformers do not fit
- Streaming inputs with strict per-step latency requirements
- Tiny problems where a transformer would be overkill
- Pedagogically — every modern architecture is easier to understand after seeing recurrence

---

## Summary

- Sequences demand parameter sharing across positions — recurrence delivers it cleanly
- Vanilla `RNN` cells suffer from vanishing and exploding gradients on long sequences
- `LSTM` and `GRU` cells use gating to make long-range learning feasible
- Bidirectional models combine left and right context for non-generative tasks
- Encoder-decoder architectures hit a bottleneck that motivated attention — the next chapter
