# Supply Chain Attacks

---
## What is a Supply Chain Attack?

- A supply chain attack targets the less-secure elements in the software or hardware supply chain
- Instead of attacking the target directly, attackers compromise a supplier, dependency, or tool the target trusts
- The compromised component is then delivered to the target through normal update/distribution channels
- Extremely effective because the malicious code arrives through trusted channels

```python
┌──────────────────────────────────────────────────────────┐
│          Supply Chain Attack Concept                      │
│                                                          │
│  Traditional Attack:                                     │
│  Attacker ─────────────────────────────> Target          │
│            (blocked by security controls)                │
│                                                          │
│  Supply Chain Attack:                                    │
│  Attacker ──> Supplier/Dependency ──> Target             │
│               (trusted channel!)                         │
│                                                          │
│  The target's own security controls                      │
│  ALLOW the malicious code in because                     │
│  it comes from a "trusted" source                        │
└──────────────────────────────────────────────────────────┘
```

---
## Types of Software Supply Chain Attacks

| Attack Type                  | Vector                                    | Example               |
|------------------------------|-------------------------------------------|-----------------------|
| Dependency confusion         | Package registry name collision           | Alex Birsan (2021)    |
| Typosquatting                | Similar package names with typos          | crossenv / cross-env  |
| Compromised maintainer       | Hijack or bribe package maintainer        | event-stream (2018)   |
| Build pipeline compromise    | Inject into CI/CD system                  | SolarWinds (2020)     |
| Code signing compromise      | Steal or forge code signing keys          | ASUS ShadowHammer     |
| Vendor software compromise   | Backdoor vendor's product                 | 3CX (2023)            |
| Open source contribution     | Malicious PR merged into project          | xz-utils (2024)       |
| Container image poisoning    | Malicious Docker images on registries     | Various               |

---
## Software Supply Chain Attack Flow

```bash
┌──────────────────────────────────────────────────────────┐
│          Attack Flow: Build Pipeline Compromise           │
│                                                          │
│  1. Attacker gains access to build system                │
│     (CI/CD server, build scripts, developer machine)     │
│                                                          │
│  2. Injects malicious code into build pipeline           │
│     (not in source code repo -- harder to detect!)       │
│                                                          │
│  3. Clean source code produces tainted binary            │
│     ┌────────────┐    ┌──────────┐    ┌─────────────┐   │
│     │ Clean      │───>│Compromised│───>│ Tainted     │   │
│     │ Source Code│    │ Build     │    │ Binary      │   │
│     │ (GitHub)   │    │ System    │    │ (signed!)   │   │
│     └────────────┘    └──────────┘    └──────┬──────┘   │
│                                              │           │
│  4. Tainted binary distributed via           │           │
│     normal software update channels          │           │
│                                              v           │
│                                       ┌─────────────┐   │
│                                       │ 18,000+     │   │
│                                       │ Customers   │   │
│                                       └─────────────┘   │
└──────────────────────────────────────────────────────────┘
```

---
## Case Study: SolarWinds SUNBURST (2020)

```bash
┌──────────────────────────────────────────────────────────┐
│          SolarWinds SUNBURST Timeline                     │
│                                                          │
│  Sep 2019  Attackers gain access to SolarWinds network   │
│                                                          │
│  Oct 2019  Attackers inject test code into Orion build   │
│            (testing their access works)                   │
│                                                          │
│  Feb 2020  SUNBURST backdoor injected into Orion build   │
│            pipeline (SolarWinds.Orion.Core.dll)          │
│                                                          │
│  Mar 2020  Tainted Orion update (2020.2) released        │
│            - Digitally signed by SolarWinds              │
│            - Distributed through normal update channel   │
│            - 18,000+ organizations installed it          │
│                                                          │
│  Dec 2020  FireEye discovers the backdoor                │
│            (9 months of undetected access!)              │
│                                                          │
│  Victims included:                                       │
│  - US Treasury, Commerce, Homeland Security              │
│  - Microsoft, Intel, Cisco, Deloitte                     │
│  - FireEye (who discovered it)                           │
│                                                          │
│  Attribution: Russian SVR (APT29 / Cozy Bear)            │
└──────────────────────────────────────────────────────────┘
```

