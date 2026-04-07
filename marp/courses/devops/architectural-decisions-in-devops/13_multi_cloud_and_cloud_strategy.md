# Multi-Cloud and Cloud Strategy
---
## Why Cloud Strategy Matters

- Cloud is no longer "if" but "how"
- Choosing a strategy impacts cost, agility, and resilience
- Wrong decisions create years of technical debt
- Strategy must align with business goals, compliance, and team skills
- No single approach fits all organizations
---
## Cloud Deployment Models Overview

![cloud_deployment_models_overview](/svg/courses/devops/architectural-decisions-in-devops/13_multi_cloud_and_cloud_strategy/cloud_deployment_models_overview.svg)

---
## Single Cloud Strategy

- All infrastructure and services on one cloud provider
- Examples: all-in on `AWS`, `Azure`, or `GCP`
- Deepest access to cloud-native features
- Single billing relationship and volume discounts
- Unified IAM, networking, and monitoring
- Smaller operations team needed
---
## Single Cloud Risks

- Complete dependency on one vendor
- Pricing changes impact entire infrastructure
- Outages affect all workloads simultaneously
- Negotiating leverage decreases over time
- Migration cost grows exponentially with adoption depth
---
## Multi-Cloud Strategy

- Workloads distributed across two or more cloud providers
- Different providers for different workloads (polyglot cloud)
- Same workload portable across providers (true multi-cloud)
- Requires abstraction layers or duplicated expertise
- Growing trend among enterprises
---
## Multi-Cloud Topology

![multi_cloud_topology](/svg/courses/devops/architectural-decisions-in-devops/13_multi_cloud_and_cloud_strategy/multi_cloud_topology.svg)

---
## Hybrid Cloud Strategy

![hybrid_cloud_strategy](/svg/courses/devops/architectural-decisions-in-devops/13_multi_cloud_and_cloud_strategy/hybrid_cloud_strategy.svg)

---
## Comparing the Three Approaches

| Aspect | Single Cloud | Multi-Cloud | Hybrid |
|--------|-------------|-------------|--------|
| Complexity | Low | High | Medium |
| Vendor lock-in | High | Low | Medium |
| Cost optimization | Good | Best potential | Variable |
| Team skills | Focused | Broad | Mixed |
| Compliance | Provider-dependent | Flexible | Strong |
---
## Vendor Lock-in: What It Really Means

- Lock-in is not just about compute instances
- The real lock-in comes from:
    - Managed databases (`DynamoDB`, `Cosmos DB`, `Spanner`)
    - Serverless platforms (`Lambda`, `Cloud Functions`)
    - Identity and access management (`IAM` policies)
    - Proprietary APIs and SDKs
    - Data egress costs making migration expensive
---
## The Lock-in Spectrum

![the_lock_in_spectrum](/svg/courses/devops/architectural-decisions-in-devops/13_multi_cloud_and_cloud_strategy/the_lock_in_spectrum.svg)

---
## Embracing Cloud-Native Services

- Cloud-native services offer significant advantages:
    - Reduced operational burden (no patching, scaling, backups)
    - Better performance through provider optimization
    - Faster time-to-market
    - Built-in high availability
- Using `RDS` instead of self-managed `PostgreSQL` saves ops time
- Using `SQS` instead of self-managed `RabbitMQ` eliminates cluster management
---
## The Cost of Not Going Cloud-Native

- Running `Kubernetes` + `PostgreSQL` + `Kafka` yourself means:
    - Hiring and retaining specialized staff
    - Handling upgrades, patches, and security fixes
    - Managing backups and disaster recovery
    - 24/7 on-call rotation
- Estimate: 2-5 full-time engineers per major self-managed service
- The "portable" choice can be the more expensive choice
---
## When to Embrace or Avoid Lock-in

- Embrace lock-in when:
    - Organization is too small for multi-vendor negotiations
    - Time-to-market is the primary constraint
    - Provider native service is significantly superior
    - Workloads are unlikely to move in 3-5 years
- Avoid lock-in when:
    - Regulatory requirements mandate multi-provider capability
    - Data volumes make egress costs a serious concern
    - You need competitive pricing leverage
---
## Regulatory and Data Sovereignty

- Laws dictate where data can be stored and processed
- Key regulations:
    - `GDPR` (EU) - data must stay in EU or approved countries
    - `CCPA` (California) - consumer data protection rights
    - `PIPL` (China) - strict data localization requirements
    - `LGPD` (Brazil), `PDPA` (Singapore) - regional frameworks
