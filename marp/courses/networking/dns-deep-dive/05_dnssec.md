---
tags:
  - networking:dns
  - security:dnssec
level: intermediate
category: networking
audience:
  - audiences:sysadmins
  - audiences:network-engineers

---

# DNSSEC

---

## What This Chapter Covers

- Why DNSSEC exists
- Records: RRSIG, DNSKEY, DS, NSEC, NSEC3
- Zone signing: KSK and ZSK
- Chain of trust
- Key rollover and operations

---

## The Problem DNSSEC Solves

- DNS responses are unauthenticated by default
- Attackers can spoof responses (cache poisoning)
- Result: traffic redirected to malicious sites
- TLS catches some of this — but DNS itself is exposed
- DNSSEC adds cryptographic authentication

---

## What DNSSEC Provides

- Authentication: response really came from the zone owner
- Integrity: response wasn't modified in transit
- Authenticated denial: "this name does not exist" is signed too
- It does NOT provide confidentiality — that's DoH/DoT
- Different protections; both useful

---

## DNSSEC Records Visualized

![dnssec_chain](svg/courses/networking/dns-deep-dive/05_dnssec/dnssec_chain.svg)

---

## DNSSEC Record Types

![dnssec_records](svg/courses/networking/dns-deep-dive/05_dnssec/dnssec_records.svg)

---

## Key Rollover

![key_rollover](svg/courses/networking/dns-deep-dive/05_dnssec/key_rollover.svg)

---

## RRSIG: Record Signatures

- Each record set is signed
- Signature is itself a record (RRSIG)
- Verifier checks signature with the public key
- Signed with the zone's private key
- Validity period limits replay

---

## DNSKEY: Public Keys

- The zone's public keys, in DNS itself
- Multiple keys allowed (rollovers, separation)
- Signed by the zone's KSK
- Lookups return both DNSKEY and its RRSIG
- Resolvers cache them for the validity period

---

## DS: Delegation Signer

- Hash of the child zone's KSK
- Stored in the parent zone
- Signed by the parent zone's keys
- Creates the chain of trust
- Critical: missing/wrong DS breaks DNSSEC

---

## KSK and ZSK

- Key Signing Key — signs DNSKEY records only
- Zone Signing Key — signs everything else
- KSK rarely changes; ZSK rotated frequently
- Splitting reduces parent-zone interaction
- KSK rollover is the harder operation

---

## NSEC: Authenticated Denial

- "This name does not exist between A and Z"
- Signed list of record-sets in the zone
- Allows authenticated NXDOMAIN
- Reveals zone contents — privacy concern
- Replaced by NSEC3 in many deployments

---

## NSEC3: Hashed Denial

- Same idea as NSEC, but names are hashed
- Doesn't reveal zone contents
- Still allows authenticated denial
- More CPU on signing; resolvers verify hashes
- Default for most signed zones today

---

## The Chain of Trust

- Root zone is signed
- Root signs `.com` (via DS)
- `.com` signs `example.com` (via DS)
- `example.com` signs its records
- Resolver validates from root downward

---

## Trust Anchor

- The root key must be known a priori
- Distributed in resolver software
- Updated rarely; high security around the root KSK
- Without a trust anchor, you trust nothing
- All DNSSEC validators ship with the root anchor

---

## Validating Resolver

- Receives signed responses from the wire
- Walks the chain to root
- Checks each signature
- AD bit set in response if validated
- Failed validation: SERVFAIL

---

## Enabling Validation

- Most modern resolvers default to validating
- `dig +dnssec` to see signatures
- AD flag in response means validated
- Test with `dig dnssec-failed.org` (intentionally broken)
- Should fail; if it doesn't, your resolver isn't validating

---

## Signing a Zone (BIND)

- Generate KSK and ZSK
- Configure auto-DNSSEC in named.conf
- Add DS to parent zone via registrar
- Verify from external validating resolver
- Monitor for rollover events

---

## Signing a Zone (Cloud)

- One-click in Route 53, Cloud DNS, others
- Provider manages keys
- You must add DS to registrar
- Verification step is yours
- Easier than running BIND for most

---

## Key Rollover: ZSK

- Every few months typically
- Generate new ZSK
- Sign zone with both old and new
- Wait for caches to update
- Remove old ZSK

---

## Key Rollover: KSK

- Every 1-5 years typically
- Coordinate with the parent (DS update)
- Slower; more impact if mishandled
- Detailed RFC 7583 procedures
- Manage with tools (knot, opendnssec)

---

## DNSSEC Operational Risks

- Expired signatures: zone goes dark
- Wrong DS at parent: validation fails
- Misaligned key timestamps: validation fails
- Lost private keys: can't sign new records
- Most outages are operational, not cryptographic

---

## Validity Periods

- RRSIG has not-before and not-after
- Default: 30 days
- Re-sign before expiration
- Automate this — manual is the enemy
- Monitor with health checks

---

## DNSSEC Adoption

- Root: 100%
- TLDs: most major ones signed
- Domains: 5-15% globally; higher in some sectors
- Validating resolvers: ~80% of users behind a validator
- DNSSEC has caught many real attacks

---

## DANE: Real-World Use

- DNS-Based Authentication of Named Entities
- TLSA records pin certs in DNS (via DNSSEC)
- Used by SMTP servers (RFC 7672)
- Strong defense against rogue CAs
- Limited browser adoption

---

## DNSSEC and DoH/DoT

- DoH/DoT encrypts DNS in transit
- DNSSEC signs the data
- They solve different problems
- Use both for full security
- Don't substitute one for the other

---

## When NOT to Use DNSSEC

- Internal-only zones with no external exposure
- Test/dev environments where breakage is acceptable
- When your team can't operationally maintain it
- DNSSEC-failed.org is a real failure mode
- Better safe and unsigned than broken and signed

---

## Common Pitfalls

- Forgetting to add DS at registrar after enabling
- Not monitoring signature expiration
- Failed key rollover stranding the zone
- Resolver doesn't validate — DNSSEC adds nothing
- Mixing signed and unsigned subzones inconsistently

---

## Validating With dig

```bash
dig +dnssec example.com A

# Look for AD flag in flags
# Look for RRSIG records in answer section
# +sigchase shows the chain (older dig)
```

---

## Tools

- `delv` — modern DNSSEC validation tool
- `dnssec-validator` browser extension
- DNSViz online debug tool
- Verisign DNSSEC analyzer
- Most cloud providers offer health pages

---

## Summary

- DNSSEC adds cryptographic signing to DNS
- RRSIG signs records, DNSKEY publishes the keys
- DS in parent zone delegates trust
- KSK and ZSK separate concerns
- Operational complexity is the main barrier — automate it
