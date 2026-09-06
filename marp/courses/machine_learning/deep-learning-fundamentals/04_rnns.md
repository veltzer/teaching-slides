---
tags:
  - data-and-ai:deep-learning
level: intermediate
category: machine-learning
audience:
  - audiences:developers
  - audiences:data-scientists

---

# Recurrent Neural Networks

---

## What This Chapter Covers

- Sequence modeling fundamentals
- Vanilla RNNs and the vanishing gradient problem
- LSTM and GRU architectures
- Sequence-to-sequence models
- Applications in text and time series

---

## What Is a Sequence

- Ordered data where order matters
- Text: word after word
- Audio: samples over time
- Sensor readings, stock prices, video

---

## Why Not a Feedforward Net

- Inputs can be variable length
- Order carries meaning
- The same word can shift the whole sentence
- We need memory of what came before

---

## The RNN Idea

- Process one element at a time
- Carry a hidden state between steps
- Reuse the same weights every step
- Hidden state summarizes the past

---

## The Recurrent Cell

![rnn_cell](svg/courses/machine_learning/deep-learning-fundamentals/04_rnns/rnn_cell.svg)

---

## Unrolling Through Time

- Same cell applied at each step
- Conceptually, a very deep feedforward net
- Each layer is one time step
- Weights are tied across layers

---

## RNN Math

- h_t = tanh(W_h h_{t-1} + W_x x_t + b)
- y_t = W_y h_t + b_y
- One set of weights for all steps
- Updated by backprop through time

---

## Backprop Through Time

- Unroll the RNN
- Apply backprop on the unrolled graph
- Gradients flow back through every step
- Memory cost grows with sequence length

---

## Truncated BPTT

- Only backprop a fixed number of steps
- Caps memory and compute
- Limits long-range learning
- Common practical compromise

---

## Vanishing Gradients

- Repeated multiplication shrinks gradients
- Early steps barely update
- Long-range dependencies are forgotten
- The main weakness of vanilla RNNs

---

## Exploding Gradients

- Same product, but blowing up
- Weights jump to nonsense
- Detect with gradient norm
- Fix with gradient clipping

---

## Gradient Clipping

- If gradient norm > threshold, scale it down
- Cheap and effective
- Often required for stable RNN training
- One line in modern frameworks

---

## LSTM

- Long Short-Term Memory
- Hochreiter and Schmidhuber, 1997
- Adds a cell state with gated updates
- Designed to preserve long-range information

---

## LSTM Gates Visualized

![lstm gates](svg/courses/machine_learning/deep-learning-fundamentals/04_rnns/lstm_gates.svg)

---

## LSTM Cell

![lstm_cell](svg/courses/machine_learning/deep-learning-fundamentals/04_rnns/lstm_cell.svg)

---

## LSTM Gates

- Forget gate: what to drop from cell state
- Input gate: what new info to add
- Output gate: what to expose as h_t
- Each gate is a small sigmoid network

---

## Why LSTMs Work

- Cell state is mostly additive
- Gradients flow through it more cleanly
- Network learns when to remember and forget
- Long dependencies become tractable

---

## GRU

- Gated Recurrent Unit
- Cho et al, 2014
- Simpler than LSTM, two gates instead of three
- Often matches LSTM with fewer parameters

---

## LSTM vs GRU

- LSTM: more parameters, more expressive
- GRU: faster, easier to train on small data
- No clear winner across tasks
- Try both, keep the better one

---

## Bidirectional RNNs

- Run one RNN forward, another backward
- Concatenate hidden states
- Each step sees past and future
- Useful when full sequence is available

---

## Stacked RNNs

- Stack multiple RNN layers
- Output of one feeds into the next
- Higher layers learn more abstract patterns
- Diminishing returns past 2-3 layers

---

## RNN in Keras

```python
model = keras.Sequential([
    layers.Embedding(vocab_size, 128),
    layers.LSTM(64, return_sequences=True),
    layers.LSTM(32),
    layers.Dense(1, activation="sigmoid"),
])
```

---

## RNN in PyTorch

```python
class Tagger(nn.Module):
    def __init__(self, vocab, hidden, classes):
        super().__init__()
        self.emb = nn.Embedding(vocab, 128)
        self.rnn = nn.LSTM(128, hidden, batch_first=True)
        self.head = nn.Linear(hidden, classes)
    def forward(self, x):
        e = self.emb(x)
        h, _ = self.rnn(e)
        return self.head(h)
```

---

## Embeddings

- Map tokens to dense vectors
- Learned during training
- Similar words land near each other
- The entry point of any text model

---

## Sequence-to-Sequence

- Input sequence, output sequence
- Different lengths allowed
- Encoder reads input
- Decoder produces output

---

## Encoder-Decoder

![seq2seq](svg/courses/machine_learning/deep-learning-fundamentals/04_rnns/seq2seq.svg)

---

## Seq2Seq Training

- Encoder summarizes input into a state
- Decoder starts from that state
- Generates one token at a time
- Trained end to end on pairs

---

## Teacher Forcing

- During training, feed the true previous token
- Stabilizes early learning
- Mismatch with inference can hurt
- Sometimes mixed with sampled tokens

---

## Beam Search

- At inference, pick top-k partial outputs
- Expand each, keep the best k
- Better than greedy, slower than greedy
- Standard for translation and captioning

---

## The Bottleneck

- Encoder must squeeze input into one vector
- Long inputs lose detail
- This motivated the attention mechanism
- Discussed in the transformers chapter

---

## Text Classification

- Embed tokens, pass through RNN
- Use final state or pooled states
- Dense head for the label
- Sentiment, topic, spam, intent

---

## Sequence Labeling

- Predict a label per token
- Part-of-speech tagging, named entity recognition
- Use return_sequences in Keras
- Combine with a CRF for structured output

---

## Time Series Forecasting

- Input: past values (and features)
- Output: future values
- RNNs handle variable history naturally
- Compare to ARIMA and gradient boosted trees

---

## Sliding Windows

- Convert series into supervised pairs
- Window of past values to next value
- Stride controls overlap
- Same trick used for many sequence tasks

---

## Multivariate Series

- Multiple input channels per time step
- Same RNN handles them
- Concatenate features along the feature axis
- Watch for differing scales

---

## When Not to Use RNNs

- Very long sequences: prefer transformers
- Small ordered data: classical methods often win
- When parallelism matters: RNNs are sequential
- When pretrained transformers exist for your task

---

## Why Transformers Won

- Parallel across the sequence
- Attention captures long range directly
- Scales much better with hardware
- Pretrained checkpoints dominate

---

## Where RNNs Still Shine

- Streaming inference: low latency per step
- Small models on edge devices
- Short sequences with strict compute budgets
- Reinforcement learning agents

---

## Common Pitfalls

- Forgetting to mask padding tokens
- Batching by random order: pad inefficiency
- Using one-hot inputs instead of embeddings
- Letting sequence length blow up memory

---

## Practical Tips

- Start with a single-layer LSTM or GRU
- Always pack and pad sequences correctly
- Clip gradients from the first run
- Track per-step and per-example losses

---

## Summary

- RNNs share weights across time and carry hidden state
- Vanilla RNNs struggle with long ranges
- LSTM and GRU gate information to keep memory alive
- Seq2seq with RNNs introduced the encoder-decoder pattern
