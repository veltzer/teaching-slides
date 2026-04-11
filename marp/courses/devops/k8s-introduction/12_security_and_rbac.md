---
tags:
  - tools:kubernetes
  - infrastructure:containers
  - infrastructure:orchestration
  - practices:devops
  - tools:docker
level: beginner
category: devops
audience:
  - audiences:developers
  - audiences:devops
  - audiences:sysadmins

---
# Security and RBAC

---

## Security Overview

1. **Authentication**: Who are you?
1. **Authorization**: What can you do?
1. **Admission Control**: Is it allowed?
1. **Network Policies**: Traffic control
1. **Pod Security**: Container constraints

---

## Security Layers

![security_layers](svg/courses/devops/k8s-introduction/12_security_and_rbac/security_layers.svg)

---

## Authentication Methods

1. **X509 Client Certs**: Certificate-based
1. **Bearer Tokens**: Static tokens
1. **Service Account Tokens**: For pods
1. **OpenID Connect**: External IdP
1. **Webhook**: External authenticator

---

## Service Accounts

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-sa
  namespace: default
automountServiceAccountToken: true

---
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: app-sa
  containers:
  - name: app
    image: myapp
```

---

## RBAC Overview

1. **Role-Based Access Control**
1. **Fine-grained permissions**
1. **Namespace or cluster scope**
1. **Default deny**
1. **Additive permissions**

---

## RBAC Components

![rbac_components](svg/courses/devops/k8s-introduction/12_security_and_rbac/rbac_components.svg)

---

## Creating a Role

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list"]
```

---

## Creating RoleBinding

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: default
subjects:
- kind: User
  name: jane
  apiGroup: rbac.authorization.k8s.io
- kind: ServiceAccount
  name: app-sa
  namespace: default
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

---

## ClusterRole Example

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: secret-reader
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "watch", "list"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: read-secrets-global
subjects:
- kind: Group
  name: managers
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: secret-reader
  apiGroup: rbac.authorization.k8s.io
```

---

## Verbs in RBAC

```yaml
verbs:
  - get        # Read single resource
  - list       # List resources
  - watch      # Watch for changes
  - create     # Create new
  - update     # Update existing
  - patch      # Partial update
  - delete     # Delete resource
  - deletecollection  # Delete multiple
  - exec       # Execute in pod
  - port-forward  # Port forwarding
```

---

## Aggregated ClusterRoles

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: monitoring
  labels:
    rbac.example.com/aggregate-to-monitoring: "true"
rules: []

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: monitoring-aggregate
aggregationRule:
  clusterRoleSelectors:
  - matchLabels:
      rbac.example.com/aggregate-to-monitoring: "true"
rules: []  # Auto-populated from matching roles
```

---

## Default Roles

```bash
# View default cluster roles
kubectl get clusterroles | grep system:

# Common default roles:
cluster-admin     # Full access
admin            # Admin within namespace
edit             # Edit most resources
view             # Read-only access
```

---

## Testing RBAC

```bash
# Check if user can perform action
kubectl auth can-i create pods --as=jane

# Check in namespace
kubectl auth can-i get pods --as=jane -n production

# Check all permissions
kubectl auth can-i --list --as=jane

# Who can perform action
kubectl auth who-can delete pods
```

---

## Pod Security Standards

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: secure-namespace
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

---

## Pod Security Levels

![pod_security_levels](svg/courses/devops/k8s-introduction/12_security_and_rbac/pod_security_levels.svg)

---

## Security Context

```yaml
apiVersion: v1
kind: Pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
        add:
        - NET_BIND_SERVICE
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
    - namespaceSelector:
        matchLabels:
          name: production
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
```

---

## Admission Controllers

```bash
# View enabled admission controllers
kubectl exec -n kube-system kube-apiserver-master -- \
  kube-apiserver -h | grep enable-admission-plugins

# Common controllers:
- NamespaceLifecycle
- LimitRanger
- ServiceAccount
- ResourceQuota
- PodSecurity
- MutatingAdmissionWebhook
- ValidatingAdmissionWebhook
```

---

## Kubernetes Security Layers

![k8s_security_layers](svg/courses/devops/k8s-introduction/12_security_and_rbac/k8s_security_layers.svg)

---

