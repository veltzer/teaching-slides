# State Management

## What is Terraform State?

- A JSON file that maps configuration to real-world resources
- Stores resource IDs, attributes, and metadata
- Default file: `terraform.tfstate`
- Created on first `terraform apply`
- Updated on every `apply` and `destroy`

---

## Why Does Terraform Need State?

- **Mapping**: Links config resources to real infrastructure
- **Performance**: Caches resource attributes (avoids querying APIs)
- **Dependencies**: Tracks resource relationships
- **Drift Detection**: Compares desired vs actual state
- **Collaboration**: Shared state enables team workflows

---

## State File Structure

```json
{
  "version": 4,
  "terraform_version": "1.7.0",
  "serial": 5,
  "lineage": "abc123-def456",
  "outputs": {
    "vpc_id": {
      "value": "vpc-12345",
      "type": "string"
    }
  },
  "resources": [
    {
      "mode": "managed",
      "type": "aws_vpc",
      "name": "main",
      "instances": [{"attributes": {"id": "vpc-12345"}}]
    }
  ]
}
```

---

## State File Lifecycle

<svg xmlns="http://www.w3.org/2000/svg" width="520" height="360" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
    <marker id="arr2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>  <rect x="90" y="20" width="340" height="46" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="260" y="46" text-anchor="middle" font-size="13" fill="#222">terraform init</text>
  <line x1="260" y1="66" x2="260" y2="84" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="90" y="84" width="340" height="46" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="260" y="110" text-anchor="middle" font-size="13" fill="#222">terraform plan</text>
  <line x1="260" y1="130" x2="260" y2="148" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="90" y="148" width="340" height="46" rx="4" fill="#fff3e0" stroke="#333" stroke-width="1.5"/>
  <text x="260" y="174" text-anchor="middle" font-size="13" fill="#222">terraform apply</text>
  <line x1="260" y1="194" x2="260" y2="212" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="90" y="212" width="340" height="46" rx="4" fill="#f0f4f8" stroke="#333" stroke-width="1.5"/>
  <text x="260" y="238" text-anchor="middle" font-size="13" fill="#222">terraform.tfstate (updated)</text>
  <line x1="260" y1="258" x2="260" y2="276" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="90" y="276" width="340" height="50" rx="4" fill="#f0f4f8" stroke="#333" stroke-width="1.5"/>
  <text x="260" y="298" text-anchor="middle" font-size="13" fill="#222">terraform.tfstate.backup</text>
  <text x="260" y="316" text-anchor="middle" font-size="11" fill="#555">(previous version)</text>
  <text x="480" y="170" text-anchor="middle" font-size="20" fill="#555">↩</text>
  <text x="470" y="188" text-anchor="middle" font-size="10" fill="#555">loop</text>
</svg>

---

## Viewing State

```bash
# Show full state in human-readable format
terraform show

# List all resources in state
terraform state list

# Show details of a specific resource
terraform state show aws_instance.web

# Output state as JSON
terraform show -json
```

---

## terraform state list Output

```bash
$ terraform state list

aws_vpc.main
aws_subnet.public[0]
aws_subnet.public[1]
aws_security_group.web
aws_instance.web
aws_db_instance.main
data.aws_ami.ubuntu
```

---

## terraform state show Output

```bash
$ terraform state show aws_instance.web

# aws_instance.web:
resource "aws_instance" "web" {
    ami                    = "ami-0c55b159cbfafe1f0"
    id                     = "i-0abc123def456"
    instance_type          = "t3.micro"
    private_ip             = "10.0.1.50"
    public_ip              = "54.123.45.67"
    subnet_id              = "subnet-12345"
    vpc_security_group_ids = ["sg-12345"]
    tags = {
        "Name" = "web-server"
    }
}
```

---

## Problems with Local State

- **No collaboration**: Only one person can modify at a time
- **No locking**: Risk of concurrent modifications
- **No encryption**: Secrets stored in plaintext
- **No backup**: Local disk failure loses state
- **No versioning**: Cannot roll back to previous state

---

## Remote State Overview

