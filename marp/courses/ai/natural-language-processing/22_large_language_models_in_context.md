---
tags:
  - data-and-ai:nlp
  - data-and-ai:llm
  - concepts:large-language-models
level: advanced
category: ai
audience:
  - audiences:developers
  - audiences:data-scientists

---

# Large Language Models in Context

---

## What This Chapter Covers

- The shape of modern `LLMs` and how they differ from earlier transformers
- Pretraining objectives and the data behind them
- Instruction tuning, `RLHF`, and the alignment toolchain
- Prompting, few-shot learning, and chain-of-thought reasoning
- Tool use, agents, and the orchestration layer
- Practical engineering: cost, latency, evaluation, safety

---

## Why a Separate Chapter

- `LLMs` reuse the transformer architecture but at a scale where new behaviors emerge
- The interface is no longer fine-tuning — it is prompting and tool use
- Engineering trade-offs shifted from training to inference and orchestration
- Evaluation, safety, and cost dominate over architecture choices
- The chapter that ties everything earlier into modern practice

---

## What Makes a Model Large

- Parameter count of billions to trillions
- Training corpora of trillions of tokens
- Context windows of thousands to millions of tokens
- Inference cost measured in dollars per query, not seconds
- Engineering intensity that requires entire infrastructure teams

---

## Scale and Emergence

- Some capabilities appear discontinuously above certain model sizes
- Few-shot in-context learning, code generation, coherent long generation
- Whether emergence is real or a metric artifact is debated
- Reliable engineering treats it as a smooth progression
- Understanding what scales and what does not is part of model selection

---

## Pretraining Objectives

- Most modern `LLMs` are causal: predict the next token
- Some use prefix language modeling for encoder-decoder variants
- Mixture-of-experts models route different tokens to different experts
- Multi-task pretraining mixes next-token prediction with denoising
- Objective choices matter at training but rarely affect downstream prompting

---

## Pretraining Data

- Web crawls (`CommonCrawl`, `C4`), books, code, scientific papers
- Curation matters enormously: dedup, quality filtering, toxicity removal
- Data mix decisions shape what the model is good at
- Coverage of languages, domains, and styles is unevenly distributed
- Where the data came from is increasingly a legal and ethical question

---

## Instruction Tuning

- Fine-tune on (instruction, response) pairs
- Teaches the model to follow user intent, not just complete text
- Datasets like `FLAN`, `Self-Instruct`, `OpenAssistant`
- Often the cheapest way to make a base model usable
- Where most "open" model variants pour effort

---

## RLHF and Preference Optimization

- Train a reward model on human preference comparisons
- Fine-tune the model with `PPO` or `DPO` against the reward
- Aligns outputs with human notions of helpfulness and safety
- Direct Preference Optimization simplified the loop and is now common
- The step that turns a competent base model into a useful product

---

## The Alignment Pipeline

![alignment_pipeline](svg/courses/ai/natural-language-processing/22_large_language_models_in_context/alignment_pipeline.svg)

---

## Prompting as Programming

- The prompt is the program, the model is the interpreter
- System prompt, user message, examples, and constraints together
- Small changes in phrasing produce large differences in output
- Reproducible prompting is harder than it sounds
- Treat prompts as versioned artifacts with tests

---

## Zero-Shot Prompting

- State the task and ask for the answer
- Works because instruction tuning teaches the model to follow instructions
- Sufficient for simple tasks: classification, paraphrase, summarization
- Sensitive to phrasing — try a few variants
- The starting point before adding examples or chains

---

## Few-Shot Prompting

- Include a handful of input-output examples in the prompt
- Demonstrates the desired format and reasoning style
- Works when the task is too quirky for zero-shot
- Strong for structured output where examples constrain the schema
- Cost: tokens spent on examples instead of user content

---

## Chain-of-Thought

- Ask the model to reason step by step before answering
- Improves performance on math, logic, and multi-step problems
- Self-consistency: sample several chains and majority-vote the answer
- Works because the model uses tokens as scratch space
- Increases cost and latency; pick when accuracy matters more

---

## Chain-of-Thought Patterns

![cot_patterns](svg/courses/ai/natural-language-processing/22_large_language_models_in_context/cot_patterns.svg)

---

## Self-Consistency

- Sample multiple reasoning chains with non-zero temperature
- Take the majority vote over the final answers
- Trades inference cost for accuracy
- Especially effective when the chains diverge but converge on the answer
- Default for high-stakes reasoning tasks

---

## Tool Use

- Let the model call external tools when it needs them
- Search, calculator, code execution, database query, API calls
- The model decides when, with what arguments, and how to combine results
- Tool descriptions are part of the prompt the model conditions on
- The bridge from a closed-world chatbot to an open-world agent

---

## Function Calling Interfaces

