---
tags:
- concepts:ai
- concepts:agents
- concepts:llm
- concepts:architecture
- concepts:rag
- concepts:mcp
- concepts:prompting
- concepts:tools
level: beginner
category: ai
audience:
- audiences:managers
- audiences:project-management
- audiences:architects

---

# Principles of Agentic AI Solution Design
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## Overview

![title](svg/lectures/ai/agentic_solution_design/title.svg)

---

## What This Lecture Covers

1. The vocabulary: prompt, command, skill, RAG, MCP, tool, agent
1. Which building block solves which kind of problem
1. What an agent is, and how it differs from a chatbot or a workflow
1. The parts of an agent: the model, triggers, context, tools, guardrails
1. How to break a business use case into an AI solution
1. Which questions to bring to your IT and data teams

---

## The Building Blocks

![building_blocks](svg/lectures/ai/agentic_solution_design/building_blocks.svg)

---

## Telling the Model What to Do

- **Prompt**: the text you type, a one-off instruction ("summarize this contract")
- **Command**: a prompt saved under a name so anyone can rerun it ("/weekly-report")
- **Skill**: a package of know-how (instructions, templates, examples) that the model loads only when the task needs it
- All three change **what the model is asked**, not what it can reach
- They are cheap to create and are usually the first thing to try

---

## Giving the Model Knowledge and Hands

- **RAG** (Retrieval-Augmented Generation): before answering, search our own documents and hand the relevant pages to the model
    - Use it when the answer lives in procedures, manuals, or past projects
- **Tool**: one concrete action the model may request, such as "search the parts catalog" or "open a ticket"
- **MCP** (Model Context Protocol): a standard plug that exposes a system's tools to any AI application
    - Think of it as USB for AI: build the connector once, reuse it everywhere

---

## Which Block Do I Need?

| The need | The building block |
|---|---|
| A better answer to a one-time question | Prompt |
| The same task, repeated by many people | Command or skill |
| Answers grounded in our own documents | RAG |
| Reading or changing data in a business system | Tool, usually via MCP |
| A multi-step task that needs judgement along the way | Agent |

---

## What Is an Agent?

- An agent is an LLM that works **in a loop** toward a **goal**
- At every step the model decides what to do next: look something up, call a tool, or finish
- It sees the result of each action and adjusts its plan
- It stops when the goal is reached, or when it hits a limit you set
- In one sentence: **a model, in a loop, with tools, until the job is done**

---

## The Agent Loop

![agent_loop](svg/lectures/ai/agentic_solution_design/agent_loop.svg)

---

## Chatbot, Workflow, or Agent?

| | Chatbot | Workflow | Agent |
|---|---|---|---|
| Who decides the steps? | Nobody, one answer | The designer, in advance | The model, at run time |
| Predictability | High | High | Lower |
| Good for | Questions and drafts | Known, repeatable processes | Open-ended tasks |
| Typical risk | Wrong answer | Rigid when reality differs | Unexpected actions |

---

## The Anatomy of an Agent

![agent_anatomy](svg/lectures/ai/agentic_solution_design/agent_anatomy.svg)

---

## Talking to the LLM

- Every step of the agent is a call to a language model: text in, text out
- **Which model?** Larger models reason better; smaller ones are faster and cheaper
- **Where does it run?** A public cloud service, a private cloud, or on our own servers
    - Sensitive or classified data usually decides this question for you
- **What does it cost?** Usage is billed per amount of text, and agents make many calls per task
- The model has no memory between calls: everything it needs must be sent each time

---

## What Starts the Agent?

![triggers](svg/lectures/ai/agentic_solution_design/triggers.svg)

---

## Context and Memory

- **Context**: everything the model sees on a given step: instructions, the goal, documents, results so far
- The context has a size limit, so the solution must choose what goes in
- **Short-term memory**: the history of the current task, kept only while it runs
- **Long-term memory**: facts saved between runs, such as user preferences or past decisions
- Too little context gives wrong answers; too much gives slow, costly, and confused ones

---

## Tools, Permissions, and Guardrails

- Every tool is a door into a real system, so decide for each one: **read only, or also write?**
- Give the agent the smallest set of permissions that does the job
- Put a **human approval** step before anything costly or hard to undo
- Set limits: number of steps, time, money, which data it may touch
- Treat incoming documents and emails as untrusted: they may contain instructions aimed at the agent

---

## How Do We Know It Works?

- Collect a set of real example cases with the expected outcome **before** building
- Measure the agent against them after every change to prompts, model, or tools
- Log every step so a wrong result can be traced to its cause
- Track cost and response time per task, not just correctness
- Decide in advance who owns the agent in production and who reviews its mistakes

---

## From Use Case to Solution

![decompose](svg/lectures/ai/agentic_solution_design/decompose.svg)

---

## Example: Supplier Inquiry Assistant

- **Use case**: buyers spend hours answering supplier emails about order status
- **Trigger**: a new email arrives in the procurement mailbox
- **Knowledge**: RAG over procurement procedures and contract terms
- **Tools**: an MCP connector to the ERP, read only, to look up orders
- **Guardrail**: the agent drafts the reply, a buyer approves before it is sent
- **Success**: half the replies sent within one hour, with no wrong order data

---

## Questions to Bring to IT and Data

- **Data**: Where does the knowledge live? Who owns it? How current is it?
- **Systems**: Which systems must the agent read or update? Is there an API or MCP connector?
- **Security**: What is the data classification? Which model hosting is allowed?
- **Identity**: Does the agent act as itself or on behalf of the user?
- **Operations**: What triggers it, how often, and what happens when it fails?
- **Ownership**: Who pays, who monitors, and who fixes it?
