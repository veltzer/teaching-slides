# Authentication Technologies & Design Flaws

## Day 2: Breaking and Securing Login Mechanisms

---

## Day 2 Overview

| Session | Topic |
|---------|-------|
| Morning Part 1 | Authentication technologies & design flaws |
| Morning Part 2 | Brute-forcing & implementation flaws |
| Afternoon Part 1 | Securing authentication |
| Afternoon Part 2 | Session management attacks |
| Late Afternoon | SQL injection basics |

---

## Authentication Fundamentals

**Authentication** = Verifying "Who are you?"
**Authorization** = Verifying "What can you do?"

```misc
Three factors of authentication:
1. Something you KNOW    (password, PIN)
2. Something you HAVE    (phone, hardware key, smart card)
3. Something you ARE     (fingerprint, face, retina)

Multi-Factor Authentication (MFA):
  Combining 2+ factors from DIFFERENT categories

  Password + SMS code = 2FA (weak - SIM swap)
  Password + TOTP app = 2FA (better)
  Password + Hardware key = 2FA (strongest)
```

---

## Authentication Technologies

| Technology | Mechanism | Common In |
|-----------|-----------|-----------|
| **Form-based** | Username/password via HTML form | Most web apps |
| **HTTP Basic** | Base64 credentials in header | APIs, legacy |
| **HTTP Digest** | Challenge-response | Legacy systems |
| **Token-based** | `JWT`, API keys | Modern APIs |
| **OAuth 2.0** | Delegated authorization | Social login |
| **SAML** | XML-based SSO | Enterprise |
| **OpenID Connect** | Identity layer on OAuth | Google, Microsoft |
| **Certificate** | Client TLS certificates | High security |
| **Kerberos** | Ticket-based | Windows/AD |

---

## Form-Based Authentication

```html
<!-- Standard login form -->
<form action="/login" method="POST">
  <input type="text" name="username">
  <input type="password" name="password">
  <input type="hidden" name="csrf_token" value="abc123">
  <button type="submit">Login</button>
</form>
```

```http
POST /login HTTP/1.1
Host: target.com
Content-Type: application/x-www-form-urlencoded

username=admin&password=secret123&csrf_token=abc123
```

- Most common authentication method
- Credentials sent in POST body
- Relies on `HTTPS` for transport security

---

## HTTP Basic Authentication

```http
# How it works:
1. Client requests protected resource
2. Server responds: 401 + WWW-Authenticate: Basic
3. Client sends: Authorization: Basic base64(user:pass)

# Example
Authorization: Basic YWRtaW46cGFzc3dvcmQ=
# Decodes to: admin:password

# Security issues:
- Credentials sent with EVERY request
- Only Base64 encoded (NOT encrypted)
- No logout mechanism (cached in browser)
- No brute-force protection built-in
- Must use HTTPS to be even remotely safe
```

---

