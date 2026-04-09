# Volumes and Storage

---

## Storage Overview

1. **Ephemeral**: Container filesystem
1. **Volumes**: Pod-level storage
1. **PersistentVolumes**: Cluster resources
1. **PersistentVolumeClaims**: Storage requests
1. **StorageClasses**: Dynamic provisioning

---

## Why Persistent Storage?

![why_persistent_storage](svg/courses/devops/k8s-introduction/10_volumes_and_storage/why_persistent_storage.svg)

---

## Volume Types

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    volumeMounts:
    - name: data
      mountPath: /data
  volumes:
  - name: data
    # Volume type options:
    emptyDir: {}
    # hostPath:
    # configMap:
    # secret:
    # persistentVolumeClaim:
```

---

## emptyDir Volume

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pd
spec:
  containers:
  - name: test-container
    image: nginx
    volumeMounts:
    - mountPath: /cache
      name: cache-volume
  volumes:
  - name: cache-volume
    emptyDir: {}
    # Or with size limit:
    # emptyDir:
    #   sizeLimit: 1Gi
```

---

## emptyDir Characteristics

![emptydir_characteristics](svg/courses/devops/k8s-introduction/10_volumes_and_storage/emptydir_characteristics.svg)

---

## hostPath Volume

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-hostpath
spec:
  containers:
  - name: test-container
    image: nginx
    volumeMounts:
    - mountPath: /test-pd
      name: test-volume
  volumes:
  - name: test-volume
    hostPath:
      path: /data
      type: DirectoryOrCreate
```

---

## hostPath Types

```yaml
hostPath:
  path: /data
  type: DirectoryOrCreate
  # Types:
  # DirectoryOrCreate - Create if doesn't exist
  # Directory - Must exist
  # FileOrCreate - Create file if doesn't exist
  # File - File must exist
  # Socket - Unix socket must exist
  # CharDevice - Character device must exist
  # BlockDevice - Block device must exist
```

---

## PersistentVolume (PV)

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-volume
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: manual
  hostPath:
    path: /mnt/data
```

---

## Access Modes

![access_modes](svg/courses/devops/k8s-introduction/10_volumes_and_storage/access_modes.svg)

---

## PersistentVolumeClaim (PVC)

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-claim
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: manual
  # Optional: bind to specific PV
  # volumeName: pv-volume
```

---

## PV and PVC Binding

![pv_and_pvc_binding](svg/courses/devops/k8s-introduction/10_volumes_and_storage/pv_and_pvc_binding.svg)

---

## Using PVC in Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
  - name: myapp
    image: nginx
    volumeMounts:
    - mountPath: /data
      name: mypd
  volumes:
  - name: mypd
    persistentVolumeClaim:
      claimName: pvc-claim
```

---

## Reclaim Policies

```yaml
persistentVolumeReclaimPolicy: Retain
# Options:
# Retain - Keep PV after PVC deleted (default)
# Delete - Delete PV and storage
# Recycle - Scrub and make available (deprecated)
```

---

## StorageClass

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  iops: "10000"
  throughput: "250"
reclaimPolicy: Delete
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer
```

---

## Dynamic Provisioning

![dynamic_provisioning](svg/courses/devops/k8s-introduction/10_volumes_and_storage/dynamic_provisioning.svg)

---

## Volume Binding Modes

```yaml
volumeBindingMode: Immediate  # Bind immediately
# or
volumeBindingMode: WaitForFirstConsumer  # Wait for pod

# WaitForFirstConsumer benefits:
# - Provision in correct zone
# - Avoid unschedulable pods
# - Better for multi-zone clusters
```

---

## StatefulSet Storage

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  serviceName: "nginx"
  replicas: 3
  template:
    spec:
      containers:
      - name: nginx
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: "fast-ssd"
      resources:
        requests:
          storage: 1Gi
```

---

## StatefulSet PVC Pattern

![statefulset_pvc_pattern](svg/courses/devops/k8s-introduction/10_volumes_and_storage/statefulset_pvc_pattern.svg)

---

