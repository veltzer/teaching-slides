# Troubleshooting

---

## Troubleshooting Overview

1. **Systematic approach** to problems
1. **Understanding** error messages
1. **Using** the right tools
1. **Checking** logs and events
1. **Common** patterns and solutions

---

## Troubleshooting Workflow

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="30" text-anchor="middle" font-size="16" font-weight="bold">Troubleshooting Process</text>
  <rect x="100" y="60" width="150" height="60" fill="#4285f4" rx="5"/>
  <text x="175" y="95" text-anchor="middle" fill="white">1. Identify Issue</text>
  <rect x="280" y="60" width="150" height="60" fill="#34a853" rx="5"/>
  <text x="355" y="95" text-anchor="middle" fill="white">2. Gather Info</text>
  <rect x="460" y="60" width="150" height="60" fill="#fbbc04" rx="5"/>
  <text x="535" y="95" text-anchor="middle">3. Analyze</text>
  <rect x="640" y="60" width="110" height="60" fill="#ea4335" rx="5"/>
  <text x="695" y="95" text-anchor="middle" fill="white">4. Fix</text>
  <rect x="200" y="160" width="400" height="180" fill="#e8f5e9" rx="5"/>
  <text x="400" y="190" text-anchor="middle" font-weight="bold">Information Sources</text>
  <text x="400" y="215" text-anchor="middle" font-size="12">• kubectl describe</text>
  <text x="400" y="235" text-anchor="middle" font-size="12">• kubectl logs</text>
  <text x="400" y="255" text-anchor="middle" font-size="12">• kubectl get events</text>
  <text x="400" y="275" text-anchor="middle" font-size="12">• kubectl exec</text>
  <text x="400" y="295" text-anchor="middle" font-size="12">• kubectl debug</text>
  <text x="400" y="315" text-anchor="middle" font-size="12">• Metrics and monitoring</text>
</svg>

---

## Common Pod Issues

1. **Pending**: Cannot be scheduled
1. **ImagePullBackOff**: Cannot pull image
1. **CrashLoopBackOff**: Container crashes
1. **RunContainerError**: Cannot start container
1. **OOMKilled**: Out of memory

---

## Pod Stuck in Pending

```bash
# Check pod status
kubectl get pod my-pod -o wide

# Check events
kubectl describe pod my-pod

# Common causes:
# - Insufficient resources
# - Node selector not matching
# - PVC not bound
# - Taints without tolerations

# Check node resources
kubectl top nodes
kubectl describe nodes
```

---

## ImagePullBackOff

```bash
# Check image details
kubectl describe pod my-pod | grep -A 5 "Image:"

# Common causes:
# - Wrong image name/tag
# - Private registry without secret
# - Registry down/unreachable
# - Rate limiting (Docker Hub)

# Fix: Create image pull secret
kubectl create secret docker-registry regcred \
  --docker-server=registry.io \
  --docker-username=user \
  --docker-password=pass
```

---

## CrashLoopBackOff

```bash
# Check logs
kubectl logs my-pod
kubectl logs my-pod --previous

# Check exit code
kubectl describe pod my-pod | grep -A 10 "Last State"

# Common causes:
# - Application error
# - Missing configuration
# - Wrong command/args
# - Health check failures

# Debug with shell
kubectl run debug --image=busybox --rm -it -- sh
```

---

## OOMKilled

```bash
# Check resource usage
kubectl top pod my-pod

# Check limits
kubectl describe pod my-pod | grep -A 5 "Limits:"

# View OOM events
kubectl get events --field-selector reason=OOMKilling

# Fix: Increase memory limits
resources:
  limits:
    memory: "512Mi"  # Increase this
  requests:
    memory: "256Mi"
```

---

## Debugging Deployments

```bash
# Check deployment status
kubectl get deployment my-app
kubectl describe deployment my-app

# Check rollout status
kubectl rollout status deployment/my-app

# Check replica sets
kubectl get rs -l app=my-app

# Common issues:
# - Insufficient quota
# - Image pull errors
# - Readiness probe failures
```

---

## Service Not Working

```bash
# Check service
kubectl get svc my-service
kubectl describe svc my-service

# Check endpoints
kubectl get endpoints my-service

# Test DNS
kubectl run test --image=busybox --rm -it -- \
  nslookup my-service

# Test connectivity
kubectl run test --image=nicolaka/netshoot --rm -it -- \
  curl my-service:80

# Common issues:
# - Selector not matching pods
# - Wrong target port
# - Network policies blocking
```

