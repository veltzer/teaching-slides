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

# Edit Mode and Agent Mode

---

## What This Chapter Covers

- Edit mode: one prompt, many files, reviewed per file
- Agent mode: Copilot runs commands and iterates on failures
- Approving tools and terminal commands
- Auto-approval settings and what they cost you
- Checkpoints and undoing an agent run
- Choosing the right surface for the task

---

## The Chat Modes in VS Code

- The mode picker sits at the bottom of the chat view
- `Ask`: answers questions, changes nothing
- `Edit`: proposes changes to files you choose
- `Agent`: picks files itself, runs tools, iterates
- `Plan`: researches and writes a plan before any edit
- Custom agents add your own named modes (next chapter)

---

## Edit Mode Today

- Edit mode is being de-emphasized in favor of agent mode
- Recent VS Code builds may hide it behind a setting
- Agent mode can do everything edit mode does, and more
- Edit mode still wins when you want a tight, predictable change
- The concepts it introduced live on in agent mode:
    - the working set of files
    - per-file `Keep` and `Undo`

---

## Multi-File Edits From One Prompt

![edit_working_set](svg/courses/ai/github-copilot-in-practice/05_edit_mode_and_agent_mode/edit_working_set.svg)

---

## Managing the Working Set

- The working set is the list of files Copilot may change
- The active editor is added automatically
- Add more with `Add Context`, `#file`, or drag and drop
- Remove files that must not change before you send
- Keep it small: three focused files beat thirty
- A file outside the working set will not be edited

---

## Reviewing Edits per File

- Changed files are listed above the chat input
- Each file opens as an inline diff in the editor
- `Keep` accepts a file, `Undo` discards it
- Step through hunks with the diff toolbar
- Edits are applied to disk before you decide: save them deliberately
- Run the tests before you `Keep` everything

---

## What Agent Mode Adds

- Decides which files to read and edit on its own
- Runs terminal commands: build, test, lint, install
- Reads the output and reacts to errors
- Iterates until the task is done or it gives up
- Calls tools: built-in ones and `MCP` servers
- One prompt can produce many model requests

---

## The Agent Loop

![agent_loop](svg/courses/ai/github-copilot-in-practice/05_edit_mode_and_agent_mode/agent_loop.svg)

---

## A Typical Agent Prompt

```markdown
Add input validation to the `createUser` endpoint in
`src/api/users.ts`. Reject empty names and invalid emails
with a 400 response. Add tests in `src/api/users.test.ts`
and run `npm test` until all tests pass.
Do not change any other endpoint.
```

- States the goal, the files, the check and the boundary
- "Run until tests pass" gives the agent its feedback loop

---

## Approving Terminal Commands and Tools

- By default the agent asks before running a command
- The prompt shows the exact command line
- Options: allow once, allow for this session, allow always
- You can edit the command before it runs
- Read every command: `rm`, `git push`, `curl | sh` deserve a pause
- Denying a command is feedback; the agent tries another route

---

## Auto-Approval Settings

```json
{
  "chat.tools.autoApprove": false,
  "chat.tools.terminal.autoApprove": {
    "npm test": true,
    "git status": true,
    "rm": false,
    "/^git push/": false
  }
}
```

- `chat.tools.autoApprove` approves every tool: avoid it
- The terminal list allows or denies commands, regex included

---

## The Risks of Auto-Approval

- The agent acts on text it reads: files, web pages, tool output
- Injected instructions can turn into real commands
- Allow lists match prefixes; chained commands can slip through
- Auto-approved deletes and pushes are hard to take back
- Safe pattern: approve read-only and test commands only
- Run risky work in a container, dev container or Codespace

---

## Checkpoints and Undo

- Each chat request creates a checkpoint of the files it touched
- `Restore Checkpoint` rolls files back to before that request
- Later requests are removed from the conversation too
- `Undo` per file still works while the edits are pending
- Checkpoints cover files, not side effects of commands
- A database migration or `git push` is not undone

---

## Use Git as Your Real Safety Net

1. Start the agent on a clean working tree or a new branch
1. Let it work
1. Review with `git diff`, not only the chat view
1. Commit what you keep, `git restore` what you do not
1. Never let the agent push for you

---

## Comparing the Surfaces

| Surface | Who picks files | Runs commands | Best for |
|---|---|---|---|
| Completions | You, by cursor | No | The next few lines |
| Ask mode | Nobody | No | Questions, explanations |
| Edit mode | You, working set | No | Known change, known files |
| Agent mode | Copilot | Yes, with approval | Change plus verify loop |
| Coding agent | Copilot, on `GitHub` | Yes, in `Actions` | Whole issue, async |

---

## A Practical Decision Guide

![surface_decision](svg/courses/ai/github-copilot-in-practice/05_edit_mode_and_agent_mode/surface_decision.svg)

---

## When a Task Is Too Big for One Run

- The prompt needs "and then" more than twice
- It touches several layers: schema, `API`, `UI`, docs
- No single command can tell the agent it is done
- The context window fills: answers start forgetting earlier files
- The diff is too large for you to review honestly

---

## Splitting a Big Task

1. Use `Plan` mode to produce a step list first
1. Turn each step into its own agent request
1. Review and commit after every step
1. Start a new chat when the context gets long
1. Hand the remaining steps to the coding agent if they are routine

---

## Knowing When to Take Over

- The agent edits the same lines back and forth
- It disables a test or a lint rule to get green
- It installs packages you did not ask for
- It keeps retrying a command that cannot work
- Stop the request, restore the checkpoint, and do it yourself

---

## Key Takeaways

- Edit mode: you choose the files, you review every file
- Agent mode: Copilot chooses, runs and iterates, you approve
- Approve read-only commands freely, everything else deliberately
- Checkpoints undo files, `git` undoes everything else
- Pick the smallest surface that can finish the task
