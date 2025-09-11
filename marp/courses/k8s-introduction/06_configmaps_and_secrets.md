# ConfigMaps and Secrets

---

## Configuration Management

1. **Separate** configuration from code
1. **Environment-specific** settings
1. **Centralized** configuration
1. **Dynamic** updates possible
1. **Version** controlled

---

## Why External Configuration?

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Configuration Management</text>
  <rect x="100" y="80" width="200" height="100" fill="#ea4335" rx="5"/>
  <text x="200" y="110" text-anchor="middle" fill="white" font-weight="bold">Hardcoded Config</text>
  <text x="200" y="135" text-anchor="middle" fill="white" font-size="11">❌ Rebuild for changes</text>
  <text x="200" y="155" text-anchor="middle" fill="white" font-size="11">❌ Environment specific</text>
  <text x="200" y="175" text-anchor="middle" fill="white" font-size="11">❌ Security risks</text>
  <rect x="350" y="80" width="200" height="100" fill="#34a853" rx="5"/>
  <text x="450" y="110" text-anchor="middle" fill="white" font-weight="bold">External Config</text>
  <text x="450" y="135" text-anchor="middle" fill="white" font-size="11">✓ No rebuild needed</text>
  <text x="450" y="155" text-anchor="middle" fill="white" font-size="11">✓ Environment agnostic</text>
  <text x="450" y="175" text-anchor="middle" fill="white" font-size="11">✓ Secure secrets</text>
  <rect x="100" y="220" width="600" height="80" fill="#fff3e0" rx="5"/>
  <text x="400" y="250" text-anchor="middle" font-weight="bold">Kubernetes Solution</text>
  <text x="400" y="275" text-anchor="middle" font-size="12">ConfigMaps for non-sensitive data | Secrets for sensitive data</text>
</svg>

---

## ConfigMaps Overview

1. **Store** non-confidential data
1. **Key-value** pairs
1. **Decouple** configuration from images
1. **Update** without rebuilding
1. **Mount** as files or environment variables

---

## Creating ConfigMaps - Literal

```bash
# From literal values
kubectl create configmap app-config \
  --from-literal=database_url=postgres://localhost/mydb \
  --from-literal=feature_flag=true

# View configmap
kubectl get configmap app-config -o yaml
```

---

## Creating ConfigMaps - File

```bash
# From file
kubectl create configmap app-config \
  --from-file=application.properties

# From directory
kubectl create configmap app-config \
  --from-file=config/

# With custom key
kubectl create configmap app-config \
  --from-file=app.conf=application.properties
```

---

## ConfigMap YAML

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  database_url: "postgres://localhost/mydb"
  log_level: "info"
  max_connections: "100"
  config.yaml: |
    server:
      port: 8080
      host: 0.0.0.0
    features:
      newUI: true
      analytics: false
```

---

## Using ConfigMaps - Environment

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    image: myapp
    env:
    - name: DATABASE_URL
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: database_url
    - name: LOG_LEVEL
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: log_level
```

---

## Using ConfigMaps - EnvFrom

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    image: myapp
    envFrom:
    - configMapRef:
        name: app-config
    - configMapRef:
        name: feature-flags
        prefix: FEATURE_  # Optional prefix
```

---

## Using ConfigMaps - Volume

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    image: myapp
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config
  volumes:
  - name: config-volume
    configMap:
      name: app-config
```

---

## ConfigMap Volume Options

```yaml
volumes:
- name: config-volume
  configMap:
    name: app-config
    items:  # Selective mounting
    - key: config.yaml
      path: app.yaml  # Custom filename
      mode: 0644      # File permissions
    - key: database_url
      path: db.conf
    defaultMode: 0644  # Default permissions
```

---

