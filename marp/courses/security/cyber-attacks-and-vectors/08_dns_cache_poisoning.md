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

<svg xmlns="http://www.w3.org/2000/svg" width="780" height="310" font-family="sans-serif">
<defs>
  <marker id="arr"  markerWidth="10" markerHeight="7" refX="9"   refY="3.5" orient="auto">
    <polygon points="0 0,10 3.5,0 7" fill="#555"/>
  </marker>
  <marker id="arrl" markerWidth="10" markerHeight="7" refX="1"   refY="3.5" orient="auto">
    <polygon points="10 0,0 3.5,10 7" fill="#555"/>
  </marker>
</defs>
<text x="390" y="22" text-anchor="middle" font-size="14" fill="#222222" font-weight="bold">DNS Resolution Chain</text>
<rect x="10" y="40" width="150" height="60" fill="#fff3e0" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="85" y="66" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">Client</text>
<text x="85" y="86" text-anchor="middle" font-size="12" fill="#222222">Browser</text>
<rect x="175" y="40" width="150" height="60" fill="#e3f2fd" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="250" y="66" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">Recursive</text>
<text x="250" y="86" text-anchor="middle" font-size="12" fill="#222222">Resolver</text>
<rect x="375" y="40" width="150" height="60" fill="#e8f5e9" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="450" y="66" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">Root DNS</text>
<text x="450" y="86" text-anchor="middle" font-size="12" fill="#222222">Server</text>
<rect x="575" y="40" width="150" height="60" fill="#e8f5e9" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="650" y="66" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">TLD DNS</text>
<text x="650" y="86" text-anchor="middle" font-size="12" fill="#222222">Server</text>
<line x1="160" y1="60" x2="175" y2="60" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<line x1="325" y1="60" x2="375" y2="60" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<line x1="525" y1="60" x2="575" y2="60" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<line x1="575" y1="80" x2="525" y2="80" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<line x1="375" y1="80" x2="325" y2="80" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<line x1="175" y1="80" x2="160" y2="80" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<rect x="575" y="160" width="150" height="60" fill="#fce4ec" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="650" y="186" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">Authoritative</text>
<text x="650" y="204" text-anchor="middle" font-size="12" fill="#222222">DNS Server</text>
<line x1="650" y1="100" x2="650" y2="160" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<line x1="575" y1="190" x2="325" y2="70" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<rect x="175" y="175" width="150" height="70" fill="#e3f2fd" stroke="#1565c0" stroke-width="1.5" rx="4"/>
<text x="250" y="195" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">DNS Cache</text>
<text x="250" y="213" text-anchor="middle" font-size="11" fill="#1565c0">example.com</text>
<text x="250" y="231" text-anchor="middle" font-size="11" fill="#1565c0">= 93.184.x.x</text>
<line x1="250" y1="100" x2="250" y2="175" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<text x="190" y="163" text-anchor="start" font-size="10" fill="#555" font-style="italic">cached for TTL</text>
</svg>

---

## Kaminsky Attack (2008)

The most famous DNS cache poisoning technique, discovered by Dan Kaminsky:

<svg xmlns="http://www.w3.org/2000/svg" width="700" height="400" font-family="sans-serif">
<defs>
  <marker id="arr"  markerWidth="10" markerHeight="7" refX="9"   refY="3.5" orient="auto">
    <polygon points="0 0,10 3.5,0 7" fill="#555"/>
  </marker>
  <marker id="arrl" markerWidth="10" markerHeight="7" refX="1"   refY="3.5" orient="auto">
    <polygon points="10 0,0 3.5,10 7" fill="#555"/>
  </marker>
</defs>
<text x="350" y="22" text-anchor="middle" font-size="14" fill="#222222" font-weight="bold">Kaminsky DNS Cache Poisoning Attack</text>
<rect x="10" y="38" width="680" height="352" fill="#fff8e1" stroke="#f9a825" stroke-width="1.5" rx="4"/>
<text x="22" y="65" text-anchor="start" font-size="13" fill="#e65100" font-weight="bold">1.</text>
<text x="55" y="65" text-anchor="start" font-size="12" fill="#222222">Attacker queries resolver for random.example.com</text>
<text x="55" y="83" text-anchor="start" font-size="11" fill="#555">(a subdomain that does NOT exist in cache)</text>
<text x="22" y="111" text-anchor="start" font-size="13" fill="#e65100" font-weight="bold">2.</text>
<text x="55" y="111" text-anchor="start" font-size="12" fill="#222222">Resolver sends query to authoritative server for example.com</text>
<text x="22" y="139" text-anchor="start" font-size="13" fill="#e65100" font-weight="bold">3.</text>
<text x="55" y="139" text-anchor="start" font-size="12" fill="#222222">Before real response arrives, attacker floods resolver with</text>
<text x="55" y="157" text-anchor="start" font-size="11" fill="#555">FORGED responses: matching Transaction ID + authority ns1.example.com = EVIL_IP</text>
<text x="22" y="185" text-anchor="start" font-size="13" fill="#e65100" font-weight="bold">4.</text>
<text x="55" y="185" text-anchor="start" font-size="12" fill="#222222">If forged response arrives FIRST and ID matches:</text>
<text x="55" y="203" text-anchor="start" font-size="11" fill="#555">Resolver caches:  example.com NS  →  EVIL_IP</text>
<text x="22" y="231" text-anchor="start" font-size="13" fill="#e65100" font-weight="bold">5.</text>
<text x="55" y="231" text-anchor="start" font-size="12" fill="#222222">ALL future queries for *.example.com are redirected to attacker!</text>
<text x="22" y="259" text-anchor="start" font-size="13" fill="#e65100" font-weight="bold">Key:</text>
<text x="55" y="259" text-anchor="start" font-size="12" fill="#222222">Attacker retries with different random subdomains until one succeeds</text>
<text x="55" y="277" text-anchor="start" font-size="11" fill="#555">— thousands of attempts possible per second</text>
</svg>

