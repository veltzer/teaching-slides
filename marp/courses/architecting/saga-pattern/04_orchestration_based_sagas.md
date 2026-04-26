---
tags:
  - architecture:saga
  - architecture:orchestration
level: advanced
category: architecture
audience:
  - audiences:architects
  - audiences:developers

---
# Orchestration-Based Sagas

---
## What This Chapter Covers

- How orchestration works
- Designing the orchestrator as a state machine
- Communication: synchronous calls vs async commands
- Persisting orchestrator state
- Timeouts and retries
- Workflow engines: Temporal, Conductor, Camunda
- Worked example: order fulfillment via orchestration

---
## How Orchestration Works

- A central orchestrator owns the saga
- It tells participant services what to do, one step at a time
- It records each step's outcome
- On failure, it walks back through compensation calls
- The orchestrator is itself a stateful aggregate

---
## The Orchestrator as a State Machine

- States: `Started`, `InventoryReserved`, `PaymentCaptured`, `Completed`, `Failed`, `Compensating`, `CompensatedFailed`
- Transitions: triggered by step outcomes
- Each state has defined next steps and compensation paths
- The state machine **is** the saga, in code

---
## State Machine Visualized

![orchestrator_state_machine](svg/courses/architecting/saga-pattern/04_orchestration_based_sagas/orchestrator_state_machine.svg)

---
## A Minimal Orchestrator in Code

```python
class OrderSagaOrchestrator:
    def handle(self, state, event):
        match (state.status, event):
            case ("started", OrderPlaced()):
                self.command(ReserveInventory(state.order_id))
                state.status = "reserving_inventory"
            case ("reserving_inventory", InventoryReserved()):
                self.command(CapturePayment(state.order_id))
                state.status = "capturing_payment"
            case ("capturing_payment", PaymentCaptured()):
                self.command(ScheduleShipment(state.order_id))
                state.status = "scheduling_shipment"
            case ("capturing_payment", PaymentFailed()):
                self.command(ReleaseInventory(state.order_id))
                state.status = "compensating"
        return state
```

---
## Synchronous Commands

- The orchestrator calls a participant via HTTP/gRPC and waits for the response
- Simpler in flow, but the orchestrator's request thread is blocked
- Failure of the participant blocks the orchestrator
- Hard to scale; not the right choice for slow participants

---
## Asynchronous Command Events

- The orchestrator emits a command event ("ReserveInventory")
- The participant subscribes, executes, emits a result event
- The orchestrator subscribes to results
- More moving parts; better for slow or unreliable participants
- The standard model in production systems

---
## Sync vs Async Commands

![sync_vs_async_commands_orchestration](svg/courses/architecting/saga-pattern/04_orchestration_based_sagas/sync_vs_async_commands_orchestration.svg)

---
## Persisting Orchestrator State

- The orchestrator must survive restarts and crashes
- Persist the saga state after every transition
- Resume from the last persisted state on startup
- Common approach: event-sourced orchestrator (chapter from CQRS course applies)

---
## Persistence Patterns

- **Event-sourced**: store every state transition as an event; replay to reconstruct
- **State snapshot**: store the latest state directly in a row
- **Workflow engine**: rely on Temporal/Conductor/Camunda to persist for you
- All three work; the choice affects observability and operational ergonomics

---
## Timeouts

- Each step needs a timeout — what if the participant never responds?
- The orchestrator's state machine has timer-driven transitions
- Reaching the timeout triggers retry, escalation, or compensation
- Without timeouts, sagas hang indefinitely

---
## Timer Patterns

- A separate timer service that emits "TimeoutElapsed" events
- The orchestrator subscribes; treats timeouts as just another event
- Workflow engines have timer primitives built in
- Whatever the mechanism, every step needs a deadline

---
## Retry Logic

- Transient failures: retry the same step
- Permanent failures: trigger compensation
- The orchestrator tracks retry count per step
- Exponential backoff between retries
- A maximum retry limit before giving up

---
## Retry Decision Tree

