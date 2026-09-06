---
tags:
  - infrastructure:cloud
  - infrastructure:aws
  - practices:security
level: beginner
category: cloud
audience:
  - audiences:developers
  - audiences:sysadmins
  - audiences:managers

---

# Identity and Access Management

---

## IAM Model

![iam_model](svg/courses/cloud/introduction-to-aws/05_identity_and_access_management/iam_model.svg)

---

## Security in AWS
- Security is the top priority
- Built into every service
- Shared responsibility model
- IAM is the foundation
- Free to use

---

## AWS IAM Overview
- Identity and Access Management
- Controls who can do what in AWS
- Authentication (who are you?)
- Authorization (what can you do?)
- Global service (not Region-specific)

---

## IAM Root User
- Created when you first set up AWS account
- Full access to everything
- Should NOT be used for daily tasks
- Enable MFA immediately
- Use only for account-level tasks (billing, support plan)

---

## Root User Best Practices
- Create IAM admin user for daily work
- Enable MFA on root account
- Do not create access keys for root
- Store root credentials securely
- Use only when absolutely required

---

## IAM Users
- Individual identity within AWS
- Unique credentials (password, access keys)
- Assigned permissions via policies
- One user per person (no sharing)
- Can have console and/or programmatic access

---

## Console vs Programmatic Access
- Console: username + password + optional MFA
- Programmatic: access key ID + secret access key
- CLI and SDK use access keys
- Can have both types simultaneously
- Access keys should be rotated regularly

---

## IAM Groups
- Collection of IAM users
- Attach policies to groups, not individual users
- Users inherit group permissions
- A user can belong to multiple groups
- Examples: Developers, Admins, ReadOnly

---

## IAM Group Best Practices
- Create groups by job function
- Attach policies to groups, not users
- Use multiple groups for overlapping responsibilities
- Groups cannot be nested
- Every user should be in at least one group

---

## IAM Entity Relationships

![iam_entity_relationships](svg/courses/cloud/introduction-to-aws/05_identity_and_access_management/iam_entity_relationships.svg)

---

## IAM Roles
- Temporary credentials for trusted entities
- No permanent credentials (no passwords or keys)
- Assumed by users, services, or external identities
- Credentials automatically rotated
- Preferred over long-lived access keys

---

## When to Use Roles
- EC2 instances accessing S3 or DynamoDB
- Lambda functions calling other AWS services
- Cross-account access
- Federated users (SAML, OIDC)
- Never embed access keys in application code

---

## IAM Policies Overview
- JSON documents defining permissions
- Attached to users, groups, or roles
- Evaluated together to determine access
- Explicit Deny always wins
- Default: all actions denied

---

## Policy Structure
- Version: policy language version
- Statement: one or more permission blocks
- Effect: Allow or Deny
- Action: which API calls (e.g., s3:GetObject)
- Resource: which AWS resources (ARN)
- Condition: optional constraints

---

## Policy Example

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::my-bucket/*"
  }]
}
```

---

## Types of Policies
- AWS Managed: pre-built by AWS (e.g., AmazonS3ReadOnlyAccess)
- Customer Managed: you create and maintain
- Inline: embedded directly in a user/group/role
- Prefer AWS Managed when they fit
- Customer Managed for custom requirements

---

## Policy Evaluation Logic
1. All requests start as denied
1. Evaluate all applicable policies
1. Any explicit Deny -> access denied
1. Any Allow -> access granted
1. No Allow found -> access denied (implicit deny)

---

## Policy Evaluation Flowchart

![policy_evaluation_logic](svg/courses/cloud/introduction-to-aws/05_identity_and_access_management/policy_evaluation_logic.svg)

---

## Least Privilege Principle
- Grant only the permissions needed
- Start with minimal access
- Add permissions as needed
- Use IAM Access Analyzer to find unused permissions
- Regularly review and trim permissions

---

## Multi-Factor Authentication
- Something you know (password)
- Something you have (MFA device)
- Virtual MFA (Google Authenticator, Authy)
- Hardware MFA (YubiKey, Gemalto)
- Required for root user, recommended for all

---

## IAM Access Keys
- Pair: Access Key ID + Secret Access Key
- Used for CLI and SDK access
- Never share or commit to code
- Rotate regularly
- Use IAM roles instead when possible

---

## IAM Password Policy
- Set minimum password length
- Require specific character types
- Enable password expiration
- Prevent password reuse
- Apply to all IAM users

---

## AWS Organizations
- Manage multiple AWS accounts centrally
- Consolidated billing across accounts
- Service Control Policies (SCPs)
- Organizational Units (OUs)
- Account-level isolation for security

---

## Organizations Structure

![organizations_structure](svg/courses/cloud/introduction-to-aws/05_identity_and_access_management/organizations_structure.svg)

---

## Service Control Policies
- Guardrails for accounts in an Organization
- Restrict which services and actions are allowed
- Applied to OUs or individual accounts
- Do not grant permissions, only restrict
- Even account root user is restricted by SCPs

---

## SCP Example: Deny Unapproved Regions

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "DenyNonApprovedRegions",
    "Effect": "Deny",
    "Action": "*",
    "Resource": "*",
    "Condition": {
      "StringNotEquals": {
        "aws:RequestedRegion": [
          "us-east-1",
          "eu-west-1"
        ]
      }
    }
  }]
}
```

---

## AWS IAM Identity Center
- Successor to AWS SSO
- Single sign-on for multiple AWS accounts
- Integrate with corporate directory (Active Directory)
- Assign permissions across accounts
- One login for all AWS accounts

---

## Security Best Practices Summary
- Enable MFA everywhere
- Use roles instead of access keys
- Apply least privilege
- Use groups to assign permissions
- Rotate credentials regularly
- Monitor with CloudTrail
- Use IAM Access Analyzer
