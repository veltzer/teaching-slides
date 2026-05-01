---
tags:
  - security:network
level: intermediate
category: networking
audience:
  - audiences:devops
  - audiences:security

---
# Introduction to Network Security

---
## What This Chapter Covers

- What network security is
- Threat model
- Defense in depth
- Layers of network controls
- Course outline

---
## What Network Security Is

- Protecting data and systems on networks
- Confidentiality, integrity, availability
- Spans hardware, software, people
- Continuous, not one-time

---
## Why It Matters

- Networks are the front door
- Attackers probe constantly
- Compliance demands controls
- Outages and breaches cost real money

---
## Threat Model

- Who might attack
- What they want
- How they get in
- What they would do once in

---
## Common Adversaries

- Opportunistic scanners
- Targeted criminal groups
- Insiders
- Nation-state actors

---
## Common Attack Goals

- Steal data
- Encrypt data for ransom
- Disrupt services
- Use you as a stepping stone

---
## Defense In Depth

- No single control suffices
- Multiple layers of barriers
- Each layer slows or stops attacker
- Failure of one is not failure of all

---
## Defense In Depth Visualized

![defense_in_depth](svg/courses/networking/network-security/01_introduction/defense_in_depth.svg)

---
## Network Layers

- Physical
- Data link
- Network
- Transport
- Application

---
## Where Controls Live

- At the perimeter
- In the cloud account
- Inside the host
- Inside the application

---
## Zero Trust

- Trust no network
- Authenticate every request
- Authorize every action
- Encrypt every connection

---
## Compliance Drivers

- PCI for payments
- HIPAA for health data
- GDPR for personal data
- Many sector-specific rules

---
## Logging And Visibility

- You cannot secure what you cannot see
- Logs and metrics required
- Centralize and retain
- Practice search

---
## Course Outline

- Perimeter and segmentation
- Encryption
- Identity and access
- Detection and response
- Cloud network security

---
## Common Beginner Mistakes

- Treating compliance as security
- Trusting internal networks
- No logs at the perimeter
- Long-lived static credentials
- Wide rules everywhere
