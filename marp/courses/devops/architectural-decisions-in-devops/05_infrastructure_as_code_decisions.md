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

<svg viewBox="0 0 750 320" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="20" width="320" height="280" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="10"/>
  <text x="180" y="55" text-anchor="middle" font-size="18" font-weight="bold" fill="#1565c0">Declarative</text>
  <text x="180" y="90" text-anchor="middle" font-size="13">"What" the desired state is</text>
  <text x="180" y="120" text-anchor="middle" font-size="13">Tool figures out "how"</text>
  <text x="180" y="160" text-anchor="middle" font-size="13" font-weight="bold">Examples:</text>
  <text x="180" y="185" text-anchor="middle" font-size="13">Terraform, CloudFormation</text>
  <text x="180" y="210" text-anchor="middle" font-size="13">Kubernetes manifests</text>
  <text x="180" y="250" text-anchor="middle" font-size="12" fill="#555">Idempotent by design</text>
  <text x="180" y="275" text-anchor="middle" font-size="12" fill="#555">Convergent behavior</text>
  <rect x="410" y="20" width="320" height="280" fill="#fce4ec" stroke="#c62828" stroke-width="2" rx="10"/>
  <text x="570" y="55" text-anchor="middle" font-size="18" font-weight="bold" fill="#c62828">Imperative</text>
  <text x="570" y="90" text-anchor="middle" font-size="13">"How" to reach the state</text>
  <text x="570" y="120" text-anchor="middle" font-size="13">Step-by-step instructions</text>
  <text x="570" y="160" text-anchor="middle" font-size="13" font-weight="bold">Examples:</text>
  <text x="570" y="185" text-anchor="middle" font-size="13">Pulumi, AWS CDK</text>
  <text x="570" y="210" text-anchor="middle" font-size="13">Shell scripts, Ansible playbooks</text>
  <text x="570" y="250" text-anchor="middle" font-size="12" fill="#555">Full programming control</text>
  <text x="570" y="275" text-anchor="middle" font-size="12" fill="#555">Order-dependent execution</text>
</svg>
---
## Declarative vs Imperative Flow

<svg viewBox="0 0 750 300" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow1" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
  <text x="20" y="30" font-size="15" font-weight="bold" fill="#1565c0">Declarative</text>
  <rect x="20" y="45" width="130" height="40" fill="#bbdefb" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="85" y="70" text-anchor="middle" font-size="12">Desired State</text>
  <line x1="150" y1="65" x2="200" y2="65" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <rect x="200" y="45" width="130" height="40" fill="#bbdefb" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="265" y="70" text-anchor="middle" font-size="12">Diff Engine</text>
  <line x1="330" y1="65" x2="380" y2="65" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <rect x="380" y="45" width="130" height="40" fill="#bbdefb" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="445" y="70" text-anchor="middle" font-size="12">Execution Plan</text>
  <line x1="510" y1="65" x2="560" y2="65" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <rect x="560" y="45" width="150" height="40" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="635" y="70" text-anchor="middle" font-size="12">Infrastructure</text>
  <text x="20" y="150" font-size="15" font-weight="bold" fill="#c62828">Imperative</text>
  <rect x="20" y="165" width="130" height="40" fill="#ffcdd2" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="85" y="190" text-anchor="middle" font-size="12">Step 1: Create</text>
  <line x1="150" y1="185" x2="200" y2="185" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <rect x="200" y="165" width="130" height="40" fill="#ffcdd2" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="265" y="190" text-anchor="middle" font-size="12">Step 2: Configure</text>
  <line x1="330" y1="185" x2="380" y2="185" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <rect x="380" y="165" width="130" height="40" fill="#ffcdd2" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="445" y="190" text-anchor="middle" font-size="12">Step 3: Validate</text>
  <line x1="510" y1="185" x2="560" y2="185" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <rect x="560" y="165" width="150" height="40" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="635" y="190" text-anchor="middle" font-size="12">Infrastructure</text>
  <text x="375" y="260" text-anchor="middle" font-size="13" fill="#555">Both paths reach the same goal; different mental models</text>
</svg>
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

