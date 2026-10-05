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

# Copilot Chat in the IDE

---

## What This Chapter Covers

- The three chat surfaces and when to use each
- Chat participants: `@workspace`, `@terminal`, `@vscode`, `@github`
- Slash commands: `/explain`, `/fix`, `/tests`, `/doc`, `/new`
- Controlling context explicitly with `#` references
- How workspace indexing works
- Getting answers into the editor and the terminal
- Verifying that an answer actually used your code

---

## The Three Chat Surfaces

![chat_surfaces](svg/courses/ai/github-copilot-in-practice/03_copilot_chat_in_the_ide/chat_surfaces.svg)

---

## The Chat View

- Opens in the secondary side bar (`Ctrl+Alt+I`, `Cmd+Ctrl+I` on macOS)
- Keeps a conversation history you can return to
- Hosts the mode picker: Ask, Edit, Agent, Plan and custom agents
- Hosts the model picker for the current conversation
- Best for exploration: "how does this module work?"
- Start a new chat (`Ctrl+N` in the view) when the topic changes

---

## Inline Chat

- `Ctrl+I` (`Cmd+I`) inside the editor
- Scoped to the current selection or the cursor position
- Result appears as a diff directly in the file
- Accept, discard, or refine with a follow-up prompt
- Also available in the integrated terminal for shell commands
- Best for: "rename these", "add error handling here", "convert to async"

---

## Quick Chat

- `Ctrl+Shift+Alt+L` opens a small floating input at the top
- One question, one answer, then it gets out of the way
- Does not clutter the main conversation history
- Can be promoted to the chat view if the question grows
- Best for: "what is the flag for ...", "what does this regex match"

---

## Which Surface for Which Question

| Question | Surface |
|---|---|
| How does the payment flow work? | Chat view |
| Rewrite this function with early returns | Inline chat |
| What does `git rebase --onto` do? | Quick chat |
| Why does this terminal command fail? | Inline chat in the terminal |
| Plan a change across several modules | Chat view, Plan or Agent mode |

---

## Chat Participants

- A participant is an expert you address with `@`
- It decides what extra context is gathered before the model runs
- Type `@` in the chat input to list the installed participants
- Extensions can contribute their own participants
- Only one participant per prompt
- No participant: the default agent picks context itself

---

## The Built-in Participants

| Participant | Knows about | Typical question |
|---|---|---|
| `@workspace` | Your project's code | Where is the retry logic? |
| `@terminal` | The integrated terminal | Explain the last command's error |
| `@vscode` | Editor settings and commands | How do I enable format on save? |
| `@github` | Repos, issues, PRs, web search | What changed in PR 412? |

---

## Participants vs `#` Tools

- In current `VS Code` the `#codebase` tool does what `@workspace` did
- `#codebase` can be combined with other tools in one prompt
- `@workspace` still works and is equivalent in Ask mode
- In Agent mode the model calls search tools on its own
- `#terminalLastCommand` and `#terminalSelection` replace most `@terminal` use
- Prefer `#` references when you want to mix several sources

---

## How Context Is Gathered

![context_gathering](svg/courses/ai/github-copilot-in-practice/03_copilot_chat_in_the_ide/context_gathering.svg)

---

## Slash Commands

| Command | What it does |
|---|---|
| `/explain` | Explain the selected code or the active file |
| `/fix` | Propose a fix for the selection or the reported problem |
| `/tests` | Generate tests for the selection, using your test framework |
| `/doc` | Add documentation comments |
| `/new` | Scaffold a new project or file set |
| `/clear` | Start a fresh conversation |

---

## Using Slash Commands Well

- A slash command is a canned prompt plus a context strategy
- Add your own text after it: `/tests use pytest fixtures, no mocks`
- `/fix` reads diagnostics from the Problems panel, not only the code
- `/tests` looks for existing test files to imitate their style
- `/new` produces a file tree preview before creating anything
- Prompt files you write appear in the same `/` list (next chapter)

