---
tags:
  - security:kubernetes
  - concepts:runtime
level: intermediate
category: security
audience:
  - audiences:devops

---
# Runtime Security and Hardening

---
## What This Chapter Covers

- Runtime threat detection (Falco, Tracee)
- Cluster hardening checklist
- Kubelet, etcd, API server hardening
- Audit logging
- Incident response basics

---
## Why Runtime Matters

- Image scans find known CVEs at build time
- Runtime catches the unknown: behavioral anomalies
- Active exploit detection in production
- Drift from the expected baseline
- Image scanning + runtime detection = full coverage

---
## Hardening Layers

![hardening_layers](svg/courses/security/kubernetes-security/06_runtime_hardening/hardening_layers.svg)

---
## Falco

- Open-source runtime security tool
- Watches syscalls via eBPF or kernel module
- Rules describe normal/abnormal
- Alerts on suspicious behavior
- The most-used tool in this space

---
## Falco Rule Example

```output
- rule: Shell in container
  desc: A shell was spawned in a container
  condition: >
    spawned_process and container and shell_procs
  output: >
    Shell spawned (user=%user.name container=%container.name)
  priority: WARNING
```

- Catches the moment an attacker drops a shell

---
## What Falco Detects

- Shells in containers
- Writes to system directories
- Reading sensitive files (/etc/shadow)
- Outbound connections to suspicious IPs
- Unexpected process executions

---
## Tracee

- Aqua's runtime security tool
- eBPF-based, similar concept to Falco
- Wider event types in some areas
- Both production-ready
- Some teams run both for coverage

---
## Runtime Tool Architecture

![runtime_arch](svg/courses/security/kubernetes-security/06_runtime_hardening/runtime_arch.svg)

---
## kube-bench

- Automated CIS Benchmark scanner
- Run on each node and the control plane
- Reports failed checks
- Tracks remediation over time
- The starting point for hardening

---
## CIS Benchmark Checks

- API server flags (--anonymous-auth=false, etc)
- Kubelet config (read-only port disabled)
- etcd encryption and TLS
- File permissions on /etc/kubernetes
- Audit logging enabled

---
## API Server Hardening

- Disable anonymous auth (--anonymous-auth=false)
- Enforce TLS 1.2+ ciphers
- Restrict API access by CIDR (cloud LB rules)
- Aggregator layer secured
- Request rate limits configured

---
## Kubelet Hardening

- Disable read-only port (--read-only-port=0)
- Require client cert auth (--anonymous-auth=false)
- Enable webhook authorization
- Audit log enabled
- Rotate certificates automatically

---
## etcd Hardening

- TLS for client and peer connections
- Mutual auth between API server and etcd
- Encryption at rest enabled
- Restrict network access to etcd (private subnet)
- Backup regularly to a separate trust domain

---
## Network Hardening

- Restrict API server CIDR allowlist
- VPC private endpoints where possible
- Disallow public node IPs
- Outbound egress controls
- Cloud security groups locked down

---
## Audit Logging

- Records every API request
- Configure audit policy (what to log)
- Levels: None, Metadata, Request, RequestResponse
- Ship logs off-cluster for retention
- Review periodically

---
## Audit Policy Example

```yaml
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
  - level: RequestResponse
    resources:
      - group: ""
        resources: ["secrets", "configmaps"]
  - level: Metadata
    omitStages: [RequestReceived]
```

- Sensitive resources at RequestResponse level
- Everything else at Metadata

---
## What to Alert On

- Failed authentication attempts
- Privilege escalation: bind to cluster-admin
- Reading/listing all secrets
- Pod creation in kube-system
- Exec into running pods

---
## Cloud Security Posture

- Cloud Security Posture Management (CSPM) tools
- Wiz, Prisma Cloud, Aqua
- Cluster + cloud + workload combined view
- Auto-detect drift from baseline
- Worth the cost for serious clusters

---
## Penetration Testing

- kube-hunter for Kubernetes-specific tests
- Standard pen tests focused on the cluster
- Run before going live; periodically thereafter
- Bug bounty programs cover real-world testing
- Results drive concrete improvements

---
## Incident Response

- Detect — runtime alerts, anomalous metrics
- Contain — isolate the pod (network policy, taint node)
- Eradicate — remove the threat
- Recover — restore service
- Learn — postmortem, fix root cause

---
## Containment Tactics

- Apply restrictive NetworkPolicy to suspect pod
- Cordon and drain the node
- Revoke service account tokens
- Snapshot the pod's filesystem before deletion
- Preserve logs and audit trail

---
## Forensics in Kubernetes

- Pod logs (ephemeral; capture early)
- Audit logs (kept centrally)
- Cloud logs (VPC flow, GuardDuty)
- Filesystem snapshots
- Image scan reports for that exact image

---
## Backup and Recovery

- etcd backups: daily minimum
- Encrypted, off-cluster
- Test restores periodically
- Velero for application-level backups
- Disaster recovery plan exercised

---
## Upgrade Hygiene

- Stay on supported versions
- Security patches: apply within weeks
- Test in staging clusters first
- Automate where possible (kubeadm, managed services)
- Out-of-support versions = unpatched CVEs

---
## Common Pitfalls

- Runtime tools deployed but no one watches alerts
- Audit logs enabled but never reviewed
- CIS Benchmark scored but findings ignored
- No incident response plan tested
- Backups exist but never restored

---
## Best Practices

- Run kube-bench regularly; track remediation
- Falco or Tracee with rules tuned to your apps
- Audit log all sensitive operations
- Test incident response with tabletop exercises
- Keep upgrade cadence tight

---
## Course Recap

- Threat landscape: 4Cs framework
- Pod Security Standards
- Network Policies
- Admission and RBAC
- Secrets and image security
- Runtime detection and hardening

---
## Final Thoughts

- Kubernetes security is layered; no single tool wins
- Misconfigurations cause most incidents
- Defense in depth: hardening, policies, runtime, audit
- Automation prevents drift
- Stay current — the platform and threats both evolve

---
## Summary

- Runtime detection (Falco, Tracee) catches active exploits
- CIS Benchmark via kube-bench is the hardening baseline
- API server, kubelet, etcd, network: harden each
- Audit logs + alerting + IR plan complete the picture
- Test backups, exercise IR, automate everything
