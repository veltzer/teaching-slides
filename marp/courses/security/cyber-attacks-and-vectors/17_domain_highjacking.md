# Domain Hijacking: Protecting Your Online Identity

---
## What is Domain Hijacking

- Domain hijacking is the act of illegally transferring or redirecting a domain name to a different destination
- It involves the attacker gaining unauthorized control over a domain name and its associated web resources
- Can occur through various methods, such as social engineering, DNS cache poisoning, or exploiting vulnerabilities in domain registration systems
- One of the most damaging attacks for businesses, as it can intercept all web and email traffic

---
## Domain Hijacking vs DNS Hijacking

![domain_hijacking_vs_dns_hijacking](svg/courses/security/cyber-attacks-and-vectors/17_domain_highjacking/domain_hijacking_vs_dns_hijacking.svg)

---
## Types of Domain Hijacking

| Type                        | Method                                    | Difficulty |
|-----------------------------|-------------------------------------------|------------|
| Registrar Account Takeover  | Compromise registrar login credentials    | Medium     |
| Social Engineering          | Trick registrar support into transferring | Medium     |
| DNS Hijacking               | Modify DNS records at server level        | Medium     |
| Domain Slamming             | Unauthorized transfer to another registrar| Low        |
| Registry Hijacking          | Exploit vulnerabilities at registry level | High       |
| Expired Domain Takeover     | Register domains after they expire        | Low        |
| Subdomain Takeover          | Claim dangling DNS records                | Low        |

---
## Registrar Account Attacks

![registrar_account_attacks](svg/courses/security/cyber-attacks-and-vectors/17_domain_highjacking/registrar_account_attacks.svg)

- Weak passwords and lack of MFA on registrar accounts are the primary attack vector
- Once inside, attacker can change nameservers, transfer the domain, or modify contact info
- Changing the WHOIS email makes recovery extremely difficult

---
## DNS Hijacking Techniques

### 1. Local DNS Hijacking
- Malware modifies the victim's local DNS settings (`/etc/resolv.conf` or router config)
- All DNS queries from the victim go to attacker-controlled resolver

### 2. Router DNS Hijacking
- Attacker compromises home/office router (default credentials)
- Changes DHCP-provided DNS servers to malicious ones

### 3. Man-in-the-Middle DNS
- Attacker intercepts DNS queries on the network
- Responds with forged DNS answers before the legitimate server

### 4. Rogue DNS Server
- Attacker operates a DNS resolver that returns malicious results
- Users are tricked or configured to use it

```bash
# Check your current DNS resolver
cat /etc/resolv.conf
nslookup example.com
dig example.com +short

# Verify DNS responses from multiple resolvers
dig @8.8.8.8 example.com +short    # Google DNS
dig @1.1.1.1 example.com +short    # Cloudflare DNS
dig @9.9.9.9 example.com +short    # Quad9 DNS
# If results differ, something may be wrong
```

---
## Expired Domain Takeover

![expired_domain_takeover](svg/courses/security/cyber-attacks-and-vectors/17_domain_highjacking/expired_domain_takeover.svg)

**Why expired domains are valuable to attackers:**
- May still have backlinks and SEO authority
- Email sent to old addresses can be intercepted
- Subdomains of other sites may still point to the expired domain
- Existing trust relationships (SSL certificates, OAuth callbacks)

```bash
# Tools to find expiring domains
whois example.com | grep -i "expir"

# Domain drop catching services monitor expiring domains
# Attackers use these to grab high-value domains the moment they drop
```

---
## Subdomain Takeover

![subdomain_takeover](svg/courses/security/cyber-attacks-and-vectors/17_domain_highjacking/subdomain_takeover.svg)

**Vulnerable services for subdomain takeover:**

| Service          | DNS Record Type | Fingerprint (when unclaimed)     |
|------------------|-----------------|----------------------------------|
| GitHub Pages     | CNAME           | "There isn't a GitHub Pages site"|
| AWS S3           | CNAME           | "NoSuchBucket"                   |
| Heroku           | CNAME           | "No such app"                    |
| Azure            | CNAME           | "404 - Web Site is not found"    |
| Shopify          | CNAME           | "Sorry, this shop is not available"|
| Fastly           | CNAME           | "Fastly error: unknown domain"   |

---
## Detecting Subdomain Takeover Vulnerabilities

```bash
# Enumerate subdomains
subfinder -d example.com -o subdomains.txt

# Check for dangling CNAME records
while read sub; do
    cname=$(dig +short CNAME "$sub")
    if [ -n "$cname" ]; then
        # Check if the CNAME target resolves
        ip=$(dig +short "$cname")
        if [ -z "$ip" ]; then
            echo "[VULNERABLE] $sub -> $cname (dangling)"
        fi
    fi
done < subdomains.txt

# Tools specifically for subdomain takeover
# subjack - checks for subdomain takeover vulnerabilities
subjack -w subdomains.txt -t 100 -timeout 30 -ssl -v

# nuclei with takeover templates
nuclei -l subdomains.txt -t takeovers/
```

---
## Monitoring Tools and Services

| Tool / Service       | Type           | Purpose                              |
|----------------------|----------------|--------------------------------------|
| SecurityTrails       | Commercial     | Domain and DNS intelligence          |
| DNStwist             | Open Source    | Detect phishing/typosquatting domains|
| Whois History        | Commercial     | Track WHOIS record changes           |
| CertStream          | Open Source    | Monitor Certificate Transparency logs|
| domaincheck          | Open Source    | Domain expiration monitoring         |