## ConfigMap Usage Patterns

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f9f9f9" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">ConfigMap Usage Patterns</text>
  <rect x="100" y="80" width="200" height="100" fill="#4285f4" rx="5"/>
  <text x="200" y="110" text-anchor="middle" fill="white" font-weight="bold">Environment Variables</text>
  <text x="200" y="135" text-anchor="middle" fill="white" font-size="11">Simple key-value</text>
  <text x="200" y="155" text-anchor="middle" fill="white" font-size="11">DATABASE_URL=...</text>
  <text x="200" y="175" text-anchor="middle" fill="white" font-size="11">LOG_LEVEL=debug</text>
  <rect x="320" y="80" width="200" height="100" fill="#34a853" rx="5"/>
  <text x="420" y="110" text-anchor="middle" fill="white" font-weight="bold">Configuration Files</text>
  <text x="420" y="135" text-anchor="middle" fill="white" font-size="11">Complex configs</text>
  <text x="420" y="155" text-anchor="middle" fill="white" font-size="11">nginx.conf</text>
  <text x="420" y="175" text-anchor="middle" fill="white" font-size="11">application.yaml</text>
  <rect x="540" y="80" width="200" height="100" fill="#fbbc04" rx="5"/>
  <text x="640" y="110" text-anchor="middle" font-weight="bold">Command Arguments</text>
  <text x="640" y="135" text-anchor="middle" font-size="11">Container args</text>
  <text x="640" y="155" text-anchor="middle" font-size="11">--config=/etc/app</text>
  <text x="640" y="175" text-anchor="middle" font-size="11">--verbose=true</text>
  <rect x="200" y="220" width="400" height="80" fill="#e8f5e9" rx="5"/>
  <text x="400" y="250" text-anchor="middle" font-weight="bold">Update Behavior</text>
  <text x="400" y="275" text-anchor="middle" font-size="12">Env vars: Require pod restart | Volume mounts: Auto-update (eventually)</text>
</svg>

---

## Secrets Overview

1. **Store** sensitive information
1. **Base64** encoded (not encrypted!)
1. **Size limit**: 1MB
1. **Types**: Opaque, Docker, TLS, etc.
1. **RBAC** controlled access

---

## Secret Types

```yaml
# Opaque (default)
type: Opaque

# Docker registry
type: kubernetes.io/dockerconfigjson

# TLS certificate
type: kubernetes.io/tls

# Service account token
type: kubernetes.io/service-account-token

# Basic auth
type: kubernetes.io/basic-auth

# SSH auth
type: kubernetes.io/ssh-auth
```

---

## Creating Secrets - Generic

```bash
# From literal
kubectl create secret generic db-secret \
  --from-literal=username=admin \
  --from-literal=password=secretpass

# From file
kubectl create secret generic db-secret \
  --from-file=username.txt \
  --from-file=password.txt

# From env file
kubectl create secret generic db-secret \
  --from-env-file=secrets.env
```

---

## Creating Secrets - Docker

```bash
# Docker registry secret
kubectl create secret docker-registry regcred \
  --docker-server=https://index.docker.io/v1/ \
  --docker-username=myuser \
  --docker-password=mypass \
  --docker-email=myemail@example.com

# From existing docker config
kubectl create secret generic regcred \
  --from-file=.dockerconfigjson=$HOME/.docker/config.json \
  --type=kubernetes.io/dockerconfigjson
```

---

## Creating Secrets - TLS

```bash
# TLS secret
kubectl create secret tls tls-secret \
  --cert=path/to/tls.crt \
  --key=path/to/tls.key

# Generate self-signed cert
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout tls.key -out tls.crt -subj "/CN=myapp.local"

kubectl create secret tls myapp-tls \
  --cert=tls.crt --key=tls.key
```

---

## Secret YAML

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  username: YWRtaW4=  # base64 encoded "admin"
  password: c2VjcmV0cGFzcw==  # base64 encoded "secretpass"

# Or use stringData (auto-encoded)
stringData:
  username: admin
  password: secretpass
```

---

## Using Secrets - Environment

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    image: myapp
    env:
    - name: DB_USERNAME
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: username
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: password
```

---

## Using Secrets - Volume

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    image: myapp
    volumeMounts:
    - name: secret-volume
      mountPath: /etc/secrets
      readOnly: true
  volumes:
  - name: secret-volume
    secret:
      secretName: db-secret
      defaultMode: 0400  # Read-only for owner
```

---

## Using Docker Registry Secret

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
    image: private-registry.io/myapp:latest
```

---

