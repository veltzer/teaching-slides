# Service Mesh & Network Policies

Advanced Kubernetes Course - Day 2, Module 3

---

## Module Overview

- Service mesh concepts
- `Istio` architecture and traffic management
- Traffic shifting and canary releases
- `NetworkPolicies` for cluster security
- Mutual `TLS` (`mTLS`)

---

## Why a Service Mesh?

<svg xmlns="http://www.w3.org/2000/svg" width="650" height="340" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
    <marker id="arr2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>  <rect x="10" y="10" width="300" height="300" rx="4" fill="#fff8e1" stroke="#f9a825" stroke-width="1.5"/>
  <text x="160" y="32" text-anchor="middle" font-size="13" fill="#e65100" font-weight="bold">Without Service Mesh</text>
  <rect x="30" y="50" width="70" height="50" rx="4" fill="#fff3e0" stroke="#ef6c00" stroke-width="1.5"/>
  <text x="65" y="80" text-anchor="middle" font-size="12" fill="#222">App A</text>
  <line x1="100" y1="75" x2="115" y2="75" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="115" y="50" width="70" height="50" rx="4" fill="#fff3e0" stroke="#ef6c00" stroke-width="1.5"/>
  <text x="150" y="80" text-anchor="middle" font-size="12" fill="#222">App B</text>
  <line x1="185" y1="75" x2="200" y2="75" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="200" y="50" width="70" height="50" rx="4" fill="#fff3e0" stroke="#ef6c00" stroke-width="1.5"/>
  <text x="235" y="80" text-anchor="middle" font-size="12" fill="#222">App C</text>
  <text x="160" y="125" text-anchor="middle" font-size="11" fill="#555">Each app handles:</text>
  <text x="160" y="142" text-anchor="middle" font-size="11" fill="#555">retries, timeouts, auth,</text>
  <text x="160" y="159" text-anchor="middle" font-size="11" fill="#555">logging, tracing, TLS...</text>
  <rect x="330" y="10" width="310" height="300" rx="4" fill="#e8f5e9" stroke="#388e3c" stroke-width="1.5"/>
  <text x="485" y="32" text-anchor="middle" font-size="13" fill="#2e7d32" font-weight="bold">With Service Mesh</text>
  <rect x="345" y="50" width="70" height="40" rx="4" fill="#e8f5e9" stroke="#43a047" stroke-width="1.5"/>
  <text x="380" y="74" text-anchor="middle" font-size="12" fill="#222">App A</text>
  <rect x="345" y="98" width="70" height="36" rx="4" fill="#ede7f6" stroke="#7b1fa2" stroke-width="1.5"/>
  <text x="380" y="120" text-anchor="middle" font-size="11" fill="#4a148c">Proxy</text>
  <line x1="415" y1="116" x2="435" y2="116" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="435" y="50" width="70" height="40" rx="4" fill="#e8f5e9" stroke="#43a047" stroke-width="1.5"/>
  <text x="470" y="74" text-anchor="middle" font-size="12" fill="#222">App B</text>
  <rect x="435" y="98" width="70" height="36" rx="4" fill="#ede7f6" stroke="#7b1fa2" stroke-width="1.5"/>
  <text x="470" y="120" text-anchor="middle" font-size="11" fill="#4a148c">Proxy</text>
  <line x1="505" y1="116" x2="525" y2="116" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="525" y="50" width="70" height="40" rx="4" fill="#e8f5e9" stroke="#43a047" stroke-width="1.5"/>
  <text x="560" y="74" text-anchor="middle" font-size="12" fill="#222">App C</text>
  <rect x="525" y="98" width="70" height="36" rx="4" fill="#ede7f6" stroke="#7b1fa2" stroke-width="1.5"/>
  <text x="560" y="120" text-anchor="middle" font-size="11" fill="#4a148c">Proxy</text>
  <text x="485" y="158" text-anchor="middle" font-size="11" fill="#555">Proxies handle all</text>
  <text x="485" y="174" text-anchor="middle" font-size="11" fill="#555">cross-cutting concerns</text>
</svg>

---

## `Istio` Architecture