---

## Fixing a Failing Test

![fix_failing_test](svg/courses/ai/github-copilot-in-practice/03_copilot_chat_in_the_ide/fix_failing_test.svg)

---

## Fixing a Failing Test in Practice

1. Run the tests from the Test Explorer
1. Hover the red test and pick "Fix Test Failure"
1. Copilot receives the test, the code under test and the failure output
1. Read the proposed change: does it fix the code or the assertion?
1. Re-run the test before accepting anything else
1. Use `/fix` with `#testFailure` for the same flow from chat

---

## Controlling Context Explicitly

| Reference | Adds |
|---|---|
| `#file` | A specific file |
| `#selection` | The current editor selection |
| `#codebase` | Relevant chunks found by searching the workspace |
| `#changes` | Your uncommitted source control changes |
| `#problems` | Diagnostics from the Problems panel |
| `#fetch` | The content of a web page |

---

## Adding Context Without Typing

- Drag files or folders from the Explorer into the chat input
- Click "Add Context" (the paperclip) to pick files, symbols, tools
- Open editors can be attached with one click
- Attach images: paste or drag a screenshot of a UI or an error dialog
- Images need a model that supports vision; the picker shows which
- Remove any context chip you did not intend before sending

---

## Example Prompt With Explicit Context

```markdown
#file:src/billing/invoice.py #file:tests/test_invoice.py
Why does test_rounding fail for amounts above 1000?
Do not change the test. Use the Decimal helpers in
#file:src/billing/money.py
```

- Three files, one question, one constraint
- Narrow context beats `#codebase` when you know where to look

---

## How Workspace Indexing Works

![workspace_index](svg/courses/ai/github-copilot-in-practice/03_copilot_chat_in_the_ide/workspace_index.svg)

---

## Why Indexing Matters

- Repositories hosted on `GitHub` get a remote semantic index
- Other folders get a local index, limited in size
- Check the index status from the Copilot status bar item
- A stale or missing index gives shallow `#codebase` answers
- Files in `.gitignore` and content exclusions are not indexed
- Large monorepos: open the sub-folder you work in

---

## Getting Answers Into Your Code

- Hover a code block: Apply in Editor, Insert at Cursor, Copy
- "Apply" merges the block into the right file as a reviewable diff
- Shell blocks have "Insert into Terminal" — it does not press Enter
- Review the diff with the same care as a colleague's commit
- Use Edit or Agent mode when the change spans several files

---

## Smart Actions in the Editor

- Right-click → Copilot: Explain, Fix, Review, Generate Docs, Generate Tests
- The sparkle icon on a diagnostic offers "Fix using Copilot"
- Source Control view: generate a commit message
- Rename symbol suggests names with Copilot
- Smart actions are slash commands with the context pre-filled

---

## Verifying Chat Answers

![verify_answer](svg/courses/ai/github-copilot-in-practice/03_copilot_chat_in_the_ide/verify_answer.svg)

---

## Making Copilot Show Its Sources

- Expand the "Used n references" line above every answer
- Each reference links to the file and line range that was sent
- Ask directly: "list the files you based this on"
- In Agent mode, read the tool calls: which searches ran, which files were read
- Zero references on a codebase question is a red flag

---

## Spotting Answers That Ignored Your Codebase

- Function names that do not exist in your project
- A different framework or library than the one you use
- Generic tutorial style code instead of your conventions
- Confident file paths that are not in the tree
- Fix: re-ask with `#codebase` or the exact `#file` references
- Still wrong? Check indexing and content exclusions

---

## Key Takeaways

- Pick the surface by scope: view for exploring, inline for changing
- Participants and `#` references decide what the model sees
- Slash commands are shortcuts; add your own constraints after them
- Explicit, narrow context gives better answers than hoping
- Always check the references before trusting a codebase answer
