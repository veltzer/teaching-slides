# Keeping Terraform in Sync

## What is Configuration Drift?

- The difference between declared config and actual infrastructure
- Occurs when resources are modified outside Terraform
- Common cause: manual changes via console or CLI
- Can lead to unexpected behavior and security issues
- Terraform detects drift during `plan` and `apply`

---

## How Drift Happens

```diagram
Terraform Config          Actual Infrastructure
+------------------+     +------------------+
| instance_type:   |     | instance_type:   |
|   t3.micro       |     |   t3.large       | <-- Changed manually
+------------------+     +------------------+
| tags:            |     | tags:            |
|   Name: web      |     |   Name: web-prod | <-- Changed manually
+------------------+     +------------------+
```

---

## Drift Use Case: Manual Console Change

```text
1. Developer creates instance via Terraform
   instance_type = "t3.micro"

2. Someone changes instance type in AWS Console
   instance_type -> "t3.large"

3. Next terraform plan detects drift:
   ~ instance_type = "t3.large" -> "t3.micro"

4. terraform apply reverts the manual change
```

---

## Drift Use Case: Security Group Modified

```text
Scenario:
  - Terraform manages security group with port 80 open
  - Admin manually opens port 22 for debugging
  - Terraform plan shows port 22 will be removed
  - This is GOOD - prevents unauthorized access lingering

Resolution options:
  1. Apply to revert (close port 22)
  2. Update config to include port 22
  3. Use ignore_changes to allow manual changes
```

---

## Drift Use Case: Resource Deleted

```output
Scenario:
  - Terraform manages an S3 bucket
  - Someone deletes the bucket manually
  - terraform plan shows bucket will be created

  # aws_s3_bucket.data will be created
  + resource "aws_s3_bucket" "data" {
      + bucket = "my-app-data"
    }

  Plan: 1 to add, 0 to change, 0 to destroy.
```

---

## Drift Use Case: Tags Modified by AWS

```text
Some AWS services auto-add tags:
  - EKS adds kubernetes.io/* tags
  - ASG adds aws:autoscaling:groupName
  - CloudFormation adds aws:cloudformation:*

Solution: Use ignore_changes
```

```hcl
resource "aws_instance" "web" {
  # ...
  lifecycle {
    ignore_changes = [tags["aws:autoscaling:groupName"]]
  }
}
```

---

## The terraform refresh Command

```bash
# Refresh state to match actual infrastructure
terraform refresh

# Same as:
terraform apply -refresh-only

# Deprecated direct command (still works):
terraform refresh
```

- Updates the state file to match actual resources
- Does NOT modify any infrastructure
- Does NOT modify configuration files

---

## Refresh Workflow

```diagram
terraform refresh
    |
    v
Query all providers for current resource state
    |
    v
Compare API responses to current state file
    |
    v
Update state file with actual values
    |
    v
State file reflects reality (not config)
```

---

## terraform plan -refresh-only

```bash
$ terraform plan -refresh-only

Note: Objects have changed outside of Terraform

Terraform detected the following changes made outside
of Terraform since the last "terraform apply":

  # aws_instance.web has been changed
  ~ resource "aws_instance" "web" {
      ~ instance_type = "t3.micro" -> "t3.large"
        id            = "i-abc123"
    }

Would you like to update the Terraform state to reflect
these detected changes?
```

---

## Detecting vs Correcting Drift

```text
Detect drift only:
  terraform plan -refresh-only
  (shows what changed, updates state only)

Correct drift:
  terraform plan
  terraform apply
  (reverts infrastructure to match config)

Adopt drift:
  Update .tf files to match actual state
  terraform plan  (should show no changes)
```

---

## Preventing Drift

- Restrict manual access to cloud consoles
- Use IAM policies to enforce Terraform-only changes
- Run `terraform plan` in CI/CD to detect drift
- Set up scheduled drift detection
- Use `prevent_destroy` for critical resources
- Document that all changes must go through Terraform

---

## Drift Detection in CI/CD

```bash
#!/bin/bash
# drift-check.sh - Run on a schedule

terraform init
terraform plan -detailed-exitcode

# Exit codes:
# 0 = No changes (no drift)
# 1 = Error
# 2 = Changes detected (drift!)

if [ $? -eq 2 ]; then
  echo "DRIFT DETECTED!"
  # Send alert to Slack/email
fi
```

