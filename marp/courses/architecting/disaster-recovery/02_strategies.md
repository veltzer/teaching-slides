---
tags:
  - architecting:patterns
  - practices:reliability
level: intermediate
category: architecting
audience:
  - audiences:architects
  - audiences:devops

---
# DR Strategies

---
## What This Chapter Covers

- Backup and restore
- Pilot light
- Warm standby
- Active-active
- Choosing among them

---
## Backup and Restore

- Cheapest tier
- Periodic backups offsite
- Restore on disaster
- RTO hours to days

---
## Pilot Light

- Minimal infrastructure running
- Data replicated continuously
- Scale up on disaster
- RTO tens of minutes to hours

---
## Warm Standby

- Reduced-capacity copy running
- Promote on disaster
- Scale to full capacity after
- RTO minutes

---
## Active-Active

- Full capacity in two or more regions
- Traffic split normally
- Survive a region loss instantly
- Highest cost

---
## Tier Comparison

![dr_tiers](svg/courses/architecting/disaster-recovery/02_strategies/dr_tiers.svg)

---
## Active-Passive

- One region serves
- Others wait
- Flip on disaster
- Cheaper than active-active

---
## Database Replication

- Sync vs async
- Sync: zero RPO, latency cost
- Async: bounded loss, lower latency
- Pick by data criticality

---
## State and Sessions

- Stateless services scale easily
- Sessions need replication or sticky regional routing
- Cookies and tokens must work cross-region
- Test on failover

---
## DNS and Traffic Routing

- Health-checked routing
- Latency-based for active-active
- Manual flip for active-passive
- TTLs matter on flip

---
## Storage Replication

- Object storage cross-region replication
- Block storage snapshots and copies
- File storage region pairs
- Verify replicas regularly

---
## Choosing a Tier

- Map RTO and RPO per service
- Cost per tier
- Critical revenue vs internal tooling
- Most orgs run multiple tiers

---
## Hybrid Strategies

- Active-active for tier 1
- Pilot light for tier 2
- Backup only for tier 3
- Document who is what

---
## Common Strategy Mistakes

- One strategy for everything
- Not measuring actual RPO and RTO
- Async replication treated as zero-loss
- DNS flip never rehearsed
- Forgetting state in caches
