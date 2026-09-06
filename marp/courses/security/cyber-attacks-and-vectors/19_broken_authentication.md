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

# Broken Authentication

---

## What is Broken Authentication

- Broken Authentication is a web application security risk that occurs when authentication mechanisms are improperly implemented, allowing attackers to compromise user accounts or gain unauthorized access to sensitive data
- Ranked #7 in OWASP Top 10 (2021) as "Identification and Authentication Failures"
- Responsible for some of the largest data breaches in history

---

## Authentication vs Authorization

```bash
┌──────────────────────────────────────────────────────────┐
│  Authentication vs Authorization                         │
├──────────────────────────┬───────────────────────────────┤
│  Authentication (AuthN)  │  Authorization (AuthZ)        │
├──────────────────────────┼───────────────────────────────┤
│  "Who are you?"          │  "What can you do?"           │
│  Verifies identity       │  Verifies permissions         │
│  Login credentials       │  Access control rules         │
│  Happens first           │  Happens after authentication │
│  401 Unauthorized        │  403 Forbidden                │
└──────────────────────────┴───────────────────────────────┘
```

- Broken authentication focuses on failures in verifying identity
- Both are critical; a failure in either can lead to unauthorized access

---

## Common Broken Authentication Vulnerabilities

- Weak or easily guessable credentials
- Lack of proper password policies
- Insecure transmission of credentials
- Improper session management
- Weak account recovery mechanisms
- Lack of multi-factor authentication

---

## Credential Stuffing Attacks

![credential_stuffing_attacks](svg/courses/security/cyber-attacks-and-vectors/19_broken_authentication/credential_stuffing_attacks.svg)

---

## Credential Stuffing Attacks: Details

**Defense against credential stuffing:**
- Rate limiting login attempts per IP and per account
- CAPTCHA after failed attempts
- Breached password detection (Have I Been Pwned API)
- Require MFA for all users

---

## Brute Force vs Credential Stuffing

| Aspect              | Brute Force              | Credential Stuffing        |
|---------------------|--------------------------|----------------------------|
| Source of passwords | Generated/dictionary     | Leaked from other breaches |
| Success rate        | Very low (< 0.1%)       | Higher (0.1% - 2%)        |
| Speed               | Slow (many attempts)     | Fast (one attempt per pair)|
| Detection           | Easier (many failures)   | Harder (looks like normal) |
| Defense             | Account lockout          | Breached password check    |

---

## Session Fixation Attack

```python
┌──────────────────────────────────────────────────────────┐
│          Session Fixation Attack                          │
│                                                          │
│  1. Attacker gets a valid session ID from the server     │
│     GET /login -> Set-Cookie: SESSIONID=abc123           │
│                                                          │
│  2. Attacker tricks victim into using that session ID    │
│     Link: https://bank.com/login?SESSIONID=abc123        │
│     Or: injected via XSS                                 │
│                                                          │
│  3. Victim logs in using the attacker's session ID       │
│     POST /login (Cookie: SESSIONID=abc123)               │
│     Server authenticates user with session abc123        │
│                                                          │
│  4. Attacker uses the same session ID                    │
│     GET /account (Cookie: SESSIONID=abc123)              │
│     Server sees authenticated session -> access granted! │
└──────────────────────────────────────────────────────────┘
```

**Defense:**
- Always regenerate session ID after successful authentication
- Never accept session IDs from URL parameters
- Set `HttpOnly` and `Secure` flags on session cookies

```python
# Flask example: regenerate session on login
from flask import session

@app.route('/login', methods=['POST'])
def login():
    if authenticate(request.form['user'], request.form['pass']):
        session.regenerate()  # Critical: new session ID
        session['user'] = request.form['user']
        session['authenticated'] = True
```

---

## JWT Vulnerabilities

### The "none" Algorithm Attack

