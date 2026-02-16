# Orchestration and Compute Choices
---
## Table of Contents

1. Compute Models Overview
1. `Kubernetes` vs Managed Containers vs `Serverless`
1. Operational Complexity and Team Capability
1. Cost Models and Scaling Characteristics
1. Portability vs Managed Convenience
1. `Kubernetes` Architecture Decisions
1. Cluster Strategies and Multi-Tenancy
1. Managed vs Self-Managed `Kubernetes`
1. `Serverless` Architecture Tradeoffs
1. Decision Framework
---
## The Compute Spectrum

<svg viewBox="0 0 700 180" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#1565c0;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#7b1fa2;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect x="10" y="90" width="680" height="12" rx="6" fill="url(#grad1)" opacity="0.3"/>
  <rect x="30" y="50" width="130" height="60" rx="8" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="95" y="75" text-anchor="middle" font-size="11" font-weight="bold" fill="#1565c0">VMs / Bare Metal</text>
  <text x="95" y="95" text-anchor="middle" font-size="9" fill="#333">Full control</text>
  <rect x="190" y="50" width="130" height="60" rx="8" fill="#e8eaf6" stroke="#283593" stroke-width="2"/>
  <text x="255" y="75" text-anchor="middle" font-size="11" font-weight="bold" fill="#283593">Self-Managed K8s</text>
  <text x="255" y="95" text-anchor="middle" font-size="9" fill="#333">Orchestrated containers</text>
  <rect x="350" y="50" width="130" height="60" rx="8" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="415" y="75" text-anchor="middle" font-size="11" font-weight="bold" fill="#6a1b9a">Managed K8s</text>
  <text x="415" y="95" text-anchor="middle" font-size="9" fill="#333">EKS, AKS, GKE</text>
  <rect x="510" y="50" width="130" height="60" rx="8" fill="#fce4ec" stroke="#b71c1c" stroke-width="2"/>
  <text x="575" y="75" text-anchor="middle" font-size="11" font-weight="bold" fill="#b71c1c">Serverless</text>
  <text x="575" y="95" text-anchor="middle" font-size="9" fill="#333">Lambda, Cloud Run</text>
  <text x="95" y="145" text-anchor="middle" font-size="10" fill="#555">More Control</text>
  <text x="575" y="145" text-anchor="middle" font-size="10" fill="#555">Less Control</text>
</svg>

- Moving right trades **control** for **convenience**
- Each step reduces operational burden but increases abstraction
---
## Kubernetes Overview

- Open-source container orchestration platform
- Originally designed by Google, now maintained by `CNCF`
- Provides:
    - Automated container deployment and scaling
    - Service discovery and load balancing
    - Storage orchestration
    - Self-healing and rolling updates
- De facto standard for container orchestration
---
## Managed Containers and Serverless Overview

**Managed container services**:
- `AWS ECS` / `Fargate`, `Azure Container Instances`, `Google Cloud Run`
- No cluster management needed
- Provider-specific APIs and configurations

**Serverless**:
- `AWS Lambda`, `Azure Functions`, `Google Cloud Functions`
- Provider manages all infrastructure
- Pay only for actual execution time
- Automatic scaling from zero to thousands of instances
---
## Kubernetes Architecture

<svg viewBox="0 0 700 300" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="10" width="680" height="80" rx="8" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="350" y="35" text-anchor="middle" font-size="13" font-weight="bold" fill="#1565c0">Control Plane</text>
  <rect x="30" y="45" width="90" height="35" rx="5" fill="#bbdefb" stroke="#1565c0" stroke-width="1"/>
  <text x="75" y="67" text-anchor="middle" font-size="9" fill="#333">API Server</text>
  <rect x="140" y="45" width="90" height="35" rx="5" fill="#bbdefb" stroke="#1565c0" stroke-width="1"/>
  <text x="185" y="67" text-anchor="middle" font-size="9" fill="#333">etcd</text>
  <rect x="250" y="45" width="90" height="35" rx="5" fill="#bbdefb" stroke="#1565c0" stroke-width="1"/>
  <text x="295" y="67" text-anchor="middle" font-size="9" fill="#333">Scheduler</text>
  <rect x="360" y="45" width="120" height="35" rx="5" fill="#bbdefb" stroke="#1565c0" stroke-width="1"/>
  <text x="420" y="67" text-anchor="middle" font-size="9" fill="#333">Controller Mgr</text>
  <rect x="500" y="45" width="120" height="35" rx="5" fill="#bbdefb" stroke="#1565c0" stroke-width="1"/>
  <text x="560" y="67" text-anchor="middle" font-size="9" fill="#333">Cloud Controller</text>
  <line x1="350" y1="90" x2="170" y2="120" stroke="#666" stroke-width="1.5" stroke-dasharray="4"/>
  <line x1="350" y1="90" x2="530" y2="120" stroke="#666" stroke-width="1.5" stroke-dasharray="4"/>
  <rect x="30" y="120" width="200" height="160" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="130" y="140" text-anchor="middle" font-size="11" font-weight="bold" fill="#2e7d32">Worker Node 1</text>
  <rect x="50" y="150" width="70" height="30" rx="4" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1"/>
  <text x="85" y="170" text-anchor="middle" font-size="8" fill="#333">kubelet</text>
  <rect x="140" y="150" width="70" height="30" rx="4" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1"/>
  <text x="175" y="170" text-anchor="middle" font-size="8" fill="#333">kube-proxy</text>
  <rect x="50" y="190" width="70" height="45" rx="4" fill="#fff9c4" stroke="#f9a825" stroke-width="1"/>
  <text x="85" y="215" text-anchor="middle" font-size="8" fill="#333">Pod A</text>
  <rect x="140" y="190" width="70" height="45" rx="4" fill="#fff9c4" stroke="#f9a825" stroke-width="1"/>
  <text x="175" y="215" text-anchor="middle" font-size="8" fill="#333">Pod B</text>
  <rect x="460" y="120" width="200" height="160" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="560" y="140" text-anchor="middle" font-size="11" font-weight="bold" fill="#2e7d32">Worker Node 2</text>
  <rect x="480" y="150" width="70" height="30" rx="4" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1"/>
  <text x="515" y="170" text-anchor="middle" font-size="8" fill="#333">kubelet</text>
  <rect x="570" y="150" width="70" height="30" rx="4" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1"/>
  <text x="605" y="170" text-anchor="middle" font-size="8" fill="#333">kube-proxy</text>
  <rect x="480" y="190" width="70" height="45" rx="4" fill="#fff9c4" stroke="#f9a825" stroke-width="1"/>
  <text x="515" y="215" text-anchor="middle" font-size="8" fill="#333">Pod C</text>
  <rect x="570" y="190" width="70" height="45" rx="4" fill="#fff9c4" stroke="#f9a825" stroke-width="1"/>
  <text x="605" y="215" text-anchor="middle" font-size="8" fill="#333">Pod D</text>