<svg xmlns="http://www.w3.org/2000/svg" width="650" height="250" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
    <marker id="arr2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>  <rect x="10" y="10" width="280" height="225" rx="4" fill="#ffebee" stroke="#c62828" stroke-width="1.5"/>
  <text x="150" y="30" text-anchor="middle" font-size="14" fill="#b71c1c" font-weight="bold">Local State</text>
  <rect x="40" y="55" width="110" height="50" rx="4" fill="#ffcdd2" stroke="#e53935" stroke-width="1.5"/>
  <text x="95" y="84" text-anchor="middle" font-size="12" fill="#222">Laptop A</text>
  <line x1="150" y1="80" x2="200" y2="80" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="245" y="75" text-anchor="middle" font-size="11" fill="#c62828">local file</text>
  <rect x="40" y="140" width="110" height="50" rx="4" fill="#ffcdd2" stroke="#e53935" stroke-width="1.5"/>
  <text x="95" y="169" text-anchor="middle" font-size="12" fill="#222">Laptop B</text>
  <line x1="150" y1="165" x2="200" y2="165" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="245" y="160" text-anchor="middle" font-size="11" fill="#c62828">local file</text>
  <text x="215" y="184" text-anchor="middle" font-size="11" fill="#c62828">(conflict!)</text>
  <rect x="340" y="10" width="300" height="225" rx="4" fill="#e8f5e9" stroke="#388e3c" stroke-width="1.5"/>
  <text x="490" y="30" text-anchor="middle" font-size="14" fill="#1b5e20" font-weight="bold">Remote State</text>
  <rect x="360" y="55" width="110" height="50" rx="4" fill="#c8e6c9" stroke="#43a047" stroke-width="1.5"/>
  <text x="415" y="84" text-anchor="middle" font-size="12" fill="#222">Laptop A</text>
  <line x1="470" y1="80" x2="510" y2="80" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="360" y="140" width="110" height="50" rx="4" fill="#c8e6c9" stroke="#43a047" stroke-width="1.5"/>
  <text x="415" y="169" text-anchor="middle" font-size="12" fill="#222">Laptop B</text>
  <line x1="470" y1="165" x2="510" y2="165" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="510" y="75" width="110" height="50" rx="4" fill="#fff3e0" stroke="#f57c00" stroke-width="1.5"/>
  <text x="565" y="96" text-anchor="middle" font-size="12" fill="#222">S3 Bucket</text>
  <text x="565" y="113" text-anchor="middle" font-size="11" fill="#555">+ DynamoDB</text>
  <line x1="470" y1="80" x2="510" y2="80" stroke="#555" stroke-width="1.5"/>
  <line x1="470" y1="165" x2="510" y2="165" stroke="#555" stroke-width="1.5"/>
  <line x1="510" y1="80" x2="510" y2="165" stroke="#555" stroke-width="1.5"/>
</svg>

---

## Backend Configuration

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

- Backends define where state is stored
- Configured in the `terraform` block
- Initialized with `terraform init`

---

## Available Backends

| Backend | Provider | Locking | Encryption |
|---------|----------|---------|------------|
| `s3` | AWS | DynamoDB | Yes |
| `azurerm` | Azure | Blob lease | Yes |
| `gcs` | GCP | Native | Yes |
| `consul` | HashiCorp | Native | Yes |
| `pg` | PostgreSQL | Native | Optional |
| `http` | Any | Optional | Optional |
| `cloud` | Terraform Cloud | Native | Yes |

---

## S3 Backend Setup

```hcl
# Create S3 bucket for state (bootstrap)
resource "aws_s3_bucket" "state" {
  bucket = "my-terraform-state"

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "state" {
  bucket = aws_s3_bucket.state.id
  versioning_configuration {
    status = "Enabled"
  }
}
```

---

## DynamoDB Table for Locking

```hcl
resource "aws_dynamodb_table" "locks" {
  name         = "terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Name = "Terraform State Lock Table"
  }
}
```

---

## S3 Backend with Full Options

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/network/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
    acl            = "bucket-owner-full-control"
    kms_key_id     = "alias/terraform-state"
  }
}
```

---

## Azure Backend

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "tfstate12345"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}
```

---

## GCS Backend

```hcl
terraform {
  backend "gcs" {
    bucket = "my-terraform-state"
    prefix = "prod/network"
  }
}
```

---

## Terraform Cloud Backend

```hcl
terraform {
  cloud {
    organization = "my-organization"

    workspaces {
      name = "my-workspace"
    }
  }
}
```

- Free tier available
- Built-in locking and versioning
- Web UI for state inspection
- Integration with VCS

---

## State Locking

