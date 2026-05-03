---
tags:
  - security:threat-modeling
  - methodology:stride
level: intermediate
category: security
audience:
  - audiences:developers
  - audiences:security-professionals

---
# STRIDE Methodology

---
## What This Chapter Covers

- The STRIDE acronym and its origin
- Each category: meaning, examples, mitigations
- STRIDE-per-element vs STRIDE-per-interaction
- Driving STRIDE from a DFD
- Strengths, weaknesses, and traps

---
## Origin and Use

- Developed at Microsoft in the late 1990s
- Designed for systematic threat enumeration
- One of the most widely adopted methodologies
- Pairs naturally with DFDs
- Excellent training tool — concrete and exhaustive

---
## The STRIDE Categories

- **S**poofing — pretending to be someone else
- **T**ampering — modifying data in transit or at rest
- **R**epudiation — denying you did something
- **I**nformation disclosure — leaking data
- **D**enial of service — making the system unavailable
- **E**levation of privilege — gaining unauthorized capabilities

---
## STRIDE Visualized

![stride_overview](svg/courses/security/threat-modeling/03_stride/stride_overview.svg)

---
## Spoofing

- Threat: an attacker impersonates a user or service
- Examples: stolen passwords, forged tokens, DNS poisoning
- The opposite of authentication
- Mitigations: strong auth (MFA), mutual TLS, signed tokens
- Verify identity before granting access — every time

---
## Tampering

- Threat: data is modified without authorization
- Examples: SQL injection writes, modified file contents, MITM edits
- The opposite of integrity
- Mitigations: input validation, signed/hashed data, immutable logs
- "Trust but verify" — every input, every storage layer

---
## Repudiation

- Threat: a user denies an action they took
- Examples: "I didn't place that order" with no audit trail
- The opposite of non-repudiation
- Mitigations: tamper-evident logs, digital signatures, audit trails
- Critical for finance, compliance, contractual systems

---
## Information Disclosure

- Threat: data leaks to unauthorized parties
- Examples: error messages with stack traces, public S3 buckets, side channels
- The opposite of confidentiality
- Mitigations: encryption, access control, careful error handling
- Defaults matter — assume "expose" is the default and lock it down

---
## Denial of Service

- Threat: legitimate users cannot use the system
- Examples: traffic floods, resource exhaustion, billing exhaustion
- The opposite of availability
- Mitigations: rate limits, quotas, CDN/WAF, scaling, circuit breakers
- Increasingly economic: denial via cloud bill explosion

---
## Elevation of Privilege

- Threat: an attacker gains capabilities they shouldn't have
- Examples: regular user reaching admin, container escape, exploited bug
- The opposite of authorization
- Mitigations: least privilege, role separation, defense in depth
- The crown-jewel threat — once achieved, everything else follows

---
## STRIDE With Examples

![stride_examples](svg/courses/security/threat-modeling/03_stride/stride_examples.svg)

---
## STRIDE Per Element Visualised

![stride_per_element](svg/courses/security/threat-modeling/03_stride/stride_per_element.svg)

---
## STRIDE Per Element

- For each DFD element, ask: which of the STRIDE threats apply?
- External entities: spoofing, repudiation
- Processes: all six categories
- Data stores: tampering, disclosure, denial
- Data flows: tampering, disclosure, denial
- A simple table per element ensures coverage

---
## STRIDE Per Interaction

- Look at each pair of elements connected by a flow
- Each interaction has its own threat surface
- More granular than per-element
- Catches threats that emerge from a *combination* of elements
- Heavier — use when stakes warrant the depth

---
## Driving STRIDE From a DFD

- Walk the DFD element by element
- For each, write down each applicable STRIDE threat
- Be specific: "spoofing of customer account via stolen cookie"
- Vague threats cannot be mitigated
- The output is a structured threat list

---
## Worked Example

- Element: web app process accepting login
- Spoofing: credential-stuffing attack
- Tampering: modified session token
- Repudiation: user denies a login (no logs)
- Disclosure: timing attack on username existence
- DoS: flood of login attempts
- EoP: bypass of MFA via downgrade

---
## STRIDE Strengths

- Comprehensive — covers the major threat categories
- Memorable — the acronym is easy to teach
- Pairs with DFDs — direct path from design to threats
- Tool support — Microsoft Threat Modeling Tool automates this
- Outputs a structured backlog of mitigations

---
## STRIDE Weaknesses

- Generates many threats — prioritization needed (DREAD, etc)
- Misses business-logic threats — STRIDE-blind to "fraud"
- Privacy threats need LINDDUN, not STRIDE
- Can become rote — same threats every time, real ones missed
- Requires judgment to know when "doesn't apply" is correct

---
## STRIDE Pitfalls

- Treating it as a checklist with no thought
- Stopping at "spoofing applies" without specifics
- Ignoring threats deemed unlikely without analysis
- Forgetting that STRIDE is for finding, not ranking
- Letting "we have a firewall" close every threat

---
## STRIDE and Existing Mitigations

- Distinguish: identified threat vs threat with mitigation in place
- "Spoofing of admin: mitigated by MFA + IP allowlist"
- The mitigation should be testable
- Track mitigation status — implemented, planned, accepted
- Re-validate when the system changes

---
## STRIDE in Agile Teams

- Run STRIDE on the diagram for each significant story
- 30-minute standup-style review
- Capture findings as backlog items
- Review status before each release
- Don't let "no time" become "no security"

---
## Variants and Extensions

- STRIDE-LM — adds Lateral Movement and Manipulation
- E-STRIDE — extends with environmental threats
- TRIM — STRIDE-style framework focused on privacy
- Most teams stick with classic STRIDE plus prioritization
- Pick variants for specific industry needs

---
## When STRIDE Is Not Enough

- Pair with LINDDUN for privacy threats
- Pair with attack trees for goal-driven analysis
- Pair with PASTA for risk-centric depth
- Pair with abuse cases for business-logic threats
- STRIDE finds technical threats; not the only threats that exist

---
## Summary

- STRIDE: spoofing, tampering, repudiation, disclosure, DoS, elevation
- Pairs with DFDs for systematic coverage
- Per-element for breadth, per-interaction for depth
- Be specific with threats; vague threats produce vague mitigations
- Combine with risk ranking and other methodologies for full coverage