<svg viewBox="0 0 700 250" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow2" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="80" width="110" height="50" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="5"/>
  <text x="75" y="100" text-anchor="middle" font-size="12" font-weight="bold">Write</text>
  <text x="75" y="118" text-anchor="middle" font-size="11">.tf files</text>
  <line x1="130" y1="105" x2="170" y2="105" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <rect x="170" y="80" width="110" height="50" fill="#e1bee7" stroke="#7b1fa2" stroke-width="2" rx="5"/>
  <text x="225" y="100" text-anchor="middle" font-size="12" font-weight="bold">Init</text>
  <text x="225" y="118" text-anchor="middle" font-size="11">providers</text>
  <line x1="280" y1="105" x2="320" y2="105" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <rect x="320" y="80" width="110" height="50" fill="#bbdefb" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="375" y="100" text-anchor="middle" font-size="12" font-weight="bold">Plan</text>
  <text x="375" y="118" text-anchor="middle" font-size="11">diff state</text>
  <line x1="430" y1="105" x2="470" y2="105" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <rect x="470" y="80" width="110" height="50" fill="#ffccbc" stroke="#d84315" stroke-width="2" rx="5"/>
  <text x="525" y="100" text-anchor="middle" font-size="12" font-weight="bold">Apply</text>
  <text x="525" y="118" text-anchor="middle" font-size="11">execute</text>
  <line x1="580" y1="105" x2="620" y2="105" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <rect x="620" y="80" width="60" height="50" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="650" y="110" text-anchor="middle" font-size="12" font-weight="bold">Done</text>
  <text x="375" y="180" text-anchor="middle" font-size="13" fill="#555">State file updated after successful apply</text>
</svg>
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

<svg viewBox="0 0 700 280" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow3" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
  <rect x="250" y="20" width="200" height="50" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="8"/>
  <text x="350" y="50" text-anchor="middle" font-size="14" font-weight="bold">State File</text>
  <line x1="250" y1="45" x2="150" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <line x1="350" y1="70" x2="350" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <line x1="450" y1="45" x2="550" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <rect x="50" y="100" width="180" height="45" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="140" y="128" text-anchor="middle" font-size="12">Resource ID Mappings</text>
  <rect x="260" y="100" width="180" height="45" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="350" y="128" text-anchor="middle" font-size="12">Dependency Graph</text>
  <rect x="470" y="100" width="180" height="45" fill="#fce4ec" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="560" y="128" text-anchor="middle" font-size="12">Attribute Values</text>
  <text x="350" y="200" text-anchor="middle" font-size="13" fill="#555">State bridges desired config and real-world resources</text>
  <text x="350" y="225" text-anchor="middle" font-size="12" fill="#d32f2f">Corrupted or lost state = manual recovery required</text>
</svg>
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

<svg viewBox="0 0 700 280" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow4" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="40" width="100" height="40" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="70" y="65" text-anchor="middle" font-size="12">User A</text>
  <rect x="20" y="180" width="100" height="40" fill="#fce4ec" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="70" y="205" text-anchor="middle" font-size="12">User B</text>
  <rect x="250" y="40" width="120" height="40" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="5"/>
  <text x="310" y="65" text-anchor="middle" font-size="12">Acquire Lock</text>
  <rect x="250" y="180" width="120" height="40" fill="#ffcdd2" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="310" y="205" text-anchor="middle" font-size="12">Lock Denied</text>
  <rect x="450" y="40" width="120" height="40" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="510" y="55" text-anchor="middle" font-size="12">Apply +</text>
  <text x="510" y="72" text-anchor="middle" font-size="12">Release Lock</text>
  <rect x="450" y="180" width="120" height="40" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="510" y="205" text-anchor="middle" font-size="12">Retry: OK</text>
  <line x1="120" y1="60" x2="250" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arrow4)"/>
  <line x1="120" y1="200" x2="250" y2="200" stroke="#333" stroke-width="2" marker-end="url(#arrow4)"/>
  <line x1="370" y1="60" x2="450" y2="60" stroke="#2e7d32" stroke-width="2" marker-end="url(#arrow4)"/>
  <line x1="370" y1="200" x2="450" y2="200" stroke="#333" stroke-width="2" marker-end="url(#arrow4)"/>
  <line x1="510" y1="80" x2="510" y2="140" stroke="#999" stroke-width="1" stroke-dasharray="5,5"/>
  <text x="540" y="125" font-size="11" fill="#999">lock released</text>
</svg>
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

