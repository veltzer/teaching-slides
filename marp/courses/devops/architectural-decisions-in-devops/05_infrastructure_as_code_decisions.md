# Infrastructure as Code Decisions
---
## What is Infrastructure as Code?

- Managing infrastructure through machine-readable definition files
- Version-controlled, repeatable, and auditable
- Replaces manual provisioning with automated workflows
- Key decision: which approach, tool, and patterns to adopt
---
## Why IaC Matters for DevOps

1. Eliminates configuration drift between environments
1. Enables reproducible deployments
1. Supports collaboration through version control
1. Provides an audit trail for compliance
1. Reduces mean time to recovery (`MTTR`)
---
## The Two Paradigms

![the_two_paradigms](/svg/courses/devops/architectural-decisions-in-devops/05_infrastructure_as_code_decisions/the_two_paradigms.svg)

---
## Declarative vs Imperative Flow

![declarative_vs_imperative_flow](/svg/courses/devops/architectural-decisions-in-devops/05_infrastructure_as_code_decisions/declarative_vs_imperative_flow.svg)

---
## Terraform Overview

- HashiCorp's declarative IaC tool
- Uses `HCL` (HashiCorp Configuration Language)
- Provider-based architecture for multi-cloud support
- Plan-and-apply workflow with explicit approval step
- Open-source core with commercial offerings (`Terraform Cloud`, `HCP Terraform`)
---
## Terraform Example

```hcl
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
  tags = {
    Name = "web-server"
    Env  = "production"
  }
}

output "public_ip" {
  value = aws_instance.web.public_ip
}
```

- Declarative: describes what should exist
- `terraform plan` shows what will change
---
## Terraform Plan-Apply Cycle

![terraform_plan_apply_cycle](/svg/courses/devops/architectural-decisions-in-devops/05_infrastructure_as_code_decisions/terraform_plan_apply_cycle.svg)

---
## Terraform Strengths and Weaknesses

- Strengths:
    - Mature ecosystem with 3000+ providers
    - Clear separation of plan and apply phases
    - `HCL` is purpose-built: readable by non-developers
    - Strong community modules on the Terraform Registry
- Weaknesses:
    - State file is a single point of failure
    - `HCL` lacks full programming constructs
    - Refactoring resources often requires `terraform state mv`
---
## Pulumi Overview

- IaC using general-purpose languages
- Supports `TypeScript`, `Python`, `Go`, `C#`, `Java`, `YAML`
- Same cloud providers as Terraform (built on provider SDKs)
- Managed state service or self-managed backends
---
## Pulumi Example

```python
import pulumi
import pulumi_aws as aws

instance = aws.ec2.Instance(
    "web-server",
    ami="ami-0c55b159cbfafe1f0",
    instance_type="t3.micro",
    tags={"Name": "web-server", "Env": "prod"},
)

pulumi.export("public_ip", instance.public_ip)
```

- Real Python: use loops, classes, and libraries
- Same outcome as the Terraform example
---
## Pulumi Strengths and Weaknesses

- Strengths:
    - Full programming language capabilities
    - Native testing with standard test frameworks
    - Strong typing catches errors before deployment
    - `Automation API` for embedding IaC in applications
- Weaknesses:
    - Steeper learning curve for ops-focused teams
    - Smaller community compared to Terraform
    - Debugging infrastructure bugs mixed with code bugs
---
## CloudFormation Overview

- AWS-native IaC service
- `JSON` or `YAML` template format
- Managed state: AWS tracks the stack state for you
- Deep integration with all AWS services on day one
- No external tooling or state backend required
---
## CloudFormation Example

```yaml
Resources:
  WebServer:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-0c55b159cbfafe1f0
      InstanceType: t3.micro
      Tags:
        - Key: Name
          Value: web-server
Outputs:
  PublicIP:
    Value: !GetAtt WebServer.PublicIp
```

- AWS manages the stack lifecycle
- Rollback on failure is automatic
---
## CloudFormation Strengths and Weaknesses

- Strengths:
    - Zero state management burden: AWS handles it
    - Automatic rollback on deployment failure
    - `StackSets` for multi-account, multi-region deploys
