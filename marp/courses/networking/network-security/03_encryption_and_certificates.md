---
tags:
  - security:network
level: intermediate
category: networking
audience:
  - audiences:devops
  - audiences:security

---
# Encryption and Certificates

---
## What This Chapter Covers

- TLS basics
- Certificates
- Key management
- Mutual TLS
- VPN protocols

---
## Why Encrypt

- Confidentiality on the wire
- Integrity of messages
- Server authenticity
- Sometimes client authenticity

---
## Symmetric vs Asymmetric

- Symmetric: same key both sides
- Asymmetric: public and private key pair
- Symmetric is fast
- Asymmetric is for handshakes

---
## TLS Handshake

- Negotiate ciphers
- Verify server certificate
- Exchange session key
- Encrypt the rest

---
## Handshake Sequence

![tls_handshake](svg/courses/networking/network-security/03_encryption_and_certificates/tls_handshake.svg)

---
## Certificates

- Identity binding to a public key
- Signed by a trusted authority
- Valid for a period
- Revoked when compromised

---
## Certificate Lifecycle

![cert_lifecycle](svg/courses/networking/network-security/03_encryption_and_certificates/cert_lifecycle.svg)

---
## Certificate Authorities

- Public CAs for the web
- Private CAs for internal systems
- Trust chains
- Compromise is critical

---
## Common Mistakes With Certificates

- Self-signed in production
- Expired certificates
- Wildcard sprawl
- No automated renewal

---
## Automated Renewal

- Short-lived certificates
- ACME for web
- Internal automation for private CA
- Forgotten cert is downtime

---
## Mutual TLS

- Both sides present certificates
- Strong identity for service-to-service
- More setup, more security
- Common in service meshes

---
## Cipher Suites

- Algorithms for handshake and bulk encryption
- Older ciphers must be disabled
- Track standards bodies
- Test with scanners

---
## TLS Versions

- 1.2 minimum today
- 1.3 preferred
- Older versions disabled
- Test with scanning tools

---
## VPN Protocols

- IPsec for site-to-site
- WireGuard for modern simplicity
- OpenVPN still common
- TLS tunnels for ad-hoc

---
## Key Management

- Hardware security modules for highest tier
- Cloud key services for most
- Rotate regularly
- Audit access

---
## Common Encryption Mistakes

- Self-signed certificates
- Long-lived keys
- No mutual TLS where it matters
- Old TLS versions enabled
- Manual cert renewal