---

## Transaction ID Vulnerability

<svg xmlns="http://www.w3.org/2000/svg" width="580" height="260" font-family="sans-serif">
<defs>
  <marker id="arr"  markerWidth="10" markerHeight="7" refX="9"   refY="3.5" orient="auto">
    <polygon points="0 0,10 3.5,0 7" fill="#555"/>
  </marker>
  <marker id="arrl" markerWidth="10" markerHeight="7" refX="1"   refY="3.5" orient="auto">
    <polygon points="10 0,0 3.5,10 7" fill="#555"/>
  </marker>
</defs>
<rect x="10" y="10" width="560" height="240" fill="#e3f2fd" stroke="#1565c0" stroke-width="1.5" rx="4"/>
<text x="290" y="36" text-anchor="middle" font-size="14" fill="#0d47a1" font-weight="bold">DNS Transaction ID Security Analysis</text>
<text x="22" y="68" text-anchor="start" font-size="12" fill="#1565c0" font-weight="bold">Transaction ID field:</text>
<text x="562" y="68" text-anchor="end" font-size="12" fill="#222">16-bit → only 65,536 possible values</text>
<text x="22" y="98" text-anchor="start" font-size="12" fill="#1565c0" font-weight="bold">Birthday paradox:</text>
<text x="562" y="98" text-anchor="end" font-size="12" fill="#222">~250 random attempts for 50% collision chance</text>
<text x="22" y="128" text-anchor="start" font-size="12" fill="#1565c0" font-weight="bold">Predictable source port:</text>
<text x="562" y="128" text-anchor="end" font-size="12" fill="#222">Attack becomes trivially easy</text>
<text x="22" y="158" text-anchor="start" font-size="12" fill="#1565c0" font-weight="bold">Source port randomization:</text>
<text x="562" y="158" text-anchor="end" font-size="12" fill="#222">Adds 16 more bits = 2^32 combinations</text>
<text x="22" y="188" text-anchor="start" font-size="12" fill="#1565c0" font-weight="bold">DNSSEC (full fix):</text>
<text x="562" y="188" text-anchor="end" font-size="12" fill="#222">Cryptographic signatures — forgery is infeasible</text>
</svg>

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

<svg xmlns="http://www.w3.org/2000/svg" width="680" height="510" font-family="sans-serif">
<defs>
  <marker id="arr"  markerWidth="10" markerHeight="7" refX="9"   refY="3.5" orient="auto">
    <polygon points="0 0,10 3.5,0 7" fill="#555"/>
  </marker>
  <marker id="arrl" markerWidth="10" markerHeight="7" refX="1"   refY="3.5" orient="auto">
    <polygon points="10 0,0 3.5,10 7" fill="#555"/>
  </marker>
</defs>
<text x="340" y="22" text-anchor="middle" font-size="14" fill="#222222" font-weight="bold">DNSSEC Chain of Trust</text>
<rect x="80" y="40" width="520" height="90" fill="#fff3e0" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="340" y="62" text-anchor="middle" font-size="13" fill="#e65100" font-weight="bold">Root Zone (.)</text>
<text x="340" y="82" text-anchor="middle" font-size="11" fill="#333">KSK signs ZSK</text>
<text x="340" y="100" text-anchor="middle" font-size="11" fill="#333">ZSK signs .com DS record</text>
<line x1="340" y1="130" x2="340" y2="166" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<text x="348" y="152" text-anchor="start" font-size="10" fill="#555" font-style="italic">DS record points to</text>
<rect x="80" y="170" width="520" height="90" fill="#e3f2fd" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="340" y="192" text-anchor="middle" font-size="13" fill="#1565c0" font-weight="bold">.com TLD</text>
<text x="340" y="212" text-anchor="middle" font-size="11" fill="#333">KSK signs ZSK</text>
<text x="340" y="230" text-anchor="middle" font-size="11" fill="#333">ZSK signs example.com DS record</text>
<line x1="340" y1="260" x2="340" y2="296" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<text x="348" y="282" text-anchor="start" font-size="10" fill="#555" font-style="italic">DS record points to</text>
<rect x="80" y="300" width="520" height="90" fill="#e8f5e9" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="340" y="322" text-anchor="middle" font-size="13" fill="#2e7d32" font-weight="bold">example.com</text>
<text x="340" y="342" text-anchor="middle" font-size="11" fill="#333">KSK signs ZSK</text>
<text x="340" y="360" text-anchor="middle" font-size="11" fill="#333">ZSK signs A records</text>
<text x="340" y="378" text-anchor="middle" font-size="11" fill="#333">RRSIG = cryptographic signature</text>
<rect x="80" y="440" width="520" height="60" fill="#f5f5f5" stroke="#bbb" stroke-width="1.5" rx="4"/>
<text x="90" y="458" text-anchor="start" font-size="11" fill="#1a1a2e" font-weight="bold">KSK</text>
<text x="128" y="458" text-anchor="start" font-size="11" fill="#444">= Key Signing Key — signs the Zone Signing Key</text>
<text x="90" y="476" text-anchor="start" font-size="11" fill="#1a1a2e" font-weight="bold">ZSK</text>
<text x="128" y="476" text-anchor="start" font-size="11" fill="#444">= Zone Signing Key — signs zone records (A, MX…)</text>
<text x="90" y="494" text-anchor="start" font-size="11" fill="#1a1a2e" font-weight="bold">DS</text>
<text x="128" y="494" text-anchor="start" font-size="11" fill="#444">= Delegation Signer — fingerprint of child's KSK in parent zone</text>
</svg>

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
