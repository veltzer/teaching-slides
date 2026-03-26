# Deployment Strategies
---
## Why Deployment Strategy Matters

- Deployment is the riskiest phase of the software delivery lifecycle
- The wrong strategy can cause downtime, data loss, or degraded user experience
- Choosing a strategy depends on:
    - Application architecture (monolith vs. microservices)
    - Infrastructure budget
    - Risk tolerance and rollback requirements
    - Database migration complexity
---
## Overview of Common Strategies

1. **Blue/Green Deployments** - switch traffic between two identical environments
1. **Canary Deployments** - gradually shift traffic to the new version
1. **Rolling Deployments** - update instances incrementally in place
1. **Feature Flags** - decouple deployment from release using code-level toggles
1. **Progressive Delivery** - combine strategies with experimentation
---
## Strategy Comparison

| Strategy | Downtime | Rollback Speed | Infra Cost | Complexity |
|----------|----------|----------------|------------|------------|
| Blue/Green | None | Instant | High | Low |
| Canary | None | Fast | Medium | Medium |
| Rolling | None | Moderate | Low | Medium |
| Feature Flags | None | Instant | Low | High |
---
## Blue/Green Deployments - Concept

- Maintain two identical production environments: `Blue` and `Green`
- Only one environment serves live traffic at any time
- Deploy the new version to the idle environment
- Switch traffic from the active to the idle environment once verified
- The old environment becomes the instant rollback target
---
## Blue/Green Architecture Diagram

<svg width="700" height="350" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
  <!-- Users -->
  <rect x="30" y="140" width="90" height="40" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="75" y="165" text-anchor="middle" font-size="13" font-weight="bold">Users</text>
  <!-- Load Balancer -->
  <rect x="200" y="140" width="120" height="40" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="5"/>
  <text x="260" y="165" text-anchor="middle" font-size="13" font-weight="bold">Load Balancer</text>
  <!-- Blue Environment -->
  <rect x="430" y="50" width="220" height="70" fill="#bbdefb" stroke="#1565c0" stroke-width="2" rx="8"/>
  <text x="540" y="78" text-anchor="middle" font-size="14" font-weight="bold" fill="#1565c0">Blue (v1 - Active)</text>
  <text x="540" y="100" text-anchor="middle" font-size="11" fill="#333">Serving live traffic</text>
  <!-- Green Environment -->
  <rect x="430" y="200" width="220" height="70" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="8"/>
  <text x="540" y="228" text-anchor="middle" font-size="14" font-weight="bold" fill="#2e7d32">Green (v2 - Idle)</text>
  <text x="540" y="250" text-anchor="middle" font-size="11" fill="#333">Deploy &amp; verify here</text>
  <!-- Arrows -->
  <line x1="120" y1="160" x2="195" y2="160" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="320" y1="155" x2="425" y2="85" stroke="#1565c0" stroke-width="3" marker-end="url(#arrow)"/>
  <line x1="320" y1="165" x2="425" y2="235" stroke="#aaa" stroke-width="1.5" stroke-dasharray="6,4" marker-end="url(#arrow)"/>
  <!-- Switch label -->
  <text x="370" y="180" text-anchor="middle" font-size="11" fill="#666">Switch</text>
</svg>

---
## Blue/Green - The Switch

- The traffic switch is typically performed by updating:
    - `DNS` records (slower propagation)
    - Load balancer target group (instant)
    - Reverse proxy upstream configuration
- After switching, monitor the new environment closely
- If problems arise, switch traffic back to the old environment immediately
---
## Blue/Green - Infrastructure Cost Implications

- You pay for **double the compute resources** at all times
- Both environments must be production-grade (same instance types, scaling policies)
- Storage costs are shared if environments point to the same data layer
- Cost optimization techniques:
    - Scale down the idle environment to minimal capacity
    - Use spot or preemptible instances for the idle side
    - Tear down the idle environment and rebuild on next deploy
---
## Blue/Green - Database Compatibility

- The database is the hardest part of blue/green deployments
- Both versions may need to read/write the same database during the switch
- Schema changes must be **backward compatible** with the old version
- Common approach: **expand-and-contract migrations**
    - Step 1: Add new columns/tables without removing old ones
    - Step 2: Deploy new version that writes to both old and new schema
    - Step 3: Migrate data
    - Step 4: Remove old columns in a future release
---
## Blue/Green - Database Migration Pattern

