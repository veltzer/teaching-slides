---
tags:
  - security:cryptography
  - security:integrity
level: intermediate
category: security
audience:
  - audiences:developers
  - audiences:security-professionals
---

# Hash Functions and MACs

---

## What a cryptographic hash gives you

- Maps any input to a fixed-length output ("digest")
- **Deterministic** — same input, same output
- **One-way** — cannot recover input from digest (preimage resistance)
- **Collision-resistant** — cannot find two inputs with the same digest
- **Avalanche** — flipping one input bit flips half the output bits

A hash is a fingerprint: small, fast, and uniquely tied to the input.

---

## The SHA family

| Algorithm | Digest size | Status |
|---|---|---|
| MD5 | 128 bits | broken — never use |
| SHA-1 | 160 bits | broken — collisions found 2017 |
| SHA-256 | 256 bits | safe, default workhorse |
| SHA-512 | 512 bits | safe, faster on 64-bit hardware |
| SHA-3 (Keccak) | 224-512 bits | safe, different design |
| BLAKE2/3 | configurable | safe, fast |

If a system still uses MD5 or SHA-1 for security, treat it as broken.

---

## SHA-2 vs SHA-3

- **SHA-2** — Merkle-Damgård construction, designed by NSA in 2001
- **SHA-3** (Keccak) — sponge construction, NIST competition winner 2012
- **Different designs** so a break of one would not break the other
- SHA-2 is faster on most hardware; SHA-3 uses fewer gates
- Both are equally trusted; pick on performance and library support

SHA-2 is the de-facto default. SHA-3 is a hedge for crypto-agility.

---

## BLAKE2 and BLAKE3

- **BLAKE2** — finalist in SHA-3 competition; faster than SHA-2 in software
- **BLAKE3** — Merkle-tree, parallelisable; faster than everything
- Used in age, WireGuard, Cargo, IPFS
- Not yet a NIST standard — adopt with eyes open

For checksums and content addressing where speed matters, BLAKE3 is hard to beat.

---

## Common use cases

- **Integrity check** — git uses SHA-1 (legacy) → SHA-256 transitioning
- **Content addressing** — IPFS, Docker layers, Cargo packages
- **Commitment schemes** — publish hash now, reveal value later
- **HMAC construction** — building MAC from any hash
- **Password hashing** — but NOT plain hash; need a slow KDF (next)

A bare hash is the right tool for many things, but not passwords.

---

## Birthday attacks

- For an n-bit hash, finding a collision takes ~2^(n/2) work
- 128-bit hash → 2^64 work — within reach of well-funded attackers
- 256-bit hash → 2^128 work — beyond reach
- Use 256-bit minimum where collision resistance matters

This is why we say "256-bit security": collision attacks halve effective bits.

---

## Why a hash is not enough

- Hashes prove **integrity** but not **authenticity**
- Anyone can compute the hash — including the attacker
- Need a secret element to bind the hash to a known sender
- That is what MACs (Message Authentication Codes) provide

A hash on its own answers "is this the same data?" — not "is this from who I think?"

---

## HMAC

![hmac](svg/courses/security/cryptography-fundamentals/04_hashes_macs/hmac.svg)

---

## HMAC — hash-based MAC

- Take a hash function (SHA-256) + a shared key + the message
- Output is a tag that only someone with the key can produce or verify
- Standardized in RFC 2104; works with any hash
- Resistant to length-extension attacks (which plain SHA-2 hashes are NOT)

```python
import hmac, hashlib
tag = hmac.new(key, message, hashlib.sha256).digest()
```

Always use `hmac.compare_digest` to check tags — constant-time comparison.

---

## AEAD — authenticated encryption with associated data

- Encrypts **and** authenticates in one primitive
- "Associated data" is authenticated but not encrypted (e.g., headers)
- Two dominant constructions:
    - **AES-GCM** — AES-CTR + GHASH MAC
    - **ChaCha20-Poly1305** — ChaCha20 stream cipher + Poly1305 MAC
- TLS 1.3 mandates AEAD; older modes are removed

If you encrypt without authenticating, attackers can flip ciphertext bits and you will not notice. AEAD is the modern answer.

---

## MAC vs digital signature

|  | MAC | Signature |
|---|---|---|
| Key model | shared symmetric | asymmetric pair |
| Verifier | anyone with the key | anyone with public key |
| Non-repudiation | no | yes |
| Speed | fast | slower |
| Use | API auth, cookies | code signing, certificates |

MAC = "we both have the key, so I trust this came from one of us." Signature = "anyone in the world can verify this came from me, and only me."
