# Cluster Administration

---

## Administration Overview

1. **Cluster** lifecycle management
1. **Monitoring** and observability
1. **Backup** and disaster recovery
1. **Upgrades** and maintenance
1. **Scaling** and performance

---

## Cluster Architecture Review

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f9f9f9" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Cluster Components</text>
  <rect x="100" y="80" width="250" height="100" fill="#e3f2fd" stroke="#1976d2" stroke-width="2" rx="5"/>
  <text x="225" y="105" text-anchor="middle" font-weight="bold">Control Plane</text>
  <text x="225" y="125" text-anchor="middle" font-size="10">• API Server</text>
  <text x="225" y="145" text-anchor="middle" font-size="10">• Scheduler, Controller</text>
  <text x="225" y="165" text-anchor="middle" font-size="10">• etcd, Cloud Controller</text>
  <rect x="400" y="80" width="250" height="100" fill="#e8f5e9" stroke="#388e3c" stroke-width="2" rx="5"/>
  <text x="525" y="105" text-anchor="middle" font-weight="bold">Worker Nodes</text>
  <text x="525" y="125" text-anchor="middle" font-size="10">• Kubelet</text>
  <text x="525" y="145" text-anchor="middle" font-size="10">• Container Runtime</text>
  <text x="525" y="165" text-anchor="middle" font-size="10">• Kube-proxy</text>
  <rect x="200" y="210" width="350" height="80" fill="#fff3e0" rx="5"/>
  <text x="375" y="235" text-anchor="middle" font-weight="bold">Add-ons</text>
  <text x="375" y="255" text-anchor="middle" font-size="11">• CoreDNS, CNI Plugin</text>
  <text x="375" y="275" text-anchor="middle" font-size="11">• Metrics Server, Dashboard</text>
</svg>

---

## kubectl Contexts

```bash
# View contexts
kubectl config get-contexts

# Current context
kubectl config current-context

# Create context
kubectl config set-context dev-context \
  --cluster=dev-cluster \
  --user=dev-user \
  --namespace=development

# Switch context
kubectl config use-context dev-context

# Delete context
kubectl config delete-context old-context
```

---

## Managing Multiple Clusters

```bash
# Merge kubeconfig files
KUBECONFIG=~/.kube/config:~/.kube/config-dev \
  kubectl config view --flatten > ~/.kube/config-merged

# Use kubectx for easy switching
kubectx                    # List contexts
kubectx production         # Switch to production
kubectx -                 # Switch to previous

# Use kubens for namespaces
kubens                     # List namespaces
kubens kube-system        # Switch namespace
```

---

## Cluster Information

```bash
# Cluster info
kubectl cluster-info
kubectl cluster-info dump > cluster-dump.txt

# Version info
kubectl version
kubectl api-versions
kubectl api-resources

# Component status
kubectl get componentstatuses

# Node info
kubectl get nodes -o wide
kubectl describe nodes
```

---

## Node Management

```bash
# Cordon node (prevent new pods)
kubectl cordon node-1

# Drain node (evict pods)
kubectl drain node-1 --ignore-daemonsets --delete-emptydir-data

# Uncordon node
kubectl uncordon node-1

# Label nodes
kubectl label nodes node-1 disktype=ssd

# Taint nodes
kubectl taint nodes node-1 key=value:NoSchedule
```

---

## etcd Backup

```bash
# Backup etcd
ETCDCTL_API=3 etcdctl snapshot save snapshot.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Verify backup
ETCDCTL_API=3 etcdctl snapshot status snapshot.db

# Restore etcd
ETCDCTL_API=3 etcdctl snapshot restore snapshot.db \
  --data-dir=/var/lib/etcd-backup
```

---

## Velero Backup

```bash
# Install Velero
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.5.0 \
  --bucket velero-backup \
  --secret-file ./credentials-velero

# Create backup
velero backup create full-backup

# Schedule backup
velero schedule create daily-backup --schedule="0 2 * * *"

# Restore backup
velero restore create --from-backup full-backup
```