</svg>

---
## Operational Complexity Comparison

| Aspect | `Kubernetes` | Managed Containers | `Serverless` |
|--------|-------------|-------------------|-------------|
| Cluster mgmt | You manage | Partial | None |
| Networking | Complex | Simplified | Abstracted |
| Scaling config | Manual rules | Auto-scale groups | Automatic |
| Monitoring | Self-setup | Integrated | Built-in |
| Security patches | Your duty | Shared | Provider |
| Learning curve | Steep | Moderate | Low |

---
## Team Capability Requirements

- **`Kubernetes`** requires:
    - Dedicated platform team (2-5 engineers minimum)
    - Deep networking and Linux knowledge
    - Experience with `YAML`, `Helm`, `kubectl`
    - On-call rotation for cluster operations
- **Managed containers** require:
    - Cloud platform familiarity
    - Container building skills
- **`Serverless`** requires:
    - Cloud SDK knowledge
    - Event-driven programming experience
    - Understanding of provider limits
---
## When K8s Complexity Is Justified

Justified:
- Running 50+ microservices
- Need fine-grained control over networking (`Istio`, `Cilium`)
- Complex deployment strategies (canary, blue-green)
- Multi-cloud or hybrid-cloud requirements
- Strict compliance needs requiring infrastructure control

NOT justified:
- Small team (fewer than 5 developers)
- Fewer than 10 services
- No dedicated ops/platform team
---
## Cost Models: Kubernetes

- **Fixed costs**:
    - Control plane fee (managed) or server costs (self-managed)
    - Base node pool always running
    - Networking and load balancer charges
- **Variable costs**:
    - Additional nodes for scaling
    - Storage volumes and data transfer
- **Hidden costs**:
    - Platform team salaries
    - Training, certification, and tooling licenses
---
## Cost Models: Managed Containers and Serverless

**Managed containers** (`AWS Fargate` example):
- Per-container-hour pricing
- $0.04048 per `vCPU` per hour
- $0.004445 per `GB` memory per hour
- No charge when containers are stopped

**Serverless** (`AWS Lambda` example):
- $0.20 per 1M requests
- $0.0000166667 per `GB`-second
- 1M free requests per month
- Best for sporadic workloads; worst for constant high-throughput
---
## Cost Comparison at Scale

<svg viewBox="0 0 650 280" xmlns="http://www.w3.org/2000/svg">
  <line x1="80" y1="20" x2="80" y2="240" stroke="#333" stroke-width="2"/>
  <line x1="80" y1="240" x2="620" y2="240" stroke="#333" stroke-width="2"/>
  <text x="40" y="135" text-anchor="middle" font-size="12" fill="#333" transform="rotate(-90,40,135)">Monthly Cost ($)</text>
  <text x="350" y="270" text-anchor="middle" font-size="12" fill="#333">Request Volume / Traffic</text>
  <text x="150" y="255" font-size="9" fill="#666">Low</text>
  <text x="350" y="255" font-size="9" fill="#666">Medium</text>
  <text x="550" y="255" font-size="9" fill="#666">High</text>
  <polyline points="80,210 200,200 350,165 500,130 600,95" fill="none" stroke="#1565c0" stroke-width="3"/>
  <polyline points="80,185 200,175 350,145 500,120 600,105" fill="none" stroke="#6a1b9a" stroke-width="3"/>
  <polyline points="80,230 200,210 350,155 500,80 600,30" fill="none" stroke="#e65100" stroke-width="3"/>
  <rect x="420" y="20" width="12" height="12" fill="#1565c0"/>
  <text x="440" y="31" font-size="10" fill="#333">Kubernetes</text>
  <rect x="420" y="40" width="12" height="12" fill="#6a1b9a"/>
  <text x="440" y="51" font-size="10" fill="#333">Managed Containers</text>
  <rect x="420" y="60" width="12" height="12" fill="#e65100"/>
  <text x="440" y="71" font-size="10" fill="#333">Serverless</text>
  <text x="300" y="110" font-size="9" fill="#e65100" font-style="italic">Serverless cost rises steeply</text>
  <text x="180" y="195" font-size="9" fill="#1565c0" font-style="italic">K8s base cost is fixed</text>
</svg>

---
## Scaling Characteristics

- **`Kubernetes`**:
    - Horizontal Pod Autoscaler (`HPA`) scales pods
    - Cluster Autoscaler adds/removes nodes (minutes)
    - Predictable but requires capacity planning
- **Managed containers**:
    - Task-level scaling (seconds)
    - No node management needed
    - Upper limits per account/region
- **`Serverless`**:
    - Near-instant scaling (milliseconds to seconds)
    - Scales to zero automatically
    - Concurrency limits per function (default 1000)
---
## Portability vs Convenience Matrix

| Factor | Self-Managed K8s | Managed K8s | Managed Containers | Serverless |
|--------|-----------------|------------|-------------------|------------|
| Portability | High | Medium | Low | Very Low |
| Ops Burden | Very High | Medium | Low | Very Low |
| Flexibility | Very High | High | Medium | Low |
| Time to Market | Slow | Medium | Fast | Very Fast |

