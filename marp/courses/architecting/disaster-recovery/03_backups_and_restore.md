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
# Backups and Restore

---
## What This Chapter Covers

- Backup types
- Storage tiers
- Encryption
- Retention
- Restore drills

---
## Why Backups

- Last line of defense
- Survive corruption, ransomware, mistakes
- Independent of running service
- Required by compliance

---
## Backup Types

- Full
- Incremental
- Differential
- Snapshot

---
## Backup Cadence

![backup_types](svg/courses/architecting/disaster-recovery/03_backups_and_restore/backup_types.svg)

---
## Frequency

- Driven by RPO
- Hourly for transactional
- Daily for analytics
- Continuous via WAL or change feeds

---
## Snapshots

- Point in time
- Often crash-consistent
- Application-consistent needs flushing
- Cheap to take, careful to verify

---
## Storage Tiers

- Hot for recent
- Warm for medium age
- Cold for long retention
- Costs differ by orders of magnitude

---
## Offsite

- Same region is not enough
- Different region or vendor
- Cross-account for ransomware safety
- Air gap for highest tier

---
## Immutability

- Object lock or WORM
- Prevents tampering
- Critical against ransomware
- Time-bound retention

---
## Encryption

- Encrypt at rest
- Encrypt in transit
- Manage keys separately
- Test that decryption still works

---
## Retention

- Driven by policy and law
- Tag backups by retention class
- Automate deletion
- Audit deletions

---
## Restore Procedures

- Documented step by step
- Roles and access required
- Estimated time
- Validation steps

---
## Restore Drills

- Quarterly minimum
- Restore to a clean environment
- Compare to expected state
- Time the operation

---
## Partial Restore

- Single table or directory
- Faster and lower-risk
- Used for accidental delete
- Keep granular backups

---
## Common Backup Mistakes

- Untested backups
- Same region only
- No immutability
- No retention policy
- No documented restore steps
