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
# Data Sovereignty and Compliance

---

## What is Data Sovereignty?
- Data is subject to the laws of the country where it is stored
- Governments require certain data to remain within borders
- Multi-cloud amplifies the challenge: data may cross multiple jurisdictions
- Not just where data lives, but where it transits
- Non-compliance can result in massive fines

---

## Why Multi-Cloud Makes This Harder
- Each provider has different Region availability
- Data replication may cross borders automatically
- CDN edge locations introduce additional jurisdictions
- Backup and DR copies may land in unexpected Regions
- Shared responsibility: cloud provides tools, you enforce policy

---

## Key Regulatory Frameworks
- GDPR (EU): data protection for EU residents
- HIPAA (US): protected health information
- SOC 2: security controls audit framework
- PCI DSS: payment card data security
- Country-specific: LGPD (Brazil), POPIA (South Africa), PDPA (Singapore)

---

## GDPR Requirements
- Lawful basis for processing personal data
- Data subject rights (access, deletion, portability)
- Data cannot leave EEA without adequate safeguards
- Standard Contractual Clauses (SCCs) for transfers
- Breach notification within 72 hours
- Fines up to 4% of global annual revenue

---

## HIPAA in Multi-Cloud
- Protected Health Information (PHI) must be encrypted at rest and in transit
- Business Associate Agreements (BAAs) required with each cloud provider
- AWS, Azure, and GCP all offer HIPAA-eligible services
- Not all services within a cloud are HIPAA-eligible
- Audit trails for all PHI access

---

## SOC 2 Compliance
- Trust Service Criteria: Security, Availability, Processing Integrity, Confidentiality, Privacy
- Requires demonstrating controls over time (Type II)
- Each cloud provider has SOC 2 reports for their infrastructure
- Your responsibility: controls on top of the cloud
- Multi-cloud: must demonstrate controls across all providers

---

## Data Residency Requirements
- Some industries require data to stay in specific countries
- Financial services: often country-specific regulators
- Government data: may require domestic clouds or sovereign regions
- Healthcare: varies widely by jurisdiction
- Identify requirements before choosing cloud Regions

---

## Data Residency Map

![residency](svg/courses/cloud/multi-cloud-strategy/08_data_sovereignty/data_residency_map.svg)

---

## Cloud Provider Region Selection
- AWS: 33+ Regions globally
- Azure: 60+ Regions globally
- GCP: 40+ Regions globally
- Not all services available in all Regions
- Sovereign clouds: AWS GovCloud, Azure Government, Azure China

---

## Terraform Data Residency Policy

```hcl
# Enforce that all resources are created in approved regions only
variable "allowed_regions" {
  type    = list(string)
  default = ["eu-west-1", "eu-central-1", "europe-west1", "westeurope"]
}

# AWS provider locked to EU region
provider "aws" {
  region = "eu-central-1"
  default_tags {
    tags = {
      DataResidency = "EU"
      Compliance    = "GDPR"
    }
  }
}

# Azure provider locked to EU region
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "eu_data" {
  name     = "rg-eu-data"
  location = "westeurope"
  tags = {
    DataResidency = "EU"
    Compliance    = "GDPR"
  }
}
```

---

## Data Classification
- Not all data has the same residency requirements
- Classify data by sensitivity: public, internal, confidential, restricted
- Apply residency rules based on classification
- Public data: may be replicated globally (CDN)
- Restricted data: must stay in specific Regions with encryption

---

## Encryption Across Clouds
- Encryption at rest: AES-256 standard across all major clouds
- Encryption in transit: TLS 1.2+ for all cross-cloud communication
- Key management: AWS KMS, Azure Key Vault, GCP Cloud KMS
- Customer-Managed Keys (CMK) for maximum control
- Consider cross-cloud key management with Vault or BYOK

---

## Audit and Governance
- Centralized logging across all clouds
- AWS CloudTrail, Azure Monitor, GCP Cloud Audit Logs
- Aggregate into SIEM (Splunk, Datadog, Sentinel)
- Prove compliance with continuous audit trails
- Automated compliance reporting

---

## Policy as Code for Compliance
- Define compliance rules as code, not documentation
- OPA (Open Policy Agent): cloud-agnostic policy engine
- AWS Config Rules, Azure Policy, GCP Organization Policy
- Shift compliance left: check in CI/CD pipeline
- Drift detection: alert when resources violate policy

---

## Cloud-Native Compliance Tools
- AWS: Config, Security Hub, Macie, GuardDuty
- Azure: Policy, Defender for Cloud, Purview
- GCP: Security Command Center, DLP API, Policy Intelligence
- Each has strengths; multi-cloud often needs a unified tool
- Examples: Prisma Cloud, Wiz, Lacework

---

## Key Takeaways
- Know your regulatory requirements before choosing Regions
- Classify data and apply residency rules per classification
- Use policy as code to enforce residency constraints automatically
- Encrypt everything, manage keys carefully across clouds
- Centralize audit logs and use unified compliance tooling
