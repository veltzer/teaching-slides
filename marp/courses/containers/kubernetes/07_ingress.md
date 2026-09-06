---
tags:
  - infrastructure:kubernetes
  - networking:ingress
level: intermediate
category: containers
audience:
  - audiences:developers

---

# Ingress

---

## What This Chapter Covers

- What Ingress is
- Ingress controllers
- Path-based routing
- TLS termination
- Common controllers
- Gateway API

---

## What Ingress Is

- HTTP / HTTPS routing into the cluster
- Routes based on host or path
- Single entry point for many services
- Replaces many LoadBalancers

---

## Ingress Path

![ingress_path](svg/courses/containers/kubernetes/07_ingress/ingress_path.svg)

---

## Ingress vs Service

- Service: layer 4 (TCP)
- Ingress: layer 7 (HTTP)
- Service exposes pods; Ingress routes HTTP traffic
- Ingress sits in front of Services

---

## Sample Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web
spec:
  rules:
  - host: example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api
            port:
              number: 80
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web
            port:
              number: 80
```

---

## Ingress Controllers

- nginx-ingress
- Traefik
- HAProxy
- AWS ALB Ingress
- Cilium Ingress
- Pick one; install separately

---

## NGINX Ingress

- Most popular
- Free, mature
- Configurable via annotations
- Fast

---

## Traefik

- Auto-discovers services
- Pretty dashboard
- Handles ACME (Let's Encrypt) natively
- Modern UX

---

## TLS Termination

- Ingress decrypts TLS
- Forwards plain to backend
- Or: pass-through (rare)
- Certificates in Secrets

---

## Sample TLS

```yaml
spec:
  tls:
  - hosts: [example.com]
    secretName: example-tls
```

---

## Cert-Manager

- Auto-provisions certs from Let's Encrypt
- Per-Ingress or per-namespace
- Renewal automated
- Standard in K8s

---

## Path Types

- Exact: must match exactly
- Prefix: starts with
- ImplementationSpecific: controller-specific
- Use Prefix or Exact

---

## Annotations

- Controller-specific config
- "nginx.ingress.kubernetes.io/rewrite-target: /"
- Rate limit, auth, headers
- Each controller has its own set

---

## Gateway API

- Newer alternative to Ingress
- More expressive
- Multiple gateway types (HTTP, TCP, UDP)
- Adoption growing

---

## Two Routing APIs

![ingress_vs_gateway](svg/courses/containers/kubernetes/07_ingress/ingress_vs_gateway.svg)

---

## When To Use Gateway API

- Need TCP / UDP routing
- Complex traffic management
- New cluster: consider it
- Existing Ingress: stick for now

---

## Common Ingress Mistakes

- One Ingress per host (use one with many paths)
- No TLS in production
- Cert-Manager misconfigured (cert renewals fail)
- Wrong pathType (matching too much / too little)
- Heavy annotations: sign of wrong tool
