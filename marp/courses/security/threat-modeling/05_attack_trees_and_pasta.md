---
tags:
  - security:threat-modeling
  - methodology:attack-trees
  - methodology:pasta
level: intermediate
category: security
audience:
  - audiences:developers
  - audiences:security-professionals
  - audiences:architects

---
# Attack Trees and PASTA

---
## What This Chapter Covers

- Attack trees: structure, nodes, semantics
- Annotating attack trees with cost, difficulty, probability
- PASTA: a risk-centric, business-aligned methodology
- The seven PASTA stages
- When to use each, and how they complement STRIDE

---
## Why Attack Trees?

- Goal-driven instead of element-driven
- "How could an attacker achieve X?" — work backward
- Captures alternative paths to the same outcome
- Reveals the cheapest path — the one to defend first
- A complementary lens to STRIDE's per-element view

---
## Attack Tree Basics

- Root node — the attacker's goal (e.g., "exfiltrate customer data")
- Child nodes — sub-goals or attack steps
- Leaves — concrete attacker actions
- AND nodes — all children needed
- OR nodes — any child suffices

---
## Attack Tree Visualized

![attack_tree](svg/courses/security/threat-modeling/05_attack_trees_and_pasta/attack_tree.svg)

---
## Building an Attack Tree

- State the attacker's goal at the root
- Brainstorm ways to achieve it — first level of children
- Decompose each path until reaching concrete actions
- Use AND/OR to capture how steps combine
- Iterate — add detail where threats are concentrated

---
## OR vs AND Nodes

- OR: any child achieves the parent — attacker picks the easiest
- AND: every child must be achieved — defenders only need to block one
- Mixing OR and AND captures complex multi-step attacks
- AND nodes are *opportunities* for defense — break any link
- OR nodes need every branch defended

---
## Annotating Nodes

- Cost — dollars, time, or skill required
- Probability — chance an attacker succeeds at this step
- Detectability — how visible the action is
- Reversibility — can the defender undo it?
- Each annotation drives different mitigation choices

---
## Computing Properties Up the Tree

- For OR nodes — minimum cost across children (attackers pick the cheapest)
- For AND nodes — sum of child costs (all required)
- Probabilities multiply for AND, take max for OR
- Lowest-cost path is the most likely attack
- Defend it first

---
## A Worked Example

- Goal: "Read another user's emails"
- OR: steal credentials, hijack session, exploit IDOR, social engineer admin
- "Steal credentials" decomposes: phishing, credential stuffing, malware
- "Phishing" further: email phishing, SMS phishing, spear phishing
- Each leaf gets cost and probability — reveals the easy path

---
## Attack Trees in Practice

- Treat as living documents — update with new techniques
- Share across teams to spread threat awareness
- Use for tabletop exercises and red-team drills
- Useful for executive communication — visual, intuitive
- Don't try to enumerate everything — focus on critical assets

---
## Attack Trees vs STRIDE

- STRIDE — what could go wrong with each element?
- Attack trees — how could an attacker achieve their goal?
- Use both: STRIDE for breadth, attack trees for the high-stakes goals
- They generate different threats; both are useful
- Attack trees are heavier — reserve them for crown-jewel scenarios

---
## What is PASTA?

- Process for Attack Simulation and Threat Analysis
- Risk-centric, business-aligned methodology
- Seven structured stages
- More heavyweight than STRIDE — for high-stakes systems
- Strong on integrating business impact

---
## PASTA's Seven Stages

- Stage 1 — define objectives (business)
- Stage 2 — define technical scope
- Stage 3 — application decomposition
- Stage 4 — threat analysis
- Stage 5 — vulnerability and weakness analysis
- Stage 6 — attack modeling and simulation
- Stage 7 — risk and impact analysis

---
## PASTA Stages Visualized

![pasta_stages](svg/courses/security/threat-modeling/05_attack_trees_and_pasta/pasta_stages.svg)

---
## Stage 1: Define Objectives

- Business goals: revenue, compliance, brand
- Identify critical assets in business terms
- Define what "secure enough" means for this system
- Engage stakeholders — security leads, product, legal
- Output: business security objectives document

---
## Stage 2: Define Technical Scope

- Boundaries of the system being modeled
- Technical assets: services, data stores, networks
- External dependencies and trust relationships
- Where the system runs (cloud, on-prem, hybrid)
- Output: scope document with explicit in/out lists

---
## Stage 3: Application Decomposition

- DFDs, use cases, user/role models
- Architectural review
- Data classification
- Identify trust boundaries
- This is where PASTA overlaps most with STRIDE-style work

---
## Stage 4: Threat Analysis

- Identify relevant threat actors and their motivations
- Use threat intel: who attacks systems like this, how, and why?
- Build a threat library specific to your context
- Consider geopolitical, industry-specific, and supply-chain threats
- Output: a curated threat list, not a generic one

---
## Stage 5: Vulnerability Analysis

- Map known vulnerabilities to your assets
- Static analysis, dynamic analysis, dependency scanning
- Identify weaknesses, not just vulnerabilities (CWE-style)
- Cross-reference with the threats from stage 4
- Output: vulnerabilities with affected assets

---
## Stage 6: Attack Modeling

- Build attack trees for the most relevant threats
- Simulate attacks — red team, tabletop exercises
- Identify attack paths from threat actor to crown jewels
- Test the assumptions in your model
- Output: validated attack scenarios

---
## Stage 7: Risk and Impact

- Quantify business risk per threat
- Calculate potential financial and reputational impact
- Prioritize mitigations against business value
- Communicate residual risk to leadership
- Output: prioritized risk-treatment plan

---
## PASTA Strengths

- Business-aligned — risk in financial terms
- Comprehensive — covers strategy through tactics
- Threat-intel driven — relevant, not theoretical
- Strong for regulated industries (finance, healthcare)
- Drives accountability at the executive level

---
## PASTA Weaknesses

- Heavyweight — costly for small teams
- Requires threat intelligence skills
- Long cycle time — not suited for weekly modeling
- Documentation overhead is significant
- Overkill for simple internal applications

---
## When to Use Attack Trees

- High-stakes assets (crown jewels)
- After a security incident — model how it happened
- For red-team planning
- For executive communication
- Combined with PASTA stage 6

---
## When to Use PASTA

- Regulated industries with formal compliance demands
- Critical infrastructure or financial systems
- Annual or semi-annual full reviews
- Major architectural changes worth deep analysis
- When STRIDE alone leaves stakeholders unconvinced

---
## Combining Methodologies

- STRIDE — daily/sprintly threat enumeration
- Attack trees — focused deep-dives for critical assets
- PASTA — annual comprehensive risk reviews
- LINDDUN — privacy-specific overlays (next chapter)
- Pick a stack appropriate to your maturity

---
## Common Pitfalls

- Building elaborate trees nobody updates
- PASTA ceremony with no follow-through actions
- Confusing breadth with depth — many shallow threats vs few real ones
- Not engaging business stakeholders in PASTA stage 1
- Treating any methodology as a substitute for thinking

---
## Summary

- Attack trees — goal-driven, multi-step, annotated with cost
- PASTA — seven-stage business-aligned methodology
- Attack trees complement STRIDE; PASTA integrates everything
- Use methodologies in combination, not exclusion
- Heavyweight tools for high-stakes systems; lighter tools for the rest
