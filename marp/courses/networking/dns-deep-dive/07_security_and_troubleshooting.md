---
tags:
  - networking:dns
  - security:attacks
  - concepts:troubleshooting
level: intermediate
category: networking
audience:
  - audiences:sysadmins
  - audiences:network-engineers

---
# DNS Security and Troubleshooting

---
## What This Chapter Covers

- DNS attack landscape
- Cache poisoning and reflection DDoS
- DNS tunneling and exfiltration
- Response Policy Zones (RPZ)
- Troubleshooting toolkit

---
## DNS Attack Landscape

- Cache poisoning
- DNS amplification DDoS
- Hijacking via registrar attacks
- Tunneling for command-and-control
- DGA (Domain Generation Algorithm) for malware

---
## Threat Map Visualized

![attack_map](svg/courses/networking/dns-deep-dive/07_security_and_troubleshooting/attack_map.svg)

---
## Cache Poisoning

- Inject fake records into a resolver's cache
- All clients of that resolver get bad answers
- Kaminsky attack (2008) was a major case
- Mitigation: random source ports, DNSSEC
- Modern resolvers are much harder to poison

---
## DNS Amplification DDoS

- Attacker spoofs source IP (the victim's)
- Sends small queries to open resolvers
- Resolvers respond with large answers to the victim
- Amplification factor of 50x or more
- Defense: don't run open resolvers; rate limit; BCP38 ingress filtering

---
## Reflection Attacks

- Similar to amplification, sometimes the same
- Attacker uses many resolvers as reflectors
- Victim's link saturates
- ANY queries are particularly damaging (now restricted)
- DNS Flag Day improvements help

---
## DNS Tunneling

- Encode arbitrary data in DNS queries
- Used by malware for command-and-control
- Hard to block — DNS is allowed everywhere
- Detect via query patterns and volume
- Specialized DNS firewalls (RPZ) help

---
## DNS Tunneling Patterns

- Many TXT queries to a controlled domain
- Long random subdomain names
- High query rates from one client
- Outbound traffic in DNS responses
- Statistical detection works well

---
## Domain Generation Algorithms (DGA)

- Malware generates domain names algorithmically
- Tries each one until it finds the active C2
- Defenders can't block static lists
- Detection by entropy, lexical patterns
- ML-based classifiers in modern security tools

---
## NXDOMAIN Hijacking

- ISPs return ads for typo'd domains
- Breaks negative caching
- Breaks software that relies on NXDOMAIN
- Major ISPs largely stopped doing this
- Watch out for it; switch resolvers if affected

---
## DNS Hijacking via Registrar

- Attacker compromises registrar account
- Changes NS records to attacker's
- All traffic redirected
- Major incidents in recent years
- Mitigation: registry lock, MFA on registrar

---
## Registrar Lock

- Disables NS changes without manual confirmation
- Many registrars offer this for free
- Some require phone confirmation
- High-value domains should be locked
- One of the most underused security features

---
## Response Policy Zones (RPZ)

- Resolver-level domain filtering
- Block, redirect, or modify responses
- Block known malicious domains
- Filter based on subscription feeds
- Works with any RPZ-aware resolver (BIND, Unbound)

---
## RPZ Use Cases

- Block ads and malware domains
- Enforce corporate policy
- Sinkhole infected hosts
- Compliance: block illegal content
- Pair with threat intelligence feeds

---
## Sinkholing

- Redirect known-bad domains to a controlled IP
- Logs which hosts try to contact them
- Identifies infected hosts in your network
- Disrupts active malware
- Standard incident-response technique

---
## Logging and Monitoring

- Log all queries (with care for privacy/scale)
- Monitor query rates per client
- Alert on entropy/randomness spikes
- Tools: Stamus, Zeek, Bro, custom pipelines
- Pair with threat intel for triage

---
## DNS Firewalls

- RPZ + threat intel + analytics
- Cloud (Cloudflare Gateway) or on-prem
- Catches early stages of many attacks
- Increasingly common in enterprises
- Privacy concerns — log retention policies

---
## Troubleshooting: dig

- The standard tool — learn it well
- `dig example.com` — basic A record
- `dig +trace example.com` — full recursive walk
- `dig +dnssec example.com` — show signatures
- `dig @8.8.8.8 example.com` — query specific resolver

---
## Reading dig Output

- HEADER: status, flags, IDs
- QUESTION: what you asked
- ANSWER: matching records
- AUTHORITY: who can answer
- ADDITIONAL: helpful glue records

---
## Useful dig Flags

- `+short` — only the answer values
- `+trace` — manual recursion
- `+norec` — disable recursion (test auth servers)
- `+noall +answer` — clean answer-only output
- `+tcp` — force TCP (test firewall issues)

---
## Common Failures: NXDOMAIN

- The name truly doesn't exist
- Or: typo in the query
- Or: the parent's NS records are broken
- Verify with `+trace` to find where it breaks
- Check parent zone delegation

---
## Common Failures: SERVFAIL

- Server-side failure
- Possibly DNSSEC validation failure
- Possibly upstream resolver issue
- Try with another resolver to isolate
- Check the zone with DNSViz

---
## Common Failures: Slow Lookups

- Network path issues to resolver
- Resolver overloaded
- TTL=0 forcing every query upstream
- Check `dig` timing in output
- Consider local cache (dnsmasq, systemd-resolved)

---
## Diagnosing Delegation

- `dig NS example.com` — what your zone says
- `dig +trace` — what the parent says
- Mismatch = lame delegation
- Fix at parent (registrar) or zone (auth server)
- Often the cause of "DNS doesn't work"

---
## Diagnosing DNSSEC

- `dig +dnssec example.com` — see signatures
- AD flag = validated
- DNSSEC failures show as SERVFAIL
- DNSViz online tool for full chain analysis
- delv command for command-line validation

---
## Wireshark for DNS

- Capture all DNS traffic
- Filter: `dns` or `tcp.port == 53`
- See exact bytes on the wire
- Useful for protocol-level debugging
- Match query/response by transaction ID

---
## Best Practices

- Lock your registrar account; enable MFA
- Use DNSSEC where stakes warrant
- Run RPZ on internal resolvers
- Monitor query patterns
- Document your DNS topology

---
## Common Pitfalls

- Not enabling registrar lock
- Open resolvers used for reflection
- DNSSEC enabled but not monitored
- TTLs too high to recover from a mistake
- No backup nameserver provider

---
## Course Recap

- Fundamentals and resolution
- Record types
- Authoritative DNS and zones
- Recursive resolvers and caching
- DNSSEC
- DoH and DoT
- Security and troubleshooting

---
## Summary

- DNS attacks are common and varied
- Cache poisoning, amplification, tunneling, hijacking
- Defenses: source-port randomization, DNSSEC, RPZ, lock
- Troubleshooting: dig, +trace, DNSSEC analyzers
- Operate with the same care as any production infrastructure
