---
tags:
  - practices:agile
  - practices:engineering
level: beginner
category: practices
audience:
  - audiences:developers
  - audiences:team-leads

---
# Agile Engineering Practices

---
## What This Chapter Covers

- The engineering practices that make Agile actually work
- Continuous integration and continuous delivery
- Test-driven development
- Pair programming and mob programming
- Refactoring and managing technical debt
- Trunk-based development and feature flags
- The role of automation

---
## Why Engineering Matters Here

- Scrum is silent on *how* you build the software
- Agile rituals without engineering practices produce bad software faster
- The ability to ship every day depends on engineering, not on standups
- Most "Agile failures" are really engineering failures
- This chapter is what closes the loop

---
## Continuous Integration

- Every code change is integrated and tested *automatically* on every push
- Catches conflicts and regressions when they're cheap to fix
- Required: a test suite that runs in minutes, not hours
- Required: discipline — broken builds get fixed *before* anything else
- Without CI, "we're agile" means "we batch up problems for sprint end"

---
## Continuous Delivery

- Every change that passes CI is *deployable*
- Doesn't mean every change is deployed — that's continuous *deployment*
- Requires automated builds, tests, and deployment pipelines
- Requires a real production-like staging environment
- Removes the "release weekend" and the heroics that come with it

---
## Continuous Deployment

- Every change that passes CI is *automatically deployed*
- Sounds scary; in practice, smaller changes mean smaller risks
- Requires excellent automated testing and monitoring
- Pair with feature flags so risky changes can be hidden
- Top-tier teams ship 100+ times per day this way

---
## Test-Driven Development

- Write a failing test first
- Write the smallest code that makes it pass
- Refactor with the tests as a safety net
- Repeat
- Forces design pressure — code that's hard to test is hard to use

---
## TDD Doesn't Just Mean "Tests"

- Tests-after produce coverage, not design
- TDD's value is in the *design feedback loop*
- Hard to test &#8594; rethink the design before it ossifies
- Skipping the test-first step misses the point
- That said, tests-after is still better than no tests

---
## Pair Programming

- Two developers, one keyboard, one screen
- Roles: driver (typing) and navigator (thinking ahead)
- Switch roles every 20-30 minutes
- Code review built in — no separate review step needed
- Knowledge spreads naturally — bus factor improves immediately

---
## Pair Programming Trade-offs

- Slower in pure throughput on simple tasks
- Faster on hard tasks, fewer bugs, better designs
- Exhausting if done all day; many teams pair on hard things only
- Remote pairing works (VS Code Live Share, JetBrains Code With Me)
- Cultural fit varies — try it, see if your team likes it

---
## Mob Programming

- The whole team works on one thing, on one screen, together
- One driver at a time; everyone else navigates
- Best for: hard problems, knowledge sharing, onboarding new team members
- Worst for: simple, parallelisable work
- Some teams mob full-time; most reach for it as a tool when stuck

---
## Refactoring

- Improve the design of existing code without changing its behaviour
- Continuous, not a separate "refactoring sprint"
- Done in small steps, with tests passing after each one
- The Boy Scout Rule: leave the code cleaner than you found it
- "We don't have time to refactor" is the path to a codebase no one wants to touch

---
## Technical Debt

- Shortcuts taken now that will cost more later
- *Some* tech debt is fine — strategic, intentional, tracked
- *Most* tech debt is unintentional and accretes silently
- Pay it down continuously, not in dedicated sprints
- A team that says "we'll clean it up later" rarely does

---
## Trunk-Based Development

- Everyone works off a single shared branch ("trunk" or "main")
- Branches are small and short-lived (hours, not days)
- Merge to trunk daily at minimum
- Avoids long-lived branch divergence and merge hell
- Forces small, incremental change — pairs naturally with CI

---
## Feature Flags

- Toggle features on/off at runtime without redeploying
- Lets unfinished features ship to production *off*
- Lets features roll out gradually (1% &#8594; 10% &#8594; 100%)
- Lets you kill a broken feature instantly
- Pair with trunk-based development to ship safely all day

---
## Automation Is the Glue

- Tests, builds, deployments, infrastructure, monitoring — all in code
- Every manual step is a chance to forget, get tired, or be inconsistent
- Automate the boring, repeatable; spend humans on the novel
- Investment up front pays back many times over a project's life
- A team without automation is using Agile theatre

---
## A Short Maturity Ladder

- Manual builds, manual tests, manual deploys: pre-Agile
- Automated tests, manual deploys: better — most teams here
- CI + CD pipeline + automated deploys: real continuous delivery
- Trunk-based + feature flags + 100s of deploys/day: top tier
- Pick a step up from where you are; don't try to leap

---
## Course Wrap-Up

- Agile is a values document, not a process recipe
- Scrum is one good implementation; Kanban is another
- Stories, estimates, sprints are *tools*, not *goals*
- Engineering practices are what make any of it work
- The team that inspects and adapts honestly is the team that improves