<svg xmlns="http://www.w3.org/2000/svg" width="620" height="400" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
    <marker id="arr2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>  <rect x="10" y="10" width="600" height="175" rx="4" fill="#e3f2fd" stroke="#1565c0" stroke-width="1.5"/>
  <text x="310" y="30" text-anchor="middle" font-size="14" fill="#0d47a1" font-weight="bold">Control Plane</text>
  <rect x="30" y="40" width="560" height="130" rx="4" fill="#bbdefb" stroke="#1976d2" stroke-width="1.5"/>
  <text x="310" y="62" text-anchor="middle" font-size="14" fill="#0d47a1" font-weight="bold">istiod</text>
  <rect x="80" y="72" width="130" height="80" rx="4" fill="#e3f2fd" stroke="#1976d2" stroke-width="1.5"/>
  <text x="145" y="105" text-anchor="middle" font-size="12" fill="#222">Pilot</text>
  <text x="145" y="123" text-anchor="middle" font-size="11" fill="#555">(config)</text>
  <rect x="260" y="72" width="130" height="80" rx="4" fill="#e3f2fd" stroke="#1976d2" stroke-width="1.5"/>
  <text x="325" y="105" text-anchor="middle" font-size="12" fill="#222">Citadel</text>
  <text x="325" y="123" text-anchor="middle" font-size="11" fill="#555">(certs)</text>
  <rect x="450" y="72" width="130" height="80" rx="4" fill="#e3f2fd" stroke="#1976d2" stroke-width="1.5"/>
  <text x="515" y="105" text-anchor="middle" font-size="12" fill="#222">Galley</text>
  <text x="515" y="123" text-anchor="middle" font-size="11" fill="#555">(validate)</text>
  <line x1="310" y1="185" x2="310" y2="215" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="360" y="204" text-anchor="middle" font-size="11" fill="#555">pushes config</text>
  <rect x="60" y="220" width="145" height="95" rx="4" fill="#ede7f6" stroke="#6a1b9a" stroke-width="1.5"/>
  <text x="132" y="248" text-anchor="middle" font-size="12" fill="#222">Envoy Proxy</text>
  <text x="132" y="266" text-anchor="middle" font-size="11" fill="#555">(sidecar)</text>
  <rect x="240" y="220" width="145" height="95" rx="4" fill="#ede7f6" stroke="#6a1b9a" stroke-width="1.5"/>
  <text x="312" y="248" text-anchor="middle" font-size="12" fill="#222">Envoy Proxy</text>
  <text x="312" y="266" text-anchor="middle" font-size="11" fill="#555">(sidecar)</text>
  <rect x="420" y="220" width="145" height="95" rx="4" fill="#ede7f6" stroke="#6a1b9a" stroke-width="1.5"/>
  <text x="492" y="248" text-anchor="middle" font-size="12" fill="#222">Envoy Proxy</text>
  <text x="492" y="266" text-anchor="middle" font-size="11" fill="#555">(sidecar)</text>
  <text x="310" y="336" text-anchor="middle" font-size="13" fill="#4a148c" font-weight="bold">Data Plane</text>
</svg>

---

## Installing `Istio`

```bash
# Download istioctl
curl -L https://istio.io/downloadIstio | sh -
export PATH=$PWD/istio-1.21.0/bin:$PATH

# Install with demo profile
istioctl install --set profile=demo -y

# Enable sidecar injection for a namespace
kubectl label namespace default istio-injection=enabled

# Verify installation
istioctl verify-install
kubectl get pods -n istio-system
```

---

## `VirtualService` - Traffic Routing

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: reviews-route
spec:
  hosts:
  - reviews
  http:
  - match:
    - headers:
        x-user-type:
          exact: beta-tester
    route:
    - destination:
        host: reviews
        subset: v2
  - route:
    - destination:
        host: reviews
        subset: v1
      weight: 90
    - destination:
        host: reviews
        subset: v2
      weight: 10
    timeout: 5s
    retries:
      attempts: 3
      perTryTimeout: 2s
```

---

## `DestinationRule` - Subsets and Policies

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: reviews-destination
spec:
  host: reviews
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        h2UpgradePolicy: DEFAULT
        http1MaxPendingRequests: 100
        http2MaxRequests: 1000
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
    trafficPolicy:
      connectionPool:
        http:
          http2MaxRequests: 500
```

---

## Traffic Shifting - Canary Release

