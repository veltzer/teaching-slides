# Ingress and Container Registries

---

## Ingress Overview

1. **HTTP/HTTPS** routing
1. **Load balancing** at L7
1. **SSL/TLS** termination
1. **Name-based** virtual hosting
1. **Path-based** routing

---

## Why Ingress?

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Service vs Ingress</text>
  <g id="services">
    <text x="200" y="80" text-anchor="middle" font-size="12">Without Ingress</text>
    <rect x="100" y="100" width="200" height="40" fill="#4285f4" rx="3"/>
    <text x="200" y="125" text-anchor="middle" fill="white">LoadBalancer Service 1</text>
    <rect x="100" y="150" width="200" height="40" fill="#4285f4" rx="3"/>
    <text x="200" y="175" text-anchor="middle" fill="white">LoadBalancer Service 2</text>
    <rect x="100" y="200" width="200" height="40" fill="#4285f4" rx="3"/>
    <text x="200" y="225" text-anchor="middle" fill="white">LoadBalancer Service 3</text>
    <text x="200" y="270" text-anchor="middle" font-size="11">Multiple Load Balancers</text>
    <text x="200" y="290" text-anchor="middle" font-size="11">Higher cost</text>
  </g>
  <g id="ingress">
    <text x="550" y="80" text-anchor="middle" font-size="12">With Ingress</text>
    <rect x="450" y="100" width="200" height="40" fill="#34a853" rx="3"/>
    <text x="550" y="125" text-anchor="middle" fill="white">Single Ingress</text>
    <rect x="450" y="160" width="60" height="30" fill="#fbbc04" rx="3"/>
    <text x="480" y="180" text-anchor="middle" font-size="10">Svc 1</text>
    <rect x="520" y="160" width="60" height="30" fill="#fbbc04" rx="3"/>
    <text x="550" y="180" text-anchor="middle" font-size="10">Svc 2</text>
    <rect x="590" y="160" width="60" height="30" fill="#fbbc04" rx="3"/>
    <text x="620" y="180" text-anchor="middle" font-size="10">Svc 3</text>
    <text x="550" y="270" text-anchor="middle" font-size="11">Single entry point</text>
    <text x="550" y="290" text-anchor="middle" font-size="11">Cost effective</text>
  </g>
</svg>

---

## Ingress Components

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: simple-ingress
spec:
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

---

## Path Types

```yaml
pathType: Exact     # Exact match
pathType: Prefix    # Prefix match
pathType: ImplementationSpecific  # Controller decides

# Examples:
# Exact: /foo matches /foo only
# Prefix: /foo matches /foo, /foo/, /foo/bar
```

---

## Host-Based Routing

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: host-based
spec:
  rules:
  - host: app1.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app1-service
            port:
              number: 80
  - host: app2.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app2-service
            port:
              number: 80
```

---

## Path-Based Routing

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: path-based
spec:
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /users
        pathType: Prefix
        backend:
          service:
            name: users-service
            port:
              number: 8080
      - path: /products
        pathType: Prefix
        backend:
          service:
            name: products-service
            port:
              number: 8080
```

---

## TLS Configuration

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: tls-ingress
spec:
  tls:
  - hosts:
    - secure.example.com
    secretName: tls-secret
  rules:
  - host: secure.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: secure-service
            port:
              number: 443
```

---

## Creating TLS Secret

```bash
# Generate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout tls.key -out tls.crt \
  -subj "/CN=secure.example.com"

# Create TLS secret
kubectl create secret tls tls-secret \
  --cert=tls.crt \
  --key=tls.key
