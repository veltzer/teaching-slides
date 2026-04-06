# Cloud Security Attacks: Exploiting Misconfigured Cloud Environments

---
## Why Cloud Security Matters

- Over 94% of enterprises use cloud services (Flexera 2024)
- Cloud misconfigurations are the #1 cause of cloud data breaches
- The shared responsibility model means customers are responsible for securing their data and configurations
- Cloud breaches cost an average of $4.75 million (IBM 2023)
- "The cloud is secure. Your configuration is not."

---
## Shared Responsibility Model

```diagram
┌──────────────────────────────────────────────────────────┐
│          Cloud Shared Responsibility Model                │
│                                                          │
│                 IaaS        PaaS        SaaS             │
│  ┌──────────┬──────────┬──────────┬──────────┐          │
│  │ Data     │ CUSTOMER │ CUSTOMER │ CUSTOMER │          │
│  ├──────────┼──────────┼──────────┼──────────┤          │
│  │ App      │ CUSTOMER │ CUSTOMER │ PROVIDER │          │
│  ├──────────┼──────────┼──────────┼──────────┤          │
│  │ Runtime  │ CUSTOMER │ PROVIDER │ PROVIDER │          │
│  ├──────────┼──────────┼──────────┼──────────┤          │
│  │ OS       │ CUSTOMER │ PROVIDER │ PROVIDER │          │
│  ├──────────┼──────────┼──────────┼──────────┤          │
│  │ Network  │ SHARED   │ PROVIDER │ PROVIDER │          │
│  ├──────────┼──────────┼──────────┼──────────┤          │
│  │ Physical │ PROVIDER │ PROVIDER │ PROVIDER │          │
│  └──────────┴──────────┴──────────┴──────────┘          │
│                                                          │
│  "Security OF the cloud" = Provider                      │
│  "Security IN the cloud" = Customer                      │
│                                                          │
│  Most breaches occur in the CUSTOMER responsibility area │
└──────────────────────────────────────────────────────────┘
```

---
## Misconfigured S3 Buckets

```bash
┌──────────────────────────────────────────────────────────┐
│          S3 Bucket Misconfiguration Attack                │
│                                                          │
│  Default S3 bucket: Private (since April 2023)           │
│  BUT: Many legacy buckets are still misconfigured        │
│                                                          │
│  Common misconfigurations:                               │
│  - Public read access (anyone can list/download)         │
│  - Public write access (anyone can upload/delete!)       │
│  - Overly permissive bucket policies                     │
│  - ACLs granting access to "AllUsers" or                 │
│    "AuthenticatedUsers"                                  │
│  - Missing encryption at rest                            │
│  - No access logging enabled                             │
└──────────────────────────────────────────────────────────┘
```

```bash
# Check if an S3 bucket is publicly accessible
aws s3 ls s3://target-bucket --no-sign-request
# If this returns contents, the bucket is PUBLIC

# Check bucket ACL
aws s3api get-bucket-acl --bucket target-bucket --no-sign-request

# Check bucket policy
aws s3api get-bucket-policy --bucket target-bucket --no-sign-request

# Enumerate S3 buckets from company name
# Tools: cloud_enum, S3Scanner, bucket-finder
python3 cloud_enum.py -k companyname -l results.txt
```

---
## Notable S3 Bucket Breaches

| Company         | Year | Records Exposed        | Data Type                      |
|-----------------|------|------------------------|--------------------------------|
| US Military     | 2017 | 1.8 billion            | Social media monitoring data   |
| Verizon         | 2017 | 6 million              | Customer PINs and records      |
| Dow Jones       | 2017 | 2.2 million            | Customer personal data         |
| Tesla           | 2018 | Unknown                | Telemetry and manufacturing    |
| Capital One     | 2019 | 106 million            | Credit applications (via SSRF) |
| Twitch          | 2021 | Entire source code     | Code + earnings data           |
| Microsoft       | 2023 | 38 TB                  | Employee data, passwords       |