---

## Cluster Upgrades

```bash
# Check current version
kubectl version --short

# Upgrade kubeadm
apt update
apt-cache madison kubeadm
apt-mark unhold kubeadm
apt install kubeadm=1.28.0-00
apt-mark hold kubeadm

# Plan upgrade
kubeadm upgrade plan

# Apply upgrade
kubeadm upgrade apply v1.28.0
```

---

## Rolling Node Upgrades

```bash
# On each node:
# 1. Drain node
kubectl drain node-1 --ignore-daemonsets

# 2. Upgrade kubelet and kubectl
apt-mark unhold kubelet kubectl
apt install kubelet=1.28.0-00 kubectl=1.28.0-00
apt-mark hold kubelet kubectl

# 3. Restart kubelet
systemctl daemon-reload
systemctl restart kubelet

# 4. Uncordon node
kubectl uncordon node-1
```

---

## Monitoring Setup

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Monitoring Stack</text>
  <rect x="100" y="80" width="150" height="80" fill="#e6522c" rx="5"/>
  <text x="175" y="110" text-anchor="middle" fill="white" font-weight="bold">Prometheus</text>
  <text x="175" y="130" text-anchor="middle" fill="white" font-size="10">Metrics collection</text>
  <text x="175" y="150" text-anchor="middle" fill="white" font-size="10">Time series DB</text>
  <rect x="270" y="80" width="150" height="80" fill="#f46800" rx="5"/>
  <text x="345" y="110" text-anchor="middle" fill="white" font-weight="bold">Grafana</text>
  <text x="345" y="130" text-anchor="middle" fill="white" font-size="10">Visualization</text>
  <text x="345" y="150" text-anchor="middle" fill="white" font-size="10">Dashboards</text>
  <rect x="440" y="80" width="150" height="80" fill="#e6522c" rx="5"/>
  <text x="515" y="110" text-anchor="middle" fill="white" font-weight="bold">Alertmanager</text>
  <text x="515" y="130" text-anchor="middle" fill="white" font-size="10">Alert routing</text>
  <text x="515" y="150" text-anchor="middle" fill="white" font-size="10">Notifications</text>
  <rect x="610" y="80" width="140" height="80" fill="#4285f4" rx="5"/>
  <text x="680" y="110" text-anchor="middle" fill="white" font-weight="bold">Loki</text>
  <text x="680" y="130" text-anchor="middle" fill="white" font-size="10">Log aggregation</text>
  <text x="680" y="150" text-anchor="middle" fill="white" font-size="10">Like Prometheus</text>
  <rect x="200" y="190" width="400" height="100" fill="#e8f5e9" rx="5"/>
  <text x="400" y="220" text-anchor="middle" font-weight="bold">Data Sources</text>
  <text x="400" y="245" text-anchor="middle" font-size="11">• Node Exporter (system metrics)</text>
  <text x="400" y="265" text-anchor="middle" font-size="11">• kube-state-metrics (K8s objects)</text>
  <text x="400" y="285" text-anchor="middle" font-size="11">• cAdvisor (container metrics)</text>
</svg>

---

## Installing Prometheus

```bash
# Using Helm
helm repo add prometheus-community \
  https://prometheus-community.github.io/helm-charts

helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace

# Access Grafana
kubectl port-forward -n monitoring \
  svc/prometheus-grafana 3000:80

# Default credentials: admin/prom-operator
```

---

## Metrics Server

```bash
# Install metrics server
kubectl apply -f https://github.com/kubernetes-sigs/\
metrics-server/releases/latest/download/components.yaml

# Verify installation
kubectl get deployment metrics-server -n kube-system

# Use metrics
kubectl top nodes
kubectl top pods --all-namespaces
kubectl top pods --containers
```

---

## Logging Architecture

