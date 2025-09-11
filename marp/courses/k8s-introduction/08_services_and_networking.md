# Services and Networking

---

## Kubernetes Networking Model

1. **Every Pod** gets unique IP
1. **Pods communicate** without NAT
1. **Nodes communicate** with Pods without NAT
1. **Pod sees** its own IP
1. **Flat network** space

---

## Network Requirements

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Kubernetes Network Model</text>
  <rect x="100" y="80" width="200" height="100" fill="#4285f4" rx="5"/>
  <text x="200" y="110" text-anchor="middle" fill="white" font-weight="bold">Container to Container</text>
  <text x="200" y="135" text-anchor="middle" fill="white" font-size="11">Same Pod</text>
  <text x="200" y="155" text-anchor="middle" fill="white" font-size="11">localhost communication</text>
  <text x="200" y="175" text-anchor="middle" fill="white" font-size="11">Shared network namespace</text>
  <rect x="320" y="80" width="200" height="100" fill="#34a853" rx="5"/>
  <text x="420" y="110" text-anchor="middle" fill="white" font-weight="bold">Pod to Pod</text>
  <text x="420" y="135" text-anchor="middle" fill="white" font-size="11">Direct IP communication</text>
  <text x="420" y="155" text-anchor="middle" fill="white" font-size="11">No NAT required</text>
  <text x="420" y="175" text-anchor="middle" fill="white" font-size="11">Across nodes</text>
  <rect x="540" y="80" width="200" height="100" fill="#fbbc04" rx="5"/>
  <text x="640" y="110" text-anchor="middle" font-weight="bold">Pod to Service</text>
  <text x="640" y="135" text-anchor="middle" font-size="11">Virtual IP (ClusterIP)</text>
  <text x="640" y="155" text-anchor="middle" font-size="11">Load balancing</text>
  <text x="640" y="175" text-anchor="middle" font-size="11">Service discovery</text>
  <rect x="250" y="220" width="300" height="80" fill="#e8f5e9" rx="5"/>
  <text x="400" y="250" text-anchor="middle" font-weight="bold">External to Service</text>
  <text x="400" y="275" text-anchor="middle" font-size="12">NodePort, LoadBalancer, Ingress</text>
</svg>

---

## Service Overview

1. **Stable** network endpoint
1. **Load balances** to Pods
1. **Service discovery** via DNS
1. **Decouples** consumers from Pods
1. **Virtual IP** (ClusterIP)

---