**SUNBURST technical details:**
- Backdoor waited 12-14 days before activating (evade sandbox analysis)
- Used DNS for C2 communication (encoded in subdomain names)
- Checked for security tools and disabled them before acting
- Only activated on "interesting" targets (selective targeting)

---
## Case Study: xz-utils Backdoor (2024)

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="340" viewBox="0 0 660 340">
  <rect width="660" height="340" fill="#f0f4f8" rx="4" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="26" font-family="sans-serif" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">xz-utils Backdoor (CVE-2024-3094)</text>
  <!-- rows -->
  <rect x="20" y="40" width="90" height="44" fill="#e3f2fd" rx="4" stroke="#555" stroke-width="1"/>
  <text x="65" y="59" font-family="sans-serif" font-size="11" font-weight="bold" fill="#1565c0" text-anchor="middle">2 years</text>
  <text x="65" y="74" font-family="sans-serif" font-size="11" fill="#1565c0" text-anchor="middle">setup</text>
  <text x="125" y="56" font-family="sans-serif" font-size="12" fill="#222">"Jia Tan" builds trust as xz-utils contributor</text>
  <text x="125" y="74" font-family="sans-serif" font-size="12" fill="#222">with legitimate patches</text>
  <rect x="20" y="92" width="90" height="44" fill="#e3f2fd" rx="4" stroke="#555" stroke-width="1"/>
  <text x="65" y="111" font-family="sans-serif" font-size="11" font-weight="bold" fill="#1565c0" text-anchor="middle">Pressure</text>
  <text x="65" y="126" font-family="sans-serif" font-size="11" fill="#1565c0" text-anchor="middle">campaign</text>
  <text x="125" y="108" font-family="sans-serif" font-size="12" fill="#222">Social pressure to add Jia Tan as co-maintainer</text>
  <text x="125" y="126" font-family="sans-serif" font-size="12" fill="#222">(sockpuppet accounts)</text>
  <rect x="20" y="144" width="90" height="58" fill="#fff3e0" rx="4" stroke="#e65100" stroke-width="1"/>
  <text x="65" y="163" font-family="sans-serif" font-size="11" font-weight="bold" fill="#e65100" text-anchor="middle">Backdoor</text>
  <text x="65" y="178" font-family="sans-serif" font-size="11" fill="#e65100" text-anchor="middle">insertion</text>
  <text x="125" y="160" font-family="sans-serif" font-size="12" fill="#222">Malicious code hidden in .xz test fixture files</text>
  <text x="125" y="178" font-family="sans-serif" font-size="12" fill="#222">Injected during build process, invisible in source</text>
  <text x="125" y="196" font-family="sans-serif" font-size="12" fill="#222">Target: liblzma → sshd (via systemd) → RCE via SSH</text>
  <rect x="20" y="210" width="90" height="44" fill="#ffebee" rx="4" stroke="#c62828" stroke-width="1"/>
  <text x="65" y="229" font-family="sans-serif" font-size="11" font-weight="bold" fill="#c62828" text-anchor="middle">Discovery</text>
  <text x="125" y="226" font-family="sans-serif" font-size="12" fill="#222">Andres Freund noticed 500ms SSH delay</text>
  <text x="125" y="244" font-family="sans-serif" font-size="12" fill="#222">and investigated (pure luck!)</text>
  <rect x="20" y="262" width="90" height="30" fill="#e8f5e9" rx="4" stroke="#2e7d32" stroke-width="1"/>
  <text x="65" y="281" font-family="sans-serif" font-size="11" font-weight="bold" fill="#2e7d32" text-anchor="middle">Impact</text>
  <text x="125" y="278" font-family="sans-serif" font-size="12" fill="#222">Would have backdoored most Linux distros — caught just before widespread deployment</text>
  <rect x="20" y="300" width="90" height="30" fill="#f3e5f5" rx="4" stroke="#7b1fa2" stroke-width="1"/>
  <text x="65" y="319" font-family="sans-serif" font-size="11" font-weight="bold" fill="#7b1fa2" text-anchor="middle">Lesson</text>
  <text x="125" y="316" font-family="sans-serif" font-size="12" fill="#222">Even open source review can be subverted with patient, long-term social engineering</text>
