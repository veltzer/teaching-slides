---
tags:
  - security:oauth2
  - tools:auth0
  - tools:keycloak
level: intermediate
category: security
audience:
  - audiences:developers

---

# Real Providers and Integration

---

## What This Chapter Covers

- Major identity providers
- Keycloak self-hosted
- Auth0 managed
- Okta enterprise
- AWS Cognito and others

---

## Choosing a Provider

- Self-host vs managed
- Multi-tenant vs single-tenant
- Enterprise SSO vs consumer
- Cost at scale
- Compliance certifications

---

## Provider Landscape Visualized

![providers](svg/courses/networking/oauth2-and-oidc/09_providers/providers.svg)

---

## Provider Picker

![provider_picker](svg/courses/networking/oauth2-and-oidc/09_providers/provider_picker.svg)

---

## Keycloak

- Open source, run by Red Hat
- Self-hosted; full control
- Supports OAuth2, OIDC, SAML
- Realms for multi-tenancy
- Free and powerful; operational burden

---

## When to Use Keycloak

- Strict data residency requirements
- Need full control over the auth server
- Existing Java enterprise familiarity
- Cost-sensitive at high volume
- Don't mind running infrastructure

---

## Auth0

- Managed service (now part of Okta)
- Excellent developer experience
- Rich SDK ecosystem
- Per-user pricing scales with growth
- Great for B2C and B2B

---

## When to Use Auth0

- Want it running quickly with minimal ops
- Diverse integrations needed
- B2C consumer apps with social login
- Don't have a security team to run Keycloak
- Budget allows per-user pricing

---

## Okta

- Enterprise-focused identity platform
- Strong B2B and workforce identity
- Powerful policies, governance, lifecycle
- More expensive than Auth0 typically
- Common in large organizations

---

## AWS Cognito

- Managed by AWS
- User pools (auth) + identity pools (federation)
- Tight integration with AWS services
- Lower cost than Auth0/Okta
- Less polished developer experience

---

## Azure AD / Entra ID

- Microsoft's identity platform
- Default for Microsoft 365 customers
- Strong enterprise SSO
- B2B and B2C variants
- Tight integration with Azure

---

## Google Identity

- Google as IdP for users with Google accounts
- Free for "log in with Google"
- Limited customization
- Use as a federated source, not primary
- Common social login

---

## GitHub Apps

- For developer-focused integrations
- JWT bearer assertion grant
- Per-installation tokens
- Excellent for CI/CD integrations
- Niche but useful

---

## Setting Up: Keycloak Quick Start

```bash
docker run -p 8080:8080 \
  -e KEYCLOAK_ADMIN=admin \
  -e KEYCLOAK_ADMIN_PASSWORD=admin \
  quay.io/keycloak/keycloak:latest start-dev
```

- Up and running in seconds
- Create a realm, a client, a user
- Test with curl or your app
- Production needs more: TLS, DB, HA

---

## Setting Up: Auth0 Quick Start

- Sign up at auth0.com
- Create an Application
- Note Client ID, Domain, Client Secret
- Configure callback URLs
- Drop their SDK into your app

---

## Common Integration Steps

- Register the client at the provider
- Get client_id (and possibly client_secret)
- Configure redirect URIs
- Set allowed grant types
- Add to your app's config

---

## Library Selection

- Use battle-tested OAuth2/OIDC libraries
- Don't implement from scratch
- Examples: Python OAuth libraries, oidc-client (JS), Spring Security
- Update libraries regularly
- Audit your dependency tree

---

## Common Library Pitfalls

- Skipping signature verification because "library handles it"
- Ignoring the warnings about Implicit flow
- Not pinning the algorithm in JWT validation
- Default lifetimes that don't match your security posture
- Custom middleware that bypasses validation

---

## Integration Patterns

![integration_patterns](svg/courses/networking/oauth2-and-oidc/09_providers/integration_patterns.svg)

---

## Federation

- Provider A federates to Provider B
- User logs in via B, but app sees A
- SAML, OIDC, custom protocols
- Common for B2B SSO
- Each step adds attack surface

---

## Social Login

- Auth via Google, Facebook, GitHub, Apple
- Provider acts as a federated IdP
- "Sign in with Apple" is required for app store apps with social login
- Map external `sub` to your internal user
- Plan for users disconnecting their social account

---

## Account Linking

- Same user, multiple identity sources
- "Link your Google and email accounts"
- Implement at your app or use provider features
- Be careful: account takeover via lax linking
- Verify both sides before linking

---

## Multi-Factor Authentication

- TOTP (Google Authenticator)
- WebAuthn / FIDO2 keys (best)
- SMS (deprecated by NIST; risky)
- Push notifications (reasonable)
- Provider supports a mix

---

## Step-Up Authentication

- Some operations need stronger auth
- Re-prompt with MFA for high-value actions
- ACR (Authentication Context Class Reference) standardizes this
- Authentication Methods References reports what was used
- Increasingly used in finance and admin

---

## Migrating Between Providers

- Plan: dual-run providers, gradually move users
- Account linking by email or external ID
- Rotate refresh tokens through the new provider
- Keep both running until adoption is complete
- Document the cutover

---

## Cost Considerations

- Auth0/Okta: per active user
- Cognito: cheaper at scale
- Keycloak: self-hosted, infra cost only
- Compare TCO including ops time
- Start managed; consider self-hosting later

---

## Operational Concerns

- Provider outages = your auth outages
- SLA matters; check it
- Status page subscription
- Failover plan: cache tokens, allow graceful degradation
- Multi-provider setups for high availability

---

## Common Pitfalls

- Trusting providers blindly without security review
- Not testing the auth flow under provider downtime
- Skipping the security best practices because "the SDK handles it"
- Account linking without verification
- Not setting up monitoring and alerts on auth events

---

## Course Recap

- Authentication vs authorization fundamentals
- OAuth2 basics and roles
- Authorization Code with PKCE
- Other grant types
- Tokens: access, refresh, ID
- OpenID Connect identity layer
- JWT in depth
- Security best practices
- Real providers

---

## Final Thoughts

- OAuth2/OIDC is the backbone of modern auth
- Most security bugs come from misuse, not the protocol
- Use libraries; pin algorithms; validate everything
- Choose providers based on team and threat model
- Stay current with the BCP — the field evolves

---

## Summary

- Keycloak self-hosted; Auth0/Okta managed; Cognito for AWS
- Use battle-tested libraries; don't roll your own
- Plan for federation, account linking, and provider failover
- The right provider matches your team, threat model, and budget
- Implement once, audit forever — security is a moving target
