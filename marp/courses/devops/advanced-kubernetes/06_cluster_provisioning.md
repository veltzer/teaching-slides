# Cluster Provisioning

Advanced Kubernetes Course - Day 2, Module 1

---

## Module Overview

- `kubeadm` deep dive
- `Cluster API` (`CAPI`)
- Infrastructure as Code for `Kubernetes`
- Multi-cluster management
- Cluster lifecycle operations

---

## `kubeadm` Architecture

```diagram
┌──────────────────────────────────────────┐
│             Control Plane Node            │
│                                          │
│  ┌──────────┐  ┌────────────────────┐    │
│  │ etcd     │  │ kube-apiserver     │    │
│  └──────────┘  └────────────────────┘    │
│  ┌──────────────────┐  ┌─────────────┐   │
│  │ kube-controller  │  │ kube-       │   │
│  │ -manager         │  │ scheduler   │   │
│  └──────────────────┘  └─────────────┘   │
│                                          │
│  ┌──────────┐  ┌────────────────────┐    │
│  │ kubelet  │  │ kube-proxy         │    │
│  └──────────┘  └────────────────────┘    │
└──────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
┌───────┴──┐  ┌────┴─────┐  ┌──┴───────┐
│ Worker 1 │  │ Worker 2 │  │ Worker 3 │
│ kubelet  │  │ kubelet  │  │ kubelet  │
│ proxy    │  │ proxy    │  │ proxy    │
└──────────┘  └──────────┘  └──────────┘
```

---

## `kubeadm` Init - Control Plane

```bash
# Prerequisites
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl

# Initialize control plane
sudo kubeadm init \
  --control-plane-endpoint "k8s-api.example.com:6443" \
  --pod-network-cidr "10.244.0.0/16" \
  --service-cidr "10.96.0.0/12" \
  --upload-certs \
  --kubernetes-version "v1.29.0"

# Configure kubectl
mkdir -p $HOME/.kube
sudo cp /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

---

## `kubeadm` Configuration File

```yaml
apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
kubernetesVersion: v1.29.0
controlPlaneEndpoint: "k8s-api.example.com:6443"
networking:
  podSubnet: "10.244.0.0/16"
  serviceSubnet: "10.96.0.0/12"
  dnsDomain: "cluster.local"
apiServer:
  extraArgs:
    audit-log-path: /var/log/kubernetes/audit.log
    audit-policy-file: /etc/kubernetes/audit-policy.yaml
    enable-admission-plugins: NodeRestriction,PodSecurity
  extraVolumes:
  - name: audit-log
    hostPath: /var/log/kubernetes
    mountPath: /var/log/kubernetes
etcd:
  local:
    dataDir: /var/lib/etcd
    extraArgs:
      quota-backend-bytes: "8589934592"
---
apiVersion: kubeadm.k8s.io/v1beta3
kind: InitConfiguration
nodeRegistration:
  criSocket: unix:///var/run/containerd/containerd.sock
  kubeletExtraArgs:
    node-labels: "node-role=control-plane"
```

---

## Joining Worker Nodes

```bash
# On control plane, generate token
kubeadm token create --print-join-command

# Output:
kubeadm join k8s-api.example.com:6443 \
  --token abcdef.0123456789abcdef \
  --discovery-token-ca-cert-hash \
    sha256:abc123...

# On worker node
sudo kubeadm join k8s-api.example.com:6443 \
  --token abcdef.0123456789abcdef \
  --discovery-token-ca-cert-hash \
    sha256:abc123...

# Verify on control plane
kubectl get nodes
NAME       STATUS   ROLES           AGE   VERSION
master-1   Ready    control-plane   10m   v1.29.0
worker-1   Ready    <none>          2m    v1.29.0
worker-2   Ready    <none>          1m    v1.29.0
```

---

## Adding Control Plane Nodes (HA)

```bash
# On first control plane, get certificate key
kubeadm init phase upload-certs --upload-certs

# Join additional control plane nodes
sudo kubeadm join k8s-api.example.com:6443 \
  --token abcdef.0123456789abcdef \
  --discovery-token-ca-cert-hash sha256:abc123... \
  --control-plane \
  --certificate-key abc456...
