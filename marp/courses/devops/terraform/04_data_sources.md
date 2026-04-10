# Data Sources

## What are Data Sources?

- Data sources allow Terraform to read information from outside
- Query existing infrastructure not managed by Terraform
- Read-only - they do not create or modify resources
- Use the `data` block instead of `resource` block
- Fetched during `terraform plan` and `terraform apply`

---

## Data Source Syntax

```hcl
data "provider_type" "local_name" {
  # Filter arguments
  filter_arg1 = "value1"
  filter_arg2 = "value2"
}

# Reference: data.provider_type.local_name.attribute
output "result" {
  value = data.provider_type.local_name.some_attribute
}
```

---

## Data Source vs Resource

| Feature | Resource | Data Source |
|---------|----------|-------------|
| Block type | `resource` | `data` |
| Action | Create/Update/Delete | Read only |
| State | Tracked in state | Refreshed each run |
| Lifecycle | Full CRUD | Read only |
| Reference | `type.name.attr` | `data.type.name.attr` |

---

## Data Source vs Resource

![data_source_vs_resource](svg/courses/devops/terraform/04_data_sources/data_source_vs_resource.svg)

---

## AWS AMI Data Source

```hcl
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]  # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
}
```

---

## Why Use AMI Data Source?

```misc
Without data source:
  ami = "ami-0c55b159cbfafe1f0"  # Hardcoded, region-specific

With data source:
  ami = data.aws_ami.ubuntu.id   # Always finds latest AMI

Benefits:
  - Works across regions automatically
  - Always uses the latest AMI version
  - No manual AMI ID lookups needed
```

---

## AWS Availability Zones Data Source

```hcl
data "aws_availability_zones" "available" {
  state = "available"

  filter {
    name   = "opt-in-status"
    values = ["opt-in-not-required"]
  }
}

resource "aws_subnet" "public" {
  count             = length(data.aws_availability_zones.available.names)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]
}
```

---

## AWS VPC Data Source

```hcl
# Find the default VPC
data "aws_vpc" "default" {
  default = true
}

# Find a VPC by tag
data "aws_vpc" "production" {
  tags = {
    Environment = "production"
  }
}

resource "aws_security_group" "web" {
  vpc_id = data.aws_vpc.default.id
  # ...
}
```

---

## AWS Subnet Data Source

```hcl
data "aws_subnets" "public" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }

  tags = {
    Tier = "public"
  }
}

# Use with for_each
resource "aws_instance" "web" {
  for_each      = toset(data.aws_subnets.public.ids)
  subnet_id     = each.value
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
}
```

---

## AWS IAM Policy Document Data Source

```hcl
data "aws_iam_policy_document" "s3_access" {
  statement {
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:ListBucket",
    ]
    resources = [
      aws_s3_bucket.data.arn,
      "${aws_s3_bucket.data.arn}/*",
    ]
  }
}

resource "aws_iam_policy" "s3_access" {
  name   = "s3-access-policy"
  policy = data.aws_iam_policy_document.s3_access.json
}
```

---

## AWS Caller Identity Data Source

```hcl
data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

output "account_id" {
  value = data.aws_caller_identity.current.account_id
}

output "caller_arn" {
  value = data.aws_caller_identity.current.arn
}

output "region" {
  value = data.aws_region.current.name
}
```

---

## AWS Security Group Data Source

```hcl
data "aws_security_group" "existing" {
  name   = "existing-sg"
  vpc_id = data.aws_vpc.default.id
}

resource "aws_instance" "web" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t3.micro"
  vpc_security_group_ids = [data.aws_security_group.existing.id]
}
```

---

## Azure Data Sources

```hcl
data "azurerm_resource_group" "existing" {
  name = "existing-rg"
}

data "azurerm_virtual_network" "existing" {
  name                = "existing-vnet"
  resource_group_name = data.azurerm_resource_group.existing.name
}

resource "azurerm_subnet" "new" {
  name                 = "new-subnet"
  resource_group_name  = data.azurerm_resource_group.existing.name
  virtual_network_name = data.azurerm_virtual_network.existing.name
  address_prefixes     = ["10.0.2.0/24"]
}
```

---

## GCP Data Sources