---

## Ingress Issues

```bash
# Check ingress
kubectl get ingress
kubectl describe ingress my-ingress

# Check ingress controller
kubectl get pods -n ingress-nginx
kubectl logs -n ingress-nginx deployment/ingress-nginx-controller

# Test with curl
curl -H "Host: app.example.com" http://ingress-ip/

# Common issues:
# - No ingress controller installed
# - Wrong host/path configuration
# - Backend service not found
# - TLS certificate issues
```

---

## Storage Problems

```bash
# Check PVC status
kubectl get pvc
kubectl describe pvc my-pvc

# Check PV status
kubectl get pv
kubectl describe pv

# Common issues:
# - No matching PV for PVC
# - Access mode mismatch
# - Storage class not found
# - Insufficient storage quota

# Check storage class
kubectl get storageclass
```

---

## Node Issues

```bash
# Check node status
kubectl get nodes
kubectl describe node node-name

# Check node conditions
kubectl get nodes -o json | \
  jq '.items[].status.conditions'

# Cordon node (prevent scheduling)
kubectl cordon node-name

# Drain node (move pods)
kubectl drain node-name --ignore-daemonsets

# Uncordon node
kubectl uncordon node-name
```

---

## Using kubectl debug

```bash
# Debug running pod
kubectl debug my-pod -it --image=busybox

# Debug with shared namespaces
kubectl debug my-pod -it --image=nicolaka/netshoot \
  --target=my-container

# Create debug copy of pod
kubectl debug my-pod -it --image=busybox \
  --copy-to=my-pod-debug

# Debug node
kubectl debug node/my-node -it --image=busybox
```

---

## Ephemeral Debug Containers

```bash
# Add ephemeral container
kubectl debug -it my-pod --image=busybox \
  --target=my-container -- sh

# View ephemeral containers
kubectl describe pod my-pod | grep -A 10 "Ephemeral"

# Use cases:
# - Debugging distroless images
# - Adding debugging tools
# - Network troubleshooting
# - File system inspection
```

---

## Logs Investigation

```bash
# View logs
kubectl logs pod-name
kubectl logs pod-name -c container-name
kubectl logs pod-name --all-containers

# Follow logs
kubectl logs -f pod-name

# Previous container logs
kubectl logs pod-name --previous

# Logs with timestamps
kubectl logs pod-name --timestamps

# Tail logs
kubectl logs pod-name --tail=100

# Logs since time
kubectl logs pod-name --since=1h
```

---

## Events Analysis

```bash
# Get all events
kubectl get events --sort-by='.lastTimestamp'

# Events for specific object
kubectl get events --field-selector \
  involvedObject.name=my-pod

# Watch events
kubectl get events --watch

# Events in namespace
kubectl get events -n my-namespace

# Filter by type
kubectl get events --field-selector type=Warning
```

---

## Network Troubleshooting

```bash
# Test DNS
kubectl run test --image=busybox --rm -it -- \
  nslookup kubernetes.default

# Test connectivity
kubectl run test --image=nicolaka/netshoot --rm -it -- bash
# Inside container:
curl service-name:port
nc -zv service-name port
ping pod-ip

# Check network policies
kubectl get networkpolicies

# Port forwarding for testing
kubectl port-forward pod-name 8080:80
```

---

## Performance Issues

```bash
# Check resource usage
kubectl top nodes
kubectl top pods
kubectl top pods --containers

# Check resource requests/limits
kubectl describe pod my-pod | grep -A 10 "Containers:"

# Check HPA status
kubectl get hpa
kubectl describe hpa my-hpa

# Check metrics server
kubectl get deployment metrics-server -n kube-system
```

---

## RBAC Troubleshooting

```bash
# Check permissions
kubectl auth can-i create pods
kubectl auth can-i create pods --as=jane
kubectl auth can-i create pods --as=system:serviceaccount:default:mysa

# List permissions
kubectl auth can-i --list

# Check roles and bindings
kubectl get roles,rolebindings
kubectl get clusterroles,clusterrolebindings

# Describe role
kubectl describe role my-role
```

---

## ConfigMap/Secret Issues

```bash
# Check if mounted
kubectl describe pod my-pod | grep -A 10 "Mounts:"

# Check if exists
kubectl get configmap my-config
kubectl get secret my-secret

# Verify content
kubectl get configmap my-config -o yaml
kubectl get secret my-secret -o jsonpath='{.data.key}' | base64 -d

# Common issues:
# - Wrong name referenced
# - Wrong key in configmap/secret
# - Missing in namespace
```