<svg viewBox="0 0 700 300" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow5" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
  <rect x="230" y="10" width="240" height="45" fill="#e8eaf6" stroke="#283593" stroke-width="2" rx="8"/>
  <text x="350" y="38" text-anchor="middle" font-size="14" font-weight="bold">Root Module (main.tf)</text>
  <line x1="280" y1="55" x2="140" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrow5)"/>
  <line x1="350" y1="55" x2="350" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrow5)"/>
  <line x1="420" y1="55" x2="560" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrow5)"/>
  <rect x="50" y="100" width="170" height="45" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="135" y="128" text-anchor="middle" font-size="12">module "network"</text>
  <rect x="265" y="100" width="170" height="45" fill="#bbdefb" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="350" y="128" text-anchor="middle" font-size="12">module "compute"</text>
  <rect x="480" y="100" width="170" height="45" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="5"/>
  <text x="565" y="128" text-anchor="middle" font-size="12">module "database"</text>
  <line x1="135" y1="145" x2="135" y2="185" stroke="#333" stroke-width="2" marker-end="url(#arrow5)"/>
  <line x1="350" y1="145" x2="350" y2="185" stroke="#333" stroke-width="2" marker-end="url(#arrow5)"/>
  <line x1="565" y1="145" x2="565" y2="185" stroke="#333" stroke-width="2" marker-end="url(#arrow5)"/>
  <rect x="50" y="185" width="170" height="35" fill="#f5f5f5" stroke="#888" stroke-width="1" rx="3"/>
  <text x="135" y="207" text-anchor="middle" font-size="11">VPC, Subnets, SGs</text>
  <rect x="265" y="185" width="170" height="35" fill="#f5f5f5" stroke="#888" stroke-width="1" rx="3"/>
  <text x="350" y="207" text-anchor="middle" font-size="11">EC2, ASG, ALB</text>
  <rect x="480" y="185" width="170" height="35" fill="#f5f5f5" stroke="#888" stroke-width="1" rx="3"/>
  <text x="565" y="207" text-anchor="middle" font-size="11">RDS, ElastiCache</text>
  <text x="350" y="265" text-anchor="middle" font-size="12" fill="#555">Modules pass outputs to each other via the root module</text>
</svg>
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

<svg viewBox="0 0 700 300" xmlns="http://www.w3.org/2000/svg">
  <rect x="150" y="10" width="400" height="40" fill="#e8eaf6" stroke="#283593" stroke-width="2" rx="8"/>
  <text x="350" y="35" text-anchor="middle" font-size="14" font-weight="bold">Developer Self-Service Portal</text>
  <rect x="150" y="70" width="400" height="40" fill="#c5cae9" stroke="#283593" stroke-width="2" rx="8"/>
  <text x="350" y="95" text-anchor="middle" font-size="13">Abstraction Layer (Terragrunt / Custom CLI)</text>
  <rect x="150" y="130" width="400" height="40" fill="#9fa8da" stroke="#283593" stroke-width="2" rx="8"/>
  <text x="350" y="155" text-anchor="middle" font-size="13">Validated Module Library</text>
  <rect x="150" y="190" width="400" height="40" fill="#7986cb" stroke="#283593" stroke-width="2" rx="8"/>
  <text x="350" y="215" text-anchor="middle" font-size="13" fill="#fff">IaC Engine (Terraform / Pulumi)</text>
  <rect x="150" y="250" width="400" height="40" fill="#5c6bc0" stroke="#283593" stroke-width="2" rx="8"/>
  <text x="350" y="275" text-anchor="middle" font-size="13" fill="#fff">Cloud Provider APIs</text>
  <text x="80" y="35" text-anchor="middle" font-size="11" fill="#555">Devs</text>
  <text x="80" y="95" text-anchor="middle" font-size="11" fill="#555">Platform</text>
  <text x="80" y="155" text-anchor="middle" font-size="11" fill="#555">Platform</text>
  <text x="80" y="215" text-anchor="middle" font-size="11" fill="#555">Engine</text>
  <text x="80" y="275" text-anchor="middle" font-size="11" fill="#555">Cloud</text>
</svg>
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

<svg viewBox="0 0 700 270" xmlns="http://www.w3.org/2000/svg">
  <text x="180" y="25" text-anchor="middle" font-size="15" font-weight="bold" fill="#1565c0">Continuous</text>
  <rect x="80" y="40" width="200" height="40" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="180" y="65" text-anchor="middle" font-size="12">Scheduled plan runs</text>
  <rect x="80" y="95" width="200" height="40" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="180" y="120" text-anchor="middle" font-size="12">Alert on any diff</text>
  <rect x="80" y="150" width="200" height="40" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="180" y="175" text-anchor="middle" font-size="12">Auto or manual remediate</text>
  <text x="520" y="25" text-anchor="middle" font-size="15" font-weight="bold" fill="#c62828">On-Demand</text>
  <rect x="420" y="40" width="200" height="40" fill="#fce4ec" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="520" y="65" text-anchor="middle" font-size="12">Manual plan before deploy</text>
  <rect x="420" y="95" width="200" height="40" fill="#fce4ec" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="520" y="120" text-anchor="middle" font-size="12">Drift found at apply time</text>
  <rect x="420" y="150" width="200" height="40" fill="#fce4ec" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="520" y="175" text-anchor="middle" font-size="12">Requires human judgment</text>
  <text x="350" y="240" text-anchor="middle" font-size="12" fill="#555">Continuous catches drift early; on-demand is simpler to operate</text>
</svg>
---
## Drift Detection Cycle