---
## Securing S3 Buckets

```json
// Secure S3 bucket policy
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "DenyPublicAccess",
            "Effect": "Deny",
            "Principal": "*",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::my-bucket",
                "arn:aws:s3:::my-bucket/*"
            ],
            "Condition": {
                "Bool": {
                    "aws:SecureTransport": "false"
                }
            }
        }
    ]
}
```

```bash
# Block all public access at account level
aws s3control put-public-access-block \
    --account-id 123456789012 \
    --public-access-block-configuration \
    "BlockPublicAcls=true,IgnorePublicAcls=true,\
     BlockPublicPolicy=true,RestrictPublicBuckets=true"

# Enable default encryption
aws s3api put-bucket-encryption --bucket my-bucket \
    --server-side-encryption-configuration '{
        "Rules": [{
            "ApplyServerSideEncryptionByDefault": {
                "SSEAlgorithm": "aws:kms",
                "KMSMasterKeyID": "alias/my-key"
            }
        }]
    }'

# Enable access logging
aws s3api put-bucket-logging --bucket my-bucket \
    --bucket-logging-status '{
        "LoggingEnabled": {
            "TargetBucket": "my-log-bucket",
            "TargetPrefix": "s3-access-logs/"
        }
    }'
```

---
## GCS Bucket Misconfigurations

```bash
# Google Cloud Storage enumeration
# Check if bucket is publicly accessible
curl https://storage.googleapis.com/target-bucket/

# List bucket contents
gsutil ls gs://target-bucket/

# Check IAM policy
gsutil iam get gs://target-bucket/

# Common misconfigurations:
# - allUsers (anyone on the internet)
# - allAuthenticatedUsers (any Google account)
# Both are effectively PUBLIC access

# Secure a GCS bucket
gsutil iam ch -d allUsers gs://my-bucket
gsutil iam ch -d allAuthenticatedUsers gs://my-bucket

# Enable uniform bucket-level access (disable ACLs)
gsutil uniformbucketlevelaccess set on gs://my-bucket
```

---
## IAM Privilege Escalation

```python
┌──────────────────────────────────────────────────────────┐
│          AWS IAM Privilege Escalation Paths               │
│                                                          │
│  1. Overly permissive IAM policies                       │
│     User has: iam:CreatePolicy + iam:AttachUserPolicy    │
│     -> Can create admin policy and attach to self        │
│                                                          │
│  2. Lambda function abuse                                │
│     User has: lambda:CreateFunction + iam:PassRole       │
│     -> Create Lambda with admin role, execute it         │
│                                                          │
│  3. EC2 instance role abuse                              │
│     User has: ec2:RunInstances + iam:PassRole            │
│     -> Launch EC2 with admin role, access from instance  │
│                                                          │
│  4. CloudFormation abuse                                 │
│     User has: cloudformation:CreateStack + iam:PassRole  │
│     -> Create stack that provisions admin resources      │
│                                                          │
│  5. STS assume role                                      │
│     Misconfigured trust policy allows cross-account      │
│     or cross-service role assumption                     │
│                                                          │
│  6. SSM parameter store                                  │
│     Secrets stored in Parameter Store with overly        │
│     permissive access policies                           │
└──────────────────────────────────────────────────────────┘
```

```bash
# Enumerate IAM permissions for current user
aws iam list-attached-user-policies --user-name myuser
aws iam list-user-policies --user-name myuser

# Check what you can do (automated enumeration)
# Using enumerate-iam tool
python3 enumerate-iam.py --access-key AKIAI... --secret-key wJalr...

# Using Pacu (AWS exploitation framework)
pacu
> import_keys --all
> run iam__enum_permissions
> run iam__privesc_scan
```

---
## IAM Best Practices

