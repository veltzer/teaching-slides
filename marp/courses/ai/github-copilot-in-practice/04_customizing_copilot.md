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

# Customizing Copilot for Your Repository

---

## What This Chapter Covers

- Repository custom instructions: `copilot-instructions.md`
- Path-scoped instruction files with `applyTo`
- Personal custom instructions
- Prompt files: reusable, parameterized prompts
- Custom agents (formerly custom chat modes)
- Verifying that your customization is actually used

---

## Why Customize at All

- Out of the box Copilot knows the language, not your project
- Every chat starts from zero: no memory of last week's correction
- Without instructions you repeat the same context in every prompt
- Instructions are context that is added for you, every time
- Checked into the repository, they are shared by the whole team
- The cheapest quality improvement Copilot offers

---

## The Customization Files

![github_folder](svg/courses/ai/github-copilot-in-practice/04_customizing_copilot/github_folder.svg)

---

## Repository Custom Instructions

- One file: `.github/copilot-instructions.md`
- Plain Markdown, no front matter required
- Added automatically to every chat request in that repository
- Used by chat in the IDE, the coding agent and code review
- Not used to steer inline completions
- Create it from chat: the `Generate Instructions` action drafts one from your code

---

## A Realistic copilot-instructions.md

```markdown
# Project conventions

- Python 3.12, type hints everywhere, `ruff` clean
- Build and test: `make check` (never call pytest directly)
- Web layer is FastAPI; business logic lives in `core/`, never in routes
- Database access only through the repository classes in `core/db/`
- Errors: raise domain exceptions from `core/errors.py`, never bare `Exception`

# Never

- Never add a new dependency without saying so explicitly
- Never edit files under `generated/`
```

---

## What to Put in It

- Build, test and lint commands, exactly as CI runs them
- Architecture in a few lines: which layer lives where
- Naming and style rules that a linter does not enforce
- Libraries to prefer and libraries that are banned
- "Never do this" rules learned from real mistakes
- Pointers to key files (`see docs/architecture.md`)

---

## What Not to Put in It

- Long prose: every line costs context on every request
- Things the code already shows clearly
- Personal taste ("I like short answers")
- Secrets, internal URLs with tokens, customer data
- Rules about the response format of one specific task
- Contradictions: two rules that cannot both be followed

---

## What Copilot Ignores No Matter How Nicely You Ask

- Instructions are context, not configuration
- "Always be 100% correct" changes nothing
- "Never hallucinate" changes nothing
- Rules that need knowledge the model does not have
- Instructions to reach things it cannot reach (private wiki, VPN)
- Very long files: rules at the bottom get diluted
- Enforce hard rules with linters and CI, not with prose

---

## Keep It Short and Concrete

| Weak instruction | Strong instruction |
|---|---|
| Write good tests | Tests use `pytest` fixtures from `tests/conftest.py` |
| Follow our style | Functions over 40 lines must be split |
| Be careful with the database | All queries go through `core/db/repo.py` |
| Use modern Python | Use `pathlib`, never `os.path` |
| Handle errors properly | Raise `NotFoundError`, never return `None` |

---

## Path-Scoped Instruction Files

- Live in `.github/instructions/` as `NAME.instructions.md`
- Front matter `applyTo` holds a glob of files the rules apply to
- Included automatically when a file in scope is in the context
- Optional `description` helps the agent decide when it is relevant
- Keep the repository-wide file short and push detail here
- Also used by the coding agent and code review

---

## An Instruction File with `applyTo`

```markdown
---
applyTo: "tests/**/*.py"
description: "Conventions for Python tests"
---

- Use `pytest`, never `unittest.TestCase`
- One behavior per test; name it `test_<unit>_<behavior>`
- Use the `client` and `db` fixtures from `tests/conftest.py`
- No sleeping: use the `frozen_clock` fixture for time
- Never mock the module under test
```

---

## Different Rules for Different Code

| File | `applyTo` | Typical rules |
|---|---|---|
| `tests.instructions.md` | `tests/**` | fixtures, naming, no sleeps |
| `frontend.instructions.md` | `web/src/**/*.tsx` | components, hooks, styling system |
| `sql.instructions.md` | `**/*.sql` | migration style, no `SELECT *` |
| `generated.instructions.md` | `generated/**` | never edit, regenerate instead |
| `docs.instructions.md` | `docs/**/*.md` | tone, heading levels |

---

## Layering Instructions

![instruction_layers](svg/courses/ai/github-copilot-in-practice/04_customizing_copilot/instruction_layers.svg)

---

## How the Layers Combine

- Personal, repository and matching path files are all included
- They are concatenated, not merged: the model sees all of them
- There is no strict override order the model is forced to follow
- Conflicting rules produce inconsistent answers
- Write each layer so it never contradicts the others
- `AGENTS.md` at the repository root is read as well, mostly by agents

---

## Personal Custom Instructions

- Preferences that follow you across repositories
- In the IDE: user-level instruction files in your profile
- On the website: personal instructions in Copilot chat settings
- Good uses: answer language, explanation depth, your shell
- Bad uses: project conventions (those belong to the team)
- Your teammates never see them, so never rely on them for shared rules