</svg>

---
## Dependency Confusion

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="330" viewBox="0 0 660 330">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>
  <rect width="660" height="330" fill="#f0f4f8" rx="4" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="26" font-family="sans-serif" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">Dependency Confusion Attack</text>
  <text x="330" y="50" font-family="sans-serif" font-size="12" fill="#555" text-anchor="middle">Company uses internal package: @company/auth-utils (private registry)</text>
  <text x="330" y="68" font-family="sans-serif" font-size="12" fill="#555" text-anchor="middle">Build system resolves: 1. Private registry, 2. Public registry (fallback)</text>
  <!-- private reg -->
  <rect x="40" y="90" width="180" height="70" fill="#e8f5e9" rx="4" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="130" y="112" font-family="sans-serif" font-size="13" font-weight="bold" fill="#2e7d32" text-anchor="middle">Private Registry</text>
  <text x="130" y="130" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">auth-utils v1.2.3</text>
  <text x="130" y="148" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">(legitimate)</text>
  <!-- public reg -->
  <rect x="440" y="90" width="180" height="70" fill="#ffebee" rx="4" stroke="#c62828" stroke-width="1.5"/>
  <text x="530" y="112" font-family="sans-serif" font-size="13" font-weight="bold" fill="#c62828" text-anchor="middle">Public Registry</text>
  <text x="530" y="130" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">auth-utils v99.0.0</text>
  <text x="530" y="148" font-family="sans-serif" font-size="11" fill="#c62828" text-anchor="middle">← MALICIOUS</text>
  <!-- arrows down to build system -->
  <line x1="130" y1="160" x2="280" y2="215" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="530" y1="160" x2="380" y2="215" stroke="#c62828" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- build system box -->
  <rect x="200" y="215" width="260" height="50" fill="#fff3e0" rx="4" stroke="#e65100" stroke-width="2"/>
  <text x="330" y="236" font-family="sans-serif" font-size="13" font-weight="bold" fill="#e65100" text-anchor="middle">Build System: v99 &gt; v1.2.3</text>
  <text x="330" y="254" font-family="sans-serif" font-size="12" fill="#c62828" text-anchor="middle">Installs PUBLIC package! ← WRONG</text>
  <text x="330" y="295" font-family="sans-serif" font-size="12" fill="#555" text-anchor="middle">Alex Birsan (2021): Compromised Apple, Microsoft, PayPal, Netflix, Uber</text>
  <text x="330" y="313" font-family="sans-serif" font-size="12" fill="#555" text-anchor="middle">with this technique</text>
</svg>

---
## Dependency Confusion Defense

```bash
# npm: Use scoped packages and registry configuration
# .npmrc
@company:registry=https://private.registry.company.com/
registry=https://registry.npmjs.org/
# Scoped packages (@company/*) always come from private registry

# Python: Use --index-url and --extra-index-url carefully
# pip.conf
[global]
index-url = https://private.registry.company.com/simple/
# Do NOT use --extra-index-url (allows fallback to PyPI!)

# Better: Pin exact versions and use lockfiles
# package-lock.json, Pipfile.lock, poetry.lock
```

