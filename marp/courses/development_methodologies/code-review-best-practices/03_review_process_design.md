---
tags:
  - practices:code-review
level: beginner
category: methodology
audience:
  - audiences:developers
  - audiences:managers

---
# Review Process Design

---
## What This Chapter Covers

- When to request a review
- Choosing reviewers
- Required vs optional reviews
- Turnaround time expectations
- Approval workflows
- A practical process per team size

---
## When to Request

- After local testing passes
- After CI passes (or you know why it doesn't)
- After self-review (read your own diff first)
- When you've explained the change in the description
- *Not*: as soon as you finish typing

---
## Process Choices

![process_choices](svg/courses/development_methodologies/code-review-best-practices/03_review_process_design/process_choices.svg)

---
## Choosing Reviewers

- One reviewer is the minimum
- Two for important changes
- Specialists for: security, performance, infrastructure
- Don't always pick the same person — spread the load
- CODEOWNERS files automate routing

---
## CODEOWNERS

```misc
# require frontend team for UI files
/web/      @frontend-team
# specific person for the security module
/auth/     @alice
```

- File in repo root
- GitHub / GitLab read it; auto-request reviews
- Avoids "who should review this?" guesswork
- Update when team membership changes

---
## Required vs Optional Reviewers

- **Required**: must approve before merge
- **Optional**: invited but not blocking
- Use required sparingly: the people who *must* see it
- Optional for FYI / cross-team awareness
- Too many required = bottleneck

---
## Turnaround Time

- Aim: review within one business day
- Faster for small PRs; slower OK for big ones
- Authors should set expectations: "no rush" or "blocking"
- Reviewers should communicate if they can't get to it
- Stale PRs rot quickly — pick them up or release them

---
## Reviewing Promptly

- Schedule review time daily, not "when I have a moment"
- 30 minutes after standup, 30 minutes before lunch — works for many
- A queue per reviewer, not a free-for-all
- Notifications honestly, not "I'll get to it"
- A team where reviews are prioritised ships faster

---
## Approval Workflows

- Single approval: one reviewer says yes &#8594; merge
- Two approvals: two yeses
- Approval-after-discussion: must address comments
- Required CI checks: green builds, tests, security scans
- Many platforms support combinations

---
## Branch Protection Rules

- Require PR before merge
- Require at least N approvals
- Require CI to pass
- Require up-to-date branch
- Forbid force-push to main
- Most projects need at least these five

---
## Merge Strategies

- **Merge commit**: preserves PR structure
- **Squash and merge**: one commit per PR (clean history)
- **Rebase and merge**: linear history, individual commits
- Pick one as a team standard; debate is otherwise endless
- "Squash and merge" is the common modern default

---
## Self-Review First

- Open the PR, read your own diff
- 50% of reviewer comments would be caught here
- Spotting your own changes from a fresh angle helps
- Especially: leftover debug code, commented-out code, typos
- Do this before requesting reviewers' time

---
## PR Description

- Explain *what* changed and *why*
- Link to the issue or design doc
- Mention what was tested and how
- Call out anything unusual
- A good description halves review time

---
## A PR Description Template

```misc
## What
Brief summary of the change.

## Why
The problem this solves.

## How
Notable implementation choices.

## Testing
What you ran; what passed; manual steps if any.

## Risk
What could break; rollback plan if needed.
```

- Most platforms support PR templates as a file in `.github/`
- Slightly different per project; a template helps consistency

---
## Process Per Team Size

- Solo: pair-program with someone or skip review (with risk)
- 2-5 people: simple process, peer reviews, small PRs
- 6-15: CODEOWNERS, two-approval requirement for risky areas
- 15+: cross-team reviews, dedicated reviewers, time budgets
- Process should grow with the team, not ahead of it

---
## Common Process Mistakes

- Process so heavy nothing ships
- No process &#8594; quality drift
- Required reviewers who never review &#8594; bottleneck
- Approving without reading
- Rushing reviews to clear the queue
- Not having a clear "what should I review next?" signal
