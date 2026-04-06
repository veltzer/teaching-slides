# Controllers and Operators

Advanced Kubernetes Course - Day 1, Module 4

---

## Module Overview

- The controller pattern
- Built-in controllers
- Writing custom controllers in `Go`
- The Operator pattern
- `Operator SDK` and `Kubebuilder`
- Real-world operator examples

---

## The Controller Pattern

Every controller follows the same reconciliation loop:

```diagram
        ┌──────────────────────────────┐
        │                              │
        ▼                              │
┌───────────────┐    ┌──────────┐     │
│ Observe       │───▶│ Compare  │     │
│ Current State │    │ Desired  │     │
└───────────────┘    │ vs       │     │
                     │ Actual   │     │
                     └────┬─────┘     │
                          │           │
                     ┌────▼─────┐     │
                     │ Act      │─────┘
                     │ (Reconcile)
                     └──────────┘
```

**Level-triggered**, not edge-triggered: Acts on current state, not events.

---

## Built-in Controllers

The `kube-controller-manager` runs many controllers:

| Controller | Manages |
|-----------|---------|
| `ReplicaSet` | Maintains desired pod count |
| `Deployment` | Rolling updates, rollbacks |
| `StatefulSet` | Ordered, stateful pods |
| `DaemonSet` | One pod per node |
| `Job` | Run-to-completion tasks |
| `CronJob` | Scheduled jobs |
| `Node` | Node lifecycle |
| `ServiceAccount` | Default service accounts |
| `Endpoint` | Service endpoint lists |
| `Namespace` | Namespace lifecycle |

---

## Controller vs Operator

| | Controller | Operator |
|---|-----------|----------|
| Manages | Any `Kubernetes` resource | Application-specific `CRD` |
| Domain knowledge | Generic | Application-specific |
| Complexity | Simple reconcile | Full lifecycle management |
| Examples | `ReplicaSet` controller | `PostgreSQL` operator |

An **Operator** = Custom Controller + Custom Resource Definition + Domain Knowledge

---

## Controller Architecture in `Go`

```go
package main

import (
    "context"
    "fmt"

    "k8s.io/client-go/kubernetes"
    "k8s.io/client-go/tools/clientcmd"
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

func main() {
    config, err := clientcmd.BuildConfigFromFlags("",
        clientcmd.RecommendedHomeFile)
    if err != nil {
        panic(err)
    }

    clientset, err := kubernetes.NewForConfig(config)
    if err != nil {
        panic(err)
    }

    pods, err := clientset.CoreV1().Pods("default").
        List(context.TODO(), metav1.ListOptions{})
    if err != nil {
        panic(err)
    }

    for _, pod := range pods.Items {
        fmt.Printf("Pod: %s Status: %s\n",
            pod.Name, pod.Status.Phase)
    }
}
```

---

## Using Informers (Watch + Cache)

```go
import (
    "k8s.io/client-go/informers"
    "k8s.io/client-go/tools/cache"
)

func main() {
    factory := informers.NewSharedInformerFactory(
        clientset, 30*time.Second)

    podInformer := factory.Core().V1().Pods().Informer()

    podInformer.AddEventHandler(cache.ResourceEventHandlerFuncs{
        AddFunc: func(obj interface{}) {
            pod := obj.(*v1.Pod)
            fmt.Printf("Pod added: %s\n", pod.Name)
        },
        UpdateFunc: func(oldObj, newObj interface{}) {
            newPod := newObj.(*v1.Pod)
            fmt.Printf("Pod updated: %s\n", newPod.Name)
        },
        DeleteFunc: func(obj interface{}) {
            pod := obj.(*v1.Pod)
            fmt.Printf("Pod deleted: %s\n", pod.Name)
        },
    })

    stopCh := make(chan struct{})
    factory.Start(stopCh)
    factory.WaitForCacheSync(stopCh)
    <-stopCh
}
```

---

## Work Queue Pattern

```go
import "k8s.io/client-go/util/workqueue"

type Controller struct {
    queue    workqueue.RateLimitingInterface
    informer cache.SharedIndexInformer
}

func (c *Controller) Run(stopCh <-chan struct{}) {
    defer c.queue.ShutDown()

    go c.informer.Run(stopCh)

    if !cache.WaitForCacheSync(stopCh,
        c.informer.HasSynced) {
        return
    }

    for c.processNextItem() {
    }
}

func (c *Controller) processNextItem() bool {
    key, quit := c.queue.Get()
    if quit {
        return false
    }
    defer c.queue.Done(key)

    err := c.reconcile(key.(string))
    if err != nil {
        c.queue.AddRateLimited(key)
        return true
    }

    c.queue.Forget(key)
    return true
}
```