<svg xmlns="http://www.w3.org/2000/svg" width="640" height="310" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
    <marker id="arr2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>  <text x="20" y="38" text-anchor="start" font-size="13" fill="#333" font-weight="bold">Step 1: 100% v1</text>
  <text x="75" y="58" text-anchor="start" font-size="12" fill="#1976d2">v1</text>
  <rect x="100" y="46" width="300" height="16" rx="2" fill="#e0e0e0" stroke="#bbb" stroke-width="1.5"/>
  <rect x="100" y="46" width="300" height="16" rx="2" fill="#1976d2" stroke="#1976d2" stroke-width="1.5"/>
  <text x="410" y="59" text-anchor="start" font-size="12" fill="#1976d2">100%</text>
  <text x="75" y="78" text-anchor="start" font-size="12" fill="#43a047">v2</text>
  <rect x="100" y="66" width="300" height="16" rx="2" fill="#e0e0e0" stroke="#bbb" stroke-width="1.5"/>
  <text x="410" y="79" text-anchor="start" font-size="12" fill="#43a047">0%</text>
  <text x="20" y="106" text-anchor="start" font-size="13" fill="#333">Step 2: 90/10 split</text>
  <text x="75" y="126" text-anchor="start" font-size="12" fill="#1976d2">v1</text>
  <rect x="100" y="114" width="300" height="16" rx="2" fill="#e0e0e0" stroke="#bbb" stroke-width="1.5"/>
  <rect x="100" y="114" width="270" height="16" rx="2" fill="#1976d2" stroke="#1976d2" stroke-width="1.5"/>
  <text x="410" y="127" text-anchor="start" font-size="12" fill="#1976d2">90%</text>
  <text x="75" y="146" text-anchor="start" font-size="12" fill="#43a047">v2</text>
  <rect x="100" y="134" width="300" height="16" rx="2" fill="#e0e0e0" stroke="#bbb" stroke-width="1.5"/>
  <rect x="100" y="134" width="30" height="16" rx="2" fill="#43a047" stroke="#43a047" stroke-width="1.5"/>
  <text x="410" y="147" text-anchor="start" font-size="12" fill="#43a047">10%</text>
  <text x="20" y="174" text-anchor="start" font-size="13" fill="#333">Step 3: 50/50 split</text>
  <text x="75" y="194" text-anchor="start" font-size="12" fill="#1976d2">v1</text>
  <rect x="100" y="182" width="300" height="16" rx="2" fill="#e0e0e0" stroke="#bbb" stroke-width="1.5"/>
  <rect x="100" y="182" width="150" height="16" rx="2" fill="#1976d2" stroke="#1976d2" stroke-width="1.5"/>
  <text x="410" y="195" text-anchor="start" font-size="12" fill="#1976d2">50%</text>
  <text x="75" y="214" text-anchor="start" font-size="12" fill="#43a047">v2</text>
  <rect x="100" y="202" width="300" height="16" rx="2" fill="#e0e0e0" stroke="#bbb" stroke-width="1.5"/>
  <rect x="100" y="202" width="150" height="16" rx="2" fill="#43a047" stroke="#43a047" stroke-width="1.5"/>
  <text x="410" y="215" text-anchor="start" font-size="12" fill="#43a047">50%</text>
  <text x="20" y="242" text-anchor="start" font-size="13" fill="#333" font-weight="bold">Step 4: 100% v2</text>
  <text x="75" y="262" text-anchor="start" font-size="12" fill="#1976d2">v1</text>
  <rect x="100" y="250" width="300" height="16" rx="2" fill="#e0e0e0" stroke="#bbb" stroke-width="1.5"/>
  <text x="410" y="263" text-anchor="start" font-size="12" fill="#1976d2">0%</text>
  <text x="75" y="282" text-anchor="start" font-size="12" fill="#43a047">v2</text>
  <rect x="100" y="270" width="300" height="16" rx="2" fill="#e0e0e0" stroke="#bbb" stroke-width="1.5"/>
  <rect x="100" y="270" width="300" height="16" rx="2" fill="#43a047" stroke="#43a047" stroke-width="1.5"/>
  <text x="410" y="283" text-anchor="start" font-size="12" fill="#43a047">100%</text>
</svg>

```bash
# Shift traffic gradually
kubectl apply -f - <<EOF
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: reviews-route
spec:
  hosts: [reviews]
  http:
  - route:
    - destination: {host: reviews, subset: v1}
      weight: 50
    - destination: {host: reviews, subset: v2}
      weight: 50
EOF
```

---

## `Gateway` - Ingress Traffic

```yaml
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: app-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 443
      name: https
      protocol: HTTPS
    tls:
      mode: SIMPLE
      credentialName: app-tls-cert
    hosts:
    - "app.example.com"
---
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: app-vs
spec:
  hosts:
  - "app.example.com"
  gateways:
  - app-gateway
  http:
  - match:
    - uri:
        prefix: /api
    route:
    - destination:
        host: api-service
        port:
          number: 8080
  - route:
    - destination:
        host: frontend-service
        port:
          number: 80
```

---

## Circuit Breaking

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: payment-service
spec:
  host: payment-service
  trafficPolicy:
    outlierDetection:
      consecutive5xxErrors: 3
      interval: 10s
      baseEjectionTime: 30s
      maxEjectionPercent: 100
    connectionPool:
      tcp:
        maxConnections: 50
      http:
        http1MaxPendingRequests: 50
        http2MaxRequests: 100
        maxRequestsPerConnection: 10
```

```misc
Normal → 3 errors → Circuit Open (30s) → Half-Open → Test → Close/Open
```

---

## Mutual `TLS` with `Istio`

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT
---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-frontend
  namespace: production
spec:
  selector:
    matchLabels:
      app: api-server
  action: ALLOW
  rules:
  - from:
    - source:
        principals:
        - cluster.local/ns/production/sa/frontend
    to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/api/*"]
```

