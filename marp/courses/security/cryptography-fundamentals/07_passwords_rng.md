---
tags:
  - security:cryptography
  - security:passwords
level: intermediate
category: security
audience:
  - audiences:developers
  - audiences:security-professionals
---

# Password Storage and Randomness

---

## Why simple hashing is not enough

- Plain `SHA256(password)` is **fast** — a GPU does billions per second
- Same password → same hash → "rainbow table" precomputed lookups
- An attacker who steals your DB cracks 90% of weak passwords in hours
- Hash functions were designed for speed; password hashing needs the opposite

You need a function that is **slow on purpose** and **unique per user**.

---

## Salting

- Random per-user value mixed into the hash
- Defeats rainbow tables — attacker must recompute per user
- Must be **per-user random**, not a single global salt
- Stored alongside the hash — not secret, just unique
- 16+ random bytes from a CSPRNG

```output
salt = os.urandom(16)
stored = salt + slow_hash(password, salt)
```

A salt does not slow individual cracking attempts. It just prevents amortizing work across users.

---

## bcrypt

- Designed in 1999, based on Blowfish key schedule
- **Cost factor** — each increment doubles the work
- Default 10–12 today; raise as hardware speeds up
- Maximum 72-byte password (silent truncation — be aware)
- Output is self-describing: `$2b$12$<salt><hash>`

```python
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
bcrypt.checkpw(password.encode(), hashed)  # bool
```

Solid choice for legacy compatibility. Argon2 is the modern preference.

---

## scrypt and memory hardness

- Designed by Colin Percival, 2009
- **Memory-hard**: requires lots of RAM, not just CPU
- Defeats GPUs and ASICs by making memory the bottleneck
- Parameters: N (work), r (memory), p (parallelism)
- Used in Litecoin, Tarsnap, some password vaults

scrypt was the first widely-deployed memory-hard KDF. Argon2 took the next step.

---

## Argon2 — current best practice

- Winner of the 2015 Password Hashing Competition
- Three variants: Argon2d (GPU-resistant), Argon2i (side-channel resistant), **Argon2id** (combines both)
- Argon2id is the OWASP-recommended default
- Tunable memory, time, and parallelism

```python
from argon2 import PasswordHasher
ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4)
hash = ph.hash(password)
ph.verify(hash, password)  # raises on mismatch
```

For new systems: Argon2id with OWASP parameters. Done.

---

## Password Hashing Compared

![argon2](svg/courses/security/cryptography-fundamentals/07_passwords_rng/argon2.svg)

---

## OWASP parameter recommendations (2024)

- **Argon2id** — m=19 MiB, t=2, p=1 (or m=12 MiB, t=3, p=1)
- **bcrypt** — cost ≥ 10
- **scrypt** — N ≥ 2^17, r=8, p=1
- **PBKDF2-HMAC-SHA256** — ≥ 600,000 iterations (last resort)

Tune so login takes ~50–500ms on your hardware. Cracking gets harder; users do not notice.

---

## Don't roll your own

- Do not invent: `SHA256(password + "secret")`, `MD5(password)`, custom rounds
- Use a library: argon2-cffi, bcrypt, libsodium
- Resist the urge to "improve" the algorithm
- Resist the urge to write password hashing without a library

The mistakes are subtle. Use what has been peer-reviewed and battle-tested.

---

## Random number generation

- All cryptography depends on **unpredictable** randomness
- Keys, nonces, IVs, salts, session tokens — all need CSPRNG
- A predictable random output undermines everything else

```python
# correct
import os, secrets
key = os.urandom(32)
token = secrets.token_urlsafe(32)

# WRONG — never for security
import random
key = random.randbytes(32)  # predictable
```

---

## OS entropy sources

- **Linux** — `/dev/urandom` (always available, fine for crypto)
- **Linux** — `/dev/random` (blocks for entropy, rarely needed)
- **Windows** — `BCryptGenRandom`, `CryptGenRandom`
- **macOS/BSD** — `arc4random`
- All seeded from kernel entropy pools (interrupt timing, hardware RNG)

Use the language stdlib (`os.urandom`, `crypto.randomBytes`) — it picks the right one.

---

## Common RNG mistakes

- `random.random()` for security — predictable Mersenne Twister
- `srand(time())` for keys — guessable seed
- Reusing the same nonce across encryptions
- Custom "shuffles" that bias the output
- VM cloning that duplicates the RNG state at fork time
- Embedded devices with no entropy at boot

If your security depends on randomness, depend on the OS RNG. Never invent a substitute.

---

## Testing for brokenness

- Generate a million tokens, check they are all distinct
- Run NIST randomness test suite (or rngtest)
- Use diagnostic tools — `dieharder`, `TestU01`
- For embedded: collect entropy at first boot before generating long-term keys

You cannot prove an RNG is good. You can usually spot one that is bad.
