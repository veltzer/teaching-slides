---
tags:
  - tools:kubernetes
  - infrastructure:containers
  - practices:devops
  - languages:go
  - concepts:service-mesh
level: advanced
category: devops
audience:
  - audiences:developers

---

# Service Mesh & Network Policies

Advanced Kubernetes Course - Day 2, Module 3

---

## Sidecar Pattern

![service_mesh](svg/courses/devops/advanced-kubernetes/08_service_mesh/service_mesh.svg)

---

## Module Overview

- Service mesh concepts
- `Istio` architecture and traffic management
- Traffic shifting and canary releases
- `NetworkPolicies` for cluster security
- Mutual `TLS` (`mTLS`)

---

## Why a Service Mesh?

![why_a_service_mesh](svg/courses/devops/advanced-kubernetes/08_service_mesh/why_a_service_mesh.svg)

---

## `Istio` Architecture

![istio_architecture](svg/courses/devops/advanced-kubernetes/08_service_mesh/istio_architecture.svg)

---

## Installing `Istio`

```bash
# Download istioctl (defaults to latest; see https://istio.io/latest/docs/releases/)
curl -L https://istio.io/downloadIstio | sh -
export PATH=$PWD/istio-<version>/bin:$PATH

# Install with demo profile (demo profile is for learning, not production)
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

![traffic_shifting_canary_release](svg/courses/devops/advanced-kubernetes/08_service_mesh/traffic_shifting_canary_release.svg)

---

## Traffic Shifting - Canary Release: Example

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

![networkpolicy_visualization](svg/courses/devops/advanced-kubernetes/08_service_mesh/networkpolicy_visualization.svg)

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
