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
# Secure Element

---

## What This Chapter Covers

- What a secure element is
- Trusted Platform Module (`TPM`)
- Hardware Security Modules (`HSM`)
- Secure enclaves and trusted execution environments
- Integrating secure elements into applications

---

## What Is A Secure Element?

- A tamper-resistant chip (or chip region) that stores keys and runs crypto operations **without ever exposing the keys**
- You hand it data and a key handle; it hands back a signature, MAC, or decrypted blob — the key stays inside
- Hardened against physical attack: probing, glitching, side-channel analysis, decapping
- Often certified — Common Criteria EAL levels, `FIPS 140-2/3`
- Examples: smartcards, SIM/eSIM, the SE in phones, dedicated chips (ATECC608, OPTIGA), `TPM`s, `HSM`s
- The common thread: **secrets are born inside and never leave**

---

## Trusted Platform Module (TPM)

- A standardized (TCG `TPM` 2.0) security chip — discrete, firmware, or integrated into the CPU (fTPM, PTT)
- What it gives you:
    - Secure key generation and storage (keys wrapped under a hardware root)
    - **PCRs** — measurement registers for measured boot and sealing (previous chapter)
    - **Attestation** — signed quotes of platform state
    - A hardware RNG and a monotonic counter (anti-rollback)
- On Linux: `/dev/tpm0`, the `tpm2-tools` suite, `tpm2-pkcs11`; integrates with LUKS, `systemd-cryptenroll`, SSH
- Cheap, ubiquitous, low-throughput — great for *device* keys, not for bulk crypto

---

## Hardware Security Module (HSM)

- The heavyweight: a dedicated appliance or PCIe card for high-assurance, high-throughput key operations
- Generates, stores, and uses keys; many keys; thousands of ops/sec; clustered for HA
- Where you find them: CAs (root key lives in an `HSM`, often offline), payment processing, code-signing infrastructure, cloud KMS backends (AWS CloudHSM, Azure Dedicated HSM, GCP Cloud HSM)
- Strict access control, role separation (m-of-n quorum to use the master key), full audit logs
- `FIPS 140-2/3` Level 3+ certified
- Interface: **`PKCS#11`**, KMIP, or vendor SDKs — your app calls the `HSM`, the key never comes back

---

## Secure Element Landscape

![secure element landscape](svg/courses/security/secure-coding/07_secure_element/landscape.svg)

---

## Secure Enclaves And TEEs

- A **TEE** (Trusted Execution Environment) carves the *main CPU* into a trusted world and a normal world
- Code in the enclave runs isolated from the OS, hypervisor, even physical RAM probing (memory is encrypted)
- **ARM TrustZone** — secure/normal world split; common in mobile and embedded (fingerprint, DRM, key handling)
- **Intel SGX** — application enclaves on the CPU (history of side-channel CVEs; partly deprecated on client)
- **AMD SEV-SNP / Intel TDX** — encrypt and attest whole VMs (the basis of "confidential computing" in the cloud)
- Apple **Secure Enclave**, Google **Titan M / Tensor** — dedicated coprocessors playing the same role
- Strength: run *arbitrary* trusted code with attestation. Weakness: bigger TCB than a fixed-function SE, and a steady stream of side-channel research

---

## Comparing The Options

| | `TPM` | `HSM` | TEE / Enclave | Discrete SE |
|---|---|---|---|---|
| Form | chip on board | appliance / card | region of main CPU | small dedicated chip |
| Throughput | low | very high | medium–high | low |
| Runs your code | no (fixed ops) | mostly no | **yes** | no |
| Typical use | device identity, boot | CA keys, payments | confidential compute | IoT device keys |
| Cost | cents | thousands+ | "free" (in the CPU) | cents |

Pick by question: protecting *a key on a device* → `TPM`/SE. *A fleet of keys at scale* → `HSM`. *Running sensitive code* → TEE.

---

## Integrating Secure Elements Into Applications

- Code to a standard interface — **`PKCS#11`** for `HSM`s/`TPM`s, vendor SDKs for SEs/TEEs — not directly to the silicon
- Your app holds **handles**, never key bytes: "sign with object 0x04", "unwrap with the SRK"
- Plan for **provisioning** — getting the right keys/certs onto the device at manufacture, securely
- Plan for **failure** — the device dies, the chip dies, the slot fills up; a non-extractable key cannot be restored, so design recovery (re-provisioning, backup keys, key hierarchies) up front
- Performance: offload the *key* operations (sign, key-agree, unwrap); do bulk symmetric crypto in software with the derived key
- Cost / complexity is real — use a secure element where the threat justifies it, not reflexively

---

## Takeaways

- A secure element keeps secrets that are *born inside and never leave* — even under physical attack
- `TPM`: cheap, everywhere, low-throughput — device identity, measured boot, sealing
- `HSM`: the appliance — CA keys, payments, code-signing, KMS backends; `PKCS#11` interface
- TEE/enclave: run *your* trusted code on the main CPU with attestation — bigger TCB, side-channel caveats
- Integrate via handles and standard APIs; design provisioning and recovery before you ship
