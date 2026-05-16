---
tags:
  - data-and-ai:ai
  - data-and-ai:llm
  - data-and-ai:mcp
level: intermediate
category: ai
audience:
  - audiences:developers
  - audiences:senior-developers
  - audiences:devops

---
# Connecting to MCP Servers

---
## What This Chapter Covers

- What MCP is and why it exists
- The MCP ecosystem
- Adding a server
- Using MCP in a workflow
- The trust boundary
- Writing a small server

---
## What MCP Is

- The Model Context Protocol
- A standard for exposing tools to LLMs
- Server speaks, client reads
- Vendor-neutral by design

---
## Why It Exists

- Every model needs the same tools
- Every team writes the same adapters
- A standard breaks that loop
- Write once, plug into many clients

---
## The Three Primitives

- Tools: actions the model can call
- Resources: data the model can read
- Prompts: reusable prompt templates
- That is the whole protocol

---
## The Three Primitives Visualized

![mcp_primitives](svg/courses/ai/claude-workshop/06_mcp/mcp_primitives.svg)

---
## Why A Standard Matters

- Tool authors target one spec
- Clients support many servers
- Swap models without rewriting
- Ecosystem effects compound

---
## The MCP Ecosystem

- Filesystem servers
- Git and GitHub servers
- Database servers
- Browser automation servers

---
## Vendor Vs Community Servers

- Vendors ship official servers
- Community fills in the gaps
- Quality varies, audit before use
- Pin versions to known-good

---
## Local Vs Remote Servers

- Local runs on your machine
- Remote runs elsewhere, talks over the wire
- Local is simpler and safer
- Remote unlocks shared state

---
## MCP Architecture

![mcp_architecture](svg/courses/ai/claude-workshop/06_mcp/mcp_architecture.svg)

---
## Adding A Server

- Edit `.claude/settings.json` or user settings
- Declare the command and args
- Pass environment variables
- Restart Claude Code to pick it up

---
## Server Configuration Shape

- A name for the server
- A command to launch it
- Optional args
- Optional env block

---
## Authentication And Secrets

- Pass tokens via env vars
- Never commit secrets
- Use a secrets manager when possible
- Rotate when in doubt

---
## Verifying It Is Wired Up

- The status line shows MCP servers
- A `/mcp` command lists them
- Tools appear in the available tools
- Smoke-test with a small call

---
## Using MCP In A Workflow

- Querying a database directly
- Driving a browser
- Reading and writing tickets
- Talking to internal services

---
## Database Example

- Connect to a read-only replica
- Let Claude write the SQL
- Inspect the result in context
- Decide what to do next

---
## Browser Example

- Open a URL
- Take a screenshot
- Read the DOM
- Fill a form and submit

---
## Issue Tracker Example

- Read open tickets
- Update status from the session
- Cross-link tickets and PRs
- Generate weekly summaries

---
## The Trust Boundary

- Every MCP server is code you run
- It sees what the model sends
- It returns what becomes context
- Prompt injection lives here

---
## Prompt Injection Via Tool Results

- A tool returns "ignore prior rules"
- The model may follow it
- A scraped page can carry hostile text
- Treat tool output like user input

---
## The Trust Boundary Visualized

![trust_boundary](svg/courses/ai/claude-workshop/06_mcp/trust_boundary.svg)

---
## Auditing A Server Before Install

- Read the source if open
- Check the publisher
- Look at issues and CVEs
- Run it in a sandbox first

---
## Writing A Minimum Server

- A few dozen lines in the SDK
- One tool, one input, one output
- Logs to stderr, not stdout
- Speaks JSON-RPC

---
## Exposing One Internal Tool

- Wrap an existing internal command
- Add input validation
- Add a clear tool description
- Ship it for your team

---
## When This Is Worth It

- The tool is used many times a day
- The team is bigger than one
- The wrapper is small
- Long-term ROI is clear

---
## When It Is Not

- One-off scripts
- Things you can just type
- Highly variable inputs
- Tools no one else will use

---
## Hands-On Exercise

- Install a filesystem MCP server
- Install a GitHub MCP server
- Use both from a single session
- Audit one server's source before installing
