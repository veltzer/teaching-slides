---
tags:
  - practices:code-review
level: beginner
category: methodology
audience:
  - audiences:developers

---
# Why Code Review Matters

---
## What This Chapter Covers

- The benefits of code review
- Bug catching, knowledge sharing, quality
- Code review as a learning tool
- The cost of skipping reviews
- Evidence from research
- The cultural payoff

---
## What Code Review Is

- Another developer reads your code before it lands
- Comments, suggestions, approval (or not)
- Most teams use a tool: GitHub PRs, GitLab MRs, Gerrit
- Universal in modern professional teams
- A practice, not a tool

---
## Why It Earns Its Time

![review_value](svg/courses/development_methodologies/code-review-best-practices/01_why_code_review_matters/review_value.svg)

---
## The Direct Benefits

- **Catches bugs early**: cheaper to fix before merge
- **Improves quality**: a second pair of eyes catches what authors miss
- **Spreads knowledge**: more people understand more of the codebase
- **Reduces tech debt**: pushes back on shortcuts in real time
- **Documents decisions**: PR comments are searchable history

---
## Knowledge Sharing

- Without reviews, only the author knows the code
- That author leaves &#8594; nobody knows
- Reviews force a second person to understand
- Reduces the bus factor (lowest number of people who can leave before the team's stuck)
- Major risk reduction at no extra cost

---
## Mentoring

- Reviews are where junior developers learn
- Senior reviewers explain *why*, not just "change this"
- Patterns and idioms transmit through reviews
- Style guidelines stick because they're enforced in real PRs
- The most underrated benefit

---
## Code Review as Documentation

- A merged PR contains: the change, the discussion, the decisions
- "Why did we do it this way?" &#8594; check the PR
- Better than wiki pages that go stale
- Captures alternatives considered and rejected
- Searchable forever in your git history

---
## What Reviews Don't Do

- They don't catch every bug — tests still matter
- They don't verify functional correctness — testing does
- They don't replace good design discussions earlier
- They aren't a security audit (though they help)
- Use the right tool for the right purpose

---
## The Cost of Skipping

- More bugs in production
- Knowledge concentrated in one head
- Code style drift across the codebase
- New developers learn from chaos
- Slower in the long run, faster in the short

---
## Evidence

- SmartBear and others have studied code review extensively
- Reviews catch ~50-70% of defects when done well
- Best ROI when authors and reviewers are engaged
- Diminishing returns past 60 minutes per PR
- Speed and quality both benefit, despite intuition

---
## The Cultural Payoff

- Trust builds when feedback is constructive
- Authors learn to anticipate reviewer concerns
- Reviewers learn the codebase deeply
- Discussions surface design tensions early
- A team with healthy reviews is a team with low ego

---
## When Reviews Become Theatre

- "LGTM" with no actual reading
- Reviews approved at 5pm so the change can ship
- Comments on style only, never on substance
- Approval as a gate, not a discussion
- This is worse than no reviews — false confidence

---
## Indicators of Healthy Reviews

- Authors thank reviewers genuinely
- Reviewers ask clarifying questions
- Disagreements happen and resolve
- Junior developers ship after PR feedback
- The codebase has a recognisable style

---
## Setting Expectations

- Every change goes through review
- Reviews are part of the work, not extra
- Time to review is part of velocity
- Reviewers are accountable for what they approve
- Authors are accountable for what they wrote

---
## What's Next

- Goals of code review
- The review process
- What to look for
- How to give and receive feedback
- Tools and metrics
- Building a culture
