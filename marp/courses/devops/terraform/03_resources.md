---
tags:
  - practices:devops
  - tools:terraform
  - infrastructure:infrastructure-as-code
  - infrastructure:cloud
  - tools:terragrunt
level: intermediate
category: devops
audience:
  - audiences:developers
  - audiences:sysadmins
  - audiences:devops

---
# Resources

## What is a Resource?

- A resource is a single piece of infrastructure
- Examples: virtual machine, DNS record, S3 bucket
- Defined using `resource` blocks in `HCL`
- Terraform manages the full lifecycle: create, read, update, delete
- Each resource belongs to a specific provider

---

## Resource Block Syntax

```hcl
resource "provider_type" "local_name" {
  argument1 = "value1"
  argument2 = "value2"

  nested_block {
    key = "value"
  }
}
```

- `provider_type`: The resource type (e.g., `aws_instance`)
- `local_name`: A unique name within your configuration
- Arguments configure the resource's properties

---

## Resource Naming Convention

```hcl
# Format: resource "TYPE" "NAME"
#   TYPE = provider_resourcetype
#   NAME = logical identifier (unique per type)

resource "aws_instance" "web_server" {
  # ...
}

resource "aws_instance" "database" {
  # ...
}

resource "google_compute_instance" "web_server" {
  # ...
}
```

---
## What are Providers?

- Plugins that Terraform uses to interact with APIs
- Each provider manages a specific set of resource types
- Must be declared in the `terraform` block
- Downloaded during `terraform init`

---
## What are Providers?

![what_are_providers](svg/courses/devops/terraform/03_resources/what_are_providers.svg)

---

## Provider Configuration

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}
```

---

## Provider Version Constraints

| Constraint | Meaning |
|-----------|---------|
| `= 5.0.0` | Exact version |
| `>= 5.0` | Minimum version |
| `~> 5.0` | Any 5.x version |
| `~> 5.30.0` | Any 5.30.x version |
| `>= 5.0, < 6.0` | Range |

---

## Multiple Provider Instances

```hcl
provider "aws" {
  region = "us-east-1"
  alias  = "east"
}

provider "aws" {
  region = "us-west-2"
  alias  = "west"
}

resource "aws_instance" "east_server" {
  provider      = aws.east
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
}

resource "aws_instance" "west_server" {
  provider      = aws.west
  ami           = "ami-0892d3c7ee96c0bf7"
  instance_type = "t3.micro"
}
```

---

## Popular Providers

| Provider | Source | Use Case |
|----------|--------|----------|
| `aws` | `hashicorp/aws` | Amazon Web Services |
| `azurerm` | `hashicorp/azurerm` | Microsoft Azure |
| `google` | `hashicorp/google` | Google Cloud |
| `kubernetes` | `hashicorp/kubernetes` | Kubernetes |
| `docker` | `kreuzwerker/docker` | Docker containers |
| `local` | `hashicorp/local` | Local files |
| `random` | `hashicorp/random` | Random values |

---

## AWS EC2 Instance Resource

```hcl
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  tags = {
    Name        = "web-server"
    Environment = "dev"
  }
}
```

---

## AWS S3 Bucket Resource

```hcl
resource "aws_s3_bucket" "data" {
  bucket = "my-company-data-bucket"

  tags = {
    Name = "Data Bucket"
  }
}

resource "aws_s3_bucket_versioning" "data" {
  bucket = aws_s3_bucket.data.id

  versioning_configuration {
    status = "Enabled"
  }
}
```

---

## AWS VPC Resource

```hcl
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "main-vpc"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "us-east-1a"
}
```

---

## AWS Security Group Resource

```hcl
resource "aws_security_group" "web" {
  name        = "web-sg"
  description = "Allow HTTP and SSH"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

---

## Azure Resource Group

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example" {
  name     = "example-resources"
  location = "East US"
}

resource "azurerm_virtual_network" "example" {
  name                = "example-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
}
```

---

## GCP Compute Instance

```hcl
provider "google" {
  project = "my-project-id"
  region  = "us-central1"
}

resource "google_compute_instance" "vm" {
  name         = "web-server"
  machine_type = "e2-micro"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network = "default"
  }
}
```

---

## Resource References

```hcl
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "public" {
  # Reference another resource's attribute
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
}

resource "aws_instance" "web" {
  subnet_id = aws_subnet.public.id
  # ...
}
```

- Format: `resource_type.resource_name.attribute`

---
## Implicit Dependencies

```hcl
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}
# Terraform automatically knows this depends on the VPC
resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
}
```

---
## Implicit Dependencies

![terraform_automatically_knows_this_depends_on_the_vpc](svg/courses/devops/terraform/03_resources/terraform_automatically_knows_this_depends_on_the_vpc.svg)

---

## Explicit Dependencies

```hcl
resource "aws_s3_bucket" "logs" {
  bucket = "app-logs-bucket"
}

resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  # Explicit dependency (no attribute reference)
  depends_on = [aws_s3_bucket.logs]
}
```

- Use `depends_on` when there is no attribute reference
- Terraform cannot infer the dependency automatically

---

## Resource Attributes

```hcl
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
}

# Computed attributes (available after apply)
output "instance_id" {
  value = aws_instance.web.id
}

