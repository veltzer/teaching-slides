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

# Security and Terraform

---

## Security Practices

![security_practices](svg/courses/devops/terraform/09_security/security_practices.svg)

---

## Security Concerns with Terraform

- State files contain sensitive data in plaintext
- Configuration files may contain secrets
- Provider credentials need secure management
- Access control for who can apply changes
- Audit trail for infrastructure changes

---

## Security Layers

![security_layers](svg/courses/devops/terraform/09_security/security_layers.svg)

---

## Security Controls

![security_controls](svg/courses/devops/terraform/09_security/security_controls.svg)

---

## Secrets in Terraform: The Problem

```hcl
# NEVER do this
resource "aws_db_instance" "main" {
  engine   = "mysql"
  username = "admin"
  password = "SuperSecret123!"  # Exposed in code AND state
}
```

- Password visible in source code
- Password stored in state file
- Anyone with repo access can see it

---

## Sensitive Variables

```hcl
variable "db_password" {
  description = "Database master password"
  type        = string
  sensitive   = true
}

resource "aws_db_instance" "main" {
  engine   = "mysql"
  username = "admin"
  password = var.db_password
}
```

```output
# Plan output hides the value:
+ password = (sensitive value)
```

---

## Providing Sensitive Variables

```bash
# Option 1: Environment variable
export TF_VAR_db_password="SuperSecret123!"
terraform apply

# Option 2: Interactive prompt (no -var, no default)
terraform apply
# var.db_password
#   Enter a value: ****

# Option 3: Separate tfvars file (not committed)
terraform apply -var-file="secrets.tfvars"
```

---

## Sensitive Outputs

```hcl
output "db_connection_string" {
  description = "Database connection string"
  value       = "mysql://${aws_db_instance.main.endpoint}"
  sensitive   = true
}
```

```bash
# Normal output shows:
# db_connection_string = <sensitive>

# To reveal:
terraform output -raw db_connection_string
terraform output -json
```

---

## AWS Secrets Manager Integration

```hcl
# Store secret in AWS Secrets Manager
resource "aws_secretsmanager_secret" "db_password" {
  name = "prod/db/password"
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = var.db_password
}

# Read secret from Secrets Manager
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "prod/db/password"
}
```

---

## AWS SSM Parameter Store

```hcl
# Store a secret parameter
resource "aws_ssm_parameter" "db_password" {
  name  = "/prod/db/password"
  type  = "SecureString"
  value = var.db_password
}

# Read a secret parameter
data "aws_ssm_parameter" "db_password" {
  name            = "/prod/db/password"
  with_decryption = true
}

resource "aws_db_instance" "main" {
  password = data.aws_ssm_parameter.db_password.value
  # ...
}
```

---

## HashiCorp Vault Integration

```hcl
provider "vault" {
  address = "https://vault.example.com:8200"
}

data "vault_generic_secret" "db_creds" {
  path = "secret/data/prod/database"
}

resource "aws_db_instance" "main" {
  engine   = "mysql"
  username = data.vault_generic_secret.db_creds.data["username"]
  password = data.vault_generic_secret.db_creds.data["password"]
}
```

---

## Vault Dynamic Secrets

```hcl
# Vault generates temporary AWS credentials
data "vault_aws_access_credentials" "creds" {
  backend = "aws"
  role    = "terraform-role"
  type    = "sts"
}

provider "aws" {
  access_key = data.vault_aws_access_credentials.creds.access_key
  secret_key = data.vault_aws_access_credentials.creds.secret_key
  token      = data.vault_aws_access_credentials.creds.security_token
  region     = "us-east-1"
}
```

---

## Vault Dynamic Secrets Flow

![vault_dynamic_secrets_flow](svg/courses/devops/terraform/09_security/vault_dynamic_secrets_flow.svg)

---

## Provider Authentication Best Practices

```bash
# AWS: Use IAM roles, not access keys
# EC2 instance role or ECS task role
provider "aws" {
  region = "us-east-1"
  # No credentials in config - uses instance role
}

# Or use AWS profiles
provider "aws" {
  region  = "us-east-1"
  profile = "terraform-admin"
}

# Or environment variables
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_SESSION_TOKEN="..."
```

---

## State File Encryption

```hcl
# S3 backend with encryption
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    kms_key_id     = "arn:aws:kms:us-east-1:123456789:key/abc-123"
    dynamodb_table = "terraform-locks"
  }
}
```

---

