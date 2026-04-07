# Variables

## Why Use Variables?

- Make configurations reusable and flexible
- Avoid hardcoding values
- Enable environment-specific deployments
- Support team collaboration
- Allow parameterized modules

---

## Variable Declaration Syntax

```hcl
variable "name" {
  description = "Description of the variable"
  type        = string
  default     = "default_value"
  sensitive   = false
  nullable    = true

  validation {
    condition     = length(var.name) > 0
    error_message = "Name must not be empty."
  }
}
```

---

## Variable Types

| Type | Example | Description |
|------|---------|-------------|
| `string` | `"hello"` | Text |
| `number` | `42` | Numeric |
| `bool` | `true` | Boolean |
| `list(type)` | `["a", "b"]` | Ordered collection |
| `set(type)` | `toset(["a", "b"])` | Unique unordered |
| `map(type)` | `{k = "v"}` | Key-value pairs |
| `object({})` | Complex structure | Named attributes |
| `tuple([])` | Mixed list | Typed elements |

---

## String Variables

```hcl
variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "myapp"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
}

resource "aws_instance" "web" {
  tags = {
    Name = "${var.project_name}-${var.environment}"
  }
  # ...
}
```

---

## Number Variables

```hcl
variable "instance_count" {
  description = "Number of instances to create"
  type        = number
  default     = 2
}

variable "disk_size_gb" {
  description = "Root disk size in GB"
  type        = number
  default     = 50
}

resource "aws_instance" "web" {
  count = var.instance_count

  root_block_device {
    volume_size = var.disk_size_gb
  }
  # ...
}
```

---

## Boolean Variables

```hcl
variable "enable_monitoring" {
  description = "Enable detailed monitoring"
  type        = bool
  default     = false
}

variable "create_dns_record" {
  description = "Whether to create a DNS record"
  type        = bool
  default     = true
}

resource "aws_instance" "web" {
  monitoring = var.enable_monitoring
  # ...
}
```

---

## List Variables

```hcl
variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

resource "aws_subnet" "public" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index)
  availability_zone = var.availability_zones[count.index]
}
```

---

## Map Variables

```hcl
variable "instance_types" {
  description = "Instance types per environment"
  type        = map(string)
  default = {
    dev     = "t3.micro"
    staging = "t3.small"
    prod    = "t3.large"
  }
}

resource "aws_instance" "web" {
  instance_type = var.instance_types[var.environment]
  # ...
}
```

---

## Object Variables

```hcl
variable "database_config" {
  description = "Database configuration"
  type = object({
    engine         = string
    instance_class = string
    storage_gb     = number
    multi_az       = bool
    backup_days    = number
  })
  default = {
    engine         = "mysql"
    instance_class = "db.t3.micro"
    storage_gb     = 20
    multi_az       = false
    backup_days    = 7
  }
}
```

---

## Using Object Variables

```hcl
resource "aws_db_instance" "main" {
  engine              = var.database_config.engine
  instance_class      = var.database_config.instance_class
  allocated_storage   = var.database_config.storage_gb
  multi_az            = var.database_config.multi_az
  backup_retention_period = var.database_config.backup_days

  # ...
}
```

---

## Tuple Variables

```hcl
variable "rule" {
  description = "Security group rule"
  type        = tuple([string, number, number, string])
  default     = ["tcp", 80, 80, "0.0.0.0/0"]
}

resource "aws_security_group_rule" "example" {
  type        = "ingress"
  protocol    = var.rule[0]
  from_port   = var.rule[1]
  to_port     = var.rule[2]
  cidr_blocks = [var.rule[3]]
  # ...
}
```

---

## Complex Variable Types

```hcl
variable "servers" {
  description = "Server configurations"
  type = list(object({
    name          = string
    instance_type = string
    subnet_id     = string
    tags          = map(string)
  }))
  default = [
    {
      name          = "web"
      instance_type = "t3.micro"
      subnet_id     = "subnet-123"
      tags          = { Role = "frontend" }
    }
  ]
}
```

---

## Variable Validation

```hcl
variable "environment" {
  description = "Deployment environment"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "instance_type" {
  type = string

  validation {
    condition     = can(regex("^t3\\.", var.instance_type))
    error_message = "Only t3 instance types are allowed."
  }
}
```

---

## Multiple Validation Rules

```hcl
variable "cidr_block" {
  description = "CIDR block for the VPC"
  type        = string

  validation {
    condition     = can(cidrhost(var.cidr_block, 0))
    error_message = "Must be a valid CIDR block."
  }

  validation {
    condition     = tonumber(split("/", var.cidr_block)[1]) <= 24
    error_message = "CIDR prefix must be /24 or larger."
  }
}
```

