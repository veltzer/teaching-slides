---
tags:
  - architecture:hexagonal
level: intermediate
category: architecture
audience:
  - audiences:architects

---

# Ports and Adapters (Hexagonal)

---

## Driving vs Driven

![driving_vs_driven](svg/courses/architecting/clean-and-hexagonal-architecture/05_ports_and_adapters_hexagonal_architecture/driving_vs_driven.svg)

---

## What This Chapter Covers

- Hexagonal architecture origins
- Ports and adapters
- Driving vs driven
- Comparison with Clean Architecture
- A worked example

---

## Hexagon

![hexagon](svg/courses/architecting/clean-and-hexagonal-architecture/05_ports_and_adapters_hexagonal_architecture/hexagon.svg)

---

## Origins

- Coined by Alistair Cockburn (2005)
- Originally called "Ports and Adapters"
- Same idea, different vocabulary, different visualisation
- Often used interchangeably with Clean Architecture
- Both push for: domain isolation

---

## Ports

- Interfaces defined by the application
- "Ways into and out of the app"
- Two kinds: driving (in) and driven (out)

---

## Adapters

- Implementations of ports
- Bridge to the outside world
- Many adapters per port possible

---

## Driving (Primary) Ports

- Triggers an action
- HTTP controller, CLI, message consumer
- The "way in"
- Calls the application

---

## Driven (Secondary) Ports

- Application calls out
- Database, external API, mailer
- The "way out"
- Application defines; adapter implements

---

## The Hexagon

- Application at the centre
- Ports on the edges
- Adapters around the outside
- Hexagon shape: arbitrary; emphasises symmetry

---

## Hexagonal vs Clean

- Clean: layered (rings)
- Hexagonal: ports on the boundary (hexagon)
- Same dependency rule
- Same testability benefits
- Mostly: visual / vocabulary differences

---

## Worked Example

```python
# Driving port
class PlaceOrderPort(ABC):
    @abstractmethod
    def place_order(self, cmd: PlaceOrderCommand): ...

# Application
class OrderService(PlaceOrderPort):
    def __init__(self, repo: OrderRepositoryPort, ...):
        ...
    def place_order(self, cmd):
        ...

# Driving adapter
class HttpOrderController:
    def __init__(self, port: PlaceOrderPort):
        ...
    def post_order(self, request):
        cmd = PlaceOrderCommand.from_request(request)
        self.port.place_order(cmd)
```

---

## Multiple Driving Adapters

- HTTP, gRPC, CLI, scheduled job
- All call the same use case via the same port
- "Place order" works the same regardless of caller
- Pure refactoring exercise to add a new caller

---

## Multiple Driven Adapters

- Postgres in prod, in-memory in test, snapshot for migration
- Test doubles are first-class
- Easy to swap implementations

---

## Trade-Offs

- More files, more abstraction
- Worth it for: long-lived domain, multiple delivery mechanisms
- Overkill for: simple CRUD

---

## Common Hexagonal Mistakes

- Ports defined outside the application (lose ownership)
- Adapters that contain business logic
- One mega-port (each is a focused interface)
- Skipping the abstraction; "we'll add it later"

---

## When To Adopt

- Domain logic with longevity
- Multiple input or output channels
- TDD-driven team
- Clear domain to model

---

## When To Skip

- One-shot scripts
- Pure CRUD
- Team without discipline
- Match the architecture to the longevity
