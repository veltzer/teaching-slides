---
tags:
  - practices:agile
  - practices:user-stories
  - practices:estimation
level: beginner
category: practices
audience:
  - audiences:developers
  - audiences:team-leads

---

# User Stories and Estimation

---

## INVEST Criteria

![invest_criteria](svg/courses/practices/agile-and-scrum/07_user_stories_and_estimation/invest_criteria.svg)

---

## What This Chapter Covers

- The user story format and why it works
- INVEST: properties of a good story
- Acceptance criteria
- Story points and relative estimation
- Planning Poker
- Velocity, capacity, and forecasting
- Splitting epics into stories

---

## What a User Story Is

- A short statement of a piece of value, from a user's perspective
- Classic format: "As a [role], I want [goal], so that [benefit]"
- Designed to fit on an index card
- Designed to be a *promise of a conversation*, not a spec
- Two developers seeing the same story should ask similar questions

---

## A Good Story Looks Like

> As a *registered customer*,
> I want to *reset my password without contacting support*,
> so that *I can recover access on my own at 2am*.

- Role: who benefits
- Action: what they want to do
- Outcome: why it matters
- Vague enough to invite conversation, specific enough to estimate

---

## What a Story Is Not

- A spec document
- A list of technical tasks
- A bug ticket ("login button broken")
- A boilerplate restated every Sprint
- A mechanism to move work between teams without conversation

---

## INVEST

- **I**ndependent: can be developed in any order relative to other stories
- **N**egotiable: the details can be discussed
- **V**aluable: delivers something the user (or business) cares about
- **E**stimable: the team has enough info to size it
- **S**mall: fits comfortably in one Sprint
- **T**estable: there's a clear way to know it's done

---

## Acceptance Criteria

- The conditions that must hold for the story to be considered done
- Often written as Given / When / Then (Gherkin)
- Lives on the story itself, not in a separate document
- Negotiable up until the team commits to the story
- Frozen once the story is being worked on, unless re-negotiated

---

## Acceptance Criteria Example

```misc
Given I am a logged-out user
When I click "Forgot Password" and enter a registered email
Then I receive an email with a single-use reset link
And the link expires after 30 minutes
And I am redirected to a confirmation page
```

- Concrete, testable, complete
- Doesn't dictate implementation
- Could be lifted into automated acceptance tests

---

## Why Estimate at All?

- To plan: how much can we commit to this Sprint?
- To forecast: when will the next milestone arrive?
- To trigger conversation: differing estimates mean differing assumptions
- *Not* to measure individual performance
- *Not* to commit to a date with management

---

## Story Points vs Hours

- Hours: an estimate of how long a *specific person* will take
- Story points: a relative size — how *big* the story is
- Story points abstract away who does the work
- Avoid the trap of "1 point = 1 day" — relative is the whole idea
- Two teams' story points are not comparable

---

## The Fibonacci Sequence

- Common scale: 1, 2, 3, 5, 8, 13, 20, 40, 100
- Bigger numbers, less precision — by design
- A "13" means "it's big and we're not sure"
- A "100" usually means "we need to split this story"
- Skip "1" if your team always rounds tiny things up

---

## Planning Poker

- Each developer picks a card with their estimate
- Reveal simultaneously
- Discuss the spread — *why* did people estimate differently?
- Re-vote until convergence (or agree to disagree on a value)
- The conversation is the point; the number is a side effect

---

## Reference Stories

- Pin a few previously-completed stories to known sizes
- "This is our 3-point story; this is our 8-point story"
- New stories get sized relative to the references
- Re-baseline occasionally as the team's understanding evolves
- Better than calibrating in the abstract

---

## Velocity

- Story points completed per Sprint
- Track over many Sprints — single-Sprint velocity is noisy
- Use the average of the last 3-5 Sprints as a forecast
- Velocity is for the *team*, by the *team*
- Velocity *is not a productivity metric*; do not treat it as one

---

## Capacity Planning

- Velocity says what we usually finish; capacity adjusts for *this* Sprint
- Subtract holidays, time off, on-call rotations, planned interruptions
- A 4-developer team with 2 on holiday has half-capacity
- Plan to capacity, not to wishful thinking
- Track actuals vs forecast over time — calibration improves

---

## Splitting Stories

- Anything bigger than ~13 points should probably split
- Split by *workflow steps*: "happy path" first, "error handling" later
- Split by *acceptance criteria*: each AC becomes its own story
- Split by *interface*: API first, UI later (or vice versa)
- Don't split by *technical layer* (database / backend / frontend) — those aren't independently valuable

---

## Common Estimation Mistakes

- Treating estimates as commitments
- Letting one loud voice dominate the estimate
- Estimating in hours and calling them story points
- Re-estimating completed stories to "match reality"
- Comparing team A's velocity to team B's
