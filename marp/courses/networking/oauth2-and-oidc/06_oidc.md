---
tags:
  - security:oidc
  - concepts:identity
level: intermediate
category: security
audience:
  - audiences:developers

---
# OpenID Connect

---
## What This Chapter Covers

- What OIDC adds on top of OAuth2
- The ID token and standard claims
- Discovery and the well-known document
- UserInfo endpoint
- Logout patterns

---
## OIDC in One Sentence

- An identity layer on top of OAuth2 that lets clients verify the user's identity using a standardized ID token.

---
## Why OIDC?

- OAuth2 alone doesn't say who the user is
- "Login with X" needs identity, not just authorization
- OIDC standardizes: get an ID token alongside access token
- One protocol for authentication and authorization
- The de facto standard for federated login

---
## OIDC vs OAuth2 Visualized

![oidc_layer](svg/courses/networking/oauth2-and-oidc/06_oidc/oidc_layer.svg)

---
## What OIDC Adds

- ID token (a JWT) with user identity
- A standard `openid` scope to request it
- Standard claims: `sub`, `name`, `email`, `picture`
- A UserInfo endpoint
- Discovery via `.well-known/openid-configuration`

---
## The ID Token

- A JWT signed by the auth server
- Contains claims about the user's identity
- Sent to the client (not the resource server)
- Verified by the client to authenticate the user
- Lifetime usually matches the access token

---
## ID Token Claims

```json
{
  "iss": "https://auth.example.com",
  "sub": "248289761001",
  "aud": "client_id_xyz",
  "exp": 1703012400,
  "iat": 1703008800,
  "auth_time": 1703008800,
  "nonce": "abc123",
  "email": "alice@example.com"
}
```

---
## Required Claims

- `iss` — issuer URL of the auth server
- `sub` — unique user ID at the issuer
- `aud` — the client's `client_id`
- `exp` — expiration time
- `iat` — issued-at time
- Validate all of these, every time

---
## The sub Claim

- The user's unique identifier at the issuer
- Stable: doesn't change if the user changes their email
- Globally unique within an issuer
- Use `(iss, sub)` as the key in your DB
- Don't use `email` — it can change or be reused

---
## Claim Buckets

![oidc_claim_buckets](svg/courses/networking/oauth2-and-oidc/06_oidc/oidc_claim_buckets.svg)

---
## Standard Scopes

- `openid` — required, asks for an ID token
- `profile` — name, picture, etc
- `email` — email address
- `address` — postal address
- `phone` — phone number
- Pick what you need; least privilege

---
## Requesting an ID Token

- Add `openid` to the scope: `scope=openid profile email`
- The auth server includes an ID token in the token response
- Without `openid`, you only get an access token
- The presence of `openid` switches OAuth2 → OIDC

---
## Token Endpoint Response (OIDC)

```json
{
  "access_token": "eyJhbGc...",
  "id_token": "eyJhbGc...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "..."
}
```

- `id_token` is new compared to plain OAuth2
- Both tokens in one response

---
## Validating the ID Token

- Verify the JWT signature using JWKS
- Check `iss` matches the configured issuer
- Check `aud` matches your `client_id`
- Check `exp` is in the future
- Check `nonce` matches what you sent

---
## Validation Step Detail

![oidc_validation_steps](svg/courses/networking/oauth2-and-oidc/06_oidc/oidc_validation_steps.svg)

---
## The Nonce Parameter

- A random value the client generates
- Sent on `/authorize` with `nonce=abc123`
- Echoed in the ID token's `nonce` claim
- Defends against replay attacks
- Always use it (different from `state`)

---
## UserInfo Endpoint

- `/userinfo` — returns user claims for an access token
- Needed when you want claims not in the ID token
- Authenticated with the access token
- Useful for fetching fresh data
- Returns same claim format as the ID token

---
## When to Use UserInfo

- Get richer user profile after login
- ID tokens are often kept small; UserInfo carries more
- When user data may have changed since token issuance
- Periodic refresh of user data
- Scope-gated; only returns what was authorized

---
## Discovery

- `https://issuer/.well-known/openid-configuration`
- Returns JSON with all endpoints and capabilities
- Clients fetch once and configure
- Auth server changes propagate
- Standard across OIDC providers

---
## Discovery Document Example

```json
{
  "issuer": "https://auth.example.com",
  "authorization_endpoint": "...",
  "token_endpoint": "...",
  "jwks_uri": "...",
  "userinfo_endpoint": "...",
  "response_types_supported": ["code"],
  "id_token_signing_alg_values_supported": ["RS256"]
}
```

---
## OIDC Flows

- Authorization Code (default for web/mobile)
- Implicit (deprecated, like in OAuth2)
- Hybrid (returns code + ID token at the same time)
- Each tagged with `response_type` parameter
- Authorization Code is the right default

---
## Hybrid Flow

- `response_type=code id_token`
- Returns code + ID token immediately
- Client validates ID token before code exchange
- Useful when you need identity before extra round-trips
- Less common than pure code flow

---
## Front-Channel Logout

- Auth server includes iframes pointing to each client's logout endpoint
- Each client clears its session
- All happens in the user's browser
- Subject to browser limits and CSP
- Less reliable than back-channel

---
## Back-Channel Logout

- Auth server sends a server-to-server logout token to each client
- Client revokes its session
- More reliable than front-channel
- Requires clients to implement a logout endpoint
- The recommended modern logout

---
## End-Session Endpoint

- `end_session_endpoint` from discovery
- Client redirects to it to log out
- May redirect back to the client after logout
- `id_token_hint` parameter helps identify the session
- The user-initiated logout flow

---
## Session Management

- Session iframe spec for cross-tab session monitoring
- Polls auth server for session changes
- Less common in modern deployments
- Browsers tightening third-party cookie support is making this harder
- Often replaced by silent token refresh

---
## OIDC vs SAML

- SAML — older, XML-based, popular in enterprise
- OIDC — newer, JSON, popular in consumer
- SAML for B2B SSO with enterprise IdPs
- OIDC for modern apps and B2C
- Both standards in active use

---
## Common Pitfalls

- Treating the ID token as an access token (don't)
- Skipping `nonce` validation
- Trusting `email` as the user identifier (use `sub`)
- Not checking `aud` on the ID token
- Forgetting that `openid` scope is required

---
## Summary

- OIDC adds standard identity on top of OAuth2
- ID token (JWT) carries claims; verify it carefully
- `sub` is the user identifier; not `email`
- UserInfo endpoint for richer profiles
- Discovery makes provider integration uniform
