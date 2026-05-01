---
tags:
  - security:network
level: intermediate
category: networking
audience:
  - audiences:devops
  - audiences:security

---
# Detection and Cloud Security

---
## What This Chapter Covers

- Logging and SIEM
- Intrusion detection
- Cloud network primitives
- DDoS defense
- Incident response

---
## Logs Everywhere

- Edge devices
- Hosts
- Applications
- Identity providers

---
## Centralization

- Forward to central store
- Search across systems
- Long retention
- Required for incident reconstruction

---
## SIEM

- Security information and event management
- Aggregates and correlates logs
- Alerting rules
- Investigation workflows

---
## IDS And IPS

- Intrusion detection observes
- Intrusion prevention blocks
- Signature and anomaly modes
- Tune to reduce false positives

---
## Endpoint Detection

- Agent on each host
- Watches processes and network
- Blocks known bad patterns
- Feeds the SIEM

---
## NetFlow And Friends

- Summary records of connections
- Useful for forensics
- Sample at high volume
- Less data than full capture

---
## Cloud Network Primitives

- Virtual private cloud
- Subnets and route tables
- Security groups
- Network ACLs

---
## Security Groups

- Stateful per-instance firewall
- Allow rules only
- Combine for layered policies
- Default deny inbound

---
## Network ACLs

- Stateless subnet-level rules
- Allow and deny rules
- Coarser than security groups
- Layered defense

---
## Private Endpoints

- Reach managed services without internet
- Cuts egress
- Tighter security boundary
- Common pattern in modern cloud

---
## DDoS Defense

- Provider-level scrubbing
- Rate limiting at edge
- Anycast spreads load
- Preplan playbook

---
## Incident Response

- Detect
- Contain
- Eradicate
- Recover
- Learn

---
## Forensics

- Preserve evidence
- Time-line reconstruction
- Chain of custody for legal
- Document everything

---
## Common Detection Mistakes

- Logs without retention
- Alerts no one reads
- Tuning never refreshed
- No tabletop exercises
- Detection only at the perimeter