- `Kubernetes` `YAML` manifests work on any conformant cluster
- Container images are portable; orchestration config is not
- `Serverless` has the deepest vendor lock-in
---
## Cluster Strategy: Cluster Per Team

<svg viewBox="0 0 650 200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="20" width="180" height="160" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="110" y="45" text-anchor="middle" font-size="12" font-weight="bold" fill="#1565c0">Team A Cluster</text>
  <rect x="40" y="60" width="60" height="35" rx="4" fill="#bbdefb" stroke="#1565c0" stroke-width="1"/>
  <text x="70" y="82" text-anchor="middle" font-size="8" fill="#333">Service 1</text>
  <rect x="120" y="60" width="60" height="35" rx="4" fill="#bbdefb" stroke="#1565c0" stroke-width="1"/>
  <text x="150" y="82" text-anchor="middle" font-size="8" fill="#333">Service 2</text>
  <rect x="40" y="110" width="140" height="25" rx="4" fill="#e8eaf6" stroke="#283593" stroke-width="1"/>
  <text x="110" y="127" text-anchor="middle" font-size="8" fill="#333">Dedicated Control Plane</text>
  <rect x="235" y="20" width="180" height="160" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="325" y="45" text-anchor="middle" font-size="12" font-weight="bold" fill="#2e7d32">Team B Cluster</text>
  <rect x="255" y="60" width="60" height="35" rx="4" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1"/>
  <text x="285" y="82" text-anchor="middle" font-size="8" fill="#333">Service 3</text>
  <rect x="335" y="60" width="60" height="35" rx="4" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1"/>
  <text x="365" y="82" text-anchor="middle" font-size="8" fill="#333">Service 4</text>
  <rect x="255" y="110" width="140" height="25" rx="4" fill="#e8eaf6" stroke="#283593" stroke-width="1"/>
  <text x="325" y="127" text-anchor="middle" font-size="8" fill="#333">Dedicated Control Plane</text>
  <rect x="450" y="20" width="180" height="160" rx="10" fill="#fff3e0" stroke="#e65100" stroke-width="2"/>
  <text x="540" y="45" text-anchor="middle" font-size="12" font-weight="bold" fill="#e65100">Team C Cluster</text>
  <rect x="470" y="60" width="60" height="35" rx="4" fill="#ffe0b2" stroke="#e65100" stroke-width="1"/>
  <text x="500" y="82" text-anchor="middle" font-size="8" fill="#333">Service 5</text>
  <rect x="550" y="60" width="60" height="35" rx="4" fill="#ffe0b2" stroke="#e65100" stroke-width="1"/>
  <text x="580" y="82" text-anchor="middle" font-size="8" fill="#333">Service 6</text>
  <rect x="470" y="110" width="140" height="25" rx="4" fill="#e8eaf6" stroke="#283593" stroke-width="1"/>
  <text x="540" y="127" text-anchor="middle" font-size="8" fill="#333">Dedicated Control Plane</text>
</svg>

- Full blast radius isolation between teams
- Higher cost: each cluster has its own control plane
- Simpler `RBAC`; independent upgrade schedules
---
## Cluster Per Team: Pros and Cons

**Pros**:
- Complete isolation (security, performance, failures)
- Teams have full admin access to their cluster
- No noisy-neighbor problems

**Cons**:
- Higher infrastructure cost (control plane per team)
- Duplicated tooling and monitoring setup
- Cross-cluster service communication is harder
- More clusters to patch and maintain
- Harder to enforce organization-wide policies
---
## Cluster Strategy: Shared Clusters

<svg viewBox="0 0 650 250" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="10" width="610" height="230" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="325" y="35" text-anchor="middle" font-size="14" font-weight="bold" fill="#1565c0">Shared Cluster</text>
  <rect x="40" y="50" width="170" height="80" rx="8" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2"/>
  <text x="125" y="70" text-anchor="middle" font-size="11" font-weight="bold" fill="#2e7d32">ns: team-a</text>
  <rect x="55" y="80" width="55" height="25" rx="3" fill="#fff9c4" stroke="#f9a825" stroke-width="1"/>
  <text x="82" y="97" text-anchor="middle" font-size="7" fill="#333">Svc 1</text>
  <rect x="120" y="80" width="55" height="25" rx="3" fill="#fff9c4" stroke="#f9a825" stroke-width="1"/>
  <text x="147" y="97" text-anchor="middle" font-size="7" fill="#333">Svc 2</text>
  <rect x="240" y="50" width="170" height="80" rx="8" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="325" y="70" text-anchor="middle" font-size="11" font-weight="bold" fill="#6a1b9a">ns: team-b</text>
  <rect x="255" y="80" width="55" height="25" rx="3" fill="#fff9c4" stroke="#f9a825" stroke-width="1"/>
  <text x="282" y="97" text-anchor="middle" font-size="7" fill="#333">Svc 3</text>
  <rect x="320" y="80" width="55" height="25" rx="3" fill="#fff9c4" stroke="#f9a825" stroke-width="1"/>
  <text x="347" y="97" text-anchor="middle" font-size="7" fill="#333">Svc 4</text>
  <rect x="440" y="50" width="170" height="80" rx="8" fill="#fff3e0" stroke="#e65100" stroke-width="2"/>
  <text x="525" y="70" text-anchor="middle" font-size="11" font-weight="bold" fill="#e65100">ns: team-c</text>
  <rect x="455" y="80" width="55" height="25" rx="3" fill="#fff9c4" stroke="#f9a825" stroke-width="1"/>
  <text x="482" y="97" text-anchor="middle" font-size="7" fill="#333">Svc 5</text>
  <rect x="520" y="80" width="55" height="25" rx="3" fill="#fff9c4" stroke="#f9a825" stroke-width="1"/>
  <text x="547" y="97" text-anchor="middle" font-size="7" fill="#333">Svc 6</text>
  <rect x="40" y="145" width="570" height="35" rx="6" fill="#e8eaf6" stroke="#283593" stroke-width="1.5"/>
  <text x="325" y="168" text-anchor="middle" font-size="11" fill="#283593">Shared Control Plane + Shared Node Pool</text>
  <rect x="40" y="190" width="570" height="35" rx="6" fill="#fce4ec" stroke="#b71c1c" stroke-width="1.5"/>
  <text x="325" y="213" text-anchor="middle" font-size="11" fill="#b71c1c">NetworkPolicy + RBAC + OPA/Gatekeeper Enforcement</text>
