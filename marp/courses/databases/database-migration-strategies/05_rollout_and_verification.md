---
tags:
  - databases:migrations
  - practices:migration
level: intermediate
category: databases
audience:
  - audiences:dba
  - audiences:architects

---
# Rollout and Verification

---
## What This Chapter Covers

- Rollout patterns
- Feature flags
- Verification
- Rollback
- Post-migration cleanup

---
## Rollout Patterns

- All at once
- Per region
- Per tenant
- Per user percentage

---
## Feature Flags

- Decouple deploy from release
- Roll back without redeploy
- Target by tenant or user
- Required for safe migrations

---
## Per-Tenant Cutover

- Smaller blast radius
- Verify each tenant before next
- Slower overall
- Best for shared schemas

---
## Per-Region Cutover

- Limit blast to one region
- Easier traffic shift
- Cross-region paths still work
- Common in multi-region setups

---
## Canary Cutover

- 1%, then 5%, then 25%, then 100%
- Watch metrics at each step
- Halt on regressions
- Default for risky changes

---
## Verification Layers

- Syntactic: counts, sums
- Semantic: sample queries match
- Behavioral: app works
- User: dogfood and beta

---
## Smoke Tests

- Critical user journeys
- Run after every step
- Automated where possible
- Block promotion on failure

---
## Performance Verification

- p50 and p99 stable
- No regression on hot queries
- Watch for new slow queries
- Compare side by side

---
## Data Verification

- Row counts match
- Hash sums per partition
- Random sample comparisons
- Spot checks of business KPIs

---
## Rollback

- Documented trigger
- Tested in lower env
- Time-bounded window
- Loud alerting on rollback path

---
## Communication

- Stakeholders informed
- Maintenance window posted
- Status page prepared
- Internal channel for incidents

---
## Post-Migration Cleanup

- Remove dual writes
- Remove old code paths
- Drop old tables
- Update docs

---
## Documentation

- What changed
- Why
- How to revert
- Lessons learned

---
## Common Rollout Mistakes

- Rolling out to all users at once
- No flag for fast rollback
- Verification after the fact
- Old code paths kept forever
- No retro after the migration
