---
tags:
  - networking:dns
  - concepts:resolvers
level: intermediate
category: networking
audience:
  - audiences:sysadmins
  - audiences:devops

---
# Recursive Resolvers and Caching

---
## What This Chapter Covers

- How resolvers walk the hierarchy
- Caching: positive and negative
- Configuring Unbound and BIND
- Public resolvers
- EDNS and resolver selection

---
## What a Resolver Does

- Receives a query from a stub
- Walks the DNS hierarchy if not cached
- Caches the answer for next time
- Returns the response to the stub
- Handles retries, fallbacks, EDNS extensions

---
## Cache: The Critical Optimization

- Without cache: every query walks the hierarchy
- With cache: first query is slow, the rest fast
- Cache hit ratio in the high 90s for popular sites
- Memory size of the cache matters
- Tuning the cache is core resolver tuning

---
## Cache Behavior Visualized

![cache_flow](svg/courses/networking/dns-deep-dive/04_resolvers/cache_flow.svg)

---
## Positive Caching

- Cache successful responses
- Each record cached per its TTL
- Different records of the same name cached independently
- Multi-level: stub, OS, browser, recursive
- All respect the TTL

---
## Negative Caching

- Cache "no such record" responses
- NXDOMAIN means the *name* doesn't exist
- NODATA means the *type* doesn't exist for that name
- Cached per the SOA minimum
- Reduces load when scanning bad names

---
## Cache Poisoning

- Attacker tricks the resolver into accepting bad data
- Once cached, all clients of that resolver get bad answers
- The Kaminsky attack (2008) was a major case
- Mitigations: random source ports, DNSSEC
- Active defense remains essential

---
## Source Port Randomization

- Old DNS used predictable source ports
- Attackers could spoof responses
- Modern resolvers randomize source ports
- 16 bits of port + 16 bits of query ID = 32 bits to guess
- Massive defense improvement; not perfect

---
## Unbound

- Validating, caching, recursive resolver
- Open source, modern, lightweight
- DNSSEC validation built in
- DoT and DoH support
- Default in many distros and projects

---
## Configuring Unbound

```output
server:
    interface: 0.0.0.0
    access-control: 192.168.1.0/24 allow
    cache-min-ttl: 300
    prefetch: yes
    qname-minimisation: yes
```

- Run on the LAN for local resolution
- Tune cache, security, privacy options
- Pair with `unbound-anchor` for DNSSEC keys

---
## BIND as Recursive Resolver

- The original DNS server
- Massive feature set, including recursion
- Views allow split-horizon DNS
- Forwarding to upstream resolvers
- Often overkill if you only need recursion (use Unbound)

---
## Public Resolvers

- 8.8.8.8 / 8.8.4.4 — Google
- 1.1.1.1 / 1.0.0.1 — Cloudflare
- 9.9.9.9 / 149.112.112.112 — Quad9
- 208.67.222.222 — OpenDNS / Cisco
- Different privacy, filtering, performance trade-offs

---
## Comparing Public Resolvers

- Google — fast, neutral
- Cloudflare — fast, no-logging promise
- Quad9 — blocks known malicious domains
- OpenDNS — content filtering options
- Pick based on privacy and feature needs

---
## Should You Run Your Own?

- Pros: privacy, control, optimization for your apps
- Cons: operational burden, attack target
- Most homes: ISP or public is fine
- Most enterprises: own resolver for visibility
- Critical infrastructure: own + redundancy

---
## Resolver Selection

- Stubs configured with one or more
- Multiple for failover; not load balancing
- Browsers may have their own (DoH bypass)
- IT policies may force-set
- Visibility: who queries what

---
## EDNS(0)

- Extension Mechanisms for DNS
- Negotiates: larger UDP, DNSSEC support, more
- Standard in modern DNS
- Most failures are firewalls dropping EDNS packets
- The "DNS doesn't work" cause more often than you think

---
## EDNS Client Subnet (ECS)

- Resolvers tell auth servers the client's IP prefix
- Authorities can return geo-tailored answers
- Privacy-leaking — some resolvers strip it
- CDNs use it heavily
- Trade-off: better routing vs more privacy exposure

---
## Forwarders

- Resolver passes queries to another resolver
- Useful in constrained networks
- Conditional forwarding for specific zones
- Common in corporate networks
- Adds a hop; affects latency and trust

---
## DNS Views (Split-Horizon)

- Different answers for different clients
- Internal clients see internal IPs
- External clients see external IPs
- Configured in BIND, available in some others
- Foundation for "intranet" DNS

---
## Query Logging

- Resolvers can log every query
- Privacy implications — be cautious
- Useful for security investigations
- High-volume — sampling often necessary
- Compliance-friendly retention policies

---
## Query Minimization

- Old: send full query name to root
- New (RFC 7816): send only what's necessary at each level
- Better privacy: root doesn't see your full domain
- Now default in modern resolvers
- Still rolling out

---
## Aggressive NSEC

- Use DNSSEC NSEC records to deduce non-existence
- Reduces queries for "this doesn't exist either"
- Improves performance for scanned domains
- Enabled by default in modern resolvers
- DNSSEC adds value beyond authentication

---
## Resolver Performance Tuning

- Cache size: bigger is better up to a point
- Threads: match to CPU cores
- Timeout values: balance retries with latency
- Prefetch popular records before TTL expires
- Benchmark with `dnsperf`

---
## Troubleshooting Resolvers

- `dig +trace` — manual recursive walk
- Check `/etc/resolv.conf`
- Test with multiple public resolvers
- Watch for stale cache during deploys
- Verify EDNS support per network path

---
## Common Pitfalls

- Misconfigured forwarder loops
- Broken EDNS upstream — silent failures
- Massive cache without enough memory
- Public resolver fallback isn't immediate
- Stale cache after a TTL drop wasn't honored

---
## Best Practices

- Run your own internal resolver
- Cache on each tier
- Set sensible TTLs
- Monitor query latency and error rates
- Test from multiple network paths

---
## Summary

- Resolvers walk the hierarchy and cache aggressively
- Cache poisoning is real; mitigations are standard
- Unbound for modern, lightweight; BIND for full features
- Public resolvers good defaults; own resolver for visibility
- EDNS, ECS, query minimization shape modern DNS
