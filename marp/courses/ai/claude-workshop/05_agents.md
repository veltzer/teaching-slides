---
tags:
  - data-and-ai:ai
  - data-and-ai:llm
  - data-and-ai:agents
level: intermediate
category: ai
audience:
  - audiences:developers
  - audiences:senior-developers

---
# Agents and Sub-Agents

---
## What This Chapter Covers

- Why sub-agents exist
- The agent catalog
- Briefing an agent well
- Foreground vs background
- Trust but verify

---
## What A Sub-Agent Is

- A second Claude in its own session
- Has its own context window
- Reports back a single result
- The main session orchestrates

---
## Why Sub-Agents Exist

- Protect the main context window
- Parallelize independent work
- Give a task a narrow tool set
- Specialize behavior

---
## Context Isolation

![subagent_isolation](svg/courses/ai/claude-workshop/05_agents/subagent_isolation.svg)

---
## Protecting The Main Context

- A big search would crowd the main window
- Delegate, get back a short report
- Main session stays small and sharp
- The agent eats the noise

---
## Parallelizing Work

- Three independent searches can run together
- Three test runs can run together
- Wall-clock time drops
- Tokens still cost

---
## A Narrow Tool Set

- An agent need not have all tools
- Read-only agents cannot break things
- Smaller surface, fewer surprises
- Trust scales down

---
## The Agent Catalog

- General-purpose for anything
- Explore for read-only search
- Plan for design work
- Code review for diffs

---
## General-Purpose

- The default
- Has all tools
- Used when nothing more specific fits
- A safe fallback

---
## Explore

- Read-only by design
- Cannot edit files
- Great for "where is X defined"
- Cheap and parallel-friendly

---
## Plan

- For laying out an approach
- Outputs a structured plan
- No file edits
- Good before a big change

---
## The Catalog

![agent_catalog](svg/courses/ai/claude-workshop/05_agents/agent_catalog.svg)

---
## Briefing An Agent Well

- The agent starts cold
- Give it goal, context, constraints
- Spell out file paths and line numbers
- Tell it the expected report shape

---
## The "Smart Colleague" Framing

- They just walked in the room
- They do not know your history
- They are bright but uninformed
- Write the brief accordingly

---
## What Context To Hand Over

- The goal in one sentence
- The relevant files and lines
- What you have ruled out
- What the answer should look like

---
## What To Leave Out

- The full chat history
- Speculation
- Multiple alternatives
- Generic "be thorough" lines

---
## Asking For A Short Report

- "Under 200 words" works
- A punch list beats a narrative
- File paths and line numbers please
- Save the prose for prose tasks

---
## Foreground Vs Background

- Foreground blocks the main session
- Background runs while you work
- Pick by whether you need the answer next
- Background needs a way to be notified

---
## When To Block

- Next step depends on the result
- Short task, no need to multitask
- Single agent, simple flow
- Default to foreground when in doubt

---
## When To Fire And Forget

- Long task, independent of next steps
- Multiple agents in parallel
- You will check back later
- Notifications close the loop

---
## Continuing An Agent

- Send a follow-up to an existing agent
- Preserves the agent's context
- Cheaper than starting fresh
- Best for related follow-up work

---
## Trust But Verify

- The agent reports what it meant to do
- Not the same as what it did
- Read the diff
- Run the tests

---
## Common Failure Modes

- Confident wrong answers
- Off-by-one in file edits
- Silently dropping requirements
- Hallucinated paths or APIs

---
## Worktree Isolation

- Run an agent on a throwaway copy
- Original tree is untouched
- Review changes side by side
- Merge or discard at will

---
## Worktree Flow

![worktree_flow](svg/courses/ai/claude-workshop/05_agents/worktree_flow.svg)

---
## Reviewing And Merging

- Diff the worktree
- Run the tests on the worktree
- Merge with a normal git workflow
- Worktree is cleaned up on success

---
## Hands-On Exercise

- Send an Explore agent to map a feature
- Send a Plan agent to design a change
- Send a general-purpose agent in a worktree
- Compare the diffs before merging
