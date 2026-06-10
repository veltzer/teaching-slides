---
tags:
- concepts:ai
- concepts:agents
- concepts:llm
- concepts:prompting
level: intermediate
category: ai
audience:
- audiences:developers

---
# The Context Window
## What an LLM Can See, and What It Forgets
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## Overview

![title](svg/lectures/ai/context_window/title.svg)

---

## What This Lecture Covers

1. What the context window is — and what it is not
1. Tokens: the unit the window is measured in
1. What actually fills the window in a real agent
1. Why a bigger context is not automatically better
1. Managing the window: clearing, summarizing, compacting
1. Working with projects far larger than any window
1. Caching, retrieval, and other supporting techniques
1. Pitfalls and good habits

---

## The Problem

- An LLM *seems* to remember your conversation
- It does not — it re-reads everything on every single turn
- The amount it can re-read is hard-limited: the context window
- Long sessions fill it up; quality drops before the limit is hit
- Real projects are far bigger than any window will ever be
- We need deliberate techniques to manage this scarce resource

---

## The Core Idea

> The context window is **everything the model can see** while generating its next reply — and the only thing it can see.

- One fixed-size buffer: instructions, history, files, results
- If it is not in the window, the model does not know it
- Measured in **tokens**, not characters or words

---

## What Is the Context Window?

![what_is_context](svg/lectures/ai/context_window/what_is_context.svg)

---

## The Context Window Is Not...

- **Not** long-term memory — it is wiped between sessions
- **Not** a database — there is no lookup, only one linear read
- **Not** the model's knowledge — that is frozen in the weights
- **Not** infinite — every model has a hard token limit

---

## Stateless at the Core

- Every API call sends the *entire* conversation again
- The model's "memory" of the chat is just this replay
- Delete a message from the replay and it never happened
- This is why context management works at all: *you* control the buffer

---

## Tokens: The Unit of Context

![tokens](svg/lectures/ai/context_window/tokens.svg)

---

## What Is a Token?

- Models read **subword pieces**, not characters or words
- A tokenizer splits text into a fixed vocabulary of pieces
- Common words are one token; rare words split into several
- Code, numbers, and non-English text often cost more tokens
- Window size, pricing, and limits are all counted in tokens

---

## Rules of Thumb

```misc
1 token   ~ 4 characters of English
1 token   ~ 3/4 of a word
100 tokens ~ 75 words ~ a short paragraph
1K tokens  ~ a page of text
100K tokens ~ a short novel
```

---

## How Big Are Windows Today?

- Early GPT models: 2K–4K tokens — a few pages
- Mid generation: 8K–32K — a long document
- Modern frontier models: 200K and up — a whole book
- Long-context variants reach 1M+ tokens
- Sounds huge — until you meet a real codebase

---

## What Fills the Window

![anatomy](svg/lectures/ai/context_window/anatomy.svg)

---

## The Hidden Overhead

- **System prompt** — instructions, rules, persona
- **Tool schemas** — every exposed tool costs tokens up front
- **Conversation history** — every prior turn, replayed
- **Tool results** — file contents, command output, search hits
- Your actual question is often the *smallest* part

---

## Why Not Just Fill It Up?

![degradation](svg/lectures/ai/context_window/degradation.svg)

---

## Cost and Latency

- You pay **per token**, on every single call
- A full window re-sent each turn multiplies the bill
- Processing long context takes real time — latency grows
- A bloated window makes every remaining turn slower and pricier

---

## Context Rot

- Model attention is not uniform across the window
- Facts buried in the middle are recalled worst — "lost in the middle"
- Irrelevant text actively *distracts*: more context can mean worse answers
- Quality degrades well before the hard limit is reached
- A lean window is not just cheaper — it is **smarter**

---

## The Management Principle

> Aim for the **smallest** context that still contains **everything** the task needs.

- Not minimal at all costs — missing facts cause failure too
- Curate: every token should earn its place
- The rest of this lecture is techniques for doing that

---

## The Toolbox

![techniques](svg/lectures/ai/context_window/techniques.svg)

---

## Technique: Clearing the Window

- Wipe the conversation and start from zero
- In chat tools: a "new conversation"; in Claude Code: `/clear`
- The cheapest, most complete reset available
- Nothing carries over — for better and for worse

---

## When to Clear

- You are starting a **genuinely new task**
- The context is **poisoned** — failed attempts, wrong paths, dead ends
- The model keeps echoing earlier mistakes
- Untangling a confused session costs more than restarting it

---

## What Clearing Costs

- Every decision, constraint, and finding is gone
- You will re-explain anything the next task still needs
- **Habit:** before clearing, write the keepers to a file
- Then the new session starts lean *and* informed

---

## Technique: Summarization

![summarization](svg/lectures/ai/context_window/summarization.svg)

---

## How Summarization Works

1. Take the oldest part of the conversation
1. Ask a model to compress it into a short summary
1. Replace those turns with the summary text
1. Keep the most recent turns verbatim
1. The session continues — shorter, but still oriented

---

## What a Good Summary Keeps

- **Decisions** made, and *why* they were made
- **Current state** — what is done, what is in progress
- **Open tasks** and known blockers
- **Hard constraints** — versions, APIs, user requirements
- **What failed** — so it is not attempted again

---

## Summarization Variants

