---
tags:
- security:forensics
- security:compliance
- practices:documentation
level: intermediate
category: security
audience:
- audiences:forensics-investigators
- audiences:security-professionals
- audiences:legal

---

# Writing an Official Digital Forensics Report
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## Overview

![title](svg/lectures/security/forensics_report_writing/title.svg)

---

## What This Lecture Covers

1. What an official forensic report is, and who reads it
1. The standards and rules that govern the report
1. The standard structure, section by section
1. How to fill in each section: what goes in, what stays out
1. Language: facts, inferences, opinions, and levels of certainty
1. Review, signing, versioning, and release
1. Common mistakes and a final checklist

---

## Scope of This Lecture

- This lecture is about the **report**, not about the investigation
- It assumes the examination work is already done and documented
- No acquisition, analysis, or tool techniques are taught here
- The question answered is: *how do I turn my work into a document that stands up*
- The same skeleton fits criminal, civil, internal, and incident response cases

---

## What Is an Official Forensic Report?

- The **formal, signed record** of a digital forensic examination
- States what was examined, how, by whom, and what was found
- Written so that another qualified examiner can **reproduce** the work
- Written so that a non-technical reader can **understand** the findings
- May become an exhibit in court, an annex to a regulator filing, or a board document
- Once released, it is permanent: every word may be quoted back to you

---

## Who Reads the Report

![report_audience](svg/lectures/security/forensics_report_writing/report_audience.svg)

---

## Kinds of Reports

| Kind | Purpose | Typical reader |
|------|---------|----------------|
| Preliminary / interim | Early findings, explicitly provisional | Case lead, management |
| Full examination report | Complete record of the examination | Investigators, counsel |
| Expert witness report | Opinion evidence for a court | Judge, jury, opposing expert |
| Executive brief | Decisions and business impact | Board, executives |
| Incident report | Response record for an organization | Security team, regulator |

---

## Kinds of Reports (cont.)

- Decide the kind **before** writing: it fixes the structure, the tone, and the rules
- An interim report must say *interim* on every page
- An expert witness report follows the court's rules, not your template
- An executive brief never replaces the full report; it points to it
- One case often produces several kinds, all from the same case file

---

## The Standards Landscape

![standards_map](svg/lectures/security/forensics_report_writing/standards_map.svg)

---

## ISO/IEC Standards

- **ISO/IEC 27037**: identification, collection, acquisition, preservation
    - Defines what must be *documented* at each step, which the report draws on
- **ISO/IEC 27041**: assurance that methods are suitable and validated
- **ISO/IEC 27042**: analysis, interpretation, and **reporting** of digital evidence
    - The core reporting standard: content, competence, and peer review
- **ISO/IEC 27043**: the overall investigation process model
- **ISO/IEC 17025**: laboratory accreditation, including requirements on reports of results

---

## Guidelines and Practice Bodies

- **NIST SP 800-86**: forensics in incident response, with a dedicated reporting phase
- **SWGDE**: requirements for report writing in digital and multimedia forensics
- **ACPO / NPCC Good Practice Guide**: the four principles, including the audit trail
- **ENFSI**: guidelines for evaluative reporting and verbal scales of support
- **Forensic Science Regulator Code of Practice** (UK): statutory requirements for reports
- Your organization's or laboratory's own **SOP** and report template

---

## Legal Rules That Shape the Report

- **US federal courts**: Rule 702 (expert testimony) and the *Daubert* standard
    - The method must be testable, reviewed, with known error rates, and accepted
- **US civil cases**: FRCP Rule 26(a)(2)(B) lists what an expert report must contain
    - Opinions and their basis, data considered, exhibits, qualifications, prior testimony, compensation
- **England and Wales**: Criminal Procedure Rules Part 19, Civil Procedure Rules Part 35
    - Require a statement of truth and a declaration of the expert's duty to the court
- Always ask counsel which jurisdiction and which rules apply **before** drafting

---

## Principles Every Standard Shares

1. **Accuracy**: every statement is supported by recorded evidence
1. **Objectivity**: findings for and against any hypothesis are reported
1. **Reproducibility**: another examiner can repeat the work from the report
1. **Completeness**: limitations, gaps, and errors are disclosed
1. **Clarity**: a lay reader can follow the conclusions
1. **Traceability**: every finding links back to an exhibit and a note

---

## The Standard Report Structure

