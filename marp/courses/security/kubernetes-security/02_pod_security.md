---
tags:
  - security:kubernetes
  - concepts:pods
level: intermediate
category: security
audience:
  - audiences:devops

---
# Pod Security Standards

---
## What This Chapter Covers

- The three Pod Security Standards
- securityContext fields
- Capabilities, seccomp, AppArmor
- Privileged containers and their risks
- PSS versus the deprecated PSP

---
## What Are Pod Security Standards?

- Built-in policy levels for pod security
- Replaces the deprecated PodSecurityPolicy (PSP)
- Three levels: Privileged, Baseline, Restricted
- Applied per-namespace via labels
- Enforced by the Pod Security Admission controller

---
## Three Levels Visualized

![pss_levels](svg/courses/security/kubernetes-security/02_pod_security/pss_levels.svg)

---
## Capabilities and Hardening

![capabilities_overview](svg/courses/security/kubernetes-security/02_pod_security/capabilities_overview.svg)

---
## Privileged

- Anything goes
- Use only for system pods (network plugins, storage)
- Never for application workloads
- Effectively no security baseline
- Reserve for trusted infrastructure

---
## Baseline

- Prevents the worst-case privileges
- Disallows hostNetwork, hostPID, hostIPC
- Disallows privileged containers
- Limits hostPath mounts
- Reasonable default for most workloads

---
## Restricted

- The strictest tier
- Requires non-root users
- Read-only root filesystem
- Drop all capabilities; only add what's needed
- Apply seccomp RuntimeDefault profile
- Production target

---
## Enforcing PSS

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: prod
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

- Three modes per level: enforce, audit, warn
- Mix levels for graceful migration

---
## Modes Explained

- enforce — block non-compliant pods
- audit — record violations in audit log
- warn — show warnings to users
- Use audit/warn before flipping enforce
- Migrate gradually, namespace by namespace

---
## securityContext Basics

```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
  containers:
    - name: app
      securityContext:
        readOnlyRootFilesystem: true
        allowPrivilegeEscalation: false
```

---
## Pod-Level vs Container-Level

- Pod-level: applies to all containers
- Container-level: overrides for one container
- Container-level wins on conflict
- Set defaults at pod, exceptions at container
- Easier to audit consistent policies

---
## Key Fields

![security_context_fields](svg/courses/security/kubernetes-security/02_pod_security/security_context_fields.svg)

---
## Running as Non-Root

- runAsNonRoot: true rejects images that try to run as root
- runAsUser: 1000 forces a specific UID
- Many images run as root by default
- Fix in the Dockerfile: USER 1000
- Required by Restricted level

---
## Read-Only Root Filesystem

- readOnlyRootFilesystem: true
- Prevents writes to the container's filesystem
- Blocks many in-container exploits
- Use emptyDir volumes for genuinely needed writes
- Strong defense for stateless apps

---
## Privilege Escalation

- allowPrivilegeEscalation: false
- Blocks setuid binaries from gaining new privileges
- Should be the default for all workloads
- Required by Restricted
- Cheap to set; high security value

---
## Capabilities

- Linux capabilities split root's powers into pieces
- NET_ADMIN, SYS_ADMIN, etc
- By default, containers get a subset
- Drop all, add only what's needed
- Many apps need none

---
## Capabilities Example

```yaml
securityContext:
  capabilities:
    drop: ["ALL"]
    add: ["NET_BIND_SERVICE"]
```

- Most apps don't need any
- NET_BIND_SERVICE for binding ports < 1024
- SYS_PTRACE only for debuggers
- Audit your image for what it actually uses

---
## Seccomp

- Filters which syscalls a container can make
- RuntimeDefault profile blocks the most dangerous
- Custom profiles for tighter restriction
- seccompProfile.type: RuntimeDefault is the safe default
- Required by Restricted

---
## Seccomp Example

```yaml
securityContext:
  seccompProfile:
    type: RuntimeDefault
```

- Most workloads work with RuntimeDefault
- For very strict workloads: write a custom profile
- Tools like falco or strace help craft profiles

---
## AppArmor

- Mandatory access control via Linux LSM
- Restrict file access, network, capabilities per profile
- Profiles loaded on the node
- Annotation-based assignment
- Less common than seccomp; powerful when used

---
## SELinux

- Alternative to AppArmor on RHEL-family systems
- Multi-level security, type enforcement
- Can be set in securityContext
- More complex; valuable in regulated environments
- Mutually exclusive with AppArmor on the same host

---
## Privileged Containers

- privileged: true → host-level access
- Effectively, root on the node
- Necessary for some system-level tools
- Never for application workloads
- Audit cluster for any privileged: true

---
## hostPID, hostIPC, hostNetwork

- hostPID: see all processes on the node
- hostIPC: share IPC namespace with host
- hostNetwork: bind to host's network
- Each is a privilege boundary breach
- Only for system pods; never for apps

---
## hostPath Mounts

- Mount any directory from the node
- Read /etc/shadow, /var/lib/docker, anything
- Frequently abused for persistence in attacks
- Restricted level forbids it
- Use PVCs or specific volume types instead

---
## Resource Limits

- Not strictly security, but related
- A pod without limits can DoS the node
- Set requests and limits on CPU/memory
- Use LimitRange to enforce defaults
- Prevent fork bombs and resource exhaustion

---
## Migrating from PSP

- PSP removed in Kubernetes 1.25
- Migration: enable PSS, run audit mode
- Compare violations against existing PSP allowances
- Adjust labels per namespace
- Tools: psp-migration-helper

---
## Auditing PSS Violations

- audit mode logs violations to audit log
- Tools (kubectl audit, K8s Audit) parse them
- Track non-compliant pods over time
- Drive remediation systematically
- Dashboard the trend

---
## Common Pitfalls

- Setting Restricted on existing namespaces — breaks workloads
- Forgetting to update CI/CD images for non-root
- Using privileged: true "just for the demo"
- Mixing PSS levels inconsistently
- Not auditing before enforcing

---
## Best Practices

- Default to Restricted in new namespaces
- Audit existing namespaces; then warn; then enforce
- Set securityContext explicitly on every pod
- Treat privileged: true as a security incident
- Use kube-bench to validate

---
## Summary

- Pod Security Standards: Privileged, Baseline, Restricted
- Per-namespace labels enable enforcement
- securityContext is the per-pod knobs
- Drop capabilities, run as non-root, read-only root
- Audit before enforce; migrate gracefully
