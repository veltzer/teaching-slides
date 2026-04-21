---
tags:
  - infrastructure:cloud
level: beginner
category: cloud
audience:
  - audiences:developers
  - audiences:sysadmins
  - audiences:devops
  - audiences:managers

---
# Choosing a Cloud Provider

---

## Evaluation Criteria
- Service catalog and capabilities
- Pricing and cost structure
- Global infrastructure and Regions
- Compliance and certifications
- Support options and SLAs

---

## Technical Considerations
- Does the provider have the services you need?
- Performance in your target Regions
- Integration with your existing tools
- API quality and documentation
- Community and ecosystem maturity

---

## Organizational Considerations
- Existing vendor relationships (Microsoft, Google)
- Team skills and training availability
- Enterprise support agreements
- Procurement and billing requirements
- Strategic partnerships

---

## Vendor Lock-In
- Proprietary services create dependencies
- Data egress costs make leaving expensive
- Unique APIs and SDKs
- Managed services with no direct equivalent elsewhere
- The more cloud-native, the more locked-in

---

## Reducing Lock-In Risk
- Use open standards (Kubernetes, Terraform, SQL)
- Abstract provider-specific APIs
- Design for portability where it matters
- Accept some lock-in for productivity gains
- Lock-in is a spectrum, not binary

---

## Terraform Multi-Provider Example

```hcl
# Same Terraform, different providers
provider "aws" {
  region = "us-east-1"
}

provider "google" {
  project = "my-project"
  region  = "us-central1"
}

# Kubernetes works on any cloud
provider "kubernetes" {
  config_path = "~/.kube/config"
}
```

---

## When Lock-In Is Acceptable
- Managed service significantly reduces development effort
- No realistic plan to switch providers
- The productivity gains outweigh the risk
- The service has no good portable alternative
- Pragmatism over ideology

---

## Migration Strategies
- Rehost (lift-and-shift): move as-is
- Replatform: minor adjustments for cloud
- Refactor: redesign for cloud-native
- Rebuild: rewrite from scratch
- Replace: switch to SaaS

---

## The 6 R's of Migration: Details
1. Rehost: lift and shift
1. Replatform: lift and reshape
1. Repurchase: switch to SaaS
1. Refactor: re-architect
1. Retain: keep on-premises for now
1. Retire: decommission

---

## The 6 R's of Migration

![6rs](svg/courses/cloud/introduction-to-cloud-computing/12_choosing_a_cloud_provider/six_rs_migration.svg)

---

## Migration Planning
- Assess current portfolio (what do you have?)
- Prioritize workloads for migration
- Start with low-risk, high-value workloads
- Build team skills along the way
- Plan for parallel running periods

---

## Multi-Cloud Strategies
- Use multiple providers strategically
- Best-of-breed service selection
- Geographic or regulatory requirements
- Avoid single point of failure
- Increased complexity is the trade-off

---

## Exit Strategies
- Plan your exit before you enter
- Ensure data export capabilities
- Document provider-specific dependencies
- Test data portability periodically
- Negotiate exit terms in contracts

---

## Making the Decision
- No universally "best" cloud provider
- Depends on your specific requirements
- Start with one provider, expand if needed
- Most important: start building in the cloud
- You can always refine your strategy later
