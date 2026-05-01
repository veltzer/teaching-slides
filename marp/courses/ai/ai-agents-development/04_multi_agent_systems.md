---
tags:
  - data-and-ai:llm
level: advanced
category: machine-learning
audience:
  - audiences:developers

---
# Multi-Agent Systems

---
## What This Chapter Covers

- Why multi-agent
- Roles and specialization
- Communication
- Orchestration
- Pitfalls

---
## Why More Than One Agent

- Specialization beats generalization
- Smaller prompts per agent
- Parallel execution
- Cleaner audit trail

---
## Roles

- Planner
- Researcher
- Writer
- Reviewer
- Each with its own prompt and tools

---
## Specialization

- Narrow tools per role
- Narrow system prompt
- Easier to evaluate
- Easier to swap models

---
## Orchestration Patterns

- Supervisor delegates
- Pipeline passes outputs
- Debate compares answers
- Swarm shares scratchpad

---
## Supervisor Pattern

- One agent routes work
- Workers report back
- Supervisor decides next step
- Maps to org chart

---
## Pipeline Pattern

- Fixed sequence of agents
- Each transforms input
- Predictable cost
- Easy to test stages

---
## Debate Pattern

- Two agents argue a question
- Third agent judges
- Reduces single-model bias
- Expensive but robust

---
## Communication

- Structured messages
- Avoid free-form chatter
- Pass artifacts not transcripts
- Version the schema

---
## Shared Memory

- Vector store for facts
- Key-value for state
- Tag entries by author
- Garbage-collect old entries

---
## Failure Isolation

- One bad agent must not poison others
- Validate handoffs
- Time-box each call
- Fall back to single-agent path

---
## Cost Control

- More agents = more tokens
- Budget per task
- Cache common sub-results
- Use small models where possible

---
## Common Multi-Agent Mistakes

- Adding agents instead of fixing prompts
- Free-form chatter between agents
- No global iteration cap
- No traceability
- Hidden infinite loops
