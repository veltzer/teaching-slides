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
# Declarative Object Configuration

Advanced Kubernetes Course - Day 3, Module 1

---

## Module Overview

- Imperative vs declarative management
- `kubectl apply` deep dive
- `Kustomize` for configuration management
- `Helm` charts
- GitOps with `ArgoCD` and `Flux`

---

## Imperative vs Declarative

**Imperative** - Tell `Kubernetes` what to do:
```bash
kubectl create deployment nginx --image=nginx:1.25
kubectl scale deployment nginx --replicas=3
kubectl set image deployment/nginx nginx=nginx:1.26
kubectl expose deployment nginx --port=80
```

**Declarative** - Tell `Kubernetes` what you want:
```bash
kubectl apply -f deployment.yaml
# Edit the YAML, then:
kubectl apply -f deployment.yaml
```

> **Best Practice**: Always use declarative management in production.

---

## How `kubectl apply` Works

![how_kubectl_apply_works](svg/courses/devops/advanced-kubernetes/11_declarative_config/how_kubectl_apply_works.svg)

---

## How `kubectl apply` Works

The `kubectl.kubernetes.io/last-applied-configuration` annotation stores the previous apply.

---

## Server-Side Apply

Preferred over client-side apply in newer `Kubernetes`:

```bash
# Server-side apply
kubectl apply --server-side -f deployment.yaml

# With field manager
kubectl apply --server-side \
  --field-manager=ci-pipeline \
  -f deployment.yaml

# Force conflicts
kubectl apply --server-side \
  --force-conflicts \
  -f deployment.yaml
```

Benefits:
- Better conflict detection
- Field ownership tracking
- No annotation size limits
- Supports `CRDs` natively

---

## `Kustomize` - File Structure

```tree
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
├── overlays/
│   ├── dev/
│   │   ├── kustomization.yaml
│   │   ├── replica-patch.yaml
│   │   └── env-config.yaml
│   ├── staging/
│   │   ├── kustomization.yaml
│   │   └── replica-patch.yaml
│   └── production/
│       ├── kustomization.yaml
│       ├── replica-patch.yaml
│       ├── hpa.yaml
│       └── resource-patch.yaml
```

---

## `Kustomize` - Base

```yaml
# base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml
- service.yaml
- configmap.yaml

commonLabels:
  app: web-frontend

commonAnnotations:
  managed-by: kustomize
```

```yaml
# base/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 1
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: web
        image: myapp:latest
        ports:
        - containerPort: 8080
```

---

## `Kustomize` - Overlay

```yaml
# overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- ../../base
- hpa.yaml

namespace: production

namePrefix: prod-

patches:
- path: replica-patch.yaml
- path: resource-patch.yaml

images:
- name: myapp
  newName: registry.example.com/myapp
  newTag: v2.5.0

configMapGenerator:
- name: app-config
  behavior: merge
  literals:
  - LOG_LEVEL=warn
  - CACHE_TTL=600

secretGenerator:
- name: db-creds
  files:
  - secrets/db-password
```

---

## `Kustomize` Patches

**Strategic merge patch:**
```yaml
# overlays/production/replica-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 5
```

**JSON patch:**
```yaml
# overlays/production/resource-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  template:
    spec:
      containers:
      - name: web
        resources:
          requests:
            cpu: "500m"
            memory: "256Mi"
          limits:
            cpu: "1"
            memory: "512Mi"
```

---

## `Kustomize` Commands

```bash
# Preview rendered manifests
kubectl kustomize overlays/production/

# Apply directly
kubectl apply -k overlays/production/

# Diff against live state
kubectl diff -k overlays/production/

# Build and pipe to other tools
kubectl kustomize overlays/production/ | \
  kubectl apply --server-side -f -

# Use with kustomize CLI for more features
kustomize build overlays/production/ | kubectl apply -f -
```

---

## `Kustomize` Components (Reusable Add-ons)

```yaml
# components/monitoring/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1alpha1
kind: Component

patches:
- patch: |-
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: web
    spec:
      template:
        metadata:
          annotations:
            prometheus.io/scrape: "true"
            prometheus.io/port: "9090"

resources:
- service-monitor.yaml
```

```yaml
# overlays/production/kustomization.yaml
components:
- ../../components/monitoring
- ../../components/security
```

---

## `Helm` Charts Overview

```tree
mychart/
├── Chart.yaml           # Chart metadata
├── values.yaml          # Default values
├── charts/              # Dependencies
├── templates/           # Template files
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── _helpers.tpl     # Template helpers
│   ├── NOTES.txt        # Post-install notes
│   └── tests/
│       └── test-connection.yaml
└── .helmignore
```

---

## `Helm` Template Example

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "mychart.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "mychart.selectorLabels" . | nindent 8 }}
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        ports:
        - containerPort: {{ .Values.service.targetPort }}
        {{- if .Values.resources }}
        resources:
          {{- toYaml .Values.resources | nindent 10 }}
        {{- end }}
        {{- if .Values.probes.liveness.enabled }}
        livenessProbe:
          httpGet:
            path: {{ .Values.probes.liveness.path }}
            port: {{ .Values.service.targetPort }}
        {{- end }}
```

---

## `Helm` Values

```yaml
# values.yaml
replicaCount: 2

image:
  repository: myapp
  tag: "v1.0.0"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80
  targetPort: 8080

resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 256Mi

probes:
  liveness:
    enabled: true
    path: /healthz
  readiness:
    enabled: true
    path: /ready

ingress:
  enabled: false
  className: nginx
  hosts:
  - host: app.example.com
    paths:
    - path: /
      pathType: Prefix
```

---

## `Helm` Commands

```bash
# Create a new chart
helm create mychart

# Template locally (debug)
helm template myrelease ./mychart -f prod-values.yaml

# Install
helm install myrelease ./mychart \
  -n production \
  --create-namespace \
  -f prod-values.yaml

# Upgrade
helm upgrade myrelease ./mychart \
  -n production \
  -f prod-values.yaml \
  --set image.tag=v2.0.0

# Rollback
helm rollback myrelease 1 -n production

# List releases
helm list -A

# Uninstall
helm uninstall myrelease -n production
```

---
## GitOps with `ArgoCD`

![gitops_with_argocd](svg/courses/devops/advanced-kubernetes/11_declarative_config/gitops_with_argocd.svg)

---
## GitOps with `ArgoCD`

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: web-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/company/k8s-manifests.git
    targetRevision: main
    path: overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
    - ServerSideApply=true
```

---

## `Kustomize` vs `Helm` vs GitOps

| Feature | `Kustomize` | `Helm` | GitOps |
|---------|-----------|------|--------|
| Template engine | No (patches) | Yes (Go templates) | Uses either |
| Package management | No | Yes | No |
| Rollback | Via Git | Built-in | Via Git |
| State tracking | None | Release history | Git history |
| Learning curve | Low | Medium | Medium |
| Best for | Env overlays | Reusable packages | Production deploys |

---

## Lab: Declarative Configuration

```bash
# 1. Create Kustomize structure
mkdir -p base overlays/{dev,prod}

# 2. Write base manifests and overlays
# (provided files)

# 3. Preview and apply
kubectl kustomize overlays/prod/
kubectl apply -k overlays/prod/

# 4. Create a Helm chart
helm create webapp

# 5. Customize values and deploy
helm install webapp ./webapp -f prod-values.yaml

# 6. Set up ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f \
  https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```
