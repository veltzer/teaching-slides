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
  - audiences:devops

---
# Putting It All Together

---
## What This Chapter Covers

- Review of what we built
- A team adoption checklist
- Pitfalls to watch for
- Where to go next

---
## What We Configured Today

- A user-level settings.json
- A project settings.json
- A CLAUDE.md per repo
- Allowlists and hooks

---
## What We Extended

- One or more skills
- At least one MCP server
- Sub-agents for delegated work
- A minimal RAG pipeline

---
## What We Practiced

- Reading the token budget
- Triggering compaction deliberately
- Briefing agents well
- Reading the diff before merging

---
## A Team Adoption Checklist

- Pick a default model per project
- Commit CLAUDE.md to every repo
- Allowlist routine commands as a team
- Add hooks for lint and format

---
## The Checklist Visualized

![adoption_checklist](svg/courses/ai/claude-workshop/08_wrap_up/adoption_checklist.svg)

---
## Skills As Team Workflows

- Identify three repeated workflows
- Write a skill for each
- Commit them with the repo
- Iterate on descriptions until they trigger

---
## Agents As An Org Habit

- Use Explore for "where is X"
- Use Plan before any big change
- Use worktree isolation for risky work
- Read the diff every time

---
## MCP As Glue

- Wrap one or two internal tools
- Treat each server as a security boundary
- Pin versions, review updates
- Audit before installing

---
## RAG Where It Earns Its Keep

- Internal knowledge bases
- Support and onboarding
- Code search and explain
- Compliance and legal lookup

---
## Pitfalls To Watch For

- Treating the agent as omniscient
- Skipping diff review
- Letting hooks paper over real bugs
- Ignoring the cost meter

---
## Cultural Pitfalls

- "AI did it" as an excuse
- Refusing to use it at all
- Skipping code review on AI diffs
- Hoarding workflows on personal laptops

---
## Cost And Quality Levers

- Pick the smallest model that works
- Cache aggressively
- Compact deliberately
- Delegate to keep main context lean

---
## Security Levers

- Allowlist narrowly
- Audit MCP servers
- Treat tool output as untrusted
- Never commit secrets

---
## Measuring Adoption

- Time to first commit on a new feature
- PRs that include AI-assisted work
- Build and test pass rates
- Developer satisfaction surveys

---
## Where To Go Next

- Deeper dive into prompt engineering
- Building production-grade RAG
- Building your own agents
- Evaluating LLM systems

---
## Recommended Follow-Ups

- A prompt engineering course
- A RAG production course
- An MCP authoring deep-dive
- A team adoption workshop

---
## Final Thoughts

- The tools shift fast, fundamentals do not
- Configuration and context outlast prompts
- Trust but verify, every time
- Have fun with it

---
## Thank You

- Questions and discussion
- Feedback shapes the next workshop
- Stay in touch
- mark.veltzer@gmail.com
