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
1. **A02** - Cryptographic Failures
1. **A03** - Injection
1. **A04** - Insecure Design
1. **A05** - Security Misconfiguration
1. **A06** - Vulnerable & Outdated Components
1. **A07** - Identification & Authentication Failures
1. **A08** - Software & Data Integrity Failures
1. **A09** - Security Logging & Monitoring Failures
1. **A10** - Server-Side Request Forgery (`SSRF`)

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

<svg xmlns="http://www.w3.org/2000/svg" width="560" height="185" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>
  <!-- Row 1 boxes -->
  <rect x="10" y="20" width="155" height="45" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="87" y="47" text-anchor="middle" font-size="13" fill="#222222">Discover Vuln</text>
  <rect x="195" y="20" width="165" height="45" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="277" y="47" text-anchor="middle" font-size="13" fill="#222222">Report to Vendor</text>
  <rect x="390" y="20" width="155" height="45" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="467" y="47" text-anchor="middle" font-size="13" fill="#222222">Vendor Patches</text>
  <!-- Row 2 boxes -->
  <rect x="10" y="120" width="155" height="45" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="87" y="147" text-anchor="middle" font-size="13" fill="#222222">Public Disclosure</text>
  <rect x="195" y="120" width="165" height="45" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="277" y="147" text-anchor="middle" font-size="13" fill="#222222">Coordinate Date</text>
  <!-- Arrows row 1 -->
  <line x1="165" y1="42" x2="193" y2="42" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="360" y1="42" x2="388" y2="42" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- Vendor Patches down-left to Coordinate Date -->
  <path d="M 467,65 L 467,95 L 277,95 L 277,118" stroke="#555" stroke-width="1.5" fill="none" marker-end="url(#arr)"/>
  <!-- Coordinate Date left to Public Disclosure -->
  <line x1="195" y1="142" x2="167" y2="142" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
</svg>

- Typical disclosure timeline: **90 days**
- Bug bounty programs provide structured reporting
- `CVE` assignment for tracking vulnerabilities

---

## The CIA Triad in Web Context

<svg xmlns="http://www.w3.org/2000/svg" width="420" height="295" font-family="sans-serif">
  <!-- Triangle fill -->
  <polygon points="210,35 25,260 395,260" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <!-- Center label -->
  <text x="210" y="180" text-anchor="middle" font-size="14" fill="#333333">CIA Triad</text>
  <!-- Vertex labels -->
  <text x="210" y="25" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Confidentiality</text>
  <text x="25" y="285" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Integrity</text>
  <text x="395" y="285" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Availability</text>
</svg>

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

```misc
1. Recon          -->  Discover target, technologies, endpoints
1. Weaponize      -->  Craft payloads for identified vulns
1. Deliver        -->  Send exploit via HTTP request
1. Exploit        -->  Trigger the vulnerability
1. Install        -->  Deploy webshell or backdoor
1. Command & Ctrl -->  Establish persistent C2 channel
1. Exfiltrate     -->  Extract sensitive data
```

---

## Defense in Depth

<svg xmlns="http://www.w3.org/2000/svg" width="600" height="250" font-family="sans-serif">
  <!-- Outermost: Network Layer -->
  <rect x="10" y="10" width="580" height="230" rx="4" fill="#fff3e0" stroke="#333333" stroke-width="1.5"/>
  <text x="300" y="32" text-anchor="middle" font-size="13" fill="#222222">Network Layer (Firewall, IDS/IPS)</text>
  <!-- Transport Layer -->
  <rect x="30" y="47" width="540" height="175" rx="4" fill="#e8f5e9" stroke="#333333" stroke-width="1.5"/>
  <text x="300" y="69" text-anchor="middle" font-size="13" fill="#222222">Transport Layer (TLS, cert pinning)</text>
  <!-- Application Layer -->
  <rect x="50" y="84" width="500" height="120" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="300" y="106" text-anchor="middle" font-size="13" fill="#222222">Application Layer (WAF, validation)</text>
  <!-- Data Layer (innermost) -->
  <rect x="70" y="120" width="460" height="70" rx="4" fill="#f0f4f8" stroke="#333333" stroke-width="1.5"/>
  <text x="300" y="159" text-anchor="middle" font-size="13" fill="#222222">Data Layer (encryption, ACLs)</text>
</svg>

- No single control is sufficient
- Layers of defense create redundancy

---

## Web Application Architecture Overview

