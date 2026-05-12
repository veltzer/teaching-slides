---
tags:
  - security:secure-coding
  - security:supply-chain
  - practices:devops
level: intermediate
category: security
audience:
  - audiences:developers
  - audiences:devops
  - audiences:security-professionals
---
# Supply Chain Security

---

## What This Chapter Covers

- How software supply chain attacks actually work
- Dependency management and verification
- Software Bill of Materials (`SBOM`)
- Package integrity and signing
- Vendor and third-party risk assessment
- Secure configuration and change management
- Separation of duties

---

## The Supply Chain Is Now The Attack Surface

- Your code is a small fraction of what ships
- The rest: direct dependencies, transitive dependencies, build tools, base images, the `CI` runner itself
- An attacker does not need to breach you — they breach something you trust
- One compromised package can reach thousands of downstream projects

> You inherit the security posture of everything you depend on.

---

## How Supply Chain Attacks Happen

- **Typosquatting** — `requets` instead of `requests`; you install the wrong thing
- **Dependency confusion** — internal package name resolved from a public registry
- **Account takeover** — maintainer's credentials stolen, malicious version published
- **Malicious maintainer / handoff** — project sold or transferred to a bad actor
- **Build system compromise** — the artifact is poisoned after the source is clean
- **Tampered binaries** — what you download is not what was built

---

## Supply Chain Attack Surface

![attack surface](svg/courses/security/secure-coding/01_supply_chain/attack_surface.svg)

---

## Dependency Management And Verification

- **Pin versions** — lockfiles (`requirements.txt` with hashes, `package-lock.json`, `Cargo.lock`)
- **Verify hashes** — `pip install --require-hashes` rejects anything that does not match
- **Vendor what matters** — for C/`C++`, vendoring or pinned submodules beat "whatever the distro has"
- **Audit transitively** — `pip-audit`, `npm audit`, `cargo audit`, OSV scanners
- **Minimize the tree** — every dependency is a trust decision; fewer is safer

---

## Software Bill Of Materials (SBOM)

- A machine-readable inventory of every component in your software
- Formats: **SPDX**, **CycloneDX**
- Generated at build time, shipped alongside the artifact
- Answers "am I affected by CVE-XXXX?" in seconds, not days — recall Log4Shell
- Increasingly a contractual / regulatory requirement (US Executive Order 14028)
- Tools: `syft`, `cyclonedx-py`, native support in many build systems

---

## Package Integrity And Signing

- **Hashes** prove the bytes did not change; **signatures** prove who produced them
- Sign releases: `GPG`, `minisign`, or **Sigstore** / `cosign` (keyless, transparency-log backed)
- Verify on download — an unverified signature is just decoration
- **Provenance** (SLSA framework): an attestation of *how* and *where* the artifact was built
- For container images: sign with `cosign`, enforce verification at deploy time

---

## Vendor And Third-Party Risk

- Treat third-party code and services as part of *your* attack surface
- Questions to ask a vendor: Do they sign releases? Publish `SBOM`s? Have a disclosure policy? A track record?
- Check project health: maintenance activity, bus factor, response time on security issues
- Have an exit plan — what happens if the project dies or goes hostile?
- Contractual controls: security requirements, audit rights, breach notification

---

## Secure Configuration And Change Management

- Configuration is code — version it, review it, test it
- No secrets in config files in the repo (see the `CI/CD` chapter)
- Every change goes through review; no direct pushes to production branches
- Reproducible builds: the same source must produce the same artifact
- Track *what* changed, *who* changed it, and *why* — the audit trail is a control

---

## Separation Of Duties

- The person who writes code should not be the person who deploys it to production
- The person who approves a change should not be the person who made it
- Why: a single compromised account or insider cannot push malicious code to prod alone
- Enforce with branch protection, required reviewers, and pipeline gates
- This is friction on purpose — it is the cost of not trusting any single point

---

## Takeaways

- The supply chain is the attack surface — you inherit your dependencies' security
- Pin and verify everything; minimize the dependency tree
- Generate an `SBOM` and sign your releases — and *verify* on the way in
- Treat configuration as code and route every change through review
- Separation of duties: no single actor pushes to production unchecked
