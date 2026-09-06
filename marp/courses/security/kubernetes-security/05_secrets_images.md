---
tags:
  - security:kubernetes
  - concepts:secrets
  - concepts:images
level: intermediate
category: security
audience:
  - audiences:devops

---

# Secrets and Image Security

---

## What This Chapter Covers

- Kubernetes Secrets: what they are and aren't
- External secret managers (Vault, AWS Secrets Manager)
- Sealed Secrets and SOPS
- Image scanning in CI/CD
- Image signing and provenance

---

## Kubernetes Secrets Basics

- `kind: Secret` — base64-encoded values
- Mounted as files or env vars
- Stored in etcd
- Default: not encrypted at rest
- "Secret" in name only by default

---

## The Encryption Gap

- Secrets are base64, not encrypted
- Anyone with etcd access reads them
- Anyone with API access via RBAC reads them
- Encryption at rest is opt-in; configure it
- A baseline expectation in 2026

---

## Encryption at Rest

```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources: ["secrets"]
    providers:
      - aescbc:
          keys:
            - name: key1
              secret: <base64-key>
      - identity: {}
```

- Configure on the API server
- KMS provider for HSM-backed keys

---

## KMS-Backed Encryption

- Uses cloud KMS (AWS KMS, GCP KMS, Azure Key Vault)
- Master key stays in HSM; never on disk
- Each Secret encrypted with a Data Encryption Key
- DEK encrypted by KMS Master Key
- Strongest at-rest protection

---

## RBAC for Secrets

- Restrict who can read Secrets
- `get`/`list` on secrets is sensitive
- Common mistake: developers granted broad access
- Least privilege per namespace
- Audit annually

---

## External Secret Stores

- HashiCorp Vault
- AWS Secrets Manager / Parameter Store
- Azure Key Vault
- GCP Secret Manager
- Single source of truth outside the cluster

---

## Storage Choices

![secret_storage_options](svg/courses/security/kubernetes-security/05_secrets_images/secret_storage_options.svg)

---

## External Secrets Operator

- Sync from external store to Kubernetes Secrets
- Or: inject directly without Secret resource (Vault Agent)
- Operator maps external paths to in-cluster Secrets
- Rotation handled centrally
- Cluster never owns the master copy

---

## ExternalSecret Example

```yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: db-creds
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
  target:
    name: db-creds-secret
  data:
    - secretKey: password
      remoteRef:
        key: prod/db
        property: password
```

---

## Sealed Secrets

- Encrypt Secrets to commit them to git
- Bitnami Sealed Secrets controller
- Public key per cluster; only that cluster can decrypt
- Workflow: kubeseal CLI to encrypt, git commit, apply
- GitOps-friendly

---

## SOPS

- Mozilla SOPS — encrypts YAML/JSON files
- Integrates with KMS, age, PGP
- Git-friendly; line-by-line encrypted
- Used by Flux and Helm for secrets in repos
- Strong alternative to Sealed Secrets

---

## Secret Sources Visualized

![secrets_flow](svg/courses/security/kubernetes-security/05_secrets_images/secrets_flow.svg)

---

## Image Scanning

- Scan images for known vulnerabilities (CVEs)
- Tools: Trivy, Grype, Snyk, Clair, Anchore
- Run in CI; block on critical findings
- Run in registry; alert on new CVEs
- Keep vulnerability DB current

---

## Supply-Chain Stages

![image_supply_chain](svg/courses/security/kubernetes-security/05_secrets_images/image_supply_chain.svg)

---

## Trivy in CI

```bash
trivy image myapp:1.0.0 \
  --severity CRITICAL,HIGH \
  --exit-code 1
```

- Fails the build on CRITICAL/HIGH
- Fast, comprehensive, free
- Defacto standard in many pipelines

---

## Base Image Hygiene

- Distroless or Alpine for minimal attack surface
- Avoid full Linux distros in containers
- Pin to specific tags or digests, not :latest
- Update base images regularly
- Multi-stage builds drop build tools

---

## Image Pull Policy

- IfNotPresent — use cached image (default)
- Always — pull every time (use with floating tags)
- Pin to digests for reproducibility
- Pull from private registries with imagePullSecrets
- Verify signature if signing is configured

---

## Image Signing

- Sigstore / Cosign — modern, free
- Notary v2 — older, OCI standard
- Sign at build, verify at admission
- Provenance: SLSA framework
- Increasingly required for supply-chain assurance

---

## Cosign Workflow

```bash
# Sign at build time
cosign sign --key cosign.key registry/app:1.0.0

# Verify before deploy
cosign verify --key cosign.pub registry/app:1.0.0
```

- Keyless signing also supported (OIDC-based)
- Fits naturally into CI/CD

---

## Verification at Admission

- Kyverno or Cosign Gatekeeper policies
- Reject pods running unsigned images
- Allow only signed images from approved registries
- Block image tampering between push and pull
- Production-ready in 2026

---

## Image Policy Example (Kyverno)

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: verify-images
spec:
  validationFailureAction: Enforce
  rules:
    - name: check-signature
      match:
        any:
          - resources:
              kinds: [Pod]
      verifyImages:
        - imageReferences:
            - "registry.example.com/*"
          attestors:
            - entries:
                - keys:
                    publicKeys: |-
                      -----BEGIN PUBLIC KEY-----
                      ...
                      -----END PUBLIC KEY-----
```

---

## Restricting Registries

- Allow only your private registry
- Block Docker Hub except for trusted images
- Catch typo-squatting (myapp vs myapp1)
- Enforce via Kyverno or Gatekeeper
- Critical for supply-chain integrity

---

## SBOM Generation

- Software Bill of Materials
- Lists every dependency in the image
- Tools: syft, Anchore, Trivy
- Required by some compliance frameworks
- Useful for vulnerability tracking

---

## Continuous Scanning

- Images scanned at build (CI)
- Re-scanned on a schedule (registry-side)
- New CVEs in old images surface daily
- Alert on critical findings in production
- Drive remediation — patch and redeploy

---

## Patch Cadence

- Security CVEs: patch within days
- High severity: within weeks
- Document expected SLAs
- Track meantime-to-patch as a metric
- Automation reduces toil

---

## Common Pitfalls

- Encryption at rest left disabled
- Long-lived static credentials in Secrets
- Images pulled by tag (mutable) without signing
- No SBOM, no idea what's in your images
- Image scanning warns but never blocks

---

## Best Practices

- Encrypt Secrets at rest with KMS
- External Secrets Operator for centralized stores
- Sealed Secrets or SOPS for GitOps
- Trivy + Cosign in every pipeline
- Verify image signatures at admission

---

## Summary

- Default Secrets are base64, not encrypted — fix this first
- External secret managers centralize and rotate
- Image scanning blocks known CVEs in CI
- Signing provides supply-chain assurance
- Continuous scanning catches new CVEs in old images
