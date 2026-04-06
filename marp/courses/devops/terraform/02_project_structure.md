# Project Structure

## Terraform File Types

| Extension | Purpose |
|-----------|---------|
| `.tf` | Main configuration files |
| `.tfvars` | Variable value definitions |
| `.tfstate` | State file (auto-generated) |
| `.tfstate.backup` | Previous state backup |
| `.terraform.lock.hcl` | Dependency lock file |
| `.terraformrc` | CLI configuration |

---

## Standard Project Layout

```tree
my-project/
├── main.tf           # Primary resources
├── variables.tf      # Input variable declarations
├── outputs.tf        # Output value declarations
├── providers.tf      # Provider configuration
├── terraform.tfvars  # Variable values
├── versions.tf       # Version constraints
├── .terraform/       # Provider plugins (auto)
├── .terraform.lock.hcl  # Lock file (auto)
└── terraform.tfstate # State file (auto)
```

---

## The main.tf File

```hcl
# main.tf - Primary resource definitions

resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr

  tags = {
    Name = "${var.project}-vpc"
  }
}

resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.main.id
  cidr_block = var.subnet_cidr

  tags = {
    Name = "${var.project}-subnet"
  }
}
```

---

## The variables.tf File

```hcl
# variables.tf - Input variable declarations

variable "project" {
  description = "Project name"
  type        = string
  default     = "myapp"
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_cidr" {
  description = "Subnet CIDR block"
  type        = string
}
```

---

## The outputs.tf File

```hcl
# outputs.tf - Values to display after apply

output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.main.id
}

output "subnet_id" {
  description = "The ID of the public subnet"
  value       = aws_subnet.public.id
}

output "vpc_cidr" {
  description = "The CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}
```

---

## The providers.tf File

```hcl
# providers.tf - Provider configuration

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project   = var.project
      ManagedBy = "Terraform"
    }
  }
}
```

---

## The versions.tf File

```hcl
# versions.tf - Version constraints

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}
```

---

## The terraform.tfvars File

```hcl
# terraform.tfvars - Variable values

project     = "webapp"
aws_region  = "us-east-1"
vpc_cidr    = "10.0.0.0/16"
subnet_cidr = "10.0.1.0/24"
environment = "staging"
```

- Automatically loaded by Terraform
- Do not commit sensitive values to version control
- Use `.tfvars` files per environment

---

## Multiple Variable Files

```tree
my-project/
├── main.tf
├── variables.tf
├── environments/
│   ├── dev.tfvars
│   ├── staging.tfvars
│   └── prod.tfvars
```

```bash
# Specify variable file explicitly
terraform plan -var-file="environments/dev.tfvars"
terraform apply -var-file="environments/prod.tfvars"
```

---

## The .terraform Directory

```tree
.terraform/
├── providers/
│   └── registry.terraform.io/
│       └── hashicorp/
│           └── aws/
│               └── 5.30.0/
│                   └── linux_amd64/
│                       └── terraform-provider-aws_v5.30.0
└── modules/
    └── modules.json
```

- Created by `terraform init`
- Contains downloaded provider plugins
- Should be in `.gitignore`

---

## The .gitignore File for Terraform

```gitignore
# Local .terraform directories
**/.terraform/*

# .tfstate files
*.tfstate
*.tfstate.*

# Crash log files
crash.log
crash.*.log

# Variable files with secrets
*.tfvars
!example.tfvars

# Override files
override.tf
override.tf.json
*_override.tf
*_override.tf.json

# CLI configuration
.terraformrc
terraform.rc
```

---

## The Lock File

```hcl
# .terraform.lock.hcl (auto-generated)

provider "registry.terraform.io/hashicorp/aws" {
  version     = "5.30.0"
  constraints = "~> 5.0"
  hashes = [
    "h1:abc123...",
    "zh:def456...",
  ]
}
```

- Ensures consistent provider versions across teams
- Should be committed to version control
- Updated with `terraform init -upgrade`

---

## terraform init Deep Dive

```bash
# Basic initialization
terraform init

# Upgrade providers to latest allowed versions
terraform init -upgrade

# Reconfigure backend
terraform init -reconfigure

# Migrate state to new backend
terraform init -migrate-state

# Use a plugin cache directory
terraform init -plugin-dir=/path/to/plugins
```

---

## terraform init Workflow

