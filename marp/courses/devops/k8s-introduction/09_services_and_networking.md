---
tags:
  - tools:kubernetes
  - infrastructure:containers
  - infrastructure:orchestration
  - practices:devops
  - tools:docker
level: beginner
category: devops
audience:
  - audiences:developers
  - audiences:devops
  - audiences:sysadmins

---

# Services and Networking

---

## Networking Layers

![k8s_networking](svg/courses/devops/k8s-introduction/09_services_and_networking/k8s_networking.svg)

---

## Kubernetes Networking Model

1. **Every Pod** gets unique IP
1. **Pods communicate** without NAT
1. **Nodes communicate** with Pods without NAT
1. **Pod sees** its own IP
1. **Flat network** space

---

## Network Requirements

![network_requirements](svg/courses/devops/k8s-introduction/09_services_and_networking/network_requirements.svg)

---

## Service Overview

1. **Stable** network endpoint
1. **Load balances** to Pods
1. **Service discovery** via DNS
1. **Decouples** consumers from Pods
1. **Virtual IP** (ClusterIP)

---

## Why Services?

![why_services](svg/courses/devops/k8s-introduction/09_services_and_networking/why_services.svg)

---

## Service Types

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: ClusterIP  # Default
  # type: NodePort
  # type: LoadBalancer
  # type: ExternalName
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
```

---

## Service Types Overview

![service_types](svg/courses/devops/k8s-introduction/09_services_and_networking/service_types.svg)

---

## ClusterIP Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  type: ClusterIP  # Default, can be omitted
  selector:
    app: backend
  ports:
  - port: 80        # Service port
    targetPort: 8080 # Container port
    protocol: TCP
```

---

## ClusterIP Characteristics

![clusterip_characteristics](svg/courses/devops/k8s-introduction/09_services_and_networking/clusterip_characteristics.svg)

---

## NodePort Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  type: NodePort
  selector:
    app: frontend
  ports:
  - port: 80         # Service port
    targetPort: 8080  # Container port
    nodePort: 30080   # Node port (30000-32767)
    protocol: TCP
```

---

## NodePort Access

![nodeport_access](svg/courses/devops/k8s-introduction/09_services_and_networking/nodeport_access.svg)

---

## LoadBalancer Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  type: LoadBalancer
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
  # Cloud provider assigns external IP
```

---

## LoadBalancer Architecture

![loadbalancer_architecture](svg/courses/devops/k8s-introduction/09_services_and_networking/loadbalancer_architecture.svg)

---

## ExternalName Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: external-db
spec:
  type: ExternalName
  externalName: database.example.com
  # No selector needed
  # Returns CNAME record
```

---

## Service Discovery

1. **Environment Variables**: Injected into Pods
1. **DNS**: Cluster DNS (CoreDNS)
1. **Headless Services**: Direct Pod IPs
1. **Service Mesh**: Advanced discovery

---

## DNS in Kubernetes

```bash
# Service DNS format
<service-name>.<namespace>.svc.cluster.local

# Examples:
backend.default.svc.cluster.local
database.production.svc.cluster.local

# Short names within namespace
backend
database

# Pod DNS (if enabled)
<pod-ip>.<namespace>.pod.cluster.local
10-244-1-5.default.pod.cluster.local
```

---

## Headless Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: headless-service
spec:
  clusterIP: None  # Headless
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
# Returns Pod IPs directly via DNS
```

---

## Endpoints

```yaml
apiVersion: v1
kind: Endpoints
metadata:
  name: my-service  # Must match Service name
subsets:
- addresses:
  - ip: 10.1.1.1
  - ip: 10.1.1.2
  ports:
  - port: 8080

# Manually managed endpoints
# Useful for external services
```

---

## Service Without Selector

```yaml
apiVersion: v1
kind: Service
metadata:
  name: external-service
spec:
  # No selector - manually manage endpoints
  ports:
  - port: 80
    targetPort: 8080

---
apiVersion: v1
kind: Endpoints
metadata:
  name: external-service
subsets:
- addresses:
  - ip: 192.168.1.100  # External IP
  ports:
  - port: 8080
```

---

## Session Affinity

```yaml
apiVersion: v1
kind: Service
metadata:
  name: sticky-service
spec:
  selector:
    app: myapp
  sessionAffinity: ClientIP  # Sticky sessions
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800  # 3 hours
  ports:
  - port: 80
    targetPort: 8080
```

---

## Multi-Port Services