<svg width="700" height="300" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr2" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
  <!-- Phase labels -->
  <text x="10" y="30" font-size="13" font-weight="bold" fill="#333">Expand-and-Contract Migration:</text>
  <!-- Phase 1 -->
  <rect x="20" y="50" width="150" height="50" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="95" y="72" text-anchor="middle" font-size="11" font-weight="bold">Phase 1: Expand</text>
  <text x="95" y="88" text-anchor="middle" font-size="10">Add new columns</text>
  <!-- Phase 2 -->
  <rect x="195" y="50" width="150" height="50" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="5"/>
  <text x="270" y="72" text-anchor="middle" font-size="11" font-weight="bold">Phase 2: Dual Write</text>
  <text x="270" y="88" text-anchor="middle" font-size="10">Both schemas active</text>
  <!-- Phase 3 -->
  <rect x="370" y="50" width="150" height="50" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="445" y="72" text-anchor="middle" font-size="11" font-weight="bold">Phase 3: Migrate</text>
  <text x="445" y="88" text-anchor="middle" font-size="10">Backfill data</text>
  <!-- Phase 4 -->
  <rect x="545" y="50" width="150" height="50" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2" rx="5"/>
  <text x="620" y="72" text-anchor="middle" font-size="11" font-weight="bold">Phase 4: Contract</text>
  <text x="620" y="88" text-anchor="middle" font-size="10">Drop old columns</text>
  <!-- Arrows -->
  <line x1="170" y1="75" x2="190" y2="75" stroke="#333" stroke-width="2" marker-end="url(#arr2)"/>
  <line x1="345" y1="75" x2="365" y2="75" stroke="#333" stroke-width="2" marker-end="url(#arr2)"/>
  <line x1="520" y1="75" x2="540" y2="75" stroke="#333" stroke-width="2" marker-end="url(#arr2)"/>
  <!-- DB -->
  <rect x="250" y="160" width="200" height="50" fill="#ffecb3" stroke="#f57c00" stroke-width="2" rx="5"/>
  <text x="350" y="185" text-anchor="middle" font-size="13" font-weight="bold">Shared Database</text>
  <text x="350" y="200" text-anchor="middle" font-size="10">Must remain compatible</text>
  <!-- Connecting lines -->
  <line x1="95" y1="100" x2="290" y2="160" stroke="#999" stroke-width="1" stroke-dasharray="4,3"/>
  <line x1="445" y1="100" x2="390" y2="160" stroke="#999" stroke-width="1" stroke-dasharray="4,3"/>
</svg>

---
## Blue/Green - When to Use

- Applications where instant rollback is critical
- Stateless applications or those with shared external data stores
- Teams with budget for double infrastructure
- Environments where you can afford full pre-production verification
- When database schema changes can be managed with expand-and-contract
---
## Canary Deployments - Concept

- Deploy the new version to a **small subset** of production infrastructure
- Route a small percentage of traffic to the canary instances
- Monitor key metrics (error rate, latency, business KPIs)
- Gradually increase traffic to the new version if metrics look healthy
- Roll back immediately if anomalies are detected
---
## Canary Traffic Split Diagram

<svg width="700" height="350" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr3" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
  <!-- Users -->
  <rect x="30" y="130" width="90" height="40" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="75" y="155" text-anchor="middle" font-size="13" font-weight="bold">Users</text>
  <!-- Router -->
  <rect x="190" y="120" width="130" height="60" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="5"/>
  <text x="255" y="148" text-anchor="middle" font-size="12" font-weight="bold">Traffic Router</text>
  <text x="255" y="166" text-anchor="middle" font-size="10">Weight-based</text>
  <!-- Stable -->
  <rect x="430" y="50" width="220" height="60" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="8"/>
  <text x="540" y="78" text-anchor="middle" font-size="13" font-weight="bold" fill="#2e7d32">Stable (v1)</text>
  <text x="540" y="96" text-anchor="middle" font-size="11">95% of traffic</text>
  <!-- Canary -->
  <rect x="430" y="200" width="220" height="60" fill="#ffcdd2" stroke="#c62828" stroke-width="2" rx="8"/>
  <text x="540" y="228" text-anchor="middle" font-size="13" font-weight="bold" fill="#c62828">Canary (v2)</text>
  <text x="540" y="246" text-anchor="middle" font-size="11">5% of traffic</text>
  <!-- Arrows -->
  <line x1="120" y1="150" x2="185" y2="150" stroke="#333" stroke-width="2" marker-end="url(#arr3)"/>
  <line x1="320" y1="140" x2="425" y2="80" stroke="#2e7d32" stroke-width="3" marker-end="url(#arr3)"/>
  <line x1="320" y1="160" x2="425" y2="230" stroke="#c62828" stroke-width="1.5" marker-end="url(#arr3)"/>
  <!-- Labels -->
  <text x="370" y="100" text-anchor="middle" font-size="11" fill="#2e7d32" font-weight="bold">95%</text>
  <text x="370" y="210" text-anchor="middle" font-size="11" fill="#c62828" font-weight="bold">5%</text>
  <!-- Monitoring -->
  <rect x="430" y="290" width="220" height="40" fill="#e1bee7" stroke="#7b1fa2" stroke-width="2" rx="5"/>
  <text x="540" y="315" text-anchor="middle" font-size="12" font-weight="bold" fill="#7b1fa2">Monitoring &amp; Alerting</text>
  <line x1="540" y1="260" x2="540" y2="285" stroke="#7b1fa2" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arr3)"/>
