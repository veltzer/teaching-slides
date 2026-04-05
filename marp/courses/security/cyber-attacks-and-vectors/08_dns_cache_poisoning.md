# DNS Cache Poisoning
---
## What is DNS Cache Poisoning?

DNS Cache Poisoning, also known as DNS Spoofing, is a type of cyber attack where an attacker exploits vulnerabilities in the Domain Name System (DNS) to redirect traffic from legitimate websites to malicious sites.

The attacker injects forged DNS records into the cache of a recursive DNS server, causing it to return incorrect IP addresses for requested domains.

---
## How Does DNS Cache Poisoning Work?
1. The attacker sends a large number of forged DNS responses to a recursive DNS server, containing false information mapping a domain name to a malicious IP address.
1. If one of the forged responses passes the validation checks and matches an existing recursive query, the server will cache the false record.
1. When a user requests the domain associated with the poisoned record, the recursive DNS server will return the malicious IP address, redirecting the user's traffic to a malicious site.
---

## Diagram

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <line x1="150" y1="50" x2="150" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="450" y1="50" x2="450" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="100" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="400" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-size="12">Actor A</text>
  <text x="450" y="55" text-anchor="middle" font-size="12">Actor B</text>
  <line x1="150" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_07_dns_cache_poisoning)"/>
  <line x1="450" y1="150" x2="150" y2="150" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd0_07_dns_cache_poisoning)"/>
  <defs>
    <marker id="arrowd0_07_dns_cache_poisoning" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---
## Consequences of DNS Cache Poisoning

- User traffic is redirected to malicious sites without their knowledge
- Sensitive information (e.g., login credentials, financial data) can be stolen
- Users can be exposed to malware, phishing attacks, or drive-by downloads
- Legitimate websites can be defaced or taken offline (Denial of Service)
- Damage to reputation and loss of customer trust

---

## Mitigating DNS Cache Poisoning

- Implementing DNS Security Extensions (DNSSEC) to digitally sign DNS records
- Using source port randomization and randomized query IDs
- Reducing the cache entry lifetime (TTL) for records
- Monitoring and filtering DNS traffic for suspicious activity
- Regularly updating DNS software and applying security patches
- Implementing redundant and diverse DNS infrastructure

---

## DNS Cache Poisoning Prevention Best Practices

- Enforce strict input validation and data sanitization
- Implement secure coding practices and code reviews
- Conduct regular security audits and penetration testing
- Monitor DNS logs and alerts for anomalies
- Educate users on the risks of DNS cache poisoning and phishing attacks
- Have an incident response plan in place for rapid mitigation

---

## DNS Resolution Process (Normal)

```
┌──────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Client   │───>│  Recursive    │───>│  Root DNS     │───>│  TLD DNS     │
│  Browser  │    │  Resolver     │    │  Server       │    │  Server      │
└──────────┘    └──────────────┘    └──────────────┘    └──────────────┘
                       │                                       │
                       │         ┌──────────────┐             │
                       │<────────│ Authoritative │<────────────│
                       │         │  DNS Server   │
                       │         └──────────────┘
                       │
                       │  Caches result for TTL period
                       v
                ┌──────────────┐
                │  DNS Cache    │
                │  example.com  │
                │  = 93.184.x.x │
                └──────────────┘
```

---

## Kaminsky Attack (2008)

The most famous DNS cache poisoning technique, discovered by Dan Kaminsky:

```
┌────────────────────────────────────────────────────────────┐
│                  Kaminsky Attack Flow                       │
│                                                            │
│  1. Attacker queries resolver for random.example.com       │
│     (a subdomain that does NOT exist in cache)             │
│                                                            │
│  2. Resolver sends query to authoritative server           │
│                                                            │
│  3. Before real response arrives, attacker floods           │
│     resolver with FORGED responses containing:              │
│     - Matching transaction ID (guessed/brute-forced)       │
│     - Authority section: ns1.example.com = EVIL_IP         │
│                                                            │
│  4. If forged response arrives FIRST and ID matches:       │
│     Resolver caches: example.com NS -> EVIL_IP             │
│                                                            │
│  5. ALL future queries for *.example.com go to attacker    │
│                                                            │
│  Key insight: Attacker can try thousands of times          │
│  with different random subdomains until one succeeds!      │
└────────────────────────────────────────────────────────────┘
```

