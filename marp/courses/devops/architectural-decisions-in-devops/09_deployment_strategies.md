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

![blue_green_architecture_diagram](svg/courses/devops/architectural-decisions-in-devops/09_deployment_strategies/blue_green_architecture_diagram.svg)

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

![blue_green_database_migration_pattern](svg/courses/devops/architectural-decisions-in-devops/09_deployment_strategies/blue_green_database_migration_pattern.svg)

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

![canary_traffic_split_diagram](svg/courses/devops/architectural-decisions-in-devops/09_deployment_strategies/canary_traffic_split_diagram.svg)

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

![rolling_update_sequence_diagram](svg/courses/devops/architectural-decisions-in-devops/09_deployment_strategies/rolling_update_sequence_diagram.svg)

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

![feature_flag_decision_tree](svg/courses/devops/architectural-decisions-in-devops/09_deployment_strategies/feature_flag_decision_tree.svg)

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

![feature_flag_lifecycle_diagram](svg/courses/devops/architectural-decisions-in-devops/09_deployment_strategies/feature_flag_lifecycle_diagram.svg)

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

![progressive_delivery_pipeline](svg/courses/devops/architectural-decisions-in-devops/09_deployment_strategies/progressive_delivery_pipeline.svg)

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

![deployment_strategies_risk_vs_speed](svg/courses/devops/architectural-decisions-in-devops/09_deployment_strategies/deployment_strategies_risk_vs_speed.svg)

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