```python
# Python: Verify package source in CI/CD
import subprocess
import json

def verify_packages():
    """Ensure no packages come from unexpected sources."""
    result = subprocess.run(
        ['pip', 'list', '--format=json'],
        capture_output=True, text=True
    )
    packages = json.loads(result.stdout)

    for pkg in packages:
        # Check each package origin
        show = subprocess.run(
            ['pip', 'show', pkg['name']],
            capture_output=True, text=True
        )
        if 'pypi.org' in show.stdout and pkg['name'].startswith('internal-'):
            raise SecurityError(
                f"Internal package {pkg['name']} installed from PyPI!"
            )
```

---
## Typosquatting Attacks

```bash
┌──────────────────────────────────────────────────────────┐
│  Typosquatting Examples                                  │
├─────────────────────┬────────────────────────────────────┤
│  Legitimate Package │  Typosquat Variants                │
├─────────────────────┼────────────────────────────────────┤
│  cross-env          │  crossenv (malicious, 2017)        │
│  lodash             │  lodahs, lodas, lodassh            │
│  requests           │  reqeusts, request, requets        │
│  colors             │  colour, colorsjs, color           │
│  urllib3             │  urllib, urlib3, urllib4            │
│  python-nmap        │  nmap-python, python_nmap          │
│  tensorflow         │  tenserflow, tensorflw             │
└─────────────────────┴────────────────────────────────────┘
│                                                          │
│  Techniques:                                             │
│  - Character substitution (o -> 0, l -> 1)              │
│  - Missing/extra characters (lodash -> lodas)            │
│  - Hyphen/underscore confusion (my-pkg -> my_pkg)        │
│  - Namespace confusion (@scope/pkg -> scope-pkg)         │
│  - Different separator (python-nmap -> python.nmap)      │
└──────────────────────────────────────────────────────────┘
```

---
## npm and PyPI Security Incidents

| Incident                | Year | Package/Registry | Impact                         |
|-------------------------|------|------------------|--------------------------------|
| event-stream            | 2018 | npm              | Crypto wallet theft            |
| ua-parser-js            | 2021 | npm              | Cryptominer + password stealer |
| colors / faker          | 2022 | npm              | Maintainer protest (corruption)|
| PyPI typosquats         | 2022 | PyPI             | 400+ malicious packages found  |
| ctx + phpass            | 2022 | PyPI/PHP         | Exfiltrated env variables      |
| Ledger Connect Kit      | 2023 | npm              | Crypto wallet drainer injected |
| polyfill.io takeover    | 2024 | CDN              | Malicious JS served to 100K+ sites |

---
## Software Bill of Materials (SBOM)

```bash
┌──────────────────────────────────────────────────────────┐
│          Software Bill of Materials (SBOM)                │
│                                                          │
│  An SBOM is a formal inventory of all components,        │
│  libraries, and dependencies in a software product       │
│                                                          │
│  Like a "nutrition label" for software                   │
│                                                          │
│  ┌────────────────────────────────────────────┐          │
│  │  MyApp v2.1.0                              │          │
│  │  ├── express v4.18.2                       │          │
│  │  │   ├── accepts v1.3.8                    │          │
│  │  │   ├── body-parser v1.20.1              │          │
│  │  │   │   └── bytes v3.1.2                 │          │
│  │  │   ├── content-type v1.0.5              │          │
│  │  │   └── cookie v0.5.0                    │          │
│  │  ├── jsonwebtoken v9.0.0                   │          │
│  │  │   └── jws v3.2.2                       │          │
│  │  └── pg v8.11.0                            │          │
│  │      └── pg-protocol v1.6.0               │          │
│  └────────────────────────────────────────────┘          │
│                                                          │
│  Formats: SPDX (ISO standard), CycloneDX (OWASP)        │
│  US Executive Order 14028 (2021) requires SBOMs          │
│  for software sold to the federal government             │
└──────────────────────────────────────────────────────────┘
```