- Weaknesses:
    - AWS-only: no multi-cloud support
    - Verbose `YAML`/`JSON` syntax for complex stacks
    - Limited support for complex logic or dynamic resources
    - Template size limits (51,200 bytes inline, 460,800 bytes in S3)
---
## Tool Comparison Matrix

| Criteria | `Terraform` | `Pulumi` | `CloudFormation` |
|----------|-----------|---------|----------------|
| Language | `HCL` | General-purpose | `YAML`/`JSON` |
| Multi-cloud | Yes | Yes | No (AWS only) |
| State mgmt | Self-managed | Self or managed | AWS-managed |
| Learning curve | Medium | Higher | Lower (AWS users) |
| Ecosystem | Very large | Growing | AWS-complete |
| Testing | Limited | Native | Limited |
---
## Choosing the Right Tool

- All-in on AWS? `CloudFormation` or `AWS CDK` may suffice
- Multi-cloud or hybrid? `Terraform` or `Pulumi`
- Developer-heavy team? `Pulumi` leverages existing skills
- Ops-heavy team? `Terraform` `HCL` is approachable
- Consider: team skills, cloud strategy, existing tooling
---
## State Management: The Core Challenge

![state_management_the_core_challenge](/svg/courses/devops/architectural-decisions-in-devops/05_infrastructure_as_code_decisions/state_management_the_core_challenge.svg)

---
## Remote State Backends

- Store state in a shared, durable location
- Common backends:
    - `AWS S3` + `DynamoDB` (locking)
    - `Azure Blob Storage`
    - `Google Cloud Storage`
    - `Terraform Cloud` / `HCP Terraform`
    - `Consul`, `PostgreSQL`
- Enables team collaboration on shared infrastructure
---
## Remote Backend Configuration

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/network/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

- Encryption at rest protects sensitive values
- `DynamoDB` table provides state locking
---
## State Locking and Collaboration

- Prevents concurrent modifications to the same state
- Without locking: race conditions corrupt state
- Lock acquired before `plan`/`apply`, released after
- Force-unlock available for stuck locks (use with caution)

```bash
terraform force-unlock LOCK_ID
```
---
## State Locking Flow

![state_locking_flow](/svg/courses/devops/architectural-decisions-in-devops/05_infrastructure_as_code_decisions/state_locking_flow.svg)

---
## State Per Environment vs Shared State

- **Per-environment state** (recommended):
    - Separate state files for `dev`, `staging`, `prod`
    - Blast radius limited to one environment
    - Independent apply cycles
- **Shared state**:
    - Single state across environments
    - Simpler to manage initially
    - Risky: one bad apply affects everything
---
## State Organization Patterns

```misc
state/
  dev/
    network/terraform.tfstate
    compute/terraform.tfstate
    database/terraform.tfstate
  staging/
    network/terraform.tfstate
    compute/terraform.tfstate
  prod/
    network/terraform.tfstate
    compute/terraform.tfstate
    database/terraform.tfstate
```

- Split by environment AND by component
- Each state file is independently lockable
---
## State Security Considerations

- State files contain sensitive data (passwords, keys, IPs)
- Encrypt state at rest and in transit
- Restrict access to state backend with IAM policies
- Avoid committing state files to version control
- Use `sensitive` flag on outputs to mask values

```hcl
output "db_password" {
  value     = aws_db_instance.main.password
  sensitive = true
}
```
---
## Reusable Modules: The Building Blocks

- Modules encapsulate a set of resources as a unit
- Accept input variables, expose outputs
- Published to registries or stored in `git` repos
- Enable consistent patterns across teams

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.0"
  cidr    = "10.0.0.0/16"
  azs     = ["us-east-1a", "us-east-1b"]
}
```
---
## Module Architecture

![module_architecture](/svg/courses/devops/architectural-decisions-in-devops/05_infrastructure_as_code_decisions/module_architecture.svg)

---
## Module Versioning Best Practices

- Pin module versions in production

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.1"
}
```