- Multi-cloud helps: deploy in local providers per jurisdiction
---
## Data Sovereignty Map

![data_sovereignty_map](/svg/courses/devops/architectural-decisions-in-devops/13_multi_cloud_and_cloud_strategy/data_sovereignty_map.svg)

---
## Cloud Strategy Decision Framework

- Ask these questions before choosing a strategy:
    - Where are our customers geographically?
    - What are our regulatory obligations?
    - What is our team's cloud expertise?
    - What is our budget for abstraction and tooling?
    - What is our risk tolerance for outages?
    - How likely is a future migration?
---
## Cloud-Agnostic Tooling

- Tools that work across cloud providers:
    - `Terraform` / `OpenTofu` for infrastructure
    - `Kubernetes` for container orchestration
    - `Prometheus` + `Grafana` for monitoring
    - `Vault` for secrets management
- Promise: write once, deploy anywhere
- Reality: "write once, debug everywhere"
- Each provider has different networking, IAM, storage, and DNS models
---
## The Lowest Common Denominator Problem

![the_lowest_common_denominator_problem](/svg/courses/devops/architectural-decisions-in-devops/13_multi_cloud_and_cloud_strategy/the_lowest_common_denominator_problem.svg)

---
## Abstraction Layer Architecture

![abstraction_layer_architecture](/svg/courses/devops/architectural-decisions-in-devops/13_multi_cloud_and_cloud_strategy/abstraction_layer_architecture.svg)

---
## Cost of Abstraction Layers

- Engineering cost to build and maintain the abstraction
- Performance overhead from additional indirection
- Feature lag: new provider features take months to integrate
- Testing cost: every change must be verified on all providers
- Debugging complexity: issues may be in the abstraction, not the app
- Estimate: 1-3 full-time engineers to maintain a cloud abstraction
---
## Terraform as a Multi-Cloud Tool

- `Terraform` uses providers to abstract cloud resources
- Same HCL syntax, different providers underneath

```hcl
# AWS
resource "aws_instance" "web" {
  ami           = "ami-0c55b159"
  instance_type = "t3.micro"
}

# GCP
resource "google_compute_instance" "web" {
  machine_type = "e2-micro"
  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }
}
```

---
## Terraform Multi-Cloud Limitations

- Resource types are completely different across providers
- You cannot reuse the same `.tf` file for multiple clouds
- State management differs per provider
- Modules are provider-specific
- `Terraform` helps with consistency, not with portability
- True portability requires a wrapper layer on top of `Terraform`
---
## Kubernetes as a Portability Layer

- `Kubernetes` provides a consistent API across clouds
- Same `Deployment`, `Service`, `Ingress` manifests work on `EKS`, `AKS`, `GKE`
- But underlying details differ:
    - Load balancer implementations
    - Storage class drivers (`EBS CSI`, `Azure Disk`, `PD CSI`)
    - Networking (`CNI` plugins vary per provider)
    - Node auto-scaling behavior (`Karpenter` vs `Autopilot`)
---
## The Real Multi-Cloud Cost

![the_real_multi_cloud_cost](/svg/courses/devops/architectural-decisions-in-devops/13_multi_cloud_and_cloud_strategy/the_real_multi_cloud_cost.svg)

---
## When Multi-Cloud Makes Sense

- Acquisitions bring different cloud footprints
- Best-of-breed services on different providers
    - `BigQuery` on GCP for analytics
    - `Azure AD` for enterprise identity
    - `AWS` for broadest service catalog
- Regulatory requirements across jurisdictions
- Genuine need for vendor negotiation leverage
---
## When Multi-Cloud Does Not Make Sense

- "We might need it someday" is not a strategy
- Small teams (under 50 engineers) rarely benefit
- If you are not using advanced cloud-native services
- If your workloads are simple web applications
- If you lack budget for the additional tooling and staff
---
## Disaster Recovery: Core Concepts

- `RPO` - Recovery Point Objective: how much data can you lose?
- `RTO` - Recovery Time Objective: how fast must you recover?
- These drive architecture and cost decisions
- Lower RPO/RTO means higher cost
- Must be defined per workload, not globally
---
## DR Tiers

