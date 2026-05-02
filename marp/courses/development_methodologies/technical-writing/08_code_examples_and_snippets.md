---
tags:
  - practices:technical-writing
  - practices:code-examples
level: beginner
category: methodology
audience:
  - audiences:developers

---
# Code Examples and Snippets

---
## What This Chapter Covers

- Writing effective code examples
- Keeping examples up to date
- Syntax highlighting and formatting
- Runnable examples and sandboxes
- Example anti-patterns
- The pyramid of example coverage

---
## Why Examples Matter

- Most developers learn by example, not theory
- A working code example is the fastest path to "I get it"
- Documentation without examples loses readers
- Examples reveal the *intended* usage
- A 3-line example often beats a 30-line description

---
## Quality Checklist

![example_quality](svg/courses/development_methodologies/technical-writing/08_code_examples_and_snippets/example_quality.svg)

---
## What Makes A Good Example

- **Self-contained**: works on its own
- **Minimal**: only what's needed for the point
- **Realistic**: looks like real code, not toy code
- **Correct**: actually runs
- **Idiomatic**: shows the recommended way

---
## Self-Contained Examples

```python
# Good: stand alone
import requests
r = requests.get("https://api.example.com/users")
r.raise_for_status()
print(r.json())

# Bad: depends on context not shown
print(api.get_users(token))
```

- Reader can copy and run
- All imports visible
- All variables defined

---
## Minimal Examples

- Don't include unrelated logic
- "Hello world" should be 5 lines, not 50
- Strip error handling for first examples (mention it later)
- Add complexity progressively
- Each example demonstrates *one* thing

---
## Realistic Examples

- "foo" / "bar" / "baz" are forgettable
- "user_id" / "order_total" / "email" stick
- Names that match real domains
- Avoid contrived setups
- Use realistic data (anonymised)

---
## Correctness

- Test your examples
- Doctests (Python), example-based testing (Rust), embed-and-test patterns
- Outdated examples are a special kind of broken
- Better: no example than a wrong example
- Automation catches what humans forget

---
## Doctests in Python

```python
def add(a, b):
    """
    Add two numbers.

    >>> add(2, 3)
    5
    >>> add(-1, 1)
    0
    """
    return a + b
```

- The example *is* the test
- `python -m doctest` runs them
- Drift impossible — broken docs fail CI

---
## Example Coverage Pyramid

- One quickstart example at the top of the doc
- Per-feature examples in the middle
- Comprehensive cookbook at the bottom
- Don't try to show everything in one example
- Layer; let readers descend as needed

---
## Syntax Highlighting

```markdown
```python
def hello():
    print("hi")
```misc
```

- Always specify the language
- Lets the renderer color-code
- Easier to read at a glance
- Wrong language tag &#8594; no highlighting

---
## Code Formatting

- Format examples with the same tool as your real code
- `black`, `prettier`, `gofmt`
- Manual formatting drifts
- Inconsistent style in examples is jarring
- Run examples through the formatter before committing

---
## Output Examples

- Show what running the code produces
- Format output blocks differently from code
- Truncate long output with `...`
- Realistic output ("OK" not enough; show *what* OK looks like)

---
## Long Examples

- For tutorials, sometimes a 50-line example is right
- Break it into chunks with explanations between
- Each chunk should be runnable on its own (or up to that point)
- Include the full file at the end
- Don't dump 500 lines without commentary

---
## Runnable Examples

- Sandboxes: CodePen, JSFiddle, Replit, Go Playground
- Lets readers experiment without setup
- Best for client-side languages and simple servers
- Worth the maintenance for popular features
- Consider security implications (anyone can run anything)

---
## Avoid In Examples

- Stale syntax (Python 2, old API versions)
- Deprecated patterns
- Anti-patterns "for clarity" (hint: clear examples *are* the clarity)
- Fictional libraries
- Code that doesn't compile

---
## Show Errors Too

- Document what happens when things go wrong
- Common errors and how to fix
- "If you see X, do Y"
- A reader hitting an error feels supported when the doc anticipated it
- Especially useful in API docs

---
## Common Example Mistakes

- Not running them; finding out later they're broken
- Copy-pasting from production code without simplifying
- Examples that depend on hidden setup
- Inconsistent style across examples
- Stale examples that haven't been touched in 2 years