</svg>

---
## Shared Clusters: Pros and Cons

**Pros**:
- Lower cost: single control plane, shared nodes
- Easier cross-service communication
- Centralized monitoring and logging
- Single upgrade path

**Cons**:
- Noisy-neighbor risk (CPU, memory, I/O)
- Complex `RBAC` configuration
- Blast radius: cluster failure affects all teams
- Namespace management overhead
---
## Namespace Strategies

**By team**:
- `team-frontend`, `team-backend`, `team-data`
- Maps to organizational structure

**By environment**:
- `dev`, `staging`, `production`
- Simple but limited isolation

**By application**:
- `order-service`, `payment-service`, `user-service`
- Fine-grained but many namespaces

**Hybrid** (recommended):
- `team-backend-prod`, `team-backend-dev`
- Combines team ownership with environment separation
---
## Namespace Isolation: ResourceQuota

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-a-quota
  namespace: team-a
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    pods: "50"
    services: "10"
```

- `ResourceQuota` limits total resource consumption
- `LimitRange` sets per-pod defaults and maximums
- `NetworkPolicy` controls pod-to-pod traffic
---
## Network Policies for Multi-Tenancy

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-cross-namespace
  namespace: team-a
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector: {}
  egress:
    - to:
        - podSelector: {}
```

- Default deny all cross-namespace traffic
- Explicitly allow only required communication paths
---
## Multi-Tenancy Models

| Model | Isolation | Cost | Complexity |
|-------|-----------|------|------------|
| Cluster per tenant | Strongest | Highest | Low per cluster |
| Namespace per tenant | Moderate | Medium | Medium |
| Virtual clusters | Strong | Medium | High |
| `Hierarchical` namespaces | Moderate | Low | Medium |

- Virtual clusters (`vCluster`) provide strong isolation within shared infra
- `Hierarchical` Namespace Controller (`HNC`) enables nested namespaces
- Choose based on compliance requirements and trust boundaries
---
## Managed Kubernetes Services Comparison

| Feature | `EKS` | `AKS` | `GKE` |
|---------|------|------|------|
| Provider | AWS | Azure | Google |
| Control plane cost | $0.10/hr | Free | Free (Standard) |
| Auto-upgrade | Optional | Optional | Default |
| Max nodes | 5,000 | 5,000 | 15,000 |
| `Autopilot` mode | No | No | Yes |
| `Fargate` support | Yes | No | No |

- All three manage the control plane for you
- Worker nodes remain your responsibility (unless using `Autopilot`/`Fargate`)
---
## Managed K8s: What You Still Own

Even with managed `Kubernetes`, you are responsible for:
- Worker node OS patches and upgrades
- `Container` runtime configuration
- Application-level security
- `Ingress` controller setup and management
- `Persistent` storage provisioning
- Cluster autoscaler configuration
- `Network` policies and `RBAC`
- Monitoring, logging, and alerting
- Backup and disaster recovery
- Cost optimization (right-sizing nodes)
---
## Self-Managed Kubernetes

When to consider:
- Regulatory requirements (air-gapped environments)
- On-premises data center deployments
- Need for specific `Kubernetes` version/patch
- Custom control plane configurations
- Edge computing scenarios

Tools for self-management:
- `kubeadm` - official bootstrapping tool
- `kops` - production-grade cluster management
- `Rancher` - multi-cluster management platform
- `Kubespray` - `Ansible`-based deployment
---
## Self-Managed vs Managed: Decision Tree

<svg viewBox="0 0 650 260" xmlns="http://www.w3.org/2000/svg">
  <rect x="200" y="10" width="250" height="40" rx="8" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="325" y="35" text-anchor="middle" font-size="12" font-weight="bold" fill="#1565c0">Need Kubernetes?</text>
  <line x1="250" y1="50" x2="130" y2="80" stroke="#333" stroke-width="1.5"/>
  <line x1="400" y1="50" x2="520" y2="80" stroke="#333" stroke-width="1.5"/>
  <text x="170" y="65" font-size="9" fill="#2e7d32">Yes</text>
  <text x="475" y="65" font-size="9" fill="#b71c1c">No</text>
  <rect x="30" y="80" width="200" height="40" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="130" y="105" text-anchor="middle" font-size="11" fill="#2e7d32">On-prem or air-gapped?</text>
  <rect x="420" y="80" width="200" height="40" rx="8" fill="#fff3e0" stroke="#e65100" stroke-width="2"/>
  <text x="520" y="105" text-anchor="middle" font-size="11" fill="#e65100">Use managed containers</text>
  <line x1="80" y1="120" x2="80" y2="150" stroke="#333" stroke-width="1.5"/>
  <line x1="180" y1="120" x2="180" y2="150" stroke="#333" stroke-width="1.5"/>
  <text x="60" y="140" font-size="9" fill="#2e7d32">Yes</text>
  <text x="195" y="140" font-size="9" fill="#b71c1c">No</text>
  <rect x="10" y="150" width="140" height="40" rx="8" fill="#fce4ec" stroke="#b71c1c" stroke-width="2"/>
  <text x="80" y="175" text-anchor="middle" font-size="11" fill="#b71c1c">Self-managed K8s</text>
  <rect x="180" y="150" width="140" height="40" rx="8" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="250" y="175" text-anchor="middle" font-size="11" fill="#6a1b9a">Managed K8s</text>
  <rect x="10" y="200" width="140" height="45" rx="6" fill="#ffebee" stroke="#c62828" stroke-width="1"/>
  <text x="80" y="218" text-anchor="middle" font-size="8" fill="#333">kubeadm, kops, Rancher</text>
  <text x="80" y="235" text-anchor="middle" font-size="8" fill="#c62828">High ops burden</text>
  <rect x="180" y="200" width="140" height="45" rx="6" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="1"/>
  <text x="250" y="218" text-anchor="middle" font-size="8" fill="#333">EKS, AKS, GKE</text>
  <text x="250" y="235" text-anchor="middle" font-size="8" fill="#6a1b9a">Medium ops burden</text>
