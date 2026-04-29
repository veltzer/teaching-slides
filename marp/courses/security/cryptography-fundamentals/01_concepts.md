---
tags:
  - security:cryptography
level: intermediate
category: security
audience:
  - audiences:developers
  - audiences:security-professionals
---
# Cryptography Concepts

---

## Four security goals

- **Confidentiality** — only the intended recipient can read the message
- **Integrity** — the message has not been altered in transit
- **Authentication** — you know who you are talking to
- **Non-repudiation** — the sender cannot later deny sending

Different primitives address different goals; few address them all at once.

---

## The principle of public algorithms

> "A cipher should be secure even if everything about the system, except the key, is public knowledge."

- Security must rest on **the secrecy of the key**, not the algorithm
- Public algorithms get peer-reviewed — that is how trust is built
- "Security through obscurity" is not security
- AES, RSA, SHA-256 — all public, all standardized, all trusted because of it

If your security depends on no one finding out how it works, you have already lost.

---

## Computational hardness

- Cryptography rests on problems that are **easy one way, hard the other**
- Multiplication is easy; factoring is hard (RSA)
- Modular exponentiation is easy; discrete log is hard (key exchange, elliptic curves)
- Hashing is easy; finding a collision is hard (SHA-2)

Security parameters quantify the work an attacker would need:

- 128-bit security ≈ 2^128 operations to break — beyond reach today
- 80 bits is no longer safe; 256 bits is paranoid-grade

---

## Cryptographic primitives

The building blocks you will compose into systems

| Primitive | Purpose | Examples |
|---|---|---|
| Symmetric cipher | Bulk encryption | AES, ChaCha20 |
| Asymmetric cipher | Key exchange, signatures | RSA, ECC |
| Hash | Fingerprint, integrity | SHA-256 |
| MAC | Authenticated integrity | HMAC, Poly1305 |
| Key derivation | Derive keys from secrets | HMAC-based and Argon2 |

You rarely use one alone — real protocols stack them.

---

## Cryptographic Primitives

![primitives](svg/courses/security/cryptography-fundamentals/01_concepts/primitives.svg)

---

## Standards bodies

- **NIST** — US standards body; runs competitions for AES, SHA-3, post-quantum
- Internet Engineering Task Force — TLS and JSON-signing specs live in RFCs
- **IEEE** — academic and hardware crypto specs
- **ISO** — international standards (often align with NIST)

Trust algorithms that have been through public review and standardization, not someone's blog post.

---

## When you need crypto, what do you reach for?

- **Encrypt a file at rest** — AES with authenticated mode and a random nonce
- **Encrypt traffic between two services** — TLS, full stop
- **Sign a release archive** — Ed25519 or modern RSA signing
- **Store a password** — Argon2id, never plain SHA
- **Derive a key from a password** — key derivation function (e.g. Argon2)
- **Random session token** — `os.urandom`, never `random.random()`

Pattern-match the goal to the primitive. Do not invent.

---

## Cryptographic agility

- Algorithms get broken — MD5, SHA-1, RC4, DES are all dead today
- Build systems that can rotate algorithms without rewrites
- Tag every encrypted message with the algorithm and version that produced it
- Plan migration paths now — quantum is coming for RSA and ECC

Crypto agility means surviving the next "this algorithm is broken" headline without an emergency.
