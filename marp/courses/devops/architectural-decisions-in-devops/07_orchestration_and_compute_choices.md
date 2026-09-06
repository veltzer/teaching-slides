---
tags:
  - practices:devops
  - concepts:architecture
  - practices:ci-cd
  - infrastructure:infrastructure-as-code
level: advanced
category: devops
audience:
  - audiences:architects
  - audiences:devops
  - audiences:managers

---

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

![the_compute_spectrum](svg/courses/devops/architectural-decisions-in-devops/07_orchestration_and_compute_choices/the_compute_spectrum.svg)

---

## The Compute Spectrum: Details

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

![kubernetes_architecture](svg/courses/devops/architectural-decisions-in-devops/07_orchestration_and_compute_choices/kubernetes_architecture.svg)

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

![cost_comparison_at_scale](svg/courses/devops/architectural-decisions-in-devops/07_orchestration_and_compute_choices/cost_comparison_at_scale.svg)

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

![cluster_strategy_cluster_per_team](svg/courses/devops/architectural-decisions-in-devops/07_orchestration_and_compute_choices/cluster_strategy_cluster_per_team.svg)

---

## Cluster Strategy: Cluster Per Team: Details

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

![cluster_strategy_shared_clusters](svg/courses/devops/architectural-decisions-in-devops/07_orchestration_and_compute_choices/cluster_strategy_shared_clusters.svg)

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

![self_managed_vs_managed_decision_tree](svg/courses/devops/architectural-decisions-in-devops/07_orchestration_and_compute_choices/self_managed_vs_managed_decision_tree.svg)

---

## Serverless Architecture Flow

![serverless_architecture_flow](svg/courses/devops/architectural-decisions-in-devops/07_orchestration_and_compute_choices/serverless_architecture_flow.svg)

---

## Cold Start: What Happens

![cold_start_what_happens](svg/courses/devops/architectural-decisions-in-devops/07_orchestration_and_compute_choices/cold_start_what_happens.svg)

---

## Cold Start: What Happens: Details

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

![vendor_lock_in_depth](svg/courses/devops/architectural-decisions-in-devops/07_orchestration_and_compute_choices/vendor_lock_in_depth.svg)

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

![event_driven_serverless_flow](svg/courses/devops/architectural-decisions-in-devops/07_orchestration_and_compute_choices/event_driven_serverless_flow.svg)

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

![hybrid_architecture_example](svg/courses/devops/architectural-decisions-in-devops/07_orchestration_and_compute_choices/hybrid_architecture_example.svg)

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

![decision_matrix_summary](svg/courses/devops/architectural-decisions-in-devops/07_orchestration_and_compute_choices/decision_matrix_summary.svg)

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
