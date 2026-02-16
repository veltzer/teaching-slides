# Artifact Management and Promotion
## Architectural Decisions in DevOps
---
## Table of Contents
1. Artifact Repository Strategies
1. Promotion Between Stages
1. Versioning Strategies
1. Immutable Artifacts and Traceability
1. Container Image Management
1. Base Image Strategies and Supply Chain Security
1. Image Scanning and Policy Enforcement
1. Slim Images vs Full Images
---
## What Is an Artifact?
- An artifact is any output produced by a build process
- Examples include:
    - Compiled binaries (`.jar`, `.dll`, `.exe`)
    - Container images (`Docker`, `OCI`)
    - Packages (`npm`, `PyPI`, `NuGet`)
    - Helm charts and configuration bundles
    - Documentation and test reports
- Artifacts must be stored, versioned, and promoted reliably
---
## Why Artifact Management Matters
- Reproducibility: rebuild or redeploy any release
- Traceability: link every deployment back to source code
- Security: scan and validate before production
- Speed: avoid rebuilding the same artifact multiple times
- Compliance: audit trail for regulated industries
---
## Artifact Repository Landscape
| Repository | Primary Use | Formats |
|------------|-------------|---------|
| `JFrog Artifactory` | Universal | All |
| `Sonatype Nexus` | Java-centric | Maven, npm, Docker |
| `AWS ECR` | Container images | OCI, Docker |
| `GitHub Packages` | Source-integrated | npm, Maven, Docker |
| `Google Artifact Registry` | GCP-native | Docker, Maven, npm |
| `Azure Artifacts` | Azure-native | NuGet, npm, Maven |
---
## Single Artifact Repository
- One centralized repository for all artifact types
- Advantages:
    - Unified access control and policies
    - Single source of truth for all teams
    - Simplified backup and disaster recovery
    - Consistent metadata and search
- Disadvantages:
    - Single point of failure
    - Can become a performance bottleneck
    - Harder to scale across regions
---
## Multiple Artifact Repositories
- Separate repositories per team, format, or environment
- Advantages:
    - Isolation and blast radius reduction
    - Independent scaling per workload
    - Team autonomy over configuration
- Disadvantages:
    - Increased operational overhead
    - Cross-repository dependency management
    - Policy consistency challenges
---
## Single vs Multiple: Decision Matrix
| Factor | Single Repo | Multiple Repos |
|--------|-------------|----------------|
| Small team (<20 devs) | Preferred | Overkill |
| Regulated industry | Simpler audit | Harder audit |
| Multi-region deploy | Needs mirrors | Natural fit |
| Polyglot ecosystem | Universal type | Format-specific |
| Cost sensitivity | Lower | Higher |
---
## Artifact Repository Architecture
<svg viewBox="0 0 700 320" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="20" width="130" height="50" rx="8" fill="#4A90D9" stroke="#333" stroke-width="2"/>
  <text x="75" y="50" text-anchor="middle" fill="white" font-size="13" font-weight="bold">CI Build</text>
  <rect x="10" y="90" width="130" height="50" rx="8" fill="#4A90D9" stroke="#333" stroke-width="2"/>
  <text x="75" y="120" text-anchor="middle" fill="white" font-size="13" font-weight="bold">Developer</text>
  <rect x="230" y="55" width="160" height="60" rx="8" fill="#E8A838" stroke="#333" stroke-width="2"/>
  <text x="310" y="80" text-anchor="middle" fill="white" font-size="13" font-weight="bold">Artifact</text>
  <text x="310" y="100" text-anchor="middle" fill="white" font-size="13" font-weight="bold">Repository</text>
  <rect x="500" y="10" width="160" height="40" rx="8" fill="#50B86C" stroke="#333" stroke-width="2"/>
  <text x="580" y="35" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Dev Deploy</text>
  <rect x="500" y="65" width="160" height="40" rx="8" fill="#50B86C" stroke="#333" stroke-width="2"/>
  <text x="580" y="90" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Staging Deploy</text>
  <rect x="500" y="120" width="160" height="40" rx="8" fill="#50B86C" stroke="#333" stroke-width="2"/>
  <text x="580" y="145" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Prod Deploy</text>
  <line x1="140" y1="45" x2="230" y2="75" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <line x1="140" y1="115" x2="230" y2="95" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <line x1="390" y1="70" x2="500" y2="30" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <line x1="390" y1="85" x2="500" y2="85" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <line x1="390" y1="100" x2="500" y2="140" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <defs>
    <marker id="arrow1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#333"/>
    </marker>
  </defs>
  <text x="350" y="210" text-anchor="middle" fill="#555" font-size="12" font-style="italic">Central repository serves all environments</text>
