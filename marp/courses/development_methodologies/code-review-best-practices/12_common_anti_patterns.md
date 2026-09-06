---
tags:
  - practices:code-review
  - practices:antipatterns
level: beginner
category: methodology
audience:
  - audiences:developers

---

# Common Anti-Patterns

---

## Review Traps to Avoid

![review_traps](svg/courses/development_methodologies/code-review-best-practices/12_common_anti_patterns/review_traps.svg)

---

## What This Chapter Covers

- Rubber stamping
- Nitpick-only reviews
- Gate-keeping behaviour
- Review bottlenecks
- Overly large PRs
- Author and reviewer anti-patterns

---

## Rubber Stamping

- "LGTM" with no actual reading
- Approval as ceremony
- Misses real issues
- Erodes the value of reviews
- Often a symptom of overload or lack of authority

---

## Anti-Patterns

![anti_patterns](svg/courses/development_methodologies/code-review-best-practices/12_common_anti_patterns/anti_patterns.svg)

---

## How Rubber Stamping Happens

- One person reviews 10 PRs an afternoon
- Review queue is 3 days deep
- The "important" PR is paired with 5 trivial ones
- Reviewer skims, approves
- The author isn't surprised either

---

## Fixing Rubber Stamping

- Smaller PRs make real reviews tractable
- More reviewers spread the load
- "Review later" is acceptable; "approve unread" isn't
- Re-open rate metric exposes the pattern
- Cultural expectation: reviews are work, not a formality

---

## Nitpick-Only Reviews

- The reviewer comments on whitespace, naming, no logic
- 20 nits, no design feedback
- Author resents the reviewer; quality doesn't improve
- Often: the reviewer doesn't understand the change well enough
- Or: the reviewer is avoiding harder topics

---

## Fixing Nitpick-Only

- Set expectations: substance first, style second
- Use formatters/linters for style — don't review what robots do
- Reviewers should ask themselves: "did I look at the logic?"
- Ask juniors to review for substance; helps growth
- Make tone a team value: "be helpful, not pedantic"

---

## Gate-Keeping

- One reviewer who blocks everything
- Often a senior with strong opinions
- Justified rejections; unjustified rejections; preference rejections
- Team learns to avoid them
- Authors lose initiative; queue grows behind the gate

---

## Fixing Gate-Keeping

- Multiple reviewers can approve
- "Strong preferences need reasons"
- Manager intervention if persistent
- Sometimes: this person is right but bad at communicating
- Coaching helps; firing rarely

---

## Review Bottlenecks

- Two people, 30 PRs in their queue, never enough time
- The team blames reviews for slow shipping
- Often: the company didn't grow review capacity with team size
- Fix: train more reviewers, distribute via CODEOWNERS
- Review is part of the work, not a tax on it

---

## Overly Large PRs

- Half the codebase changed in one PR
- Reviewers can't actually review it
- Approved by "trust"
- Bugs make it through
- Solution: split (covered in chapter 7)

---

## "I'll Fix It Later" PRs

- TODO comments that never become tickets
- "We can clean this up next sprint"
- Tech debt accretes silently
- Solution: every TODO becomes an issue with a link
- Or: don't merge until cleaned up

---

## "Just A Quick Fix"

- A bug fix that adds 200 lines
- A "config change" that touches business logic
- A "rename" that introduces a behaviour change
- Author downplays scope; reviewer doesn't notice
- Solution: read the diff, not the description

---

## Author Anti-Pattern: Defensive Replies

- Every comment gets a multi-paragraph defence
- Reviewers stop commenting
- Quality declines
- Often: imposter syndrome, fear of being wrong
- Fix: receive feedback gracefully (chapter 6)

---

## Author Anti-Pattern: Friend-Shopping

- "Bob always approves; let me ask Bob"
- Bypasses the right reviewer
- Hides real issues
- Manager should notice; CODEOWNERS prevents
- Cultural: this is gaming; address the underlying issue

---

## Reviewer Anti-Pattern: Drive-By Bombs

- Comment days after approval
- Author has moved on
- Discussion happens after the fact
- Frustrating for everyone
- Fix: comment promptly; once approved, move on

---

## Reviewer Anti-Pattern: Scope Creep

- "While you're here, can you also fix Y?"
- Y is unrelated to the PR
- Author either does it (delaying the original change) or pushes back (friction)
- Fix: file a separate issue for Y
- Keep PRs focused

---

## Team Anti-Pattern: No Reviews

- "We trust each other"
- Quality drift over time
- Knowledge silos
- New hires learn from no examples
- The most expensive shortcut

---

## Team Anti-Pattern: All Reviews Are Equal

- Hot patches reviewed with the same rigour as feature work
- Routine doc updates wait days for review
- Match effort to risk
- A 1-line typo fix doesn't need 2 senior approvals
- Tier your process

---

## Common Mistakes

- Approving without reading
- Blocking without explaining
- Letting bottlenecks fester
- Treating PR size as immutable
- Failing to retire anti-patterns when they're identified
