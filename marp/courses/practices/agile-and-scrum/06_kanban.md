---
tags:
  - practices:kanban
  - practices:agile
level: beginner
category: practices
audience:
  - audiences:developers
  - audiences:team-leads

---

# Kanban

---

## Kanban Basics

![kanban_basics](svg/courses/practices/agile-and-scrum/06_kanban/kanban_basics.svg)

---

## What This Chapter Covers

- Where Kanban came from
- The Kanban board
- Work-in-progress (WIP) limits
- Flow metrics: lead time, cycle time, throughput
- Scrumban: when teams blend the two
- When to choose Kanban over Scrum

---

## Where Kanban Came From

- Toyota Production System, 1940s-50s
- Cards ("kanban") signalled "we need more of this part"
- Pull-based: work moves only when downstream is ready for it
- Adapted to knowledge work in the 2000s by David J. Anderson
- Now common in software, especially for support and ops teams

---

## The Kanban Board

- Columns = stages of work (Backlog, To Do, In Progress, Review, Done)
- Cards = individual work items
- Cards move left to right as work progresses
- The state of the board is the state of the team
- Physical board (whiteboard + sticky notes) or digital tool — same idea

---

## A Simple Board

![kanban_board](svg/courses/practices/agile-and-scrum/06_kanban/kanban_board.svg)

---

## Six Practices of Kanban

- **Visualise** the work
- **Limit** work-in-progress
- **Manage** flow
- Make policies **explicit**
- Implement **feedback** loops
- Improve collaboratively, evolve experimentally
- The first three are the headline; the rest support them

---

## Work-In-Progress Limits

- Each column has a max number of cards
- "In Progress: max 3" means no fourth card can enter until one leaves
- Forces the team to *finish* before *starting*
- Surfaces bottlenecks — the column where cards pile up is the constraint
- Counterintuitive but powerful: less WIP = more done

---

## Why WIP Limits Work

- Multitasking has a real cost: context switches, half-finished work
- A small WIP keeps focus high and quality up
- Feedback loops shorten — half-done work doesn't sit untouched for days
- Bottlenecks become visible — the team can act on them
- Teams that resist WIP limits usually have the worst flow

---

## Lead Time vs Cycle Time

- **Lead time**: from when the customer asked to when they got it
- **Cycle time**: from when work *started* to when it ended
- Lead time includes time waiting in the backlog
- Cycle time is what the team controls
- Both are useful — lead time is what the customer feels

---

## Throughput

- Cards completed per unit time (e.g., per week)
- Useful for forecasting future capacity
- Doesn't depend on card sizing — useful for teams that don't estimate
- Variability matters: a team that did 10/3/12/1 had 26 cards in 4 weeks but is wildly unpredictable
- Track over many weeks to see the pattern

---

## Cumulative Flow Diagram

- A stacked area chart: cards in each column, over time
- Widening "In Progress" band = WIP is growing &#8594; trouble
- Flat "Done" line = nothing is shipping
- Steep "Backlog" growth = demand outpaces capacity
- One picture summarises a month of flow

---

## Scrum vs Kanban

- Scrum: time-boxed sprints, defined roles, defined events
- Kanban: continuous flow, no required roles or events
- Scrum is good for product development with a clear cadence
- Kanban is good for support / ops / interrupt-driven work
- Many teams blend the two

---

## Scrumban

- Take Scrum's planning and Retrospective
- Replace the Sprint with continuous flow
- Replace velocity with cycle time / throughput
- Some teams adopt this gradually — start with Scrum, drift toward Kanban
- Others do the reverse — start loose, add structure

---

## When To Choose Kanban Over Scrum

- Work is interrupt-driven (support, on-call, ops)
- Items vary wildly in size and can't be batched into Sprints sensibly
- The team is small (2-3 people) and Sprint overhead is high relative to throughput
- The work is well-understood and the team needs predictability over experimentation
- Stakeholders need work pulled in continuously rather than at Sprint boundaries

---

## Common Kanban Mistakes

- Skipping WIP limits — turns the board into a backlog viewer
- One column called "Doing" with 25 cards in it
- No policy for what makes a card "Done" in each column
- Tracking metrics without using them to drive change
- Treating Kanban as "Scrum without the meetings" — it's not the same thing
