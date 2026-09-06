---
tags:
  - data-and-ai:llm
level: intermediate
category: machine-learning
audience:
  - audiences:developers

---

# Introduction to Prompt Engineering

---

## What This Chapter Covers

- What prompt engineering is
- Why it matters
- LLMs basics
- Tokens and context windows
- Roles in conversations
- Course outline

---

## What Prompt Engineering Is

- Designing inputs that produce desired outputs
- Skill for using LLMs effectively
- Less software, more linguistics
- Empirical, iterative

---

## What Goes In a Prompt

![prompt_basics](svg/courses/ai/prompt-engineering/01_introduction/prompt_basics.svg)

---

## Why It Matters

- Same model, different prompts: vastly different results
- Production systems live or die by prompts
- Cheaper than fine-tuning
- Faster than retraining

---

## LLMs in 60 Seconds

- Trained on massive text
- Predict next token given context
- Context window: how much it remembers
- Stochastic: same prompt, different output

---

## Tokens

- Smaller than words
- "Hello world" = 2 tokens
- Cost and limits in tokens
- Different tokeniser per model

---

## Context Window

- Hard limit on input + output
- 4K, 32K, 128K, 1M tokens depending on model
- Larger window is not free
- Use wisely

---

## System, User, Assistant

- system: behaviour and role
- user: human input
- assistant: model output
- Standard chat format

---

## Sample Conversation

- System: "You are a helpful coding assistant"
- User: "Write a Python factorial function"
- Assistant: code response

---

## Determinism

- Temperature 0: most likely token
- Higher temperature: more variety
- Production: low temperature
- Creative: high temperature

---

## Output Variability

- Same prompt may give different results
- Test with multiple runs
- Pin model versions
- Beware of API drift

---

## Course Outline

- Prompt patterns
- Chain of thought
- Few-shot examples
- Tool use
- Evaluation
- Production patterns

---

## Common Introduction Mistakes

- Treating LLMs as deterministic
- One-shot prompts without iteration
- Not testing edge cases
- Ignoring token costs
- Confusing prompt skill with model intelligence
