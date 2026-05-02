---
tags:
  - concepts:design-patterns
  - concepts:structural-patterns
level: intermediate
category: design-patterns
audience:
  - audiences:developers

---
# Structural Design Patterns

---
## What This Chapter Covers

- Seven patterns for *composing* classes and objects
- Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy
- Each: intent, structure, code, when to use, trade-offs
- Two patterns get longer treatment because they appear most often

---
## Why Structural Patterns

- They answer: how do classes and objects fit together?
- The goal is flexibility: substitute parts, layer behaviour, expose simpler interfaces
- They keep dependencies pointing the right way
- Most are about indirection — adding a layer to gain flexibility

---
## Patterns at a Glance

![structural_patterns](svg/courses/design_patterns/design-patterns/03_structural_design_patterns/structural_patterns.svg)

---
## Compared

![structural_compared](svg/courses/design_patterns/design-patterns/03_structural_design_patterns/structural_compared.svg)

---
## Adapter

- *Intent*: convert one interface to another expected by clients
- Used when an existing class doesn't match what you need
- Wrap the legacy class; expose the desired interface
- Two flavours: object adapter (composition) and class adapter (inheritance)
- The "USB-to-HDMI" of object design

---
## Adapter in Code

```python
class OldPrinter:
    def print_text(self, txt): ...

class TargetPrinter(ABC):
    @abstractmethod
    def render(self, document): ...

class PrinterAdapter(TargetPrinter):
    def __init__(self, old): self._old = old
    def render(self, document):
        self._old.print_text(document.to_string())
```

- Client code uses `TargetPrinter`
- Adapter forwards calls to `OldPrinter`'s API

---
## Bridge

- *Intent*: decouple an abstraction from its implementation so the two can vary independently
- Without Bridge: every combination is its own class (RedCircle, BlueCircle, RedSquare, BlueSquare)
- With Bridge: Shape *has-a* Renderer; multiply by adding either independently
- Common in graphics and persistence layers
- Looks like Strategy at small scale; differs in intent (varying *implementation*, not *algorithm*)

---
## Composite

- *Intent*: treat individual objects and compositions of objects uniformly
- A `File` and a `Directory` both implement `Filesystem`
- A `Directory` contains `Filesystem` objects (which may be Files or other Directories)
- Recursive operations like `size()` work on both transparently
- Heavy use in UI trees, file systems, organisation hierarchies

---
## Composite in Code

```python
class Component(ABC):
    @abstractmethod
    def size(self): ...

class File(Component):
    def __init__(self, bytes): self._bytes = bytes
    def size(self): return self._bytes

class Directory(Component):
    def __init__(self): self._children = []
    def add(self, c): self._children.append(c)
    def size(self): return sum(c.size() for c in self._children)
```

- `Directory.size()` recurses through children
- Clients work with `Component` regardless of leaf or composite

---
## Decorator

- *Intent*: add responsibility to an object dynamically without changing its class
- Wrap an object in another object that implements the same interface
- The wrapper adds behaviour before / after delegating to the wrapped object
- Stack wrappers as deep as you need
- Java I/O is the classic: `BufferedReader(new InputStreamReader(new FileInputStream(...)))`

---
## Decorator in Code

```python
class Notifier(ABC):
    @abstractmethod
    def send(self, msg): ...

class EmailNotifier(Notifier):
    def send(self, msg): print("email:", msg)

class WithTimestamp(Notifier):
    def __init__(self, inner): self._inner = inner
    def send(self, msg):
        self._inner.send(f"[{datetime.now()}] {msg}")

n = WithTimestamp(EmailNotifier())
n.send("hello")  # email: [2026-...] hello
```

- Each decorator implements `Notifier` and *holds* a `Notifier`
- Stack them: `WithLogging(WithTimestamp(EmailNotifier()))`

---
## Decorator vs Inheritance

- Decorator adds behaviour at *runtime*; inheritance fixes it at compile time
- Decorator stacks; inheritance gives you a single chain
- A user can pick which decorators to apply for *this* instance
- Less explosion of subclasses than `EmailWithLogging`, `EmailWithTimestamp`, `EmailWithBoth`
- Trade-off: many small classes that look similar

---
## Facade

- *Intent*: provide a unified, simpler interface to a complex subsystem
- The subsystem is still there; the facade just makes the common case easy
- Library APIs almost always have a facade for the 90% case
- Doesn't restrict access to the full subsystem — just simplifies the obvious path
- One of the easiest patterns to apply correctly

---
## Facade in Code

```python
class HomeTheaterFacade:
    def __init__(self, amp, dvd, screen, lights):
        self._amp, self._dvd, self._screen, self._lights = amp, dvd, screen, lights

    def watch_movie(self, movie):
        self._lights.dim(10)
        self._screen.down()
        self._amp.on()
        self._amp.set_volume(5)
        self._dvd.play(movie)
```

- Client calls `theater.watch_movie("Dune")`
- Doesn't have to know about all the components

---
## Flyweight

- *Intent*: share many small objects efficiently by separating *intrinsic* (shared) from *extrinsic* (per-instance) state
- Classic example: a text editor with millions of character objects — share the font/glyph data
- Intrinsic state lives in the flyweight; extrinsic state is passed in per call
- Heavy memory savings; complex to apply correctly
- Modern systems often achieve the same with object pools or interning

---
## Proxy

- *Intent*: provide a placeholder for another object to control access
- Same interface as the real object; clients can't tell the difference
- Common variants:
    - **Virtual Proxy**: defers expensive creation until needed
    - **Protection Proxy**: enforces access permissions
    - **Remote Proxy**: forwards calls across a network (RPC clients)
    - **Caching Proxy**: caches results of slow calls

---
## Proxy in Code

```python
class Image:
    def display(self): ...

class RealImage(Image):
    def __init__(self, filename):
        self._filename = filename
        self._load_from_disk()
    def display(self): print("show", self._filename)

class ImageProxy(Image):
    def __init__(self, filename):
        self._filename = filename
        self._real = None
    def display(self):
        if self._real is None:
            self._real = RealImage(self._filename)
        self._real.display()
```

- Construction of `ImageProxy` is cheap
- Disk read happens only on first `display()`

---
## Choosing Among Structural Patterns

- Wrong-shaped interface &#8594; Adapter
- Two dimensions of variation &#8594; Bridge
- Tree of like objects &#8594; Composite
- Optional behaviours stacked &#8594; Decorator
- Simpler entry point to a subsystem &#8594; Facade
- Many small shared objects &#8594; Flyweight
- Controlled access to an object &#8594; Proxy

---
## Patterns vs Composition

- All structural patterns *use* composition
- The pattern names a *purpose* for the composition
- Without the pattern names: "I'm wrapping a class" gives no hint *why*
- With the names: Adapter tells your reader the wrap is about interface translation
- Vocabulary buys you precise communication

---
## Common Mistakes

- Adapter chain wrapping an Adapter that wraps an Adapter — fix the underlying interface
- Decorator chain so deep nobody can see what's actually happening
- Composite where the leaves and branches need *different* APIs but inherit a shared one anyway
- Facade that's so thin it's redundant; the original API was already fine
- Proxy that adds latency for caching but the underlying call was already fast
