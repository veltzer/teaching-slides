# Introduction to Terraform

## Course Overview
- 3-day comprehensive `Terraform` training
- Day 1: Fundamentals, project structure, resources, data sources, variables, state
- Day 2: Reuse patterns, drift management, security, functions
- Day 3: Building infrastructure, provisioners, debugging, Packer

---

## What is Infrastructure as Code (IaC)?

- Managing infrastructure through code instead of manual processes
- Infrastructure is described in definition files
- Files can be versioned, shared, and reused
- Enables automation, consistency, and repeatability
- Reduces human error and configuration drift

---

## IaC Benefits

- **Version Control**: Track changes over time with `git`
- **Collaboration**: Teams can review infrastructure changes
- **Repeatability**: Deploy identical environments every time
- **Speed**: Provision infrastructure in minutes, not days
- **Documentation**: Code serves as living documentation
- **Cost Management**: Easily tear down unused resources

---

## IaC Approaches

| Approach | Description | Tools |
|----------|-------------|-------|
| Declarative | Define desired state | `Terraform`, `CloudFormation` |
| Imperative | Define exact steps | `Ansible`, scripts |
| Mutable | Modify existing resources | `Ansible`, `Chef` |
| Immutable | Replace resources entirely | `Terraform`, `Packer` |

---

## What is Terraform?

- Open-source IaC tool by HashiCorp
- Uses declarative configuration language (`HCL`)
- Manages cloud and on-premise resources
- Supports multiple cloud providers simultaneously
- Maintains a state file to track resources
- Plans changes before applying them

---

## Terraform Key Features

- **Multi-Cloud**: Works with AWS, Azure, GCP, and many more
- **Plan Before Apply**: Preview changes before execution
- **Resource Graph**: Determines correct order of operations
- **State Management**: Tracks real-world resource state
- **Modularity**: Reuse configurations with modules
- **Extensibility**: Custom providers via plugin system

---

## Terraform vs Other IaC Tools

| Feature | `Terraform` | `CloudFormation` | `Pulumi` | `Ansible` |
|---------|-----------|----------------|---------|---------|
| Multi-Cloud | Yes | AWS only | Yes | Yes |
| Language | `HCL` | `JSON`/`YAML` | General purpose | `YAML` |
| State | Yes | Managed | Yes | No |
| Approach | Declarative | Declarative | Imperative | Imperative |
| Agentless | Yes | Yes | Yes | Yes |

---

## Terraform Architecture

![terraform_architecture](svg/courses/devops/terraform/01_introduction/terraform_architecture.svg)

---

## How Terraform Works

1. Write configuration files in `HCL`
1. Run `terraform init` to initialize providers
1. Run `terraform plan` to preview changes
1. Run `terraform apply` to create/modify resources
1. Terraform updates the state file
1. Run `terraform destroy` to tear down resources

---

## Terraform Workflow Diagram

![terraform_workflow_diagram](svg/courses/devops/terraform/01_introduction/terraform_workflow_diagram.svg)

---

## Installing Terraform

- Download from `https://www.terraform.io/downloads`
- Available for Linux, macOS, Windows
- Single binary, no dependencies

```bash
# Linux (Ubuntu/Debian)
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```

---

## Verifying Installation

```bash
# Check version
terraform version

# Output:
# Terraform v1.7.0
# on linux_amd64

# Enable tab completion
terraform -install-autocomplete
```

---

## Installing with Package Managers

```bash
# macOS with Homebrew
brew tap hashicorp/tap
brew install hashicorp/tap/terraform

# Windows with Chocolatey
choco install terraform

# Using tfenv (version manager)
git clone https://github.com/tfutils/tfenv.git ~/.tfenv
tfenv install 1.7.0
tfenv use 1.7.0
```

---

## Introduction to HCL

- `HCL` = HashiCorp Configuration Language
- Human-readable configuration format
- JSON-compatible (can use `.tf.json` files)
- Supports comments, variables, and expressions
- File extension: `.tf`

---

## HCL Basic Syntax

```hcl
# This is a comment

/* This is a
   multi-line comment */

# Block syntax
block_type "label1" "label2" {
  argument1 = "value1"
  argument2 = 42
  argument3 = true

  nested_block {
    key = "value"
  }
}
```

---

## HCL Data Types

| Type | Example | Description |
|------|---------|-------------|
| `string` | `"hello"` | Text value |
| `number` | `42`, `3.14` | Numeric value |
| `bool` | `true`, `false` | Boolean value |
| `list` | `["a", "b"]` | Ordered collection |
| `map` | `{key = "val"}` | Key-value pairs |
| `null` | `null` | Absence of value |

