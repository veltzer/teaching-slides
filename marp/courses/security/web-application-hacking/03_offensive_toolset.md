# Offensive Toolset & Practice Targets

## Building Your Pentesting Arsenal

---

## The Pentester's Toolkit Overview

```text
+--Reconnaissance---+  +---Scanning------+  +---Exploitation--+
| Burp Suite        |  | Nmap            |  | sqlmap          |
| OWASP ZAP         |  | Nikto           |  | Metasploit      |
| Browser DevTools   |  | dirb/gobuster   |  | Commix          |
| curl / httpie      |  | wfuzz           |  | BeEF            |
| Recon-ng           |  | Nuclei          |  | XSStrike        |
+-------------------+  +-----------------+  +-----------------+
```

---

## Burp Suite - The Swiss Army Knife

- **Proxy** - Intercept and modify requests
- **Scanner** - Automated vulnerability detection (Pro)
- **Repeater** - Manually modify and resend requests
- **Intruder** - Automated fuzzing and brute-forcing
- **Decoder** - Encode/decode data
- **Comparer** - Diff responses
- **Sequencer** - Analyze token randomness
- **Extender** - Plugin ecosystem

---

## Burp Suite - Proxy Setup

```text
Browser Configuration:
  Proxy: 127.0.0.1
  Port:  8080

Burp CA Certificate:
  1. Navigate to http://burp
  2. Download CA certificate
  3. Import into browser trust store

Firefox:
  Settings -> Privacy -> Certificates -> Import

Chrome:
  Settings -> Security -> Manage Certificates -> Import
```

---

## Burp Suite - Intercepting Requests

```http
# Intercepted POST request
POST /api/login HTTP/1.1
Host: target.com
Content-Type: application/json
Cookie: session=abc123

{"username":"admin","password":"password123"}

# You can modify ANY part before forwarding:
# - Headers (cookies, auth tokens)
# - URL parameters
# - Request body
# - HTTP method
```

---

## Burp Suite - Repeater Usage

```text
1. Right-click request in Proxy -> Send to Repeater
2. Modify the request as needed
3. Click "Send" to get the response
4. Compare responses to identify behavior changes

Example: Testing for SQL injection
Original:  username=admin&password=test
Modified:  username=admin'&password=test
Modified:  username=admin' OR '1'='1&password=test
Modified:  username=admin'--&password=test
```

---

## Burp Suite - Intruder Attack Types

| Attack Type | Use Case |
|------------|----------|
| **Sniper** | One payload position at a time |
| **Battering Ram** | Same payload in all positions |
| **Pitchfork** | Different payload lists, parallel |
| **Cluster Bomb** | All combinations of payloads |

```text
# Sniper example - brute force password
POST /login
username=admin&password=§PAYLOAD§

Payload list: rockyou.txt (top 1000)
```

---

## Burp Suite - Useful Extensions

| Extension | Purpose |
|-----------|---------|
| **Autorize** | Access control testing |
| **Logger++** | Enhanced logging |
| **JSON Beautifier** | Format JSON responses |
| **JWT Editor** | Manipulate JWT tokens |
| **Param Miner** | Discover hidden parameters |
| **Active Scan++** | Enhanced scanning |
| **Backslash Powered Scanner** | Novel injection detection |
| **Turbo Intruder** | High-speed fuzzing |

---

## OWASP ZAP - Free Alternative

```bash
# Start ZAP
zaproxy

# ZAP API for automation
# Start an active scan
curl "http://localhost:8080/JSON/ascan/action/scan/\
?url=http://target.com&recurse=true"

# Get scan results
curl "http://localhost:8080/JSON/core/view/alerts/\
?baseurl=http://target.com"

# ZAP CLI automation
zap-cli quick-scan http://target.com
zap-cli active-scan http://target.com
zap-cli alerts
```

---

## Browser Developer Tools

```text
F12 or Ctrl+Shift+I to open DevTools

Key tabs for pentesting:
- Network:    Monitor all HTTP requests/responses
- Console:    Execute JavaScript, see errors
- Elements:   Inspect/modify DOM in real-time
- Application: View cookies, localStorage, sessionStorage
- Sources:    Debug JavaScript, find source maps

Useful Console commands:
> document.cookie           // View cookies
> localStorage              // View local storage
> JSON.parse(atob('...'))   // Decode JWT payload
```

---

## curl - Command Line HTTP Client