## Why Services?

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="30" text-anchor="middle" font-size="16" font-weight="bold">Problem: Pod IPs are Ephemeral</text>
  <g id="without-service">
    <text x="200" y="70" text-anchor="middle" font-size="12">Without Service</text>
    <rect x="100" y="90" width="100" height="40" fill="#888" rx="3"/>
    <text x="150" y="115" text-anchor="middle" fill="white">Client</text>
    <circle cx="150" cy="200" r="25" fill="#ea4335"/>
    <text x="150" y="205" text-anchor="middle" fill="white" font-size="10">Pod</text>
    <text x="150" y="235" text-anchor="middle" font-size="10">10.1.1.5 ❌</text>
    <circle cx="230" cy="200" r="25" fill="#34a853"/>
    <text x="230" y="205" text-anchor="middle" fill="white" font-size="10">Pod</text>
    <text x="230" y="235" text-anchor="middle" font-size="10">10.1.1.6 ✓</text>
    <path d="M 150 130 L 150 175" stroke="#666" stroke-width="2" stroke-dasharray="5,5"/>
    <text x="150" y="280" text-anchor="middle" font-size="11">Direct connection fails</text>
  </g>
  <g id="with-service">
    <text x="600" y="70" text-anchor="middle" font-size="12">With Service</text>
    <rect x="500" y="90" width="100" height="40" fill="#888" rx="3"/>
    <text x="550" y="115" text-anchor="middle" fill="white">Client</text>
    <rect x="480" y="160" width="140" height="40" fill="#4285f4" rx="3"/>
    <text x="550" y="185" text-anchor="middle" fill="white">Service</text>
    <circle cx="500" cy="260" r="25" fill="#ea4335"/>
    <text x="500" y="265" text-anchor="middle" fill="white" font-size="10">Pod</text>
    <text x="500" y="295" text-anchor="middle" font-size="10">10.1.2.5 ❌</text>
    <circle cx="600" cy="260" r="25" fill="#34a853"/>
    <text x="600" y="265" text-anchor="middle" fill="white" font-size="10">Pod</text>
    <text x="600" y="295" text-anchor="middle" font-size="10">10.1.2.7 ✓</text>
    <path d="M 550 130 L 550 160" stroke="#666" stroke-width="2"/>
    <path d="M 550 200 L 600 235" stroke="#666" stroke-width="2"/>
    <text x="550" y="330" text-anchor="middle" font-size="11">Service handles routing</text>
  </g>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f9f9f9" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">ClusterIP Service</text>
  <rect x="200" y="100" width="400" height="60" fill="#4285f4" rx="5"/>
  <text x="400" y="125" text-anchor="middle" fill="white" font-weight="bold">ClusterIP: 10.96.10.20</text>
  <text x="400" y="145" text-anchor="middle" fill="white" font-size="12">Internal only - No external access</text>
  <circle cx="250" cy="230" r="30" fill="#34a853"/>
  <text x="250" y="235" text-anchor="middle" fill="white">Pod 1</text>
  <circle cx="400" cy="230" r="30" fill="#34a853"/>
  <text x="400" y="235" text-anchor="middle" fill="white">Pod 2</text>
  <circle cx="550" cy="230" r="30" fill="#34a853"/>
  <text x="550" y="235" text-anchor="middle" fill="white">Pod 3</text>
  <path d="M 300 160 L 250 200" stroke="#666" stroke-width="2"/>
  <path d="M 400 160 L 400 200" stroke="#666" stroke-width="2"/>
  <path d="M 500 160 L 550 200" stroke="#666" stroke-width="2"/>
  <rect x="100" y="100" width="80" height="60" fill="#888" rx="5"/>
  <text x="140" y="135" text-anchor="middle" fill="white" font-size="11">Other Pods</text>
  <path d="M 180 130 L 195 130" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">NodePort Service</text>
  <rect x="100" y="80" width="150" height="60" fill="#888" rx="5"/>
  <text x="175" y="110" text-anchor="middle" fill="white">External Client</text>
  <text x="175" y="125" text-anchor="middle" fill="white" font-size="10">192.168.1.100</text>
  <rect x="320" y="80" width="180" height="60" fill="#4285f4" rx="5"/>
  <text x="410" y="105" text-anchor="middle" fill="white">Node 1</text>
  <text x="410" y="125" text-anchor="middle" fill="white" font-size="11">10.0.0.1:30080</text>
  <rect x="520" y="80" width="180" height="60" fill="#4285f4" rx="5"/>
  <text x="610" y="105" text-anchor="middle" fill="white">Node 2</text>
  <text x="610" y="125" text-anchor="middle" fill="white" font-size="11">10.0.0.2:30080</text>
  <rect x="320" y="180" width="380" height="50" fill="#34a853" rx="5"/>
  <text x="510" y="210" text-anchor="middle" fill="white">Service (ClusterIP: 10.96.10.20:80)</text>
  <circle cx="370" cy="280" r="25" fill="#fbbc04"/>
  <text x="370" y="285" text-anchor="middle">Pod</text>
  <circle cx="460" cy="280" r="25" fill="#fbbc04"/>
  <text x="460" y="285" text-anchor="middle">Pod</text>
  <circle cx="550" cy="280" r="25" fill="#fbbc04"/>
  <text x="550" y="285" text-anchor="middle">Pod</text>
  <circle cx="640" cy="280" r="25" fill="#fbbc04"/>
  <text x="640" y="285" text-anchor="middle">Pod</text>
  <path d="M 250 110 L 315 110" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 250 110 L 515 110" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 410 140 L 410 175" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 610 140 L 510 175" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f9f9f9" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">LoadBalancer Service</text>
  <rect x="300" y="70" width="200" height="50" fill="#ea4335" rx="5"/>
  <text x="400" y="95" text-anchor="middle" fill="white" font-weight="bold">Cloud Load Balancer</text>
  <text x="400" y="110" text-anchor="middle" fill="white" font-size="10">External IP: 35.1.2.3</text>
  <rect x="150" y="150" width="120" height="50" fill="#4285f4" rx="5"/>
  <text x="210" y="180" text-anchor="middle" fill="white" font-size="11">Node 1</text>
  <rect x="340" y="150" width="120" height="50" fill="#4285f4" rx="5"/>
  <text x="400" y="180" text-anchor="middle" fill="white" font-size="11">Node 2</text>
  <rect x="530" y="150" width="120" height="50" fill="#4285f4" rx="5"/>
  <text x="590" y="180" text-anchor="middle" fill="white" font-size="11">Node 3</text>
  <rect x="200" y="230" width="400" height="40" fill="#34a853" rx="5"/>
  <text x="400" y="255" text-anchor="middle" fill="white">Service + NodePort</text>
  <circle cx="250" cy="310" r="20" fill="#fbbc04"/>
  <circle cx="350" cy="310" r="20" fill="#fbbc04"/>
  <circle cx="450" cy="310" r="20" fill="#fbbc04"/>
  <circle cx="550" cy="310" r="20" fill="#fbbc04"/>
  <path d="M 400 120 L 210 145" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 400 120 L 400 145" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 400 120 L 590 145" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Network Policy Rules</text>
  <rect x="100" y="80" width="200" height="120" fill="#4285f4" rx="5"/>
  <text x="200" y="110" text-anchor="middle" fill="white" font-weight="bold">Ingress Rules</text>
  <text x="200" y="135" text-anchor="middle" fill="white" font-size="11">Control incoming traffic</text>
  <text x="200" y="155" text-anchor="middle" fill="white" font-size="11">• From pods</text>
  <text x="200" y="175" text-anchor="middle" fill="white" font-size="11">• From namespaces</text>
  <text x="200" y="195" text-anchor="middle" fill="white" font-size="11">• From IP blocks</text>
  <rect x="320" y="80" width="200" height="120" fill="#34a853" rx="5"/>
  <text x="420" y="110" text-anchor="middle" fill="white" font-weight="bold">Egress Rules</text>
  <text x="420" y="135" text-anchor="middle" fill="white" font-size="11">Control outgoing traffic</text>
  <text x="420" y="155" text-anchor="middle" fill="white" font-size="11">• To pods</text>
  <text x="420" y="175" text-anchor="middle" fill="white" font-size="11">• To namespaces</text>
  <text x="420" y="195" text-anchor="middle" fill="white" font-size="11">• To IP blocks</text>
  <rect x="540" y="80" width="200" height="120" fill="#fbbc04" rx="5"/>
  <text x="640" y="110" text-anchor="middle" font-weight="bold">Default Behavior</text>
  <text x="640" y="135" text-anchor="middle" font-size="11">No policy = Allow all</text>
  <text x="640" y="155" text-anchor="middle" font-size="11">With policy:</text>
  <text x="640" y="175" text-anchor="middle" font-size="11">• Whitelist mode</text>
  <text x="640" y="195" text-anchor="middle" font-size="11">• Explicit allow only</text>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f9f9f9" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Service Mesh Architecture</text>
  <rect x="100" y="80" width="150" height="100" fill="#4285f4" rx="5"/>
  <text x="175" y="110" text-anchor="middle" fill="white" font-weight="bold">App Container</text>
  <rect x="100" y="190" width="150" height="60" fill="#34a853" rx="5"/>
  <text x="175" y="225" text-anchor="middle" fill="white">Sidecar Proxy</text>
  <rect x="300" y="80" width="150" height="100" fill="#4285f4" rx="5"/>
  <text x="375" y="110" text-anchor="middle" fill="white" font-weight="bold">App Container</text>
  <rect x="300" y="190" width="150" height="60" fill="#34a853" rx="5"/>
  <text x="375" y="225" text-anchor="middle" fill="white">Sidecar Proxy</text>
  <rect x="500" y="80" width="150" height="100" fill="#4285f4" rx="5"/>
  <text x="575" y="110" text-anchor="middle" fill="white" font-weight="bold">App Container</text>
  <rect x="500" y="190" width="150" height="60" fill="#34a853" rx="5"/>
  <text x="575" y="225" text-anchor="middle" fill="white">Sidecar Proxy</text>
  <path d="M 250 220 L 295 220" stroke="#666" stroke-width="2" stroke-dasharray="5,5"/>
  <path d="M 450 220 L 495 220" stroke="#666" stroke-width="2" stroke-dasharray="5,5"/>
  <rect x="250" y="280" width="300" height="50" fill="#ea4335" rx="5"/>
  <text x="400" y="310" text-anchor="middle" fill="white">Control Plane (Istio, Linkerd)</text>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="30" text-anchor="middle" font-size="16" font-weight="bold">Load Balancing Algorithms</text>
  <rect x="100" y="60" width="600" height="80" fill="#4285f4" rx="5"/>
  <text x="400" y="90" text-anchor="middle" fill="white" font-weight="bold">Service: my-app</text>
  <text x="400" y="115" text-anchor="middle" fill="white">ClusterIP: 10.96.10.20</text>
  <g id="rr">
    <text x="200" y="170" text-anchor="middle" font-weight="bold">Round Robin (Default)</text>
    <circle cx="150" cy="220" r="25" fill="#34a853"/>
    <text x="150" y="225" text-anchor="middle" fill="white">Pod 1</text>
    <circle cx="200" cy="220" r="25" fill="#34a853"/>
    <text x="200" y="225" text-anchor="middle" fill="white">Pod 2</text>
    <circle cx="250" cy="220" r="25" fill="#34a853"/>
    <text x="250" y="225" text-anchor="middle" fill="white">Pod 3</text>
    <path d="M 200 140 L 150 195" stroke="#666" stroke-width="2"/>
    <path d="M 200 140 L 200 195" stroke="#666" stroke-width="2"/>
    <path d="M 200 140 L 250 195" stroke="#666" stroke-width="2"/>
    <text x="200" y="270" text-anchor="middle" font-size="11">1→2→3→1→2→3...</text>
  </g>
  <g id="session">
    <text x="550" y="170" text-anchor="middle" font-weight="bold">Session Affinity</text>
    <circle cx="500" cy="220" r="25" fill="#fbbc04"/>
    <text x="500" y="225" text-anchor="middle">Pod 1</text>
    <circle cx="550" cy="220" r="25" fill="#888"/>
    <text x="550" y="225" text-anchor="middle" fill="white">Pod 2</text>
    <circle cx="600" cy="220" r="25" fill="#888"/>
    <text x="600" y="225" text-anchor="middle" fill="white">Pod 3</text>
    <path d="M 550 140 L 500 195" stroke="#666" stroke-width="3"/>
    <text x="550" y="270" text-anchor="middle" font-size="11">Client → Same Pod</text>
  </g>
</svg>

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