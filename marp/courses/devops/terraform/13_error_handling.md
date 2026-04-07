# Error Handling and Debugging

## Common Error Categories

![common_error_categories](/svg/courses/devops/terraform/13_error_handling/common_error_categories.svg)

---

## Configuration Errors: Syntax

```output
Error: Invalid character

  on main.tf line 5:

  resource "aws_instance" "web" {
    ami = "ami-12345"
    instance_type = "t3.micro"
  }  # <-- extra closing brace

Error: Argument or block definition required

  on main.tf line 3, in resource "aws_instance" "web":
     3:   ami =
```

---

## Configuration Errors: Missing Required

```output
Error: Missing required argument

  on main.tf line 1, in resource "aws_instance" "web":
   1: resource "aws_instance" "web" {

  The argument "ami" is required, but no definition was found.

Error: Missing required argument

  on main.tf line 1, in resource "aws_instance" "web":
   1: resource "aws_instance" "web" {

  The argument "instance_type" is required, but no definition
  was found.
```

---

## Configuration Errors: Type Mismatch

```output
Error: Invalid value for variable

  on main.tf line 5:
   5:   instance_count = "three"

  var.instance_count expects a number, but got a string.

Error: Incorrect attribute value type

  on main.tf line 3, in resource "aws_instance" "web":
   3:   count = "3"

  Inappropriate value for attribute "count": a number is required.
```

---

## Configuration Errors: Unknown Reference

```output
Error: Reference to undeclared resource

  on main.tf line 10, in resource "aws_subnet" "public":
  10:   vpc_id = aws_vpc.main.id

  A managed resource "aws_vpc" "main" has not been declared
  in the root module.

Fix: Check resource names for typos or missing declarations.
```

---

## Provider Errors: Authentication

```output
Error: No valid credential sources found

  Provider "aws" requires valid credentials.

  Please set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
  or configure a profile in ~/.aws/credentials.

Error: error configuring Terraform AWS Provider:
  no valid credential sources for Terraform AWS Provider
  found.
```

```bash
# Fix: Set credentials
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
```

---

## Provider Errors: API Errors

```output
Error: creating EC2 Instance: operation error EC2:
  RunInstances, api error InvalidAMIID.NotFound:
  The image id '[ami-invalid]' does not exist

Error: creating S3 Bucket: BucketAlreadyExists:
  The requested bucket name is not available

Error: creating RDS DB Instance: DBInstanceAlreadyExists:
  DB instance already exists
```

---

## Provider Errors: Quota and Limits

```output
Error: creating EC2 Instance: VcpuLimitExceeded:
  You have requested more vCPU capacity than your
  current vCPU limit of 32 allows.

Error: creating VPC: VpcLimitExceeded:
  The maximum number of VPCs has been reached.

Fix:
  1. Request quota increase via AWS console
  2. Clean up unused resources
  3. Use a different region
```

---

## Provider Errors: Permission Denied

```output
Error: creating EC2 Instance: UnauthorizedOperation:
  You are not authorized to perform this operation.
  User: arn:aws:iam::123456789:user/terraform
  is not authorized to perform: ec2:RunInstances

Fix:
  1. Check IAM permissions
  2. Add required policies to the Terraform user/role
  3. Verify you are using the correct AWS account
```

---

## State Errors: Lock

```output
Error: Error locking state: Error acquiring the state lock

Lock Info:
  ID:        d7b8c2a1-1234-5678-abcd-ef0123456789
  Path:      s3://my-state/terraform.tfstate
  Operation: OperationTypeApply
  Who:       alice@workstation
  Version:   1.7.0
  Created:   2024-01-15 10:30:00 UTC

Terraform acquires a state lock to protect against
concurrent state file modification.
```

---

## Resolving State Lock Issues

```bash
# Wait for the other operation to finish (preferred)

# Force unlock if the process crashed
terraform force-unlock d7b8c2a1-1234-5678-abcd-ef0123456789

# Verify state is not corrupted after force unlock
terraform plan
```

- Only force-unlock if certain the other process is not running
- A crashed process may leave an orphaned lock

---

## State Errors: Corrupt State

```output
Error: Failed to load state: Unsupported state file format

Error: Error refreshing state: state data in S3 does
  not have the expected content.

Recovery options:
  1. Restore from terraform.tfstate.backup
  2. Restore from S3 versioning
  3. Import resources into new state
```

---

## State Recovery from Backup

```bash
# Option 1: Use local backup
cp terraform.tfstate.backup terraform.tfstate
terraform plan

# Option 2: Restore from S3 versioning
aws s3api list-object-versions \
  --bucket my-terraform-state \
  --prefix prod/terraform.tfstate

aws s3api get-object \
  --bucket my-terraform-state \
  --key prod/terraform.tfstate \
  --version-id "abc123" \
  terraform.tfstate
```

---

## Dependency Errors: Cycles

```output
Error: Cycle: aws_security_group.a,
  aws_security_group.b

This occurs when resources reference each other:
  SG A references SG B
  SG B references SG A
```

```hcl
# Fix: Use separate security group rules
resource "aws_security_group" "a" {
  name = "sg-a"
}

resource "aws_security_group_rule" "a_to_b" {
  security_group_id        = aws_security_group.a.id
  source_security_group_id = aws_security_group.b.id
  type                     = "ingress"
  # ...
}
```

---

## Terraform Logging

```bash
# Set log level
export TF_LOG=TRACE

# Available levels (most to least verbose):
# TRACE, DEBUG, INFO, WARN, ERROR

# Log to file
export TF_LOG_PATH="terraform.log"

# Run terraform with logging enabled
terraform plan

# Disable logging
unset TF_LOG
unset TF_LOG_PATH
```

