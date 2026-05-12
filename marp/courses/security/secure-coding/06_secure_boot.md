---
tags:
  - security:secure-coding
  - hardware-and-embedded:embedded
  - operating-systems:linux
level: intermediate
category: security
audience:
  - audiences:embedded-engineers
  - audiences:developers
  - audiences:security-professionals
---
# Secure Boot

---

## What This Chapter Covers

- The boot chain of trust
- `UEFI` Secure Boot
- Bootloader verification
- Kernel and module signing
- Measured boot and trusted platform modules

---

## Why Boot Security?

- All your OS-level security assumes the OS itself is genuine — if the boot path is compromised, nothing above it can be trusted
- A bootkit / rootkit installed below the OS is invisible to the OS and survives reinstall
- "Evil maid" attacks: brief physical access to tamper with the bootloader or firmware
- For embedded devices in the field: prevent running modified or counterfeit firmware
- The job: establish trust at power-on and carry it up, stage by stage

---

## The Boot Chain Of Trust

- Each stage **verifies the next before handing off**, starting from something unforgeable
- **Root of trust** — immutable code/keys in ROM or fuses; you cannot change it, so you must be able to trust it
- ROM → first-stage bootloader → second-stage bootloader → kernel → init / OS
- Break any link and everything *above* it is suspect — the chain is only as strong as its weakest verification
- "Secure boot" enforces this: refuse to run an unsigned or wrongly-signed next stage
- "Measured boot" records what ran (without necessarily refusing) for later attestation

---

## The Boot Chain Of Trust

![chain of trust](svg/courses/security/secure-coding/06_secure_boot/chain_of_trust.svg)

---

## UEFI Secure Boot

- Firmware feature: only execute bootloaders/drivers signed by a key in the firmware's database
- Key hierarchy: **PK** (Platform Key) → **KEK** (Key Exchange Keys) → **db** (allowed signatures) / **dbx** (revoked signatures)
- On PCs: Microsoft's keys are pre-enrolled; Linux distros boot via a signed `shim` that then verifies GRUB
- `dbx` is the revocation list — how a known-bad bootloader (e.g., BootHole-era GRUB) gets blocked
- You can enroll your own keys ("setup mode") for full control — common on embedded and locked-down systems
- It only covers the firmware → bootloader handoff; the kernel must continue the chain

---

## Bootloader Verification

- The bootloader is the pivot — it is verified by firmware and must in turn verify the kernel
- It must check the kernel image **and** the initramfs **and** the kernel command line (an attacker editing `init=/bin/sh` bypasses everything)
- GRUB can verify signed kernels; embedded loaders like U-Boot have a "verified boot" / FIT-image signing mechanism
- Keep the bootloader minimal and updatable — it is security-critical code that needs patching
- Anti-rollback: refuse to load an older, known-vulnerable version (counter in fuses or `TPM`)

---

## Kernel And Module Signing

- The verified kernel must extend the chain into what *it* loads
- **Module signing** — the kernel refuses to load unsigned modules (`module.sig_enforce=1`); blocks malicious driver injection
- **Lockdown mode** — restricts even root from paths that could patch the running kernel (`/dev/mem`, kexec of unsigned images, certain debug interfaces)
- **IMA/EVM** — Linux Integrity Measurement Architecture: measure and/or appraise files (including userspace binaries) against signatures before execution
- **dm-verity** — read-only root filesystem with a hash tree; any tampered block is detected on read (Android, ChromeOS, many appliances)

---

## Measured Boot And TPMs

- Different goal from "refuse to boot": **record** what executed so a verifier can judge it later
- Each stage hashes the next and **extends** the digest into a `TPM` **PCR** (Platform Configuration Register) — a one-way running tally that cannot be rewound
- The resulting PCR values are a fingerprint of exactly what booted
- **Remote attestation** — the `TPM` signs a quote of the PCRs; a server checks it against known-good values before granting access (ties back to the hardware-protocols chapter)
- **Sealing** — encrypt data so it only decrypts when the PCRs match (e.g., a disk-encryption key released only to a known-good boot state — `systemd-cryptenroll`, BitLocker)

---

## Secure Boot vs Measured Boot

| | Secure Boot | Measured Boot |
|---|---|---|
| Action | refuse bad stages | record every stage |
| Decision point | at boot, locally | later, by a verifier |
| Backing | firmware key DB | `TPM` PCRs |
| Failure mode | does not boot | boots, but attestation fails |
| Best together | gate the boot | prove the state |

Use both: secure boot stops the obvious; measured boot lets you *prove* the result.

---

## Takeaways

- Everything above the boot path trusts that the boot path is genuine — so secure it first
- Chain of trust: an immutable root, each stage verifying the next before handoff
- `UEFI` Secure Boot covers firmware → bootloader; the kernel continues it (module signing, lockdown, IMA, dm-verity)
- Verify the kernel command line and initramfs too — not just the kernel image
- Measured boot + `TPM` PCRs turn "we booted clean" into something you can attest and seal secrets to
