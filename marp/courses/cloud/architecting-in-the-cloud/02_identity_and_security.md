---
tags:
  - infrastructure:cloud
  - practices:security
  - concepts:architecture
level: intermediate
category: cloud
audience:
  - audiences:developers
  - audiences:architects
  - audiences:devops

---
# Identity and Security in the Cloud

---

## Security as a Foundation
- Security is not an afterthought
- Build security into architecture from day one
- Shared responsibility model
- Cloud gives you tools; you must use them
- Breaches are usually misconfiguration, not provider failure

---

## Identity is the New Perimeter
- Traditional: castle-and-moat (firewall around everything)
- Cloud: identity-based access control
- Every API call is authenticated and authorized
- No network location is inherently trusted
- Zero trust principles apply

---

## Zero Trust vs Perimeter Security

![zero_trust](svg/courses/cloud/architecting-in-the-cloud/02_identity_and_security/zero_trust_vs_perimeter.svg)

---

## Corporate Identity Mapping
- Map corporate identities to cloud identities
- Single Sign-On (SSO) via SAML or OIDC
- AWS IAM Identity Center, Azure AD, Google Workspace
- Users authenticate once, access all cloud resources
- Centralized user lifecycle management

---

## Federation
- Connect existing identity provider to cloud
- Active Directory, Okta, Auth0, Ping Identity
- Users don't need separate cloud credentials
- Roles assumed after federated authentication
- Reduces credential sprawl

---

## Service Accounts and Roles
- Applications need identity too
- Use cloud-native roles (IAM Roles, Managed Identities)
- No hardcoded credentials in code
- Temporary credentials, automatically rotated
- Principle of least privilege for every service

---

## EC2 IAM Role Trust Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {
      "Service": "ec2.amazonaws.com"
    },
    "Action": "sts:AssumeRole"
  }]
}
```

---

## Least Privilege at Scale
- Start with no permissions
- Add only what is needed
- Use policy conditions for fine-grained control
- Regular access reviews
- Automated detection of unused permissions

---

## Multi-Account Strategy
- Separate accounts for different purposes
- Production, staging, development, security, logging
- Blast radius containment
- Clear cost allocation
- AWS Organizations, Azure Management Groups

---

## Account Structure Example
1. Root/Management account (billing, organization)
1. Security account (CloudTrail, GuardDuty, SIEM)
1. Shared Services account (CI/CD, DNS, artifacts)
1. Production accounts (per product or team)
1. Development/Sandbox accounts (experimentation)

---

## Multi-Account Structure

![multi_account](svg/courses/cloud/architecting-in-the-cloud/02_identity_and_security/multi_account_structure.svg)

---

## Creating VPN with the Cloud
- Site-to-site VPN: connect on-premises to cloud
- Encrypted tunnel over public internet
- IPSec protocols
- Redundant tunnels for availability
- Quick to set up, but internet-dependent

---

## Dedicated Connections
- AWS Direct Connect, Azure ExpressRoute, GCP Interconnect
- Private, dedicated network link to cloud
- Lower latency, consistent performance
- Higher bandwidth (1 Gbps to 100 Gbps)
- More expensive, longer setup time

---

## When to Use VPN vs Dedicated Connect
- VPN: lower cost, quick setup, moderate bandwidth
- Dedicated: high bandwidth, low latency, consistency
- Many organizations start with VPN, add dedicated later
- Use both for redundancy
- Dedicated for production, VPN as backup

---

## VPN vs Direct Connect

![vpn_dc](svg/courses/cloud/architecting-in-the-cloud/02_identity_and_security/vpn_vs_direct_connect.svg)

---

## Working with Multiple Accounts
- Cross-account roles for access
- Centralized logging account
- Shared VPC / Transit Gateway for networking
- Service Catalog for approved resources
- Guardrails via Service Control Policies

---

## Network Security in the Cloud
- VPC isolation between workloads
- Security Groups and Network ACLs
- Private subnets for sensitive resources
- No public IPs unless necessary
- Defense in depth: multiple layers

---

## Encryption Everywhere
- Encrypt data at rest (KMS-managed keys)
- Encrypt data in transit (TLS everywhere)
- Encrypt data in use (confidential computing emerging)
- Managed key rotation
- Customer-managed vs provider-managed keys

---

## Secrets Management
- Never store secrets in code or environment variables
- Use Secrets Manager, Parameter Store, Key Vault
- Automatic rotation of database credentials
- Applications retrieve secrets at runtime
- Audit secret access

---

## Retrieve a Secret at Runtime

```bash
# Store a secret
aws secretsmanager create-secret \
  --name prod/db/password \
  --secret-string 'SuperSecret123!'

# Retrieve in application code (Python)
import boto3
client = boto3.client('secretsmanager')
resp = client.get_secret_value(
    SecretId='prod/db/password'
)
password = resp['SecretString']
```

---

## Security Monitoring
- CloudTrail / Activity Log for API auditing
- GuardDuty / Defender for threat detection
- Security Hub / Sentinel for centralized security posture
- Automated alerting on suspicious activity
- Incident response playbooks

---

## Zero Trust Architecture
- Never trust, always verify
- Verify every request regardless of network location
- Micro-segmentation: fine-grained access control
- Assume breach: minimize blast radius
- Cloud is ideal for zero trust implementation

---

## WAF and DDoS Protection
- Web Application Firewall: filter malicious HTTP traffic
- AWS WAF, Azure WAF, Cloud Armor
- DDoS protection: AWS Shield, Azure DDoS Protection
- Rate limiting and bot detection
- Layer 7 protection for web applications

---

## Security Automation
- Automated compliance scanning (Config, Policy)
- Auto-remediation of violations
- Infrastructure as Code for security configs
- Security in CI/CD pipeline
- Reduce human error through automation

---

## Compliance in Cloud Architecture
- Choose Regions based on data residency requirements
- Use compliance-certified services
- Implement audit logging from day one
- Regular compliance assessments
- Cloud providers provide compliance reports (SOC, ISO, etc.)

---

## API Security
- Authenticate all API calls
- Rate limiting and throttling
- API keys for external consumers
- OAuth 2.0 / JWT for user authentication
- Input validation at the API boundary

---

## Data Classification
- Classify data by sensitivity level
- Public, internal, confidential, restricted
- Apply controls based on classification
- Different encryption and access controls per level
- Retention policies based on classification

---

## Incident Response Planning
- Prepare before incidents occur
- Runbooks for common scenarios
- Automated evidence collection (snapshots, logs)
- Containment: isolate compromised resources
- Post-incident review and improvement

---

## Security Architecture Best Practices
- Identity-based access everywhere
- Encrypt everything by default
- Least privilege for all entities
- Network isolation for every tier
- Monitor, detect, and respond continuously
- Automate security controls