## Token-Based Authentication (JWT)

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="240" viewBox="0 0 660 240">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>
  <rect width="660" height="240" fill="#f0f4f8" rx="4" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="24" font-family="sans-serif" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">JSON Web Token (JWT) Structure</text>
  <!-- structure -->
  <rect x="20" y="38" width="140" height="36" fill="#e3f2fd" rx="4" stroke="#1565c0" stroke-width="1.5"/>
  <text x="90" y="52" font-family="sans-serif" font-size="12" font-weight="bold" fill="#1565c0" text-anchor="middle">Header</text>
  <text x="90" y="67" font-family="sans-serif" font-size="10" fill="#555" text-anchor="middle">{"alg":"HS256","typ":"JWT"}</text>
  <text x="168" y="61" font-family="sans-serif" font-size="16" fill="#999" text-anchor="middle">.</text>
  <rect x="175" y="38" width="310" height="36" fill="#e8f5e9" rx="4" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="330" y="52" font-family="sans-serif" font-size="12" font-weight="bold" fill="#2e7d32" text-anchor="middle">Payload</text>
  <text x="330" y="67" font-family="sans-serif" font-size="10" fill="#555" text-anchor="middle">{"sub":"1234","name":"John","role":"user","exp":1700000000}</text>
  <text x="493" y="61" font-family="sans-serif" font-size="16" fill="#999" text-anchor="middle">.</text>
  <rect x="500" y="38" width="140" height="36" fill="#fff3e0" rx="4" stroke="#e65100" stroke-width="1.5"/>
  <text x="570" y="52" font-family="sans-serif" font-size="12" font-weight="bold" fill="#e65100" text-anchor="middle">Signature</text>
  <text x="570" y="67" font-family="sans-serif" font-size="10" fill="#555" text-anchor="middle">HMACSHA256(header.payload)</text>
  <!-- flow -->
  <rect x="30" y="105" width="170" height="50" fill="#e3f2fd" rx="4" stroke="#333" stroke-width="1.5"/>
  <text x="115" y="127" font-family="sans-serif" font-size="13" font-weight="bold" fill="#222" text-anchor="middle">1. Login</text>
  <text x="115" y="145" font-family="sans-serif" font-size="12" fill="#555" text-anchor="middle">with credentials</text>
  <line x1="200" y1="130" x2="238" y2="130" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="240" y="105" width="170" height="50" fill="#e8f5e9" rx="4" stroke="#333" stroke-width="1.5"/>
  <text x="325" y="127" font-family="sans-serif" font-size="13" font-weight="bold" fill="#222" text-anchor="middle">2. Get JWT</text>
  <text x="325" y="145" font-family="sans-serif" font-size="12" fill="#555" text-anchor="middle">token from server</text>
  <line x1="410" y1="130" x2="448" y2="130" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="450" y="105" width="180" height="50" fill="#fff3e0" rx="4" stroke="#333" stroke-width="1.5"/>
  <text x="540" y="127" font-family="sans-serif" font-size="13" font-weight="bold" fill="#222" text-anchor="middle">3. Send JWT</text>
  <text x="540" y="145" font-family="sans-serif" font-size="12" fill="#555" text-anchor="middle">with every request</text>
  <text x="330" y="195" font-family="sans-serif" font-size="12" fill="#555" text-anchor="middle">Stateless: server verifies signature without storing session state</text>
</svg>

---

## JWT Security Issues

```python
# Attack 1: Algorithm confusion (none algorithm)
# Change header to: {"alg":"none","typ":"JWT"}
# Remove signature
# Result: header.payload.  (empty signature)

# Attack 2: HS256 vs RS256 confusion
# If server uses RS256 (asymmetric), change to HS256
# Sign with the PUBLIC key (which attacker knows)
# Server verifies HMAC with public key = valid!

# Attack 3: Weak secret brute-force
# Using hashcat:
hashcat -a 0 -m 16500 jwt.txt wordlist.txt

# Attack 4: Modify payload without re-signing
# Some implementations don't verify signature!

# Defense: Always verify algorithm, use strong secrets
```

---

