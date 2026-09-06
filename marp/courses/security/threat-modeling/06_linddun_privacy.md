---
tags:
  - security:threat-modeling
  - methodology:linddun
  - concepts:privacy
level: intermediate
category: security
audience:
  - audiences:developers
  - audiences:security-professionals

---

# LINDDUN: Privacy Threats

---

## What This Chapter Covers

- Why privacy needs a separate methodology
- The seven LINDDUN categories
- Mapping LINDDUN to GDPR and similar regulations
- Per-element analysis with LINDDUN
- Mitigation patterns for privacy threats

---

## Why Privacy Is Not Just Security

- Security threats: confidentiality of data
- Privacy threats: appropriate use of data
- A perfectly secure system can still violate privacy
- Example: linking pseudonymous accounts violates privacy without leaking data
- LINDDUN was designed to fill this gap

---

## LINDDUN Categories

- **L**inkability
- **I**dentifiability
- **N**on-repudiation
- **D**etectability
- **D**isclosure of information
- **U**nawareness
- **N**on-compliance

---

## LINDDUN Visualized

![linddun_overview](svg/courses/security/threat-modeling/06_linddun_privacy/linddun_overview.svg)

---

## Categories Detailed

![linddun_categories](svg/courses/security/threat-modeling/06_linddun_privacy/linddun_categories.svg)

---

## Linkability

- Threat: separate items can be tied to the same subject
- Example: combining "user 42 clicked X" and "user 42 bought Y" reveals behavior
- Cookies, device fingerprints, account IDs all enable linking
- Mitigations: pseudonymization, isolated identifiers, data minimization
- Tension with personalization — make the trade-off explicit

---

## Identifiability

- Threat: a subject can be uniquely identified
- Example: re-identifying anonymized data via combining attributes
- The famous "anonymized" data sets that weren't
- Mitigations: k-anonymity, differential privacy, attribute suppression
- A particular concern when sharing data sets externally

---

## Non-Repudiation (Unwanted)

- For privacy: subject cannot deny an action when they should be able to
- Different from security: in security, non-repudiation is desired
- Example: a whistleblowing platform that proves who submitted what
- Mitigations: deniable channels, ephemeral credentials, careful logging
- Affects sensitive systems: healthcare, dissident, journalism

---

## Detectability

- Threat: an outsider can tell that an item exists, even without seeing it
- Example: confirming that someone is in a sensitive support program
- Existence reveals information even when content is hidden
- Mitigations: dummy data, fixed-size encryption, oblivious access
- Hard to mitigate fully — a useful threat to surface in design

---

## Disclosure of Information

- Threat: information leaks to unauthorized parties
- Overlaps with STRIDE's information disclosure
- Privacy lens: whose data, what categories, to whom
- Mitigations: encryption, access control, careful API design
- Especially important for special-category data (health, race, religion)

---

## Unawareness

- Threat: subject is unaware of how their data is collected or used
- Example: data harvested by a vendor without notice
- The opt-in/opt-out, dark-patterns, hidden-tracking territory
- Mitigations: clear consent UX, privacy notices, dashboards
- Often the legal team's primary concern

---

## Non-Compliance

- Threat: the system violates laws or contractual obligations
- GDPR, CCPA, HIPAA, sectoral regulations
- Examples: cross-border data transfers, retention violations
- Mitigations: data flow inventories, retention controls, contractual flow-downs
- The "thing the lawyers worry about"

---

## Per-Element Analysis

- Like STRIDE, LINDDUN can be applied per DFD element
- Each element type maps to applicable LINDDUN categories
- Data flows: linkability, disclosure
- Data stores: identifiability, disclosure, non-compliance
- Processes: detectability, unawareness

---

## LINDDUN and GDPR

- GDPR's principles map to LINDDUN categories
- Lawfulness — non-compliance
- Purpose limitation — unawareness, non-compliance
- Data minimization — linkability, identifiability
- Storage limitation — non-compliance
- LINDDUN is a structured way to threat-model GDPR exposure

---

## LINDDUN and CCPA / Other Regs

- CCPA — opt-out, deletion, data sale notification
- HIPAA — sectoral health data with specific controls
- COPPA — children's data
- Each has its own emphasis; LINDDUN remains the structured tool
- The threats, then mitigations, then map to specific obligations

---

## Worked Example: Analytics Pipeline

- Element: telemetry events from mobile app
- Linkability: device ID enables session linking
- Identifiability: combining attributes can re-identify
- Detectability: opening the app is itself a signal
- Disclosure: third-party analytics SDK has access
- Unawareness: opt-out flow buried in settings
- Non-compliance: cross-border transfer to a region without adequacy

---

## Privacy Mitigation Patterns

- Pseudonymization — separate identifiers from PII
- Encryption at rest and in transit
- Data minimization — collect less, retain less
- Local processing — keep data on device when possible
- Differential privacy — add noise to aggregate queries

---

## Privacy by Design

- Privacy considered from the start, not bolted on
- Data flows mapped before they're built
- Default to private — users opt in, not out
- Document the legal basis for each data use
- LINDDUN structures this into actionable threats

---

## Privacy Engineering vs Privacy Policy

- Policy says what you do; engineering enforces it
- LINDDUN catches gaps where policy can't reach
- Example: policy says "we don't share with third parties" — but the analytics SDK does
- Engineering controls turn policy into reality
- Threat modeling exposes the gap

---

## Tools for LINDDUN

- LINDDUN GO — a card-based facilitated workshop
- Microsoft Threat Modeling Tool with privacy extensions
- OWASP Threat Dragon — threat libraries that include privacy
- Spreadsheet templates — start there if no specialized tool
- Tooling matters less than discipline

---

## Common Pitfalls

- Treating privacy as a legal-only concern
- Confusing "encrypted" with "private" — encryption doesn't help linkability
- Skipping "unawareness" because it's UX — it's a real threat
- Missing third-party data flows in the DFD
- Updating the threat model only when regulations change

---

## Privacy Threat Categories That Surprise

- Voice and video — biometric data, often regulated
- ML models that memorize training data — disclosure threat
- Recommender systems revealing user attributes
- Search queries persisted longer than needed
- Server access logs containing identifiers

---

## When to Apply LINDDUN

- Any system handling personal data
- Especially: health, financial, location, biometric, children's data
- Before launching a new feature that changes data flows
- Annually for systems under GDPR
- After privacy incidents or regulatory changes

---

## Integrating LINDDUN With STRIDE

- STRIDE for security threats
- LINDDUN for privacy threats
- Same DFD, two passes
- Some threats span both (information disclosure)
- Mitigations may overlap; track each lineage

---

## Summary

- LINDDUN — seven categories of privacy threats
- Privacy is not the same as security; both are needed
- Maps cleanly to GDPR and similar regulations
- Per-element analysis with mitigation patterns
- Privacy threat modeling catches the gaps policy cannot
