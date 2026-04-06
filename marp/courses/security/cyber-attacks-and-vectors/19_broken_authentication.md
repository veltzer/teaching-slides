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

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="260" font-family="sans-serif">
  <defs>
    <marker id="arw1" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>
  <rect x="1" y="1" width="658" height="258" rx="4" fill="#fff" stroke="#333" stroke-width="1.5"/>
  <rect x="1" y="1" width="658" height="34" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="23" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">Credential Stuffing Flow</text>
  <text x="14" y="54" font-size="13" fill="#333">1. Data breach at Site A leaks millions of username:password pairs</text>
  <text x="14" y="72" font-size="13" fill="#333">2. Attacker obtains the leaked credentials (dark web, paste sites, etc.)</text>
  <text x="14" y="90" font-size="13" fill="#333">3. Automated tool tries each credential pair against Site B, Site C, Site D...</text>
  <rect x="14" y="106" width="110" height="76" rx="4" fill="#fff3e0" stroke="#333" stroke-width="1.5"/>
  <text x="69" y="140" font-size="13" font-weight="bold" fill="#222" text-anchor="middle">Attacker</text>
  <text x="69" y="158" font-size="12" fill="#555" text-anchor="middle">(botnet)</text>
  <rect x="430" y="106" width="110" height="76" rx="4" fill="#f0f4f8" stroke="#333" stroke-width="1.5"/>
  <text x="485" y="150" font-size="13" font-weight="bold" fill="#222" text-anchor="middle">Site B</text>
  <line x1="124" y1="126" x2="430" y2="126" stroke="#555" stroke-width="1.5" marker-end="url(#arw1)"/>
  <text x="277" y="120" font-size="11" fill="#555" text-anchor="middle">user1:pass1</text>
  <text x="548" y="130" font-size="12" fill="#c62828" font-weight="bold">FAIL</text>
  <line x1="124" y1="146" x2="430" y2="146" stroke="#555" stroke-width="1.5" marker-end="url(#arw1)"/>
  <text x="277" y="140" font-size="11" fill="#555" text-anchor="middle">user2:pass2</text>
  <text x="542" y="150" font-size="12" fill="#2e7d32" font-weight="bold">SUCCESS!</text>
  <line x1="124" y1="166" x2="430" y2="166" stroke="#555" stroke-width="1.5" marker-end="url(#arw1)"/>
  <text x="277" y="160" font-size="11" fill="#555" text-anchor="middle">user3:pass3</text>
  <text x="548" y="170" font-size="12" fill="#c62828" font-weight="bold">FAIL</text>
  <text x="14" y="216" font-size="13" fill="#555" font-style="italic">&#9888; Works because 65% of people reuse passwords</text>
</svg>

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

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="224" font-family="sans-serif">
  <rect x="1" y="1" width="658" height="222" rx="4" fill="#fff" stroke="#333" stroke-width="1.5"/>
  <rect x="1" y="1" width="658" height="34" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="23" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">Password Storage Evolution</text>
  <!-- Row: TERRIBLE -->
  <rect x="14" y="44" width="86" height="24" rx="3" fill="#ffcdd2" stroke="#c62828" stroke-width="1"/>
  <text x="57" y="61" font-size="12" fill="#b71c1c" font-weight="bold" text-anchor="middle">TERRIBLE</text>
  <text x="114" y="61" font-size="13" fill="#333">plaintext</text>
  <text x="290" y="61" font-size="12" fill="#555" font-family="monospace">"password123"</text>
  <!-- Row: BAD MD5 -->
  <rect x="14" y="76" width="86" height="24" rx="3" fill="#ffcdd2" stroke="#c62828" stroke-width="1"/>
  <text x="57" y="93" font-size="12" fill="#b71c1c" font-weight="bold" text-anchor="middle">BAD</text>
  <text x="114" y="93" font-size="13" fill="#333">MD5 hash</text>
  <text x="290" y="93" font-size="12" fill="#555" font-family="monospace">5f4dcc3b...</text>
  <!-- Row: BAD SHA-256 -->
  <rect x="14" y="108" width="86" height="24" rx="3" fill="#ffcdd2" stroke="#c62828" stroke-width="1"/>
  <text x="57" y="125" font-size="12" fill="#b71c1c" font-weight="bold" text-anchor="middle">BAD</text>
  <text x="114" y="125" font-size="13" fill="#333">SHA-256 hash</text>
  <text x="290" y="125" font-size="12" fill="#555" font-family="monospace">5e884898...</text>
  <!-- Row: BETTER -->
  <rect x="14" y="140" width="86" height="24" rx="3" fill="#fff9c4" stroke="#f9a825" stroke-width="1"/>
  <text x="57" y="157" font-size="12" fill="#e65100" font-weight="bold" text-anchor="middle">BETTER</text>
  <text x="114" y="157" font-size="13" fill="#333">SHA-256 + salt</text>
  <text x="290" y="157" font-size="12" fill="#555" font-family="monospace">salt + 5e884898...</text>
  <!-- Row: GOOD -->
  <rect x="14" y="172" width="86" height="24" rx="3" fill="#c8e6c9" stroke="#388e3c" stroke-width="1"/>
  <text x="57" y="189" font-size="12" fill="#1b5e20" font-weight="bold" text-anchor="middle">GOOD</text>
  <text x="114" y="189" font-size="13" fill="#333">bcrypt</text>
  <text x="290" y="189" font-size="12" fill="#555" font-family="monospace">$2b$12$...</text>
  <!-- Row: BEST -->
  <rect x="14" y="196" width="86" height="24" rx="3" fill="#a5d6a7" stroke="#2e7d32" stroke-width="1"/>
  <text x="57" y="213" font-size="12" fill="#1b5e20" font-weight="bold" text-anchor="middle">BEST</text>
  <text x="114" y="213" font-size="13" fill="#333">Argon2id</text>
  <text x="290" y="213" font-size="12" fill="#555" font-family="monospace">$argon2id$v=19$...</text>
