---
tags:
  - infrastructure:kubernetes
  - tools:helm
level: intermediate
category: containers
audience:
  - audiences:developers
  - audiences:devops

---
# Helm

---
## What This Chapter Covers

- What Helm is
- Charts
- Values
- Installing and upgrading
- Repositories
- Alternatives

---
## What Helm Is

- The package manager for K8s
- Bundle: many manifests as a "chart"
- Templates with values
- Standard for installing common tools

---
## Helm Concepts

![helm_concepts](svg/courses/containers/kubernetes/09_helm/helm_concepts.svg)

---
## Charts

- A chart: a bundle of manifests + config
- Versioned
- Reusable
- Templated with Go templates

---
## Chart Structure

```tree
mychart/
├── Chart.yaml      # metadata
├── values.yaml     # default config
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    └── ingress.yaml
```

---
## Values

- Configurable inputs
- Override defaults at install
- "image: {{ .Values.image.repository }}"

---
## Installing

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install my-postgres bitnami/postgresql
```

- Or with custom values:

```bash
helm install my-postgres bitnami/postgresql -f values.yaml
```

---
## Upgrading

```bash
helm upgrade my-postgres bitnami/postgresql --version 12.5.0
```

- Idempotent
- Rolling restart of changed resources
- Rollback if failed

---
## Rollback

```bash
helm rollback my-postgres
```

- To previous revision
- History preserved

---
## Templating

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-web
spec:
  replicas: {{ .Values.replicas }}
```

- Go template syntax
- .Values from values.yaml
- .Release: install metadata

---
## Helmfile

- Manage many releases declaratively
- One file, many helm installs
- GitOps-friendly

---
## Repositories

- Public: artifacthub.io
- Private: ChartMuseum, Harbor, JFrog
- OCI registries (since Helm 3.8)

---
## When To Use

- Installing third-party software (Postgres, nginx, Redis)
- Templating your own apps for reuse
- Multi-environment deploys

---
## When Not To

- Simple internal app (kubectl apply might suffice)
- Heavy templating that obscures
- Use Kustomize for overrides without templating

---
## Kustomize Alternative

- Built into kubectl
- Overlays without templating
- "Base + overlays per environment"
- Simpler for some cases; less powerful

---
## Helm vs Kustomize

- Helm: templating, package management
- Kustomize: patches, overlays
- Many teams: Helm for third-party, Kustomize for own apps
- Or: Helm for everything

---
## Common Helm Mistakes

- Hardcoded values that should be configurable
- Templating too aggressively (unreadable charts)
- Not pinning chart versions
- Not testing upgrades on staging
- Storing secrets in values.yaml