</svg>

---
## Canary - Traffic Splitting Mechanisms

- **Load balancer weighted routing** - assign weights to target groups (e.g., `AWS ALB`, `NGINX`)
- **Service mesh** - `Istio`, `Linkerd`, or `Consul Connect` route at Layer 7
- **DNS-based splitting** - weighted `CNAME` or `A` records
- **Application-level routing** - middleware inspects headers or cookies
- **Kubernetes** - use `Argo Rollouts` or `Flagger` for automated canary
---
## Canary - Traffic Splitting with `Istio`

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: my-service
spec:
  hosts:
    - my-service
  http:
    - route:
        - destination:
            host: my-service
            subset: stable
          weight: 95
        - destination:
            host: my-service
            subset: canary
          weight: 5
```

---
## Canary - Key Metrics to Monitor

- **Error rate** - HTTP 5xx responses, exception counts
- **Latency** - p50, p95, p99 response times
- **Throughput** - requests per second handled
- **Resource usage** - CPU, memory, disk I/O on canary instances
- **Business metrics** - conversion rates, checkout completions
- **Saturation** - queue depths, connection pool usage
---
## Canary - Rollback Criteria

- Define **automated rollback triggers** before deploying:
    - Error rate exceeds baseline by more than 1%
    - p99 latency exceeds 2x the stable version
    - Any critical health check failure
- Use **statistical significance** to avoid false positives
- Require a minimum observation window (e.g., 10 minutes)
- Rollback should be automatic, not dependent on human decision
---
## Canary - Progressive Traffic Ramp

1. Deploy canary with 1% traffic
1. Wait 5 minutes, check metrics
1. Increase to 5%
1. Wait 10 minutes, check metrics
1. Increase to 25%
1. Wait 15 minutes, check metrics
1. Increase to 50%
1. Wait 15 minutes, check metrics
1. Promote to 100%
- At any step, if metrics degrade, roll back to 0%
---
## Canary - Automated Rollout with `Flagger`

```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: my-app
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  progressDeadlineSeconds: 600
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
      - name: request-success-rate
        thresholdRange:
          min: 99
