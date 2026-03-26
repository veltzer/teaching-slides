# Reuse Patterns

## Why Reuse?

- Avoid duplicating configuration across environments
- Maintain consistency between dev, staging, and production
- Reduce errors from copy-paste
- Enable team collaboration through shared components
- Follow DRY (Don't Repeat Yourself) principle

---

## Reuse Strategies in Terraform

```txt
+------------------+     +------------------+
| Workspaces       |     | Modules          |
| Same config,     |     | Reusable config  |
| different state  |     | components       |
+------------------+     +------------------+

+------------------+     +------------------+
| Outputs          |     | Remote State     |
| Export values    |     | Cross-project    |
| from configs     |     | data sharing     |
+------------------+     +------------------+
```

---

## Terraform Workspaces

- Allow multiple state files for the same configuration
- Each workspace has its own state
- Default workspace is named `default`
- Useful for managing multiple environments

---

## Workspace Commands

```bash
# List all workspaces
terraform workspace list

# Create a new workspace
terraform workspace new staging

# Switch to a workspace
terraform workspace select staging

# Show current workspace
terraform workspace show

# Delete a workspace
terraform workspace delete staging
```

---

## Using Workspaces in Configuration

```hcl
locals {
  env_config = {
    default = {
      instance_type  = "t3.micro"
      instance_count = 1
    }
    staging = {
      instance_type  = "t3.small"
      instance_count = 2
    }
    production = {
      instance_type  = "t3.large"
      instance_count = 4
    }
  }

  config = local.env_config[terraform.workspace]
}
```

---

## Workspace-Based Resource Naming

```hcl
resource "aws_instance" "web" {
  count         = local.config.instance_count
  instance_type = local.config.instance_type
  ami           = data.aws_ami.ubuntu.id

  tags = {
    Name        = "web-${terraform.workspace}-${count.index}"
    Environment = terraform.workspace
  }
}
```

---

## Workspaces with Remote Backend

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "app/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"

    # State stored as:
    # env:/staging/app/terraform.tfstate
    # env:/production/app/terraform.tfstate
  }
}
```

---

## Workspace Limitations

- All environments share the same configuration code
- Cannot have different providers per workspace
- Cannot have different resources per workspace (easily)
- Risk of applying to wrong workspace
- Better for simple environment differences

```bash
# Always verify workspace before apply
terraform workspace show
terraform plan
terraform apply
```

---

## Outputs

```hcl
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = aws_subnet.public[*].id
}

output "db_endpoint" {
  description = "Database connection endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}
```

---

## Output Uses

```bash
# View all outputs
terraform output

# Get specific output
terraform output vpc_id

# Get raw value (no quotes)
terraform output -raw vpc_id

# Get JSON format
terraform output -json

# Use in scripts
VPC_ID=$(terraform output -raw vpc_id)
echo "VPC is: $VPC_ID"
```

---

## Consuming Outputs via Remote State

```hcl
# In the networking project
output "vpc_id" {
  value = aws_vpc.main.id
}

# In the compute project
data "terraform_remote_state" "network" {
  backend = "s3"
  config = {
    bucket = "my-terraform-state"
    key    = "network/terraform.tfstate"
    region = "us-east-1"
  }
}

resource "aws_instance" "web" {
  subnet_id = data.terraform_remote_state.network.outputs.subnet_id
  # ...
}
```

---

## What are Modules?

- A module is a container for related Terraform resources
- Any directory with `.tf` files is a module
- The root module is your working directory
- Child modules are called from the root module
- Modules accept inputs (variables) and produce outputs

---

## Module Structure

```txt
modules/vpc/
├── main.tf         # Resources
├── variables.tf    # Input variables
├── outputs.tf      # Output values
└── README.md       # Documentation

modules/ec2/
├── main.tf
├── variables.tf
└── outputs.tf
```

---

## Creating a Module

```hcl
# modules/vpc/variables.tf
variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "name" {
  description = "Name prefix for resources"
  type        = string
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
}
```

---

## Module Resources

```hcl
# modules/vpc/main.tf
resource "aws_vpc" "this" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true

  tags = {
    Name = "${var.name}-vpc"
  }
}

resource "aws_subnet" "public" {
  count      = length(var.public_subnet_cidrs)
  vpc_id     = aws_vpc.this.id
  cidr_block = var.public_subnet_cidrs[count.index]

  tags = {
    Name = "${var.name}-public-${count.index}"
  }
}
```

---

## Module Outputs

```hcl
# modules/vpc/outputs.tf
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.this.id
}