- Step fails → check error type
- Transient (network, timeout) → retry with backoff
- Permanent (validation, business rule) → compensate
- Unknown error → conservative; usually compensate
- "Permanent" or "transient" classification belongs to the participant

---
## Centralized Visibility

- The orchestrator's state is the single place to see "where is order 42?"
- Build a dashboard from the orchestrator's state store
- Alerts can fire on stuck sagas, high error rates, slow steps
- This is the killer feature of orchestration

---
## Orchestrator Dashboard Wishlist

- List all in-flight sagas with current state
- Filter by status, time spent in current state, retry count
- Drill down to see the step history
- Click to manually retry, skip, or abort
- Operators love this; choreography needs custom tooling to provide it

---
## Workflow Engines

- Tools that provide saga primitives out of the box
- **Temporal**: durable workflows in code; very popular
- **Conductor** (Netflix): JSON-defined workflows
- **Camunda**: BPMN-driven workflows; enterprise
- **AWS Step Functions**: serverless state machines
- **Apache Airflow**: scheduled DAGs (less suited to interactive sagas)

---
## Workflow Engine Comparison

![workflow_engines](svg/courses/architecting/saga-pattern/04_orchestration_based_sagas/workflow_engines.svg)

---
## When to Use a Workflow Engine

- The team prefers an external tool over building orchestration in-house
- Visibility and audit are first-class business requirements
- The workflow includes long delays (days, weeks) — engines handle this well
- Multiple workflows need similar primitives — the engine is leverage

---
## When Not to Use a Workflow Engine

- The flow is small and fits in 200 lines of orchestrator code
- The team doesn't want to depend on another piece of infrastructure
- The workflow rarely changes; a hand-coded state machine is sufficient
- The engine's deployment complexity exceeds the saga's complexity

---
## Worked Example: Order Saga via Orchestration

![orchestration_order_saga](svg/courses/architecting/saga-pattern/04_orchestration_based_sagas/orchestration_order_saga.svg)

---
## Order Saga Flow

- Trigger: `PlaceOrder` command arrives
- Orchestrator creates new saga; emits `ReserveInventory` command
- Inventory: reserves; emits `InventoryReserved` event
- Orchestrator: receives event; emits `CapturePayment` command
- Payment: captures; emits `PaymentCaptured` event
- Orchestrator: emits `ScheduleShipment`; on success → `Completed`

---
## Order Saga: Failure Path

- Payment emits `PaymentFailed`
- Orchestrator transitions to `Compensating`
- Emits `ReleaseInventory` command
- Inventory: releases; emits `InventoryReleased`
- Orchestrator: emits `NotifyCustomerOfFailure`
- Saga ends in `Failed` state with audit trail

---
## Anti-Patterns Specific to Orchestration

- **God orchestrator**: one orchestrator that knows everything — hard to maintain
- **Distributed orchestrator state**: state spread across services rather than the orchestrator
- **Embedded business logic in commands**: keep commands declarative; let participants enforce rules
- **No timeout**: a participant outage hangs the orchestrator forever

---
## Choreography vs Orchestration: Operator's View

- **Choreography**: "What's happening?" → query 5 services, build a timeline
- **Orchestration**: "What's happening?" → query the orchestrator

---
## Choreography vs Orchestration: Developer's View

- **Choreography**: change the flow → coordinate edits across multiple services
- **Orchestration**: change the flow → edit the orchestrator's state machine

---
## A Common Hybrid

- Use orchestration for the top-level workflow that crosses bounded contexts
- Use choreography within a context for fine-grained event reactions
- The orchestrator at the top owns the saga
- The choreography below it moves data without dragging the orchestrator into details

---
## Summary

- Orchestration: a central orchestrator drives the saga as a state machine
- Async command events scale better than synchronous calls
- Orchestrator state must persist; workflow engines do this for you
- Timeouts and retries are first-class concerns
- Visibility is orchestration's killer feature
- Workflow engines (Temporal, Conductor, Camunda) provide saga primitives out of the box
