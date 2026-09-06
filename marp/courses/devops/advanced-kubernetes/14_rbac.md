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

# Role-Based Access Control (`RBAC`)

Advanced Kubernetes Course - Day 3, Module 4

---

## Module Overview

- `RBAC` concepts and architecture
- `Roles` and `ClusterRoles`
- `RoleBindings` and `ClusterRoleBindings`
- `ServiceAccounts`
- Auditing and troubleshooting
- Least-privilege patterns

---

## `RBAC` Architecture

![rbac_architecture](svg/courses/devops/advanced-kubernetes/14_rbac/rbac_architecture.svg)

---

## `RBAC` API Verbs

| Verb | HTTP Method | Description |
|------|-------------|-------------|
| `get` | GET | Read a single resource |
| `list` | GET | List multiple resources |
| `watch` | GET (streaming) | Watch for changes |
| `create` | POST | Create a resource |
| `update` | PUT | Full update |
| `patch` | PATCH | Partial update |
| `delete` | DELETE | Delete a resource |
| `deletecollection` | DELETE | Delete multiple |

Additional: `bind`, `escalate`, `impersonate`

---

## `Role` - Namespace-Scoped Permissions

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: production
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["pods/log"]
  verbs: ["get"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: deployment-manager
  namespace: production
rules:
- apiGroups: ["apps"]
  resources: ["deployments", "replicasets"]
  verbs: ["get", "list", "watch", "create",
          "update", "patch", "delete"]
- apiGroups: [""]
  resources: ["services"]
  verbs: ["get", "list", "create", "update", "patch"]
- apiGroups: ["networking.k8s.io"]
  resources: ["ingresses"]
  verbs: ["get", "list", "create", "update", "patch"]
```

---

## `ClusterRole` - Cluster-Wide Permissions

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: node-viewer
rules:
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["namespaces"]
  verbs: ["get", "list"]
- apiGroups: ["metrics.k8s.io"]
  resources: ["nodes", "pods"]
  verbs: ["get", "list"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: secret-reader
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "list"]
  # Restrict to specific secrets by name
  resourceNames: ["app-tls", "app-config"]
```

---

## `RoleBinding`

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: dev-team-pod-reader
  namespace: production
subjects:
# User
- kind: User
  name: alice@example.com
  apiGroup: rbac.authorization.k8s.io
# Group
- kind: Group
  name: dev-team
  apiGroup: rbac.authorization.k8s.io
# ServiceAccount
- kind: ServiceAccount
  name: ci-pipeline
  namespace: cicd
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

---

## `ClusterRoleBinding`

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: cluster-admin-binding
subjects:
- kind: Group
  name: platform-team
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io

---
# ClusterRole bound at namespace level
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: dev-view-production
  namespace: production
subjects:
- kind: Group
  name: developers
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole    # ClusterRole used in RoleBinding
  name: view           # Built-in ClusterRole
  apiGroup: rbac.authorization.k8s.io
```

---

## Built-in `ClusterRoles`

| Role | Permissions |
|------|------------|
| `cluster-admin` | Full cluster access (superuser) |
| `admin` | Full namespace access, including `RBAC` |
| `edit` | Read/write most resources (no `RBAC`) |
| `view` | Read-only access (no secrets) |

```bash
# View built-in roles
kubectl get clusterroles | grep -E "^(admin|edit|view|cluster-admin)"

# Inspect permissions
kubectl describe clusterrole edit

# See all bindings for a user
kubectl get rolebindings,clusterrolebindings \
  --all-namespaces \
  -o jsonpath='{range .items[?(@.subjects[0].name=="alice")]}
    {.metadata.name}{"\n"}{end}'
```

---

## `ServiceAccounts`

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: api-reader
  namespace: production
  annotations:
    # AWS IRSA
    eks.amazonaws.com/role-arn: arn:aws:iam::123:role/api-reader
automountServiceAccountToken: false

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-consumer
spec:
  template:
    spec:
      serviceAccountName: api-reader
      automountServiceAccountToken: true
      containers:
      - name: app
        image: myapp:v2
```

---

## `ServiceAccount` Token Projection

```yaml
spec:
  containers:
  - name: app
    image: myapp:v2
    volumeMounts:
    - name: token
      mountPath: /var/run/secrets/tokens
      readOnly: true
  volumes:
  - name: token
    projected:
      sources:
      - serviceAccountToken:
          audience: vault.example.com
          expirationSeconds: 3600
          path: vault-token
      - serviceAccountToken:
          audience: api.example.com
          expirationSeconds: 7200
          path: api-token
```

Bound tokens are:
- Time-limited (auto-rotated)
- Audience-bound
- Object-bound (invalidated when pod deleted)

---

## `RBAC` for `CI/CD` Pipelines

```yaml
# ServiceAccount for CI/CD
apiVersion: v1
kind: ServiceAccount
metadata:
  name: cicd-deployer
  namespace: cicd

---
# Role: Can deploy to staging
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: deployer
  namespace: staging
rules:
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch", "create",
          "update", "patch"]
- apiGroups: [""]
  resources: ["services", "configmaps"]
  verbs: ["get", "list", "create", "update", "patch"]
- apiGroups: ["networking.k8s.io"]
  resources: ["ingresses"]
  verbs: ["get", "list", "create", "update", "patch"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: cicd-deployer-binding
  namespace: staging
subjects:
- kind: ServiceAccount
  name: cicd-deployer
  namespace: cicd
roleRef:
  kind: Role
  name: deployer
  apiGroup: rbac.authorization.k8s.io
```

---

## Testing `RBAC` Permissions

```bash
# Check if you can do something
kubectl auth can-i create deployments -n production
# yes

# Check as another user
kubectl auth can-i create deployments \
  -n production \
  --as=alice@example.com
# no

# Check as a ServiceAccount
kubectl auth can-i list pods \
  -n production \
  --as=system:serviceaccount:cicd:cicd-deployer
# yes

# List all permissions for current user
kubectl auth can-i --list -n production

# Verbose output
kubectl auth can-i --list -n production | head -20
Resources   Non-Resource URLs   Resource Names   Verbs
pods        []                  []               [get list watch]
deployments []                  []               [get list watch create]
```

---

## Aggregated `ClusterRoles`

```yaml
# Base role with aggregation label
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: monitoring-view
  labels:
    rbac.example.com/aggregate-to-monitoring: "true"
rules:
- apiGroups: ["monitoring.coreos.com"]
  resources: ["prometheusrules", "servicemonitors"]
  verbs: ["get", "list", "watch"]

---
# Aggregating ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: monitoring-admin
aggregationRule:
  clusterRoleSelectors:
  - matchLabels:
      rbac.example.com/aggregate-to-monitoring: "true"
rules: []  # Rules are auto-populated
```

Adding new `ClusterRoles` with the label automatically adds their rules.

---

## Audit Logging

```yaml
# /etc/kubernetes/audit-policy.yaml
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
# Log all access to secrets at Metadata level
- level: Metadata
  resources:
  - group: ""
    resources: ["secrets"]

# Log pod creation/deletion at RequestResponse level
- level: RequestResponse
  resources:
  - group: ""
    resources: ["pods"]
  verbs: ["create", "delete"]

# Don't log read-only requests to endpoints
- level: None
  resources:
  - group: ""
    resources: ["endpoints"]
  verbs: ["get", "list", "watch"]

# Default: log at Metadata level
- level: Metadata
```

---

## `RBAC` Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `cluster-admin` everywhere | Create minimal roles |
| Wildcard verbs (`*`) | List explicit verbs |
| Wildcard resources (`*`) | List explicit resources |
| `automountServiceAccountToken: true` | Set to `false` by default |
| Shared `ServiceAccounts` | One per application |
| No audit logging | Enable and monitor |
| Binding to `default` SA | Create dedicated SAs |

---

## RBAC Model

![rbac_model](svg/courses/devops/advanced-kubernetes/14_rbac/rbac_model.svg)

---

## Least Privilege Example

```yaml
# Bad: Overly permissive
rules:
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["*"]

# Good: Minimal permissions for a web app
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get", "watch"]
  resourceNames: ["app-config"]
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get"]
  resourceNames: ["app-tls"]
```

```bash
# Discover what permissions an app actually needs
# 1. Run with broad permissions
# 2. Check audit logs
# 3. Create minimal role based on actual access
kubectl logs -n kube-system kube-apiserver-master | \
  grep "alice@example.com"
```

---

## `RBAC` with OIDC (External Identity)

```yaml
# kube-apiserver flags
--oidc-issuer-url=https://accounts.google.com
--oidc-client-id=my-k8s-client-id
--oidc-username-claim=email
--oidc-groups-claim=groups
```

```yaml
# Bind OIDC group to ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: sre-team-admin
subjects:
- kind: Group
  name: sre-team@example.com
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: admin
  apiGroup: rbac.authorization.k8s.io
```

---

## Lab: `RBAC` Configuration

```bash
# 1. Create ServiceAccounts for different roles
kubectl create sa developer -n production
kubectl create sa viewer -n production
kubectl create sa deployer -n cicd

# 2. Create Roles with appropriate permissions
kubectl apply -f developer-role.yaml
kubectl apply -f viewer-role.yaml

# 3. Create RoleBindings
kubectl apply -f role-bindings.yaml

# 4. Test permissions
kubectl auth can-i create pods -n production \
  --as=system:serviceaccount:production:developer

kubectl auth can-i delete pods -n production \
  --as=system:serviceaccount:production:viewer

# 5. Enable and check audit logs
# 6. Identify overly permissive bindings
kubectl get clusterrolebindings -o json | \
  jq '.items[] | select(.roleRef.name=="cluster-admin")'
```