![report_structure](svg/lectures/security/forensics_report_writing/report_structure.svg)

---

## Report Skeleton

```markdown
- Cover page and document control
- Executive summary
- Examiner details and qualifications
- Authorization, request, and scope
- Evidence received (exhibit list)
- Chain of custody
- Methodology, tools, and environment
- Findings
- Timeline of events
- Conclusions and opinions
- Limitations
- Declarations and signature
- Appendices
```

---

## Cover Page and Document Control

- Report title, **case number**, and your laboratory's report number
- Classification and handling marking (e.g., *Confidential, Legal Privilege*)
- Requesting party, examiner, reviewer, and dates
- **Version** and **status**: draft, interim, final, supplementary
- Page numbering in the form *page N of M* on every page
- A distribution list: who received which version, and when

---

## Document Control Table

| Version | Date | Author | Change | Status |
|---------|------|--------|--------|--------|
| 0.1 | 2026-03-02 | J. Doe | First draft | Draft |
| 0.2 | 2026-03-05 | J. Doe | Peer review comments addressed | Draft |
| 1.0 | 2026-03-07 | J. Doe | Approved by A. Smith | Final |
| 1.1 | 2026-04-11 | J. Doe | Supplementary exhibit 7 | Supplementary |

- Never overwrite a released version; issue a new one and record why

---

## Executive Summary

- **Written last**, read first; often the only page a decision maker reads
- One page at most, in plain language with no jargon
- States: the question asked, what was examined, the key findings, the conclusion
- Every claim here must appear, with support, in the body
- No new information that is not in the findings section
- Avoid adjectives that sound like advocacy: *clearly*, *obviously*, *undeniably*

---

## Executive Summary: Example

```markdown
On 2026-03-01 ACME Ltd requested an examination of a laptop
(exhibit JD/1) to determine whether customer data was copied to
removable media between 2026-02-10 and 2026-02-20.

A USB storage device was connected to JD/1 on 2026-02-14 at
21:07 UTC. Records show 1,284 files from the "Customers" share
were accessed in the following eleven minutes. No evidence was
found that the files were transmitted over the network.

In my opinion the findings provide strong support for the
proposition that the files were copied to the USB device.
```

---

## Examiner Details and Qualifications

- Full name, role, organization, and contact details
- Relevant qualifications, certifications, and training
- Years and type of experience **relevant to this case**
- Accreditation of the laboratory, if any, and its scope
- For expert reports: prior testimony and publications as the rules require
- Name every other person who did part of the work, and what they did

---

## Authorization, Request, and Scope

- **Who** asked for the examination, **when**, and under what authority
    - Warrant, court order, consent, contract, or internal policy reference
- The **questions** you were asked, quoted exactly as received
- What is **in scope**: devices, accounts, date ranges, data types
- What is **out of scope**, and any restrictions imposed (privilege, privacy)
- Changes to scope during the work, with date and who approved them

---

## Evidence Received: The Exhibit List

| Exhibit | Description | Serial / ID | Received | Hash (SHA-256) |
|---------|-------------|-------------|----------|----------------|
| JD/1 | Laptop, Dell Latitude 7440 | `5CG2341XYZ` | 2026-03-01 | n/a (device) |
| JD/1/A | Image of internal SSD of JD/1 | image file | 2026-03-02 | `9f2c…e41a` |
| JD/2 | USB flash drive, 64 GB | `AA0123456` | 2026-03-03 | `41b7…0cd9` |

- One row per item, with a **unique exhibit reference** used everywhere after
- Put full hash values in an appendix; shorten them only in tables

---

## Evidence Received: Describing Items

- Describe each item as received: make, model, serial, condition, seals
- Record the seal numbers and whether they were intact on arrival
- Note anything unusual: damage, missing parts, powered on, open packaging
- Derived items (images, exports) get their own exhibit references
- Photographs of items as received go in an appendix, referenced by number

---

## Chain of Custody

![chain_of_custody](svg/lectures/security/forensics_report_writing/chain_of_custody.svg)

---

## Chain of Custody: What to Record

| Exhibit | Date / time (UTC) | Released by | Received by | Purpose | Seal |
|---------|-------------------|-------------|-------------|---------|------|
| JD/1 | 2026-03-01 09:14 | P. Green (client) | J. Doe | Examination | S-0412 intact |
| JD/1 | 2026-03-01 09:40 | J. Doe | Evidence store | Storage | S-0412 intact |
| JD/1 | 2026-03-02 08:05 | Evidence store | J. Doe | Imaging | S-0412 broken, resealed S-0419 |

