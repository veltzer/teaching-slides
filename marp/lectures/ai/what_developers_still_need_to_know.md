---
audience:
  - audiences:developers
  - audiences:senior-developers
  - audiences:architects
  - audiences:team-leads
category: ai
level: intermediate
tags:
  - data-and-ai:ai
  - concepts:programming
  - concepts:best-practices
  - concepts:test-quality
  - practices:productivity
---

# What Developers Using AI Still Need to Know

## The Programming Judgment AI Cannot Supply

## Mark Veltzer

## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## Overview

![title](svg/lectures/ai/what_developers_still_need_to_know/title.svg)

---

## What This Lecture Covers

1. What `AI` changed about programming, and what it did not
1. Evaluating `AI` suggestions: the typical failure modes
1. Correctness you must still own: specs, invariants, edge cases, numbers
1. Data structures, complexity and memory the `AI` will not choose for you
1. Concurrency: where `AI` code is most dangerous
1. Design and architecture decisions you must never delegate
1. Tests strong enough to let the `AI` run wild
1. Debugging what you shipped, and rethinking process beyond Agile

---

## The Shift: From Writing to Judging

- `AI` assistants draft functions, modules, tests and whole designs on demand
- Many developers concluded that the fundamentals no longer matter
- The opposite is true: once code arrives faster than you can read it, the bottleneck moves
- The scarce skill is no longer *producing* code but *judging* it
- Judgment rests entirely on knowledge the `AI` cannot supply for you

---

## Where the Bottleneck Went

![bottleneck](svg/lectures/ai/what_developers_still_need_to_know/writing_vs_judging.svg)

---

## What the AI Actually Is

- A very good pattern completer, trained on a vast amount of existing code
- It produces the *most likely* continuation, not the *correct* one
- It has no model of your requirements, your data, or your production load
- It does not run the code in its head; it predicts what code usually looks like
- It is an excellent drafter and a poor engineer: treat it accordingly

---

## "It Compiles and the Tests Pass" Is Not "It Is Correct"

- The compiler checks syntax and types, not meaning
- The tests check only what someone thought to assert
- When the `AI` wrote both the code and the tests, they share the same blind spots
- Concurrency bugs, performance cliffs and security holes all pass a green build
- Correct means: does what the specification requires, for *every* valid input

---

## The Confidence Trap

- `AI` output is fluent, well formatted, and confidently explained
- Fluency triggers trust: it *reads* like code written by an expert
- Subtly wrong code is more dangerous than obviously wrong code
- The explanation that comes with the code is also generated, and can be equally wrong
- Responsibility for what you merge still lands on you, not on the tool

---

## Skills That Became More Valuable, Not Less

- **Reading code fast and critically**: you now read far more than you write
- **Knowing what correct looks like**: you cannot recognize what you cannot define
- **Smelling a bad design early**: before the `AI` copies it into twenty files
- **Reasoning about cost**: complexity, memory, contention
- **Building safety nets**: tests that make aggressive change safe

---

## Read as a Reviewer, Not an Author

- An author reads to confirm their intent; a reviewer reads to find what is wrong
- Generated code has no author intent to confirm: you must reconstruct it
- Read the diff, not the chat: the explanation is a claim, the code is the fact
- For each function ask: what are the inputs, what must hold, what can go wrong
- If you cannot explain a line, you are not ready to accept it

---

## The Failure Modes of AI Code

![failures](svg/lectures/ai/what_developers_still_need_to_know/failure_modes.svg)

---

## Plausible but Wrong

```python
def is_leap_year(year):
    # Looks right, reads well, passes 2024 and 2023
    return year % 4 == 0

def median(values):
    values.sort()                 # mutates the caller's list
    return values[len(values) // 2]   # wrong for even lengths, crashes on []
```

- Both functions pass the obvious example test
- `is_leap_year(1900)` returns `True`; the century rule was silently dropped
- `median` has three bugs in two lines: side effect, even length, empty input

---

## Hallucinated and Outdated APIs

- The `AI` invents functions that *should* exist: `requests.get_json(url)`, `list.sum()`
- It mixes versions: a parameter renamed two releases ago, a removed module
- It reaches for patterns that were idiomatic years ago and are deprecated now
- Defence: the import must resolve, the call must exist in *your* pinned version
- Check the documentation for anything unfamiliar; a confident name is not evidence

---

## Copied-In Security Holes

```python
# What the AI often suggests
cur.execute(f"SELECT * FROM users WHERE name = '{name}'")

# What it should be
cur.execute("SELECT * FROM users WHERE name = %s", (name,))
```

- Training data is full of insecure examples, so insecure code is *likely* code
- Watch for injection, weak hashing (`md5` for passwords), disabled certificate checks
- Watch for secrets pasted into source and over-broad permissions

---

## Ask: "How Would This Break?"