</svg>

---
## Promotion Between Stages
- Promotion = moving an artifact from one stage to the next
- Typical pipeline: `dev` -> `staging` -> `production`
- Key principle: **never rebuild** between stages
- The same binary tested in staging is deployed to production
- Promotion is a metadata operation, not a rebuild
---
## Promotion Pipeline: Overview
<svg viewBox="0 0 700 250" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="80" width="120" height="60" rx="10" fill="#4A90D9" stroke="#333" stroke-width="2"/>
  <text x="80" y="105" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Build</text>
  <text x="80" y="125" text-anchor="middle" fill="white" font-size="11">Unit Tests</text>
  <rect x="180" y="80" width="120" height="60" rx="10" fill="#E8A838" stroke="#333" stroke-width="2"/>
  <text x="240" y="105" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Dev Repo</text>
  <text x="240" y="125" text-anchor="middle" fill="white" font-size="11">Snapshot</text>
  <rect x="340" y="80" width="120" height="60" rx="10" fill="#D96B4A" stroke="#333" stroke-width="2"/>
  <text x="400" y="105" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Staging Repo</text>
  <text x="400" y="125" text-anchor="middle" fill="white" font-size="11">Integration</text>
  <rect x="500" y="80" width="120" height="60" rx="10" fill="#50B86C" stroke="#333" stroke-width="2"/>
  <text x="560" y="105" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Prod Repo</text>
  <text x="560" y="125" text-anchor="middle" fill="white" font-size="11">Release</text>
  <line x1="140" y1="110" x2="180" y2="110" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <line x1="300" y1="110" x2="340" y2="110" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <line x1="460" y1="110" x2="500" y2="110" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <text x="230" y="170" text-anchor="middle" fill="#555" font-size="10">promote</text>
  <text x="390" y="170" text-anchor="middle" fill="#555" font-size="10">promote</text>
  <text x="550" y="170" text-anchor="middle" fill="#555" font-size="10">promote</text>
  <text x="160" y="55" text-anchor="middle" fill="#333" font-size="10">auto</text>
  <text x="320" y="55" text-anchor="middle" fill="#333" font-size="10">gate: tests pass</text>
  <text x="480" y="55" text-anchor="middle" fill="#333" font-size="10">gate: approval</text>
  <defs>
    <marker id="arrow2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---
## Promotion Strategies
- **Copy promotion**: artifact is copied to a new repository
    - Clear separation between stages
    - Higher storage cost
- **Metadata promotion**: artifact stays in place, label changes
    - Lower storage cost
    - Requires robust tagging system
- **Virtual repository promotion**: logical views over one physical repo
    - Best of both worlds
    - Supported by `Artifactory` and `Nexus`
---
## Promotion Gates
- Each promotion step should require passing quality gates
- Common gates:
    - Unit test pass rate >= threshold
    - Integration test success
    - Security scan (no critical CVEs)
    - Code coverage minimum
    - Performance regression check
    - Manual approval (for production)
- Gates should be automated where possible
---
## Promotion Example in `JFrog` CLI
```bash
# Promote a build from dev to staging
jfrog rt build-promote \
  "my-app" \
  "42" \
  "staging-local" \
  --status "Staged" \
  --comment "Passed integration tests" \
  --copy true
```
- Build name: `my-app`, build number: `42`
- Target repository: `staging-local`
- `--copy true` keeps the original in dev
---
## Semantic Versioning (SemVer)
- Format: `MAJOR.MINOR.PATCH`
    - `MAJOR`: breaking changes
    - `MINOR`: new features, backward compatible
    - `PATCH`: bug fixes, backward compatible
- Examples:
    - `1.0.0` -> `2.0.0` (breaking API change)
    - `1.0.0` -> `1.1.0` (new endpoint added)
    - `1.0.0` -> `1.0.1` (bug fix)