</svg>

---
## Serverless Architecture Flow

<svg viewBox="0 0 650 220" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="30" width="100" height="50" rx="8" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="70" y="55" text-anchor="middle" font-size="10" font-weight="bold" fill="#1565c0">Event</text>
  <text x="70" y="70" text-anchor="middle" font-size="8" fill="#555">HTTP / Queue</text>
  <line x1="120" y1="55" x2="170" y2="55" stroke="#333" stroke-width="1.5" marker-end="url(#arrowhead)"/>
  <rect x="170" y="30" width="110" height="50" rx="8" fill="#fff3e0" stroke="#e65100" stroke-width="2"/>
  <text x="225" y="55" text-anchor="middle" font-size="10" font-weight="bold" fill="#e65100">API Gateway</text>
  <text x="225" y="70" text-anchor="middle" font-size="8" fill="#555">Route + Auth</text>
  <line x1="280" y1="55" x2="330" y2="55" stroke="#333" stroke-width="1.5" marker-end="url(#arrowhead)"/>
  <rect x="330" y="20" width="120" height="70" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="390" y="45" text-anchor="middle" font-size="10" font-weight="bold" fill="#2e7d32">Function</text>
  <text x="390" y="60" text-anchor="middle" font-size="8" fill="#555">Your Code</text>
  <text x="390" y="75" text-anchor="middle" font-size="8" fill="#555">Runs on demand</text>
  <line x1="450" y1="55" x2="500" y2="55" stroke="#333" stroke-width="1.5" marker-end="url(#arrowhead)"/>
  <rect x="500" y="30" width="120" height="50" rx="8" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="560" y="55" text-anchor="middle" font-size="10" font-weight="bold" fill="#6a1b9a">Backend</text>
  <text x="560" y="70" text-anchor="middle" font-size="8" fill="#555">DB / Storage / API</text>
  <rect x="120" y="120" width="420" height="60" rx="8" fill="#fafafa" stroke="#bdbdbd" stroke-width="1.5" stroke-dasharray="6"/>
  <text x="330" y="145" text-anchor="middle" font-size="11" font-weight="bold" fill="#666">Provider Manages Everything Below</text>
  <text x="200" y="165" font-size="9" fill="#888">OS</text>
  <text x="270" y="165" font-size="9" fill="#888">Runtime</text>
  <text x="340" y="165" font-size="9" fill="#888">Scaling</text>
  <text x="410" y="165" font-size="9" fill="#888">Networking</text>
  <text x="480" y="165" font-size="9" fill="#888">Security</text>
</svg>

---
## Cold Start: What Happens

<svg viewBox="0 0 650 180" xmlns="http://www.w3.org/2000/svg">
  <text x="20" y="25" font-size="11" font-weight="bold" fill="#333">Cold Start Timeline</text>
  <rect x="20" y="40" width="600" height="30" rx="4" fill="#f5f5f5" stroke="#bdbdbd" stroke-width="1"/>
  <rect x="20" y="40" width="100" height="30" rx="4" fill="#ffcdd2" stroke="#c62828" stroke-width="1"/>
  <text x="70" y="60" text-anchor="middle" font-size="8" fill="#333">Download Code</text>
  <rect x="120" y="40" width="80" height="30" rx="0" fill="#fff9c4" stroke="#f9a825" stroke-width="1"/>
  <text x="160" y="60" text-anchor="middle" font-size="8" fill="#333">Init Runtime</text>
  <rect x="200" y="40" width="100" height="30" rx="0" fill="#ffe0b2" stroke="#e65100" stroke-width="1"/>
  <text x="250" y="60" text-anchor="middle" font-size="8" fill="#333">Init Framework</text>
  <rect x="300" y="40" width="320" height="30" rx="4" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1"/>
  <text x="460" y="60" text-anchor="middle" font-size="8" fill="#333">Execute Function (Warm)</text>
  <text x="20" y="100" font-size="11" font-weight="bold" fill="#333">Warm Start Timeline</text>
  <rect x="20" y="110" width="600" height="30" rx="4" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1"/>
  <text x="320" y="130" text-anchor="middle" font-size="8" fill="#333">Execute Function (Instance Already Running)</text>
  <text x="170" y="165" font-size="9" fill="#c62828">Cold: 100ms - 10s+ depending on runtime</text>
</svg>

- Cold starts happen when no idle instance exists
- Frequency depends on traffic patterns and provider
---
## Cold Start Impact by Runtime

| Runtime | Typical Cold Start | Notes |
|---------|-------------------|-------|
| `Python` | 200-500ms | Fast init, large packages slow it |
| `Node.js` | 200-500ms | V8 startup is efficient |
| `Java` | 1-10s | JVM startup is heavy |
| `Go` | 50-200ms | Compiled binary, minimal overhead |
| `.NET` | 500ms-3s | CLR initialization |
| `Rust` | 50-150ms | Compiled, very fast |

Mitigation strategies:
- Provisioned concurrency (pre-warmed instances)
- Keep functions small and dependency-light
- Use compiled languages for latency-sensitive paths
---
## Cold Start Mitigation Techniques

1. **Provisioned concurrency**
    - Pre-warms N instances that stay ready
    - Eliminates cold starts but adds fixed cost
    - `AWS Lambda`: $0.015 per `GB`-hour provisioned
1. **Keep-alive pings**
    - Schedule periodic invocations to keep instances warm
    - Unreliable: provider may still reclaim instances