- Empty input, a single element, the maximum size
- Duplicate keys, negative numbers, zero, `null`
- Unicode, time zones, daylight saving, leap years
- The network is slow, the disk is full, the call is retried
- Two callers at the same time
- Cross-check: ask the `AI` to attack its own code, then verify against the documentation

---

## Keep, Fix, or Throw Away

- **Keep**: you understand it, it fits the design, the tests prove the behaviour
- **Fix**: the idea is right, the details are not; edit it yourself or with a precise prompt
- **Throw away**: wrong approach, wrong structure, or you cannot follow it
- Throwing away is cheap: regeneration is nearly free
- Accepting bad code is expensive: the cost grows with every line built on top of it

---

## Keep the AI on a Short Leash

- Ask for small, verifiable steps, not a thousand-line leap
- One concern per change: a refactor *or* a feature, never both
- Review and commit each step before asking for the next
- A small diff can be read completely; a giant one gets skimmed
- If a step cannot be verified, it is too big

---

## Specify What "Correct" Means

- "Correct" means nothing until the problem is specified precisely
- Valid inputs: types, ranges, sizes, encodings
- Expected outputs, including for errors and edge cases
- Non-functional requirements: latency, memory, thread safety
- The more precise your specification, the better the `AI` output *and* your review

---

## Invariants, Pre-conditions and Post-conditions

```python
def withdraw(account, amount):
    # pre-condition
    assert amount > 0, "amount must be positive"
    assert account.balance >= amount, "insufficient funds"
    before = account.balance
    account.balance -= amount
    # post-condition
    assert account.balance == before - amount
    # invariant of every Account
    assert account.balance >= 0
```

- Stating them forces you to know what the code must do
- They are the questions to ask of every generated function

---

## Boundaries and Off-by-One

```python
# Generated: "return the last n items"
def last_n(items, n):
    return items[-n:]
```

- `last_n([1, 2, 3], 0)` returns `[1, 2, 3]`, not `[]`: `-0` is `0`
- Classic boundary traps: `<` versus `<=`, inclusive versus exclusive ranges
- Fence-post counting: ten posts, nine gaps
- Always test the empty collection, one element, and exactly at the limit

---

## Numeric Pitfalls

```python
>>> 0.1 + 0.2 == 0.3
False
>>> sum([0.1] * 10)
0.9999999999999999
```

- Floating point is binary: never compare with `==`, never store money in a `float`
- Fixed-width integers overflow: `int32` wraps past 2,147,483,647 in C, Java, C#
- `(low + high) / 2` overflows; `low + (high - low) / 2` does not
- Integer division, rounding mode and precision loss on conversion

---

## Trace by Hand, Verify Every Claim

- You must be able to trace a function by hand with a small input
- If you cannot, you cannot tell whether a fix is a fix
- The `AI`'s explanation ("this is O(n log n)", "this is thread-safe") is a claim
- Verify claims with a test, a benchmark, or the documentation, never with another prompt
- Trust nothing you have not checked; check everything you merge

---

## Why the AI Reaches for the Obvious Structure

- It picks what appears most often in examples: a list, a loop, a nested loop
- It does not know your data size, your access pattern, or your hot path
- The obvious structure works perfectly on the ten items in the test
- At production scale, the wrong choice becomes the outage
- Choosing the data structure is a design decision: it is yours

---

## Accidental O(n²)

```python
# Generated: "remove customers who already ordered"
def new_customers(customers, orders):
    ordered = [o.customer_id for o in orders]       # a list
    return [c for c in customers if c.id not in ordered]

# The fix: one character of thinking
def new_customers(customers, orders):
    ordered = {o.customer_id for o in orders}       # a set
    return [c for c in customers if c.id not in ordered]
```

- `in` on a list is a linear scan; inside a loop, the whole thing is quadratic
- Also watch: string concatenation in a loop, `list.pop(0)`, a query per row

---

## Why It Matters at Scale

![complexity](svg/lectures/ai/what_developers_still_need_to_know/complexity_growth.svg)

---

## Choose the Structure from the Access Pattern

| Access pattern | Structure | Typical cost |
| --- | --- | --- |
| Index by position, iterate in order | Array / dynamic array | O(1) index |
| Membership, lookup by key | Hash set / hash map | O(1) average |
| Ordered keys, range queries | Balanced tree, sorted array | O(log n) |
| Always take the smallest | Heap / priority queue | O(log n) |
| Add and remove at both ends | Deque | O(1) |

- Start from the operations the code performs most, not from the syntax that came out

---

## Memory: Invisible to the AI

- Every allocation and copy costs time, and the `AI` copies freely
- Slicing, `list(...)`, and `+` on strings create new objects each time
- Reading a whole file into memory works in the test, fails on a 50 GB log
- Locality: walking contiguous memory is far faster than chasing pointers
- Ask of every loop: what does it allocate, and how many times?