```json
// Least privilege IAM policy example
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::specific-bucket/prefix/*",
            "Condition": {
                "IpAddress": {
                    "aws:SourceIp": "10.0.0.0/8"
                },
                "StringEquals": {
                    "aws:RequestedRegion": "us-east-1"
                }
            }
        }
    ]
}
```

```c
┌──────────────────────────────────────────────────────────┐
│  IAM Security Best Practices                             │
├──────────────────────────────────────────────────────────┤
│  [ ] Use least privilege (specific actions + resources)  │
│  [ ] Avoid wildcard (*) in actions and resources         │
│  [ ] Use conditions to restrict access (IP, region, MFA) │
│  [ ] Enable MFA for all IAM users (especially root)      │
│  [ ] Use IAM roles instead of long-lived access keys     │
│  [ ] Rotate access keys regularly (90 days max)          │
│  [ ] Use IAM Access Analyzer to find unused permissions  │
│  [ ] Enable CloudTrail for all API calls                 │
│  [ ] Use SCPs (Service Control Policies) in AWS Org      │
│  [ ] Remove unused users, roles, and policies            │
└──────────────────────────────────────────────────────────┘
```

---
## IMDS Attacks (169.254.169.254)

```bash
┌──────────────────────────────────────────────────────────┐
│          Instance Metadata Service (IMDS) Attack          │
│                                                          │
│  Every cloud VM has a metadata service at:               │
│  http://169.254.169.254 (link-local address)             │
│                                                          │
│  This service provides:                                  │
│  - Instance ID, region, availability zone                │
│  - Network configuration                                │
│  - IAM role temporary credentials (!)                    │
│  - User data scripts (may contain secrets!)              │
│                                                          │
│  Attack scenario:                                        │
│  SSRF vulnerability -> Request to 169.254.169.254        │
│  -> Extract IAM role credentials -> Access AWS APIs      │
│                                                          │
│  This is how Capital One was breached (2019):            │
│  - SSRF in WAF -> IMDS -> IAM credentials               │
│  - Used credentials to access S3 buckets                 │
│  - 106 million customer records exposed                  │
└──────────────────────────────────────────────────────────┘
```

```bash
# Exploiting IMDS v1 (no authentication required)
# From within a compromised EC2 instance or via SSRF:

# Get instance metadata
curl http://169.254.169.254/latest/meta-data/

# Get IAM role name
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/

# Get temporary credentials for the role
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/MyRole
# Returns: AccessKeyId, SecretAccessKey, Token

# Get user-data (may contain secrets!)
curl http://169.254.169.254/latest/user-data/
```

---
## IMDS v2: The Defense

```bash
# IMDSv2 requires a session token (PUT request first)
# This prevents SSRF exploitation because:
# 1. Requires a PUT request (most SSRF only allows GET)
# 2. Token has TTL and hop limit (1 hop = can't reach from containers)

# IMDSv2 workflow:
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" \
    -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")

curl -H "X-aws-ec2-metadata-token: $TOKEN" \
    http://169.254.169.254/latest/meta-data/

# Enforce IMDSv2 on all EC2 instances
aws ec2 modify-instance-metadata-options \
    --instance-id i-1234567890abcdef0 \
    --http-tokens required \
    --http-put-response-hop-limit 1 \
    --http-endpoint enabled

# Enforce IMDSv2 for all new instances via SCP
# Or use AWS Config rule: ec2-imdsv2-check

# GCP equivalent: Requires Metadata-Flavor header
curl -H "Metadata-Flavor: Google" \
    http://169.254.169.254/computeMetadata/v1/instance/
# (This header requirement provides some SSRF protection)

# Azure equivalent
curl -H "Metadata: true" \
    "http://169.254.169.254/metadata/instance?api-version=2021-02-01"
```

---
## IMDS Across Cloud Providers

