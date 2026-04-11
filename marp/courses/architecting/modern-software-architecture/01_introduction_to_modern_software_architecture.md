---
tags:
  - concepts:architecture
  - concepts:microservices
  - concepts:design-patterns
level: advanced
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Introduction to Modern Software Architecture

---
## What Is Software Architecture?

![what_is_software_architecture](svg/courses/architecting/modern-software-architecture/01_introduction_to_modern_software_architecture/what_is_software_architecture.svg)

---
## Why Architecture Matters

- Determines the long-term maintainability of a system
- Impacts team velocity, deployment speed, and operational cost
- Poor architecture creates technical debt that compounds over time
- Good architecture enables change without rewriting the system

---
## The Monolithic Architecture

- A single deployable unit containing all functionality
- Shared memory space and a single database
- All modules compiled and deployed together
- The traditional default for most applications

---
## Monolith Diagram

![monolith_diagram](svg/courses/architecting/modern-software-architecture/01_introduction_to_modern_software_architecture/monolith_diagram.svg)

---
## Advantages of the Monolith

- Simple to develop initially
- Easy to test end-to-end
- Straightforward deployment as a single artifact
- Low operational overhead for small teams
- No network latency between components

---
## Disadvantages of the Monolith

- Codebase grows large and hard to understand
- A single bug can bring down the entire application
- Scaling requires replicating the whole system
- Technology choices are locked in for all modules
- Deployment of one change requires redeploying everything

---
## The Path to Microservices

- Monoliths become harder to maintain as organizations grow
- Teams step on each other when working in the same codebase
- Deployment frequency decreases as risk increases
- The need for independent scaling drives decomposition

---
## Architecture Evolution

![architecture_evolution](svg/courses/architecting/modern-software-architecture/01_introduction_to_modern_software_architecture/architecture_evolution.svg)

---
## What Are Microservices?

- An architectural style where a system is composed of small, independent services
- Each service runs in its own process and communicates over a network
- Services are organized around business capabilities
- Each service can be deployed, scaled, and updated independently

---
## Microservices Diagram

![microservices_diagram](svg/courses/architecting/modern-software-architecture/01_introduction_to_modern_software_architecture/microservices_diagram.svg)

---
## Key Characteristics of Microservices

- Single responsibility per service
- Decentralized data management
- Independent deployability
- Lightweight communication protocols
- Designed for failure and resilience

---
## Monolith vs Microservices Comparison

| Aspect | Monolith | Microservices |
|--------|----------|---------------|
| Deployment | Single unit | Independent services |
| Scaling | Vertical | Horizontal per service |
| Technology | Uniform stack | Polyglot |
| Team structure | Shared codebase | Service ownership |
| Complexity | In the code | In the infrastructure |

---
## The Transition Journey

![the_transition_journey](svg/courses/architecting/modern-software-architecture/01_introduction_to_modern_software_architecture/the_transition_journey.svg)

---
## Modular Monolith as a Stepping Stone

![modular_monolith](svg/courses/architecting/modern-software-architecture/01_introduction_to_modern_software_architecture/modular_monolith.svg)

---
## Service-Oriented Architecture (SOA)

![soa_architecture](svg/courses/architecting/modern-software-architecture/01_introduction_to_modern_software_architecture/soa_architecture.svg)

---
## SOA vs Microservices

| Aspect | SOA | Microservices |
|--------|-----|---------------|
| Service size | Large, coarse-grained | Small, fine-grained |
| Communication | `ESB`, `SOAP` | `REST`, `gRPC`, messaging |
| Data | Shared databases common | Database per service |
| Governance | Centralized | Decentralized |

---
## When to Choose Microservices

- Large teams that need to work independently
- Different parts of the system have different scaling needs
- Business domains are well understood and bounded
- Organization can invest in operational infrastructure

---
## When to Stay with a Monolith

- Small teams with limited operational expertise
- The domain is not well understood yet
- Rapid prototyping and early-stage products
- Low traffic with no need for independent scaling

---
## What Are Architectural Drivers?

- Forces that shape the architecture of a system
- Include functional requirements, quality attributes, and constraints
- Help architects make informed decisions
- Provide a rationale for every design choice

---
## Categories of Architectural Drivers

![categories_of_architectural_drivers](svg/courses/architecting/modern-software-architecture/01_introduction_to_modern_software_architecture/categories_of_architectural_drivers.svg)

---
## Quality Attributes Defined

- Non-functional requirements that measure system quality
- Often expressed as measurable scenarios
- Examples: `availability`, `scalability`, `security`, `performance`
- They drive the most important architectural decisions

---
## Common Quality Attributes

- `Availability` - system uptime and recovery time
- `Scalability` - ability to handle increased load
- `Performance` - response time and throughput
- `Security` - protection of data and access control
- `Maintainability` - ease of making changes
- `Testability` - ease of validating behavior

