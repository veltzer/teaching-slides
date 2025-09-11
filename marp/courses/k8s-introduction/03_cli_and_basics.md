# CLI and Kubernetes Basics

---

## kubectl Overview

1. **Command-line tool** for Kubernetes
1. **Communicates** with API server
1. **Manages** cluster resources
1. **Universal** across all Kubernetes clusters
1. **Declarative** and imperative operations

---

## kubectl Command Structure

```bash
kubectl [command] [TYPE] [NAME] [flags]
```

1. **command**: Operation (get, create, delete)
1. **TYPE**: Resource type (pod, service)
1. **NAME**: Resource name (optional)
1. **flags**: Additional options

---

## Essential kubectl Commands

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">kubectl Command Categories</text>
  <rect x="100" y="80" width="150" height="80" fill="#4285f4" rx="5"/>
  <text x="175" y="110" text-anchor="middle" fill="white" font-weight="bold">Basic</text>
  <text x="175" y="130" text-anchor="middle" fill="white" font-size="11">get, create</text>
  <text x="175" y="145" text-anchor="middle" fill="white" font-size="11">delete, edit</text>
  <rect x="270" y="80" width="150" height="80" fill="#34a853" rx="5"/>
  <text x="345" y="110" text-anchor="middle" fill="white" font-weight="bold">Debugging</text>
  <text x="345" y="130" text-anchor="middle" fill="white" font-size="11">describe, logs</text>
  <text x="345" y="145" text-anchor="middle" fill="white" font-size="11">exec, port-forward</text>
  <rect x="440" y="80" width="150" height="80" fill="#fbbc04" rx="5"/>
  <text x="515" y="110" text-anchor="middle" font-weight="bold">Deployment</text>
  <text x="515" y="130" text-anchor="middle" font-size="11">apply, rollout</text>
  <text x="515" y="145" text-anchor="middle" font-size="11">scale, autoscale</text>
  <rect x="610" y="80" width="140" height="80" fill="#ea4335" rx="5"/>
  <text x="680" y="110" text-anchor="middle" fill="white" font-weight="bold">Cluster</text>
  <text x="680" y="130" text-anchor="middle" fill="white" font-size="11">cluster-info</text>
  <text x="680" y="145" text-anchor="middle" fill="white" font-size="11">top, version</text>
  <rect x="100" y="190" width="150" height="80" fill="#9c27b0" rx="5"/>
  <text x="175" y="220" text-anchor="middle" fill="white" font-weight="bold">Config</text>
  <text x="175" y="240" text-anchor="middle" fill="white" font-size="11">config, label</text>
  <text x="175" y="255" text-anchor="middle" fill="white" font-size="11">annotate, patch</text>
  <rect x="270" y="190" width="150" height="80" fill="#607d8b" rx="5"/>
  <text x="345" y="220" text-anchor="middle" fill="white" font-weight="bold">Advanced</text>
  <text x="345" y="240" text-anchor="middle" fill="white" font-size="11">proxy, cp</text>
  <text x="345" y="255" text-anchor="middle" fill="white" font-size="11">auth, plugin</text>
</svg>

---

## Getting Started

```bash
# Check kubectl version
kubectl version --short

# View cluster information
kubectl cluster-info

# Check available nodes
kubectl get nodes

# View all resources
kubectl get all
```

---

## Resource Types

```bash
# List all resource types
kubectl api-resources

# Short names
kubectl api-resources --verbs=list --namespaced

# Common short names
po    → pods
svc   → services
deploy → deployments
rs    → replicasets
cm    → configmaps
```

---

## Creating a Cluster

```bash
# With Minikube
minikube start

# Verify cluster
kubectl cluster-info

# Check component status
kubectl get componentstatuses

# View cluster events
kubectl get events
```

---

## First Deployment

```bash
# Create deployment imperatively
kubectl create deployment hello-node \
  --image=k8s.gcr.io/echoserver:1.10

# Check deployment
kubectl get deployments

# Check pods
kubectl get pods

# Check replica sets
kubectl get replicasets
```

---

