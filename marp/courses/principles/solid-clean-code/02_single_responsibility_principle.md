---
tags:
  - concepts:solid
  - concepts:srp
level: intermediate
category: design-patterns
audience:
  - audiences:developers

---
# Single Responsibility Principle (SRP)

---
## With vs Without SRP

![srp](svg/courses/principles/solid-clean-code/02_single_responsibility_principle/srp.svg)

---
## One Reason to Change

![srp_one_reason](svg/courses/principles/solid-clean-code/02_single_responsibility_principle/srp_one_reason.svg)

---
## What This Chapter Covers

- A precise statement of SRP
- A worked refactoring
- Cohesion and coupling
- How to spot SRP violations
- Trade-offs and limits

---
## The Principle, Stated Carefully

- "A class should have *one reason to change*" — Robert C. Martin
- *Reason to change* = a single source of requirements
- Same class touched for billing, reporting, and email = three reasons
- Same class touched only for billing variations = one reason
- SRP isn't "one thing", it's "one *axis* of variation"

---
## A Smelly Class

```python
class Report:
    def gather_data(self): ...      # talks to DB
    def format_html(self): ...      # rendering
    def format_pdf(self): ...       # rendering
    def email_to(self, addr): ...   # SMTP
    def save_to_disk(self, p): ...  # filesystem
```

- Five responsibilities in one class
- DB schema change &#8594; touch this class
- Marketing wants new HTML &#8594; touch this class
- New SMTP provider &#8594; touch this class
- Three teams stepping on each other

---
## After Refactoring

```python
class ReportRepository:
    def fetch(self): ...

class ReportFormatter:
    def to_html(self, report): ...
    def to_pdf(self, report): ...

class ReportSender:
    def email(self, doc, addr): ...
    def save_to_disk(self, doc, path): ...
```

- Each class has one reason to change
- The three teams now own three classes
- Consumers compose them as needed

---
## Cohesion and Coupling

- **Cohesion**: how related are the things inside one class?
- **Coupling**: how much does one class know about another?
- SRP raises cohesion (one purpose per class)
- Done well, also lowers coupling (each class knows less)
- Done poorly, can *raise* coupling — lots of tiny classes that all need each other

---
## Spotting Violations

- The class name needs an "and" or "or" to describe it
- Different methods are tested with different setups
- Different methods import different libraries
- Git history shows the class touched by separate teams for separate reasons
- The class file is over ~500 lines

---
## SRP at the Function Level

- The same idea applies smaller
- A function that fetches, transforms, and writes is doing too much
- Refactor: `fetch()`, `transform()`, `write()` — three small functions
- Compose at the call site
- Each function gets a precise name and a focused test

---
## SRP and Microservices

- The principle scales: a microservice should have one reason to deploy
- "Inventory service" — yes
- "Inventory + invoicing + reporting service" — three reasons to redeploy
- Same logic, different scope
- Don't apply mechanically; coordination cost matters too

---
## When NOT to Split

- The "responsibilities" always change *together*
- The split would create classes that are useless on their own
- The team is small and the splits add navigation overhead without clear benefit
- The result would be procedural code in OO clothing

---
## Limits and Trade-offs

- Splitting too aggressively gives you a swarm of tiny classes
- Each new class is a new file, a new test, more navigation
- "Class explosion" is its own smell
- Aim for the *level of granularity that matches your team's needs*
- A 5-person startup and a 200-person platform team have different sweet spots

---
## A Useful Test

- Imagine three separate teams owning the codebase
- Could each team's changes happen in *different* classes?
- If yes, your responsibilities are well-split
- If no, find the shared class and see if it can be split
- This thought experiment beats abstract debate

---
## SRP and Other Principles

- SRP enables OCP — you can extend a focused class without breaking it
- SRP enables ISP — focused classes have focused interfaces
- SRP enables testing — fewer reasons to mock
- A class that violates SRP usually violates several others too
- Fix the SRP problem first; the rest often follow

---
## A Refactoring Recipe

- Identify the cluster of methods that always change together &#8594; one new class
- Identify another cluster &#8594; another new class
- Move the methods, with their state, into the new classes
- Wire up the original class to delegate, or replace it entirely
- Run the tests; commit when green

---
## Common Mistakes

- Splitting along *technical* lines (DTO, Service, Repository) when the responsibility is one *business* concept
- Creating a class per method (over-application)
- Ending up with a "GodFacade" that wires up the small classes — recreates the original
- Splitting by what *can* change rather than what *does* change
- Forgetting that "what changes together stays together" is also valid