---

## CrashLoopBackOff Diagnosis

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">CrashLoopBackOff Diagnosis</text>
  <rect x="100" y="80" width="200" height="60" fill="#4285f4" rx="5"/>
  <text x="200" y="110" text-anchor="middle" fill="white" font-weight="bold">Check Logs</text>
  <text x="200" y="125" text-anchor="middle" fill="white" font-size="10">kubectl logs pod --previous</text>
  <rect x="320" y="80" width="200" height="60" fill="#34a853" rx="5"/>
  <text x="420" y="110" text-anchor="middle" fill="white" font-weight="bold">Check Exit Code</text>
  <text x="420" y="125" text-anchor="middle" fill="white" font-size="10">kubectl describe pod</text>
  <rect x="540" y="80" width="200" height="60" fill="#fbbc04" rx="5"/>
  <text x="640" y="110" text-anchor="middle" font-weight="bold">Check Resources</text>
  <text x="640" y="125" text-anchor="middle" font-size="10">Memory/CPU limits</text>
  <rect x="100" y="160" width="640" height="150" fill="#e8f5e9" rx="5"/>
  <text x="420" y="185" text-anchor="middle" font-weight="bold">Common Exit Codes</text>
  <text x="250" y="210" text-anchor="start" font-size="11">• 0: Success (check restart policy)</text>
  <text x="250" y="230" text-anchor="start" font-size="11">• 1: General errors</text>
  <text x="250" y="250" text-anchor="start" font-size="11">• 125: Container failed to run</text>
  <text x="250" y="270" text-anchor="start" font-size="11">• 126: Container command not executable</text>
  <text x="250" y="290" text-anchor="start" font-size="11">• 127: Container command not found</text>
  <text x="500" y="210" text-anchor="start" font-size="11">• 128+n: Fatal signal n</text>
  <text x="500" y="230" text-anchor="start" font-size="11">• 137: SIGKILL (OOM)</text>
  <text x="500" y="250" text-anchor="start" font-size="11">• 139: SIGSEGV</text>
  <text x="500" y="270" text-anchor="start" font-size="11">• 143: SIGTERM</text>
</svg>

---

## DNS Troubleshooting

```bash
# Check CoreDNS pods
kubectl get pods -n kube-system -l k8s-app=kube-dns

# Check CoreDNS logs
kubectl logs -n kube-system -l k8s-app=kube-dns

# Test DNS resolution
kubectl run test --image=busybox --rm -it -- sh
# Inside pod:
nslookup kubernetes.default
nslookup my-service.my-namespace
cat /etc/resolv.conf

# Check DNS config
kubectl get configmap coredns -n kube-system -o yaml
```

---

## Cluster Component Issues

```bash
# Check control plane components
kubectl get pods -n kube-system

# Check component status
kubectl get componentstatuses

# Check API server
kubectl get --raw /healthz

# Check etcd
kubectl exec -n kube-system etcd-master -- \
  etcdctl endpoint health

# Check scheduler
kubectl logs -n kube-system kube-scheduler-master

# Check controller manager
kubectl logs -n kube-system kube-controller-manager-master
```

---

## Using Metrics

```bash
# Install metrics server if not present
kubectl apply -f https://github.com/kubernetes-sigs/\
metrics-server/releases/latest/download/components.yaml

# View node metrics
kubectl top nodes

# View pod metrics
kubectl top pods --all-namespaces
kubectl top pods --sort-by=memory
kubectl top pods --sort-by=cpu

# Container metrics
kubectl top pod my-pod --containers
```

---

## Common Error Messages

```yaml
# ErrImagePull
- Wrong image name
- Private registry auth

# InvalidImageName
- Malformed image reference

# RegistryUnavailable
- Registry down or blocked

# RunContainerError
- Command not found
- Permission issues

# PostStartHookError
- Lifecycle hook failed

# PreStopHookError
- Shutdown hook failed
```

---

## Health Check Debugging

```bash
# Test liveness endpoint
kubectl exec -it my-pod -- curl localhost:8080/healthz

# Test readiness endpoint
kubectl exec -it my-pod -- curl localhost:8080/ready

# Check probe configuration
kubectl get pod my-pod -o yaml | grep -A 20 Probe

# View probe events
kubectl describe pod my-pod | grep -i probe
kubectl get events --field-selector involvedObject.name=my-pod
```

---

## Resource Quota Issues

