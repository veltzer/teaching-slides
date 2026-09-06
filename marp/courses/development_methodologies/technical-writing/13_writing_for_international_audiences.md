---
tags:
  - practices:technical-writing
  - practices:internationalisation
level: beginner
category: methodology
audience:
  - audiences:developers

---

# Writing for International Audiences

---

## Global Writing Tips

![global_writing_tips](svg/courses/development_methodologies/technical-writing/13_writing_for_international_audiences/global_writing_tips.svg)

---

## What This Chapter Covers

- Plain language principles
- Localisation considerations
- Cultural sensitivity
- What translates well, what doesn't
- Practical tips
- When localisation is worth it

---

## Why It Matters

- Most software users worldwide aren't native English speakers
- Even if they read English, technical English is hard
- Plain English is an act of inclusion
- Cheaper than localisation; helps everyone, not just translators
- Even US-only docs benefit

---

## Practices

![global_writing](svg/courses/development_methodologies/technical-writing/13_writing_for_international_audiences/intl_writing.svg)

---

## Plain Language Basics

- Short sentences (under 25 words)
- Common words (use "use", not "utilise")
- Active voice
- One idea per sentence
- Lists for sequential steps
- Same advice that helps native speakers, more so for non-native

---

## What Translates Poorly

- **Idioms**: "hit the ground running" makes no sense
- **Jargon**: domain-specific shortcuts
- **Cultural references**: sports, holidays, politics
- **Wordplay and humour**: rarely survives
- **Sarcasm**: never works in writing, ever

---

## What Translates Well

- Concrete nouns: "the database", "the user"
- Specific verbs: "click", "type", "save"
- Numbers and units (with explicit currency / measurement units)
- Step-by-step instructions
- Diagrams and screenshots

---

## Numbers and Units

- "1,000": Anglo-American thousands separator; many countries use "1.000"
- "1,000.50": European decimal in some places
- ISO 8601 dates: 2026-05-01 — unambiguous
- Currency: "USD 100", not "$100"
- Time zones: "14:00 UTC" not "2pm"

---

## Date Formats

- US: 5/1/2026 (May 1)
- UK / EU: 1/5/2026 (also May 1, but different)
- Asia: often 2026/5/1
- Confusing across borders
- Always: ISO 8601 (YYYY-MM-DD)

---

## Localisation vs Internationalisation

- **i18n**: making the software ready for multiple locales
- **L10n**: actually translating into specific locales
- Doc i18n: separating translatable text from layout
- Doc L10n: getting it translated by a native speaker
- Both are projects of their own

---

## Cost of Localisation

- Translation: $0.10-$0.30 per word per language, professionally
- Maintenance: every doc change requires re-translation
- Review: native speaker per locale to verify
- Hidden costs: cultural adaptation, terminology consistency
- Pick the locales that justify the cost

---

## Tools for Localisation

- Crowdin, Lokalise, Phrase, Transifex: web-based translation platforms
- Translation memory: re-use of previously-translated phrases
- Glossaries enforce consistent translation of key terms
- Integration with git/CI workflows
- Free tiers for open source

---

## Cultural Sensitivity

- Examples shouldn't centre one culture
- Names: include diverse examples
- Examples that might be offensive in some cultures
- Religious / political references: avoid
- Test with diverse reviewers if possible

---

## Avoiding Casual Language

- "Hey there!" — feels presumptuous in some cultures
- "Awesome!" — overused American
- Apologies that sound performative
- Stick with neutral, factual tone for international docs
- Save personality for the marketing site, not the docs

---

## Inclusive Language

- "Master/slave" → "primary/replica"
- "Whitelist/blacklist" → "allowlist/blocklist"
- "Guys" → "everyone" or "team"
- "He/she" → "they"
- "Crazy" / "insane" → use less ableist words
- Tools (alex, woke) catch these

---

## When Localisation Is Worth It

- Large user base in non-English-speaking regions
- Compliance requirements (GDPR has localisation expectations)
- High-stakes documentation (medical, financial, legal)
- Customer-paying for the service
- High-conversion content (landing pages, onboarding)

---

## When Plain English Is Enough

- Internal docs
- Engineering reference docs
- Open source projects with English-speaking maintainers
- Early-stage products with one market
- Most of the time, this is the right answer

---

## A Practical Approach

- Default: write in plain English
- Avoid idioms and jargon
- Use ISO date format
- Specify units clearly
- Localise only when justified by user data
- Keep docs short — less to translate

---

## Common Mistakes

- Jargon-heavy docs assuming everyone reads English
- Idioms that don't translate
- Ambiguous dates
- US-centric examples
- Translating without a native reviewer
- Localising once, then forgetting to maintain