<svg xmlns="http://www.w3.org/2000/svg" width="650" height="240" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
    <marker id="arr2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>  <rect x="10" y="10" width="280" height="215" rx="4" fill="#ffebee" stroke="#c62828" stroke-width="1.5"/>
  <text x="150" y="30" text-anchor="middle" font-size="14" fill="#b71c1c" font-weight="bold">Without Locking</text>
  <rect x="30" y="50" width="140" height="40" rx="4" fill="#ffcdd2" stroke="#e53935" stroke-width="1.5"/>
  <text x="100" y="74" text-anchor="middle" font-size="12" fill="#222">User A: tf apply</text>
  <rect x="30" y="110" width="140" height="40" rx="4" fill="#ffcdd2" stroke="#e53935" stroke-width="1.5"/>
  <text x="100" y="134" text-anchor="middle" font-size="12" fill="#222">User B: tf apply</text>
  <line x1="170" y1="70" x2="220" y2="100" stroke="#555" stroke-width="1.5"/>
  <line x1="170" y1="130" x2="220" y2="100" stroke="#555" stroke-width="1.5"/>
  <rect x="195" y="82" width="80" height="36" rx="4" fill="#ef9a9a" stroke="#c62828" stroke-width="1.5"/>
  <text x="235" y="104" text-anchor="middle" font-size="12" fill="#b71c1c" font-weight="bold">CONFLICT!</text>
  <rect x="330" y="10" width="300" height="215" rx="4" fill="#e8f5e9" stroke="#388e3c" stroke-width="1.5"/>
  <text x="480" y="30" text-anchor="middle" font-size="14" fill="#1b5e20" font-weight="bold">With Locking</text>
  <rect x="345" y="55" width="270" height="65" rx="4" fill="#c8e6c9" stroke="#43a047" stroke-width="1.5"/>
  <text x="480" y="79" text-anchor="middle" font-size="12" fill="#222" font-weight="bold">User A: tf apply</text>
  <text x="480" y="101" text-anchor="middle" font-size="11" fill="#2e7d32">→ Acquires lock → Apply → Release</text>
  <rect x="345" y="140" width="270" height="65" rx="4" fill="#c8e6c9" stroke="#43a047" stroke-width="1.5"/>
  <text x="480" y="164" text-anchor="middle" font-size="12" fill="#222" font-weight="bold">User B: tf apply</text>
  <text x="480" y="186" text-anchor="middle" font-size="11" fill="#2e7d32">→ Waits → Acquires → Apply</text>
</svg>

---

## State Lock Error

```output
Error: Error locking state: Error acquiring the state lock

Lock Info:
  ID:        a1b2c3d4-e5f6-7890
  Path:      my-terraform-state/prod/terraform.tfstate
  Operation: OperationTypeApply
  Who:       user@hostname
  Version:   1.7.0
  Created:   2024-01-15 10:30:00 UTC
```

```bash
# Force unlock (use with extreme caution)
terraform force-unlock a1b2c3d4-e5f6-7890
```

---

## State File Organization Patterns

<svg xmlns="http://www.w3.org/2000/svg" width="620" height="300" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
    <marker id="arr2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>  <rect x="10" y="10" width="600" height="67" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="310" y="30" text-anchor="middle" font-size="13" fill="#222" font-weight="bold">Pattern 1: Single State File</text>
  <text x="120" y="46" text-anchor="end" font-size="12" fill="#333">all-resources/</text>
  <text x="130" y="46" text-anchor="start" font-size="12" fill="#555">→ terraform.tfstate</text>
  <rect x="10" y="87" width="600" height="111" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="310" y="107" text-anchor="middle" font-size="13" fill="#222" font-weight="bold">Pattern 2: Per-Environment States</text>
  <text x="120" y="123" text-anchor="end" font-size="12" fill="#333">dev/</text>
  <text x="130" y="123" text-anchor="start" font-size="12" fill="#555">→ dev.tfstate</text>
  <text x="120" y="145" text-anchor="end" font-size="12" fill="#333">staging/</text>
  <text x="130" y="145" text-anchor="start" font-size="12" fill="#555">→ staging.tfstate</text>
  <text x="120" y="167" text-anchor="end" font-size="12" fill="#333">prod/</text>
  <text x="130" y="167" text-anchor="start" font-size="12" fill="#555">→ prod.tfstate</text>
  <rect x="10" y="208" width="600" height="111" rx="4" fill="#fff3e0" stroke="#333" stroke-width="1.5"/>
  <text x="310" y="228" text-anchor="middle" font-size="13" fill="#222" font-weight="bold">Pattern 3: Per-Component States</text>
  <text x="120" y="244" text-anchor="end" font-size="12" fill="#333">network/</text>
  <text x="130" y="244" text-anchor="start" font-size="12" fill="#555">→ network.tfstate</text>
  <text x="120" y="266" text-anchor="end" font-size="12" fill="#333">compute/</text>
  <text x="130" y="266" text-anchor="start" font-size="12" fill="#555">→ compute.tfstate</text>
  <text x="120" y="288" text-anchor="end" font-size="12" fill="#333">database/</text>
  <text x="130" y="288" text-anchor="start" font-size="12" fill="#555">→ database.tfstate</text>
