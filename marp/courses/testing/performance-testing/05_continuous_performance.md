---
tags:
  - testing:performance
level: intermediate
category: testing
audience:
  - audiences:developers
  - audiences:testers

---
# Continuous Performance

---
## What This Chapter Covers

- Performance in CI
- Trend tracking
- Alerts on regressions
- Capacity planning
- Culture

---
## Why Continuous

- Performance regressions sneak in
- One pre-launch test is not enough
- Catch close to commit
- Faster fixes

---
## Smoke Perf In CI

- Small synthetic load
- A few minutes per build
- Compares to prior build
- Blocks egregious regressions

---
## Nightly Full Tests

- Realistic workload
- Multiple scenarios
- Long enough to catch warm-up effects
- Trend over weeks

---
## Trend Tracking

- Store metrics over time
- Plot per build
- Spot regressions visually
- Alert on threshold breach

---
## Regression Alerts

- p99 latency above target
- Throughput below target
- Error rate above floor
- Page or ticket per breach

---
## Bisect Regressions

- Run between known-good and known-bad
- Narrow to a commit
- Same as bug bisecting
- Saves time

---
## Capacity Planning Inputs

- Max sustainable rate per service
- Resource use at max
- Margin for growth
- Update quarterly

---
## Forecasting

- Project growth from analytics
- Compare to capacity
- Plan capacity adds
- Plan architecture work

---
## Headroom

- Aim for 50% utilization at peak
- Allow burst headroom
- Scale before saturation
- Document the policy

---
## Performance Budgets

- Per endpoint or per page
- Track in CI
- Reject changes that exceed
- Negotiate increases explicitly

---
## Performance Reviews

- Monthly or quarterly
- Cross-team
- Discuss trends
- Plan investments

---
## Onboarding New Services

- Performance plan required
- Initial test before launch
- Continuous tests after
- Same as new test discipline

---
## Tooling Investment

- Reuse generators
- Standardize result format
- Centralize trend storage
- Cheap to run more often

---
## Culture

- Performance is everyone's job
- Engineers and testers collaborate
- Leadership sees the trends
- Customers feel the difference

---
## Common Continuous Mistakes

- One engineer owns it all
- No CI integration
- No trend storage
- No alerts
- Performance "owned" by no one
