# Helm and GitOps

---

## Helm Overview

1. **Package manager** for Kubernetes
1. **Charts** bundle resources
1. **Templates** with values
1. **Dependency** management
1. **Release** management

---

## Why Helm?

![why_helm](svg/courses/devops/k8s-introduction/14_helm_and_gitops/why_helm.svg)

---

## Helm Architecture

```bash
# Helm 3 Architecture (no Tiller)
┌─────────────┐
│  Helm CLI   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Kubernetes  │
│  API Server │
└─────────────┘
```

---

## Installing Helm

```bash
# Download and install
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Or using package manager
brew install helm  # macOS
sudo snap install helm --classic  # Ubuntu

# Verify installation
helm version
```

---

## Helm Chart Structure

```bash
mychart/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default values
├── templates/          # Template files
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── _helpers.tpl    # Template helpers
├── charts/             # Chart dependencies
└── README.md          # Documentation
```

---

## Helm Chart Structure Diagram

![helm_chart_structure](svg/courses/devops/k8s-introduction/14_helm_and_gitops/helm_chart_structure.svg)

---

## Chart.yaml

```yaml
apiVersion: v2
name: myapp
description: A Helm chart for my application
type: application
version: 1.0.0        # Chart version
appVersion: "2.0.0"   # App version
keywords:
  - web
  - application
maintainers:
  - name: John Doe
    email: john@example.com
dependencies:
  - name: postgresql
    version: 11.x.x
    repository: https://charts.bitnami.com/bitnami
```

---

## values.yaml

```yaml
replicaCount: 3

image:
  repository: myapp
  tag: "2.0.0"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  className: nginx
  host: app.example.com

resources:
  limits:
    cpu: 100m
    memory: 128Mi
  requests:
    cpu: 50m
    memory: 64Mi
```

---

## Template Example

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
        - containerPort: {{ .Values.service.port }}
```

---

## Helm Commands

```bash
# Create new chart
helm create mychart

# Install chart
helm install myrelease ./mychart

# Install with custom values
helm install myrelease ./mychart -f custom-values.yaml

# Upgrade release
helm upgrade myrelease ./mychart

# List releases
helm list

# Rollback
helm rollback myrelease 1

# Uninstall
helm uninstall myrelease
```

---

## Helm Repositories

```bash
# Add repository
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add stable https://charts.helm.sh/stable

# Update repositories
helm repo update

# Search charts
helm search repo nginx

# Show chart info
helm show chart bitnami/nginx
helm show values bitnami/nginx
```

---

## Installing from Repository

```bash
# Search for chart
helm search repo wordpress

# Install from repo
helm install my-wordpress bitnami/wordpress

# Install specific version
helm install my-wordpress bitnami/wordpress --version 15.2.22

# Install with custom values
helm install my-wordpress bitnami/wordpress \
  --set wordpressUsername=admin \
  --set wordpressPassword=secretpass
```

---

## Template Functions

```yaml
# Conditionals
{{- if .Values.ingress.enabled }}
apiVersion: networking.k8s.io/v1
kind: Ingress
...
{{- end }}

# Loops
{{- range .Values.ingress.hosts }}
- host: {{ .host }}
  http:
    paths:
    {{- range .paths }}
    - path: {{ .path }}
    {{- end }}
{{- end }}

# Default values
{{ .Values.service.port | default 80 }}
```

---

## Helm Hooks

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "mychart.fullname" . }}-preinstall
  annotations:
    "helm.sh/hook": pre-install
    "helm.sh/hook-weight": "5"
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  template:
    spec:
      containers:
      - name: pre-install
        image: busybox
        command: ['sh', '-c', 'echo Pre-install hook']
```

---

## Hook Types

```yaml
"helm.sh/hook": pre-install    # Before install
"helm.sh/hook": post-install   # After install
"helm.sh/hook": pre-delete     # Before delete
"helm.sh/hook": post-delete    # After delete
"helm.sh/hook": pre-upgrade    # Before upgrade
"helm.sh/hook": post-upgrade   # After upgrade
"helm.sh/hook": pre-rollback   # Before rollback
"helm.sh/hook": post-rollback  # After rollback
"helm.sh/hook": test          # Helm test
```

---

## Debugging Templates

```bash
# Dry run
helm install myrelease ./mychart --dry-run --debug

# Template rendering
helm template myrelease ./mychart

# Lint chart
helm lint ./mychart

# Get manifest of installed release
helm get manifest myrelease

# Get values of installed release
helm get values myrelease
```

---

## Helm Secrets

```bash
# Install helm-secrets plugin
helm plugin install https://github.com/jkroepke/helm-secrets

# Encrypt values file
helm secrets enc values-secret.yaml

# Install with encrypted values
helm secrets install myrelease ./mychart -f values-secret.yaml

# Edit encrypted file
helm secrets edit values-secret.yaml
```

---

## GitOps Overview

1. **Git as single source of truth**
1. **Declarative infrastructure**
1. **Version controlled**
1. **Automated deployments**
1. **Pull-based model**

---

## GitOps Principles

![gitops_principles](svg/courses/devops/k8s-introduction/14_helm_and_gitops/gitops_principles.svg)

---

## ArgoCD Installation

