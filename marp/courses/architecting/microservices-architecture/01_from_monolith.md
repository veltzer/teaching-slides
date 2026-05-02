---
tags:
  - concepts:microservices
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# From Monolith to Microservices

---
## What This Course Is About

- Microservices: an application split into small, independently deployable services
- Each service owns a slice of the domain
- Services communicate over the network
- This course covers the design choices and trade-offs

---
## Monolith vs Microservices

![monolith_to_services](svg/courses/architecting/microservices-architecture/01_from_monolith/monolith_to_services.svg)

---
## A Monolith

- One codebase, one deployment
- One database
- One team or several teams sharing the codebase
- Simple to start; everything in one place

---
## When the Monolith Hurts

- Multiple teams stepping on each other's commits
- A change in one feature requires testing all features
- Releases are coordinated across the whole company
- Scaling means scaling everything, even cold paths
- The codebase exceeds anyone's mental capacity

---
## What Microservices Promise

- Independent deployment per service
- Independent scaling per service
- Team autonomy: own a service end-to-end
- Tech diversity: pick the right tool per service
- Fault isolation: one service's bug doesn't take down the rest

---
## What Microservices Cost

- Distributed system complexity (network, partial failure)
- More moving parts to operate
- Cross-service data consistency is hard
- Local debugging becomes distributed tracing
- Testing across service boundaries is non-trivial

---
## When Microservices Are Right

- Multiple teams that need to work independently
- Different parts of the system have different scaling profiles
- The domain is large enough to be split meaningfully
- Operational maturity to handle distributed systems

---
## When Microservices Are Wrong

- Small team, small domain
- Operations team isn't ready for distributed systems
- The domain isn't well understood yet — boundaries shift
- Premature optimization for scale you don't have

---
## A Realistic Trade-Off

- Monolith: simple to build, hard to scale organizationally
- Microservices: complex to build, scale to many teams
- The right answer is somewhere on the spectrum, often both at once
- "Modular monolith" is a real and useful intermediate

---
## The Modular Monolith

- One deployable, but internally split into modules with clear boundaries
- Modules don't share data; they communicate through well-defined interfaces
- Easy to extract a module into a microservice later if needed
- Many teams stop here intentionally

---
## Migration Patterns

- **Big bang**: rewrite as microservices — almost always wrong
- **Strangler fig**: extract one capability at a time
- **Branch-by-abstraction**: build the new alongside the old, gradually flip traffic
- The strangler fig is the safe, common path

---
## Strangler Fig in One Slide

- Identify a capability to extract
- Build a new service for that capability
- Route traffic to the new service for some users, fall back to the monolith for others
- Increase the new service's traffic share until it's 100%
- Remove the capability from the monolith

---
## Anti-Patterns

- **Distributed monolith**: services exist but are tightly coupled
- **Nano-services**: too many tiny services, more pipe than substance
- **Database-per-table**: services that share a database aren't really separate
- **Microservices because Netflix**: the architecture has to fit your team and domain

---
## Course Roadmap

- Chapter 2: principles and what makes a service "micro"
- Chapter 3-4: decomposition and bounded contexts
- Chapter 5-6: communication and APIs
- Chapter 7: data
- Chapter 8-9: discovery and resilience
- Chapter 10-12: deployment, testing, observability
- Chapter 13-14: composition and scaling

---
## Summary

- Microservices solve specific problems and create new ones
- The choice is not all-or-nothing
- Modular monolith is a real intermediate
- Migration is incremental — strangler fig, not big bang
- The rest of the course is the design choices that follow from "yes, microservices"
