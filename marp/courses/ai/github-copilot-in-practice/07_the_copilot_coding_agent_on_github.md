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

# The Copilot Coding Agent on GitHub

---

## What This Chapter Covers

- What the coding agent is and how it differs from agent mode
- Delegating work: issues, chat, the IDE and the agents panel
- Writing issues an agent can actually implement
- Following and steering a session through the pull request
- Preparing a repository: setup steps, instructions, firewall, `MCP`
- Economics: premium requests, `Actions` minutes and task fit

---

## What the Coding Agent Is

- An autonomous agent that runs on `GitHub`, not on your laptop
- You hand it a task; it hands you back a pull request
- Runs inside an ephemeral `GitHub Actions` environment
- Works on its own `copilot/` branch, never on your default branch
- Opens a draft pull request, pushes commits, then requests your review
- Asynchronous: you keep working while it works

---

## The Lifecycle of a Task

![agent_lifecycle](svg/courses/ai/github-copilot-in-practice/07_the_copilot_coding_agent_on_github/agent_lifecycle.svg)

---

## Agent Mode vs the Coding Agent

![ide_versus_cloud](svg/courses/ai/github-copilot-in-practice/07_the_copilot_coding_agent_on_github/ide_versus_cloud.svg)

---

## Side by Side

| Aspect | Agent mode (IDE) | Coding agent (GitHub) |
|---|---|---|
| Where it runs | Your machine | `Actions` runner |
| Supervision | You approve tools live | Unattended, review at the end |
| Output | Edits in your working tree | Draft pull request |
| Environment | Whatever you have installed | `copilot-setup-steps.yml` |
| Network | Your network | Firewall with allowlist |
| Best for | Exploratory, interactive work | Well-defined backlog items |

---

## Who Can Use It

- Requires a plan that includes the coding agent (Pro, Pro+, Business, Enterprise)
- In organizations an admin must enable the coding agent policy
- Repository owners can opt repositories in or out
- Only users with write access can assign tasks or steer it
- Comments from users without write access are ignored by the agent
- The agent cannot approve or merge its own pull request

---

## Delegating From an Issue

1. Open an issue that describes the change
1. In the `Assignees` box, choose `Copilot`
1. Optionally pick a base branch, a custom agent and extra instructions
1. Copilot reacts with 👀 and opens a draft pull request within a minute
1. The pull request links back to the issue and closes it on merge

---

## Other Ways to Delegate

- From the agents panel or the agents page on `github.com`: type a task, pick a repository
- From `Copilot Chat` on `github.com`: ask it to open a pull request
- From `VS Code`: the "delegate to coding agent" button in chat hands off the current conversation
- From the `GitHub` `MCP` server in any agent: `create_pull_request_with_copilot`
- From the Copilot `CLI`: the `/delegate` command
- All routes end in the same place: a draft pull request

---

## The Issue Is the Prompt

- The agent sees the issue title, body and existing comments
- It does not see the hallway conversation that led to the issue
- Vague issue in, vague pull request out
- Write it as you would for a capable new teammate on day one
- Include where, what, how to verify, and what not to touch

---

## A Good Issue

```markdown
Title: Reject negative quantities in POST /orders

The order API accepts `quantity: -3` and creates a refund by accident.

Where: `src/api/orders.py`, function `create_order`
Expected: return 422 with error code `INVALID_QUANTITY` when quantity < 1
Verify: add tests in `tests/api/test_orders.py`; run `pytest tests/api`
Out of scope: do not change the database schema or other endpoints
```

---

## Issues That Fail

- "Improve performance" - no target, no measurement
- "Refactor the auth module" - no definition of done
- "Fix the flaky test" - when the flakiness is in shared infrastructure
- "Upgrade to the new framework" - hundreds of files, many decisions
- Anything that needs credentials, production data or a human decision
- Split large work into issues the agent can finish in one session

---

## Reading the Session Log

- The pull request timeline has a "View session" link
- The log shows each step: files read, commands run, test output
- Watch it live, or read it afterwards to understand the change
- Look for: skipped tests, commands that failed silently, guesses
- The pull request description summarizes what it believes it did
- Trust the log and the diff, not the summary

---

## Steering With Review Comments

- Review the pull request like any other: inline comments and a review
- Mention `@copilot` so the agent picks the comment up
- Batch comments into one review rather than many single comments
- The agent starts a new session, pushes commits, and asks for review again
- Be concrete: "use the existing `Money` type" beats "this is wrong"

---

## Example Steering Comment

```markdown
@copilot Two changes please:
- Validate in the request schema, not inside create_order
- The test only covers -3; add cases for 0 and for a missing quantity
Keep the error code INVALID_QUANTITY.
```

---

## Iterating Until Mergeable