---

## The Reconcile Function

```go
func (c *Controller) reconcile(key string) error {
    namespace, name, err := cache.SplitMetaNamespaceKey(key)
    if err != nil {
        return err
    }

    // Get the current state
    obj, exists, err := c.informer.GetStore().
        GetByKey(key)
    if err != nil {
        return err
    }

    if !exists {
        // Object was deleted
        fmt.Printf("Object %s/%s deleted\n",
            namespace, name)
        return nil
    }

    // Compare desired vs actual state
    pod := obj.(*v1.Pod)

    // Take action to reconcile
    if pod.Labels["managed-by"] == "my-controller" {
        return c.ensureDesiredState(pod)
    }

    return nil
}
```

---

## Operator Pattern with `Kubebuilder`

```bash
# Initialize a new operator project
kubebuilder init \
  --domain example.com \
  --repo github.com/example/database-operator

# Create an API (CRD + Controller)
kubebuilder create api \
  --group database \
  --version v1alpha1 \
  --kind PostgreSQL

# Project structure
tree .
├── api/
│   └── v1alpha1/
│       ├── postgresql_types.go
│       └── zz_generated.deepcopy.go
├── config/
│   ├── crd/
│   ├── manager/
│   ├── rbac/
│   └── samples/
├── controllers/
│   └── postgresql_controller.go
├── main.go
├── Dockerfile
└── Makefile
```

---

## Defining the `CRD` Types

```go
// api/v1alpha1/postgresql_types.go
package v1alpha1

import metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"

type PostgreSQLSpec struct {
    // Version of PostgreSQL to deploy
    Version string `json:"version"`

    // Number of replicas
    Replicas int32 `json:"replicas"`

    // Storage size per instance
    StorageSize string `json:"storageSize"`

    // Enable automated backups
    BackupEnabled bool `json:"backupEnabled,omitempty"`

    // Backup schedule in cron format
    BackupSchedule string `json:"backupSchedule,omitempty"`
}

type PostgreSQLStatus struct {
    // Current state of the cluster
    Phase string `json:"phase"`

    // Number of ready replicas
    ReadyReplicas int32 `json:"readyReplicas"`

    // Last backup timestamp
    LastBackup *metav1.Time `json:"lastBackup,omitempty"`

    // Human-readable conditions
    Conditions []metav1.Condition `json:"conditions,omitempty"`
}

//+kubebuilder:object:root=true
//+kubebuilder:subresource:status
//+kubebuilder:printcolumn:name="Version",type=string,JSONPath=`.spec.version`
//+kubebuilder:printcolumn:name="Replicas",type=integer,JSONPath=`.spec.replicas`
//+kubebuilder:printcolumn:name="Phase",type=string,JSONPath=`.status.phase`

type PostgreSQL struct {
    metav1.TypeMeta   `json:",inline"`
    metav1.ObjectMeta `json:"metadata,omitempty"`
    Spec              PostgreSQLSpec   `json:"spec,omitempty"`
    Status            PostgreSQLStatus `json:"status,omitempty"`
}
```

---

## The Operator Reconcile Loop

```go
// controllers/postgresql_controller.go
func (r *PostgreSQLReconciler) Reconcile(
    ctx context.Context,
    req ctrl.Request,
) (ctrl.Result, error) {
    log := r.Log.WithValues("postgresql", req.NamespacedName)

    // Fetch the PostgreSQL instance
    pg := &databasev1alpha1.PostgreSQL{}
    if err := r.Get(ctx, req.NamespacedName, pg); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }

    // Ensure StatefulSet exists
    if err := r.ensureStatefulSet(ctx, pg); err != nil {
        return ctrl.Result{}, err
    }

    // Ensure Service exists
    if err := r.ensureService(ctx, pg); err != nil {
        return ctrl.Result{}, err
    }

    // Ensure backups are configured
    if pg.Spec.BackupEnabled {
        if err := r.ensureBackupCronJob(ctx, pg); err != nil {
            return ctrl.Result{}, err
        }
    }

    // Update status
    return r.updateStatus(ctx, pg)
}
```

---

## Creating Owned Resources

```go
func (r *PostgreSQLReconciler) ensureStatefulSet(
    ctx context.Context,
    pg *databasev1alpha1.PostgreSQL,
) error {
    sts := &appsv1.StatefulSet{}
    err := r.Get(ctx, types.NamespacedName{
        Name:      pg.Name,
        Namespace: pg.Namespace,
    }, sts)

    if errors.IsNotFound(err) {
        sts = r.buildStatefulSet(pg)
        // Set owner reference for garbage collection
        ctrl.SetControllerReference(pg, sts, r.Scheme)
        return r.Create(ctx, sts)
    }

    if err != nil {
        return err
    }

    // Update if spec changed
    if *sts.Spec.Replicas != pg.Spec.Replicas {
        sts.Spec.Replicas = &pg.Spec.Replicas
        return r.Update(ctx, sts)
    }

    return nil
}
```

