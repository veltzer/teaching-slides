---
tags:
  - security:threat-modeling
  - concepts:sdlc
  - concepts:remediation
level: intermediate
category: security
audience:
  - audiences:developers
  - audiences:devops
  - audiences:managers

---
# Integration and Remediation

---
## What This Chapter Covers

- Threat modeling in agile and DevOps workflows
- Tools: Microsoft TMT, OWASP Threat Dragon, IriusRisk, Threagile
- Connecting threats to issue trackers
- Prioritization and remediation tracking
- Validating mitigations through testing

---
## The Integration Problem

- Threat modeling is most valuable when it influences code
- Most threat models live in PDFs nobody reads
- The fix: integrate with the actual development workflow
- Tickets, pull requests, CI checks
- "Living threat model" is the goal

---
## Threat Modeling in Agile

- One threat model per epic, not per project
- Update during the design phase of each story
- 30-minute timebox for moderate features
- Output: tickets in the same backlog as feature work
- Friction kills the practice — keep it fast

---
## Agile Integration Visualised

![agile_integration](svg/courses/security/threat-modeling/08_integration_and_remediation/agile_integration.svg)

---
## Lightweight Threat Modeling

- "What can go wrong?" on the whiteboard
- DFD on a sticky-note level
- STRIDE pass per element, captured in a doc
- Two hours, three engineers — done
- Heavy methodologies for high-stakes systems only

---
## Per-Epic Threat Modeling

- Architect proposes the design
- Security engineer (or rotated dev) joins for an hour
- Walk through the design, mark threats, capture mitigations
- Mitigations become acceptance criteria in stories
- Re-review at the end of the epic

---
## Threat Modeling Cadence

- Per feature — for any feature touching auth, data, or trust boundaries
- Per release — sanity check before shipping
- Quarterly — review accumulated threats and mitigations
- Annually — full top-down review of critical systems
- Match the cadence to risk

---
## Microsoft Threat Modeling Tool

- Free, Windows-only, Microsoft-supported
- Visual DFD editor with built-in STRIDE
- Generates threats automatically per element
- Templates for common architectures
- Strong starting point for STRIDE-focused teams

---
## OWASP Threat Dragon

- Open source, cross-platform
- Web and desktop versions
- DFD editor with threat capture
- Customizable threat libraries
- Good fit for teams that prefer open tools

---
## IriusRisk

- Commercial, automated threat modeling
- Architecture-driven — answer questions, get threats
- Integrates with Jira, Azure DevOps
- Strong compliance reporting
- Suited to enterprises with compliance demands

---
## Threagile

- Diagram-as-code: YAML describes the system
- Generates threats and risk reports automatically
- Lives in the repo, version-controlled
- Integrates into CI for design-time security checks
- Strong fit for infrastructure-as-code teams

---
## Tool Comparison Visualized

![tool_comparison](svg/courses/security/threat-modeling/08_integration_and_remediation/tool_comparison.svg)

---
## Choosing a Tool

- Team size, budget, regulatory environment
- Diagram-as-code if your culture is GitOps
- Visual editors for architects who think visually
- Automated tools for compliance reporting
- Start with paper or whiteboard; tool later

---
## Connecting to Issue Trackers

- Each unmitigated threat becomes a ticket
- Same backlog, same prioritization, same workflow
- Labels: threat-model, severity, methodology
- The threat lives in code review when implementation arrives
- A threat without a ticket is a forgotten threat

---
## Threat IDs and Traceability

- Give each threat a stable ID
- Reference the ID in commits and PRs that mitigate
- Search the codebase for IDs to find related code
- Audit trail: from threat to fix to test
- Especially valuable for compliance evidence

---
## Prioritization in Practice

- Don't prioritize threats individually — prioritize batches
- Critical and high — fix this sprint or accept risk
- Medium — backlog with deadline
- Low — accept, with a note explaining why
- The point is making decisions, not stacking the rank

---
## Mitigation Strategies

- Eliminate — change the design so the threat doesn't apply
- Reduce — add controls that make exploitation harder
- Transfer — insurance, contractual liability
- Accept — document and move on
- Each is valid in context

---
## Mitigation Strategies Visualised

![mitigation_strategies](svg/courses/security/threat-modeling/08_integration_and_remediation/mitigation_strategies.svg)

---
## Eliminate by Design

- Don't store data you don't need
- Don't expose endpoints that aren't used
- Don't trust inputs you can avoid receiving
- Strongest mitigation — there's no exploit when there's nothing to exploit
- Often the cheapest path to security

---
## Mitigation Tracking

- Status: planned, implemented, tested, accepted, monitored
- Owner: who is responsible
- Due date: even "low" needs a date
- Evidence: test cases, logs, configurations
- Review the tracker, not the threat list, in standups

---
## Validating Mitigations

- Unit and integration tests that exercise the threat
- Negative tests — the attack should fail
- Security tests in CI: SAST, DAST, dependency scans
- Manual penetration testing for critical features
- A mitigation without a test is hope-driven security

---
## Continuous Threat Modeling

- New code triggers a model review
- New dependencies trigger a model review
- New compliance requirements trigger a model review
- Trigger from PR labels, file paths, or design-doc changes
- Automation reduces friction; doesn't replace judgment

---
## Threat Modeling and Code Review

- Reviewers ask: does this PR introduce a new threat?
- Reviewers ask: does this PR mitigate a tracked threat?
- A "threat-model" label can require security review
- Pair with checklists for common patterns
- Code review is the most consistent place to catch drift

---
## Metrics That Matter

- Threats found per review — calibrates the model
- Time from threat to mitigation
- Threats accepted vs threats mitigated
- Coverage: percentage of features with a current threat model
- Avoid vanity metrics — count what changes behavior

---
## Building a Security Culture

- Threat modeling is a habit, not an event
- Celebrate developers who find threats early
- Treat findings as learning, not failure
- Rotate threat-modeling facilitators across teams
- A team that does it weekly is a team that knows its system

---
## Common Pitfalls

- Threat models that exist but nobody reads
- "We did one last year" — stale models are wrong models
- Tooling chosen for features, not for adoption
- Findings sitting in a tracker forever, untouched
- Compliance ceremony with no actual mitigation

---
## Anti-Patterns to Avoid

- One central security team owns all threat models
- Threat modeling sessions without architects present
- "The cloud handles it" without verification
- Skipping threat models for "internal" systems
- Treating low-rated threats as "no threat"

---
## Maturity Stages Visualised

![maturity_levels](svg/courses/security/threat-modeling/08_integration_and_remediation/maturity_levels.svg)

---
## Maturing the Practice

- Stage 1 — ad-hoc, when someone remembers
- Stage 2 — required for major changes
- Stage 3 — embedded in design reviews
- Stage 4 — automated where possible, integrated with CI
- Stage 5 — culture-driven, every developer thinks this way

---
## Course Recap

- Fundamentals — what threat modeling is and isn't
- DFDs — the foundation
- STRIDE — systematic enumeration
- DREAD and risk — prioritization
- Attack trees and PASTA — depth and business alignment
- LINDDUN — privacy
- In practice — microservices, cloud, APIs
- Integration — making it stick

---
## Final Thoughts

- The best threat model is the one your team actually uses
- Lightweight beats comprehensive if comprehensive doesn't ship
- Iteration beats perfection — update over time
- Combine methodologies; don't be religious about one
- Remember the four questions, every time

---
## Summary

- Integrate threat modeling into the development workflow
- Choose tools your team will use, not just admire
- Connect threats to issue trackers for accountability
- Validate mitigations with tests; trust evidence over intent
- Build the culture; the artifacts follow