```yaml
# Fluentd DaemonSet for log collection
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: kube-system
spec:
  selector:
    matchLabels:
      name: fluentd
  template:
    spec:
      containers:
      - name: fluentd
        image: fluent/fluentd-kubernetes-daemonset
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: containers
          mountPath: /var/lib/docker/containers
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: containers
        hostPath:
          path: /var/lib/docker/containers
```

---

## Cluster Autoscaling

```yaml
# Cluster Autoscaler
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cluster-autoscaler
  namespace: kube-system
spec:
  template:
    spec:
      containers:
      - image: k8s.gcr.io/autoscaling/cluster-autoscaler:v1.28.0
        name: cluster-autoscaler
        command:
        - ./cluster-autoscaler
        - --v=4
        - --stderrthreshold=info
        - --cloud-provider=aws
        - --skip-nodes-with-local-storage=false
        - --expander=least-waste
        - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled
```

---

## Resource Management

```bash
# Set resource quotas
kubectl create quota my-quota \
  --hard=cpu=10,memory=20Gi,pods=10

# View resource usage
kubectl describe resourcequota my-quota

# Top consumers
kubectl top pods --all-namespaces | sort -k3 -rn | head

# Find pods without limits
kubectl get pods --all-namespaces -o json | \
  jq '.items[] | select(.spec.containers[].resources.limits == null)'
```

---

## Certificate Management

```bash
# Check certificate expiration
kubeadm certs check-expiration

# Renew certificates
kubeadm certs renew all

# Manual certificate generation
openssl req -x509 -newkey rsa:4096 -keyout key.pem \
  -out cert.pem -days 365 -nodes

# Using cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/\
releases/download/v1.13.0/cert-manager.yaml
```

---

## Audit Logging

```yaml
# Audit policy (/etc/kubernetes/audit-policy.yaml)
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
- level: Metadata
  resources:
  - group: ""
    resources: ["secrets", "configmaps"]
- level: RequestResponse
  resources:
  - group: ""
    resources: ["pods", "services"]

# Enable in API server
--audit-log-path=/var/log/kubernetes/audit.log
--audit-policy-file=/etc/kubernetes/audit-policy.yaml
--audit-log-maxage=30
--audit-log-maxbackup=10
--audit-log-maxsize=100
```

---

## Performance Tuning

```bash
# API server tuning
--max-requests-inflight=400
--max-mutating-requests-inflight=200

# etcd tuning
--quota-backend-bytes=8589934592  # 8GB

# Kubelet tuning
--max-pods=110
--pods-per-core=10
--kube-api-qps=50
--kube-api-burst=100

# Network tuning
sysctl -w net.ipv4.ip_forward=1
sysctl -w net.bridge.bridge-nf-call-iptables=1
```

---

## High Availability Setup

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f9f9f9" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">HA Control Plane</text>
  <rect x="100" y="80" width="150" height="50" fill="#4285f4" rx="5"/>
  <text x="175" y="110" text-anchor="middle" fill="white">Load Balancer</text>
  <rect x="50" y="160" width="100" height="60" fill="#34a853" rx="5"/>
  <text x="100" y="185" text-anchor="middle" fill="white" font-size="11">Master 1</text>
  <text x="100" y="205" text-anchor="middle" fill="white" font-size="10">API, etcd</text>
  <rect x="175" y="160" width="100" height="60" fill="#34a853" rx="5"/>
  <text x="225" y="185" text-anchor="middle" fill="white" font-size="11">Master 2</text>
  <text x="225" y="205" text-anchor="middle" fill="white" font-size="10">API, etcd</text>
  <rect x="300" y="160" width="100" height="60" fill="#34a853" rx="5"/>
  <text x="350" y="185" text-anchor="middle" fill="white" font-size="11">Master 3</text>
  <text x="350" y="205" text-anchor="middle" fill="white" font-size="10">API, etcd</text>
  <rect x="450" y="100" width="250" height="180" fill="#fff3e0" rx="5"/>
  <text x="575" y="125" text-anchor="middle" font-weight="bold">Worker Nodes</text>
  <circle cx="500" cy="170" r="20" fill="#fbbc04"/>
  <circle cx="550" cy="170" r="20" fill="#fbbc04"/>
  <circle cx="600" cy="170" r="20" fill="#fbbc04"/>
  <circle cx="650" cy="170" r="20" fill="#fbbc04"/>
  <circle cx="500" cy="220" r="20" fill="#fbbc04"/>
  <circle cx="550" cy="220" r="20" fill="#fbbc04"/>
  <circle cx="600" cy="220" r="20" fill="#fbbc04"/>
  <circle cx="650" cy="220" r="20" fill="#fbbc04"/>
