---
tags:
  - infrastructure:kubernetes
  - infrastructure:rbac
level: intermediate
category: containers
audience:
  - audiences:devops

---

# Role-Based Access Control (RBAC)

---

## What This Chapter Covers

- RBAC concepts
- Roles and ClusterRoles
- RoleBindings and ClusterRoleBindings
- ServiceAccounts
- Common patterns
- Auditing

---

## RBAC Concepts

- Subjects (users, groups, service accounts)
- Verbs (get, list, create, update, delete)
- Resources (pods, deployments, services, ...)
- Combine: who can do what to what

---

## RBAC Model

![rbac_model](svg/courses/containers/kubernetes/08_role_based_access_control_rbac/rbac_model.svg)

---

## Roles

- Permissions per namespace
- Verbs + resources
- "Read pods in this namespace"

---

## Sample Role

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""]
  resources: [pods]
  verbs: [get, list, watch]
```

---

## ClusterRoles

- Cluster-wide permissions
- Or: reusable definitions
- Apply via ClusterRoleBinding (cluster) or RoleBinding (namespace)

---

## RoleBinding

- Binds a Role to subjects
- Per-namespace
- "User Alice can do what pod-reader allows"

---

## ClusterRoleBinding

- Binds a ClusterRole to subjects
- Cluster-wide
- "Admin gets cluster-admin"

---

## Built-In Roles

- cluster-admin: everything
- admin: edit anything in a namespace
- edit: modify resources
- view: read-only
- Use as starting points

---

## Subjects of Access

![rbac_subjects](svg/courses/containers/kubernetes/08_role_based_access_control_rbac/rbac_subjects.svg)

---

## ServiceAccount

- Identity for pods
- Each pod has one (default if not specified)
- Used for: pods to call the K8s API
- Or: cloud workload identity

---

## Sample ServiceAccount

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: web-app
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: web-app
subjects:
- kind: ServiceAccount
  name: web-app
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

---

## Pod's ServiceAccount

```yaml
spec:
  serviceAccountName: web-app
```

- Default to non-default account
- Don't use the default ServiceAccount

---

## Workload Identity (Cloud)

- AWS IRSA, GCP Workload Identity
- ServiceAccount &#8594; cloud IAM role
- Pods get cloud credentials without secrets
- Standard for cloud-native apps

---

## Auditing

- Enable audit logs at API server
- Track: who did what, when, succeed/fail
- Forward to SIEM
- Compliance requirement

---

## Common RBAC Patterns

- Per-team namespace + RoleBinding
- Per-app ServiceAccount + minimal Role
- Read-only ClusterRole for monitoring
- cluster-admin: only break-glass

---

## Anti-Patterns

- Using cluster-admin for everything
- Default ServiceAccount with broad permissions
- Same RoleBinding pattern in every namespace (use ClusterRole)
- No audit log
- Permissions never reviewed

---

## Common RBAC Mistakes

- Granting wildcard verbs
- Permissions to everyone
- ServiceAccounts shared across apps
- No periodic review
- Service account tokens checked into git
