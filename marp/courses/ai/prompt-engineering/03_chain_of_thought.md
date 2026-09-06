---
tags:
  - data-and-ai:llm
level: intermediate
category: machine-learning
audience:
  - audiences:developers

---

# Chain of Thought

---

## Variants

![cot_variants](svg/courses/ai/prompt-engineering/03_chain_of_thought/cot_variants.svg)

---

## What This Chapter Covers

- Reasoning prompts
- Step by step
- Self-consistency
- Tree of thoughts
- Tradeoffs

---

## Why Reasoning Prompts

- LLMs answer math wrong if asked directly
- Asked to think step by step: much better
- Trades tokens for accuracy

---

## Sample Without CoT

- Q: 17 x 24
- A: 408
- Often wrong on harder problems

---

## Sample With CoT

- Q: 17 x 24
- A: 17 x 24 = 17 x 20 + 17 x 4 = 340 + 68 = 408
- Shows work; more accurate

---

## Triggering CoT

- Append "Let's think step by step"
- Or include reasoning in few-shot examples
- Or use system prompt
- Multiple ways

---

## When CoT Helps

- Math
- Multi-step logic
- Decisions with constraints
- Code understanding

---

## CoT Helps vs Hurts

![cot_when](svg/courses/ai/prompt-engineering/03_chain_of_thought/cot_when.svg)

---

## When It Hurts

- Simple lookups
- Wastes tokens
- Slows responses
- Don't blindly add

---

## Self-Consistency

- Generate multiple chains
- Pick most common answer
- Ensemble of one model
- Robust to single-chain errors

---

## Tree of Thoughts

- Explore multiple branches
- Score and prune
- For complex problems
- Higher cost

---

## ReAct

- Reason + Act
- Interleave thinking and tool calls
- Foundation of agents
- Covered in agents course

---

## Latency Cost

- More tokens out: slower
- Streaming hides some of this
- Decide per use case

---

## Hidden Reasoning

- Some models think internally
- Output: just the answer
- "Reasoning models" (o1, etc.)
- Different prompting style

---

## Common CoT Mistakes

- Asking for reasoning then ignoring it
- Long prompts that overflow context
- Mixing CoT and rigid format constraints
- Not validating the final answer
- Using CoT where lookups suffice
