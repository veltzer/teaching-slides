---
tags:
  - security:cryptography
  - security:libraries
level: intermediate
category: security
audience:
  - audiences:developers
  - audiences:security-professionals
---
# Pitfalls, Libraries, and the Post-Quantum Future

---

## Don't roll your own crypto

- The first rule of cryptographic engineering
- Even cryptographers don't roll their own — they collaborate, peer-review, publish, fix
- Subtle bugs (off-by-one in counter, biased random sampling) ruin security entirely
- Compiler optimizations can introduce timing leaks
- Side channels are easy to introduce, hard to detect

If you find yourself writing the inner loop of an encryption algorithm: stop. Use a library.

---

## ECB usage in the wild

- Adobe leaked 150M password hashes in ECB mode (2013) — recoverable patterns
- Many "encrypted" databases use ECB by default and call it secure
- Pictures encrypted with ECB still show their content
- IoT devices ship with ECB-encrypted firmware

If your library's "encrypt" function takes only key + data with no IV — investigate. Likely ECB.

---

## Nonce reuse

- AES-GCM reuse: same key + nonce + different plaintext → keystream recovered
- ChaCha20-Poly1305 same story
- ECDSA k reuse: private key recoverable from two signatures
- IV reuse in CBC: leaks information about prefix similarity

Track nonces. Use a counter or 12 bytes from `os.urandom`. Never reset.

---

## Weak algorithms still in use

| Should be gone | Sometimes still seen |
|---|---|
| MD5 | yes — git, package checksums |
| SHA-1 | yes — TLS certs (mostly retired), git |
| RC4 | yes — old WPA, old TLS |
| 3DES | yes — financial systems |
| RSA-1024 | yes — embedded devices |
| DES | yes — cash machines, kerberos legacy |

Inventory your stack. Replace what you find.

---

## Timing attacks

- Compare two MAC tags byte-by-byte → leaks how many bytes matched
- Modular exponentiation that branches on key bits → leaks the key
- SQL queries that return faster on user-not-found
- Network timing measured remotely is precise enough to extract keys

Use **constant-time comparison**: `hmac.compare_digest`, `subtle.ConstantTimeCompare` (Go), `sodium_memcmp`.

---

## Hard-coded secrets

- Keys in source: visible to everyone with repo access, leak via git history
- Keys in container images: visible to anyone who pulls the image
- Keys in build artifacts: shipped to every customer
- API keys in mobile apps: extractable in minutes

Use environment variables, secret managers, KMS, HSM. Rotate when exposed.

---

## Picking a Library

![library_choice](svg/courses/security/cryptography-fundamentals/08_pitfalls_libraries/library_choice.svg)

---

## Library landscape

- **OpenSSL** — the workhorse; CLI + libcrypto/libssl; complex API
- **libsodium** — modern, high-level, hard to misuse
- **NaCl** — libsodium's progenitor; minimal API, opinionated defaults
- **Python `cryptography`** — Pythonic wrapper around OpenSSL
- **Go `crypto/*`** — stdlib; comprehensive
- **BoringSSL** — Google's OpenSSL fork; not for general use
- **Rust `ring`, `rustcrypto`** — pure-Rust implementations

Pick mainstream, actively maintained, with good documentation.

---

## libsodium — the recommendation

- High-level: `crypto_secretbox` for symmetric, `crypto_box` for asymmetric
- Sensible defaults; almost no knobs to turn the wrong way
- Available for C, Python, JavaScript, Go, Rust, etc.
- Bindings are thin wrappers — same security guarantees

```python
from nacl.secret import SecretBox
import nacl.utils
key = nacl.utils.random(SecretBox.KEY_SIZE)
box = SecretBox(key)
ciphertext = box.encrypt(b"hello")  # nonce auto-included
```

If you don't have a strong reason to pick something else, libsodium is the answer.

---

## OpenSSL CLI essentials

```output
# generate keys
openssl genrsa -out key.pem 4096
openssl ec -genkey -name prime256v1 -out ec.pem

# inspect a cert
openssl x509 -in cert.pem -text -noout

# test TLS
openssl s_client -connect example.com:443 -servername example.com

# generate CSR
openssl req -new -key key.pem -out csr.pem
```

These four are 90% of operational TLS work.

---

## The quantum threat

- A sufficiently large quantum computer breaks RSA, ECC, DH in polynomial time (Shor's algorithm)
- Symmetric crypto (AES) only loses half its bits to Grover — AES-256 still safe
- Hashes lose half their collision resistance — SHA-384+ for long-term
- "Harvest now, decrypt later" — adversaries record traffic for future decryption

Estimated break date: 5–30 years. Long-term secrets need protection now.

---

## NIST post-quantum standardization

- 2016 — NIST opened competition for PQ algorithms
- 2022 — first winners: Kyber (KEM), Dilithium and Falcon (signatures), SPHINCS+ (signatures)
- 2024 — formally standardized as ML-KEM, ML-DSA, SLH-DSA
- Hybrid mode: classical + PQ in parallel — protects against either being broken

Browsers, TLS libraries, Cloudflare, Google all rolling out hybrid X25519+Kyber now.

---

## Migration planning

- **Inventory** — where is RSA/ECC used? Long-term keys, signatures, transport?
- **Crypto-agility** — can you swap algorithms without rewrite?
- **Hybrid first** — deploy classical + PQ in parallel
- **Long-term data** — encrypt with PQ-resistant scheme today
- **Wait on signatures** — unless data must be verifiable in 30 years
- **Size matters** — Dilithium signatures are ~2KB vs Ed25519's 64 bytes

The point of crypto-agility is to be ready when the time comes, not to predict when.

---

## Final survival rules

1. Use libraries; never write your own primitives
1. AEAD for encryption (AES-GCM, ChaCha20-Poly1305)
1. Argon2id for passwords
1. `os.urandom` for randomness
1. Constant-time comparison for tags
1. TLS 1.3, mandatory; disable everything older
1. Plan for PQ migration; deploy hybrid where you can
1. Read the OWASP Cryptographic Storage Cheat Sheet annually

The boring choices are the safe choices.
