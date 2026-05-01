---
tags:
  - data-and-ai:llm
level: advanced
category: machine-learning
audience:
  - audiences:developers

---
# Planning and Reasoning

---
## What This Chapter Covers

- Planning approaches
- ReAct in depth
- Plan-and-execute
- Reflection
- Trade-offs

---
## Why Planning

- Multi-step goals
- Branching decisions
- Recoverable failures
- Cheaper than brute-force loops

---
## ReAct

- Thought, action, observation
- Each step in chat history
- Model sees full trajectory
- Simple to implement

---
## ReAct Trade-offs

- Easy to start with
- Burns tokens fast
- Long traces drift
- Harder to debug

---
## Plan-and-Execute

- LLM emits a plan first
- Executor runs each step
- Cheaper steps without LLM
- Re-plans on failure

---
## Reflection

- After acting, model critiques
- Detects mistakes
- Generates corrected step
- Adds tokens but reduces errors

---
## Tree of Thoughts

- Explore multiple branches
- Score each path
- Backtrack when stuck
- Expensive but powerful

---
## Self-Consistency

- Sample multiple traces
- Vote on the answer
- Reduces hallucination
- More tokens, more confidence

---
## When to Use Which

- Simple goals: ReAct
- Predictable workflows: plan-and-execute
- High-stakes: reflection or voting
- Hard problems: tree of thoughts

---
## Stopping Conditions

- Goal met by tool result
- Max iterations
- Cost ceiling
- User cancels

---
## Long-Horizon Tasks

- Break into sub-goals
- Each sub-goal a fresh agent
- Pass state explicitly
- Avoid context bloat

---
## Debugging Plans

- Log every thought
- Inspect failure points
- Replay traces
- Add asserts mid-loop

---
## Common Planning Mistakes

- No iteration cap
- Plan never re-evaluated
- Ignoring tool errors
- Mixing planner and executor concerns
- Treating LLM plans as authoritative
