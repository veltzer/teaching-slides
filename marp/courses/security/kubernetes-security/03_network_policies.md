---
tags:
  - security:kubernetes
  - concepts:network-policy
level: intermediate
category: security
audience:
  - audiences:devops

---
# Network Policies

---
## What This Chapter Covers

- The default permissive network model
- NetworkPolicy resource basics
- Ingress and egress rules
- Selectors: pod, namespace, IP block
- CNI requirements and tools

---
## Default Network Behavior

- Every pod can talk to every other pod
- Cross-namespace communication is allowed by default
- Outbound traffic to anywhere on the internet
- This is the explicit Kubernetes design
- Lateral movement after one compromise is trivial

---
## Why It Matters

![policy_intent](svg/courses/security/kubernetes-security/03_network_policies/policy_intent.svg)

---
## Why NetworkPolicies Matter

- Limit east-west traffic (pod-to-pod)
- Limit egress (outbound to the internet)
- Defense in depth — even if a pod is compromised
- Required by most compliance frameworks
- Implementing them is mandatory in 2026

---
## Network Topology Visualized

![network_default](svg/courses/security/kubernetes-security/03_network_policies/network_default.svg)

---
## NetworkPolicy Resource

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
  namespace: prod
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
```

- Empty podSelector matches all pods in the namespace
- No ingress or egress rules = deny all

---
## Default Deny Everything

- Apply a default-deny in every namespace
- Then add explicit allow rules
- "Whitelist" approach
- Cleanest security posture
- More work but worth it

---
## Allowing Specific Ingress

```yaml
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes: [Ingress]
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: web
      ports:
        - protocol: TCP
          port: 8080
```

---
## Allowing Specific Egress

```yaml
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes: [Egress]
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: db
      ports:
        - protocol: TCP
          port: 5432
```

---
## Selectors

- podSelector — match by labels in same namespace
- namespaceSelector — match by namespace labels
- ipBlock — IP CIDR allowlist
- Combine: pods in namespace X with label Y
- Cross-namespace: namespaceSelector + podSelector

---
## Cross-Namespace Example

```yaml
ingress:
  - from:
      - namespaceSelector:
          matchLabels:
            tier: web
        podSelector:
          matchLabels:
            app: frontend
```

- Pods labeled `app: frontend` in any namespace labeled `tier: web`

---
## DNS Egress

- Pods need DNS to function
- Without DNS allowed, name resolution breaks
- Allow egress to kube-system DNS pods on UDP 53
- Easy to forget; common cause of "policies broke us"

---
## DNS Egress Rule

```yaml
egress:
  - to:
      - namespaceSelector:
          matchLabels:
            kubernetes.io/metadata.name: kube-system
      - podSelector:
          matchLabels:
            k8s-app: kube-dns
    ports:
      - protocol: UDP
        port: 53
```

---
## Egress to Outside Cluster

- ipBlock for external endpoints
- Allow specific CIDRs (e.g., your DB at 10.20.30.0/24)
- Combined with except clauses for sub-ranges
- Useful for restricting where workloads can connect

---
## ipBlock Example

```yaml
egress:
  - to:
      - ipBlock:
          cidr: 0.0.0.0/0
          except:
            - 169.254.169.254/32  # cloud metadata
            - 10.0.0.0/8           # private internal
```

- Allow internet but block sensitive endpoints

---
## CNI Requirement

- NetworkPolicy is a spec; CNI plugins implement it
- Calico, Cilium, Antrea, Weave: full support
- Flannel: no native support (needs extra)
- Some older CNIs ignore policies silently
- Verify your CNI implements policies

---
## Calico

- Most-used CNI for NetworkPolicy
- Supports standard Kubernetes policies + Calico extensions
- Global policies, deny-all rules, advanced selectors
- Felix and Typha for performance at scale

---
## Cilium

- eBPF-based; high performance
- Layer 7 policies (HTTP, gRPC, Kafka)
- Hubble for observability
- Increasingly popular for new deployments
- Identity-based rather than IP-based

---
## Layer 7 Policies (Cilium)

- Allow only specific HTTP paths/methods
- Filter Kafka topics
- Scope DNS lookups by name
- Beyond standard NetworkPolicy capabilities
- Trade-off: CNI lock-in but powerful

---
## Testing Policies

- Pre-deploy with `kubectl apply --dry-run`
- Verify with test pods (`netshoot`, `nicolaka`)
- Tools: `np-viewer`, `cilium connectivity test`
- Test ingress and egress paths
- Negative tests: confirm bad paths are blocked

---
## Default Deny Workflow

- Apply default-deny per namespace
- Test workloads — many will break
- Add allow rules per service-to-service connection
- Document each allowed flow
- Iterate and tighten

---
## Policy Visualization

- Tools to render the active policy graph
- Otterize, np-guard, netpol viewers
- Helps audits and onboarding
- Spot unintended cross-namespace flows
- Run periodically

---
## Common Pitfalls

- Forgetting DNS egress
- Default-deny applied without testing — outage
- Selectors that match the wrong pods (test labels)
- Policies in CNI that doesn't enforce them
- Overlap and conflicts between policies

---
## Multi-Cluster Considerations

- NetworkPolicy is per-cluster
- Cross-cluster requires service mesh or CNI features
- Cilium ClusterMesh, Istio, Submariner
- Don't assume policies extend across clusters
- Plan boundaries explicitly

---
## Audit and Monitoring

- Cilium Hubble: flow logs in real time
- Calico Enterprise: similar
- Falco can detect anomalies
- VPC flow logs at the cloud layer for L3/L4
- Layer multiple sources for full picture

---
## Best Practices

- Default-deny in every namespace
- Allow each connection explicitly
- Test policies in audit mode first
- Document policies alongside service definitions
- Re-validate after every architecture change

---
## Summary

- Default Kubernetes networking is permissive — change it
- Default-deny + explicit allow is the goal
- Selectors (pod, namespace, IP) build precise rules
- DNS egress is easy to forget
- CNI must implement policies; verify your choice
