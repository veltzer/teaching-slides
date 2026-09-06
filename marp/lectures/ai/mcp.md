---
tags:
- concepts:ai
- concepts:agents
- concepts:llm
- concepts:tools
- concepts:mcp
level: intermediate
category: ai
audience:
- audiences:developers

---

# The Model Context Protocol
## A Universal Standard for Connecting LLMs to the World
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## Overview

![title](svg/lectures/ai/mcp/title.svg)

---

## What This Lecture Covers

1. The problem MCP solves — the M×N integration mess
1. What MCP is, and where it came from
1. Hosts, clients, and servers — the architecture
1. The three primitives: tools, resources, prompts
1. Transports: stdio and HTTP
1. The lifecycle of a session and a tool call
1. Security, pitfalls, and good habits

---

## The Problem

- An LLM is a text engine — on its own it cannot reach the world
- We give it **tools**, but each tool is wired to one app, one model
- Every integration is re-built for every host and every provider
- The same GitHub or database connector is written again and again
- We need *one* way to plug capabilities into *any* agent

---

## The M×N Explosion

![the_problem](svg/lectures/ai/mcp/the_problem.svg)

---

## M Hosts, N Tools

- **M** AI apps — editors, chatbots, IDEs, custom agents
- **N** integrations — files, GitHub, Slack, Postgres, your API
- Wire each host to each tool directly: **M × N** bespoke connectors
- Every new host re-implements every integration from scratch
- Every new tool must be ported to every host that wants it

---

## The Core Idea

> MCP is an open protocol that lets any AI app talk to any tool through one shared interface.

- A tool is written **once** as an MCP *server*
- Any MCP *host* can connect to it — no per-app glue
- M × N bespoke connectors collapse into M + N

---

## From M×N to M+N

![m_plus_n](svg/lectures/ai/mcp/m_plus_n.svg)

---

## What Is MCP?

- The Model Context Protocol — an open standard
- Introduced by Anthropic in late 2024, now broadly adopted
- A wire protocol built on **JSON-RPC 2.0**
- It standardizes *how* an agent discovers and calls capabilities
- Think "USB-C for AI" — one port, many devices

---

## The "USB-C for AI" Analogy

![usb_analogy](svg/lectures/ai/mcp/usb_analogy.svg)

---

## The Architecture

![architecture](svg/lectures/ai/mcp/architecture.svg)

---

## Three Roles

- **Host** — the AI app the user interacts with (e.g. Claude Code)
- **Client** — lives inside the host; one client per server connection
- **Server** — exposes capabilities (tools, data) over the protocol
- The host runs the LLM; the server runs the real code

---

## Why a Client Per Server

- The host may connect to several servers at once
- Each connection is an isolated **client–server** pair
- One misbehaving server cannot see another's traffic
- The host multiplexes results from all of them into the model

---

## The Three Primitives

![primitives](svg/lectures/ai/mcp/primitives.svg)

---

## Tools, Resources, Prompts

- **Tools** — functions the model can *call* to act or fetch
- **Resources** — data the host can *read* into context (files, rows)
- **Prompts** — reusable templates the user can *invoke*
- One server may offer any mix of the three

---

## Who Is in Control

- **Tools** are *model-controlled* — the LLM decides to call them
- **Resources** are *app-controlled* — the host decides what to load
- **Prompts** are *user-controlled* — the user picks them, e.g. a slash command
- The distinction shapes how each primitive is exposed and secured

---

## A Tool, As MCP Sees It

```json
{
  "name": "search_issues",
  "description": "Search GitHub issues in a repo. Use when the user asks about open bugs.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "repo":  { "type": "string", "description": "owner/name" },
      "query": { "type": "string", "description": "Search terms" }
    },
    "required": ["repo", "query"]
  }
}
```

---

## Discovery Is Dynamic

- A host does not hard-code a server's tools
- On connect, it calls `tools/list` and learns them at run time
- Add a tool to the server — every host sees it next session
- The same holds for `resources/list` and `prompts/list`

---

## Transports

![transports](svg/lectures/ai/mcp/transports.svg)

---

## Two Ways to Connect

- **stdio** — the host launches the server as a local subprocess
    - Messages flow over stdin / stdout — simple, private, fast
    - Ideal for local tools: filesystem, git, your own scripts
- **HTTP** — the server is a remote service the host calls
    - Uses HTTP with streaming for server-to-client messages
    - Ideal for hosted, multi-user, or shared integrations

---

## Same Protocol, Either Way

- The JSON-RPC messages are *identical* across transports
- Only the pipe differs — a subprocess or a network socket
- Write your server logic once; pick a transport to suit deployment
- A local stdio server can later be exposed over HTTP unchanged

---

## The Session Lifecycle

![lifecycle](svg/lectures/ai/mcp/lifecycle.svg)

---

## How a Session Begins

