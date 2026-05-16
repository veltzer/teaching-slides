---
tags:
  - security:secure-coding
  - security:encryption
  - languages:c
  - languages:c++
  - languages:python
level: intermediate
category: security
audience:
  - audiences:developers
  - audiences:embedded-engineers
  - audiences:security-professionals
---
# Encryption

---

## What This Chapter Covers

- Symmetric vs asymmetric encryption
- Hashing and message authentication codes
- `TLS`/`SSL` and secure transport
- Key generation, storage, and rotation
- Common cryptographic pitfalls in C, `C++`, and `Python`

---

## The One Rule

> Do not roll your own crypto. Do not roll your own crypto. Do not roll your own crypto.

- Use vetted libraries: **libsodium**, **OpenSSL** / **BoringSSL**, the `Python` `cryptography` package
- Prefer high-level "do the right thing" APIs over assembling primitives yourself
- The dangerous mistakes are not in the algorithms — they are in how you use them
- If you find yourself choosing an IV by hand, stop and find the high-level API

---

## Symmetric vs Asymmetric — At A Glance

![symmetric vs asymmetric](svg/courses/security/secure-coding/03_encryption/symmetric_vs_asymmetric.svg)

---

## Symmetric vs Asymmetric

| | Symmetric | Asymmetric |
|---|---|---|
| Keys | one shared secret | public + private pair |
| Speed | fast | slow |
| Use for | bulk data | key exchange, signatures |
| Examples | `AES-GCM`, `ChaCha20-Poly1305` | `RSA`, `ECC`, `Ed25519` |

Real systems use both: asymmetric to agree on a key, symmetric to move the data — that is how `TLS` works.

---

## Authenticated Encryption (AEAD)

- Plain encryption hides data but does not detect tampering — an attacker can flip bits
- **AEAD** (Authenticated Encryption with Associated Data) gives confidentiality **and** integrity
- Use `AES-GCM` or `ChaCha20-Poly1305` — encryption and a MAC, in one operation
- "Associated data": headers you authenticate but do not encrypt (e.g., a message type)
- If your encryption call does not also authenticate, you are using the wrong one

---

## Hashing And MACs

- **Hash** — one-way fingerprint; `SHA-256`, `SHA-3`, `BLAKE2`. No key. Anyone can compute it
- **MAC** — keyed integrity tag; `HMAC-SHA-256`, `Poly1305`. Proves "someone with the key sent this"
- `MD5` and `SHA-1` are **broken** for security use — collisions are practical
- For passwords, a plain hash is wrong — use a slow KDF: **Argon2id**, `scrypt`, or `bcrypt`
- Compare MACs and tokens with a **constant-time** comparison, never `==`

---

## TLS / SSL And Secure Transport

- "SSL" is dead terminology — what runs today is **TLS 1.2 and TLS 1.3**; disable everything older
- `TLS 1.3` removed the dangerous legacy options (RC4, CBC modes, renegotiation, static `RSA` key exchange)
- **Validate certificates** — check the chain, the hostname, the expiry. Disabling verification "to make it work" is the classic catastrophic bug
- Use the platform / library defaults for cipher suites — do not hand-pick
- Consider mutual `TLS` for service-to-service traffic; pin or use a private CA

---

## Key Generation, Storage, And Rotation

- **Generate** from a cryptographic RNG: `os.urandom`, `getrandom(2)`, `/dev/urandom` — never `random.random()` or `rand()`
- **Store** outside the code: a secrets manager, `HSM`/`TPM`, or at minimum an env var or KMS-encrypted blob — never hardcoded, never in git
- **Rotate** on a schedule and on suspicion of compromise; tag ciphertext with the key id/version so old data still decrypts
- **Scope** keys narrowly — one purpose per key; a leaked key should have a small blast radius
- **Destroy** retired keys when no live data depends on them

---

## Cryptographic Pitfalls in C and C++

- **Memory exposure** — keys linger in freed buffers, swap, and core dumps; use the library's secure-zero (`OPENSSL_cleanse`, `sodium_memzero`), not `memset` (the compiler may elide it)
- **Nonce/IV reuse** — reusing a `GCM` nonce under the same key is catastrophic; use a counter or random 96-bit nonce, never a constant
- **Ignoring return values** — `EVP_*` calls fail; an unchecked failure can mean "no encryption happened"
- **Timing leaks** — `memcmp` on a MAC leaks via timing; use `CRYPTO_memcmp`
- **Hand-rolled padding / parsing** — buffer overflows in the crypto glue, not the cipher

---

## Cryptographic Pitfalls in Python

- `random` is **not** cryptographic — use `secrets` (`secrets.token_bytes`, `secrets.token_urlsafe`) or `os.urandom`
- Old `pycrypto` is unmaintained — use the `cryptography` package or `PyNaCl`
- Use `Fernet` or `AESGCM` from `cryptography`, not bare `Cipher(AES, modes.ECB)` — **ECB is not encryption**, it leaks patterns
- For passwords: `argon2-cffi` or `bcrypt`, never `hashlib.sha256(password)`
- Compare tokens with `hmac.compare_digest`, never `==`
- `pickle` is not encryption and not safe on untrusted input — different problem, equally fatal

---

## Crypto Agility

- Algorithms get broken — `MD5`, `SHA-1`, `RC4`, `DES`, `RSA-1024` are all dead now
- Tag every ciphertext, signature, and token with the algorithm and version that produced it
- Build migration paths *before* you need them — emergency crypto swaps go badly
- **Post-quantum is coming** — a sufficiently large quantum computer breaks `RSA` and `ECC`; `NIST` has standardized replacements (ML-KEM, ML-DSA). Plan the transition now

---

## Takeaways

- Don't roll your own — use libsodium, OpenSSL, or `Python` `cryptography`
- Use `AEAD` (`AES-GCM`, `ChaCha20-Poly1305`); plain encryption is not enough
- `MD5`/`SHA-1` are broken; passwords need Argon2/`bcrypt`, not a fast hash
- `TLS 1.2`/`1.3` only, and **actually validate certificates**
- Keys from a CSPRNG, out of the code, rotated, scoped — and tag everything for agility
