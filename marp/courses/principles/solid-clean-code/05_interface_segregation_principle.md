---
tags:
  - concepts:solid
  - concepts:isp
level: intermediate
category: design-patterns
audience:
  - audiences:developers

---

# Interface Segregation Principle (ISP)

---

## What This Chapter Covers

- A precise statement of ISP
- A worked example: the Worker / Robot problem
- Role-based interfaces
- ISP and testing
- Trade-offs

---

## The Principle, Stated Carefully

- "Clients should not be forced to depend on methods they do not use"
- A *fat* interface forces every implementer to fulfil every method
- Clients are coupled to methods they never call
- A change to one of those methods rebuilds and re-tests every client
- Solution: many small interfaces, each focused on a *role*

---

## Fat vs Split

![isp_split](svg/courses/principles/solid-clean-code/05_interface_segregation_principle/isp_split.svg)

---

## A Smelly Interface

```java
public interface Worker {
    void work();
    void eat();
    void sleep();
}

public class Human implements Worker { ... }
public class Robot implements Worker {
    public void eat()   { throw new UnsupportedOperationException(); }
    public void sleep() { throw new UnsupportedOperationException(); }
}
```

- Robot is forced to implement methods that don't apply
- Liskov violation lurking — calling eat on Robot crashes
- Adding `bathe()` later affects Robot for no reason

---

## Refactored With Small Interfaces

```java
public interface Workable { void work(); }
public interface Feedable  { void eat(); }
public interface Restable  { void sleep(); }

public class Human implements Workable, Feedable, Restable { ... }
public class Robot implements Workable { ... }
```

- Each implementer takes only what applies
- No more no-op or throwing methods
- Each interface evolves independently

---

## Role-Based Interfaces

- Define interfaces by *what the client needs*, not by *what the implementer is*
- "Comparable" — needed by sort
- "Iterable" — needed by for-each loops
- "Closeable" — needed by try-with-resources
- Each interface is a *role* an object can play

---

## The Client Decides the Shape

- An interface should be designed from the *consumer*'s perspective
- "What methods does this consumer actually need?"
- That set becomes the interface
- The implementer may also satisfy other interfaces
- This inverts the usual instinct of "design the interface around the implementation"

---

## A Real-World Example

```python
class Repository(Protocol):
    def get(self, id): ...
    def save(self, obj): ...
    def delete(self, id): ...
    def search(self, query): ...
    def export_csv(self): ...
    def archive(self): ...
```

- Some consumers only `get`/`save`
- Some only `search`
- Some only `archive`
- One fat interface vs three focused ones — pick consumer-by-consumer

---

## After ISP

```python
class Reader(Protocol):
    def get(self, id): ...
    def search(self, q): ...

class Writer(Protocol):
    def save(self, obj): ...
    def delete(self, id): ...

class Archiver(Protocol):
    def archive(self): ...
    def export_csv(self): ...
```

- Most clients depend on one of these, not all
- Adding archive features only affects archive consumers

---

## ISP and Testing

- Smaller interfaces &#8594; smaller mocks
- A test that only needs `Reader` doesn't have to stub every method of a fat repository
- Less coupling between tests and implementation details
- Less brittle tests when the implementation evolves

---

## ISP Across Boundaries

- Same idea applies to API endpoints
- Don't return everything every consumer might want — different endpoints for different needs
- Same idea applies to module exports
- Same idea applies to event payloads — don't include 50 fields for one consumer of 3

---

## ISP and OCP

- Small interfaces are easier to keep stable (closed)
- New behaviour goes into a new small interface
- Existing consumers aren't affected
- The combination scales well in growing codebases

---

## Trade-offs

- Many small interfaces &#8594; more files, more navigation
- Some teams prefer one interface and accept the no-op methods
- Pragmatism: split when the no-op pattern actually appears, not preemptively
- Don't fragment so much that you can't see the whole picture

---

## When NOT to Apply

- Truly cohesive interfaces where every method is used together
- Internal helper interfaces that have one consumer
- Domain types that *should* expose all their behaviour
- The split would create interfaces nobody implements separately

---

## Recognising Violations

- Implementations with throwing or no-op methods
- Test mocks that need to stub 15 methods to test 1
- An interface change forces a recompile of unrelated clients
- Interface name needs an "And" or "All" to be honest

---

## A Refactoring Recipe

- List every method on the fat interface
- For each consumer, list which methods it actually uses
- Cluster methods by consumer
- Create one interface per cluster
- Original implementer implements all of them — clients depend on one each

---

## Common Mistakes

- One interface per method (over-application)
- Splitting along *what could change* rather than *what consumers need*
- Forgetting to actually update the consumers to depend on the small interfaces
- Naming small interfaces by their implementer rather than their role (`HumanWorkable` instead of `Workable`)
