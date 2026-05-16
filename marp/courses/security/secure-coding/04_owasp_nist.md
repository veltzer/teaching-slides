---
tags:
  - security:secure-coding
  - security:owasp
  - security:compliance
  - languages:c
  - languages:c++
  - languages:python
level: intermediate
category: security
audience:
  - audiences:developers
  - audiences:devops
  - audiences:security-professionals
---
# OWASP and NIST

---

## What This Chapter Covers

- `OWASP` `Top` 10 overview
- Secure coding guidelines per language
- `NIST` Cybersecurity Framework
- `NIST` Secure Software Development Framework (`SSDF`)
- Applying standards to real-world codebases

---

## Why Standards?

- They turn "be secure" into a concrete, reviewable checklist
- They are built from real incidents — the `OWASP` `Top` 10 is what actually goes wrong
- They give you a shared vocabulary with auditors, customers, and your own team
- They are increasingly required: contracts, procurement, regulation, executive orders
- Use them as a baseline, not a ceiling — passing the checklist is the start, not the finish

---

## OWASP Top 10 (2021)

- **A01 Broken Access Control** — users doing things they should not
- **A02 Cryptographic Failures** — weak/missing crypto, secrets in the clear
- **A03 Injection** — `SQL`, OS command, `LDAP`; untrusted data in a command
- **A04 Insecure Design** — the flaw is in the design, not the code
- **A05 Security Misconfiguration** — defaults, debug endpoints, verbose errors
- **A06 Vulnerable and Outdated Components** — the supply chain again
- **A07 Identification and Authentication Failures** — weak login, session handling
- **A08 Software and Data Integrity Failures** — unverified updates, insecure deserialization
- **A09 Security Logging and Monitoring Failures** — you cannot see the attack
- **A10 Server-Side Request Forgery (SSRF)** — the server fetches an attacker's URL

---

## OWASP Top 10 At A Glance

![owasp top 10](svg/courses/security/secure-coding/04_owasp_nist/owasp_top10.svg)

---

## The Recurring Themes

- **Trust boundaries** — every place untrusted data enters is a place to validate
- **Injection is one bug** — data interpreted as code: `SQL`, shell, `HTML`, `LDAP`, deserialization
- **Least privilege** — code, services, and users get the minimum they need
- **Fail closed** — an error condition denies access, it does not grant it
- **Defense in depth** — no single control is your only control
- **Don't trust the client** — validation on the client is UX; validation on the server is security

---

## Secure Coding Guidelines: C and C++

- **Memory safety is the whole game** — buffer overflows, use-after-free, double-free
- Avoid `strcpy`, `strcat`, `sprintf`, `gets` — use bounded variants and check lengths
- Integer overflow before allocation → tiny buffer, huge write; check the arithmetic
- Initialize everything; never use a pointer after `free` (and null it)
- Compiler/tooling: `-Wall -Wextra`, `-fstack-protector-strong`, ASan/UBSan, fuzzing
- Reference: **CERT C/C++ Secure Coding Standard**, the C++ Core Guidelines

---

## Secure Coding Guidelines: Python

- Never build `SQL` by string formatting — parameterized queries only
- Never pass user input to `os.system`, `subprocess(shell=True)`, `eval`, or `exec`
- Never `pickle.loads` (or `yaml.load`, or unverified `json` into objects) untrusted data
- Validate and normalize file paths — block `../` traversal before opening
- Pin dependencies, scan with `pip-audit`; lint with `bandit`
- Watch the framework defaults: `DEBUG=False` in prod, CSRF on, secure cookie flags

---

## Defense In Depth

![defense in depth](svg/courses/security/secure-coding/04_owasp_nist/defense_in_depth.svg)

---

## NIST Cybersecurity Framework (CSF)

- An organization-level framework for managing cybersecurity risk — broader than code
- Six functions: **Govern, Identify, Protect, Detect, Respond, Recover**
- Not a checklist of controls — a structure for deciding *which* controls and *how much*
- Tiers (1–4) describe how mature and integrated your risk management is
- Profiles map the framework to your specific business and threat context
- Where it touches you: "Protect" and "Detect" pull in secure development practices

---

## NIST Secure Software Development Framework (SSDF)

- `NIST` SP 800-218 — secure-development practices, organized into four groups:
- **PO — Prepare the Organization** — define requirements, roles, toolchains
- **PS — Protect the Software** — protect source and artifacts from tampering (signing, access control)
- **PW — Produce Well-Secured Software** — threat modeling, secure design, code review, testing
- **RV — Respond to Vulnerabilities** — disclosure process, triage, remediation, root-cause
- This is the framework US federal software procurement increasingly requires attestation against
- Note: `NIST` SP 800-218A extends `SSDF` to generative `AI` (covered in the `AI` chapter)

---

## Applying Standards To Real Codebases

- Don't try to "be compliant" all at once — pick the highest-risk gaps first
- **Threat model** the system → the model tells you which `Top` 10 items actually apply
- Turn the standard into a **PR review checklist** — make it part of the normal flow
- Automate what you can: `SAST`, dependency scans, secret scanning in `CI` (next chapter)
- Track exceptions explicitly — a documented, time-boxed exception beats silent non-compliance
- Map your controls to the framework once, maintain the map, reuse it for every audit

---

## Takeaways

- The `OWASP` `Top` 10 is a list of what actually goes wrong — know it cold
- Most of it reduces to: validate at trust boundaries, least privilege, fail closed
- C/`C++`: memory safety; `Python`: no injection, no unsafe deserialization
- `NIST` CSF manages risk at the org level; `NIST` `SSDF` (SP 800-218) covers secure development
- Adopt standards incrementally, threat-model-first, and bake the checklist into code review