```asm
┌──────────────────────────────────────────────────────────┐
│          JWT "none" Algorithm Attack                      │
│                                                          │
│  Normal JWT:                                             │
│  Header:  {"alg": "HS256", "typ": "JWT"}                │
│  Payload: {"sub": "user123", "role": "user"}             │
│  Signature: HMAC-SHA256(header.payload, secret)          │
│                                                          │
│  Attacker modifies:                                      │
│  Header:  {"alg": "none", "typ": "JWT"}                 │
│  Payload: {"sub": "user123", "role": "admin"}            │
│  Signature: (empty)                                      │
│                                                          │
│  If server accepts "none" algorithm, no signature check! │
└──────────────────────────────────────────────────────────┘
```

### Key Confusion Attack (RS256 to HS256)

```python
# Vulnerable server uses RS256 (asymmetric)
# Public key is known to attacker

# Attacker crafts token:
import jwt
import json

public_key = open('public_key.pem').read()

# Trick: sign with HS256 using the PUBLIC key as the HMAC secret
# Server code that verifies with the public key will accept it!
forged_token = jwt.encode(
    {"sub": "admin", "role": "admin"},
    public_key,
    algorithm="HS256"
)
# If server does: jwt.decode(token, public_key, algorithms=["RS256", "HS256"])
# The forged token passes verification!
```

---

## JWT Security Best Practices

```python
# SECURE JWT verification in Python
import jwt

# Always specify exact allowed algorithms
ALLOWED_ALGORITHMS = ["RS256"]  # Never include "none" or "HS256" with RS

def verify_token(token):
    try:
        payload = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=ALLOWED_ALGORITHMS,  # Explicit whitelist
            options={
                "require": ["exp", "iat", "sub"],  # Required claims
                "verify_exp": True,
                "verify_iat": True,
            }
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
```

| JWT Pitfall                | Defense                                     |
|----------------------------|---------------------------------------------|
| "none" algorithm accepted  | Whitelist specific algorithms                |
| Algorithm confusion        | Never mix symmetric and asymmetric           |
| No expiration              | Always set and verify `exp` claim            |
| Token in URL               | Use Authorization header or HttpOnly cookie  |
| Secret in source code      | Use environment variables or key vault       |
| Long-lived tokens          | Short expiry + refresh token rotation        |

---

## Password Storage

![password_storage](svg/courses/security/cyber-attacks-and-vectors/19_broken_authentication/password_storage.svg)

---

## Password Storage: Comparison

### Why bcrypt/Argon2 are Preferred

| Algorithm  | Speed (hashes/sec) | Memory Usage | Resistant To        |
|------------|--------------------|--------------|--------------------|
| MD5        | ~10 billion/sec    | Negligible   | Nothing            |
| SHA-256    | ~5 billion/sec     | Negligible   | Nothing            |
| bcrypt     | ~30,000/sec        | 4 KB         | GPU attacks        |
| scrypt     | ~20,000/sec        | 16+ MB       | GPU + ASIC attacks |
| Argon2id   | ~10,000/sec        | 64+ MB       | GPU, ASIC, side-ch.|

---

## Implementing Secure Password Hashing

```python
# Python: Using bcrypt
import bcrypt

def hash_password(password: str) -> str:
    """Hash a password with bcrypt (cost factor 12)."""
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its bcrypt hash."""
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed.encode('utf-8')
    )

# Python: Using Argon2 (recommended for new applications)
from argon2 import PasswordHasher

ph = PasswordHasher(
    time_cost=3,        # Number of iterations
    memory_cost=65536,  # 64 MB memory
    parallelism=4,      # 4 parallel threads
)

hashed = ph.hash("user_password")
# $argon2id$v=19$m=65536,t=3,p=4$...

try:
    ph.verify(hashed, "user_password")
    # Optionally check if rehash is needed
    if ph.check_needs_rehash(hashed):
        new_hash = ph.hash("user_password")
except Exception:
    print("Invalid password")
```

---

## Multi-Factor Authentication (MFA)

