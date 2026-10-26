---
tags:
  - data-and-ai:ai
  - data-and-ai:generative-ai
  - data-and-ai:agents
  - concepts:code-generation
  - practices:productivity
level: intermediate
category: ai
audience:
  - audiences:developers
  - audiences:team-leads

---

# Working with Kiro
## The Spec-Driven Agentic IDE from AWS
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## Overview

![title](svg/lectures/ai/kiro/title.svg)

---

## What This Lecture Covers

1. What `Kiro` is, installing it, and the `.kiro/` workspace it creates
1. Chat modes, execution modes, checkpoints, and context providers
1. Steering files: always-on project knowledge for the agent
1. Specs: driving a feature from one sentence to executed tasks
1. Agent hooks and `MCP` servers
1. The `Kiro` CLI, custom agents, and headless use in scripts

---

## What Kiro Is

- An agentic IDE from AWS, built on Code OSS, so it looks and feels like `VS Code`
- The agent lives in the side panel; it reads, edits, runs commands, and asks before risky steps
- Four building blocks make it more than a chat window: specs, steering, hooks, and `MCP`
- A companion CLI runs the same agent in a terminal and in CI
- This lecture is about *the tool*; the method itself is covered in the *Spec-Driven Development with AI* course

---

## Installing and Signing In

- Download the installer for macOS, Windows, or Linux from the `Kiro` site
- Sign in with Google, GitHub, an AWS Builder ID, or IAM Identity Center for company accounts
- On first launch, import your `VS Code` settings, keybindings, and extensions
- Extensions come from the Open VSX registry, not the Microsoft marketplace
- Open a folder: `Kiro` treats the open workspace as the agent's world

---

## The Workspace Kiro Creates

![workspace_layout](svg/lectures/ai/kiro/workspace_layout.svg)

---

## Everything Lives in `.kiro/`

- `specs/<feature>/`: the three spec files for one feature
- `steering/`: `Markdown` files the agent reads before it does anything
- `hooks/`: automations triggered by IDE events
- `settings/mcp.json`: the tool servers available to the agent
- `agents/`: custom agents for the CLI
- All of it is plain text in your repository: review it, diff it, commit it

---

## Two Chat Modes, Two Execution Modes

![modes](svg/lectures/ai/kiro/modes.svg)

---

## Vibe Mode

- Conversational: describe what you want, the agent explores and acts
- Best for small changes, exploration, questions about the code, and quick fixes
- The agent reads files on its own; you do not paste code into the chat
- Switch to Spec mode when the work is big enough to deserve a plan
- Both modes share steering, hooks, and `MCP`; only the workflow differs

---

## Autopilot and Supervised

- **Supervised**: every file edit and command waits for your approval
- **Autopilot**: the agent edits files freely and runs commands it is trusted to run
- Toggle in the chat panel; start in Supervised on an unfamiliar codebase
- Commands you approve can be added to a trusted list, so autopilot stops asking for them
- Risky commands still ask, even in autopilot: deletes, pushes, package installs

---

## Checkpoints

- Every agent turn records a checkpoint of the files it touched
- Restore a checkpoint to roll the workspace back to that point in the conversation
- Cheaper than `git stash` when an agent run went sideways
- Checkpoints are per conversation; `git` is still your durable history
- Habit: review the diff after each turn, restore early rather than argue with the agent

---

## Giving the Agent Context

![context_providers](svg/lectures/ai/kiro/context_providers.svg)

---

## Context Providers in Practice

- Type `#` in the chat to attach context explicitly
- `#File` and `#Folder`: the exact code you are talking about
- `#Codebase`: let the agent search the whole repository for relevant files
- `#Problems`: the diagnostics panel, so "fix these errors" needs no copying
- `#Terminal` and `#Git Diff`: the last command output, the current change set
- `#URL`: fetch a documentation page into the conversation

---

## Steering Files

- `Markdown` files in `.kiro/steering/`, loaded into the agent's context automatically
- The standing brief for the project: product facts, stack, conventions, hard rules
- Replaces the paragraph you used to paste at the start of every chat
- Committed to `git`, so the whole team teaches the agent together
- Keep each file focused; the agent reads them on every request

---

## Generating the Default Steering

- "Generate steering docs" in the panel makes three files by studying the repository:
    - `product.md`: what the product does and for whom
    - `tech.md`: languages, frameworks, build and test commands
    - `structure.md`: directory layout and where things go
- Treat them as a first draft: fix what the agent guessed wrong
- Add your own files alongside: `testing.md`, `api-conventions.md`, `security.md`

---

## Steering Inclusion Modes

![steering_inclusion](svg/lectures/ai/kiro/steering_inclusion.svg)

---

## A Steering File

```markdown
---
inclusion: fileMatch
fileMatchPattern: "src/api/**/*.py"
---

# API conventions

- Every endpoint is defined with `FastAPI` and typed `pydantic` models
- Errors return the `ErrorResponse` schema, never a bare string
- New endpoints need a test in `tests/api/` before the task is done
```

