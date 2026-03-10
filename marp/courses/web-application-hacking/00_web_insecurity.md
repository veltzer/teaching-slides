---
marp: true
theme: default
paginate: true
---

# Web Application (In)security

## Understanding the Modern Threat Landscape

---

## Course Overview

- 5-day intensive Web Application Hacking course
- Focus on **authorized** penetration testing techniques
- Every attack paired with **defense and mitigation**
- Hands-on labs and a final CTF exercise
- Goal: Think like an attacker, defend like a professional

---

## Why Web Application Security Matters

- Over **70%** of breaches involve web applications (Verizon DBIR)
- Web apps are the **primary attack surface** for most organizations
- Average cost of a data breach: **$4.45 million** (IBM 2023)
- Regulatory compliance: `GDPR`, `PCI-DSS`, `HIPAA`, `SOX`
- Reputational damage is often irreversible

---

## The Evolution of Web Attacks

| Era | Primary Attacks | Defenses |
|-----|----------------|----------|
| 1990s | Simple defacement | Firewalls |
| 2000s | `SQL injection`, `XSS` | WAFs, input validation |
| 2010s | API attacks, logic flaws | DevSecOps, SAST/DAST |
| 2020s | Supply chain, `SSRF`, deserialization | Zero Trust, shift-left |

---

## OWASP Top 10 (2021)

1. **A01** - Broken Access Control
2. **A02** - Cryptographic Failures
3. **A03** - Injection
4. **A04** - Insecure Design
5. **A05** - Security Misconfiguration
6. **A06** - Vulnerable & Outdated Components
7. **A07** - Identification & Authentication Failures
8. **A08** - Software & Data Integrity Failures
9. **A09** - Security Logging & Monitoring Failures
10. **A10** - Server-Side Request Forgery (`SSRF`)

---

## The Attacker's Mindset

- **Reconnaissance** - Gather information before attacking
- **Enumeration** - Map the attack surface thoroughly
- **Exploitation** - Leverage vulnerabilities found
- **Post-exploitation** - Escalate privileges, pivot
- **Persistence** - Maintain access
- **Covering tracks** - Clean up evidence

> "Defenders must be right every time. Attackers only need to be right once."

---

## Legal & Ethical Framework

- **ALWAYS** obtain written authorization before testing
- Scope definition is critical - what is in/out of scope
- Rules of engagement: testing windows, methods allowed
- Emergency contacts and escalation procedures
- Report all findings responsibly
- **Never** test systems you do not have permission to test

---

## Responsible Disclosure

```text
+------------------+     +------------------+     +------------------+
|  Discover Vuln   | --> |  Report to Vendor| --> |  Vendor Patches  |
+------------------+     +------------------+     +------------------+
                                                          |
+------------------+     +------------------+             |
| Public Disclosure| <-- |  Coordinate Date | <-----------+
+------------------+     +------------------+
```

- Typical disclosure timeline: **90 days**
- Bug bounty programs provide structured reporting
- `CVE` assignment for tracking vulnerabilities

---

## The CIA Triad in Web Context

```text
           Confidentiality
               /\
              /  \
             /    \
            / CIA  \
           /  Triad \
          /----------\
  Integrity          Availability
```

- **Confidentiality**: Prevent unauthorized data access (`SQL injection`, data leaks)
- **Integrity**: Prevent unauthorized data modification (`XSS`, `CSRF`)
- **Availability**: Prevent service disruption (`DoS`, resource exhaustion)

---

## Attack Categories

| Category | Examples |
|----------|----------|
| **Injection** | `SQL injection`, `XSS`, `OS command injection` |
| **Broken Auth** | Credential stuffing, session hijacking |
| **Data Exposure** | Sensitive data in responses, weak crypto |
| **Access Control** | `IDOR`, privilege escalation |
| **Misconfig** | Default creds, verbose errors, open buckets |
| **Logic Flaws** | Business logic bypass, race conditions |

---

## The Kill Chain - Web Edition

```text
1. Recon          -->  Discover target, technologies, endpoints
2. Weaponize      -->  Craft payloads for identified vulns
3. Deliver        -->  Send exploit via HTTP request
4. Exploit        -->  Trigger the vulnerability
5. Install        -->  Deploy webshell or backdoor
6. Command & Ctrl -->  Establish persistent C2 channel
7. Exfiltrate     -->  Extract sensitive data
```

---

## Defense in Depth

```text
+-----------------------------------------------+
|  Network Layer  (Firewall, IDS/IPS)           |
|  +-------------------------------------------+|
|  |  Transport Layer  (TLS, cert pinning)     ||
|  |  +---------------------------------------+||
|  |  |  Application Layer  (WAF, validation) |||
|  |  |  +-----------------------------------+|||
|  |  |  |  Data Layer  (encryption, ACLs)   ||||
|  |  |  +-----------------------------------+|||
|  |  +---------------------------------------+||
|  +-------------------------------------------+|
+-----------------------------------------------+
```

- No single control is sufficient
- Layers of defense create redundancy

---

## Web Application Architecture Overview

```text
+--------+     +--------+     +-----------+     +----------+
| Browser| --> | Web    | --> | App       | --> | Database |
| Client |     | Server |     | Server    |     | Server   |
+--------+     +--------+     +-----------+     +----------+
    |              |               |                  |
  HTML/JS       Nginx/          Node/Java/         MySQL/
  CSS           Apache          Python/PHP         PostgreSQL
```

