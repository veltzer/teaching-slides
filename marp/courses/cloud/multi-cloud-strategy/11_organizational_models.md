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
# Organizational Models for Multi-Cloud

## Mark Veltzer

## mark.veltzer@gmail.com

---

## People Before Technology
- Multi-cloud strategy fails without the right organizational structure
- Technology decisions are easier than people decisions
- Team structure shapes cloud architecture (Conway's Law)
- Skills gaps are the top blocker for multi-cloud adoption
- Invest in people as much as in platforms

---

## Conway's Law in Multi-Cloud
- Organizations design systems that mirror their communication structure
- Siloed cloud teams produce siloed cloud architectures
- Cross-functional teams produce integrated architectures
- Deliberately structure teams to get the architecture you want
- Inverse Conway Maneuver: design teams around desired architecture

---

## Common Organizational Models
1. Cloud-per-team: each team owns one cloud
1. Platform team: central team manages all clouds
1. Cloud Center of Excellence: advisory and governance body
1. Federated model: shared standards with team autonomy
1. Hybrid: combination of the above

---

## Cloud-Per-Team Model
- Team A uses AWS, Team B uses Azure, Team C uses GCP
- Simple: each team goes deep on one cloud
- Risk: silos, inconsistent practices, duplication of effort
- Knowledge does not transfer between teams
- Acceptable for initial adoption, problematic at scale

---

## Central Platform Team Model
- Dedicated team manages infrastructure across all clouds
- Provides standardized APIs, templates, and guardrails
- Application teams consume platform services
- Consistent governance and cost management
- Risk: platform team becomes a bottleneck

---

## Cloud Center of Excellence (CCoE)
- Advisory body, not an operational team
- Sets standards, best practices, and approved patterns
- Reviews architecture decisions across clouds
- Training and knowledge sharing
- Works alongside delivery teams, not above them

---

## CCoE Responsibilities
- Define multi-cloud architecture standards
- Evaluate and approve new cloud services
- Maintain reference architectures and templates
- Run training programs and certifications
- Conduct architecture reviews and provide guidance

---

## Federated Model
- Central team sets guardrails and standards
- Individual teams have autonomy within guardrails
- Balance between consistency and agility
- Platform team provides tools, not mandates
- Most successful model for large organizations

---

## Platform Team Structure
- Platform engineering: IaC, CI/CD, observability
- Security engineering: identity, compliance, policy
- FinOps: cost management and optimization
- SRE: reliability, incident response, DR
- Developer experience: self-service, documentation, onboarding

---

## Team Structure Models

![teams](svg/courses/cloud/multi-cloud-strategy/11_organizational_models/team_structure.svg)

---

## Self-Service Platforms
- Developers should not need to understand every cloud
- Provide abstracted interfaces: CLI, portal, API
- Internal Developer Platform (IDP): Backstage, Port, Humanitec
- Standardized deployment pipelines per workload type
- Reduce cognitive load while maintaining multi-cloud flexibility

---

## Skills and Training Strategy
- Each cloud requires specialized knowledge
- Full-stack multi-cloud expertise is rare and expensive
- Strategy: T-shaped skills (deep in one, broad across all)
- Certification paths: AWS SA, Azure SA, GCP PCA
- Cross-training rotations between cloud teams

---

## Training Investment
- Budget for certifications and training per engineer
- Hands-on labs are more effective than lectures alone
- Sandbox accounts for experimentation on each cloud
- Internal knowledge base and runbook library
- Lunch-and-learn sessions for cross-cloud topics

---

## Key Takeaways
- Organizational structure determines multi-cloud success or failure
- Federated model with a platform team scales best
- Cloud Center of Excellence provides governance without bottlenecks
- Invest in T-shaped skills: deep in one cloud, broad across all
- Self-service platforms reduce the multi-cloud skill burden on developers
