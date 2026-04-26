---
tags:
  - concepts:api
  - concepts:security
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Authentication and Security

---
## Authentication vs Authorization

- **Authentication** (AuthN): who is making the request?
- **Authorization** (AuthZ): may they do this?
- Both happen on every request; both are server-side
- The client doesn't enforce either — only suggests intent

---
## API Keys

- A simple shared secret
- Sent in a header: `Authorization: Bearer api-key-abc123`
- Easy to implement, easy to leak
- Useful for server-to-server, less for end-user authentication

---
## API Key Limitations

- A leaked key is a permanent breach until rotated
- No expiration by default
- No fine-grained scopes
- No way to attribute action to a real user
- Use API keys, but don't rely on them alone for sensitive APIs

---
## OAuth 2.0

- A framework for delegated authorization
- The user authorizes the app (third-party client) to access their resources
- The app gets a token; the API checks the token
- Industry standard for user-permitted access

---
## OAuth Flows

- **Authorization Code**: web apps; user logs in, app gets a code, exchanges for token
- **Authorization Code with PKCE**: mobile and SPA apps; same idea, more secure
- **Client Credentials**: server-to-server (no user)
- **Device Code**: TVs, CLIs without browsers
- **Refresh Token**: get a new access token without re-authenticating

---
## OpenID Connect (OIDC)

- An identity layer on top of OAuth 2.0
- Adds an `id_token` (JWT) with user identity claims
- Common stack: OAuth 2.0 for authorization + OIDC for authentication

---
## JWT Tokens

- JSON Web Token: a signed (sometimes encrypted) JSON payload
- Three parts: header, payload, signature (base64-url encoded, dot-separated)
- The payload contains claims (user id, expiration, scopes)
- The signature lets the API verify the token without a database lookup

---
## JWT Anatomy

```
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1MSIsImV4cCI6MTczNzAwMDAwMH0.signature
```

- Header: algorithm and type
- Payload: claims (sub, exp, iat, scopes, etc.)
- Signature: HMAC or RSA over header + payload

---
## JWT Caveats

- JWTs cannot be revoked easily — use short expiry + refresh tokens
- Storing JWTs in browser localStorage is XSS-risky
- httpOnly cookies are better for browser-based apps
- Don't put sensitive data in the payload — it's just base64, anyone can read it

---
## Scopes and Permissions

- A scope is a named permission: `read:orders`, `write:orders`, `admin:users`
- Tokens carry the scopes the user granted
- The API checks scopes on each endpoint
- Coarse scopes lead to over-permissioned tokens; very fine scopes burden the user

---
## Authorization at the API

- Every endpoint declares what scope/role/permission it requires
- Middleware checks the token has it
- Returns 403 if not — different from 401 (no token at all)
- The resource owner check is separate: scope says "can edit orders", but does this user own this order?

---
## Transport Security

- HTTPS everywhere — even between internal services
- Mutual TLS (mTLS) for service-to-service in zero-trust networks
- HSTS header tells browsers to always use HTTPS
- TLS 1.2 minimum; prefer TLS 1.3

---
## CORS

- Browsers enforce same-origin policy by default
- For cross-origin API calls, the server returns CORS headers
- Be explicit: which origins, which methods, which headers
- Don't use `Access-Control-Allow-Origin: *` for authenticated APIs

---
## CSRF

- Relevant for cookie-authenticated APIs called from browsers
- Mitigations: SameSite cookies, CSRF tokens, double-submit cookies
- Token-authenticated APIs (Bearer header) don't have this problem
- Browser-facing APIs need explicit CSRF design

---
## Common Vulnerabilities

- Broken authentication (predictable tokens, weak secrets)
- Broken authorization (IDOR — accessing /users/43 when you're user 42)
- Mass assignment (POST sets fields the user shouldn't control)
- Excessive data exposure (returning more than the consumer needs)
- Unrestricted resource consumption (no pagination, no rate limit)

---
## OWASP API Security Top 10

- A widely-used checklist
- Updated every few years
- Run through it during API design reviews
- The 10 items align well with this chapter

---
## Summary

- AuthN: who; AuthZ: may they
- OAuth + OIDC for user-permitted access
- JWT for stateless tokens; short-lived plus refresh
- Scopes coarse enough to be usable, fine enough to be safe
- HTTPS, CORS, CSRF, OWASP Top 10 — all baseline
