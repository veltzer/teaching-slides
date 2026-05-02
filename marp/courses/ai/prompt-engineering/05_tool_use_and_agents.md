---
tags:
  - data-and-ai:llm
level: intermediate
category: machine-learning
audience:
  - audiences:developers

---
# Tool Use and Agents

---
## What This Chapter Covers

- Tool use overview
- Function calling
- ReAct loop
- Agents
- Multi-step tasks
- Limits

---
## What Tool Use Is

- LLM calls external functions
- Read files, search web, query DB
- Extends model beyond its training
- Foundation of agents

---
## Sample Flow

- User asks question
- Model decides: needs search tool
- Code runs search, returns results
- Model uses results to answer

---
## Function Calling

- Define tools with schemas
- Model picks tool + args
- Code executes; result back to model
- Loop until done

---
## ReAct

- Reason then Act
- Each step: think out loud, choose tool
- Returns observation
- Iterate

---
## Agent Loop

- 1. Read state and goal
- 1. Reason
- 1. Pick action (tool or reply)
- 1. Execute
- 1. Repeat until done

---
## Loop Visualised

![agent_loop](svg/courses/ai/prompt-engineering/05_tool_use_and_agents/agent_loop.svg)

---
## Tools to Provide

- Search: Google, internal docs
- Code execution: sandboxed Python
- File ops: read, write
- API calls: weather, stocks, services

---
## System Prompts for Agents

- Describe tools and when to use
- Limits and safety
- Output format
- Error handling expectations

---
## Multi-Step Tasks

- Plan first; act in steps
- Verify between steps
- Recover on errors
- Stop when done

---
## Limits

- Context fills up over many steps
- Compounding errors
- Loops if not careful
- Cost adds up

---
## Memory

- Conversation history is implicit memory
- For longer-term: external store
- Embeddings, summaries
- Replay relevant memory each turn

---
## Safety

- Sandboxing tool execution
- Permission prompts for risky ops
- Audit logs
- Human in the loop where needed

---
## Common Tool-Use Mistakes

- No safety bounds on agents
- Tools without descriptions; model picks badly
- Free-form output where schema needed
- No max-steps; infinite loops
- Lacking observability into agent behaviour
