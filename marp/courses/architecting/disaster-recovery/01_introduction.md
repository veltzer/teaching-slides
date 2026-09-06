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

# Introduction to Disaster Recovery

---

## What This Chapter Covers

- What DR is
- DR vs backup
- DR vs HA
- RPO and RTO
- Course outline

---

## What DR Is

- Resuming service after a disaster
- Disaster: data center loss, region loss, ransomware
- Process plus tooling
- A discipline, not a product

---

## DR vs Backup

- Backup: data copies
- DR: ability to operate
- Backup is necessary, not sufficient
- DR includes process, runbooks, people

---

## DR vs HA

- HA: survive component failure
- DR: survive site or region failure
- HA is automatic, DR may be manual
- They overlap, not the same

---

## RPO

- Recovery Point Objective
- Acceptable data loss
- Measured in time
- Drives backup frequency

---

## RTO

- Recovery Time Objective
- Acceptable downtime
- Measured in time
- Drives architecture cost

---

## RPO and RTO Visualized

![rpo_rto](svg/courses/architecting/disaster-recovery/01_introduction/rpo_rto_axes.svg)

---

## Cost Curve

- Lower RPO and RTO cost more
- Differentiate per service
- Tier critical vs non-critical
- Document the trade-off

---

## Disaster Categories

- Hardware failure
- Network failure
- Human error
- Malicious action
- Natural events

---

## Categories Overview

![disaster_categories](svg/courses/architecting/disaster-recovery/01_introduction/disaster_categories.svg)

---

## DR Strategies Spectrum

- Backup and restore
- Pilot light
- Warm standby
- Active-active

---

## Compliance Drivers

- Regulators define minimums
- Banks, healthcare, government
- Audits verify
- Document everything

---

## Stakeholders

- Engineering
- Operations
- Security
- Business owners
- Legal

---

## Course Outline

- Strategies in depth
- Backup and restore
- Multi-region
- Testing
- Runbooks

---

## Common DR Mistakes

- Treating backup as DR
- No RPO or RTO targets
- No tested runbook
- No regular drill
- Single-region for critical service