</svg>

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

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="274" font-family="sans-serif">
  <rect x="1" y="1" width="658" height="272" rx="4" fill="#fff" stroke="#333" stroke-width="1.5"/>
  <rect x="1" y="1" width="658" height="34" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="23" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">Common OAuth Vulnerabilities</text>
  <!-- Item 1 -->
  <circle cx="28" cy="54" r="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="1"/>
  <text x="28" y="58" font-size="11" font-weight="bold" fill="#1565c0" text-anchor="middle">1</text>
  <text x="46" y="58" font-size="13" font-weight="bold" fill="#222">Open Redirect in redirect_uri</text>
  <text x="46" y="74" font-size="12" fill="#555">Attacker sets redirect_uri=https://evil.com — gets the authorization code</text>
  <!-- Item 2 -->
  <circle cx="28" cy="100" r="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="1"/>
  <text x="28" y="104" font-size="11" font-weight="bold" fill="#1565c0" text-anchor="middle">2</text>
  <text x="46" y="104" font-size="13" font-weight="bold" fill="#222">Insufficient redirect_uri validation</text>
  <text x="46" y="120" font-size="12" fill="#555">Allows https://app.com.evil.com or https://app.com/../evil</text>
  <!-- Item 3 -->
  <circle cx="28" cy="146" r="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="1"/>
  <text x="28" y="150" font-size="11" font-weight="bold" fill="#1565c0" text-anchor="middle">3</text>
  <text x="46" y="150" font-size="13" font-weight="bold" fill="#222">Missing state parameter (CSRF)</text>
  <text x="46" y="166" font-size="12" fill="#555">Attacker can force victim to link attacker's account</text>
  <!-- Item 4 -->
  <circle cx="28" cy="192" r="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="1"/>
  <text x="28" y="196" font-size="11" font-weight="bold" fill="#1565c0" text-anchor="middle">4</text>
  <text x="46" y="196" font-size="13" font-weight="bold" fill="#222">Token leakage in browser history / referrer</text>
  <text x="46" y="212" font-size="12" fill="#555">Implicit flow puts token in URL fragment — visible in logs and referrer headers</text>
  <!-- Item 5 -->
  <circle cx="28" cy="238" r="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="1"/>
  <text x="28" y="242" font-size="11" font-weight="bold" fill="#1565c0" text-anchor="middle">5</text>
  <text x="46" y="242" font-size="13" font-weight="bold" fill="#222">Scope escalation</text>
  <text x="46" y="258" font-size="12" fill="#555">Application requests more permissions than needed</text>
</svg>

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

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="296" font-family="sans-serif">
  <rect x="1" y="1" width="658" height="294" rx="4" fill="#fff" stroke="#333" stroke-width="1.5"/>
  <rect x="1" y="1" width="658" height="34" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="23" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">Password Reset Vulnerabilities</text>
  <!-- INSECURE column -->
  <rect x="14" y="44" width="304" height="240" rx="4" fill="#ffebee" stroke="#c62828" stroke-width="1.5"/>
  <rect x="14" y="44" width="304" height="28" rx="4" fill="#c62828"/>
  <text x="166" y="63" font-size="13" font-weight="bold" fill="#fff" text-anchor="middle">&#10006; INSECURE</text>
  <text x="26" y="90" font-size="12" fill="#333">&#8226; Predictable reset tokens (sequential,</text>
  <text x="34" y="106" font-size="12" fill="#333">  timestamp-based)</text>
  <text x="26" y="122" font-size="12" fill="#333">&#8226; Reset link never expires</text>
  <text x="26" y="138" font-size="12" fill="#333">&#8226; Token sent in URL (logged in server logs,</text>
  <text x="34" y="154" font-size="12" fill="#333">  referrer headers)</text>
  <text x="26" y="170" font-size="12" fill="#333">&#8226; Security questions with guessable answers</text>
  <text x="26" y="186" font-size="12" fill="#333">&#8226; Password sent via email in plaintext</text>
  <text x="26" y="202" font-size="12" fill="#333">&#8226; No rate limiting on reset requests</text>
  <!-- SECURE column -->
  <rect x="342" y="44" width="304" height="240" rx="4" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5"/>
  <rect x="342" y="44" width="304" height="28" rx="4" fill="#2e7d32"/>
  <text x="494" y="63" font-size="13" font-weight="bold" fill="#fff" text-anchor="middle">&#10004; SECURE</text>
  <text x="354" y="90" font-size="12" fill="#333">&#8226; Cryptographically random reset tokens</text>
  <text x="362" y="106" font-size="12" fill="#333">  (256-bit)</text>
  <text x="354" y="122" font-size="12" fill="#333">&#8226; Short expiration (15–30 minutes)</text>
  <text x="354" y="138" font-size="12" fill="#333">&#8226; Single use — invalidate after use</text>
  <text x="354" y="154" font-size="12" fill="#333">&#8226; Rate limit reset requests</text>
  <text x="354" y="170" font-size="12" fill="#333">&#8226; Notify user on all account changes</text>
  <text x="354" y="186" font-size="12" fill="#333">&#8226; Require re-authentication for sensitive</text>
  <text x="362" y="202" font-size="12" fill="#333">  changes</text>
</svg>

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