---

## `NetworkPolicy` Basics

By default, all pods can communicate with all pods. `NetworkPolicies` restrict this:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

This blocks **all** ingress and egress traffic in the `production` namespace.

---

## `NetworkPolicy` - Allow Specific Traffic

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api-server
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    - namespaceSelector:
        matchLabels:
          name: monitoring
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: UDP
      port: 53
```

---

## `NetworkPolicy` Visualization

<svg xmlns="http://www.w3.org/2000/svg" width="650" height="370" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
    <marker id="arr2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>  <rect x="10" y="10" width="630" height="320" rx="4" fill="#f8f9fa" stroke="#333" stroke-width="1.5"/>
  <text x="325" y="30" text-anchor="middle" font-size="14" fill="#333" font-weight="bold">production namespace</text>
  <rect x="35" y="55" width="130" height="65" rx="4" fill="#e3f2fd" stroke="#1976d2" stroke-width="1.5"/>
  <text x="100" y="82" text-anchor="middle" font-size="13" fill="#222">frontend</text>
  <line x1="165" y1="87" x2="220" y2="87" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="192" y="80" text-anchor="middle" font-size="10" fill="#555">8080</text>
  <rect x="220" y="45" width="200" height="155" rx="4" fill="#e8f5e9" stroke="#388e3c" stroke-width="1.5"/>
  <text x="320" y="68" text-anchor="middle" font-size="13" fill="#222" font-weight="bold">api-server</text>
  <text x="320" y="90" text-anchor="middle" font-size="11" fill="#555">Ingress:</text>
  <text x="320" y="106" text-anchor="middle" font-size="11" fill="#555">  from: frontend</text>
  <text x="320" y="122" text-anchor="middle" font-size="11" fill="#555">  port: 8080</text>
  <text x="320" y="142" text-anchor="middle" font-size="11" fill="#555">Egress:</text>
  <text x="320" y="158" text-anchor="middle" font-size="11" fill="#555">  to: database</text>
  <text x="320" y="174" text-anchor="middle" font-size="11" fill="#555">  port: 5432</text>
  <line x1="320" y1="200" x2="320" y2="235" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="340" y="222" text-anchor="middle" font-size="10" fill="#555">5432</text>
  <rect x="220" y="235" width="200" height="65" rx="4" fill="#fff3e0" stroke="#f57c00" stroke-width="1.5"/>
  <text x="320" y="263" text-anchor="middle" font-size="13" fill="#222">database</text>
  <text x="320" y="282" text-anchor="middle" font-size="11" fill="#555">port: 5432</text>
  <text x="35" y="325" text-anchor="start" font-size="11" fill="#c62828">✗ backend → api-server (BLOCKED)   ✗ api-server → internet (BLOCKED)</text>
</svg>

---

## `NetworkPolicy` Patterns

**Allow from specific namespace:**
```yaml
ingress:
- from:
  - namespaceSelector:
      matchLabels:
        purpose: monitoring
```

**Allow DNS egress (essential!):**
```yaml
egress:
- to:
  - namespaceSelector: {}
  ports:
  - protocol: UDP
    port: 53
  - protocol: TCP
    port: 53
```

**CIDR block:**
```yaml
egress:
- to:
  - ipBlock:
      cidr: 10.0.0.0/8
      except:
      - 10.0.1.0/24
```

---

## Observing Network Traffic

```bash
# Check if NetworkPolicy CNI supports policies
# (Calico, Cilium, Weave - YES; Flannel - NO)

# List policies
kubectl get networkpolicy -A

# Describe a policy
kubectl describe networkpolicy api-policy -n production

# Test connectivity
kubectl exec frontend-pod -- \
  curl -s -o /dev/null -w "%{http_code}" \
  http://api-server:8080/health

# Should be blocked
kubectl exec backend-pod -- \
  curl -s -o /dev/null -w "%{http_code}" \
  http://api-server:8080/health
```

---

## Lab: Service Mesh and Network Policies

```bash
# 1. Install Istio
istioctl install --set profile=demo
kubectl label namespace default istio-injection=enabled

# 2. Deploy sample app with v1 and v2
kubectl apply -f bookinfo.yaml

# 3. Configure traffic splitting
kubectl apply -f virtual-service-90-10.yaml

# 4. Apply NetworkPolicies
kubectl apply -f deny-all.yaml
kubectl apply -f allow-specific.yaml

# 5. Test connectivity
kubectl exec -it sleep -- curl productpage:9080

# 6. Observe traffic in Kiali dashboard
istioctl dashboard kiali
```
