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

# Agent Mode Deep Dive and MCP

---

## What This Chapter Covers

- How agent mode uses its built-in tools
- Adding `MCP` servers at workspace and user level
- The `GitHub` `MCP` server, browser automation and databases
- Controlling the blast radius: tools, approvals, prompt injection
- `AGENTS.md` and instructions in agent mode
- Agent workflows that work, and when to take over

---

## Agent Mode and Its Tools

![agent_tools](svg/courses/ai/github-copilot-in-practice/06_agent_mode_deep_dive_and_mcp/agent_tools.svg)

---

## The Agent Loop

- The model never touches your machine directly
- It emits a tool call: name plus `JSON` arguments
- `VS Code` runs the tool and returns the result as text
- The model reads the result and decides the next call
- The loop ends when the model answers instead of calling a tool
- Every capability the agent has is a tool you can see and switch off

---

## The Built-in Tool Set

| Tool group | What it does | Example |
| --- | --- | --- |
| `#codebase`, `#search` | Find code by meaning or text | Locate the auth middleware |
| `#editFiles`, `#new` | Create and change files | Add a new endpoint |
| `#runInTerminal` | Run shell commands | `npm install`, `make` |
| `#runTests`, `#testFailure` | Run tests, read failures | Fix the red test |
| `#problems` | Read compiler and lint diagnostics | Clear type errors |
| `#fetch` | Download a web page | Read an `API` doc |

---

## Watching a Session Step by Step

- Each tool call appears in the chat as a collapsible step
- Expand a step to see the exact arguments and the raw output
- Terminal commands run in a visible terminal you can inspect
- Edited files show inline diffs with Keep and Undo
- The context indicator shows how full the window is getting
- Use the chat debug view to see the full request when in doubt

---

## Reading the Trace Critically

1. Did it search before editing, or guess file names?
1. Did it run the tests, or only claim they pass?
1. Did it read the error output, or retry blindly?
1. Did it touch files outside the task?
1. Did it change a test to make it pass?

---

## What MCP Adds

- `MCP`: Model Context Protocol, an open standard for tools
- A server exposes tools, resources and prompts
- `VS Code` is the client; agent mode calls the server's tools
- Transports: `stdio` (local process) and `HTTP` (remote)
- The same server works in `VS Code`, the `CLI` and the coding agent
- Build once, plug into every client

---

## Workspace vs User Configuration

![config_scopes](svg/courses/ai/github-copilot-in-practice/06_agent_mode_deep_dive_and_mcp/config_scopes.svg)

---

## A Workspace `mcp.json`

```json
{
  "inputs": [{ "type": "promptString", "id": "pg-url",
               "description": "Postgres URL", "password": true }],
  "servers": {
    "github": { "type": "http",
                "url": "https://api.githubcopilot.com/mcp/" },
    "playwright": { "type": "stdio", "command": "npx",
                    "args": ["@playwright/mcp@latest"] },
    "postgres": { "type": "stdio", "command": "npx",
                  "args": ["-y", "@modelcontextprotocol/server-postgres",
                           "${input:pg-url}"] }
  }
}
```

---

## Secrets in MCP Configuration

- Never commit a token into `.vscode/mcp.json`
- `inputs` with `"password": true` prompt once and store securely
- Reference them as `${input:id}` in `args`, `env` or `headers`
- `envFile` can point to a git-ignored `.env` file
- Remote servers like `GitHub` use `OAuth` sign-in instead of tokens
- Rotate any token that ever appeared in a commit

---

## Installing and Starting a Server

1. Add it from the `MCP` gallery in the Extensions view, or
1. Run `MCP: Add Server` from the command palette, or
1. Edit `.vscode/mcp.json` by hand
1. Click Start in the code lens above the server entry
1. Check the output with `MCP: List Servers` then Show Output
1. Open the tools picker and confirm the new tools are listed

---

## When a Server Does Not Appear

- `npx` or `uvx` not on the `PATH` that `VS Code` inherited
- The server crashed on startup: read its output channel
- `JSON` error in `mcp.json`: the editor underlines it
- Organization policy disables `MCP` servers in Copilot
- Too many tools enabled: `VS Code` caps the count per request
- Restart the server after changing its configuration

---

## The GitHub MCP Server

- Official server maintained by `GitHub`
- Remote at `https://api.githubcopilot.com/mcp/`, or run locally in `Docker`
- Tools for issues, pull requests, code search, `Actions` and security alerts
- Toolsets let you load only the groups you need
- Read-only mode for exploration without risk
- Authenticates as you: it can do whatever your account can do

---

## GitHub MCP from Chat

```markdown
List open issues labelled "bug" in this repo that
have no assignee, newest first.

Why did the last CI run on main fail? Show the
failing step's log and propose a fix.

Open a draft pull request from this branch with a
summary of the changes in the description.
```

---

## Useful MCP Servers

| Server | Transport | Typical use |
| --- | --- | --- |
| `GitHub` | `HTTP` | Issues, pull requests, `CI` logs |
| `Playwright` | `stdio` | Drive a browser, check the `UI` |
| `Postgres` / `SQLite` | `stdio` | Inspect schema, run queries |
| `Context7` | `HTTP` | Current library documentation |
| `Azure` / `AWS` | `stdio` | Cloud resource queries |
| Filesystem | `stdio` | Files outside the workspace |

