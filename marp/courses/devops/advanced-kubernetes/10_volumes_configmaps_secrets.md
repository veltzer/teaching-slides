# Advanced Volumes, `ConfigMaps` & `Secrets`

Advanced Kubernetes Course - Day 2, Module 5

---

## Module Overview

- Volume types and lifecycle
- `PersistentVolumes` and `PersistentVolumeClaims`
- Storage classes and dynamic provisioning
- `CSI` drivers
- `ConfigMaps` and `Secrets` deep dive
- External secret management

---

## Volume Types Overview

| Type | Persistence | Use Case |
|------|-------------|----------|
| `emptyDir` | Pod lifetime | Temp data, shared between containers |
| `hostPath` | Node lifetime | Node-level access (testing only) |
| `configMap` | Cluster lifetime | Configuration files |
| `secret` | Cluster lifetime | Sensitive data |
| `persistentVolumeClaim` | Independent | Databases, stateful apps |
| `projected` | Varies | Combine multiple sources |
| `csi` | Varies | Custom storage via `CSI` |

---

## `PersistentVolume` and `PersistentVolumeClaim`

![persistentvolume_and_persistentvolumeclaim](/svg/courses/devops/advanced-kubernetes/10_volumes_configmaps_secrets/persistentvolume_and_persistentvolumeclaim.svg)

---

## `PersistentVolume` Specification

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfs-pv
spec:
  capacity:
    storage: 100Gi
  accessModes:
  - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: nfs
  mountOptions:
  - hard
  - nfsvers=4.1
  nfs:
    server: nfs-server.example.com
    path: /exports/data
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: nfs-claim
spec:
  accessModes:
  - ReadWriteMany
  storageClassName: nfs
  resources:
    requests:
      storage: 50Gi
```

---

## Access Modes

| Mode | Abbreviation | Description |
|------|-------------|-------------|
| `ReadWriteOnce` | `RWO` | Single node read-write |
| `ReadOnlyMany` | `ROX` | Multiple nodes read-only |
| `ReadWriteMany` | `RWX` | Multiple nodes read-write |
| `ReadWriteOncePod` | `RWOP` | Single pod read-write |

```misc
RWO:  Node1[Pod-A] ✓   Node2[Pod-B] ✗
ROX:  Node1[Pod-A] R    Node2[Pod-B] R
RWX:  Node1[Pod-A] RW   Node2[Pod-B] RW
RWOP: Pod-A RW           Pod-B ✗
```

---

## Reclaim Policies

| Policy | Behavior |
|--------|----------|
| `Retain` | Keep PV and data after PVC deletion |
| `Delete` | Delete PV and underlying storage |
| `Recycle` | Deprecated, use dynamic provisioning |

```bash
# Check PV status
kubectl get pv
NAME     CAPACITY   ACCESS   RECLAIM    STATUS      CLAIM
nfs-pv   100Gi      RWX      Retain     Bound       default/nfs-claim
data-pv  50Gi       RWO      Delete     Released    -
```

---

## `StorageClass` - Dynamic Provisioning

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
  annotations:
    storageclass.kubernetes.io/is-default-class: "false"
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  iops: "5000"
  throughput: "250"
  encrypted: "true"
  kmsKeyId: "arn:aws:kms:us-east-1:123:key/abc"
reclaimPolicy: Delete
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer
mountOptions:
- noatime
```

---

## Volume Expansion

```yaml
# StorageClass must have allowVolumeExpansion: true

# Expand by editing the PVC
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: database-data
spec:
  accessModes: [ReadWriteOnce]
  storageClassName: fast-ssd
  resources:
    requests:
      storage: 200Gi    # was 100Gi
```

```bash
kubectl patch pvc database-data -p \
  '{"spec":{"resources":{"requests":{"storage":"200Gi"}}}}'

# Check resize status
kubectl get pvc database-data
kubectl describe pvc database-data | grep Conditions
```

> Note: Shrinking volumes is **not** supported.

---

## Volume Snapshots

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: db-snapshot-20240315
spec:
  volumeSnapshotClassName: csi-aws-snapclass
  source:
    persistentVolumeClaimName: database-data
---
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshotClass
metadata:
  name: csi-aws-snapclass
driver: ebs.csi.aws.com
deletionPolicy: Retain
---
# Restore from snapshot
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: database-data-restored
spec:
  accessModes: [ReadWriteOnce]
  storageClassName: fast-ssd
  resources:
    requests:
      storage: 100Gi
  dataSource:
    name: db-snapshot-20240315
    kind: VolumeSnapshot
    apiGroup: snapshot.storage.k8s.io
```

---

## `CSI` Driver Architecture

![csi_driver_architecture](/svg/courses/devops/advanced-kubernetes/10_volumes_configmaps_secrets/csi_driver_architecture.svg)

---

## `ConfigMaps` - Creation Methods

```bash
# From literal values
kubectl create configmap app-config \
  --from-literal=DATABASE_HOST=postgres \
  --from-literal=DATABASE_PORT=5432 \
  --from-literal=LOG_LEVEL=info

# From file
kubectl create configmap nginx-config \
  --from-file=nginx.conf

# From directory
kubectl create configmap app-configs \
  --from-file=config/

# From env file
kubectl create configmap env-config \
  --from-env-file=.env.production