## Deployment Process Flow

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="30" text-anchor="middle" font-size="16" font-weight="bold">Deployment Creation Flow</text>
  <rect x="50" y="60" width="140" height="60" fill="#4285f4" rx="5"/>
  <text x="120" y="95" text-anchor="middle" fill="white">kubectl create</text>
  <rect x="230" y="60" width="140" height="60" fill="#34a853" rx="5"/>
  <text x="300" y="95" text-anchor="middle" fill="white">API Server</text>
  <rect x="410" y="60" width="140" height="60" fill="#fbbc04" rx="5"/>
  <text x="480" y="95" text-anchor="middle">etcd Store</text>
  <rect x="590" y="60" width="140" height="60" fill="#ea4335" rx="5"/>
  <text x="660" y="95" text-anchor="middle" fill="white">Controller</text>
  <rect x="230" y="160" width="140" height="60" fill="#9c27b0" rx="5"/>
  <text x="300" y="195" text-anchor="middle" fill="white">Scheduler</text>
  <rect x="410" y="160" width="140" height="60" fill="#607d8b" rx="5"/>
  <text x="480" y="195" text-anchor="middle" fill="white">Kubelet</text>
  <rect x="590" y="160" width="140" height="60" fill="#ff5722" rx="5"/>
  <text x="660" y="195" text-anchor="middle" fill="white">Container</text>
  <rect x="320" y="260" width="160" height="80" fill="#4caf50" rx="5"/>
  <text x="400" y="305" text-anchor="middle" fill="white">Running Pod</text>
  <path d="M 190 90 L 225 90" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 370 90 L 405 90" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 550 90 L 585 90" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 660 120 L 300 155" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 370 190 L 405 190" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 550 190 L 585 190" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 660 220 L 480 255" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
</svg>

---

## Viewing Resources

```bash
# List pods
kubectl get pods

# List with more details
kubectl get pods -o wide

# Watch for changes
kubectl get pods -w

# All namespaces
kubectl get pods --all-namespaces
kubectl get pods -A
```

---

## Output Formats

```bash
# YAML output
kubectl get pod my-pod -o yaml

# JSON output
kubectl get pod my-pod -o json

# Custom columns
kubectl get pods -o custom-columns=\
NAME:.metadata.name,STATUS:.status.phase

# JSONPath
kubectl get pods -o jsonpath='{.items[*].metadata.name}'
```

---

## Describing Resources

```bash
# Describe pod
kubectl describe pod my-pod

# Describe deployment
kubectl describe deployment my-deployment

# Describe node
kubectl describe node minikube

# Describe service
kubectl describe service my-service
```

---

## Creating Resources

```bash
# From YAML file
kubectl create -f pod.yaml

# From URL
kubectl create -f https://example.com/pod.yaml

# From directory
kubectl create -f ./configs/

# Dry run
kubectl create deployment test --image=nginx --dry-run=client
```

---

## Imperative vs Declarative

## Imperative Commands
```bash
kubectl create deployment nginx --image=nginx
kubectl expose deployment nginx --port=80
kubectl scale deployment nginx --replicas=3
```

## Declarative Approach
```bash
kubectl apply -f nginx-deployment.yaml
kubectl apply -f nginx-service.yaml
```

---

## Basic YAML Structure

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    app: nginx
spec:
  containers:
  - name: nginx
    image: nginx:1.21
    ports:
    - containerPort: 80
```

---

## Applying Configurations

```bash
# Apply configuration
kubectl apply -f config.yaml

# Apply with record
kubectl apply -f config.yaml --record

# Apply from stdin
cat config.yaml | kubectl apply -f -

# Apply multiple files
kubectl apply -f file1.yaml -f file2.yaml
```

---

## Editing Resources

```bash
# Edit deployment
kubectl edit deployment my-deployment

# Edit with different editor
KUBE_EDITOR="nano" kubectl edit deployment my-deployment

# Edit and save to file
kubectl get deployment my-deployment -o yaml > dep.yaml
# Edit dep.yaml
kubectl apply -f dep.yaml
```

---

## Deleting Resources

```bash
# Delete by name
kubectl delete pod my-pod

# Delete by file
kubectl delete -f pod.yaml

# Delete by label
kubectl delete pods -l app=test

# Delete all pods
kubectl delete pods --all

# Force delete
kubectl delete pod my-pod --grace-period=0 --force
```

---

## Labels and Selectors

```bash
# Add label
kubectl label pod my-pod env=production

