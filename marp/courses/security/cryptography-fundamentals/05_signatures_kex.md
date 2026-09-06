---
tags:
  - security:cryptography
  - security:signatures
level: intermediate
category: security
audience:
  - audiences:developers
  - audiences:security-professionals
---

# Digital Signatures and Key Exchange

---

## What a signature buys you

- **Authenticity** — only the holder of the private key could have produced this
- **Integrity** — any change to the message invalidates the signature
- **Non-repudiation** — the signer cannot later deny signing
- **Public verifiability** — anyone with the public key can check

The crypto building block behind: code signing, TLS certificates, JWTs, package managers, software updates, blockchain.

---

## How signing actually works

```output
sign:    sig = sign(privkey, hash(message))
verify:  verify(pubkey, hash(message), sig)
```

- You sign the **hash** of the message, not the message itself
    - Asymmetric ops are slow; hashes are fast
    - Hash of any size message fits in one signing operation
- The signature is bound to the exact bytes via the hash
- Change one bit of the message → completely different hash → signature invalid

---

## RSA signatures

- **PKCS#1 v1.5** — old, deterministic, has known attacks; avoid in new code
- **PSS** — Probabilistic Signature Scheme; modern, randomized, secure
- 2048-bit RSA minimum; 3072 or 4096 for long-term
- Slow: 1-6ms to sign, fast to verify

```python
from cryptography.hazmat.primitives.asymmetric import padding
sig = priv.sign(msg, padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                  salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256())
```

---

## ECDSA — Elliptic Curve DSA

- The standard NIST curve signature scheme
- Curves: P-256, P-384, P-521 (commonly P-256)
- Smaller than RSA for equivalent security
- **Critical caveat**: needs strong randomness for each signature. Reusing the random k reveals the private key (Sony PS3 hack, 2010)

ECDSA is everywhere — TLS certs, Bitcoin, JWT ES256. Just use a library that handles k correctly.

---

## Ed25519 — modern signatures done right

- Edwards-curve Digital Signature Algorithm on Curve25519
- **Deterministic** — k derived from private key + message, no RNG needed
- Simple, fast, hard to misuse
- Small: 32-byte public key, 64-byte signature
- Used in: SSH, Tor, modern TLS, age, sigstore

For new systems where you control both ends: Ed25519 is the right answer.

---

## Sign and Verify

![sign_verify](svg/courses/security/cryptography-fundamentals/05_signatures_kex/sign_verify.svg)

---

## Code signing

- Distribute software with a signature; user verifies before executing
- Apple, Microsoft, Google Play all enforce this
- Linux: package managers (apt, dnf) verify GPG signatures of repositories
- Container images: cosign + sigstore for OCI artefacts
- Drivers: kernel-mode code must be signed on Windows

The chain of trust is rooted in publisher certificates installed on user systems.

---

## Forward secrecy

- A property of session protocols: compromising long-term keys later does not expose past sessions
- Achieved by **ephemeral** key exchange (DHE, ECDHE) for each session
- Even if the server's private key leaks tomorrow, today's traffic stays safe
- TLS 1.3 mandates forward secrecy; TLS 1.2 has it as an option

If your protocol uses static RSA key exchange, every session is forever vulnerable to a future key compromise.

---

## Authenticated key exchange

- DH alone has no identity — open to man-in-the-middle
- Add signatures over the DH values to prove identity
- TLS pattern:
  1. Server signs (DHE_pub, hostname) with its cert key
  1. Client verifies the cert chain back to a trusted root
  1. Client + server complete DH to derive the session key
- Same idea in SSH, Signal, Noise framework

You need both the speed of DH for key agreement and the identity of signatures for authentication.

---

## Key derivation functions

- Take one secret + context, produce purpose-specific keys
- **HKDF** — modern, two-step (extract + expand); HMAC-based
- **PBKDF2** — older, password-oriented, simpler API
- Use HKDF when you have a high-entropy secret already (e.g., from DH)
- Use Argon2/PBKDF2 when deriving from a password

```python
hkdf = HKDF(algorithm=hashes.SHA256(), length=32,
            salt=salt, info=b"my-app encryption key")
key = hkdf.derive(shared_secret)
```

---

## Key agreement vs key transport

- **Key agreement** (DH/ECDH) — both parties contribute to the shared secret
- **Key transport** (RSA encrypt of a key) — one party generates, sends to other

Agreement gives forward secrecy; transport does not. TLS 1.3 dropped RSA key transport entirely.

When you can: use ECDH(E). When you must use RSA: limit it to authentication, not key transport.