```yaml
apiVersion: v1
kind: Service
metadata:
  name: multi-port-service
spec:
  selector:
    app: myapp
  ports:
  - name: http
    port: 80
    targetPort: 8080
  - name: https
    port: 443
    targetPort: 8443
  - name: metrics
    port: 9090
    targetPort: 9090
```

---

## Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: web-netpol
spec:
  podSelector:
    matchLabels:
      app: web
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
```

---

## Network Policy Types

![network_policy_types](svg/courses/devops/k8s-introduction/09_services_and_networking/network_policy_types.svg)

---

## Deny All Network Policy

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
  namespace: production
spec:
  podSelector: {}  # All pods in namespace
  policyTypes:
  - Ingress
  - Egress
  # No rules = deny all
```

---

## Allow Specific Traffic

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-policy
spec:
  podSelector:
    matchLabels:
      tier: backend
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: frontend
    - podSelector:
        matchLabels:
          tier: frontend
    ports:
    - protocol: TCP
      port: 8080
```

---

## Service Mesh Overview

![service_mesh_overview](svg/courses/devops/k8s-introduction/09_services_and_networking/service_mesh_overview.svg)

---

## kube-proxy Modes

1. **userspace**: Oldest, slowest
1. **iptables**: Default, good performance
1. **ipvs**: Best performance, advanced LB

```bash
# Check kube-proxy mode
kubectl get configmap kube-proxy -n kube-system -o yaml | grep mode
```

---

## Service Debugging

```bash
# Check service
kubectl get svc my-service
kubectl describe svc my-service

# Check endpoints
kubectl get endpoints my-service

# Test DNS
kubectl run test --image=busybox --rm -it -- nslookup my-service

# Test connectivity
kubectl run test --image=nicolaka/netshoot --rm -it -- curl my-service
```

---

## Port Forwarding

```bash
# Forward local port to service
kubectl port-forward service/my-service 8080:80

# Forward to pod
kubectl port-forward pod/my-pod 8080:80

# Forward multiple ports
kubectl port-forward service/my-service 8080:80 8443:443

# Bind to all interfaces
kubectl port-forward --address 0.0.0.0 service/my-service 8080:80
```

---

## Service Load Balancing

![service_load_balancing](svg/courses/devops/k8s-introduction/09_services_and_networking/service_load_balancing.svg)

---

## CoreDNS Configuration

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        kubernetes cluster.local in-addr.arpa ip6.arpa {
          pods insecure
          fallthrough in-addr.arpa ip6.arpa
        }
        forward . /etc/resolv.conf
        cache 30
        loop
        reload
    }
```

---

## Custom DNS

```yaml
apiVersion: v1
kind: Pod
spec:
  dnsPolicy: "None"  # Custom DNS
  dnsConfig:
    nameservers:
    - 8.8.8.8
    - 8.8.4.4
    searches:
    - ns1.svc.cluster.local
    - my.dns.search.suffix
    options:
    - name: ndots
      value: "5"
```

---

## Service Monitoring

```bash
# Service metrics
kubectl top pods -l app=myapp

# Check service endpoints
kubectl get endpoints my-service -o wide

# Watch endpoint changes
kubectl get endpoints my-service --watch

# Service events
kubectl get events --field-selector involvedObject.name=my-service
```

---

## Troubleshooting Services

1. **No endpoints**: Check selector labels
1. **Connection refused**: Check target port
1. **DNS not working**: Check CoreDNS
1. **Intermittent failures**: Check pod health
1. **Wrong port**: Verify port mappings

---

## Service Best Practices

1. **Use** appropriate service type
1. **Label** pods consistently
1. **Set** resource limits on pods
1. **Monitor** endpoint health
1. **Document** port mappings

---

## Common Service Patterns

```yaml
# Internal microservice
apiVersion: v1
kind: Service
metadata:
  name: internal-api
spec:
  type: ClusterIP
  selector:
    app: api
  ports:
  - port: 80
    targetPort: 8080

---
# Public facing service
apiVersion: v1
kind: Service
metadata:
  name: public-web
spec:
  type: LoadBalancer
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 8080
```

---

## Service Security

1. **Network Policies**: Control traffic flow
1. **TLS termination**: At ingress/service mesh
1. **Service accounts**: For pod identity
1. **RBAC**: Control service access
1. **Encryption**: Service mesh mTLS

---

## Summary

1. Services provide stable networking
1. Multiple service types for different needs
1. DNS enables service discovery
1. Network policies control traffic
1. Service mesh adds advanced features
