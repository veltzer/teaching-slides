---
tags:
  - security:threat-modeling
  - methodology:dread
  - concepts:risk
level: intermediate
category: security
audience:
  - audiences:developers
  - audiences:security-professionals
  - audiences:managers

---

# DREAD and Risk Rating

---

## What This Chapter Covers

- DREAD's five dimensions and how to score
- Calculating and comparing risk ratings
- DREAD's strengths and well-known limitations
- Alternatives: CVSS, qualitative matrices
- Pragmatic risk rating for real teams

---

## Why Rate Threats?

- STRIDE finds many threats — you cannot fix them all today
- Rating drives priority: which threat first, which can wait
- Rating drives accept/mitigate/transfer decisions
- A good rating is defensible and reproducible
- A bad rating is just a number with feelings

---

## DREAD Dimensions

- **D**amage potential — how bad is exploitation?
- **R**eproducibility — how reliable is the attack?
- **E**xploitability — how hard is it to perform?
- **A**ffected users — how many are impacted?
- **D**iscoverability — how easy is it to find?

---

## DREAD Visualized

![dread_dimensions](svg/courses/security/threat-modeling/04_dread_and_risk/dread_dimensions.svg)

---

## Damage Potential

- 0 — no damage
- 5 — limited individual user impact (one account)
- 10 — full system compromise, data breach, financial loss
- Consider: confidentiality, integrity, availability impact
- Consider: regulatory and reputational damage

---

## Reproducibility

- 0 — virtually impossible to reproduce
- 5 — reproducible under specific conditions
- 10 — reproducible every time, no special conditions
- A reliable exploit is a much bigger threat
- Race conditions and rare bugs may rate low here

---

## Exploitability

- 0 — requires advanced custom tooling and access
- 5 — typical attacker with publicly available tools
- 10 — script kiddie can do it from a browser
- Includes: skill, tools, time, prerequisite access
- Public exploits move this rating up dramatically

---

## Affected Users

- 0 — none
- 5 — some users in some scenarios
- 10 — all users, all the time
- Different user classes weigh differently — admins matter more
- Internal-only systems still have "users" worth considering

---

## Discoverability

- 0 — virtually undiscoverable
- 5 — discoverable through dedicated effort
- 10 — already public, on a search engine
- Controversial — "obscurity is not security" tension
- Many practitioners drop this dimension; we'll discuss why

---

## Calculating a Score

- Naive: average all five (DREAD / 5)
- Weighted: emphasize damage and exploitability
- Banding: 0-3 low, 4-6 medium, 7-8 high, 9-10 critical
- Avoid false precision — 7.4 vs 7.6 is meaningless
- Use the score to bucket, then judge

---

## Worked Example

- Threat: SQL injection in login endpoint
- Damage: 10 (full DB compromise)
- Reproducibility: 10 (every time)
- Exploitability: 9 (common tool, sqlmap)
- Affected users: 10 (everyone using auth)
- Discoverability: 10 (well-known techniques)
- Average: 9.8 — critical, fix now

---

## DREAD Strengths

- Simple — five dimensions, easy to teach
- Memorable — names stick
- Produces a comparable score
- Drives "what to fix first" conversations
- Useful entry-level rating system

---

## DREAD Weaknesses

- Subjective — your "8" is my "6"
- Discoverability is contested — drop it or weight low
- Equal weighting hides what matters most
- Microsoft itself moved away from DREAD
- Risk of false precision — a number is not a justification

---

## The Discoverability Debate

- "Discoverable threats are riskier" — true in some sense
- "Obscurity is not security" — also true
- A bug deep in the codebase is still a bug
- Many practitioners drop the dimension entirely
- Or: weight it last, use only as a tiebreaker

---

## Mitigating DREAD's Subjectivity

- Calibrate as a team — what does an "8" mean for *this* threat?
- Anchor with known examples: "this is like the Heartbleed CVE"
- Document the reasoning, not just the score
- Re-rate periodically — exploit landscape shifts
- Two raters, then reconcile, beats one rater alone

---

## CVSS as an Alternative

- Common Vulnerability Scoring System
- Industry-standard, used in CVEs and vendor advisories
- More complex: base, temporal, environmental scores
- Better for known vulnerabilities than threat-model threats
- Worth using for known CVEs in dependencies

---

## Qualitative Matrices

- 3x3 or 5x5 matrix: likelihood × impact
- Each axis: low / medium / high (or 1-5)
- Cell color: green / yellow / red
- No false-precision numbers, just buckets
- Often easier to defend in a meeting

---

## Likelihood × Impact Matrix

![risk_matrix](svg/courses/security/threat-modeling/04_dread_and_risk/risk_matrix.svg)

---

## Pragmatic Risk Rating

- Pick a system you trust your team to apply consistently
- Document the criteria for each level
- Apply the same system across the threat list
- Re-rate when the threat landscape changes
- Don't optimize the rating system — optimize the *response* to threats

---

## What to Do With a Rating

- Critical — fix before release, escalate
- High — fix in current sprint
- Medium — fix in next quarter, document
- Low — accept or backlog
- Document the *decision* explicitly per threat

---

## Risk Acceptance

- Sometimes the cost of fixing exceeds the cost of the threat
- Risk acceptance is a valid choice — when documented
- Who has authority to accept what level of risk?
- Define this *before* the threats start piling up
- Re-review accepted risks annually

---

## Risk Transfer

- Insurance, contractual liability, third-party services
- Doesn't eliminate the risk — moves who pays
- A useful tool but not a substitute for mitigation
- Reputational damage usually doesn't transfer
- Consider transfer for low-frequency, high-impact threats

---

## Common Pitfalls

- Treating DREAD scores as objective truth
- Re-rating to match a desired outcome ("we need this to be low")
- Letting one expensive-to-fix threat dominate the list
- Failing to update ratings as exploits emerge
- Stopping at the rating without making a decision

---

## Summary

- DREAD: damage, reproducibility, exploitability, affected, discoverability
- Pragmatic, simple — good for teaching, weak in precision
- Discoverability is the most controversial dimension
- Alternatives: CVSS for known CVEs, matrices for qualitative
- The rating exists to drive a decision — don't lose that purpose
