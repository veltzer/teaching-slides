---
tags:
  - security:threat-modeling
  - concepts:diagrams
level: intermediate
category: security
audience:
  - audiences:developers
  - audiences:architects

---

# Data Flow Diagrams

---

## What This Chapter Covers

- The five DFD elements
- Drawing multi-level DFDs
- Identifying trust boundaries
- Tools and conventions
- DFDs for distributed systems

---

## Why DFDs?

- Threats are about how data moves and changes hands
- DFDs make those movements explicit
- They expose the trust boundaries where attacks occur
- Simple, language-agnostic, accessible to non-developers
- The starting point of nearly every threat methodology

---

## The Five DFD Elements

- External entity (a square) — actors outside your system
- Process (a circle) — code that transforms data
- Data store (parallel lines or open box) — databases, files, queues
- Data flow (arrow) — data moving between elements
- Trust boundary (dashed line) — where trust changes

---

## DFD Elements Visualized

![dfd_elements](svg/courses/security/threat-modeling/02_data_flow_diagrams/dfd_elements.svg)

---

## External Entity

- Anything outside your system that interacts with it
- Users, browsers, third-party APIs, partner services
- You cannot control them — you can only validate what they send
- Each external entity is a potential attacker
- Label them concretely: "Customer browser", "Stripe API"

---

## Process

- A unit of work that transforms or routes data
- Web services, microservices, scripts, batch jobs
- Each process has trust assumptions about its inputs
- Each process can be compromised — protect what it produces
- Granularity matters — too coarse hides threats, too fine is noisy

---

## Data Store

- Where data lives at rest: databases, caches, queues, file systems
- Each store has its own trust profile
- Threats against stores: tampering, disclosure, denial
- Different stores often live in different trust zones
- Note encryption, retention, access controls per store

---

## Data Flow

- An arrow showing data moving from A to B
- Label with what's flowing: "credit card", "session token", "order JSON"
- Direction matters — read vs write changes the threat profile
- Crosses trust boundaries — these are the high-risk flows
- Encryption status of the flow itself is a threat-relevant property

---

## Trust Boundary

- A dashed line where trust changes
- Network boundary — public internet vs internal network
- Process boundary — privilege escalation between processes
- Data boundary — sanitized vs unsanitized inputs
- Where threats live — almost every threat crosses a boundary

---

## Levels of Detail

- Level 0 (context) — system as a single bubble, external entities around it
- Level 1 — major subsystems and their interactions
- Level 2 — inside one subsystem, the processes and stores
- Deeper levels for complex subsystems
- Match the level to the threat-modeling task at hand

---

## Drawing Order Matters

- Start with external entities — who/what is on the outside?
- Add the system as one process or several
- Connect with data flows
- Mark the data stores touched
- Draw trust boundaries last — they emerge from the structure

---

## A Practical Walkthrough

- E-commerce checkout: user, web app, payment service, order DB
- External entity: user with browser
- Processes: web app, payment service
- Data store: order DB, payment-state cache
- Trust boundaries: between user and web app, between web app and payment service

---

## Anti-Patterns to Avoid

- Drawing UML class diagrams — wrong tool, no data flows
- Showing every method call — too low-level
- Skipping the data store labels — threats need specifics
- Hiding external dependencies — they're often the threat
- Inconsistent levels of detail across the same diagram

---

## DFDs for Distributed Systems

- Each microservice is a process — and a trust boundary if owned by another team
- Message queues are data stores with flow semantics
- API gateways are processes that mediate boundaries
- Service meshes implement trust at the platform layer
- Be explicit: which network call is mTLS, which is plaintext?

---

## DFDs and Cloud

- Managed services are external entities you partly trust
- IAM roles define who/what can act as a process
- Encryption-at-rest changes the data-store threat profile
- Cross-region flows cross legal trust boundaries
- Capture cloud-specific assumptions explicitly

---

## DFDs and APIs

- Each endpoint is a data flow with input and output
- Each endpoint has its own auth posture — capture it
- Public, authenticated, internal — three different trust levels
- Rate limits and quotas affect denial-of-service threats
- An API gateway sits at a major trust boundary

---

## Tools for DFDs

- Pen and whiteboard — fastest first pass
- draw.io / diagrams.net — free, web, exportable
- Lucidchart — collaborative, polished
- Microsoft Threat Modeling Tool — DFD plus STRIDE built in
- OWASP Threat Dragon — open-source, threat-aware

---

## Diagrams as Code

- PlantUML, Mermaid, Structurizr — text-based diagrams
- Live in the repo, version-controlled, reviewable
- Auto-generated images for docs and reviews
- Slower to draw initially; cheaper to maintain
- Recommended for teams that produce many threat models

---

## Keeping DFDs Current

- A DFD that doesn't match the system is worse than no DFD
- Update during design reviews; reject PRs that change architecture without updating
- Periodic audit: walk a recent change through the diagram
- If updates feel painful, the diagram is too detailed
- Aim for usable, not exhaustive

---

## Quality Checklist

- Every external entity reaches a process via a data flow
- Every process has at least one input and one output
- Every data store has at least one process reading or writing
- Every trust boundary marks a real change in trust
- The diagram fits on one screen at the chosen level

---

## Summary

- DFDs are the foundation of threat modeling
- Five elements: entity, process, store, flow, boundary
- Multi-level diagrams scale to complex systems
- Trust boundaries are where threats happen
- Maintainable diagrams beat exhaustive ones
