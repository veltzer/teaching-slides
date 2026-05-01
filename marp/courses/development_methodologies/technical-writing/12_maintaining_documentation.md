---
tags:
  - practices:technical-writing
  - practices:maintenance
level: beginner
category: methodology
audience:
  - audiences:developers
  - audiences:managers

---
# Maintaining Documentation

---
## What This Chapter Covers

- Documentation debt
- Strategies for keeping docs current
- Ownership and responsibility
- Archiving outdated content
- Periodic doc reviews
- The cost of not maintaining

---
## Documentation Debt

- Like tech debt, but for docs
- Each unreviewed change adds to it
- Each stale page adds to it
- Hard to measure, easy to feel
- A team with high doc debt has frustrated users

---
## Why Docs Decay

- Code changes; docs don't
- Authors leave; docs lose owners
- Tools change; docs don't update
- New features ship without docs
- Old features deprecate; docs still describe them

---
## Strategies for Keeping Docs Current

- Docs in the same PR as the code change
- Required doc updates for user-facing changes
- Quarterly doc audits
- Auto-generated docs where feasible
- Owners per doc area

---
## Docs With Code

- The most effective strategy
- A code change that affects docs requires the doc update in the same PR
- Reviewers enforce
- Eliminates "I'll update the docs later"
- Universal in mature engineering teams

---
## Required Doc Checkboxes

- PR template includes "did this need a doc change?"
- "Yes, updated", "Yes, will follow up", "No"
- Visible signal at review time
- Following-up on "follow up" is the hard part
- Combined with team norms, works well

---
## Auto-Generated Docs

- API docs from OpenAPI / source comments
- Database schema diagrams from the schema
- Dependency graphs from package files
- Configuration references from typed config schemas
- The docs that take care of themselves

---
## Owners

- Per-doc area, in CODEOWNERS
- Owner responsible for keeping it current
- Owner's manager monitors
- Without owners, decay is inevitable
- Even a "weak" owner is better than none

---
## Quarterly Doc Audit

- Review traffic data
- Check: still accurate? still useful?
- Update or archive
- A 2-hour exercise per area
- Catches what continuous maintenance misses

---
## Archiving

- Old features that no longer exist: don't pretend they do
- Move to an "archive" section
- Or delete with a redirect
- Better to have no doc than a wrong doc
- Search results should not lead to outdated content

---
## Deprecation Notices

- For features being phased out
- "Deprecated in 1.4; will be removed in 2.0"
- Clear migration path
- Visible at the top of the doc
- Better than silently breaking users

---
## Stale Indicators

- Date stamps on pages ("last updated 2026-05-01")
- "This page may be out of date" badges for pages older than N months
- Encourages updates by making age visible
- Don't show dates so prominently they distract
- Subtle; just enough to prompt review

---
## Doc Tests in CI

- Code examples that run as tests
- Schema-validated configuration examples
- Link checks
- Each test catches one form of decay
- Worth the setup; pays back continuously

---
## Reorganising

- Periodically: are the docs structured for current users?
- Information architecture changes as the product matures
- A reorganisation every 1-2 years is common
- Disruptive in the moment; pays off long-term
- Redirects from old URLs preserve external links

---
## Cost of Bad Docs

- Repeated questions
- Slower onboarding
- Decisions revisited
- Customer churn
- Engineering time on questions instead of features
- Real money, every day

---
## Cost of Good Docs

- Time to write and maintain
- Tooling and CI
- Review effort
- Owners' time
- Less than the cost of bad docs by a wide margin

---
## A Maintenance Cadence

- Daily: PR-level doc updates with code changes
- Weekly: review the doc backlog (if any)
- Monthly: check link-check and lint reports
- Quarterly: per-area audit
- Yearly: full content review

---
## Common Maintenance Mistakes

- "We'll set up doc maintenance next quarter"
- Massive doc rewrites instead of incremental updates
- No owners; everyone's responsibility
- Treating docs as a cost to minimise
- Forgetting docs in the deprecation process
