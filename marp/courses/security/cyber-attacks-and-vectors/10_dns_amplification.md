# DNS Amplification Attacks

- DNS amplification is a type of Distributed Denial of Service (DDoS) attack that exploits open DNS resolvers to amplify malicious traffic directed at a target system or network

---
## How DNS Amplification Works

1. Attacker finds open DNS resolvers on the internet
1. Sends small DNS queries with spoofed source IP (victim's IP)
1. Open resolvers respond to the spoofed query, sending larger DNS responses to victim
1. With many open resolvers, amplified traffic overwhelms victim's resources

---
## Amplification Factor

- Attacker's query is small (e.g., few bytes)
- DNS response from open resolver is much larger (e.g., kilobytes)
- Amplification factor can range from 10x to 1000x
- Generates massive traffic with little bandwidth from attacker

---
## Diagram

![diagram](svg/courses/security/cyber-attacks-and-vectors/10_dns_amplification/diagram.svg)

---
## Demo

```bash
dig . NS +trace
```

### Look at the large response

---
## Impact of DNS Amplification

- Overwhelms victim's network and server resources
- Causes Denial of Service for legitimate users
- Difficult to trace the source of the attack
- Can target any system or network on the internet

---
## Mitigating DNS Amplification

- Disable open DNS resolvers (only respond to legitimate sources)
- Implement DDoS protection and traffic filtering
- Use DNS Response Rate Limiting (RRL)
- Deploy Anycast DNS to distribute traffic across multiple servers
- Keep DNS software up-to-date and patched

---

## Why Amplification Works: Query vs Response Size

```bash
# Small query (~44 bytes):
dig example.com A
# Query: 44 bytes
# Large response (~3000+ bytes):
dig . ANY
# Response: ~3000 bytes
# Amplification factor: ~68x
# DNSSEC-signed responses are even larger:
dig . DNSKEY +dnssec
# Response: ~4000+ bytes
# TXT records with SPF/DKIM:
dig google.com TXT
# Response: multiple large TXT records
```

---

## Why Amplification Works: Query vs Response Size

![response_multiple_large_txt_records](svg/courses/security/cyber-attacks-and-vectors/10_dns_amplification/response_multiple_large_txt_records.svg)

---

## IP Spoofing: The Enabler

![ip_spoofing_the_enabler](svg/courses/security/cyber-attacks-and-vectors/10_dns_amplification/ip_spoofing_the_enabler.svg)

---

## Finding Open Resolvers (for defenders)

```bash
# Check if a DNS server is an open resolver
# (test your OWN servers only)
dig @your-dns-server.com example.com A +short
# If it responds: it is resolving for external queries

# Shodan query to find open resolvers (research purposes)
# shodan search "port:53 recursion: enabled"

# Check the Open Resolver Project
# openresolver.com - tracks open resolvers globally

# Verify your DNS server is NOT an open resolver:
# From an EXTERNAL network:
dig @your-dns-ip example.com
# Should get REFUSED or no response
```

---

## BCP38: Ingress Filtering (Source Address Validation)

![bcp38_ingress_filtering_source_address_validation](svg/courses/security/cyber-attacks-and-vectors/10_dns_amplification/bcp38_ingress_filtering_source_address_validation.svg)

---

## BCP38: Ingress Filtering (Source Address Validation)

If all ISPs implemented BCP38, IP spoofing-based amplification would be impossible.

---

## Other Amplification Protocols

DNS is not the only protocol abused for amplification:

| Protocol    | Port  | Amplification Factor | Bandwidth Potential |
|-------------|-------|---------------------|---------------------|
| DNS         | 53    | 28-54x              | Very High           |
| NTP         | 123   | 556x                | Extreme             |
| Memcached   | 11211 | 51,000x             | Extreme             |
| SSDP        | 1900  | 30x                 | High                |
| SNMP        | 161   | 6x                  | Medium              |
| CharGEN     | 19    | 358x                | High                |
| LDAP        | 389   | 46-55x              | High                |

The 2018 GitHub attack used Memcached amplification: 1.35 Tbps!

---

## Mitigation: Defense in Depth

```bash
# 1. Disable open resolver (BIND)
# named.conf:
# options {
#     allow-recursion { localhost; 192.168.0.0/16; };
#     allow-query-cache { localhost; 192.168.0.0/16; };
# };

# 2. Rate limit DNS responses (BIND RRL)
# rate-limit {
#     responses-per-second 10;
#     window 5;
# };

# 3. Block ANY queries (they serve no legitimate purpose)
# response-policy { zone "rpz.local"; };

# 4. Implement BCP38 on network edge
# (Cisco router example)
# interface GigabitEthernet0/0
#   ip verify unicast source reachable-via rx

# 5. Monitor with flow data
# nfsen / ntopng for NetFlow analysis
# Alert on unusual DNS response volumes
```

---

## Exercise: DNS Amplification Analysis

1. Set up a DNS resolver in a test lab
1. Use `dig` to measure response sizes for different query types (A, MX, TXT, ANY, DNSKEY)
1. Calculate the amplification factor for each query type
1. Verify your resolver is not open to external queries
1. Configure BIND to restrict recursion and enable RRL
1. Use Wireshark to capture and analyze DNS amplification traffic patterns
1. Set up a monitoring dashboard that alerts on anomalous DNS response volume

## Conclusion

DNS amplification attacks are a significant threat, as they can generate massive amounts of traffic with relatively little effort from the attacker. By securing DNS infrastructure, implementing DDoS mitigation strategies, and keeping systems up-to-date, organizations can protect themselves from these types of attacks and maintain the availability of their online services.