---

## Log Levels Explained

| Level | Description | Use Case |
|-------|-------------|----------|
| `TRACE` | All internal operations | Deep debugging |
| `DEBUG` | Detailed operations | Provider issues |
| `INFO` | General information | Normal operations |
| `WARN` | Warnings | Deprecated features |
| `ERROR` | Errors only | Production monitoring |

---

## Separate Provider Logging

```bash
# Log only the AWS provider
export TF_LOG_PROVIDER=DEBUG

# Log only Terraform core
export TF_LOG_CORE=TRACE

# Combine both
export TF_LOG_CORE=WARN
export TF_LOG_PROVIDER=DEBUG
export TF_LOG_PATH="terraform.log"

terraform plan
```

---

## Reading Debug Output

```output
2024-01-15T10:30:00.123Z [DEBUG] provider.aws:
  HTTP Request Sent:
    Method: POST
    URL: https://ec2.us-east-1.amazonaws.com/
    Headers:
      Authorization: AWS4-HMAC-SHA256 ...
    Body: Action=RunInstances&...

2024-01-15T10:30:01.456Z [DEBUG] provider.aws:
  HTTP Response Received:
    Status: 400
    Body: <Error><Code>InvalidAMIID</Code>...
```

---

## Crash Logs

```misc
If Terraform crashes, it creates a crash.log file:

crash.log contains:
  - Stack trace
  - Terraform version
  - Go runtime info
  - Provider versions

Submit crash logs to:
  github.com/hashicorp/terraform/issues
```

```bash
# Check for crash logs
ls crash.log crash.*.log
```

---

## terraform validate

```bash
# Check configuration validity
terraform validate

# JSON output for CI/CD
terraform validate -json
```

```json
{
  "valid": false,
  "error_count": 1,
  "diagnostics": [
    {
      "severity": "error",
      "summary": "Missing required argument",
      "detail": "\"ami\" is required"
    }
  ]
}
```

---

## Pre-Apply Validation

```bash
#!/bin/bash
# validate-and-apply.sh

echo "=== Formatting ==="
terraform fmt -check -recursive || { echo "Format check failed"; exit 1; }

echo "=== Validating ==="
terraform validate || { echo "Validation failed"; exit 1; }

echo "=== Planning ==="
terraform plan -out=tfplan || { echo "Plan failed"; exit 1; }

echo "=== Applying ==="
terraform apply tfplan
```

---

## Common Mistakes and Fixes

| Mistake | Fix |
|---------|-----|
| Hardcoded AMI IDs | Use `data.aws_ami` data source |
| Missing `depends_on` | Add explicit dependencies |
| Not using `-out` with plan | Always save plan file |
| Editing state manually | Use `terraform state` commands |
| Not locking state | Enable DynamoDB locking |
| Ignoring plan output | Review every change carefully |

---

## Handling Partial Failures

```misc
Scenario: Apply creates 3 of 5 resources, then fails

State after partial failure:
  Resource A: Created (in state)
  Resource B: Created (in state)
  Resource C: Created (in state)
  Resource D: Failed (NOT in state)
  Resource E: Not attempted

Resolution:
  1. Fix the error (permissions, quota, etc.)
  2. Run terraform apply again
  3. Terraform creates only D and E
```

---

## Troubleshooting Provider Issues

```bash
# Check provider version
terraform version

# Upgrade providers
terraform init -upgrade

# Clear provider cache
rm -rf .terraform/providers/
terraform init

# Use specific provider version
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "= 5.30.0"  # Exact version
    }
  }
}
```

---

## Troubleshooting State Issues

```bash
# List resources in state
terraform state list

# Show resource details
terraform state show aws_instance.web

# Pull remote state locally
terraform state pull > state.json

# Check state file format
python3 -m json.tool terraform.tfstate > /dev/null
# If this fails, state is corrupt
```

---

## Debugging Plan Differences

```bash
# Show detailed plan with JSON
terraform plan -json | jq .

# Compare config to state
terraform show -json | jq '.values.root_module.resources'

# Show what will change
terraform plan -json | jq 'select(.type == "planned_change")'
```

---

## Targeted Operations for Debugging

```bash
# Plan/apply only specific resources
terraform plan -target=aws_instance.web
terraform apply -target=aws_instance.web

# Useful for:
#   - Isolating failing resources
#   - Testing changes incrementally
#   - Working around dependency issues

# Warning: Targeted apply can leave state inconsistent
# Always do a full plan afterwards
```

---

## Error Handling Best Practices

- Always run `terraform validate` before `plan`
- Review plan output carefully before `apply`
- Use `-out=tfplan` to save plans
- Enable state locking for team environments
- Keep provider versions pinned
- Use `TF_LOG` for debugging, not in production
- Maintain state backups (S3 versioning)
- Test changes in dev before prod

---

## CI/CD Error Handling

```bash
#!/bin/bash
set -euo pipefail

terraform init -input=false

terraform plan -input=false -out=tfplan \
  -detailed-exitcode 2>&1 | tee plan_output.txt

EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ]; then
  echo "No changes needed"
elif [ $EXIT_CODE -eq 2 ]; then
  echo "Changes detected, applying..."
  terraform apply -input=false tfplan
else
  echo "Plan failed!"
  exit 1
fi
```

---

## Chapter Summary

- Configuration errors are caught by `terraform validate`
- Provider errors come from cloud API failures
- State errors include locks, corruption, and mismatches
- Use `TF_LOG=DEBUG` for detailed debugging output
- Separate provider and core logging is available
- Partial failures are handled by re-running `apply`
- Always save plan files with `-out` flag
- Use targeted operations to isolate issues
- Implement pre-apply validation in CI/CD pipelines