- `always`: loaded in every chat; `fileMatch`: only when matching files are in play
- `manual`: loaded only when you reference it with `#` in the chat

---

## Referencing Files from Steering

```markdown
---
inclusion: always
---

# Data model

The canonical schema is in #[[file:schema/openapi.yaml]].
Never invent fields that are not in that file.
```

- `#[[file:...]]` pulls the file into context whenever the steering file is loaded
- Point at the source of truth instead of copying it into the steering file
- Good targets: `OpenAPI` specs, schema files, the lint configuration

---

## Specs: From One Sentence to Tasks

![spec_flow](svg/lectures/ai/kiro/spec_flow.svg)

---

## Starting a Spec

- Switch the chat to Spec mode and describe the feature in a sentence or two
- `Kiro` creates `.kiro/specs/<feature>/` and writes `requirements.md` first
- Nothing moves to the next stage until you approve the current one
- You can also start from existing code: "write a spec for the current export module"
- One spec per feature; the folder name becomes the feature's identity

---

## requirements.md

```markdown
# Requirements

## Requirement 1: Export orders as CSV

**User story:** As an analyst, I want to export filtered orders
so that I can analyze them in a spreadsheet.

### Acceptance criteria

1. WHEN the user clicks Export THEN the system SHALL stream a CSV
   containing exactly the rows currently filtered
1. IF the result exceeds 100,000 rows THEN the system SHALL
   offer an asynchronous export instead
```

- Acceptance criteria use the `EARS` form; `Kiro` writes them, you check them

---

## Reviewing Requirements

- Read every criterion as a test you could write; if you cannot, it is vague
- Refine in the chat: "add a criterion for an empty result set"
- Or edit the file directly; the agent picks up your edits on the next turn
- Approve with the button in the chat: `Kiro` moves on to `design.md`
- Time spent here is the cheapest time in the whole feature

---

## design.md

- Architecture and component overview for this feature only
- Interfaces: function signatures, request and response shapes, data model changes
- Sequence diagrams in `Mermaid` for the main flows
- Error handling and a testing strategy section
- The agent reads the existing code before writing it, so the design fits what is there
- Approve to move on to the implementation plan

---

## tasks.md

```markdown
# Implementation plan

- [ ] 1. Add the `OrderExport` service
    - [ ] 1.1 Write the CSV serializer with streaming output
    - [ ] 1.2 Unit tests for the serializer
    - _Requirements: 1.1_
- [ ] 2. Expose the export endpoint
    - [ ] 2.1 Add `POST /orders/export` with the filter payload
    - [ ] 2.2 Return the asynchronous job for large results
    - _Requirements: 1.1, 1.2_
```

- Every task points back to the requirements it satisfies

---

## Executing Tasks

- Open `tasks.md`: each task shows a "Start task" action in the editor
- Run one task at a time; the agent implements, runs tests, and ticks the box
- Tasks keep a status: not started, in progress, completed
- Review the diff after each task, as you would a small pull request
- A failing task is a signal: fix the design or the requirement, not just the code

---

## Keeping Specs Alive

- Requirements changed? Edit `requirements.md` and ask to update design and tasks
- "Update tasks" re-plans the remaining work without touching finished tasks
- Commit the spec folder with the code; the spec is the feature's documentation
- Specs for existing code document what is there before you change it
- A spec nobody updates is a lie in the repository; delete it or fix it

---

## Agent Hooks

![hooks_flow](svg/lectures/ai/kiro/hooks_flow.svg)

---

## Creating a Hook

- Open the Agent Hooks section in the `Kiro` panel and describe the automation in plain language
- `Kiro` writes the hook file; you adjust the trigger, the pattern, and the prompt
- Triggers: a file is edited, created, or deleted; a prompt is submitted; or a manual button
- Actions: send a prompt to the agent, or run a shell command
- Hooks live in `.kiro/hooks/` and are shared through `git` like everything else

---

## A Hook File

```json
{
  "enabled": true,
  "name": "Keep tests in sync",
  "description": "Update unit tests when a source module changes",
  "version": "1",
  "when": {
    "type": "fileEdited",
    "patterns": ["src/**/*.py"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "A source file changed. Update its tests; do not touch other modules."
  }
}
```

---

## Useful Hook Patterns

- **On save**: update the tests or the docstring of the edited module
- **On create**: scaffold a new component from the project's template
- **On delete**: find and remove dangling imports and references
- **Manual button**: "review the current diff for security issues"
- **On prompt**: inject a reminder of the coding standard into every request
- Keep hook prompts narrow; a hook that rewrites the world on every save is noise

---

## MCP Servers

![mcp_scopes](svg/lectures/ai/kiro/mcp_scopes.svg)

---

## Configuring MCP