| Tier | Strategy | RTO | RPO | Cost |
|------|----------|-----|-----|------|
| 1 | Backup and Restore | Hours | Hours | Low |
| 2 | Pilot Light | 30 min | Minutes | Medium |
| 3 | Warm Standby | Minutes | Seconds | High |
| 4 | Active-Active | Near zero | Near zero | Very High |
---
## Backup and Restore Architecture

![backup_and_restore_architecture](/svg/courses/devops/architectural-decisions-in-devops/13_multi_cloud_and_cloud_strategy/backup_and_restore_architecture.svg)

---
## Warm Standby Architecture

![warm_standby_architecture](/svg/courses/devops/architectural-decisions-in-devops/13_multi_cloud_and_cloud_strategy/warm_standby_architecture.svg)

---
## Active-Active Architecture

![active_active_architecture](/svg/courses/devops/architectural-decisions-in-devops/13_multi_cloud_and_cloud_strategy/active_active_architecture.svg)

---
## Cross-Region Networking and Replication

- Connectivity options:
    - `VPC Peering` - direct, low-latency, same provider
    - `Transit Gateway` - hub-and-spoke model
    - `Direct Connect` / `ExpressRoute` - dedicated links
- Replication strategies:
    - **Synchronous**: zero data loss, higher latency
    - **Asynchronous**: minimal lag, possible data loss
    - **Eventual consistency**: replicas converge over time
---
## Multi-Region DNS Failover

```yaml
# Route 53 health check and failover example
Resources:
  PrimaryHealthCheck:
    Type: AWS::Route53::HealthCheck
    Properties:
      HealthCheckConfig:
        FullyQualifiedDomainName: "primary.example.com"
        Port: 443
        Type: HTTPS
        FailureThreshold: 3
  DNSRecord:
    Type: AWS::Route53::RecordSet
    Properties:
      Name: "app.example.com"
      Type: A
      SetIdentifier: "primary"
      Failover: PRIMARY
      HealthCheckId: !Ref PrimaryHealthCheck
```

---
## Cross-Cloud DR Architecture

![cross_cloud_dr_architecture](/svg/courses/devops/architectural-decisions-in-devops/13_multi_cloud_and_cloud_strategy/cross_cloud_dr_architecture.svg)

---
## Testing and Automating DR

- Test your DR plan before you need it
- Tools: `Chaos Monkey`, `Gremlin`, `Litmus`
- Regular "Game Day" exercises simulate real failures
- All DR infrastructure must be defined in code
    - `Terraform`, `Pulumi`, or `CloudFormation` for infra
    - `Ansible` or scripts for failover orchestration
- No manual steps during high-stress failover events
---
## Multi-Region Data Consistency

- CAP theorem applies: you cannot have all three:
    - **Consistency**: all reads return the latest write
    - **Availability**: every request gets a response
    - **Partition tolerance**: system works despite network splits
- Multi-region systems must choose between CP and AP
- Most choose AP with eventual consistency
- Critical transactions may need CP with higher latency
---
## Egress Costs and Exit Strategy

- Cloud providers charge for outbound data transfer
- Typical egress costs:
    - `AWS`: $0.09/GB, `Azure`: $0.087/GB, `GCP`: $0.12/GB
- Cross-cloud replication can cost thousands per month
- Even with single cloud, plan for potential migration:
    - Use standard data formats (`Parquet`, `JSON`, `Avro`)
    - Avoid proprietary query languages where possible
    - Document all cloud-specific dependencies
---
## Cloud Strategy Anti-Patterns

- "Multi-cloud by accident" - no intentional strategy
- "Resume-driven multi-cloud" - using tools for learning, not value
- "All eggs in one basket" - no DR plan at all
- "Over-abstracted" - seven layers between app and cloud
- "Lift and shift forever" - running VMs without using cloud services
- "Cloud-native maximalist" - using every managed service available
---
## Decision Matrix: Choosing Your Strategy

![decision_matrix_choosing_your_strategy](/svg/courses/devops/architectural-decisions-in-devops/13_multi_cloud_and_cloud_strategy/decision_matrix_choosing_your_strategy.svg)

---
## Summary: Key Takeaways

- Start with business requirements, not technology preferences
- Single cloud is right for most organizations
- Multi-cloud adds real value only when justified by specific needs
- Abstraction layers are expensive to build and maintain
- The LCD problem limits what you can achieve portably
- DR and HA plans must be tested, not just documented
- Data sovereignty increasingly drives cloud strategy
- Always account for hidden costs: egress, staff, tooling