```bash
# Basic GET request
curl https://target.com

# POST with data
curl -X POST -d "user=admin&pass=test" https://target.com/login

# Custom headers
curl -H "Authorization: Bearer TOKEN" https://target.com/api

# Follow redirects, show headers
curl -L -v https://target.com

# Send JSON
curl -X POST -H "Content-Type: application/json" \
  -d '{"user":"admin"}' https://target.com/api

# Save response with headers
curl -D headers.txt -o response.html https://target.com
```

---

## Nmap - Network Scanner

```bash
# Basic port scan
nmap -sV target.com

# Web-focused scan
nmap -sV -p 80,443,8080,8443 target.com

# HTTP enumeration scripts
nmap --script http-enum -p 80 target.com
nmap --script http-headers -p 80 target.com
nmap --script http-methods -p 80 target.com

# Aggressive web scan
nmap -sV --script "http-*" -p 80,443 target.com

# Vulnerability scan
nmap --script vuln -p 80,443 target.com
```

---

## Nikto - Web Server Scanner

```bash
# Basic scan
nikto -h https://target.com

# Scan specific port
nikto -h target.com -p 8080

# Use specific tuning
# 1=Interesting File  2=Misconfig  3=Info Disclosure
# 4=Injection         5=Remote File Retrieval
# 6=Denial of Service 7=Remote Source Inclusion
# 8=Command Execution 9=SQL Injection
nikto -h target.com -Tuning 1234

# Save output
nikto -h target.com -o report.html -Format htm
```

---

## Directory & File Discovery Tools

```bash
# gobuster - fast directory brute-forcing
gobuster dir -u https://target.com \
  -w /usr/share/wordlists/dirb/common.txt \
  -x php,html,txt,bak \
  -t 50

# dirb - classic directory scanner
dirb https://target.com /usr/share/wordlists/dirb/common.txt

# ffuf - fast fuzzer
ffuf -u https://target.com/FUZZ \
  -w /usr/share/wordlists/dirb/common.txt \
  -mc 200,301,302,403

# dirsearch - Python-based
dirsearch -u https://target.com -e php,asp,aspx,jsp
```

---

## ffuf - Advanced Fuzzing

```bash
# Fuzz GET parameters
ffuf -u "https://target.com/page?FUZZ=test" \
  -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt

# Fuzz POST data
ffuf -u https://target.com/login \
  -X POST -d "username=admin&password=FUZZ" \
  -w /usr/share/wordlists/rockyou.txt \
  -fc 401

# Fuzz headers
ffuf -u https://target.com/api \
  -H "X-Custom-Header: FUZZ" \
  -w wordlist.txt

# Virtual host discovery
ffuf -u https://target.com \
  -H "Host: FUZZ.target.com" \
  -w subdomains.txt -fc 302
```

---

## sqlmap - SQL Injection Automation

```bash
# Basic test
sqlmap -u "https://target.com/page?id=1" --batch

# Test POST parameter
sqlmap -u "https://target.com/login" \
  --data="username=admin&password=test" -p username

# Dump database
sqlmap -u "https://target.com/page?id=1" \
  --dbs --batch

# Use with Burp request file
sqlmap -r request.txt --batch

# Bypass WAF
sqlmap -u "https://target.com/page?id=1" \
  --tamper=space2comment,between --random-agent
```

---

## Nuclei - Template-Based Scanner

```bash
# Update templates
nuclei -update-templates

# Basic scan
nuclei -u https://target.com

# Scan with specific templates
nuclei -u https://target.com -t cves/
nuclei -u https://target.com -t exposures/
nuclei -u https://target.com -t misconfiguration/

# Scan list of URLs
nuclei -l urls.txt -t technologies/

# Filter by severity
nuclei -u https://target.com -severity critical,high
```

---

## Wordlists - Essential Resources

```bash
# SecLists - The ultimate collection
git clone https://github.com/danielmiessler/SecLists

# Key wordlists:
# Discovery/Web-Content/
#   common.txt            - Common directories/files
#   directory-list-2.3-medium.txt - Larger list
#   raft-large-words.txt  - RAFT project words
#
# Passwords/
#   rockyou.txt           - Classic password list
#   darkweb2017-top10000.txt
#
# Fuzzing/
#   special-chars.txt     - Special characters
#   SQLi/                 - SQL injection payloads
#   XSS/                  - XSS payloads

# Kali default location
ls /usr/share/wordlists/
ls /usr/share/seclists/
```

---

## Setting Up DVWA

```bash
# Docker method (recommended)
docker run -d -p 8080:80 \
  --name dvwa vulnerables/web-dvwa

# Access: http://localhost:8080
# Default login: admin / password
# Setup: Click "Create / Reset Database"

# Security levels:
# Low      -> No protection (learn the basics)
# Medium   -> Some protection (learn bypasses)
# High     -> Strong protection (advanced techniques)
# Impossible -> Properly secured (see correct code)
```

