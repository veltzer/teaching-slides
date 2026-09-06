---
tags:
  - concepts:architecture
  - concepts:security
  - concepts:zero-trust
level: advanced
category: architecture
audience:
  - audiences:developers
  - audiences:architects
  - audiences:devops

---

# Security Architecture

---

## Why Security Is Architectural

- Security bolted on after delivery is slow, expensive, and often wrong
- Every architectural decision — service boundaries, data stores, communication — has a security dimension
- The architect owns the threat model, not just the org chart
- A single insecure integration can compromise an entire distributed system

---

## The Three Core Concerns

- **Confidentiality** — only authorized parties can read data
- **Integrity** — data cannot be tampered with without detection
- **Availability** — the system remains usable despite attacks
- Every design choice trades these three in different ways

---

## Authentication vs Authorization

- **Authentication (AuthN)** — *who* is making this request?
- **Authorization (AuthZ)** — *is this principal allowed to do this?*
- Both are needed; neither replaces the other
- A common architectural mistake: binding authorization to the transport layer (IP allow-lists) instead of identity

---

## OAuth 2.0

- Delegated authorization framework — not authentication on its own
- The client gets an **access token** and presents it to resource servers
- Resource servers validate the token and grant scoped access
- Does not say who the user is — that is OIDC's job

---

## OAuth 2.0 Flow

- **Authorization Code** (with PKCE) — for interactive users in web/mobile apps
- **Client Credentials** — for service-to-service
- **Refresh Token** — long-lived credential to obtain new access tokens
- **Device Code** — for devices without keyboards (TVs, CLIs)

Avoid the implicit and password grants — both are deprecated for security reasons.

---

## OpenID Connect (OIDC)

- A thin identity layer on top of OAuth 2.0
- Adds the **ID token** (a JWT) that identifies the user
- Enables single sign-on across apps using one identity provider
- Standardized claims: `sub`, `email`, `name`, `iat`, `exp`

---

## JWT Anatomy

```misc
header.payload.signature
```

- **Header** — algorithm and key ID
- **Payload** — claims (subject, scopes, expiry)
- **Signature** — HMAC or RSA/ECDSA signature over header + payload
- Verified by checking the signature and the `exp` claim

---

## JWT Pitfalls

- **Stateless revocation is hard** — a leaked token is usable until it expires
- **Algorithm confusion** — `alg: none` attacks, HMAC-vs-RSA key confusion
- **Long expiry** — set aggressive `exp`; use refresh tokens for continuity
- **Storing sensitive data in claims** — anyone can decode a JWT; only the signature is protected
- Prefer short-lived access tokens (5–15 min) with refresh tokens

---

## mTLS (Mutual TLS)

- Both client and server present X.509 certificates
- Each side verifies the other's cert against a trusted CA
- Gives cryptographic identity to service-to-service calls
- The backbone of service mesh security and zero-trust networking

---

## mTLS vs Token Auth

| Aspect | mTLS | Bearer token |
|--------|------|-------------|
| Identity | Certificate | Claim in token |
| Rotation | Short-lived certs, automated | Refresh tokens |
| Revocation | CRL / OCSP / short TTL | Token blacklist |
| Scope | Workload-level | Request-level |
| Best for | Service-to-service | User-to-service |

Real systems use both — mTLS under the hood, tokens for user context.

---

## RBAC: Role-Based Access Control

- Principals have **roles**; roles have **permissions**; permissions gate actions
- Simple to reason about and easy to audit
- Works poorly for rules like "the user who created this resource can edit it"
- Kubernetes RBAC is the canonical example

---

## ABAC: Attribute-Based Access Control

- Decisions use arbitrary attributes of the subject, resource, action, and environment
- Example: "a manager in department X can approve expenses under $10k during business hours"
- More expressive than RBAC, harder to audit and reason about
- Policy languages: Rego (OPA), Cedar, XACML

---

## Choosing RBAC vs ABAC

- Start with RBAC; add targeted ABAC rules when roles can't express a constraint
- Pure ABAC is hard to explain to auditors and harder to test
- Combine them: broad coarse-grained RBAC + narrow fine-grained ABAC for exceptions
- OPA is a good fit for policy-as-code in Kubernetes-heavy stacks

---

## Zero-Trust Networking