- Pre-release: `1.0.0-alpha.1`, `1.0.0-rc.2`
---
## SemVer: Version Ordering
<svg viewBox="0 0 650 200" xmlns="http://www.w3.org/2000/svg">
  <line x1="50" y1="100" x2="620" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <circle cx="100" cy="100" r="8" fill="#4A90D9"/>
  <text x="100" y="85" text-anchor="middle" fill="#333" font-size="11" font-weight="bold">1.0.0-alpha</text>
  <circle cx="200" cy="100" r="8" fill="#4A90D9"/>
  <text x="200" y="85" text-anchor="middle" fill="#333" font-size="11" font-weight="bold">1.0.0-rc.1</text>
  <circle cx="300" cy="100" r="8" fill="#50B86C"/>
  <text x="300" y="85" text-anchor="middle" fill="#333" font-size="11" font-weight="bold">1.0.0</text>
  <circle cx="400" cy="100" r="8" fill="#50B86C"/>
  <text x="400" y="85" text-anchor="middle" fill="#333" font-size="11" font-weight="bold">1.0.1</text>
  <circle cx="500" cy="100" r="8" fill="#E8A838"/>
  <text x="500" y="85" text-anchor="middle" fill="#333" font-size="11" font-weight="bold">1.1.0</text>
  <circle cx="600" cy="100" r="8" fill="#D96B4A"/>
  <text x="600" y="85" text-anchor="middle" fill="#333" font-size="11" font-weight="bold">2.0.0</text>
  <text x="100" y="130" text-anchor="middle" fill="#555" font-size="9">pre-release</text>
  <text x="300" y="130" text-anchor="middle" fill="#555" font-size="9">stable</text>
  <text x="400" y="130" text-anchor="middle" fill="#555" font-size="9">patch</text>
  <text x="500" y="130" text-anchor="middle" fill="#555" font-size="9">minor</text>
  <text x="600" y="130" text-anchor="middle" fill="#555" font-size="9">major</text>
  <defs>
    <marker id="arrow3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---
## Commit-Based Versioning
- Use the `git` commit hash as the version identifier
- Format: `<branch>-<short-sha>-<timestamp>`
- Example: `main-a3f8b2c-20260215`
- Advantages:
    - No human decisions about version numbers
    - Direct traceability to source code
    - Works well with continuous deployment
- Disadvantages:
    - No semantic meaning
    - Hard to communicate to customers
    - Ordering is not immediately obvious
---
## SemVer vs Commit-Based: When to Use
| Scenario | Recommended Strategy |
|----------|---------------------|
| Public library / API | `SemVer` |
| Internal microservice | Commit-based |
| Mobile app (app store) | `SemVer` |
| Infrastructure as Code | Commit-based |
| Shared SDK | `SemVer` |
| Continuous deployment service | Commit-based |
---
## Hybrid Versioning
- Combine `SemVer` with commit metadata
- Format: `MAJOR.MINOR.PATCH+build.sha`
- Example: `2.3.1+build.a3f8b2c`
- Benefits:
    - Human-readable version for releases
    - Machine-traceable back to exact commit
    - Build metadata does not affect precedence
- Tools: `GitVersion`, `semantic-release`, `conventional-commits`
---
## Immutable Artifacts
- Once published, an artifact version must never change
- Overwriting a version is a critical anti-pattern
- Rules:
    - Published versions are read-only
    - Deleting and re-uploading the same version is forbidden
    - Use new version numbers for any change
- Repository configuration: enable "prevent overwrite" policies
---
## Why Immutability Matters
- **Reproducibility**: re-deploy any past version exactly
- **Security**: tampering is detectable
- **Caching**: proxies and clients can cache safely
- **Auditing**: every version has a clear history
- **Debugging**: production always matches tested binary
- Breaking immutability = breaking trust in the pipeline
---
## Traceability: From Deploy to Source
<svg viewBox="0 0 700 220" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="80" width="110" height="50" rx="8" fill="#50B86C" stroke="#333" stroke-width="2"/>
  <text x="75" y="110" text-anchor="middle" fill="white" font-size="11" font-weight="bold">Production</text>
  <rect x="170" y="80" width="110" height="50" rx="8" fill="#E8A838" stroke="#333" stroke-width="2"/>
  <text x="225" y="110" text-anchor="middle" fill="white" font-size="11" font-weight="bold">Artifact v2.3.1</text>
  <rect x="320" y="80" width="110" height="50" rx="8" fill="#4A90D9" stroke="#333" stroke-width="2"/>
  <text x="375" y="110" text-anchor="middle" fill="white" font-size="11" font-weight="bold">Build #142</text>
  <rect x="470" y="80" width="110" height="50" rx="8" fill="#D96B4A" stroke="#333" stroke-width="2"/>
  <text x="525" y="110" text-anchor="middle" fill="white" font-size="11" font-weight="bold">Commit a3f8b2c</text>
  <line x1="130" y1="105" x2="170" y2="105" stroke="#333" stroke-width="2" marker-end="url(#arrow4)"/>
  <line x1="280" y1="105" x2="320" y2="105" stroke="#333" stroke-width="2" marker-end="url(#arrow4)"/>
  <line x1="430" y1="105" x2="470" y2="105" stroke="#333" stroke-width="2" marker-end="url(#arrow4)"/>
  <text x="150" y="75" text-anchor="middle" fill="#555" font-size="9">runs</text>
  <text x="300" y="75" text-anchor="middle" fill="#555" font-size="9">built by</text>
  <text x="450" y="75" text-anchor="middle" fill="#555" font-size="9">from</text>
  <text x="350" y="180" text-anchor="middle" fill="#555" font-size="11" font-style="italic">Full traceability chain from deploy to commit</text>
  <defs>
    <marker id="arrow4" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---