```

```diagram
        ┌─── Load Balancer ───┐
        │  k8s-api.example.com │
        └──┬────────┬────────┬─┘
           │        │        │
     ┌─────┴─┐  ┌──┴────┐  ┌┴──────┐
     │Master1│  │Master2│  │Master3│
     │ etcd  │  │ etcd  │  │ etcd  │
     └───────┘  └───────┘  └───────┘
```

---

## `kubeadm` Upgrade

```bash
# Check available versions
sudo apt-cache madison kubeadm

# Upgrade kubeadm
sudo apt-get install -y kubeadm=1.30.0-*

# Plan the upgrade
sudo kubeadm upgrade plan

# Apply the upgrade (control plane)
sudo kubeadm upgrade apply v1.30.0

# Upgrade kubelet and kubectl
sudo apt-get install -y \
  kubelet=1.30.0-* kubectl=1.30.0-*
sudo systemctl daemon-reload
sudo systemctl restart kubelet

# Drain and upgrade workers one by one
kubectl drain worker-1 --ignore-daemonsets --delete-emptydir-data
# SSH to worker, upgrade kubeadm, kubelet, kubectl
kubectl uncordon worker-1
```

---

## `etcd` Backup and Restore

```bash
# Backup
ETCDCTL_API=3 etcdctl snapshot save /backup/etcd-snap.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Verify backup
ETCDCTL_API=3 etcdctl snapshot status /backup/etcd-snap.db \
  --write-out=table

# Restore
ETCDCTL_API=3 etcdctl snapshot restore /backup/etcd-snap.db \
  --data-dir=/var/lib/etcd-restore

# Update etcd manifest to use restored data
sudo vi /etc/kubernetes/manifests/etcd.yaml
# Change: --data-dir=/var/lib/etcd-restore
```

---

## `Cluster API` (`CAPI`) Overview

Declarative `Kubernetes`-style `APIs` to create, configure, and manage clusters:

```diagram
┌──────────────────────────────────────────────┐
│           Management Cluster                  │
│                                              │
│  ┌────────────────┐  ┌───────────────────┐   │
│  │ CAPI Core      │  │ Infrastructure    │   │
│  │ Controllers    │  │ Provider (AWS,    │   │
│  │                │  │ Azure, vSphere)   │   │
│  └────────────────┘  └───────────────────┘   │
│  ┌────────────────┐  ┌───────────────────┐   │
│  │ Bootstrap      │  │ Control Plane     │   │
│  │ Provider       │  │ Provider          │   │
│  │ (kubeadm)      │  │ (KubeadmCP)      │   │
│  └────────────────┘  └───────────────────┘   │
└──────────────┬───────────────────────────────┘
               │ manages
    ┌──────────┼──────────┐
    ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐
│Cluster1│ │Cluster2│ │Cluster3│
│  (dev) │ │  (stg) │ │  (prd) │
└────────┘ └────────┘ └────────┘
```

---

## `CAPI` - Cluster Definition

```yaml
apiVersion: cluster.x-k8s.io/v1beta1
kind: Cluster
metadata:
  name: production
  namespace: clusters
spec:
  clusterNetwork:
    pods:
      cidrBlocks: ["192.168.0.0/16"]
    services:
      cidrBlocks: ["10.128.0.0/12"]
  controlPlaneRef:
    apiVersion: controlplane.cluster.x-k8s.io/v1beta1
    kind: KubeadmControlPlane
    name: production-control-plane
  infrastructureRef:
    apiVersion: infrastructure.cluster.x-k8s.io/v1beta2
    kind: AWSCluster
    name: production
```

---

## `CAPI` - Infrastructure Provider (AWS)

```yaml
apiVersion: infrastructure.cluster.x-k8s.io/v1beta2
kind: AWSCluster
metadata:
  name: production
  namespace: clusters
spec:
  region: us-east-1
  sshKeyName: k8s-admin
  network:
    vpc:
      cidrBlock: "10.0.0.0/16"
    subnets:
    - availabilityZone: us-east-1a
      cidrBlock: "10.0.1.0/24"
      isPublic: false
    - availabilityZone: us-east-1b
      cidrBlock: "10.0.2.0/24"
      isPublic: false
    - availabilityZone: us-east-1c
      cidrBlock: "10.0.3.0/24"
      isPublic: false