```

---

## Ingress Controllers

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f9f9f9" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Popular Ingress Controllers</text>
  <rect x="100" y="80" width="150" height="80" fill="#009639" rx="5"/>
  <text x="175" y="110" text-anchor="middle" fill="white" font-weight="bold">NGINX</text>
  <text x="175" y="130" text-anchor="middle" fill="white" font-size="10">Most popular</text>
  <text x="175" y="150" text-anchor="middle" fill="white" font-size="10">Feature rich</text>
  <rect x="270" y="80" width="150" height="80" fill="#f48120" rx="5"/>
  <text x="345" y="110" text-anchor="middle" fill="white" font-weight="bold">Traefik</text>
  <text x="345" y="130" text-anchor="middle" fill="white" font-size="10">Auto SSL</text>
  <text x="345" y="150" text-anchor="middle" fill="white" font-size="10">Dynamic config</text>
  <rect x="440" y="80" width="150" height="80" fill="#659dbd" rx="5"/>
  <text x="515" y="110" text-anchor="middle" fill="white" font-weight="bold">HAProxy</text>
  <text x="515" y="130" text-anchor="middle" fill="white" font-size="10">High performance</text>
  <text x="515" y="150" text-anchor="middle" fill="white" font-size="10">Enterprise</text>
  <rect x="610" y="80" width="140" height="80" fill="#ff9900" rx="5"/>
  <text x="680" y="110" text-anchor="middle" font-weight="bold">AWS ALB</text>
  <text x="680" y="130" text-anchor="middle" font-size="10">AWS native</text>
  <text x="680" y="150" text-anchor="middle" font-size="10">Managed</text>
  <rect x="180" y="180" width="150" height="80" fill="#4285f4" rx="5"/>
  <text x="255" y="210" text-anchor="middle" fill="white" font-weight="bold">GCE</text>
  <text x="255" y="230" text-anchor="middle" fill="white" font-size="10">Google Cloud</text>
  <text x="255" y="250" text-anchor="middle" fill="white" font-size="10">Global LB</text>
  <rect x="350" y="180" width="150" height="80" fill="#0078d4" rx="5"/>
  <text x="425" y="210" text-anchor="middle" fill="white" font-weight="bold">Azure</text>
  <text x="425" y="230" text-anchor="middle" fill="white" font-size="10">Application GW</text>
  <text x="425" y="250" text-anchor="middle" fill="white" font-size="10">WAF support</text>
  <rect x="520" y="180" width="150" height="80" fill="#dc382d" rx="5"/>
  <text x="595" y="210" text-anchor="middle" fill="white" font-weight="bold">Kong</text>
  <text x="595" y="230" text-anchor="middle" fill="white" font-size="10">API Gateway</text>
  <text x="595" y="250" text-anchor="middle" fill="white" font-size="10">Plugins</text>
</svg>

---

## Installing NGINX Ingress

```bash
# Using Helm
helm repo add ingress-nginx \
  https://kubernetes.github.io/ingress-nginx
helm install ingress-nginx ingress-nginx/ingress-nginx

# Or using manifest
kubectl apply -f https://raw.githubusercontent.com/\
kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/\
provider/cloud/deploy.yaml
```

---

## Ingress Annotations

```yaml
metadata:
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
    nginx.ingress.kubernetes.io/proxy-connect-timeout: "600"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "600"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "600"
```

---

## Rate Limiting

```yaml
metadata:
  annotations:
    nginx.ingress.kubernetes.io/limit-rps: "10"
    nginx.ingress.kubernetes.io/limit-rpm: "600"
    nginx.ingress.kubernetes.io/limit-connections: "10"
    nginx.ingress.kubernetes.io/limit-whitelist: \
      "10.0.0.0/8,172.16.0.0/12"
```

---

## Basic Authentication

```bash
# Create auth file
htpasswd -c auth admin

# Create secret
kubectl create secret generic basic-auth --from-file=auth

# Use in Ingress
metadata:
  annotations:
    nginx.ingress.kubernetes.io/auth-type: basic
    nginx.ingress.kubernetes.io/auth-secret: basic-auth
    nginx.ingress.kubernetes.io/auth-realm: 'Authentication Required'
```

---

## Ingress Class

```yaml
apiVersion: networking.k8s.io/v1
kind: IngressClass
metadata:
  name: nginx
spec:
  controller: k8s.io/ingress-nginx
  parameters:
    apiGroup: k8s.example.com
    kind: IngressParameters
    name: external-config
