---
tags:
  - data-and-ai:reporting
  - data-and-ai:communication
level: beginner
category: data-science
audience:
  - audiences:data-analysts

---
# Reporting

---
## What This Chapter Covers

- Report types and their purposes
- Structuring an analytical report
- Automating reporting workflows
- Presenting findings to stakeholders
- Recommendations and next steps
- The handoff to action

---
## Report Types

- **Recurring**: same metrics, regular cadence (weekly, monthly)
- **Ad-hoc**: one-off answer to a specific question
- **Deep-dive**: multi-week analysis on a strategic question
- **Status**: project progress and risks
- Each has a different structure and audience

---
## What a Report Is For

- A document that *triggers* a decision or *records* one
- Both informs and persuades
- Stands alone — can be read without the analyst present
- Lives longer than a slide deck
- Pre-meeting reading material if you're lucky

---
## Structuring an Analytical Report

- **Executive summary**: 3-5 bullets, the headline
- **Question and context**: why we did this
- **Approach**: how we did it (briefly)
- **Findings**: what we learned
- **Recommendations**: what we should do
- **Caveats**: what we don't know
- **Appendix**: data, methodology details

---
## The Executive Summary

- The single most important section
- Most readers stop here
- 3-5 bullets, each one sentence
- Lead with the recommendation
- "We should do X because Y, with Z risk" is the template

---
## Findings

- Lead with the most important
- Each finding gets a heading
- Numbers, charts, brief interpretation
- Cite the source and the date range
- Don't bury the lede in a long methodology section

---
## Recommendations

- Concrete: who should do what, by when
- Tied to findings: each recommendation references the finding that motivated it
- Quantified where possible: expected impact
- Includes risks and prerequisites
- The bridge between analysis and action

---
## Caveats

- What you don't know
- Data quality issues that might affect conclusions
- Assumptions you made
- Alternative interpretations
- Honest caveats build trust; missing caveats break it

---
## Automated Reports

- Scheduled queries that produce a report
- Tools: Hex, Mode, Tableau Subscriptions, Looker Schedules, custom scripts
- Email or Slack delivery
- Same content every time, fresh data
- Frees analyst time from repetitive runs

---
## Building an Automation

- Parameterise the date range
- Templated narrative around the data
- Tested for edge cases (missing data, schema changes)
- Owner per report; alerts on failure
- Documented in a runbook

---
## When Automation Helps

- Recurring reports with stable structure
- Audiences that want consistency
- Metrics where the *trend* matters more than fresh interpretation
- Compliance or audit reports
- Most weekly status reports

---
## When Automation Hurts

- Stakeholders need a *story*, not numbers
- The data is exploratory, not stable
- Schema and definitions are still drifting
- New questions arise every cycle
- Some reports need a human in the loop

---
## Presenting Findings

- Slides for live presentation; reports for reading
- Slides: one message per slide, headline as title
- Don't read the slide; talk *through* it
- Anticipate questions; have backup slides ready
- Practice once — really

---
## Stakeholder Q&A

- "I don't know" is acceptable; "I'll find out" is the follow-up
- Don't bluff; data people who bluff get caught fast
- Take notes on questions; they often become the next analysis
- Some stakeholders test analysts with known answers
- Calibration over time builds trust

---
## After the Report

- Track whether the recommendation was acted on
- Check whether the predicted outcome materialised
- Calibration: were our predictions accurate?
- Lessons feed the next analysis
- This loop is what makes an analyst trusted

---
## Recommendations and Next Steps

- Always end the report with a list
- Each item: who, what, by when
- Owner accountable for follow-through
- Next analyst meeting reviews status
- Without this, reports go on a shelf

---
## Common Mistakes

- 50-page reports nobody reads
- Buried recommendations
- No caveats — overconfidence backfires
- Automated reports nobody maintains
- "Send me the data" without analysis or recommendation

---
## Course Wrap-Up

- The data analyst's job is *answering questions* and *communicating answers*
- SQL, Python, Excel, Tableau are tools; thinking is the skill
- Cleaning takes most of the time; budget for it
- Statistics keeps you honest about uncertainty
- Storytelling is what makes the work matter
- Iterate on your craft over years; tools change, fundamentals stay