## Secret vs ConfigMap

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">ConfigMap vs Secret</text>
  <rect x="100" y="80" width="300" height="200" fill="#4285f4" rx="5"/>
  <text x="250" y="110" text-anchor="middle" fill="white" font-weight="bold">ConfigMap</text>
  <text x="250" y="135" text-anchor="middle" fill="white" font-size="11">✓ Non-sensitive data</text>
  <text x="250" y="155" text-anchor="middle" fill="white" font-size="11">✓ Plain text storage</text>
  <text x="250" y="175" text-anchor="middle" fill="white" font-size="11">✓ Application settings</text>
  <text x="250" y="195" text-anchor="middle" fill="white" font-size="11">✓ Feature flags</text>
  <text x="250" y="215" text-anchor="middle" fill="white" font-size="11">✓ Config files</text>
  <text x="250" y="235" text-anchor="middle" fill="white" font-size="11">✓ No size limit concerns</text>
  <text x="250" y="255" text-anchor="middle" fill="white" font-size="11">Example: app.properties</text>
  <rect x="420" y="80" width="300" height="200" fill="#ea4335" rx="5"/>
  <text x="570" y="110" text-anchor="middle" fill="white" font-weight="bold">Secret</text>
  <text x="570" y="135" text-anchor="middle" fill="white" font-size="11">✓ Sensitive data</text>
  <text x="570" y="155" text-anchor="middle" fill="white" font-size="11">✓ Base64 encoded</text>
  <text x="570" y="175" text-anchor="middle" fill="white" font-size="11">✓ Passwords, tokens</text>
  <text x="570" y="195" text-anchor="middle" fill="white" font-size="11">✓ TLS certificates</text>
  <text x="570" y="215" text-anchor="middle" fill="white" font-size="11">✓ SSH keys</text>
  <text x="570" y="235" text-anchor="middle" fill="white" font-size="11">✓ 1MB size limit</text>
  <text x="570" y="255" text-anchor="middle" fill="white" font-size="11">Example: db-password</text>
</svg>

---

## Immutable ConfigMaps and Secrets

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  key: value
immutable: true  # Cannot be updated

---
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
data:
  password: cGFzc3dvcmQ=
immutable: true  # Cannot be updated
```

---

## Benefits of Immutability

1. **Protection** from accidental updates
1. **Performance** improvement (no watches)
1. **Predictable** deployments
1. **Version** control via new names
1. **Rollback** capability

---

## ConfigMap/Secret Updates

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="30" text-anchor="middle" font-size="16" font-weight="bold">Update Propagation</text>
  <rect x="100" y="60" width="150" height="60" fill="#4285f4" rx="5"/>
  <text x="175" y="95" text-anchor="middle" fill="white">ConfigMap Updated</text>
  <rect x="100" y="150" width="250" height="60" fill="#34a853" rx="5"/>
  <text x="225" y="175" text-anchor="middle" fill="white">Volume Mount</text>
  <text x="225" y="195" text-anchor="middle" fill="white" font-size="10">Updates in ~1 minute</text>
  <rect x="100" y="240" width="250" height="60" fill="#ea4335" rx="5"/>
  <text x="225" y="265" text-anchor="middle" fill="white">Environment Variable</text>
  <text x="225" y="285" text-anchor="middle" fill="white" font-size="10">Requires pod restart</text>
  <rect x="400" y="150" width="300" height="120" fill="#fff3e0" rx="5"/>
  <text x="550" y="180" text-anchor="middle" font-weight="bold">Update Strategy</text>
  <text x="550" y="205" text-anchor="middle" font-size="11">1. Create new ConfigMap version</text>
  <text x="550" y="225" text-anchor="middle" font-size="11">2. Update deployment to use new version</text>
  <text x="550" y="245" text-anchor="middle" font-size="11">3. Rolling update applies changes</text>
  <path d="M 250 90 L 345 175" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 250 90 L 345 265" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
</svg>

---

## Projected Volumes

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    volumeMounts:
    - name: all-configs
      mountPath: /etc/config
  volumes:
  - name: all-configs
    projected:
      sources:
      - configMap:
          name: app-config
      - secret:
          name: app-secret
      - downwardAPI:
          items:
          - path: "labels"
            fieldRef:
              fieldPath: metadata.labels
```

---

## Encryption at Rest

```bash
# Enable encryption at rest (API server config)
--encryption-provider-config=/path/to/encryption-config.yaml

# Encryption config example
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
```

---