---
apiVersion: networking.k8s.io/v1
kind: Ingress
spec:
  ingressClassName: nginx  # Use specific class
```

---

## Default Backend

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: default-backend
spec:
  defaultBackend:
    service:
      name: default-service
      port:
        number: 80
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 80
```

---

## Container Registries Overview

1. **Store** container images
1. **Version** control for images
1. **Access** control and security
1. **Image** scanning
1. **Distribution** across regions

---

## Registry Types

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Container Registry Options</text>
  <rect x="100" y="80" width="200" height="100" fill="#4285f4" rx="5"/>
  <text x="200" y="110" text-anchor="middle" fill="white" font-weight="bold">Docker Hub</text>
  <text x="200" y="135" text-anchor="middle" fill="white" font-size="11">Public/Private repos</text>
  <text x="200" y="155" text-anchor="middle" fill="white" font-size="11">Official images</text>
  <text x="200" y="175" text-anchor="middle" fill="white" font-size="11">Rate limits</text>
  <rect x="320" y="80" width="200" height="100" fill="#ff9900" rx="5"/>
  <text x="420" y="110" text-anchor="middle" font-weight="bold">Amazon ECR</text>
  <text x="420" y="135" text-anchor="middle" font-size="11">AWS integrated</text>
  <text x="420" y="155" text-anchor="middle" font-size="11">IAM support</text>
  <text x="420" y="175" text-anchor="middle" font-size="11">Scanning</text>
  <rect x="540" y="80" width="200" height="100" fill="#34a853" rx="5"/>
  <text x="640" y="110" text-anchor="middle" fill="white" font-weight="bold">Google GCR/AR</text>
  <text x="640" y="135" text-anchor="middle" fill="white" font-size="11">Global replication</text>
  <text x="640" y="155" text-anchor="middle" fill="white" font-size="11">Vulnerability scan</text>
  <text x="640" y="175" text-anchor="middle" fill="white" font-size="11">Binary auth</text>
  <rect x="100" y="200" width="200" height="100" fill="#0078d4" rx="5"/>
  <text x="200" y="230" text-anchor="middle" fill="white" font-weight="bold">Azure ACR</text>
  <text x="200" y="255" text-anchor="middle" fill="white" font-size="11">Geo-replication</text>
  <text x="200" y="275" text-anchor="middle" fill="white" font-size="11">Tasks/Build</text>
  <rect x="320" y="200" width="200" height="100" fill="#dc382d" rx="5"/>
  <text x="420" y="230" text-anchor="middle" fill="white" font-weight="bold">Harbor</text>
  <text x="420" y="255" text-anchor="middle" fill="white" font-size="11">Open source</text>
  <text x="420" y="275" text-anchor="middle" fill="white" font-size="11">RBAC, scanning</text>
  <rect x="540" y="200" width="200" height="100" fill="#ea4335" rx="5"/>
  <text x="640" y="230" text-anchor="middle" fill="white" font-weight="bold">Quay.io</text>
  <text x="640" y="255" text-anchor="middle" fill="white" font-size="11">Red Hat</text>
  <text x="640" y="275" text-anchor="middle" fill="white" font-size="11">Security focus</text>
</svg>

---

## Using Private Registry

```bash
# Login to registry
docker login myregistry.io

# Tag image
docker tag myapp:latest myregistry.io/myapp:latest

# Push image
docker push myregistry.io/myapp:latest

# Create registry secret in Kubernetes
kubectl create secret docker-registry regcred \
  --docker-server=myregistry.io \
  --docker-username=user \
  --docker-password=pass \
  --docker-email=email@example.com
```

---

## Using Registry Secret

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: private-app
spec:
  imagePullSecrets:
  - name: regcred
  containers:
  - name: app
    image: myregistry.io/myapp:latest
```

---

## Image Pull Policy

```yaml
spec:
  containers:
  - name: app
    image: myapp:latest
    imagePullPolicy: Always
    # Options:
    # Always - Always pull
    # IfNotPresent - Pull if not cached
    # Never - Never pull
