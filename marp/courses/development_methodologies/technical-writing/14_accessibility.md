---
tags:
  - practices:technical-writing
  - practices:accessibility
level: beginner
category: methodology
audience:
  - audiences:developers

---
# Accessibility

---
## What This Chapter Covers

- Why accessibility matters in docs
- Accessible document structure
- Alt text for images and diagrams
- Screen reader considerations
- Color and contrast
- Practical tips and tooling

---
## Why It Matters

- Some users can't see, hear, or use a mouse
- Documentation should reach all users
- Accessible docs are better for everyone (clearer structure, better contrast)
- Legal requirements in many jurisdictions (ADA, WCAG, EAA)
- A small effort that helps a lot of people

---
## WCAG Standards

- Web Content Accessibility Guidelines
- Three levels: A, AA, AAA
- AA is the common target (most laws require it)
- Four principles: Perceivable, Operable, Understandable, Robust
- Apply to documentation websites as much as web apps

---
## Accessible Structure

- Use semantic markup (real headings, not bold text)
- Hierarchy follows H1 → H2 → H3 (no skipping)
- Lists for lists, paragraphs for paragraphs
- Tables for tabular data, not for layout
- Markdown does most of this automatically

---
## Alt Text for Images

- Every meaningful image needs alt text
- Describes what the image shows
- For decorative images: empty alt (`alt=""`) tells screen readers to skip
- Don't say "image of..." — screen readers do that
- For complex diagrams: longer description in surrounding text

---
## Alt Text Examples

- Bad: "Image"
- Bad: "screenshot.png"
- Good: "Database admin panel showing three connected services"
- For complex: "See description below" + actual description in prose
- Be specific; describe the meaning, not the visual

---
## Diagrams and Screenshots

- Add a text description nearby
- Don't rely on the diagram alone
- Mermaid diagrams have built-in text
- For exported images: write a paragraph that conveys the same information
- Both seeing and non-seeing users benefit

---
## Screen Readers

- Software that reads the screen aloud
- JAWS, NVDA, VoiceOver, TalkBack
- Read in document order
- Headings, lists, links all announced
- Test your docs by closing your eyes and listening

---
## Color and Contrast

- WCAG AA: 4.5:1 contrast for normal text, 3:1 for large
- Tools: WebAIM contrast checker, browser dev tools
- Light grey on white: a perennial accessibility failure
- Don't rely on color alone for meaning
- "Items in red are required" — also use a label

---
## Color-Blind Considerations

- ~8% of men, ~0.5% of women have some color vision deficiency
- Common: red-green confusion
- Don't use red/green as the only distinguishing feature
- Use shapes, patterns, or text labels alongside color
- Test with simulators (Sim Daltonism, Color Oracle)

---
## Link Text

- Bad: "click here", "read more"
- Good: "read the API reference", "view the changelog"
- Screen reader users navigate by link list
- "Click here" out of context is meaningless
- Descriptive link text helps everyone

---
## Keyboard Navigation

- Some users can't use a mouse
- Doc sites should be fully keyboard-navigable
- Tab moves focus; Enter activates
- Visible focus indicators
- Test by unplugging your mouse

---
## Code Blocks Are Often Inaccessible

- Long lines that horizontally scroll
- Color-only syntax highlighting (low contrast on some themes)
- Copy buttons not keyboard-accessible
- Solution: choose accessible doc themes
- Material for MkDocs and Docusaurus do well by default

---
## Alt Text for Code Screenshots

- Code as image: nightmare for accessibility
- Always prefer code blocks over screenshots of code
- Code blocks are screen-readable, copyable, searchable
- Screenshots are a last resort
- If you must: include the code in the alt text or surrounding prose

---
## Accessibility Tooling

- **axe** (browser extension): scans for issues
- **Lighthouse** (built into Chrome): accessibility audit
- **WebAIM WAVE**: visual feedback on a page
- Vale rules can flag inaccessible patterns
- Run regularly, fix incrementally

---
## Manual Testing

- Tab through your doc site
- Try a screen reader for one page
- Use Sim Daltonism to view in color-deficient mode
- Use browser zoom at 200% to test for layout breakage
- Once a quarter; not every PR

---
## Common Accessibility Mistakes

- Missing alt text
- Color as the only indicator
- Bad heading hierarchy
- "Click here" links
- Low contrast text on backgrounds
- Code as screenshots
- Long inaccessible PDFs as primary docs

---
## Course Wrap-Up

- Technical writing is craft you can learn
- Audience first; everything else follows
- Use the right document type for the job
- Style and structure matter as much as content
- Maintain docs continuously; they decay otherwise
- Accessibility and internationalisation widen your reach
- Better docs = better software, every time