```

---

## `CAPI` - Control Plane

```yaml
apiVersion: controlplane.cluster.x-k8s.io/v1beta1
kind: KubeadmControlPlane
metadata:
  name: production-control-plane
  namespace: clusters
spec:
  replicas: 3
  version: v1.29.0
  machineTemplate:
    infrastructureRef:
      apiVersion: infrastructure.cluster.x-k8s.io/v1beta2
      kind: AWSMachineTemplate
      name: production-cp
  kubeadmConfigSpec:
    initConfiguration:
      nodeRegistration:
        kubeletExtraArgs:
          cloud-provider: external
    joinConfiguration:
      nodeRegistration:
        kubeletExtraArgs:
          cloud-provider: external
```

---

## `CAPI` - Worker Machines

```yaml
apiVersion: cluster.x-k8s.io/v1beta1
kind: MachineDeployment
metadata:
  name: production-workers
  namespace: clusters
spec:
  clusterName: production
  replicas: 5
  selector:
    matchLabels:
      cluster.x-k8s.io/cluster-name: production
  template:
    spec:
      clusterName: production
      version: v1.29.0
      bootstrap:
        configRef:
          apiVersion: bootstrap.cluster.x-k8s.io/v1beta1
          kind: KubeadmConfigTemplate
          name: production-workers
      infrastructureRef:
        apiVersion: infrastructure.cluster.x-k8s.io/v1beta2
        kind: AWSMachineTemplate
        name: production-workers
---
apiVersion: infrastructure.cluster.x-k8s.io/v1beta2
kind: AWSMachineTemplate
metadata:
  name: production-workers
  namespace: clusters
spec:
  template:
    spec:
      instanceType: m5.xlarge
      iamInstanceProfile: nodes.cluster-api-provider-aws.sigs.k8s.io
      sshKeyName: k8s-admin
      rootVolume:
        size: 100
        type: gp3
```

---

## `CAPI` - Lifecycle Management

```bash
# Install CAPI and providers
clusterctl init \
  --infrastructure aws \
  --bootstrap kubeadm \
  --control-plane kubeadm

# Create cluster
kubectl apply -f cluster.yaml

# Get cluster status
clusterctl describe cluster production

# Get kubeconfig for workload cluster
clusterctl get kubeconfig production > prod.kubeconfig

# Upgrade cluster version
kubectl patch kubeadmcontrolplane production-control-plane \
  --type merge \
  -p '{"spec": {"version": "v1.30.0"}}'

# Scale workers
kubectl scale machinedeployment production-workers \
  --replicas=10

# Delete cluster
kubectl delete cluster production
```

---

## `CAPI` Providers Ecosystem

| Category | Providers |
|----------|-----------|
| Infrastructure | `AWS`, `Azure`, `GCP`, `vSphere`, `OpenStack`, `Metal3` |
| Bootstrap | `kubeadm`, `Talos`, `EKS`, `MicroK8s` |
| Control Plane | `kubeadm`, `Talos`, `Nested` |
| Add-ons | `Helm`, `ClusterResourceSet` |

---

## Multi-Cluster with `CAPI`

```bash
# Manage clusters from management cluster
kubectl get clusters -A
NAMESPACE   NAME         PHASE
clusters    production   Provisioned
clusters    staging      Provisioned
clusters    dev          Provisioned

# Apply workloads to specific cluster
kubectl --kubeconfig=prod.kubeconfig apply -f app.yaml

# Or use tools like ArgoCD for GitOps
argocd cluster add production --kubeconfig=prod.kubeconfig
```

---

## Lab: Provision a Cluster

```bash
# Option A: kubeadm (VMs required)
# 1. Provision VMs (Vagrant, cloud, etc.)
# 2. Install container runtime
# 3. kubeadm init on master
# 4. kubeadm join on workers
# 5. Install CNI

# Option B: CAPI (management cluster required)
# 1. Install CAPI on existing cluster
clusterctl init --infrastructure docker
# 2. Create a CAPD cluster (Docker-based)
kubectl apply -f capd-cluster.yaml
# 3. Watch provisioning
clusterctl describe cluster my-cluster
# 4. Get kubeconfig and test
clusterctl get kubeconfig my-cluster > my.kubeconfig
kubectl --kubeconfig=my.kubeconfig get nodes
```