## Resource Quotas

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: dev
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    persistentvolumeclaims: "10"
    pods: "50"
    services: "10"
```

---

## LimitRange

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: mem-limit-range
spec:
  limits:
  - default:
      memory: 512Mi
      cpu: "1"
    defaultRequest:
      memory: 256Mi
      cpu: "0.5"
    max:
      memory: 1Gi
      cpu: "2"
    min:
      memory: 128Mi
      cpu: "200m"
    type: Container
```

---

## Secrets Management

```yaml
# Encrypt secrets at rest
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
    - secrets
    providers:
    - aescbc:
        keys:
        - name: key1
          secret: <base64-encoded-secret>
    - identity: {}
```

---

## Image Security

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    image: myregistry.io/myapp:v1.2.3
    imagePullPolicy: Always
  imagePullSecrets:
  - name: regcred
  # Security scanning
  initContainers:
  - name: scan
    image: aquasec/trivy
    args: ["image", "--exit-code", "1",
           "--severity", "HIGH,CRITICAL",
           "myregistry.io/myapp:v1.2.3"]
```

---

## OPA (Open Policy Agent)

```yaml
# Example OPA policy
package kubernetes.admission

deny[msg] {
  input.request.kind.kind == "Pod"
  input.request.object.spec.containers[_].image
  not starts_with(input.request.object.spec.containers[_].image, "myregistry.io/")
  msg := "Images must be from myregistry.io"
}

deny[msg] {
  input.request.kind.kind == "Pod"
  not input.request.object.spec.securityContext.runAsNonRoot
  msg := "Pods must run as non-root"
}
```

---

## Falco Runtime Security

```yaml
# Falco rule example
- rule: Write below etc
  desc: Detect writes below /etc
  condition: >
    evt.type = write and
    fd.name startswith /etc and
    not proc.name in (allowed_processes)
  output: >
    File below /etc written (user=%user.name
    command=%proc.cmdline file=%fd.name)
  priority: ERROR
```

---

## Security Scanning Tools

![security_scanning_tools](svg/courses/devops/k8s-introduction/12_security_and_rbac/security_scanning_tools.svg)

---

## CIS Kubernetes Benchmark

```bash
# Run kube-bench
kubectl apply -f https://raw.githubusercontent.com/\
aquasecurity/kube-bench/main/job.yaml

# Check results
kubectl logs job/kube-bench

# Key areas checked:
- Control plane security
- etcd configuration
- Control plane configuration
- Worker node security
- Policies
```

---

## Audit Logging

```yaml
# Audit policy
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
- level: RequestResponse
  omitStages:
  - RequestReceived
  resources:
  - group: ""
    resources: ["secrets", "configmaps"]
  namespaces: ["production"]
- level: Metadata
  resources:
  - group: ""
    resources: ["pods", "services"]
```

---

## Security Best Practices

1. **Least privilege** principle
1. **Network segmentation** with policies
1. **Image scanning** and signing
1. **Secrets rotation** regularly
1. **Audit logging** enabled

---

## Common Security Issues

1. **Default service account**: Too permissive
1. **No network policies**: Open communication
1. **Latest tags**: Mutable images
1. **Root containers**: Privilege escalation
1. **No resource limits**: DoS attacks

---

## RBAC Debugging

```bash
# Check RBAC permissions
kubectl auth can-i --list --as=system:serviceaccount:default:mysa

# Describe role
kubectl describe role pod-reader

# Get rolebindings for user
kubectl get rolebindings,clusterrolebindings \
  --all-namespaces -o json | \
  jq '.items[] | select(.subjects[]?.name=="jane")'

# Audit RBAC
kubectl-who-can create pods
```

---

## mTLS with Service Mesh

```yaml
# Istio PeerAuthentication
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
spec:
  mtls:
    mode: STRICT

# Linkerd annotation
metadata:
  annotations:
    linkerd.io/inject: enabled
```

---

## Compliance Frameworks

1. **PCI DSS**: Payment card security
1. **HIPAA**: Healthcare data
1. **SOC 2**: Service organizations
1. **ISO 27001**: Information security
1. **GDPR**: Data protection

---

## Summary

1. RBAC controls access to resources
1. Pod Security Standards enforce policies
1. Network policies segment traffic
1. Security scanning prevents vulnerabilities
1. Defense in depth approach essential
