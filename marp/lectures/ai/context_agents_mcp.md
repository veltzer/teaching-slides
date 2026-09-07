---
tags:
- concepts:ai
- concepts:agents
- concepts:llm
- concepts:tools
- concepts:mcp
- concepts:prompting
- concepts:workflows
level: intermediate
category: ai
audience:
- audiences:developers
- audiences:team-leads

---

# Context Engineering, Agentic Workflows, and MCP
## What the Model Sees, What It Does, and What It Can Reach
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## Overview

![title](svg/lectures/ai/context_agents_mcp/title.svg)

---

## What This Lecture Covers

1. Why a strong model still fails on your codebase
1. Context engineering: curating what the model sees
1. Repo memory, conventions, and docs as engineered inputs
1. Agentic workflows: plan, act, verify, iterate
1. Guardrails, autonomy levels, and failure modes
1. MCP and tool integration: GitHub, CI, browser, tickets
1. Putting the three levers together

---

## The Problem

- The model is brilliant and knows nothing about *your* project
- Every session starts blank: no memory of yesterday's decisions
- It cannot see your build, your tests, or your ticket tracker
- Left alone, it guesses conventions and invents file layouts
- Prompting harder does not fix this — the missing piece is **engineering**

---

## The Three Levers

![three_levers](svg/lectures/ai/context_agents_mcp/three_levers.svg)

---

## Three Levers, One Goal

- **Context**: control what the model sees before it answers
- **Agency**: let it plan, run tools, and check its own work
- **Integration**: wire it into the systems your team already uses
- Each lever compensates for a different weakness of a bare model
- Together they turn a chat window into a colleague with access

---

## What Is Context Engineering?

- The discipline of deciding **what enters the context window**, and when
- Prompt engineering asks "how do I phrase it?"
- Context engineering asks "what should be in front of the model at all?"
- Inputs: instructions, repo memory, retrieved files, tool results, history
- The output is a curated window, not a longer prompt

---

## Prompt vs Context Engineering

| Aspect | Prompt engineering | Context engineering |
|---|---|---|
| Unit | One message | The whole window |
| Owner | Whoever types | The team and the repo |
| Lifetime | One turn | Every session |
| Artifact | Wording | Files, tools, retrieval |
| Failure | Bad answer | Wrong facts, wrong conventions |

---

## What the Model Sees

![context_anatomy](svg/lectures/ai/context_agents_mcp/context_anatomy.svg)

---

## The Layers of a Window

- **System instructions**: who the model is and the rules it must obey
- **Repo memory**: project facts loaded automatically every session
- **Retrieved content**: files, docs, and search results pulled on demand
- **Tool results**: build output, test logs, diffs — the ground truth
- **Conversation**: the task, the plan, and what happened so far
- Every layer competes for the same finite attention budget

---

## Curate, Do Not Stuff

- A bigger window is not a better window
- Attention degrades as the window fills — relevant facts get lost in noise
- Stale content is worse than missing content: the model trusts it
- Ask of every token: *does this change the answer?*
- The goal is the **smallest** window that contains everything needed

---

## Repo Memory

- A file the agent loads at the start of every session in this repo
- Common names: `CLAUDE.md`, `AGENTS.md`, `.cursorrules`
- Holds what a new team member would be told on day one
- Committed to git: reviewed, versioned, shared with everyone
- This is the single highest-leverage context file you own

---

## What Belongs in Repo Memory

- How to build, test, and lint — the **exact** commands
- Conventions the linters do not enforce: naming, layout, style
- Architectural boundaries: what talks to what, and what must not
- Known traps: flaky tests, slow steps, things that look wrong but are right
- What to never do: force-push, edit generated files, disable checks

---

## A Repo Memory Example

```markdown
# Project Rules

## Build
- Always build with `rsconstruct build --verbose -j10`.
- Run scripts directly (`./scripts/foo.py`), never via `python`.

## Conventions
- Shebang is `#!/usr/bin/env python`, never `python3`.
- Includes are project-root-relative, never `../../..`.