---

## Transaction ID Vulnerability

```
┌──────────────────────────────────────────────────┐
│     DNS Transaction ID: 16-bit field              │
│     Only 65,536 possible values                   │
│                                                  │
│     Birthday paradox: ~250 attempts for           │
│     50% chance of guessing correctly              │
│                                                  │
│     Combined with source port (if predictable):   │
│     Attack becomes trivially easy                 │
│                                                  │
│     Fix: Source port randomization adds 16 more   │
│     bits = 2^32 combinations to guess             │
└──────────────────────────────────────────────────┘
```

---

## Detecting DNS Cache Poisoning

```bash
# Monitor DNS cache for unexpected changes
# On BIND:
rndc dumpdb -cache
grep "example.com" /var/named/data/cache_dump.db

# Check for mismatched DNS responses
dig @8.8.8.8 example.com A +short
dig @1.1.1.1 example.com A +short
# Different answers may indicate poisoning

# Monitor for high volumes of DNS responses
tcpdump -i eth0 -n 'udp src port 53' -c 1000 | \
    awk '{print $3}' | sort | uniq -c | sort -rn | head

# Check DNSSEC validation
dig example.com +dnssec +short
# AD flag in response = DNSSEC validated

# Passive DNS monitoring tools:
# - Farsight DNSDB
# - PassiveTotal
# - Security Onion
```

---

## DNSSEC: How It Works

```
┌────────────────────────────────────────────────────────────┐
│              DNSSEC Chain of Trust                          │
│                                                            │
│  Root Zone (.)                                             │
│  ┌─────────────────────┐                                   │
│  │ KSK signs ZSK       │                                   │
│  │ ZSK signs .com DS   │                                   │
│  └─────────┬───────────┘                                   │
│            │ DS record points to                           │
│            v                                               │
│  .com TLD                                                  │
│  ┌─────────────────────┐                                   │
│  │ KSK signs ZSK       │                                   │
│  │ ZSK signs example   │                                   │
│  │   .com DS            │                                   │
│  └─────────┬───────────┘                                   │
│            │ DS record points to                           │
│            v                                               │
│  example.com                                               │
│  ┌─────────────────────┐                                   │
│  │ KSK signs ZSK       │                                   │
│  │ ZSK signs A record  │                                   │
│  │ RRSIG = signature   │                                   │
│  └─────────────────────┘                                   │
│                                                            │
│  KSK = Key Signing Key                                     │
│  ZSK = Zone Signing Key                                    │
│  DS  = Delegation Signer                                   │
└────────────────────────────────────────────────────────────┘
```

```bash
# Verify DNSSEC for a domain
dig example.com +dnssec
# Look for RRSIG records and AD (Authenticated Data) flag

# Check the full DNSSEC chain
delv @8.8.8.8 example.com
# Shows "fully validated" if DNSSEC chain is intact

# Test DNSSEC validation with known-bad domain
dig dnssec-failed.org @8.8.8.8
# Should return SERVFAIL if resolver validates DNSSEC
```

---

## Exercise: DNS Cache Poisoning Lab

1. Set up a local BIND DNS resolver in a VM
2. Configure it as a caching resolver for a test domain
3. Use Wireshark to capture DNS traffic and observe:
   - Transaction IDs
   - Source ports
   - TTL values in cached records
4. Enable source port randomization and verify with packet captures
5. Enable DNSSEC validation and test with known signed domains
6. Compare resolution behavior with and without DNSSEC for poisoned records
7. Set up DNS monitoring with passive DNS logging
