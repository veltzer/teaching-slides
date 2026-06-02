---
tags:
- concepts:ai
- concepts:agents
- concepts:llm
level: intermediate
category: ai
audience:
- audiences:developers

---
# Skills in AI
## Packaging Reusable Expertise for LLM Agents
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## Overview

![title](svg/lectures/ai/skills/title.svg)

---

## What This Lecture Covers

1. What a "skill" is — and what it is not
1. The anatomy of a skill folder
1. Progressive disclosure and why it matters
1. How an agent discovers and loads a skill
1. Skills versus tools, RAG, and fine-tuning
1. Authoring, testing, and refining skills
1. Pitfalls, security, and good habits

---

## The Problem

- LLMs are powerful generalists
- But they don't know *your* procedures
- Your team's coding style, your report format, your deploy checklist
- Re-explaining it in every prompt is wasteful and inconsistent
- Fine-tuning is slow, costly, and opaque
- We want a lightweight, shareable way to teach an agent a task

---

## The Core Idea

> A skill is a folder of instructions an agent reads **only when the task calls for it**.

- Plain Markdown plus any helper files
- Loaded at run time, not baked into the model
- Like handing a capable new hire the right runbook

---

## What Is a Skill?

![what_is_a_skill](svg/lectures/ai/skills/what_is_a_skill.svg)

---

## A Skill Is Not...

- **Not** training or fine-tuning — the weights never change
- **Not** a prompt you paste every time — it loads itself
- **Not** a single function call — it can describe a whole workflow
- **Not** tied to one model — it is just files and a convention

---

## Why "Skill" Is a Good Name

- A human skill is *learned procedure* you can apply when relevant
- You don't recite every skill you have at all times
- You reach for the right one when the situation demands it
- Skills for agents work the same way: dormant until triggered

---

## The Anatomy of a Skill

![anatomy](svg/lectures/ai/skills/anatomy.svg)

---

## SKILL.md: The Entry Point

```markdown
---
name: pdf-processing
description: >
  Fill, split, and extract text from PDF forms.
  Use when the user mentions PDFs or form fields.
---

# PDF Processing

To fill a form, run `scripts/fill.py`.
For field layout details, see `reference.md`.
```

---

## The Two Required Fields

- **name** — a short, unique identifier
- **description** — what it does *and* when to use it
- Everything else in the body is free-form Markdown
- The description is what the agent sees before loading anything else

---

## Bundled Files

- **Linked docs** — `reference.md`, `forms.md`, deep detail read on demand
- **Scripts** — code the agent runs instead of reasoning step by step
- **Templates / data** — example files, schemas, fixtures
- All live in the same folder — copy it, zip it, commit it

---

## Progressive Disclosure

![progressive_disclosure](svg/lectures/ai/skills/progressive_disclosure.svg)

---

## Three Levels of Detail

1. **Metadata** — name + description, always loaded, tiny
1. **Body** — the SKILL.md instructions, loaded when the skill fires
1. **Linked files** — reference docs and scripts, loaded only if needed

The agent pays the token cost only for the depth it actually reaches.

---

## Why Progressive Disclosure Matters

- The context window is a scarce, expensive resource
- Loading every procedure all the time does not scale
- Most of any given skill is irrelevant to most tasks
- Disclosing detail lazily keeps context focused and cheap

---

## The Context-Cost Tradeoff

![context_savings](svg/lectures/ai/skills/context_savings.svg)

---

## How an Agent Uses a Skill

![lifecycle](svg/lectures/ai/skills/lifecycle.svg)

---

## The Match Is Semantic

- No regex, no rule engine, no keyword table
- The model *reads* the descriptions and judges relevance
- This is flexible — it handles paraphrase and intent
- It is also fragile — a vague description simply never wins

---

## The Description Is Everything

![description_matters](svg/lectures/ai/skills/description_matters.svg)

---

## Writing a Good Description

1. State the capability in concrete terms
1. Name the triggers — words a user would actually say
1. Add a "use when…" clause to mark the boundary
1. Avoid overlap with your other skills

---

## Description: Before and After

```yaml
# Weak — never fires
description: Helps with documents

# Strong — fires on the right tasks
description: >
  Fill, split, and extract text from PDF forms.
  Use when the user mentions PDFs or form fields.
```

---

## Skills vs Tools vs RAG vs Fine-Tuning

![skills_vs_alternatives](svg/lectures/ai/skills/skills_vs_alternatives.svg)

---

## Four Different Questions

- **Skill** — *how* do I do this task?
- **Tool / MCP** — *what action* can I take in the world?
- **RAG** — *what facts* are true or known?
- **Fine-tuning** — what behaviour is *baked into* the model?

---

## They Are Complementary

- A skill often *instructs the agent to call a tool*
- A skill can tell the agent *when to retrieve* with RAG
- Fine-tuning shapes instinct; skills supply explicit procedure
- A mature agent uses all four together

