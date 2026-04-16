---
tags:
  - security:security
  - security:web-security
  - security:penetration-testing
  - security:owasp
level: advanced
category: security
audience:
  - audiences:developers
  - audiences:security-professionals

---

# Securing Authentication

## Building Robust Login Systems

---

## Defense Strategy Overview

![defense_strategy_overview](svg/courses/security/web-application-hacking/09_securing_authentication/defense_strategy_overview.svg)

---

## Password Storage Best Practices

```python
# WRONG: Plaintext
password = "secret123"  # Never!

# WRONG: Simple hash
import hashlib
hashed = hashlib.md5(password.encode()).hexdigest()  # Never!

# WRONG: Hash without salt
hashed = hashlib.sha256(password.encode()).hexdigest()

# RIGHT: bcrypt (adaptive, salted)
import bcrypt
salt = bcrypt.gensalt(rounds=12)
hashed = bcrypt.hashpw(password.encode(), salt)

# RIGHT: Argon2 (winner of Password Hashing Competition)
from argon2 import PasswordHasher
ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4)
hashed = ph.hash(password)
verified = ph.verify(hashed, password)  # Returns True/False
```

---

## Password Policy Recommendations

```misc
Minimum Requirements (NIST SP 800-63B):
- Minimum 8 characters (12+ recommended)
- Maximum at least 64 characters
- Allow all ASCII and Unicode characters
- Check against breach databases (HIBP)
- No composition rules (e.g., must have uppercase)
- No periodic password rotation (unless compromised)
- No password hints or knowledge-based questions

Implementation:
- Use zxcvbn for password strength estimation
- Provide real-time feedback during password creation
- Block top 100,000 most common passwords
- Check against organization-specific terms
```

---

## Rate Limiting Implementation

```python
# Using Redis for rate limiting
import redis
import time

r = redis.Redis()

def check_rate_limit(identifier, max_attempts=5, window=300):
    """Allow max_attempts per window (seconds)"""
    key = f"login_attempts:{identifier}"
    current = r.get(key)

    if current and int(current) >= max_attempts:
        ttl = r.ttl(key)
        return False, f"Too many attempts. Try again in {ttl}s"

    pipe = r.pipeline()
    pipe.incr(key)
    pipe.expire(key, window)
    pipe.execute()

    return True, "OK"

# Apply to login endpoint
# Use both IP AND username as identifiers
# Implement exponential backoff for repeated offenders
```

---

## Account Lockout Strategy

```misc
Progressive Response:
Attempt 1-3:   Normal login
Attempt 4-5:   Add CAPTCHA
Attempt 6-10:  Add delay (increasing)
Attempt 11+:   Temporary lockout (15 min)
Attempt 20+:   Longer lockout (1 hour)

Important considerations:
- Lock by ACCOUNT, not just by IP
- But also track by IP (to catch distributed attacks)
- Always allow password reset even when locked
- Notify the account owner of lockout
- Log all lockout events for monitoring
- Reset counter on successful login
- Don't reveal lockout status to attacker
```

---

## Secure Session Configuration

```python
# Flask example with secure session settings
from flask import Flask, session
app = Flask(__name__)

app.config.update(
    SECRET_KEY=os.urandom(32),           # Strong random secret
    SESSION_COOKIE_SECURE=True,           # HTTPS only
    SESSION_COOKIE_HTTPONLY=True,          # No JavaScript access
    SESSION_COOKIE_SAMESITE='Lax',        # CSRF protection
    SESSION_COOKIE_NAME='__Host-session', # Cookie prefix
    PERMANENT_SESSION_LIFETIME=1800,      # 30 min timeout
)

# Express.js example
app.use(session({
    secret: crypto.randomBytes(32).toString('hex'),
    cookie: {
        secure: true,
        httpOnly: true,
        sameSite: 'lax',
        maxAge: 1800000
    },
    resave: false,
    saveUninitialized: false
}));
```

---

## Secure Password Reset Flow