## Implementing Traceability
- Embed metadata in every artifact:
    - `git` commit SHA
    - Build number and timestamp
    - Builder identity (CI system, agent)
    - Source branch and repository URL
- Use build-info manifests (e.g., `JFrog Build Info`)
- Store Software Bill of Materials (`SBOM`)
---
## SBOM: Software Bill of Materials
- A machine-readable inventory of all components
- Standards: `SPDX`, `CycloneDX`
- Contents:
    - Direct and transitive dependencies
    - License information
    - Vulnerability references
- Required by US Executive Order 14028 for federal software
- Generate at build time, attach to the artifact
---
## Container Image Management
- Container images are the dominant artifact type in modern DevOps
- Key concerns:
    - Base image selection
    - Layer optimization
    - Security scanning
    - Registry management
    - Tag and digest strategies
---
## Container Image Layers
<svg viewBox="0 0 500 300" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="20" width="300" height="40" rx="5" fill="#D96B4A" stroke="#333" stroke-width="2"/>
  <text x="250" y="45" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Application Code (2 MB)</text>
  <rect x="100" y="70" width="300" height="40" rx="5" fill="#E8A838" stroke="#333" stroke-width="2"/>
  <text x="250" y="95" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Dependencies (45 MB)</text>
  <rect x="100" y="120" width="300" height="40" rx="5" fill="#4A90D9" stroke="#333" stroke-width="2"/>
  <text x="250" y="145" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Runtime (30 MB)</text>
  <rect x="100" y="170" width="300" height="40" rx="5" fill="#50B86C" stroke="#333" stroke-width="2"/>
  <text x="250" y="195" text-anchor="middle" fill="white" font-size="12" font-weight="bold">OS Base Layer (80 MB)</text>
  <text x="70" y="45" text-anchor="end" fill="#555" font-size="10">Layer 4</text>
  <text x="70" y="95" text-anchor="end" fill="#555" font-size="10">Layer 3</text>
  <text x="70" y="145" text-anchor="end" fill="#555" font-size="10">Layer 2</text>
  <text x="70" y="195" text-anchor="end" fill="#555" font-size="10">Layer 1</text>
  <text x="250" y="250" text-anchor="middle" fill="#555" font-size="11" font-style="italic">Each layer is cached and shared across images</text>
</svg>

---
## Base Image Strategies
- **Official images**: maintained by Docker or vendors
    - `node:20`, `python:3.12`, `openjdk:21`
- **Verified publisher images**: from trusted organizations
- **Custom base images**: built and maintained internally
    - Pre-approved packages and security hardening
    - Consistent across all teams
- Decision factors:
    - Trust level and update frequency
    - Organizational compliance requirements