1. The host starts a **client** and connects to the server
1. They **initialize** — exchanging versions and capabilities
1. The client asks `tools/list`, `resources/list`, `prompts/list`
1. The host now knows everything the server can do
1. The session stays open for many calls

---

## The Tool-Call Loop Over MCP

![tool_call_flow](svg/lectures/ai/mcp/tool_call_flow.svg)

---

## Step by Step

1. The model decides to call a tool and emits name + arguments
1. The host's client sends `tools/call` to the server
1. The **server** runs the real code and returns a result
1. The host feeds the result back into the model's context
1. The model continues — answering, or calling another tool

---

## The Boundary Still Holds

- The model only *asks* — it never runs the server's code
- The host validates and routes; the server executes
- This is the same safety boundary as plain tool use
- MCP standardizes the wire, not the trust model

---

## MCP vs Plain Tools

![mcp_vs_tools.svg](svg/lectures/ai/mcp/mcp_vs_tools.svg)

---

## What MCP Adds

- Plain tools live *inside* one app's code, bound to one host
- MCP tools live in a *separate, reusable server*
- Discovery, transport, and schema become a shared standard
- The capability outlives any single app or model

---

## When to Build an MCP Server

- A capability is needed by **more than one** agent or app
- You want it **decoupled** from any single host's codebase
- It should be **shareable** — internally or with the community
- You want **dynamic discovery** instead of recompiling the host

---

## When Plain Tools Suffice

- A one-off tool used by a single in-house agent
- Logic so trivial that a server is overhead
- A capability tightly coupled to one app's internals
- Start simple; promote to an MCP server when reuse appears

---

## The Growing Ecosystem

- Official servers: filesystem, git, GitHub, Slack, Postgres, more
- SDKs in Python, TypeScript, and other languages
- Hosts: Claude Code, Claude Desktop, IDEs, custom agents
- Write a server once; the whole ecosystem can use it

---

## A Minimal Server (Conceptual)

```python
# 1. Declare the server and its capabilities
# 2. Register each tool: name, description, input schema
# 3. Implement the handler that runs when the tool is called
# 4. Choose a transport (stdio or HTTP) and serve
# 5. Any MCP host can now connect, list, and call your tools
```

A server is *just functions plus a manifest* — spoken over a standard wire.

---

## Security: A Server Runs Real Code

- A server can read files, query databases, send messages
- A malicious or buggy server can leak or destroy data
- The model can be *tricked* into calling it (prompt injection)
- **Only connect servers you trust; scope their permissions**

---

## Security: Trust the Source

- An MCP server is a third-party dependency — vet it like one
- Prefer official or audited servers for sensitive systems
- Run local servers with least privilege; sandbox where possible
- Confirm risky actions with a human in the loop

---

## Common Pitfalls

![pitfalls](svg/lectures/ai/mcp/pitfalls.svg)

---

## Pitfall: Too Many Tools

- One host connected to a dozen chatty servers
- Hundreds of tool schemas bloat context and confuse the model
- **Fix:** connect only the servers a task needs; group by agent

---

## Pitfall: Vague Tool Descriptions

- The model picks a tool by *reading its description*
- A weak description means the right tool never fires
- **Fix:** state the capability and the trigger, just like plain tools

---

## Good Habits

- Expose one clear job per tool; describe its trigger
- Keep each server focused; connect only what a task needs
- Type input schemas tightly and validate every call
- Treat every server as untrusted code until you vet it
- Prefer official servers for anything that touches real systems

---

## A Worked Example: A Git Server

- Exposes tools: `git_log`, `git_diff`, `git_blame`
- Exposes resources: the working tree's files, read-only
- Runs locally over **stdio**, launched by the host
- Any MCP host gains git awareness with zero custom code

---

## What the Example Shows

- One server, several sharply-scoped tools
- A mix of **tools** (actions) and **resources** (readable data)
- Local **stdio** transport — private and fast
- Total portability: every host can reuse the same server

---

## MCP and Multi-Agent Systems

- A sub-agent connects only to the servers it needs
- Keeps each agent's tool set small and its choices focused
- Servers are the shared vocabulary between agents
- A planner can route work to agents wired to the right servers

---

## The Mental Model

![mental_model](svg/lectures/ai/mcp/mental_model.svg)

---

## Summary

- MCP is an **open protocol** connecting any AI app to any tool
- It collapses **M × N** bespoke connectors into **M + N**
- **Host, client, server** — the host runs the model, the server runs code
- Three primitives: **tools**, **resources**, **prompts**
- One server, written once, is reusable across hosts and models

---

## Where to Start

1. Pick a capability more than one of your agents needs
1. Wrap it as a small MCP server with sharp, well-described tools
1. Run it over stdio and connect it from your host
1. Vet, scope, then share it across your agents

Build the capability once; let every agent plug in.

---

## Questions?

- MCP is the standard port between agents and the world
- Write a tool once; any host can speak to it
- Start with one trusted server and grow from there

## Thank You
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)
