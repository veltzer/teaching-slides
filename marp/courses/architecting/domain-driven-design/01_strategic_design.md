---
tags:
  - concepts:domain-driven-design
level: advanced
category: architecture
audience:
  - audiences:architects
  - audiences:developers

---
# Strategic Domain-Driven Design

---
## What This Course Covers

- DDD is two halves: strategic (the big picture) and tactical (the building blocks)
- This chapter: strategic — bounded contexts, language, context maps
- Later chapters: tactical building blocks, integration with CQRS/ES, sagas, refactoring

---
## What DDD Is

- A philosophy of software development centered on the business domain
- Eric Evans' 2003 book "Domain-Driven Design"
- Bridges the gap between domain experts and developers
- Especially valuable for complex domains where the model isn't obvious

---
## Why DDD

- Software for complex domains needs careful modeling
- "Just write code" results in models that don't match reality
- DDD provides a vocabulary and techniques to align code with domain
- Strategic DDD scales better than ad-hoc design

---
## The Domain

- The problem space the software addresses
- "We sell shoes online" is a domain
- Within it: catalog, ordering, fulfillment, returns, accounting, marketing
- Each is a distinct area with its own concepts

---
## Subdomains

- A domain divides into subdomains
- **Core**: what differentiates the business
- **Supporting**: necessary but not differentiating
- **Generic**: solved problems (auth, billing, search)
- Invest most in the core; buy or use libraries for generic

---
## Bounded Context

- A boundary within which a particular domain model applies
- Inside: one set of terms, one model, one consistency rule
- Outside: different terms, different model
- The unit of "this is one team's responsibility"

---
## Bounded Contexts in Practice

![bounded_context](svg/courses/architecting/domain-driven-design/01_strategic_design/bounded_context.svg)

---
## Why Bounded Contexts

- Without them, every concept becomes "global" — `User` means everything
- With them, `User` means one specific thing in this context
- Different contexts can have different fields and rules for the same name
- Translation happens at the boundary

---
## A Concrete Example

- In Sales context: `Customer` has order history and lifetime value
- In Shipping context: `Customer` has delivery addresses
- In Billing context: `Customer` has payment methods and credit limit
- Three different `Customer` models; three different services

---
## Ubiquitous Language

- Each bounded context has its own vocabulary
- Inside a context: domain experts and developers speak the same language
- The code reflects the language: class names, method names, variables
- "Place an order" in conversation = `place_order` in code

---
## Building the Ubiquitous Language

- Workshops with domain experts
- Glossaries of terms (per context)
- Examples and counter-examples
- Iterate as understanding deepens
- Treat as a living document

---
## Context Mapping

- Documents how bounded contexts relate
- Names the kind of relationship
- Useful for planning integrations
- A diagram + descriptions

---
## Common Context Map Relationships

- **Customer/Supplier**: upstream provides, downstream consumes; downstream's needs influence upstream
- **Conformist**: downstream adopts upstream's model wholesale (no influence)
- **Anti-Corruption Layer (ACL)**: downstream translates upstream's model
- **Open Host Service**: upstream provides a clean public protocol
- **Published Language**: a shared schema between two contexts

---
## Anti-Corruption Layer

- A translator between bounded contexts
- Maps incoming terms into your context's language
- Prevents another context's vocabulary from polluting yours
- Often implemented as a thin module per integration

---
## ACL Example

- Sales emits `OrderPlaced` with fields `customer_id`, `items`, `address`
- Billing only cares about `customer_id` and total amount
- The Billing ACL maps Sales' event into Billing's `BillingRequest`
- Billing's domain language stays clean

---
## Core Domain Focus

- Identify the core domain — what makes the business different
- Invest most engineering energy there
- Buy, use libraries, or simplify in supporting/generic subdomains
- "Differentiation matters; commodity doesn't"

---
## Domain Vision Statement

- A short paragraph describing the core domain
- What's important; what's not
- Why this domain matters to the business
- Aligns the team on priorities

---
## Big Ball of Mud

- The anti-pattern: no clear boundaries, no consistent language
- Every concept entangled with every other
- The default outcome without strategic design
- DDD's strategic design is the antidote

---
## Strategic Patterns Recap

- Bounded contexts as the unit
- Ubiquitous language inside each
- Context maps for integrations
- ACL where vocabularies meet
- Core domain prioritization

---
## Anti-Patterns

- "One unified model for everything"
- Bounded contexts that match the org chart by accident, not design
- Skipping strategic design and starting with tactical building blocks
- Glossaries that nobody updates

---
## Summary

- Strategic DDD is about boundaries, language, and integration
- Bounded contexts are the unit; each has its own ubiquitous language
- Context maps document the relationships
- ACLs translate at boundaries
- Core domain gets the engineering investment
