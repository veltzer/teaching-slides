---
tags:
  - infrastructure:kubernetes
level: intermediate
category: containers
audience:
  - audiences:developers

---
# Services and Service Discovery

---
## What This Chapter Covers

- What a Service is
- Service types
- DNS in K8s
- Endpoint slices
- Headless services
- External services

---
## Why Services

- Pods are ephemeral; IPs change
- A Service: stable endpoint
- Load-balances across pod replicas
- The way to reach pods

---
## ClusterIP

- Default
- Stable cluster-internal IP and DNS
- Not accessible from outside
- For: service-to-service

---
## Sample Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web
spec:
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 8080
```

---
## NodePort

- Opens a port on every node
- Accessible from outside cluster
- Range 30000-32767
- Rarely used directly in production

---
## LoadBalancer

- Cloud-provisioned LB
- Public IP / DNS
- Bill: per LB hour
- Standard for exposing services in cloud

---
## ExternalName

- DNS alias for an external service
- "my-svc &#8594; db.example.com"
- No proxy; just DNS
- For: bringing external services into cluster naming

---
## DNS

- Every service has a DNS name
- `<service>.<namespace>.svc.cluster.local`
- Short forms work in same namespace
- CoreDNS provides; configurable

---
## Pod-To-Service

- Pod queries DNS for service name
- Gets ClusterIP
- kube-proxy routes to a backing pod
- Round-robin by default

---
## Endpoint Slices

- Modern replacement for Endpoints
- Lists pods backing a service
- Better scalability
- Used by kube-proxy

---
## Headless Service

```yaml
spec:
  clusterIP: None
```

- No load balancing
- DNS returns all pod IPs
- For: clients that want their own LB / sharding
- Used by StatefulSets

---
## Session Affinity

- Send same client to same pod
- ClientIP-based
- "Sticky sessions"
- Disable when stateless

---
## kube-proxy Modes

- iptables (default): per-rule routing
- IPVS: better for many services
- eBPF (Cilium): newer, faster

---
## External Connections

- LoadBalancer: cloud LB
- NodePort: open port on every node
- Ingress: HTTP routing (next chapter)
- Pick by use case

---
## Common Service Mistakes

- LoadBalancer per service (cost)
- Wrong selector labels (no endpoints)
- ClusterIP service expected from outside
- Headless when ClusterIP would do
- Sticky sessions with stateless apps (defeats load balancing)
