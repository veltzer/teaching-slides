---
tags:
  - data-and-ai:ai
  - data-and-ai:llm
  - practices:productivity
level: intermediate
category: ai
audience:
  - audiences:developers
  - audiences:senior-developers
  - audiences:devops

---

# Configuring Claude

---

## What This Chapter Covers

- Two layers of configuration
- Global settings
- Project settings
- CLAUDE.md and memory
- Permissions, hooks and safety

---

## Two Layers Of Configuration

- User level: your machine, all projects
- Project level: this repo, all users
- Both can override defaults
- Order of precedence matters

---

## Where Claude Looks

- User: `~/.claude/settings.json`
- Project: `.claude/settings.json`
- Local: `.claude/settings.local.json`
- Environment variables on top

---

## What Belongs In Each Layer

- User: personal taste, theme, keys
- Project: shared rules, allowed tools
- Local: machine quirks, secrets paths
- Never commit secrets

---

## Configuration Layers

![config_layers](svg/courses/ai/claude-workshop/02_configuration/config_layers.svg)

---

## The User settings.json

- Default model selection
- Theme and status line
- Editor integration
- Personal allowlists

---

## Default Model Selection

- Pick Sonnet for daily driving
- Override per session with `/model`
- Set per project when needed
- Match cost to task

---

## Theme And Status Line

- Light, dark and high contrast themes
- Status line shows model and tokens
- Customize with a shell command
- Use `/statusline` to configure

---

## Editor Integration

- VS Code and JetBrains extensions
- Inline diff review
- File jump from the chat
- Diagnostics integration

---

## The Project settings.json

- Checked into git
- Shared across the team
- Defines project rules
- The team agrees on this file

---

## settings.local.json

- Not checked in
- For your machine only
- Local secrets and overrides
- Add it to `.gitignore`

---

## Project Environment Variables

- Set in `.claude/settings.json`
- Available to tools and hooks
- No secrets in committed files
- Use OS env vars for secrets

---

## Sharing Configuration

- Commit the project settings
- Document the conventions in CLAUDE.md
- New joiners get the rules for free
- Treat config as code

---

## CLAUDE.md

- Plain markdown, lives in repo
- Always loaded into context
- Tells Claude how to behave here
- Keep it short and high signal

---

## What To Put In CLAUDE.md

- Coding style and conventions
- Build and test commands
- "Do not do this" rules
- Important file locations

---

## What Not To Put In CLAUDE.md

- Long histories or war stories
- Things obvious from the code
- Personal preferences
- Anything you would not want every prompt to see

---

## Per Directory CLAUDE.md

- Subdirectory CLAUDE.md is also loaded
- Use for area-specific rules
- Backend rules vs frontend rules
- Avoid duplication with the root

---

## CLAUDE.md At A Glance

![claude_md](svg/courses/ai/claude-workshop/02_configuration/claude_md.svg)

---

## Permissions And Safety

- Every tool can be approved or denied
- Denials apply this session
- Allowlists are durable
- Read-only tools rarely need prompts

---

## Approving And Denying Tools

- Inline prompt when needed
- "Allow once" vs "always allow"
- Deny when you do not understand
- Revisit allowlists periodically

---

## Allowlisting Commands

- Cut down on prompts for routine commands
- Pin specific shapes, not free `bash`
- `npm run build` not `npm *`
- Review the list in code review

---

## Permission Flow

![permissions_flow](svg/courses/ai/claude-workshop/02_configuration/permissions_flow.svg)

---

## Hooks

- Shell commands the harness runs
- Triggered by events: stop, tool use, edit
- Configured in `settings.json`
- Cannot be enforced from memory alone

---

## What Hooks Can And Cannot Do

- Can: lint, format, notify, block
- Cannot: change the model's mind
- Use them to enforce rules deterministically
- Failing hook blocks the action

---

## Hooks In The Session Lifecycle

![hooks_lifecycle](svg/courses/ai/claude-workshop/02_configuration/hooks_lifecycle.svg)

---

## Working With Many Repos

- Each repo has its own CLAUDE.md
- Each repo has its own settings
- Context does not leak across repos
- Different model per project is fine

---

## Verifying Configuration

- `/config` shows current settings
- `/permissions` shows allowlists
- Inspect actual files in `.claude/`
- Test a small command after changes

---

## Hands-On Exercise

- Add a CLAUDE.md to your repo
- Allowlist your build command
- Add a hook that runs the linter
- Re-run a task and see the change