```bash
# DNStwist: Find domains similar to yours (phishing/typosquat)
dnstwist --registered example.com

# Monitor Certificate Transparency for your domain
# (alerts when new SSL certs are issued for your domain)
curl -s "https://crt.sh/?q=%25.example.com&output=json" | \
    python3 -m json.tool

# Check WHOIS for recent changes
whois example.com | grep -E "Updated|Changed|Modified"

# Set up automated monitoring
# Monitor nameserver changes
dig NS example.com +short > /tmp/ns_current.txt
diff /tmp/ns_baseline.txt /tmp/ns_current.txt
```

---
## Domain Lock Features

### Registry Lock (Highest Protection)

```python
┌──────────────────────────────────────────────────────────┐
│          Domain Lock Levels                               │
│                                                          │
│  Level 1: Registrar Lock (clientTransferProhibited)      │
│  ├── Prevents unauthorized transfers between registrars  │
│  ├── Can be toggled from registrar control panel         │
│  └── Minimum recommended protection                     │
│                                                          │
│  Level 2: Registrar Update Lock (clientUpdateProhibited) │
│  ├── Prevents changes to domain data (nameservers, etc.) │
│  ├── Must contact registrar support to modify            │
│  └── Adds friction but significantly increases security  │
│                                                          │
│  Level 3: Registry Lock (serverTransferProhibited +      │
│           serverUpdateProhibited + serverDeleteProhibited)│
│  ├── Locked at the registry level (e.g., Verisign)       │
│  ├── Requires multi-party verification to unlock         │
│  ├── Most secure option available                        │
│  └── Recommended for mission-critical domains            │
└──────────────────────────────────────────────────────────┘
```

```bash
# Check current lock status of a domain
whois example.com | grep -i "status"
# Look for: clientTransferProhibited, serverTransferProhibited, etc.
```

---
## DNSSEC: DNS Security Extensions

![dnssec_dns_security_extensions](svg/courses/security/cyber-attacks-and-vectors/17_domain_highjacking/dnssec_dns_security_extensions.svg)

```bash
# Check if a domain has DNSSEC enabled
dig example.com +dnssec +short
dig DNSKEY example.com +short

# Validate DNSSEC chain
delv @8.8.8.8 example.com
# Should show "fully validated"

# Check DS records at parent zone
dig DS example.com @a.gtld-servers.net +short
```

---
## Defending Against Domain Hijacking

### Registrar Security Checklist

![registrar_security_checklist](svg/courses/security/cyber-attacks-and-vectors/17_domain_highjacking/registrar_security_checklist.svg)

---
## DNS Monitoring and Alerting

```bash
#!/bin/bash
# Simple DNS change monitoring script

DOMAIN="example.com"
BASELINE_NS="/var/lib/dns-monitor/ns_baseline.txt"
BASELINE_A="/var/lib/dns-monitor/a_baseline.txt"
LOG="/var/log/dns-monitor.log"

# Get current records
CURRENT_NS=$(dig NS "$DOMAIN" +short | sort)
CURRENT_A=$(dig A "$DOMAIN" +short | sort)

# Compare with baseline
if [ "$(cat $BASELINE_NS)" != "$CURRENT_NS" ]; then
    echo "$(date) ALERT: NS records changed for $DOMAIN" >> "$LOG"
    echo "Old: $(cat $BASELINE_NS)" >> "$LOG"
    echo "New: $CURRENT_NS" >> "$LOG"
    # Send alert (email, Slack, PagerDuty, etc.)
fi

if [ "$(cat $BASELINE_A)" != "$CURRENT_A" ]; then
    echo "$(date) ALERT: A records changed for $DOMAIN" >> "$LOG"
    echo "Old: $(cat $BASELINE_A)" >> "$LOG"
    echo "New: $CURRENT_A" >> "$LOG"
fi
```

---
## Real-World Domain Hijacking Incidents

| Incident                    | Year | Impact                                    |
|-----------------------------|------|-------------------------------------------|
| Panix.com hijacking         | 2005 | ISP domain transferred without consent    |
| CheckFree.com               | 2008 | Financial site redirected, malware served |
| Twitter DNS hijack          | 2009 | Iranian Cyber Army defaced Twitter        |
| Lenovo.com                  | 2015 | Domain redirected by Lizard Squad         |
| Brazilian bank hijack       | 2017 | All bank domains hijacked for 5 hours     |
| MyEtherWallet DNS hijack    | 2018 | BGP hijack to steal cryptocurrency        |
| Squarespace mass hijack     | 2024 | Domains migrated from Google Domains      |

---
## Incident Response for Domain Hijacking

1. **Detect**: Monitor for unauthorized DNS/WHOIS changes
2. **Verify**: Confirm the hijacking through multiple DNS resolvers
3. **Contact registrar**: Report unauthorized changes immediately
4. **Contact registry**: Escalate to the TLD registry if registrar is unresponsive
5. **Preserve evidence**: Screenshot WHOIS records, DNS responses, server logs
6. **Contact ICANN**: File a Transfer Dispute Resolution complaint
7. **Legal action**: Engage legal counsel for UDRP or court proceedings
8. **Notify users**: Warn users about potential phishing during hijacking period
9. **Post-incident**: Strengthen registrar security, enable registry lock

---
## Key Takeaways

- Domain hijacking can completely redirect your web and email traffic
- Registrar account security (strong passwords + MFA) is the first line of defense
- Domain locks (especially registry locks) prevent unauthorized changes
- DNSSEC prevents DNS response forgery but not registrar-level attacks
- Monitor your DNS records, WHOIS data, and certificate transparency logs
- Subdomain takeover is a commonly overlooked vulnerability
- Expired domains can be weaponized -- always set auto-renewal
- Have an incident response plan specific to domain hijacking scenarios