- Structured tool descriptions in `JSON` schema
- Model emits a `JSON` object naming the function and arguments
- The application parses and executes the call, returns the result
- Implemented in OpenAI, Anthropic, Google, and most modern `LLM` APIs
- Cleanly separates model output from system actions

---

## A Function-Calling Trace

```misc
user: What is the weather in Paris tomorrow?
assistant -> tool: {"name": "get_weather",
                    "args": {"city": "Paris", "date": "2026-04-28"}}
tool -> assistant: {"high_c": 17, "low_c": 9, "rain_pct": 60}
assistant -> user: Tomorrow in Paris should be 9-17 C with a 60% chance of rain.
```

- Two model turns separated by a real-world tool call
- The orchestrator validates inputs, runs the tool, and feeds results back

---

## Agents

- A loop where the model decides actions until a goal is achieved
- `ReAct`: alternate reasoning and tool calls
- Memory across steps is held in the conversation or a scratchpad
- Long horizons are still hard; cost grows with steps
- The frontier of practical `LLM` deployment

---

## Agent Architectures

![agent_architecture](svg/courses/ai/natural-language-processing/22_large_language_models_in_context/agent_architecture.svg)

---

## Memory Systems

- Short-term: the conversation window the model sees
- Long-term: external store (vector DB, summaries, episodic memory)
- Retrieval pulls relevant memories into the prompt as needed
- Forgetting matters — unbounded memory degrades retrieval
- Memory architecture is product-specific, not model-specific

---

## Context Window Engineering

- Where a piece of information lives in the prompt affects how the model uses it
- "Lost-in-the-middle" — long contexts often miss content near the middle
- System prompts at the start, user query at the end is the safest layout
- Retrieval results closer to the query token are weighted more heavily
- Test the layout, do not assume the model attends uniformly

---

## In-Context Learning Limits

- The model does not actually learn from examples; it pattern-matches
- Failure modes: bias toward the majority class, format drift, ignoring examples
- Few-shot performance plateaus quickly with more examples
- Calibrated few-shot evaluation is harder than it looks
- For many production tasks, fine-tuning still wins

---

## Fine-Tuning vs Prompting

- Prompting wins on speed of iteration and zero training data
- Fine-tuning wins on cost per query and consistency
- LoRA and `QLoRA` made fine-tuning cheap on commodity GPUs
- Hybrid: fine-tune for behavior, prompt for context
- The decision is task-dependent, not a one-time global choice

---

## Cost and Latency

- Token-based pricing rewards prompt compression and structured outputs
- Latency-to-first-token matters for chat; total time matters for batch
- Caching prompts and outputs can cut cost an order of magnitude
- Speculative decoding and continuous batching drive serving efficiency
- Cost is the constraint that defines what is shippable

---

## Safety and Guardrails

- Red-teaming surfaces unsafe outputs before users do
- Input filters block prompt injection and policy violations
- Output filters catch refusal failures and policy slips
- Tool sandboxing limits damage from autonomous actions
- Layered safety beats any single filter

---

## Prompt Injection

- Adversarial input embedded in retrieved documents or user content
- Can override system instructions and exfiltrate data
- A real and growing risk in `RAG` and tool-using agents
- Hard problem: there is no perfect defense yet
- Treat retrieved content as untrusted user input

---

## Evaluation at Scale

- Human preference rating remains the gold standard for chat quality
- `LLM`-as-judge approximates human eval at lower cost
- Task-specific benchmarks: `MMLU`, `HumanEval`, `BIG-bench`
- Holistic evaluation across capability, safety, latency, and cost
- No single benchmark captures real-world fitness

---

## When to Use What

- Closed task with stable schema: fine-tuned smaller model
- Open-ended chat: instruction-tuned `LLM`
- Knowledge-grounded QA: `RAG` over instruction-tuned `LLM`
- Multi-step task with tool use: agent loop on a strong base model
- Cost-bound batch processing: fine-tuned mid-size model

---

## Common Production Pitfalls

- Treating prompts as throwaway code rather than versioned artifacts
- Ignoring cost until the bill arrives
- Skipping evaluation outside the training distribution
- Not handling tool errors or model refusals gracefully
- Testing on benchmarks that no longer reflect the deployed task

---

## Anti-Patterns

- Believing prompts that work today will work after the next model release
- Treating an `LLM` as a calculator without tool use for arithmetic
- Long-running agent loops with no budget caps
- Open prompts on user-supplied content without injection defenses
- Promising capabilities the model cannot actually deliver

---

## Summary

- Modern `LLMs` are transformers at a scale where the interface changed
- Pretraining + instruction tuning + `RLHF` is the alignment recipe
- Prompting and tool use replaced fine-tuning as the default interaction
- Agents extend `LLMs` into multi-step problem solving
- Engineering practice now lives at the orchestration and safety layer
