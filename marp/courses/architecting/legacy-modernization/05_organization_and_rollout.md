---
tags:
  - architecting:patterns
level: intermediate
category: architecting
audience:
  - audiences:architects

---
# Organization and Rollout

---
## What This Chapter Covers

- People side of modernization
- Funding and metrics
- Risk management
- Rollout plans
- Sustaining change

---
## Conway's Law

- Systems mirror communications
- Reorg may precede rearchitect
- Or follow it
- Plan both together

---
## Two-Speed Teams

- Old system needs caretakers
- New system needs builders
- Same people split focus poorly
- Dedicated teams help

---
## Two Teams Visualized

![two_speed_teams](svg/courses/architecting/legacy-modernization/05_organization_and_rollout/two_speed_teams.svg)

---
## Rotation

- Avoid permanent old-system jail
- Knowledge transfer in both directions
- Career growth for caretakers
- Cross-pollination

---
## Funding

- Multi-year budget
- Tied to business outcomes
- Not "tech debt" alone
- Shielded from quarter-cuts

---
## Metrics

- Slices retired
- Defects per slice
- Lead time for change
- Cost per request

---
## Communication

- Roadmap visible to all
- Wins celebrated
- Setbacks discussed
- No surprises to leadership

---
## Risk Management

- List the top ten risks
- Mitigation per risk
- Owner per risk
- Reviewed monthly

---
## Rollout Patterns

- Internal first
- Friendly customers
- Percentage rollout
- Per-tenant

---
## Pattern Catalog

![rollout_patterns](svg/courses/architecting/legacy-modernization/05_organization_and_rollout/rollout_patterns.svg)

---
## Feature Flags

- Decouple deploy from release
- Roll back without redeploy
- Target by tenant, region, user
- Clean up retired flags

---
## Incident Response

- Old system, new system, hybrid each fail differently
- On-call must know all three
- Runbooks for each path
- Drill regularly

---
## Sustaining Change

- Modernization is years not months
- Leadership turnover threatens it
- Document the why
- Onboard new leaders fast

---
## Sunset Planning

- Decommission is the end goal
- Track active dependencies
- Remove last caller
- Celebrate the shutdown

---
## Common Organizational Mistakes

- No executive sponsor
- Funding cut at first hard year
- Caretakers given no career path
- Old system never sunset
- Treating it as engineering only
