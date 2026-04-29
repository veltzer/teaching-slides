---
tags:
  - security:oauth2
  - security:pkce
level: intermediate
category: security
audience:
  - audiences:developers

---
# Authorization Code Flow with PKCE

---
## What This Chapter Covers

- The Authorization Code flow step-by-step
- Why an intermediate code instead of a token
- PKCE: what, why, how
- Implementation walkthrough
- Common pitfalls

---
## Why Authorization Code?

- The most secure OAuth2 flow
- Code is exchanged for tokens server-to-server
- Tokens never travel through the user agent's URL
- Browser history and referer don't leak tokens
- The recommended default for almost all clients

---
## Authorization Code Flow Visualized

![authcode_flow](svg/courses/networking/oauth2-and-oidc/03_authcode_pkce/authcode_flow.svg)

---
## Step 1: Authorization Request

```output
GET /authorize
    ?response_type=code
    &client_id=app123
    &redirect_uri=https://app.example.com/callback
    &scope=read:profile
    &state=abc123
    &code_challenge=hashed_value
    &code_challenge_method=S256
```

- Browser redirect; the user sees the auth server's login UI
- All parameters carried in the URL

---
## Step 2: User Consent

- Auth server authenticates the user (login form, MFA)
- Shows consent screen with requested scopes
- User clicks "Allow" or "Deny"
- Decision is recorded; the user is sent back

---
## Step 3: Code Returned

- Auth server redirects back to the client's `redirect_uri`
- Adds `?code=AUTHCODE&state=abc123`
- The code is short-lived (60s typical)
- Single-use — exchange it once
- The state is verified by the client

---
## Step 4: Token Exchange

```output
POST /token
Authorization: Basic base64(client_id:client_secret)

grant_type=authorization_code
&code=AUTHCODE
&redirect_uri=https://app.example.com/callback
&code_verifier=original_value
```

- Server-to-server; no browser involved
- Authenticated with client credentials and PKCE verifier

---
## Step 5: Tokens Received

```output
{
  "access_token": "eyJhbGciOi...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "tGzv3...",
  "scope": "read:profile"
}
```

- Tokens are now in the client's possession
- The code is consumed and cannot be reused

---
## Step 6: Using the Access Token

```output
GET /api/profile
Authorization: Bearer eyJhbGciOi...
```

- Client sends each API request with the bearer token
- Resource server validates and authorizes
- Token expires; client refreshes when needed

---
## Why Not Just Tokens in the Redirect?

- The deprecated Implicit flow did this
- Tokens land in browser URL, history, server logs
- Cannot be revoked easily after leak
- No client authentication on retrieval
- Authorization Code with PKCE replaces Implicit entirely

---
## What Is PKCE?

- Proof Key for Code Exchange
- Pronounced "pixie"
- RFC 7636
- Adds a per-request secret to the code exchange
- Designed for public clients but recommended for all

---
## Why PKCE?

- Public clients (SPA, mobile) can't keep a secret
- An attacker intercepting the code can't redeem it without the verifier
- Defends against authorization code interception
- Protects even confidential clients
- Cheap to implement; high security value

---
## How PKCE Works

- Client generates a random `code_verifier`
- Computes `code_challenge = SHA256(code_verifier)`
- Sends `code_challenge` + method on `/authorize`
- Sends raw `code_verifier` on `/token`
- Server hashes verifier and compares — must match

---
## PKCE Visualized

![pkce_flow](svg/courses/networking/oauth2-and-oidc/03_authcode_pkce/pkce_flow.svg)

---
## code_verifier Properties

- Random string, 43-128 chars
- URL-safe characters: `[A-Z][a-z][0-9]-._~`
- High entropy (use a CSPRNG)
- Different per authorization request
- Forgotten after use

---
## code_challenge_method

- `S256` — SHA-256 hash, base64url-encoded (recommended)
- `plain` — verifier sent as-is (for legacy only; avoid)
- Always use S256 in new implementations
- Servers should reject plain unless legacy clients exist

---
## Implementing PKCE (Pseudocode)

```python
verifier = base64url(random_bytes(32))
challenge = base64url(sha256(verifier))

# 1. Send challenge with /authorize
auth_url = build_url(
    challenge=challenge,
    method="S256"
)

# 2. Send verifier with /token
token = exchange_code(code, verifier)
```

---
## Storing the Verifier

- Browser session: `sessionStorage`
- Native app: secure storage (Keychain, Keystore)
- Never in cookies (XSRF surface)
- Discard after the token is received
- Don't log it

---
## State Parameter Reminder

- PKCE doesn't replace `state`
- State prevents CSRF on the authorize endpoint
- PKCE prevents authorization code interception
- Use both, always
- Yes, both — they protect against different attacks

---
## When to Use This Flow

- Web apps with a backend (confidential client)
- SPAs (public client + PKCE)
- Mobile apps (public client + PKCE)
- Desktop apps with embedded browser
- Default for almost everything modern

---
## Refresh Tokens

- Long-lived; used to get new access tokens
- Sent to the token endpoint with `grant_type=refresh_token`
- Should be rotated on each use (RFC 6749 + best practices)
- Stored carefully — leaking is worse than access token leak
- Bind to client; refuse cross-client reuse

---
## Common Pitfalls

- Using Implicit flow in 2026 (deprecated)
- PKCE on confidential clients omitted (do it anyway)
- code_challenge_method=plain instead of S256
- Reusing the verifier across requests
- Forgetting to validate state

---
## Browser-Only Considerations

- SPAs should use the BFF (Backend For Frontend) pattern when possible
- Tokens stored in browser are at XSS risk
- Backend can hold tokens; SPA uses session cookies
- Mobile apps: store in OS-provided secure storage
- Don't put tokens in localStorage casually

---
## Mobile-Specific

- Use system browser, not embedded webview
- Custom URL schemes can be hijacked
- App Links / Universal Links are safer
- Use AppAuth library where available
- PKCE is mandatory

---
## Testing the Flow

- Browser dev tools to inspect the redirect chain
- Token endpoint via curl with the captured code
- Decode the resulting access token (if JWT)
- Hit the resource server with the token
- Confirm scopes match what was requested

---
## Summary

- Authorization Code is the recommended flow
- PKCE adds a per-request secret to defeat code interception
- State + PKCE: both, always
- Implicit flow is dead; don't use it
- For SPAs and mobile, PKCE is non-negotiable