```

---
## Canary - When to Use

- High-traffic applications where issues affect many users quickly
- When you need data-driven confidence before full rollout
- Microservices architectures where individual services can be routed independently
- Teams with mature monitoring and observability infrastructure
- When rollback speed is important but you cannot afford full blue/green costs
---
## Rolling Deployments - Concept

- Update instances **one at a time** (or in small batches)
- Each batch is taken out of service, updated, health-checked, and returned
- The process continues until all instances run the new version
- No additional infrastructure is required beyond the existing fleet
---
## Rolling Update Sequence Diagram

<svg width="700" height="300" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr4" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
  <!-- Title -->
  <text x="350" y="25" text-anchor="middle" font-size="14" font-weight="bold">Rolling Update: 4 Instances</text>
  <!-- Step 1 -->
  <text x="15" y="65" font-size="11" font-weight="bold">Step 1:</text>
  <rect x="80" y="50" width="55" height="30" fill="#ffcdd2" stroke="#c62828" stroke-width="2" rx="4"/>
  <text x="107" y="70" text-anchor="middle" font-size="10" fill="#c62828">v2</text>
  <rect x="145" y="50" width="55" height="30" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="4"/>
  <text x="172" y="70" text-anchor="middle" font-size="10">v1</text>
  <rect x="210" y="50" width="55" height="30" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="4"/>
  <text x="237" y="70" text-anchor="middle" font-size="10">v1</text>
  <rect x="275" y="50" width="55" height="30" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="4"/>
  <text x="302" y="70" text-anchor="middle" font-size="10">v1</text>
  <!-- Step 2 -->
  <text x="15" y="115" font-size="11" font-weight="bold">Step 2:</text>
  <rect x="80" y="100" width="55" height="30" fill="#bbdefb" stroke="#1565c0" stroke-width="2" rx="4"/>
  <text x="107" y="120" text-anchor="middle" font-size="10" fill="#1565c0">v2</text>
  <rect x="145" y="100" width="55" height="30" fill="#ffcdd2" stroke="#c62828" stroke-width="2" rx="4"/>
  <text x="172" y="120" text-anchor="middle" font-size="10" fill="#c62828">v2</text>
  <rect x="210" y="100" width="55" height="30" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="4"/>
  <text x="237" y="120" text-anchor="middle" font-size="10">v1</text>
  <rect x="275" y="100" width="55" height="30" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="4"/>
  <text x="302" y="120" text-anchor="middle" font-size="10">v1</text>
  <!-- Step 3 -->
  <text x="15" y="165" font-size="11" font-weight="bold">Step 3:</text>
  <rect x="80" y="150" width="55" height="30" fill="#bbdefb" stroke="#1565c0" stroke-width="2" rx="4"/>
  <text x="107" y="170" text-anchor="middle" font-size="10" fill="#1565c0">v2</text>
  <rect x="145" y="150" width="55" height="30" fill="#bbdefb" stroke="#1565c0" stroke-width="2" rx="4"/>
  <text x="172" y="170" text-anchor="middle" font-size="10" fill="#1565c0">v2</text>
  <rect x="210" y="150" width="55" height="30" fill="#ffcdd2" stroke="#c62828" stroke-width="2" rx="4"/>
  <text x="237" y="170" text-anchor="middle" font-size="10" fill="#c62828">v2</text>
  <rect x="275" y="150" width="55" height="30" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="4"/>
  <text x="302" y="170" text-anchor="middle" font-size="10">v1</text>
  <!-- Step 4 -->
  <text x="15" y="215" font-size="11" font-weight="bold">Step 4:</text>
  <rect x="80" y="200" width="55" height="30" fill="#bbdefb" stroke="#1565c0" stroke-width="2" rx="4"/>
  <text x="107" y="220" text-anchor="middle" font-size="10" fill="#1565c0">v2</text>
  <rect x="145" y="200" width="55" height="30" fill="#bbdefb" stroke="#1565c0" stroke-width="2" rx="4"/>
  <text x="172" y="220" text-anchor="middle" font-size="10" fill="#1565c0">v2</text>
  <rect x="210" y="200" width="55" height="30" fill="#bbdefb" stroke="#1565c0" stroke-width="2" rx="4"/>
  <text x="237" y="220" text-anchor="middle" font-size="10" fill="#1565c0">v2</text>
  <rect x="275" y="200" width="55" height="30" fill="#bbdefb" stroke="#1565c0" stroke-width="2" rx="4"/>
  <text x="302" y="220" text-anchor="middle" font-size="10" fill="#1565c0">v2</text>
  <!-- Legend -->
  <rect x="420" y="80" width="20" height="15" fill="#c8e6c9" stroke="#2e7d32" stroke-width="1" rx="2"/>
  <text x="450" y="92" font-size="11">Running v1</text>
  <rect x="420" y="105" width="20" height="15" fill="#ffcdd2" stroke="#c62828" stroke-width="1" rx="2"/>
  <text x="450" y="117" font-size="11">Updating to v2</text>
  <rect x="420" y="130" width="20" height="15" fill="#bbdefb" stroke="#1565c0" stroke-width="1" rx="2"/>
  <text x="450" y="142" font-size="11">Running v2</text>
</svg>

---
## Rolling - Update Ordering

- **One-at-a-time** - safest, slowest; one instance updated per step
- **Batch updates** - update N instances at a time (e.g., 25% of fleet)
- **Zone-aware** - update one availability zone at a time
- Update ordering considerations:
    - Maintain minimum healthy instances at all times
    - Respect `PodDisruptionBudget` in Kubernetes
    - Consider data locality and session affinity
---
## Rolling - Health Checks

- Each updated instance must pass health checks before the next batch starts
- Types of health checks:
    - **Liveness** - is the process running?
    - **Readiness** - can it accept traffic?
    - **Startup** - has it finished initializing?
- Configure appropriate timeouts and thresholds
- Fail the deployment if any instance fails to become healthy
---
## Rolling - Kubernetes Example

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  template:
    spec:
      containers:
        - name: app
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
```

---
## Rolling - Backward Compatibility Requirements

- During a rolling update, **both versions run simultaneously**
- API contracts must be backward compatible:
    - New fields should be optional
    - Removed fields should be deprecated first
    - Endpoints should be versioned (`/api/v1/`, `/api/v2/`)
- Message formats (queues, events) must be readable by both versions
- Shared caches must handle both versions' data formats
---
## Rolling - Handling Stateful Services

- Stateful services add complexity to rolling updates
- Strategies:
    - **Leader election** - update followers first, then the leader
    - **Ordered updates** - `StatefulSet` with `OrderedReady` policy in Kubernetes
    - **Drain before update** - stop accepting new work, finish current work, then update
- Database replicas need special care for schema compatibility
---
## Rolling - When to Use