---
## Quality Attribute Scenarios

- A structured way to specify quality attributes
- Components of a scenario:
    - Source: who or what generates the stimulus
    - Stimulus: the event or condition
    - Artifact: the part of the system affected
    - Environment: the conditions under which it occurs
    - Response: what the system does
    - Measure: how success is quantified

---
## Example Quality Attribute Scenario

- Source: A user
- Stimulus: Submits a search request
- Artifact: Search service
- Environment: Normal operation under peak load
- Response: Returns results to the user
- Measure: Within 200 milliseconds for the 95th percentile

---
## The Quality Attribute Triangle

![the_quality_attribute_triangle](svg/courses/architecting/modern-software-architecture/01_introduction_to_modern_software_architecture/the_quality_attribute_triangle.svg)

---
## Architectural Trade-Offs

- No architecture can optimize every quality attribute
- Improving one attribute often degrades another
- Architects must understand and document trade-offs
- Stakeholder priorities determine which attributes win

---
## Classic Trade-Off: Consistency vs Availability

- In distributed systems, you cannot have both perfectly
- Strong consistency may require blocking requests during failures
- High availability may return stale data
- The `CAP` theorem formalizes this constraint

---
## Classic Trade-Off: Performance vs Security

- Encryption and authorization add processing overhead
- Detailed audit logging impacts throughput
- Network segmentation adds latency
- The right balance depends on the threat model

---
## Classic Trade-Off: Simplicity vs Flexibility

- More abstractions enable future change but add complexity now
- Over-engineering wastes time if requirements do not change
- Under-engineering creates costly rework when they do
- Start simple and refactor when the need becomes clear

---
## Trade-Off Analysis Framework

1. Identify the key quality attributes for the system
1. Rank them by stakeholder priority
1. Map each architectural decision to affected attributes
1. Document which attributes benefit and which suffer
1. Validate with stakeholders before committing

---
## Architecture Decision Records (ADR)

- A lightweight document capturing one architectural decision
- Includes context, decision, status, and consequences
- Creates a decision log that future developers can reference
- Prevents revisiting settled decisions without new information

---
## ADR Template

```markdown
## ADR-001: Use Event-Driven Communication

**Status:** Accepted

**Context:**
Services need to communicate without tight coupling.

**Decision:**
Use an event broker for inter-service communication.

**Consequences:**
- Reduced coupling between services
- Added complexity in debugging message flows
```

---
## Evaluating Architecture: ATAM

- `Architecture Tradeoff Analysis Method`
- A structured evaluation of software architecture
- Identifies risks, sensitivity points, and trade-off points
- Brings architects and stakeholders together

---
## ATAM Process Overview

![atam_process_overview](svg/courses/architecting/modern-software-architecture/01_introduction_to_modern_software_architecture/atam_process_overview.svg)

---
## Fitness Functions

- Automated checks that validate architectural properties
- Inspired by evolutionary architecture concepts
- Examples:
    - Dependency checks to prevent cyclic imports
    - Performance benchmarks that run in `CI/CD`
    - Security scans that block vulnerable dependencies

---
## Conway's Law

- "Organizations which design systems are constrained to produce designs which are copies of the communication structures of these organizations"
- Team structure influences system architecture
- Microservices work best when teams align with service boundaries
- Inverse Conway Maneuver: restructure teams to get the architecture you want

---
## Conway's Law Illustrated

![conway_s_law_illustrated](svg/courses/architecting/modern-software-architecture/01_introduction_to_modern_software_architecture/conway_s_law_illustrated.svg)

---
## The Role of the Software Architect

- Translates business goals into technical decisions
- Communicates architecture to all stakeholders
- Balances short-term delivery with long-term sustainability
- Continuously evaluates and evolves the architecture

---
## Architecture Is Not a One-Time Activity

- Requirements evolve and so must the architecture
- New technologies create new opportunities and risks
- Monitoring production systems reveals architectural weaknesses
- Regular architecture reviews keep the system healthy

---
## Evolutionary Architecture

- Architecture that supports guided, incremental change
- Uses fitness functions to enforce invariants
- Embraces change rather than trying to predict the future
- Small, reversible decisions are preferred over big, irreversible ones

---
## Key Principles of Modern Architecture

- Design for failure, not just for success
- Prefer loose coupling and high cohesion
- Automate everything: builds, tests, deployments, monitoring
- Measure and observe before optimizing
- Make decisions reversible whenever possible

---
## Summary

- Modern architecture is a spectrum from monoliths to microservices
- Quality attributes drive the most important design decisions
- Every architectural choice involves trade-offs
- Document decisions using ADRs and validate with ATAM
- Align team structure with system boundaries
- Architecture must evolve with the system and organization