<svg xmlns="http://www.w3.org/2000/svg" width="680" height="120" font-family="sans-serif">
  <defs>
    <marker id="arr4" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>
  <!-- Box 1: Browser/Client -->
  <rect x="10" y="15" width="130" height="50" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="75" y="37" text-anchor="middle" font-size="13" fill="#222222">Browser /</text>
  <text x="75" y="53" text-anchor="middle" font-size="13" fill="#222222">Client</text>
  <!-- Box 2: Web Server -->
  <rect x="185" y="15" width="130" height="50" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="250" y="37" text-anchor="middle" font-size="13" fill="#222222">Web</text>
  <text x="250" y="53" text-anchor="middle" font-size="13" fill="#222222">Server</text>
  <!-- Box 3: App Server -->
  <rect x="360" y="15" width="130" height="50" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="425" y="37" text-anchor="middle" font-size="13" fill="#222222">App</text>
  <text x="425" y="53" text-anchor="middle" font-size="13" fill="#222222">Server</text>
  <!-- Box 4: Database Server -->
  <rect x="535" y="15" width="135" height="50" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="602" y="37" text-anchor="middle" font-size="13" fill="#222222">Database</text>
  <text x="602" y="53" text-anchor="middle" font-size="13" fill="#222222">Server</text>
  <!-- Arrows -->
  <line x1="140" y1="40" x2="183" y2="40" stroke="#555" stroke-width="1.5" marker-end="url(#arr4)"/>
  <line x1="315" y1="40" x2="358" y2="40" stroke="#555" stroke-width="1.5" marker-end="url(#arr4)"/>
  <line x1="490" y1="40" x2="533" y2="40" stroke="#555" stroke-width="1.5" marker-end="url(#arr4)"/>
  <!-- Sub-labels -->
  <text x="75" y="82" text-anchor="middle" font-size="11" fill="#555555">HTML/JS CSS</text>
  <text x="250" y="82" text-anchor="middle" font-size="11" fill="#555555">Nginx/Apache</text>
  <text x="425" y="82" text-anchor="middle" font-size="11" fill="#555555">Node/Java/Python/PHP</text>
  <text x="602" y="82" text-anchor="middle" font-size="11" fill="#555555">MySQL/PostgreSQL</text>
</svg>

- Each tier introduces potential attack vectors
- Trust boundaries exist between each component

---

## Common Vulnerability Lifecycle

1. **Introduction** - Developer writes vulnerable code
1. **Discovery** - Attacker or researcher finds the flaw
1. **Exploitation** - Vulnerability is actively exploited
1. **Disclosure** - Vulnerability is reported
1. **Patch** - Vendor releases a fix
1. **Deployment** - Organizations apply the patch

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

<svg xmlns="http://www.w3.org/2000/svg" width="500" height="380" font-family="sans-serif">
  <defs>
    <marker id="arr5" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>
  <!-- Boxes -->
  <rect x="90" y="15" width="270" height="42" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="225" y="41" text-anchor="middle" font-size="13" fill="#222222">Reconnaissance</text>
  <rect x="90" y="87" width="270" height="42" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="225" y="113" text-anchor="middle" font-size="13" fill="#222222">Enumeration &amp; Mapping</text>
  <rect x="90" y="159" width="270" height="42" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="225" y="185" text-anchor="middle" font-size="13" fill="#222222">Vulnerability Discovery</text>
  <rect x="90" y="231" width="270" height="42" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="225" y="257" text-anchor="middle" font-size="13" fill="#222222">Exploitation</text>
  <rect x="90" y="303" width="270" height="42" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="225" y="329" text-anchor="middle" font-size="13" fill="#222222">Reporting &amp; Remediation</text>
  <!-- Down arrows -->
  <line x1="225" y1="57" x2="225" y2="85" stroke="#555" stroke-width="1.5" marker-end="url(#arr5)"/>
  <line x1="225" y1="129" x2="225" y2="157" stroke="#555" stroke-width="1.5" marker-end="url(#arr5)"/>
  <line x1="225" y1="201" x2="225" y2="229" stroke="#555" stroke-width="1.5" marker-end="url(#arr5)"/>
  <line x1="225" y1="273" x2="225" y2="301" stroke="#555" stroke-width="1.5" marker-end="url(#arr5)"/>
  <!-- Iterate arrow: right side loop back to top -->
  <path d="M 360,324 L 430,324 L 430,36 L 362,36" stroke="#555" stroke-width="1.5" fill="none" marker-end="url(#arr5)"/>
  <!-- Iterate label -->
  <text transform="rotate(-90 450 183)" x="450" y="183" text-anchor="middle" font-size="12" fill="#555555">iterate</text>
</svg>

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

```misc
1. Executive Summary (1-2 pages)
   - Scope, timeline, overall risk rating
   - Critical findings in plain language

1. Methodology
   - Standards followed (OWASP, PTES, OSSTMM)
   - Tools used

1. Findings (per vulnerability)
   - Title, severity (CVSS), affected URL
   - Description, evidence, impact
   - Remediation recommendation

1. Appendices
   - Detailed scan output
   - Full request/response logs
   - Risk rating methodology
```

---

## CVSS Scoring for Pentesters

```misc
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

```misc
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
1. **Document everything** - Keep detailed notes and screenshots
1. **Think like an attacker** - Understand motivation and methodology
1. **Defend in depth** - No single fix is sufficient
1. **Automate wisely** - Tools assist, they don't replace thinking
1. **Stay current** - Threats evolve constantly
1. **Practice ethically** - Use only authorized targets

---

## Summary - Day 1 Opening

- Web applications are the #1 attack vector
- The OWASP Top 10 provides a prioritized risk list
- Legal authorization is **mandatory** before any testing
- Defense in depth is the only viable strategy
- We have powerful tools and legal practice environments
- This course will make you think like both attacker and defender

> Next: Server Platforms & Web Technologies
