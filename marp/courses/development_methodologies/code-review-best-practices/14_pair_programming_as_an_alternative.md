---
tags:
  - practices:code-review
  - practices:pair-programming
level: beginner
category: methodology
audience:
  - audiences:developers

---
# Pair Programming as an Alternative

---
## What This Chapter Covers

- What pair programming is
- When pairing replaces review
- Combining pairing and review
- Trade-offs and benefits
- Remote pairing
- A practical adoption strategy

---
## What Pairing Is

- Two developers, one keyboard, one screen
- One drives (types); the other navigates (thinks ahead)
- Switch roles every 20-30 minutes
- Same task, simultaneous attention
- Active collaboration, not just sitting together

---
## How It Replaces Review

- The "second pair of eyes" happens in real time
- Bugs caught as they're written
- Design discussion before code is committed
- No separate review step needed (often)
- Faster integration; lower defect rate

---
## When Pairing Wins

- Hard problems
- Onboarding new team members
- Cross-training across the team
- Critical changes that need extra care
- Code in unfamiliar areas of the codebase

---
## When Pairing Loses

- Simple, well-understood work
- Independent task chunks
- When one person needs deep focus
- When the team is geographically scattered (mitigated by remote tools)
- When personalities clash

---
## Pairing + Review

- Pair on the change
- A *third* developer reviews the PR
- Catches things both pair members missed
- Spreads knowledge to a third person
- Best of both worlds; higher cost

---
## Trade-Offs

- Pro: fewer bugs, better designs, knowledge sharing
- Pro: real-time mentoring
- Con: 2x developer-hours per task
- Con: exhausting if done all day
- Con: cultural fit varies

---
## Throughput Math

- 2 devs pairing produce *less* than 2 devs working separately on simple tasks
- 2 devs pairing produce *more* than 2 devs working separately on hard tasks
- The crossover depends on task complexity
- Many studies; results vary; teams must experiment

---
## Mob Programming

- The whole team works on one thing, on one screen
- One driver, everyone navigates
- For very hard problems, knowledge sharing
- 4-6 people typical
- Pair programming taken to its limit

---
## When Mobbing Wins

- Designing a critical new system
- Onboarding multiple new hires
- Unblocking a stuck team
- Working through a complex algorithm
- Team-wide pattern adoption

---
## Remote Pairing

- VS Code Live Share, JetBrains Code With Me, GitHub Codespaces
- Both can edit the same file
- Voice over Zoom / Slack
- Works as well as in-person for many teams
- Async pairing exists but loses much of the benefit

---
## Pairing Etiquette

- Switch driver/navigator regularly
- Talk through your thinking
- Ask questions, don't lecture
- Take breaks (it's exhausting)
- Don't dominate the keyboard

---
## Pair-Programming Anti-Patterns

- "Backseat driver" who takes over the keyboard
- Silent navigator who just watches
- Pair as performance review of the junior
- Endless theoretical discussion, no code written
- Pair on simple tasks "for the value" — none gained

---
## Adoption Strategy

- Try pairing for one task per week
- Mix the pairs (don't always pair the same two)
- Rotate driver/navigator
- Retro after a month: what worked? what didn't?
- Adopt what your team likes; drop what they don't

---
## When Reviews Are Better

- Async work across time zones
- Independent tasks with low coupling
- Personal preference for solo focus
- Team culture that values flow
- Not every team enjoys pairing

---
## Combining Reviews and Pairing

- Pair on the *design* and the *risky parts*
- Solo on the *implementation*
- Review for substance and integration
- A balanced practice
- Most healthy teams blend the two

---
## Common Mistakes

- Pairing on everything (exhausting; diminishing returns)
- Pairing on nothing (missing the high-leverage cases)
- Pairing one senior with one junior, calling it mentoring (often is just supervision)
- Replacing reviews entirely with pairing without third-eye check
- Forcing the practice on a resistant team
