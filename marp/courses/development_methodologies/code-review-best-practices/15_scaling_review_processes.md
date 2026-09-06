---
tags:
  - practices:code-review
  - practices:scaling
level: beginner
category: methodology
audience:
  - audiences:developers
  - audiences:managers

---

# Scaling Review Processes

---

## What This Chapter Covers

- Reviews in large teams
- Cross-team reviews
- Review load balancing
- Documentation and standards
- Tooling at scale
- The shift from "everyone knows everything" to "specialists own areas"

---

## Why Scale Matters

- 5-person team: everyone reviews everything; works fine
- 50-person team: needs structure; can't do that
- 500+: needs heavy structure; tools, owners, automation
- Without process scaling, reviews become a bottleneck
- The patterns differ at each size

---

## Levers for Scale

![scale_review](svg/courses/development_methodologies/code-review-best-practices/15_scaling_review_processes/scale_review.svg)

---

## Small Teams (under 10)

- Ad-hoc routing: pick anyone available
- Review every PR; everyone reviews everything
- Quality maintained by personal relationships
- Process light
- This works; don't add overhead before you need it

---

## Medium Teams (10-50)

- CODEOWNERS to route by area
- Two-approval requirement for risky areas
- Review checklists per change type
- Weekly review-health check-in
- Process visible but not heavy

---

## Large Teams (50+)

- CODEOWNERS strict; specialists own areas
- Tier-based review requirements
- Bots for trivial enforcement
- Documented norms; onboarding includes reviewing
- Process is part of the team culture, not improvised

---

## Cross-Team Reviews

- A change touches multiple teams' code
- Requires reviewers from each
- Slower; sometimes much slower
- Good for: sharing patterns, breaking silos
- Bad when: every change becomes a multi-team negotiation

---

## Review Load Balancing

- Without management, reviews concentrate on the same people
- Senior people get crushed; junior people get little experience
- Auto-rotation tools (PullApprove, GitHub's auto-assignment)
- "Office hours" for cross-team reviews
- Match capacity to demand; track over time

---

## Specialist Reviews

- Security team for sensitive changes
- Performance team for hot-path changes
- Database team for schema changes
- Don't make them required for everything; just where they matter
- Specialists are scarce; protect their time

---

## Documentation at Scale

- "How we review" doc, kept current
- Style guide; linter config matches it
- Architecture decision records (ADRs)
- Onboarding includes a review-shadow program
- Culture doesn't transmit by osmosis at 100+ people

---

## Tooling at Scale

- Self-hosted GitHub Enterprise, GitLab, or similar
- Custom bots for org-specific rules
- Dashboards for review health metrics
- Integration with ticketing, CI, deployment
- Investments compound; pay them down once

---

## Trunk-Based Development

- Common at scale: one branch (`main`), small frequent merges
- Feature flags for incomplete work
- PRs short-lived (hours, not days)
- Reviews happen fast because PRs are small
- Industry-standard for high-velocity teams

---

## Stacked PRs

- Series of PRs, each based on the previous
- Reviewers see incremental changes
- Tools: Graphite, ghstack, Sapling
- Common at companies with strict trunk-based development
- A practice; not strictly necessary

---

## Review Office Hours

- A scheduled hour for review pairing
- Anyone can drop a stuck PR
- A senior person walks through with the author
- Mentoring + unblocking in one
- Useful for crossing team boundaries

---

## Asynchronous Reviews

- Distributed teams across time zones
- PRs sit overnight, reviewed in another zone
- Sun-follows-engineering pattern
- Requires excellent PR descriptions (no live questions)
- Faster end-to-end than waiting for one zone

---

## When Reviews Are A Liability

- A 50-person team where the same 5 people approve everything
- 2-week review queues
- Shipping pressure makes people skip
- The system has failed
- Restructure: more owners, smaller PRs, better tools

---

## Continuous Process Improvement

- Quarterly review-of-reviews
- Surveys: "is the review process helping?"
- Adjust based on what you find
- Treat the process as a product; iterate
- Static processes age badly

---

## Common Scaling Mistakes

- Heavyweight process applied to a small team
- Light process applied to a large team
- Adding more required reviewers when the bottleneck is throughput
- Buying tools to fix culture problems
- Letting review queues become someone's daily nightmare

---

## Course Wrap-Up

- Reviews are a powerful practice when done well
- Goals first; process second; tools third
- Tone matters as much as content
- Match effort to risk
- Culture is what compounds
- A team that reviews well outperforms one that doesn't, every time
