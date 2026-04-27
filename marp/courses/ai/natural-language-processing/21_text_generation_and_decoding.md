---
tags:
  - data-and-ai:nlp
  - data-and-ai:llm
  - concepts:text-generation
level: advanced
category: ai
audience:
  - audiences:developers
  - audiences:data-scientists

---
# Text Generation and Decoding

---
## What This Chapter Covers

- The decoding step that turns a language model into a text generator
- Greedy and beam search and where each fails
- Sampling strategies: temperature, top-k, top-p, typical sampling
- Constrained decoding and how to bend a model to a schema
- Speculative decoding and other speed tricks
- Evaluating generated text when there is no single right answer

---
## Why Decoding Matters

- A trained model gives us probabilities; decoding turns them into text
- Two systems with the same weights produce very different output by changing decoder
- The decoder is the cheapest knob between you and the user-facing behavior
- Often more impactful in practice than swapping models
- Also where the most surprising and frustrating failures hide

---
## The Generation Loop

- The model emits a probability distribution over the next token
- The decoder picks one token, appends it to the prompt, and repeats
- Stops on an end-of-sequence token, max length, or external rule
- Every choice during the picking step is the decoder's job
- Modern serving stacks intermix decoding with caching and batching

---
## Decoding Strategies Overview

![decoding_strategies](svg/courses/ai/natural-language-processing/21_text_generation_and_decoding/decoding_strategies.svg)

---
## Greedy Decoding

- Pick the most probable next token at every step
- Cheap, deterministic, and often produces decent output
- Locally optimal — globally weak when the right choice is not most probable now
- Tends to repeat itself on open-ended generation
- A fine baseline for short structured outputs

---
## Beam Search

- Maintain a beam of `k` partial sequences and extend each step
- Score with the cumulative log probability
- Length penalty prevents the model from preferring short sequences
- Standard for `MT` and structured generation
- Bland and repetitive on open-ended creative tasks

---
## When Beam Search Goes Wrong

- Repetitive output: `the dog the dog the dog`
- Beam search collapses on the safest continuation
- A high-probability sequence is not always a good one
- For open-ended generation, sampling beats beam by a lot
- For closed-ended generation, beam still wins on average

---
## Temperature Sampling

- Divide logits by `T` before softmax
- `T < 1` sharpens the distribution; `T > 1` flattens it
- `T = 0` is mathematically greedy
- The single most useful knob in production decoding
- A starting point for almost every other sampling method

---
## Top-K Sampling

- Sample from the top `K` most probable tokens after renormalizing
- Truncates the long tail that often contains noise
- `K` between 20 and 50 is a typical default
- Easier to reason about than pure temperature sampling
- Loses information when the top-K is dominated by one token

---
## Top-P (Nucleus) Sampling

- Sample from the smallest set of tokens whose cumulative probability exceeds `p`
- Adapts the candidate set to the local distribution
- `p` around 0.9 is a typical default
- Generally outperforms top-K on open-ended generation
- The default in many `LLM` APIs

---
## Typical Sampling

- Sample tokens whose information content is closest to the entropy of the distribution
- Avoids both very predictable and very surprising tokens
- Less common in practice but worth knowing
- Useful when top-p produces too-bland or too-erratic output
- A diagnostic option more than a default

---
## Sampling Distributions Compared

![sampling_distributions](svg/courses/ai/natural-language-processing/21_text_generation_and_decoding/sampling_distributions.svg)

---
## Repetition Penalties

- Discount tokens that appear in the recent context
- Frequency penalty: scale by token count in the prompt
- Presence penalty: flat discount for any token that has appeared
- Hides degenerate behavior more than it cures it
- Useful, but a red flag if you need them just to make output readable

---
## Stop Sequences and EOS

- The decoder stops when it emits an end-of-sequence token
- Custom stop sequences let you cut on user-defined boundaries
- Critical for structured output where the model must stop on `}` or `</answer>`
- Easy to forget and a common source of runaway generations
- Always set a max-tokens cap as a safety net

---
## Constrained Decoding

- Restrict the candidate tokens to those allowed by a grammar or schema
- Forces the model to produce valid `JSON`, `SQL`, or domain-specific syntax
- Implemented by zeroing out logits of illegal tokens before sampling
- `outlines`, `guidance`, and `lm-format-enforcer` are popular toolkits
- Higher quality structured output than prompt-only approaches