```python
┌──────────────────────────────────────────────────────────┐
│          Authentication Factors                           │
│                                                          │
│  Something You Know    Something You Have    Something   │
│  ┌─────────────────┐  ┌─────────────────┐  You Are      │
│  │  Password        │  │  Phone / TOTP   │  ┌──────────┐│
│  │  PIN             │  │  Hardware key   │  │Fingerprint││
│  │  Security Q&A    │  │  Smart card     │  │Face ID    ││
│  │  Passphrase      │  │  SMS code       │  │Iris scan  ││
│  └─────────────────┘  └─────────────────┘  └──────────┘│
│                                                          │
│  MFA = Two or more factors from DIFFERENT categories     │
│  (Password + Security Q = still single factor!)          │
└──────────────────────────────────────────────────────────┘
```

### MFA Strength Comparison

| Method            | Security Level | Phishing Resistant | User Experience |
|-------------------|---------------|-------------------|-----------------|
| SMS OTP           | Low           | No                | Easy            |
| Email OTP         | Low           | No                | Easy            |
| TOTP (Authenticator)| Medium     | No                | Medium          |
| Push notification | Medium        | Partially         | Easy            |
| FIDO2/WebAuthn    | High          | Yes               | Easy            |
| Hardware key (YubiKey)| Highest  | Yes               | Medium          |

---

## MFA Bypass Techniques

```bash
┌──────────────────────────────────────────────────────────┐
│          Common MFA Bypass Methods                        │
│                                                          │
│  1. SIM Swapping (defeats SMS-based MFA)                 │
│     Attacker convinces carrier to transfer phone number  │
│                                                          │
│  2. Real-time Phishing Proxy (defeats TOTP)              │
│     Tool (evilginx2) relays credentials + TOTP in real   │
│     time between victim and legitimate site              │
│                                                          │
│  3. MFA Fatigue / Push Bombing                           │
│     Repeatedly send push notifications until user        │
│     accidentally approves (Uber breach 2022)             │
│                                                          │
│  4. Session Token Theft (bypasses MFA entirely)          │
│     Steal session cookie after MFA is complete           │
│     (via XSS, malware, or browser extension)             │
│                                                          │
│  5. Recovery Code Theft                                  │
│     Social engineer support to reset MFA                 │
│     Or steal stored backup/recovery codes                │
└──────────────────────────────────────────────────────────┘
```

**Defense against MFA bypass:**
- Use phishing-resistant methods (FIDO2/WebAuthn)
- Implement number matching for push notifications
- Rate limit MFA attempts
- Monitor for suspicious MFA enrollment changes

---

## OAuth Misconfigurations

![oauth_misconfigurations](svg/courses/security/cyber-attacks-and-vectors/19_broken_authentication/oauth_misconfigurations.svg)

---

## OAuth Misconfigurations: Example

```python
# Secure OAuth implementation checklist
OAUTH_CONFIG = {
    # Strict redirect URI matching (exact match only)
    "redirect_uris": ["https://myapp.com/callback"],
    # Always use authorization code flow (not implicit)
    "response_type": "code",
    # Always include state parameter for CSRF protection
    "state": generate_random_state(),
    # Use PKCE (Proof Key for Code Exchange)
    "code_challenge": generate_pkce_challenge(),
    "code_challenge_method": "S256",
    # Request minimum necessary scopes
    "scope": "openid email profile",
}
```

---

## Insecure Password Reset Flows

![insecure_password_reset_flows](svg/courses/security/cyber-attacks-and-vectors/19_broken_authentication/insecure_password_reset_flows.svg)

---

## Insecure Password Reset Flows: Example

```python
import secrets
from datetime import datetime, timedelta
def create_reset_token(user_email):
    """Generate a secure password reset token."""
    token = secrets.token_urlsafe(32)  # 256-bit random token
    expiry = datetime.utcnow() + timedelta(minutes=15)
    # Store hashed token (never store raw token in DB)
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    db.store_reset_token(user_email, token_hash, expiry)
    # Send token to user's verified email
    reset_url = f"https://app.com/reset?token={token}"
    send_email(user_email, reset_url)
    # Always return same message (prevent email enumeration)
    return "If an account exists, a reset link has been sent."
```

---

## Session Management Best Practices

