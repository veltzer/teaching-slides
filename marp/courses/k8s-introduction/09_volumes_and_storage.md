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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Container Storage Problem</text>
  <g id="without">
    <text x="200" y="80" text-anchor="middle" font-size="12">Without Volumes</text>
    <rect x="100" y="100" width="200" height="80" fill="#ea4335" rx="5"/>
    <text x="200" y="130" text-anchor="middle" fill="white" font-weight="bold">Container</text>
    <text x="200" y="150" text-anchor="middle" fill="white" font-size="11">Writes data</text>
    <text x="200" y="170" text-anchor="middle" fill="white" font-size="11">Container crashes ❌</text>
    <rect x="100" y="200" width="200" height="60" fill="#888" rx="5"/>
    <text x="200" y="235" text-anchor="middle" fill="white">Data Lost!</text>
  </g>
  <g id="with">
    <text x="550" y="80" text-anchor="middle" font-size="12">With Volumes</text>
    <rect x="450" y="100" width="200" height="80" fill="#34a853" rx="5"/>
    <text x="550" y="130" text-anchor="middle" fill="white" font-weight="bold">Container</text>
    <text x="550" y="150" text-anchor="middle" fill="white" font-size="11">Writes to volume</text>
    <text x="550" y="170" text-anchor="middle" fill="white" font-size="11">Container crashes ✓</text>
    <rect x="450" y="200" width="200" height="60" fill="#4285f4" rx="5"/>
    <text x="550" y="235" text-anchor="middle" fill="white">Data Persists!</text>
  </g>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f9f9f9" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">emptyDir Volume Lifecycle</text>
  <rect x="200" y="80" width="400" height="100" fill="#e8f5e9" rx="5"/>
  <text x="400" y="110" text-anchor="middle" font-weight="bold">Pod Created</text>
  <rect x="250" y="120" width="100" height="40" fill="#4285f4" rx="3"/>
  <text x="300" y="145" text-anchor="middle" fill="white" font-size="11">Container 1</text>
  <rect x="450" y="120" width="100" height="40" fill="#4285f4" rx="3"/>
  <text x="500" y="145" text-anchor="middle" fill="white" font-size="11">Container 2</text>
  <rect x="330" y="200" width="140" height="50" fill="#fbbc04" rx="5"/>
  <text x="400" y="230" text-anchor="middle">emptyDir Volume</text>
  <path d="M 300 160 L 370 195" stroke="#666" stroke-width="2"/>
  <path d="M 500 160 L 430 195" stroke="#666" stroke-width="2"/>
  <text x="400" y="280" text-anchor="middle" font-size="12">✓ Shared between containers</text>
  <text x="400" y="300" text-anchor="middle" font-size="12">✓ Survives container restarts</text>
  <text x="400" y="320" text-anchor="middle" font-size="12">❌ Deleted when Pod deleted</text>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">PersistentVolume Access Modes</text>
  <rect x="100" y="80" width="200" height="100" fill="#4285f4" rx="5"/>
  <text x="200" y="110" text-anchor="middle" fill="white" font-weight="bold">ReadWriteOnce (RWO)</text>
  <text x="200" y="135" text-anchor="middle" fill="white" font-size="11">Single node</text>
  <text x="200" y="155" text-anchor="middle" fill="white" font-size="11">Read-write access</text>
  <text x="200" y="175" text-anchor="middle" fill="white" font-size="11">Most common</text>
  <rect x="320" y="80" width="200" height="100" fill="#34a853" rx="5"/>
  <text x="420" y="110" text-anchor="middle" fill="white" font-weight="bold">ReadOnlyMany (ROX)</text>
  <text x="420" y="135" text-anchor="middle" fill="white" font-size="11">Multiple nodes</text>
  <text x="420" y="155" text-anchor="middle" fill="white" font-size="11">Read-only access</text>
  <text x="420" y="175" text-anchor="middle" fill="white" font-size="11">Shared data</text>
  <rect x="540" y="80" width="200" height="100" fill="#fbbc04" rx="5"/>
  <text x="640" y="110" text-anchor="middle" font-weight="bold">ReadWriteMany (RWX)</text>
  <text x="640" y="135" text-anchor="middle" font-size="11">Multiple nodes</text>
  <text x="640" y="155" text-anchor="middle" font-size="11">Read-write access</text>
  <text x="640" y="175" text-anchor="middle" font-size="11">NFS, CephFS</text>
  <rect x="250" y="210" width="300" height="80" fill="#e8f5e9" rx="5"/>
  <text x="400" y="235" text-anchor="middle" font-weight="bold">New Mode (1.22+)</text>
  <text x="400" y="260" text-anchor="middle" font-size="12">ReadWriteOncePod (RWOP)</text>
  <text x="400" y="280" text-anchor="middle" font-size="11">Single pod only</text>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="30" text-anchor="middle" font-size="16" font-weight="bold">PV-PVC Binding Process</text>
  <rect x="100" y="60" width="150" height="80" fill="#4285f4" rx="5"/>
  <text x="175" y="90" text-anchor="middle" fill="white" font-weight="bold">PV Created</text>
  <text x="175" y="110" text-anchor="middle" fill="white" font-size="10">10Gi Available</text>
  <text x="175" y="130" text-anchor="middle" fill="white" font-size="10">Status: Available</text>
  <rect x="300" y="60" width="150" height="80" fill="#34a853" rx="5"/>
  <text x="375" y="90" text-anchor="middle" fill="white" font-weight="bold">PVC Created</text>
  <text x="375" y="110" text-anchor="middle" fill="white" font-size="10">Request: 5Gi</text>
  <text x="375" y="130" text-anchor="middle" fill="white" font-size="10">Status: Pending</text>
  <rect x="500" y="60" width="150" height="80" fill="#fbbc04" rx="5"/>
  <text x="575" y="90" text-anchor="middle" font-weight="bold">Binding</text>
  <text x="575" y="110" text-anchor="middle" font-size="10">Match found</text>
  <text x="575" y="130" text-anchor="middle" font-size="10">PVC → PV</text>
  <rect x="250" y="180" width="300" height="80" fill="#ea4335" rx="5"/>
  <text x="400" y="210" text-anchor="middle" fill="white" font-weight="bold">Bound State</text>
  <text x="400" y="235" text-anchor="middle" fill="white" font-size="11">PV Status: Bound</text>
  <text x="400" y="255" text-anchor="middle" fill="white" font-size="11">PVC Status: Bound</text>
  <path d="M 250 100 L 295 100" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 450 100 L 495 100" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 575 140 L 400 175" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f9f9f9" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Dynamic Volume Provisioning</text>
  <rect x="100" y="80" width="150" height="60" fill="#4285f4" rx="5"/>
  <text x="175" y="105" text-anchor="middle" fill="white" font-weight="bold">PVC Created</text>
  <text x="175" y="125" text-anchor="middle" fill="white" font-size="10">StorageClass: fast</text>
  <rect x="300" y="80" width="150" height="60" fill="#34a853" rx="5"/>
  <text x="375" y="105" text-anchor="middle" fill="white" font-weight="bold">Provisioner</text>
  <text x="375" y="125" text-anchor="middle" fill="white" font-size="10">Creates storage</text>
  <rect x="500" y="80" width="150" height="60" fill="#fbbc04" rx="5"/>
  <text x="575" y="105" text-anchor="middle" font-weight="bold">PV Created</text>
  <text x="575" y="125" text-anchor="middle" font-size="10">Automatically</text>
  <rect x="300" y="180" width="150" height="60" fill="#ea4335" rx="5"/>
  <text x="375" y="205" text-anchor="middle" fill="white" font-weight="bold">Bound</text>
  <text x="375" y="225" text-anchor="middle" fill="white" font-size="10">PVC → PV</text>
  <path d="M 250 110 L 295 110" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 450 110 L 495 110" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 575 140 L 375 175" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <rect x="200" y="260" width="400" height="60" fill="#e8f5e9" rx="5"/>
  <text x="400" y="285" text-anchor="middle" font-weight="bold">No Manual PV Creation Needed!</text>
  <text x="400" y="305" text-anchor="middle" font-size="11">Storage provisioned on-demand</text>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">StatefulSet Volume Claims</text>
  <rect x="100" y="80" width="200" height="60" fill="#4285f4" rx="5"/>
  <text x="200" y="110" text-anchor="middle" fill="white" font-weight="bold">web-0</text>
  <text x="200" y="130" text-anchor="middle" fill="white" font-size="11">Pod</text>
  <rect x="100" y="160" width="200" height="60" fill="#34a853" rx="5"/>
  <text x="200" y="190" text-anchor="middle" fill="white" font-weight="bold">www-web-0</text>
  <text x="200" y="210" text-anchor="middle" fill="white" font-size="11">PVC (1Gi)</text>
  <rect x="320" y="80" width="200" height="60" fill="#4285f4" rx="5"/>
  <text x="420" y="110" text-anchor="middle" fill="white" font-weight="bold">web-1</text>
  <text x="420" y="130" text-anchor="middle" fill="white" font-size="11">Pod</text>
  <rect x="320" y="160" width="200" height="60" fill="#34a853" rx="5"/>
  <text x="420" y="190" text-anchor="middle" fill="white" font-weight="bold">www-web-1</text>
  <text x="420" y="210" text-anchor="middle" fill="white" font-size="11">PVC (1Gi)</text>
  <rect x="540" y="80" width="200" height="60" fill="#4285f4" rx="5"/>
  <text x="640" y="110" text-anchor="middle" fill="white" font-weight="bold">web-2</text>
  <text x="640" y="130" text-anchor="middle" fill="white" font-size="11">Pod</text>
  <rect x="540" y="160" width="200" height="60" fill="#34a853" rx="5"/>
  <text x="640" y="190" text-anchor="middle" fill="white" font-weight="bold">www-web-2</text>
  <text x="640" y="210" text-anchor="middle" fill="white" font-size="11">PVC (1Gi)</text>
  <path d="M 200 140 L 200 155" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 420 140 L 420 155" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 640 140 L 640 155" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="400" y="260" text-anchor="middle" font-size="12">Each pod gets its own PVC</text>
  <text x="400" y="280" text-anchor="middle" font-size="12">PVCs persist when pods are deleted</text>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f9f9f9" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Cloud Storage Options</text>
  <rect x="100" y="80" width="200" height="100" fill="#ff9900" rx="5"/>
  <text x="200" y="110" text-anchor="middle" font-weight="bold">AWS</text>
  <text x="200" y="135" text-anchor="middle" font-size="11">• EBS (Block)</text>
  <text x="200" y="155" text-anchor="middle" font-size="11">• EFS (NFS)</text>
  <text x="200" y="175" text-anchor="middle" font-size="11">• FSx (Lustre)</text>
  <rect x="320" y="80" width="200" height="100" fill="#4285f4" rx="5"/>
  <text x="420" y="110" text-anchor="middle" fill="white" font-weight="bold">Google Cloud</text>
  <text x="420" y="135" text-anchor="middle" fill="white" font-size="11">• Persistent Disk</text>
  <text x="420" y="155" text-anchor="middle" fill="white" font-size="11">• Filestore (NFS)</text>
  <text x="420" y="175" text-anchor="middle" fill="white" font-size="11">• Cloud Storage</text>
  <rect x="540" y="80" width="200" height="100" fill="#0078d4" rx="5"/>
  <text x="640" y="110" text-anchor="middle" fill="white" font-weight="bold">Azure</text>
  <text x="640" y="135" text-anchor="middle" fill="white" font-size="11">• Azure Disk</text>
  <text x="640" y="155" text-anchor="middle" fill="white" font-size="11">• Azure Files</text>
  <text x="640" y="175" text-anchor="middle" fill="white" font-size="11">• Azure NetApp</text>
  <rect x="200" y="210" width="400" height="80" fill="#e8f5e9" rx="5"/>
  <text x="400" y="240" text-anchor="middle" font-weight="bold">Common Features</text>
  <text x="400" y="265" text-anchor="middle" font-size="12">• Dynamic provisioning via CSI</text>
  <text x="400" y="285" text-anchor="middle" font-size="12">• Snapshot support, encryption, resizing</text>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Common Storage Patterns</text>
  <rect x="100" y="80" width="150" height="100" fill="#4285f4" rx="5"/>
  <text x="175" y="110" text-anchor="middle" fill="white" font-weight="bold">Shared Config</text>
  <text x="175" y="135" text-anchor="middle" fill="white" font-size="11">ConfigMap</text>
  <text x="175" y="155" text-anchor="middle" fill="white" font-size="11">ReadOnlyMany</text>
  <text x="175" y="175" text-anchor="middle" fill="white" font-size="11">Multiple pods</text>
  <rect x="270" y="80" width="150" height="100" fill="#34a853" rx="5"/>
  <text x="345" y="110" text-anchor="middle" fill="white" font-weight="bold">Database</text>
  <text x="345" y="135" text-anchor="middle" fill="white" font-size="11">StatefulSet</text>
  <text x="345" y="155" text-anchor="middle" fill="white" font-size="11">ReadWriteOnce</text>
  <text x="345" y="175" text-anchor="middle" fill="white" font-size="11">Per-pod PVC</text>
  <rect x="440" y="80" width="150" height="100" fill="#fbbc04" rx="5"/>
  <text x="515" y="110" text-anchor="middle" font-weight="bold">Shared Data</text>
  <text x="515" y="135" text-anchor="middle" font-size="11">NFS/CephFS</text>
  <text x="515" y="155" text-anchor="middle" font-size="11">ReadWriteMany</text>
  <text x="515" y="175" text-anchor="middle" font-size="11">Concurrent</text>
  <rect x="610" y="80" width="140" height="100" fill="#ea4335" rx="5"/>
  <text x="680" y="110" text-anchor="middle" fill="white" font-weight="bold">Cache</text>
  <text x="680" y="135" text-anchor="middle" fill="white" font-size="11">emptyDir</text>
  <text x="680" y="155" text-anchor="middle" fill="white" font-size="11">Memory</text>
  <text x="680" y="175" text-anchor="middle" fill="white" font-size="11">Ephemeral</text>
</svg>

---

## Summary

1. Volumes provide persistent storage
1. PVs and PVCs abstract storage details
1. StorageClasses enable dynamic provisioning
1. Multiple volume types for different needs
1. CSI provides standard storage interface
