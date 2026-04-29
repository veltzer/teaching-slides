---
tags:
  - security:oauth2
  - concepts:grants
level: intermediate
category: security
audience:
  - audiences:developers

---
# OAuth2 Grant Types

---
## What This Chapter Covers

- The full grant-type catalog
- Client Credentials for service-to-service
- Device Code for limited-input devices
- Why Implicit and Resource-Owner-Password are deprecated
- Choosing the right grant

---
## Grant Types Overview

- Authorization Code (with PKCE) — the default
- Client Credentials — service-to-service
- Device Authorization — TVs, CLIs
- Refresh Token — for token renewal
- Implicit — deprecated
- Resource Owner Password Credentials — deprecated

---
## Grant Selection Visualized

![grant_picker](svg/courses/networking/oauth2-and-oidc/04_grant_types/grant_picker.svg)

---
## Client Credentials Grant

- For machine-to-machine (no user)
- Client authenticates with its own credentials
- Receives an access token directly
- No refresh token (just request another)
- The right tool for backend service auth

---
## Client Credentials Request

```output
POST /token
Authorization: Basic base64(client_id:client_secret)
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
&scope=internal:read
```

- One round trip, no user
- Use for cron jobs, internal API calls, server-to-server

---
## When to Use Client Credentials

- Service-to-service inside your platform
- Backend pulling data from another backend
- Webhooks where the sender authenticates as itself
- Any non-user context
- Pair with mTLS at the network layer for defense in depth

---
## Device Authorization Grant

- For devices without a browser or with limited input
- Smart TVs, CLIs, IoT devices
- User completes auth on a separate device (phone)
- Device polls for authorization completion
- RFC 8628

---
## Device Flow Steps

- Device requests a device code
- Auth server returns device code, user code, verification URL
- Device displays the user code and URL
- User enters the code on their phone, authorizes
- Device polls and eventually gets a token

---
## Device Flow Example

```output
# Device gets:
device_code:    abc-xyz
user_code:      WDJB-MJHT
verification_uri: https://example.com/device

# Device shows:
"Visit example.com/device and enter WDJB-MJHT"

# Device polls /token until user finishes
```

---
## Refresh Token Grant

- Exchange a refresh token for a new access token
- Use when access token expires
- Refresh token may itself rotate (recommended)
- Most common alongside Authorization Code
- Sometimes alongside Client Credentials

---
## Refresh Token Request

```output
POST /token
grant_type=refresh_token
&refresh_token=tGzv3...
&client_id=app123
&client_secret=...
```

- Returns a new access token (and possibly a new refresh token)
- Old refresh token invalidated if rotation enabled

---
## Refresh Token Rotation

- Each use of a refresh token returns a new one
- Old token marked used; reuse triggers an alert
- Suspected theft: revoke the entire family
- Best practice in modern auth servers
- Especially valuable for SPAs and mobile

---
## Implicit Grant: Why Deprecated

- Token returned directly in the redirect URL
- Token in browser history, referer headers, server logs
- Cannot be authenticated (no client secret possible)
- Vulnerable to token leakage
- Replaced by Authorization Code + PKCE

---
## Implicit Grant Status

- Removed from OAuth 2.1 draft
- Major providers warn against new use
- Migrate existing apps to PKCE
- Some grandfathered support remains
- Don't add it to new projects in 2026

---
## Resource-Owner-Password: Why Deprecated

- Resource Owner Password Credentials
- App collects username/password directly
- Sends to auth server for tokens
- Defeats the whole point of OAuth2 (avoid sharing passwords)
- Should not exist in modern systems

---
## When Resource-Owner-Password Was Acceptable

- Migration from legacy systems
- Trusted first-party apps (your own iOS app)
- Now: even those should use Authorization Code + PKCE
- Never for third-party apps
- OAuth 2.1 removes it

---
## SAML Bearer Assertion Grant

- For migrating from SAML to OAuth2
- Trade a SAML assertion for an OAuth2 token
- Bridges enterprise SSO with modern APIs
- RFC 7522
- Niche but useful in enterprise

---
## JWT Bearer Assertion Grant

- Trade a signed JWT for an OAuth2 token
- Used for service accounts in many cloud platforms (Google, GitHub Apps)
- Client signs JWT with its private key
- Auth server verifies; issues access token
- Strong cryptographic identity, no shared secrets

---
## Token Exchange Grant

- RFC 8693
- Exchange one token for another
- Useful for delegation, impersonation
- "I have token A; give me token B for service Y"
- Building block for advanced architectures

---
## Choosing a Grant

- User logs in via browser → Authorization Code + PKCE
- Backend calling backend → Client Credentials
- TV/CLI → Device Authorization
- SPA / mobile → Authorization Code + PKCE (NEVER Implicit)
- Token refresh → Refresh Token

---
## Grant Type Decision Tree

- Is there a user involved? No → Client Credentials
- Yes user, has browser? Yes → Authorization Code + PKCE
- Yes user, no browser? → Device Authorization
- Need a new token? → Refresh Token
- Anything else: review carefully

---
## Anti-Patterns to Avoid

- Using Resource-Owner-Password for "convenience"
- Using Implicit because "we always have"
- Storing client secrets in mobile apps
- Reusing one access token for both user and service contexts
- Skipping PKCE because the client is "confidential enough"

---
## Migration Path

- Deprecate Implicit/Resource-Owner-Password by date
- Audit existing clients
- Move to Authorization Code + PKCE
- Communicate the timeline clearly
- Some flows may need re-architecting (BFF pattern)

---
## Multiple Grants Per Client

- A client can have several grant types enabled
- Match the grants to the contexts where the client runs
- Restrict at the auth server — least privilege
- Audit which grants each client uses
- Reduce attack surface

---
## Operational Concerns

- Monitor failed token requests per grant
- Alert on Implicit grant usage if you've deprecated it
- Track refresh token rotation health
- Watch for refresh token reuse alerts
- Set tight rate limits on the token endpoint

---
## Summary

- Authorization Code + PKCE: the modern default
- Client Credentials: machine-to-machine
- Device Authorization: limited-input devices
- Refresh Token: renew access tokens
- Implicit and Resource-Owner-Password: avoid; deprecated
- Match the grant to the context, not vice versa
