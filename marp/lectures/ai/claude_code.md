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
# Agents at the Command Line
## Working with the Claude Code CLI
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## Overview

![title](svg/lectures/ai/claude_code/title.svg)

---

## What This Lecture Covers

1. What Claude Code is and how it runs an agent in your terminal
1. Sessions, permissions, and giving the agent context
1. Customization: project memory, skills, subagents, hooks
1. Extending the agent with MCP servers
1. Headless mode: agents in scripts, pipelines, and CI
1. Cost, safety, and daily-workflow habits

---

## What Is Claude Code?

- A command-line agent: a model in a loop, with tools, in *your* terminal
- It reads files, edits code, runs commands, and uses git — under your control
- The working directory is its world; your repo is its context
- You steer it with plain language; it does the mechanical work
- It is an *agent harness* — everything from the previous lecture applies

---

## Installing and Starting

```bash
# install once
npm install -g @anthropic-ai/claude-code

# start an interactive session in your project
cd my-project
claude

# or start with a task already in hand
claude "explain the build system in this repo"
```

---

## Your First Session

- Type what you want done, in plain language, like to a colleague
- The agent explores the repo itself — you do not paste files into it
- It proposes actions; you approve, refine, or reject
- Everything happens in your working directory, visible in git
- Quit with `Ctrl+D`; nothing is hidden — check `git diff` anytime

---

## The Agent Behind the Prompt

![agent_behind_prompt](svg/lectures/ai/claude_code/agent_behind_prompt.svg)

---

## The Built-in Tools

- **Read / Write / Edit** — file operations with precise, reviewable diffs
- **Glob / Grep** — fast code search across the repository
- **Bash** — run commands: build, test, git, anything in your shell
- **WebSearch / WebFetch** — pull in documentation and fresh facts
- **Task** — spawn subagents for delegated work
- The same loop as any agent: model decides, tools execute, results return

---

## Permission Modes

- By default the agent **asks** before edits and commands
- Auto-accept mode: edits proceed, dangerous commands still ask
- **Plan mode**: read-only — the agent may look but not touch
- A bypass mode exists for sandboxes and CI — never for your laptop
- Cycle modes interactively; or start with `claude --permission-mode plan`

---

## Controlling Permissions

```json
{
  "permissions": {
    "allow": [
      "Bash(npm test:*)",
      "Bash(git diff:*)",
      "Read(~/projects/**)"
    ],
    "deny": [
      "Bash(rm -rf:*)",
      "Read(.env)"
    ]
  }
}
```

- Lives in `.claude/settings.json` — commit it and the team shares the policy

---

## Giving Context: CLAUDE.md

- `CLAUDE.md` at the repo root is loaded into **every** session
- It is the project's standing brief: build commands, conventions, rules
- Run `/init` and the agent drafts one by studying the repo
- Checked into git — the whole team teaches the agent together
- The single highest-leverage file in the whole setup

---

## What Goes in CLAUDE.md

1. How to build, test, and lint — the exact commands
1. Project conventions: style, naming, directory layout
1. Hard rules: what must never be done, what must always be done
1. Pointers to important files and how the pieces fit together
1. Keep it short — it competes for context on every single call

---

## Prompting an Agent Effectively

- State the **goal and the constraints**, not the keystrokes
- Give acceptance criteria: "done when the test passes"
- Reference files by path; paste error output verbatim
- Big task? Ask for a plan first, then approve it step by step
- Correct course early — a wrong direction compounds in a loop

---

## Plan Mode

- The agent explores, reads, and designs — with writes disabled
- You get a reviewable plan before anything is touched
- Approve the plan, and the agent executes it step by step
- Ideal for large refactors, unfamiliar code, and risky changes
- Think first, act second — enforced by the harness, not by hope

---

## Sessions: Continue and Resume

```bash
# continue the most recent session in this project
claude --continue

# pick an older session to resume
claude --resume
```

- A session is the agent's short-term memory — history, plan, decisions
- Resuming restores the full context, days later if needed
- One session per task keeps context clean; `/clear` starts fresh

---

## Context in the CLI

- The context window fills with history and tool results as you work
- `/compact` summarizes the session so far and frees space
- Compaction also happens automatically near the limit
- `/cost` shows what the session has consumed
- Long-lived sessions drift — prefer focused sessions per task

---

## Skills and Slash Commands

- A **skill** packages instructions the agent loads on demand
- Invoked explicitly as `/name`, or picked up when relevant
- Lives in `.claude/skills/<name>/SKILL.md` — versioned with the repo
- Use them for repeatable procedures: release steps, review checklists
- Prompt once, reuse forever — team knowledge becomes executable

---

## Writing Your Own Skill

```markdown
---
name: fix-issue
description: Fix a GitHub issue end to end
---

Given an issue number:

1. Read the issue with `gh issue view`.
1. Locate the relevant code and reproduce the problem.
1. Implement a fix and add a regression test.
1. Run the full test suite.
1. Commit referencing the issue.
```

