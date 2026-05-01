---
tags:
  - data-and-ai:data-analytics
level: beginner
category: data-driven
audience:
  - audiences:managers

---
# The Value of Data

---
## What This Chapter Covers

- Why data became a strategic asset
- The kinds of value data creates
- Where data is (and isn't) being collected today
- Realistic case studies
- Common reasons data initiatives fail
- A frame for the rest of the course

---
## A Sobering Statistic

- Gartner estimates organisations use ~0.5% of the data they collect
- Most companies are sitting on petabytes they will never look at
- That's not a tools problem; it's an organisational one
- "We have data" and "we use data" are different sentences
- The gap between them is where this course lives

---
## What "Data Value" Means

- Data has value when it changes a decision
- Pretty dashboards that nobody uses are decoration
- A small report that triggers a real change is worth more
- Value is *down-stream*, in the action it enables
- Managers should ask: "what would we do differently if we knew this?"

---
## Categories of Value

- **Operational**: detect failures, route around outages
- **Customer**: who they are, what they want, what's broken
- **Product**: which features land, which never get used
- **Market**: pricing power, competitive position
- **Financial**: margins, attribution, forecasting

---
## Where Data Lives

- Application databases (transactional, current state)
- Event streams (clicks, sessions, transactions over time)
- Logs (operational, debugging, audit)
- Third-party (analytics platforms, ad networks, payment processors)
- Files (uploads, exports, spreadsheets nobody owns)

---
## Storage Reality

- Most organisations have *all* of these
- Few have a single way to query across them
- Data lives in silos owned by different teams
- A simple "what are our top-10 customers by revenue?" can take a week
- The first job is often *connection*, not analysis

---
## Case Study 1: Netflix Recommendations

- Watching history + ratings &#8594; what to recommend
- Recommendations drive ~80% of viewing time
- The data isn't impressive on its own; the *system* around it is
- Without recommendations, retention drops measurably
- The data isn't the asset — what they *do* with it is

---
## Case Study 2: Bank Fraud Detection

- Every transaction is scored in real time against millions of patterns
- A fraction of a second decides "approve" or "challenge"
- Built on transaction-level data going back years
- Saves billions in losses annually
- Same data was sitting in the same DBs 20 years ago, unused

---
## Case Study 3: A Failed Data Initiative

- A retailer spends $50M building a "data lake"
- 18 months later: 200 TB of data, no business outcome
- Cause: nobody asked "what decision is this enabling?"
- Tools were built; questions never were
- This is the *most common* outcome of data initiatives

---
## Why Initiatives Fail

- No clear question being answered
- No champion in the business who acts on the answer
- Data quality issues nobody is empowered to fix
- "Build it and they will come" — they almost never do
- The technical project succeeds; the business outcome doesn't

---
## Data Maturity Levels

- **Reactive**: data is in databases; queries when something breaks
- **Reporting**: weekly dashboards, post-hoc explanations
- **Analytical**: scheduled deep-dives that change roadmaps
- **Predictive**: forecasts feed planning
- **Prescriptive**: data drives automated decisions

---
## Where Most Companies Are

- Most are at "reporting" — dashboards exist
- Few make it to "analytical" without organisational change
- "Predictive" requires data quality and modelling investment
- "Prescriptive" requires trust in the model and automation
- Skipping levels rarely works

---
## Who Owns the Decision?

- Data without a decision-maker is shelfware
- Every analytics initiative needs a *named owner* in the business
- Owner asks the question, owns the answer, takes the action
- Without an owner, even good answers go nowhere
- Manager-led initiatives outperform tool-led ones

---
## The Cost Side

- Storage isn't free; analytics tools aren't free; data engineers aren't free
- Many companies spend 10x the value they extract
- Cost growth is super-linear with data volume
- Budgeting for data ROI is unusual; budgeting for "data infrastructure" is common
- Treat data investments like any other investment

---
## What This Course Will Do

- Day 1: how to *collect* data and make it usable
- Day 2: frameworks for *thinking* about data
- Day 3: *tools* — from spreadsheet to data lake
- Day 4: *advanced topics* — AI, big data, what's coming
- Throughout: the *business* lens, not the technical one
