---
tags:
  - security:jwt
  - concepts:tokens
level: intermediate
category: security
audience:
  - audiences:developers

---
# JWT in Depth

---
## What This Chapter Covers

- JWT structure: header, payload, signature
- Algorithms: HS256, RS256, ES256
- Validation steps
- Common claims
- Pitfalls and attacks

---
## What Is a JWT?

- JSON Web Token (RFC 7519)
- A signed, base64url-encoded string
- Three parts separated by dots: `header.payload.signature`
- Self-contained — carries claims and a signature
- Used for ID tokens and often access tokens

---
## JWT Structure Visualized

![jwt_anatomy](svg/courses/networking/oauth2-and-oidc/07_jwt/jwt_anatomy.svg)

---
## Three Parts

- Header — algorithm and key ID
- Payload — claims (the data)
- Signature — prevents tampering
- All three are base64url-encoded
- Signature covers header + payload

---
## Header Example

```json
{
  "alg": "RS256",
  "typ": "JWT",
  "kid": "key-2026-04"
}
```

- `alg` — signing algorithm
- `typ` — always `JWT` (or omitted)
- `kid` — key ID for rotation

---
## Payload (Claims) Example

```json
{
  "iss": "https://auth.example.com",
  "sub": "user_42",
  "aud": "client_xyz",
  "exp": 1703012400,
  "iat": 1703008800,
  "scope": "read:profile"
}
```

- Standard claims plus custom ones
- All values JSON

---
## Standard Claims

- `iss` — issuer
- `sub` — subject (user)
- `aud` — audience
- `exp` — expiration time (epoch)
- `nbf` — not before time
- `iat` — issued at
- `jti` — unique JWT ID

---
## Signature

- `signature = HMAC_SHA256(base64(header) + "." + base64(payload), secret)`
- Or RSA/EC signature with private key
- Verifier recomputes and compares
- Detects any tampering with header or payload
- The whole point of a JWT

---
## Signing Algorithms

- HS256 — HMAC-SHA256, symmetric (shared secret)
- RS256 — RSA + SHA256, asymmetric
- ES256 — ECDSA + SHA256, asymmetric (smaller keys)
- PS256 — RSA with probabilistic padding, modern variant
- Ed25519 — modern, fast, small

---
## HS256 vs RS256

- HS256: same secret signs and verifies
- RS256: private key signs, public key verifies
- HS256 simpler but secret must be widely shared
- RS256 better for distributed validation
- Use RS256 (or ES256) in OAuth2/OIDC

---
## JWT Pitfall Catalogue

![jwt_pitfalls](svg/courses/networking/oauth2-and-oidc/07_jwt/jwt_pitfalls.svg)

---
## The "alg=none" Attack

- A malicious token with `alg: "none"`
- Library accepts it without checking signature
- Attacker forges any claims
- Real CVEs from 2015 onward
- Modern libraries reject this; verify yours does

---
## Algorithm Confusion Attack

- Server uses RS256 (asymmetric)
- Attacker sends a JWT with `alg: HS256` using the public key as the HMAC secret
- Vulnerable libraries verify it as valid
- Critical: pin the algorithm explicitly when verifying
- Don't trust `alg` from the header

---
## Validation Steps

- Decode header; check `alg` matches what you expect
- Look up signing key by `kid`
- Verify signature with the correct algorithm
- Check `iss`, `aud`, `exp`, `nbf`, `iat`
- Check any custom claims your app needs

---
## Validation in Pseudocode

```python
def validate(jwt, expected_iss, expected_aud):
    header, payload, sig = decode(jwt)
    assert header["alg"] == "RS256"
    key = jwks.get(header["kid"])
    verify_rs256(jwt, key)
    assert payload["iss"] == expected_iss
    assert payload["aud"] == expected_aud
    assert payload["exp"] > now()
    return payload
```

---
## JWKS: Key Distribution

- JSON Web Key Set
- Auth server publishes public keys at `/.well-known/jwks.json`
- Each key has a `kid`
- Clients fetch and cache
- Re-fetch on cache miss for unknown `kid`

---
## JWKS Example

```json
{
  "keys": [
    {
      "kty": "RSA",
      "kid": "key-2026-04",
      "use": "sig",
      "alg": "RS256",
      "n": "modulus...",
      "e": "AQAB"
    }
  ]
}
```

---
## Key Rotation

- Auth server rotates keys periodically
- Old and new live side-by-side during rotation
- Tokens carry `kid` so clients pick the right key
- Clients re-fetch JWKS on unknown `kid`
- Standard practice in OIDC

---
## Lifetimes for JWT

- Short access tokens: 5-15 min
- ID tokens: same as access
- Long lifetimes amplify any leak
- Pair with refresh tokens for UX
- Don't use 24h JWTs without a strong reason

---
## JWT vs Opaque Tokens (Recap)

- JWT: stateless, scales, hard to revoke
- Opaque: stateful, revocable, slower
- Use JWT for most APIs
- Use opaque or hybrid for high-revocation needs
- Many auth servers offer both

---
## Encrypted JWTs

- JSON Web Encryption (RFC 7516)
- Encrypts the payload, not just signs it
- Five parts instead of three
- Use when claims are sensitive
- Most OAuth2 deployments use signed JWTs, not encrypted

---
## When to Encrypt

- Claims contain personally identifiable info you don't want exposed
- Tokens travel through untrusted intermediaries
- Compliance requires encrypted-at-rest tokens
- Otherwise, signing alone is enough
- Clients almost never decrypt; auth servers use encryption for inter-server

---
## Common JWT Pitfalls

- Trusting `alg` from the header
- Not validating `aud`
- Long-lived tokens with no revocation strategy
- Storing tokens in localStorage (XSS exposure)
- Logging tokens (please don't)

---
## Decoding JWTs for Debugging

- jwt.io — decodes and validates in browser (don't paste prod tokens)
- `jwt-cli` — command-line decoder
- Most languages have library decoders
- Decoding is not validating — never trust without verifying signature

---
## Best Practices

- Pin the expected algorithm during validation
- Always check `iss` and `aud`
- Short token lifetimes; pair with refresh
- Use JWKS for key distribution
- Monitor for unusual `kid` values

---
## When NOT to Use JWT

- Sessions where you can use server-side session storage instead
- Cases where revocation is a hard requirement
- Very small payloads where overhead matters
- Use the right tool — JWT isn't always it

---
## Summary

- JWT: header + payload + signature, base64url-encoded
- RS256/ES256 over HS256 for OAuth2/OIDC
- Validate signature, then claims, every time
- `alg=none` and algorithm confusion are real attack classes
- Short lifetimes + JWKS rotation = solid foundation