## CSI (Container Storage Interface)

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: csi-storage
provisioner: ebs.csi.aws.com  # CSI driver
parameters:
  type: gp3
  encrypted: "true"
  kmsKeyId: "arn:aws:kms:us-west-2:111122223333:key/1234"
```

---

## Volume Snapshots

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: data-snapshot
spec:
  volumeSnapshotClassName: csi-snapclass
  source:
    persistentVolumeClaimName: data-pvc

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: restore-pvc
spec:
  dataSource:
    name: data-snapshot
    kind: VolumeSnapshot
    apiGroup: snapshot.storage.k8s.io
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

---

## Volume Expansion

```yaml
# Enable expansion in StorageClass
allowVolumeExpansion: true

# Then resize PVC:
kubectl patch pvc data-pvc -p \
  '{"spec":{"resources":{"requests":{"storage":"20Gi"}}}}'

# Note:
# - Online expansion support varies by provider
# - May require pod restart
```

---

## ConfigMap as Volume

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    volumeMounts:
    - name: config
      mountPath: /etc/config
  volumes:
  - name: config
    configMap:
      name: app-config
      items:
      - key: app.properties
        path: application.properties
```

---

## Secret as Volume

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    volumeMounts:
    - name: secrets
      mountPath: /etc/secrets
      readOnly: true
  volumes:
  - name: secrets
    secret:
      secretName: app-secrets
      defaultMode: 0400  # Permissions
```

---

## Projected Volumes

```yaml
volumes:
- name: all-in-one
  projected:
    sources:
    - secret:
        name: mysecret
    - configMap:
        name: myconfigmap
    - downwardAPI:
        items:
        - path: "annotations"
          fieldRef:
            fieldPath: metadata.annotations
    - serviceAccountToken:
        path: token
```

---

## Local Persistent Volumes

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: local-pv
spec:
  capacity:
    storage: 100Gi
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Delete
  storageClassName: local-storage
  local:
    path: /mnt/disks/ssd1
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - node-1
```

---

## Volume Best Practices

1. **Use** PVCs for persistent data
1. **Set** appropriate access modes
1. **Configure** reclaim policies
1. **Monitor** storage usage
1. **Backup** critical data

---

## Storage Monitoring

```bash
# Check PV status
kubectl get pv

# Check PVC status
kubectl get pvc

# Describe PVC for events
kubectl describe pvc my-pvc

# Check storage usage in pod
kubectl exec -it my-pod -- df -h
```

---

## Troubleshooting Storage

1. **PVC Pending**: Check StorageClass, capacity
1. **Mount errors**: Check access modes
1. **Permission denied**: Check security context
1. **No space**: Monitor and expand volumes
1. **Slow performance**: Check storage type

---

## Cloud Provider Storage

![cloud_provider_storage](svg/courses/devops/k8s-introduction/10_volumes_and_storage/cloud_provider_storage.svg)

---

## Volume Security

```yaml
apiVersion: v1
kind: Pod
spec:
  securityContext:
    fsGroup: 2000  # Group ownership
    fsGroupChangePolicy: "OnRootMismatch"
  containers:
  - name: app
    securityContext:
      runAsUser: 1000
      runAsGroup: 3000
    volumeMounts:
    - name: data
      mountPath: /data
```

---

## Backup Strategies

1. **Volume Snapshots**: Native K8s snapshots
1. **Velero**: Cluster backup tool
1. **Database dumps**: Application-level
1. **Storage replication**: Provider-level
1. **Continuous backup**: Real-time sync

---

## Performance Considerations

```yaml
# High-performance storage
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: high-perf
provisioner: kubernetes.io/aws-ebs
parameters:
  type: io2
  iopsPerGB: "50"  # Up to 64,000 IOPS
  encrypted: "true"
```

---

## Storage Patterns

![storage_patterns](svg/courses/devops/k8s-introduction/10_volumes_and_storage/storage_patterns.svg)

---

## Summary

1. Volumes provide persistent storage
1. PVs and PVCs abstract storage details
1. StorageClasses enable dynamic provisioning
1. Multiple volume types for different needs
1. CSI provides standard storage interface