</svg>

---

## Disaster Recovery Plan

1. **Regular backups** of etcd
1. **Document** cluster configuration
1. **Test** restore procedures
1. **Monitor** cluster health
1. **Runbook** for common issues

---

## Security Hardening

```bash
# Disable anonymous auth
--anonymous-auth=false

# Enable RBAC
--authorization-mode=RBAC

# Enable admission controllers
--enable-admission-plugins=NodeRestriction,ResourceQuota,\
  PodSecurityPolicy,SecurityContextDeny

# Encrypt secrets
--encryption-provider-config=/etc/kubernetes/encryption-config.yaml

# Enable audit logging
--audit-log-path=/var/log/kubernetes/audit.log
```

---

## Compliance Scanning

```bash
# CIS Benchmark with kube-bench
kubectl apply -f https://raw.githubusercontent.com/\
aquasecurity/kube-bench/main/job.yaml

kubectl logs job/kube-bench

# Polaris for best practices
kubectl apply -f https://github.com/FairwindsOps/polaris/\
releases/latest/download/dashboard.yaml

kubectl port-forward -n polaris svc/polaris-dashboard 8080:80
```

---

## Cost Optimization

```bash
# Kubecost installation
helm install kubecost kubecost/cost-analyzer \
  --namespace kubecost --create-namespace

# Access dashboard
kubectl port-forward -n kubecost \
  deployment/kubecost-cost-analyzer 9090

# Recommendations:
# - Right-size resources
# - Use spot instances
# - Clean up unused resources
# - Implement pod autoscaling
```

---

## Cluster Cleanup

```bash
# Delete completed pods
kubectl delete pod --field-selector=status.phase==Succeeded

# Delete failed pods
kubectl delete pod --field-selector=status.phase==Failed

# Clean evicted pods
kubectl get pods --all-namespaces | grep Evicted | \
  awk '{print $2 " --namespace=" $1}' | \
  xargs kubectl delete pod

# Prune unused images
docker system prune -a

# Clean unused volumes
docker volume prune
```

---

## Troubleshooting Tools

```bash
# kubectl plugins
kubectl krew install tree
kubectl krew install capacity
kubectl krew install who-can

# k9s - Terminal UI
brew install k9s

# stern - Multi-pod logs
brew install stern
stern my-app --since 1h

# kube-capacity - Resource usage
kube-capacity --pods
```

---

## Maintenance Windows

```bash
# Create PodDisruptionBudget
kubectl create pdb my-pdb --selector=app=myapp \
  --min-available=2

# Cordon nodes for maintenance
for node in node-1 node-2; do
  kubectl cordon $node
done

# Perform maintenance
# ...

# Uncordon nodes
for node in node-1 node-2; do
  kubectl uncordon $node
done
```

---

## Cluster Dashboard

```bash
# Deploy dashboard
kubectl apply -f https://raw.githubusercontent.com/\
kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml

# Create admin user
kubectl create serviceaccount dashboard-admin -n kube-system
kubectl create clusterrolebinding dashboard-admin \
  --clusterrole=cluster-admin \
  --serviceaccount=kube-system:dashboard-admin

# Get token
kubectl -n kube-system create token dashboard-admin

# Access dashboard
kubectl proxy
# http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
```

---

