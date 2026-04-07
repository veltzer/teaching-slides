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
![artifact_repository_architecture](/svg/courses/devops/architectural-decisions-in-devops/04_artifact_management_and_promotion/artifact_repository_architecture.svg)

---
## Promotion Between Stages
- Promotion = moving an artifact from one stage to the next
- Typical pipeline: `dev` -> `staging` -> `production`
- Key principle: **never rebuild** between stages
- The same binary tested in staging is deployed to production
- Promotion is a metadata operation, not a rebuild
---
## Promotion Pipeline: Overview
![promotion_pipeline_overview](/svg/courses/devops/architectural-decisions-in-devops/04_artifact_management_and_promotion/promotion_pipeline_overview.svg)

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
![semver_version_ordering](/svg/courses/devops/architectural-decisions-in-devops/04_artifact_management_and_promotion/semver_version_ordering.svg)

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
![traceability_from_deploy_to_source](/svg/courses/devops/architectural-decisions-in-devops/04_artifact_management_and_promotion/traceability_from_deploy_to_source.svg)

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
![container_image_layers](/svg/courses/devops/architectural-decisions-in-devops/04_artifact_management_and_promotion/container_image_layers.svg)

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
![base_image_tiering](/svg/courses/devops/architectural-decisions-in-devops/04_artifact_management_and_promotion/base_image_tiering.svg)

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
![policy_enforcement_architecture](/svg/courses/devops/architectural-decisions-in-devops/04_artifact_management_and_promotion/policy_enforcement_architecture.svg)

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
![slim_image_comparison](/svg/courses/devops/architectural-decisions-in-devops/04_artifact_management_and_promotion/slim_image_comparison.svg)

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
![multi_stage_build_layer_diagram](/svg/courses/devops/architectural-decisions-in-devops/04_artifact_management_and_promotion/multi_stage_build_layer_diagram.svg)

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
![container_image_lifecycle](/svg/courses/devops/architectural-decisions-in-devops/04_artifact_management_and_promotion/container_image_lifecycle.svg)

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
