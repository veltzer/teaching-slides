---
tags:
  - practices:code-review
  - tools:github
  - tools:gitlab
level: beginner
category: methodology
audience:
  - audiences:developers

---
# Review Tools

---

## Review Tool Categories

![tool_categories](svg/courses/development_methodologies/code-review-best-practices/08_review_tools/tool_categories.svg)

---
## What This Chapter Covers

- GitHub pull requests
- GitLab merge requests
- Gerrit code review
- Inline comments and suggestions
- Review assignment and CODEOWNERS
- Tool-agnostic features that matter

---
## What a Review Tool Provides

- A way to see the diff
- Inline comments on specific lines
- Threaded discussions
- Approval state
- CI status integration
- Branch protection rules
- All major tools have these

---
## GitHub Pull Requests

- The dominant tool for open source and many companies
- Tightly integrated with GitHub Actions for CI
- Reviewers, assignees, labels
- Discussion threads, suggestions, conversations
- Easy to use; not the most powerful

---
## GitHub Suggestions

- Inline code suggestions reviewers can apply
- "Click to commit" without manually editing
- Excellent for small fixes
- Multiple suggestions can be applied at once
- Speeds up small changes dramatically

---
## GitHub Code Review Features

- Required reviewers (via CODEOWNERS)
- Branch protection: require N approvals, status checks
- Conversations must be resolved before merge
- Auto-merge when conditions met
- Draft PRs for in-progress work

---
## GitLab Merge Requests

- Equivalent to PRs; richer features in some areas
- Built-in CI/CD pipelines
- Approval rules per project (advanced licence)
- Code quality reports inline in the diff
- Threaded discussions; resolve markers

---
## Gerrit

- Older, used at Google, OpenStack, Android
- Per-commit review (not per-branch)
- Vote-based: +2 to merge, -2 to block
- Patch sets for revisions; reviewers see what changed between sets
- Different model; takes adjustment

---
## Phabricator / Phorge

- Used at Facebook (then deprecated; community fork is Phorge)
- Differential review tool: stack of patches
- Reviewers comment per-revision
- Less common today; mentioned for completeness

---
## Inline Comments

- The standard mechanism for line-specific feedback
- Open a thread; multiple replies possible
- Resolve when addressed
- Most tools track unresolved threads as merge blockers
- The unit of review communication

---
## Code Suggestions

- "Suggest" a code change inline
- Author can apply with one click
- Saves the round trip of "make this change"
- Use for: small typos, nitpicks, simple refactors
- Don't suggest for big design changes — discuss first

---
## CODEOWNERS

```misc
*.py        @python-team
/auth/      @alice @bob
/.github/   @ops-team
```

- Maps file paths to required reviewers
- Auto-requests reviews on PR creation
- Required-review enforcement at branch level
- Living document; update as the team changes
- Standard in larger codebases

---
## Review Assignment

- Round-robin: spread reviews across the team
- Owner-based: route by file path (CODEOWNERS)
- Self-selection: anyone can pick up reviews
- Hybrid: CODEOWNERS for critical, free-for-all for the rest
- Pick what your team can sustain

---
## Notifications

- Email per comment? Drowns the inbox
- Slack integrations bridge the right amount
- Per-PR notifications for the participants only
- Tool-specific: GitHub Mobile, Gerrit's gertty, etc.
- Configure notifications so reviews are visible without overwhelming

---
## Linters and Formatters in Reviews

- Run linters in CI; fail builds on issues
- Auto-format on save / pre-commit
- Pre-commit hooks (`pre-commit` framework)
- Formatters reduce review noise dramatically
- Don't review what a robot can review

---
## Review Bots

- Auto-comment on PRs: stale notifications, large PR warnings, security scans
- Useful for repetitive checks
- Can become noisy; tune them
- Examples: Dependabot, Renovate, CodeQL, Snyk
- Bots don't replace humans

---
## CI Integration

- Status checks visible on the PR
- Merge blocked until checks pass
- Runs on every push
- Tests, linters, security scans, type checks
- The first review is by the CI

---
## Common Tool Mistakes

- Disabling required reviewers "just for this"
- Force-pushing during review &#8594; reviewers lose context
- Resolving comments without addressing them
- Bot spam that drowns real comments
- Approving via mobile, half-read
