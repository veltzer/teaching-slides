---
tags:
  - architecting:patterns
level: intermediate
category: architecting
audience:
  - audiences:architects

---

# Modernization Strategies

---

## What This Chapter Covers

- The six strategies
- Trade-offs
- When to pick which
- Combining strategies

---

## Encapsulate

- Wrap legacy with API
- No internal changes
- Lowest risk
- Buys time, not progress

---

## Rehost

- Lift and shift to new infrastructure
- Same code, new platform
- Cloud migration is the common case
- Cost shifts but does not drop

---

## Replatform

- Minor changes for new platform
- Swap database engine
- Containerize
- Capture some platform benefits

---

## Refactor

- Internal restructuring
- Same behavior, cleaner code
- Enables future change
- Slow and invisible to users

---

## Rearchitect

- Restructure for new properties
- Microservices, event-driven
- Larger investment
- New risks introduced

---

## Rebuild

- Same scope, new code base
- Use modern stack
- Behavior preserved
- Expensive but bounded

---

## Replace

- Buy or use SaaS instead
- Drop the in-house code
- Data migration is the work
- Vendor lock-in trade

---

## Choosing

- Per system, not per portfolio
- Strategic value drives investment
- Risk drives speed
- Money drives scope

---

## Effort vs Value

![effort_vs_value](svg/courses/architecting/legacy-modernization/02_strategies/effort_vs_value.svg)

---

## Combining

- Encapsulate first to slow bleeding
- Rehost to escape data center
- Refactor inside the wrapper
- Replace pieces over time

---

## Sequencing

- Buy time before investing
- Stabilize before improving
- Improve before innovating
- Skipping steps risks rework

---

## Sequence Over Time

![strategy_combos](svg/courses/architecting/legacy-modernization/02_strategies/strategy_combos.svg)

---

## What Not to Do

- Big bang
- Strategy by hype
- Strategy by team preference
- Strategy with no ROI

---

## Decision Record

- Document the choice
- Document the constraints
- Revisit when constraints change
- Treat as living artifact

---

## Common Strategy Mistakes

- One strategy for everything
- No exit criteria
- No measurable outcome
- Underestimating data work
- Ignoring people change