```

---

## Image Tagging Strategy

```bash
# Bad - Mutable tag
myapp:latest

# Good - Immutable tags
myapp:v1.2.3
myapp:1.2.3-build-456
myapp:sha256:abc123...
myapp:20240115-1430

# Semantic versioning
myapp:1.2.3        # Specific version
myapp:1.2          # Minor version
myapp:1            # Major version
```

---

## Harbor Installation

```bash
# Using Helm
helm repo add harbor https://helm.goharbor.io
helm install harbor harbor/harbor \
  --set expose.type=ingress \
  --set expose.ingress.hosts.core=harbor.example.com \
  --set persistence.enabled=true \
  --set harborAdminPassword=Harbor12345
```

---

## Image Scanning

```yaml
# Example with Trivy scanner
apiVersion: v1
kind: Pod
metadata:
  annotations:
    container.apparmor.security.beta.kubernetes.io/scanner: \
      runtime/default
spec:
  initContainers:
  - name: scanner
    image: aquasec/trivy
    args:
    - image
    - --exit-code
    - "1"
    - --severity
    - "HIGH,CRITICAL"
    - myapp:latest
```

---

## Registry Mirroring

```yaml
# Configure containerd for mirror
[plugins."io.containerd.grpc.v1.cri".registry.mirrors."docker.io"]
  endpoint = ["https://mirror.example.com"]

[plugins."io.containerd.grpc.v1.cri".registry.configs."mirror.example.com".auth]
  username = "user"
  password = "pass"
```

---

## Multi-Architecture Images

```bash
# Build multi-arch image
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t myapp:latest \
  --push .

# Manifest list
docker manifest create myapp:latest \
  myapp:latest-amd64 \
  myapp:latest-arm64

docker manifest push myapp:latest
```

---

## Image Size Optimization

```dockerfile
# Multi-stage build
FROM golang:1.20 AS builder
WORKDIR /app
COPY . .
RUN go build -o myapp

FROM alpine:3.18
RUN apk --no-cache add ca-certificates
COPY --from=builder /app/myapp /usr/local/bin/
CMD ["myapp"]
```

---

## Registry Webhooks

```yaml
# Harbor webhook example
webhooks:
  - name: image-pushed
    endpoint: https://webhook.example.com/notify
    events:
      - PUSH_ARTIFACT
      - SCANNING_COMPLETED
    enabled: true
```

---

## Cert-Manager for TLS

```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/\
releases/download/v1.13.0/cert-manager.yaml

# Create ClusterIssuer
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt
    solvers:
    - http01:
        ingress:
          class: nginx
```

---

## Using Cert-Manager

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt"
spec:
  tls:
  - hosts:
    - app.example.com
    secretName: app-tls  # Auto-generated
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app
            port:
              number: 80
```

---

## Monitoring Ingress

```bash
# Check ingress status
kubectl get ingress

# Describe ingress
kubectl describe ingress my-ingress

# Check ingress controller logs
kubectl logs -n ingress-nginx deployment/ingress-nginx-controller

# Check endpoints
kubectl get endpoints -n ingress-nginx
```

---

## Troubleshooting Ingress

1. **404 errors**: Check path and pathType
1. **502/503 errors**: Check backend service
1. **SSL errors**: Verify certificate and secret
1. **Slow response**: Check timeouts
1. **No address**: Check controller status

---

## Registry Best Practices

1. **Use** specific tags, not latest
1. **Scan** images for vulnerabilities
1. **Sign** images for trust
1. **Limit** image size
1. **Clean** old images regularly

---

## Ingress Best Practices

1. **Use** TLS for all production
1. **Implement** rate limiting
1. **Configure** appropriate timeouts
1. **Monitor** ingress metrics
1. **Use** ingress classes

---

## Summary

1. Ingress provides L7 load balancing
1. Multiple ingress controllers available
1. TLS termination at ingress level
1. Container registries store images
1. Security scanning is essential
