---
tags:
  - data-and-ai:data-analytics
  - data-and-ai:business-case
level: beginner
category: data-driven
audience:
  - audiences:managers

---

# The Business Case for Data Analysis

---

## What This Chapter Covers

- Marketing decisions data can answer
- Business decisions: pricing, segmentation
- Understanding your users
- Product decisions: what to build, what to retire
- Feature and UI changes informed by data
- The case for further data investment

---

## Marketing Decisions

- Which channels actually convert?
- Cost per acquisition by source — and lifetime value
- Which ads, emails, landing pages perform?
- Attribution: who deserves credit when 5 touches happened?
- Spend reallocation is the highest-ROI use of marketing data

---

## Building the Case

![roi_dimensions](svg/courses/data_driven/data-analytics-for-managers/04_the_business_case_for_data_analysis/roi_dimensions.svg)

---

## Multi-Touch Attribution

- Last-click attribution: simple, gives 100% credit to the final touch
- First-click: gives credit to the discovery
- Linear / time-decay / data-driven: split credit across touches
- No model is "correct"; pick one and apply it consistently
- Switching attribution models retroactively breaks every comparison

---

## Business Decisions: Pricing

- Test prices on real customers (with care)
- Price elasticity: how does demand change with price?
- Segmented pricing: students, enterprises, regions
- Bundling: multi-product discounts vs single-product
- The wrong price is rarely "too cheap" — it's usually "wrong target"

---

## Business Decisions: Segmentation

- Group customers by behaviour, not by demographics alone
- "Power users", "occasional", "trial-only" — actionable segments
- Segments often map to different acquisition strategies and product needs
- A great product for one segment can be irrelevant to another
- Segment-level metrics surface this; aggregate metrics hide it

---

## Understanding Your Users

- Who they are: demographics, role, company size
- What they do: feature usage, sequences, paths
- What they want: surveys, NPS, qualitative interviews
- Why they leave: exit surveys, support tickets, cancellation reasons
- Quantitative + qualitative together; either alone misleads

---

## Cohort Analysis

- Compare users by *when they signed up*, not just where they are now
- "Users who signed up in March" vs "users who signed up in October"
- Reveals whether retention is improving or declining
- Aggregated metrics hide cohort-level shifts
- Standard tool for SaaS; underused everywhere else

---

## Cohort Workflow

![cohort_analysis](svg/courses/data_driven/data-analytics-for-managers/04_the_business_case_for_data_analysis/cohort_analysis.svg)

---

## New Products: Build vs Buy vs Skip

- Data on existing usage hints at unmet needs
- Surveys on willingness to pay refine
- Smoke tests (a landing page, a fake checkout) measure real interest
- Build only when usage data + intent signals + business case all align
- Most product ideas are bad; data filters quickly

---

## Features: What to Add, What to Remove

- 80% of features are used by less than 20% of users
- Removing rarely-used features is a *positive* — less complexity, less support
- Adding features without removing leads to product bloat
- Track *every* feature's adoption; surface low-usage ones
- Have the awkward conversation about retiring features

---

## UI Decisions

- A/B test changes that touch real users
- Log enough to attribute the difference to the change
- Statistical significance matters — don't ship on noise
- Some things are unsafe to A/B test (legal copy, navigation that breaks workflows)
- Pair tests with qualitative observation — *why* did the metric move?

---

## Terminating Products

- The hardest decision: shutting down something with users
- Data: usage trend, revenue contribution, support cost, opportunity cost
- A 100-user product losing money is a distraction
- Communicate early, migrate where possible, be honest
- Better than a slow death — your team and your customers benefit

---

## The Case for More Data

- Each successful initiative justifies more data investment
- Failed initiatives expose gaps to fix
- Track the ROI of analytics work like any other investment
- Without ROI tracking, the data org becomes a cost centre
- With it, the data org becomes a competitive advantage

---

## A Worked Example

- Product team wants to build a new dashboard feature
- Question 1: how many users would use it? &#8594; usage data on adjacent features
- Question 2: would they pay extra? &#8594; survey + smoke test
- Question 3: build cost? &#8594; engineering estimate
- Decision: build only if usage projection + revenue lift > cost

---

## Decision Hygiene

- Document the decision and the data that led to it
- Set a review date — was the data right?
- Calibrate over time — your "we'll get 1000 users" estimates *will* be wrong
- Better calibration = better future decisions
- The discipline matters more than the answer in any single case

---

## Common Mistakes

- Asking data to *justify* a decision already made
- Confusing correlation with causation
- A/B testing without enough power; calling noise "significance"
- Optimising local metrics at the cost of global outcomes
- Listening to data that confirms; ignoring data that doesn't
