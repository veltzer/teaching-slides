---
tags:
  - networking:dns
  - concepts:records
level: intermediate
category: networking
audience:
  - audiences:sysadmins
  - audiences:developers

---

# DNS Record Types

---

## What This Chapter Covers

- Address records: A, AAAA
- Aliases: CNAME, ALIAS/ANAME
- Mail and service: MX, SRV
- Metadata: TXT, CAA, SOA
- Modern records: HTTPS, SVCB, TLSA

---

## A and AAAA

- A — IPv4 address
- AAAA — IPv6 address
- Most basic, most queried
- Many websites have multiple A records (load balancing)
- Order may vary per query (round-robin)

---

## Common Record Types Visualized

![record_types](svg/courses/networking/dns-deep-dive/02_record_types/record_types.svg)

---

## CNAME And Aliases

![cname_aname](svg/courses/networking/dns-deep-dive/02_record_types/cname_aname.svg)

---

## Specialised Records

![special_records](svg/courses/networking/dns-deep-dive/02_record_types/special_records.svg)

---

## CNAME

- Canonical name — alias one domain to another
- `www.example.com CNAME example.com`
- Resolver follows the chain
- Cannot exist alongside other records at the same name
- Cannot apply at the zone apex (without ALIAS)

---

## CNAME Limitations

- The "no apex CNAME" rule is real and important
- `example.com` cannot be `CNAME example-elb.aws.com`
- Use `ALIAS` (Route 53) or `ANAME` (others) — provider-specific
- These resolve at the DNS layer, not the protocol
- Behave like A/AAAA but pointing to a name

---

## MX Records

- Mail Exchange — where email for this domain goes
- Has a priority (lower = preferred)
- `example.com MX 10 mail.example.com`
- Multiple MX for redundancy
- Senders try lowest priority first

---

## NS Records

- Nameserver — which servers are authoritative for the zone
- Listed in the zone itself (and at the parent)
- Multiple NS for redundancy
- Updates require coordinating registrar and server
- Mismatches between parent/child cause delegation issues

---

## TXT Records

- Arbitrary text — many uses
- SPF (mail authentication)
- DKIM (mail signing keys)
- DMARC (mail policy)
- Domain ownership verification (Google, AWS, etc)
- Maximum 255 chars per string; multiple strings allowed

---

## SPF, DKIM, DMARC

- SPF — which servers may send email for the domain
- DKIM — public keys for verifying email signatures
- DMARC — policy for SPF/DKIM failures
- All three live in TXT records
- The standard email-deliverability trinity

---

## SRV Records

- Service discovery
- `_service._proto.name` (e.g. `_sip._tcp.example.com`)
- Includes priority, weight, port, target
- Used by SIP, XMPP, Active Directory, Kubernetes
- Underused for general service discovery

---

## PTR Records

- Reverse DNS — IP to name
- Live in the `in-addr.arpa` (IPv4) or `ip6.arpa` (IPv6) tree
- Often controlled by your ISP, not you
- Important for mail server reputation
- Used by some logs and access controls

---

## SOA Records

- Start of Authority — zone metadata
- Primary nameserver, admin email, serial, timers
- Serial number bumped on each change
- Refresh, retry, expire govern secondary syncs
- Minimum is the negative caching TTL

---

## SOA Example

```output
example.com. SOA ns1.example.com. admin.example.com. (
    2026010101  ; serial
    3600        ; refresh
    1800        ; retry
    604800      ; expire
    300         ; minimum (negative TTL)
)
```

- Serial format usually YYYYMMDDNN by convention
- Critical for secondary servers to track changes

---

## CAA Records

- Certificate Authority Authorization
- Specifies which CAs may issue for the domain
- `example.com CAA 0 issue "letsencrypt.org"`
- CAs check before issuing certs
- Strong defense against fraudulent certs

---

## NS Apex vs Subdomain

- NS at the apex: who runs the whole zone
- NS at a subdomain: delegation to another zone
- `dev.example.com NS ns1.dev-provider.com`
- The subdomain becomes its own zone
- Useful for separating dev/prod or team-owned subdomains

---

## HTTPS and SVCB

- Newer record types (RFC 9460)
- Carry HTTPS connection hints
- Eliminate an extra round-trip
- Support encrypted ClientHello (ECH)
- Browsers and Cloudflare adopting actively

---

## TLSA Records

- DANE — TLS keys via DNS
- Pin certificates outside the CA system
- Requires DNSSEC for trust
- Used by SMTP, sometimes HTTPS
- Enterprise and security-conscious deployments

---

## DS and DNSKEY

- DS — Delegation Signer (in parent zone)
- DNSKEY — public keys (in child zone)
- The chain of trust for DNSSEC
- Covered in detail in chapter 5
- Mention here for record type completeness

---

## Wildcards

- `*.example.com A 1.2.3.4`
- Matches any name not otherwise defined
- Useful for catch-all subdomains
- Be careful — easy to accidentally route everything
- More-specific records win over wildcards

---

## When to Use Which

- A/AAAA — direct addresses, leaf records
- CNAME — aliases pointing to existing records
- MX — email routing
- SRV — service discovery (rare in web)
- TXT — verification, mail auth, anything custom
- CAA — control cert issuance

---

## Common Mistakes

- CNAME at the zone apex — breaks
- TXT records for SPF mixing with other purposes
- Missing CAA — anyone can issue a cert for you
- Mismatched NS records between registrar and zone
- Forgetting AAAA when adding IPv6 support

---

## TTL by Record Type

- High traffic A records: short TTL (60-300s)
- Stable infra A records: longer TTL (3600s+)
- MX records: typically days
- TXT verification: minutes
- Match TTL to change frequency

---

## Tools for Querying Each

- `dig example.com A` — A record only
- `dig example.com ANY` — all (often filtered now)
- `dig example.com MX` — mail records
- `dig example.com TXT` — text records
- `dig _dmarc.example.com TXT` — DMARC

---

## Summary

- Each record type has a specific purpose; learn the common ones
- A/AAAA for addresses, CNAME for aliases
- MX, SRV for service discovery
- TXT carries verification, mail auth, custom data
- New types (HTTPS, SVCB, TLSA) bring DNS-layer optimization
