---
tags:
  - data-and-ai:data-analytics
  - data-and-ai:tools
level: beginner
category: data-driven
audience:
  - audiences:managers

---
# Tools

---
## The Analyst Tool Stack

![tool_choices](svg/courses/data_driven/data-analytics-for-managers/06_tools/tool_choices.svg)

---
## What This Chapter Covers

- Web analytics: Google Analytics
- Behavioural analytics: Mixpanel, Amplitude
- BI / visualisation tools: Tableau, Power BI
- Search and big-data: Elasticsearch + Kibana, Splunk
- How to evaluate tools without burning budget
- A practical buying framework

---
## Tool Categories at a Glance

- **Web / mobile analytics**: visits, sessions, conversions
- **Product / behavioural**: feature usage, funnels, cohorts
- **BI / visualisation**: dashboards over warehoused data
- **Logs / observability**: searching, alerting on machine-generated data
- **Statistical / advanced**: notebooks, models, experiments

---
## Google Analytics

- The most-deployed analytics platform, free at the entry tier
- Tracks page views, sessions, conversions, traffic sources
- GA4 (the current version): event-based, harder learning curve than GA3
- Privacy-first changes are reshaping what GA can see
- Strong on web, weaker on product/behavioural depth

---
## What GA Is Good For

- "How many people visited and from where?"
- Marketing channel performance
- Conversion funnel from landing page to checkout
- A/B testing via Google Optimize (sunset; alternatives include VWO, Optimizely)
- High-level traffic and acquisition reporting

---
## What GA Misses

- Per-user behavioural depth ("which features does Customer X use?")
- Long-running cohort retention beyond the basics
- Server-side events without setup work
- Compliance-friendly defaults are improving but not automatic
- Many teams complement GA with Mixpanel or Amplitude

---
## Mixpanel

- Behavioural analytics tool — every action is an *event*
- Strong on funnels, retention, cohorts
- Per-user properties and per-event properties make slicing easy
- More expensive than GA at scale
- Common pairing: GA for marketing, Mixpanel for product

---
## Amplitude

- Direct competitor to Mixpanel, similar feature set
- Strong on cross-platform (web + mobile + server)
- Notebooks for ad-hoc analysis
- Generous free tier in recent years
- Picking between Mixpanel and Amplitude is largely taste

---
## Tableau

- The default for "big" BI: financial services, retail, manufacturing
- Beautiful visualisations; broad source connectivity
- Steep license costs at scale
- Server / Cloud versions for sharing
- Strong community and training resources

---
## Power BI

- Microsoft's BI platform, cheap if you have Office 365
- Tight integration with Excel, SharePoint, SQL Server
- DAX language for advanced calculations (steep learning curve)
- Dominant in enterprises that already run Microsoft
- Can feel constrained outside that ecosystem

---
## Looker / Looker Studio

- Looker (Google Cloud): semantic layer (LookML), dashboards, embedded analytics
- Looker Studio: free, simpler dashboards on common GCP sources
- Strong fit for engineering-friendly orgs that want a code-defined metrics layer
- Heavier deployment than Tableau or Power BI
- Especially common at GCP shops

---
## Open-Source BI: Metabase, Superset

- **Metabase**: easy to deploy, friendly UI, capable for most teams
- **Apache Superset**: more powerful, more configuration
- Free; you pay in operational effort
- Good fit for cost-sensitive teams that have engineering capacity
- Many startups start here, migrate to Tableau/Looker as they grow

---
## Elasticsearch + Kibana

- Originally for logs and full-text search
- Used for security, observability, sometimes analytics
- Kibana visualises Elasticsearch data
- "ELK stack" (Elasticsearch + Logstash + Kibana) is the classic deployment
- Modern variants: OpenSearch (Amazon's fork)

---
## Splunk

- Enterprise log analytics
- Powerful query language (SPL); steep learning curve
- Historically expensive; pricing reform underway
- Common in large enterprises with security-and-compliance needs
- Open-source competitors (Loki, OpenSearch) eating its low end

---
## Choosing a Tool

- Start with the *question*, not the tool
- Try the free tier or trial; build a real dashboard
- Get the consuming audience to use it — *they* are the customers
- Total cost: licences + setup + training + ongoing curation
- The "shiny demo" is rarely the daily reality

---
## A Buying Framework

- What decisions will this tool support?
- Who will use it (and at what literacy level)?
- What's the source data, and is it ready?
- 12-month total cost (not just year-1 list price)
- Exit cost: how hard is it to migrate off?

---
## Buying Lenses

![buying_framework](svg/courses/data_driven/data-analytics-for-managers/06_tools/buying_framework.svg)

---
## Tool Sprawl

- Most companies end up with 5-10 analytics tools
- Each owned by a different team, with overlapping capabilities
- Consolidation projects fail more often than they succeed
- Be intentional about scope before adding the 11th tool
- Better: master 2-3 tools deeply

---
## Common Mistakes

- Buying based on a sales demo
- Ignoring data-source compatibility
- No champion in the consuming team &#8594; tool sits unused
- Treating "we have the tool" as "we have the capability"
- Over-investing in tools relative to people skills