---
## Base Image Tiering
<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg">
  <rect x="180" y="10" width="240" height="50" rx="8" fill="#D96B4A" stroke="#333" stroke-width="2"/>
  <text x="300" y="30" text-anchor="middle" fill="white" font-size="11" font-weight="bold">Tier 3: Application Images</text>
  <text x="300" y="48" text-anchor="middle" fill="white" font-size="10">myapp:2.3.1</text>
  <rect x="140" y="80" width="320" height="50" rx="8" fill="#E8A838" stroke="#333" stroke-width="2"/>
  <text x="300" y="100" text-anchor="middle" fill="white" font-size="11" font-weight="bold">Tier 2: Runtime Base Images</text>
  <text x="300" y="118" text-anchor="middle" fill="white" font-size="10">node-base:20, python-base:3.12</text>
  <rect x="100" y="150" width="400" height="50" rx="8" fill="#4A90D9" stroke="#333" stroke-width="2"/>
  <text x="300" y="170" text-anchor="middle" fill="white" font-size="11" font-weight="bold">Tier 1: OS Foundation Images</text>
  <text x="300" y="188" text-anchor="middle" fill="white" font-size="10">ubuntu-hardened:22.04, alpine-approved:3.19</text>
  <text x="300" y="240" text-anchor="middle" fill="#555" font-size="11" font-style="italic">Each tier inherits security policies from below</text>
</svg>

---
## Supply Chain Security for Images
- Software supply chain attacks target build dependencies
- Key protections:
    - Sign images with `cosign` or Docker Content Trust
    - Verify base image provenance with `SLSA` framework
    - Pin base images by `digest`, not `tag`
    - Use `Sigstore` for keyless signing
- Example: pin by digest
```dockerfile
FROM node@sha256:a3f8b2c4e5d6...
```
---
## Image Signing with `cosign`
```bash
# Sign an image after push
cosign sign \
  --key cosign.key \
  myregistry.io/myapp:2.3.1

# Verify before deploy
cosign verify \
  --key cosign.pub \
  myregistry.io/myapp:2.3.1
```
- Signatures are stored alongside the image in the registry
- Kubernetes admission controllers can enforce verification
---
## Image Scanning Overview
- Scanning detects known vulnerabilities (CVEs) in image layers
- When to scan:
    - At build time (fail the pipeline)
    - At push to registry (block storage)
    - At runtime (detect drift)
    - On schedule (new CVEs emerge daily)
- Popular scanners: `Trivy`, `Grype`, `Snyk`, `Clair`
---
## Scanning with `Trivy`
```bash
# Scan a local image
trivy image myapp:2.3.1

# Fail CI if critical or high CVEs found
trivy image \
  --severity CRITICAL,HIGH \
  --exit-code 1 \
  myapp:2.3.1

# Output as JSON for pipeline processing
trivy image \
  --format json \
  --output results.json \
  myapp:2.3.1
```
---
## Vulnerability Severity Levels
| Severity | Action | SLA Example |
|----------|--------|-------------|
| Critical | Block deployment | Fix within 24 hours |
| High | Block promotion to prod | Fix within 7 days |
| Medium | Allow with exception | Fix within 30 days |
| Low | Informational | Fix at next release |
| Negligible | Ignore | No action required |
---
## Policy Enforcement Architecture
<svg viewBox="0 0 700 280" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="100" width="120" height="50" rx="8" fill="#4A90D9" stroke="#333" stroke-width="2"/>
  <text x="80" y="130" text-anchor="middle" fill="white" font-size="11" font-weight="bold">Developer Push</text>
  <rect x="180" y="100" width="120" height="50" rx="8" fill="#E8A838" stroke="#333" stroke-width="2"/>
  <text x="240" y="120" text-anchor="middle" fill="white" font-size="11" font-weight="bold">Registry</text>
  <text x="240" y="138" text-anchor="middle" fill="white" font-size="10">Webhook</text>
  <rect x="340" y="100" width="120" height="50" rx="8" fill="#D96B4A" stroke="#333" stroke-width="2"/>
  <text x="400" y="120" text-anchor="middle" fill="white" font-size="11" font-weight="bold">Scanner</text>
  <text x="400" y="138" text-anchor="middle" fill="white" font-size="10">Trivy / Grype</text>
  <rect x="500" y="70" width="140" height="40" rx="8" fill="#50B86C" stroke="#333" stroke-width="2"/>
  <text x="570" y="95" text-anchor="middle" fill="white" font-size="11" font-weight="bold">Pass: Tag OK</text>
  <rect x="500" y="140" width="140" height="40" rx="8" fill="#C0392B" stroke="#333" stroke-width="2"/>
  <text x="570" y="165" text-anchor="middle" fill="white" font-size="11" font-weight="bold">Fail: Quarantine</text>
  <line x1="140" y1="125" x2="180" y2="125" stroke="#333" stroke-width="2" marker-end="url(#arrow5)"/>
  <line x1="300" y1="125" x2="340" y2="125" stroke="#333" stroke-width="2" marker-end="url(#arrow5)"/>
  <line x1="460" y1="115" x2="500" y2="90" stroke="#333" stroke-width="2" marker-end="url(#arrow5)"/>
  <line x1="460" y1="135" x2="500" y2="160" stroke="#333" stroke-width="2" marker-end="url(#arrow5)"/>
  <defs>
    <marker id="arrow5" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---
