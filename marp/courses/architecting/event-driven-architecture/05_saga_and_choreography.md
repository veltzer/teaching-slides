---
tags:
  - patterns:saga
  - patterns:choreography
level: advanced
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Saga and Choreography Patterns

---
## What This Chapter Covers

- The distributed transaction problem
- Saga: orchestration approach
- Choreography: decentralized approach
- Compensating transactions
- Long-running processes; tracking saga state

---
## The Distributed Transaction Problem

- Multi-service workflow: reserve inventory, charge payment, ship order
- Each service has its own database
- ACID across all is what we want; only available locally
- Two-phase commit doesn't fit microservices
- Sagas are the response

---
## What Is a Saga?

- A sequence of local transactions
- Each step is atomic within its service
- If a step fails, previously completed steps are *compensated*
- No global lock, no shared transaction
- Eventual consistency by design

---
## Saga Visualized

![saga_overview](svg/courses/architecting/event-driven-architecture/05_saga_and_choreography/saga_overview.svg)

---
## Two Approaches

- Orchestration: a coordinator drives each step
- Choreography: each service reacts to events from others
- Different ownership, different failure modes
- Both are sagas — they differ in who holds the state machine
- Pick per workflow; mix within a system

---
## Orchestration: The Coordinator

- A dedicated saga coordinator (orchestrator)
- Sends commands to each service in order
- Waits for completion or failure events
- On failure, sends compensation commands in reverse order
- The state machine is explicit and centralized

---
## Orchestration: Pros

- Clear, explicit workflow logic
- Easy to monitor and debug — one place to look
- Failure handling is centralized
- New services slot in by adding a step
- The orchestrator is the system of record for the workflow

---
## Orchestration: Cons

- The orchestrator is a single point of complexity
- Adds coupling: services must respond to commands
- The orchestrator's bugs affect every workflow
- Scaling the orchestrator is its own concern
- Risk of becoming a "god service"

---
## Choreography: The Reactive Approach

- No central coordinator
- Each service reacts to events from others
- Step 1 emits an event; step 2 listens, does its thing, emits another
- Compensations are also event-driven
- The "workflow" emerges from decentralized rules

---
## Choreography: Pros

- No single point of failure
- Each service is self-contained
- New steps don't require modifying existing services
- Aligns naturally with event-driven systems
- Loose coupling extended to workflow

---
## Choreography: Cons

- The workflow is implicit — hard to see end to end
- Debugging requires correlating events across services
- Easy to create cycles or accidental loops
- New developers struggle to understand the flow
- Failure recovery is harder to coordinate

---
## Choreography Visualized

![choreography](svg/courses/architecting/event-driven-architecture/05_saga_and_choreography/choreography.svg)

---
## When to Choose Orchestration

- Long, complex workflows with branching logic
- Strong audit and observability requirements
- Centralized error handling matters
- Workflow changes happen often; ownership is clear
- Regulated industries with explicit process documentation

---
## When to Choose Choreography

- Short workflows with linear or simple flow
- Services owned by independent teams
- Workflow logic is naturally distributed
- Adding new reactions is more frequent than changing existing flow
- Pure event-driven culture

---
## Compensating Transactions

- The "undo" of a previously completed step
- Not a database rollback — the original commit stands
- A new transaction that semantically reverses
- "Refund" compensates "Charge"
- Must be idempotent and well-defined per step

---
## Designing Compensations

- For each step, write its compensation up front
- Compensation must succeed or be retriable
- Sometimes the compensation isn't a clean undo (sent email can't be unsent)
- Communicate the partial state to the user honestly
- Document compensation semantics per step

---
## Long-Running Processes

- Sagas can take hours, days, or weeks
- The orchestrator (or choreographers) must persist state
- Survival across deployments and restarts is required
- Timeouts at each step prevent stuck sagas
- Workflow engines (Temporal, Camunda) handle this

---
## Saga State Tracking

- Per saga: ID, current step, status, started_at, completed_at
- Status: pending, succeeded, compensating, failed
- Persisted in a database, queryable
- Operations dashboards built on this state
- Debugging starts from the state record

---
## Workflow Engines

- Temporal — code-as-workflow, durable execution
- Camunda — BPMN-based, business-friendly
- AWS Step Functions — managed, integrates with AWS
- Cadence — Temporal's predecessor
- All solve persistence, retries, timeouts so you don't have to

---
## Mixing Orchestration and Choreography

- Top-level workflow is orchestrated
- Sub-workflows within a bounded context can be choreographed
- Or: orchestration coordinates choreography across boundaries
- Pure approaches are rare; hybrids are pragmatic
- Document the choice per workflow

---
## Error Handling

- Different errors need different responses
- Transient: retry with backoff
- Business rule failure: compensate
- Catastrophic: alert humans, halt workflow
- Distinguish at design time, not at debug time

---
## Partial Failure Scenarios

- Step succeeds but ack fails — appears as failure
- Compensation fails — now you have a stuck saga
- Step times out — was it done? unclear
- Each scenario needs an explicit handling decision
- Test these paths; they're not theoretical

---
## Tracking Saga State Across Services

- Correlation ID flows through every event
- Each service logs with the correlation ID
- Tracing tools (OpenTelemetry) follow it across hops
- The orchestrator (if any) is the saga state authority
- Without correlation, debugging is nearly impossible

---
## Common Anti-Patterns

- "Compensation = call DELETE" — semantic vs technical undo
- Skipping compensations because "it'll be rare"
- Using sagas where a single ACID transaction would work
- Choreography that loops or has implicit cycles
- Orchestrators that grow into monoliths

---
## Saga Testing

- Unit-test each step's command and compensation
- Integration-test the happy path end-to-end
- Test forced-failure paths: each step fails in turn
- Test compensation chains
- Test timeouts and partial failures explicitly

---
## Summary

- Sagas: local transactions plus compensations, no 2PC
- Orchestration: central coordinator, explicit state
- Choreography: distributed events, emergent workflow
- Both work; choose based on team and workflow complexity
- Workflow engines handle the heavy lifting if you let them
