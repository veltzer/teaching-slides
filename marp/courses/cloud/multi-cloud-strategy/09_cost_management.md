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
# Cost Management Across Providers

---

## The Multi-Cloud Cost Challenge
- Each cloud has different pricing models and units
- Comparing costs across providers is not straightforward
- Egress charges compound in multi-cloud architectures
- Discounts are provider-specific and non-transferable
- Without unified visibility, costs spiral

---

## Unified Cost Visibility
- Single pane of glass for all cloud spending
- Normalize costs across different billing formats
- Tools: CloudHealth, Apptio Cloudability, Finout, Vantage
- Cloud-native: AWS Cost Explorer + Azure Cost Management + GCP Billing
- Custom dashboards combining all three via APIs

---

## Unified Cost View

![cost](svg/courses/cloud/multi-cloud-strategy/09_cost_management/unified_cost_view.svg)

---

## FinOps for Multi-Cloud
- FinOps is the practice of managing cloud costs as a team sport
- Three phases: Inform, Optimize, Operate
- Inform: who is spending what, where
- Optimize: rightsize, reserve, eliminate waste
- Operate: continuous governance and accountability

---

## FinOps Team Structure
- FinOps practitioner: central coordination
- Engineering: owns resource usage decisions
- Finance: budget tracking and forecasting
- Executives: set cost targets and priorities
- In multi-cloud: each cloud may need a subject matter expert

---

## Consistent Tagging Strategy
- Tags are the foundation of cost allocation
- Enforce the same tag keys across all clouds
- Minimum tags: Team, Environment, CostCenter, Application
- Automate tag enforcement with policies
- Untagged resources = unattributed cost = waste

---

## Multi-Cloud Tagging with Terraform

```hcl
# Define common tags in a local variable
locals {
  common_tags = {
    Team        = "platform"
    Environment = "production"
    CostCenter  = "CC-4200"
    Application = "order-service"
    ManagedBy   = "terraform"
  }
}

# AWS resource with consistent tags
resource "aws_instance" "app" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "m5.large"
  tags          = local.common_tags
}

# Azure resource with the same tags
resource "azurerm_linux_virtual_machine" "app" {
  name                = "vm-order-service"
  resource_group_name = azurerm_resource_group.main.name
  location            = "westeurope"
  size                = "Standard_D2s_v3"
  tags                = local.common_tags
  # ... other config
}

# GCP resource with the same labels
resource "google_compute_instance" "app" {
  name         = "vm-order-service"
  machine_type = "e2-standard-2"
  zone         = "europe-west1-b"
  labels       = local.common_tags
  # ... other config
}
```

---

## Cost Allocation and Chargeback
- Allocate costs to business units or teams
- Showback: show teams what they spend (informational)
- Chargeback: charge teams for what they spend (financial)
- Requires mature tagging and reporting
- Multi-cloud: normalize units before comparing

---

## Committed Use Discounts
- AWS: Reserved Instances (RIs), Savings Plans
- Azure: Reserved VM Instances, Azure Savings Plans
- GCP: Committed Use Discounts (CUDs)
- Discounts range from 20% to 72% depending on commitment
- Challenge: commits lock you to a specific provider

---

## Discount Strategy in Multi-Cloud
- Commit to each cloud proportionally to steady-state usage
- Use on-demand for burst and variable workloads
- Do not over-commit to one cloud if migration is planned
- Review commitments quarterly
- Spot/Preemptible for fault-tolerant workloads across all clouds

---

## Egress Costs: The Hidden Tax
- Cloud providers charge for data leaving their network
- Cross-cloud data transfer doubles egress costs
- AWS: $0.09/GB out, Azure: $0.087/GB, GCP: $0.12/GB (approximate)
- Design to minimize cross-cloud data movement
- Co-locate tightly coupled services on the same cloud

---

## Reducing Egress Costs
- Use cloud interconnects (AWS Direct Connect, Azure ExpressRoute, GCP Interconnect)
- Dedicated interconnects have lower per-GB costs
- Compress data before transferring across clouds
- Cache frequently accessed cross-cloud data locally
- Consider Google Cloud CDN Interconnect or similar programs

---

## Rightsizing Across Clouds
- Instance types differ across providers
- Use cloud-native rightsizing tools per provider
- AWS Compute Optimizer, Azure Advisor, GCP Recommender
- Normalize instance families for comparison
- Automate rightsizing reviews monthly

---

## Key Takeaways
- Unified visibility across all clouds is non-negotiable
- Consistent tagging is the foundation of cost management
- FinOps practices apply to multi-cloud with added complexity
- Egress costs are the biggest hidden cost of multi-cloud
- Commit to discounts carefully when workloads may move
