---
tags:
  - practices:scrum
level: beginner
category: practices
audience:
  - audiences:developers
  - audiences:team-leads

---
# The Scrum Framework

---
## What This Chapter Covers

- Scrum's origin and what it actually is (and isn't)
- The three roles: Product Owner, Scrum Master, Developers
- The three artifacts: Product Backlog, Sprint Backlog, Increment
- The five events
- The Definition of Done
- The five Scrum values

---
## Where Scrum Came From

- Coined in a 1986 *Harvard Business Review* article: "The New New Product Development Game"
- Adapted to software in the 1990s by Schwaber and Sutherland
- Documented in the Scrum Guide, updated periodically (latest 2020)
- The Scrum Guide is short — under 20 pages — and free
- Read it. Most people who critique Scrum have never read it.

---
## What Scrum Is

- A lightweight framework for delivering value in iterative cycles
- Three roles, three artifacts, five events, three commitments
- Empirical: inspect and adapt, don't predict and follow
- Time-boxed: every event has a maximum duration
- Self-managing: the team decides *how* to do the work

---
## What Scrum Is Not

- A complete project management methodology
- A set of engineering practices (Scrum says nothing about TDD, CI, refactoring)
- A way to estimate fixed-price projects
- An off-the-shelf solution — every team adapts it
- A guarantee of success — bad teams using Scrum produce bad results faster

---
## Scrum at a Glance

![scrum_overview](svg/courses/practices/agile-and-scrum/02_the_scrum_framework/scrum_overview.svg)

---
## The Product Owner

- One person — never a committee
- Owns the Product Backlog: what to build, in what order, why
- Maximises the value of the product the team delivers
- Talks to customers and stakeholders; brings their concerns to the team
- Can decline stakeholder requests if they don't fit the product vision

---
## The Scrum Master

- Coaches the team in Scrum and removes impediments
- Not a manager — has no authority over team members' work assignments
- Facilitates events but doesn't run them
- Helps the Product Owner with backlog techniques
- Helps the organisation understand what Scrum is and isn't

---
## The Developers

- Cross-functional: collectively have all skills needed to build a Done Increment
- Self-managing: choose how to do the work, not what to do
- Accountable for the quality of the Increment
- Typically 3-9 people; smaller is fine, larger needs splitting
- "Developer" includes anyone doing the work — engineers, designers, testers

---
## Product Backlog

- The single ordered list of everything the team might build
- Items at the top are more refined and ready
- Items at the bottom are vague and might never be done
- The Product Owner is accountable for it; anyone can suggest items
- Refined continuously through "backlog refinement" sessions (formerly "grooming")

---
## Sprint Backlog

- The subset of Product Backlog items the team commits to *this Sprint*
- Plus a plan for delivering them
- Plus the Sprint Goal that ties them together
- Owned by the Developers
- Updated daily as understanding evolves

---
## Increment

- A concrete step toward the product goal
- Must meet the Definition of Done
- Multiple increments may be created in one Sprint
- The sum of all increments is the working product
- An Increment that isn't Done is *not* an Increment

---
## The Five Events

- The Sprint itself (the container for everything else)
- Sprint Planning (start of the Sprint)
- Daily Scrum (every day during the Sprint)
- Sprint Review (end of the Sprint, with stakeholders)
- Sprint Retrospective (end of the Sprint, internal)

---
## Definition of Done

- The team's shared understanding of what "complete" means
- Code reviewed, tests written, deployed to staging, documented, etc.
- Created and owned by the Developers, often with input from stakeholders
- Same Definition of Done for every backlog item
- Without it, "done" means whatever each developer wants it to mean

---
## Definition of Ready (Optional)

- The team's shared understanding of when an item is ready to enter a Sprint
- Typically: clear acceptance criteria, dependencies known, sized
- Not part of the Scrum Guide — but commonly used
- Helps avoid pulling in items that aren't actually plannable
- Don't make it so strict that nothing ever qualifies

---
## The Five Scrum Values

- **Commitment**: do what the team agreed to do
- **Focus**: work on the Sprint Goal, not 17 other things
- **Openness**: share progress and obstacles honestly
- **Respect**: trust your teammates to do their jobs
- **Courage**: do the right thing, raise hard issues
- These aren't decoration — they're how Scrum actually works in practice

---
## Why Scrum Often Fails

- Roles are filled by job titles, not by people who actually do the role
- The Product Owner is a part-time stakeholder with no authority
- Events become rituals: read out a status, no discussion
- The Definition of Done is a wishlist, not a gate
- Management uses velocity as a performance metric — guarantees gaming

---
## Adopting Scrum: Practical Advice

- Start with the events, then add the roles
- Run a real Retrospective after every sprint and *act* on what you find
- Keep the Sprint short at first (1-2 weeks) — feedback is the point
- Don't add tools; pick a whiteboard and a stack of cards
- Once Scrum runs cleanly, adapt — but adapt deliberately, not by accident