## OAuth 2.0 Flow

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="310" viewBox="0 0 660 310">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
    <marker id="arr2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#2e7d32"/>
    </marker>
  </defs>
  <rect width="660" height="310" fill="#f0f4f8" rx="4" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="24" font-family="sans-serif" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">OAuth 2.0 Authorization Code Flow</text>
  <!-- boxes -->
  <rect x="30" y="45" width="130" height="50" fill="#e3f2fd" rx="4" stroke="#1565c0" stroke-width="1.5"/>
  <text x="95" y="67" font-family="sans-serif" font-size="13" font-weight="bold" fill="#1565c0" text-anchor="middle">User Browser</text>
  <rect x="500" y="45" width="130" height="50" fill="#e8f5e9" rx="4" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="565" y="67" font-family="sans-serif" font-size="13" font-weight="bold" fill="#2e7d32" text-anchor="middle">Auth Server</text>
  <rect x="30" y="195" width="130" height="50" fill="#fff3e0" rx="4" stroke="#e65100" stroke-width="1.5"/>
  <text x="95" y="215" font-family="sans-serif" font-size="13" font-weight="bold" fill="#e65100" text-anchor="middle">App Server</text>
  <!-- lifelines -->
  <line x1="95" y1="95" x2="95" y2="195" stroke="#888" stroke-width="1" stroke-dasharray="4,3"/>
  <line x1="565" y1="95" x2="565" y2="280" stroke="#888" stroke-width="1" stroke-dasharray="4,3"/>
  <line x1="95" y1="245" x2="95" y2="280" stroke="#888" stroke-width="1" stroke-dasharray="4,3"/>
  <!-- step 1 -->
  <line x1="95" y1="112" x2="555" y2="112" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="325" y="108" font-family="sans-serif" font-size="11" fill="#333" text-anchor="middle">1. Click "Login with Google" → redirect to Auth Server</text>
  <!-- step 2 -->
  <line x1="555" y1="140" x2="105" y2="140" stroke="#2e7d32" stroke-width="1.5" marker-end="url(#arr2)"/>
  <text x="325" y="136" font-family="sans-serif" font-size="11" fill="#2e7d32" text-anchor="middle">2. User authenticates &amp; consents → redirect with code</text>
  <!-- step 3 -->
  <line x1="95" y1="165" x2="105" y2="193" stroke="#555" stroke-width="1" stroke-dasharray="3,2"/>
  <line x1="105" y1="220" x2="555" y2="220" stroke="#e65100" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="325" y="216" font-family="sans-serif" font-size="11" fill="#e65100" text-anchor="middle">3. App Server exchanges code for Access Token</text>
  <line x1="555" y1="240" x2="115" y2="240" stroke="#e65100" stroke-width="1.5" marker-end="url(#arr2)"/>
  <text x="325" y="254" font-family="sans-serif" font-size="11" fill="#333" text-anchor="middle">← Access Token</text>
  <!-- step 4 -->
  <text x="95" y="280" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">4. Use Access Token to call APIs / GET /api/userinfo</text>
</svg>

---

## OAuth 2.0 Attack Vectors

```misc
1. Open Redirect in redirect_uri
   # Steal authorization code
   redirect_uri=https://attacker.com/callback

2. CSRF - Missing state parameter
   # Force victim to link attacker's account

3. Authorization Code Interception
   # If not using PKCE

4. Token Leakage via Referer header
   # Token in URL fragment leaked to third parties

5. Scope escalation
   # Request more permissions than intended

6. Implicit flow token theft
   # Tokens in URL fragments are exposed
```

---

## Common Authentication Design Flaws

```misc
1. Weak Password Policy
   - No minimum length
   - No complexity requirements
   - No breach database checking

2. Verbose Error Messages
   WRONG: "Invalid password for user admin"
   RIGHT: "Invalid username or password"

3. No Account Lockout
   - Unlimited login attempts
   - No rate limiting
   - No CAPTCHA after failures

4. Insecure Password Reset
   - Predictable reset tokens
   - No expiration on reset links
   - Security questions with guessable answers
```

---

## Username Enumeration

```bash
# Timing-based enumeration
# Valid user: Server checks password (slow)
# Invalid user: Server rejects immediately (fast)

# Via login form
# "Invalid password" -> user exists
# "Invalid username or password" -> ambiguous (good)
# "Account not found" -> user doesn't exist

# Via registration
# "Email already registered" -> user exists

# Via password reset
# "Reset link sent to your email" (always) -> good
# "No account with that email" -> enumeration!

# Automated enumeration
ffuf -u http://target.com/login \
  -X POST -d "username=FUZZ&password=test" \
  -w /usr/share/seclists/Usernames/top-usernames-shortlist.txt \
  -fr "Invalid username"  # Filter responses with this text
```

---

## Password Reset Vulnerabilities