<svg xmlns="http://www.w3.org/2000/svg" width="480" height="380">
  <defs>
    <marker id="arr" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
    </marker>
  </defs>
  <!-- terraform init -->
  <rect x="160" y="10" width="160" height="40" rx="4" fill="#7b1fa2" stroke="#333" stroke-width="1.5"/>
  <text x="240" y="35" font-family="monospace" font-size="14" font-weight="bold" fill="#fff" text-anchor="middle">terraform init</text>
  <!-- vertical trunk -->
  <line x1="240" y1="50" x2="240" y2="70" stroke="#555" stroke-width="1.5"/>

  <!-- Branch: Configure backend -->
  <line x1="240" y1="70" x2="240" y2="90" stroke="#555" stroke-width="1.5"/>
  <line x1="240" y1="80" x2="100" y2="80" stroke="#555" stroke-width="1.5"/>
  <line x1="100" y1="80" x2="100" y2="100" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="10" y="100" width="180" height="36" rx="4" fill="#f0f4f8" stroke="#555" stroke-width="1.5"/>
  <text x="100" y="123" font-family="sans-serif" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">Configure backend</text>
  <line x1="100" y1="136" x2="100" y2="156" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="10" y="156" width="180" height="36" rx="4" fill="#fff3e0" stroke="#aaa" stroke-width="1"/>
  <text x="100" y="179" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">Local or remote state</text>

  <!-- Branch: Download providers -->
  <line x1="240" y1="80" x2="240" y2="100" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="160" y="100" width="160" height="36" rx="4" fill="#f0f4f8" stroke="#555" stroke-width="1.5"/>
  <text x="240" y="123" font-family="sans-serif" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">Download providers</text>
  <line x1="240" y1="136" x2="240" y2="156" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="160" y="156" width="160" height="36" rx="4" fill="#fff3e0" stroke="#aaa" stroke-width="1"/>
  <text x="240" y="172" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">Check version constraints</text>
  <line x1="240" y1="192" x2="240" y2="212" stroke="#555" stroke-width="1.5"/>
  <rect x="160" y="212" width="160" height="36" rx="4" fill="#fff3e0" stroke="#aaa" stroke-width="1"/>
  <text x="240" y="235" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">Download from registry</text>
  <line x1="240" y1="248" x2="240" y2="268" stroke="#555" stroke-width="1.5"/>
  <rect x="160" y="268" width="160" height="36" rx="4" fill="#fff3e0" stroke="#aaa" stroke-width="1"/>
  <text x="240" y="291" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">Verify checksums</text>

  <!-- Branch: Download modules -->
  <line x1="240" y1="80" x2="380" y2="80" stroke="#555" stroke-width="1.5"/>
  <line x1="380" y1="80" x2="380" y2="100" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="300" y="100" width="170" height="36" rx="4" fill="#f0f4f8" stroke="#555" stroke-width="1.5"/>
  <text x="385" y="123" font-family="sans-serif" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">Download modules</text>
  <line x1="385" y1="136" x2="385" y2="156" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="300" y="156" width="170" height="36" rx="4" fill="#fff3e0" stroke="#aaa" stroke-width="1"/>
  <text x="385" y="179" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">From registry or git</text>

  <!-- Create lock file -->
  <line x1="240" y1="304" x2="240" y2="328" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="150" y="328" width="180" height="36" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="240" y="351" font-family="sans-serif" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">Create lock file</text>
</svg>

---

## terraform plan Deep Dive

```bash
# Basic plan
terraform plan

# Save plan to a file
terraform plan -out=tfplan

# Plan for destroy
terraform plan -destroy

# Target specific resources
terraform plan -target=aws_instance.web

# Set variables inline
terraform plan -var="instance_type=t3.large"

# Refresh-only mode
terraform plan -refresh-only
```

---

## Reading a Plan Output

```output
Terraform will perform the following actions:

  # aws_instance.web will be created
  + resource "aws_instance" "web" {
      + ami                    = "ami-0c55b159cbfafe1f0"
      + instance_type          = "t3.micro"
      + id                     = (known after apply)
      + public_ip              = (known after apply)
      + tags                   = {
          + "Name" = "web-server"
        }
    }

Plan: 1 to add, 0 to change, 0 to destroy.
```

---

## terraform apply Deep Dive

```bash
# Apply with interactive confirmation
terraform apply

# Apply a saved plan (no confirmation needed)
terraform apply tfplan

# Auto-approve (skip confirmation)
terraform apply -auto-approve

# Apply with specific variable file
terraform apply -var-file="prod.tfvars"

# Target specific resource
terraform apply -target=aws_instance.web

# Set parallelism
terraform apply -parallelism=20
```

---

## terraform apply Workflow

