---
tags:
  - security:oauth2
  - concepts:tokens
level: intermediate
category: security
audience:
  - audiences:developers

---
# Tokens: Access, Refresh, and ID

---
## What This Chapter Covers

- The three token types and their roles
- Token formats: opaque vs JWT
- Validation strategies
- Storage in different client types
- Revocation and introspection

---
## Three Token Types

- Access token — authorizes API calls
- Refresh token — renews access tokens
- ID token — carries user identity (OIDC only)
- Each has different lifetime and use
- Mixing them up is a common bug

---
## Access vs Refresh

![token_lifecycle](svg/courses/networking/oauth2-and-oidc/05_tokens/token_lifecycle.svg)

---
## Access Token

- Short-lived (5-60 minutes typically)
- Sent to the resource server
- Bearer token in `Authorization: Bearer ...`
- Carries scopes and (optionally) identity
- Resource server doesn't need to call auth server (for JWT)

---
## Refresh Token

- Long-lived (hours to weeks)
- Used only at the token endpoint
- Never sent to the resource server
- Should rotate on each use
- Most sensitive — guard it carefully

---
## ID Token

- OIDC-specific
- A JWT with user identity claims
- Sent to the client (not used for API access)
- Verified by the client to authenticate the user
- Should never be used as an API access token

---
## Token Roles Visualized

![token_roles](svg/courses/networking/oauth2-and-oidc/05_tokens/token_roles.svg)

---
## Opaque Tokens

- Random strings; meaningless to anyone but the auth server
- Resource server must call `/introspect` to validate
- Easy to revoke (server keeps state)
- Network round-trip per request adds latency
- Caching introspection results helps

---
## JWT Tokens

- Self-contained; signed by the auth server
- Resource server validates signature locally
- No network call to the auth server per request
- Much higher throughput
- Revocation is harder (covered later)

---
## JWT Versus Opaque Comparison

![jwt_vs_opaque](svg/courses/networking/oauth2-and-oidc/05_tokens/jwt_vs_opaque.svg)

---
## Choosing Between Them

- High volume, low latency → JWT
- Strong revocation needs → opaque + introspection
- Cached introspection: hybrid
- Major providers usually offer both
- Mix per scope or per client if your stack supports it

---
## Token Lifetimes

- Access: 5-60 min (Google: 1h; AWS: 1h)
- Refresh: 24h to 30 days; rotation extends
- ID token: same as access typically
- Match to your security and UX trade-offs
- Shorter access + rotation refresh = strong default

---
## Token Storage Choices

![storage_choices](svg/courses/networking/oauth2-and-oidc/05_tokens/storage_choices.svg)

---
## Storage: Server-Side Apps

- Tokens in the server-side session store
- Browser only sees a session cookie
- Backend mints requests using the token
- The BFF (Backend For Frontend) pattern
- Most secure for SPAs and mobile

---
## Storage: SPAs

- Avoid `localStorage` (XSS reads it)
- Memory-only (lost on reload, but safe)
- httpOnly + Secure cookies via BFF (best)
- Consider using BFF and not handling tokens in the SPA
- If you must, accept the risk and document it

---
## Storage: Mobile

- iOS secure storage (key store)
- Android secure storage (key store + encrypted preferences)
- Never in plain shared preferences
- Use the platform OAuth library where possible
- Wipe on logout

---
## Storage: CLI Tools

- OS credential store (Linux secret service, macOS key store, Windows credential manager)
- File with strict permissions as a fallback
- Token refresh in the background
- Don't print tokens to logs
- Consider device authorization grant for the initial login

---
## Token Validation: JWT

- Verify signature using the auth server's public key
- Check `iss` (issuer), `aud` (audience), `exp` (expiration)
- Reject tokens with weak algorithms (alg=none)
- Cache JWKS but respect TTL
- Don't roll your own JWT library

---
## JWKS

- JSON Web Key Set
- Auth server publishes public keys at `/.well-known/jwks.json`
- Client/resource server fetches and caches
- Rotates keys; keys identified by `kid`
- Always look up by `kid` and re-fetch if missing

---
## Token Validation: Opaque

- Resource server calls `/introspect` (RFC 7662)
- POST with the token, basic auth as the resource server
- Response: `{"active": true, "scope": "...", "exp": ...}`
- Cache valid responses briefly
- Always check `active=true`

---
## Audience and Authorization

- `aud` claim says who the token is for
- Resource server must check it
- Tokens with the wrong audience must be rejected
- Cross-service token theft is mitigated by audience checking
- Often forgotten — check yours

---
## Scopes vs Permissions

- Scopes are coarse: `read:profile`, `write:posts`
- Permissions/roles are fine: "user 42 can edit post 7"
- Scopes pass through OAuth2; permissions live in your app
- Both are needed for full authorization
- Don't expect scopes alone to do fine-grained authz

---
## Revocation

- `/revoke` endpoint takes a token
- Marks it invalid going forward
- Refresh tokens must be revocable
- Access tokens (JWT) are tricky to revoke before expiration
- Short access token TTL limits damage

---
## Revoking JWTs

- Maintain a deny list of `jti` (JWT IDs)
- Resource server checks the deny list per request
- Erodes the JWT scaling advantage
- Alternative: short TTL + rotation
- Combine: short JWT TTL, deny-list for emergencies

---
## Token Introspection

- `/introspect` endpoint (RFC 7662)
- Resource server queries auth server about a token
- Useful for opaque tokens; possible for JWT too
- Authenticated as the resource server
- Returns active/inactive, scope, claims

---
## Refresh Token Rotation Details

- New refresh token returned with each use
- Old token invalidated immediately
- Reuse of old token = client compromised
- Server revokes all tokens in the family
- Security best practice; some providers default-on

---
## Token Binding (Future)

- Bind tokens to client TLS keys
- Theft alone insufficient — need the key too
- Limited deployment; standardization in flux
- Closely related: Demonstrating-Proof-of-Possession
- Strongest mitigation for token theft

---
## Proof-of-Possession

- A way to bind a token to a holder's key
- Client signs each request with its key
- Resource server verifies — the token plus the proof
- Defeats simple token theft
- Adoption growing in financial APIs

---
## Common Pitfalls

- Treating ID tokens as access tokens
- Forgetting to validate `aud`
- Storing tokens in cookies without httpOnly + Secure
- No revocation strategy
- Long-lived access tokens (>1h without good reason)

---
## Summary

- Three token types; each has a specific role
- Opaque vs JWT: revocation vs scaling trade-off
- Validate signatures, issuer, audience, expiration
- Storage depends on client type — never localStorage if you can avoid it
- Refresh token rotation is the modern best practice
