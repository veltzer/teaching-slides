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

# Account Takeover: Protecting Your Digital Identities

---

## What is Account Takeover

- Account takeover (ATO) is a type of cyber attack where a malicious actor gains unauthorized access to a user's account.
- Attackers can leverage stolen credentials, stolen session tokens, or exploit vulnerabilities to gain control over accounts.
- ATO attacks can target various types of accounts, including email, social media, banking, e-commerce, and more.

---

## Consequences of Account Takeover

- Loss of privacy and data breaches
- Financial losses and fraud
- Reputation damage and identity theft
- Disruption of business operations
- Compliance and regulatory issues

---

## Common Account Takeover Techniques

- Credential stuffing (using stolen credentials from data breaches)
- Phishing and social engineering tactics
- Exploiting vulnerabilities in web applications or APIs
- Session hijacking and token theft
- Brute-force attacks and password cracking

---

## Defending Against Account Takeover

- Implement strong authentication measures
- Enhance monitoring and detection capabilities
- Enforce secure password policies and hygiene
- Conduct regular security assessments
- Educate and raise user awareness
- Stay informed about emerging threats and techniques

---

## Strong Authentication Measures

- Implement multi-factor authentication (MFA)
- Use stronger authentication factors (e.g., hardware tokens, biometrics)
- Leverage behavioral analytics and risk-based authentication
- Implement passwordless authentication solutions
- Regularly rotate and update authentication credentials

---

## Monitoring and Detection

- Deploy user behavior analytics and anomaly detection systems
- Monitor for suspicious login activities and session hijacking attempts
- Implement web application firewalls (WAFs) and intrusion detection/prevention systems (IDS/IPS)
- Leverage security information and event management (SIEM) solutions
- Conduct regular log analysis and incident response procedures

---

## Password Policies and Hygiene

- Enforce strong password policies (length, complexity, expiration)
- Discourage password reuse across accounts
- Encourage the use of password managers
- Regularly rotate and reset passwords, especially for privileged accounts
- Implement password blacklisting and strength checking

---

## Security Assessments and Testing

- Conduct regular vulnerability assessments and penetration testing
- Identify and remediate vulnerabilities in web applications, APIs, and authentication mechanisms
- Perform code reviews and secure coding practices
- Test and validate authentication and authorization controls

---

## User Awareness and Education

- Provide security awareness training for employees and users
- Educate users on identifying phishing attempts and social engineering tactics
- Promote good password hygiene practices
- Encourage users to enable and utilize MFA and other security features
- Foster a culture of security awareness and responsibility

---

## Staying Vigilant and Informed

- Stay updated on the latest account takeover techniques and trends
- Subscribe to threat intelligence feeds and security advisories
- Participate in information sharing communities (ISACs, CERTs)
- Collaborate with industry partners and law enforcement agencies
- Continuously assess and improve your organization's security posture

---

## Account Takeover Attack Flow

![account_takeover_attack_flow](svg/courses/security/cyber-attacks-and-vectors/15_account_takeover/account_takeover_attack_flow.svg)

---

## Credential Stuffing in Detail

```python
# How credential stuffing works (educational purposes only)
# Attackers automate login attempts using breach data

# Breach database format (available on dark web):
# email:password
# user@example.com:Summer2023!
# john@company.com:P@ssw0rd123

# Attacker script pattern:
import requests

# VULNERABLE: No rate limiting, no CAPTCHA
def credential_stuff(target_url, credentials_file):
    with open(credentials_file) as f:
        for line in f:
            email, password = line.strip().split(':')
            resp = requests.post(target_url, data={
                'email': email,
                'password': password
            })
            if 'Welcome' in resp.text:
                print(f"[+] Valid: {email}:{password}")
    # Attackers rotate proxies and add delays to evade detection
```

Why it works: 65% of people reuse passwords across sites.

---

## Detecting Credential Stuffing

```python
# Server-side detection patterns

from collections import defaultdict
import time

login_attempts = defaultdict(list)  # IP -> timestamps
failed_logins = defaultdict(int)    # username -> count
ip_user_map = defaultdict(set)      # IP -> set of usernames

def detect_stuffing(ip, username, success):
    now = time.time()

    # Pattern 1: Many different usernames from one IP
    ip_user_map[ip].add(username)
    if len(ip_user_map[ip]) > 20:
        alert(f"Credential stuffing: {ip} tried {len(ip_user_map[ip])} users")

    # Pattern 2: High failure rate from one IP
    login_attempts[ip].append((now, success))
    recent = [s for t, s in login_attempts[ip] if now - t < 300]
    failures = sum(1 for s in recent if not s)
    if failures > 10:
        alert(f"Brute force: {ip} had {failures} failures in 5min")

    # Pattern 3: Login from unusual location
    # Compare IP geolocation to user's typical locations
    # Flag if new country/city
```

---

## Rate Limiting and Account Protection

```python
# Flask rate limiting example
from flask_limiter import Limiter

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Max 5 login attempts per minute
def login():
    # ... authentication logic ...
    pass

# Progressive delays after failed attempts
@app.route('/login', methods=['POST'])
def login_with_backoff():
    username = request.form['username']
    failures = get_failure_count(username)

    if failures >= 3:
        delay = min(2 ** (failures - 3), 60)  # 1s, 2s, 4s, 8s...60s
        time.sleep(delay)

    if failures >= 10:
        # Lock account, require email verification
        lock_account(username)
        send_unlock_email(username)
        return 'Account locked. Check email.', 423

    # ... attempt authentication ...
```

---

## Real-World ATO Incidents

| Incident               | Year | Details                                 |
|------------------------|------|-----------------------------------------|
| Dunkin' Donuts         | 2019 | Credential stuffing, rewards points stolen|
| Zoom                   | 2020 | 500K accounts sold on dark web ($0.002 each)|
| The North Face         | 2020 | Credential stuffing on customer accounts |
| PayPal                 | 2022 | 35,000 accounts breached via stuffing    |
| 23andMe                | 2023 | 6.9M profiles accessed via credential stuffing|

---

## Exercise: Account Takeover Defense

1. Build a login system with Flask that tracks:
   - Failed login attempts per IP
   - Failed login attempts per username
   - Login location (IP geolocation)
1. Implement progressive rate limiting (delays increase with failures)
1. Add account lockout after 10 failed attempts
1. Implement CAPTCHA after 3 failed attempts
1. Add email notification for logins from new devices/locations
1. Simulate a credential stuffing attack and verify defenses trigger
1. Implement Have I Been Pwned API check for password changes
