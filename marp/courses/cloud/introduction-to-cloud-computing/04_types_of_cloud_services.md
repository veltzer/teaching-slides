---
tags:
  - infrastructure:cloud
  - infrastructure:iaas
  - infrastructure:paas
level: beginner
category: cloud
audience:
  - audiences:developers
  - audiences:sysadmins
  - audiences:devops
  - audiences:managers

---
# Types of Cloud Services

---

## The Service Model Spectrum
- From maximum control to maximum convenience
- IaaS: you manage the most
- PaaS: provider manages infrastructure
- SaaS: provider manages everything
- FaaS: provider manages all except your code

---

## Infrastructure as a Service (IaaS)
- Rent virtual machines, storage, networks
- You manage the OS, runtime, and applications
- Maximum control and flexibility
- Examples: EC2, Azure VMs, Google Compute Engine
- Closest to traditional on-premises

---

## IaaS Responsibilities
- Provider: physical hardware, networking, virtualization
- Customer: OS, patches, runtime, application, data
- Most control but most management burden
- Good for lift-and-shift migrations
- Good for custom or legacy workloads

---

## Platform as a Service (PaaS)
- Deploy applications without managing infrastructure
- Provider manages OS, runtime, middleware
- You manage the application code and data
- Examples: AWS Elastic Beanstalk, Azure App Service, Heroku
- Faster development and deployment

---

## PaaS Responsibilities
- Provider: hardware, OS, runtime, middleware
- Customer: application code, data, configuration
- Less control but less management
- Great for web applications and APIs
- Developers focus on code, not servers

---

## Software as a Service (SaaS)
- Ready-to-use applications over the internet
- Provider manages everything
- You use the application and manage your data
- Examples: Gmail, Salesforce, Office 365, Slack
- Subscription model, no installation

---

## SaaS Characteristics
- Accessible via web browser
- Automatic updates and patches
- Multi-tenant architecture
- Subscription or usage-based pricing
- Minimal IT involvement

---

## Function as a Service (FaaS)
- Serverless compute model
- Upload code, provider runs it
- No servers to provision or manage
- Pay only when code executes
- Examples: AWS Lambda, Azure Functions, Google Cloud Functions

---

## FaaS Characteristics
- Event-driven execution
- Automatic scaling (zero to thousands)
- Millisecond billing granularity
- Stateless by design
- Maximum abstraction from infrastructure

---

## Comparing Service Models
- IaaS: "Give me a machine, I'll handle the rest"
- PaaS: "Give me a platform, I'll write the code"
- SaaS: "Give me a working application"
- FaaS: "Run my function when triggered"
- Each has its place in a cloud strategy

---

## Shared Responsibility Across Models
- IaaS: customer manages most, provider manages least
- PaaS: responsibility shifts toward provider
- SaaS: provider manages almost everything
- FaaS: provider manages all runtime aspects
- Security responsibility shifts accordingly

---

## Choosing the Right Model
- Legacy applications: often start with IaaS
- New web applications: PaaS is efficient
- End-user tools: SaaS when available
- Event-driven workloads: FaaS
- Most organizations use a mix of all models

---

## Beyond the Core Models
- CaaS: Containers as a Service (ECS, AKS, GKE)
- DBaaS: Database as a Service (RDS, Cloud SQL)
- AIaaS: AI as a Service (SageMaker, Vertex AI)
- The "as a Service" model extends everywhere
- Each removes a layer of management burden
