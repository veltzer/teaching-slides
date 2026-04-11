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
# What Is Cloud Computing

---

## Definition
- On-demand delivery of IT resources over the internet
- Pay-as-you-go pricing model
- No need to own or manage physical hardware
- Servers, storage, databases, networking as a service
- Fundamental shift in how IT is consumed

---

## NIST Definition
- National Institute of Standards and Technology
- Five essential characteristics
- Three service models
- Four deployment models
- The industry-standard definition

---

## On-Demand Self-Service
- Provision resources without human interaction
- No need to call or email an IT department
- Web console, CLI, or API
- Resources available in minutes
- Developer self-service

---

## Broad Network Access
- Available over the network (internet or private)
- Standard mechanisms and protocols
- Accessible from any device
- Laptops, phones, tablets, servers
- No special client software required

---

## Resource Pooling
- Provider serves multiple customers from shared resources
- Multi-tenant model
- Resources dynamically assigned and reassigned
- Customer generally does not control exact location
- Economies of scale for the provider

---

## Rapid Elasticity
- Scale up and down quickly
- Capabilities appear unlimited to the consumer
- Provision and release automatically
- Handle traffic spikes without pre-planning
- Pay only for what you actually use

---

## Measured Service
- Resource usage monitored, controlled, and reported
- Transparency for provider and consumer
- Pay-per-use billing
- Metering at the appropriate level (storage, CPU, bandwidth)
- Enables cost optimization

---

## Before the Cloud
- Buy and rack physical servers
- Weeks or months to provision
- Capacity planning guesswork
- Large upfront capital expenditure
- Underutilized or overloaded hardware

---

## The Problem with Traditional IT
- Over-provision: waste money on idle resources
- Under-provision: performance problems and outages
- Hardware refresh cycles every 3-5 years
- Dedicated staff for maintenance and patching
- Slow to respond to business changes

---

## How Cloud Solves This
- Convert CapEx to OpEx
- Provision in minutes, not months
- Scale to actual demand
- No hardware to manage or refresh
- Focus on applications, not infrastructure

---

## Cloud vs Virtualization
- Virtualization: run multiple VMs on one physical server
- Cloud: virtualization + self-service + metering + elasticity
- Virtualization is a building block of cloud
- Cloud adds automation, APIs, and billing
- Private virtualization is not cloud by itself

---

## Cloud vs Hosting
- Traditional hosting: fixed servers, fixed price
- Cloud: elastic resources, usage-based pricing
- Hosting: manual scaling (call support)
- Cloud: API-driven, automatic scaling
- Cloud: global infrastructure out of the box

---

## Cloud Service Categories
- Compute: virtual machines, containers, functions
- Storage: object, block, file
- Networking: virtual networks, DNS, CDN
- Databases: relational, NoSQL, caching
- And hundreds more specialized services

---

## Who Uses Cloud?
- Startups: launch without capital investment
- Enterprises: modernize and scale
- Government: improve citizen services
- Education: research computing on demand
- Every industry and company size

---

## Cloud Adoption Trends
- Majority of enterprise workloads now in cloud
- Multi-cloud strategies are common
- Cloud-native development is the default for new apps
- Edge computing extends cloud to the periphery
- AI/ML services driving new adoption

---

## Cloud Terminology
- Instance: a virtual server
- Region: geographic data center cluster
- Availability Zone: isolated data center
- Tenant: a customer using shared resources
- SLA: Service Level Agreement

---

## More Cloud Terminology
- Provisioning: creating and configuring resources
- Elasticity: automatic scaling to demand
- Orchestration: automated arrangement of services
- Workload: an application or service running in the cloud
- API: Application Programming Interface (how you talk to cloud)

---

## Cloud vs Colocation
- Colocation: rent space in a data center, bring your hardware
- Cloud: provider owns all hardware, you rent capacity
- Colocation: you manage everything except the building
- Cloud: provider manages hardware and often software
- Colocation suits regulated industries with specific hardware needs

---

## Cloud Myths
- "Cloud is always cheaper" (not always, depends on usage)
- "Cloud is not secure" (often more secure than on-premises)
- "Cloud means losing control" (you control what matters)
- "Migrating to cloud is easy" (it requires planning)
- Evaluate each myth against your specific context

---

## Real-World Cloud Scale
- Netflix: streams to 200M+ subscribers from AWS
- Spotify: runs entirely on GCP
- LinkedIn: migrated to Azure
- Government agencies: increasing cloud adoption
- Cloud handles the world's most demanding workloads

---

## When Cloud May Not Be the Answer
- Ultra-low latency requirements (microseconds)
- Strict data sovereignty preventing any cloud use
- Predictable, steady workloads (sometimes cheaper on-premises)
- Legacy systems with no migration path
- Always evaluate, don't assume cloud is automatic

---

## Summary
- Cloud = on-demand, elastic, metered IT resources
- Five NIST characteristics define cloud
- Solves the problems of traditional IT
- Used by organizations of all sizes
- Foundation for modern application development
