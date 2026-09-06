---
tags:
- concepts:ai
- concepts:agents
- concepts:llm
- concepts:tools
level: intermediate
category: ai
audience:
- audiences:developers

---

# Tools in AI
## Giving LLM Agents Hands to Act on the World
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## Overview

![title](svg/lectures/ai/tools/title.svg)

---

## What This Lecture Covers

1. What a "tool" is — and why a language model needs one
1. The anatomy of a tool definition
1. The tool-use loop: how a model calls a function
1. Schemas, validation, and structured arguments
1. Tools versus skills, RAG, and fine-tuning
1. MCP: a standard protocol for tools
1. Designing good tools — and the pitfalls to avoid

---

## The Problem

- An LLM is a text engine — it predicts tokens, nothing more
- On its own it cannot read a file, query a database, or send mail
- Its knowledge is frozen at training time
- It cannot do arithmetic reliably or check today's price
- We need to let the model *reach outside itself* and act

---

## The Core Idea

> A tool is a function you expose to the model, which it can choose to call to get information or change the world.

- You describe the function; the model decides when to use it
- The model emits a request; *your code* runs the function
- The result flows back into the conversation

---

## What Is a Tool?

![what_is_a_tool](svg/lectures/ai/tools/what_is_a_tool.svg)

---

## A Tool Is Not...

- **Not** something the model runs itself — *your* runtime executes it
- **Not** baked into the weights — it is supplied at request time
- **Not** a guarantee — the model may call it wrong, or not at all
- **Not** free — each tool's schema costs context tokens

---

## Why Models Need Tools

- **Facts** — fresh, private, or precise data the model never saw
- **Actions** — sending email, creating a ticket, deploying code
- **Computation** — exact math, code execution, deterministic logic
- **Reach** — anything beyond the text the model was trained on

The model supplies *judgement*; the tool supplies *capability*.

---

## The Anatomy of a Tool

![anatomy](svg/lectures/ai/tools/anatomy.svg)

---

## A Tool Definition

```json
{
  "name": "get_weather",
  "description": "Get the current weather for a city. Use when the user asks about temperature or conditions.",
  "input_schema": {
    "type": "object",
    "properties": {
      "city": { "type": "string", "description": "City name, e.g. 'Paris'" }
    },
    "required": ["city"]
  }
}
```

---

## The Three Parts

- **name** — a short, unique identifier the model emits to call it
- **description** — what it does *and* when to use it
- **input_schema** — the arguments, typed, in JSON Schema
- The description and schema are *all the model knows* about the tool

---

## The Tool-Use Loop

![tool_use_loop](svg/lectures/ai/tools/tool_use_loop.svg)

---

## Step by Step

1. You send the prompt **plus** the list of tool definitions
1. The model replies with a **tool call**: name + arguments
1. *Your code* executes the function and captures the result
1. You send the **result** back to the model
1. The model continues — answering, or calling another tool

---

## The Model Only Asks

- The model never runs anything — it emits a structured *request*
- This is the critical safety boundary: you stay in control
- You validate, you decide, you execute, you return
- A tool call is a suggestion, not a command

---

## Schemas and Validation

![schema_validation](svg/lectures/ai/tools/schema_validation.svg)

---

## Why the Schema Matters

- It tells the model exactly what arguments are valid
- It lets the model emit well-formed, typed JSON
- Your runtime can **validate** before executing — reject bad calls
- A vague schema yields vague, often wrong, calls

---

## Schema: Weak vs Strong

```json
// Weak — the model guesses
{ "properties": { "q": { "type": "string" } } }

// Strong — the model is guided
{ "properties": {
    "query":  { "type": "string", "description": "Search terms" },
    "limit":  { "type": "integer", "description": "Max results, 1-50" }
  },
  "required": ["query"]
}
```

---

## Tools vs Skills vs RAG vs Fine-Tuning

![tools_vs_alternatives](svg/lectures/ai/tools/tools_vs_alternatives.svg)

---

## Four Different Questions

- **Tool** — *what action* can I take in the world?
- **Skill** — *how* do I carry out this procedure?
- **RAG** — *what facts* should I pull into context?
- **Fine-tuning** — what behaviour is *baked into* the model?

---

## They Are Complementary

- A **skill** often *instructs the agent to call a tool*
- A tool can *perform the retrieval* that RAG describes
- Fine-tuning shapes instinct; tools supply concrete capability
- A mature agent uses all four together

---

## When to Expose a Tool

- The task is a **discrete action** with a clear input and output
- It needs **fresh or private data** the model cannot know
- It needs **deterministic** results — math, lookups, transforms
- It must **change the world** — write, send, deploy, delete