---

## Browser Automation in the Loop

- `Playwright` `MCP` lets the agent open pages and click
- It reads the accessibility tree, not screenshots, by default
- Loop: change the code, reload the page, check the result
- Good for: reproducing a `UI` bug, verifying a form flow
- Point it at a local dev server, never at production
- Treat page text as untrusted input to the model

---

## Databases in the Loop

- The agent reads the real schema instead of guessing columns
- Write a migration, then query to verify it applied
- Connect with a read-only role whenever possible
- Use a local or disposable database, never production
- Query results go into the model context: mind sensitive data

---

## Enabling and Disabling Tools

- The tools picker lists built-in, extension and `MCP` tools
- Uncheck whole servers or individual tools per chat
- Fewer tools means better tool choice and fewer tokens
- Tool sets group tools under one name, e.g. `#reader`
- Reference a tool or tool set in the prompt with `#`
- Custom agents pin their own tool list in front matter

---

## Defining a Tool Set

```json
{
  "reader": {
    "tools": ["codebase", "search", "problems", "usages"],
    "description": "Read-only exploration of the code",
    "icon": "book"
  }
}
```

- Created via `Chat: Configure Tool Sets`
- Use `#reader` in a prompt to restrict the agent to these tools

---

## Tool Approval Prompts

- Terminal commands and `MCP` tools ask before running by default
- Allow once, for this session, for this workspace, or always
- Terminal auto-approve can use allow and deny command patterns
- `chat.tools.autoApprove` approves everything: avoid it
- Approval fatigue is real: keep the enabled set small instead
- Read the command, not just the button

---

## When Not to Auto-Approve

| Never auto-approve | Usually safe to approve |
| --- | --- |
| `git push`, `rm -rf`, deploy scripts | `ls`, `cat`, `git status` |
| Package installs from new sources | Running the test suite |
| `MCP` tools that write: merge, comment | `MCP` tools that only read |
| Network calls with credentials | Local build commands |
| Database writes | Read-only queries on a dev database |

---

## Prompt Injection Through Tool Results

![injection_path](svg/courses/ai/github-copilot-in-practice/06_agent_mode_deep_dive_and_mcp/injection_path.svg)

---

## Practical Precautions

- Assume every issue, web page and query result may contain instructions
- Do not mix untrusted input and powerful tools in one session
- Use read-only `GitHub` toolsets when exploring public repositories
- Install `MCP` servers only from sources you trust
- Run risky sessions in a dev container or codespace
- Review the diff and the tool trace before you commit

---

## Instructions in Agent Mode

- `.github/copilot-instructions.md` is sent with every agent request
- `.github/instructions/*.instructions.md` apply by `applyTo` glob
- `AGENTS.md` at the root, or nested per folder, is also read
- Put build, test and lint commands here: the agent will run them
- State the rules: no new dependencies, never edit generated code
- Same files are read by the coding agent and the `CLI`

---

## A Minimal `AGENTS.md`

```markdown
# Agent notes

## Build and test
- Install: `npm ci`
- Test: `npm test -- --run`
- Lint: `npm run lint` (must be clean)

## Rules
- Never edit files under `src/generated/`
- Add a test for every bug fix
- Do not add dependencies without asking
```

---

## Reproducible Agent Runs

- Commit `.vscode/mcp.json`, instructions and prompt files together
- Commit custom agents in `.github/agents/*.agent.md`
- Pin the tool list in the agent file, not in each person's picker
- Describe the dev environment in a dev container
- A teammate should get the same tools and rules on clone
- Share prompts as prompt files, not as chat history

---

## Workflow: Fixing a Failing Build

1. Give the agent the failing command, not a description of it
1. Let it run the command and read the full output
1. Ask for the root cause before the fix
1. Let it fix, rerun and iterate until green
1. Check the diff: tests weakened, errors suppressed?
1. Commit only what you understand

---

## Workflow: Scaffolding a Feature

1. Start in Plan mode: get a file-by-file plan
1. Review and edit the plan before any code exists
1. Switch to agent mode and implement the plan
1. Ask it to run tests and lint after each step
1. Keep each run to one coherent change
1. Commit between runs so checkpoints are cheap

---

## Knowing When to Stop

![stop_signals](svg/courses/ai/github-copilot-in-practice/06_agent_mode_deep_dive_and_mcp/stop_signals.svg)

---

## Taking Over Cleanly

- Press Stop: do not let a confused run keep editing
- Restore a checkpoint or `git restore` the damage
- Keep what was useful: the diagnosis, a partial fix
- Fix the hard part by hand, then hand back the routine part
- Start a new chat with a narrower prompt and fresh context
- Add the lesson to the instructions so the next run avoids it

---

## Key Takeaways

- Agent mode is a loop of tool calls you can watch and control
- `MCP` servers add tools; configure them per workspace or per user
- Keep the enabled tool set small and approvals deliberate
- Tool results are untrusted input: plan for prompt injection
- Instructions and `AGENTS.md` make runs consistent for the team
- Stop early, take over, and feed the lesson back into the rules