- Applications with many identical instances behind a load balancer
- Budget-constrained environments (no extra infrastructure needed)
- When brief periods of mixed versions are acceptable
- Stateless or loosely-coupled services
- Kubernetes-native workloads using `Deployment` or `StatefulSet`
---
## Feature Flags - Concept

- Separate **deployment** (shipping code) from **release** (enabling functionality)
- Code for the new feature is deployed but hidden behind a conditional check
- The flag can be toggled at runtime without a new deployment
- Enables dark launches, A/B testing, and gradual rollouts
---
## Feature Flag Decision Tree

<svg width="700" height="350" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr5" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
  <!-- Root -->
  <rect x="250" y="20" width="200" height="40" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="350" y="45" text-anchor="middle" font-size="12" font-weight="bold">Incoming Request</text>
  <!-- Check flag -->
  <rect x="240" y="100" width="220" height="40" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="20"/>
  <text x="350" y="125" text-anchor="middle" font-size="12" font-weight="bold">Feature Flag ON?</text>
  <!-- Yes path -->
  <rect x="80" y="200" width="180" height="40" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="170" y="225" text-anchor="middle" font-size="12" font-weight="bold" fill="#2e7d32">New Code Path (v2)</text>
  <!-- No path -->
  <rect x="440" y="200" width="180" height="40" fill="#ffcdd2" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="530" y="225" text-anchor="middle" font-size="12" font-weight="bold" fill="#c62828">Old Code Path (v1)</text>
  <!-- Arrows -->
  <line x1="350" y1="60" x2="350" y2="95" stroke="#333" stroke-width="2" marker-end="url(#arr5)"/>
  <line x1="290" y1="140" x2="200" y2="195" stroke="#2e7d32" stroke-width="2" marker-end="url(#arr5)"/>
  <line x1="410" y1="140" x2="500" y2="195" stroke="#c62828" stroke-width="2" marker-end="url(#arr5)"/>
  <!-- Labels -->
  <text x="220" y="165" text-anchor="middle" font-size="12" fill="#2e7d32" font-weight="bold">Yes</text>
  <text x="480" y="165" text-anchor="middle" font-size="12" fill="#c62828" font-weight="bold">No</text>
  <!-- Flag source -->
  <rect x="530" y="95" width="140" height="50" fill="#e1bee7" stroke="#7b1fa2" stroke-width="2" rx="5"/>
  <text x="600" y="115" text-anchor="middle" font-size="11" font-weight="bold" fill="#7b1fa2">Flag Service</text>
  <text x="600" y="132" text-anchor="middle" font-size="10" fill="#555">LaunchDarkly, etc.</text>
  <line x1="460" y1="120" x2="525" y2="120" stroke="#7b1fa2" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arr5)"/>
</svg>

---
## Feature Flags - Implementation Example

```python
from feature_flags import client

def get_checkout_page(user, cart):
    if client.is_enabled("new-checkout-flow", user):
        return render_new_checkout(user, cart)
    else:
        return render_old_checkout(user, cart)
```

- The flag `new-checkout-flow` is evaluated at runtime
- Can target specific users, percentages, or segments
- No redeployment needed to enable or disable
---
## Feature Flag Types

- **Release flags** - toggle incomplete features in production; short-lived
- **Experiment flags** - A/B tests for data-driven decisions; medium-lived
- **Ops flags** - circuit breakers and kill switches; long-lived
- **Permission flags** - gate features by user tier or entitlement; permanent
- Each type has a different expected lifecycle and management strategy
---
## Feature Flag Lifecycle Management

1. **Create** - define the flag with a clear owner and expiration date
1. **Develop** - code behind the flag, test both paths
1. **Roll out** - gradually enable for more users
1. **Evaluate** - analyze metrics and decide on permanence
1. **Clean up** - remove the flag and dead code path
- Every flag should have a planned removal date in the backlog
---
## Feature Flag Lifecycle Diagram

