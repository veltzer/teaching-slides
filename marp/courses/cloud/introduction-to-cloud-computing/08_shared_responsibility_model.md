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
# Shared Responsibility Model

---

## What is the Shared Responsibility Model?
- Cloud security is a shared effort
- Provider is responsible for security **of** the cloud
- Customer is responsible for security **in** the cloud
- Division depends on the service model
- Most critical concept in cloud security

---

## Shared Responsibility Model

![srm](svg/courses/cloud/introduction-to-cloud-computing/08_shared_responsibility_model/shared_responsibility_model.svg)

---

## Provider Responsibilities
- Physical data center security
- Hardware and networking infrastructure
- Hypervisor and virtualization layer
- Global network backbone
- Service availability and patching of managed services

---

## Customer Responsibilities
- Data classification and encryption
- Identity and access management
- Operating system patches (for IaaS)
- Application security
- Network and firewall configuration

---

## IaaS Responsibilities Split
- Provider: physical host, network, storage hardware
- Customer: guest OS, patches, application, data
- Customer: firewall rules and network config
- Customer: encryption of data at rest and in transit
- Most responsibility falls on the customer

---

## PaaS Responsibilities Split
- Provider: OS, runtime, middleware, patching
- Customer: application code, data, access control
- Less for the customer to manage
- Provider handles more of the security stack
- Customer still owns data security

---

## SaaS Responsibilities Split
- Provider: everything except customer data and access
- Customer: user access management
- Customer: data they input into the service
- Least responsibility for the customer
- But still responsible for proper use

---

## Responsibility by Service Type

![responsibility](svg/courses/cloud/introduction-to-cloud-computing/08_shared_responsibility_model/responsibility_by_service_type.svg)

---

## Why It Matters
- Misconfigured resources are the #1 cloud security issue
- Open S3 buckets, overly permissive IAM policies
- "It's in the cloud" does not mean "it's automatically secure"
- Understanding the model prevents breaches
- Each team must know their responsibilities

---

## Common Customer Mistakes
- Leaving storage publicly accessible
- Not enabling MFA
- Overly permissive IAM policies
- Not encrypting sensitive data
- Ignoring security group configurations

---

## Real-World Breaches
- Capital One (2019): misconfigured WAF on AWS
- Misconfigured S3 buckets: countless data exposures
- Exposed databases: no authentication enabled
- All were customer responsibility failures
- The cloud was not breached; the configuration was

---

## Compliance in the Cloud
- Provider holds certifications (SOC 2, ISO 27001, HIPAA)
- Customer must still configure for compliance
- Shared compliance responsibility
- Use provider compliance tools and reports
- Audit regularly

---

## Encryption Responsibilities
- Encryption at rest: customer enables and manages keys
- Encryption in transit: customer configures TLS/HTTPS
- Key management: customer controls who accesses keys
- Provider offers KMS (Key Management Service)
- Customer decides what to encrypt and how

---

## Best Practices
- Understand the model for every service you use
- Enable encryption everywhere
- Use IAM with least privilege
- Monitor and audit continuously
- Automate security configuration
