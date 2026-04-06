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

```diagram
JSON Web Token structure:
header.payload.signature

Header:  {"alg":"HS256","typ":"JWT"}
Payload: {"sub":"1234","name":"John","role":"user","exp":1700000000}
Signature: HMACSHA256(base64(header) + "." + base64(payload), secret)

+----------+     +---------+     +----------+
| 1. Login | --> | 2. Get  | --> | 3. Send  |
| with     |     | JWT     |     | JWT with |
| creds    |     | token   |     | requests |
+----------+     +---------+     +----------+
```

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

```diagram
+--------+                               +----------+
| User   |                               | Auth     |
| Browser|                               | Server   |
+---+----+                               +----+-----+
    |  1. Click "Login with Google"            |
    |---> App redirects to Auth Server ------->|
    |                                          |
    |  2. User authenticates & consents        |
    |<--- Auth Server redirects with code <----|
    |                                          |
+---+----+                               +----+-----+
| App    |  3. Exchange code for token    | Auth     |
| Server |------------------------------->| Server   |
|        |<---------- Access Token -------|          |
+---+----+                               +----------+
    |
    |  4. Use token to access resources
    |--->  GET /api/userinfo
```

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

```misc
Kerberos Flow (Windows/AD environments):
1. User -> KDC: "I am user X" (AS-REQ)
2. KDC -> User: Ticket Granting Ticket (AS-REP)
3. User -> KDC: TGT + "I want access to Service Y" (TGS-REQ)
4. KDC -> User: Service Ticket (TGS-REP)
5. User -> Service: Service Ticket (AP-REQ)
6. Service -> User: Access granted (AP-REP)

Attacks:
- AS-REP Roasting: Request TGT for users without pre-auth
- Kerberoasting: Request service tickets, crack offline
- Golden Ticket: Forge TGTs with krbtgt hash
- Silver Ticket: Forge service tickets with service hash
- Pass-the-Ticket: Reuse stolen tickets
```

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