# Update label
kubectl label pod my-pod env=staging --overwrite

# Remove label
kubectl label pod my-pod env-

# Select by label
kubectl get pods -l env=production
kubectl get pods -l 'env in (production, staging)'
```

---

## Namespaces

```bash
# List namespaces
kubectl get namespaces

# Create namespace
kubectl create namespace development

# Use namespace
kubectl get pods -n development

# Set default namespace
kubectl config set-context --current --namespace=development
```

---

## Working with Namespaces

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f9f9f9" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Kubernetes Namespaces</text>
  <rect x="100" y="80" width="180" height="240" fill="#e3f2fd" stroke="#1976d2" stroke-width="2" rx="5"/>
  <text x="190" y="105" text-anchor="middle" font-weight="bold">default</text>
  <circle cx="140" cy="150" r="25" fill="#4285f4"/>
  <text x="140" y="155" text-anchor="middle" fill="white" font-size="11">Pod</text>
  <circle cx="210" cy="150" r="25" fill="#4285f4"/>
  <text x="210" y="155" text-anchor="middle" fill="white" font-size="11">Pod</text>
  <rect x="120" y="200" width="80" height="40" fill="#34a853" rx="3"/>
  <text x="160" y="225" text-anchor="middle" fill="white" font-size="11">Service</text>
  <rect x="120" y="260" width="80" height="40" fill="#fbbc04" rx="3"/>
  <text x="160" y="285" text-anchor="middle" font-size="11">ConfigMap</text>
  <rect x="310" y="80" width="180" height="240" fill="#e8f5e9" stroke="#388e3c" stroke-width="2" rx="5"/>
  <text x="400" y="105" text-anchor="middle" font-weight="bold">kube-system</text>
  <circle cx="350" cy="150" r="25" fill="#34a853"/>
  <text x="350" y="155" text-anchor="middle" fill="white" font-size="11">DNS</text>
  <circle cx="420" cy="150" r="25" fill="#34a853"/>
  <text x="420" y="155" text-anchor="middle" fill="white" font-size="11">Proxy</text>
  <rect x="330" y="200" width="80" height="40" fill="#4285f4" rx="3"/>
  <text x="370" y="225" text-anchor="middle" fill="white" font-size="11">Controller</text>
  <rect x="520" y="80" width="180" height="240" fill="#fff3e0" stroke="#ff9800" stroke-width="2" rx="5"/>
  <text x="610" y="105" text-anchor="middle" font-weight="bold">production</text>
  <circle cx="560" cy="150" r="25" fill="#ff9800"/>
  <text x="560" y="155" text-anchor="middle" fill="white" font-size="11">App</text>
  <circle cx="630" cy="150" r="25" fill="#ff9800"/>
  <text x="630" y="155" text-anchor="middle" fill="white" font-size="11">App</text>
  <rect x="540" y="200" width="80" height="40" fill="#ea4335" rx="3"/>
  <text x="580" y="225" text-anchor="middle" fill="white" font-size="11">Service</text>
</svg>

---

## Logs and Debugging

```bash
# View logs
kubectl logs my-pod

# Follow logs
kubectl logs -f my-pod

# Previous container logs
kubectl logs my-pod --previous

# Multi-container pod
kubectl logs my-pod -c container-name

# Tail logs
kubectl logs my-pod --tail=50
```

---

## Executing Commands

```bash
# Execute command
kubectl exec my-pod -- ls /

# Interactive shell
kubectl exec -it my-pod -- /bin/bash

# Specific container
kubectl exec -it my-pod -c container-name -- /bin/sh

# Run command and exit
kubectl exec my-pod -- cat /etc/hostname
```

---

## Port Forwarding

```bash
# Forward local port to pod
kubectl port-forward my-pod 8080:80

# Forward to deployment
kubectl port-forward deployment/my-deployment 8080:80

# Forward to service
kubectl port-forward service/my-service 8080:80

# Bind to all interfaces
kubectl port-forward --address 0.0.0.0 my-pod 8080:80
```

---

## Copying Files

```bash
# Copy from local to pod
kubectl cp ./local-file my-pod:/tmp/remote-file

# Copy from pod to local
kubectl cp my-pod:/tmp/remote-file ./local-file

