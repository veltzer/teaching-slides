---
tags:
  - architecture:saga
  - concepts:distributed-systems
level: advanced
category: architecture
audience:
  - audiences:architects
  - audiences:developers

---
# The Distributed Transactions Problem

---
## What This Chapter Covers

- ACID transactions and where they break
- Two-phase commit and why it does not scale
- The CAP theorem in practice
- Eventual consistency: contract, not compromise
- Why we need a different pattern for cross-service workflows

---
## ACID Transactions: The Comfort Zone

- **A**tomicity: all or nothing
- **C**onsistency: invariants hold before and after
- **I**solation: concurrent transactions don't see each other's intermediate state
- **D**urability: committed writes survive crashes
- A single-node relational database gives you all four

---
## ACID Across Service Boundaries

- Each service has its own database
- A business action touches multiple services
- Each service's commit is atomic locally
- The combined operation is **not** atomic
- Service A may commit and service B may fail

---
## A Concrete Failure

- "Place order" touches Inventory, Payments, Shipping
- Inventory commits the reservation
- Payments commits the charge
- Shipping is down
- Now: inventory reserved, money taken, no shipment scheduled
- Without coordination, we have an inconsistent system state

---
## Two-Phase Commit (2PC)

- A coordinator asks every participant: "Can you commit?"
- All participants must vote yes (prepare phase)
- Then the coordinator tells everyone: "Commit"
- If any participant votes no, everyone rolls back
- Single-decision atomicity across multiple participants

---
## Why 2PC Breaks Down

- **Blocking**: participants hold locks during prepare; high latency
- **Coordinator failure**: if the coordinator crashes mid-protocol, participants are stuck
- **Heuristic decisions**: timeouts force unsafe local choices
- **No fit for HTTP services**: long-held locks are incompatible with web-scale traffic
- **Vendor coupling**: requires participants that speak XA or similar

---
## The 2PC Tradeoff

- 2PC trades availability for consistency
- It only works when participants are tightly coupled and reliable
- Microservices are deliberately loosely coupled and individually fallible
- 2PC and microservices are an architectural mismatch

---
## CAP Theorem: A Reminder

- In the presence of a network partition, a system can guarantee at most two of:
    - **C**onsistency
    - **A**vailability
    - **P**artition tolerance
- Networks partition; you don't get to choose P
- Real choice: C or A under partition

---
## CAP in Microservices

- Cross-service communication is a network call
- A network call can fail or be slow
- Demanding strong consistency makes the system unavailable when one service is slow
- Demanding availability means accepting eventual consistency
- Most microservice systems pick A — and live with eventual consistency

---
## Eventual Consistency: The Contract

- After a finite time, all replicas/services converge to the same state
- During the window, observers may see inconsistent views
- The window is bounded under healthy operation
- It is not "eventual maybe" — it is a real guarantee

---
## Eventual Consistency vs No Consistency

- Eventual consistency is a guarantee with a deadline
- No consistency is just bugs
- The difference: explicit design, monitoring, and recovery for the inconsistent window
- Sagas are the design pattern that makes eventual consistency tractable

---
## Long-Running Business Processes

- "Place order" is not a single click — it's a multi-step process
- Reserve inventory → charge payment → notify warehouse → schedule shipping
- Each step takes seconds to minutes
- Holding a transaction across all of these is not feasible
- The process needs its own state machine, separate from any single database

---
## What a Long-Running Process Needs

- A way to record progress through the steps
- A way to handle one step's failure after another succeeded
- A way to recover from coordinator restarts
- A way to give up after enough retries
- A way to expose status to humans

---
## Cross-Bounded-Context Workflows

- A business process often spans multiple bounded contexts
- Sales bounded context, Inventory bounded context, Shipping bounded context
- Each owns its own model, its own database, its own deployment
- The workflow connects them; it does not live inside any one
- The workflow itself is a domain concept worth naming

---
## The Saga Pattern: Brief Definition

- A saga is a sequence of local transactions, one per service
- If any step fails, previous steps are undone with **compensating** actions
- No global lock; no shared transaction
- Eventual consistency is built in by design

---
## Saga Visualized at a High Level

![distributed_transaction_problem](svg/courses/architecting/saga-pattern/01_distributed_transactions_problem/distributed_transaction_problem.svg)

---
## Why Sagas Fit Microservices

- Each step is local to a service — no cross-service locks
- Failures are first-class — every step has a planned undo
- The orchestration is explicit — debugging is possible
- Eventual consistency is the contract — no false promise of atomicity
- Aligns with how brokers, queues, and event stores work in practice

---
## What Sagas Don't Solve

- They don't make distributed transactions "feel atomic" — they make them **eventually correct**
- They don't help with isolation — concurrent sagas can see each other's partial state
- They don't replace good design — bad service boundaries make sagas miserable
- They don't eliminate the need for retries, idempotency, or monitoring

---
## Anti-Pattern: Pretending 2PC Works

- "Let's just call all the services in sequence and roll back if anything fails"
- Roll back of a successful HTTP call is undefined — that response already left the building
- Without compensations, "rollback" is a wish
- This is the failure mode this course exists to prevent

---
## When You Don't Need a Saga

- The business process touches one service only — local transaction is enough
- The process is read-only — no consistency to maintain
- The process can tolerate full inconsistency on failure (e.g., best-effort logging)
- Sagas have real cost; only use them when the cost is justified

---
## Course Roadmap

- This chapter: the problem
- Chapter 2: saga fundamentals — choreography vs orchestration
- Chapter 3: choreography deep-dive
- Chapter 4: orchestration deep-dive
- Chapter 5: compensating transactions
- Chapter 6: testing, debugging, and operating sagas

---
## Summary

- ACID across services is impossible without 2PC, and 2PC is impractical for microservices
- CAP forces a choice; microservices typically pick availability and accept eventual consistency
- Long-running cross-service processes need their own state machine
- The saga pattern: local transactions plus compensations
- Eventual consistency is a contract, not a compromise — sagas make it tractable
