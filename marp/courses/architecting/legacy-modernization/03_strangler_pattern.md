---
tags:
  - architecting:patterns
level: intermediate
category: architecting
audience:
  - audiences:architects

---
# The Strangler Pattern

---
## What This Chapter Covers

- The pattern
- How it works
- Routing layer
- Carving slices
- Pitfalls

---
## What It Is

- Wrap the legacy
- Build new alongside
- Route per slice
- Retire the legacy when empty

---
## Why The Name

- After the strangler fig tree
- Grows around the host
- Eventually replaces it
- Slow but inevitable

---
## When To Use

- Cannot stop and rewrite
- Need to keep shipping
- Risk must be small per step
- Long timeline available

---
## The Routing Layer

- Sits between client and old system
- Inspects each request
- Routes to old or new
- Logs everything

---
## Building the Router

- Reverse proxy is common
- API gateway works
- Service mesh in Kubernetes
- Custom code as a last resort

---
## Carving a Slice

- Pick a coherent feature
- Identify its data
- Identify its callers
- Build the new path

---
## First Slice Choice

- Boring, valuable, contained
- Avoid the trickiest piece
- Avoid the trivial piece
- Pick something that proves the model

---
## Data Strategy

- Read from legacy first
- Write to legacy first
- Then mirror
- Then migrate ownership

---
## Behavioral Parity

- New must match old
- Test with real traffic
- Shadow mode first
- Gate the cutover

---
## Cutting Over

- Feature flag per slice
- Per-tenant rollout
- Monitor errors
- Roll back fast

---
## Retirement

- Old code path unused
- Stop traffic
- Decommission
- Archive what compliance requires

---
## Pitfalls

- Strangler pattern adopted as label, not practice
- Router becomes the legacy
- Data ownership unclear
- No retirement step

---
## Common Strangler Mistakes

- Carving too big a slice
- No parity testing
- No measure of progress
- Funding cut after 30%
- Skipping cleanup