| Provider | URL                          | Authentication                    | Version |
|----------|------------------------------|-----------------------------------|---------|
| AWS      | 169.254.169.254              | IMDSv2: PUT token required        | v1/v2   |
| GCP      | 169.254.169.254              | Metadata-Flavor header required   | v1      |
| Azure    | 169.254.169.254              | Metadata: true header required    | Various |
| DigitalOcean| 169.254.169.254           | None                              | v1      |
| Oracle   | 169.254.169.254              | Authorization header optional     | v2      |

---
## Serverless Injection

```bash
┌──────────────────────────────────────────────────────────┐
│          Serverless (Lambda/Function) Injection            │
│                                                          │
│  Serverless functions are not immune to injection!       │
│                                                          │
│  Attack vectors:                                         │
│  - Event data injection (API Gateway, S3, SNS triggers)  │
│  - Environment variable exfiltration                     │
│  - Temporary credential theft                            │
│  - Dependency vulnerabilities in function packages       │
│  - Cold start timing attacks                             │
└──────────────────────────────────────────────────────────┘
```

```python
# VULNERABLE: Lambda function with OS command injection
import subprocess
import json

def handler(event, context):
    # User input from API Gateway
    filename = event['queryStringParameters']['file']

    # DANGEROUS: User input in shell command
    result = subprocess.run(
        f"cat /tmp/{filename}",
        shell=True, capture_output=True, text=True
    )
    return {
        'statusCode': 200,
        'body': result.stdout
    }

# Attacker: ?file=test;env
# Reveals all environment variables including:
# AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN

# SECURE: Validate input, avoid shell execution
import os

def handler(event, context):
    filename = event['queryStringParameters']['file']

    # Validate: only allow alphanumeric + limited chars
    if not filename.replace('-', '').replace('_', '').isalnum():
        return {'statusCode': 400, 'body': 'Invalid filename'}

    # Use safe file operations (no shell)
    filepath = os.path.join('/tmp', os.path.basename(filename))
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        return {'statusCode': 200, 'body': content}
    except FileNotFoundError:
        return {'statusCode': 404, 'body': 'Not found'}
```

---
## Serverless Security Best Practices

```bash
┌──────────────────────────────────────────────────────────┐
│  Serverless Security Checklist                           │
├──────────────────────────────────────────────────────────┤
│  [ ] Least privilege IAM role per function               │
│  [ ] No secrets in environment variables (use Secrets    │
│      Manager or Parameter Store)                         │
│  [ ] Input validation on all event data                  │
│  [ ] Dependency scanning (npm audit, pip-audit)          │
│  [ ] VPC attachment for functions accessing internal     │
│      resources                                           │
│  [ ] Short timeout values (prevent abuse)                │
│  [ ] Concurrency limits (prevent DoS)                    │
│  [ ] Layer/dependency pinning                            │
│  [ ] Enable X-Ray tracing for monitoring                 │
│  [ ] No shell execution (subprocess, exec)               │
└──────────────────────────────────────────────────────────┘
```

---
## Cross-Tenant Vulnerabilities

```bash
┌──────────────────────────────────────────────────────────┐
│          Cross-Tenant Attack Scenarios                    │
│                                                          │
│  1. Shared infrastructure exploits                       │
│     - Side-channel attacks on shared hardware            │
│     - Container escape in multi-tenant environments      │
│     - Shared database instance with weak isolation       │
│                                                          │
│  2. Misconfigured cross-account access                   │
│     - IAM roles with overly permissive trust policies    │
│     - Shared S3 buckets between accounts                 │
│     - Cross-account Lambda invocation                    │
│                                                          │
│  3. Resource enumeration                                 │
│     - Predictable resource naming (account ID in ARN)    │
│     - S3 bucket name guessing                            │
│     - Snapshot and AMI sharing misconfigurations         │
│                                                          │
│  4. SaaS tenant isolation failures                       │
│     - Broken tenant identification in multi-tenant apps  │
│     - Shared API keys across tenants                     │
│     - Database row-level security bypass                 │
└──────────────────────────────────────────────────────────┘
```