# Copy with container
kubectl cp my-pod:/tmp/file ./file -c container-name

# Copy directory
kubectl cp ./local-dir my-pod:/tmp/remote-dir
```

---

## Scaling Applications

```bash
# Scale deployment
kubectl scale deployment my-deployment --replicas=5

# Scale with condition
kubectl scale deployment my-deployment --replicas=10 \
  --current-replicas=5

# Autoscale
kubectl autoscale deployment my-deployment \
  --min=2 --max=10 --cpu-percent=80
```

---

## Exposing Applications

```bash
# Expose deployment
kubectl expose deployment my-deployment --port=80

# Expose with type
kubectl expose deployment my-deployment \
  --port=80 --type=LoadBalancer

# Expose pod
kubectl expose pod my-pod --port=80 --name=my-service

# Expose with target port
kubectl expose deployment my-deployment \
  --port=8080 --target-port=80
```

---

## Service Types

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Kubernetes Service Types</text>
  <rect x="100" y="100" width="150" height="200" fill="#4285f4" rx="5"/>
  <text x="175" y="130" text-anchor="middle" fill="white" font-weight="bold">ClusterIP</text>
  <text x="175" y="155" text-anchor="middle" fill="white" font-size="11">Internal only</text>
  <circle cx="175" cy="200" r="20" fill="white"/>
  <text x="175" y="205" text-anchor="middle" font-size="10">Pod</text>
  <circle cx="175" cy="250" r="20" fill="white"/>
  <text x="175" y="255" text-anchor="middle" font-size="10">Pod</text>
  <rect x="275" y="100" width="150" height="200" fill="#34a853" rx="5"/>
  <text x="350" y="130" text-anchor="middle" fill="white" font-weight="bold">NodePort</text>
  <text x="350" y="155" text-anchor="middle" fill="white" font-size="11">Node IP:Port</text>
  <rect x="295" y="180" width="110" height="30" fill="white" rx="3"/>
  <text x="350" y="200" text-anchor="middle" font-size="10">30000-32767</text>
  <rect x="450" y="100" width="150" height="200" fill="#fbbc04" rx="5"/>
  <text x="525" y="130" text-anchor="middle" font-weight="bold">LoadBalancer</text>
  <text x="525" y="155" text-anchor="middle" font-size="11">External LB</text>
  <rect x="470" y="180" width="110" height="30" fill="white" rx="3"/>
  <text x="525" y="200" text-anchor="middle" font-size="10">Cloud Provider</text>
  <rect x="625" y="100" width="125" height="200" fill="#ea4335" rx="5"/>
  <text x="687" y="130" text-anchor="middle" fill="white" font-weight="bold">ExternalName</text>
  <text x="687" y="155" text-anchor="middle" fill="white" font-size="11">DNS CNAME</text>
  <rect x="635" y="180" width="105" height="30" fill="white" rx="3"/>
  <text x="687" y="200" text-anchor="middle" font-size="10">External DNS</text>
</svg>

---

## Rolling Updates

```bash
# Update image
kubectl set image deployment/my-deployment \
  nginx=nginx:1.21

# Check rollout status
kubectl rollout status deployment/my-deployment

# Pause rollout
kubectl rollout pause deployment/my-deployment

# Resume rollout
kubectl rollout resume deployment/my-deployment
```

---

## Rollback

```bash
# View rollout history
kubectl rollout history deployment/my-deployment

# Rollback to previous
kubectl rollout undo deployment/my-deployment

# Rollback to specific revision
kubectl rollout undo deployment/my-deployment --to-revision=2

# Check rollback status
kubectl rollout status deployment/my-deployment
```

---

## Resource Management

```bash
# View resource usage
kubectl top nodes
kubectl top pods

# With containers
kubectl top pod my-pod --containers

# Sort by CPU
kubectl top pods --sort-by=cpu

# Sort by memory
kubectl top pods --sort-by=memory
```

---

## Contexts and Clusters

```bash
# View contexts
kubectl config get-contexts

# Current context
kubectl config current-context

# Switch context
kubectl config use-context production

# Set cluster
kubectl config set-cluster my-cluster --server=https://1.2.3.4

# Set credentials
kubectl config set-credentials user --token=token
```

---

## kubectl Plugins

```bash
# List available plugins
kubectl plugin list

