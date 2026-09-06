---
tags:
  - data-and-ai:data-analytics
  - data-and-ai:data-engineering
level: beginner
category: data-driven
audience:
  - audiences:managers

---

# Collecting Data

---

## What This Chapter Covers

- Mapping organisational data sources
- Joining data across silos
- Dealing with outliers and missing data
- When (and how) to generate fake data
- Storage choices for analytics data
- The tradeoffs of "collect everything"

---

## Mapping Your Sources

- Inventory before you build: where does data already live?
- Application databases, event streams, third-party services, files
- Each has owners; each has access policies
- Build a one-page map: source &#8594; what's in it &#8594; who owns it
- This map is more valuable than most analytics dashboards

---

## Joining Data Across Sources

- Most useful questions span multiple systems
- "How much do top-50 paid users use feature X?" needs billing + usage events
- Joins require *consistent identifiers* — `customer_id` shared across systems
- Without consistent IDs, you spend weeks reconciling
- Establish a "golden ID" early; force every system to use it

---

## The Identity Problem

- One human user can be five different IDs (web session, login, billing, support, marketing)
- Reconciling them is a project on its own
- Identity resolution platforms (CDPs) exist for this
- For managers: insist on shared IDs *before* the data flows in
- After the fact, it's an ongoing tax

---

## Identity States

![identity_resolution](svg/courses/data_driven/data-analytics-for-managers/02_collecting_data/identity_resolution.svg)

---

## Outliers

- Data has anomalies: bots, test accounts, system glitches
- Top 10% of any metric is often outliers, not real users
- Excluding them changes the answer significantly
- Document what you exclude and why
- Recurring outliers point to data-quality root causes worth fixing

---

## Missing Data

- Some fields are empty; some are wrong but look full
- Strategies: drop rows, impute (fill with median/mean/model), or treat "missing" as a value
- Each has biases; the choice matters
- A "we have 50% missing data on field X" is itself a finding
- Document treatment in every report

---

## Test, Internal, and Bot Traffic

- Your QA team's accounts inflate every metric
- Bots scraping your site count as users
- Internal employees clicking through workflows count as users
- Filter aggressively; ask data engineers what's in the dataset
- Reports without these filters tell a flattering, false story

---

## Generating Fake Data

- Sometimes you need data the production system can't share (PII, compliance)
- Synthetic data tools generate realistic-but-fake records
- Useful for: dev environments, training models, demos
- Risk: synthetic data masks real-world patterns
- Use for *development*; don't use for analysis

---

## Choosing Where to Store

- Operational DBs (Postgres, MySQL): for app state, fast, expensive at scale
- Data warehouses (Snowflake, BigQuery, Redshift): for analytics, slower writes, fast queries
- Data lakes (S3 + Parquet): for raw data, cheapest, requires query layer
- Lakehouses (Databricks, Iceberg): blur the line; one storage, many uses
- Pick based on access patterns, not vendor enthusiasm

---

## The Cost of "Collect Everything"

- Storage is cheap; processing is not
- 100 TB of unused logs costs both money and attention
- Schemas drift; old data becomes uninterpretable
- Privacy and compliance get harder as data ages
- Collect intentionally; document what you collect *and why*

---

## Privacy and Compliance

- GDPR (EU), CCPA (California), HIPAA (US health), and many more
- Personal data has legal obligations: right to access, right to delete
- "Anonymous" data often isn't — combinations re-identify
- Bake privacy into the *collection* step, not the cleanup step
- Compliance failures are expensive and reputation-shredding

---

## Quality Over Quantity

- A clean 10K-row dataset beats a dirty 10M-row one
- "Clean" means: known schema, defined missingness, identified entities, documented sources
- Most analytics time goes to cleaning; budget accordingly
- Invest in data quality at the *source* — it compounds
- "Garbage in, dashboard out" is the most expensive form of garbage

---

## A Practical Workflow

- Define the question
- Find the sources
- Sketch the joins
- Identify quality risks (outliers, missing, dupes)
- Pull a sample, eyeball it
- Iterate before building anything automated

---

## Common Mistakes

- Building pipelines before knowing the question
- Treating data quality as someone else's problem
- Storing without retention policies — becomes legal liability
- Joining on inconsistent IDs and reporting confidently wrong numbers
- Buying tools before mapping what you have
