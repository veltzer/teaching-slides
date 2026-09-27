---
tags:
  - infrastructure:linux
  - security:forensics
  - security:security
level: advanced
category: security
audience:
  - audiences:security-professionals

---

# Capstone Forensic Investigation

## Course: Linux Forensics - Day 5 (continued)
- A full investigation that exercises every skill from the week
- You receive a disk image and a memory dump from a compromised host
- Work the case end to end, then defend your conclusions in the report
- This is analysis of prepared evidence in an isolated lab environment

---

## The Scenario

- A Linux server showed unexplained outbound traffic and was taken offline
- You are handed a forensic disk image and a `LiME` memory capture
- Both exhibits arrive with hashes; verify them before touching anything
- Your task is to reconstruct what happened, in order, with evidence

```bash
# First act on any exhibit: prove integrity
sha256sum -c /evidence/disk.dd.sha256
sha256sum -c /evidence/ram.lime.sha256

# Work on copies, mounted read-only
mount -o ro,loop,offset=$((2048*512)) /evidence/disk.dd /mnt/case
```

---

## Objectives

1. 1. Establish the initial point of compromise and its timestamp
1. 1. Reconstruct the attacker's timeline across disk and memory
1. 1. Identify the privilege escalation path to root
1. 1. Recover the implant and characterize what it does
1. 1. Assess persistence, then classify the incident's risk
1. 1. Produce a court-ready report with a full evidence trail

---

## Suggested Workflow: Disk

```bash
# Build a super-timeline to anchor every later finding
fls -r -m / -o 2048 /evidence/disk.dd > /evidence/body
mactime -b /evidence/body -d > /evidence/timeline.csv

# Follow the intrusion through the usual artifacts
less /mnt/case/var/log/auth.log
cat /mnt/case/home/*/.bash_history
ls -la /mnt/case/etc/cron.d /mnt/case/etc/systemd/system

# Recover deleted evidence the attacker tried to remove
extundelete /evidence/disk.dd --restore-all
```

- Let the timeline drive the story; hang each artifact off a timestamp

---

## Suggested Workflow: Memory

```bash
# Ground truth for what was actually running
vol -f /evidence/ram.lime linux.pstree
vol -f /evidence/ram.lime linux.bash

# Hidden objects and kernel tampering
vol -f /evidence/ram.lime linux.hidden_modules
vol -f /evidence/ram.lime linux.check_syscall

# Live network state at capture time
vol -f /evidence/ram.lime linux.sockstat
```

- Memory reveals what disk cannot: running processes and hidden modules
- Reconcile the memory picture against the disk timeline for contradictions

---

## Characterizing the Implant

- Recover the implant binary from disk or dump it from memory
- Analyze it statically and in an isolated sandbox, never on a live network
- Goal is to document capability and IOCs, not to operate the malware

```bash
# Static triage of the recovered binary
file recovered_implant ; sha256sum recovered_implant
strings -n 8 recovered_implant | grep -iE "http|/tmp|sh -i|connect"
readelf -a recovered_implant | less
```

- Record its persistence mechanism, its C2 endpoints, and its capabilities
- Tie every IOC back to something observed in the timeline or the traffic

---

## Deliverables

1. 1. An executive summary and an incident risk classification
1. 1. A timeline reconstructing the compromise from entry to detection
1. 1. The privilege escalation path, with the evidence for each step
1. 1. The implant analysis: persistence, IOCs, and capabilities
1. 1. A hash-verified evidence appendix and a chain-of-custody record

---

## Assessment Criteria

- Every claim is backed by a specific, reproducible piece of evidence
- Disk and memory findings are reconciled rather than reported in isolation
- The timeline is coherent and accounts for the attacker's actions
- Integrity is provable end to end: hashes, read-only handling, clean notes
- The report is clear enough for a non-technical decision-maker to act on