- Use `git` tags for internal modules
- Avoid pointing modules at `main` branch
- Test module upgrades in lower environments first
- Maintain a changelog for breaking changes
---
## Abstraction Layers and Platform Engineering

![abstraction_layers_and_platform_engineering](/svg/courses/devops/architectural-decisions-in-devops/05_infrastructure_as_code_decisions/abstraction_layers_and_platform_engineering.svg)

---
## Terragrunt: DRY Terraform

- Wrapper around Terraform to reduce repetition
- Manages remote state configuration automatically
- Supports dependency ordering between modules
- Generates backend and provider blocks

```hcl
terraform {
  source = "git::git@github.com:org/modules.git//vpc?ref=v1.2.0"
}
inputs = {
  cidr = "10.0.0.0/16"
  environment = "production"
}
```
---
## What is Configuration Drift?

- Drift occurs when real infrastructure diverges from IaC definitions
- Causes:
    - Manual changes via console or CLI
    - Hotfixes applied outside the IaC workflow
    - External automation modifying resources
    - Cloud provider auto-scaling or auto-updates
- Result: IaC no longer reflects reality
---
## Drift Detection Approaches

![drift_detection_approaches](/svg/courses/devops/architectural-decisions-in-devops/05_infrastructure_as_code_decisions/drift_detection_approaches.svg)

---
## Drift Detection Cycle

![drift_detection_cycle](/svg/courses/devops/architectural-decisions-in-devops/05_infrastructure_as_code_decisions/drift_detection_cycle.svg)

---
## Auto-Remediation: Benefits and Risks

- Benefits:
    - Automatically apply IaC state to fix drift
    - Eliminates human delay in responding to drift
    - Ensures compliance-critical resources stay configured
    - Pairs well with policy-as-code (`OPA`, `Sentinel`)
- Risks:
    - May revert intentional manual changes (emergency hotfixes)
    - Can cause outages if the IaC definition is wrong
    - Requires rock-solid IaC definitions and testing
---
## Preventing Drift in the First Place

1. Enforce IaC-only changes via `SCP` or IAM policies
1. Use `read-only` console access for most users
1. Tag manually created resources for review
1. Implement CI/CD pipelines for all infrastructure changes
1. Educate teams on the cost of manual modifications
---
## IaC Testing Strategies

- **Static analysis**: `tflint`, `checkov`, `tfsec`
- **Unit tests**: Validate module logic in isolation
- **Integration tests**: Deploy to ephemeral environment, verify, destroy
- **Policy tests**: `OPA` / `Sentinel` rules against plan output
- **Contract tests**: Verify module inputs and outputs

```bash
tflint --init && tflint
checkov -d .
```
---
## IaC in CI/CD Pipelines

```yaml
jobs:
  plan:
    steps:
      - uses: actions/checkout@v4
      - run: terraform init
      - run: terraform validate
      - run: terraform plan -out=tfplan
      - run: checkov -d .
  apply:
    needs: plan
    if: github.ref == 'refs/heads/main'
    steps:
      - run: terraform apply tfplan
```

- Plan on every PR; apply on merge to `main`
---
## Policy as Code

- Codify governance rules alongside infrastructure
- Tools: `HashiCorp Sentinel`, `Open Policy Agent` (`OPA`), `Kyverno`
- Enforce before apply (shift-left compliance)
- Examples of policies:
    - All S3 buckets must have encryption enabled
    - No public security group rules on port 22
    - All resources must have `owner` and `environment` tags
    - Instance types must be from an approved list
---
## Summary: Key IaC Decisions

![summary_key_iac_decisions](/svg/courses/devops/architectural-decisions-in-devops/05_infrastructure_as_code_decisions/summary_key_iac_decisions.svg)

---
## Recommended Reading

- "Terraform: Up and Running" by Yevgeniy Brikman
- "Infrastructure as Code" by Kief Morris (O'Reilly)
- HashiCorp Learn: [developer.hashicorp.com/terraform](https://developer.hashicorp.com/terraform)
- Pulumi documentation: [pulumi.com/docs](https://www.pulumi.com/docs/)
- `CloudFormation` User Guide on AWS documentation
- Gruntwork blog on IaC best practices
