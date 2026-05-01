---
tags:
  - concepts:clean-code
  - concepts:naming
level: intermediate
category: design-patterns
audience:
  - audiences:developers

---
# Clean Code Fundamentals

---
## What This Chapter Covers

- Naming: variables, functions, classes
- Function design: small, focused, single-purpose
- Parameter management
- Comment best practices
- Avoiding magic numbers and strings
- Code organisation

---
## Naming Matters Most

- The single biggest readability lever
- A good name eliminates the need for most comments
- A name lasts longer than the code in it
- Renaming is the cheapest refactor — modern IDEs do it instantly
- Pay the cost of a thoughtful name now; save the cost of a bad one many times over

---
## Naming Variables

- Reveal *intent*, not *type*: `total_seconds` over `t`
- Avoid abbreviations: `customer` over `cust`
- Loop counters: `i`, `j`, `k` are fine for tiny loops
- Boolean names start with `is_`, `has_`, `can_`
- Constants: `UPPER_SNAKE_CASE`

---
## Naming Functions

- Verb phrases: `calculate_total`, `send_email`, `is_eligible`
- One verb each — `calculate_and_send` is two functions
- Honest about side effects: `save_to_disk` over `process`
- Avoid weasel words: `handle`, `manage`, `process` say nothing
- A good function name lets a reader skip the body

---
## Naming Classes

- Noun phrases: `OrderService`, `Customer`, `EmailSender`
- Avoid generic suffixes when you can: `Customer` over `CustomerObject`
- Avoid `*Manager`, `*Handler`, `*Processor` — they say nothing about what the class actually does
- Names with "And" or "Or" suggest a SRP violation
- Class names are read everywhere; spend the time

---
## Function Length

- The classic guideline: a function should fit on one screen
- The strict version (Robert Martin): 5-10 lines
- The relaxed version: as small as it can reasonably be
- Long functions hide complexity; small functions surface it
- Pay attention to your eye scanning back to find context

---
## Function Responsibility

- One thing, well-named for what it does
- A function that loads, transforms, and writes is three functions in disguise
- Extract until each function does *exactly* what its name says
- This is SRP at the function level
- Tests get smaller and clearer with each extraction

---
## Function Parameters

- Fewer is better: 0-3 parameters is the sweet spot
- 4+ parameters &#8594; consider grouping into an object
- Boolean parameters are usually a smell: `send_email(true, false)` reads like noise
- Better: two functions, or named arguments
- Default values are fine; use them to add optionality

---
## Avoiding Long Parameter Lists

```python
# painful
def book_room(customer_id, room_type, start_date, end_date,
              breakfast, parking, smoking, currency):
    ...

# better
def book_room(reservation: ReservationRequest):
    ...
```

- Group related parameters into a class
- The class name documents what they mean together
- Adding a new field doesn't break every caller

---
## Comments: When to Write Them

- *Why* the code does something non-obvious — yes
- A surprising workaround for a bug — yes
- A reference to an external spec — yes
- Restating *what* the code does — almost never
- Documentation is a separate concern from code comments

---
## Comments: When Not To

- Don't restate the code: `// increment i` next to `i++`
- Don't comment out code — delete it; git has the history
- Don't write a comment to apologise for unclear code — fix the code
- Don't write a header comment that goes stale immediately
- Self-documenting code beats most comments

---
## Magic Numbers and Strings

```python
# painful
if order.total > 1000:
    apply_discount(order, 0.1)

# better
HIGH_VALUE_THRESHOLD = 1000
HIGH_VALUE_DISCOUNT = 0.1

if order.total > HIGH_VALUE_THRESHOLD:
    apply_discount(order, HIGH_VALUE_DISCOUNT)
```

- Constants name the *meaning*, not the value
- Easier to change in one place
- A reader sees *why* 1000 matters

---
## Code Formatting

- Consistent indentation, line length, spacing
- Use a formatter (Black, Prettier, gofmt) — settle the bikeshed
- Group related code; blank lines between groups
- Order matters: public methods before private; called methods after callers
- Format on save; fight no one over it

---
## File Structure

- One main concept per file
- File name matches the main class
- Imports at the top, grouped: standard library, third-party, local
- Helpers below the public surface
- Tests in a parallel directory mirror, not in the same file

---
## Naming Conventions Per Language

- Python: `snake_case` for functions and variables, `PascalCase` for classes
- Java: `camelCase` for methods, `PascalCase` for classes
- Go: `camelCase` for unexported, `PascalCase` for exported
- Pick the language idiom; consistency within a project beats personal preference
- Linters enforce most of this for free

---
## Reading Code

- Code is read 10x more than written
- Optimise for the reader, not the writer
- "Clever" tricks have a cost every time someone reads them
- Boring code that's obviously correct is a feature
- Skim a function — if you can't tell what it does in 10 seconds, rename or split

---
## Common Mistakes

- One-letter variable names outside tiny loops
- Functions that do "and"
- Class names with no information (`Manager`, `Handler`, `Util`)
- Long parameter lists with boolean flags
- Block comments restating the code below them
- Magic numbers in conditional branches
