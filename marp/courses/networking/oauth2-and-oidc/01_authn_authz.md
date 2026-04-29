---
tags:
  - security:oauth2
  - concepts:authentication
level: intermediate
category: security
audience:
  - audiences:developers

---
# Authentication and Authorization

---
## What This Chapter Covers

- Authentication vs authorization
- The four OAuth2 roles
- Why OAuth2 exists
- OAuth2 vs OIDC
- Course roadmap

---
## Authentication

- Who are you?
- Verifying identity
- Username + password, MFA, biometrics, certificates
- Result: a verified identity claim
- The first half of access control

---
## Authorization

- What can you do?
- Granting permissions to a verified identity
- Roles, scopes, attributes, policies
- Result: a decision (allow or deny)
- The second half of access control

---
## A Common Mix-Up

- "Log in with Google" looks like authentication
- But OAuth2 itself is authorization
- OIDC layers identity on top
- Misusing OAuth2 for pure authentication is a known mistake
- We will fix the mental model in this chapter

---
## Why Not Just Use Passwords?

- Sharing passwords with third-party apps is dangerous
- Apps would need to store passwords
- Revoking access requires changing passwords everywhere
- Granular permissions impossible with just a password
- OAuth2 solves: delegated, scoped access without sharing credentials

---
## OAuth2 Roles

- Resource Owner — the user
- Client — the application
- Authorization Server — issues tokens
- Resource Server — hosts the protected API
- All four have well-defined responsibilities

---
## OAuth2 Roles Visualized

![oauth_roles](svg/courses/networking/oauth2-and-oidc/01_authn_authz/oauth_roles.svg)

---
## Resource Owner

- Usually a human user
- Owns the data being accessed
- Approves or denies access requests
- The "you" in "Allow App to access your data?"
- Sometimes a system in machine-to-machine flows

---
## Client

- The application requesting access
- Could be a web app, mobile app, CLI, server
- Has a client ID; usually a client secret
- Configured at the authorization server beforehand
- Different security postures per client type

---
## Authorization Server

- Authenticates the user
- Issues tokens to the client
- Manages consent
- Run by the identity provider
- Examples: Auth0, Okta, Keycloak, Cognito

---
## Resource Server

- Hosts the API the client wants to access
- Validates tokens on each request
- Returns data based on token scopes
- May or may not be the same domain as the auth server
- Stateless validation enables scaling

---
## What OAuth2 Is Not

- Not authentication (despite common misuse)
- Not encryption (use TLS for that)
- Not user management
- Not session management for the resource server
- It's specifically delegated authorization

---
## What OIDC Adds

- A standardized identity layer on top of OAuth2
- Adds an ID token (JWT)
- Standard claims: sub, name, email, etc
- A UserInfo endpoint
- Discovery and standard scopes (`openid`, `profile`, `email`)

---
## When You Need OAuth2

- Letting users grant third-party apps access to your API
- Federating identity from a SaaS provider
- Service-to-service authorization
- API authorization at scale
- Almost every modern web app

---
## When You Need OIDC

- Single sign-on (SSO) flows
- "Log in with X" buttons
- When you need user identity, not just authorization
- Federation between organizations
- Identity-aware proxies and zero-trust networks

---
## OAuth2 Specs

- RFC 6749 — the core framework
- RFC 6750 — bearer token usage
- RFC 7636 — PKCE
- RFC 8252 — OAuth2 for native apps
- Draft 2.1 — current best practices consolidated

---
## OIDC Specs

- OpenID Connect Core 1.0
- Discovery, Dynamic Registration
- Session Management
- Front-channel and back-channel logout
- All built on OAuth2

---
## Mental Model

- Authentication: I know who you are
- OAuth2 authorization: I know you let this app act on your behalf
- OIDC: a standardized way to convey "who" alongside OAuth2
- Tokens are the carrier
- The auth server is the trusted party

---
## Course Roadmap

- Chapter 2: OAuth2 basics
- Chapter 3: Authorization Code flow with PKCE
- Chapter 4: Other grant types
- Chapter 5: Token types
- Chapter 6: OpenID Connect
- Chapter 7: JWTs in depth
- Chapter 8: Security best practices
- Chapter 9: Real providers and integration

---
## Common Misconceptions

- "OAuth2 logs users in" — no, OAuth2 grants access; OIDC does login
- "JWT means OAuth2" — JWT is a token format; OAuth2 doesn't require it
- "OAuth2 is encryption" — no, it's authorization; encryption is TLS
- "Just use access tokens for login" — leads to insecure deployments
- "Scopes equal permissions" — scopes are coarse; fine-grained authz is separate

---
## Summary

- Authentication is "who"; authorization is "what"
- OAuth2 has four roles: owner, client, auth server, resource server
- OAuth2 is authorization; OIDC adds identity
- Don't confuse the two — most security bugs come from the confusion
- The rest of the course goes deep on flows, tokens, and security