```json
// VULNERABLE: Cross-account role trust policy
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": {"AWS": "*"},  // ANY AWS account!
        "Action": "sts:AssumeRole"
    }]
}

// SECURE: Specific account with external ID
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": {"AWS": "arn:aws:iam::123456789012:root"},
        "Action": "sts:AssumeRole",
        "Condition": {
            "StringEquals": {
                "sts:ExternalId": "unique-secret-id-12345"
            }
        }
    }]
}
```

---
## Cloud Security Scanning Tools

| Tool           | Type          | Cloud Support       | License      |
|----------------|---------------|---------------------|--------------|
| ScoutSuite     | Multi-cloud   | AWS, Azure, GCP     | Open source  |
| Prowler        | AWS-focused   | AWS (primary)       | Open source  |
| Checkov        | IaC scanning  | AWS, Azure, GCP     | Open source  |
| CloudSploit    | Multi-cloud   | AWS, Azure, GCP     | Open source  |
| Trivy          | Multi-purpose | AWS, containers     | Open source  |
| CSPM tools     | Platform      | Varies              | Commercial   |

---
## ScoutSuite: Multi-Cloud Auditing

```bash
# Install ScoutSuite
pip install scoutsuite

# Scan AWS account
scout aws --profile my-profile

# Scan specific AWS services
scout aws --services s3 iam ec2 rds lambda

# Scan GCP project
scout gcp --project-id my-project

# Scan Azure subscription
scout azure --cli

# ScoutSuite generates an HTML report with findings:
# - Public S3 buckets
# - Overly permissive IAM policies
# - Unencrypted EBS volumes
# - Security group misconfigurations
# - CloudTrail not enabled
# - MFA not enabled for root
```

---
## Prowler: AWS Security Assessment

```bash
# Install Prowler
pip install prowler

# Run full AWS security assessment
prowler aws

# Run specific checks
prowler aws --checks s3_bucket_public_access \
    iam_root_mfa_enabled \
    ec2_instance_imdsv2_enabled

# Run checks aligned to compliance frameworks
prowler aws --compliance cis_2.0_aws    # CIS Benchmark
prowler aws --compliance pci_3.2.1       # PCI DSS
prowler aws --compliance hipaa           # HIPAA

# Output as JSON for automation
prowler aws -M json -o /tmp/prowler-results/

# Common critical findings:
# - Root account without MFA
# - S3 buckets with public access
# - Security groups allowing 0.0.0.0/0 on port 22
# - CloudTrail not enabled in all regions
# - Access keys older than 90 days
# - IMDSv1 still enabled on EC2 instances
```

---
## Infrastructure as Code (IaC) Security

```bash
# Checkov: Scan Terraform/CloudFormation before deployment
pip install checkov

# Scan Terraform files
checkov -d ./terraform/

# Scan CloudFormation templates
checkov -f cloudformation-template.yaml

# Scan Kubernetes manifests
checkov -d ./k8s/

# Example Checkov findings:
# FAILED: CKV_AWS_18 - S3 bucket logging not enabled
# FAILED: CKV_AWS_19 - S3 bucket encryption not enabled
# FAILED: CKV_AWS_21 - S3 versioning not enabled
# FAILED: CKV_AWS_145 - EBS encryption not enabled
```

```hcl
// Terraform: Secure S3 bucket configuration
resource "aws_s3_bucket" "secure_bucket" {
  bucket = "my-secure-bucket"
}

resource "aws_s3_bucket_public_access_block" "secure_bucket" {
  bucket = aws_s3_bucket.secure_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "secure_bucket" {
  bucket = aws_s3_bucket.secure_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.my_key.arn
    }
  }
}

resource "aws_s3_bucket_versioning" "secure_bucket" {
  bucket = aws_s3_bucket.secure_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_logging" "secure_bucket" {
  bucket = aws_s3_bucket.secure_bucket.id

  target_bucket = aws_s3_bucket.log_bucket.id
  target_prefix = "s3-access-logs/"
}
```

