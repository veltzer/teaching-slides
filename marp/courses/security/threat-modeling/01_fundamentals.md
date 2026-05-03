---
tags:
  - security:threat-modeling
  - concepts:fundamentals
level: intermediate
category: security
audience:
  - audiences:developers
  - audiences:security-professionals

---
# Threat Modeling Fundamentals

---
## What This Chapter Covers

- What threat modeling is and what it is not
- Where it fits in the development lifecycle
- Attacker profiles and threat actor models
- Scoping a threat model
- Iteration: threat models that stay alive

---
## What Is Threat Modeling?

- A structured analysis of a system's security
- "What can go wrong?" answered before it does
- Identifies threats, ranks them, drives mitigation
- Outputs: a model, a threat list, mitigation actions
- Inputs: system design, attacker profile, security goals

---
## Four Questions, Always

- What are we building?
- What can go wrong?
- What are we going to do about it?
- Did we do a good job?
- These four frame every methodology — STRIDE, PASTA, etc

---
## The Four Questions Visualized

![threat_questions](svg/courses/security/threat-modeling/01_fundamentals/threat_questions.svg)

---
## Four Questions Visualised

![four_questions](svg/courses/security/threat-modeling/01_fundamentals/four_questions.svg)

---
## Why It Matters

- Security bugs found in design are 10x cheaper than in code
- Code review can't see architectural flaws
- Penetration testing finds symptoms, not root causes
- Threat modeling catches "you forgot to authenticate that path"
- Compliance increasingly demands documented threat analysis

---
## What Threat Modeling Is Not

- Not a checklist exercise
- Not a one-time workshop you forget about
- Not exclusive to security teams
- Not a replacement for testing and code review
- Not something to do "if there is time"

---
## When to Threat Model

- Early in design — sketch the system, sketch the threats
- Whenever the architecture changes meaningfully
- When new dependencies, integrations, or data flows appear
- Before each major release as a final check
- After incidents — your model missed something

---
## Threat Modeling in the SDLC

![sdlc_placement](svg/courses/security/threat-modeling/01_fundamentals/sdlc_placement.svg)

---
## Who Participates?

- Architects and senior developers (system knowledge)
- Security engineers (threat knowledge)
- Product managers (data sensitivity, user impact)
- Operations (real production constraints)
- A mix beats a security-only review every time

---
## Attacker Profiles

- Script kiddie — opportunistic, automated tools
- Skilled criminal — financially motivated, persistent
- Insider — already inside, hard to detect
- Nation-state — well-resourced, patient, targeted
- Different profiles target different assets

---
## Attacker Profile Comparison

![attacker_profiles](svg/courses/security/threat-modeling/01_fundamentals/attacker_profiles.svg)

---
## Threat Actor Considerations

- Capability — what skills and tools they have
- Motivation — money, ideology, espionage, revenge
- Opportunity — what access they realistically achieve
- Risk tolerance — how much heat they accept
- Right model: think about the actors *most likely* for your system

---
## Defining Scope

- Pick a subsystem, not the whole world
- Boundaries: what's in, what's out, what's a dependency
- Time-boxed: a threat model that takes 6 months is dead
- Specific: "the order placement flow" beats "the e-commerce app"
- Document the scope explicitly to prevent drift

---
## Security Assumptions

- "We trust the database server" — write it down
- "TLS is enforced everywhere" — write it down
- "Logs are tamper-evident" — write it down
- Assumptions become the audit trail of your model
- An untrue assumption is a hidden threat

---
## Constraints and Trade-Offs

- Performance, cost, time-to-market all push back on security
- A threat model surfaces these conflicts explicitly
- "Encrypt all PII" vs "10ms p99 latency" — pick a strategy
- Document the *decision*, not just the threat
- Future engineers need to know why something is or isn't done

---
## Iterative Threat Modeling

- Do not aim for perfect — aim for current and useful
- Update the model when the system updates
- Keep it close to the code — Markdown in the repo, not a wiki nobody reads
- A 60% accurate model used weekly beats a 95% model gathering dust
- Treat the model as living documentation

---
## Output Artifacts

- A data flow diagram (or equivalent)
- A list of identified threats
- A risk rating for each (qualitative or numeric)
- Mitigation status: planned, implemented, accepted
- A history of decisions for future reviewers

---
## Common Misconceptions

- "We're agile, we don't have time" — agile teams need *lighter* threat models
- "We use a framework, it's secure" — frameworks have flaws and misuse
- "Pen tests cover this" — pen tests don't see architecture
- "We're not a target" — automated attacks don't care
- "Compliance covers it" — compliance is the floor, not the ceiling

---
## Lightweight Threat Modeling

- Whiteboard a diagram in 30 minutes
- Walk through STRIDE per element in another 60
- Capture top 5 threats, decide on each
- Total: half a day per moderate feature
- Not a 200-page document — a living artifact

---
## Maturity Stages

- Stage 0 — none, hope-driven security
- Stage 1 — ad-hoc, when someone remembers
- Stage 2 — required for major changes, documented
- Stage 3 — embedded in design reviews, tracked in tickets
- Stage 4 — automated where possible, integrated with CI

---
## Tools or Pen and Paper?

- Pen and paper for the first pass — speed matters
- Diagram tool (draw.io, Lucidchart) for shareable artifacts
- Specialized tools (Microsoft TMT, Threat Dragon) for repeatable analysis
- Code-as-model tools (Threagile) for CI integration
- The right tool depends on your stage and team

---
## Course Roadmap

- Chapter 2 — Data flow diagrams: the foundation
- Chapter 3 — STRIDE: systematic threat enumeration
- Chapter 4 — DREAD: ranking what we found
- Chapter 5 — Attack trees and PASTA
- Chapter 6 — LINDDUN for privacy
- Chapter 7 — Modeling for microservices, cloud, APIs
- Chapter 8 — Integrating threat modeling and tracking remediation

---
## Summary

- Threat modeling answers "what can go wrong?" early
- Iterative, scoped, lightweight — not a one-shot artifact
- Multidisciplinary — architects, security, product, ops
- The four questions structure every methodology
- The goal is fewer security bugs, faster, cheaper
