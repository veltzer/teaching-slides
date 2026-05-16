---
tags:
  - data-and-ai:ai
  - data-and-ai:llm
level: intermediate
category: ai
audience:
  - audiences:developers
  - audiences:senior-developers

---
# The Context Window and Compaction

---
## What This Chapter Covers

- What lives in the context window
- Token budgets in real sessions
- How long sessions fail
- Compaction in practice
- Prompt caching

---
## What Is The Context Window

- Everything the model sees this turn
- System prompt and rules
- Memory and CLAUDE.md
- The running conversation

---
## What Else Lives There

- Tool definitions
- Tool results
- File reads and command output
- Past assistant turns

---
## The System Prompt

- Set by Anthropic and the harness
- Defines the agent's behavior
- You do not edit it directly
- You influence it via CLAUDE.md and config

---
## Tool Results

- Big tool outputs cost tokens
- They stay in context until compaction
- A noisy `find` can blow the budget
- Use grep over find, head over cat

---
## File Reads

- Each read consumes tokens
- Re-reading the same file is wasteful
- The harness caches some reads
- Be intentional about what to load

---
## What Is In The Window

![context_window](svg/courses/ai/claude-workshop/03_context_and_compaction/context_window.svg)

---
## Token Budgets

- Models have hard token limits
- 200K, 1M and more depending on model
- Output also costs against the budget
- A "1M context" model is still finite

---
## Cost As A Function Of Tokens

- Input tokens cost less than output
- Cache hits cost less than fresh reads
- Long sessions get expensive
- Watch the meter, not just the answer

---
## Latency As A Function Of Tokens

- Bigger context means slower turns
- Each tool call adds a round trip
- Cache hits are faster
- Short prompts win when possible

---
## Reading Your Window

- Status line shows token usage
- `/cost` shows the running total
- Inspect what is taking the space
- Trim accordingly

---
## How Long Sessions Go Wrong

- Attention drifts from early rules
- The model forgets what it was doing
- Old tool results crowd useful context
- Errors compound silently

---
## Tool Result Spam

- Verbose output fills the window
- Pipe through head, grep, wc
- Use background tasks for long output
- Ask for summaries, not dumps

---
## The "I Forgot" Failure Mode

- Mid-task drift
- Repeating already-done work
- Re-asking the user for known facts
- Time to compact or restart

---
## What Is Compaction

- The harness summarizes earlier turns
- A compact representation replaces the old
- The conversation continues
- Old detail is gone

---
## Automatic Compaction

- Triggered as you approach the limit
- The harness picks the moment
- You see a notice in the session
- Work proceeds normally after

---
## Manual Compaction

- `/compact` triggers it on demand
- Useful before a heavy task
- Useful at logical chapter breaks
- Better than letting it surprise you

---
## What Survives Compaction

- The summary the harness wrote
- Your CLAUDE.md and rules
- The current goal
- Any pinned tasks

---
## What Does Not Survive

- Verbatim tool outputs
- File contents you read
- Exact diffs and command output
- Implicit understanding

---
## Compaction: Before And After

![compaction_before_after](svg/courses/ai/claude-workshop/03_context_and_compaction/compaction_before_after.svg)

---
## Prompt Caching

- Anthropic caches identical prefixes
- Cache hits are cheaper and faster
- Five minute TTL by default
- Structure prompts to maximize hits

---
## Keeping The Cache Warm

- Reuse the same system prompt
- Avoid changing CLAUDE.md mid-session
- Keep heavy reads near the start
- Repeat queries soon, not later

---
## The Five Minute Window

- TTL resets on each hit
- A long sleep busts the cache
- Plan pauses around it
- Cheaper to keep going than to come back

---
## Prompt Cache In Practice

![prompt_cache](svg/courses/ai/claude-workshop/03_context_and_compaction/prompt_cache.svg)

---
## Starting Fresh Vs Continuing

- Continue when the goal is the same
- Restart when context is poisoned
- Restart between unrelated tasks
- A fresh session is cheap

---
## Sub-Agents To Stay Clean

- Delegate big reads to an agent
- Get back a short report
- Main context stays small
- More on this later

---
## Writing Things Down

- Memory and notes outlive a session
- The repo outlives any conversation
- Persist decisions where they belong
- Do not trust the conversation alone

---
## Hands-On Exercise

- Trigger a compaction with `/compact`
- Compare the session before and after
- Watch the token meter on a long task
- Plan a session with a cache-friendly shape
