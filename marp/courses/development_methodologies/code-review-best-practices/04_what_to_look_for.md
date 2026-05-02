---
tags:
  - practices:code-review
level: beginner
category: methodology
audience:
  - audiences:developers

---
# What to Look For

---
## What This Chapter Covers

- Bugs and logic errors
- Design and architecture concerns
- Code style and consistency
- Test coverage and quality
- Security considerations
- Performance implications
- A mental checklist

---
## Review Priorities

![review_priorities](svg/courses/development_methodologies/code-review-best-practices/04_what_to_look_for/review_priorities.svg)

---
## A Mental Checklist

- Does it work? (correctness)
- Is it well-structured? (design)
- Will I understand it in 6 months? (readability)
- Is it tested? (quality)
- Does it open security holes? (security)
- Will it scale? (performance)
- Run through these every time

---
## A Reviewer's Lens

![review_checklist](svg/courses/development_methodologies/code-review-best-practices/04_what_to_look_for/review_checklist.svg)

---
## Bugs and Logic Errors

- Off-by-one errors
- Null / undefined handling
- Wrong boundary conditions
- Inverted conditions
- Concurrency issues (race conditions, deadlocks)
- Compare against the description: does the code match?

---
## How To Spot Bugs

- Run the code mentally with sample inputs
- Especially edge cases: 0, negative, max, empty, null
- Compare with similar code elsewhere
- Look for "off-by-one" in loops and array indices
- Trust your "this looks weird" instinct

---
## Design Concerns

- Is this in the right module?
- Are the abstractions right for the problem?
- Could it be simpler?
- Does it duplicate something elsewhere?
- Will this scale to other use cases?
- Design issues are expensive to fix later

---
## When To Push Back on Design

- The change is in the wrong direction
- A simpler approach exists
- The abstraction creates more complexity than it solves
- Be specific: "consider X because Y"
- Block when the design is wrong; suggest when it's just different

---
## Code Style

- Naming, formatting, indentation
- *Most* of this should be automated
- Linters and formatters run in CI
- Reviews catch what tools miss
- Comment "nit:" for style nitpicks (so authors know they're not blockers)

---
## Test Coverage

- Are there tests at all?
- Do they cover the changed behaviour?
- Do they test failure modes, not just happy paths?
- Are they fast and reliable?
- "Tests added" without checking what they test is rubber-stamping

---
## Test Quality

- A test that always passes is worse than no test
- Tests should fail when the code is wrong
- Mutation testing reveals weak tests (kill the mutant)
- Brittle tests slow everyone down
- Quality > quantity for tests

---
## Security

- Untrusted input handling
- SQL injection, XSS, command injection
- Auth and authorisation
- Secrets in code or configs
- Third-party deps with known CVEs
- For sensitive areas: get a security review

---
## Common Security Smells

- String concatenation into queries (SQL injection)
- HTML built with template strings (XSS)
- Hashing passwords with MD5 / SHA1 (broken)
- Hard-coded credentials
- `eval()` on user input
- Disabled cert validation

---
## Performance

- Loops over large datasets
- N+1 queries against the database
- Synchronous network calls in hot paths
- Large objects in memory
- Don't optimise prematurely; do flag clear issues

---
## Performance Smells

- Database query inside a loop
- Repeated identical computation that could be cached
- Reading entire files into memory when streaming would work
- O(n^2) algorithms on potentially large inputs
- Synchronous I/O in async contexts

---
## Comments and Documentation

- Are comments explaining *why*, not *what*?
- Are doc strings updated for changed APIs?
- Are TODOs traceable (issue links)?
- Does the change update relevant docs?
- Doc rot is real; comment changes catch it

---
## What NOT To Look For

- Personal style preferences (tabs vs spaces — let the formatter decide)
- Things you'd have written differently for no clear reason
- Defects that have nothing to do with this PR
- Issues outside the PR's scope
- Save those for the right channel; don't pile onto a PR

---
## Common Mistakes

- Reviewing only style, missing logic bugs
- Asking for changes that are out of scope
- Treating "different from how I'd do it" as "wrong"
- Approving without reading the substantive changes
- Spending an hour on a one-line fix
