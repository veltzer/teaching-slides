---
tags:
  - security:network
level: intermediate
category: networking
audience:
  - audiences:devops
  - audiences:security

---

# Identity and Access

---

## What This Chapter Covers

- Authentication
- Authorization
- Service identity
- Network policies
- Zero trust

---

## Authentication

- Proving who you are
- Passwords plus MFA
- Or hardware tokens
- Or certificates

---

## Identity Layers

![auth_layers](svg/courses/networking/network-security/04_identity_and_access/auth_layers.svg)

---

## MFA

- Two factors: knowledge plus possession
- Hardware tokens preferred
- Phone-based as fallback
- SMS is no longer adequate

---

## Single Sign-On

- One identity, many systems
- Reduces password sprawl
- Centralizes audit
- Compromise is critical

---

## Authorization

- What you may do once authenticated
- Role-based or attribute-based
- Least privilege default
- Audit changes

---

## Service Identity

- Servers and services authenticate too
- Workload identity in cloud
- Mutual TLS in service meshes
- No shared secrets

---

## API Keys

- Long-lived tokens
- Easy to leak
- Difficult to rotate
- Replace with short-lived where possible

---

## Short-Lived Tokens

- Issued by an identity provider
- Expire in minutes to hours
- Refreshed as needed
- Smaller blast radius on compromise

---

## Network Policies

- Per-workload allow rules
- Deny by default
- Express in declarative form
- Enforced at host or proxy

---

## Zero Trust

- Identity is the new perimeter
- Every request authenticated
- Every request authorized
- No implicit trust by IP

---

## Request Path

![zero_trust_request](svg/courses/networking/network-security/04_identity_and_access/zero_trust_request.svg)

---

## Audit Logs

- Every login, every access
- Centralized
- Long retention
- Tamper-evident

---

## Privileged Access Management

- Special workflow for high-privilege actions
- Approval before access
- Time-bounded sessions
- Recorded

---

## Secrets Management

- Vaults for secrets
- Secrets injected, not embedded
- Rotated regularly
- Audited

---

## Common Identity Mistakes

- Shared accounts
- SMS as primary MFA
- Long-lived API keys
- No audit retention
- Implicit trust by network
