---
tags:
  - practices:code-review
level: beginner
category: methodology
audience:
  - audiences:developers

---
# Giving Constructive Feedback

---

## Constructive Feedback Guidelines

![feedback_guidelines](svg/courses/development_methodologies/code-review-best-practices/05_giving_constructive_feedback/feedback_guidelines.svg)

---
## What This Chapter Covers

- Tone and language
- Being specific and actionable
- Distinguishing nits from blockers
- Asking questions vs making demands
- Praising good work
- A few rephrasings to learn

---
## Anatomy of Feedback

![feedback_anatomy](svg/courses/development_methodologies/code-review-best-practices/05_giving_constructive_feedback/feedback_anatomy.svg)

---
## Feedback Principles

![feedback_principles](svg/courses/development_methodologies/code-review-best-practices/05_giving_constructive_feedback/feedback_principles.svg)

---
## Why Tone Matters

- Reviews persist in writing; tone reads worse than spoken
- Authors invest effort; harsh feedback hurts
- A defensive author argues; an embarrassed author hides
- Constructive tone keeps the discussion productive
- This is not about being nice — it's about being effective

---
## Be Specific

- "This is wrong" — useless
- "This will throw if `users` is empty" — actionable
- Cite line numbers, attach examples
- Suggest the fix when reasonable
- Vague feedback wastes everyone's time

---
## Be Actionable

- Every comment should imply a change (or explicitly not)
- "I prefer X" without a reason &#8594; not actionable
- "X is more idiomatic because Y" &#8594; actionable
- Prefer "consider" to "must"
- Authors should know what to do with each comment

---
## Nits vs Blockers

- **nit:** prefix for stylistic / minor preferences
- Blockers: things that must change before merge
- Authors free to ignore nits
- Reviewers free to insist on blockers
- Saves arguments by being explicit about which is which

---
## Examples of nits

- "nit: this could use a more descriptive name"
- "nit: missing trailing newline"
- "nit: prefer `const` here"
- All easy to ignore if the author disagrees
- Don't pile up nits; one or two per PR is plenty

---
## Asking Questions vs Demands

- "Why did you do it this way?" beats "Don't do it this way"
- Questions invite the author to explain
- Sometimes the author has a good reason
- Sometimes asking the question reveals the bug
- A wrong reason is fixed by understanding it

---
## Question-Based Examples

- "Have you considered using X here?"
- "Is the empty-list case handled?"
- "What happens if this fails?"
- Each invites a thoughtful response
- Authors learn more from answering questions than from following orders

---
## Praising Good Work

- Reviews aren't only about problems
- "Nice handling of the edge case" costs nothing, builds morale
- Highlight clever solutions; reinforces good practice
- Feels weird the first time; gets natural fast
- Teams with positive feedback culture have lower turnover

---
## Avoid "You" Statements

- "You forgot the null check" &#8594; defensive reaction
- "There's a missing null check" &#8594; about the code, not the person
- Subtle but real difference
- Discussing code is easier than discussing people
- Even compliments work better impersonally: "this approach is elegant"

---
## When You're Wrong

- The author replies; the reply has merit
- "Ah, you're right, I missed that" — say it clearly
- Don't dig in to save face
- Authors notice reviewers who admit mistakes
- Builds trust both ways

---
## Severity Vocabulary

- **must**: blocks merge
- **should**: strong recommendation
- **consider**: take it or leave it
- **nit**: stylistic, no enforcement
- **q:** or **question:**: clarifying ask, no implied change
- Pick a vocabulary your team uses; stick with it

---
## Long Comments

- Sometimes a substantial comment is right
- For explanations, design discussions, security details
- Keep them rare; prefer brevity
- A long comment in every PR is a sign of design-level disagreement
- Lift those into a separate discussion

---
## Reviewer Time

- Don't leave 50 nits on a 100-line PR
- That's a code style problem, not a review problem
- Pick the top 3-5; let the others slide
- Author's attention is finite; spend it on the important
- A flood of comments demotivates

---
## Common Mistakes

- Sarcasm in writing — never reads as intended
- "Just" or "simply" — implies the author is dumb
- Drive-by comments after approval — confusing
- Picking on whitespace, missing a logic bug
- One reviewer who never approves anything; team works around them