1. Read the diff and the session log
1. Approve the workflow run so `CI` executes on the agent's pull request
1. Leave one batched review with `@copilot` for anything that must change
1. Repeat until `CI` is green and the diff is what you would have written
1. Mark ready for review, get a second human approval if rules require it
1. Merge - you own the code now

---

## When to Stop Steering

- Three rounds without convergence: the task was badly shaped
- The agent keeps fixing symptoms instead of the cause
- The diff grows in places the issue never mentioned
- Close the pull request, rewrite or split the issue, try again
- Or check out the branch and finish it yourself

---

## Preparing a Repository

- The agent starts from a fresh runner with your code checked out
- Anything else it needs must be installed before it starts
- `.github/workflows/copilot-setup-steps.yml` defines that preparation
- The workflow must contain a single job called `copilot-setup-steps`
- Without it, the agent installs dependencies by trial and error, slowly
- Test the file by running the workflow manually from the `Actions` tab

---

## A Setup Steps Workflow

```yaml
name: "Copilot Setup Steps"
on: workflow_dispatch
jobs:
  copilot-setup-steps:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-python@v6
        with:
          python-version: "3.13"
      - run: pip install uv && uv sync --all-groups
      - run: pytest --collect-only -q
```

---

## Setup Steps Options

- `runs-on` can point to larger runners or self-hosted runners
- `timeout-minutes` caps setup time (maximum 59)
- Only a few job keys are honored: `steps`, `permissions`, `runs-on`, `services`, `snapshot`, `timeout-minutes`
- Secrets and variables come from the `copilot` environment in repo settings
- Setup steps run before the firewall is enabled
- If a step fails, the agent still starts - check the log

---

## Instructions the Agent Reads

- `.github/copilot-instructions.md`: repository-wide conventions
- `.github/instructions/*.instructions.md`: path-scoped rules via `applyTo`
- `AGENTS.md` files, nearest one to the edited file wins
- Custom agents in `.github/agents/*.agent.md` selectable when assigning
- Put build and test commands here; the agent runs what you tell it to
- An instruction it cannot verify is an instruction it may skip

---

## The Firewall

![firewall_boundary](svg/courses/ai/github-copilot-in-practice/07_the_copilot_coding_agent_on_github/firewall_boundary.svg)

---

## Working With the Firewall

- On by default: limits where the agent can send data
- The recommended allowlist covers common registries and `GitHub` services
- Add internal mirrors and documentation hosts in repository settings
- Blocked requests appear as a warning in the pull request
- Prefer installing in setup steps over widening the allowlist
- Disabling the firewall opens a path for data exfiltration through prompt injection

---

## MCP Servers for the Coding Agent

- Configured in repository settings under `Copilot` `Coding agent`
- `GitHub` and `Playwright` servers are available by default
- Extra servers are declared in a `JSON` block with `mcpServers`
- Tools must be listed explicitly; the agent uses them without asking
- Secrets referenced as `COPILOT_MCP_*` from the `copilot` environment
- Prefer read-only tools; the agent cannot ask you before calling one

---

## An MCP Configuration

```json
{
  "mcpServers": {
    "sentry": {
      "type": "local",
      "command": "npx",
      "args": ["@sentry/mcp-server@latest"],
      "tools": ["get_issue_details", "search_issues"],
      "env": { "SENTRY_ACCESS_TOKEN": "COPILOT_MCP_SENTRY_TOKEN" }
    }
  }
}
```

---

## What It Costs

| Resource | Consumed by | Notes |
|---|---|---|
| Premium requests | Each session (start or steering round) | One request times model multiplier |
| `Actions` minutes | The runner, for the whole session | Counted against your plan |
| Larger runners | Optional in setup steps | Billed at larger-runner rates |
| Reviewer time | Every pull request | The real bottleneck |

At time of writing - check docs.github.com for current rates.

---

## Task Fit

![task_fit](svg/courses/ai/github-copilot-in-practice/07_the_copilot_coding_agent_on_github/task_fit.svg)

---

## Task Shapes

| Succeeds | Wastes money |
|---|---|
| Bug with a reproduction and a test | "Something is slow somewhere" |
| Add tests to an untested module | Large refactor across the codebase |
| Dependency bump with a green suite | Change requiring production access |
| Documentation and type annotations | Design decision nobody has made yet |
| Small feature with acceptance criteria | Work spanning several repositories |
| Mechanical migration of a few files | Tasks with no automated verification |

---

## Key Takeaways

- The coding agent turns an issue into a draft pull request, asynchronously
- The issue is the prompt: specify where, what, how to verify
- Steer with batched `@copilot` review comments and read the session log
- Prepare the repository: setup steps, instructions, firewall, `MCP`
- Delegate scoped, verifiable, specified tasks; keep the rest