- Never trust by network location — the corporate LAN is not trusted
- Every request is authenticated and authorized, regardless of origin
- Mutual TLS between all workloads
- Short-lived credentials rotated automatically
- Based on NIST SP 800-207 and Google's BeyondCorp paper

---

## Zero-Trust Principles

- Assume breach — design as if an attacker is already inside
- Verify explicitly — identity, device, location, behavior
- Use least-privilege access — ephemeral, narrow, auditable
- Encrypt in transit and at rest — TLS and disk-level encryption everywhere
- Continuously monitor — revoke trust when signals change

---

## Secrets Management

- Secrets never live in source code, config files, or container images
- A dedicated secret manager stores, rotates, and audits access
- Applications fetch secrets at runtime with a short-lived credential
- Tools: `HashiCorp Vault`, `AWS Secrets Manager`, `GCP Secret Manager`, `Azure Key Vault`

---

## Secret Rotation

- Short rotation window limits blast radius of a leak
- Database passwords, API keys, signing keys — all should rotate on a schedule
- Automate: no human ever reads a production password
- Applications must handle rotation gracefully (no hardcoded credentials in memory forever)

---

## Threat Modeling with STRIDE

- **Spoofing** — impersonating another principal
- **Tampering** — modifying data in flight or at rest
- **Repudiation** — denying an action after the fact
- **Information Disclosure** — leaking data to unauthorized parties
- **Denial of Service** — making the system unavailable
- **Elevation of Privilege** — gaining more access than authorized

Walk every service through STRIDE during architecture review.

---

## The OWASP Top 10 at the Architecture Layer

Most of OWASP is a code-level checklist, but four items are architectural:

- **Broken Access Control** — authZ decisions scattered across the codebase
- **Security Misconfiguration** — defaults that expose internals
- **Insecure Design** — missing threat modeling, missing auth boundaries
- **Server-Side Request Forgery (SSRF)** — services that fetch arbitrary URLs without egress controls

Fix them once at the architecture level instead of in every service.

---

## Defense in Depth

- No single layer is fully trusted
- WAF at the edge, mTLS between services, authZ checks in each service, encryption at rest in each store
- Assume any one layer will eventually be bypassed
- Adds latency and complexity — budget for both

---

## Encryption at Rest

- Disk-level encryption (LUKS, EBS encryption, Cloud KMS-managed)
- Field-level encryption for the most sensitive columns
- Transparent Data Encryption (TDE) in databases for everything else
- Key management is the hard part — rotate keys, audit access, never export

---

## Encryption in Transit

- TLS 1.2+ everywhere; prefer TLS 1.3
- mTLS inside the cluster; one-way TLS at the edge
- Certificate rotation must be automated (cert-manager, ACME)
- Deprecate old TLS and cipher suites on a schedule

---

## Supply Chain Security

- Every dependency is a potential attacker
- Pin versions; scan for known vulnerabilities (`Snyk`, `Dependabot`, `Trivy`)
- Verify artifact signatures (`cosign`, `sigstore`)
- Generate and store SBOM (Software Bill of Materials) per release
- SLSA framework classifies build-pipeline integrity

---

## Common Architectural Mistakes

- **Auth at the gateway only** — services trust any inbound request, so a breach of one service compromises all
- **Hard-coded service-to-service API keys** — rotation never happens
- **Shared database credentials** — no way to trace which service did what
- **IP allow-lists as the primary defense** — trivially bypassed inside the network
- **Secrets in environment variables logged by mistake** — rotate immediately

---

## The Architect's Security Checklist

- Every service authenticates its callers
- Every service authorizes every request based on identity, not network
- All inter-service traffic uses mTLS
- Secrets come from a vault, rotate on a schedule, and never land in logs
- A documented threat model exists per bounded context
- Dependency and image scanning runs in CI on every change
- Incident response playbook is tested, not just written

---

## Summary

- Security is architectural, not a feature you can add at the end
- Separate AuthN (OAuth/OIDC) from AuthZ (RBAC/ABAC); bind decisions to identity, not IPs
- mTLS secures service-to-service; JWT handles user context
- Zero-trust assumes breach and verifies every request explicitly
- Secrets live in vaults and rotate automatically
- Threat modeling (STRIDE) belongs in architecture review
- Defense in depth, supply chain integrity, and encryption everywhere