<svg viewBox="0 0 700 350" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow7" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
  <rect x="260" y="20" width="180" height="45" fill="#bbdefb" stroke="#1565c0" stroke-width="2" rx="8"/>
  <text x="350" y="48" text-anchor="middle" font-size="13" font-weight="bold">Scan Infrastructure</text>
  <line x1="440" y1="42" x2="530" y2="80" stroke="#333" stroke-width="2" marker-end="url(#arrow7)"/>
  <rect x="480" y="80" width="180" height="45" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="8"/>
  <text x="570" y="108" text-anchor="middle" font-size="13" font-weight="bold">Compare to State</text>
  <line x1="570" y1="125" x2="570" y2="170" stroke="#333" stroke-width="2" marker-end="url(#arrow7)"/>
  <rect x="480" y="170" width="180" height="45" fill="#ffccbc" stroke="#d84315" stroke-width="2" rx="8"/>
  <text x="570" y="198" text-anchor="middle" font-size="13" font-weight="bold">Drift Detected?</text>
  <line x1="570" y1="215" x2="570" y2="260" stroke="#333" stroke-width="2" marker-end="url(#arrow7)"/>
  <rect x="480" y="260" width="180" height="45" fill="#ffcdd2" stroke="#c62828" stroke-width="2" rx="8"/>
  <text x="570" y="288" text-anchor="middle" font-size="13" font-weight="bold">Alert / Remediate</text>
  <line x1="480" y1="282" x2="350" y2="282" stroke="#333" stroke-width="2" marker-end="url(#arrow7)"/>
  <rect x="170" y="260" width="180" height="45" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="8"/>
  <text x="260" y="288" text-anchor="middle" font-size="13" font-weight="bold">Update IaC / Apply</text>
  <line x1="260" y1="260" x2="310" y2="65" stroke="#333" stroke-width="2" marker-end="url(#arrow7)"/>
  <text x="350" y="340" text-anchor="middle" font-size="12" fill="#555">Continuous loop ensures infrastructure stays aligned with code</text>
</svg>
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

<svg viewBox="0 0 700 320" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="20" width="310" height="60" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="8"/>
  <text x="175" y="45" text-anchor="middle" font-size="13" font-weight="bold" fill="#1565c0">1. Paradigm</text>
  <text x="175" y="65" text-anchor="middle" font-size="11">Declarative vs Imperative</text>
  <rect x="370" y="20" width="310" height="60" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="8"/>
  <text x="525" y="45" text-anchor="middle" font-size="13" font-weight="bold" fill="#2e7d32">2. Tool</text>
  <text x="525" y="65" text-anchor="middle" font-size="11">Terraform vs Pulumi vs CloudFormation</text>
  <rect x="20" y="100" width="310" height="60" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="8"/>
  <text x="175" y="125" text-anchor="middle" font-size="13" font-weight="bold" fill="#f9a825">3. State Strategy</text>
  <text x="175" y="145" text-anchor="middle" font-size="11">Backend, locking, per-env split</text>
  <rect x="370" y="100" width="310" height="60" fill="#fce4ec" stroke="#c62828" stroke-width="2" rx="8"/>
  <text x="525" y="125" text-anchor="middle" font-size="13" font-weight="bold" fill="#c62828">4. Modularity</text>
  <text x="525" y="145" text-anchor="middle" font-size="11">Reusable modules vs inline</text>
  <rect x="20" y="180" width="310" height="60" fill="#e8eaf6" stroke="#283593" stroke-width="2" rx="8"/>
  <text x="175" y="205" text-anchor="middle" font-size="13" font-weight="bold" fill="#283593">5. Drift Management</text>
  <text x="175" y="225" text-anchor="middle" font-size="11">Continuous vs on-demand detection</text>
  <rect x="370" y="180" width="310" height="60" fill="#e0f2f1" stroke="#00695c" stroke-width="2" rx="8"/>
  <text x="525" y="205" text-anchor="middle" font-size="13" font-weight="bold" fill="#00695c">6. Governance</text>
  <text x="525" y="225" text-anchor="middle" font-size="11">Policy as code, testing, CI/CD</text>
  <text x="350" y="290" text-anchor="middle" font-size="13" fill="#555">Each decision shapes your IaC maturity and team velocity</text>
</svg>
---
## Recommended Reading

- "Terraform: Up and Running" by Yevgeniy Brikman
- "Infrastructure as Code" by Kief Morris (O'Reilly)
- HashiCorp Learn: [developer.hashicorp.com/terraform](https://developer.hashicorp.com/terraform)
- Pulumi documentation: [pulumi.com/docs](https://www.pulumi.com/docs/)
- `CloudFormation` User Guide on AWS documentation
- Gruntwork blog on IaC best practices