1. **Optimize package size**
    - Smaller deployment = faster download and init
    - Use tree-shaking and avoid unnecessary dependencies
1. **Use `SnapStart`** (Java on `AWS Lambda`)
    - Snapshots initialized JVM state
    - Reduces Java cold starts to ~200ms
---
## Vendor Lock-In Depth

<svg viewBox="0 0 650 240" xmlns="http://www.w3.org/2000/svg">
  <text x="325" y="25" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Lock-In Depth by Component</text>
  <rect x="50" y="45" width="550" height="35" rx="6" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2"/>
  <text x="325" y="67" text-anchor="middle" font-size="11" fill="#2e7d32">Function Code (Portable)</text>
  <text x="610" y="67" font-size="9" fill="#2e7d32">Low</text>
  <rect x="50" y="90" width="550" height="35" rx="6" fill="#fff9c4" stroke="#f9a825" stroke-width="2"/>
  <text x="325" y="112" text-anchor="middle" font-size="11" fill="#9e6e06">Runtime Configuration (Semi-Portable)</text>
  <text x="610" y="112" font-size="9" fill="#f9a825">Med</text>
  <rect x="50" y="135" width="550" height="35" rx="6" fill="#ffe0b2" stroke="#e65100" stroke-width="2"/>
  <text x="325" y="157" text-anchor="middle" font-size="11" fill="#e65100">Event Sources + Triggers (Provider-Specific)</text>
  <text x="610" y="157" font-size="9" fill="#e65100">High</text>
  <rect x="50" y="180" width="550" height="35" rx="6" fill="#ffcdd2" stroke="#c62828" stroke-width="2"/>
  <text x="325" y="202" text-anchor="middle" font-size="11" fill="#c62828">IAM + Permissions + Integrations (Deeply Locked)</text>
  <text x="610" y="202" font-size="9" fill="#c62828">Very High</text>
</svg>

---
## Serverless Lock-In: Practical Examples

**`AWS Lambda`** ties you to:
- `API Gateway` for HTTP routing
- `SQS`/`SNS`/`EventBridge` for event sources
- `IAM` roles and policies
- `CloudWatch` for logging
- `DynamoDB` Streams, `S3` events, `Kinesis`

**Migrating away requires rewriting**:
- All event source integrations
- Authentication and authorization
- Monitoring and alerting
- Deployment automation (`SAM`/`CDK`/`Serverless Framework`)

The business logic is portable; everything around it is not.

---
## Reducing Serverless Lock-In

- Use abstraction frameworks:
    - `Serverless Framework` - multi-cloud deployment
    - `Knative` - `Kubernetes`-based serverless
    - `OpenFaaS` - portable functions
- Keep business logic in pure libraries
    - Thin handler wraps provider-specific event format
    - Core logic has no provider SDK imports
- Use standard protocols:
    - `HTTP` instead of provider-specific triggers
    - `CloudEvents` for event format standardization
- Accept some lock-in as a trade-off for velocity
---
## Event-Driven vs Request-Driven

**Event-driven** (`serverless` natural fit):

- Message queue processing
- File upload processing
- Database change streams
- Scheduled tasks (`cron`)
- IoT sensor data ingestion

**Request-driven** (may prefer containers):
- Synchronous API endpoints
- WebSocket connections
- Long-running computations
- Stateful sessions
- Low-latency requirements (< 10ms)

Event-driven workloads align best with serverless economics.

---
## Event-Driven Serverless Flow

<svg viewBox="0 0 650 250" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="20" width="100" height="40" rx="8" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="70" y="45" text-anchor="middle" font-size="9" font-weight="bold" fill="#1565c0">S3 Upload</text>
  <rect x="20" y="75" width="100" height="40" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="70" y="100" text-anchor="middle" font-size="9" font-weight="bold" fill="#2e7d32">SQS Queue</text>
  <rect x="20" y="130" width="100" height="40" rx="8" fill="#fff3e0" stroke="#e65100" stroke-width="2"/>
  <text x="70" y="155" text-anchor="middle" font-size="9" font-weight="bold" fill="#e65100">Schedule</text>
  <rect x="20" y="185" width="100" height="40" rx="8" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="70" y="210" text-anchor="middle" font-size="9" font-weight="bold" fill="#6a1b9a">DB Stream</text>
  <line x1="120" y1="40" x2="220" y2="115" stroke="#1565c0" stroke-width="1.5"/>
  <line x1="120" y1="95" x2="220" y2="115" stroke="#2e7d32" stroke-width="1.5"/>
  <line x1="120" y1="150" x2="220" y2="125" stroke="#e65100" stroke-width="1.5"/>
  <line x1="120" y1="205" x2="220" y2="130" stroke="#6a1b9a" stroke-width="1.5"/>
  <rect x="220" y="95" width="130" height="55" rx="8" fill="#fff9c4" stroke="#f9a825" stroke-width="2"/>
  <text x="285" y="118" text-anchor="middle" font-size="11" font-weight="bold" fill="#9e6e06">Lambda</text>
  <text x="285" y="138" text-anchor="middle" font-size="9" fill="#555">Process Event</text>
  <line x1="350" y1="108" x2="430" y2="60" stroke="#333" stroke-width="1.5"/>
  <line x1="350" y1="122" x2="430" y2="122" stroke="#333" stroke-width="1.5"/>
  <line x1="350" y1="138" x2="430" y2="190" stroke="#333" stroke-width="1.5"/>
  <rect x="430" y="35" width="120" height="40" rx="8" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="490" y="60" text-anchor="middle" font-size="9" font-weight="bold" fill="#1565c0">DynamoDB</text>
  <rect x="430" y="100" width="120" height="40" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="490" y="125" text-anchor="middle" font-size="9" font-weight="bold" fill="#2e7d32">SNS Topic</text>
  <rect x="430" y="170" width="120" height="40" rx="8" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="490" y="195" text-anchor="middle" font-size="9" font-weight="bold" fill="#6a1b9a">S3 Bucket</text>
</svg>

---
## Serverless Limits to Know

