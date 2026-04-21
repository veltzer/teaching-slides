---
tags:
  - security:security
  - security:cyber-attacks
  - security:penetration-testing
  - security:vulnerabilities
level: intermediate
category: security
audience:
  - audiences:developers
  - audiences:security-professionals

---

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

![diagram](svg/courses/security/cyber-attacks-and-vectors/08_dns_cache_poisoning/diagram.svg)

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

![dns_resolution_process_normal](svg/courses/security/cyber-attacks-and-vectors/08_dns_cache_poisoning/dns_resolution_process_normal.svg)

---

## Kaminsky Attack (2008): Overview

The most famous DNS cache poisoning technique, discovered by Dan Kaminsky:

---

## Kaminsky Attack (2008)

![kaminsky_attack_2008](svg/courses/security/cyber-attacks-and-vectors/08_dns_cache_poisoning/kaminsky_attack_2008.svg)

---

## Transaction ID Vulnerability

![transaction_id_vulnerability](svg/courses/security/cyber-attacks-and-vectors/08_dns_cache_poisoning/transaction_id_vulnerability.svg)

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

![dnssec_how_it_works](svg/courses/security/cyber-attacks-and-vectors/08_dns_cache_poisoning/dnssec_how_it_works.svg)

---

## DNSSEC: How It Works: Example

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
1. Configure it as a caching resolver for a test domain
1. Use Wireshark to capture DNS traffic and observe:
   - Transaction IDs
   - Source ports
   - TTL values in cached records
1. Enable source port randomization and verify with packet captures
1. Enable DNSSEC validation and test with known signed domains
1. Compare resolution behavior with and without DNSSEC for poisoned records
1. Set up DNS monitoring with passive DNS logging
