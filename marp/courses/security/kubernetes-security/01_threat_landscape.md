---
tags:
  - security:kubernetes
  - concepts:threat-model
level: intermediate
category: security
audience:
  - audiences:devops
  - audiences:security-professionals

---
# Kubernetes Threat Landscape

---
## What This Chapter Covers

- Why Kubernetes security is its own discipline
- The 4Cs: Cloud, Cluster, Container, Code
- Major threat actors and attack paths
- Common misconfigurations
- Defense in depth strategy

---
## Why Kubernetes Security Matters

- Kubernetes runs production for most modern companies
- Misconfigurations are common; some are catastrophic
- A compromised cluster can mean data loss, supply chain attacks, ransom
- Dynamic, distributed: hard to audit point-in-time
- Multiple layers — each needs hardening

---
## The 4Cs of Cloud-Native Security

- Cloud — provider account, IAM, networking
- Cluster — control plane, API server, etcd, nodes
- Container — image, runtime, capabilities
- Code — application security
- Each is necessary; none is sufficient

---
## 4Cs Visualized

![4cs](svg/courses/security/kubernetes-security/01_threat_landscape/4cs.svg)

---
## Common Attack Surfaces

![attack_surfaces](svg/courses/security/kubernetes-security/01_threat_landscape/attack_surfaces.svg)

---
## Cloud Layer

- Identity and access management
- Network controls (VPC, security groups)
- Encryption keys (KMS)
- Compromise here = total compromise
- Most cloud breaches are misconfiguration

---
## Cluster Layer

- API server authentication and authorization
- etcd encryption at rest
- Kubelet hardening
- Audit logging
- Control plane upgrade hygiene

---
## Container Layer

- Image provenance and scanning
- Pod Security Standards
- Capabilities, seccomp, AppArmor
- Read-only filesystems
- Non-root users

---
## Code Layer

- Application vulnerabilities (OWASP-style)
- Dependency hygiene
- Secrets handling
- Out of scope for this course; not out of scope for security

---
## Threat Actors

- Opportunistic scanners — automated discovery of misconfigs
- Insiders — disgruntled or careless employees
- Supply chain — compromised images, charts, operators
- Advanced — nation-state, financial criminal groups
- Each warrants different defenses

---
## Actor Profiles

![threat_actors](svg/courses/security/kubernetes-security/01_threat_landscape/threat_actors.svg)

---
## Common Attack Paths

- Exposed dashboard or API server
- Container escape via kernel/runtime bugs
- RBAC misconfiguration: over-privileged service accounts
- Stolen kubeconfig from a developer machine
- Compromised CI/CD pipeline pushing malicious images

---
## The Most Common Misconfigs

- Containers running as root
- Privileged containers (--privileged)
- HostPath mounts without restriction
- Open admin ports (kubelet, etcd)
- Weak RBAC: cluster-admin everywhere

---
## Pod Escape Scenarios

- Privileged container → host root
- HostPath mount → read host files
- HostPID → see host processes
- HostNetwork → bypass network policies
- Each is a designed-in danger; restrict via Pod Security Standards

---
## RBAC Pitfalls

- ClusterRole/ClusterRoleBinding sprawl
- Default service accounts with broad access
- Wildcard verbs (`*` resources, `*` verbs)
- Long-lived tokens
- Lack of audit on what was granted

---
## Network Threats

- East-west traffic without policies
- Pod-to-pod free communication by default
- Exfiltration via outbound DNS or HTTP
- Lateral movement after one compromised pod
- Default-deny network policies fix most of this

---
## Supply Chain Threats

- Compromised base images
- Malicious npm/pip dependencies
- Hijacked Helm charts
- Backdoored operators
- Always verify provenance; sign and verify

---
## Etcd Compromise

- Etcd holds all cluster state, including secrets
- Default: secrets are base64, not encrypted
- Encryption at rest is opt-in
- Anyone with etcd access has cluster admin
- Etcd network exposure is critical

---
## Kubelet Compromise

- Kubelet runs on every node
- Has root on the node
- Read-only port (10255) historically allowed unauthenticated access
- Disable; require authentication
- Compromise = node compromise

---
## API Server Exposure

- The brain of the cluster
- Internet-exposed in many setups
- Authentication required for everything
- Authorization layered: RBAC + admission
- Audit log every request

---
## Defense in Depth

- No single control suffices
- Image scanning catches some bugs
- PSP/PSS catches some misconfigs
- Network policies catch some lateral movement
- RBAC catches some authz mistakes
- Layer them all

---
## Compliance Frameworks

- CIS Kubernetes Benchmark — most-used baseline
- NIST 800-190 — container security guidelines
- PCI DSS — for payment-handling clusters
- SOC 2 — common for SaaS
- Each maps to specific Kubernetes controls

---
## CIS Benchmark

- Hundreds of recommendations
- Tools like kube-bench automate the audit
- Run regularly, fix systematically
- Score improvements measurable
- Starting point for every serious cluster

---
## Course Roadmap

- Chapter 2: Pod Security Standards
- Chapter 3: Network Policies
- Chapter 4: Admission Controllers and RBAC
- Chapter 5: Secrets and Image Scanning
- Chapter 6: Runtime Security and Hardening

---
## Common Misconceptions

- "Cloud provider handles security" — only the cluster floor; you secure your workloads
- "Image scanning is enough" — runtime threats beat scans
- "Default settings are safe" — they are not
- "We're internal-only" — east-west matters too
- "RBAC is just RBAC" — it's a complex skill in itself

---
## What Tools Exist

- kube-bench — CIS benchmark scanner
- kube-hunter — penetration testing
- Trivy / Grype / Snyk — image scanners
- Falco / Tracee — runtime detection
- OPA / Kyverno — policy engines
- Each fits a different layer

---
## Summary

- The 4Cs frame Kubernetes security: Cloud, Cluster, Container, Code
- Misconfigurations are the most common source of incidents
- Defense in depth across layers; no silver bullets
- CIS Benchmark is the baseline; tools automate the audit
- The next chapters go deep on each layer