---
## JSON-Constrained Decoding

```python
import outlines

schema = """{"name": "string", "age": "integer"}"""
generator = outlines.generate.json(model, schema)
result = generator("Generate a person record.")
# result is guaranteed to be valid JSON matching the schema
```

- Schema enforcement at decode time, not as a post-hoc parser
- Especially useful for tool calls and structured extraction
- Essentially free to add when the model is a local one

---
## Logit Biases

- Force or suppress specific tokens by adding to their logits
- Push the model toward or away from particular vocabulary
- Useful for branding, safety lists, and domain language
- A blunt instrument; overuse breaks fluency
- Pair with sampling strategies, not greedy decoding

---
## Speculative Decoding

- A small draft model proposes several tokens at once
- The main model verifies them in a single forward pass
- Accept the longest prefix that the main model agrees with
- Output is identical to vanilla decoding but throughput is higher
- Standard in latency-sensitive `LLM` serving

---
## Speculative Decoding Diagram

![speculative_decoding](svg/courses/ai/natural-language-processing/21_text_generation_and_decoding/speculative_decoding.svg)

---
## Streaming Output

- Send tokens to the user as they are decoded
- Latency-to-first-token matters more than total time on long outputs
- `SSE` and `WebSocket` are typical transport choices
- Most production `LLM` UIs stream by default
- Streaming changes the shape of error handling — partial outputs visible

---
## Batching at Inference

- Multiple requests share one forward pass for speedup
- Continuous batching adds new requests as old ones finish
- `vLLM` and `TGI` implement modern continuous batching
- Doubles or triples throughput at fixed latency
- The single biggest cost lever for self-hosted `LLM` services

---
## Caching at Inference

- KV cache reuses attention keys and values across decode steps
- Prompt cache shares prefixes across requests with shared system prompts
- Speculative cache and paged attention extend this further
- Memory becomes the bottleneck before compute on most modern GPUs
- Knowing what is cached and what is recomputed is part of operating an `LLM`

---
## Decoding for Different Tasks

- Translation: beam search, length-penalty 1.0, beam 4-6
- Summarization: beam or low-temperature sampling
- Code generation: low temperature, sometimes greedy with constraints
- Creative writing: high temperature with top-p
- Structured extraction: constrained decoding with grammars

---
## Evaluating Generated Text

- Reference-based: `BLEU`, `ROUGE`, `BERTScore`, `chrF`
- Reference-free: perplexity, fluency classifiers, `LLM`-as-judge
- Human preference rating remains the gold standard
- Pick metrics that match what the user actually cares about
- Multiple metrics catch different failure modes

---
## Hallucination Under Different Decoders

- Greedy and low-temperature sampling reduce hallucination but reduce variety
- High-temperature sampling and large top-k increase invention
- Constrained decoding hard-blocks structural hallucination
- Retrieval grounding addresses factual hallucination
- The decoder alone cannot solve a model's prior beliefs

---
## Production Decoding Patterns

- Per-task default: temperature 0 for tools, 0.7 for chat
- Stop sequences set per consumer of the output
- Max tokens that match the actual budget, not a default
- Streaming when latency matters
- Logging the decoder configuration alongside the output

---
## Common Production Pitfalls

- Forgetting to set max tokens and burning a budget on a runaway response
- Beam search on creative tasks producing repetitive bland output
- Top-p with a tiny `p` collapsing to greedy behavior
- Constrained decoding without testing the grammar end-to-end
- Logit biases that distort calibration on benchmarks

---
## Anti-Patterns

- One temperature for every task in a system
- Using greedy decoding for creative writing
- Skipping streaming on user-facing chat
- Treating the decoder as a fixed property of the model
- Reporting evaluation numbers without disclosing the decoding setup

---
## Summary

- Decoding bridges probabilities and text and dominates output quality
- Greedy and beam are good defaults for closed tasks; sampling for open ones
- Top-p and temperature together cover most real-world needs
- Constrained decoding is the cheap way to reliable structured output
- Speculative decoding and continuous batching are the speed levers in production