<svg width="700" height="180" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr6" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
  <!-- Stages -->
  <rect x="20" y="60" width="100" height="45" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="70" y="80" text-anchor="middle" font-size="11" font-weight="bold">Create</text>
  <text x="70" y="95" text-anchor="middle" font-size="9">Set owner</text>
  <rect x="155" y="60" width="100" height="45" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="5"/>
  <text x="205" y="80" text-anchor="middle" font-size="11" font-weight="bold">Develop</text>
  <text x="205" y="95" text-anchor="middle" font-size="9">Code + test</text>
  <rect x="290" y="60" width="100" height="45" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="340" y="80" text-anchor="middle" font-size="11" font-weight="bold">Roll Out</text>
  <text x="340" y="95" text-anchor="middle" font-size="9">Gradual enable</text>
  <rect x="425" y="60" width="100" height="45" fill="#e1bee7" stroke="#7b1fa2" stroke-width="2" rx="5"/>
  <text x="475" y="80" text-anchor="middle" font-size="11" font-weight="bold">Evaluate</text>
  <text x="475" y="95" text-anchor="middle" font-size="9">Analyze data</text>
  <rect x="560" y="60" width="110" height="45" fill="#ffcdd2" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="615" y="80" text-anchor="middle" font-size="11" font-weight="bold">Clean Up</text>
  <text x="615" y="95" text-anchor="middle" font-size="9">Remove flag</text>
  <!-- Arrows -->
  <line x1="120" y1="82" x2="150" y2="82" stroke="#333" stroke-width="2" marker-end="url(#arr6)"/>
  <line x1="255" y1="82" x2="285" y2="82" stroke="#333" stroke-width="2" marker-end="url(#arr6)"/>
  <line x1="390" y1="82" x2="420" y2="82" stroke="#333" stroke-width="2" marker-end="url(#arr6)"/>
  <line x1="525" y1="82" x2="555" y2="82" stroke="#333" stroke-width="2" marker-end="url(#arr6)"/>
  <!-- Timeline -->
  <line x1="20" y1="140" x2="670" y2="140" stroke="#aaa" stroke-width="2"/>
  <text x="70" y="160" text-anchor="middle" font-size="10" fill="#666">Day 0</text>
  <text x="340" y="160" text-anchor="middle" font-size="10" fill="#666">Week 2-4</text>
  <text x="615" y="160" text-anchor="middle" font-size="10" fill="#666">Remove by deadline</text>
</svg>

---
## Feature Flags - Testing Complexity

- Each flag doubles the possible code paths: N flags = 2^N combinations
- Testing strategy:
    - Test each flag independently in both ON and OFF states
    - Test critical flag combinations explicitly
    - Use **combinatorial testing** to reduce test matrix size
- Example: 10 flags = 1024 combinations
    - Full testing is impractical
    - Focus on pairwise coverage (every pair of flags tested together)
---
## Feature Flags - Testing in CI/CD

```yaml
# CI pipeline testing both flag states
test-feature-flags:
  stage: test
  parallel:
    matrix:
      - FLAG_STATE: ["on", "off"]
  script:
    - export NEW_CHECKOUT=$FLAG_STATE
    - pytest tests/checkout/
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

- Run tests with each flag toggled independently
- Flag combinations for integration tests
---
## Feature Flags - Technical Debt from Long-Lived Flags

- Flags that outlive their purpose become **technical debt**
- Symptoms of flag debt:
    - Nobody remembers what a flag controls
    - Both code paths diverge significantly
    - Removing the flag requires a major refactor
    - Flag interactions cause unexpected behavior
- Prevention:
    - Set expiration dates on every flag
    - Add lint rules that flag stale feature flags
    - Track flag age in dashboards
---
## Feature Flags - Stale Flag Detection

```python
# Example: lint rule for stale flags
import datetime

FLAG_REGISTRY = {
    "new-checkout": {
        "created": "2025-01-15",
        "expires": "2025-04-15",
        "owner": "checkout-team",
    },
}

def check_stale_flags():
    today = datetime.date.today()
    for name, meta in FLAG_REGISTRY.items():
        expires = datetime.date.fromisoformat(
            meta["expires"]
        )
        if today > expires:
            print(f"STALE FLAG: {name}")