## Kubernetes Admission Control
- Enforce image policies at deploy time
- Tools: `OPA Gatekeeper`, `Kyverno`, `Sigstore Policy Controller`
- Common policies:
    - Only allow images from approved registries
    - Require image signatures
    - Block images with critical CVEs
    - Enforce non-root containers
```yaml
# Kyverno policy snippet
spec:
  rules:
  - name: check-image-registry
    match:
      resources:
        kinds: ["Pod"]
    validate:
      pattern:
        spec:
          containers:
          - image: "myregistry.io/*"
```
---
## Slim Images vs Full Images
| Aspect | Full Image | Slim Image |
|--------|-----------|------------|
| Size | 200-900 MB | 5-50 MB |
| Attack surface | Large | Minimal |
| Debugging tools | Included | Missing |
| Build complexity | Simple | Higher |
| Startup time | Slower | Faster |
| CVE count | Many | Few |
---
## Common Base Image Options
| Image | Size | Shell | Package Manager |
|-------|------|-------|-----------------|
| `ubuntu:22.04` | ~77 MB | `bash` | `apt` |
| `debian:bookworm-slim` | ~52 MB | `bash` | `apt` |
| `alpine:3.19` | ~7 MB | `ash` | `apk` |
| `distroless` | ~2-20 MB | None | None |
| `scratch` | 0 MB | None | None |
| `chainguard` | ~2-15 MB | None | `apk` (build) |
---
## Slim Image Comparison
<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="20" text-anchor="middle" fill="#333" font-size="13" font-weight="bold">Image Size Comparison (Node.js App)</text>
  <rect x="60" y="40" width="400" height="30" rx="4" fill="#D96B4A" stroke="#333" stroke-width="1"/>
  <text x="65" y="60" fill="white" font-size="11" font-weight="bold">node:20 (910 MB)</text>
  <rect x="60" y="80" width="200" height="30" rx="4" fill="#E8A838" stroke="#333" stroke-width="1"/>
  <text x="65" y="100" fill="white" font-size="11" font-weight="bold">node:20-slim (180 MB)</text>
  <rect x="60" y="120" width="80" height="30" rx="4" fill="#4A90D9" stroke="#333" stroke-width="1"/>
  <text x="65" y="140" fill="white" font-size="11" font-weight="bold">alpine (70 MB)</text>
  <rect x="60" y="160" width="30" height="30" rx="4" fill="#50B86C" stroke="#333" stroke-width="1"/>
  <text x="95" y="180" fill="#333" font-size="11" font-weight="bold">distroless (25 MB)</text>
  <text x="300" y="230" text-anchor="middle" fill="#555" font-size="11" font-style="italic">Smaller images = faster pulls, less attack surface</text>
</svg>