---

## Setting Variables: Precedence Order

![setting_variables_precedence_order](/svg/courses/devops/terraform/05_variables/setting_variables_precedence_order.svg)

---

## Setting Variables via CLI

```bash
# Single variable
terraform apply -var="instance_type=t3.large"

# Multiple variables
terraform apply \
  -var="instance_type=t3.large" \
  -var="environment=prod" \
  -var="instance_count=5"

# Complex types
terraform apply -var='availability_zones=["us-east-1a","us-east-1b"]'

# Map
terraform apply -var='tags={Name="web",Env="prod"}'
```

---

## Setting Variables via .tfvars Files

```hcl
# terraform.tfvars (auto-loaded)
project_name   = "webapp"
environment    = "staging"
instance_count = 3
instance_type  = "t3.small"

availability_zones = [
  "us-east-1a",
  "us-east-1b",
]

tags = {
  Team   = "platform"
  Owner  = "devops"
}
```

---

## Variable File Naming

```misc
Auto-loaded files:
  terraform.tfvars          # Always loaded
  terraform.tfvars.json     # Always loaded
  *.auto.tfvars             # Always loaded (alphabetical)
  *.auto.tfvars.json        # Always loaded

Manually loaded:
  terraform apply -var-file="prod.tfvars"
  terraform apply -var-file="environments/staging.tfvars"
```

---

## Setting Variables via Environment Variables

```bash
# Prefix with TF_VAR_
export TF_VAR_instance_type="t3.large"
export TF_VAR_environment="production"
export TF_VAR_instance_count=5

# Complex types as JSON
export TF_VAR_tags='{"Name":"web","Env":"prod"}'
export TF_VAR_availability_zones='["us-east-1a","us-east-1b"]'

# Then run normally
terraform apply
```

---

## Environment Variables for Secrets

```bash
# Store sensitive values in environment
export TF_VAR_db_password="super-secret-password"
export TF_VAR_api_key="sk-1234567890"

# These will NOT appear in .tfvars files
# and will NOT be committed to version control
```

```hcl
variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}
```

---

## Sensitive Variables

```hcl
variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

resource "aws_db_instance" "main" {
  password = var.db_password
  # ...
}
```

```output
# terraform plan output:
  + resource "aws_db_instance" "main" {
      + password = (sensitive value)
    }
```

---

## Sensitive Output Handling

```hcl
output "db_password" {
  value     = var.db_password
  sensitive = true
}
```

```bash
# Will show:
# db_password = <sensitive>

# To see the value:
terraform output -raw db_password
terraform output -json
```

---

## Local Values

```hcl
locals {
  project_prefix = "${var.project}-${var.environment}"

  common_tags = {
    Project     = var.project
    Environment = var.environment
    ManagedBy   = "Terraform"
    Team        = var.team
  }

  is_production = var.environment == "prod"
}

resource "aws_instance" "web" {
  instance_type = local.is_production ? "t3.large" : "t3.micro"
  tags          = merge(local.common_tags, { Name = "${local.project_prefix}-web" })
  # ...
}
```

---

## locals vs variables

| Feature | `variable` | `locals` |
|---------|-----------|----------|
| Set by | User/caller | Internal computation |
| Scope | Module input | Within module only |
| Reusable | Across modules | Within declaring module |
| Purpose | External input | Computed values |
| Reference | `var.name` | `local.name` |

---

## Variable Best Practices

- Always add `description` to variables
- Use `type` constraints for all variables
- Add `validation` blocks for critical inputs
- Mark secrets as `sensitive = true`
- Provide sensible `default` values when possible
- Use `locals` for computed values, not variables
- Keep variable names consistent across modules

---

## Organizing Variables by File

```tree
variables.tf          # All variable declarations
├── General variables (project, environment, region)
├── Networking variables (VPC, subnets, CIDRs)
├── Compute variables (instance types, counts)
└── Database variables (engine, size, backups)

terraform.tfvars      # Default values
dev.tfvars            # Dev environment overrides
staging.tfvars        # Staging environment overrides
prod.tfvars           # Production environment overrides
```

---

## Chapter Summary

- Variables make Terraform configurations reusable and flexible
- Types include `string`, `number`, `bool`, `list`, `map`, `object`, `tuple`
- Set variables via CLI flags, `.tfvars` files, or environment variables
- Precedence: CLI > `-var-file` > `.auto.tfvars` > `terraform.tfvars` > env vars > defaults
- Use `validation` blocks to enforce constraints
- Mark sensitive data with `sensitive = true`
- Use `locals` for internal computed values
- Always add descriptions and type constraints