```

---

## `ConfigMap` YAML

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: production
data:
  # Simple key-value pairs
  DATABASE_HOST: "postgres.production.svc"
  DATABASE_PORT: "5432"
  LOG_LEVEL: "info"
  CACHE_TTL: "300"

  # Multi-line config file
  app.yaml: |
    server:
      port: 8080
      read_timeout: 30s
      write_timeout: 30s
    database:
      max_connections: 100
      idle_timeout: 10m
    logging:
      format: json
      level: info

  # Another config file
  nginx.conf: |
    server {
        listen 80;
        server_name _;
        location / {
            proxy_pass http://localhost:8080;
        }
    }
```

---

## Using `ConfigMaps`

**As environment variables:**
```yaml
spec:
  containers:
  - name: app
    envFrom:
    - configMapRef:
        name: app-config
    env:
    - name: SPECIFIC_KEY
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: DATABASE_HOST
```

**As volume mount:**
```yaml
spec:
  containers:
  - name: app
    volumeMounts:
    - name: config
      mountPath: /etc/app
      readOnly: true
  volumes:
  - name: config
    configMap:
      name: app-config
      items:
      - key: app.yaml
        path: config.yaml
      - key: nginx.conf
        path: nginx.conf
```

---

## `ConfigMap` Auto-Reload

Volume-mounted `ConfigMaps` are updated automatically (with delay):

```yaml
spec:
  containers:
  - name: app
    volumeMounts:
    - name: config
      mountPath: /etc/app
  - name: config-reloader
    image: jimmidyson/configmap-reload:v0.9.0
    args:
    - --volume-dir=/etc/app
    - --webhook-url=http://localhost:8080/-/reload
    - --webhook-method=POST
    volumeMounts:
    - name: config
      mountPath: /etc/app
      readOnly: true
  volumes:
  - name: config
    configMap:
      name: app-config
```

> Environment variables from `ConfigMaps` are **NOT** auto-updated.

---

## `Secrets` - Types

| Type | Usage |
|------|-------|
| `Opaque` | Arbitrary data (default) |
| `kubernetes.io/tls` | TLS certificate + key |
| `kubernetes.io/dockerconfigjson` | Docker registry auth |
| `kubernetes.io/basic-auth` | Username + password |
| `kubernetes.io/ssh-auth` | SSH private key |
| `kubernetes.io/service-account-token` | SA token |

---

## Creating `Secrets`

```bash
# Generic secret
kubectl create secret generic db-credentials \
  --from-literal=username=admin \
  --from-literal=password='S3cur3P@ss!'

# TLS secret
kubectl create secret tls app-tls \
  --cert=tls.crt \
  --key=tls.key

# Docker registry secret
kubectl create secret docker-registry regcred \
  --docker-server=registry.example.com \
  --docker-username=user \
  --docker-password=pass
```

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
type: Opaque
stringData:          # Plain text (encoded on apply)
  username: admin
  password: S3cur3P@ss!
  connection-string: |
    host=postgres port=5432 dbname=myapp
    user=admin password=S3cur3P@ss!
```

---

## `Secret` Security Considerations

**By default, `Secrets` are NOT encrypted at rest!**

Enable encryption:
```yaml
# /etc/kubernetes/enc/enc.yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
- resources:
  - secrets
  providers:
  - aescbc:
      keys:
      - name: key1
        secret: <base64-encoded-32-byte-key>
  - identity: {}
```

```bash
# Add to kube-apiserver args:
--encryption-provider-config=/etc/kubernetes/enc/enc.yaml

# Encrypt existing secrets
kubectl get secrets --all-namespaces -o json | \
  kubectl replace -f -
```

---

## External Secrets Operator

```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-secrets-manager
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: external-secrets-sa
---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: SecretStore
  target:
    name: db-credentials
    creationPolicy: Owner
  data:
  - secretKey: username
    remoteRef:
      key: production/database
      property: username
  - secretKey: password
    remoteRef:
      key: production/database
      property: password
```

---

## Projected Volumes

Combine multiple sources into one mount:

```yaml
spec:
  containers:
  - name: app
    volumeMounts:
    - name: all-in-one
      mountPath: /etc/app
      readOnly: true
  volumes:
  - name: all-in-one
    projected:
      sources:
      - configMap:
          name: app-config
          items:
          - key: app.yaml
            path: config.yaml
      - secret:
          name: db-credentials
          items:
          - key: password
            path: db-password
      - serviceAccountToken:
          audience: vault
          expirationSeconds: 3600
          path: token
      - downwardAPI:
          items:
          - path: labels
            fieldRef:
              fieldPath: metadata.labels
```

---

## Immutable `ConfigMaps` and `Secrets`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config-v2
immutable: true
data:
  DATABASE_HOST: "postgres.production.svc"
  LOG_LEVEL: "info"
```

Benefits:
- Protects against accidental changes
- Reduces `API` server load (no watch needed)
- Improves cluster performance at scale

> To update: create a new `ConfigMap` with new name, update pod spec.

---

## Lab: Storage and Configuration

```bash
# 1. Create a StorageClass
kubectl apply -f fast-ssd-storageclass.yaml

# 2. Create PVC and verify dynamic provisioning
kubectl apply -f database-pvc.yaml
kubectl get pvc,pv

# 3. Create ConfigMap and Secret
kubectl apply -f app-config.yaml
kubectl create secret generic db-creds \
  --from-literal=password=secret123

# 4. Deploy app using volumes, ConfigMaps, Secrets
kubectl apply -f full-app-deployment.yaml

# 5. Update ConfigMap and verify hot-reload
kubectl edit configmap app-config

# 6. Take a volume snapshot
kubectl apply -f volume-snapshot.yaml
```