---

## Keeping Personal and Team Instructions Apart

- Team file says what the code must look like
- Personal file says how you like to be talked to
- Never restate team rules personally "to be safe": drift follows
- If your personal rule fights the team rule, change one of them
- When answers look odd, disable personal instructions and retry
- Rule of thumb: would a new teammate need it? Then it is a team rule

---

## Prompt Files

- Reusable prompts stored as `.github/prompts/NAME.prompt.md`
- Run them in chat by typing `/NAME`
- Front matter sets the mode, the model and the tools
- Variables make them parameterized: `${input:name}`, `${selection}`, `${file}`
- Checked in: a team workflow becomes a runnable command
- User-level prompt files exist too, for your own routines

---

## A Prompt File

```markdown
---
mode: agent
description: "Add a REST endpoint with tests"
tools: ["codebase", "editFiles", "runTests"]
---

Add a new endpoint `${input:route:e.g. GET /orders/{id}}`.

1. Follow the existing patterns in [routes](../../app/routes/)
1. Put logic in `core/`, keep the route thin
1. Add tests in `tests/api/` and run them until they pass
1. Summarize changed files at the end
```

---

## Running a Prompt File

![prompt_flow](svg/courses/ai/github-copilot-in-practice/04_customizing_copilot/prompt_flow.svg)

---

## Turning a Team Workflow into a Prompt

1. Pick a task the team does weekly the same way
1. Write down the steps a senior developer would follow
1. Link the reference files instead of pasting them
1. Replace the variable parts with `${input:...}` placeholders
1. Run it on three real cases and fix what goes wrong
1. Commit it and announce the `/name` to the team

---

## Good Candidates for Prompt Files

- Scaffold a new endpoint, component or migration
- Write a release note from the commits since a tag
- Review the current diff against the security checklist
- Explain a module for onboarding
- Generate test cases for the selected function
- Prepare a pull request description

---

## Instructions vs Prompt Files

| Question | Instructions | Prompt file |
|---|---|---|
| When is it used? | Every request, automatically | Only when you type `/name` |
| What does it hold? | Rules and conventions | A task and its steps |
| Parameters? | No | Yes, `${input:...}` |
| Picks tools or model? | No | Yes, in front matter |
| Cost of being long | Paid on every request | Paid only when run |

---

## Where Does This Content Go

![which_file](svg/courses/ai/github-copilot-in-practice/04_customizing_copilot/which_file.svg)

---

## Custom Agents

- Package a persona, a tool set and instructions under one name
- Stored as `.github/agents/NAME.agent.md`
- Formerly called custom chat modes (`.github/chatmodes/*.chatmode.md`)
- Selected from the agent dropdown in the chat view, next to `Ask`, `Edit`, `Agent`, `Plan`
- Stays active for the whole conversation, unlike a prompt file
- Typical agents: planner, reviewer, documentation writer

---

## A Custom Agent

```markdown
---
description: "Plan a change without touching code"
tools: ["codebase", "search", "fetch", "githubRepo"]
model: "Claude Sonnet 4.5"
---

You are a planning assistant. Never edit files.

- Read the relevant code before proposing anything
- Output a numbered plan: files to change, risks, tests to add
- Ask one clarifying question if the request is ambiguous
```

---

## Instructions, Prompt Files and Custom Agents

| | Instructions | Prompt file | Custom agent |
|---|---|---|---|
| Activated by | Automatically | `/name` | Agent dropdown |
| Lifetime | Every request | One request | Whole conversation |
| Restricts tools | No | Yes | Yes |
| Best for | Conventions | Repeatable tasks | Roles and personas |

---

## Seeing Which Instructions Were Used

- Expand the `References` list under a chat response
- Instruction files that were included appear there by name
- Path-scoped files appear only if a matching file was in context
- No reference means the file was not sent: the model never saw it
- Check this first, before rewording an instruction

---

## Debugging Instructions That Are Not Picked Up

- Wrong location or name: must be `.github/copilot-instructions.md`
- Wrong suffix: `.instructions.md` and `.prompt.md` are required
- Setting `github.copilot.chat.codeGeneration.useInstructionFiles` turned off
- Setting `chat.promptFiles` turned off, or prompt folder not configured
- `applyTo` glob does not match: test it against a real path
- Organization policy may disable some customization features
- Use the chat diagnostics view to see what was loaded

---

## Verifying Behavior, Not Just Loading

1. Write a rule with a visible effect (a naming convention)
1. Ask for code the rule should shape
1. Confirm the file is in `References`
1. Confirm the code follows the rule
1. Repeat with a teammate's machine to catch personal-only settings
1. Keep a short checklist of these probes in the repository

---

## Key Takeaways

- `copilot-instructions.md` is short, concrete and always on
- Path-scoped files carry the detailed rules for parts of the code
- Personal instructions are for taste, never for team rules
- Prompt files turn repeatable tasks into `/commands`
- Custom agents package a role with its tools for a whole session
- Always check `References` before blaming the model
