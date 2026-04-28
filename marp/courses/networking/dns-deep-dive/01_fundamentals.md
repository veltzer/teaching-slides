---
tags:
  - networking:dns
  - concepts:fundamentals
level: intermediate
category: networking
audience:
  - audiences:developers
  - audiences:sysadmins

---
# DNS Fundamentals and Resolution

---
## What This Chapter Covers

- Purpose and namespace hierarchy
- Domain name structure
- Resolution: recursive vs iterative
- Resolvers and authoritative nameservers
- Wire format, TTL, caching

---
## What Is DNS?

- The Domain Name System
- Maps human-friendly names to addresses (and more)
- Distributed, hierarchical database
- Foundational internet infrastructure
- Used billions of times per second worldwide

---
## Why DNS Matters

- Without it: every website needs an IP address memorized
- With it: type a name, get connected
- Far more than name → IP — many record types
- Failures cascade: DNS down → many systems unusable
- Often the actual cause of "internet is down"

---
## The Namespace Hierarchy

- Root (`.`) at the top
- Top-level domains (TLDs): `.com`, `.org`, `.uk`
- Second-level domains: `example.com`, `wikipedia.org`
- Subdomains: `mail.example.com`, `en.wikipedia.org`
- Each level delegated to the next

---
## Hierarchy Visualized

![hierarchy](svg/courses/networking/dns-deep-dive/01_fundamentals/hierarchy.svg)

---
## Domain Name Anatomy

- `mail.example.com.` (the trailing dot is the root)
- `mail` — leftmost label, deepest in tree
- `example` — second-level
- `com` — top-level
- Read right-to-left for hierarchy

---
## Fully Qualified Domain Name

- FQDN ends with the (often-implicit) root dot
- `example.com.` is fully qualified
- `example` alone is not — relative
- Resolvers add search domains for relative names
- Always use FQDNs in configs to avoid ambiguity

---
## Resolution: The Big Picture

- Client wants `www.example.com`
- Asks a recursive resolver
- Resolver walks the hierarchy
- Returns the answer to the client
- Caches it for next time

---
## Recursive vs Iterative

- Recursive resolver: "find the answer for me"
- Iterative resolver: "tell me where to look next"
- Stub resolvers (your laptop): always recursive
- Authoritative nameservers: always iterative
- Recursive resolvers do the iterative walking

---
## Resolution Walk

- Stub asks recursive: `www.example.com?`
- Recursive asks root: where is `.com`?
- Root replies: ask `a.gtld-servers.net`
- Recursive asks that server: where is `example.com`?
- It replies: ask `ns1.example.com`
- That server replies: `www.example.com is 1.2.3.4`

---
## Resolution Visualized

![resolution_flow](svg/courses/networking/dns-deep-dive/01_fundamentals/resolution_flow.svg)

---
## Root Servers

- 13 logical root servers (a-m.root-servers.net)
- Each backed by anycast — many physical instances worldwide
- Operated by 12 organizations
- Hold the root zone — pointers to all TLDs
- Critical infrastructure; carefully maintained

---
## TLD Servers

- Hold delegation records for each domain in the TLD
- `.com` zone: who runs `example.com`?
- Operated by registries (Verisign for `.com`)
- Massive query load
- Anycast deployment everywhere

---
## Authoritative Nameservers

- Hold the actual records for a zone
- Run by domain owners or DNS providers
- Cloudflare, Route 53, NS1, others
- Multiple per zone for redundancy
- The source of truth for that domain

---
## Stub Resolvers

- The DNS client on your laptop, phone, server
- Doesn't do recursion itself
- Asks a configured recursive resolver
- Configured via DHCP or `/etc/resolv.conf`
- Tiny piece of code; large blast radius

---
## Recursive Resolvers

- Do the work of walking the hierarchy
- Heavy caching reduces upstream load
- Public ones: `8.8.8.8`, `1.1.1.1`, `9.9.9.9`
- ISPs run their own
- Enterprises run their own (often Unbound or BIND)

---
## DNS Wire Protocol

- Default: UDP port 53
- TCP port 53 for large responses (>512 bytes traditionally)
- Modern DNS: EDNS(0) extends UDP up to 4096 bytes
- DoH/DoT for encrypted variants (later chapter)
- Simple binary format; not human-readable

---
## DNS Message Structure

- Header: ID, flags, counts
- Question: name, type, class
- Answer: matching records
- Authority: who can answer authoritatively
- Additional: helpful glue records

---
## TTL: Time To Live

- Each record has a TTL — seconds to cache
- Short TTL (60s): fast propagation, more queries
- Long TTL (24h): less load, slower propagation
- Plan TTL drops before changes you want fast
- Negative caching also uses TTL

---
## TTL Trade-Offs

- Service migration: drop TTL to 60s a day before
- Cut over, monitor
- Raise TTL back when stable
- Shorter TTL = better failover, more cost
- Critical infrastructure often uses 5-15 minute TTLs

---
## Caching

- Recursive resolvers cache aggressively
- Stub resolvers cache too (often per-process)
- Browsers cache too (often per-tab)
- Multi-layer caching is the norm
- Cache invalidation is hard; thus TTL

---
## Negative Caching

- "Domain doesn't exist" responses are cached too
- NXDOMAIN response cached per SOA minimum
- Reduces load when checking many bad names
- Default 5-15 minutes typically
- Configurable per zone

---
## UDP vs TCP

- UDP for most queries — small, fast, fire-and-forget
- TCP fallback when UDP packet too big
- TCP also for zone transfers (AXFR/IXFR)
- DNSSEC responses often need TCP
- Modern resolvers use both seamlessly

---
## Common Pitfalls

- Forgetting the trailing dot in zone files
- Setting TTLs too high during a migration
- Hardcoding `8.8.8.8` instead of using DHCP
- Not testing across multiple resolvers
- Ignoring NXDOMAIN caching during testing

---
## Tools You'll Use

- `dig` — the standard query tool
- `nslookup` — older, simpler queries
- `host` — quick name-to-IP and reverse
- `drill` — DNSSEC-aware
- Browser dev tools — for HTTP-level DNS effects

---
## Summary

- DNS: distributed hierarchy from root through TLDs to domains
- Stub asks recursive; recursive walks the hierarchy
- TTL governs caching at every level
- Caching is what makes DNS fast — and propagation slow
- The next chapters go deep on records, security, and operations
