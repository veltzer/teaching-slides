---
tags:
  - architecture:saga
level: advanced
category: architecture
audience:
  - audiences:architects
  - audiences:developers

---

# Compensating Transactions

---

## Designing Compensations

![compensation_design](svg/courses/architecting/saga-pattern/05_compensating_transactions/compensation_design.svg)

---

## What This Chapter Covers

- Compensation vs rollback
- Designing semantically correct compensations
- Non-compensatable steps and pivot transactions
- Partial compensation and idempotency
- Failure during compensation (nested failures)
- Communicating compensations to users
- Testing compensations

---

## Compensation Is Not Rollback

- A database rollback erases the transaction; the change never happened
- A compensation is a **new** transaction that undoes the effect of an earlier one
- The compensation appears in the audit log; the original is also still there
- "We charged you, and then we refunded you" — both events visible in history

---

## Compensation in Practice

- Original: `Charge $100 from card 4242`
- Compensation: `Refund $100 to card 4242`
- Both events occurred; the customer's balance reflects both
- The audit, the dispute resolution, and the customer support flow all rely on this

---

## Semantic Correctness

- A compensation must reverse the **business effect**, not just the technical operation
- "Reserved 5 units of SKU X" → compensation is "Released 5 units of SKU X"
- Not always trivial — what undoes "Sent customer a confirmation email"?
- Some effects can't be undone; we'll handle those next

---

## Designing a Compensation

- For each step, ask: "If everything after this fails, what restores business state?"
- Document the compensation alongside the step in the saga definition
- Verify with domain experts — not all forward steps have intuitive reverses
- The compensation is a first-class business operation, not an afterthought

---

## Compensation Examples

| Forward step | Compensation |
|---|---|
| Reserve inventory | Release inventory |
| Capture payment | Refund payment |
| Schedule shipment | Cancel shipment |
| Issue voucher | Revoke voucher |
| Send confirmation email | Send correction email |
| Print physical letter | (cannot be undone) |

- The last row is the problem we tackle next

---

## Non-Compensatable Steps

- Some operations cannot be reversed — you can't un-send a physical mailing
- Some operations should not be reversed for business reasons
- These are real, common, and require explicit design choices
- Two patterns: pivot transactions and forward-only steps

---

## Pivot Transactions

- A point in the saga past which the saga can no longer be compensated
- Once we cross it, we are committed to the forward path
- The saga must succeed in completing — failure escalates to humans
- Place the pivot at the last reversible step

---

## Pivot Transaction Diagram

![pivot_transaction](svg/courses/architecting/saga-pattern/05_compensating_transactions/pivot_transaction.svg)

---

## Forward-Only Beyond the Pivot

- After the pivot, every remaining step is treated as forward recovery
- Retry indefinitely; escalate to humans on persistent failure
- Compensation is no longer an option
- Communicate clearly: the user has committed; the system will deliver

---

## Designing the Pivot

- Look at the business — when does the system make a commitment that can't be undone?
- Examples: physical shipment leaves the warehouse; legal contract finalized
- Place the pivot just **before** that step
- Everything before the pivot has compensations; everything after is forward-only

---

## Partial Compensation

- A step might do multiple things; only some need compensating
- Example: "captured payment + earned loyalty points"
- Compensation might refund the payment but leave the points (or revoke them)
- Decide per business rule; don't assume symmetry

---

## Idempotent Compensations

- Like forward steps, compensations may be retried
- They must be safe to call multiple times
- Releasing already-released inventory should be a no-op, not an error
- Refunding an already-refunded payment should be detected and ignored

---

## Idempotent Compensation Pattern

```python
def release_inventory(reservation_id):
    reservation = reservations.find(reservation_id)
    if reservation is None or reservation.released:
        return  # already released; idempotent no-op
    reservation.released = True
    inventory.add(reservation.sku, reservation.qty)
    reservations.save(reservation)
```

- Check current state first
- Take action only if needed
- Persist the new state
- Return success either way

---

## Compensation Order

- Compensations run in **reverse** order from the forward steps
- Forward: reserve → charge → ship
- Compensation: cancel ship → refund → release reservation
- Last step that succeeded is the first to be undone

---

## What If a Compensation Fails?

- Network glitches, services down — compensations can fail too
- Two strategies:
    1. Retry the compensation with backoff
    1. After enough retries, escalate to humans
- Never silently give up on a compensation

---

## Nested Failure Handling

- Compensation N retries; eventually succeeds; saga moves to compensation N-1
- If compensation N permanently fails, the saga halts
- A halted saga is a manual ops task: identify the divergence, fix it, mark the saga resolved
- Halted sagas need monitoring and runbooks

---

## Halted Saga Process

- Saga reaches max compensation retries
- Saga state is set to `RequiresIntervention`
- Alert fires for the on-call team
- Operator inspects the timeline, decides on resolution (refund manually, contact customer, etc.)
- Operator updates the saga state to closed; saga store reflects the resolution

---

## Communicating to End Users

- During the saga: "Your order is processing"
- On success: "Your order is confirmed" (with confirmation number)
- On compensated failure: "We weren't able to complete your order. Your card has been refunded."
- On halted saga: "We had a problem; our support team will contact you within 24 hours"

---

## UX Patterns for Compensations

- Don't say "rolled back" to a user — they don't think in those terms
- Say what was undone in business language: "your charge was refunded"
- Provide a reference id for the saga so support can find it
- Surface estimated resolution time when known

---

## Compensations and Audit

- Every compensation is auditable
- Reports should distinguish between "transactions that completed" and "transactions that were compensated"
- Compliance often requires both: the original action and its undo, with timestamps and reasons
- Don't lose the compensation reason — it explains the audit trail

---

## Testing Compensations

- Compensations are easy to forget — they only run in failure paths
- CI must exercise them: "given step 2 fails, then step 1 is compensated"
- Test happy and unhappy paths with the same rigor
- Specifically test: idempotent compensations, compensation order, halted-saga path

---

## A Compensation Test

```python
def test_payment_failure_compensates_inventory():
    saga = OrderSaga.start(order_id="42", items=[item("a", 1)])
    saga.handle(InventoryReserved(order_id="42"))
    saga.handle(PaymentFailed(order_id="42", reason="insufficient_funds"))

    assert saga.status == "compensating"
    assert saga.commands_emitted == [
        ReserveInventory(order_id="42"),
        CapturePayment(order_id="42"),
        ReleaseInventory(order_id="42"),
    ]
```

- Drive the saga through events
- Assert the compensation commands are emitted
- Pure test; no real services needed

---

## Anti-Patterns

- **No compensation for some step**: defeats the saga; either add one or place a pivot
- **Compensation that requires data we threw away**: design the forward step to record what compensation needs
- **Hiding compensation in retries**: a retry of a forward step is not a compensation
- **Compensation that has its own non-trivial side effects**: hard to test, hard to reason about

---

## Real-World Examples

- **Stripe**: charge → refund (compensation is `refund` API call)
- **Shopify**: order placed → order cancelled (compensation issues refund + restocks inventory)
- **Airline booking**: seat reserved → seat released (timeout-driven compensation if not paid)
- **SaaS provisioning**: account created → account suspended (rare; often forward-only beyond pivot)

---

## Summary

- Compensations are new transactions that undo previous ones — not database rollbacks
- Design compensations alongside their forward steps; verify with domain experts
- Non-compensatable steps require pivot transactions and forward-only flow afterward
- Idempotent compensations are mandatory
- Failed compensations are escalated to humans, never silently ignored
- Test compensation paths with the same rigor as happy paths
