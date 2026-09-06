---
tags:
  - practices:technical-writing
  - practices:review
level: beginner
category: methodology
audience:
  - audiences:developers

---

# Review Processes

---

## Reviewing Docs

![review_for_docs](svg/courses/development_methodologies/technical-writing/11_review_processes/review_for_docs.svg)

---

## Documentation Review Stages

![review_stages](svg/courses/development_methodologies/technical-writing/11_review_processes/review_stages.svg)

---

## What This Chapter Covers

- Peer review for documentation
- Editorial checklists
- Feedback loops with users
- Review hygiene specific to docs
- Roles in the review process
- Building review into the team's rhythm

---

## Why Review Docs

- Two pairs of eyes catch what one misses
- Reviewers ask the questions readers will
- Style and consistency enforced naturally
- Knowledge spreads through reviewing
- Review is where docs get good

---

## Doc Reviews vs Code Reviews

- Same PR, same tools
- Different focus: clarity over correctness
- "I don't understand this" is the most useful comment
- Less back-and-forth typically
- Skim of preview deploy, then close read

---

## Who Should Review

- Domain expert: catches accuracy issues
- Writer or editor: catches clarity issues
- New developer: catches assumed knowledge
- Get all three when possible
- For small teams: rotate roles

---

## Editorial Checklists

- Style consistency (per the team style guide)
- Heading hierarchy
- Code examples tested
- Links work
- Spelling and grammar
- A short checklist; not a 50-item form

---

## A Sample Editorial Checklist

- [ ] Title and headings clear
- [ ] One topic per section
- [ ] Code examples runnable
- [ ] No passive voice without reason
- [ ] No jargon undefined on first use
- [ ] Links work (internal and external)
- [ ] Images have alt text

---

## Feedback Loops With Users

- Track which docs are read (page analytics)
- Track which docs lead to support tickets
- Survey users on doc satisfaction
- "Was this page helpful?" widgets
- Acted-on feedback closes the loop

---

## Page Analytics

- Time on page, exit rate, search queries
- Identifies docs that aren't doing their job
- Pages with high exit rate often confuse
- Pages with low traffic might need promotion or deletion
- Use as signal, not gospel

---

## Support Ticket Mining

- Common questions in tickets &#8594; missing docs
- Repeat questions &#8594; doc that exists but isn't found / clear
- Each ticket is a vote for a doc improvement
- Quarterly review of ticket categories vs doc coverage
- Closes the loop between docs and reality

---

## "Was This Helpful?" Widgets

- Single thumb-up / thumb-down per page
- Optional follow-up: "what was missing?"
- Aggregated trends drive priorities
- Free in most modern doc platforms
- Pay attention to the negatives

---

## Reviewing Changed Pages

- A doc change PR should have someone outside the author review
- Even small changes benefit
- Especially: anything user-facing
- Auto-routing via CODEOWNERS
- Don't merge unreviewed user-facing docs

---

## Reviewing Existing Docs

- Quarterly: check pages by traffic
- Update what's read; archive what's not
- A doc owner per area
- Less effort than rewriting from scratch later
- Continuous maintenance beats periodic overhaul

---

## Doc Review Roles

- **Author**: writes the change
- **Subject expert**: checks accuracy
- **Editor**: checks clarity and style
- **User proxy**: a fresh reader (often a junior or someone from another team)
- Smaller teams: one person plays multiple roles

---

## Onboarding a Doc Reviewer

- Read the style guide
- Pair-review with an experienced reviewer for a few PRs
- Start with smaller PRs
- Manager check-in after a month
- Same approach as code review onboarding

---

## When To Reject

- Inaccurate (factually wrong)
- Confusing (a fresh reader gets lost)
- Off-style (and doesn't match style guide for a reason)
- Out of scope (this PR shouldn't change that doc)
- Suggest improvements; don't just say no

---

## When To Approve

- Accurate
- Clear
- On-style
- Doesn't make the doc worse than before
- "Better than what was there" is enough; perfect is the enemy of good

---

## Common Doc Review Mistakes

- Approving a doc the reviewer doesn't actually understand
- Nitpicking on style while missing inaccuracy
- Not running the code examples
- Letting docs sit in review for weeks
- No feedback loop with actual users
