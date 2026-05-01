---
tags:
  - architecture:api-gateway
  - architecture:auth
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# Authentication and Authorisation

---
## What This Chapter Covers

- Auth at the gateway: why
- API keys, JWTs, OAuth 2.0
- Mutual TLS
- Token introspection
- Authorisation (RBAC, ABAC)
- Caching auth decisions
- Pitfalls

---
## Why At The Gateway

- One place to enforce auth, not N services
- Backends trust the gateway has done it
- Reduces surface area
- Centralised policy
- Failure mode: gateway misconfig &#8594; widespread impact

---
## API Keys

- Simple shared secret
- Header (`X-API-Key`) or query param
- Best for server-to-server; never for browser clients
- Easy to rotate; easy to leak
- Pair with rate limiting per key

---
## JWT (JSON Web Tokens)

- Self-contained; signed
- Header.Payload.Signature
- Gateway verifies signature; trusts claims
- Stateless: no DB lookup needed
- Most modern API standard

---
## JWT Verification

- Gateway has the public key (or JWKS endpoint)
- Verifies signature
- Checks expiry, issuer, audience
- Extracts user info from claims
- Fast; per-request

---
## OAuth 2.0

- A framework for delegated authorisation
- Resource owner (user) gives token to client
- Client uses token to call API
- Many flows: authorisation code, client credentials, device, etc.
- Industry standard

---
## OAuth 2.0 Flows

- **Authorisation Code**: web apps; user redirected to authorise
- **Client Credentials**: service-to-service
- **Device Code**: TVs, IoT; "go to URL, enter code"
- **Implicit**: deprecated; don't use
- **PKCE**: hardened code flow for SPAs and mobile

---
## OAuth Token Types

- **Access token**: short-lived; the actual auth
- **Refresh token**: longer-lived; gets new access tokens
- **ID token** (OIDC): user identity (separate from auth)
- Each has its purpose

---
## Token Introspection

- Send the token to the auth server: "is this valid?"
- Auth server returns: yes / no, claims, expiry
- Latency: per-request round trip
- Use cache to mitigate
- Required when token isn't a self-contained JWT

---
## OpenID Connect

- Identity layer on top of OAuth
- Adds: ID tokens, standard user claims
- Used for: "Sign in with Google" flows
- The de facto standard for federated auth
- Most enterprise auth uses OIDC

---
## mTLS (Mutual TLS)

- Both client and server authenticate with certificates
- Strong: no shared secrets to leak
- Used for: service-to-service, IoT devices, B2B partners
- Setup overhead: cert issuance and rotation
- Less suitable for browser clients

---
## RBAC: Role-Based Access Control

- Users have roles; roles have permissions
- "Admin role can DELETE; Viewer can only GET"
- Easy to reason about
- Limits: doesn't capture fine-grained context
- The standard model

---
## ABAC: Attribute-Based Access Control

- Access depends on attributes: user, resource, action, context
- "Admins can delete *their own* records"
- More powerful; harder to reason about
- Common in compliance-heavy domains
- Tools: OPA (Open Policy Agent)

---
## Caching Auth Decisions

- Token introspection is expensive
- Cache the result for the token's TTL
- Reduce auth-server load by 100x
- Stale cache risk: revoked tokens still valid until cache expires
- Trade-off: latency vs revocation freshness

---
## Common Auth Mistakes

- API keys in URLs (logged everywhere)
- JWT without expiry
- Long-lived tokens with no rotation
- Auth checks at the service, not the gateway (sometimes both is correct)
- Disabling cert validation "for testing" — and forgetting to re-enable