---
## Multi-Stage Builds
- Separate build environment from runtime environment
- Build stage has compilers and tools
- Runtime stage has only the application binary
```dockerfile
# Build stage
FROM golang:1.22 AS builder
WORKDIR /app
COPY . .
RUN go build -o myapp

# Runtime stage
FROM gcr.io/distroless/static
COPY --from=builder /app/myapp /
CMD ["/myapp"]
```
---
## Multi-Stage Build: Layer Diagram
<svg viewBox="0 0 650 250" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="30" width="250" height="180" rx="8" fill="none" stroke="#D96B4A" stroke-width="2" stroke-dasharray="5,5"/>
  <text x="145" y="22" text-anchor="middle" fill="#D96B4A" font-size="12" font-weight="bold">Build Stage (discarded)</text>
  <rect x="40" y="45" width="210" height="30" rx="4" fill="#D96B4A" stroke="#333" stroke-width="1"/>
  <text x="145" y="65" text-anchor="middle" fill="white" font-size="10">Go Compiler (300 MB)</text>
  <rect x="40" y="85" width="210" height="30" rx="4" fill="#E8A838" stroke="#333" stroke-width="1"/>
  <text x="145" y="105" text-anchor="middle" fill="white" font-size="10">Build Dependencies (150 MB)</text>
  <rect x="40" y="125" width="210" height="30" rx="4" fill="#4A90D9" stroke="#333" stroke-width="1"/>
  <text x="145" y="145" text-anchor="middle" fill="white" font-size="10">Source Code (5 MB)</text>
  <rect x="40" y="165" width="210" height="30" rx="4" fill="#50B86C" stroke="#333" stroke-width="1"/>
  <text x="145" y="185" text-anchor="middle" fill="white" font-size="10">Binary Output (10 MB)</text>
  <rect x="370" y="30" width="250" height="130" rx="8" fill="none" stroke="#50B86C" stroke-width="2"/>
  <text x="495" y="22" text-anchor="middle" fill="#50B86C" font-size="12" font-weight="bold">Runtime Stage (shipped)</text>
  <rect x="390" y="45" width="210" height="30" rx="4" fill="#4A90D9" stroke="#333" stroke-width="1"/>
  <text x="495" y="65" text-anchor="middle" fill="white" font-size="10">Distroless Base (2 MB)</text>
  <rect x="390" y="85" width="210" height="30" rx="4" fill="#50B86C" stroke="#333" stroke-width="1"/>
  <text x="495" y="105" text-anchor="middle" fill="white" font-size="10">Binary (10 MB)</text>
  <text x="495" y="145" text-anchor="middle" fill="#555" font-size="11" font-weight="bold">Total: 12 MB</text>
  <line x1="250" y1="180" x2="390" y2="100" stroke="#333" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrow6)"/>
  <text x="320" y="130" text-anchor="middle" fill="#333" font-size="10">COPY</text>
  <defs>
    <marker id="arrow6" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---
## Distroless Images
- Created by Google, contain only the application and runtime
- No shell, no package manager, no OS utilities
- Benefits:
    - Dramatically reduced CVE count
    - Impossible to `exec` into for attackers
    - Smaller image size
- Available for: `Java`, `Python`, `Node.js`, `Go`, `.NET`
```dockerfile
FROM gcr.io/distroless/java21-debian12
COPY target/myapp.jar /app.jar
CMD ["app.jar"]
```
---
## When NOT to Use Slim Images
- During development (need debugging tools)
- When troubleshooting production issues
- When the application requires OS-level packages
- Strategy: use slim in production, full in development
```yaml
# docker-compose.yml
services:
  app:
    image: ${APP_IMAGE:-myapp:dev-full}
    # Override per environment:
    # dev:  myapp:dev-full (with shell, curl, etc.)
    # prod: myapp:prod-distroless
```
---
## Tag Strategies for Container Images
- Avoid using `latest` in production
- Good tagging practices:
    - `myapp:2.3.1` (SemVer release)
    - `myapp:main-a3f8b2c` (branch + commit)
    - `myapp:sha-a3f8b2c4e5d6` (full digest reference)
- Always prefer digest references for deployments
```bash
# Pin by digest in Kubernetes
image: myregistry.io/myapp@sha256:a3f8...
```
---
## The Danger of Mutable Tags
- Tags like `latest`, `stable`, `v2` can be overwritten
- Problem: same tag may point to different images over time
- Real-world incident example:
    - `myapp:latest` updated at 14:00
    - Pod restart at 14:30 pulls new version
    - Untested code now running in production
