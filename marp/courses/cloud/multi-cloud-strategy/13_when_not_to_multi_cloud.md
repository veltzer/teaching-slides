---
tags:
  - infrastructure:cloud
  - infrastructure:aws
  - infrastructure:azure
  - infrastructure:gcp
  - concepts:architecture
level: advanced
category: cloud
audience:
  - audiences:architects
  - audiences:managers

---
# When Not to Go Multi-Cloud

## Mark Veltzer

## mark.veltzer@gmail.com

---

## The Honest Question
- Multi-cloud is not always the right answer
- Every architecture decision has trade-offs
- Multi-cloud adds complexity, cost, and cognitive load
- Sometimes single-cloud is the better strategy
- This chapter helps you make a pragmatic decision

---

## Multi-Cloud Complexity Tax
- Every abstraction layer adds latency, bugs, and maintenance
- Teams must learn multiple cloud platforms
- IaC templates must support multiple providers
- CI/CD pipelines multiply
- Incident response spans multiple consoles and APIs

---

## The Lowest Common Denominator Problem
- Abstracting across clouds means using only common features
- You lose access to each cloud's best capabilities
- Example: DynamoDB Streams, Azure Cognitive Services, BigQuery ML
- The abstraction layer becomes your real platform
- Innovation speed drops when you cannot use native features

---

## When Single-Cloud is Better
- Small to medium organizations with limited cloud teams
- Workloads that heavily use cloud-native services
- When one cloud clearly dominates your requirements
- Early-stage companies that need velocity over resilience
- When the cost of multi-cloud exceeds the risk it mitigates

---

## Cost Reality Check
- Multi-cloud overhead: 15-30% higher total cost of ownership
- Egress fees between clouds add up quickly
- Dual tooling: monitoring, security, governance tools for each cloud
- Staff costs: broader skill requirements, more training
- Opportunity cost: time spent on abstraction vs product features

---

## Complexity vs Benefit

![complexity](svg/courses/cloud/multi-cloud-strategy/13_when_not_to/complexity_vs_benefit.svg)

---

## The Vendor Lock-In Fear
- Lock-in fear is the top driver for multi-cloud adoption
- But how real is the risk?
- Major cloud providers are stable, well-funded companies
- Contractual protections (pricing commitments, SLAs) exist
- Switching costs exist, but they are manageable when needed

---

## Analyzing Lock-In Risk
- Compute (VMs, containers): low lock-in, easily portable
- Managed databases: moderate lock-in, standard engines help
- Serverless (Lambda, Cloud Functions): high lock-in
- Proprietary ML/AI services: very high lock-in
- Quantify lock-in per workload, not as a blanket concern

---

## Portability Without Multi-Cloud
- Use open standards: Kubernetes, PostgreSQL, Terraform
- Avoid proprietary APIs where open alternatives exist
- Containerize everything
- Keep data in portable formats
- You can be portable without running on multiple clouds

---

## Single-Cloud Optimized Architecture

```hcl
# Single-cloud architecture: simpler, cheaper, fully optimized
# This uses AWS-native services without abstraction overhead

resource "aws_ecs_cluster" "main" {
  name = "production"
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_ecs_service" "api" {
  name            = "api-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.api.arn
  desired_count   = 3
  launch_type     = "FARGATE"

  load_balancer {
    target_group_arn = aws_lb_target_group.api.arn
    container_name   = "api"
    container_port   = 8080
  }
}

resource "aws_dynamodb_table" "orders" {
  name         = "orders"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "order_id"
  range_key    = "created_at"

  attribute {
    name = "order_id"
    type = "S"
  }
  attribute {
    name = "created_at"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }
}

# Native integration: DynamoDB Streams -> Lambda -> SNS
# No cross-cloud translation needed
resource "aws_lambda_event_source_mapping" "orders_stream" {
  event_source_arn  = aws_dynamodb_table.orders.stream_arn
  function_name     = aws_lambda_function.order_processor.arn
  starting_position = "LATEST"
}
```

---

## Compare: Multi-Cloud Version of Same Architecture

```hcl
# Multi-cloud version: more code, more complexity, fewer features
# Must use cloud-agnostic alternatives for everything

resource "kubernetes_deployment" "api" {
  metadata {
    name = "api-service"
  }
  spec {
    replicas = 3
    selector {
      match_labels = { app = "api" }
    }
    template {
      metadata {
        labels = { app = "api" }
      }
      spec {
        container {
          name  = "api"
          image = "myregistry/api:latest"
          port {
            container_port = 8080
          }
        }
      }
    }
  }
}

# Must use PostgreSQL instead of DynamoDB for portability
# Loses DynamoDB Streams, pay-per-request, auto-scaling
resource "helm_release" "postgresql" {
  name       = "orders-db"
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "postgresql"
  values     = [file("postgres-values.yaml")]
}
# Now you manage the database yourself on every cloud
```

