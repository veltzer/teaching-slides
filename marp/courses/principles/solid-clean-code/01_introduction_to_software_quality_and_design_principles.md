---
tags:
  - concepts:clean-code
  - concepts:quality
level: intermediate
category: design-patterns
audience:
  - audiences:developers
  - audiences:architects

---

# Introduction to Software Quality and Design Principles

---

## What This Chapter Covers

- What "clean" code actually means
- Technical debt: where it comes from, what it costs
- Code smells and how to spot them
- Design principles vs design patterns
- Why the SOLID principles matter
- A short tour of the day ahead

---

## SOLID Overview

![solid_overview](svg/courses/principles/solid-clean-code/01_introduction_to_software_quality_and_design_principles/solid_overview.svg)

---

## What "Clean" Means

- Code that reads like prose
- Each function does one thing, named for what it does
- No surprises hiding in the implementation
- A new developer can navigate without a map
- "Clean" is what you wish *yesterday's* developer had written

---

## Quality Attributes

![quality_attributes](svg/courses/principles/solid-clean-code/01_introduction_to_software_quality_and_design_principles/quality_attributes.svg)

---

## Three Audiences for Code

- **The compiler / interpreter**: needs syntactic correctness
- **Other developers**: need to understand and change it
- **Future you**: also needs to understand and change it
- The compiler is the easy one
- The other two are why we care about clean code

---

## Technical Debt

- A metaphor: shortcuts now, payments later
- Some debt is *strategic*: ship fast, refactor after launch
- Most debt is *unintentional*: rushed change, no tests, "I'll fix it later"
- Like financial debt, the interest compounds
- Unlike financial debt, you can't see the balance — until you can't move

---

## What Tech Debt Looks Like

- Adding a feature now takes 3x as long as it did a year ago
- Tests fail "intermittently" but no one investigates
- Whole modules nobody is willing to touch
- The same bug fixed three times because it kept reappearing
- Shipping requires heroics from the same two people

---

## Code Smells

- Surface-level signs of deeper design problems
- Catalogued by Martin Fowler in *Refactoring*
- Not bugs — code that works but should change
- Examples: long method, large class, duplicated code, feature envy
- A smell is an *invitation* to investigate, not a verdict

---

## Common Code Smells

- **Long Method**: hard to read, hard to test
- **Large Class**: too many responsibilities
- **Duplicated Code**: change one place, miss the others
- **Long Parameter List**: probably wants its own object
- **Feature Envy**: a method that wants to be on the other class
- **Primitive Obsession**: int/string everywhere; needs a value type

---

## Design Principles vs Design Patterns

- **Principles**: general guidance ("favour composition over inheritance")
- **Patterns**: named, reusable solutions (Strategy, Observer, Factory)
- Principles are timeless; patterns come and go with fashion
- Apply principles always; patterns when the shape fits
- This course is about the principles

---

## The Cost of Not Caring

- 70% of a system's lifetime cost is *maintenance*
- Code is read 10x more often than it is written
- A weekly hour wasted by 5 developers wading through bad code = 250 hours / year
- Bad code drives senior people to leave
- Replacing those people is the most expensive part of all

---

## A Short History of SOLID

- Robert C. Martin compiled them from existing principles in the 1990s
- Acronym coined later (~2004) by Michael Feathers
- Each letter is named after an existing OO pioneer
- They've held up well — common in interviews, tutorials, and real code
- They aren't perfect; they aren't the only thing — they are *useful*

---

## SOLID at a Glance

- **S**ingle Responsibility Principle (SRP)
- **O**pen/Closed Principle (OCP)
- **L**iskov Substitution Principle (LSP)
- **I**nterface Segregation Principle (ISP)
- **D**ependency Inversion Principle (DIP)
- One letter per principle, one chapter per letter

---

## Languages We'll Use

- Most examples in Python — concise, readable on slides
- Some in Java — for the static-typing examples
- A few in C# — for the .NET-flavoured patterns
- Principles are language-agnostic; the *examples* aren't
- Translate to your stack as you read

---

## How to Use This Material

- Read the principle
- Look at the worked example
- Find a similar smell in your own codebase
- Refactor it (with tests)
- Notice whether the result feels easier to change

---

## What's Coming

- One chapter per SOLID principle, with refactoring examples
- Then clean-code fundamentals: naming, functions, comments
- Then advanced techniques: error handling, complexity, legacy code
- The day ends with a unified view: how these principles play together
- Bring a problem from your own codebase to apply this to