<svg xmlns="http://www.w3.org/2000/svg" width="400" height="440">
  <defs>
    <marker id="arr" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
    </marker>
  </defs>
  <!-- terraform apply header -->
  <rect x="100" y="10" width="200" height="40" rx="4" fill="#7b1fa2" stroke="#333" stroke-width="1.5"/>
  <text x="200" y="35" font-family="monospace" font-size="14" font-weight="bold" fill="#fff" text-anchor="middle">terraform apply</text>

  <!-- steps -->
  <line x1="200" y1="50" x2="200" y2="70" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="60" y="70" width="280" height="36" rx="4" fill="#f0f4f8" stroke="#555" stroke-width="1.5"/>
  <text x="200" y="93" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Read current state</text>

  <line x1="200" y1="106" x2="200" y2="126" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="60" y="126" width="280" height="36" rx="4" fill="#f0f4f8" stroke="#555" stroke-width="1.5"/>
  <text x="200" y="149" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Compare config vs state</text>

  <line x1="200" y1="162" x2="200" y2="182" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="60" y="182" width="280" height="36" rx="4" fill="#f0f4f8" stroke="#555" stroke-width="1.5"/>
  <text x="200" y="205" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Generate execution plan</text>

  <line x1="200" y1="218" x2="200" y2="238" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="60" y="238" width="280" height="36" rx="4" fill="#f0f4f8" stroke="#555" stroke-width="1.5"/>
  <text x="200" y="261" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Show plan to user</text>

  <line x1="200" y1="274" x2="200" y2="294" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="60" y="294" width="280" height="36" rx="4" fill="#fff3e0" stroke="#555" stroke-width="1.5"/>
  <text x="200" y="317" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Wait for confirmation</text>

  <line x1="200" y1="330" x2="200" y2="350" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="60" y="350" width="280" height="36" rx="4" fill="#e3f2fd" stroke="#555" stroke-width="1.5"/>
  <text x="200" y="373" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Create / modify / delete resources</text>

  <line x1="200" y1="386" x2="200" y2="406" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="60" y="406" width="280" height="36" rx="4" fill="#e8f5e9" stroke="#555" stroke-width="1.5"/>
  <text x="200" y="429" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Update state file → Show outputs</text>
</svg>

---

## terraform destroy Deep Dive

```bash
# Destroy all resources
terraform destroy

# Auto-approve destruction
terraform destroy -auto-approve

# Destroy specific resource only
terraform destroy -target=aws_instance.web

# Preview what will be destroyed
terraform plan -destroy
```

- Destroys resources in correct dependency order
- Removes resources from state after deletion
- Irreversible operation - use with caution

---

## Splitting Configuration into Files

```tree
large-project/
├── main.tf           # Core resources
├── networking.tf     # VPC, subnets, routes
├── security.tf       # Security groups, IAM
├── compute.tf        # EC2 instances, ASGs
├── storage.tf        # S3, EBS, EFS
├── database.tf       # RDS, DynamoDB
├── dns.tf            # Route53 records
├── variables.tf      # All variable declarations
├── outputs.tf        # All outputs
└── providers.tf      # Provider config
```

---

## Multi-Environment Structure

```tree
infrastructure/
├── modules/
│   ├── vpc/
│   ├── compute/
│   └── database/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   └── prod/
│       ├── main.tf
│       ├── variables.tf
│       └── terraform.tfvars
```

---

## Override Files

```hcl
# override.tf - Overrides values in main config

# Original in main.tf:
# resource "aws_instance" "web" {
#   instance_type = "t3.micro"
# }

# Override for local testing:
resource "aws_instance" "web" {
  instance_type = "t3.nano"
}
```

- Files named `override.tf` or `*_override.tf` are special
- They merge with the main configuration
- Useful for local development overrides

---

## terraform show

```bash
# Show current state in human-readable format
terraform show

# Show a saved plan
terraform show tfplan

# Output as JSON
terraform show -json
terraform show -json tfplan
```

- Displays the current state of managed resources
- Useful for debugging and inspection

---

## terraform output

```bash
# Show all outputs
terraform output

# Show specific output
terraform output vpc_id

# Show as JSON
terraform output -json

# Show raw value (no quotes)
terraform output -raw vpc_id
```

---

## terraform graph

```bash
# Generate dependency graph in DOT format
terraform graph

# Save and convert to image
terraform graph | dot -Tpng > graph.png

# Filter by type
terraform graph -type=plan
terraform graph -type=apply
```

- Generates a visual representation of resource dependencies
- Uses GraphViz DOT format
- Helps understand resource ordering

---

## Resource Dependencies in Graph

```output
terraform graph output:

digraph {
  "[root] aws_vpc.main"
    -> "[root] provider.aws"

  "[root] aws_subnet.public"
    -> "[root] aws_vpc.main"

  "[root] aws_instance.web"
    -> "[root] aws_subnet.public"
    -> "[root] aws_security_group.web"
}
```

---

## terraform console

```bash
# Start interactive console
terraform console

# Try expressions
> 1 + 2
3
> "hello, ${"world"}"
hello, world
> max(5, 12, 9)
12
> cidrsubnet("10.0.0.0/16", 8, 1)
10.0.1.0/24
```

- Interactive environment for testing expressions
- Has access to state and variables

---

## Chapter Summary

- Standard project uses `main.tf`, `variables.tf`, `outputs.tf`, `providers.tf`
- The `.terraform` directory holds downloaded plugins (add to `.gitignore`)
- The `.terraform.lock.hcl` file should be committed to version control
- `terraform init` downloads providers and configures the backend
- `terraform plan` previews changes without modifying anything
- `terraform apply` creates, updates, or deletes resources
- `terraform destroy` removes all managed resources
- Split large configurations across multiple `.tf` files
