---
tags:
  - security:secure-coding
  - practices:ci-cd
  - practices:devops
level: intermediate
category: security
audience:
  - audiences:devops
  - audiences:developers
  - audiences:security-professionals
---

# CI/CD Security

---

## What This Chapter Covers

- Securing the build pipeline
- Secrets management in `CI/CD`
- Static and dynamic analysis integration
- Container image scanning and signing
- Artifact integrity and provenance

---

## The Pipeline Is Production

- Your `CI/CD` system has: source access, deploy credentials, signing keys, cloud admin
- Compromise the pipeline and you do not need to compromise anything else
- It is also a juicy target *because* it is often the least-hardened system you own
- "It is just a build server" is exactly the attitude that gets exploited
- Real incidents: SolarWinds, Codecov, the `tj-actions` token leak — all pipeline compromises

---

## Securing The Build Pipeline

- **Pin everything** — actions/jobs by commit SHA, not a mutable tag; base images by digest
- **Least privilege** — each job gets a short-lived, narrowly-scoped token; no standing admin creds
- **Isolated runners** — ephemeral, single-use; never run untrusted PR code on a privileged runner
- **Protect the config** — pipeline definitions live in the repo and go through review like any code
- **Hermetic builds** — no network during build where possible; deps come from a controlled mirror
- **Audit logging** — every build, every deploy, who triggered it, what it produced

---

## Secrets Management In CI/CD

- **Never in the repo** — not in code, not in config, not in history; if it leaked once, rotate it
- Use the platform's secret store, or pull from a vault (`HashiCorp Vault`, cloud KMS) at runtime
- Prefer **short-lived credentials** — OIDC federation to the cloud beats a long-lived access key
- Mask secrets in logs; assume `set -x` and crash dumps will try to print them
- Scope per-job and per-environment — a PR pipeline must not see production secrets
- Rotate on a schedule; have a tested "rotate everything now" runbook
- Run a **secret scanner** (`gitleaks`, `trufflehog`) on every commit to catch leaks early

---

## CI/CD Threat Surface

![cicd surface](svg/courses/security/secure-coding/05_cicd_security/cicd_surface.svg)

---

## Controls Along The Pipeline

![pipeline controls](svg/courses/security/secure-coding/05_cicd_security/pipeline_controls.svg)

---

## Static And Dynamic Analysis In The Pipeline

- **SAST** — analyze source for bug patterns: `Semgrep`, `CodeQL`, `bandit`, clang static analyzer
- **DAST** — test the running app for exploitable behavior: ZAP, Burp, fuzzers
- **SCA** — dependency vulnerability scanning: `pip-audit`, `npm audit`, Trivy, Grype
- **IaC scanning** — Terraform/Kubernetes/Dockerfile misconfig: `checkov`, `tfsec`, `kube-linter`
- Run them in `CI`; fail the build on new high-severity findings; track and triage the rest
- Watch the false-positive rate — a noisy gate gets ignored, which is worse than no gate

---

## Container Image Scanning And Signing

- **Scan** images for known CVEs in the OS packages and app dependencies — `Trivy`, `Grype`, Clair
- Rebuild on a cadence so base-image fixes actually land — a scan result rots fast
- Use minimal bases (distroless, Alpine, scratch) — fewer packages, fewer CVEs, smaller surface
- **Sign** images with `cosign` (keyless via Sigstore, or with a KMS key)
- **Enforce** verification at deploy — admission controllers (Kyverno, Gatekeeper, Connaisseur) reject images that are unsigned or not scanned
- Pin by digest in deployment manifests, not by `:latest`

---

## Artifact Integrity And Provenance

- **Integrity** — the artifact you deploy is byte-for-byte what the pipeline built (hashes, signatures)
- **Provenance** — a signed statement of *how* it was built: which source commit, which builder, which steps
- **SLSA** (Supply-chain Levels for Software Artifacts) — a maturity ladder for build integrity
    - L1: provenance exists → L2: signed by the build service → L3: hardened, isolated builds
- Store artifacts in a registry with immutability and access control; never overwrite a published version
- Generate the `SBOM` here too, and attach it as an attestation alongside the artifact
- Verify provenance at deploy — an unverified attestation proves nothing

---

## A Hardened Pipeline, End To End

1. 1. 1. Commit pushed → secret scan, `SAST`, lint run on an isolated runner
1. 1. 1. PR requires review from someone other than the author (separation of duties)
1. 1. 1. On merge: hermetic build, `SBOM` generated, artifact + provenance signed via OIDC
1. 1. 1. Image scanned for CVEs; build fails on new criticals
1. 1. 1. Artifact pushed to an immutable registry
1. 1. 1. Deploy: admission controller verifies signature, provenance, and scan status — or rejects

---

## Takeaways

- The pipeline holds your keys and your prod access — harden it like production
- Secrets never live in the repo; prefer short-lived OIDC credentials; scan for leaks
- Pin actions and images by digest; run on ephemeral, isolated runners
- Put `SAST`/`DAST`/`SCA`/IaC scanning in `CI` — fail on new criticals, triage the rest
- Sign artifacts and images, generate provenance (`SLSA`), and verify at deploy time
