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

# Copilot on the GitHub Website and the CLI

---

## What This Chapter Covers

- Generated pull request summaries
- Copilot code review: on demand and automatic
- Steering review with instruction files
- Copilot chat on `github.com` and Copilot Spaces
- The Copilot `CLI`: commands, agent mode, permissions
- Commit messages and failed `CI` runs

---

## Generated Pull Request Summaries

- Click the Copilot icon in the pull request description box
- Copilot reads the diff and writes a summary with a file-by-file list
- Works when opening a pull request and when editing an existing one
- Edit the result: it describes *what* changed, rarely *why*
- Add the motivation, the linked issue and the testing notes yourself
- Uses the repository custom instructions when they exist

---

## Copilot Code Review

![review_flow](svg/courses/ai/github-copilot-in-practice/08_copilot_on_the_github_website_and_the_cli/review_flow.svg)

---

## Requesting a Review on Demand

1. Open the pull request
1. In the **Reviewers** menu, select **Copilot**
1. Wait a minute or two while the review runs
1. Read the inline comments and suggested changes
1. Apply a suggestion with one click, or dismiss it
1. Push new commits and re-request the review if needed

- Also available from `VS Code` on uncommitted changes or a selection

---

## What the Review Is and Is Not

- Always leaves a **Comment** review
- Never **Approves**, never **Requests changes**
- Therefore it never satisfies or blocks a required-review rule
- Each review consumes a premium request from the author's or org's budget
- Finds local problems well: typos, null checks, off-by-one, missing awaits
- Misses design problems, cross-repository effects and business intent

---

## Automatic Review Triggers

| Trigger | Configured in | Typical use |
|---|---|---|
| Manual request | Pull request **Reviewers** menu | One-off second look |
| Personal setting | Your Copilot settings | Review every pull request you open |
| Repository ruleset | Settings → Rules → Rulesets | Every pull request on `main` |
| Organization ruleset | Org settings → Rulesets | Many repositories at once |
| Review new pushes | Ruleset option | Re-review after each push |
| Review drafts | Ruleset option | Feedback before ready for review |

---

## Setting Up an Automatic Review Ruleset

1. Repository **Settings** → **Rules** → **Rulesets** → **New branch ruleset**
1. Target the branches to protect, e.g. the default branch
1. Enable **Automatically request Copilot code review**
1. Optionally enable **Review new pushes** and **Review draft pull requests**
1. Save; the next pull request gets Copilot as a reviewer automatically

- Organization owners can apply the same ruleset across repositories

---

## Steering Review with Instructions

- Review reads `.github/copilot-instructions.md`
- Path-scoped `.github/instructions/*.instructions.md` apply by `applyTo` glob
- Put review-specific guidance in its own section
- Write concrete, checkable rules, not aspirations
- Long instruction files get truncated: keep the important rules first

---

## A Review Instructions File

```markdown
---
applyTo: "src/api/**/*.ts"
---
# API review rules

- Every handler validates input with the `zod` schema in `schemas/`
- Never log request bodies; they may contain personal data
- Database access goes through `repo/`, never raw `SQL` in handlers
- Flag any new endpoint without a test in `tests/api/`
```

---

## A First Pass, Not a Verdict

- Treat Copilot as the reviewer who reads every line, but not the big picture
- Resolve or dismiss each comment explicitly; do not leave noise
- A human still owns approval, design and risk judgment
- Track false positives and turn recurring ones into instructions
- Do not let "Copilot found nothing" replace a real review

---

## Copilot Chat on the Website

![website_chat](svg/courses/ai/github-copilot-in-practice/08_copilot_on_the_github_website_and_the_cli/website_chat.svg)

---

## Asking About Any Repository

- Open chat from any page on `github.com` or at `github.com/copilot`
- The current repository, file, issue or pull request becomes context
- Good questions: "Where is authentication handled?", "Summarize this issue thread"
- Attach more repositories, files or issues with the attach button
- Works on repositories you have never cloned
- Answers are only as good as the indexed code; verify file references

---

## Copilot Spaces

![spaces_grounding](svg/courses/ai/github-copilot-in-practice/08_copilot_on_the_github_website_and_the_cli/spaces_grounding.svg)

---

## Working With Spaces