- Invoke it: `/fix-issue 1234`

---

## Subagents

![subagents](svg/lectures/ai/claude_code/subagents.svg)

---

## When to Use Subagents

- Research and review tasks whose output is a **compact answer**
- Parallel work: five files reviewed by five subagents at once
- Keeping the main session clean — the child's noise never enters it
- Specialized roles: a security reviewer with its own prompt and tools
- Remember the price: a fresh context, a full brief, extra tokens

---

## Defining Custom Subagents

```markdown
---
name: security-reviewer
description: Reviews diffs for security problems.
  Use after any change to auth or input handling.
tools: Read, Grep, Glob
---

You are a security reviewer. Examine the change for
injection, authentication, and data-exposure issues.
Report findings with file, line, and severity.
Never modify files.
```

- One file in `.claude/agents/` — the description tells the main agent when to delegate

---

## Parallel Sessions with Worktrees

![worktrees](svg/lectures/ai/claude_code/worktrees.svg)

---

## Hooks: Deterministic Automation

- Hooks run **your** commands at fixed points in the agent's loop
- Before a tool runs, after it runs, when the agent finishes
- Unlike prompts, hooks are guaranteed — code, not persuasion
- Use them for: formatting after edits, lint gates, custom logging, alerts
- Configured in `.claude/settings.json`, shared with the team

---

## Hook Example

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command",
            "command": "./scripts/format_changed.sh" }
        ]
      }
    ]
  }
}
```

- Every file the agent edits gets formatted — always, automatically

---

## MCP: Adding External Tools

- The Model Context Protocol connects external tool servers to the CLI
- Databases, browsers, issue trackers, internal services — as agent tools
- The agent discovers the tools and calls them like built-ins
- Servers are shared: write once, use from any MCP-capable host
- Project-scoped config in `.mcp.json` travels with the repo

---

## Adding an MCP Server

```bash
# add a local server run as a subprocess
claude mcp add my-db -- npx @example/postgres-mcp

# add a remote server over HTTP
claude mcp add issues --transport http \
    https://mcp.example.com/issues

# list what is configured
claude mcp list
```

---

## Headless Mode

![headless_mode](svg/lectures/ai/claude_code/headless_mode.svg)

---

## Headless Basics

```bash
# one-shot: run a task, print the result, exit
claude -p "summarize the changes in the last 5 commits"

# structured output for scripts
claude -p "list TODO comments as JSON" --output-format json

# constrain what the agent may do
claude -p "run the test suite and report failures" \
    --allowedTools "Bash(npm test:*)" "Read"
```

---

## Claude Code in CI

- The same agent runs in pipelines: an API key and a prompt
- Review pull requests, triage failures, update changelogs
- Constrain tools tightly — CI is unattended by definition
- Treat the output as a *draft*: a human merges, the agent proposes
- Budget every run: turns, tokens, and time, enforced by the pipeline

---

## Cost and Monitoring

- Agent loops multiply tokens — the context is re-sent every turn
- `/cost` per session; provider dashboards for the fleet
- Keep CLAUDE.md lean and tool output clipped — both are billed every call
- Focused sessions beat marathon sessions on both cost and quality
- In CI, cap spend per run and alert on outliers

---

## Safety at the Command Line

- The agent runs with **your** permissions on **your** machine
- Keep the default ask-first mode for anything destructive
- Deny-list secrets: `.env`, keys, credentials — in settings, not in hope
- Fetched web content is untrusted input — the injection lesson applies
- Bypass mode belongs in disposable sandboxes only

---

## The Customization Stack

![customization_stack](svg/lectures/ai/claude_code/customization_stack.svg)

---

## Tips from the Trenches

- Start every project with `/init`, then refine CLAUDE.md as you learn
- Let the agent verify itself: "run the tests before declaring done"
- Use plan mode by reflex on anything unfamiliar or large
- Interrupt early — do not let a wrong plan burn ten minutes
- Turn every repeated instruction into a skill or a CLAUDE.md rule

---

## Anti-Patterns

- **The kitchen-sink session**: one endless session for every task
- **The blind approval**: auto-accepting without reading diffs
- **The bloated brief**: a CLAUDE.md so long it drowns the task
- **The unbounded pipeline**: headless runs with no budget or tool limits
- **The secret leak**: credentials readable by an agent that browses the web

---

## Summary

- Claude Code is the agent loop from lecture one, living in your terminal
- Context is king: CLAUDE.md, focused sessions, lean tool output
- Customize in layers: memory, skills, subagents, hooks, MCP
- Headless mode turns the agent into a scriptable building block
- You stay in control: permissions, budgets, review — always

---

## Questions?

- An agent in the terminal is a colleague, not a vending machine
- Teach it once in CLAUDE.md; correct it early in the loop
- Small sessions, clear briefs, and review — that is the whole craft

## Thank You
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)