```bash
# Check quotas
kubectl get resourcequota
kubectl describe resourcequota my-quota

# Check current usage
kubectl get resourcequota my-quota -o yaml

# Check limit ranges
kubectl get limitrange
kubectl describe limitrange

# Common issues:
# - Exceeded CPU/memory quota
# - Exceeded object count
# - PVC quota exceeded
```

---

## Debugging Tools

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f9f9f9" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Debugging Tools</text>
  <rect x="100" y="80" width="150" height="80" fill="#4285f4" rx="5"/>
  <text x="175" y="110" text-anchor="middle" fill="white" font-weight="bold">kubectl</text>
  <text x="175" y="130" text-anchor="middle" fill="white" font-size="10">Primary tool</text>
  <text x="175" y="150" text-anchor="middle" fill="white" font-size="10">Built-in debug</text>
  <rect x="270" y="80" width="150" height="80" fill="#34a853" rx="5"/>
  <text x="345" y="110" text-anchor="middle" fill="white" font-weight="bold">k9s</text>
  <text x="345" y="130" text-anchor="middle" fill="white" font-size="10">Terminal UI</text>
  <text x="345" y="150" text-anchor="middle" fill="white" font-size="10">Interactive</text>
  <rect x="440" y="80" width="150" height="80" fill="#fbbc04" rx="5"/>
  <text x="515" y="110" text-anchor="middle" font-weight="bold">stern</text>
  <text x="515" y="130" text-anchor="middle" font-size="10">Multi-pod logs</text>
  <text x="515" y="150" text-anchor="middle" font-size="10">Real-time tail</text>
  <rect x="610" y="80" width="140" height="80" fill="#ea4335" rx="5"/>
  <text x="680" y="110" text-anchor="middle" fill="white" font-weight="bold">kubectx</text>
  <text x="680" y="130" text-anchor="middle" fill="white" font-size="10">Context switch</text>
  <text x="680" y="150" text-anchor="middle" fill="white" font-size="10">Namespace mgmt</text>
  <rect x="180" y="180" width="150" height="80" fill="#9c27b0" rx="5"/>
  <text x="255" y="210" text-anchor="middle" fill="white" font-weight="bold">kube-capacity</text>
  <text x="255" y="230" text-anchor="middle" fill="white" font-size="10">Resource view</text>
  <text x="255" y="250" text-anchor="middle" fill="white" font-size="10">Utilization</text>
  <rect x="350" y="180" width="150" height="80" fill="#607d8b" rx="5"/>
  <text x="425" y="210" text-anchor="middle" fill="white" font-weight="bold">kubectl-tree</text>
  <text x="425" y="230" text-anchor="middle" fill="white" font-size="10">Resource tree</text>
  <text x="425" y="250" text-anchor="middle" fill="white" font-size="10">Dependencies</text>
  <rect x="520" y="180" width="150" height="80" fill="#ff5722" rx="5"/>
  <text x="595" y="210" text-anchor="middle" fill="white" font-weight="bold">ksniff</text>
  <text x="595" y="230" text-anchor="middle" fill="white" font-size="10">Packet capture</text>
  <text x="595" y="250" text-anchor="middle" fill="white" font-size="10">tcpdump</text>
</svg>

---

## Emergency Recovery

```bash
# Backup critical resources
kubectl get all --all-namespaces -o yaml > backup.yaml

# Delete stuck namespace
kubectl get namespace stuck-ns -o json | \
  jq '.spec.finalizers = []' | \
  kubectl replace --raw /api/v1/namespaces/stuck-ns/finalize -f -

# Force delete pod
kubectl delete pod my-pod --grace-period=0 --force

# Reset failed deployment
kubectl rollout undo deployment/my-app
kubectl rollout restart deployment/my-app
```

---

## Best Practices

1. **Always check** logs and events first
1. **Use** kubectl describe for details
1. **Test** in isolation with debug pods
1. **Monitor** resource usage
1. **Document** solutions for future

---

## Troubleshooting Checklist

1. ✓ Check pod status and events
1. ✓ Review logs (current and previous)
1. ✓ Verify image and pull secrets
1. ✓ Check resource limits and quotas
1. ✓ Test network connectivity
1. ✓ Verify configurations and secrets
1. ✓ Check RBAC permissions
1. ✓ Review health checks

---

## Summary

1. Systematic approach to troubleshooting
1. Multiple tools and techniques available
1. Common patterns and solutions
1. Understanding error messages is key
1. Practice makes perfect