---

## HCL Strings

```hcl
# Simple string
name = "terraform-instance"

# String interpolation
greeting = "Hello, ${var.name}!"

# Heredoc syntax
description = <<-EOT
  This is a multi-line
  string value that preserves
  line breaks.
EOT
```

---

## HCL Collections

```hcl
# List
availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]

# Map
tags = {
  Name        = "web-server"
  Environment = "production"
  Team        = "platform"
}

# Nested structure
settings = {
  cpu    = 4
  memory = 8192
  disks  = ["sda", "sdb"]
}
```

---

## HCL Expressions

```hcl
# Arithmetic
instance_count = var.base_count * 2

# Conditional
instance_type = var.env == "prod" ? "m5.large" : "t3.micro"

# For expression (list)
upper_names = [for name in var.names : upper(name)]

# For expression (map)
name_map = {for name in var.names : name => upper(name)}
```

---

## Terraform Configuration Blocks

![terraform_configuration_blocks](svg/courses/devops/terraform/01_introduction/terraform_configuration_blocks.svg)

---

## The terraform Block

```hcl
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}
```

---

## Provider Block

```hcl
provider "aws" {
  region  = "us-east-1"
  profile = "my-aws-profile"

  default_tags {
    tags = {
      ManagedBy = "Terraform"
    }
  }
}

provider "google" {
  project = "my-gcp-project"
  region  = "us-central1"
}
```

---

## Your First Terraform Configuration

```hcl
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
  }
}

resource "local_file" "hello" {
  content  = "Hello, Terraform!"
  filename = "${path.module}/hello.txt"
}
```

---

## Running Your First Configuration

```bash
# Initialize the working directory
terraform init

# Preview what will happen
terraform plan

# Create the resource
terraform apply

# Verify
cat hello.txt
# Output: Hello, Terraform!

# Clean up
terraform destroy
```

---

## Understanding terraform init Output

```output
Initializing the backend...

Initializing provider plugins...
- Finding hashicorp/local versions matching "~> 2.0"...
- Installing hashicorp/local v2.4.0...
- Installed hashicorp/local v2.4.0

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running
"terraform plan" to see any changes that are required
for your infrastructure.
```

---

## Understanding terraform plan Output

```output
Terraform will perform the following actions:

  # local_file.hello will be created
  + resource "local_file" "hello" {
      + content              = "Hello, Terraform!"
      + directory_permission = "0777"
      + file_permission      = "0777"
      + filename             = "./hello.txt"
      + id                   = (known after apply)
    }

Plan: 1 to add, 0 to change, 0 to destroy.
```

---

## Plan Symbols

| Symbol | Meaning |
|--------|---------|
| `+` | Resource will be created |
| `-` | Resource will be destroyed |
| `~` | Resource will be updated in-place |
| `-/+` | Resource will be destroyed and recreated |
| `<=` | Data source will be read |

---

## Terraform CLI Commands Overview

| Command | Description |
|---------|-------------|
| `terraform init` | Initialize working directory |
| `terraform plan` | Preview changes |
| `terraform apply` | Apply changes |
| `terraform destroy` | Destroy resources |
| `terraform fmt` | Format configuration files |
| `terraform validate` | Validate configuration |
| `terraform show` | Show current state |

---

## terraform fmt

```bash
# Format all .tf files in current directory
terraform fmt

# Format recursively
terraform fmt -recursive

# Check formatting without changing files
terraform fmt -check

# Show diff of formatting changes
terraform fmt -diff
```

- Automatically fixes indentation and alignment
- Use in CI/CD to enforce consistent style

---

## terraform validate

```bash
# Validate configuration syntax
terraform validate

# Successful output:
# Success! The configuration is valid.

# Error output example:
# Error: Missing required argument
#   on main.tf line 5, in resource "aws_instance" "web":
#    5: resource "aws_instance" "web" {
# The argument "ami" is required, but no definition was found.
```

---

## Chapter Summary

- Infrastructure as Code defines infrastructure in version-controlled files
- `Terraform` is a declarative, multi-cloud IaC tool by HashiCorp
- `HCL` is Terraform's human-readable configuration language
- The core workflow is: `init` -> `plan` -> `apply` -> `destroy`
- Configuration uses blocks: `terraform`, `provider`, `resource`, `variable`
- `terraform fmt` and `terraform validate` help maintain quality