---

## Unnecessary Multi-Cloud Scenarios
- Using GCP just for BigQuery when AWS Redshift would suffice
- Running secondary cloud for a single non-critical workload
- Multi-cloud to satisfy a checkbox without clear requirements
- Following industry trends without analyzing your own needs
- "Everyone is doing multi-cloud" is not a strategy

---

## The Multi-Cloud Decision Framework
- Step 1: Identify the specific problem you are trying to solve
- Step 2: Quantify the risk of single-cloud (probability x impact)
- Step 3: Estimate the cost of multi-cloud (TCO + opportunity cost)
- Step 4: Compare alternatives (portability, contractual protections, insurance)
- Step 5: Decide based on evidence, not fear

---

## Decision Matrix

| Factor | Single-Cloud | Multi-Cloud |
|--------|-------------|-------------|
| Complexity | Lower | Higher |
| Cost | Lower | 15-30% higher |
| Talent needs | Focused | Broader |
| Vendor risk | Higher | Lower |
| Innovation speed | Faster | Slower |
| Resilience | Region-level | Provider-level |

---

## When Multi-Cloud IS Justified
- Regulatory requirement for provider diversity
- Merger/acquisition brings a second cloud
- Specific best-of-breed service on another cloud (e.g., GCP for ML)
- Provider-level DR for critical national infrastructure
- Very large organizations with deep cloud expertise on multiple teams

---

## Accidental Multi-Cloud
- Most multi-cloud is not strategic, it is accidental
- One team chose AWS, another chose Azure
- Acquisition brought GCP workloads
- Shadow IT deployed on a different cloud
- Accidental multi-cloud has costs without benefits

---

## Rationalizing Accidental Multi-Cloud
- Audit all cloud usage across the organization
- Decide: consolidate or embrace
- If consolidating: migrate to the dominant provider
- If embracing: invest in governance, tooling, and skills
- Half-measures (ignoring the second cloud) are the worst option

---

## The Build vs Buy Tradeoff
- Multi-cloud abstraction layers can be built or bought
- Building: full control, high maintenance cost
- Buying: Anthos, Azure Arc, vendor-managed platforms
- Both add complexity compared to single-cloud native
- Evaluate whether the abstraction is worth the cost

---

## Opportunity Cost
- Every hour spent on multi-cloud abstraction is not spent on product
- Engineering velocity matters more than theoretical resilience
- Startups should almost never go multi-cloud
- Growth companies should evaluate carefully
- Enterprises have the resources but should still question the need

---

## Case Study: Startup That Went Multi-Cloud Too Early
- 20-person startup, B2B SaaS product
- CTO mandated multi-cloud from day one
- Built Kubernetes abstraction across AWS and GCP
- Result: 40% of engineering time on infrastructure
- Product development stalled, competitors moved faster
- Eventually consolidated to single cloud, regained velocity

---

## Case Study: Enterprise That Benefited from Multi-Cloud
- Fortune 500 financial services company
- Regulatory requirement for provider diversity
- AWS for primary workloads, Azure for Microsoft integrations
- GCP for data analytics (BigQuery)
- Invested in platform team (15 engineers)
- Justified by regulatory compliance and genuine best-of-breed needs

---

## Case Study: The Middle Ground
- Mid-size company, 200 engineers
- Primary cloud: AWS (95% of workloads)
- Secondary use: GCP BigQuery for analytics only
- Did not invest in full multi-cloud abstraction
- Used Terraform for both, accepted some duplication
- Pragmatic: multi-cloud where it matters, single-cloud everywhere else

---

## Avoiding Multi-Cloud Pitfalls
- Do not abstract prematurely
- Start with single-cloud, add second only when justified
- Keep portability in mind without over-engineering for it
- Containerize workloads for future flexibility
- Use standard databases and protocols where possible

---

## The Pragmatic Path
- Default to single-cloud until proven otherwise
- Invest in portability (containers, open standards, IaC)
- Add a second cloud only for specific, justified reasons
- Govern multi-cloud properly if you adopt it
- Review the decision annually as requirements change

---

## Questions to Ask Before Going Multi-Cloud
- What specific problem does multi-cloud solve for us?
- Can we solve it with single-cloud alternatives?
- Do we have the team to support multiple clouds?
- Have we calculated the total cost of ownership?
- Is our organization mature enough for this complexity?

---

## Key Takeaways
- Multi-cloud is a tool, not a goal
- Single-cloud with portability is often the better strategy
- Quantify the actual risk of vendor lock-in for your workloads
- Accidental multi-cloud should be rationalized, not ignored
- The right answer depends on your specific context, team, and requirements
- When in doubt, start simple and add complexity only when justified