---

## When NOT to Use a Tool

- A multi-step *procedure with conventions* → write a **skill**
- A large body of changing *facts to read* → use **RAG**
- Pure text reasoning the model already does well → just ask
- An action too dangerous to expose → keep a human in the loop

---

## MCP: A Standard for Tools

![mcp](svg/lectures/ai/tools/mcp.svg)

---

## The Model Context Protocol

- A tool today is often re-implemented per app, per model
- **MCP** is an open protocol: a server *offers* tools, any client uses them
- Write a tool once as an MCP server — every MCP host can call it
- Tools become portable, like the skills convention is portable

---

## A Minimal Tool Loop (Any Agent)

```python
# 1. Send prompt + tool definitions to the model
# 2. If the reply is a tool call, parse name + arguments
# 3. Validate arguments against the schema; reject if bad
# 4. Execute the real function; capture the result
# 5. Send the result back; repeat until the model is done
```

Tools are *just functions plus a description* — supportable anywhere.

---

## Designing Good Tools

![designing_tools](svg/lectures/ai/tools/designing_tools.svg)

---

## Design Principles

1. **One job per tool** — narrow, predictable, easy to describe
1. **Describe the trigger** — say *when* to use it, not just what
1. **Type the inputs tightly** — constrain ranges, enums, formats
1. **Return clean results** — concise, structured, model-readable

---

## Write Descriptions for the Model

- The model picks a tool by *reading the description*
- State the capability in concrete terms
- Name the situation that should trigger it
- Avoid overlap — two tools that both "fit" cause bad picks

---

## Errors Are Tool Results Too

- A failed call should return an **error message**, not crash
- Tell the model *why* it failed and *how* to fix the call
- The model can then retry with corrected arguments
- Silent failures leave the model guessing — fail loudly, clearly

---

## Common Pitfalls

![pitfalls](svg/lectures/ai/tools/pitfalls.svg)

---

## Pitfall: The Kitchen-Sink Tool

- One tool with a `mode` flag that does ten different things
- Vague description, sprawling schema, unpredictable behaviour
- **Fix:** split into several small, single-purpose tools

---

## Pitfall: Too Many Tools

- Dozens of tool schemas bloat context and confuse the model
- The model picks slowly, and sometimes picks wrong
- **Fix:** expose only what the task needs; group by sub-agent

---

## Security: Tools Act for Real

- A tool can delete data, spend money, or send messages
- The model can be *tricked* into calling it (prompt injection)
- Never expose a destructive tool without guardrails
- **Validate inputs, scope permissions, confirm risky actions**

---

## Good Habits

- One tool, one clear job — narrow beats broad
- Write the description for the model, with explicit triggers
- Constrain the schema tightly; validate every call
- Return structured results and informative errors
- Scope and confirm anything that changes the world

---

## A Worked Example: Create Ticket

```json
{
  "name": "create_ticket",
  "description": "Open a bug ticket in the tracker. Use when the user reports a defect to be fixed.",
  "input_schema": {
    "type": "object",
    "properties": {
      "title":    { "type": "string" },
      "severity": { "type": "string", "enum": ["low", "high", "critical"] }
    },
    "required": ["title", "severity"]
  }
}
```

---

## What the Example Shows

- A clear, trigger-rich description — *when* to use it
- A tight schema: `severity` is an enum, not free text
- Required fields force the model to supply what matters
- One job: it opens a ticket, nothing else

---

## Tools and Multi-Agent Systems

- A sub-agent can be given just the tools it needs
- Keeps each agent's context small and its choices focused
- A planner agent can route work to tool-equipped workers
- Fewer tools per agent means faster, more reliable selection

---

## The Mental Model

![mental_model](svg/lectures/ai/tools/mental_model.svg)

---

## Summary

- A tool is a **function** the model can **choose to call**
- The model only *asks* — **your code** runs it and returns the result
- The **schema** guides the call; the **description** decides if it fires
- Tools complement skills, RAG, and fine-tuning — they don't replace them
- **MCP** makes tools portable across hosts and models

---

## Where to Start

1. Pick one action your agent keeps needing to take
1. Define it: a sharp name, a trigger-rich description, a tight schema
1. Wire the tool-use loop: call, validate, execute, return
1. Add guardrails, then grow a small, focused toolset

Give the model judgement *and* the hands to act on it.

---

## Questions?

- Tools turn a text engine into an agent that can act
- The model decides; your runtime stays in control
- Start narrow, type tightly, and keep a human on the dangerous calls

## Thank You
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)
