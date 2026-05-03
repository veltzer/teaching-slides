---
tags:
  - data-and-ai:data-analysis
level: beginner
category: data-science
audience:
  - audiences:data-analysts
  - audiences:developers

---
# Data Analysis Workflow

---
## What This Chapter Covers

- What data analysis actually is
- The end-to-end lifecycle
- Four kinds of analysis: descriptive, diagnostic, predictive, prescriptive
- How to frame a question well
- Where data comes from
- Turning raw data into actionable insight

---
## Workflow

![workflow](svg/courses/data_science/data-analyst-fundamentals/01_data_analysis_workflow/workflow.svg)

---
## Core Analyst Skills

![analyst_skills](svg/courses/data_science/data-analyst-fundamentals/01_data_analysis_workflow/analyst_skills.svg)

---
## What Data Analysis Is

- Looking at data to *answer a question* or *make a decision*
- Distinct from data *engineering* (moving and cleaning) and data *science* (modelling)
- Most analysts blend all three at junior levels
- The skill is asking the right question and presenting the answer clearly
- Tools matter; thinking matters more

---
## The Lifecycle

- **Ask**: define the question
- **Get**: pull data from sources
- **Clean**: fix what's missing or wrong
- **Explore**: look around, find patterns
- **Analyse**: confirm patterns, test hypotheses
- **Communicate**: tell the story
- **Act**: trigger a decision

---
## Where Time Actually Goes

- Cleaning: 60-70% (industry estimates)
- Asking and getting: 10-15%
- Analysing: 10-15%
- Communicating: 10%
- "Do data analysis" sounds like analysing; it's mostly cleaning

---
## Four Kinds of Analysis

- **Descriptive**: what happened? (sales last quarter)
- **Diagnostic**: why did it happen? (which campaign drove the spike)
- **Predictive**: what will happen? (sales next quarter)
- **Prescriptive**: what should we do? (which campaign to fund)
- Most work is descriptive and diagnostic

---
## Defining Questions

- Vague: "how is the product doing?"
- Better: "what is week-over-week active users for the last 12 weeks?"
- Specify: time range, metric, segments, comparison
- A good question already implies the chart you'll build
- Bad questions waste days of work

---
## Framing Problems

- Start with the *decision* the answer will support
- "If users dropped, we'll do X. If users grew, we'll do Y."
- If you can't say what you'll do with the answer, don't ask the question yet
- Time spent framing saves time analysing
- Push back on requestors who can't articulate the decision

---
## Data Sources

- **Operational databases**: live state, transactional
- **Data warehouses**: cleaned, joined, modelled
- **Event streams**: clicks, sessions, transactions over time
- **Third-party**: ad platforms, CRMs, payment processors
- **Files**: spreadsheets, exports, manual entries
- Most analysts touch all of these in a year

---
## Data Acquisition

- Get the right grain: per-user, per-event, per-day
- Sample if the dataset is huge; full data if you need precision
- Document the query — future-you will need to reproduce it
- Keep a copy of the raw data before transforming
- Cleanups overwrite history; raw is your safety net

---
## Raw to Insight: A Worked Example

- Question: "Has feature X driven retention?"
- Get: weekly active users + feature X usage events
- Clean: filter test accounts, deduplicate sessions
- Explore: cohort users by first feature X use
- Analyse: compare retention curves
- Communicate: one chart, one paragraph
- Act: greenlight feature X investment, or not

---
## Reproducibility

- Every analysis should be re-runnable
- SQL queries in version control; notebooks committed
- Date ranges parameterised, not hardcoded
- Random seeds set for samples
- "I ran it last month and got a different number" = no reproducibility

---
## Documenting Analyses

- A short README per analysis: question, sources, methods, findings
- Future you will thank present you
- Stakeholders need to know the assumptions to interpret results
- Reviewers need it to spot mistakes
- Documentation is not optional in data work

---
## Tools at a Glance

- **SQL**: where the data lives; learn it well
- **Python + pandas**: cleaning, analysis, plotting
- **Excel / Google Sheets**: still indispensable
- **Tableau / Power BI / Looker**: dashboards
- **Notebooks** (Jupyter): exploratory work
- **Git**: version control for queries and notebooks

---
## Career Path

- Junior analyst: write queries, build dashboards, answer questions
- Senior analyst: pick the right questions, mentor, own metrics
- Analytics engineer: build the data models everyone queries
- Data scientist: build models that predict
- All paths start with these fundamentals

---
## Common Mistakes

- Analysing without a clear question
- Skipping the cleaning step ("the data looks fine")
- One chart, no narrative
- Drawing causal conclusions from correlations
- Failing to document; another analyst can't reproduce your work
