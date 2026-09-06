---
tags:
  - infrastructure:cloud
level: beginner
category: cloud
audience:
  - audiences:developers
  - audiences:sysadmins
  - audiences:devops
  - audiences:managers

---

# Cloud Deployment Models

---

## Four Deployment Models
- Public cloud
- Private cloud
- Hybrid cloud
- Multi-cloud
- Each serves different organizational needs

---

## Cloud Deployment Models

![deployment](svg/courses/cloud/introduction-to-cloud-computing/05_cloud_deployment_models/deployment_models.svg)

---

## Public Cloud
- Owned and operated by a third-party provider
- Shared infrastructure, multi-tenant
- Available to anyone over the internet
- Pay-as-you-go pricing
- Examples: AWS, Azure, GCP

---

## Public Cloud Advantages
- No upfront investment
- Elastic scaling
- Global reach
- Broad service catalog
- Provider handles all maintenance

---

## Public Cloud Concerns
- Data sovereignty and compliance
- Shared infrastructure (noisy neighbors)
- Vendor lock-in risk
- Less control over infrastructure
- Internet dependency

---

## Private Cloud
- Dedicated infrastructure for one organization
- On-premises or hosted by a provider
- Full control over security and compliance
- Higher cost, more customization
- Examples: VMware, OpenStack, AWS Outposts

---

## Private Cloud Advantages
- Complete control over infrastructure
- Customized security policies
- Meet strict regulatory requirements
- Predictable performance
- Data stays on your premises

---

## Private Cloud Disadvantages
- High upfront and ongoing costs
- Limited scalability compared to public
- Requires specialized staff
- Slower to innovate
- Hardware refresh responsibility

---

## Hybrid Cloud
- Combination of public and private cloud
- Workloads move between environments
- Connected via VPN or dedicated links
- Unified management where possible
- Best of both worlds (in theory)

---

## Hybrid Cloud Use Cases
- Sensitive data on-premises, compute in public cloud
- Burst to public cloud during peak demand
- Disaster recovery in public cloud
- Gradual migration to public cloud
- Regulatory requirements for some workloads

---

## Hybrid Cloud Architecture

![hybrid](svg/courses/cloud/introduction-to-cloud-computing/05_cloud_deployment_models/hybrid_cloud_architecture.svg)

---

## Multi-Cloud Strategy
- Using two or more public cloud providers
- Avoid vendor lock-in
- Best-of-breed service selection
- Geographic or regulatory requirements
- Risk mitigation

---

## Multi-Cloud Challenges
- Increased complexity in management
- Skills needed for multiple platforms
- Networking between clouds
- Inconsistent tooling and APIs
- Cost visibility across providers

---

## Choosing the Right Deployment Model
- Public: most workloads, cost-effective, scalable
- Private: strict compliance, legacy systems
- Hybrid: transition period, specific compliance needs
- Multi-cloud: vendor independence, best-of-breed
- Most organizations end up with a mix
