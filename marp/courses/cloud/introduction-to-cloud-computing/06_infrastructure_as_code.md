---
tags:
  - infrastructure:cloud
  - practices:devops
  - practices:iac
level: beginner
category: cloud
audience:
  - audiences:developers
  - audiences:sysadmins
  - audiences:devops

---
# Infrastructure as Code Concepts

---

## What is Infrastructure as Code?
- Manage infrastructure through definition files
- Treat infrastructure like application code
- Version controlled, reviewed, tested
- Repeatable and consistent deployments
- No manual clicking in web consoles

---

## Why Infrastructure as Code?
- Eliminate configuration drift
- Reproduce environments exactly
- Audit trail through version control
- Faster disaster recovery
- Enable CI/CD for infrastructure

---

## Declarative vs Imperative
- Declarative: describe the desired state ("I want 3 servers")
- Imperative: describe the steps ("create server, then create server, then...")
- Declarative is preferred for IaC
- The tool figures out how to reach desired state
- Idempotent: run multiple times, same result

---

## Manual vs Automated
- Manual: log into console, click buttons
- Problems: human error, inconsistency, no audit trail
- Automated: define in code, apply with a command
- Repeatable, reviewable, testable
- Infrastructure changes go through pull requests

---

## Configuration Drift
- Over time, environments diverge from intended state
- Manual changes accumulate
- Staging no longer matches production
- Debugging becomes harder
- IaC prevents drift by being the single source of truth

---

## Terraform
- Open-source IaC tool by HashiCorp
- Cloud-agnostic: works with AWS, Azure, GCP, and more
- Declarative HCL language
- State management tracks current infrastructure
- Large ecosystem of providers and modules

---

## Terraform HCL Example

```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  tags = {
    Name = "web-server"
  }
}
```

---

## AWS CloudFormation
- AWS-native IaC service
- YAML or JSON templates
- Deep integration with all AWS services
- Stack management and rollback
- No additional cost (pay for resources created)

---

## CloudFormation Template Example

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Resources:
  WebBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-web-assets
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
```

---

## AWS CDK
- Cloud Development Kit
- Define infrastructure in TypeScript, Python, Java, etc.
- Compiles down to CloudFormation
- Use programming constructs (loops, conditions)
- Higher-level abstractions

---

## Pulumi
- IaC using general-purpose programming languages
- TypeScript, Python, Go, C#, Java
- Multi-cloud support
- State management (cloud or self-hosted)
- Full programming language power

---

## Pulumi Python Example

```python
import pulumi_aws as aws

bucket = aws.s3.Bucket("my-bucket",
    acl="private",
    versioning=aws.s3.BucketVersioningArgs(
        enabled=True,
    ),
)
```

---

## IaC Best Practices
- Store templates in version control
- Use modules for reusable components
- Review changes before applying (plan/preview)
- Test infrastructure code
- Use separate state per environment

---

## IaC in the Development Workflow
1. Developer writes infrastructure code
1. Code review via pull request
1. CI pipeline validates and plans changes
1. Approved changes applied automatically
1. Infrastructure versioned alongside application code

---

## IaC Workflow

![iac](svg/courses/cloud/introduction-to-cloud-computing/06_infrastructure_as_code/iac_workflow.svg)

---

## Getting Started with IaC
- Start with a small project
- Use a single tool consistently
- Learn the declarative mindset
- Practice with cloud free tiers
- Gradually replace manual processes
