---
tags:
  - data-and-ai:ai
  - data-and-ai:llm
  - practices:productivity
level: intermediate
category: ai
audience:
  - audiences:developers
  - audiences:senior-developers

---

# Skills

---

## What This Chapter Covers

- What a skill is
- Built-in skills
- Authoring a skill
- Slash commands
- When not to use one

---

## What A Skill Is

- A named, reusable instruction set
- Has its own tools and rules
- Invoked when relevant
- A way to package a workflow

---

## Skills Vs Plain Prompts

- A prompt is one-shot
- A skill is durable and reusable
- A skill has a description that triggers it
- A skill can scope its tools

---

## Skills Vs Agents

- A skill runs in the main conversation
- An agent runs in its own context
- A skill shares your tokens
- An agent does not

---

## Skills Vs Sub-Agents

![skills_vs_agents](svg/courses/ai/claude-workshop/04_skills/skills_vs_agents.svg)

---

## Anatomy Of A Skill

- A name and a description
- Trigger conditions
- Instructions and rules
- Optional tool list

---

## Built-In Skills

- Shipped with Claude Code
- Visible in the skills list
- Cover common workflows
- A good place to learn the pattern

---

## Touring The Built-Ins

- `init` to set up CLAUDE.md
- `review` to review a PR
- `security-review` for a security pass
- `update-config` to edit settings

---

## Reading A Skill Description

- The description tells when it fires
- Lead with the trigger words
- Be specific about scope
- Avoid overly broad descriptions

---

## Invoking Explicitly

- Type `/<name>` to call it
- The model still decides how to apply it
- Arguments after the name pass in
- Useful for testing a new skill

---

## Authoring A Skill

- Place a file in `.claude/skills/`
- Name it after the trigger
- Write a clear description
- Write the instructions

---

## Anatomy Visualized

![skill_anatomy](svg/courses/ai/claude-workshop/04_skills/skill_anatomy.svg)

---

## A Good Description

- States the trigger conditions
- Lists example phrases
- Says what is in scope
- Says what is out of scope

---

## Scoping Tools

- Allow only what the skill needs
- Read-only skills should not have Write
- Bash should be the last resort
- Smaller scope is safer

---

## Versioning A Skill

- Commit it to the repo
- Treat it like code
- Review changes in PRs
- Tag with the team that owns it

---

## Sharing Across A Team

- Project skills live in the repo
- Personal skills live in `~/.claude/skills/`
- Shared skills can live in a separate repo
- Symlinks or a sync tool keep them in step

---

## Slash Commands

- A user-facing way to invoke a skill
- Maps a team workflow to a name
- Short and memorable
- Documented in CLAUDE.md

---

## Workflow Patterns

- `review` to do a structured PR review
- `refactor` to apply a known refactor
- `summarize` for a meeting note
- `audit` for a checklist pass

---

## A Concrete Example

- Skill: `release-notes`
- Reads recent commits
- Groups by type
- Outputs markdown for the changelog

---

## When Not To Use A Skill

- One-off tasks
- Things easier to type than to invoke
- Cases where a prompt is clearer
- Tasks that change every time

---

## Common Skill Mistakes

- Description too vague to trigger
- Description too broad and fires everywhere
- Doing too much in one skill
- Not scoping tools

---

## Hands-On Exercise

- Write a skill that runs your linter
- Trigger it implicitly with a prompt
- Trigger it explicitly with `/<name>`
- Iterate on the description until it fires when you want
