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

<svg width="700" height="400" xmlns="http://www.w3.org/2000/svg">
  <!-- Attacker -->
  <rect x="50" y="180" width="100" height="40" fill="#ffcdd2" stroke="#d32f2f" stroke-width="2" rx="5"/>
  <text x="100" y="205" text-anchor="middle" font-size="14" font-weight="bold">Attacker</text>

  <!-- Primary Open DNS Resolver -->
  <rect x="300" y="50" width="150" height="40" fill="#c8e6c9" stroke="#388e3c" stroke-width="2" rx="5"/>
  <text x="375" y="75" text-anchor="middle" font-size="14">Open DNS Resolver</text>

  <!-- Additional Open DNS Resolvers -->
  <rect x="300" y="120" width="150" height="40" fill="#c8e6c9" stroke="#388e3c" stroke-width="2" rx="5"/>
  <text x="375" y="145" text-anchor="middle" font-size="14">Open DNS Resolver</text>

  <rect x="300" y="190" width="150" height="40" fill="#c8e6c9" stroke="#388e3c" stroke-width="2" rx="5"/>
  <text x="375" y="215" text-anchor="middle" font-size="14">Open DNS Resolver</text>

  <rect x="300" y="260" width="150" height="40" fill="#c8e6c9" stroke="#388e3c" stroke-width="2" rx="5"/>
  <text x="375" y="285" text-anchor="middle" font-size="14">Open DNS Resolver</text>

  <!-- Victim -->
  <rect x="550" y="180" width="100" height="40" fill="#ffecb3" stroke="#f57c00" stroke-width="2" rx="5"/>
  <text x="600" y="205" text-anchor="middle" font-size="14" font-weight="bold">Victim</text>

  <!-- Arrow from Attacker to Primary DNS Resolver -->
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>

  <!-- Small spoofed query -->
  <path d="M 150 190 Q 225 120 300 70" stroke="#d32f2f" stroke-width="2" fill="none" marker-end="url(#arrowhead)"/>
  <text x="225" y="125" text-anchor="middle" font-size="11" fill="#d32f2f">Small spoofed query</text>

  <!-- Large DNS responses from all resolvers -->
  <path d="M 450 70 Q 500 125 550 180" stroke="#ff6b6b" stroke-width="3" fill="none" marker-end="url(#arrowhead)"/>
  <text x="490" y="115" text-anchor="middle" font-size="11" fill="#ff6b6b">Large DNS response</text>

  <path d="M 450 140 Q 500 160 550 185" stroke="#ff6b6b" stroke-width="3" fill="none" marker-end="url(#arrowhead)"/>

  <path d="M 450 210 L 550 205" stroke="#ff6b6b" stroke-width="3" fill="none" marker-end="url(#arrowhead)"/>

  <path d="M 450 280 Q 500 240 550 195" stroke="#ff6b6b" stroke-width="3" fill="none" marker-end="url(#arrowhead)"/>

  <!-- Amplification indicator -->
  <text x="375" y="350" text-anchor="middle" font-size="14" font-weight="bold" fill="#d32f2f">Amplification Factor: 10x - 1000x</text>
</svg>

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

```diagram
┌──────────────────────────────────────────────────┐
│     Amplification Factors by Record Type          │
├──────────────────────────────────────────────────┤
│  Query Type     │  Typical Factor                │
├─────────────────┼────────────────────────────────┤
│  A record       │  2-3x                          │
│  MX record      │  5-10x                         │
│  TXT record     │  10-20x                        │
│  ANY query      │  30-70x                        │
│  DNSSEC (DNSKEY)│  40-100x                       │
│  EDNS0 (4096)   │  Up to 100x                    │
└──────────────────────────────────────────────────┘
```

---

## IP Spoofing: The Enabler

```diagram
┌──────────────────────────────────────────────────────────┐
│           IP Spoofing in DNS Amplification                │
│                                                          │
│  Attacker IP: 10.0.0.1                                   │
│  Victim IP:   192.168.1.100                              │
│                                                          │
│  Step 1: Attacker crafts UDP packet                      │
│  ┌────────────────────────────────────┐                  │
│  │  Source IP: 192.168.1.100 (VICTIM) │  <-- Spoofed!    │
│  │  Dest IP:   8.8.8.8 (Open DNS)    │                  │
│  │  Query:     dig . ANY             │                  │
│  └─���──────────────────────────────────┘                  │
│                                                          │
│  Step 2: DNS server responds to VICTIM                   │
│  ���────────────────────────────────────���                  │
│  │  Source IP: 8.8.8.8               │                  │
│  │  Dest IP:   192.168.1.100 (VICTIM)│                  │
│  │  Response:  ~3000 bytes           │  <-- Amplified!  │
│  └──────────���─────────────────────────┘                  │
│                                                          │
│  UDP is connectionless: no handshake to verify source    │
└──────���──────────────────────────────��────────────────────┘
```

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

```diagram
┌──────────────────────────────────────────────────────────┐
│          BCP38 / RFC 2827: Ingress Filtering              │
│                                                          │
│  ISP Network: 203.0.113.0/24                             │
│                                                          │
│  WITHOUT BCP38:                                          │
│  ┌────────┐                    ┌──────────┐              │
│  │ Host   │── src: 10.0.0.1 ──│  Router   │──> Internet │
│  │        │   (spoofed!)       │  (passes) │             │
│  └────────┘                    └──────────┘              │
│                                                          │
│  WITH BCP38:                                             │
│  ┌��───────┐                    ┌──────────┐              │
│  │ Host   │── src: 10.0.0.1 ──│  Router   │──x DROPPED  │
│  │        │   (not in range)   │  (checks) │             │
│  └────────┘                    └──────────┘              │
│                                                          │
│  Router only forwards packets with source IPs            │
│  belonging to its customer network (203.0.113.0/24)      │
└──────────────────────────────────────────────────────────┘
```

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
2. Use `dig` to measure response sizes for different query types (A, MX, TXT, ANY, DNSKEY)
3. Calculate the amplification factor for each query type
4. Verify your resolver is not open to external queries
5. Configure BIND to restrict recursion and enable RRL
6. Use Wireshark to capture and analyze DNS amplification traffic patterns
7. Set up a monitoring dashboard that alerts on anomalous DNS response volume

## Conclusion

DNS amplification attacks are a significant threat, as they can generate massive amounts of traffic with relatively little effort from the attacker. By securing DNS infrastructure, implementing DDoS mitigation strategies, and keeping systems up-to-date, organizations can protect themselves from these types of attacks and maintain the availability of their online services.