```misc
Attack 1: Predictable Reset Tokens
  https://target.com/reset?token=user123_20240115_001
  # Token contains: username + date + counter
  # Easy to predict!

Attack 2: Token Reuse
  # Token not invalidated after use
  # Attacker can use same link multiple times

Attack 3: Host Header Poisoning
  POST /forgot-password HTTP/1.1
  Host: attacker.com         # <-- Poisoned

  # Reset email contains:
  # https://attacker.com/reset?token=abc123
  # Victim clicks -> token sent to attacker

Attack 4: No Rate Limiting on Reset
  # Brute-force short numeric reset codes
```

---

## Multi-Factor Authentication Bypass

```misc
MFA Bypass Techniques:

1. Skip the MFA step entirely
   # After login, go directly to /dashboard
   # Instead of /mfa-verify

2. Brute-force the MFA code
   # 6-digit code = 1,000,000 combinations
   # No rate limiting? Brute-force in minutes

3. Response manipulation
   # Change {"success":false} to {"success":true}

4. Backup codes
   # Often simpler, may not be rate-limited

5. SIM swapping (for SMS-based MFA)
   # Social engineer the mobile carrier

6. Session fixation before MFA
   # Session already partially authenticated
```

---

## Remember Me Functionality

```python
# VULNERABLE: Predictable remember-me token
remember_token = base64_encode(username + ":" + md5(password))
# Attacker can reconstruct this if they know password hash

# VULNERABLE: Permanent token, never expires
Set-Cookie: remember_me=abc123; Expires=Thu, 01 Jan 2099

# VULNERABLE: Token reveals user info
Set-Cookie: remember_me=admin_1705276800
# Contains username and timestamp

# SECURE implementation:
import secrets
token = secrets.token_urlsafe(32)
# Store hash of token in database
# Set reasonable expiration (30 days)
# Invalidate on password change
# Allow users to see/revoke active sessions
```

---

## Lab Exercise: Authentication Testing

**Target**: DVWA - Brute Force module

1. Set DVWA security to "Low"
1. Intercept login request in Burp
1. Identify username enumeration
1. Note error message differences
1. Test for account lockout (there is none)
1. Prepare for brute-force attacks

```bash
# Quick test
curl -v http://localhost:8080/vulnerabilities/brute/ \
  -b "PHPSESSID=your_session; security=low" \
  -d "username=admin&password=test&Login=Login"
```

---

## Kerberos Authentication

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="330" viewBox="0 0 660 330">
  <rect width="660" height="330" fill="#f0f4f8" rx="4" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="24" font-family="sans-serif" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">Kerberos Flow (Windows / AD Environments)</text>
  <!-- flow steps -->
  <rect x="20" y="38" width="300" height="150" fill="#e3f2fd" rx="4" stroke="#1565c0" stroke-width="1"/>
  <text x="30" y="60" font-family="sans-serif" font-size="13" font-weight="bold" fill="#1565c0">Authentication Flow</text>
  <text x="30" y="80" font-family="sans-serif" font-size="12" fill="#222">1. User → KDC: "I am user X" (AS-REQ)</text>
  <text x="30" y="98" font-family="sans-serif" font-size="12" fill="#222">2. KDC → User: Ticket Granting Ticket (AS-REP)</text>
  <text x="30" y="116" font-family="sans-serif" font-size="12" fill="#222">3. User → KDC: TGT + "Access Service Y" (TGS-REQ)</text>
  <text x="30" y="134" font-family="sans-serif" font-size="12" fill="#222">4. KDC → User: Service Ticket (TGS-REP)</text>
  <text x="30" y="152" font-family="sans-serif" font-size="12" fill="#222">5. User → Service: Service Ticket (AP-REQ)</text>
  <text x="30" y="170" font-family="sans-serif" font-size="12" fill="#222">6. Service → User: Access granted (AP-REP)</text>
  <!-- attacks -->
  <rect x="340" y="38" width="300" height="150" fill="#ffebee" rx="4" stroke="#c62828" stroke-width="1"/>
  <text x="350" y="60" font-family="sans-serif" font-size="13" font-weight="bold" fill="#c62828">Known Attacks</text>
  <text x="350" y="80" font-family="sans-serif" font-size="12" fill="#222">AS-REP Roasting: Request TGT, crack offline</text>
  <text x="350" y="98" font-family="sans-serif" font-size="12" fill="#222">Kerberoasting: Request svc tickets, crack offline</text>
  <text x="350" y="116" font-family="sans-serif" font-size="12" fill="#222">Golden Ticket: Forge TGTs with krbtgt hash</text>
  <text x="350" y="134" font-family="sans-serif" font-size="12" fill="#222">Silver Ticket: Forge service tickets with svc hash</text>
  <text x="350" y="152" font-family="sans-serif" font-size="12" fill="#222">Pass-the-Ticket: Reuse stolen tickets</text>
  <!-- legend -->
  <rect x="20" y="205" width="620" height="50" fill="#fff9c4" rx="4" stroke="#f57f17" stroke-width="1"/>
  <text x="330" y="225" font-family="sans-serif" font-size="12" font-weight="bold" fill="#f57f17" text-anchor="middle">Key Components</text>
  <text x="330" y="245" font-family="sans-serif" font-size="12" fill="#555" text-anchor="middle">KDC (Key Distribution Center) contains: AS (Authentication Service) + TGS (Ticket Granting Service)</text>
