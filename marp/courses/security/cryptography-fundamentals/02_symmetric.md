---
tags:
  - security:cryptography
  - security:symmetric
level: intermediate
category: security
audience:
  - audiences:developers
  - audiences:security-professionals
---

# Symmetric Encryption

---

## Modes

![symmetric_modes](svg/courses/security/cryptography-fundamentals/02_symmetric/symmetric_modes.svg)

---

## The shared-key model

- Sender and receiver share the **same key**
- Encrypt with key K → cipher-text; decrypt with same K → plaintext
- Fast: hardware-accelerated on modern CPUs (AES-NI on x86)
- Catch: how do you exchange the key in the first place?

That key-distribution problem is what asymmetric crypto exists to solve. Once a shared key is in place, symmetric does the bulk of the work.

---

## AES — Advanced Encryption Standard

- 128-bit block cipher; key sizes 128, 192, 256
- Selected by NIST in 2001 from a public competition (originally a competing design)
- 20+ years of cryptanalysis with no practical break
- Hardware support (AES-NI) makes it screamingly fast
- AES-128 is fine for everything except very long-term archival

When in doubt: AES-256-GCM. Defensible default.

---

## ChaCha20

- Stream cipher designed by Daniel Bernstein
- 256-bit key, 96-bit nonce
- Faster than AES on hardware **without** AES-NI (mobile, embedded)
- No timing side-channels — same speed regardless of input
- Always paired with Poly1305 MAC for authenticated encryption

TLS 1.3 supports both AES-GCM and ChaCha20-Poly1305 — clients pick based on hardware.

---

## When to use which

- **Server-side, x86/ARM with AES-NI** — AES-256-GCM is fastest
- **Mobile, embedded, no AES hardware** — ChaCha20-Poly1305
- **Need long-term confidentiality** — AES-256 (paranoia margin)
- **Anywhere you would have used "AES" before** — use AES-GCM, not AES-CBC

Both are excellent. Pick on hardware reality, not folklore.

---

## Block Cipher Modes

![aes_modes](svg/courses/security/cryptography-fundamentals/02_symmetric/aes_modes.svg)

---

## ECB — and why never to use it

- "Electronic Codebook": encrypt each block independently with the same key
- Same plaintext block → same cipher-text block
- Patterns leak through the encryption
- The infamous "ECB penguin" image makes this visible: an encrypted bitmap still shows the silhouette
- Useful only in textbook examples and as a what-not-to-do

If a library lets you choose ECB, choose anything else.

---

## CBC — Cipher Block Chaining

- Each block XOR-combined with the previous cipher-text block before encryption
- Random IV (initialization vector) for the first block — never reused
- Sequential: cannot parallelize encryption
- Vulnerable to padding-oracle attacks if you do not authenticate
- "CBC + HMAC" was the standard pattern before AEAD came along

CBC is not broken, but it is **error-prone**. AEAD modes are the modern answer.

---

## CTR — Counter mode

- Encrypt a counter to produce a key-stream; XOR key-stream with plaintext
- Turns a block cipher into a stream cipher
- Fully parallel — encrypt blocks in any order
- No padding needed — output length = input length
- **Nonce reuse is catastrophic** — same nonce = same key-stream = XOR reveals plaintext

CTR alone gives you confidentiality but not integrity. Combine with a MAC, or use GCM.

---

## GCM — Counter Mode with Authentication

- CTR mode for encryption + GHASH for authentication, in one pass
- Provides **AEAD**: authenticated encryption with associated data
- 96-bit nonce (must be unique per key), 128-bit auth tag
- Header data ("associated data") is authenticated but not encrypted
- Reusing a nonce with the same key breaks security catastrophically

```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
key = AESGCM.generate_key(bit_length=256)
aesgcm = AESGCM(key)
nonce = os.urandom(12)
ct = aesgcm.encrypt(nonce, plaintext, associated_data=b"header")
```

---

## Key generation

- **Always** from a CSPRNG: `os.urandom`, `/dev/urandom`, `crypto.randomBytes`
- 256 bits is the modern default; 128 bits is acceptable
- Never derive keys from low-entropy sources (passwords, timestamps, PIDs)
- For password-based keys: use a key-derivation function (Argon2)

```python
import os
key = os.urandom(32)  # 256 bits
```

If you ever wrote `random.random()` to make a key — that key is not secret.

---

## Key storage

- **Never hardcode** — leaks via git history, logs, support tickets
- Environment variables — adequate for short-lived secrets
- Secret managers (Vault, AWS Secrets Manager, GCP Secret Manager)
- Hardware Security Modules (HSM) — keys never leave the device
- Kernel keyring (Linux) for short-term in-memory storage

The key is the entire secret. Treat it like one.

---

## Padding-oracle attacks

- Some servers tell the attacker "padding invalid" vs "decryption failed"
- That single bit of info, repeated, lets you decrypt arbitrary cipher-texts
- Famous against TLS 1.0 (BEAST, Lucky13) and ASP.NET (2010)
- Mitigation: use AEAD modes — there is nothing to oracle

If you must use CBC, you must use **constant-time MAC verification before decryption**. Most people get this wrong. Use AEAD.