output "public_subnet_ids" {
  description = "IDs of public subnets"
  value       = aws_subnet.public[*].id
}

output "vpc_cidr_block" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.this.cidr_block
}
```

---

## Using a Module

```hcl
# root main.tf
module "vpc" {
  source = "./modules/vpc"

  name                = "myapp"
  vpc_cidr            = "10.0.0.0/16"
  public_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24"]
}

# Reference module outputs
resource "aws_instance" "web" {
  subnet_id = module.vpc.public_subnet_ids[0]
  # ...
}

output "vpc_id" {
  value = module.vpc.vpc_id
}
```

---

## Module Sources

```hcl
# Local path
module "vpc" {
  source = "./modules/vpc"
}

# Terraform Registry
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"
}

# GitHub
module "vpc" {
  source = "github.com/org/repo//modules/vpc?ref=v1.0.0"
}

# S3 bucket
module "vpc" {
  source = "s3::https://bucket.s3.amazonaws.com/vpc.zip"
}
```

---

## Module Versioning

```hcl
# Pin to specific version
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.2"
}

# Allow patch updates
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.1.0"
}

# Allow minor updates
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"
}
```

---

## Terraform Registry

```txt
registry.terraform.io
├── Providers
│   ├── hashicorp/aws
│   ├── hashicorp/azurerm
│   └── hashicorp/google
└── Modules
    ├── terraform-aws-modules/vpc/aws
    ├── terraform-aws-modules/ec2-instance/aws
    ├── terraform-aws-modules/s3-bucket/aws
    └── terraform-aws-modules/rds/aws
```

- Official and community modules
- Versioned releases
- Documentation and examples
- Quality ratings

---

## Using Registry Modules

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "my-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true
}
```

---

## Module Composition

```hcl
module "vpc" {
  source = "./modules/vpc"
  # ...
}

module "security" {
  source = "./modules/security"
  vpc_id = module.vpc.vpc_id
}

module "compute" {
  source     = "./modules/compute"
  subnet_ids = module.vpc.public_subnet_ids
  sg_ids     = [module.security.web_sg_id]
}

module "database" {
  source     = "./modules/database"
  subnet_ids = module.vpc.private_subnet_ids
  sg_ids     = [module.security.db_sg_id]
}
```

---

## Module Composition Diagram

```txt
+----------------+
|  Root Module   |
+-------+--------+
        |
   +----+----+----+--------+
   |         |    |        |
   v         v    v        v
+-----+ +----+ +---+ +--------+
| VPC | | SG | |EC2| |  RDS   |
+-----+ +----+ +---+ +--------+
   |         |    ^        ^
   |         |    |        |
   +---------+----+--------+
     (outputs flow between modules)
```

---

## Multiple Module Instances

```hcl
module "web_servers" {
  source        = "./modules/ec2"
  instance_type = "t3.micro"
  count         = 3
  name          = "web-${count.index}"
}

# Or with for_each
module "services" {
  for_each = {
    api    = "t3.small"
    worker = "t3.medium"
    cache  = "t3.large"
  }
  source        = "./modules/ec2"
  instance_type = each.value
  name          = each.key
}
```

---

## Module Best Practices

- Keep modules focused on a single responsibility
- Use clear, descriptive variable and output names
- Always add `description` to variables and outputs
- Pin module versions with `version` constraint
- Document modules with a `README.md`
- Use consistent naming conventions
- Keep modules generic and reusable
- Avoid hardcoding values inside modules

---

## Private Module Registry

```txt
Options for sharing modules privately:

1. Git repositories (GitHub, GitLab, Bitbucket)
   source = "git::https://gitlab.com/org/module.git"

2. S3/GCS buckets
   source = "s3::https://bucket.s3.amazonaws.com/module.zip"

3. Terraform Cloud/Enterprise Private Registry
   source = "app.terraform.io/org/module/provider"

4. Local file paths (monorepo)
   source = "../shared-modules/vpc"
```

---

## Chapter Summary

- Workspaces allow multiple states for the same configuration
- Outputs export values from configurations for use elsewhere
- Remote state enables cross-project data sharing
- Modules are reusable containers of Terraform resources
- Modules accept variables as inputs and expose outputs
- Source modules from local paths, registries, or git repos
- Always version your module dependencies
- Compose modules together for complex architectures
