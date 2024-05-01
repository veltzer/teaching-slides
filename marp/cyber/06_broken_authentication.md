---
marp: true
---

# Broken Authentication

---

## What is Broken Authentication?

Broken Authentication is a web application security risk that occurs when authentication mechanisms are improperly implemented, allowing attackers to compromise user accounts or gain unauthorized access to sensitive data.

---

## Common Broken Authentication Vulnerabilities

- Weak or easily guessable credentials
- Lack of proper password policies
- Insecure transmission of credentials
- Improper session management
- Weak account recovery mechanisms
- Lack of multi-factor authentication

---

## Weak or Easily Guessable Credentials

- Using default or weak passwords
- Allowing short or common passwords
- Storing passwords in plain-text or with weak encryption

---

## Lack of Proper Password Policies

- No requirements for password complexity
- No password expiration or history policies
- No account lockout mechanisms after failed attempts

---

## Insecure Transmission of Credentials

- Transmitting credentials over unencrypted channels
- Failure to use HTTPS for authentication pages
- Lack of protection against man-in-the-middle attacks

---

## Improper Session Management

- Lack of proper session expiration and termination
- Predictable or insecure session IDs
- Lack of protection against session fixation or hijacking

---

## Weak Account Recovery Mechanisms

- Insecure password reset processes
- Lack of verification for account recovery requests
- Disclosure of sensitive information during recovery

---

## Lack of Multi-Factor Authentication

- Relying solely on passwords for authentication
- Failure to implement additional authentication factors
- Lack of risk-based or adaptive authentication measures

---

## Consequences of Broken Authentication

- Unauthorized access to user accounts and data
- Impersonation and identity theft
- Data breaches and data exfiltration
- Regulatory fines and legal implications
- Damage to reputation and customer trust

---

## Mitigating Broken Authentication

- Implement strong password policies and hashing
- Use secure communication protocols (HTTPS, TLS)
- Implement proper session management mechanisms
- Implement multi-factor authentication
- Conduct regular security audits and penetration testing
- Educate users on secure authentication practices
