---
tags:
  - security:oauth2
  - concepts:best-practices
level: intermediate
category: security
audience:
  - audiences:developers
  - audiences:security-professionals

---

# OAuth2 Security Best Practices

---

## What This Chapter Covers

- The OAuth2 Best Current Practices (BCP)
- Common attacks and mitigations
- Token theft prevention
- Logout and session security
- Audit and monitoring

---

## OAuth2 BCP

- RFC 6819 (Threats and considerations)
- OAuth 2.0 Security Best Current Practice (draft, regularly updated)
- Lots of changes since RFC 6749 (2012)
- Modern recommendations consolidate years of attacks
- Read it; it's the cumulative wisdom of the community

---

## Threat Catalogue

![security_threats](svg/courses/networking/oauth2-and-oidc/08_security/security_threats.svg)

---

## CSRF on Authorize

- Attacker tricks user into starting an auth flow
- Returns to attacker-chosen redirect
- Defense: `state` parameter, verified on return
- Always use it; never skip
- Random, unpredictable, single-use

---

## Authorization Code Interception

- Attacker steals the code in transit (mobile, native apps)
- Defense: PKCE
- Code without verifier is useless
- Now mandatory for all clients in OAuth 2.1
- Critical for SPA and mobile

---

## Open-Redirect Abuse

- Loose redirect URI matching = open redirect
- Attacker registers `https://evil.com/` and redirects through
- Defense: exact-match registered URIs
- No wildcards
- Check this on every provider integration

---

## Token Replay

- Attacker steals a token; replays it later
- Defense: short token TTL; mTLS or proof-of-possession for binding
- Detection: monitor IP/UA changes
- Refresh token rotation also helps
- Long tokens = bigger replay window

---

## Cross-Site Request Forgery on Token

- Less common but real
- Defense: client authentication on the token endpoint
- TLS-bound origin verification helps
- CORS policies on the token endpoint
- Don't `*` allowed origins

---

## XSS-Driven Token Theft

- Attacker XSS injects a script that steals tokens
- localStorage tokens are easy targets
- Defense: BFF pattern, httpOnly cookies, CSP
- Memory-only tokens are safer
- XSS is still XSS — fix the underlying bug too

---

## Mix-Up Attacks

- Attacker swaps which auth server the client thinks it's talking to
- Defense: always include `iss` in the response, verify it
- Modern providers do this; some old ones don't
- Increasingly built into specs
- Worth checking your provider's posture

---

## Phishing-Resistant Auth

- WebAuthn / FIDO2 at the auth server
- Resistant to phishing because origin is bound in the assertion
- Pair with OAuth2/OIDC for a strong stack
- Increasingly required for high-value apps
- Best practice in 2026

---

## Defence In Depth Layers

![defence_layers](svg/courses/networking/oauth2-and-oidc/08_security/defence_layers.svg)

---

## TLS Everywhere

- Every endpoint, every request
- HSTS at minimum
- Strong cipher suites only
- Avoid downgrade attacks
- TLS 1.3 wherever supported

---

## Token Storage Recap

- Server-side: secure session store
- SPA: BFF pattern preferred; in-memory as fallback
- Mobile: OS secure storage (key store)
- CLI: OS credential manager
- Never plain text on disk

---

## Refresh Token Security

- Most sensitive token — guard it
- Rotate on every use
- Detect reuse — revoke the family
- Bind to client IP / device when possible
- Consider sender-constrained refresh tokens

---

## Sender-Constrained Tokens

- Proof-of-possession — sign each request to bind the token
- mTLS — token bound to TLS client cert
- Token theft alone is insufficient — need the key
- Strongest mitigation in spec drafts
- Worth deploying for high-stakes APIs

---

## Logout Properly

- Local: clear session and tokens
- Global: end_session_endpoint or back-channel logout
- Inform other clients via OIDC back-channel
- Don't leave dangling sessions
- Revoke refresh tokens explicitly on logout

---

## Consent Hygiene

- Show clear, concrete consent screens
- "App X wants to read your profile" not "Access your data"
- Allow granular per-scope decisions
- Re-consent on scope changes
- Audit consent records

---

## Scope Hygiene

- Don't request more than you need
- Users notice and reject excessive consent
- Different scopes per integration tier
- Audit what each scope actually grants
- Drift over time — review periodically

---

## Audit Logging

- Log every authorize and token call
- Include client_id, user, scopes, IP, UA
- Alert on unusual patterns: many failures, geo changes
- Retain per compliance requirements
- Tools: SIEM, custom dashboards

---

## Rate Limiting

- Per-IP, per-client, per-user
- Token endpoint is high-value; protect it
- Authorize endpoint less critical (user-driven)
- Slow brute force on credential entry
- Watch for distributed attacks

---

## Provider-Side Concerns

- If you run an auth server: keep it patched
- Audit JWKS rotation procedures
- Test failover; auth down = everything down
- Monitor for anomalies
- Subscribe to security advisories from your provider

---

## Multi-Tenant Considerations

- One auth server, many tenants
- Tenant ID in claims (custom claim)
- Resource server checks tenant alongside sub
- Don't let tokens cross tenants
- Tenant isolation is your job

---

## Common Mistakes Recap

- Skipping `state` and `nonce`
- Loose redirect URI matching
- localStorage for tokens
- Long-lived access tokens
- Trusting `alg` from JWT header

---

## Threat Model Quick Check

- Token theft via XSS — BFF, no localStorage
- Token theft in transit — TLS everywhere
- Phishing — WebAuthn for auth server
- Replay — short TTL, sender-constrained
- Confused deputy — audience validation

---

## Compliance and Standards

- Financial-grade API profiles for high-stakes
- GDPR for data minimization in claims
- SOC 2 / ISO for operational discipline
- HIPAA for healthcare
- Match implementation to compliance regime

---

## Testing Your Implementation

- OAuth2/OIDC compliance test suites (OpenID Foundation provides one)
- Negative tests: malformed tokens, expired, wrong audience
- Penetration testing focused on auth flow
- Bug bounty programs catch real issues
- Routine audits, not one-time

---

## Summary

- OAuth2 BCP captures cumulative attack lessons
- PKCE, state, nonce: required hygiene
- Short tokens, refresh rotation, sender-constrained tokens
- BFF pattern for browsers
- Defense in depth — TLS, CORS, CSP, audit, monitor