output "public_ip" {
  value = aws_instance.web.public_ip
}

output "private_ip" {
  value = aws_instance.web.private_ip
}
```

---

## Argument vs Attribute

| Concept | Description | Example |
|---------|-------------|---------|
| Argument | Value you set in config | `instance_type = "t3.micro"` |
| Attribute | Value returned by provider | `aws_instance.web.id` |
| Computed | Set by provider, not user | `public_ip` |
| Required | Must be specified | `ami` for `aws_instance` |
| Optional | Has a default value | `associate_public_ip_address` |

---

## Multiple Resources with count

```hcl
resource "aws_instance" "web" {
  count         = 3
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  tags = {
    Name = "web-server-${count.index}"
  }
}

# Access: aws_instance.web[0], aws_instance.web[1], ...
output "instance_ids" {
  value = aws_instance.web[*].id
}
```

---

## Conditional Resources with count

```hcl
variable "create_database" {
  type    = bool
  default = true
}

resource "aws_db_instance" "main" {
  count = var.create_database ? 1 : 0

  engine         = "mysql"
  instance_class = "db.t3.micro"
  # ...
}

output "db_endpoint" {
  value = var.create_database ? aws_db_instance.main[0].endpoint : null
}
```

---

## Multiple Resources with for_each

```hcl
variable "instances" {
  default = {
    web  = "t3.micro"
    api  = "t3.small"
    worker = "t3.medium"
  }
}

resource "aws_instance" "servers" {
  for_each      = var.instances
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = each.value

  tags = {
    Name = each.key
  }
}
```

---

## count vs for_each

| Feature | `count` | `for_each` |
|---------|---------|------------|
| Index type | Numeric | String key |
| Removal | Shifts indices | Removes by key |
| Input | Number | Map or set |
| Reference | `resource[0]` | `resource["key"]` |
| Best for | Identical resources | Distinct resources |

---

## Resource Lifecycle

![resource_lifecycle](svg/courses/devops/terraform/03_resources/resource_lifecycle.svg)

---

## Lifecycle Meta-Arguments

```hcl
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  lifecycle {
    create_before_destroy = true
    prevent_destroy       = true
    ignore_changes        = [tags]
  }
}
```

---

## create_before_destroy

```hcl
resource "aws_instance" "web" {
  ami           = "ami-new-version"
  instance_type = "t3.micro"

  lifecycle {
    create_before_destroy = true
  }
}
```

```misc
Default:    Destroy old --> Create new  (downtime)
With flag:  Create new  --> Destroy old (zero downtime)
```

---

## prevent_destroy

```hcl
resource "aws_db_instance" "production" {
  engine         = "mysql"
  instance_class = "db.r5.large"

  lifecycle {
    prevent_destroy = true
  }
}
```

- Prevents accidental deletion of critical resources
- Terraform will error if destroy is attempted
- Must be removed from config to allow destruction

---

## ignore_changes

```hcl
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  lifecycle {
    # Ignore changes made outside Terraform
    ignore_changes = [
      tags,
      user_data,
    ]

    # Or ignore ALL changes
    # ignore_changes = all
  }
}
```

---

## replace_triggered_by

```hcl
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  lifecycle {
    replace_triggered_by = [
      null_resource.deployment_trigger.id
    ]
  }
}

resource "null_resource" "deployment_trigger" {
  triggers = {
    deploy_version = var.deploy_version
  }
}
```

---

## Timeouts

```hcl
resource "aws_db_instance" "main" {
  engine         = "mysql"
  instance_class = "db.r5.large"

  timeouts {
    create = "60m"
    update = "30m"
    delete = "30m"
  }
}
```

- Some resources take a long time to provision
- Set custom timeouts per operation
- Prevents Terraform from timing out prematurely

---

## The random Provider

```hcl
resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
}

resource "aws_s3_bucket" "data" {
  bucket = "my-app-${random_string.suffix.result}"
}
```

- Generates random values for unique naming
- Types: `random_string`, `random_id`, `random_pet`, `random_integer`

---

## The null_resource

```hcl
resource "null_resource" "example" {
  triggers = {
    config_hash = filemd5("config.yaml")
  }

  provisioner "local-exec" {
    command = "echo Configuration changed!"
  }
}
```

- Does not manage any real infrastructure
- Useful for running provisioners
- Recreated when `triggers` change

---

## Resource Documentation

- Each provider has detailed documentation
- Visit `registry.terraform.io`
- Browse by provider and resource type

```tree
registry.terraform.io
    └── providers/
        └── hashicorp/
            └── aws/
                └── docs/
                    ├── resources/
                    │   ├── instance.md
                    │   ├── s3_bucket.md
                    │   └── ...
                    └── data-sources/
                        ├── ami.md
                        └── ...
```

---

## Chapter Summary

- Resources are the fundamental building blocks of Terraform
- Each resource belongs to a provider (AWS, Azure, GCP, etc.)
- Resources are referenced as `type.name.attribute`
- Dependencies can be implicit (references) or explicit (`depends_on`)
- `count` creates multiple identical resources
- `for_each` creates multiple distinct resources from a map or set
- Lifecycle meta-arguments control create, update, and delete behavior
- Use `prevent_destroy` to protect critical resources
