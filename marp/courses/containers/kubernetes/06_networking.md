---
tags:
  - infrastructure:kubernetes
  - networking:k8s
level: intermediate
category: containers
audience:
  - audiences:developers

---
# Networking

---
## What This Chapter Covers

- Pod networking model
- CNI plugins
- NetworkPolicy
- Service mesh briefly
- DNS
- Common patterns

---
## Pod Networking Model

- Every pod has its own IP
- Pods can reach pods directly (no NAT inside cluster)
- Pod IPs are routable in the cluster
- Containers within a pod share a network namespace

---
## Network Layers

![cluster_network](svg/courses/containers/kubernetes/06_networking/cluster_network.svg)

---
## CNI Plugins

- Calico, Flannel, Weave, Cilium
- Implement the pod networking model
- Each: trade-offs in performance, features
- Pick at cluster install

---
## Cilium

- eBPF-based; modern
- Fast; rich observability
- NetworkPolicy + service mesh
- Increasing adoption

---
## NetworkPolicy

- Firewall rules within the cluster
- Default: all pods can talk to all
- Apply policies to restrict
- Requires CNI that enforces (Calico, Cilium)

---
## Sample NetworkPolicy

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-access
spec:
  podSelector:
    matchLabels:
      app: db
  policyTypes: [Ingress]
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: api
```

---
## Default-Deny

- Block all by default; allow specific
- "Zero trust" within the cluster
- More secure
- More configuration

---
## DNS

- CoreDNS in every cluster
- Service DNS: `<service>.<ns>.svc.cluster.local`
- Pod DNS optional
- Forwards external queries upstream

---
## DNS Caching

- Pods can have NodeLocal DNSCache
- Reduces CoreDNS load
- Faster resolution
- Recommended at scale

---
## Service Mesh

- Adds: mTLS, traffic management, observability
- Tools: Istio, Linkerd, Consul Connect
- Cilium with Cilium Service Mesh
- Heavy; adopt only if needed

---
## Service Mesh Use Cases

- Encrypted service-to-service (mTLS)
- Canary deploys with traffic splitting
- Detailed per-call metrics / tracing
- Most teams: skip for years

---
## External Traffic

- LoadBalancer: cloud LB
- Ingress: HTTP routing (next chapter)
- Gateway API: newer alternative

---
## Egress

- Pods to external internet: allowed by default
- Restrict with NetworkPolicy egress rules
- For compliance: required

---
## DNS Policies On Pods

- ClusterFirst (default): cluster DNS first
- Default: node's DNS
- None: don't set
- Custom resolv.conf

---
## Common Networking Mistakes

- No NetworkPolicies (everything talks to everything)
- Default-allow leaving pods exposed
- Service mesh overkill for small clusters
- Hard-coded pod IPs (they change)
- DNS performance not monitored
