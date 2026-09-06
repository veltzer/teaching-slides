---
tags:
  - practices:code-review
level: beginner
category: methodology
audience:
  - audiences:developers

---

# PR Size and Structure

---

## Pull Request Sizing

![pr_sizing](svg/courses/development_methodologies/code-review-best-practices/07_pr_size_and_structure/pr_sizing.svg)

---

## What This Chapter Covers

- Why smaller PRs are better
- Stacked PRs
- Descriptive titles and descriptions
- Linking to issues and context
- Draft PRs
- Splitting big work

---

## Why Small PRs

- Easier to review thoroughly
- Faster to merge
- Lower risk of breaking things
- Easier to roll back if needed
- Keep momentum on the team

---

## Defect Detection vs PR Size

![pr_size_curve](svg/courses/development_methodologies/code-review-best-practices/07_pr_size_and_structure/pr_size_curve.svg)

---

## How Small Is Small

- Industry research: ~100-200 lines is the sweet spot
- 400+ lines: review quality drops sharply
- 1000+ lines: rubber-stamping common
- Some changes are inherently large; split where possible
- "Small" relative to complexity, not just line count

---

## Splitting a Big Change

- Refactor first, in its own PR
- Add new code in another PR
- Wire up the new code in a third
- Each PR independently mergeable
- Reviews go faster; risk lower at each step

---

## Stacked PRs

- A series of PRs each based on the previous
- Reviewers see incremental, focused changes
- Tools: ghstack, Graphite, Sapling, manual chains
- More setup than single PRs; pays off for big initiatives
- The pattern at companies that do trunk-based development

---

## PR Titles

- Should be informative on its own
- "Fix bug" — bad
- "Fix off-by-one in pagination on user list" — good
- Format conventions: "[Component] Action" works
- Will appear in the merge commit, in release notes, in git log

---

## PR Descriptions

- What changed and why
- Link to the issue / spec
- Mention testing done
- Call out any unusual decisions
- Note any rollback considerations
- A good description halves review time

---

## A PR Description Template

```misc
## What
Brief summary.

## Why
Problem statement; link to issue.

## How
Implementation notes; alternatives considered.

## Testing
What was run; what passed; manual steps.

## Risks
What could break; rollback plan.
```

- Most platforms support PR templates
- Saves authors from inventing the structure each time

---

## Linking to Issues

- "Fixes #123" auto-closes the issue when merged (GitHub, GitLab)
- "Refs #456" links without closing
- Important: link both ways for traceability
- Future maintainers thank you
- Audit trails for compliance

---

## Draft PRs

- "I want feedback but it's not done"
- Mark as Draft (GitHub) or WIP (GitLab)
- Reviewers know not to merge yet
- Useful for early design feedback
- Convert to "Ready for Review" when done

---

## When To Open Draft

- After enough work to show direction
- Before sinking days into the wrong approach
- For design-heavy changes especially
- Surfaces concerns early
- Cheaper to redirect than to redo

---

## Atomic Commits

- Each commit does one thing
- Useful for: bisecting, rebasing, partial reverts
- Squashing on merge keeps history clean
- Within a PR, individual commits help reviewers
- Style varies by team; pick one and stick

---

## Cleaning Up Before Review

- Squash WIP commits
- Drop debug logs
- Delete commented-out code
- Run the linter
- Self-review the diff
- Submitting messy is disrespectful of reviewer time

---

## Big PRs That Can't Be Split

- Massive renames
- Auto-generated code
- Large dependency upgrades
- Note in the description: "this had to be one PR because..."
- Reviewers can scan rather than read every line
- Pair with manual smoke testing

---

## The Cost of Large PRs

- Stalled in review for days
- Requires huge cognitive load to review
- Conflicts with other work
- High risk of regressions
- "I'll review this when I have time" → never
- Smaller PRs are kinder to your future self

---

## Common Mistakes

- One huge PR for a feature — sits in review for a week
- PR title that reveals nothing
- Description that's just "see ticket"
- Mixing refactor + feature in one PR
- Forgetting to link the issue
