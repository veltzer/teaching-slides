---
tags:
  - data-and-ai:ai
  - data-and-ai:generative-ai
  - concepts:code-generation
  - tools:github
  - practices:productivity
level: intermediate
category: ai
audience:
  - audiences:developers
  - audiences:team-leads
  - audiences:devops

---

# Orientation and Setup

---

## What This Chapter Covers

- The Copilot product family and its surfaces
- Where Copilot runs and which IDE this course uses
- Plans, premium requests and model multipliers
- Signing in and verifying that Copilot really works
- Organization policies that change what you see
- The model picker: fast models vs deep models

---

## One License, Many Surfaces

![surfaces](svg/courses/ai/github-copilot-in-practice/01_orientation_and_setup/surfaces.svg)

---

## The Product Family

- Completions: ghost text while you type
- Chat: questions and answers in the IDE and on `GitHub`
- Edit mode: multi-file changes you review before accepting
- Agent mode: Copilot runs commands, reads output and iterates
- Coding agent: works on `GitHub` from an issue, returns a pull request
- Code review, the `CLI`, and pull request summaries
- All of it billed against one Copilot seat

---

## Where Copilot Runs

| Environment | Completions | Chat | Agent mode |
| --- | --- | --- | --- |
| `VS Code` | yes | yes | yes |
| `JetBrains` `IDEs` | yes | yes | yes |
| `Visual Studio` | yes | yes | yes |
| `Neovim` | yes | plugin | no |
| `Xcode` | yes | yes | yes |
| `GitHub` website | no | yes | coding agent |
| Terminal (`copilot` `CLI`) | no | yes | yes |

---

## Why This Course Uses VS Code

- New Copilot features usually ship in `VS Code` first
- Agent mode, `MCP`, prompt files and custom agents are most complete there
- Settings live in plain `JSON`, easy to share and diff
- The same concepts transfer to `JetBrains` and `Visual Studio`
- Where another IDE differs, the slide says so

---

## Plans at a Glance

| Plan | Who it is for | Premium requests per month |
| --- | --- | --- |
| Free | individuals trying it out | 50 (limited completions) |
| Pro | individual developers | 300 |
| Pro+ | heavy individual users | 1500 |
| Business | organizations | 300 per seat |
| Enterprise | enterprises on `GHEC` | 1000 per seat |

At time of writing — check docs.github.com for current numbers.

---

## Which Features Need Which Plan

| Feature | Free | Pro / Pro+ | Business / Enterprise |
| --- | --- | --- | --- |
| Completions and chat | limited | yes | yes |
| Agent mode in the IDE | yes | yes | yes |
| Coding agent | no | yes | yes, if policy allows |
| Copilot code review | limited | yes | yes |
| Policies and content exclusion | no | no | yes |
| Audit log and usage metrics | no | no | yes |

---

## Premium Requests and Multipliers

- Completions and the included base model do not use premium requests on paid plans
- Every prompt you send with a premium model costs `1 x multiplier`, however many tool calls follow
- Cheap, fast models have small multipliers; frontier models have large ones
- The coding agent and code review also consume premium requests
- Over the allowance: requests fail or are billed, depending on the budget setting
- The multiplier table changes with every new model — read it, do not memorize it

---

## Getting a Seat in an Organization

- An owner or billing manager assigns seats to users or teams
- Assignment by team is easiest to maintain
- The seat comes with the organization's policies attached
- Personal and organization seats can coexist; the organization one wins in its repositories
- Check your status at `github.com/settings/copilot`

---

## Signing In from VS Code

1. Install the `GitHub Copilot` and `GitHub Copilot Chat` extensions
1. Click the Copilot icon in the status bar and choose sign in
1. Authorize `VS Code` in the browser with the account that has the seat
1. Confirm the status bar icon shows Copilot as active
1. Open the chat view with `Ctrl+Alt+I`

---

## Verifying It Actually Works

- Completions: type a function signature and wait for ghost text
- Chat: ask `@workspace what does this repository do?`
- Agent mode: switch the chat to Agent and ask it to run the tests
- Check the `GitHub Copilot` output channel for errors
- A silent status bar icon usually means the wrong account

---

## Policies That Change What You See

![policies](svg/courses/ai/github-copilot-in-practice/01_orientation_and_setup/policies.svg)

---

## Symptoms of a Policy

- A model is missing from the picker: the organization disabled it
- Agent mode or `MCP` is greyed out: a preview or agent policy is off
- No suggestions in some files: content exclusion is active
- Suggestions vanish mid-line: the public code filter blocked a match
- When in doubt, ask the organization owner before debugging your setup

---

## The Model Picker

- The chat input has a model dropdown; the choice applies per conversation
- Completions use a separate, smaller model chosen in settings
- `Auto` lets Copilot pick a model and gives a multiplier discount
- The organization decides which models appear at all
- Switching models mid-conversation keeps the history

---

## Choosing a Model per Task

| Task | Model kind | Why |
| --- | --- | --- |
| Quick question, rename, small fix | fast, cheap | latency matters more than depth |
| Explaining unfamiliar code | mid-range | good reasoning, low cost |
| Multi-file refactor in agent mode | strong reasoning | fewer wrong turns |
| Hard bug, design decision | deep reasoning | worth the multiplier |
| Long agent session | strong but not the most expensive | cost adds up per turn |

---

## Watching Your Budget

- `github.com/settings/copilot` shows premium requests used this month
- The IDE status bar menu shows the current usage
- Set a budget for paid overage instead of an unlimited one
- Default to a cheap model and escalate deliberately
- A day of agent work with a frontier model can consume dozens of requests

---

## Key Takeaways

- Copilot is one seat with many surfaces — pick the surface per task
- The plan sets quotas; the organization policy sets what you can actually use
- Verify completions, chat and agent mode before blaming the tool
- Treat the model picker as a cost and quality dial