## Never
- Never disable a check in CI to make a build green.
- Never mass-edit human-authored content with a script.
```

---

## Memory Has Layers

![memory_layers](svg/lectures/ai/context_agents_mcp/memory_layers.svg)

---

## Scoping Memory

- **Global**: personal habits that apply to every repo you touch
- **Project**: rules of this codebase, committed and shared
- **Directory**: rules for one subtree, loaded only when working there
- **Session**: what was learned in this task — decisions, findings, state
- Narrow scope keeps each layer short; short layers get read

---

## Conventions as Context

- Formatters and linters are context the model cannot argue with
- A failing lint is a precise instruction: fix *this line* *this way*
- Encode rules in tools first, prose second — tools never go stale
- Type hints, schemas, and test names tell the model what "correct" means
- The repo memory then only needs to say: "run the linter, obey it"

---

## Docs the Model Can Find

- Do not paste the manual into the window — make it **findable**
- A short index in memory: "database rules live in `doc/db.md`"
- The agent reads the file when the task touches the database
- Progressive disclosure: pointer first, full content on demand
- Docs in the repo beat docs in a wiki: the agent can `grep` the repo

---

## Skills: Instructions on Demand

- A skill is a named, self-contained procedure: "release", "add-endpoint"
- Loaded only when invoked or when the task clearly matches
- Keeps the always-on memory small while preserving depth
- Skills can reference scripts, templates, and checklists in the repo
- Think of them as runbooks the agent can execute

---

## Keeping Context Fresh

- Memory rots: commands change, directories move, rules get repealed
- Every time the agent does something wrong twice, fix the memory once
- Review memory files in code review like any other source
- Prune aggressively: a rule nobody can explain gets deleted
- Assign an owner — unowned context becomes fiction within months

---

## Context Anti-Patterns

- **The kitchen sink**: a thousand-line memory file nobody reads, including the model
- **The stale map**: paths and commands that no longer exist
- **The wiki dump**: prose pasted where a pointer would do
- **The secret rule**: a convention that lives only in one reviewer's head
- **The hoarder**: never clearing a session, so old tasks poison new ones

---

## Context Engineering Checklist

1. Repo memory exists, is short, and is committed
1. Build, test, and lint commands are exact and ready to paste
1. Rules that can be tools are tools; the rest is prose
1. Deep docs are indexed by pointer, not pasted
1. Someone owns the memory and prunes it on every drift

---

## From Chat to Agent

- A chat answers; an **agent** acts until the task is done
- It reads files, edits, runs commands, and looks at the results
- The model chooses each next step based on what it just observed
- The loop ends when the goal is verified, not when the text stops
- Autonomy is a dial, not a switch — you decide how far it turns

---

## The Agent Loop

![agent_loop](svg/lectures/ai/context_agents_mcp/agent_loop.svg)

---

## Plan, Act, Observe, Verify

- **Plan**: turn the goal into concrete steps before touching code
- **Act**: one tool call — read, edit, run, search
- **Observe**: the real output, not the model's expectation of it
- **Verify**: tests, linters, and checks decide whether the step worked
- Repeat until verification passes, or stop and report why it cannot

---

## Plan First

- A plan is cheap; a wrong edit across twenty files is not
- Good plans name the files, the order, and the verification for each step
- Review the plan when the task is large or the blast radius is wide
- Plan mode: the agent may read and think but not yet change anything
- A plan the human approved is also context for the rest of the run

---

## The Tools an Agent Needs

| Tool | Purpose | Risk |
|---|---|---|
| Read / search | Understand the code | None |
| Edit / write | Change the code | Medium |
| Run command | Build, test, script | High |
| Web fetch | Read docs and references | Low |
| Subagent | Delegate a bounded subtask | Medium |

---

## Tests Are the Feedback Signal

- Without tests the agent grades its own homework — and passes itself
- A failing test is a precise, machine-readable "not done yet"
- Ask for the test first: it fixes the definition of success
- The agent iterates against red until green, then stops
- Coverage gaps become agent blind spots — close them before delegating

---

## Iterating on Its Own

- Run the build; read the error; fix; run again — no human in the loop
- Typical cycle: a few seconds per iteration, dozens of iterations per task
- The agent should be reading **real output**, never summarizing from memory
- Cap the iterations: an agent that loops forever is spending your budget
- After N failures the right move is to stop and explain, not to keep guessing

---

## The Autonomy Dial

- **Ask every time**: every edit and command needs approval
- **Auto-accept edits**: free to change files, asks before commands
- **Auto-run**: everything allowed inside a sandbox or allowlist
- **Headless**: no human present — runs in CI on a trigger
- Turn it up as trust grows; turn it down for irreversible actions

---

## Subagents and Parallel Work

![subagents](svg/lectures/ai/context_agents_mcp/subagents.svg)

---

## Why Delegate?

- A subagent gets a **fresh window**: no clutter from the parent task
- Independent subtasks run in parallel — review five modules at once
- Only the conclusion returns; the noise stays in the child
- Give each subagent a tight brief and a clear definition of done
- Isolate risky work in a worktree so parallel agents never collide

---

## Guardrails

- **Hooks**: deterministic scripts that run before or after tool calls
    - block a `git push` when tests are red; run the formatter after every edit
- **Sandboxes**: the agent can break its container, not your laptop
- **Allowlists**: which commands may run without asking
- **Budgets**: tokens, time, and iterations — enforced by code, not prompts

---

## A Hook Example

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "./scripts/guard_push.sh" }
        ]
      }
    ]
  }
}
```