## State Access Control (AWS)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": "arn:aws:s3:::my-terraform-state/*"
    },
    {
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": "arn:aws:s3:::my-terraform-state"
    },
    {
      "Effect": "Allow",
      "Action": ["dynamodb:PutItem", "dynamodb:GetItem", "dynamodb:DeleteItem"],
      "Resource": "arn:aws:dynamodb:*:*:table/terraform-locks"
    }
  ]
}
```

---

## RBAC with Terraform Cloud

```tree
Terraform Cloud Organization
├── Owners (full access)
├── Teams
│   ├── platform-team
│   │   ├── Workspace: prod-infra (admin)
│   │   └── Workspace: staging-infra (admin)
│   ├── dev-team
│   │   ├── Workspace: dev-infra (write)
│   │   └── Workspace: prod-infra (read)
│   └── security-team
│       └── All workspaces (read)
```

---

## Terraform Cloud Permission Levels

| Permission | Capabilities |
|-----------|-------------|
| Read | View state, view runs |
| Plan | Queue plans (no apply) |
| Write | Queue plans and apply |
| Admin | Manage workspace settings |
| Owner | Full organization access |

---

## Policy as Code with Sentinel

```python
# sentinel/restrict-instance-types.sentinel
import "tfplan/v2" as tfplan

allowed_types = ["t3.micro", "t3.small", "t3.medium"]

main = rule {
  all tfplan.resource_changes as _, rc {
    rc.type is "aws_instance" and
    rc.change.after.instance_type in allowed_types
  }
}
```

- Sentinel is HashiCorp's policy-as-code framework
- Runs between plan and apply
- Enforces governance rules

---

## OPA (Open Policy Agent) Alternative

```rego
# policy/terraform.rego
package terraform

deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_instance"
  not startswith(resource.change.after.instance_type, "t3.")
  msg := sprintf("Instance %v uses disallowed type: %v",
    [resource.address, resource.change.after.instance_type])
}
```

```bash
# Run OPA against terraform plan
terraform plan -out=tfplan
terraform show -json tfplan > plan.json
opa eval -i plan.json -d policy/ "data.terraform.deny"
```

---

## Securing the CI/CD Pipeline

![securing_the_ci_cd_pipeline](svg/courses/devops/terraform/09_security/securing_the_ci_cd_pipeline.svg)

---

## Securing the CI/CD Pipeline: Details

- Store credentials in CI/CD secret store
- Run policy checks before apply
- Require approval for production changes

---

## GitHub Actions Secrets

```yaml
# .github/workflows/terraform.yml
name: Terraform
on: push
jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - name: Terraform Init
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: terraform init
```

---

## OIDC Authentication (No Stored Keys)

```hcl
# No long-lived credentials needed
# GitHub Actions uses OIDC to assume AWS role

# AWS IAM role trusts GitHub OIDC provider
data "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com"
}

resource "aws_iam_role" "github_actions" {
  name = "github-actions-terraform"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Federated = data.aws_iam_openid_connect_provider.github.arn }
      Action = "sts:AssumeRoleWithWebIdentity"
    }]
  })
}
```

---

## Security Scanning Tools

| Tool | Purpose |
|------|---------|
| `tfsec` | Static analysis for security issues |
| `checkov` | Policy-as-code scanning |
| `terrascan` | Compliance scanning |
| `tflint` | Linting and best practices |
| `trivy` | Vulnerability scanning |

---

## tfsec Example

```bash
# Install and run tfsec
brew install tfsec
tfsec .
```

```output
Result: AWS Security Group allows ingress from 0.0.0.0/0

  main.tf line 15:
    ingress {
      cidr_blocks = ["0.0.0.0/0"]
      from_port   = 22
      to_port     = 22
    }

  Impact:     Your port 22 is exposed to the internet
  Resolution: Set a more restrictive CIDR range
  Severity:   CRITICAL
```

---

## checkov Example

```bash
# Install and run checkov
pip install checkov
checkov -d .
```

```output
Passed checks: 12, Failed checks: 3, Skipped checks: 0

Check: CKV_AWS_79: "Ensure Instance Metadata Service Version 1
  is not enabled"
  FAILED for resource: aws_instance.web
  File: /main.tf:15-25

Check: CKV_AWS_88: "EC2 instance should not have public IP"
  FAILED for resource: aws_instance.web
  File: /main.tf:15-25
```

---

## Security Best Practices Summary

- Never hardcode secrets in `.tf` files
- Mark sensitive variables with `sensitive = true`
- Encrypt state files at rest (S3 + KMS)
- Use IAM roles instead of access keys
- Integrate with Vault for dynamic secrets
- Implement policy-as-code (Sentinel or OPA)
- Use OIDC for CI/CD authentication
- Run security scanners (`tfsec`, `checkov`) in CI

---

## Chapter Summary

- Terraform state contains sensitive data - always encrypt
- Use `sensitive = true` on variables and outputs
- Integrate with secrets managers (Vault, AWS Secrets Manager, SSM)
- Restrict state access with IAM policies
- Terraform Cloud provides built-in RBAC
- Policy-as-code enforces governance before apply
- Use OIDC for keyless CI/CD authentication
- Run security scanners as part of the development workflow
