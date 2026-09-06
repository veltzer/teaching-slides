---
tags:
  - practices:technical-writing
  - practices:style
level: beginner
category: methodology
audience:
  - audiences:developers

---

# Writing Style

---

## Writing Style Principles

![style_principles](svg/courses/development_methodologies/technical-writing/04_writing_style/style_principles.svg)

---

## What This Chapter Covers

- Clarity and conciseness
- Active vs passive voice
- Consistent terminology
- Sentence and paragraph structure
- Avoiding jargon and ambiguity
- A few rules that fix most prose

---

## Active Voice

![passive_to_active](svg/courses/development_methodologies/technical-writing/04_writing_style/passive_to_active.svg)

---

## Style Pillars

![style_pillars](svg/courses/development_methodologies/technical-writing/04_writing_style/style_pillars.svg)

---

## Clarity Above All

- The reader's first reading is the right reading
- Anything that requires re-reading is a failure
- Clarity beats elegance
- Clarity beats cleverness
- Clarity beats brevity, sometimes

---

## Conciseness, Without Cutting Meaning

- Every word should earn its place
- "Due to the fact that" &#8594; "because"
- "In order to" &#8594; "to"
- "At this point in time" &#8594; "now"
- Cut 30% on revision; the prose gets stronger

---

## Active Voice

- "The system writes the log" — active
- "The log is written by the system" — passive
- Active voice is shorter and clearer
- Use passive only when the actor is unknown or irrelevant
- "Records are kept for 7 years" is fine

---

## Why Passive Drains Energy

- "It is recommended that" &#8594; "we recommend"
- "Errors should be handled" &#8594; "handle errors"
- "It can be noted that" &#8594; just say it
- Passive piles up corporate-speak
- Active prose gets read

---

## Consistent Terminology

- Pick one term per concept; use it everywhere
- Don't switch between "user", "customer", "client" unless they mean different things
- Build a glossary for non-obvious terms
- Inconsistency creates confusion that adds up
- Tools: Vale (style linter) can enforce

---

## Sentence Length

- Mix short and medium
- Avoid long sentences with multiple clauses
- A sentence should fit one idea
- 15-25 words is a comfortable maximum
- Read aloud; if you run out of breath, split

---

## Paragraph Structure

- One paragraph, one idea
- Open with the topic; explain or expand; close
- 3-5 sentences typical for technical prose
- A paragraph longer than half a screen is too long
- Lists are paragraphs in disguise; use them

---

## Avoiding Jargon

- Jargon: terminology specific to a field, opaque to outsiders
- Define on first use, then use freely
- For a beginner audience: minimise
- For an expert audience: jargon saves words
- Inappropriate jargon excludes; appropriate jargon includes

---

## Avoiding Ambiguity

- "It" is dangerous — what does "it" refer to?
- "This" is dangerous — what does "this" refer to?
- Be specific: "the response", "the connection", "the error"
- Read your draft and ask: "what could be misread?"
- Edit for ambiguity ruthlessly

---

## Concrete Over Abstract

- "Set the timeout to 30 seconds" beats "Configure the timeout appropriately"
- "Returns 404" beats "Returns an error response"
- Numbers beat adjectives when accuracy matters
- Examples beat descriptions
- Concrete language is also easier to translate

---

## Tone

- Confident but not arrogant
- Direct but not curt
- Friendly but not chatty
- Professional but not stiff
- Read your draft as if a stranger wrote it; would you trust the writer?

---

## "We" vs "You" vs Imperative

- "We recommend X" — formal
- "You should X" — direct
- "Do X" — imperative; tightest
- For tutorials: imperative for steps, "you" for explanation
- For reference: third person ("the function returns...")

---

## Easy Edits That Improve Most Prose

- Cut adjectives and adverbs
- Cut "very", "really", "actually"
- Replace "things", "stuff" with the actual nouns
- Replace passive with active
- Break long sentences

---

## Examples

- Bad: "It is generally considered to be a good practice to have unit tests written before the implementation code is finalized."
- Good: "Write tests before the code."
- Bad: "The user should ensure that proper authentication has been performed prior to attempting access."
- Good: "Authenticate before accessing."
- Each cuts ~70%; meaning preserved

---

## Style Guides

- Google's developer documentation style guide is excellent
- Microsoft Manual of Style
- Apple Style Guide (consumer-friendly)
- Pick one; refer when unsure
- A style guide is a tie-breaker, not a straightjacket

---

## Common Style Mistakes

- "Should" everywhere — when do you mean "must"?
- Passive throughout — sounds bureaucratic
- Inconsistent terms — confuses readers
- Long sentences — readers lose the thread
- Dropping the topic mid-paragraph — leaves them lost
