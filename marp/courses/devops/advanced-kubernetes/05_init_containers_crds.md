# Init Containers & Custom Resource Definitions

Advanced Kubernetes Course - Day 1, Module 5

---

## Module Overview

- Init containers: purpose and patterns
- Sidecar containers
- `Custom Resource Definitions` (`CRDs`)
- Validation and versioning
- Aggregated `API` servers

---

## Init Containers

Run **before** app containers start, in order, one at a time:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-app
spec:
  initContainers:
  - name: wait-for-db
    image: busybox:1.36
    command: ['sh', '-c',
      'until nc -z postgres-service 5432;
       do echo waiting for db; sleep 2; done']
  - name: init-schema
    image: postgres:16
    command: ['psql', '-h', 'postgres-service',
      '-U', 'admin', '-f', '/schema/init.sql']
    volumeMounts:
    - name: schema
      mountPath: /schema
  containers:
  - name: web
    image: myapp:v2
    ports:
    - containerPort: 8080
  volumes:
  - name: schema
    configMap:
      name: db-schema
```

---

## Init Container Properties

| Property | Init Container | Regular Container |
|----------|---------------|-------------------|
| Runs | Before app containers | After init completes |
| Order | Sequential | Parallel |
| Must succeed | Yes (all) | Depends on `restartPolicy` |
| Probes | Not supported | Supported |
| Resource limits | Independent | Shared |
| Lifecycle hooks | Not supported | Supported |

---

## Init Container Use Cases

<svg xmlns="http://www.w3.org/2000/svg" width="640" height="310">
  <defs>
    <marker id="arr" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
    </marker>
  </defs>
  <!-- outer Pod box -->
  <rect x="10" y="10" width="620" height="295" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="320" y="32" font-family="sans-serif" font-size="14" font-weight="bold" fill="#222" text-anchor="middle">Pod Lifecycle</text>
  <!-- Init 1 -->
  <rect x="30" y="48" width="140" height="80" rx="4" fill="#fff3e0" stroke="#555" stroke-width="1.5"/>
  <text x="100" y="68" font-family="sans-serif" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">Init 1</text>
  <text x="100" y="88" font-family="sans-serif" font-size="12" fill="#555" text-anchor="middle">Clone repo</text>
  <!-- arrow -->
  <line x1="170" y1="88" x2="210" y2="88" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- Init 2 -->
  <rect x="210" y="48" width="140" height="80" rx="4" fill="#fff3e0" stroke="#555" stroke-width="1.5"/>
  <text x="280" y="68" font-family="sans-serif" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">Init 2</text>
  <text x="280" y="88" font-family="sans-serif" font-size="12" fill="#555" text-anchor="middle">Migrate DB</text>
  <!-- arrow -->
  <line x1="350" y1="88" x2="390" y2="88" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- App Container -->
  <rect x="390" y="48" width="210" height="80" rx="4" fill="#e8f5e9" stroke="#555" stroke-width="1.5"/>
  <text x="495" y="68" font-family="sans-serif" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">App Container</text>
  <text x="495" y="88" font-family="sans-serif" font-size="12" fill="#555" text-anchor="middle">Main workload</text>
  <!-- Common patterns section -->
  <line x1="20" y1="145" x2="620" y2="145" stroke="#aaa" stroke-width="1" stroke-dasharray="4"/>
  <text x="30" y="165" font-family="sans-serif" font-size="13" font-weight="bold" fill="#333">Common patterns:</text>
  <text x="30" y="185" font-family="sans-serif" font-size="12" fill="#333">• Wait for dependencies</text>
  <text x="30" y="205" font-family="sans-serif" font-size="12" fill="#333">• Download / prepare configs</text>
  <text x="30" y="225" font-family="sans-serif" font-size="12" fill="#333">• Clone source code</text>
  <text x="30" y="245" font-family="sans-serif" font-size="12" fill="#333">• Database migrations</text>
  <text x="30" y="265" font-family="sans-serif" font-size="12" fill="#333">• Register with service mesh</text>
  <text x="30" y="285" font-family="sans-serif" font-size="12" fill="#333">• Seed data</text>
</svg>

---

## Init Container: Clone Config from Git

```yaml
spec:
  initContainers:
  - name: git-clone
    image: alpine/git:latest
    command:
    - git
    - clone
    - --depth=1
    - https://github.com/company/app-config.git
    - /config
    volumeMounts:
    - name: config-volume
      mountPath: /config
  containers:
  - name: app
    image: myapp:v3
    volumeMounts:
    - name: config-volume
      mountPath: /app/config
      readOnly: true
  volumes:
  - name: config-volume
    emptyDir: {}
```

---

## Init Container: Permissions Setup

```yaml
spec:
  initContainers:
  - name: fix-permissions
    image: busybox:1.36
    command: ['sh', '-c', 'chown -R 1000:1000 /data']
    securityContext:
      runAsUser: 0
    volumeMounts:
    - name: data
      mountPath: /data
  - name: sysctl
    image: busybox:1.36
    command: ['sysctl', '-w', 'vm.max_map_count=262144']
    securityContext:
      privileged: true
  containers:
  - name: elasticsearch
    image: elasticsearch:8.12.0
    securityContext:
      runAsUser: 1000
    volumeMounts:
    - name: data
      mountPath: /usr/share/elasticsearch/data
  volumes:
  - name: data
    persistentVolumeClaim:
      claimName: es-data
```

---

## Sidecar Containers (Native in `Kubernetes` 1.28+)

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-with-sidecar
spec:
  initContainers:
  - name: log-shipper
    image: fluent-bit:latest
    restartPolicy: Always    # Makes it a sidecar
    volumeMounts:
    - name: logs
      mountPath: /var/log/app
  containers:
  - name: app
    image: myapp:v2
    volumeMounts:
    - name: logs
      mountPath: /var/log/app
  volumes:
  - name: logs
    emptyDir: {}
```

The `restartPolicy: Always` on an init container marks it as a **sidecar** that runs alongside the main containers.

---

## Sidecar Patterns

<svg xmlns="http://www.w3.org/2000/svg" width="540" height="330">
  <defs>
    <marker id="arrf" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
    </marker>
    <marker id="arrb" markerWidth="8" markerHeight="6" refX="1" refY="3" orient="auto">
      <path d="M8,0 L8,6 L0,3 z" fill="#555"/>
    </marker>
  </defs>
  <!-- Pod outer box -->
  <rect x="10" y="10" width="520" height="310" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="270" y="32" font-family="sans-serif" font-size="14" font-weight="bold" fill="#222" text-anchor="middle">Pod</text>

  <!-- Row 1: App + Log Shipper -->
  <rect x="30" y="45" width="130" height="60" rx="4" fill="#fff" stroke="#555" stroke-width="1.5"/>
  <text x="95" y="70" font-family="sans-serif" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">App</text>
  <text x="95" y="88" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">Container</text>
  <line x1="160" y1="75" x2="220" y2="75" stroke="#555" stroke-width="1.5" marker-end="url(#arrf)"/>
  <rect x="220" y="45" width="170" height="60" rx="4" fill="#fff3e0" stroke="#555" stroke-width="1.5"/>
  <text x="305" y="68" font-family="sans-serif" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">Log Shipper</text>
  <text x="305" y="86" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">(Sidecar)</text>

  <!-- Row 2: App + Service Mesh Proxy -->
  <rect x="30" y="130" width="130" height="60" rx="4" fill="#fff" stroke="#555" stroke-width="1.5"/>
  <text x="95" y="155" font-family="sans-serif" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">App</text>
  <text x="95" y="173" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">Container</text>
  <line x1="220" y1="160" x2="160" y2="160" stroke="#555" stroke-width="1.5" marker-end="url(#arrf)"/>
  <rect x="220" y="130" width="200" height="60" rx="4" fill="#fff3e0" stroke="#555" stroke-width="1.5"/>
  <text x="320" y="152" font-family="sans-serif" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">Service Mesh Proxy</text>
  <text x="320" y="170" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">(Sidecar – Envoy)</text>

  <!-- Row 3: App + Config Reloader -->
  <rect x="30" y="215" width="130" height="60" rx="4" fill="#fff" stroke="#555" stroke-width="1.5"/>
  <text x="95" y="240" font-family="sans-serif" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">App</text>
  <text x="95" y="258" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">Container</text>
  <line x1="220" y1="245" x2="160" y2="245" stroke="#555" stroke-width="1.5" marker-end="url(#arrf)"/>
  <rect x="220" y="215" width="170" height="60" rx="4" fill="#fff3e0" stroke="#555" stroke-width="1.5"/>
  <text x="305" y="238" font-family="sans-serif" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">Config Reloader</text>
  <text x="305" y="256" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">(Sidecar)</text>
</svg>

---

## Custom Resource Definitions (`CRDs`)

Extend the `Kubernetes` `API` with your own resource types:

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: certificates.cert-manager.io
spec:
  group: cert-manager.io
  names:
    kind: Certificate
    listKind: CertificateList
    plural: certificates
    singular: certificate
    shortNames:
    - cert
    - certs
  scope: Namespaced
  versions:
  - name: v1
    served: true
    storage: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            required: [secretName, issuerRef]
            properties:
              secretName:
                type: string
              duration:
                type: string
              issuerRef:
                type: object
                properties:
                  name:
                    type: string
                  kind:
                    type: string
```

---

## `CRD` Validation

```yaml
schema:
  openAPIV3Schema:
    type: object
    properties:
      spec:
        type: object
        required: [replicas, version]
        properties:
          replicas:
            type: integer
            minimum: 1
            maximum: 10
          version:
            type: string
            pattern: '^\d+\.\d+\.\d+$'
          tier:
            type: string
            enum: [basic, standard, premium]
          config:
            type: object
            x-kubernetes-preserve-unknown-fields: true
          resources:
            type: object
            properties:
              cpu:
                type: string
                pattern: '^\d+m?$'
              memory:
                type: string
                pattern: '^\d+(Mi|Gi)$'
```

---

## `CRD` Additional Printer Columns

```yaml
versions:
- name: v1
  served: true
  storage: true
  additionalPrinterColumns:
  - name: Version
    type: string
    jsonPath: .spec.version
  - name: Replicas
    type: integer
    jsonPath: .spec.replicas
  - name: Status
    type: string
    jsonPath: .status.phase
  - name: Age
    type: date
    jsonPath: .metadata.creationTimestamp
  subresources:
    status: {}
    scale:
      specReplicasPath: .spec.replicas
      statusReplicasPath: .status.replicas
```

```bash
kubectl get databases
NAME          VERSION   REPLICAS   STATUS    AGE
production    16.1      3          Running   5d
staging       16.1      1          Running   2d
```

---

## `CRD` Versioning

```yaml
spec:
  versions:
  - name: v1alpha1
    served: true
    storage: false
  - name: v1beta1
    served: true
    storage: false
  - name: v1
    served: true
    storage: true
  conversion:
    strategy: Webhook
    webhook:
      conversionReviewVersions: ["v1"]
      clientConfig:
        service:
          name: crd-conversion-webhook
          namespace: system
          path: /convert
```

---

## Creating and Using `CRDs`

```bash
# Install the CRD
kubectl apply -f my-crd.yaml

# Verify
kubectl get crd | grep myresource

# Create an instance
kubectl apply -f - <<EOF
apiVersion: mygroup.example.com/v1
kind: MyResource
metadata:
  name: test-resource
spec:
  replicas: 3
  version: "1.0.0"
  tier: premium
EOF

# Interact like any Kubernetes resource
kubectl get myresource
kubectl describe myresource test-resource
kubectl delete myresource test-resource
```

---

## `CRD` Categories

Group your `CRDs` under `kubectl get all`:

```yaml
spec:
  names:
    kind: Database
    plural: databases
    categories:
    - all
    - database-operator
```

```bash
# Now shows up in 'kubectl get all'
kubectl get all

# Or use custom category
kubectl get database-operator
```

---

## Webhook Validation

For validation beyond `OpenAPI` schema:

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  name: validate-database
webhooks:
- name: validate.database.example.com
  admissionReviewVersions: ["v1"]
  clientConfig:
    service:
      name: webhook-service
      namespace: system
      path: /validate-database
  rules:
  - apiGroups: ["database.example.com"]
    apiVersions: ["v1"]
    operations: ["CREATE", "UPDATE"]
    resources: ["databases"]
  failurePolicy: Fail
  sideEffects: None
```

---

## Webhook Handler in `Go`

```go
func (v *DatabaseValidator) Handle(
    ctx context.Context,
    req admission.Request,
) admission.Response {
    db := &databasev1.Database{}
    if err := v.decoder.Decode(req, db); err != nil {
        return admission.Errored(
            http.StatusBadRequest, err)
    }

    // Custom validation logic
    if db.Spec.Replicas > 1 &&
       db.Spec.Tier == "basic" {
        return admission.Denied(
            "basic tier only supports 1 replica")
    }

    if db.Spec.StorageSize == "" &&
       db.Spec.Tier == "premium" {
        return admission.Denied(
            "premium tier requires explicit storage size")
    }

    return admission.Allowed("")
}
```

---

## Mutating Webhooks

Automatically set defaults or inject fields:

```go
func (m *DatabaseMutator) Handle(
    ctx context.Context,
    req admission.Request,
) admission.Response {
    db := &databasev1.Database{}
    if err := m.decoder.Decode(req, db); err != nil {
        return admission.Errored(
            http.StatusBadRequest, err)
    }

    // Set defaults
    if db.Spec.StorageSize == "" {
        db.Spec.StorageSize = "10Gi"
    }
    if db.Spec.BackupSchedule == "" &&
       db.Spec.BackupEnabled {
        db.Spec.BackupSchedule = "0 2 * * *"
    }

    // Add standard labels
    if db.Labels == nil {
        db.Labels = make(map[string]string)
    }
    db.Labels["managed-by"] = "database-operator"

    marshaledDB, err := json.Marshal(db)
    if err != nil {
        return admission.Errored(
            http.StatusInternalServerError, err)
    }

    return admission.PatchResponseFromRaw(
        req.Object.Raw, marshaledDB)
}
```

---

## Aggregated `API` Server

For complex use cases beyond `CRDs`:

```yaml
apiVersion: apiregistration.k8s.io/v1
kind: APIService
metadata:
  name: v1alpha1.metrics.example.com
spec:
  group: metrics.example.com
  version: v1alpha1
  service:
    name: metrics-api
    namespace: system
  groupPriorityMinimum: 100
  versionPriority: 100
  caBundle: <base64-ca-cert>
```

| Feature | `CRD` | Aggregated `API` |
|---------|------|-----------------|
| Storage | `etcd` (built-in) | Custom backend |
| Validation | OpenAPI + Webhooks | Custom code |
| Subresources | Limited | Full control |
| Complexity | Low | High |

---

## Lab: Create a `CRD` with Validation

1. Define a `CRD` for a `WebApplication` resource
1. Add `OpenAPI` validation schema
1. Add printer columns
1. Create instances and test validation
1. Optional: Add a validating webhook

```bash
# Apply CRD
kubectl apply -f webapp-crd.yaml

# Test valid resource
kubectl apply -f valid-webapp.yaml

# Test invalid resource (should be rejected)
kubectl apply -f invalid-webapp.yaml

# List with custom columns
kubectl get webapps
```