```bash
# Create namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/\
argoproj/argo-cd/stable/manifests/install.yaml

# Expose UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Get admin password
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
```

---

## ArgoCD Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/user/repo
    targetRevision: HEAD
    path: k8s-manifests
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

---

## ArgoCD with Helm

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: helm-app
spec:
  source:
    repoURL: https://github.com/user/repo
    targetRevision: HEAD
    path: charts/myapp
    helm:
      valueFiles:
      - values.yaml
      - values-prod.yaml
      parameters:
      - name: image.tag
        value: v2.0.0
```

---

## Flux Installation

```bash
# Install Flux CLI
curl -s https://fluxcd.io/install.sh | sudo bash

# Bootstrap Flux
flux bootstrap github \
  --owner=$GITHUB_USER \
  --repository=$GITHUB_REPO \
  --branch=main \
  --path=./clusters/my-cluster \
  --personal

# Check installation
flux check
```

---

## Flux GitRepository

```yaml
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: GitRepository
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 1m
  ref:
    branch: main
  url: https://github.com/user/repo

---
apiVersion: kustomize.toolkit.fluxcd.io/v1beta2
kind: Kustomization
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 10m
  path: "./k8s"
  prune: true
  sourceRef:
    kind: GitRepository
    name: myapp
```

---

## Flux with Helm

```yaml
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: HelmRepository
metadata:
  name: bitnami
  namespace: flux-system
spec:
  interval: 10m
  url: https://charts.bitnami.com/bitnami

---
apiVersion: helm.toolkit.fluxcd.io/v2beta1
kind: HelmRelease
metadata:
  name: nginx
spec:
  interval: 5m
  chart:
    spec:
      chart: nginx
      version: '13.x.x'
      sourceRef:
        kind: HelmRepository
        name: bitnami
  values:
    service:
      type: LoadBalancer
```

---

## GitOps Repository Structure

```bash
k8s-config/
├── base/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── kustomization.yaml
├── overlays/
│   ├── development/
│   │   ├── kustomization.yaml
│   │   └── patch.yaml
│   └── production/
│       ├── kustomization.yaml
│       └── patch.yaml
└── .flux.yaml         # Flux configuration
```

---

## Kustomize with GitOps

```yaml
# base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - deployment.yaml
  - service.yaml

# overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
bases:
  - ../../base
patchesStrategicMerge:
  - patch.yaml
configMapGenerator:
  - name: app-config
    literals:
      - env=production
```

---

## Deployment Strategies

![deployment_strategies](svg/courses/devops/k8s-introduction/14_helm_and_gitops/deployment_strategies.svg)

---

## Argo Rollouts

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: myapp-rollout
spec:
  replicas: 5
  strategy:
    canary:
      steps:
      - setWeight: 20
      - pause: {duration: 1m}
      - setWeight: 40
      - pause: {duration: 1m}
      - setWeight: 60
      - pause: {duration: 1m}
      - setWeight: 80
      - pause: {duration: 1m}
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:v2
```

---

## Sealed Secrets with GitOps

```bash
# Install sealed-secrets controller
kubectl apply -f https://github.com/bitnami-labs/\
sealed-secrets/releases/download/v0.18.0/controller.yaml

# Create sealed secret
echo -n mypassword | kubectl create secret generic mysecret \
  --dry-run=client --from-file=password=/dev/stdin -o yaml | \
  kubeseal -o yaml > sealed-secret.yaml

# Commit to Git
git add sealed-secret.yaml
git commit -m "Add sealed secret"
git push
```

---

## Multi-Environment GitOps

```bash
# Repository structure
environments/
├── base/
│   └── kustomization.yaml
├── staging/
│   ├── kustomization.yaml
│   └── values.yaml
└── production/
    ├── kustomization.yaml
    └── values.yaml

# ArgoCD App of Apps pattern
apps/
├── staging/
│   └── applications.yaml
└── production/
    └── applications.yaml
```

---

## GitOps Best Practices

1. **Separate** config and code repos
1. **Use** semantic versioning
1. **Implement** progressive delivery
1. **Monitor** sync status
1. **Automate** secret management

---

## Helm Best Practices

1. **Use** subchart for common resources
1. **Validate** with JSON schema
1. **Test** with helm test
1. **Document** values clearly
1. **Version** charts properly

---

## Monitoring GitOps

```bash
# ArgoCD metrics
kubectl port-forward -n argocd \
  svc/argocd-metrics 8082:8082

# Flux alerts
apiVersion: notification.toolkit.fluxcd.io/v1beta1
kind: Alert
metadata:
  name: myapp-alert
spec:
  providerRef:
    name: slack
  eventSeverity: error
  eventSources:
  - kind: GitRepository
    name: myapp
  - kind: Kustomization
    name: myapp
```

---

## Troubleshooting Helm

```bash
# Check release status
helm status myrelease

# Get release history
helm history myrelease

# Debug failed release
helm get values myrelease
helm get manifest myrelease

# Rollback failed upgrade
helm rollback myrelease

# Fix stuck release
helm delete myrelease --no-hooks
```

---

## Summary

1. Helm simplifies Kubernetes deployments
1. Charts package related resources
1. GitOps provides declarative deployments
1. Git becomes single source of truth
1. Automation improves reliability