---

## When to Reach for a Skill

- The task is **procedural** — there are steps to follow
- It **recurs** — you do it more than once
- It has **conventions** specific to you or your team
- You want it **inspectable and versioned**, not hidden in weights

---

## When NOT to Use a Skill

- A pure, stateless action → expose a **tool** instead
- Large bodies of changing facts → use **RAG**
- A behaviour needed on *every* request → maybe a system prompt
- A one-off task you'll never repeat → just ask directly

---

## Skills Are Portable

![portability](svg/lectures/ai/skills/portability.svg)

---

## The Same Folder, Many Hosts

- **Claude Code** discovers skills in a skills directory
- The **Claude Agent SDK** can load a folder as a skill source
- **Other LLM agents** can adopt the same convention
- **Your own harness** can parse the front matter and load lazily

The artifact is portable; only the loading glue differs.

---

## A Minimal Loader (Any Agent)

```python
# 1. At startup, read every skill's name + description
# 2. Put just those lines in the system prompt
# 3. When the model says "use skill X", read X/SKILL.md
# 4. Add the body to context; follow its links on demand
```

Skills are *just files plus a convention* — easy to support anywhere.

---

## Authoring a Skill

![authoring_loop](svg/lectures/ai/skills/authoring_loop.svg)

---

## The Authoring Loop

1. **Do it once by hand** — note where the agent struggles
1. **Capture the steps** — write SKILL.md and a sharp description
1. **Test on real tasks** — does it fire? does it succeed?
1. **Refine and trim** — cut noise, push detail to linked files

---

## Write It Like Documentation

- Your reader is a capable but forgetful colleague
- Be explicit about steps, order, and edge cases
- Prefer short and clear over long and exhaustive
- Show, don't just tell — include a worked example

---

## Scripts vs Tokens

![scripts_in_skills](svg/lectures/ai/skills/scripts_in_skills.svg)

---

## When to Ship a Script

- Use the **model** for fuzzy, judgement work: summarize, classify, rewrite
- Ship a **script** for exact, repeatable work: parse, validate, transform
- Scripts are deterministic, cheap, and testable
- Tell the agent in SKILL.md which path to take, and when

---

## Rule of Thumb

> If the task has a single correct answer every time, give the agent a **script** — not a paragraph.

- Saves tokens
- Removes a class of mistakes
- Makes the skill's behaviour reproducible

---

## Common Pitfalls

![pitfalls](svg/lectures/ai/skills/pitfalls.svg)

---

## Pitfall: The Kitchen-Sink Skill

- One skill that tries to "do everything"
- Vague trigger, bloated body, slow to load
- **Fix:** one skill, one job — split by single purpose

---

## Pitfall: Overlapping Skills

- Two descriptions both match the same request
- The agent picks unpredictably between them
- **Fix:** make boundaries crisp; disjoint "use when" clauses

---

## Security: Skills Run Code

- A skill can carry scripts and *instructions*
- Both can do harm if the skill is malicious
- Treat an installed skill like any third-party dependency
- **Review before you install; scope what scripts may touch**

---

## Good Habits

- Version skills in git; review diffs like code
- Keep each body lean; push detail to linked files
- Sandbox or scope bundled scripts
- Re-test descriptions when you add a neighbouring skill
- Prefer many small, sharp skills over a few broad ones

---

## A Worked Example: Brand Voice

```markdown
---
name: brand-voice
description: >
  Rewrite copy in ACME's house style.
  Use when drafting public-facing text: emails, posts, docs.
---

# ACME Brand Voice

- Warm, plain, second person ("you")
- No jargon; expand acronyms on first use
- See `examples.md` for before/after pairs
```

---

## What the Example Shows

- A clear, trigger-rich description
- A short body with the rules that matter most
- Detail (the examples) deferred to a linked file
- Zero code — pure procedural knowledge, loaded on demand

---

## Skills and Multi-Agent Systems

- A sub-agent can be given just the skills it needs
- Keeps each agent's context small and on-topic
- Skills become the shared vocabulary between agents
- Compose: a planner agent picks skills for worker agents

---

## The Mental Model

![mental_model](svg/lectures/ai/skills/mental_model.svg)

---

## Summary

- A skill is a **folder of instructions** loaded **on demand**
- **Progressive disclosure** keeps context cheap and focused
- The **description** decides whether a skill ever fires
- Skills complement tools, RAG, and fine-tuning — they don't replace them
- They are **portable**: just files plus a convention

---

## Where to Start

1. Pick one repetitive task you do today
1. Write a single SKILL.md with a sharp description
1. Test whether your agent reaches for it
1. Trim, then grow a small library over time

Move expertise out of heads and into versioned, reusable files.

---

## Questions?

- Skills turn run-time instructions into reusable assets
- No retraining, no lock-in, fully inspectable
- Start small, iterate, and share

## Thank You
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)