- Solution: immutable tags or digest pinning
---
## Container Image Lifecycle
<svg viewBox="0 0 700 250" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="90" width="100" height="50" rx="8" fill="#4A90D9" stroke="#333" stroke-width="2"/>
  <text x="70" y="120" text-anchor="middle" fill="white" font-size="10" font-weight="bold">Build</text>
  <rect x="150" y="90" width="100" height="50" rx="8" fill="#E8A838" stroke="#333" stroke-width="2"/>
  <text x="200" y="120" text-anchor="middle" fill="white" font-size="10" font-weight="bold">Scan</text>
  <rect x="280" y="90" width="100" height="50" rx="8" fill="#D96B4A" stroke="#333" stroke-width="2"/>
  <text x="330" y="120" text-anchor="middle" fill="white" font-size="10" font-weight="bold">Sign</text>
  <rect x="410" y="90" width="100" height="50" rx="8" fill="#50B86C" stroke="#333" stroke-width="2"/>
  <text x="460" y="120" text-anchor="middle" fill="white" font-size="10" font-weight="bold">Promote</text>
  <rect x="540" y="90" width="100" height="50" rx="8" fill="#8E44AD" stroke="#333" stroke-width="2"/>
  <text x="590" y="120" text-anchor="middle" fill="white" font-size="10" font-weight="bold">Deploy</text>
  <line x1="120" y1="115" x2="150" y2="115" stroke="#333" stroke-width="2" marker-end="url(#arrow7)"/>
  <line x1="250" y1="115" x2="280" y2="115" stroke="#333" stroke-width="2" marker-end="url(#arrow7)"/>
  <line x1="380" y1="115" x2="410" y2="115" stroke="#333" stroke-width="2" marker-end="url(#arrow7)"/>
  <line x1="510" y1="115" x2="540" y2="115" stroke="#333" stroke-width="2" marker-end="url(#arrow7)"/>
  <text x="70" y="160" text-anchor="middle" fill="#555" font-size="9">Dockerfile</text>
  <text x="200" y="160" text-anchor="middle" fill="#555" font-size="9">Trivy/Grype</text>
  <text x="330" y="160" text-anchor="middle" fill="#555" font-size="9">cosign</text>
  <text x="460" y="160" text-anchor="middle" fill="#555" font-size="9">Tag/Copy</text>
  <text x="590" y="160" text-anchor="middle" fill="#555" font-size="9">K8s/ECS</text>
  <defs>
    <marker id="arrow7" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---
## Garbage Collection and Retention
- Artifact repositories accumulate data quickly
- Retention policies are essential:
    - Keep last N versions of each artifact
    - Delete untagged images after X days
    - Preserve all production-promoted versions
    - Archive to cold storage after retention period
- Automate with registry-native GC or tools like `skopeo`
---
## Registry Mirroring and Caching
- Pull-through cache reduces external dependency
- Mirror strategy:
    - Primary registry in main region
    - Read-only mirrors in other regions
    - Pull-through proxy for public registries
- Benefits:
    - Faster image pulls
    - Resilience against upstream outages
    - Reduced egress costs
    - Bandwidth savings
---
## Artifact Promotion: Complete Pipeline
```yaml
# GitHub Actions promotion example
jobs:
  build:
    steps:
    - run: docker build -t myapp:$SHA .
    - run: trivy image --exit-code 1 myapp:$SHA
    - run: docker push registry/myapp:$SHA
  promote-staging:
    needs: build
    steps:
    - run: cosign verify registry/myapp:$SHA
    - run: skopeo copy \
        docker://registry/myapp:$SHA \
        docker://registry/staging/myapp:$SHA
  promote-prod:
    needs: promote-staging
    environment: production
    steps:
    - run: skopeo copy \
        docker://registry/staging/myapp:$SHA \
        docker://registry/prod/myapp:$SHA
```
---
## Artifact Metadata Best Practices
- Label every artifact with:
    - `org.opencontainers.image.source` (repo URL)
    - `org.opencontainers.image.revision` (commit SHA)
    - `org.opencontainers.image.created` (timestamp)
    - `org.opencontainers.image.version` (SemVer)
```dockerfile
LABEL org.opencontainers.image.source=\
  "https://github.com/myorg/myapp"
LABEL org.opencontainers.image.revision=\
  "a3f8b2c"
LABEL org.opencontainers.image.version=\
  "2.3.1"
```
---
## Anti-Patterns to Avoid
- Rebuilding artifacts between environments
- Using `latest` tag in production deployments
- Storing secrets in artifact layers
- Skipping vulnerability scans in CI
- Allowing mutable versions in release repos
- Not cleaning up old artifacts (storage bloat)
- Missing SBOM generation
- Running containers as root
---
## Artifact Management Maturity Model
| Level | Characteristics |
|-------|----------------|
| Level 1 | Manual builds, no central repository |
| Level 2 | Central repository, basic CI uploads |
| Level 3 | Automated promotion, scanning gates |
| Level 4 | Signed artifacts, SBOM, full traceability |
| Level 5 | Policy-as-code, automated compliance |
---
## Key Takeaways
- Store artifacts in a central repository with clear promotion stages
- Never rebuild between environments; promote the tested artifact
- Choose versioning strategy based on audience: `SemVer` for public, commit-based for internal
- Enforce immutability to guarantee reproducibility
- Sign and scan container images at every stage
- Use slim or `distroless` base images in production
- Automate policy enforcement with admission controllers
- Maintain full traceability from deployment back to source commit