- Every transfer, every opening, every resealing: no gaps in time
- The report summarizes the chain; the signed forms go in an appendix

---

## Methodology, Tools, and Environment

- Describe **what** was done and **why**, at a level another examiner can repeat
- Reference the SOP or documented procedure followed, by identifier and version
- List every tool with **name, version, and vendor**, and its validation status
- Describe the examination environment: workstation, OS, write blocking
- Record any **deviation** from the procedure and its justification
- Do not paste tool manuals; cite them

---

## Tools Table

| Tool | Version | Purpose | Validation |
|------|---------|---------|------------|
| Imaging tool A | 4.7.1 | Acquisition of JD/1 | Lab validation VR-2025-11 |
| Analysis suite B | 2.3.0 | Artifact parsing | Lab validation VR-2026-02 |
| Hash utility C | 9.4 | Integrity verification | Vendor test set |

- A tool with no validation record is a question waiting in cross-examination
- When a finding relies on one tool, say whether it was verified by a second method

---

## Findings

- The heart of the report: **one finding per subsection**, each with a short heading
- Each finding states: the observation, the exhibit, the location, and the time
- Link every finding to its supporting artifact in an appendix
- Report findings that **weaken** the requesting party's case as well
- Keep interpretation separate from observation (see the language section)
- Order findings logically: by question asked, by exhibit, or chronologically

---

## Writing a Single Finding

```markdown
### Finding 3: USB storage device connected to JD/1

Observation: The system registry of exhibit JD/1/A records a USB
storage device with serial number AA0123456, first connected on
2026-02-14 at 21:07:32 UTC (Appendix C, item C-12).

Correlation: This serial number matches exhibit JD/2.

Significance: This places JD/2 in contact with JD/1 within the
date range in question.
```

---

## Timeline of Events

- A chronological table of the significant events across all exhibits
- **One time zone** for the whole report, normally UTC, stated at the top
- Record the source clock and any known offset or drift for each exhibit
- Each row cites the finding and exhibit it comes from
- Mark events whose time is approximate or inferred
- Keep it to the events that matter; full exports go in an appendix

---

## Timeline Example

| Time (UTC) | Event | Exhibit | Source |
|------------|-------|---------|--------|
| 2026-02-14 21:02:10 | User `jsmith` logs on | JD/1/A | Finding 2 |
| 2026-02-14 21:07:32 | USB device AA0123456 connected | JD/1/A | Finding 3 |
| 2026-02-14 21:08–21:19 | 1,284 files in `Customers` accessed | JD/1/A | Finding 4 |
| 2026-02-14 21:21:45 | USB device removed | JD/1/A | Finding 3 |

---

## Conclusions and Opinions

- Answer **each question from the scope**, in the same order, one by one
- Each conclusion cites the findings it rests on
- State the alternative explanations that were considered, and why they were rejected
- If a question cannot be answered, say so and say why
- Clearly label which statements are **opinion**, and give the basis for each
- Never conclude beyond what the findings support

---

## Limitations

- What could **not** be examined: encrypted volumes, missing devices, damaged media
- Restrictions from the scope or authorization that may affect the conclusions
- Known limitations or error rates of the tools and methods used
- Assumptions made, such as clock accuracy or account ownership
- Data that may exist elsewhere and was not provided
- A limitations section strengthens the report; hiding them destroys it

---

## Declarations and Signature

- A **statement of truth**: the report is true to the best of your knowledge
- A declaration of **independence** and of your duty to the court, where required
- Confirmation that you followed the stated procedures, or disclosure of where not
- A statement that you will update the report if new information changes it
- Signature, printed name, date, and the reviewer's signature
- Use the **exact wording** the applicable court rules prescribe

---

## Appendices

- Full exhibit list with complete hash values
- Signed chain of custody forms
- Tool list with versions and validation references
- Detailed artifact listings, screenshots, and extracts cited by findings
- Glossary of technical terms for the lay reader
- Examiner CV, if the rules require it
- Number every appendix item, so findings can cite *Appendix C, item C-12*

---

## Language: Fact, Inference, Opinion

![fact_inference_opinion](svg/lectures/security/forensics_report_writing/fact_inference_opinion.svg)

---