```json
{
  "mcpServers": {
    "aws-docs": {
      "command": "uvx",
      "args": ["awslabs.aws-documentation-mcp-server@latest"],
      "env": { "FASTMCP_LOG_LEVEL": "ERROR" },
      "disabled": false,
      "autoApprove": ["search_documentation", "read_documentation"]
    }
  }
}
```

- Workspace servers in `.kiro/settings/mcp.json`, personal ones in `~/.kiro/settings/mcp.json`

---

## Working with MCP Tools

- The `MCP` section of the panel lists servers, their tools, and connection state
- `autoApprove` names tools that may run without asking; leave write tools off that list
- `disabled: true` keeps a server configured but off, handy for expensive servers
- Servers launched with `uvx` or `npx` need those tools installed on the machine
- Logs for a failing server are in the output panel; most failures are a missing binary or key

---

## Powers

- Powers bundle an `MCP` server with steering and hooks for one tool or service
- Install one from the catalog instead of writing the configuration by hand
- The agent loads a power's instructions only when the task calls for it, saving context
- Typical powers: cloud providers, payment APIs, design tools, databases
- Write your own power to package your team's internal services for the agent

---

## Kiro CLI

![ide_cli_shared](svg/lectures/ai/kiro/ide_cli_shared.svg)

---

## CLI Basics

```bash
# install, then sign in once
kiro-cli login

# interactive chat in the current project
cd my-project
kiro-cli chat

# start with a task already in hand
kiro-cli chat "explain how the build works in this repo"
```

- The CLI reads the same `.kiro/steering/`, specs, hooks, and `MCP` configuration as the IDE

---

## CLI Slash Commands

- `/context`: show what is in the context window and add or remove files
- `/tools`: list tools and set which ones are trusted to run without asking
- `/agent`: switch to a custom agent for the rest of the session
- `/model`: pick the model for this session
- `/compact`: summarize the conversation so far to free up context
- `/usage`: how much context and how many credits the session has used
- `/save` and `/load`: persist a conversation and pick it up later

---

## Custom Agents in the CLI

```json
{
  "name": "reviewer",
  "description": "Read-only code reviewer",
  "prompt": "Review the diff for bugs and missing tests. Never edit files.",
  "tools": ["read", "shell"],
  "allowedTools": ["read"],
  "resources": [
    "file://.kiro/steering/**/*.md",
    "file://docs/review-checklist.md"
  ]
}
```

- Lives in `.kiro/agents/reviewer.json`; run it with `kiro-cli chat --agent reviewer`

---

## Kiro in Scripts and CI

```bash
# one shot, no prompts, output to stdout
kiro-cli chat --no-interactive --trust-all-tools \
  --agent reviewer \
  "Review the changes in this branch against docs/review-checklist.md"
```

- `--no-interactive` makes the agent answer once and exit
- `--trust-all-tools` belongs in a sandboxed runner, never on your laptop
- Pin the agent and its allowed tools; the CI job is the permission boundary
- Pipe the output into a pull request comment or a build artifact

---

## The Autonomous Agent

- A cloud-hosted `Kiro` agent connected to a repository, currently in preview
- Assign it an issue; it works from the repository's steering and specs and opens a pull request
- It runs in its own environment, so your laptop is not the execution host
- Same artifacts as the IDE: a good `.kiro/` directory makes the remote agent useful
- Review its pull requests like any contributor's; it is not exempt from the rules

---

## Plans, Credits, Models

- Usage is metered in credits; a free tier includes a monthly allowance, paid tiers add more
- Spec mode and autopilot runs cost more than a single chat answer
- The model picker lets you trade speed for capability per conversation
- Watch usage in the panel; long autopilot sessions on big repositories burn credits fast
- Company accounts through IAM Identity Center bring central billing and policy

---

## A Daily Workflow

1. Open the project; make sure steering reflects the current state of the code
1. Small change: Vibe mode, Supervised, attach `#File`, review the diff
1. Real feature: Spec mode; approve requirements, design, tasks in turn
1. Execute tasks one at a time; let hooks keep tests and docs in sync
1. Commit code and spec together; the pull request shows both
1. Repeated instruction? Move it into steering or a hook

---

## Anti-Patterns

- **Autopilot too early**: letting an unfamiliar codebase be edited unsupervised
- **Spec theater**: approving `requirements.md` without reading it
- **Steering bloat**: a dozen `always` files that drown every request
- **Hook storms**: hooks that trigger the agent on every keystroke-level save
- **Stale specs**: `tasks.md` ticked by hand instead of by executing the task
- **Secrets in `mcp.json`**: API keys committed with the workspace configuration

---

## Summary

- `Kiro` is a `VS Code`-shaped IDE with an agent, specs, steering, hooks, and `MCP` built in
- Steering teaches the agent once; specs turn a feature into reviewed artifacts and tasks
- Hooks automate the housekeeping; `MCP` and powers add tools
- The CLI and the autonomous agent reuse the same `.kiro/` directory outside the IDE
- You stay in control through Supervised mode, trusted commands, checkpoints, and review
