---
tags:
  - security:secure-coding
  - hardware-and-embedded:embedded
  - security:application-security
level: intermediate
category: security
audience:
  - audiences:embedded-engineers
  - audiences:developers
  - audiences:security-professionals
---
# Designing Secure Protocols with Hardware

---

## What This Chapter Covers

- Hardware security fundamentals
- Hardware-software trust boundaries
- Designing secure communication protocols
- Attestation and authentication mechanisms
- Key management with hardware support

---

## Why Bring Hardware Into It?

- Software secrets live in memory — readable by anyone with the right access
- Hardware can hold a key that **never leaves the chip**, even under physical attack
- It gives you a root of trust you do not have to recreate at boot
- It anchors identity: "this is genuinely device #4711, not an emulator"
- The cost: complexity, supply chain for the hardware itself, harder updates

---

## Hardware Security Fundamentals

- **Secure key storage** — keys generated and used inside the chip; export is impossible
- **Cryptographic accelerators** — fast `AES`, `ECC`, hashing without exposing keys
- **True random number generators** — entropy from physical noise, not a PRNG
- **Tamper resistance** — detect probing, voltage glitching, side channels
- **Unique device identity** — a factory-provisioned key or fuse per device
- Examples: `TPM`, secure elements, ARM TrustZone, dedicated security chips

---

## Hardware-Software Trust Boundaries

- Draw the line: what runs in the trusted hardware vs. the rich (untrusted) OS
- Everything crossing the boundary must be **validated** — assume the OS side is hostile
- Keep the trusted side **small** — less code, less attack surface, easier to audit
- The hardware exposes operations ("sign this", "decrypt that"), never the key
- Define the threat model explicitly: what is the hardware protecting *against*?

---

## Hardware Trust Boundary

![trust boundary](svg/courses/security/secure-coding/02_hardware_protocols/trust_boundary.svg)

---

## Anatomy Of A Secure Channel

![secure channel](svg/courses/security/secure-coding/02_hardware_protocols/secure_channel.svg)

---

## Designing Secure Communication Protocols

- **Do not invent your own** — use `TLS`, `Noise`, or another reviewed protocol
- Required properties: confidentiality, integrity, authentication, replay protection
- **Mutual authentication** — both ends prove identity, not just the server
- **Forward secrecy** — a stolen long-term key does not decrypt past sessions
- **Freshness** — nonces, counters, or timestamps so old messages cannot be replayed
- Fail closed — an unauthenticated peer gets nothing

---

## Attestation And Authentication

- **Authentication** — "I am device #4711" (prove possession of a device key)
- **Attestation** — "and I am running firmware version X with these measurements"
- Attestation is signed by a key the device cannot forge or extract
- A remote verifier checks the signature and the reported state before trusting the device
- Used for: provisioning, onboarding, conditional access, fleet integrity checks
- Ties directly to measured boot (see the Secure Boot chapter)

---

## Key Management With Hardware Support

- **Generate** keys inside the hardware — they are born protected, never seen in software
- **Use** keys via opaque handles — your code says "sign with handle 3", not "here is the key"
- **Rotate** by provisioning new keys and retiring old handles; tag data with the key version
- **Hierarchy** — a device root key wraps session keys; only the root needs hardware
- **Destroy** by clearing the slot — the data it protected is now unrecoverable
- Backup is the hard part — a key that cannot be extracted cannot be backed up

---

## A Worked Example: Device Onboarding

1. 1. 1. Device boots; secure boot verifies firmware (chain of trust holds)
1. 1. 1. Device generates a key pair inside its secure element
1. 1. 1. Device sends the public key plus a signed attestation of its firmware state
1. 1. 1. Backend verifies the attestation against known-good measurements
1. 1. 1. Backend issues a certificate binding the device identity to the public key
1. 1. 1. All later traffic uses mutually authenticated `TLS` with that certificate

---

## Takeaways

- Hardware buys you a root of trust and keys that never leave the chip
- Keep the trusted side small; validate everything crossing the boundary
- Never roll your own protocol — use `TLS` or `Noise`, with mutual auth and forward secrecy
- Authentication says who; attestation says who *and* in what state
- Hardware-backed keys: generate inside, use by handle, rotate by version
