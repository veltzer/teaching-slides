---
tags:
  - infrastructure:cloud
  - practices:finops
  - practices:cost-optimization
level: intermediate
category: cloud
audience:
  - audiences:devops
  - audiences:architects
  - audiences:managers

---
# Tagging Strategies and Cost Allocation

---

## Why Tagging Matters
- Tags are the foundation of cost allocation
- Without tags, costs are a black box
- Answer: "Who is spending what and why?"
- Enable showback and chargeback
- Required for any meaningful FinOps practice

---

## What Are Tags?
- Key-value pairs attached to cloud resources
- Example: Environment=Production, Team=Backend
- Metadata that describes the resource
- Used for billing, operations, security, automation
- Free to create, expensive to ignore

---

## Tagging with CLI and Terraform

```bash
# Tag via AWS CLI
aws ec2 create-tags --resources i-abc123 \
  --tags Key=Team,Value=Platform \
       Key=CostCenter,Value=CC-1234

# Tag in Terraform
resource "aws_instance" "web" {
  ami           = "ami-0c55b159"
  instance_type = "t3.micro"
  tags = {
    Team        = "Platform"
    CostCenter  = "CC-1234"
    Environment = "production"
  }
}
```

---

## Designing a Tagging Strategy
- Define mandatory tags for all resources
- Keep tag keys consistent (naming convention)
- Document the strategy and share widely
- Start simple, expand as needed
- Align with organizational structure

---

## Common Tag Categories
- Cost allocation: Team, Project, CostCenter
- Environment: Environment (dev, staging, prod)
- Operations: Owner, ManagedBy, Application
- Security: DataClassification, Compliance
- Automation: AutoShutdown, BackupPolicy

---

## Mandatory vs Optional Tags
- Mandatory: must be present on every resource
- Optional: useful but not required
- Minimum mandatory set: Team, Environment, Project
- Enforce mandatory tags via policies
- Optional tags add value for specific workflows

---

## Tag Naming Conventions
- Consistent case: CamelCase or snake_case
- Prefix for organization: company:team
- Avoid spaces and special characters
- Document allowed values (enum approach)
- Example: env=prod, env=dev (not Environment=Production)

---

## Tag Enforcement
- Prevention: block resource creation without tags
- Detection: scan and report untagged resources
- AWS: SCP policies, AWS Config rules
- Azure: Azure Policy
- GCP: Organization policies

---

## Tag Enforcement with AWS Config

```json
{
  "ConfigRuleName": "required-tags",
  "Source": {
    "Owner": "AWS",
    "SourceIdentifier": "REQUIRED_TAGS"
  },
  "InputParameters": {
    "tag1Key": "Team",
    "tag2Key": "Environment",
    "tag3Key": "CostCenter"
  },
  "Scope": {
    "ComplianceResourceTypes": [
      "AWS::EC2::Instance",
      "AWS::RDS::DBInstance"
    ]
  }
}
```

---

## Automation for Tagging
- Tag on creation via IaC templates
- Auto-tag from CI/CD pipelines
- Lambda/Functions to tag untagged resources
- Scheduled scans for compliance
- Inheritance from parent resources (where supported)

---

## Cost Allocation Using Tags
- Activate cost allocation tags in billing settings
- Tags appear in Cost Explorer and billing reports
- Filter and group costs by any tag
- Untagged resources show as "No tag"
- Goal: 100% of spend is tagged and allocated

---

## Tagging and Cost Allocation Flow

![tagging_flow](svg/courses/cloud/finops/02_tagging_strategies/tagging_flow.svg)

---

## Account-Based Cost Allocation
- Separate AWS accounts per team or project
- Costs automatically separated
- AWS Organizations for account management
- Combine with tags for fine-grained allocation
- Accounts + tags = complete cost visibility

---

## Showback vs Chargeback
- Showback: inform teams of their spending (no billing)
- Chargeback: bill teams for their actual usage
- Showback is a good starting point
- Chargeback drives stronger accountability
- Both require good tagging and allocation

---

## Cost Allocation Reports
- Regular reports per team, project, environment
- Trend analysis: is spending growing?
- Anomaly detection: sudden spikes
- Comparison against budget
- Share widely and discuss in team meetings

---

## Common Tagging Pitfalls
- Inconsistent tag values (prod vs production vs PROD)
- Too many mandatory tags (creates friction)
- Not enforcing tags (they decay quickly)
- Tagging after the fact (retroactive is painful)
- Not including tags in IaC templates
