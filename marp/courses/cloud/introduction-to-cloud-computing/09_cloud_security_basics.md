---
tags:
  - infrastructure:cloud
  - practices:security
level: beginner
category: cloud
audience:
  - audiences:developers
  - audiences:sysadmins
  - audiences:devops
  - audiences:managers

---

# Cloud Security Basics

---

## Identity and Access Management
- Control who can access what
- Authentication: verify identity
- Authorization: grant permissions
- Every cloud provider has an IAM service
- Foundation of cloud security

---

## Least Privilege Principle
- Grant only the minimum permissions needed
- Start with no access, add as required
- Review and trim permissions regularly
- Applies to users, services, and applications
- Prevents blast radius of compromised credentials

---

## Multi-Factor Authentication
- Something you know (password)
- Something you have (phone, hardware key)
- Dramatically reduces account compromise risk
- Should be mandatory for all users
- Especially critical for admin accounts

---

## Encryption at Rest
- Data stored in encrypted form
- Protect against physical theft or unauthorized access
- Provider-managed or customer-managed keys
- Transparent to applications (handled by service)
- Enable for all storage: disks, databases, objects

---

## Encryption in Transit
- Protect data moving between services
- TLS/HTTPS for all communications
- VPN for site-to-site connections
- Mutual TLS for service-to-service
- Prevent eavesdropping and man-in-the-middle

---

## Encryption at Rest and in Transit

![encryption](svg/courses/cloud/introduction-to-cloud-computing/09_cloud_security_basics/encryption_at_rest_and_transit.svg)

---

## Key Management
- Centralized key management services (KMS)
- Create, rotate, and control access to keys
- Hardware Security Modules (HSM) for high security
- Automatic key rotation policies
- Audit key usage

---

## KMS Encryption Example

```bash
# Create a KMS key
aws kms create-key \
  --description "App encryption key"

# Encrypt data
aws kms encrypt \
  --key-id alias/my-app-key \
  --plaintext fileb://secret.txt \
  --output text --query CiphertextBlob
```

---

## Network Security in the Cloud
- Virtual Private Clouds for isolation
- Security Groups as instance-level firewalls
- Network ACLs for subnet-level control
- Private subnets for sensitive workloads
- VPN or private connectivity to on-premises

---

## Firewall and Access Control
- Default deny: block everything, allow explicitly
- Layered security (defense in depth)
- Web Application Firewalls (WAF) for HTTP traffic
- DDoS protection services
- Network segmentation

---

## Defense in Depth

![defense](svg/courses/cloud/introduction-to-cloud-computing/09_cloud_security_basics/defense_in_depth.svg)

---

## Logging and Monitoring
- Log all API calls and access
- Monitor for unusual activity
- Set up alerts for security events
- Retain logs for compliance and forensics
- Centralized log management

---

## Compliance and Regulatory Considerations
- GDPR: European data protection
- HIPAA: healthcare data in the US
- SOC 2: service organization controls
- PCI DSS: payment card data
- Cloud providers offer compliance tools and certifications

---

## Data Residency
- Some regulations require data in specific countries
- Choose cloud Regions accordingly
- Understand where replicas and backups are stored
- Provider compliance documentation covers this
- Multi-Region does not mean every Region

---

## Security Automation
- Infrastructure as Code for security configurations
- Automated compliance scanning
- Auto-remediation of policy violations
- Security as part of CI/CD pipeline
- Reduce human error through automation

---

## Incident Response in the Cloud
- Have a plan before incidents occur
- Leverage cloud logging for investigation
- Isolate compromised resources quickly
- Forensics using snapshots and logs
- Practice incident response regularly