- Each tier introduces potential attack vectors
- Trust boundaries exist between each component

---

## Common Vulnerability Lifecycle

1. **Introduction** - Developer writes vulnerable code
2. **Discovery** - Attacker or researcher finds the flaw
3. **Exploitation** - Vulnerability is actively exploited
4. **Disclosure** - Vulnerability is reported
5. **Patch** - Vendor releases a fix
6. **Deployment** - Organizations apply the patch

> The window between steps 3 and 6 is the **danger zone**

---

## Setting Up Your Testing Environment

- **Kali Linux** - Primary pentesting OS
- **Burp Suite** - Web proxy and scanner
- **OWASP ZAP** - Free alternative proxy
- **Browser DevTools** - Built-in inspection
- **Docker** - For running vulnerable apps
- **VPN** - For lab connectivity

```bash
# Quick setup check
which burpsuite && echo "Burp Suite installed"
which zaproxy && echo "ZAP installed"
which sqlmap && echo "sqlmap installed"
```

---

## Practice Targets (Legal!)

| Target | Description |
|--------|-------------|
| **DVWA** | Damn Vulnerable Web Application |
| **WebGoat** | OWASP training application |
| **Juice Shop** | Modern `JavaScript` app with vulns |
| **HackTheBox** | Online pentesting labs |
| **TryHackMe** | Guided hacking exercises |
| **PortSwigger Academy** | Free web security training |

```bash
# Start DVWA in Docker
docker run -d -p 8080:80 vulnerables/web-dvwa
```

---

## What We Will Cover

| Day | Topics |
|-----|--------|
| **Day 1** | Web (In)security, Mapping, Reconnaissance |
| **Day 2** | Authentication, Sessions, SQL Injection basics |
| **Day 3** | Advanced SQL Injection, XSS |
| **Day 4** | Back-end Attacks, Logic Flaws, Hardening |
| **Day 5** | Boot2Root, CTF, Putting It All Together |

---

## Security Testing Methodology

```text
+---> Reconnaissance
|         |
|         v
|    Enumeration & Mapping
|         |
|         v
|    Vulnerability Discovery
|         |
|         v
|    Exploitation
|         |
|         v
|    Reporting & Remediation
|         |
+---------+  (iterate)
```

---

## Types of Security Testing

| Type | Description | Approach |
|------|------------|----------|
| **Black Box** | No prior knowledge | Simulates external attacker |
| **Gray Box** | Partial knowledge (creds, docs) | Most common pentest |
| **White Box** | Full source code access | Code review + testing |
| **Red Team** | Adversarial simulation | Full-scope, stealth |
| **Bug Bounty** | Crowdsourced testing | Public programs |

---

## Penetration Testing Report Structure

```text
1. Executive Summary (1-2 pages)
   - Scope, timeline, overall risk rating
   - Critical findings in plain language

2. Methodology
   - Standards followed (OWASP, PTES, OSSTMM)
   - Tools used

3. Findings (per vulnerability)
   - Title, severity (CVSS), affected URL
   - Description, evidence, impact
   - Remediation recommendation

4. Appendices
   - Detailed scan output
   - Full request/response logs
   - Risk rating methodology
```

---

## CVSS Scoring for Pentesters

```text
Common Vulnerability Scoring System (CVSS v3.1)

Score Range -> Severity
0.0          None
0.1 - 3.9    Low
4.0 - 6.9    Medium
7.0 - 8.9    High
9.0 - 10.0   Critical

Base Metrics:
  Attack Vector:    Network / Adjacent / Local / Physical
  Attack Complexity: Low / High
  Privileges Required: None / Low / High
  User Interaction:  None / Required
  Scope:            Unchanged / Changed
  Confidentiality:  None / Low / High
  Integrity:        None / Low / High
  Availability:     None / Low / High

Calculator: https://www.first.org/cvss/calculator/3.1
```

---

## Real-World Breach Case Studies

```text
Equifax (2017) - 147 million records
  Vulnerability: Apache Struts RCE (CVE-2017-5638)
  Root cause: Unpatched server for 2 months
  Lesson: Patch management is critical

Capital One (2019) - 106 million records
  Vulnerability: SSRF via misconfigured WAF
  Root cause: Overprivileged IAM role + SSRF
  Lesson: Least privilege + SSRF prevention

SolarWinds (2020) - 18,000+ organizations
  Vulnerability: Supply chain attack
  Root cause: Compromised build system
  Lesson: Supply chain security matters

MOVEit (2023) - 2,000+ organizations
  Vulnerability: SQL injection (CVE-2023-34362)
  Root cause: Unpatched file transfer software
  Lesson: Even simple vulns have massive impact
```

---

## Key Principles for This Course

1. **Never test without authorization** - Always have written permission
2. **Document everything** - Keep detailed notes and screenshots
3. **Think like an attacker** - Understand motivation and methodology
4. **Defend in depth** - No single fix is sufficient
5. **Automate wisely** - Tools assist, they don't replace thinking
6. **Stay current** - Threats evolve constantly
7. **Practice ethically** - Use only authorized targets

---

## Summary - Day 1 Opening

- Web applications are the #1 attack vector
- The OWASP Top 10 provides a prioritized risk list
- Legal authorization is **mandatory** before any testing
- Defense in depth is the only viable strategy
- We have powerful tools and legal practice environments
- This course will make you think like both attacker and defender

> Next: Server Platforms & Web Technologies