- Create a Space at `github.com/copilot/spaces`
- Add repositories, individual files, issues, pull requests and free text
- Add instructions that apply to every question asked in the Space
- Share with your organization so everyone gets the same grounding
- Sources from repositories stay in sync with the default branch
- Use from the IDE and the `CLI` through the `GitHub` `MCP` server

---

## Knowledge Bases Became Spaces

| | Knowledge bases (retired) | Copilot Spaces |
|---|---|---|
| Plan | Enterprise only | All plans with chat |
| Content | Markdown files in repositories | Code, files, issues, PRs, free text |
| Instructions | None | Per-Space instructions |
| Sharing | Organization | Personal or organization |
| Use outside website | Limited | IDE and `CLI` via `MCP` |

- Migrate existing knowledge bases into Spaces

---

## Copilot in the CLI

- The old `gh copilot` extension (`suggest`, `explain`) is retired
- The replacement is the standalone Copilot `CLI`: command `copilot`
- Install with `npm install -g @github/copilot`, sign in with `/login`
- Interactive mode: a chat and agent session in your terminal
- Programmatic mode: `copilot -p "..."` for scripts and automation
- Ships with the `GitHub` `MCP` server already configured

---

## Explaining and Suggesting Commands

```bash
$ copilot
> what does this do: tar -xzvf backup.tgz -C /srv --strip-components=1
  Extracts the gzip archive into /srv, verbose, dropping the
  top-level directory from every path.

> find all files over 100MB modified in the last week
  find . -type f -size +100M -mtime -7
  Run this command? (y/n)
```

---

## Copilot as an Agent in the Terminal

![cli_agent_loop](svg/courses/ai/github-copilot-in-practice/08_copilot_on_the_github_website_and_the_cli/cli_agent_loop.svg)

---

## Trusted Directories and Permissions

- On start, Copilot asks whether to trust the current directory
- It reads and edits files only under trusted directories
- Every shell command or tool call asks for approval by default
- Approve once, approve for the session, or reject and redirect
- Flags pre-approve or forbid tools for unattended runs
- `--deny-tool` always wins over `--allow-tool`

---

## Permission Flags

| Flag | Effect |
|---|---|
| `--allow-tool 'shell(git)'` | Run any `git` command without asking |
| `--deny-tool 'shell(rm)'` | Never run `rm`, even if allowed elsewhere |
| `--allow-tool 'write'` | Edit files without asking |
| `--allow-tool 'github'` | Use the `GitHub` `MCP` server tools freely |
| `--allow-all-tools` | Approve everything: only in a sandbox |

---

## Useful Slash Commands

| Command | What it does |
|---|---|
| `/model` | Switch the model for this session |
| `/mcp` | List, add or disable `MCP` servers |
| `/delegate` | Hand the task to the coding agent as a pull request |
| `/add-dir` | Trust an additional directory |
| `/usage` | Show premium requests used this session |
| `/clear` | Start a fresh conversation |

---

## A Programmatic Run

```bash
copilot -p "Run the unit tests, fix any failure in src/parser, \
  and summarize what you changed" \
  --allow-tool 'shell(npm test)' \
  --allow-tool 'write' \
  --deny-tool 'shell(git push)'
```

- Narrow allow-lists turn the agent into a safe batch job
- Keep `git push` and deployment commands out of reach

---

## Commit Message Generation

- In the `VS Code` Source Control view, click the sparkle icon
- Copilot writes a message from the staged diff
- Follows conventions it finds in recent history and instructions
- Add a commit-message section to your instructions for team format
- Still read it: the message states *what*, you add *why*

---

## Explaining a Failed CI Run

- On a failed `GitHub Actions` job, click **Explain error**
- Copilot reads the log and points at the failing step and likely cause
- Ask follow-ups in the same chat: "show the line in the workflow file"
- From the pull request, ask Copilot to fix it, or `/delegate` the fix
- Verify the diagnosis locally before trusting a proposed fix

---

## Key Takeaways

- Copilot review is a fast first pass that comments but never approves
- Rulesets make review automatic; instruction files make it relevant
- Website chat and Spaces answer questions without cloning anything
- The `copilot` `CLI` is a full agent: control it with tool permissions
- Small conveniences, summaries, commit messages and `CI` explanations, add up
