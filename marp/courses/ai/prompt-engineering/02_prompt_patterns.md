---
tags:
  - data-and-ai:llm
level: intermediate
category: machine-learning
audience:
  - audiences:developers

---

# Prompt Patterns

---

## What This Chapter Covers

- Zero-shot
- Few-shot
- Role prompting
- Instruction following
- Format constraints
- Templates

---

## Chain-of-Thought

![cot_pattern](svg/courses/ai/prompt-engineering/02_prompt_patterns/cot_pattern.svg)

---

## Zero-Shot

- Just ask
- No examples
- Modern models do well at this
- Baseline approach

---

## Few-Shot

- Provide examples in the prompt
- Model learns the pattern
- 2-5 examples often enough
- Demonstrate the format

---

## Sample Few-Shot

- Q: 2+2 A: 4
- Q: 3+5 A: 8
- Q: 7+1 A: ?
- Model: 8

---

## Role Prompting

- "You are an expert Rust developer"
- Sets persona
- Influences vocabulary and depth
- Useful but not magical

---

## Common Patterns

![persona_template](svg/courses/ai/prompt-engineering/02_prompt_patterns/persona_template.svg)

---

## Instructions

- Be specific and explicit
- "Summarize in 3 bullets" beats "summarize"
- State the goal
- State the audience

---

## Format Constraints

- "Return JSON with keys: name, age, city"
- "Output only the SQL"
- Models follow format better than ever
- Validate output

---

## Delimiters

- ```triple backticks```
- Or: <tags>
- Separate instruction from data
- Reduces ambiguity

---

## Prompt Templates

- Reusable shape with placeholders
- Library: LangChain, others
- Or: just f-strings
- Versionable

---

## Chain of Thought

- "Let's think step by step"
- Or: built into the prompt
- Improves reasoning on math, logic
- Costs more tokens

---

## Self-Consistency

- Sample multiple completions
- Pick majority answer
- More compute, better accuracy
- For: critical reasoning

---

## Generated Knowledge

- Ask model for facts first
- Use those in main prompt
- Multi-step
- Costlier, sometimes better

---

## Common Pattern Mistakes

- Vague instructions
- No examples for unusual tasks
- Mixing instruction and data
- Format specified vaguely
- Templates with too many slots
