---
tags:
  - security:cryptography
  - security:tls
  - security:pki
level: intermediate
category: security
audience:
  - audiences:developers
  - audiences:security-professionals
  - audiences:devops
---
# TLS and PKI

---

## What TLS gives the application

- **Confidentiality** — bytes between client and server are encrypted
- **Integrity** — bytes cannot be tampered with mid-flight
- **Authenticity** — server proves it owns the domain (cert validation)
- Optional: client authentication (mutual TLS)
- Forward secrecy is mandatory in TLS 1.3

The application speaks plaintext on a TLS socket; the library handles the rest.

---

## TLS version history

| Version | Year | Status |
|---|---|---|
| SSL 2.0/3.0 | 1995 | broken, removed |
| TLS 1.0 | 1999 | deprecated, padding-oracle attacks |
| TLS 1.1 | 2006 | deprecated |
| TLS 1.2 | 2008 | still common, getting old |
| TLS 1.3 | 2018 | modern, simpler, faster |

Disable everything below TLS 1.2; enable TLS 1.3 if you can.

---

## TLS 1.3 improvements over 1.2

- One round-trip handshake (was two) → faster connections
- Removed: RSA key exchange, static DH, SHA-1, MD5, RC4, CBC modes, compression
- Mandatory forward secrecy (ECDHE only)
- Encrypted handshake after the first round-trip
- 0-RTT resumption (with replay caveats)
- Simpler cipher suite negotiation

TLS 1.2 has 200+ cipher suites including dangerous ones. TLS 1.3 has 5, all safe.

---

## TLS 1.3 Handshake

![handshake](svg/courses/security/cryptography-fundamentals/06_tls_pki/handshake.svg)

---

## What is in a cipher suite

TLS 1.2 cipher suite name reads as: KX_AUTH_WITH_ENC_MAC

```output
ECDHE_RSA_WITH_AES_256_GCM_SHA384
└─key── └sign └─bulk encryption─ └─PRF
```

- **Key exchange** — how the symmetric key is agreed (ECDHE, DHE)
- **Authentication** — how the server proves identity (RSA, ECDSA)
- **Cipher** — symmetric encryption algorithm and mode
- **MAC/PRF** — integrity + key derivation

TLS 1.3 simplifies: cipher suite specifies only AEAD + hash; key exchange and auth are separate.

---

## What a certificate is

- An X.509 document binding a public key to an identity
- Fields: subject, issuer, validity dates, public key, extensions
- Signed by a Certificate Authority (CA) using the CA's private key
- Verifying a cert means: walk up the chain to a trusted root

A cert without its chain is unverifiable. A cert without a trusted root in the chain is unvalidated.

---

## The trust chain

```output
Root CA (in browser/OS trust store)
   └── Intermediate CA (signed by root)
          └── Leaf cert (your server)
```

- Browsers and OSes ship a list of ~150 trusted root CAs
- Your server presents leaf + intermediate(s); browser fetches root from local store
- Each link is verified by signature checking
- Self-signed certs do not chain to a trusted root → browser warning

The whole web's trust depends on those root CAs not being compromised. They have been (DigiNotar, 2011) — bad day.

---

## Certificate lifecycle

1. **Generate** keypair on server
1. **Create CSR** (Certificate Signing Request) with public key + identity
1. **Submit** CSR to CA (commercial or Let's Encrypt)
1. **CA validates** domain control (DNS, HTTP, email)
1. **CA signs** the cert and returns it
1. **Install** on server; configure web server to use it
1. **Renew** before expiry (Let's Encrypt: 90 days; commercial: 1 year cap)

ACME automation (certbot, lego, acme.sh) makes this hands-off.

---

## Let's Encrypt

- Free, automated, ACME protocol
- Domain-validated certs only (no EV, no OV)
- 90-day validity, renew anytime in last 30 days
- Rate limits per domain prevent abuse
- ~50% of all web certs as of 2025

It killed the "certs are expensive and annoying" excuse for not using HTTPS.

---

## Revocation — the perpetual headache

- Cert leaked or owner abused? CA wants to revoke it
- **CRL** — CA publishes list of revoked serials; clients download
- **OCSP** — client asks CA in real-time "is this cert revoked?"
- **OCSP stapling** — server fetches OCSP response, sends with handshake
- Browsers mostly ignore CRL/OCSP for performance; rely on short cert lifetimes instead

Short-lived certs (Let's Encrypt's 90 days) make revocation less urgent.

---

## Common TLS misconfigurations

- Old protocols enabled (SSLv3, TLS 1.0, 1.1)
- Weak ciphers (RC4, 3DES, export grade)
- Missing intermediate certs in chain
- Self-signed certs in production
- Wildcard certs across security boundaries
- Long-lived certs that no one knows how to renew
- HSTS missing; no `Strict-Transport-Security` header

Test with `testssl.sh` or SSL Labs Server Test before going live.

---

## Certificate pinning

- Hardcode the expected cert (or its public key hash) in the client
- Defeats compromised CAs and rogue intermediaries
- Mostly for mobile apps and high-value backends
- HPKP (HTTP Public Key Pinning) was deprecated for the web — too easy to brick yourself

Use sparingly. Pin the public key, not the cert. Have a backup pin and a rotation plan.