# Install krew (plugin manager)
curl -fsSL https://github.com/kubernetes-sigs/krew/\
releases/latest/download/krew.tar.gz | tar -xz
./krew-linux_amd64 install krew

# Install plugin
kubectl krew install tree
kubectl tree deployment my-deployment
```

---

## Useful Aliases

```bash
# Common aliases
alias k=kubectl
alias kgp='kubectl get pods'
alias kgs='kubectl get services'
alias kgd='kubectl get deployments'

# Apply alias
alias ka='kubectl apply -f'

# Delete alias
alias kdel='kubectl delete'

# Describe alias
alias kdes='kubectl describe'
```

---

## JSONPath Queries

```bash
# Get pod IPs
kubectl get pods -o jsonpath='{.items[*].status.podIP}'

# Get container images
kubectl get pods -o jsonpath=\
'{.items[*].spec.containers[*].image}'

# Custom format
kubectl get pods -o jsonpath=\
'{range .items[*]}{.metadata.name}{"\t"}{.status.phase}{"\n"}{end}'
```

---

## Dry Run and Diff

```bash
# Dry run (client-side)
kubectl apply -f config.yaml --dry-run=client

# Dry run (server-side)
kubectl apply -f config.yaml --dry-run=server

# Show diff
kubectl diff -f config.yaml

# Generate YAML
kubectl create deployment test --image=nginx \
  --dry-run=client -o yaml > deployment.yaml
```

---

## Wait Conditions

```bash
# Wait for pod to be ready
kubectl wait --for=condition=ready pod/my-pod

# Wait with timeout
kubectl wait --for=condition=ready pod/my-pod --timeout=60s

# Wait for deletion
kubectl wait --for=delete pod/my-pod --timeout=60s

# Wait for deployment
kubectl wait --for=condition=available \
  deployment/my-deployment --timeout=300s
```

---

## Field Selectors

```bash
# Select by field
kubectl get pods --field-selector status.phase=Running

# Multiple fields
kubectl get pods --field-selector \
  status.phase=Running,metadata.namespace=default

# Not equal
kubectl get pods --field-selector status.phase!=Running

# Combine with labels
kubectl get pods -l app=nginx \
  --field-selector status.phase=Running
```

---

## Resource Quotas

```bash
# View quotas
kubectl get resourcequota

# Describe quota
kubectl describe resourcequota my-quota

# Create quota
kubectl create quota my-quota \
  --hard=cpu=1000,memory=200Gi,pods=10

# Edit quota
kubectl edit resourcequota my-quota
```

---

## API Resources

```bash
# List all resources
kubectl api-resources

# Namespaced resources
kubectl api-resources --namespaced=true

# Non-namespaced resources
kubectl api-resources --namespaced=false

# By API group
kubectl api-resources --api-group=apps
```

---

## Proxy and API Access

```bash
# Start proxy
kubectl proxy

# Access API via proxy
curl http://localhost:8001/api/v1/namespaces/default/pods

# Direct API access
kubectl get --raw /api/v1/namespaces/default/pods

# API versions
kubectl api-versions
```

---

## Tips and Tricks

1. **Tab completion**: Enable for faster typing
1. **Aliases**: Create for common commands
1. **Contexts**: Separate dev/prod environments
1. **Dry run**: Always test before applying
1. **Labels**: Use consistently for organization

---

## Common Patterns

```bash
# Quick pod for testing
kubectl run test --image=busybox --rm -it -- /bin/sh

# Debug pod
kubectl run debug --image=nicolaka/netshoot --rm -it -- /bin/bash

# Get all resources
kubectl get all -A

# Delete all in namespace
kubectl delete all --all -n test
```

---

## Troubleshooting Commands

```bash
# Get events
kubectl get events --sort-by='.lastTimestamp'

# Describe for details
kubectl describe pod my-pod | grep -A 10 Events

# Check logs
kubectl logs my-pod --previous

# Resource usage
kubectl top pod my-pod --containers
```

---

## Summary

1. `kubectl` is the primary Kubernetes CLI
1. Supports imperative and declarative operations
1. Rich set of commands for all operations
1. Multiple output formats available
1. Essential tool for Kubernetes management
