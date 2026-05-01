---
tags:
  - practices:code-review
  - practices:metrics
level: beginner
category: methodology
audience:
  - audiences:developers
  - audiences:managers

---
# Review Metrics

---
## What This Chapter Covers

- Why measure review work
- Time to review
- Review throughput
- Comment density
- Using metrics responsibly
- The risk of misuse

---
## Why Measure

- Spot bottlenecks
- Identify patterns of friction
- Guide process improvement
- Demonstrate the value of reviewing
- *Not*: ranking individuals

---
## Time to First Review

- Hours from PR opened to first comment / approval
- Aim: under 1 business day
- Long times signal: too few reviewers, low priority, oversized PRs
- Watch the *p95*, not just the median
- The metric most predictive of team velocity

---
## Time to Merge

- From PR opened to merged
- Includes all rounds of review
- 2-3 days median is typical
- Above a week: investigate
- Long-tail PRs are often stuck on disagreement

---
## Throughput

- Number of PRs merged per week (per team)
- Useful as a trend, not a target
- Goes down when refactors land; goes up when shipping
- Compare against historical baseline
- Don't optimise this number directly

---
## PR Size Distribution

- Histogram of lines changed
- Aim: most PRs under 200 lines
- Long tail of huge PRs reveals splitting opportunities
- Track over time: is the distribution shifting?
- Visible to the team often nudges behaviour

---
## Comment Density

- Comments per 100 lines of changed code
- Lower for small fixes; higher for risky changes
- Outliers point to PRs that needed more discussion
- Useful for noticing rubber-stamping (comment density of zero)
- Don't target a number — observe and ask why

---
## Review Participation

- Per-developer: how many PRs reviewed vs authored
- Imbalanced participation flags burnout risk
- Some senior people get over-loaded
- CODEOWNERS distribute load by area
- Periodic check-ins help

---
## Re-Open Rate

- PRs reopened after merge (something broke)
- High rate = reviews aren't catching issues
- Investigate root causes, not the people
- Often: PR too large, reviewer too rushed, missing tests
- A leading indicator of quality

---
## Coverage Metrics In Review

- Did test coverage drop?
- Did the PR add tests?
- Many CI tools surface this in the PR comments
- Coverage isn't quality — but a sudden drop is a signal
- Use it to prompt conversation, not as a hard gate

---
## DORA Metrics for Reviews

- The DORA framework includes "lead time for changes"
- That includes review time
- Reviews are part of the engineering pipeline
- Optimising review throughput improves DORA
- Useful in management conversations

---
## Misusing Metrics

- "You reviewed 12 PRs this week, you should do 20" — disaster
- Goodhart's law: a measure as a target stops being a good measure
- Speed metrics &#8594; rubber-stamping
- Comment count metrics &#8594; nitpicking
- Use metrics for *team*-level diagnosis, not individual evaluation

---
## What To Show The Team

- Aggregate trends, not individual scoreboards
- Time-to-first-review by week
- Median PR size
- Re-open rate
- Long-stuck PRs that need attention
- Surface, discuss, improve

---
## What To Avoid Showing

- Per-person review counts
- Per-person comment counts
- Speed rankings
- Anything that creates competition for the wrong thing
- Healthy reviews are slow when they need to be

---
## Process Improvements

- Long times to first review &#8594; better routing, more reviewers
- High re-open rate &#8594; smaller PRs, better tests
- Long lead times &#8594; CI speed, async expectations
- Each metric points at a process change
- Iterate on the process; don't blame the people

---
## Common Mistakes

- Tracking metrics nobody acts on
- Using metrics to discipline rather than improve
- Treating speed as the only metric
- Punishing the people who *do* the most reviews
- Forgetting metrics are signals, not truth
