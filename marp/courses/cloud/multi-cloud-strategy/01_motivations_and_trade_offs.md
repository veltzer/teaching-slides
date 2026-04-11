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
# Multi-Cloud Motivations and Trade-Offs

---

## What Is Multi-Cloud?
- Using services from two or more public cloud providers
- Distinct from hybrid cloud (public + private)
- Deliberate strategy, not accidental sprawl
- Requires intentional architecture decisions
- Growing adoption across enterprises

---

## Multi-Cloud vs Hybrid Cloud
- Multi-cloud: multiple public clouds (AWS + Azure + GCP)
- Hybrid cloud: public cloud + on-premises infrastructure
- These are orthogonal — you can have both
- Hybrid addresses data locality and legacy systems
- Multi-cloud addresses vendor risk and best-of-breed needs

---

<!-- SVG placeholder: diagram showing multi-cloud vs hybrid cloud topology -->

## Multi-Cloud vs Hybrid Cloud

---

## Why Multi-Cloud: Avoiding Vendor Lock-In
- Reduce dependency on a single provider
- Maintain negotiating leverage on pricing
- Protect against provider outages or policy changes
- Preserve ability to migrate workloads
- Strategic insurance against vendor risk

---

## Why Multi-Cloud: Best-of-Breed Services
- AWS excels in breadth and ecosystem maturity
- Azure leads in enterprise identity and Microsoft integration
- GCP leads in data analytics and machine learning
- Each provider has unique strengths
- Pick the best tool for each workload

---

## Why Multi-Cloud: Compliance and Data Sovereignty
- Regulations may require specific geographic regions
- Some regions only available on certain providers
- Government contracts may mandate specific clouds
- Data residency laws vary by country
- Multi-cloud enables compliance flexibility

---

## Why Multi-Cloud: Business Resilience
- Provider-level outages do happen (AWS us-east-1, Azure AD)
- Multi-cloud enables disaster recovery across providers
- Reduces blast radius of any single failure
- Meets strict SLA requirements through redundancy
- Critical for mission-critical applications

---

## Why Multi-Cloud: Mergers and Acquisitions
- Acquired companies often use different providers
- Forcing migration is expensive and risky
- Multi-cloud lets you integrate gradually
- Common in large enterprises
- Organic multi-cloud is the most common path

---

## The Cost of Multi-Cloud: Complexity
- Every additional provider multiplies operational surface
- Different APIs, SDKs, CLIs, and consoles
- Networking between clouds is non-trivial
- Security policies must span multiple platforms
- Monitoring and observability become harder

---

## The Cost of Multi-Cloud: Skills Gap
- Engineers need expertise across multiple platforms
- Certifications and training multiply
- Hiring becomes more difficult
- Deep expertise is harder to achieve per platform
- Consider whether breadth or depth serves you better

---

<!-- SVG placeholder: chart comparing complexity growth with number of cloud providers -->

## Complexity Growth with Provider Count

---

## Benefits vs Risks

![risks](svg/courses/cloud/multi-cloud-strategy/01_motivations/multi_cloud_risks.svg)

---

## The Cost of Multi-Cloud: Financial Overhead
- Volume discounts are diluted across providers
- Reserved instances and committed-use lose effectiveness
- Data transfer between clouds is expensive
- Tooling and management overhead adds cost
- The multi-cloud tax is real — budget for it

---

## Common Multi-Cloud Patterns
- Active-active: workloads run simultaneously on multiple clouds
- Active-passive: failover from primary to secondary cloud
- Segmented: different workloads on different clouds
- Burst: overflow from primary cloud to secondary
- Segmented is the most common and easiest to manage

---

## Multi-Cloud Patterns

![patterns](svg/courses/cloud/multi-cloud-strategy/01_motivations/multi_cloud_patterns.svg)

---

## Terraform Multi-Provider Declaration

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

provider "azurerm" {
  features {}
}

provider "google" {
  project = "my-project"
  region  = "us-central1"
}
```

---

## When Multi-Cloud Makes Sense
- Large enterprises with diverse workload requirements
- Strict compliance or data sovereignty needs
- Business-critical applications requiring provider-level DR
- Organizations with strong platform engineering teams
- M&A scenarios with existing multi-provider footprint

---

## When Multi-Cloud Is Not Worth It
- Small to mid-size organizations
- Teams lacking cloud expertise depth
- Workloads with tight inter-service coupling
- When the primary driver is only cost optimization
- When a single provider meets all requirements
