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

![why_external_configuration](svg/courses/devops/k8s-introduction/07_configmaps_and_secrets/why_external_configuration.svg)

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

![configmap_usage_patterns](svg/courses/devops/k8s-introduction/07_configmaps_and_secrets/configmap_usage_patterns.svg)

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

![secret_vs_configmap](svg/courses/devops/k8s-introduction/07_configmaps_and_secrets/secret_vs_configmap.svg)

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

![configmap_secret_updates](svg/courses/devops/k8s-introduction/07_configmaps_and_secrets/configmap_secret_updates.svg)

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

![external_secret_management](svg/courses/devops/k8s-introduction/07_configmaps_and_secrets/external_secret_management.svg)

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
