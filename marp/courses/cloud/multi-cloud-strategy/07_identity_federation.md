---
tags:
  - infrastructure:cloud
  - infrastructure:aws
  - infrastructure:azure
  - infrastructure:gcp
  - concepts:architecture
level: advanced
category: cloud
audience:
  - audiences:architects
  - audiences:managers

---
# Identity Federation in Multi-Cloud

---

## Why Identity Federation Matters
- Users need access to AWS, Azure, and GCP
- Separate credentials per cloud is unsustainable
- Security risk: credential sprawl and inconsistent policies
- Federation: single identity, multiple clouds
- Foundation for any multi-cloud strategy

---

## Identity Providers (IdP)
- Central authority for user identity
- Examples: Okta, Azure AD (Entra ID), Google Workspace, Ping Identity
- Supports protocols: SAML 2.0, OIDC, WS-Federation
- Single source of truth for users and groups
- Enforces MFA, conditional access, and session policies

---

## Single Sign-On Across Clouds
- User authenticates once against the IdP
- IdP issues tokens for each cloud provider
- No separate passwords per cloud
- Session management is centralized
- Reduces phishing risk and password fatigue

---

## SAML 2.0 Federation
- Industry standard for enterprise SSO
- IdP (e.g., Okta) sends SAML assertion to cloud SP
- Cloud provider trusts the IdP via metadata exchange
- Assertion contains user identity and group memberships
- Used primarily for console/browser access

---

## OIDC Federation
- Modern, token-based federation protocol
- Preferred for programmatic and workload identity
- IdP issues JWT tokens
- Cloud provider validates token against IdP JWKS endpoint
- Lighter weight than SAML, better for APIs

---

## AWS IAM Identity Center
- Centralized access for multiple AWS accounts
- Integrates with external IdPs via SAML or SCIM
- Permission sets define access per account
- Supports attribute-based access control (ABAC)
- Replaces the old AWS SSO service

---

## Microsoft Entra ID
- Microsoft identity platform (formerly Azure AD)
- Native IdP for Azure, also federates to AWS and GCP
- Supports SAML, OIDC, and WS-Federation
- Conditional Access policies for risk-based authentication
- B2B collaboration for cross-organization identity

---

## GCP Workload Identity Federation
- Allows external workloads to access GCP without service account keys
- Supports AWS, Azure, OIDC, and SAML identity providers
- Maps external identity to GCP IAM role
- No long-lived credentials stored outside GCP
- Preferred over exporting service account keys

---

## GCP Workload Identity Federation Config

```yaml
# Create a workload identity pool
gcloud iam workload-identity-pools create "multi-cloud-pool" \
  --location="global" \
  --display-name="Multi-Cloud Identity Pool"

# Add an AWS provider to the pool
gcloud iam workload-identity-pools providers create-aws \
  "aws-provider" \
  --location="global" \
  --workload-identity-pool="multi-cloud-pool" \
  --account-id="123456789012"

# Add an OIDC provider (e.g., Azure AD)
gcloud iam workload-identity-pools providers create-oidc \
  "azure-provider" \
  --location="global" \
  --workload-identity-pool="multi-cloud-pool" \
  --issuer-uri="https://login.microsoftonline.com/TENANT_ID/v2.0" \
  --allowed-audiences="api://my-app-id"
```

---

## Cross-Cloud IAM Mapping
- Map IdP groups to cloud-specific roles
- Example: "CloudAdmins" group -> AWS Admin role + Azure Contributor + GCP Editor
- Maintain mapping table in IaC (Terraform)
- Review mappings quarterly
- Principle of least privilege still applies per cloud

---

## Cross-Cloud Identity Federation

![identity](svg/courses/cloud/multi-cloud-strategy/07_identity_federation/cross_cloud_identity.svg)

---

## Workload Identity vs User Identity
- User identity: humans accessing consoles and APIs
- Workload identity: services calling other services across clouds
- Workload identity avoids storing secrets in code
- AWS: IAM roles for service accounts
- Azure: Managed Identity
- GCP: Workload Identity Federation

---

## Secrets Management Across Clouds
- Each cloud has a secrets manager (AWS Secrets Manager, Azure Key Vault, GCP Secret Manager)
- Challenge: applications may need secrets from multiple clouds
- Options: centralize in one vault or use cloud-native per provider
- HashiCorp Vault as a cross-cloud secrets engine
- Never store secrets in code, environment variables, or config files

---

## HashiCorp Vault for Multi-Cloud
- Single secrets management plane across all clouds
- Dynamic secrets: generates short-lived credentials on demand
- AWS, Azure, and GCP secrets engines built in
- Unified audit log for all secret access
- Supports auto-rotation and lease management

---

## Key Takeaways
- Use a single IdP (Okta, Entra ID) as the identity source of truth
- SAML for console access, OIDC for programmatic/workload access
- Workload Identity Federation eliminates long-lived cross-cloud credentials
- Map IdP groups to cloud roles consistently
- Centralize secrets management with Vault or use cloud-native per provider