## External Secret Management

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f9f9f9" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">External Secret Solutions</text>
  <rect x="100" y="80" width="150" height="80" fill="#4285f4" rx="5"/>
  <text x="175" y="110" text-anchor="middle" fill="white" font-weight="bold">HashiCorp Vault</text>
  <text x="175" y="135" text-anchor="middle" fill="white" font-size="11">Dynamic secrets</text>
  <text x="175" y="150" text-anchor="middle" fill="white" font-size="11">Rotation</text>
  <rect x="270" y="80" width="150" height="80" fill="#34a853" rx="5"/>
  <text x="345" y="110" text-anchor="middle" fill="white" font-weight="bold">AWS Secrets</text>
  <text x="345" y="135" text-anchor="middle" fill="white" font-size="11">Manager</text>
  <text x="345" y="150" text-anchor="middle" fill="white" font-size="11">IAM integration</text>
  <rect x="440" y="80" width="150" height="80" fill="#fbbc04" rx="5"/>
  <text x="515" y="110" text-anchor="middle" font-weight="bold">Azure Key Vault</text>
  <text x="515" y="135" text-anchor="middle" font-size="11">Managed service</text>
  <text x="515" y="150" text-anchor="middle" font-size="11">HSM support</text>
  <rect x="610" y="80" width="140" height="80" fill="#ea4335" rx="5"/>
  <text x="680" y="110" text-anchor="middle" fill="white" font-weight="bold">Sealed Secrets</text>
  <text x="680" y="135" text-anchor="middle" fill="white" font-size="11">GitOps friendly</text>
  <text x="680" y="150" text-anchor="middle" fill="white" font-size="11">Encrypted</text>
  <rect x="200" y="200" width="400" height="100" fill="#e8f5e9" rx="5"/>
  <text x="400" y="230" text-anchor="middle" font-weight="bold">Integration Methods</text>
  <text x="400" y="255" text-anchor="middle" font-size="12">• Sidecar injector pattern</text>
  <text x="400" y="275" text-anchor="middle" font-size="12">• CSI driver for secrets</text>
</svg>

---

## Sealed Secrets Example

```bash
# Install sealed-secrets controller
kubectl apply -f https://github.com/bitnami-labs/\
sealed-secrets/releases/download/v0.18.0/controller.yaml

# Install kubeseal CLI
wget https://github.com/bitnami-labs/sealed-secrets/\
releases/download/v0.18.0/kubeseal-linux-amd64
chmod +x kubeseal-linux-amd64
sudo mv kubeseal-linux-amd64 /usr/local/bin/kubeseal

# Create sealed secret
echo -n mypassword | kubectl create secret generic \
  mysecret --dry-run=client --from-file=password=/dev/stdin \
  -o yaml | kubeseal -o yaml > sealed-secret.yaml
```

---

## Best Practices - ConfigMaps

1. **Version** ConfigMaps with names
1. **Use** immutable when possible
1. **Separate** by environment
1. **Document** configuration options
1. **Validate** before deployment

---

## Best Practices - Secrets

1. **Enable** encryption at rest
1. **Use** RBAC to limit access
1. **Rotate** secrets regularly
1. **Avoid** committing to Git
1. **Consider** external secret managers

---

## Anti-patterns to Avoid

1. **Don't** store secrets in ConfigMaps
1. **Don't** log secret values
1. **Don't** use default service account
1. **Don't** share secrets across namespaces
1. **Don't** hardcode in images

---

## Debugging ConfigMaps/Secrets

```bash
# List all configmaps
kubectl get configmaps

# Describe configmap
kubectl describe configmap app-config

# View configmap data
kubectl get configmap app-config -o yaml

# List secrets (names only)
kubectl get secrets

# Decode secret
kubectl get secret db-secret -o jsonpath=\
'{.data.password}' | base64 -d
```

---

## Troubleshooting Common Issues

1. **Key not found**: Check spelling and case
1. **Permission denied**: Check RBAC
1. **Not updating**: Check mount vs env var
1. **Size limit**: Keep under 1MB
1. **Base64 errors**: Proper encoding

---

## ConfigMap/Secret Backup

```bash
# Backup all configmaps
kubectl get configmaps --all-namespaces -o yaml > configmaps-backup.yaml

# Backup all secrets
kubectl get secrets --all-namespaces -o yaml > secrets-backup.yaml

# Restore
kubectl apply -f configmaps-backup.yaml
kubectl apply -f secrets-backup.yaml
```

---

## Environment-Specific Config

```yaml
# dev-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: development
data:
  api_url: "https://dev-api.example.com"
  debug: "true"

---
# prod-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: production
data:
  api_url: "https://api.example.com"
  debug: "false"
```

---

## Kustomize for Config Management

```yaml
# kustomization.yaml
configMapGenerator:
- name: app-config
  literals:
  - database_url=postgres://localhost/mydb
  - cache_size=100
  files:
  - application.properties

secretGenerator:
- name: db-secret
  literals:
  - username=admin
  - password=secretpass
```

---

## Summary

1. ConfigMaps store non-sensitive configuration
1. Secrets store sensitive data (base64 encoded)
1. Both support env vars and volume mounts
1. Updates behave differently for each method
1. Consider external secret management for production