| Limit | `AWS Lambda` | `Azure Functions` | `Cloud Functions` |
|-------|-------------|-------------------|-------------------|
| Max timeout | 15 min | 10 min (consumption) | 60 min (v2) |
| Max memory | 10 `GB` | 1.5 `GB` (consumption) | 32 `GB` |
| Package size | 250 `MB` unzipped | No hard limit | 500 `MB` unzipped |
| Concurrency | 1000 default | 200 default | 1000 default |
| Temp storage | 10 `GB` | 500 `MB` | In-memory only |

- These limits shape what workloads can run serverless
- Limits can often be increased by request
---
## Hybrid Architectures

Most real-world systems combine compute models:

- **`Kubernetes`** for:
    - Core API services with steady traffic
    - Stateful workloads (databases, caches)
    - ML model serving
- **Managed containers** for:
    - Batch processing jobs
    - Internal tools and dashboards
- **`Serverless`** for:
    - Event processing pipelines
    - Webhooks and integrations
    - Scheduled tasks and cron jobs
    - Image/video processing triggers
---
## Hybrid Architecture Example

<svg viewBox="0 0 650 240" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="10" width="300" height="110" rx="8" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="160" y="30" text-anchor="middle" font-size="12" font-weight="bold" fill="#1565c0">Kubernetes Cluster</text>
  <rect x="25" y="42" width="80" height="30" rx="4" fill="#bbdefb" stroke="#1565c0" stroke-width="1"/>
  <text x="65" y="61" text-anchor="middle" font-size="8" fill="#333">API Gateway</text>
  <rect x="120" y="42" width="80" height="30" rx="4" fill="#bbdefb" stroke="#1565c0" stroke-width="1"/>
  <text x="160" y="61" text-anchor="middle" font-size="8" fill="#333">Core API</text>
  <rect x="215" y="42" width="80" height="30" rx="4" fill="#bbdefb" stroke="#1565c0" stroke-width="1"/>
  <text x="255" y="61" text-anchor="middle" font-size="8" fill="#333">Auth Service</text>
  <rect x="25" y="82" width="80" height="30" rx="4" fill="#bbdefb" stroke="#1565c0" stroke-width="1"/>
  <text x="65" y="101" text-anchor="middle" font-size="8" fill="#333">Redis Cache</text>
  <rect x="120" y="82" width="80" height="30" rx="4" fill="#bbdefb" stroke="#1565c0" stroke-width="1"/>
  <text x="160" y="101" text-anchor="middle" font-size="8" fill="#333">PostgreSQL</text>
  <rect x="350" y="10" width="280" height="50" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="490" y="30" text-anchor="middle" font-size="11" font-weight="bold" fill="#2e7d32">Serverless Functions</text>
  <text x="400" y="48" font-size="8" fill="#333">Image Resize</text>
  <text x="490" y="48" font-size="8" fill="#333">Email Send</text>
  <text x="570" y="48" font-size="8" fill="#333">Webhooks</text>
  <rect x="350" y="70" width="280" height="50" rx="8" fill="#fff3e0" stroke="#e65100" stroke-width="2"/>
  <text x="490" y="90" text-anchor="middle" font-size="11" font-weight="bold" fill="#e65100">Managed Containers</text>
  <text x="400" y="108" font-size="8" fill="#333">Batch Jobs</text>
  <text x="490" y="108" font-size="8" fill="#333">Data Pipeline</text>
  <text x="580" y="108" font-size="8" fill="#333">Reports</text>
  <rect x="100" y="145" width="450" height="45" rx="8" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="325" y="173" text-anchor="middle" font-size="11" font-weight="bold" fill="#6a1b9a">Shared: Message Queue, Object Storage, CDN</text>
  <line x1="160" y1="120" x2="325" y2="145" stroke="#6a1b9a" stroke-width="1" stroke-dasharray="4"/>
  <line x1="490" y1="60" x2="325" y2="145" stroke="#6a1b9a" stroke-width="1" stroke-dasharray="4"/>
  <line x1="490" y1="120" x2="325" y2="145" stroke="#6a1b9a" stroke-width="1" stroke-dasharray="4"/>
</svg>

---
## RBAC and Policy Enforcement

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: team-backend
  name: team-backend-dev
rules:
  - apiGroups: ["", "apps"]
    resources: ["pods", "deployments",
                "services"]
    verbs: ["get", "list", "create",
            "update", "delete"]
  - apiGroups: [""]
    resources: ["secrets"]
    verbs: ["get", "list"]