```hcl
data "google_compute_image" "debian" {
  family  = "debian-11"
  project = "debian-cloud"
}

data "google_compute_zones" "available" {
  region = "us-central1"
  status = "UP"
}

resource "google_compute_instance" "vm" {
  name         = "web-server"
  machine_type = "e2-micro"
  zone         = data.google_compute_zones.available.names[0]

  boot_disk {
    initialize_params {
      image = data.google_compute_image.debian.self_link
    }
  }
}
```

---

## The external Data Source

```hcl
data "external" "ip_info" {
  program = ["bash", "-c", <<-EOT
    IP=$(curl -s https://api.ipify.org)
    echo "{\"ip\": \"$IP\"}"
  EOT
  ]
}

output "my_ip" {
  value = data.external.ip_info.result.ip
}
```

- Runs an external script
- Script must return valid JSON to stdout
- Useful for integrating with non-Terraform tools

---

## The http Data Source

```hcl
data "http" "my_ip" {
  url = "https://api.ipify.org?format=json"

  request_headers = {
    Accept = "application/json"
  }
}

locals {
  my_ip = jsondecode(data.http.my_ip.response_body).ip
}

output "my_public_ip" {
  value = local.my_ip
}
```

---

## The local_file Data Source

```hcl
data "local_file" "config" {
  filename = "${path.module}/config.json"
}

locals {
  config = jsondecode(data.local_file.config.content)
}

output "app_name" {
  value = local.config.app_name
}
```

- Reads a file from the local filesystem
- Content available as string or base64

---

## The template_file Data Source

```hcl
data "template_file" "user_data" {
  template = file("${path.module}/user_data.tpl")

  vars = {
    server_name = var.server_name
    db_host     = aws_db_instance.main.endpoint
    db_port     = 3306
  }
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  user_data     = data.template_file.user_data.rendered
}
```

---

## Using templatefile Function Instead

```hcl
# Modern approach (preferred over template_file data source)
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"

  user_data = templatefile("${path.module}/user_data.tpl", {
    server_name = var.server_name
    db_host     = aws_db_instance.main.endpoint
    db_port     = 3306
  })
}
```

- `templatefile()` is a built-in function
- No need for a separate data source block

---

## Data Source Dependencies

```hcl
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

# This data source depends on the VPC being created first
data "aws_subnets" "main" {
  filter {
    name   = "vpc-id"
    values = [aws_vpc.main.id]
  }

  depends_on = [aws_subnet.public]
}
```

- Data sources can depend on resources
- Use `depends_on` for explicit ordering

---

## Filtering Data Sources

```hcl
# Multiple filters (AND logic)
data "aws_ami" "example" {
  most_recent = true
  owners      = ["self"]

  filter {
    name   = "name"
    values = ["myapp-*"]
  }

  filter {
    name   = "tag:Environment"
    values = ["production"]
  }

  filter {
    name   = "state"
    values = ["available"]
  }
}
```

---

## Plural Data Sources

```hcl
# Singular: returns one resource
data "aws_subnet" "example" {
  id = "subnet-12345"
}

# Plural: returns multiple resources
data "aws_subnets" "example" {
  filter {
    name   = "vpc-id"
    values = [aws_vpc.main.id]
  }
}

# Use plural results in a loop
resource "aws_instance" "web" {
  for_each  = toset(data.aws_subnets.example.ids)
  subnet_id = each.value
  # ...
}
```

---

## Data Source Use Cases

| Use Case | Data Source |
|---------------------------|-----------------------------------|
| Find latest AMI | aws_ami |
| Get current account info | aws_caller_identity |
| List availability zones | aws_availability_zones |
| Read existing VPC config | aws_vpc, aws_subnets |
| Get DNS zone info | aws_route53_zone |
| Read SSM parameters | aws_ssm_parameter |
| Get secret from Vault | vault_generic_secret |
| Read remote state | terraform_remote_state |

---

## terraform_remote_state Data Source

```hcl
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

- Read outputs from another Terraform project
- Enables cross-project references

---

## Chapter Summary

- Data sources read existing information without creating resources
- Use `data` blocks to query infrastructure not managed by Terraform
- Common pattern: look up AMIs, VPCs, subnets dynamically
- `terraform_remote_state` enables cross-project data sharing
- Filters narrow results; use `most_recent` for latest matches
- Prefer `templatefile()` function over `template_file` data source
- Data sources refresh on every `plan` and `apply`