---

## `RBAC` for the Operator

```go
//+kubebuilder:rbac:groups=database.example.com,
//  resources=postgresqls,verbs=get;list;watch;
//  create;update;patch;delete
//+kubebuilder:rbac:groups=database.example.com,
//  resources=postgresqls/status,verbs=get;update;patch
//+kubebuilder:rbac:groups=apps,
//  resources=statefulsets,verbs=get;list;watch;
//  create;update;patch;delete
//+kubebuilder:rbac:groups="",
//  resources=services,verbs=get;list;watch;
//  create;update;patch;delete
//+kubebuilder:rbac:groups=batch,
//  resources=cronjobs,verbs=get;list;watch;
//  create;update;patch;delete
```

Generated from annotations into `config/rbac/role.yaml`.

---

## Using the Custom Resource

```yaml
apiVersion: database.example.com/v1alpha1
kind: PostgreSQL
metadata:
  name: production-db
  namespace: production
spec:
  version: "16.1"
  replicas: 3
  storageSize: "100Gi"
  backupEnabled: true
  backupSchedule: "0 2 * * *"
```

```bash
# Apply the resource
kubectl apply -f production-db.yaml

# Check status
kubectl get postgresql
NAME            VERSION   REPLICAS   PHASE
production-db   16.1      3          Running

# Describe for details
kubectl describe postgresql production-db
```

---

## Real-World Operators

| Operator | Purpose |
|----------|---------|
| `prometheus-operator` | Monitoring stack |
| `cert-manager` | TLS certificate management |
| `strimzi` | `Apache Kafka` on `Kubernetes` |
| `zalando/postgres-operator` | `PostgreSQL` clusters |
| `elastic-cloud-on-k8s` | `Elasticsearch` clusters |
| `rook` | Storage orchestration |
| `ArgoCD` | GitOps continuous delivery |

Explore: [OperatorHub.io](https://operatorhub.io)

---

## Operator Maturity Model

```misc
Level 5: Auto Pilot
    │     Full lifecycle, auto-tuning
Level 4: Deep Insights
    │     Metrics, alerts, log processing
Level 3: Full Lifecycle
    │     Backup, restore, failover
Level 2: Seamless Upgrades
    │     Patch and minor version upgrades
Level 1: Basic Install
    │     Automated provisioning
Level 0: Planning
          No automation
```

---

## Building and Deploying an Operator

```bash
# Generate CRD manifests
make manifests

# Install CRDs
make install

# Run locally for development
make run

# Build container image
make docker-build IMG=myregistry/pg-operator:v0.1.0

# Push to registry
make docker-push IMG=myregistry/pg-operator:v0.1.0

# Deploy to cluster
make deploy IMG=myregistry/pg-operator:v0.1.0

# Verify
kubectl get pods -n system
kubectl logs -n system -l control-plane=controller-manager
```

---

## Operator Testing

```go
var _ = Describe("PostgreSQL Controller", func() {
    Context("When creating a PostgreSQL resource", func() {
        It("Should create a StatefulSet", func() {
            pg := &databasev1alpha1.PostgreSQL{
                ObjectMeta: metav1.ObjectMeta{
                    Name:      "test-pg",
                    Namespace: "default",
                },
                Spec: databasev1alpha1.PostgreSQLSpec{
                    Version:  "16.1",
                    Replicas: 3,
                    StorageSize: "10Gi",
                },
            }

            Expect(k8sClient.Create(ctx, pg)).
                Should(Succeed())

            stsKey := types.NamespacedName{
                Name: "test-pg", Namespace: "default"}
            sts := &appsv1.StatefulSet{}

            Eventually(func() bool {
                err := k8sClient.Get(ctx, stsKey, sts)
                return err == nil
            }, timeout, interval).Should(BeTrue())

            Expect(*sts.Spec.Replicas).To(Equal(int32(3)))
        })
    })
})
```

---

## Lab: Build a Simple Operator

1. Initialize project with `Kubebuilder`
1. Define a `WebApp` `CRD` with fields: image, replicas, port
1. Implement reconciliation to create `Deployment` + `Service`
1. Test with `envtest`
1. Deploy to cluster

```bash
kubebuilder init --domain mycompany.com \
  --repo github.com/mycompany/webapp-operator

kubebuilder create api \
  --group apps \
  --version v1 \
  --kind WebApp

make manifests install run
```
