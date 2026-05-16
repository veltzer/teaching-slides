---
tags:
  - data-and-ai:ai
  - data-and-ai:llm
level: intermediate
category: ai
audience:
  - audiences:developers
  - audiences:senior-developers

---
# Introduction and Orientation

---
## What This Chapter Covers

- What Claude is and is not
- The Claude model family
- A mental model for an LLM coding agent
- Workshop ground rules

---
## Claude the Model vs Claude the Product

- The model is the weights and the API
- The product is what wraps the model
- Same model can power many surfaces
- We will mostly use Claude Code

---
## Claude Code as a Coding Agent

- Runs in your terminal
- Reads files, edits files, runs commands
- Asks for permission when needed
- Designed for real day-to-day work

---
## Other Claude Surfaces

- The web app at claude.ai
- The Anthropic API
- IDE extensions for VS Code and JetBrains
- The desktop app

---
## Surfaces At A Glance

![surfaces](svg/courses/ai/claude-workshop/01_introduction/surfaces.svg)

---
## When To Use Which Surface

- Web app for ad hoc questions
- Claude Code for codebase work
- API for building apps on top
- IDE extension for inline help

---
## The Claude Model Family

- Opus: the heaviest model
- Sonnet: balanced default
- Haiku: small and fast
- Pick by task, not by habit

---
## When To Reach For Opus

- Hard reasoning
- Long multi-step coding tasks
- Architectural questions
- Anything where you would pay for quality

---
## When To Reach For Sonnet

- Default for most coding work
- Good speed and quality balance
- Cheaper than Opus per token
- Handles long context well

---
## When To Reach For Haiku

- Quick fixes and small edits
- High volume background tasks
- Cost-sensitive workflows
- Latency-sensitive interactions

---
## Model Family Trade-Offs

![model_family](svg/courses/ai/claude-workshop/01_introduction/model_family.svg)

---
## Cost, Latency and Capability

- Bigger model: better but slower and pricier
- Smaller model: faster and cheaper
- The right model is task-shaped
- Measure, do not guess

---
## Knowledge Cutoff

- The model knows the world up to a date
- After that it is blind
- New libraries, new APIs are unknown
- Feed it docs or let it fetch

---
## Why Claude Reads And Runs Things

- Static answers go stale fast
- Real codebases need real reads
- Running tests beats guessing
- The agent loop closes feedback

---
## The Agent Loop

![agent_loop](svg/courses/ai/claude-workshop/01_introduction/agent_loop.svg)

---
## Prompts Are Not The Whole Story

- The agent reads files, you do not paste
- Tools and permissions shape behavior
- Config and memory shape behavior
- The prompt is just one input

---
## Where Humans Stay In The Loop

- Reviewing diffs before merge
- Approving risky commands
- Naming the goal
- Catching subtle wrongness

---
## Workshop Ground Rules

- We work on a real repo all day
- Capture prompts, configs, outputs
- Break things on purpose
- Ask out loud, not in DMs

---
## Common Newcomer Mistakes

- Treating the agent like a search engine
- Skipping permission review
- Ignoring the cost meter
- Forgetting to read the diff