---

## Agents in CI

- Trigger: a new issue, a failing build, a review request
- The agent runs headless: reads the failure, proposes a fix, opens a PR
- A human still merges — the agent never has write access to `main`
- Every action leaves a trail: the transcript is the audit log
- Start with read-only jobs (triage, summarize), then earn write access

---

## Agent Failure Modes

- **Gaming the test**: deleting or weakening the check instead of fixing the code
- **The eternal loop**: retrying the same failed fix with cosmetic changes
- **Scope creep**: "while I was here" refactors nobody asked for
- **False completion**: "done" without having run the verification
- **Context blindness**: ignoring repo memory because it scrolled out

---

## Reviewing Agent Work

- Review the diff exactly as you would a human's — no shortcuts
- Read the transcript for *how* it got there: skipped steps hide there
- Check that verification actually ran, not just that it was mentioned
- Watch for deleted tests, loosened assertions, silenced warnings
- If the review takes longer than the task, the task was too big

---

## Agentic Workflow Checklist

1. A plan exists and names its verification steps
1. Tests define done; the agent iterates against them
1. Autonomy matches the blast radius of the task
1. Hooks and sandboxes enforce what prompts only request
1. A human reviews the diff **and** the transcript

---

## Why Integration Matters

- An agent limited to the filesystem is a very smart text editor
- Real work lives in GitHub, CI, the browser, and the ticket tracker
- Without access, the human becomes the copy-paste bridge
- Every integration removes one hand-off and one chance for drift
- The question is not *whether* to integrate but *how* to do it safely

---

## The M × N Problem

![m_x_n](svg/lectures/ai/context_agents_mcp/m_x_n.svg)

---

## One Protocol Instead of M × N Connectors

- M agent hosts, N systems: each pair needs its own adapter
- Each adapter re-implements auth, schemas, errors, and pagination
- **MCP**, the Model Context Protocol, standardizes the interface
- Write one server per system; every host that speaks MCP can use it
- The ecosystem does the integration work once, for everyone

---

## MCP in One Slide

- **Host**: the application the user talks to — editor, CLI, chatbot
- **Client**: the host's connection to one server
- **Server**: exposes a system as tools, resources, and prompts
- Transports: `stdio` for local processes, HTTP for remote services
- The model sees only the tool list; the plumbing is invisible to it

---

## Wiring the Model into Your Stack

![mcp_stack](svg/lectures/ai/context_agents_mcp/mcp_stack.svg)

---

## The Three Primitives

