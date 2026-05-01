---
tags:
  - data-and-ai:llm
level: advanced
category: machine-learning
audience:
  - audiences:developers

---
# Introduction to AI Agents

---
## What This Chapter Covers

- What an AI agent is
- Agents vs chatbots
- Core components
- Agent loop
- Use cases

---
## What an Agent Is

- LLM with tools
- Reasons over a goal
- Plans, acts, observes
- Iterates until done

---
## Agent vs Chatbot

- Chatbot: single-turn reply
- Agent: multi-turn, multi-tool
- Chatbot reacts; agent acts
- Agents have goals, not just inputs

---
## Core Components

- Model (the LLM)
- Tools (functions it can call)
- Memory (state across turns)
- Planner (what to do next)

---
## The Agent Loop

- Receive goal
- Think (LLM call)
- Act (tool call)
- Observe (tool result)
- Repeat until goal met

---
## ReAct Pattern

- Reason + Act
- Interleave thought and action
- Each step grounded in observation
- Foundation for many agents

---
## Tool Calling

- LLM emits structured call
- Runtime executes tool
- Result fed back to LLM
- LLM decides next step

---
## Memory

- Short-term: conversation context
- Long-term: vector store
- Working memory: scratchpad
- Persistence across sessions

---
## Use Cases

- Code generation and review
- Customer support automation
- Research assistants
- Workflow automation

---
## Risks

- Tool calls can have side effects
- Hallucinated tool args
- Infinite loops
- Cost explosion

---
## What You Will Build

- Single-tool agent
- Multi-tool agent
- Multi-agent system
- Production-grade agent

---
## Common Beginner Mistakes

- Treating agents as deterministic
- No tool guardrails
- No iteration cap
- Ignoring cost
- Not logging steps
