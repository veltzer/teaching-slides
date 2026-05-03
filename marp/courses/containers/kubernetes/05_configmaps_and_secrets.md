---
tags:
  - infrastructure:kubernetes
level: intermediate
category: containers
audience:
  - audiences:developers

---
# ConfigMaps and Secrets

---
## What This Chapter Covers

- ConfigMap
- Secret
- Mounting as env or file
- Updates
- External secret managers
- Best practices

---
## Compare and Contrast

![config_secret](svg/courses/containers/kubernetes/05_configmaps_and_secrets/config_secret.svg)

---
## ConfigMap

- Key-value pairs
- For non-secret config
- Per-namespace
- Mountable as env vars or files

---
## Sample ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  LOG_LEVEL: info
  database_url: postgres://db:5432/app
```

---
## Mount As Env

```yaml
envFrom:
- configMapRef:
    name: app-config
```

Or per-key:

```yaml
env:
- name: LOG_LEVEL
  valueFrom:
    configMapKeyRef:
      name: app-config
      key: LOG_LEVEL
```

---
## Mount As File

```yaml
volumes:
- name: config
  configMap:
    name: app-config
volumeMounts:
- name: config
  mountPath: /etc/app
```

- Each key becomes a file

---
## Secret

- Like ConfigMap, but base64-encoded
- For sensitive values
- "Encoded" not "encrypted" by default
- Combine with: encryption at rest, RBAC

---
## Two Object Types

![configmap_vs_secret](svg/courses/containers/kubernetes/05_configmaps_and_secrets/configmap_vs_secret.svg)

---
## Sample Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-password
type: Opaque
data:
  password: cGFzc3dvcmQ=  # base64
```

---
## Mounting Secrets

- Same as ConfigMap (env or file)
- File mount: more secure (can be read-only)
- Don't print secret env vars in logs

---
## Updates

- Edit and apply: pods don't restart automatically
- File mounts: kubelet syncs (eventually)
- Env: requires pod restart
- Use a tool like Reloader to auto-restart on change

---
## Encryption At Rest

- Default: secrets in etcd in plaintext
- Enable encryption-at-rest at the cluster level
- Cloud (EKS, GKE, AKS): can use cloud KMS

---
## External Secrets

- Don't store secrets in K8s; reference them
- HashiCorp Vault, AWS Secrets Manager
- External Secrets Operator: syncs to K8s Secret
- Standard for production

---
## Sealed Secrets

- Encrypt secrets in YAML; safe to commit
- Bitnami Sealed Secrets
- Decrypted only by the in-cluster controller
- GitOps-friendly

---
## Best Practices

- Per-environment configs (dev, staging, prod)
- Don't commit raw secrets
- RBAC to limit who reads secrets
- Audit secret access
- Rotate periodically

---
## Common ConfigMap / Secret Mistakes

- Putting secrets in ConfigMaps
- Mounting all secrets (LMP), one wins
- Storing config in image (not configurable)
- No encryption at rest
- Logging secrets accidentally