---
## Cloud Attack Detection

```python
┌──────────────────────────────────────────────────────────┐
│  Cloud-Specific Detection Rules                          │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Monitor for:                                            │
│  - Console login from unusual locations/IPs              │
│  - API calls from new IP addresses                       │
│  - Root account usage (should be near-zero)              │
│  - IAM policy changes (especially iam:*)                 │
│  - S3 bucket policy modifications                        │
│  - Security group changes (especially ingress 0.0.0.0/0) │
│  - CloudTrail disabled or modified                       │
│  - New IAM users or access keys created                  │
│  - Cross-region resource creation                        │
│  - Large data transfers to external destinations         │
│  - IMDS access from unexpected applications              │
└──────────────────────────────────────────────────────────┘
```

```bash
# AWS CloudTrail: Query for suspicious activity
# Using Athena to query CloudTrail logs

# Find root account API calls (should be rare)
# SELECT * FROM cloudtrail_logs
# WHERE useridentity.type = 'Root'
# AND eventtime > '2024-01-01'

# Find IAM privilege escalation attempts
# SELECT * FROM cloudtrail_logs
# WHERE eventsource = 'iam.amazonaws.com'
# AND eventname IN ('CreatePolicy', 'AttachUserPolicy',
#                    'AttachRolePolicy', 'CreateRole')

# AWS GuardDuty: Automated threat detection
aws guardduty create-detector --enable
# Detects: cryptocurrency mining, credential exfiltration,
# unusual API calls, unauthorized access attempts
```

---
## Cloud Security Checklist

```bash
┌──────────────────────────────────────────────────────────┐
│  Cloud Security Comprehensive Checklist                  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Identity & Access:                                      │
│  [ ] MFA on all accounts (especially root/owner)         │
│  [ ] Least privilege IAM policies                        │
│  [ ] No long-lived access keys (use roles)               │
│  [ ] Regular access reviews and key rotation             │
│                                                          │
│  Storage:                                                │
│  [ ] Block public access on all buckets                  │
│  [ ] Encryption at rest and in transit                   │
│  [ ] Access logging enabled                              │
│  [ ] Versioning for critical data                        │
│                                                          │
│  Compute:                                                │
│  [ ] IMDSv2 enforced on all instances                    │
│  [ ] Security groups: least privilege, no 0.0.0.0/0     │
│  [ ] Regular patching and AMI updates                    │
│  [ ] No secrets in user-data or env variables            │
│                                                          │
│  Monitoring:                                             │
│  [ ] CloudTrail/Activity Log enabled in all regions      │
│  [ ] GuardDuty/Security Center enabled                   │
│  [ ] Alerting on critical configuration changes          │
│  [ ] Regular security posture assessments                │
│                                                          │
│  IaC & Pipeline:                                         │
│  [ ] IaC security scanning (Checkov, tfsec)              │
│  [ ] No hardcoded secrets in code/templates              │
│  [ ] Immutable infrastructure where possible             │
│  [ ] Drift detection for configuration changes           │
└──────────────────────────────────────────────────────────┘
```

---
## Key Takeaways

- Cloud misconfigurations are the leading cause of cloud breaches -- not provider vulnerabilities
- The shared responsibility model means security IN the cloud is your job
- Publicly accessible storage buckets (S3, GCS) remain one of the most common misconfigurations
- IAM privilege escalation through overly permissive policies is a critical attack path
- IMDS attacks (169.254.169.254) can leak IAM credentials via SSRF -- enforce IMDSv2
- Serverless functions are not immune to injection attacks -- validate all event inputs
- Open source tools (ScoutSuite, Prowler, Checkov) provide excellent security posture visibility
- IaC scanning catches misconfigurations before deployment (shift left)
- CloudTrail/Activity Logs and threat detection services are essential for incident detection
- Regular automated security assessments should be part of cloud operations