## Advanced Workloads

```yaml
# Job for batch processing
apiVersion: batch/v1
kind: Job
metadata:
  name: batch-job
spec:
  completions: 10
  parallelism: 2
  backoffLimit: 4
  template:
    spec:
      containers:
      - name: worker
        image: myapp:batch
      restartPolicy: Never

# CronJob for scheduled tasks
apiVersion: batch/v1
kind: CronJob
metadata:
  name: backup-job
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: myapp:backup
```

---

## Multi-Container Patterns

```yaml
# Sidecar pattern
spec:
  containers:
  - name: app
    image: myapp
  - name: logging-agent
    image: fluentd

# Init container pattern
spec:
  initContainers:
  - name: init-db
    image: busybox
    command: ['sh', '-c', 'until nc -z db 3306; do sleep 1; done']
  containers:
  - name: app
    image: myapp

# Ambassador pattern
spec:
  containers:
  - name: app
    image: myapp
  - name: proxy
    image: nginx
```

---

## Custom Resources (CRDs)

```yaml
# Define CRD
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: databases.example.com
spec:
  group: example.com
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
            properties:
              size:
                type: string
  scope: Namespaced
  names:
    plural: databases
    singular: database
    kind: Database
```

---

## Operators Pattern

```go
// Simplified operator logic
func (r *DatabaseReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    // Get custom resource
    var database v1.Database
    if err := r.Get(ctx, req.NamespacedName, &database); err != nil {
        return ctrl.Result{}, err
    }

    // Create/update resources based on spec
    deployment := r.deploymentForDatabase(&database)
    service := r.serviceForDatabase(&database)

    // Apply resources
    if err := r.Create(ctx, deployment); err != nil {
        return ctrl.Result{}, err
    }

    return ctrl.Result{}, nil
}
```

---

## Service Mesh Overview

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Service Mesh Options</text>
  <rect x="100" y="80" width="150" height="100" fill="#466bb0" rx="5"/>
  <text x="175" y="110" text-anchor="middle" fill="white" font-weight="bold">Istio</text>
  <text x="175" y="135" text-anchor="middle" fill="white" font-size="10">Feature rich</text>
  <text x="175" y="155" text-anchor="middle" fill="white" font-size="10">Complex</text>
  <text x="175" y="175" text-anchor="middle" fill="white" font-size="10">Envoy proxy</text>
  <rect x="270" y="80" width="150" height="100" fill="#26d0ce" rx="5"/>
  <text x="345" y="110" text-anchor="middle" font-weight="bold">Linkerd</text>
  <text x="345" y="135" text-anchor="middle" font-size="10">Lightweight</text>
  <text x="345" y="155" text-anchor="middle" font-size="10">Simple</text>
  <text x="345" y="175" text-anchor="middle" font-size="10">Rust proxy</text>
  <rect x="440" y="80" width="150" height="100" fill="#00d1b2" rx="5"/>
  <text x="515" y="110" text-anchor="middle" font-weight="bold">Consul</text>
  <text x="515" y="135" text-anchor="middle" font-size="10">Multi-platform</text>
  <text x="515" y="155" text-anchor="middle" font-size="10">Service discovery</text>
  <text x="515" y="175" text-anchor="middle" font-size="10">HashiCorp</text>
  <rect x="200" y="210" width="400" height="80" fill="#e8f5e9" rx="5"/>
  <text x="400" y="240" text-anchor="middle" font-weight="bold">Common Features</text>
  <text x="400" y="265" text-anchor="middle" font-size="11">Traffic management, Security (mTLS), Observability</text>
</svg>

---

## Best Practices Summary

1. **Automate** everything possible
1. **Monitor** proactively
1. **Backup** regularly
1. **Document** procedures
1. **Test** disaster recovery

---

## Summary

1. Effective cluster administration is critical
1. Monitoring and logging are essential
1. Regular backups prevent disasters
1. Automation reduces human error
1. Continuous learning and improvement
