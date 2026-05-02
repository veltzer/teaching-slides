---
tags:
  - practices:technical-writing
level: beginner
category: methodology
audience:
  - audiences:developers

---
# Audience Analysis

---
## Audience Quadrants

![audience_quadrants](svg/courses/development_methodologies/technical-writing/02_audience_analysis/audience_quadrants.svg)

---
## What This Chapter Covers

- Why audience matters
- Identifying your audience
- Adjusting tone and complexity
- User personas for documentation
- Empathy in technical communication
- Common audience mistakes

---
## Why Audience Matters

- The same content, written for different audiences, becomes different documents
- "Internal engineers" and "external customers" don't share vocabulary or context
- Junior and senior engineers need different levels of detail
- Writing for the wrong audience is the most common doc failure
- Knowing your audience is half the job

---
## Identifying Your Audience

- Who reads this? (specifically)
- What do they already know?
- What do they need to do after reading?
- How much time do they have?
- What's their motivation?

---
## Common Engineering Audiences

- Developers using your library
- Internal engineers extending the system
- New hires onboarding
- On-call engineers in incidents
- Stakeholders making decisions
- Future you, six months from now

---
## Tone Per Audience

- Customer-facing: friendly, encouraging, supportive
- Internal engineering: direct, factual, jargon-allowed
- Executive: brief, conclusion-first, business-language
- New hire: patient, comprehensive, foundational
- Same content, very different prose

---
## Complexity Calibration

- Beginner: define every term, explain every concept
- Intermediate: assume basics, explain the new parts
- Advanced: just the differences, all assumptions implicit
- Mismatching this loses the reader fast
- A "Hello World" tutorial that drops into category theory has lost the audience

---
## User Personas

- Documented profiles of typical readers
- "Alex: 3 years experience, knows Python, new to async"
- Used by content teams to make consistent decisions
- Less common in pure engineering docs; useful for libraries with many users
- 2-3 personas; not a dozen

---
## Empathy

- Imagine the reader: tired, frustrated, on a deadline
- They don't want to read your doc; they want their problem solved
- Get to the point fast
- Anticipate the next question; answer it before they ask
- Writing with empathy is the difference between great docs and adequate ones

---
## "What Would I Have Wanted To Know?"

- Think back to when you didn't know this thing
- What confused you? What clicked?
- Write for that earlier version of yourself
- A powerful technique for new-hire docs
- "I wish someone had told me X" — write that down

---
## Adjusting for International Audiences

- Plain language: shorter sentences, common words
- Avoid idioms ("hit the ground running" doesn't translate)
- Date format: ISO 8601 (2026-05-01) for unambiguous
- Currency: state explicitly (USD 100, not $100)
- Cultural references: avoid

---
## Multi-Audience Documents

- Some docs serve multiple audiences (READMEs, especially)
- Layer the content: quick start at top, deep dive below
- Anchors / links let readers jump to their level
- Don't try to write a beginner-and-expert paragraph; pick one
- Most one-stop docs end up half-good for everyone

---
## When You Don't Know Your Audience

- Ask
- Look at issue tracker / support tickets — what do real users ask?
- Check usage logs — what features get used?
- Survey, even informally
- Better to write narrowly for a known audience than broadly for an imagined one

---
## Customer vs Internal Tone Examples

- Customer: "If you encounter an issue, please reach out to our support team."
- Internal: "If it breaks, page on-call."
- Both convey the same information; tone signals who they're for
- Match the tone to where the doc lives

---
## Empathy Anti-Patterns

- "It's obvious that..."
- "Simply do X" (it's never simple if they're reading this)
- "Just" anything
- "As any engineer knows..."
- Each one tells the reader they don't belong

---
## Common Audience Mistakes

- Writing for the audience *you wish* you had instead of the one you have
- Assuming readers will read top to bottom
- Mixing audiences in one doc and confusing both
- Forgetting that future-you is also an audience
- Not asking real users what they need