## Language: Writing Rules

- Write in the **first person** and the **past tense**: *I examined*, *I found*
- Use precise, neutral terms: *the account `jsmith` was used*, not *Smith did it*
- Attribute actions to accounts, devices, and processes, not to people
    - Placing a person at the keyboard needs evidence of its own
- Define every technical term the first time, or in the glossary
- Prefer numbers to adjectives: *1,284 files*, not *a large number of files*
- Never use emotive or accusatory words: *suspicious*, *malicious*, *guilty*

---

## Language: Weak and Strong Phrasing

| Avoid | Prefer |
|-------|--------|
| The suspect deleted the files | The files were deleted while account `jsmith` was logged on |
| It is obvious that data was stolen | The findings are consistent with data being copied to JD/2 |
| The hacker used malware | An executable not part of the OS was found; see Finding 6 |
| Around midnight | 2026-02-14 23:58:12 UTC |
| I am sure | In my opinion the findings provide strong support for … |

---

## Expressing Certainty

- Evaluative opinions compare **at least two propositions**
    - e.g., *the files were copied by the user* versus *the files were never copied*
- State how much more likely the findings are under one than the other
- Use a **defined verbal scale** and include it in the report
- Never state certainty that the evidence cannot carry
- *Consistent with* is weak; say so, or avoid it alone

---

## A Verbal Scale of Support

| Verbal expression | Meaning |
|-------------------|---------|
| No support | Findings equally likely under both propositions |
| Weak support | Findings slightly more likely under one proposition |
| Moderate support | Findings clearly more likely under one proposition |
| Strong support | Findings much more likely under one proposition |
| Very strong support | Findings far more likely under one proposition |

- Based on ENFSI guidelines; use the scale your laboratory has adopted

---

## Handling Sensitive Content

- Do not reproduce indecent, private, or privileged material in the report body
- Describe it, and reference it by exhibit and item; hold the content separately
- Redact personal data not needed to answer the questions
- Mark privileged sections and follow counsel's instructions on distribution
- Record every redaction, so the unredacted version can be produced if ordered

---

## The Review and Release Process

![review_process](svg/lectures/security/forensics_report_writing/review_process.svg)

---

## Technical and Administrative Review

- **Technical review** by a second qualified examiner
    - Are the findings supported by the notes and artifacts?
    - Are the conclusions justified, and the alternatives considered?
- **Administrative review** for form and completeness
    - Case numbers, exhibit references, page numbers, spelling, signatures
- Record who reviewed what, when, and how disagreements were resolved
- The reviewer signs the report or a review record kept on file

---

## Release, Versions, and Supplements

- Release the final version as a **signed, locked PDF**, and record its hash
- Record every recipient on the distribution list
- Never edit a released report: issue a **supplementary report** instead
- A supplement states what changed, why, and which report it supplements
- Keep the case file (notes, drafts, review records) as long as policy requires
- Drafts may be disclosable: write them carefully too

---

## Common Mistakes

- Conclusions that go beyond the findings, or answer questions never asked
- Mixed time zones, or times with no time zone at all
- Exhibit references that change names halfway through the report
- Tool output pasted into the body with no explanation
- No limitations section, or one that hides inconvenient gaps
- Attributing actions to a person when the evidence shows only an account
- Findings that help the other side quietly left out

---

## Final Checklist

1. Every question from the scope has an answer or a stated reason why not
1. Every finding cites an exhibit, a location, a time, and an appendix item
1. Every exhibit has a unique reference, a description, and a hash where applicable
1. Chain of custody is complete with no gaps
1. Tools are listed with versions and validation references
1. One time zone, stated at the top, used everywhere
1. Opinions are labelled, use the defined scale, and give their basis

---

## Final Checklist (cont.)

8. Limitations and assumptions are disclosed
9. The executive summary contains nothing absent from the body
10. Technical and administrative reviews are recorded
11. The declarations use the wording the applicable rules require
12. Version, status, page numbering, and distribution list are correct
13. The released PDF is signed, locked, and its hash recorded

---

## Key Takeaways

- The report is the product of the examination; the work is only as good as its report
- Follow a recognized structure, and the rules of the forum that will read it
- Separate observation, inference, and opinion, and label each
- Make every statement traceable to an exhibit and reproducible by another examiner
- Disclose limitations and contrary findings: objectivity is the report's credibility
- Review, sign, lock, and never edit a released version