```bash
# Generate SBOM with Syft
syft dir:./myapp -o spdx-json > sbom.spdx.json
syft dir:./myapp -o cyclonedx-json > sbom.cdx.json

# Scan SBOM for known vulnerabilities with Grype
grype sbom:./sbom.spdx.json

# npm: Built-in audit
npm audit
npm audit --json

# Python
pip-audit
safety check
```

---
## Verification Strategies

### Package Signing and Verification

```bash
# npm: Check package provenance (npm v9+)
npm audit signatures

# Python: Verify package hashes
pip install --require-hashes -r requirements.txt
# requirements.txt with hashes:
# requests==2.31.0 \
#   --hash=sha256:58cd2187c01e70e6e26505bca751777aa9f2ee0b7f4300988b709f44e013003eb

# Go: Module checksums verified automatically
# go.sum file contains expected hashes
go mod verify

# Container images: Verify signatures
cosign verify --key cosign.pub myregistry/myimage:latest
```

---
## Sigstore: Open Source Signing

```bash
┌──────────────────────────────────────────────────────────┐
│          Sigstore Ecosystem                               │
│                                                          │
│  Problem: Traditional code signing requires managing     │
│  long-lived private keys (complex and risky)             │
│                                                          │
│  Sigstore solution: Keyless signing using OIDC identity  │
│                                                          │
│  Components:                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐               │
│  │  Cosign   │  │  Fulcio   │  │  Rekor   │               │
│  │ (signing  │  │ (cert     │  │ (trans-  │               │
│  │  tool)    │  │  authority)│  │  parency │               │
│  └────┬──────┘  └────┬──────┘  │  log)    │               │
│       │              │         └────┬─────┘               │
│       v              v              v                     │
│  1. Developer authenticates via OIDC (GitHub, Google)    │
│  2. Fulcio issues short-lived signing certificate        │
│  3. Cosign signs the artifact                            │
│  4. Signature recorded in Rekor transparency log         │
│  5. Certificate expires (no long-lived keys to steal!)   │
└──────────────────────────────────────────────────────────┘
```

```bash
# Sign a container image with Sigstore/Cosign
cosign sign myregistry.io/myimage:v1.0.0
# (triggers OIDC login, keyless signing)

# Verify a signed image
cosign verify myregistry.io/myimage:v1.0.0

# Sign a blob/artifact
cosign sign-blob --bundle artifact.bundle myfile.tar.gz

# npm provenance (uses Sigstore)
npm publish --provenance
# Publishes with cryptographic proof of build origin
```

---
## CI/CD Pipeline Security

```bash
┌──────────────────────────────────────────────────────────┐
│  Securing the Build Pipeline                             │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Source Code:                                            │
│  [ ] Require signed commits (git commit -S)             │
│  [ ] Branch protection rules (required reviews)          │
│  [ ] Dependency scanning in PRs (Dependabot, Snyk)       │
│  [ ] Pin dependencies to exact versions + lockfiles      │
│                                                          │
│  Build System:                                           │
│  [ ] Isolated, ephemeral build environments              │
│  [ ] Reproducible builds (same source = same binary)     │
│  [ ] Minimal build permissions (least privilege)         │
│  [ ] Audit trail for all build actions                   │
│  [ ] Secret scanning (no credentials in code)            │
│                                                          │
│  Artifacts:                                              │
│  [ ] Sign all build artifacts (Sigstore/Cosign)          │
│  [ ] Generate SBOM for every release                     │
│  [ ] Scan artifacts for vulnerabilities before deploy    │
│  [ ] Use content-addressable storage (by hash, not tag)  │
│                                                          │
│  Distribution:                                           │
│  [ ] Verify signatures before deployment                 │
│  [ ] Use private/curated package registries              │
│  [ ] Monitor for unauthorized changes post-deploy        │
└──────────────────────────────────────────────────────────┘
```