```misc
1. User requests reset for email
2. ALWAYS respond: "If account exists, email sent"
3. Generate cryptographically random token (32+ bytes)
4. Store HASH of token in database (not plaintext)
5. Set expiration (15-30 minutes max)
6. Send HTTPS link with token to registered email
7. On reset page: validate token hash, check expiry
8. Allow ONE use only - invalidate after use
9. Invalidate all existing sessions after reset
10. Send confirmation email that password was changed

DO NOT:
- Include password or username in reset email
- Use sequential or predictable tokens
- Allow token reuse
- Skip expiration checks
```

---

## Multi-Factor Authentication Best Practices

```misc
Recommended MFA methods (strongest to weakest):
1. Hardware security keys (FIDO2/WebAuthn)
2. Authenticator apps (TOTP - Google Auth, Authy)
3. Push notifications (with number matching)
4. SMS codes (vulnerable to SIM swap, but better than nothing)

Implementation checklist:
[ ] Enforce MFA at the server, not just the client
[ ] Validate MFA on every sensitive operation
[ ] Rate limit MFA code attempts (max 5)
[ ] Expire TOTP codes after one use
[ ] Provide backup codes (store hashed)
[ ] Allow MFA recovery via secure process
[ ] Log MFA events for monitoring
[ ] Don't allow MFA step to be skipped via URL manipulation
```

---

## Generic Error Messages

```python
# VULNERABLE - reveals user existence
@app.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(username=request.form['username']).first()
    if not user:
        return "User not found", 401      # Reveals user doesn't exist
    if not user.check_password(request.form['password']):
        return "Incorrect password", 401   # Reveals user exists
    return redirect('/dashboard')

# SECURE - generic message
@app.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(username=request.form['username']).first()
    if not user or not user.check_password(request.form['password']):
        # Add constant-time delay to prevent timing attacks
        time.sleep(random.uniform(0.1, 0.3))
        return "Invalid username or password", 401
    return redirect('/dashboard')
```

---

## Timing Attack Prevention

```python
import hmac
import time

def constant_time_compare(a, b):
    """Prevent timing attacks on string comparison"""
    return hmac.compare_digest(a.encode(), b.encode())

def login(username, password):
    user = get_user(username)

    if user is None:
        # Still perform password hash to keep timing constant
        dummy_hash = "$2b$12$dummy.hash.for.timing.attack.prevention"
        bcrypt.checkpw(password.encode(), dummy_hash.encode())
        return False

    return bcrypt.checkpw(password.encode(), user.password_hash.encode())

# Without this, attackers can determine valid usernames
# by measuring response time differences
```

---

## Authentication Security Checklist

```misc
Transport:
[x] All login pages served over HTTPS
[x] HSTS header enabled
[x] No credentials in URL parameters

Storage:
[x] Passwords hashed with bcrypt/Argon2
[x] Unique salt per password
[x] Adequate work factor (bcrypt rounds >= 12)

Login:
[x] Generic error messages
[x] Rate limiting on login attempts
[x] Account lockout after N failures
[x] CAPTCHA after repeated failures
[x] MFA available and enforced for sensitive accounts

Session:
[x] Secure, HttpOnly, SameSite cookies
[x] Session timeout (idle and absolute)
[x] Session invalidation on logout
[x] New session ID on privilege change
```

---

## WebAuthn / FIDO2 - The Future of Authentication

```misc
WebAuthn replaces passwords with cryptographic credentials

Registration:
  1. Server sends challenge (random bytes)
  2. Authenticator creates key pair
  3. Private key stays on device (NEVER leaves)
  4. Public key sent to server
  5. Server stores public key for user

Authentication:
  1. Server sends challenge
  2. Authenticator signs challenge with private key
  3. Signed response sent to server
  4. Server verifies with stored public key

Benefits:
  - Phishing resistant (origin-bound)
  - No shared secrets
  - No password database to breach
  - Fast and user-friendly

Hardware: YubiKey, Google Titan, platform authenticators
```