```

---
## Feature Flags - Common Pitfalls

- **Nested flags** - flag A depends on flag B, creating brittle logic
- **Flag sprawl** - too many flags make the system unpredictable
- **Missing defaults** - flag service outage should fall back to a safe default
- **Performance** - evaluating flags on every request adds latency
    - Use local caching with periodic sync
    - Avoid remote calls in hot paths
---
## Feature Flags - Tooling Landscape

- **`LaunchDarkly`** - enterprise flag management with targeting and analytics
- **`Unleash`** - open-source feature toggle system
- **`Flagsmith`** - open-source with remote config capabilities
- **`Split.io`** - feature flags combined with experimentation
- **`AWS AppConfig`** - feature flags within the AWS ecosystem
- **Custom solutions** - config files, environment variables, database rows
---
## Feature Flags - When to Use

- When you want to deploy code without exposing features to all users
- For A/B testing and experimentation
- When you need runtime kill switches for risky features
- To enable trunk-based development (no long-lived branches)
- When different customers need different feature sets
---
## Progressive Delivery - Concept

- Progressive delivery **combines** deployment strategies with experimentation
- Core idea: release gradually, observe, and decide based on data
- Builds on canary deployments by adding:
    - User segmentation and targeting
    - Automated analysis and promotion
    - Integration with experimentation platforms
---
## Progressive Delivery Pipeline

<svg width="700" height="280" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr7" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
  <!-- Pipeline stages -->
  <rect x="20" y="30" width="120" height="50" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="80" y="52" text-anchor="middle" font-size="11" font-weight="bold">Build &amp; Test</text>
  <text x="80" y="68" text-anchor="middle" font-size="9">CI pipeline</text>
  <rect x="175" y="30" width="120" height="50" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="5"/>
  <text x="235" y="52" text-anchor="middle" font-size="11" font-weight="bold">Deploy Canary</text>
  <text x="235" y="68" text-anchor="middle" font-size="9">1-5% traffic</text>
  <rect x="330" y="30" width="120" height="50" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="390" y="52" text-anchor="middle" font-size="11" font-weight="bold">Analyze</text>
  <text x="390" y="68" text-anchor="middle" font-size="9">Auto metrics check</text>
  <rect x="485" y="30" width="120" height="50" fill="#e1bee7" stroke="#7b1fa2" stroke-width="2" rx="5"/>
  <text x="545" y="52" text-anchor="middle" font-size="11" font-weight="bold">Promote</text>
  <text x="545" y="68" text-anchor="middle" font-size="9">Increase traffic</text>
  <!-- Arrows -->
  <line x1="140" y1="55" x2="170" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arr7)"/>
  <line x1="295" y1="55" x2="325" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arr7)"/>
  <line x1="450" y1="55" x2="480" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arr7)"/>
  <!-- Feedback loop -->
  <path d="M 545 80 L 545 130 L 235 130 L 235 85" stroke="#f57c00" stroke-width="2" fill="none" stroke-dasharray="6,3" marker-end="url(#arr7)"/>
  <text x="390" y="148" text-anchor="middle" font-size="10" fill="#f57c00" font-weight="bold">Repeat until 100% or rollback</text>
  <!-- Rollback -->
  <rect x="330" y="180" width="120" height="40" fill="#ffcdd2" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="390" y="205" text-anchor="middle" font-size="11" font-weight="bold" fill="#c62828">Rollback</text>
  <line x1="390" y1="80" x2="390" y2="175" stroke="#c62828" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arr7)"/>
  <text x="415" y="140" font-size="10" fill="#c62828">Metrics fail</text>
  <!-- Full rollout -->
  <rect x="530" y="120" width="130" height="40" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="595" y="145" text-anchor="middle" font-size="11" font-weight="bold" fill="#2e7d32">Full Rollout</text>
  <line x1="570" y1="80" x2="585" y2="115" stroke="#2e7d32" stroke-width="2" marker-end="url(#arr7)"/>
</svg>

---
## Progressive Delivery - User Segmentation

- Target specific groups before broader rollout:
    - **Internal users** (dogfooding)
    - **Beta testers** (opt-in early adopters)
    - **Geographic regions** (roll out to one region first)
    - **Customer tiers** (free users before enterprise)
- Segmentation reduces blast radius of failures
- Provides early feedback from representative user groups
---
## Progressive Delivery - Experimentation

- Run **controlled experiments** during progressive rollout
- Compare metrics between control group (old version) and treatment (new version)
- Statistical methods:
    - **Frequentist** - p-value and confidence intervals
    - **Bayesian** - posterior probability of improvement
- Automated experiment evaluation prevents premature decisions
- Tools: `Optimizely`, `Statsig`, `Eppo`, `GrowthBook`
---
## Progressive Delivery - Combining Strategies

- A real-world deployment often uses multiple strategies together:
    - **Feature flags** to hide incomplete work in trunk
    - **Canary deployment** to validate infrastructure changes
    - **Progressive rollout** to increase traffic gradually
    - **Experimentation** to measure business impact
- The combination provides both safety and data-driven decisions
---
## Deployment Strategies - Risk vs. Speed

<svg width="700" height="350" xmlns="http://www.w3.org/2000/svg">
  <!-- Axes -->
  <line x1="80" y1="290" x2="650" y2="290" stroke="#333" stroke-width="2"/>
  <line x1="80" y1="290" x2="80" y2="40" stroke="#333" stroke-width="2"/>
  <!-- Axis labels -->
  <text x="370" y="330" text-anchor="middle" font-size="13" font-weight="bold">Deployment Speed</text>
  <text x="30" y="170" text-anchor="middle" font-size="13" font-weight="bold" transform="rotate(-90, 30, 170)">Safety</text>
  <!-- Points -->
  <circle cx="200" cy="240" r="30" fill="#bbdefb" stroke="#1565c0" stroke-width="2" opacity="0.8"/>
  <text x="200" y="244" text-anchor="middle" font-size="10" font-weight="bold">Blue/</text>
  <text x="200" y="256" text-anchor="middle" font-size="10" font-weight="bold">Green</text>
  <circle cx="350" cy="130" r="30" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" opacity="0.8"/>
  <text x="350" y="134" text-anchor="middle" font-size="10" font-weight="bold">Progressive</text>
  <text x="350" y="146" text-anchor="middle" font-size="10" font-weight="bold">Delivery</text>
  <circle cx="500" cy="200" r="30" fill="#fff9c4" stroke="#f9a825" stroke-width="2" opacity="0.8"/>
  <text x="500" y="204" text-anchor="middle" font-size="10" font-weight="bold">Rolling</text>
  <circle cx="300" cy="100" r="30" fill="#e1bee7" stroke="#7b1fa2" stroke-width="2" opacity="0.8"/>
  <text x="300" y="104" text-anchor="middle" font-size="10" font-weight="bold">Canary</text>
  <circle cx="550" cy="120" r="30" fill="#ffcdd2" stroke="#c62828" stroke-width="2" opacity="0.8"/>
  <text x="550" y="118" text-anchor="middle" font-size="10" font-weight="bold">Feature</text>
  <text x="550" y="130" text-anchor="middle" font-size="10" font-weight="bold">Flags</text>
  <!-- Axis arrows -->
  <text x="640" y="280" font-size="11" fill="#666">Fast</text>
  <text x="85" y="55" font-size="11" fill="#666">Safe</text>
</svg>

---
## Choosing the Right Strategy

- **Blue/Green** - choose when you need instant rollback and can afford double infrastructure
- **Canary** - choose when you want data-driven confidence with moderate infrastructure cost
- **Rolling** - choose when budget is tight and brief mixed-version states are acceptable
- **Feature Flags** - choose when you need to decouple deployment from release
- **Progressive Delivery** - choose when you want maximum safety with experimentation
---
## Choosing Based on Application Type

- **Monolithic applications**
    - Blue/green or rolling deployments work well
    - Feature flags add complexity but enable trunk-based development
- **Microservices**
    - Canary and progressive delivery shine here
    - Each service can have its own deployment strategy
- **Stateful services** (databases, queues)
    - Rolling with ordered updates and leader awareness
    - Blue/green with expand-and-contract migrations
---
## Infrastructure as Code for Deployment Strategies

- Define deployment strategies in `IaC` to ensure consistency
- `Kubernetes` - `Deployment`, `Argo Rollouts`, `Flagger`
- `AWS` - `CodeDeploy` with deployment configurations
- `Terraform` - lifecycle rules and create-before-destroy
- `Pulumi`, `CDK` - programmatic deployment orchestration
- Store deployment configuration alongside application code
---
## Observability is Non-Negotiable

- No deployment strategy works without proper observability
- Required pillars:
    - **Metrics** - `Prometheus`, `Datadog`, `CloudWatch`
    - **Logs** - `ELK stack`, `Loki`, `CloudWatch Logs`
    - **Traces** - `Jaeger`, `Zipkin`, `OpenTelemetry`
- Define SLOs (Service Level Objectives) before deploying
- Automated alerts that trigger rollback decisions
---
## Rollback Strategies Compared

| Strategy | Rollback Method | Time to Rollback | Data Risk |
|----------|----------------|------------------|-----------|
| Blue/Green | Switch traffic back | Seconds | Low |
| Canary | Remove canary instances | Seconds | Low |
| Rolling | Re-deploy old version | Minutes | Medium |
| Feature Flags | Toggle flag off | Instant | Low |
| Progressive | Automated by controller | Seconds | Low |

---
## Real-World Example: Deploying a Payment Service

1. Develop behind a feature flag (`new-payment-gateway`)
1. Deploy code to production with the flag OFF
1. Enable the flag for internal employees (dogfooding)
1. Enable for 5% of users via canary with flag targeting
1. Monitor error rates and payment success rates for 24 hours
1. Progressively roll out to 25%, 50%, 100%
1. Remove the feature flag and old code path within 30 days
---
## Anti-Patterns to Avoid

- **Big bang deployments** - deploying everything at once with no rollback plan
- **Manual deployments** - relying on humans to run scripts in production
- **Skipping health checks** - assuming the deployment succeeded without verification
- **Ignoring database migrations** - breaking changes that prevent rollback
- **Permanent feature flags** - flags that never get cleaned up
- **No monitoring** - deploying blind without observability
---
## Summary

- Every deployment strategy is a trade-off between **cost**, **speed**, **safety**, and **complexity**
- Blue/green gives instant rollback at the cost of double infrastructure
- Canary provides data-driven confidence with moderate overhead
- Rolling is cost-effective but requires backward compatibility
- Feature flags decouple deploy from release but create testing and debt challenges
- Progressive delivery combines these techniques for maximum confidence
- The best teams use **multiple strategies together** based on the change type
