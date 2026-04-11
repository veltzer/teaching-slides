---
tags:
  - infrastructure:cloud
  - concepts:architecture
level: intermediate
category: cloud
audience:
  - audiences:developers
  - audiences:architects
  - audiences:devops

---
# Introduction

---

## Why Cloud Architecture Matters
- Cloud is not just someone else's computer
- New environment demands new thinking
- Old patterns do not translate directly
- Proper architecture saves money and pain
- Architecture mistakes are expensive to fix later

---

## Cloud vs On-Premises Architecture
- On-premises: design for peak capacity
- Cloud: design for elasticity
- On-premises: vertical scaling
- Cloud: horizontal scaling preferred
- Cloud: failure is expected, design for it

---

## Advantages of Cloud Computing
- Elastic scaling to actual demand
- Global deployment in minutes
- Pay only for what you consume
- Managed services reduce operational burden
- Rapid experimentation at low cost

---

## The Cost of Getting It Wrong
- Over-architected: too complex, too expensive
- Under-architected: outages, poor performance
- Lift-and-shift without rethinking: worst of both worlds
- Cloud-naive patterns: huge bills
- Architecture reviews prevent these mistakes

---

## Well-Architected Apps: Basic Principles
- Design for failure (everything fails eventually)
- Decouple components (loose coupling)
- Think horizontally (scale out, not up)
- Automate everything
- Use managed services where possible

---

## Design for Failure
- Assume any component can fail at any time
- No single points of failure
- Graceful degradation over hard crashes
- Retry with backoff and circuit breakers
- Test failure scenarios regularly

---

## Decouple Components
- Components should communicate through well-defined interfaces
- Queues between producers and consumers
- Events for asynchronous communication
- Each component scales independently
- Changes to one component don't cascade

---

## Think Horizontally
- Prefer many small instances over few large ones
- Stateless services scale easily
- Shared-nothing architecture
- Distribute across Availability Zones
- Load balancers in front of everything

---

## Automate Everything
- Infrastructure as Code for all resources
- Automated deployments and rollbacks
- Auto-healing (replace failed instances)
- Automated scaling based on metrics
- No manual SSH into production machines

---

## Use Managed Services
- Don't run what the cloud provider can run for you
- Managed databases, queues, caches, search
- Lower operational burden
- Built-in high availability and backups
- Focus engineering on business logic

---

## First Example: A Simple Web App
- Load balancer in front
- Auto-scaled web tier (stateless)
- Managed database backend (Multi-AZ)
- Static assets in object storage + CDN
- This pattern handles most web applications

---

## Scaling the Simple Web App
- Add read replicas for database reads
- Add caching layer (ElastiCache/Memcached)
- Move sessions to external store (Redis/DynamoDB)
- Background jobs via queues
- Each change addresses a specific bottleneck

---

## Architecture Decision Process
1. Identify the requirements (functional and non-functional)
1. Consider multiple options
1. Evaluate trade-offs (cost, complexity, performance)
1. Document the decision and rationale
1. Review and revisit as requirements change

---

## The Twelve-Factor App
- Methodology for building cloud-native applications
- Codebase in version control
- Config in environment, not code
- Stateless processes
- Port binding, disposability
- Foundation for well-architected cloud apps

---

## Non-Functional Requirements in the Cloud
- Availability: what uptime do you need? (99.9% vs 99.99%)
- Scalability: how many users, requests, data volume?
- Latency: acceptable response time?
- Durability: can you afford to lose data?
- Cost: what is the budget?

---

## Trade-Offs Are Everywhere
- Cost vs performance
- Consistency vs availability (CAP theorem)
- Complexity vs resilience
- Vendor lock-in vs productivity
- Every architecture decision involves trade-offs

---

## Cost as an Architecture Constraint
- Cloud makes cost a first-class architecture concern
- Right architecture can save 10x on cloud bills
- Wrong architecture can bankrupt you
- Always estimate cost during design
- Revisit cost assumptions regularly

---

## The Well-Architected Framework
- AWS Well-Architected Framework (6 pillars)
- Azure Well-Architected Framework (5 pillars)
- GCP Architecture Framework
- Common themes: reliability, security, cost, performance
- Use as a checklist for architecture reviews

---

## Architecture Documentation
- Architecture Decision Records (ADRs)
- Document the decision, context, and rationale
- Lightweight format (1 page per decision)
- Version controlled alongside code
- Future team members understand why

---

## Anti-Patterns to Avoid
- Treating cloud like a data center
- Ignoring cost in architecture decisions
- Building everything from scratch
- Single region, single AZ deployments
- Tight coupling between all components

---

## Operational Excellence in the Cloud
- Automate operations (runbooks, scripts)
- Monitor everything
- Learn from failures (blameless post-mortems)
- Make small, reversible changes
- Anticipate and prepare for failure

---

## Reliability Principles
- Test recovery procedures
- Automatically recover from failure
- Scale horizontally to increase availability
- Stop guessing capacity
- Manage change through automation

---

## Performance Efficiency
- Democratize advanced technologies (managed services)
- Go global in minutes
- Use serverless architectures where appropriate
- Experiment more often
- Consider mechanical sympathy (match tech to workload)

---

## Course Roadmap
- Identity and security
- Compute: renting and managing machines
- Scalability patterns
- Storage, queues, and data
- Serverless and containers
- Disaster recovery and caching
- Advanced patterns and services