| Primitive | Direction | Example |
|---|---|---|
| Tool | Model calls it | `create_pull_request` |
| Resource | Model reads it | `ci://run/1234/log` |
| Prompt | User invokes it | "triage this issue" |

- Tools act, resources inform, prompts package a workflow
- Most integration work is tools; resources keep the window lean

---

## Configuring a Server

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
    },
    "tickets": {
      "url": "https://mcp.tracker.example/sse"
    }
  }
}
```

---

## Wiring GitHub

- Read issues, PRs, review comments, and diffs without leaving the session
- Open a PR with a body that links the issue and lists the verification
- Respond to review comments by pushing fixes to the same branch
- Scope the token: one repo, no admin, short expiry
- The agent proposes; branch protection decides what lands

---

## Wiring CI

- Read the failing job's log — the actual log, not a summary
- Correlate the failure with the diff that caused it
- Re-run a job after a fix; wait for the result before declaring victory
- Local gate first: run what the workflow runs before pushing
- Never fix CI by editing the workflow to stop checking

---

## Wiring the Browser

- Some verification is visual: layouts, flows, console errors
- A browser tool lets the agent load the page, click, and screenshot
- Read the console and network log instead of guessing why it broke
- Record the session so the reviewer sees what the agent saw
- Keep it in a test profile: no production cookies, no real accounts

---

## Wiring Tickets

- The ticket is the task statement — the agent should read the source
- Pull acceptance criteria into the plan; ask when they are missing
- Post progress back: branch name, PR link, what was verified
- Transition state only through the tool, never by editing a database
- The tracker becomes the shared memory between humans and agents

---

## From Ticket to Merged PR

![ticket_to_pr](svg/lectures/ai/context_agents_mcp/ticket_to_pr.svg)

---

## The Full Loop

1. The agent reads the ticket and the linked discussion
1. It plans, then edits under the repo's conventions
1. Tests run locally until green; the linter passes
1. A PR opens with the verification listed; CI runs
1. Review comments come back; the agent addresses them
1. A human approves and merges; the ticket closes itself

---

## Trust Boundaries

![trust_boundaries](svg/lectures/ai/context_agents_mcp/trust_boundaries.svg)

---

## Everything a Tool Returns Is Untrusted

- A web page, an issue body, a log line — any of them can contain instructions
- **Prompt injection**: text in a tool result that tries to steer the agent
- The model cannot reliably tell data from commands — assume it cannot
- Design so the damage is bounded: least privilege, read-only by default
- Irreversible actions require a human, no matter what the text says

---

## Tool Hygiene

- Fewer tools, better described: the model picks from the descriptions
- One tool, one job — a kitchen-sink tool gets called wrong
- Return structured errors: the agent can act on "not found", not on a stack trace
- Log every call with its arguments — that is your audit trail
- Pin servers you trust; a malicious server is a supply-chain attack

---

## Integration Checklist

1. Every system is reached through a tool, never through pasted screenshots
1. Tokens are scoped, short-lived, and stored in a secret store
1. Writes to shared systems go through review or approval
1. Tool results are treated as untrusted input
1. Every tool call is logged and attributable

---

## The Levers Reinforce Each Other

- Good **context** makes the agent's plans correct on the first try
- Good **tools** give the agent real feedback instead of guesses
- A good **loop** turns feedback into fixes without a human relaying it
- Weak context plus strong tools is an agent doing the wrong thing fast
- Strong context with no tools is a well-informed agent that cannot check

---

## Where to Start

1. Write the repo memory today: build, test, lint, and the three biggest traps
1. Pick one task with a good test suite; let the agent iterate against it
1. Add one MCP server — GitHub is the usual first — with a scoped token
1. Add one hook that blocks the one thing that must never happen
1. Review the transcript of the first ten runs; fix the memory each time

---

## Summary

- Context engineering: curate the window — memory, conventions, findable docs
- Agentic workflows: plan, act, observe, verify — tests define done
- MCP: one protocol wires the model into GitHub, CI, browser, and tickets
- Guardrails in code, not in prose: hooks, sandboxes, scoped tokens
- The model is the engine; the engineering around it is what ships