---

## Measure Instead of Guessing

```python
import timeit
setup = "data = list(range(100_000)); s = set(data)"
print(timeit.timeit("99_999 in data", setup=setup, number=1000))
print(timeit.timeit("99_999 in s", setup=setup, number=1000))
```

- Neither you nor the `AI` should guess about performance: measure it
- Benchmark with realistic data sizes, not toy inputs
- Profile before optimizing; the hot spot is rarely where you expect
- Keep a benchmark for any performance claim you rely on

---

## Why Concurrency Is Where AI Code Is Most Dangerous

- Concurrent code that looks right is often wrong
- The bugs depend on timing, so tests usually pass anyway
- Training examples are full of subtly broken locking patterns
- The `AI` cannot see the possible orderings: it predicts text, it does not explore thread schedules
- A passing run proves nothing about a concurrent program

---

## Shared Mutable State

```python
import threading

counter = 0

def worker():
    global counter
    for _ in range(100_000):
        counter += 1      # read, add, write: three steps, not one

threads = [threading.Thread(target=worker) for _ in range(4)]
```

- `counter += 1` is a read-modify-write; two threads can interleave inside it
- The result is sometimes 400,000 and sometimes less: a data race
- Shared *and* mutable is the problem; remove either one and it goes away

---

## A Lost Update, Step by Step

![race](svg/lectures/ai/what_developers_still_need_to_know/race_condition.svg)

---

## Deadlocks, Livelocks and Lock Ordering

- **Deadlock**: thread 1 holds A and waits for B, thread 2 holds B and waits for A
- **Livelock**: both threads keep backing off and retrying, nothing progresses
- **Starvation**: one thread never gets the lock
- The standard cure: a global lock order, always acquire A before B
- Keep critical sections short; never call unknown code while holding a lock

---

## Why "Just Add a Lock" Is Usually Wrong

```python
# Each call is locked, the combination is not
if key not in cache:          # check
    cache[key] = compute(key) # act
```

- Two locked operations in a row are not one atomic operation: check-then-act races
- Too coarse a lock serializes the program and kills the parallelism you wanted
- Too fine a lock misses the invariant that spans several fields
- Ask: *which invariant* does this lock protect, and is every access covered?

---

## Memory Models and Visibility

- Cores have caches; compilers and CPUs reorder instructions
- A write on one core is not automatically visible on another
- A "stop" flag set by one thread may never be seen by the thread polling it
- Language memory models define what is guaranteed: `volatile`, atomics, `std::memory_order`
- Synchronization is about visibility and ordering, not just mutual exclusion

---

## Threads, Processes or Async

| Model | Best for | Main risk |
| --- | --- | --- |
| Threads | Shared-memory parallel work | Races, deadlocks |
| Processes | CPU-bound work, isolation | Serialization and startup cost |
| Async | Many concurrent waits on I/O | A blocking call stalls everything |

- In standard `Python` builds the GIL stops threads speeding up CPU-bound work; the `AI` often forgets
- Calling a blocking function inside `async` code is a frequent generated bug

---

## Making Concurrency Reviewable

- **Immutability**: data that cannot change cannot race
- **Message passing**: queues and channels instead of shared variables
- **Ownership**: one thread owns each piece of state; others ask it
- **Higher-level primitives**: thread pools, futures, concurrent collections
- Prefer designs where correctness can be seen by reading, not argued about

---

## Reviewing AI-Generated Concurrent Code

1. List every piece of state touched by more than one thread
1. For each, find what protects it, and check that *every* access is protected
1. Look for check-then-act and read-modify-write sequences
1. Check lock order and look for calls made while holding a lock
1. Look for blocking calls in async code
1. Stress test with many threads and many iterations, under a race detector if available

---

## Decisions the AI Implements but Must Never Make

- System boundaries: what is a module, a service, a library
- Data model and ownership of data
- Consistency, failure handling and retry strategy
- Dependencies: what you take on and what you refuse
- Trade-offs: simplicity versus flexibility, now versus later
- The `AI` will happily make all of these implicitly, one suggestion at a time

---

## Cohesion and Coupling

- **Cohesion**: things that change together live together
- **Coupling**: how much one part must know about another
- The `AI` does not feel either; it solves the local prompt
- It reaches across boundaries because the code it needs is visible in the context
- Every generated shortcut across a boundary is a small, permanent coupling

---

## Abstractions: Good, Leaky, Premature

- **Good**: hides a decision that may change, with a small, stable interface
- **Leaky**: callers must know what is underneath to use it correctly
- **Premature**: an interface with one implementation and no second in sight
- The `AI` tends to produce both extremes: copy-paste duplication or factory-of-factories
- Design patterns are vocabulary for discussing design, not goals to collect

---

## How Generated Code Rots an Architecture

