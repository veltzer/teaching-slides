---
tags:
  - security:network
level: intermediate
category: networking
audience:
  - audiences:devops
  - audiences:security

---
# Perimeter and Segmentation

---
## What This Chapter Covers

- Firewalls
- Proxies
- VPNs
- Network segmentation
- Micro-segmentation

---
## Firewalls

- Allow-listed traffic only
- Stateful by default
- Default-deny is the only safe stance
- Logged on every drop

---
## Stateful vs Stateless

- Stateful tracks connections
- Stateless inspects each packet
- Stateful is the standard
- Stateless still useful at edge

---
## Web Application Firewall

- Application-layer filter
- Blocks known attack patterns
- Tunable rule sets
- Not a substitute for secure code

---
## Proxies

- Forward proxies for outbound
- Reverse proxies for inbound
- Decode traffic for inspection
- Add caching and rate limiting

---
## TLS Termination

- Decrypt at trusted point
- Inspect or route
- Re-encrypt to backend in some setups
- Manage certificates carefully

---
## VPNs

- Encrypted tunnel between sites or users
- Site-to-site for offices
- Remote-access for users
- Slowly being replaced by zero-trust access

---
## Bastion Hosts

- Single entry point to internal systems
- Audited
- Hardened
- Logs every session

---
## Segmentation

- Split network by trust zones
- Limit lateral movement
- Different rules per zone
- Default for any non-trivial network

---
## VLANs

- Logical separation on shared hardware
- Cheap to deploy
- Can be bypassed if misconfigured
- Pair with proper firewalling

---
## Micro-Segmentation

- Per-workload rules
- Cloud-native or host-based
- Limits blast radius of breach
- Tooling has matured

---
## DMZ

- Public-facing systems isolated
- Cannot reach internal directly
- Common pattern for legacy
- Cloud services replace some uses

---
## NAT

- Translates internal addresses
- Provides accidental obscurity
- Not a security control itself
- Often combined with firewall

---
## Common Perimeter Mistakes

- Wide allow rules
- One zone for everything
- VPN as the only barrier
- VLAN without firewall
- WAF in detect-only mode forever