</svg>

---

## Key Path Strategies for S3

```tree
s3://my-terraform-state/
├── global/
│   └── iam/terraform.tfstate
├── dev/
│   ├── network/terraform.tfstate
│   ├── compute/terraform.tfstate
│   └── database/terraform.tfstate
├── staging/
│   ├── network/terraform.tfstate
│   └── ...
└── prod/
    ├── network/terraform.tfstate
    └── ...
```

---

## Moving Resources in State

```bash
# Rename a resource in state
terraform state mv aws_instance.old aws_instance.new

# Move resource to a module
terraform state mv aws_instance.web module.compute.aws_instance.web

# Move between state files
terraform state mv -state-out=other.tfstate \
  aws_instance.web aws_instance.web
```

---

## Removing Resources from State

```bash
# Remove a resource from state (does NOT destroy it)
terraform state rm aws_instance.web

# Remove a module from state
terraform state rm module.vpc

# Remove a specific indexed resource
terraform state rm 'aws_instance.web[0]'
```

- Resource continues to exist in the cloud
- Terraform no longer manages it
- Useful for adopting resources into different configs

---

## Pulling and Pushing State

```bash
# Download remote state to local file
terraform state pull > terraform.tfstate.backup

# Upload local state to remote backend
terraform state push terraform.tfstate

# Force push (dangerous)
terraform state push -force terraform.tfstate
```

---

## Replacing Resources in State

```bash
# Mark a resource for replacement on next apply
terraform apply -replace="aws_instance.web"

# Previously known as "taint" (deprecated)
terraform taint aws_instance.web      # deprecated
terraform untaint aws_instance.web    # deprecated
```

- Forces recreation of a resource
- Useful when a resource is in a bad state

---

## State Backup

```misc
Automatic backups:
  terraform.tfstate         # Current state
  terraform.tfstate.backup  # Previous state

S3 versioning:
  Every state update creates a new version
  Previous versions accessible via S3 console

Manual backup:
  terraform state pull > backup-$(date +%Y%m%d).json
```

---

## Sensitive Data in State

- State file contains all resource attributes
- Passwords, API keys, and secrets are stored in plaintext
- Always encrypt state at rest

```misc
Mitigations:
  1. Use encrypted backends (S3 with KMS, Azure with encryption)
  2. Restrict access to state storage (IAM policies)
  3. Never commit state files to version control
  4. Use Terraform Cloud for managed encryption
  5. Mark variables as sensitive = true
```

---

## Migrating State Backends

```bash
# Step 1: Update backend configuration in .tf files

# Step 2: Re-initialize with migration
terraform init -migrate-state

# Terraform will ask:
# Do you want to copy existing state to the new backend?
# Enter "yes"

# Step 3: Verify state is accessible
terraform state list
```

---

## State Disaster Recovery

```bash
# If state is lost but resources exist:

# 1. Create a new empty state
terraform init

# 2. Import each resource
terraform import aws_vpc.main vpc-12345
terraform import aws_instance.web i-abc123

# 3. Verify configuration matches
terraform plan
# Should show no changes if config matches reality
```

---

## Chapter Summary

- State maps Terraform config to real-world resources
- Local state is unsuitable for team collaboration
- Use remote backends (S3, Azure Blob, GCS) for shared state
- Enable state locking with DynamoDB (AWS) or native locking
- Always encrypt state files at rest
- Use `terraform state` commands to inspect and modify state
- Never commit state files to version control
- Organize state by environment and component