```

- Bind roles to groups from your identity provider
- `OPA Gatekeeper` enforces policies at admission time
- Enforce required labels, approved registries, resource limits
---
## Cost Optimization Strategies

**`Kubernetes`**:
1. Right-size nodes to match workload profiles
1. Use spot/preemptible instances (60-90% savings)
1. Implement `VPA` to auto-adjust resource requests
1. Monitor with `Kubecost` or `kubectl top`

**`Serverless`**:
1. Optimize memory allocation (more memory = more CPU = faster)
1. Use `ARM` architecture (`Graviton2`: 20% cheaper)
1. Batch operations per invocation
1. Set appropriate timeouts to prevent runaway costs

```bash
# Check K8s resource usage vs requests
kubectl top pods -n production
```

---
## Observability Across Compute Models

| Aspect | `Kubernetes` | Managed Containers | `Serverless` |
|--------|-------------|-------------------|-------------|
| Metrics | `Prometheus`/`Grafana` | CloudWatch/Monitor | Built-in |
| Logging | `EFK`/`Loki` stack | Provider logs | Provider logs |
| Tracing | `Jaeger`/`Zipkin` | `X-Ray`/App Insights | `X-Ray`/built-in |
| Custom dashboards | Full control | Limited | Limited |
| Cost tracking | `Kubecost` | Provider tools | Provider tools |

- Unified observability across models is challenging
- Consider `OpenTelemetry` as a vendor-neutral standard
---
## Security Considerations by Model

**`Kubernetes`**:
- Container image scanning (`Trivy`, `Snyk`)
- Pod Security Standards (restricted, baseline, privileged)
- Network policies for micro-segmentation
- Secrets management (`Vault`, `Sealed Secrets`, `ESO`)

**Managed containers**:
- Image scanning by provider
- Task-level IAM roles
- VPC networking

**`Serverless`**:
- Function-level IAM (least privilege)
- No OS to patch
- Provider handles runtime security
- Focus shifts to application-level security
---
## CI/CD Patterns by Compute Model

**`Kubernetes`**:
```bash
# GitOps flow
git push -> CI builds image -> push to registry
-> ArgoCD detects change -> syncs to cluster
```

**Managed containers**:
```bash
# Pipeline flow
git push -> CI builds image -> push to registry
-> update task definition -> rolling deploy
```

**`Serverless`**:
```bash
# SAM/CDK flow
git push -> CI runs tests -> sam build
-> sam deploy -> traffic shifting (canary)
```

- `GitOps` is the gold standard for `Kubernetes`
---
## Decision Framework

Ask these questions in order:

1. **How many services** do you run?
    - < 5: Managed containers or serverless
    - 5-20: Managed `Kubernetes` or containers
    - 20+: `Kubernetes` (managed or self-managed)
1. **What is your traffic pattern?**
    - Spiky/unpredictable: Serverless
    - Steady: Containers / `Kubernetes`
1. **Do you need multi-cloud portability?**
    - Yes: `Kubernetes`
    - No: Managed containers or serverless
1. **What is your team size?**
    - < 5 engineers: Avoid self-managed `K8s`
    - 15+: Any model works
---
## Decision Matrix Summary

<svg viewBox="0 0 650 240" xmlns="http://www.w3.org/2000/svg">
  <text x="325" y="20" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Choosing Your Compute Model</text>
  <rect x="30" y="40" width="140" height="50" rx="8" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="100" y="60" text-anchor="middle" font-size="10" font-weight="bold" fill="#1565c0">Small Team</text>
  <text x="100" y="78" text-anchor="middle" font-size="9" fill="#555">< 5 engineers</text>
  <rect x="30" y="100" width="140" height="40" rx="6" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="100" y="125" text-anchor="middle" font-size="10" fill="#2e7d32">Serverless / Managed</text>
  <line x1="100" y1="90" x2="100" y2="100" stroke="#333" stroke-width="1.5"/>
  <rect x="255" y="40" width="140" height="50" rx="8" fill="#fff3e0" stroke="#e65100" stroke-width="2"/>
  <text x="325" y="60" text-anchor="middle" font-size="10" font-weight="bold" fill="#e65100">Medium Team</text>
  <text x="325" y="78" text-anchor="middle" font-size="9" fill="#555">5-15 engineers</text>
  <rect x="255" y="100" width="140" height="40" rx="6" fill="#fff9c4" stroke="#f9a825" stroke-width="1.5"/>
  <text x="325" y="125" text-anchor="middle" font-size="10" fill="#9e6e06">Managed K8s / Hybrid</text>
  <line x1="325" y1="90" x2="325" y2="100" stroke="#333" stroke-width="1.5"/>
  <rect x="480" y="40" width="140" height="50" rx="8" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="2"/>
  <text x="550" y="60" text-anchor="middle" font-size="10" font-weight="bold" fill="#6a1b9a">Large Team</text>
  <text x="550" y="78" text-anchor="middle" font-size="9" fill="#555">15+ engineers</text>
  <rect x="480" y="100" width="140" height="40" rx="6" fill="#e8eaf6" stroke="#283593" stroke-width="1.5"/>
  <text x="550" y="125" text-anchor="middle" font-size="10" fill="#283593">K8s + Platform Team</text>
  <line x1="550" y1="90" x2="550" y2="100" stroke="#333" stroke-width="1.5"/>
  <rect x="100" y="160" width="450" height="60" rx="10" fill="#fafafa" stroke="#bdbdbd" stroke-width="1.5"/>
  <text x="325" y="185" text-anchor="middle" font-size="11" font-weight="bold" fill="#333">Key Principle</text>
  <text x="325" y="207" text-anchor="middle" font-size="10" fill="#555">Choose the simplest model that meets your requirements.</text>
</svg>

---
## Anti-Patterns to Avoid

1. **"Kubernetes all the things"**
    - Not every workload needs `K8s` orchestration
    - A cron job does not need a `CronJob` resource
1. **Premature multi-cloud**
    - Portability has a real engineering cost
    - Build for one cloud first, abstract later
1. **Serverless monolith**
    - One giant `Lambda` function defeats the purpose
    - But too many tiny functions creates orchestration hell
1. **Ignoring cold starts in user-facing paths**
    - Test latency under realistic conditions
    - Provision concurrency for critical endpoints
1. **No cost alerts**
    - Serverless can generate surprise bills
---
## Emerging Trends

- **`WebAssembly` (`Wasm`) on the server**
    - Near-instant cold starts (< 1ms)
    - Language-agnostic, sandboxed execution
    - `Spin`, `Fermyon Cloud`, `Cosmonic`
- **`Kubernetes` simplification**
    - `GKE Autopilot`, `EKS Auto Mode`
    - Reducing operational burden while keeping `K8s` API
- **Edge compute**
    - `Cloudflare Workers`, `Deno Deploy`, `Lambda@Edge`
    - Functions at CDN edge locations worldwide
- **`FinOps` integration**
    - Cost visibility built into orchestration tooling
    - Real-time cost attribution per team/service
---
## Key Takeaways

- There is no universally correct compute model
- Match your choice to **team capability** and **workload characteristics**
- `Kubernetes` provides maximum flexibility at the cost of complexity
- Managed containers balance control and convenience
- `Serverless` offers minimum ops but maximum vendor lock-in
- Most production systems use a **hybrid approach**
- Start simple, add complexity only when justified
- Always account for **total cost of ownership**, not just infrastructure
- Invest in `IaC` and `GitOps` regardless of compute model
- Revisit decisions annually as the landscape evolves
