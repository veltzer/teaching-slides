---
tags:
  - practices:code-review
level: beginner
category: methodology
audience:
  - audiences:developers

---

# Review Checklists

---

## Reviewer's Checklist

![review_checklist](svg/courses/development_methodologies/code-review-best-practices/10_review_checklists/review_checklist.svg)

---

## Checklist Topics

![checklist_topics](svg/courses/development_methodologies/code-review-best-practices/10_review_checklists/checklist_topics.svg)

---

## What This Chapter Covers

- Why use checklists
- Creating team-specific checklists
- Common checklist items
- Avoiding checklist fatigue
- When to use, when to skip
- Sample checklists

---

## Why Checklists Help

- Tired reviewers miss things
- A short list keeps the basics covered
- Especially helpful for junior reviewers
- New domains (security, perf) benefit most
- Famous in medicine, aviation; works for code too

---

## When Checklists Fail

- Too long &#8594; nobody reads
- Too generic &#8594; no value
- Mandatory checkbox-ticking &#8594; rubber stamping
- Feels like ritual, not engagement
- A wrong checklist is worse than none

---

## A Generic Starting Point

- [ ] PR description explains what and why
- [ ] Tests added or updated
- [ ] No commented-out code
- [ ] No debug logging
- [ ] CI passes

---

## A Bug-Fix Checklist

- [ ] Root cause identified, not symptom
- [ ] Test reproduces the original bug
- [ ] Fix is minimal — no scope creep
- [ ] Similar code elsewhere checked for same bug
- [ ] Issue or ticket linked

---

## A New-Feature Checklist

- [ ] Design discussed before coding
- [ ] Acceptance criteria met
- [ ] Tests cover happy and edge cases
- [ ] Logging and metrics adequate
- [ ] Docs updated
- [ ] Migration / rollout plan if needed

---

## A Security-Sensitive Checklist

- [ ] Untrusted input validated
- [ ] No secrets in code or config
- [ ] Auth checked at every entry point
- [ ] Output encoded for context (HTML, SQL)
- [ ] Error messages don't leak sensitive info
- [ ] Crypto uses proven libraries

---

## A Performance-Sensitive Checklist

- [ ] N+1 queries checked
- [ ] Loops bounded
- [ ] Large allocations justified
- [ ] Network calls async / non-blocking
- [ ] Profiled before claiming "fast"

---

## A Refactoring Checklist

- [ ] Behaviour preserved (tests still pass without changes)
- [ ] No new dependencies
- [ ] No new public APIs
- [ ] Diff scope is the refactor only
- [ ] Easier to read after than before

---

## A Database-Migration Checklist

- [ ] Backward-compatible (deploys old + new code together)
- [ ] Long-running operations chunked
- [ ] Indexes added before queries that use them
- [ ] Tested against production-size data
- [ ] Rollback plan documented

---

## Per-Team Checklists

- Build your own based on incidents you've had
- "Last quarter's bugs would've been caught by..."
- Document with the team
- Review the checklist itself periodically
- Drop items that never trigger

---

## Lightweight Checklists

- 3-5 items max for general use
- Specific checklists for specific change types
- One-line items, not paragraphs
- Linked from the PR template
- A 30-second mental scan, not a 30-minute exercise

---

## When To Use a Checklist

- Reviewing in a domain you don't know well
- Reviewing a security-sensitive change
- Reviewing a database migration
- Onboarding new reviewers
- After a recent bug pattern surfaced

---

## When Not To Use One

- Trivial PRs
- Small fixes
- Doc-only changes
- A checklist would slow you down for no benefit
- Match effort to risk

---

## Avoiding Checklist Fatigue

- Keep them short
- Keep them current
- Differentiate "must" from "consider"
- Don't make checking mandatory; make it visible
- Check the items genuinely, not as a ritual

---

## Common Mistakes

- 30-item checklist nobody completes
- Same checklist for every PR
- Treating checklist items as merge gates
- Never updating the checklist
- Inventing the checklist alone instead of with the team
