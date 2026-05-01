---
tags:
  - testing:chaos
  - practices:reliability
level: advanced
category: testing
audience:
  - audiences:devops
  - audiences:developers

---
# Operationalizing Chaos

---
## What This Chapter Covers

- Continuous chaos
- Chaos in CI
- Org culture
- Metrics
- Mistakes to avoid

---
## Continuous Chaos

- Scheduled experiments
- Run during business hours
- Small blast radius
- Always observed

---
## Chaos In CI

- Per-service chaos suites
- Run on PRs that touch resilience
- Fail builds on regression
- Catch issues before deploy

---
## Why It Pays Off

- Bugs found in working hours
- Cheaper than 3 AM pages
- Learning compounds
- Confidence grows

---
## Culture Shift

- Failure is normal
- Practice is the cure
- Blameless review of experiments
- Leadership sponsorship

---
## Metrics

- Experiments per quarter
- Action items closed
- Mean time to recover
- Customer-impact incidents avoided

---
## Tooling

- Pick a platform
- Or in-house wrappers
- Integrate with monitoring
- Integrate with deploy tooling

---
## Safety Rails

- Per-experiment quotas
- Allowlists for safe targets
- Big red abort button
- Auto-stop on customer impact

---
## Onboarding New Services

- Resilience checklist
- Initial chaos experiments mandated
- Resolve before production traffic
- Re-run on architecture changes

---
## Multi-Tenant Concerns

- Avoid impacting one tenant for another
- Tenant-aware injection
- Tenant-aware abort
- Document the boundaries

---
## Compliance

- Some regulators require it
- Document experiments
- Audit log of injections
- Tie to business risk register

---
## Vendor And Provider Failures

- Inject mocked vendor outages
- Test failover paths
- Document fallback business behavior
- Practice annually minimum

---
## When Not To Do Chaos

- During launches
- During known unstable periods
- Without leadership buy-in
- Without monitoring

---
## Scaling Up

- Start with one service
- Spread to neighbors
- Standardize platform
- Eventually default for all

---
## Common Operational Mistakes

- One time, one team
- No ownership
- No integration with deploy
- Skipping action items
- Treating it as a side project
