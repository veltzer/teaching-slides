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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Kubernetes Security Layers</text>
  <rect x="100" y="80" width="600" height="50" fill="#4285f4" rx="5"/>
  <text x="400" y="110" text-anchor="middle" fill="white" font-weight="bold">Cloud/Infrastructure Security</text>
  <rect x="150" y="150" width="500" height="50" fill="#34a853" rx="5"/>
  <text x="400" y="180" text-anchor="middle" fill="white" font-weight="bold">Cluster Security (RBAC, Network Policies)</text>
  <rect x="200" y="220" width="400" height="50" fill="#fbbc04" rx="5"/>
  <text x="400" y="250" text-anchor="middle" font-weight="bold">Container Security (Images, Runtime)</text>
  <rect x="250" y="290" width="300" height="50" fill="#ea4335" rx="5"/>
  <text x="400" y="320" text-anchor="middle" fill="white" font-weight="bold">Application Security (Code)</text>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f9f9f9" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">RBAC Components</text>
  <rect x="100" y="80" width="150" height="80" fill="#4285f4" rx="5"/>
  <text x="175" y="110" text-anchor="middle" fill="white" font-weight="bold">Role</text>
  <text x="175" y="130" text-anchor="middle" fill="white" font-size="10">Namespace scoped</text>
  <text x="175" y="150" text-anchor="middle" fill="white" font-size="10">Define permissions</text>
  <rect x="270" y="80" width="150" height="80" fill="#34a853" rx="5"/>
  <text x="345" y="110" text-anchor="middle" fill="white" font-weight="bold">ClusterRole</text>
  <text x="345" y="130" text-anchor="middle" fill="white" font-size="10">Cluster scoped</text>
  <text x="345" y="150" text-anchor="middle" fill="white" font-size="10">Cross-namespace</text>
  <rect x="440" y="80" width="150" height="80" fill="#fbbc04" rx="5"/>
  <text x="515" y="110" text-anchor="middle" font-weight="bold">RoleBinding</text>
  <text x="515" y="130" text-anchor="middle" font-size="10">Bind Role to users</text>
  <text x="515" y="150" text-anchor="middle" font-size="10">Namespace scoped</text>
  <rect x="610" y="80" width="140" height="80" fill="#ea4335" rx="5"/>
  <text x="680" y="110" text-anchor="middle" fill="white" font-weight="bold">ClusterRoleBinding</text>
  <text x="680" y="130" text-anchor="middle" fill="white" font-size="9">Bind ClusterRole</text>
  <text x="680" y="150" text-anchor="middle" fill="white" font-size="10">Cluster wide</text>
  <rect x="250" y="200" width="300" height="100" fill="#e8f5e9" rx="5"/>
  <text x="400" y="230" text-anchor="middle" font-weight="bold">Subjects</text>
  <text x="400" y="255" text-anchor="middle" font-size="12">• Users</text>
  <text x="400" y="275" text-anchor="middle" font-size="12">• Groups</text>
  <text x="400" y="295" text-anchor="middle" font-size="12">• ServiceAccounts</text>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Pod Security Standards</text>
  <rect x="100" y="80" width="200" height="150" fill="#34a853" rx="5"/>
  <text x="200" y="110" text-anchor="middle" fill="white" font-weight="bold">Privileged</text>
  <text x="200" y="135" text-anchor="middle" fill="white" font-size="11">• Unrestricted</text>
  <text x="200" y="155" text-anchor="middle" fill="white" font-size="11">• No limitations</text>
  <text x="200" y="175" text-anchor="middle" fill="white" font-size="11">• System pods</text>
  <text x="200" y="195" text-anchor="middle" fill="white" font-size="11">• Least secure</text>
  <rect x="320" y="80" width="200" height="150" fill="#fbbc04" rx="5"/>
  <text x="420" y="110" text-anchor="middle" font-weight="bold">Baseline</text>
  <text x="420" y="135" text-anchor="middle" font-size="11">• Minimal restrictions</text>
  <text x="420" y="155" text-anchor="middle" font-size="11">• Prevents escalations</text>
  <text x="420" y="175" text-anchor="middle" font-size="11">• Default for most</text>
  <text x="420" y="195" text-anchor="middle" font-size="11">• Moderate security</text>
  <rect x="540" y="80" width="200" height="150" fill="#ea4335" rx="5"/>
  <text x="640" y="110" text-anchor="middle" fill="white" font-weight="bold">Restricted</text>
  <text x="640" y="135" text-anchor="middle" fill="white" font-size="11">• Heavily restricted</text>
  <text x="640" y="155" text-anchor="middle" fill="white" font-size="11">• Security hardened</text>
  <text x="640" y="175" text-anchor="middle" fill="white" font-size="11">• Best practices</text>
  <text x="640" y="195" text-anchor="middle" fill="white" font-size="11">• Most secure</text>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f9f9f9" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Security Tools</text>
  <rect x="100" y="80" width="150" height="80" fill="#4285f4" rx="5"/>
  <text x="175" y="110" text-anchor="middle" fill="white" font-weight="bold">Trivy</text>
  <text x="175" y="130" text-anchor="middle" fill="white" font-size="10">Image scanning</text>
  <text x="175" y="150" text-anchor="middle" fill="white" font-size="10">Config audit</text>
  <rect x="270" y="80" width="150" height="80" fill="#34a853" rx="5"/>
  <text x="345" y="110" text-anchor="middle" fill="white" font-weight="bold">Kubesec</text>
  <text x="345" y="130" text-anchor="middle" fill="white" font-size="10">Manifest analysis</text>
  <text x="345" y="150" text-anchor="middle" fill="white" font-size="10">Security score</text>
  <rect x="440" y="80" width="150" height="80" fill="#fbbc04" rx="5"/>
  <text x="515" y="110" text-anchor="middle" font-weight="bold">kube-bench</text>
  <text x="515" y="130" text-anchor="middle" font-size="10">CIS benchmark</text>
  <text x="515" y="150" text-anchor="middle" font-size="10">Compliance check</text>
  <rect x="610" y="80" width="140" height="80" fill="#ea4335" rx="5"/>
  <text x="680" y="110" text-anchor="middle" fill="white" font-weight="bold">Polaris</text>
  <text x="680" y="130" text-anchor="middle" fill="white" font-size="10">Best practices</text>
  <text x="680" y="150" text-anchor="middle" fill="white" font-size="10">Validation</text>
</svg>

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
