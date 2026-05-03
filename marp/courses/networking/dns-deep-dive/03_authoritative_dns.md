---
tags:
  - networking:dns
  - concepts:authoritative
level: intermediate
category: networking
audience:
  - audiences:sysadmins
  - audiences:devops

---
# Authoritative DNS and Zones

---
## What This Chapter Covers

- Zone file format and structure
- Primary and secondary nameservers
- Zone transfers: AXFR and IXFR
- Dynamic DNS and TSIG
- Cloud-hosted zones

---
## What Is a Zone?

- A contiguous portion of the namespace
- Administered as a unit
- One SOA record at the apex
- May contain delegations to sub-zones
- Lives on authoritative nameservers

---
## Zone File Format

```output
$ORIGIN example.com.
$TTL 3600

@   IN  SOA  ns1.example.com. admin.example.com. (
                2026010101 3600 1800 604800 300)
@   IN  NS   ns1.example.com.
@   IN  NS   ns2.example.com.
@   IN  A    1.2.3.4
www IN  A    1.2.3.4
mail IN MX 10 mail.example.com.
mail IN A    5.6.7.8
```

---
## Zone File Anatomy

- `$ORIGIN` — the zone name
- `$TTL` — default TTL for records
- `@` — shorthand for the origin
- Names without trailing dot are relative
- Tab-separated; columns are name, class, type, data

---
## Primary Nameserver

- Holds the master copy of the zone
- All edits made here
- Pushes changes to secondaries via NOTIFY
- Single source of truth
- Often called "master" historically

---
## Secondary Nameservers

- Read-only copies of the zone
- Pull from primary via AXFR or IXFR
- Provide redundancy and load distribution
- Can be in different geographic locations
- Listed in NS records alongside primary

---
## Zone Transfer Visualized

![zone_transfer](svg/courses/networking/dns-deep-dive/03_authoritative_dns/zone_transfer.svg)

---
## Zone File Anatomy

![zone_file](svg/courses/networking/dns-deep-dive/03_authoritative_dns/zone_file.svg)

---
## Anycast Deployment

![anycast_deployment](svg/courses/networking/dns-deep-dive/03_authoritative_dns/anycast_deployment.svg)

---
## AXFR — Full Zone Transfer

- Transfer the entire zone
- Used on initial sync and when serial mismatches significantly
- Over TCP — UDP can't carry it
- Can be large for big zones
- Often restricted by IP for security

---
## IXFR — Incremental Zone Transfer

- Transfer only the changes since a given serial
- Faster for small updates to large zones
- Falls back to AXFR if too many changes
- More complex protocol than AXFR
- Default in modern setups

---
## NOTIFY

- Primary tells secondaries: "I've updated"
- Sent on every zone change
- Triggers secondaries to fetch the new zone
- Faster than waiting for the refresh interval
- Standard in modern deployments

---
## Serial Number

- Increases with every zone change
- Secondaries compare their serial with primary's
- Higher serial = newer zone
- Convention: YYYYMMDDNN
- Bumping the serial without changes is occasionally needed

---
## Refresh, Retry, Expire

- Refresh: how often to check for updates (3600s default)
- Retry: if check fails, retry interval (1800s)
- Expire: give up after this long (604800s = 1 week)
- After expire, secondary stops serving the zone
- Tune for your topology

---
## TSIG: Authenticated Updates

- Transaction signatures for DNS messages
- Shared secret between primary and secondary
- Authenticates AXFR/IXFR/NOTIFY/UPDATE
- Prevents impersonation
- Standard for managed DNS today

---
## Dynamic DNS

- RFC 2136: programmatic record updates
- Used by DHCP servers (consumer routers)
- Used by Active Directory
- Authenticated with TSIG or GSS-TSIG
- A power tool — use with care

---
## Glue Records

- A nameserver's address inside its own zone
- Without glue: chicken-and-egg lookup problem
- Parent zone provides hints
- Required when nameserver is inside the zone
- Easy to forget — breaks delegation

---
## Cloud-Hosted Zones

- AWS Route 53
- Google Cloud DNS
- Azure DNS
- Cloudflare DNS
- All managed; you don't run servers

---
## Route 53

- Highly available, globally distributed
- Health checks integrated with DNS
- Latency-based and geolocation routing
- Private zones for VPCs
- Pay per query (very cheap at low volume)

---
## Choosing a Provider

- Performance (anycast quality)
- Features (health checks, geolocation, DNSSEC)
- Reliability (track record matters)
- Price (per zone, per query)
- Most enterprises use multiple providers for redundancy

---
## Multi-Provider DNS

- Two providers serving the same zone
- NS records point to both
- Survives one provider's outage
- Adds operational complexity
- Sync mechanism: CI pipeline writing both APIs

---
## Zone File Best Practices

- Comment liberally
- Group related records
- Use consistent TTLs
- Bump serial on every change
- Validate before deploying

---
## Validation Tools

- `named-checkzone` — BIND-specific zone validation
- `nsd-checkzone` — for NSD
- Online tools for DNSSEC and propagation
- Cloud providers run validation on their side
- Test before deploying production changes

---
## Change Management

- All changes via version-controlled zone files
- Pull-request reviews like code
- Automated validation in CI
- Roll-forward plans for failures
- DNS changes need rollback paths

---
## Common Pitfalls

- Forgetting to bump the serial
- Inconsistent NS at parent and child
- TTL too long during a planned change
- No backup provider; one provider's outage is yours
- Forgetting glue when delegating

---
## Operational Concerns

- Monitor query rates per zone
- Alert on AXFR failures
- Track propagation lag (`dig` + monitor)
- Plan for DDoS — use DDoS-protected providers
- Keep registrar credentials secure (lock domains)

---
## Summary

- Zones are the unit of authoritative DNS administration
- Primary holds the truth; secondaries provide redundancy
- AXFR/IXFR for transfer; TSIG for authentication
- Cloud DNS removes operational burden
- Multi-provider for true high availability
