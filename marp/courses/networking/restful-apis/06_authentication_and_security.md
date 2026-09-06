---
tags:
  - networking:rest
  - security:authentication
level: intermediate
category: networking
audience:
  - audiences:developers

---

# Authentication and Security

---

## Auth Methods

![auth_methods](svg/courses/networking/restful-apis/06_authentication_and_security/auth_methods.svg)

---

## What This Chapter Covers

- Auth concepts
- API keys
- Basic auth
- Bearer tokens / JWT
- OAuth2
- HTTPS, CORS, common pitfalls

---

## Authentication vs Authorisation

- Authn: who are you
- Authz: what can you do
- Different concerns
- Often discussed together

---

## API Keys

- Static secret per client
- In header (X-API-Key) or query (less safe)
- Simple; no expiry
- Good for: server-to-server, internal

---

## Basic Auth

- Username + password, base64 encoded
- Sent every request
- Easy but exposes credentials
- Use over HTTPS only; rare in modern APIs

---

## Bearer Tokens

- `Authorization: Bearer <token>`
- Token issued after login
- Opaque or self-contained
- Standard for REST APIs

---

## JWT

- JSON Web Token
- Header.payload.signature
- Self-contained, signed
- Stateless verification

---

## JWT Pros and Cons

- Pro: no DB lookup per request
- Pro: works across services
- Con: can't easily revoke
- Con: large; payload sent every call

---

## OAuth2

- Delegated authorisation
- "Sign in with Google"
- Authorisation server, resource server, client
- Standard for third-party access

---

## OAuth2 Flows

- Authorization code: web apps
- Client credentials: machine-to-machine
- Device flow: TVs, CLIs
- Implicit and password: deprecated

---

## OIDC

- OpenID Connect
- Authentication on top of OAuth2
- Adds id_token (JWT)
- Standard for SSO

---

## HTTPS

- Required everywhere
- Encrypts in transit
- Authenticates server
- HSTS to enforce

---

## CORS

- Cross-Origin Resource Sharing
- Browser-enforced
- Headers: Access-Control-Allow-*
- Origin whitelist

---

## Rate Limiting

- Cap requests per client
- Headers: X-RateLimit-*
- 429 Too Many Requests
- Protect from abuse

---

## Input Validation

- Don't trust clients
- Validate types, ranges, formats
- Reject early
- Prevents injection

---

## Common Security Mistakes

- Storing JWT in localStorage (XSS)
- API keys in URLs (logged)
- Missing rate limits
- Verbose error messages leaking internals
- CORS with `*` for credentialed requests

---

## Layered Security Controls

![security_layers](svg/courses/networking/restful-apis/06_authentication_and_security/security_layers.svg)
