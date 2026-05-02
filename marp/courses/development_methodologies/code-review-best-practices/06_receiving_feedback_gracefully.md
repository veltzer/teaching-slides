---
tags:
  - practices:code-review
level: beginner
category: methodology
audience:
  - audiences:developers

---
# Receiving Feedback Gracefully

---
## What This Chapter Covers

- Separating ego from code
- Responding to comments
- Knowing when to push back
- Learning from feedback
- Common author anti-patterns
- The mindset that grows fastest

---
## Code Is Not You

- Reviewers comment on the code, not on you
- Even if it feels personal, treat it as not
- Authors who internalise this grow fastest
- Authors who don't burn out
- Practice this; it's a skill

---
## Receiving Practices

![receiving_feedback](svg/courses/development_methodologies/code-review-best-practices/06_receiving_feedback_gracefully/receiving_feedback.svg)

---
## Default Response: Curiosity

- "Why do they think that?"
- Read the comment carefully before reacting
- Sometimes the reviewer missed something — easy to clarify
- Sometimes the reviewer is right — easy to agree
- Sometimes you both have a point — discuss

---
## Responding To Comments

- Acknowledge each comment
- Either change the code, or explain why not
- "Done" with a commit reference
- "I think this is fine because..." with reasoning
- Silence on a comment leaves the reviewer guessing

---
## When To Push Back

- The reviewer is wrong on facts
- The reviewer's preference doesn't match the codebase's conventions
- The change would worsen the code
- The change is out of scope for this PR
- Push back politely; defend with reasons, not pride

---
## Pushing Back Examples

- "I considered that; I went with this because [reason]. Open to changing."
- "That's a good idea but it's outside this PR's scope; I'll open a follow-up."
- "I think the existing pattern in this file uses X, so I followed it."
- All clear, factual, non-confrontational
- Practice these phrasings

---
## Hard Feedback

- "This whole approach is wrong"
- The most painful feedback to receive
- Often the most valuable
- Take a breath; don't reply for an hour
- Then engage substantively; sometimes they're right

---
## When To Defer To The Reviewer

- They have more context (longer at the company, owns the area)
- The cost of changing is small
- You don't have a strong reason
- "Pick your battles" applies
- Don't fight every comment; reviewers have finite patience too

---
## Learning From Feedback

- Each PR is a free mentoring session
- Patterns repeat across reviews
- Note the same comment showing up; address the underlying habit
- Junior to senior is mostly this loop
- Senior developers got that way by listening

---
## Asking For Clarification

- "Could you elaborate?" beats arguing past each other
- "I'm not sure what you mean — could you suggest specifically?"
- Better than guessing wrong
- Reviewers usually appreciate the engagement
- Saves a back-and-forth round

---
## Avoiding Author Anti-Patterns

- Defensiveness on every comment
- Long argumentative replies
- "I'll fix it later" with no follow-up
- Re-requesting review without addressing previous comments
- Going around the reviewer to a friendlier one

---
## When To Escalate

- Reviewer blocks for unclear reasons
- Disagreement persists after discussion
- A third party can break the tie
- Tech lead, manager, ARB
- Rare; usually a sign of larger team friction

---
## Author's Bill of Rights

- Specific, actionable feedback
- Reviewers explain *why*
- A timely first review
- Praise alongside critique
- Disagreement, not dismissal
- Reviewers who treat you as a peer

---
## Common Mistakes

- Treating feedback as criticism of you personally
- Replying defensively before reading carefully
- Marking comments as "resolved" without actually addressing
- Losing track of which comments need responses
- Running out of energy on big PRs and rubber-stamping the rest
