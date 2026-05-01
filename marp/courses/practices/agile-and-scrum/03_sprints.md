---
tags:
  - practices:scrum
  - practices:sprints
level: beginner
category: practices
audience:
  - audiences:developers
  - audiences:team-leads

---
# Sprints

---
## What This Chapter Covers

- What a Sprint actually is, in mechanical terms
- Sprint Planning: agreeing on what and how
- The work of the Sprint itself
- Sprint Review: showing what got built
- Sprint length and how to choose
- Handling change mid-Sprint

---
## A Sprint Is a Container

- A fixed time-box, 1 to 4 weeks long
- Begins immediately after the previous Sprint ends — no gaps
- Contains the four other Scrum events
- Aim: a Done Increment by the end
- Same length each time — predictability lets people plan

---
## The Sprint Goal

- One coherent objective for the Sprint
- "Validate the new checkout flow", not "do these 9 unrelated tickets"
- Lets the team make trade-offs during the Sprint without losing direction
- If a Backlog Item is dropped, the Sprint Goal can still be met
- Without a Sprint Goal, a Sprint is just a list

---
## Sprint Planning

- Time-boxed: max 8 hours for a 4-week Sprint, less for shorter ones
- Three questions:
    - **Why** is this Sprint valuable? (Sprint Goal)
    - **What** can be done this Sprint? (forecast from Backlog)
    - **How** will the work get done? (plan)
- The Product Owner brings the Backlog; the Developers commit to the work

---
## Forecasting Capacity

- The team uses past data (velocity, throughput) to forecast
- Account for holidays, time off, on-call duty, known interruptions
- A new team has no history — guess, then correct
- Pulling in *more* than you can deliver is worse than pulling in less
- "Stretch goals" are a smell — they imply you didn't really plan

---
## Working the Sprint

- Developers self-organise: who does what, in what order
- Coordinate via the Daily Scrum
- Sprint Backlog is updated throughout the Sprint as understanding evolves
- Definition of Done applies to *every* item, not just the last few
- Stay focused on the Sprint Goal — defer other work

---
## Sprint Review

- Time-boxed: max 4 hours for a 4-week Sprint
- The team shows the Increment to stakeholders
- Working software, not slides — demo from a real environment
- Stakeholders give feedback; this informs Backlog updates
- *Not* a status meeting — a working session about what's next

---
## Sprint Review Antipatterns

- Polished slide deck instead of working software
- "We didn't have time to demo, here's a screenshot"
- Stakeholders who critique tone instead of substance ("button is the wrong shade of blue")
- The Product Owner running the demo while developers stay quiet
- Treating the Review as a sign-off ceremony — it isn't

---
## Choosing a Sprint Length

- 1 week: fast feedback, lots of overhead from events
- 2 weeks: most common, good balance
- 3-4 weeks: rarely a good idea — feedback gets stale
- Same length every time so the cadence is predictable
- New teams: start at 2 weeks, change later if you have a real reason

---
## Handling Change Mid-Sprint

- The Sprint Backlog is owned by the Developers
- Items can be added, removed, or split if it helps reach the Sprint Goal
- *Goal* changes are different — they cancel the Sprint
- Cancellation is rare and decided by the Product Owner
- Losing a day to a production incident does not cancel the Sprint

---
## Cancelling a Sprint

- Only the Product Owner can do it
- Reason: the Sprint Goal becomes obsolete (market shift, business pivot)
- Costly: in-progress work is wasted, team morale takes a hit
- Should be very rare; if it isn't, planning is broken
- After cancellation: review the Backlog, plan a new Sprint

---
## Sprint Hygiene

- Demo is at the *end* of the Sprint, on the planned date
- Don't ship to production from the Sprint Review environment without a real release process
- Update estimates and acceptance criteria *before* you start the work, not after
- Keep one source of truth for the Sprint Backlog (a board, not three spreadsheets)
- Update tickets honestly — half-truths corrupt next Sprint's planning

---
## Velocity, Carefully

- Velocity = amount of work the team typically completes in a Sprint
- Useful as a *forecasting* tool for the team
- Useless as a performance metric across teams
- Goes up when work is split smaller (not because the team got faster)
- Stops being useful the moment management starts measuring it