- **Rolling** — continuously fold old turns into one running summary
- **Hierarchical** — summarize summaries as the session grows
- **On demand** — compress only when approaching the limit
- **Selective** — keep code and constraints verbatim, compress chatter

---

## Technique: Compaction

![compaction](svg/lectures/ai/context_window/compaction.svg)

---

## Auto-Compaction

- Agent frameworks watch the window as it fills
- Near a threshold, they summarize old context **automatically**
- The agent keeps working across the boundary — no restart
- Claude Code does this; you may only notice a short pause
- Long-running agents are impossible without it

---

## Compaction Is Lossy

- A summary is a *paraphrase* — detail does not survive
- Exact code, precise numbers, verbatim quotes can vanish
- After compaction, **re-read** files instead of trusting recall
- Critical constraints belong in files or system prompts, not history

---

## Clear vs Compact

![clearing_vs_compacting](svg/lectures/ai/context_window/clearing_vs_compacting.svg)

---

## Choosing Between Them

- **Clear** when the next task does not need the past
- **Compact** when the *same* task must continue
- Clearing is lossless about the future, total loss of the past
- Compaction keeps the thread, but blurs the detail
- Both beat limping along with a full, rotten window

---

## Working with Large Projects

![large_projects](svg/lectures/ai/context_window/large_projects.svg)

---

## The Codebase Never Fits

- A medium repository is **millions** of tokens
- No window will ever hold it — stop trying
- Treat the window as a *workbench*, not a *warehouse*
- Bring in only the files the current step needs

---

## Search First, Read Second

- Never "read everything to get familiar"
- **Search** (grep, glob, code index) to locate the relevant spots
- Read those files — ideally only the relevant sections
- Drop them from focus when the step is done

---

## Files as External Memory

- The filesystem survives clears, compactions, and sessions
- Write plans, decisions, and progress to files as you go
- `TODO.md`, design notes, a project journal
- Project instruction files (e.g. `CLAUDE.md`) reload every session
- **If it must be remembered, it belongs in a file**

---

## Progressive Disclosure

- Keep cheap *pointers* in context; load detail on demand
- A skill's one-line description sits in context; its body loads when used
- Same idea for docs: index in context, content fetched when needed
- Pay tokens only for the depth the task actually reaches

---

## Subagents: Fresh Windows

- A subagent is a separate model call with its **own empty window**
- Send it a focused task: "find where X is configured"
- It burns *its* context searching — and returns a short answer
- Only the conclusion enters your window, not the journey
- Parallel subagents explore a large project without flooding anyone

---

## Retrieval: Pull, Don't Preload

- RAG: index the large corpus *outside* the model
- Retrieve only the chunks relevant to the current question
- The window holds the question and a handful of hits
- Scales to corpora a thousand times the window size

---

## Prompt Caching

- Providers can **cache** the unchanging prefix of your prompt
- System prompt and tool schemas are processed once, reused cheaply
- Cuts cost and latency dramatically — but *not* window usage
- Design for it: stable content first, changing content last

---

## Trim at the Source

- Tool results are the biggest silent context hogs
- Return the **relevant slice**, not the whole file
- Paginate long listings; truncate noisy logs
- Summarize a result before it enters context, not after

---

## Common Pitfalls

![pitfalls](svg/lectures/ai/context_window/pitfalls.svg)

---

## Pitfall: Context Hoarding

- "Keep it all, the model might need it" — it mostly will not
- Cost rises, attention dilutes, answers get worse
- **Fix:** curate aggressively; re-fetch beats carrying dead weight

---

## Pitfall: Compacting Away the Constraint

- A critical requirement lived only in an early chat turn
- Compaction paraphrased it — or dropped it entirely
- The agent then confidently violates it
- **Fix:** persist hard constraints to files or the system prompt

---

## Pitfall: Mistaking Context for Memory

- "I told it yesterday" — yesterday's window is gone
- A new session knows only what is loaded into it
- **Fix:** durable knowledge goes in files, instructions, or retrieval

---

## Good Habits

- Know roughly how full your window is — watch the gauge
- Clear between unrelated tasks; compact within long ones
- Write decisions and constraints to files as you make them
- Search before reading; read sections, not repositories
- Delegate exploration to subagents; keep only conclusions
- Put stable content first to exploit prompt caching

---

## The Mental Model

![mental_model](svg/lectures/ai/context_window/mental_model.svg)

---

## Desk, Shelf, Library

- The **window** is your desk — fast, tiny, everything in reach
- **Files and retrieval** are the shelf — fetched when needed
- The **weights** are the library — vast, fixed, background knowledge
- Productive work means a *tidy desk*, not a bigger one

---

## Summary

- The context window is **all the model sees** — finite and stateless
- It is measured in **tokens**; overhead eats it fast
- More context costs money, time, and **accuracy** — curate it
- **Clear** between tasks, **summarize and compact** within them
- Large projects: search, retrieve, delegate, and use **files as memory**

---

## Where to Start

1. Watch your context usage for one real working session
1. Start clearing between tasks — note what you had to re-explain
1. Move those things into project files so they reload for free
1. Add retrieval or subagents only when the project outgrows that

The window is a workbench: keep on it exactly what the work needs.

---

## Questions?

- One fixed buffer of tokens decides what the model knows right now
- Lean context is cheaper, faster, and more accurate
- Files, retrieval, and fresh windows scale beyond any limit

## Thank You
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)