- Each suggestion is locally reasonable and globally inconsistent
- Three ways to do logging, two error-handling styles, four date libraries
- Duplicated logic drifts apart until the copies disagree
- Naming loses consistency, so the code stops explaining itself
- No single change is the problem; the sum of them is

---

## Make Design Intent Explicit

```markdown
# ARCHITECTURE.md (read by every AI session)
- Layers: api -> service -> repository. Never call repository from api.
- Errors: raise domain exceptions; only the api layer maps them to HTTP.
- Time: always timezone-aware UTC, via the clock module.
- No new dependencies without discussion.
```

- Write down the decisions so the `AI` stays inside them
- Enforce what you can mechanically: linters, import rules, architecture tests
- Review for design fit, not only for local correctness

---

## Tests Are the Leash That Lets You Let Go

- You can trust `AI` refactoring exactly as far as your tests reach
- With a strong suite, you can let the `AI` rewrite whole modules
- With a weak suite, every change is a gamble you cannot evaluate
- Tests turn "it looks right" into "it is proven to behave the same"
- The workflow: lock behaviour with tests, then let the `AI` change code freely

---

## The Rewrite Loop

![leash](svg/lectures/ai/what_developers_still_need_to_know/tests_as_leash.svg)

---

## Assert Behaviour, Not Implementation

```python
# Brittle: breaks on any refactor, proves little
def test_total_calls_helper(mocker):
    spy = mocker.spy(Cart, "_sum_items")
    Cart([Item(price=100)]).total()
    spy.assert_called_once()

# Robust: survives any correct rewrite
def test_total_applies_discount():
    cart = Cart([Item(price=100)], discount=0.1)
    assert cart.total() == 90
```

- Tests that check *how* block refactoring; tests that check *what* enable it

---

## Coverage That Means Something

- Coverage tells you which lines ran, not which behaviours were checked
- A test with no meaningful assertion gives full coverage and zero protection
- `AI`-written tests often assert what the code *does*, not what it *should* do
- Mutation testing asks the real question: if I break the code, does a test fail?
- Aim for strong assertions on important behaviour, not for a percentage

---

## Characterization Tests

- Before letting the `AI` touch legacy code, pin down what it does today
- Feed real inputs, record the outputs, assert those outputs exactly
- They document current behaviour, including bugs you have not decided to fix
- Now the `AI` can restructure freely: any behaviour change shows up red
- Once the refactor is done, replace them with intent-revealing tests

---

## Property-Based Testing

```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sort_properties(xs):
    result = my_sort(xs)
    assert len(result) == len(xs)
    assert all(a <= b for a, b in zip(result, result[1:]))
    assert sorted(xs) == result
```

- State properties that must hold for *all* inputs; the tool searches for counterexamples
- Finds exactly the empty, huge, negative and duplicate cases the `AI` skipped

---

## Don't Let the AI Grade Its Own Homework

- Tests written from the code confirm the code, bugs included
- Write or approve the test *first*, from the specification
- When the `AI` writes tests, review the assertions, not the setup
- Never accept "fixed the failing test" when the fix changed the assertion
- Keep tests fast, deterministic and isolated: they are the precondition for aggressive change

---

## Debugging Code You Did Not Write

- When it breaks in production, you have to fix it, not the `AI`
- Read the stack trace from the bottom frame of *your* code upward
- Use the scientific method: observe, hypothesize, predict, test, repeat
- Reproduce first, with a failing test that captures the bug
- Bisect: `git bisect` finds the change, logging and a debugger find the line
- Avoid the "I don't know why it works" codebase: understand code before you own it

---

## Why Agile Ceremony Existed

- Agile was a response to slow, expensive change
- Short iterations, estimates and standups manage the cost of building the wrong thing
- When a working draft is cheap and immediate, much of that machinery loses its purpose
- Story points and estimation theatre measure effort that the `AI` now absorbs
- The scarce resources are now direction, design and verification

---

## What to Retire, What to Keep

- **Retire**: estimation theatre, ticket churn, status meetings that read the board aloud
- **Keep**: close contact with users, small increments, retrospectives that change things
- **Measure**: working, tested software as the unit of progress, not closed tickets
- **Protect**: design ownership and review time, the new bottleneck
- Accelerate the mechanics; keep humans in charge of direction

---

## A Working Model for AI-Era Teams

![loop](svg/lectures/ai/what_developers_still_need_to_know/ai_era_loop.svg)

---

## Summary

- `AI` made writing code cheap; judging code is now the core skill
- Review generated code as a suspicious reviewer: plausible is not correct
- Own correctness, complexity, memory and concurrency: the `AI` cannot see them
- Make the design decisions yourself and write them down so the `AI` follows them
- Build tests strong enough that the `AI` can rewrite freely, and never let it grade itself
- Reshape the process around tight loops: specify, generate, verify, integrate
