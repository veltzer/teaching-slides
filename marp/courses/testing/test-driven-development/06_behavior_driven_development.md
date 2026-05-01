---
tags:
  - practices:tdd
  - practices:bdd
level: intermediate
category: testing
audience:
  - audiences:developers
  - audiences:testers

---
# Behavior-Driven Development

---
## What This Chapter Covers

- BDD principles
- Gherkin syntax: Given-When-Then
- Feature files and scenarios
- BDD frameworks: Cucumber, Behave, SpecFlow
- Mapping steps to code
- Living documentation

---
## What BDD Is

- A discipline of describing behaviour in business-readable language
- Builds on TDD
- Adds a layer: stakeholders write or read the specs
- Often coincides with acceptance testing
- Coined by Dan North in the 2000s

---
## Why BDD

- Bridges the gap between business and developers
- Specs become tests automatically
- Living documentation that doesn't lie (because tests fail when behaviour drifts)
- Promotes conversation about what the system *should* do
- A different kind of feedback loop

---
## Gherkin Syntax

```misc
Feature: User signup

  Scenario: Successful signup with valid email
    Given I am on the signup page
    When I enter "alice@example.com" and a strong password
    And I click "Create account"
    Then I am redirected to the dashboard
    And I receive a welcome email
```

---
## Given-When-Then

- **Given**: the initial context (preconditions)
- **When**: the action being tested
- **Then**: the expected outcome
- **And** / **But**: continuations of any clause
- One Scenario, one behaviour

---
## Feature Files

- Each `Feature` is a coherent capability
- Multiple `Scenario`s per feature
- Lives in a `.feature` file
- Plain text; readable by non-developers
- Versioned alongside the code

---
## A Full Feature File

```misc
Feature: Shopping cart

  Background:
    Given I am logged in as "alice@example.com"

  Scenario: Add item to empty cart
    Given my cart is empty
    When I add "Item A" to my cart
    Then my cart contains 1 item

  Scenario: Add item to non-empty cart
    Given my cart has 1 item
    When I add "Item B" to my cart
    Then my cart contains 2 items
```

---
## Cucumber

- The original BDD framework (Ruby; ports for many languages)
- Cucumber-JVM (Java), Cucumber-JS (JavaScript), etc.
- Reads feature files; runs step definitions
- Output: green/red per scenario
- Most-known BDD tool

---
## Behave (Python)

- Cucumber-style for Python
- Same Gherkin syntax
- Step definitions in Python decorated with `@given`, `@when`, `@then`
- Less complex than Cucumber's JVM ecosystem
- Common in Django/Flask BDD projects

---
## SpecFlow (.NET)

- Cucumber-style for C#
- Visual Studio integration
- Generates step definition stubs
- Common in .NET enterprise contexts
- Maintained, mature

---
## Mapping Steps To Code

```python
from behave import given, when, then

@given('I am on the signup page')
def step_on_signup(context):
    context.page = SignupPage(context.browser)

@when('I enter "{email}" and a strong password')
def step_enter_creds(context, email):
    context.page.enter_email(email)
    context.page.enter_password(generate_strong())

@then('I am redirected to the dashboard')
def step_dashboard(context):
    assert context.browser.current_url.endswith('/dashboard')
```

---
## Step Definition Reuse

- Same step text used across many scenarios &#8594; one definition
- Parameters via `{name}` syntax
- Tables for tabular data
- DRY for tests
- Saves enormous duplication

---
## Backgrounds

- A `Background` section runs before each scenario in the feature
- Sets up shared preconditions
- Saves repeating "Given I am logged in" in every scenario
- Use sparingly; too much background hides what's special

---
## Scenario Outlines

```misc
Scenario Outline: Login validation
  When I enter <email> and <password>
  Then I see <result>

  Examples:
    | email           | password  | result          |
    | a@b.com         | strong    | dashboard       |
    | a@b.com         | weak      | password error  |
    | invalid         | strong    | email error     |
```

- Same scenario, multiple data sets
- Expands to N scenarios at runtime
- Reduces duplication; preserves precision

---
## BDD Workflow

- Stakeholders + developers write feature files together
- Developers implement step definitions
- Run scenarios; iterate until green
- Feature files stay current as living documentation
- New behaviour: new scenario first

---
## BDD vs Plain TDD

- TDD: developer-only; unit-level
- BDD: stakeholder-readable; behaviour-level
- BDD scenarios are integration / acceptance tests
- TDD is for the design; BDD is for the spec
- Use both: TDD for units, BDD for end-to-end behaviours

---
## Living Documentation

- Feature files describe what the system does
- They *can't* lie because they're executable tests
- Stakeholders read them; not all run them
- Replaces stale wiki pages
- The most underrated benefit of BDD

---
## When BDD Fails

- Stakeholders not involved (just developers writing English-flavoured tests)
- Step definitions become unmaintained
- Slow scenarios that nobody runs
- Mock-heavy step implementations (defeats the integration purpose)
- "Cucumber theatre" — looks like BDD; isn't

---
## Common BDD Mistakes

- Treating Gherkin as just another test syntax
- Engineers writing scenarios alone (no stakeholder input)
- Scenarios that test implementation, not behaviour
- Step explosion (every test gets its own steps)
- Slow, fragile end-to-end tests as the only tests