---

## Breached Password Detection

```python
# Check passwords against known breaches
# Using Have I Been Pwned API (k-anonymity model)

import hashlib
import requests

def is_password_breached(password):
    """Check if password appears in breach databases.
    Uses k-anonymity - only first 5 chars of hash sent."""

    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]

    # Request all hashes matching this prefix
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)

    # Check if our suffix appears in results
    for line in response.text.splitlines():
        hash_suffix, count = line.split(':')
        if hash_suffix == suffix:
            return True, int(count)

    return False, 0

# Usage during registration/password change
breached, count = is_password_breached(new_password)
if breached:
    return f"This password has appeared in {count} data breaches. Choose another."
```

---

## Authentication Monitoring & Alerting

```python
# Events to monitor and alert on:

ALERT_RULES = {
    'brute_force': {
        'condition': 'Failed logins > 10 in 5 minutes for same account',
        'action': 'Lock account, alert security team',
        'severity': 'HIGH'
    },
    'credential_stuffing': {
        'condition': 'Failed logins > 100 in 5 minutes from same IP',
        'action': 'Block IP, alert security team',
        'severity': 'HIGH'
    },
    'impossible_travel': {
        'condition': 'Login from two geolocations too far apart',
        'action': 'Challenge with MFA, alert user',
        'severity': 'MEDIUM'
    },
    'new_device': {
        'condition': 'Login from unrecognized device/browser',
        'action': 'Send email notification to user',
        'severity': 'LOW'
    },
    'admin_login': {
        'condition': 'Any admin account login',
        'action': 'Log and alert',
        'severity': 'INFO'
    }
}
```

---

## Passwordless Authentication

```misc
Passwordless methods eliminate password risks entirely:

1. Magic Links
   - User enters email
   - Server sends one-time link to email
   - User clicks link -> authenticated
   - Token expires after use or timeout

2. WebAuthn / Passkeys
   - Biometric or hardware key authentication
   - No password to phish, brute-force, or leak
   - Supported by all major platforms

3. One-Time Passcodes (OTP)
   - SMS or email code for each login
   - Simple but SMS is vulnerable to SIM swap

4. Push Notifications
   - App sends push to registered device
   - User approves or denies
   - Number matching prevents MFA fatigue

Benefits:
  - No password database to breach
  - No credential stuffing possible
  - No phishing of passwords
  - Better user experience
```

---

## Secure Registration Flow

```python
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # 1. Validate input
    if not is_valid_username(username):     # Alphanumeric, 3-30 chars
        return error("Invalid username format")
    if not is_valid_email(email):           # RFC 5322 compliant
        return error("Invalid email format")

    # 2. Check password strength
    if not is_strong_password(password):    # zxcvbn score >= 3
        return error("Password too weak")

    # 3. Check breached passwords
    if is_password_breached(password)[0]:
        return error("Password found in breach database")

    # 4. Check for duplicate (prevent enumeration!)
    # ALWAYS return same response regardless
    if User.query.filter_by(email=email).first():
        send_already_registered_email(email)
    else:
        user = User(username=username, email=email)
        user.set_password(password)  # Argon2 hash
        db.session.add(user)
        send_verification_email(email)

    return "If valid, a verification email has been sent"
```

---

## Lab: Review DVWA Security Levels

Compare DVWA brute-force module at each security level:

| Level | Protection |
|-------|-----------|
| **Low** | No protection at all |
| **Medium** | `sleep(2)` on failure |
| **High** | Random token + sleep |
| **Impossible** | Account lockout + CSRF token |

Examine the source code at each level to understand the defenses.

---

## Summary

- Use Argon2 or bcrypt for password storage
- Implement progressive rate limiting
- Use generic error messages everywhere
- Prevent timing attacks with constant-time operations
- Enforce MFA with hardware keys or TOTP apps
- Secure password reset with random, expiring tokens
- Monitor and alert on authentication anomalies

> Next: Session Management Attacks