</svg>

---

## SAML Authentication

```xml
<!-- SAML is used for Single Sign-On (SSO) -->
<!-- IdP sends signed assertion to Service Provider -->

<saml:Assertion>
  <saml:Issuer>https://idp.company.com</saml:Issuer>
  <saml:Subject>
    <saml:NameID>john@company.com</saml:NameID>
  </saml:Subject>
  <saml:Conditions>
    <saml:AudienceRestriction>
      <saml:Audience>https://app.company.com</saml:Audience>
    </saml:AudienceRestriction>
  </saml:Conditions>
  <saml:AttributeStatement>
    <saml:Attribute Name="role">
      <saml:AttributeValue>admin</saml:AttributeValue>
    </saml:Attribute>
  </saml:AttributeStatement>
</saml:Assertion>

<!-- Attacks: XML signature wrapping, assertion manipulation -->
```

---

## API Key Authentication

```http
# API keys are simple but have significant risks

# In header (recommended)
GET /api/data HTTP/1.1
Authorization: Bearer sk_live_abc123def456
X-API-Key: abc123def456

# In URL parameter (NOT recommended - logged/cached)
GET /api/data?api_key=abc123def456

# Common API key mistakes:
# 1. Hardcoded in client-side JavaScript
# 2. Committed to version control (Git)
# 3. No rotation policy
# 4. Same key for all permission levels
# 5. No rate limiting per key
# 6. Keys don't expire

# Defense:
# - Store in environment variables
# - Rotate regularly
# - Scope keys to minimum permissions
# - Monitor usage patterns
```

---

## Certificate-Based Authentication

```misc
Client Certificate Authentication (mTLS):

  1. Server requests client cert during TLS handshake
  2. Client presents its X.509 certificate
  3. Server validates against trusted CA
  4. Server extracts identity from certificate CN/SAN
  5. Access granted based on certificate identity

Advantages:
  - No passwords to steal or brute-force
  - Mutual authentication (both sides verified)
  - Certificate revocation possible via CRL/OCSP

Disadvantages:
  - Complex key management and distribution
  - Private key theft = impersonation
  - User experience challenges
```

---

## Summary

- Authentication is the first line of defense
- Multiple technologies exist, each with unique attack vectors
- `JWT` tokens must be properly validated (algorithm, signature, claims)
- `OAuth` 2.0 misconfigurations enable account takeover
- Username enumeration is a common and underestimated flaw
- Password reset mechanisms are frequently vulnerable
- MFA can be bypassed if not properly implemented

> Next: Brute-Forcing & Implementation Flaws