```python
# Secure session configuration (Flask example)
app.config.update(
    SESSION_COOKIE_SECURE=True,       # HTTPS only
    SESSION_COOKIE_HTTPONLY=True,      # No JavaScript access
    SESSION_COOKIE_SAMESITE='Lax',    # CSRF protection
    SESSION_COOKIE_NAME='__Host-sid', # Cookie prefix protection
    PERMANENT_SESSION_LIFETIME=1800,  # 30 minute timeout
)
```

| Session Setting        | Purpose                              | Recommended Value |
|------------------------|--------------------------------------|-------------------|
| `Secure` flag          | Only send over HTTPS                 | Always True       |
| `HttpOnly` flag        | Prevent XSS access to cookie         | Always True       |
| `SameSite` attribute   | CSRF protection                      | `Lax` or `Strict` |
| Session timeout        | Limit session lifetime               | 15-30 minutes     |
| Session ID length      | Prevent brute force                  | 128+ bits entropy |
| Regenerate on login    | Prevent session fixation             | Always            |
| Invalidate on logout   | Prevent session reuse                | Always            |

---

## Implementing Account Lockout

```python
from datetime import datetime, timedelta
import time

MAX_ATTEMPTS = 5
LOCKOUT_DURATION = timedelta(minutes=15)
ATTEMPT_WINDOW = timedelta(minutes=30)

def check_login(username, password):
    user = db.get_user(username)

    # Check if account is locked
    if user.locked_until and user.locked_until > datetime.utcnow():
        remaining = (user.locked_until - datetime.utcnow()).seconds
        # Constant time response (prevent timing attacks)
        time.sleep(0.5)
        return f"Account locked. Try again in {remaining}s."

    # Verify password (constant time comparison)
    if not verify_password(password, user.password_hash):
        user.failed_attempts += 1
        user.last_failed = datetime.utcnow()

        if user.failed_attempts >= MAX_ATTEMPTS:
            user.locked_until = datetime.utcnow() + LOCKOUT_DURATION
            notify_user(user, "Account locked due to failed attempts")

        db.save(user)
        # Generic message (prevent username enumeration)
        return "Invalid credentials."

    # Success: reset failed attempts
    user.failed_attempts = 0
    user.locked_until = None
    session.regenerate()
    return "Login successful."
```

---

## Authentication Security Checklist

```sql
┌──────────────────────────────────────────────────────────┐
│          Authentication Security Checklist                │
├──────────────────────────────────────────────────────────┤
│  Passwords:                                              │
│  [ ] Minimum 8 characters, encourage passphrases         │
│  [ ] Check against breached password databases           │
│  [ ] Hash with bcrypt/Argon2id (never MD5/SHA)           │
│  [ ] No password hints or security questions             │
│                                                          │
│  Sessions:                                               │
│  [ ] Regenerate session ID on login/privilege change     │
│  [ ] Set Secure, HttpOnly, SameSite cookie flags         │
│  [ ] Implement idle and absolute timeouts                │
│  [ ] Invalidate sessions on logout (server-side)         │
│                                                          │
│  MFA:                                                    │
│  [ ] Require MFA for all users (not just admins)         │
│  [ ] Prefer FIDO2/WebAuthn over SMS/TOTP                 │
│  [ ] Rate limit MFA attempts                             │
│  [ ] Implement number matching for push notifications    │
│                                                          │
│  General:                                                │
│  [ ] Use HTTPS everywhere                                │
│  [ ] Implement account lockout with backoff              │
│  [ ] Log all authentication events                       │
│  [ ] Generic error messages (prevent enumeration)        │
│  [ ] Rate limit login endpoints                          │
└──────────────────────────────────────────────────────────┘
```

---

## Key Takeaways

- Broken authentication is one of the most common and dangerous web vulnerabilities
- Credential stuffing exploits password reuse -- use breached password detection and MFA
- Always hash passwords with bcrypt or Argon2id, never MD5/SHA
- JWT tokens require careful implementation (algorithm whitelisting, expiration, key management)
- Session fixation is prevented by regenerating session IDs after login
- MFA significantly reduces risk but is not bulletproof -- prefer FIDO2/WebAuthn
- OAuth flows must strictly validate redirect URIs and use PKCE
- Defense in depth: combine strong passwords + MFA + session management + monitoring