---

## Setting Up OWASP Juice Shop

```bash
# Docker method
docker run -d -p 3000:3000 \
  --name juiceshop bkimminich/juice-shop

# Access: http://localhost:3000
# Features:
# - Modern SPA (Angular + Node.js)
# - Score board tracks challenges
# - 100+ challenges at varying difficulty
# - REST API with Swagger docs
# - Covers OWASP Top 10

# Access score board:
# http://localhost:3000/#/score-board
```

---

## Setting Up WebGoat

```bash
# Docker method
docker run -d -p 8081:8080 -p 9090:9090 \
  --name webgoat webgoat/webgoat

# Access WebGoat: http://localhost:8081/WebGoat
# Access WebWolf: http://localhost:9090/WebWolf

# Features:
# - Guided lessons with explanations
# - Interactive exercises
# - Covers injection, authentication, XSS, etc.
# - Hints available for each lesson
# - Built-in solution verification
```

---

## Lab Environment Architecture

```text
+--Your Machine (Kali/Host)--+
|                             |
| Browser -> Burp Suite -+   |
|                         |   |
| Terminal (curl, nmap)   |   |
|                         |   |
+-----------+-------------+   |
            |                 |
            v                 |
+--Docker Network-------------+
|                              |
| DVWA        :8080            |
| Juice Shop  :3000            |
| WebGoat     :8081            |
| Custom Labs :various         |
+------------------------------+
```

---

## Methodology: The Testing Workflow

```text
1. Configure proxy (Burp Suite)
2. Browse the application manually
3. Review site map and identify entry points
4. Run automated scanners (Nikto, Nuclei)
5. Perform directory/file discovery
6. Test each entry point manually:
   a. Input validation flaws
   b. Authentication/authorization
   c. Business logic
   d. Error handling
7. Exploit confirmed vulnerabilities
8. Document and report findings
```

---

## Burp Suite Macros and Session Handling

```text
Session Handling Rules allow Burp to maintain
authenticated sessions during scanning/fuzzing:

1. Project Options -> Sessions -> Session Handling Rules
2. Add rule -> Check session is valid
3. Define macro to re-authenticate if session expires

Macros:
- Record a login sequence (POST /login)
- Burp replays it when session expires
- Extracts CSRF tokens automatically

Use cases:
- Scanning authenticated areas
- Fuzzing behind login pages
- Testing multi-step workflows
- Handling anti-CSRF tokens

Configuration:
- Scope: Define which tools use the rule
- Conditions: When to check session validity
- Actions: Run macro, update cookies
```

---

## Reporting and Evidence Collection

```bash
# Good evidence collection is critical for reports

# Screenshots - use flameshot or gnome-screenshot
flameshot gui           # Interactive screenshot tool

# HTTP evidence - save requests/responses from Burp
# Right-click in Proxy/Repeater -> Copy to file

# Terminal logging
script -a session.log   # Record terminal session
# or use tmux logging:
# tmux: Ctrl+B, then :pipe-pane 'cat >> session.log'

# Automated reporting
# Burp Suite: Generate report (HTML/XML)
# ZAP: Report -> Generate HTML Report
# Nmap: -oA flag saves in all formats

# Evidence for each finding:
# 1. Screenshot of the vulnerability
# 2. Full HTTP request that triggers it
# 3. Full HTTP response showing the impact
# 4. Steps to reproduce (numbered list)
# 5. Proof of concept (working payload)
```

---

## Lab Exercise: Tool Setup & Verification

**Tasks**:
1. Start Burp Suite and configure browser proxy
2. Launch DVWA container and log in
3. Browse DVWA through Burp and examine traffic
4. Use Burp Repeater to modify a request
5. Run `nikto` against DVWA
6. Run `gobuster` against DVWA
7. Document all findings

```bash
# Verification commands
docker ps  # Confirm containers running
curl -I http://localhost:8080  # Test DVWA
nikto -h http://localhost:8080
gobuster dir -u http://localhost:8080 -w /usr/share/wordlists/dirb/common.txt
```

---

## Summary

- Burp Suite is the essential web testing proxy
- OWASP ZAP provides a free alternative
- Command-line tools (`curl`, `nmap`, `ffuf`) complement GUI tools
- `sqlmap` automates SQL injection detection and exploitation
- Wordlists are critical - SecLists is the go-to collection
- Practice on DVWA, Juice Shop, and WebGoat
- Always follow a structured methodology

> Next: Web Spidering & Content Discovery