---
## SLSA Framework (Supply-chain Levels for Software Artifacts)

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="280" viewBox="0 0 660 280">
  <rect width="660" height="280" fill="#f0f4f8" rx="4" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="26" font-family="sans-serif" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">SLSA Levels (pronounced "salsa") — https://slsa.dev</text>
  <rect x="30" y="45" width="600" height="46" fill="#eeeeee" rx="4" stroke="#999" stroke-width="1"/>
  <text x="90" y="65" font-family="sans-serif" font-size="13" font-weight="bold" fill="#333">Level 0</text>
  <text x="160" y="65" font-family="sans-serif" font-size="13" fill="#555">No guarantees</text>
  <text x="160" y="82" font-family="sans-serif" font-size="11" fill="#888">(most software today)</text>
  <rect x="30" y="98" width="600" height="46" fill="#e3f2fd" rx="4" stroke="#1565c0" stroke-width="1"/>
  <text x="90" y="118" font-family="sans-serif" font-size="13" font-weight="bold" fill="#1565c0">Level 1</text>
  <text x="160" y="118" font-family="sans-serif" font-size="13" fill="#333">Build provenance exists</text>
  <text x="160" y="135" font-family="sans-serif" font-size="11" fill="#555">(documentation of how it was built)</text>
  <rect x="30" y="151" width="600" height="46" fill="#e8f5e9" rx="4" stroke="#2e7d32" stroke-width="1"/>
  <text x="90" y="171" font-family="sans-serif" font-size="13" font-weight="bold" fill="#2e7d32">Level 2</text>
  <text x="160" y="171" font-family="sans-serif" font-size="13" fill="#333">Signed provenance, hosted build service</text>
  <text x="160" y="188" font-family="sans-serif" font-size="11" fill="#555">(tamper-resistant build records)</text>
  <rect x="30" y="204" width="600" height="60" fill="#fff3e0" rx="4" stroke="#e65100" stroke-width="1.5"/>
  <text x="90" y="224" font-family="sans-serif" font-size="13" font-weight="bold" fill="#e65100">Level 3</text>
  <text x="160" y="224" font-family="sans-serif" font-size="13" fill="#333">Hardened build platform</text>
  <text x="160" y="242" font-family="sans-serif" font-size="11" fill="#555">(isolated, ephemeral, auditable builds)</text>
  <text x="160" y="257" font-family="sans-serif" font-size="11" fill="#555">(protects against SolarWinds-style attacks)</text>
</svg>

---
## Practical Defense Checklist

```bash
# 1. Lock all dependency versions
npm ci                    # Uses lockfile, not package.json ranges
pip install -r requirements.txt  # Pin exact versions

# 2. Audit dependencies regularly
npm audit
pip-audit
snyk test

# 3. Monitor for new vulnerabilities
# GitHub Dependabot (automatic)
# Snyk (continuous monitoring)
# OSV (open source vulnerability database)

# 4. Use lockfiles and verify integrity
npm ci --ignore-scripts   # Don't run postinstall scripts
pip install --require-hashes -r requirements.txt

# 5. Minimize dependencies
# Ask: Do I really need this library?
# Can I write this myself in < 50 lines?

# 6. Pin container base images by digest
# BAD:  FROM node:18
# GOOD: FROM node:18@sha256:abc123def456...

# 7. Scan container images
trivy image myapp:latest
grype myapp:latest
```

---
## Key Takeaways

- Supply chain attacks exploit trust relationships to bypass security controls
- SolarWinds demonstrated that even signed, officially distributed software can be backdoored
- The xz-utils incident showed that long-term social engineering can compromise open source
- Dependency confusion and typosquatting are low-effort, high-impact attack vectors
- SBOMs provide visibility into what components are in your software
- Sigstore enables keyless signing, making artifact verification more accessible
- SLSA framework provides maturity levels for build pipeline security
- Defense requires: dependency pinning, lockfiles, auditing, signing, and monitoring
- The software supply chain is only as strong as its weakest link