---

## Importing Existing Resources

- Bring existing infrastructure under Terraform management
- Required when adopting Terraform for existing environments
- Two approaches: `terraform import` and `import` blocks

---

## terraform import Command

```bash
# Syntax: terraform import <address> <resource_id>

# Import an EC2 instance
terraform import aws_instance.web i-abc123def456

# Import a VPC
terraform import aws_vpc.main vpc-12345

# Import an S3 bucket
terraform import aws_s3_bucket.data my-bucket-name

# Import a security group
terraform import aws_security_group.web sg-12345
```

---

## Import Workflow

```text
Step 1: Write the resource block in .tf files
        (even if incomplete)

Step 2: Run terraform import
        terraform import aws_instance.web i-abc123

Step 3: Run terraform state show to see attributes
        terraform state show aws_instance.web

Step 4: Update .tf files to match imported state
        (copy attributes from state show output)

Step 5: Run terraform plan
        (should show no changes if config matches)
```

---

## Import Example Step by Step

```hcl
# Step 1: Write a stub resource block
resource "aws_instance" "web" {
  # Will be filled in after import
}
```

```bash
# Step 2: Import the resource
terraform import aws_instance.web i-abc123def456
```

```bash
# Step 3: View the imported state
terraform state show aws_instance.web
```

---

## Import Example: Filling in Config

```hcl
# Step 4: Update config to match reality
resource "aws_instance" "web" {
  ami                    = "ami-0c55b159cbfafe1f0"
  instance_type          = "t3.micro"
  subnet_id              = "subnet-12345"
  vpc_security_group_ids = ["sg-12345"]
  key_name               = "my-key"

  tags = {
    Name = "web-server"
  }
}
```

```bash
# Step 5: Verify - should show no changes
terraform plan
```

---

## Import Blocks (Terraform 1.5+)

```hcl
import {
  to = aws_instance.web
  id = "i-abc123def456"
}

resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
  # ...
}
```

- Declarative alternative to `terraform import` command
- Can be committed to version control
- Runs during `terraform plan` and `terraform apply`

---

## Multiple Import Blocks

```hcl
import {
  to = aws_vpc.main
  id = "vpc-12345"
}

import {
  to = aws_subnet.public
  id = "subnet-67890"
}

import {
  to = aws_security_group.web
  id = "sg-11111"
}
```

---

## Generating Config from Import

```bash
# Generate config for imported resources (Terraform 1.5+)
terraform plan -generate-config-out=generated.tf
```

- Terraform generates `.tf` files from imported resources
- Review and refine the generated code
- Removes the need to manually write resource blocks

---

## Import with for_each

```hcl
import {
  for_each = {
    web    = "i-abc123"
    api    = "i-def456"
    worker = "i-ghi789"
  }
  to = aws_instance.servers[each.key]
  id = each.value
}

resource "aws_instance" "servers" {
  for_each      = toset(["web", "api", "worker"])
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
}
```

---

## Import Limitations

- Not all resources support import
- Some attributes may not be importable
- Complex resources may require manual config tuning
- State-only operation (does not generate config automatically before 1.5)
- Must write config before importing (except with `-generate-config-out`)

---

## terraform state rm for Re-import

```bash
# Remove resource from state (keeps actual resource)
terraform state rm aws_instance.web

# Re-import with different address
terraform import module.compute.aws_instance.web i-abc123
```

- Useful when reorganizing configuration
- Resource continues to exist in the cloud
- Must re-import to manage again

---

## Moved Blocks for Refactoring

```hcl
# Rename a resource without recreating it
moved {
  from = aws_instance.web_server
  to   = aws_instance.web
}

# Move into a module
moved {
  from = aws_instance.web
  to   = module.compute.aws_instance.web
}
```

- Tells Terraform the resource was renamed
- Prevents destroy and recreate
- Can be removed after everyone has applied

---

## Chapter Summary

- Configuration drift occurs when infrastructure diverges from config
- `terraform refresh` updates state to match actual infrastructure
- `terraform plan` detects drift and proposes corrections
- `terraform import` brings existing resources under management
- Import blocks (1.5+) provide a declarative import approach
- Use `-generate-config-out` to auto-generate config from imports
- `moved` blocks enable safe resource refactoring
- Prevent drift with access controls and CI/CD checks
