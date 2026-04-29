---
tags:
  - security:cryptography
  - security:asymmetric
level: intermediate
category: security
audience:
  - audiences:developers
  - audiences:security-professionals
---
# Asymmetric Encryption

---

## The two-key idea

- Each party has a **key pair**: public key and private key
- What one encrypts, only the other can decrypt
- Publish the public key freely; guard the private key absolutely
- Solves the key-distribution problem of symmetric crypto

You can encrypt to anyone whose public key you can find, without ever sharing a secret with them in advance.

---

## Two distinct uses

| Direction | Public key does | Private key does | Purpose |
|---|---|---|---|
| Encrypt | encrypts | decrypts | confidentiality |
| Sign | verifies | signs | authentication |

The same math, two opposite usages. Confusing them is a classic source of bugs — never use the same RSA key for both encryption and signing.

---

## RSA in one minute

- Pick two large primes p and q; n = p * q
- Public key: (n, e) where e is small (usually 65537)
- Private key: d such that e * d ≡ 1 mod φ(n)
- Encrypt: c = m^e mod n; Decrypt: m = c^d mod n
- Security rests on the difficulty of **factoring n**

Strength is set by key size: 2048 bits is the modern minimum, 4096 is conservative, 1024 is broken.

---

## RSA caveats

- **Slow** compared to symmetric — never use it for bulk data
- Can only encrypt data smaller than the key size
- Must use proper padding: **OAEP** for encryption, **PSS** for signatures
- PKCS#1 v1.5 padding has known attacks (Bleichenbacher) — avoid for new code

The standard RSA pattern: encrypt a random AES key with RSA, then use AES to encrypt the actual data. This is "hybrid encryption."

---

## Elliptic Curve Cryptography

- Same one-way function idea, but using points on an elliptic curve
- 256-bit ECC ≈ 3072-bit RSA in security
- Smaller keys, smaller signatures, faster operations
- Common curves: P-256 (NIST), Curve25519 (Bernstein), secp256k1 (Bitcoin)

For new code, prefer ECC over RSA. Smaller, faster, equivalently secure.

---

## ![w:50](svg/courses/security/cryptography-fundamentals/03_asymmetric/dh_exchange.svg)

---

![](svg/courses/security/cryptography-fundamentals/03_asymmetric/dh_exchange.svg)

---

## Diffie-Hellman key exchange

- Two parties **agree on a shared secret** over a public channel
- Neither sends the secret — they each compute it locally
- Eavesdroppers see the public values but cannot derive the shared key
- Discrete-log problem: g^ab mod p is easy to compute knowing a or b, hard otherwise

DH does not authenticate — without signatures, a man-in-the-middle can intercept. Always combine DH with authentication (certificates).

---

## Curve selection

- **Curve25519 (X25519)** — DH; fast, simple, hard to misuse
- **Ed25519** — signatures; companion to X25519
- **P-256 (secp256r1)** — NIST standard; widely deployed in TLS
- **P-384, P-521** — bigger NIST curves; rarely needed
- **secp256k1** — Bitcoin/Ethereum; works for general use too

Default to Curve25519/Ed25519 unless interoperability demands otherwise.

---

## Hybrid encryption — the universal pattern

```
1. Generate a random symmetric key K
2. Encrypt the data with K using AES-GCM
3. Encrypt K with the recipient's public key
4. Send (encrypted_K, encrypted_data)
```

- Combines asymmetric (key transport) + symmetric (bulk speed)
- Used by TLS, age, GPG, S/MIME, JWE
- "Encrypting a file" with RSA almost always means this pattern

You almost never use raw asymmetric encryption on application data.

---

## Performance comparison

| Operation | RSA-2048 | RSA-4096 | ECDSA P-256 | Ed25519 |
|---|---|---|---|---|
| Sign | 1ms | 6ms | 0.05ms | 0.05ms |
| Verify | 0.05ms | 0.1ms | 0.15ms | 0.1ms |
| Key gen | 100ms | 1000ms | 0.1ms | 0.05ms |

Numbers vary by hardware, but the shape is consistent: ECC is dramatically faster for signing and key generation; RSA is faster for verification.

---

## When to pick what

- **TLS server cert** — ECDSA P-256 (smaller, faster handshake)
- **SSH key** — Ed25519 (modern, simple, fast)
- **Code signing** — RSA-4096 with PSS (long-term, broad tool support)
- **JWT signing** — Ed25519 if your library supports it; ES256 otherwise
- **Encrypting a file for someone** — age (X25519 + ChaCha20-Poly1305)

Match the algorithm to the deployment, not to what you learned in school.
